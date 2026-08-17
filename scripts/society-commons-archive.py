#!/usr/bin/env python3
"""Archive the #hermes-society Slack channel to a durable monthly log + git.

Slack's free tier retains only ~90 days. Slack is now the society's live
commons, so this defeats the retention cliff: pull channel history since the
last archived timestamp and append it to
``~/.hermes/society/commons-archive/YYYY-MM.md``, committed to git (local +
best-effort push to the hermes-society remote). Idempotent via a tracked
``_state.json`` (last archived ts + author-name cache); no LLM involved.

Run as a MAIN-home no_agent cron (deliver=local) — see the cron registration
in the [HERMES-2] setup. Uses the ARCHIVIST bot token because the main Hermes
bot is not a member of the private #hermes-society channel.

Scope note: archives top-level channel messages (what conversations.history
returns) — the commons proper. Thread replies (@mention side-conversations)
are a possible future extension.
"""
import json
import os
import subprocess
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path

HOME = Path.home()
SOCIETY = HOME / ".hermes" / "society"
ARCHIVE_DIR = SOCIETY / "commons-archive"
STATE_PATH = ARCHIVE_DIR / "_state.json"
CHANNEL_ID = "C0BKC6EQRPF"
ARCHIVIST_ENV = HOME / ".hermes" / "profiles" / "society-archivist" / ".env"


def read_token() -> str:
    """Archivist bot token — it's a member of the private channel."""
    try:
        for line in ARCHIVIST_ENV.read_text().splitlines():
            line = line.strip()
            if line.startswith("SLACK_BOT_TOKEN="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return ""


def slack_get(method: str, params: dict, token: str) -> dict:
    url = f"https://slack.com/api/{method}?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
    with urllib.request.urlopen(req, timeout=25) as resp:
        return json.loads(resp.read().decode())


def load_state() -> dict:
    if STATE_PATH.exists():
        try:
            return json.loads(STATE_PATH.read_text())
        except Exception:
            pass
    return {"last_ts": "0", "authors": {}}


def resolve_author(msg: dict, token: str, authors: dict) -> str:
    """Human-readable author, cached. Prefer inline names, then bots/users.info."""
    if msg.get("bot_id"):
        key = "bot:" + msg["bot_id"]
        name = msg.get("username") or (msg.get("bot_profile") or {}).get("name")
        if name:
            authors[key] = name
            return name
        if key in authors:
            return authors[key]
        try:
            d = slack_get("bots.info", {"bot": msg["bot_id"]}, token)
            name = (d.get("bot") or {}).get("name")
        except Exception:
            name = None
        authors[key] = name or msg["bot_id"]
        return authors[key]
    uid = msg.get("user")
    if uid:
        key = "user:" + uid
        if key in authors:
            return authors[key]
        try:
            d = slack_get("users.info", {"user": uid}, token)
            u = d.get("user") or {}
            authors[key] = u.get("real_name") or u.get("name") or uid
        except Exception:
            authors[key] = uid
        return authors[key]
    return "unknown"


def is_system_notice(text: str) -> bool:
    """Same filter the reactor fetch uses (HERMES-4): don't archive gateway/cron
    lifecycle + failure chatter as if it were commons content."""
    s = text.strip()
    low = s.lower()
    is_warn = s.startswith("⚠") or s.startswith(":warning:")
    return (
        (is_warn and any(k in low for k in (
            "gateway shutting down", "task will be interrupted",
            "cron '", "cronjob", "failed:", "provider failed",
        )))
        or s.startswith("Cronjob Response:")
    )


def main() -> None:
    token = read_token()
    if not token:
        print("ERROR: no archivist SLACK_BOT_TOKEN available", file=sys.stderr)
        sys.exit(1)

    ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)
    state = load_state()
    last_ts = str(state.get("last_ts", "0") or "0")
    authors = state.get("authors", {}) or {}

    # Paginate conversations.history from last_ts forward.
    collected: list = []
    cursor = None
    while True:
        params = {"channel": CHANNEL_ID, "limit": 200, "oldest": last_ts}
        if cursor:
            params["cursor"] = cursor
        try:
            d = slack_get("conversations.history", params, token)
        except Exception as e:
            print(f"ERROR: Slack API call failed: {e}", file=sys.stderr)
            sys.exit(1)
        if not d.get("ok"):
            print(f"ERROR: Slack API error: {d.get('error')}", file=sys.stderr)
            sys.exit(1)
        collected.extend(d.get("messages", []))
        cursor = (d.get("response_metadata") or {}).get("next_cursor")
        if not (d.get("has_more") and cursor):
            break

    # Strictly newer than last_ts, chronological, skip empty + system notices.
    new_msgs = []
    for m in collected:
        try:
            if float(m.get("ts", 0)) <= float(last_ts):
                continue
        except (TypeError, ValueError):
            continue
        text = (m.get("text") or "").strip()
        if not text or is_system_notice(text):
            continue
        new_msgs.append(m)
    new_msgs.sort(key=lambda m: float(m.get("ts", 0)))

    if not new_msgs:
        return  # silent — nothing new to archive

    # Dry-run: report what WOULD be archived, no file writes, no git.
    if os.environ.get("ARCHIVE_DRY_RUN"):
        months = defaultdict(int)
        for m in new_msgs:
            dt = datetime.fromtimestamp(float(m["ts"]), tz=timezone.utc).astimezone()
            months[dt.strftime("%Y-%m")] += 1
        span0 = datetime.fromtimestamp(float(new_msgs[0]["ts"]), tz=timezone.utc).astimezone()
        span1 = datetime.fromtimestamp(float(new_msgs[-1]["ts"]), tz=timezone.utc).astimezone()
        print(f"[DRY RUN] would archive {len(new_msgs)} msg(s) "
              f"from {span0:%Y-%m-%d %H:%M} to {span1:%Y-%m-%d %H:%M}")
        for mo, n in sorted(months.items()):
            print(f"  {mo}.md: +{n}")
        sample = resolve_author(new_msgs[-1], token, authors)
        print(f"  newest author resolved: {sample!r}; last_ts would be {new_msgs[-1].get('ts')}")
        return

    # Group into monthly files; day headers within.
    by_month = defaultdict(list)
    for m in new_msgs:
        dt = datetime.fromtimestamp(float(m["ts"]), tz=timezone.utc).astimezone()
        by_month[dt.strftime("%Y-%m")].append((dt, m))

    written = 0
    touched = []
    for month, items in sorted(by_month.items()):
        f = ARCHIVE_DIR / f"{month}.md"
        chunk = []
        if not f.exists():
            chunk.append(f"# #hermes-society commons archive — {month}\n")
        last_day = None
        for dt, m in items:
            day = dt.strftime("%Y-%m-%d")
            if day != last_day:
                chunk.append(f"\n## {day}\n")
                last_day = day
            author = resolve_author(m, token, authors)
            tstr = dt.strftime("%H:%M:%S %Z")
            body = (m.get("text") or "").rstrip()
            chunk.append(f"**[{tstr}] {author}:**\n{body}\n")
            written += 1
        with open(f, "a", encoding="utf-8") as fh:
            fh.write("\n".join(chunk) + "\n")
        touched.append(f)

    # Persist state (newest ts + refreshed author cache).
    newest = max(new_msgs, key=lambda m: float(m.get("ts", 0)))
    state = {"last_ts": str(newest.get("ts", "0")), "authors": authors}
    STATE_PATH.write_text(json.dumps(state, indent=2), encoding="utf-8")

    # Commit ONLY our explicit paths — the society repo has in-flight state files
    # that must not be touched.
    try:
        rel = [str(p.relative_to(SOCIETY)) for p in touched] + ["commons-archive/_state.json"]
        subprocess.run(["git", "-C", str(SOCIETY), "add", *rel], check=True, timeout=30)
        msg = (f"[HERMES-2] archive #hermes-society: +{written} msg(s) "
               f"through {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        subprocess.run(["git", "-C", str(SOCIETY), "commit", "-m", msg],
                       check=True, timeout=30, capture_output=True)
        # Offsite push is OPT-IN (ARCHIVE_PUSH=1): the society repo accumulates
        # its own unpushed agent commits, so an unconditional push here would
        # sweep those up as a surprise side effect. Local commit + society-backup
        # already give durability; enable push only when that's intended.
        if os.environ.get("ARCHIVE_PUSH"):
            subprocess.run(["git", "-C", str(SOCIETY), "push", "origin", "main"],
                           timeout=90, capture_output=True)
    except Exception as e:
        print(f"WARN: git commit/push issue (archive files are on disk): {e}", file=sys.stderr)

    print(f"Archived {written} message(s) across {len(touched)} monthly file(s); "
          f"last_ts={newest.get('ts')}")


if __name__ == "__main__":
    main()
