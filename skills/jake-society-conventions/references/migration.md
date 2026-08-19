# Hermes Migration — Moving to a New Mac

## The Migration Script

`~/.hermes/scripts/migrate-hermes.sh` creates a tarball at `~/Desktop/hermes-migration.tar.gz` containing all critical Hermes state.

### What gets migrated (small, critical)

| File | Purpose |
|---|---|
| `config.yaml` | Provider/model/tools config |
| `.env` | API keys (Anthropic, DeepSeek, etc.) |
| `auth.json` | OAuth tokens |
| `google_token.json`, `google_client_secret.json` | Google Workspace auth |
| `SOUL.md` | Agent identity |
| `channel_directory.json` | Gateway platform config |
| `state.db` (~680MB) | Full session history + memories |
| `skills/` (~13MB) | All installed skills (heavily customized, not replaceable from hub) |
| `scripts/` | Watchdog, tracking, society scripts |
| `cron/jobs.json` | Cron job definitions |

### What gets skipped

| Path | Reason |
|---|---|
| `hermes-agent/` (3.6GB) | Reinstall fresh |
| `logs/`, `cache/`, `audio_cache/`, `image_cache/` | Start clean |
| `node/`, `bin/`, `lsp/` | Recreated on install |
| `sessions/` request dumps | Transient |

### New Machine Setup

1. Install Hermes fresh: `curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash`
2. Stop gateway: `hermes gateway stop`
3. Extract tarball over `~/.hermes/`
4. Verify `state.db` is readable
5. `git clone git@github.com:jribnik/hermes-society.git ~/.hermes/society`
6. Recreate cron jobs (read `cron/jobs.json`, use `cronjob` tool)
7. Start gateway: `hermes gateway start`
8. Test: send a message from Slack

### Pitfalls

- **Skills are customized, not replaceable.** The hermes-society skill has 454 patches. Fresh downloads from the hub would lose all society-specific knowledge.
- **API keys must be verified.** After extraction, test each provider: `hermes config check`.
- **Gateway restart must be external.** `hermes gateway restart` cannot run from inside the gateway process.
- **state.db is large (680MB+).** Use rsync with progress for large file transfer if the tarball approach is too slow.
