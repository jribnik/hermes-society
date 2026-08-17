# Operational Patterns (from 2026-06-29 session)

## Gemini Fallback Removal

Free-tier Gemini (gemini-2.5-flash) hits rate limits at ~5 req/min and causes cron job failures. Fix:

```bash
hermes config set fallback_model.provider ""
hermes config set fallback_model.model ""
hermes cron update <job_id> --model deepseek-chat --provider deepseek
```

Pin ALL society cron jobs explicitly — per-job override is stable vs. the main model setting.

## Watchdog Threshold Drift

`scripts/watchdog.py` constants that must match prompt thresholds:
- **Commons limit:** Was 100, now 300. Must match the Curator prompt's rolloff threshold.
- **Model comparison:** Strip `**` bold markers before comparing: `clean_model = current_model.replace('**', '').strip()`
- **Backup glob:** Target `society-backup-*.tar.gz` specifically

## Session Reorganization

Files moved from flat `sessions/` to `sessions/<instance>/` subdirectories. All prompt paths updated from `sessions/instance_NAME.md` to `sessions/instance/NAME.md`. Git handles as renames with full history. Copy prompts to `baseline/prompts-snapshot/` after changes.

## Session Export Script

`society-export-sessions.py` updated over time:
- Repo: `~/hermes-society/` → `~/.hermes/society/` → `~/hermes-society-sessions/` (separate private repo)
- Transcripts: `sessions/transcripts/` → `transcripts/`
- Filter: `WHERE s.source = 'cron'` to exclude Slack conversations

## README Accuracy

After any filesystem reorganization, update the ASCII tree in README.md. Remove gitignored dirs from the tree.
