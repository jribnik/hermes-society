# Claude Code Delegation Wrapper

Location: `~/.hermes/scripts/claude-fallback.sh`

Priority chain: **fable → opus → sonnet**. Provides automatic model fallback on rate limits.

## Critical Pitfall: `set -e` kills the cascade

The original wrapper had `set -euo pipefail` which causes the script to exit on ANY non-zero
exit code — including `claude -p` hitting a rate limit. This means the fallback chain never
executes beyond the first failure.

**Fix:** Use `set +e` in the fallback loop:

```bash
set +e
MODELS=("fable" "opus" "sonnet")
for MODEL in "${MODELS[@]}"; do
    OUTPUT=$(claude -p --model "$MODEL" "$PROMPT" 2>&1)
    EXIT_CODE=$?
    
    # Check for rate-limit patterns in output
    if echo "$OUTPUT" | grep -qiE "rate limit|session limit|usage limit|quota"; then
        echo "[claude-fallback] $MODEL rate-limited, trying next..." >&2
        continue
    fi
    
    # Check for non-zero exit
    if [ $EXIT_CODE -ne 0 ]; then
        echo "[claude-fallback] $MODEL exited with code $EXIT_CODE, trying next..." >&2
        continue
    fi
    
    # Success
    echo "$OUTPUT"
    exit 0
done

echo "[claude-fallback] All models failed." >&2
exit 1
```

## Anthropic OAuth Third-Party Billing Trap

**Jul 2026 policy change:** Anthropic now classifies API calls by source:

- **First-party** (`claude -p` CLI): draws from Pro/Max plan subscription limits ✅ free
- **Third-party** (Hermes provider, custom OAuth apps): draws from "extra usage" paid credits ❌

This means building OAuth authentication into Hermes (reading `~/.claude/.credentials.json`
for direct API access) is technically possible but economically unviable — every call
bills against paid credits rather than the plan subscription.

**The OAuth feature was built and tested** (55 tests, `feature/anthropic-oauth` branch
in `jribnik/hermes-agent`) but is blocked by this policy change.

**Recommendation:** Use `claude -p` via this wrapper for heavy delegation tasks.
Do not try to route Hermes' direct API calls through Anthropic OAuth.
