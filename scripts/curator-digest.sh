#!/bin/bash
# Deliver the latest curator summary to Slack. Silent when there's nothing new.
CURATOR_DIR="$HOME/.hermes/society/curator-summaries"
LAST_FILE="$HOME/.hermes/society/.curator-digest-last"

latest=$(ls -t "$CURATOR_DIR"/curator_*.md 2>/dev/null | head -1)
if [ -z "$latest" ]; then
  exit 0
fi

# Only deliver if this file hasn't been sent yet
if [ -f "$LAST_FILE" ] && [ "$(cat "$LAST_FILE")" = "$latest" ]; then
  exit 0
fi

echo "$latest" > "$LAST_FILE"
echo "📋 *Curator Summary — $(basename "$latest" .md)*"
echo ""
cat "$latest"
