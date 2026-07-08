#!/usr/bin/env bash
# Record model baseline for Hermes Society — run once to establish baseline.
# Called by: first-time setup, or to update after intentional model change.

BASELINE_DIR="$HOME/.hermes/society/baseline"
mkdir -p "$BASELINE_DIR"

# Read model from a recent session file to establish baseline
MODEL=""
RECENT_SESSION=$(ls -t ~/.hermes/society/sessions/archivist/*.md 2>/dev/null | head -1)
if [ -n "$RECENT_SESSION" ]; then
    MODEL=$(head -10 "$RECENT_SESSION" | grep -i "^model:" | sed 's/^[Mm]odel:\s*//')
fi

# Record the model baseline
cat > "$BASELINE_DIR/model-baseline.json" << EOF
{
  "model": "${MODEL:-unknown}",
  "recorded_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "provider": "deepseek",
  "description": "Baseline model version for Hermes Society. If this changes unexpectedly, all instances may have different behavior."
}
EOF

# Also snapshot prompt files for diffing later
PROMPT_SNAPSHOT="$BASELINE_DIR/prompts-snapshot"
mkdir -p "$PROMPT_SNAPSHOT"
cp ~/.hermes/society/prompts/*.md "$PROMPT_SNAPSHOT/" 2>/dev/null

echo "[BASELINE] Recorded model: ${MODEL:-unknown}"
echo "[BASELINE] Prompt snapshot at: $PROMPT_SNAPSHOT"
echo "[BASELINE] Run 'diff -r ~/.hermes/society/prompts/ $PROMPT_SNAPSHOT' to detect prompt drift."
