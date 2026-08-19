# No-Agent Script Cron for Periodic Checks (Tracking, Watchdog, Heartbeat)

Use `no_agent=true` with `cronjob` for mechanical polling tasks where an LLM adds no value. The script is the job — its stdout is delivered directly to the user.

## Pattern

```python
# Create a script that:
# 1. Checks a state file for the last known status
# 2. Queries the external service
# 3. Compares with previous state
# 4. Outputs ONLY when something changed (silent otherwise)
# 5. Saves current state for next comparison
```

```
cronjob(
    action='create',
    script='tracking-check.py',       # script lives at ~/.hermes/scripts/
    name='tracking-check',            # human name
    schedule='0 10 * * *',            # daily at 10am
    no_agent=True,                    # no LLM — script IS the job
    deliver='origin'                  # deliver to origin when stdout is non-empty
)
```

## Key Design Decisions

1. **State storage on disk** — `~/.hermes/scripts/check-<id>.json` stores `last_status`, `last_detail`, `last_check`. Persists across cron runs.
2. **Silent when unchanged** — empty stdout = nothing delivered to user. Only prints when status differs from last saved state.
3. **First check reports** — when no state file exists, first successful check reports the initial status.
4. **Failed queries exit silently** — if the external service is unreachable, don't spam the user. Exit 0 with no output. The state file gets updated on successful queries only.
5. **Multiple backends** — try primary API first, fall back to secondary. Both fail? Exit silently.

## Usage: USPS Tracking Check

Script at `~/.hermes/scripts/tracking-check.py`. Tries USPS tracking API first, falls back to third-party tracker. State saved to `~/.hermes/scripts/tracking-<number>.json`. Cron runs daily at 10am PT.

## When to Use This Pattern

- Tracking number monitoring (USPS, FedEx, UPS, DHL)
- Service health checks (is an API up? is a site responding?)
- Threshold monitors (disk usage, memory, temperature)
- Heartbeat verification (is another system still running?)
- Any periodic check where "nothing changed" is the expected outcome and "something changed" is the signal

## When NOT to Use

- Content that needs intelligent summarization → use LLM-driven cron (no_agent=False)
- Conditional logic that requires reasoning → LLM-driven
- Checks that need cross-referencing with other data sources → LLM-driven
