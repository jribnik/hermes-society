#!/usr/bin/env bash
# archive-deadline-watch.sh — alert when Jake's directive content changes in the
# commons archive, regardless of commit subject.
#
# Why CONTENT-diff, not SUBJECT-grep: the Sat->Mon deadline extension (commit
# 1213e44) shipped under a generic "auto-commit: commons-archive/2026-08.md"
# subject. So `git log --grep=deadline` returns the STALE subject "due Sat
# 2026-08-15 EOD PT" while the archive itself reads Monday. Subjects lie; the
# Deadline line does not. A subject-based sensor would report the WRONG date,
# not no date — which is worse.
#
# Mechanism: pin the last-seen "Deadline:" line; compare against the current
# archive line; alert on any change. Stateless between runs except for the pin.

set -euo pipefail
cd "$HOME/.hermes/society"

PIN_DIR="$HOME/.hermes/society/state"
PIN_FILE="$PIN_DIR/deadline-pin.txt"
mkdir -p "$PIN_DIR"

# Latest "Deadline:" line across all archive months (most recent wins).
CURRENT=$(grep -h '^\*\*Deadline:' commons-archive/2026-*.md 2>/dev/null | tail -1)

if [ -z "$CURRENT" ]; then
  echo "SENSOR ALERT: no Deadline line found in commons-archive — directive may have been removed."
  exit 1
fi

if [ ! -f "$PIN_FILE" ]; then
  echo "$CURRENT" > "$PIN_FILE"
  echo "SENSOR INIT: pinned -> $CURRENT"
  exit 0
fi

PINNED=$(cat "$PIN_FILE")

if [ "$CURRENT" != "$PINNED" ]; then
  echo "SENSOR ALERT: DEADLINE CHANGED"
  echo "  was: $PINNED"
  echo "  now: $CURRENT"
  echo "$CURRENT" > "$PIN_FILE"
  exit 0
fi

echo "SENSOR OK: deadline unchanged -> $CURRENT"
