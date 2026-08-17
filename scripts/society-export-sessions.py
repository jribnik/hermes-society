#!/usr/bin/env python3
"""
Export Hermes session history to the hermes-society-sessions GitHub repo.

Runs as a no_agent cron job. Exports society agent sessions (source='cron')
from the last 7 days as markdown transcripts, commits them to the repo at
sessions/transcripts/YYYY/MM/DD-*.md, and pushes.

Usage:
  python3 society-export-sessions.py           # normal run (last 7 days)
  python3 society-export-sessions.py --all      # export ALL sessions
  python3 society-export-sessions.py --days 3   # last N days
"""

import os
import sys
import json
import sqlite3
import tempfile
import subprocess
from pathlib import Path
from datetime import datetime, timezone
from collections import defaultdict

HOME = Path.home()
SESSIONS_DB = HOME / '.hermes' / 'state.db'
PROFILES_DIR = HOME / '.hermes' / 'profiles'
# Society agents migrated to Slack each run in their own HERMES_HOME profile
# with a separate state.db, so the export must aggregate those too.
SOCIETY_PROFILES = ['society-archivist', 'society-advocate', 'society-synthesizer']
REPO_DIR = HOME / 'hermes-society-sessions'
EXPORT_BASE = REPO_DIR / 'transcripts'
GIT_EMAIL = "hermes-society@nousresearch.com"
GIT_NAME = "Hermes Society Bot"

# ---- Helpers ----

_DBS = {}

def get_db(db_path):
    """Return a cached row-factory connection for the given DB path."""
    key = str(db_path)
    conn = _DBS.get(key)
    if conn is None:
        conn = sqlite3.connect(str(db_path))
        conn.row_factory = sqlite3.Row
        _DBS[key] = conn
    return conn

def iter_homes():
    """Yield (label, db_path, source_filter) for every home to export from.

    - main home: the original cron society (source='cron' only).
    - each society profile home: the migrated Slack agent (all sources).
    """
    yield ('main', SESSIONS_DB, 'cron')
    for prof in SOCIETY_PROFILES:
        db = PROFILES_DIR / prof / 'state.db'
        if db.exists():
            yield (prof.replace('society-', ''), db, None)

def log(msg):
    print(f"[session-export] {msg}")

def run(cmd, cwd=None, timeout=60):
    """Run a shell command, return (returncode, stdout, stderr)."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=cwd)
        return r.returncode, r.stdout.strip(), r.stderr.strip()
    except subprocess.TimeoutExpired:
        return -1, "", "timeout"
    except FileNotFoundError:
        return -2, "", "command not found"

def get_gh_token():
    """Try to get a GitHub PAT for public repos."""
    # Check env
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        return token
    # Check gh CLI
    rc, out, _ = run(["gh", "auth", "token"])
    if rc == 0 and out:
        return out
    return None

def needs_git_setup():
    """Check if git user config is set in the repo scope."""
    rc, _, _ = run(["git", "config", "user.email"], cwd=str(REPO_DIR))
    return rc != 0

def setup_git():
    """Set git user for this repo."""
    run(["git", "config", "user.email", GIT_EMAIL], cwd=str(REPO_DIR))
    run(["git", "config", "user.name", GIT_NAME], cwd=str(REPO_DIR))

# ---- Query sessions ----

def _rows_to_sessions(db, label, rows):
    """Attach last-message timestamp + home/db provenance to each session row."""
    out = []
    for row in rows:
        last_msg = db.execute(
            "SELECT MAX(timestamp) as last_ts FROM messages WHERE session_id = ?",
            (row['id'],)).fetchone()
        last_ts = last_msg['last_ts'] if last_msg and last_msg['last_ts'] else row['started_at']
        out.append({
            'id': row['id'],
            'source': row['source'],
            'title': row['title'] or '',
            'started_at': last_ts,
            'message_count': row['actual_msgs'] or 0,
            'home': label,
            'db': db,
        })
    return out

def get_session_ids(db, label, source_filter, days_back=7):
    """Get sessions from the last N days for one home."""
    cutoff = datetime.now(timezone.utc).timestamp() - (days_back * 86400)
    where = "WHERE s.started_at >= ?"
    params = [cutoff]
    if source_filter:
        where += " AND s.source = ?"
        params.append(source_filter)
    rows = db.execute(f"""
        SELECT s.id, s.source, s.title, s.started_at, s.message_count,
               COUNT(m.id) as actual_msgs
        FROM sessions s
        LEFT JOIN messages m ON m.session_id = s.id
        {where}
        GROUP BY s.id
        ORDER BY s.started_at DESC
    """, params).fetchall()
    return _rows_to_sessions(db, label, rows)

def get_all_session_ids(db, label, source_filter=None):
    """Get ALL sessions for one home."""
    where = "WHERE s.source = ?" if source_filter else ""
    params = [source_filter] if source_filter else []
    rows = db.execute(f"""
        SELECT s.id, s.source, s.title, s.started_at, s.message_count,
               COUNT(m.id) as actual_msgs
        FROM sessions s
        LEFT JOIN messages m ON m.session_id = s.id
        {where}
        GROUP BY s.id
        ORDER BY s.started_at DESC
    """, params).fetchall()
    return _rows_to_sessions(db, label, rows)

def get_messages(db, session_id):
    """Get all messages for a session from its home DB."""
    cursor = db.execute("""
        SELECT role, content, timestamp, tool_name, tool_call_id,
               tool_calls, finish_reason, token_count
        FROM messages
        WHERE session_id = ?
        ORDER BY timestamp ASC, id ASC
    """, (session_id,))
    return cursor.fetchall()

# Sensitive patterns to redact — keep this list updated
SENSITIVE_PATTERNS = [
    # Private keys (PEM blocks) — match first, before narrower patterns
    (r'-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----',
     '***REDACTED PRIVATE KEY***'),
    # GitHub tokens
    (r'gh[ops]_[a-zA-Z0-9_]{10,}', 'ghp_***REDACTED***'),
    (r'github_pat_[a-zA-Z0-9_]{20,}', 'github_pat_***REDACTED***'),
    (r'ghu_[a-zA-Z0-9_]{10,}', 'ghu_***REDACTED***'),
    # Anthropic / OpenAI / generic sk- keys (specific before generic)
    (r'sk-ant-[a-zA-Z0-9_\-]{20,}', 'sk-ant-***REDACTED***'),
    (r'sk-[a-zA-Z0-9]{20,}', 'sk-***REDACTED***'),
    # AWS access-key IDs and secret keys
    (r'AKIA[0-9A-Z]{16}', 'AKIA***REDACTED***'),
    (r'(aws_secret_access_key|aws_secret)["\']?\s*[=:]\s*["\']?[A-Za-z0-9/+=]{40}',
     r'\1=***REDACTED***'),
    # Google API keys
    (r'AIza[0-9A-Za-z_\-]{35}', 'AIza***REDACTED***'),
    # Slack tokens (xoxb, xoxp, xapp, xoxa, xoxr, xoxs)
    (r'xox[baprs]-[a-zA-Z0-9\-]{10,}', 'xox*-***REDACTED***'),
    # Passwords embedded in URLs (scheme://user:PASS@host)
    (r'([a-zA-Z][a-zA-Z0-9+.\-]*://[^\s:/@]+):[^\s:/@]+@', r'\1:***REDACTED***@'),
    # api_key = ... / apikey: ...
    (r'(api[_-]?key|apikey)["\']?\s*[=:]\s*["\']?[a-zA-Z0-9_\-]{16,}', r'\1=***REDACTED***'),
    # Bearer tokens
    (r'Bearer\s+[a-zA-Z0-9_\-\.]{20,}', 'Bearer ***REDACTED***'),
    # Authorization headers
    (r'Authorization:\s*[a-zA-Z0-9_\-\.]{10,}', 'Authorization: ***REDACTED***'),
]

def sanitize_content(text):
    """Remove sensitive credentials from text before exporting."""
    if not text:
        return text
    import re
    result = text
    for pattern, replacement in SENSITIVE_PATTERNS:
        result = re.sub(pattern, replacement, result)
    return result

def render_session_to_md(session):
    """Render a session's messages into a markdown transcript."""
    sid = session['id']
    msgs = session['messages']
    
    lines = []
    lines.append(f"# Session: {sanitize_content(session['title'] or sid)}")
    lines.append(f"")
    lines.append(f"- **Session ID:** `{sid}`")
    lines.append(f"- **Source:** {session['source'] or 'unknown'}")
    lines.append(f"- **Messages:** {len(msgs)}")
    if msgs:
        first_ts = datetime.fromtimestamp(msgs[0]['timestamp'], tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        last_ts = datetime.fromtimestamp(msgs[-1]['timestamp'], tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
        lines.append(f"- **Started:** {first_ts}")
        lines.append(f"- **Ended:** {last_ts}")
    lines.append(f"")
    lines.append(f"---")
    lines.append(f"")
    
    for msg in msgs:
        role = msg['role']
        ts = datetime.fromtimestamp(msg['timestamp'], tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        content = sanitize_content(msg.get('content', '') or "")
        
        if role == 'system':
            lines.append(f"### 🖥 System ({ts})")
        elif role == 'user':
            lines.append(f"### 👤 User ({ts})")
        elif role == 'assistant':
            lines.append(f"### 🤖 Assistant ({ts})")
            
            # Show tool calls if present
            if msg.get('tool_calls'):
                try:
                    tool_calls = json.loads(msg['tool_calls'])
                    if isinstance(tool_calls, list):
                        for tc in tool_calls:
                            fn = tc.get('function', {})
                            name = fn.get('name', '?')
                            args = fn.get('arguments', '{}')
                            if isinstance(args, str):
                                    try:
                                        args = json.loads(args)
                                    except json.JSONDecodeError:
                                        pass
                            # Sanitize args
                            args_str = json.dumps(args, indent=2)
                            args_str = sanitize_content(args_str)
                            lines.append(f"")
                            lines.append(f"  🔧 **Tool: `{name}`**")
                            lines.append(f"  ```json")
                            lines.append(f"  {args_str}")
                            lines.append(f"  ```")
                    elif isinstance(tool_calls, dict):
                        # Legacy format
                        fn = tool_calls.get('function', {})
                        name = fn.get('name', '?')
                        lines.append(f"")
                        lines.append(f"  🔧 **Tool: `{name}`**")
                except (json.JSONDecodeError, TypeError):
                    lines.append(f"")
                    lines.append(f"  🔧 **Tool calls:** (raw)")
                    lines.append(f"  ```")
                    lines.append(f"  {msg['tool_calls']}")
                    lines.append(f"  ```")
            
        elif role == 'tool':
            tool_name = msg.get('tool_name') or msg.get('tool_call_id', '?')
            lines.append(f"### 🔧 Tool Result (`{tool_name}`) ({ts})")
        else:
            lines.append(f"### {role.capitalize()} ({ts})")
        
        if content.strip():
            # Check if content is already markdown-like or has code blocks
            has_code = "```" in content
            is_long = len(content) > 200
            
            if has_code or is_long:
                lines.append(f"")
                lines.append(content)
            else:
                lines.append(f"")
                lines.append(f"> {content}")
        else:
            lines.append(f"")
            lines.append(f"*(empty)*")
        
        lines.append(f"")
    
    return "\n".join(lines)

# ---- Git operations ----

def clone_or_pull_repo(token):
    """Clone the repo if needed, or pull latest."""
    if REPO_DIR.exists() and (REPO_DIR / '.git').exists():
        log(f"Repo exists at {REPO_DIR}, pulling...")
        rc, out, err = run(["git", "pull", "--rebase"], cwd=str(REPO_DIR))
        if rc != 0:
            log(f"Warning: git pull failed: {err}")
        return True
    
    log(f"Cloning repo...")
    parent = REPO_DIR.parent
    parent.mkdir(parents=True, exist_ok=True)
    
    # Remove existing dir if it's a stale file
    if REPO_DIR.exists():
        import shutil
        shutil.rmtree(str(REPO_DIR))
    
    # Use SSH URL (assumes SSH key is configured for GitHub)
    repo_url = "git@github.com:jribnik/hermes-society-sessions.git"
    rc, out, err = run(["git", "clone", repo_url, str(REPO_DIR)])
    
    if rc != 0:
        log(f"Failed to clone repo: {err}")
        return False
    return True

def export_and_push(session_ids, token):
    """Export sessions to markdown files, commit, and push."""
    EXPORT_BASE.mkdir(parents=True, exist_ok=True)
    
    # Track what we've written per date
    written_files = []
    total_sessions = len(session_ids)
    
    for i, sess in enumerate(session_ids):
        msgs = get_messages(sess['db'], sess['id'])
        if not msgs:
            continue
        
        sess['messages'] = [dict(m) for m in msgs]
        
        # Determine date from first message timestamp
        first_ts = datetime.fromtimestamp(msgs[0]['timestamp'], tz=timezone.utc)
        date_prefix = first_ts.strftime("%Y-%m-%d")
        year = first_ts.strftime("%Y")
        month = first_ts.strftime("%m")
        
        # Sanitize title for filename
        title_slug = sess.get('title', sess['id'])
        # Remove non-alphanumeric chars (except hyphens/underscores), truncate
        safe_title = "".join(c if c.isalnum() or c in '-_' else '_' for c in title_slug[:40]).strip('_') or 'untitled'
        
        date_dir = EXPORT_BASE / year / month
        date_dir.mkdir(parents=True, exist_ok=True)
        
        # Prefix the agent/home into the filename for the migrated profiles so
        # they don't collide with the main home and their provenance is clear.
        home = sess.get('home', 'main')
        prefix = "" if home == 'main' else f"{home}_"
        filename = f"{date_prefix}_{prefix}{safe_title}_{sess['id'][:8]}.md"
        filepath = date_dir / filename
        
        # Skip if already exists and same content (but we overwrite anyway on daily runs)
        markdown = render_session_to_md(sess)
        filepath.write_text(markdown, encoding='utf-8')
        written_files.append(filepath)
        
        if (i + 1) % 10 == 0:
            log(f"  Exported {i+1}/{total_sessions}...")
    
    if not written_files:
        log("No sessions to export.")
        return True
    
    log(f"Exported {len(written_files)} session transcripts.")
    
    # Also update the index
    write_session_index(written_files, session_ids)
    
    # Also add unreleased changelog entry
    update_changelog(written_files, session_ids)
    
    # Git commit and push
    run(["git", "add", "-A"], cwd=str(REPO_DIR))
    
    rc, out, err = run(["git", "diff", "--cached", "--quiet"], cwd=str(REPO_DIR))
    if rc == 0:
        log("No changes to commit.")
        return True
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    count = len(written_files)
    rc, out, err = run([
        "git", "commit", "-m", f"session-export: {count} transcripts from {today}",
        "-m", f"Automated export of {count} session transcripts ({total_sessions} sessions queried)."
    ], cwd=str(REPO_DIR))
    
    if rc != 0:
        log(f"Commit failed: {err}")
        return False
    
    rc, out, err = run(["git", "push"], cwd=str(REPO_DIR), timeout=120)
    if rc != 0:
        log(f"Push failed: {err}")
        return False
    
    log(f"Successfully pushed {count} transcripts to GitHub.")
    return True

def update_changelog(written_files, all_sessions):
    """Add an 'Unreleased' entry to the changelog for this export run.
    Deduplicates by date so we don't pile up duplicate entries."""
    changelog_path = REPO_DIR / 'CHANGELOG.md'
    
    if not changelog_path.exists():
        log("No CHANGELOG.md found, skipping changelog update.")
        return
    
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # Count by source
    by_source = defaultdict(int)
    for sess in all_sessions:
        by_source[sess.get('source', 'unknown')] += 1
    
    source_summary = ", ".join(f"{k}={v}" for k, v in sorted(by_source.items()))
    
    # Check if there's already an Unreleased entry for today (dedup)
    existing = changelog_path.read_text()
    today_header = f"### Session export ({today})"
    if today_header in existing:
        log(f"Changelog entry for {today} already exists, skipping.")
        return
    
    entry = f"""
### Session export ({today})
- **{len(written_files)} transcripts** committed ({source_summary})
"""
    
    # Insert after "## [Unreleased]" line
    unreleased_marker = "## [Unreleased]\n"
    if unreleased_marker in existing:
        idx = existing.index(unreleased_marker) + len(unreleased_marker)
        new_content = existing[:idx] + entry + existing[idx:]
        changelog_path.write_text(new_content)
        log(f"Added changelog entry for {today} ({len(written_files)} transcripts).")
    else:
        log("No [Unreleased] section found in CHANGELOG.md, skipping.")

def write_session_index(written_files, all_sessions):
    """Write/update a session index page for easy navigation."""
    index_file = EXPORT_BASE / "README.md"
    
    lines = ["# Session Transcripts", "", "Auto-exported from Hermes session database.", "", "## By Date", ""]
    
    # Group by year/month — scan the FULL tree, not just this run's files, so
    # the index reflects every transcript on disk, not only the recent batch.
    by_year_month = defaultdict(list)
    for fp in EXPORT_BASE.rglob("*.md"):
        if fp.name == "README.md":
            continue
        rel = fp.relative_to(EXPORT_BASE)
        if len(rel.parts) != 3:  # expect YYYY/MM/<file>.md
            continue
        year, month = rel.parts[0], rel.parts[1]
        by_year_month[f"{year}/{month}"].append(rel.name)
    
    for ym in sorted(by_year_month.keys(), reverse=True):
        lines.append(f"### {ym.replace('/', '-')}")
        for fname in sorted(by_year_month[ym], reverse=True):
            lines.append(f"- [{fname}]({ym}/{fname})")
        lines.append("")
    
    # Also list by source for the most recent
    by_source = defaultdict(list)
    for sess in all_sessions[:50]:  # Recent 50
        source = sess.get('source', 'unknown')
        by_source[source].append(sess)
    
    lines.append("## By Source (Recent)")
    lines.append("")
    for source in sorted(by_source.keys()):
        count = len(by_source[source])
        lines.append(f"**{source}** — {count} sessions in last export window")
    
    lines.append("")
    lines.append("---")
    lines.append("*Last updated: " + datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC") + "*")
    
    index_file.write_text("\n".join(lines) + "\n", encoding='utf-8')
    log(f"Updated session index at {index_file}")

# ---- Main ----

def main():
    argv = sys.argv[1:]

    export_all = "--all" in argv
    days = 7
    for i, a in enumerate(argv):
        if a.startswith("--days="):
            try:
                days = int(a.split("=", 1)[1])
            except (ValueError, IndexError):
                pass
        elif a == "--days" and i + 1 < len(argv):
            try:
                days = int(argv[i + 1])
            except ValueError:
                pass
    
    token = None  # Using SSH auth (key-based)
    
    # 1. Clone/pull repo
    if not clone_or_pull_repo(token):
        log("FATAL: Could not set up repo. Aborting.")
        sys.exit(1)
    
    # 2. Set git config
    if needs_git_setup():
        setup_git()
    
    # 3. Get sessions — aggregate across the main home + each society profile
    sessions = []
    for label, db_path, source_filter in iter_homes():
        db = get_db(db_path)
        if export_all:
            homes_sessions = get_all_session_ids(db, label, source_filter)
        else:
            homes_sessions = get_session_ids(db, label, source_filter, days)
        if homes_sessions:
            log(f"  {label}: {len(homes_sessions)} session(s)")
        sessions.extend(homes_sessions)

    if export_all:
        log("Exporting ALL sessions...")
    else:
        log(f"Exporting sessions from last {days} days...")

    if not sessions:
        log("No sessions found.")
        sys.exit(0)

    log(f"Found {len(sessions)} sessions to export across all homes.")
    
    # 4. Export and push
    if export_and_push(sessions, token):
        log("Export complete.")
    else:
        log("Export failed.")
        sys.exit(1)

if __name__ == "__main__":
    main()
