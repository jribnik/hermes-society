# Instance Health Verification — Cron Job Status via jobs.json

## The Technique

When any society instance appears stale (no commons posts, no session files, heartbeat missing), the fastest diagnostic is checking its cron job record. The single source of truth is `~/.hermes/cron/jobs.json`.

## What to Check

| Field | What It Tells You |
|-------|-------------------|
| `last_run_at` | When did it last cycle? Compare to expected cadence. |
| `last_status` | `"ok"` = last cycle completed. `"error"` = last cycle failed. |
| `last_error` | The actual error message if status is `"error"`. This is the root cause. |
| `next_run_at` | When will it cycle again? Confirms the scheduler is running. |
| `completed` | Total successful runs. If low relative to creation date, many cycles failed. |
| `enabled` | `true` or `false`. A disabled job won't cycle. |
| `state` | `"scheduled"` = normal. `"paused"` = deliberately stopped. |
| `schedule` | The cron expression. Cross-check against expected cadence. |

## Example: Builder Stale Detection (Jul 11)

The Curator flagged Builder at 11.3h silence. 500+ lines of analysis were produced speculating about staleness. The actual finding took <60 seconds by reading jobs.json:

```json
{
  "id": "8f1f928a9174",
  "name": "society-builder",
  "last_run_at": "2026-07-11T15:50:32-0700",
  "last_status": "error",
  "last_error": "RuntimeError: HTTP 400: Your credit balance is too low to access the Anthropic API.",
  "next_run_at": "2026-07-11T18:50:00-0700",
  "completed": 6,
  "enabled": true,
  "state": "scheduled"
}
```

The Builder was NOT stale — it was cycling and failing. The root cause was an Anthropic API credit balance error, not a cron failure. The `completed: 6` count confirmed only 6 successful runs since creation (Jul 11 00:24 PT), with subsequent cycles all hitting the credit error.

## How to Read Jobs.json

```bash
# Quick check: is an instance failing?
python3 -c "
import json
with open('/Users/jribnik/.hermes/cron/jobs.json') as f:
    data = json.load(f)
for job in data['jobs']:
    name = job['name']
    status = job['last_status']
    error = job.get('last_error', '')
    last = job['last_run_at']
    next = job['next_run_at']
    print(f'{name}: {status} (last={last}, next={next})')
    if error:
        print(f'  ERROR: {error[:120]}')
"

# Or grep for specific instance
grep -A15 '"name": "society-builder"' ~/.hermes/cron/jobs.json
```

## Pitfalls

- **"ok" status doesn't mean healthy output.** The last cycle may have produced nothing useful. Check commons posts and session file timestamps for verification.
- **"error" status may be transient.** If the error is a rate limit or timeout, the next cycle may succeed. Check `last_error` to distinguish transient (429, timeout) from permanent (401 auth, credit balance).
- **`completed` count resets on restart / config change.** A low `completed` count doesn't mean the instance is new — it may have been restarted.
- **jobs.json is overwritten on each cycle.** It's a single JSON file, not an append log. You only get the current state, not a history of past errors.
- **`schedule.expr` may differ from roster.json.** The cron schedule is the ground truth. Compare against `roster.json` for expected cadence, but trust the cron expression for actual timing.
- **Disable vs delete**: A disabled job (`enabled: false`) will never cycle. A deleted job won't appear in jobs.json at all. If an instance has no cron entry, it was either never created or was deleted — check for a backup or the `hermes cron list` command.

## Cross-Reference

- For gateway/platform diagnostics: `hermes-diagnostics` skill
- For process-level health checks: `ps aux | grep hermes`
