#!/usr/bin/env python3
"""
Hermes Society Watchdog — no-agent mode cron script.

Runs as a standalone watchdog using cronjob(no_agent=True).
On each tick:
  1. Checks that all three daily-instance session files exist and are < 8h old
  2. Checks backup is < 24h old
  3. Checks the Slack commons archive (commons-archive/YYYY-MM.md) is < 48h fresh
  4. Checks the per-profile Slack agents' heartbeat (profiles/society-*/state.db)
  5. Reports any failures

SILENT on success — only outputs when something is wrong.
Designed for `cronjob(action='create', script='watchdog.sh', no_agent=True)`.
"""
import os, json, glob, subprocess, sys
from pathlib import Path
from datetime import datetime, timezone, timedelta

SOCIETY = Path.home() / '.hermes' / 'society'
SESSIONS = SOCIETY / 'sessions'
BACKUP   = SOCIETY / 'backup'

errors = []
warnings = []

now = datetime.now(timezone.utc)

# ── 1. Session file freshness ──────────────────────────────────
MISSING_SESSION_FIX_HINT = (
    "[FIX-HINT] Session files may exist in git but not in the working tree. "
    "Run: cd ~/.hermes/society && git checkout -- sessions/ to restore them."
)
for role in ['archivist', 'advocate', 'synthesizer']:
    role_dir = SESSIONS / role
    files = sorted(role_dir.glob("*.md")) if role_dir.exists() else []
    if not files:
        # Check if git knows about the directory (tracked but deleted from WT)
        try:
            result = subprocess.run(
                ['git', 'ls-files', f'sessions/{role}/'],
                capture_output=True, text=True, cwd=str(SOCIETY), timeout=5
            )
            if result.stdout.strip():
                errors.append(
                    f"[CRON-WATCHDOG] No session files on disk for {role}, "
                    f"but git tracks them — working tree files were deleted! "
                    f"{MISSING_SESSION_FIX_HINT}"
                )
            else:
                errors.append(f"[CRON-WATCHDOG] No session files found for {role} — instance may have never run!")
        except Exception:
            errors.append(f"[CRON-WATCHDOG] No session files found for {role} — instance may have never run!")
        continue
    latest = max(f.stat().st_mtime for f in files)
    age_hours = (now.timestamp() - latest) / 3600
    if age_hours > 8:
        errors.append(f"[CRON-WATCHDOG] {role} last session is {age_hours:.1f}h old — stale!")

# ── 2. Backup freshness ────────────────────────────────────────
if not BACKUP.exists():
    errors.append("[BACKUP] No backup directory exists — no backup has ever been taken!")
elif not any(BACKUP.iterdir()):
    errors.append("[BACKUP] Backup directory exists but is empty!")
else:
    latest_backup = max(BACKUP.glob("*"), key=lambda f: f.stat().st_mtime)
    backup_age = (now.timestamp() - latest_backup.stat().st_mtime) / 3600
    if backup_age > 24:
        errors.append(f"[BACKUP] Last backup ({latest_backup.name}) is {backup_age:.1f}h old!")

# ── 3. Commons archive freshness ───────────────────────────────
# The commons is now the Slack channel (append-only, no line count). What
# matters is that the durable git archive (society-commons-archive.py, daily)
# is keeping up — Slack's free tier only retains ~90 days. Warn if the latest
# monthly archive file is stale (>48h since last write).
ARCHIVE_DIR = SOCIETY / 'commons-archive'
if ARCHIVE_DIR.is_dir():
    archives = sorted(ARCHIVE_DIR.glob('*.md'))
    if not archives:
        warnings.append("[COMMONS] commons-archive/ exists but has no monthly files yet.")
    else:
        newest = max(archives, key=lambda f: f.stat().st_mtime)
        age_h = (now.timestamp() - newest.stat().st_mtime) / 3600
        if age_h > 48:
            warnings.append(f"[COMMONS] Slack archive stale — {newest.name} last written {age_h:.1f}h ago (society-commons-archive runs daily).")
else:
    warnings.append("[COMMONS] commons-archive/ missing — Slack commons is not being archived (90-day retention risk).")

# ── 4. Per-profile Slack agents heartbeat ─────────────────────
# The three producing instances run in their own HERMES_HOME profiles (separate
# state.db). All three fire on the SAME every-3h cron cadence (0/20/40 */3) and
# are full, equal members (no prime-mover/reactor split since the equal-
# initiative redesign) — so each is held to the same <8h freshness standard.
# A stale heartbeat here is a real outage (e.g. a wedged gateway), the exact
# failure the fd-exhaustion incident produced.
import sqlite3
PROFILES = Path.home() / '.hermes' / 'profiles'
for agent in ['archivist', 'advocate', 'synthesizer']:
    db = PROFILES / f'society-{agent}' / 'state.db'
    if not db.exists():
        continue
    try:
        conn = sqlite3.connect(f'file:{db}?mode=ro', uri=True)
        row = conn.execute("SELECT MAX(started_at) FROM sessions").fetchone()
        conn.close()
    except Exception:
        continue
    last = row[0] if row else None
    if not last:
        errors.append(f"[SLACK-AGENT] {agent} profile has no sessions yet — instance never ran!")
        continue
    age_h = (now.timestamp() - last) / 3600
    if age_h > 8:
        errors.append(f"[SLACK-AGENT] {agent} last ran {age_h:.1f}h ago — stale! (fires every ~3h)")

# ── 5. Report ──────────────────────────────────────────────────
if not errors and not warnings:
    sys.exit(0)  # silent on success (no_agent=True)

lines = []
if errors:
    lines.append("❌ HERMES SOCIETY WATCHDOG — FAILURES DETECTED")
    lines.extend(errors)
if warnings:
    if not errors:
        lines.append("⚠️  HERMES SOCIETY WATCHDOG — WARNINGS")
    lines.extend(warnings)

lines.append(f"\nChecked at: {now.isoformat()}")
print("\n".join(lines))
sys.exit(1 if errors else 0)
