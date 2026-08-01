#!/usr/bin/env bash
# Deploy the canonical, profile-agnostic fetch_slack_messages.py into each
# society profile's scripts/ dir. The cron --script sandbox requires the file to
# physically live in the profile's own scripts/ (symlinks that resolve outside
# it are rejected), so "one script" = one canonical source here, copied to all.
# Edit society/scripts/fetch_slack_messages.py, then run this to sync.
set -euo pipefail
CANON="$(cd "$(dirname "$0")" && pwd)/fetch_slack_messages.py"
for p in society-archivist society-advocate society-synthesizer; do
  dst="$HOME/.hermes/profiles/$p/scripts/fetch_slack_messages.py"
  install -m 755 "$CANON" "$dst"
  echo "deployed → $dst"
done
