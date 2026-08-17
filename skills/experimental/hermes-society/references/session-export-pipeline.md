# Session Transcript Export Pipeline

## Repo Layout

Session transcripts are exported to a **separate private repo** at `~/hermes-society-sessions/`.
Remote: `git@github.com:jribnik/hermes-society-sessions.git` (private).
This keeps Jake's private Slack chat history separated from the public society data.

## How It Works

- **Script**: `~/.hermes/scripts/society-export-sessions.py`
- **Schedule**: Daily at 05:00 PT (no_agent cron job `society-session-export`)
- **Scope**: Last 7 days of **cron-only** sessions from the SQLite state DB (`WHERE s.source = 'cron'`). Slack/DM sessions (Jake's private chats) are excluded to keep private conversations out of the experiment repo.
- **Founding conversations**: Three key early conversations are preserved separately in `founding/` directory of the sessions repo.
- **Output**: Markdown transcripts in `transcripts/YYYY/MM/` with a session index README
- **Sensitive data**: Redacted (API keys, tokens, slack tokens via regex patterns)
- **Changelog**: Appends an "Unreleased" entry to `CHANGELOG.md` on each run

## Key Paths

| Item | Path |
|------|------|
| Export script | `~/.hermes/scripts/society-export-sessions.py` |
| Transcripts repo | `~/hermes-society-sessions/` |
| Society repo | `~/.hermes/society/` (git remote: `jribnik/hermes-society`) |
| Cron job name | `society-session-export` |

## Setup

1. Create `jribnik/hermes-society-sessions` on GitHub (private)
2. The script handles clone/pull/commit/push via SSH keys
3. If main branch lacks upstream tracking, run: `git branch --set-upstream-to=origin/main main`

## Known Failure Modes

### Mode 1: `.invalid` Branch (Jul 2026 — unresolved)

The sessions repo's `.git/HEAD` points to `ref: refs/heads/.invalid` — an unborn branch that exists as a local reference but has no matching remote. Git refuses commit on such a ref because there's no upstream. The fix is `git branch -m main` (one command).

**Cumulative retry debt:** Each automatic retry (scheduled 05:00 PT daily) does NOT fail cleanly — it degrades the state:

1. **First retry** → `.invalid` branch prevents commit, but `git add` succeeds, writing to index
2. **Second retry** (Jul 29 05:00 PT) → COMMIT_EDITMSG generated (117 bytes, "196 transcripts"). Lock contention introduced on HEAD (`fatal: cannot lock ref 'HEAD': reference already exists`)
3. **Next retry** (projected) → Three active failure modes: `.invalid` branch + HEAD lock contention + dirty index from partial writes

The export script assumes either success (state resets) or clean failure (state unchanged). The actual failure mode is cumulative: each retry writes partial state that the next retry must contend with. Documented in Advocate session 2026-07-29 §2.
