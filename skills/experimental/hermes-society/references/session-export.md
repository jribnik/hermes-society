# Session Export Pipeline

Added 2026-06-28 as part of the resilience infrastructure layer. Preserves all conversation history as a permanent, off-device, queryable record on GitHub.

## Script

**Location:** `~/.hermes/scripts/society-export-sessions.py`

**Cron:** no_agent, daily at 05:00 PT (job_id `00241c77a679`)

**What it does:**
1. Queries `~/.hermes/state.db` (SQLite — Hermes session store) for all sessions from the last 7 days
2. Exports each session as a standalone markdown transcript with emoji-labeled messages
3. Organizes by `sessions/transcripts/YYYY/MM/` folder structure in the repo
4. Sanitizes credentials before writing (GitHub tokens, Slack xox* tokens, API keys, Bearer headers)
5. Writes/updates a `README.md` session index at the transcripts root
6. Commits and pushes to `github.com/jribnik/hermes-society` via SSH

**Auth:** SSH key-based (`git@github.com:jribnik/hermes-society.git`). The `gh` CLI is authed to the enterprise GitHub (github.zeromark.internal), not public GitHub, so SSH is the working auth method.

## Changelog Integration

The script also updates the repo's `CHANGELOG.md` on every run:

- Calls `update_changelog()` which appends a dated entry under `## [Unreleased]`
- Deduplicates by date — if an entry for today already exists, it's skipped
- Entry format: `### Session export (YYYY-MM-DD)` with transcript count and source breakdown

See `references/changelog-workflow.md` for the full changelog structure and release cutting process.

## Ad-hoc Usage

```bash
# Last 7 days (default)
python3 ~/.hermes/scripts/society-export-sessions.py

# Last N days
python3 ~/.hermes/scripts/society-export-sessions.py --days=30

# Export everything
python3 ~/.hermes/scripts/society-export-sessions.py --all
```

## Credential Sanitization

Session transcripts can contain tokens embedded in tool call outputs (e.g. `gho_*` tokens used during git operations). The script uses regex-based sanitization before writing any content:

| Pattern | Replacement |
|---------|-------------|
| `gh[ops]_[a-zA-Z0-9_]{10,}` | `ghp_***REDACTED***` |
| `github_pat_[a-zA-Z0-9_]{20,}` | `github_pat_***REDACTED***` |
| `ghu_[a-zA-Z0-9_]{10,}` | `ghu_***REDACTED***` |
| API keys (`api_key=...`) | `api_key=***REDACTED***` |
| Bearer tokens (`Bearer ...`) | `Bearer ***REDACTED***` |
| Slack tokens (`xox[baprs]-...`) | `xox*-***REDACTED***` |

**Keep this list updated** as new token types appear in tool call output. GitHub's push protection will reject commits containing live tokens — the sanitizer must catch them before they reach the file.

## First Export Stats

- **51 transcripts** from the last ~30 days
- **61 total session files** on GitHub (51 new + 10 prior session dumps from the initial repo commit)
- **96 total files** in the repo after export commit
- Repo went from 46 files / 4,271 lines → 96 files / ~5,800+ lines

## GitHub Push Protection

GitHub's push protection scans for secrets and rejects pushes containing live tokens. If a token slips through the sanitizer, you'll see:

```
remote: - GITHUSH PUSH PROTECTION
remote: - Push cannot contain secrets
remote:   —— GitHub Personal Access Token ——
remote:    locations:
remote:      - commit: abc123...
remote:        path: sessions/transcripts/...md:867
```

**Fix:** Either (a) update the sanitizer regex to catch the leaked pattern, then `git reset HEAD~1`, re-run the script, and push; or (b) visit the unblock URL GitHub provides in the error message to bypass secret scanning for that specific commit (not recommended — better to fix the sanitizer).

## Future Improvements

- Add a `--since=<date>` flag for arbitrary date ranges
- Parallelize session fetching (currently sequential SQL)
- Add delta mode: only export sessions newer than the last commit
- Add a `--stats-only` mode that just updates the index without rewriting all transcripts
