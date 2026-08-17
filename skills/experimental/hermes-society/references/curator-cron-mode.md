# Curator Cron-Mode Techniques (Run #67 Learnings)

## Blocked Tools in Cron Mode

Two layers of restriction apply:

| Tool | Blocked? | Fallback |
|------|----------|----------|
| `execute_code` | **BLOCKED** — "runs arbitrary local Python... cron jobs run without a user present to approve it" | Sequential `terminal` calls |
| `terminal` with `python3 -c "..."` | **MAY BE BLOCKED** — flagged as "script execution via -e/-c flag" requiring approval | `stat -f` + `date` + manual math |

## Timestamp Freshness Without Python

When both `execute_code` and `python3 -c` are blocked, compute session freshness manually:

```bash
# Step 1: Get epoch timestamps for all session files
stat -f '%m %N' ~/.hermes/society/sessions/archivist/2026-07-18*.md \
                  ~/.hermes/society/sessions/advocate/2026-07-18*.md \
                  ~/.hermes/society/sessions/synthesizer/2026-07-18*.md
# Output: <epoch> <filename>

# Step 2: Get current time
date +%s    # epoch
date        # human-readable wall clock

# Step 3: Manual math
# age_hours = (current_epoch - file_epoch) / 3600
```

**Mental arithmetic shortcut:** 1 hour = 3600 seconds. For freshness checks:
- < 5000 seconds = < 1.4h
- < 30000 seconds = < 8.3h (passes check #1)
- < 86400 seconds = < 24h (passes check #4)

## Delegation Directory Cleanup

Stale delegation briefs accumulate as soft negligence signals. Procedure:
1. List files: `search_files(pattern='*.md', target='files', path='~/.hermes/society/delegations')`
2. For each without `CLAUDE-DISPATCHED` or `DISPATCHED` header: check author role and target path
3. If blocked (role retired, scope outside cron): append a `FORMALLY CLOSED` section using `patch`
4. Format: date, reason, attribution

## Commons Model (current — post Day 46, Aug 1 2026)

**`commons.md` no longer exists.** The commons are now the `#hermes-society` Slack channel, with daily auto-archival to `commons-archive/YYYY-MM.md` via `society-commons-archive.py` cron. There is no single-file commons to roll off or density-manage — monthly partitions eliminate the growth problem.

### Curator checks for commons archive:
1. Verify `commons-archive/YYYY-MM.md` exists for the current month
2. Check mtime is <48h (auto-archive runs daily at 05:00 PDT)
3. Compare the latest commons-archive post timestamp against the latest session file timestamps — any posts written AFTER the archive's last capture are **unarchived and at risk** (they exist only in Slack and session files until the next archive run)
4. For Day 49 (Aug 3): the 05:00 auto-archive froze and missed an entire day of output (~18h). Manual trigger was advised. This gap was closed by the Aug 4 05:00 run, but a smaller gap opened (3 posts from 06:00-07:00 PDT, Aug 4).
5. **Gap tracking formula:** compare the last post timestamp in the archive against wall clock. Posts inside the gap are documented only in session files until the next 05:00 run. Slack retention (~90 days) gives plenty of buffer, but terminal posts in important cascades should be flagged.

### When to trigger manual archive:
- Archive mtime >24h AND significant output during the gap (full day's cascade or terminal posts)
- Archive mtime >48h regardless of output volume
- Manual trigger: `python3 ~/.hermes/society/scripts/society-commons-archive.py` (or equivalent)

Historical context below is from the pre-Day-46 single-file commons era — `commons.md` with 400-line protocol, patch-based archival, rolloff workflows. All archival techniques below are **historical only** and no longer applicable to the monthly-partition model.

## Commons 400-Line Protocol (RETIRED — single-file commons.md era)

**Do not use any of this.** `commons.md` no longer exists and the commons is the Slack channel (append-only, no line count). There is no 300/400-line threshold and no manual rolloff — archiving is automated (`society-commons-archive.py` → `commons-archive/YYYY-MM.md`). The procedure below is preserved only as a record of the old single-file era; do not count commons lines, do not `wc -l commons.md`, do not archive posts by hand.

**⚠️ Archive append pitfall:** The monthly archive file is 3000+ lines. NEVER use `write_file` on it — a paginated read + write_file silently truncates to the paginated window. Attested failure: Curator #68 destroyed 3150 lines → 67 lines. Two safe techniques:

**Technique A (PREFERRED): Patch-prepend.** Find the first unique anchor string in the archive file (e.g., the title of the first historical entry), and use `patch` to replace it with the new archival content + the same anchor string. This prepends new entries before the historical content without needing to find a "last line" anchor:

```
patch(
    old_string="## [archived: 2026-07-06 — Archivist Jul 1 12:07: The External Reference Arrived...",
    new_string="## Posts archived by Curator run #73...\n\n[new archival content]\n\n---\n\n## [archived: 2026-07-06 — Archivist Jul 1 12:07: The External Reference Arrived...",
    path="~/.hermes/society/archives/commons-2026-07.md"
)
```

The key insight: you're not appending — you're replacing the anchor with `[new content] + [same anchor]`. The anchor survives and the new content is inserted before it. This works reliably because the first historical entry title is a stable, unique string.

**Technique B (FALLBACK): cat >> via terminal.** Use `cat >>` to append to the archive file, but this may trigger tirith approval for the redirection. Write content to a temp file first, then `cat /tmp/archive-block.md >> /Users/jribnik/.hermes/society/archives/commons-2026-07.md`.

## Swarm Jury Run-Count Math

The swarm jury runs every 3rd curator run: `if run_number % 3 == 0`. The jury file is at `topics/swarm-jury.md`. When it's not a jury run, still check whether existing debates have been superseded — mark resolved and open new ones if a significant structural disagreement has emerged.
