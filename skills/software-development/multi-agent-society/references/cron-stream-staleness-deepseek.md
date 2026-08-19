# Cron Stream Staleness on DeepSeek

## Symptom

Society cron jobs (archivist, advocate, synthesizer, curator) fail intermittently with:

```
# Cron Job: society-archivist (FAILED)

## Error
RuntimeError: [Errno 32] Broken pipe
```

## Root Cause

The error log reveals the actual mechanism (`~/.hermes/logs/errors.log`):

```
Stream stale for 240s (threshold 240s) — no chunks received. model=deepseek-chat context=~88,443 tokens. Killing connection.
```

Each cron job builds up 77K–150K tokens of conversation context per run (multiple file reads, tool calls, API responses within the same invocation). DeepSeek's time-to-first-token at these context sizes exceeds the `HERMES_STREAM_STALE_TIMEOUT` (default 180s), triggering the stale-stream detector in `agent/chat_completion_helpers.py` (around line 2595). This tears down the HTTP connection, which surfaces as `[Errno 32] Broken pipe` on the client side.

## Affected Jobs (2026-06-30)

| Job | Context size | Staleness logged |
|-----|-------------|------------------|
| society-archivist | 88K tokens | multiple failures at 06:16 |
| society-advocate | 18K tokens | retried at 06:23 (threshold 180s → 240s) |
| society-synthesizer | 103K tokens | retried at 06:49 |
| society-curator | 150K tokens | 3 retries at 07:03–07:19 |

The problem was not agent-mode session accumulation (each cron run gets a fresh `session_id = cron_{job_id}_{timestamp}`). It was the **within-run** context growing large enough that the first API response took >180s.

## Fix Applied

Added to `~/.hermes/.env`:

```
HERMES_STREAM_STALE_TIMEOUT=600
```

This gives the model 10 minutes (600s) to start streaming before the staleness detector kills the connection. Change requires gateway restart to take effect.

## Code Path

1. `cron/scheduler.py` creates `AIAgent(session_id=f"cron_{job_id}_{timestamp}", ...)`
2. `agent/chat_completion_helpers.py` reads `HERMES_STREAM_STALE_TIMEOUT` at line 2544, defaults to 180s
3. For non-local, non-OpenRouter providers, the effective timeout is `max(base, 300.0)` for Gemini/Groq, `max(base, 240.0)` for others — so at default 180s, DeepSeek gets 240s
4. The staleness detector at line 2592 logs `"Stream stale for %.0fs..."` and calls `_close_request_client_once("stale_stream_kill")`

## Future Considerations

- Long-term fix would be to enable context compression per-cron-run or switch to a model with faster TTFB at high context
- The 600s value is a generous buffer — if DeepSeek improves TTFB (or context sizes shrink), it can be reduced back to 180s
