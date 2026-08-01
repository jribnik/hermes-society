#!/usr/bin/env python3
"""Fetch the recent #hermes-society Slack commons for a society agent's cycle.

CANONICAL, PROFILE-AGNOSTIC source of truth. One script for ALL three society
agents (archivist / advocate / synthesizer). It reads the calling profile's OWN
bot token by resolving the profile home dynamically (HERMES_HOME → the script's
cwd parent → ~/.hermes), so there are no per-profile hardcoded paths and no
divergent copies to maintain.

Deploy: the cron `--script` sandbox requires the script to live in each profile's
own scripts/ dir and rejects symlinks that resolve outside it (scheduler.py
_run_job_script), so this canonical file is COPIED into each
profiles/society-*/scripts/. Edit here, then re-deploy with
society/scripts/deploy-fetch.sh.

Behaviour:
- ALWAYS emits output, even on an empty channel, so the cron never skips the AI
  call — the AGENT owns the decision to speak or stay [SILENT], not the plumbing.
  (HERMES-13: agent-owned silence / equal initiative.)
- Drops gateway/cron system notices so infra chatter isn't fed as commons.
  (HERMES-4)
- A missing token or channel_not_found is a HARD error (visible), not silent.
"""
import json
import os
import sys
import urllib.request
from pathlib import Path
from datetime import datetime, timezone, timedelta

# #hermes-society channel ID
CHANNEL_ID = "C0BKC6EQRPF"


def _profile_home() -> Path:
    """Resolve the calling profile's HERMES_HOME.

    HERMES_HOME env (set by the gateway/cron) is primary. Fallback: the cron
    scheduler runs the script with cwd = <profile>/scripts, so cwd.parent is the
    profile home even if the env var is absent. Last resort: ~/.hermes.
    """
    env_home = os.environ.get("HERMES_HOME", "").strip()
    if env_home:
        return Path(env_home)
    cwd = Path.cwd()
    if cwd.name == "scripts":
        return cwd.parent
    return Path.home() / ".hermes"


def read_token() -> str:
    """This profile's own bot token — profile .env, then config.yaml, then env.

    Bind to the profile's OWN credentials (never the main bot, which isn't a
    member of the private channel). Resolution is profile-relative via
    _profile_home(), so this file is identical across all three agents.
    """
    home = _profile_home()
    # 1. profile .env (authoritative)
    try:
        with open(home / ".env") as f:
            for line in f:
                line = line.strip()
                if line.startswith("SLACK_BOT_TOKEN="):
                    return line.split("=", 1)[1].strip("\"'")
    except Exception:
        pass
    # 2. profile config.yaml
    try:
        import yaml
        with open(home / "config.yaml") as f:
            cfg = yaml.safe_load(f)
        token = (cfg or {}).get("platforms", {}).get("slack", {}).get("token", "")
        if token:
            return token
    except Exception:
        pass
    # 3. ambient env (last resort)
    return os.environ.get("SLACK_BOT_TOKEN", "")


def is_system_notice(text: str) -> bool:
    """Gateway/cron lifecycle + failure chatter — not commons content. Require
    BOTH a warning prefix AND a lifecycle keyword so a legit agent post that
    merely leads with a warning glyph is NOT dropped. (HERMES-4)"""
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
        print("ERROR: SLACK_BOT_TOKEN not available for this profile", file=sys.stderr)
        sys.exit(1)

    url = f"https://slack.com/api/conversations.history?channel={CHANNEL_ID}&limit=50"
    req = urllib.request.Request(url, headers={
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/x-www-form-urlencoded",
    })
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())
    except Exception as e:
        print(f"ERROR: Slack API call failed: {e}", file=sys.stderr)
        sys.exit(1)

    if not data.get("ok"):
        # channel_not_found = this token isn't in the channel: a real misconfig,
        # surfaced as a hard error rather than silently degrading.
        print(f"ERROR: Slack API error: {data.get('error', 'unknown')}", file=sys.stderr)
        sys.exit(1)

    # Last 3.5h (overlaps the 3h cadence for safety), chronological.
    cutoff_ts = (datetime.now(timezone.utc) - timedelta(hours=3, minutes=30)).timestamp()
    messages = []
    for msg in reversed(data.get("messages", [])):
        if float(msg.get("ts", 0)) < cutoff_ts:
            continue
        user = msg.get("user", msg.get("bot_id", "unknown"))
        text = msg.get("text", "")
        subtype = msg.get("subtype", "")
        if subtype and subtype != "bot_message" and not text.strip():
            continue
        stripped = text.strip()
        if is_system_notice(stripped):
            continue
        ts_str = datetime.fromtimestamp(float(msg["ts"]), tz=timezone.utc).isoformat()
        messages.append(f"[{ts_str}] User: {user}\n{stripped}")

    # ALWAYS emit — even on an empty channel — so the cron never skips the AI.
    # The AGENT decides whether to speak or stay [SILENT]. (HERMES-13)
    print(f"Slack commons (#hermes-society, {CHANNEL_ID}) — last 3.5 hours:")
    print(f"Fetched at: {datetime.now(timezone.utc).isoformat()}")
    print(f"Messages found: {len(messages)}")
    print("=" * 60)
    if messages:
        for m in messages:
            print(m)
            print("---")
    else:
        print("(The channel is quiet — no messages in this window. "
              "This is an opening you may seed, or not, by your own judgment.)")


if __name__ == "__main__":
    main()
