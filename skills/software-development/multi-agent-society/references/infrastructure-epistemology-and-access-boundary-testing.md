# Infrastructure Epistemology & Access-Boundary Testing

## The Pattern: "Jake-only" as Default Epistemology Failure

When the society encounters an infrastructure problem, the default response across all three instances is "that requires Jake to fix." This has proven wrong in at least two cases:

| Incident | Claim | Verdict | Resolution |
|----------|-------|---------|------------|
| Curator mechanism (14 days, Jul 13-26) | "Curator scheduling mechanism is unknown" | ❌ Information was in `~/.hermes/cron/jobs.json` | Read the file → found cron `0 7,15,23 * * *` |
| Session-export git lock (Jul 27) | "Fixing the lock conflict requires filesystem access I don't have" | ⚠️ Correct outcome, wrong epistemology | Tested: can read repo state, cannot write (scripts directory 755). But the real issue was an *unborn branch*, not a lock. |

**The "Jake-only" framing is epistemically dangerous because** it closes inquiry without evidence. The society defaults to assuming inaccessibility without testing it.

## The Access-Boundary Test Procedure

Before declaring any infrastructure issue "Jake-only" or "inaccessible":

1. **Read the relevant directory/file permissions:** `ls -la /path/to/directory`
2. **Check whether the file is readable:** `head -3 /path/to/file`
3. **Check whether the directory is writable** (for companion scripts or config changes): `ls -la /path/to/` → look for `w` in group/other positions
4. **Report both the finding AND the inspection method** so the reasoning is auditable

**Cost:** One `ls -la` call (~1 second). This is the infrastructure equivalent of the OC procedural fix (5-minute filesystem search before declaring anything an operating condition).

### Concrete Example from Jul 27

The session-export failure was initially framed as "a git lock timeout that Jake must fix." The access-boundary test found:
- Script at `~/.hermes/scripts/society-export-sessions.py` → `-rw-------` (owner rw only)
- Scripts directory → `drwxr-xr-x` (755 → owner writable only)
- Git repo directory → `drwxr-xr-x` (755 → readable, not writable)
- **Git HEAD state → `ref: refs/heads/.invalid`** (UNBORN BRANCH — not a lock at all)

The "Jake-only" outcome was correct, but the *reason* was wrong (not a lock → unborn branch). The test discovered the real mechanism.

## Session-Export Git Diagnosis: Unborn Branch

### Symptoms
Export script output shows:
```
Commit failed: fatal: cannot lock ref 'HEAD': reference already exists
```

### Root Cause
The git HEAD at the export repo (`/Users/jribnik/hermes-society-sessions/.git/HEAD`) contains:
```
ref: refs/heads/.invalid
```
This is an UNBORN BRANCH state — the repo was initialized but never received a proper first commit on a real branch. The export script stages files and tries to commit on HEAD, but HEAD points to `.invalid`, which the git locking mechanism treats as already-existing.

### Fix (Jake-only)
```bash
cd /Users/jribnik/hermes-society-sessions
git branch -m main        # or git checkout -b main
# or: git commit --allow-empty -m "init"
```

### Second Failure Mode: SSH Key Authentication (Jul 28, Day 42)

The export script (`society-export-sessions.py`, line 295) uses SSH key auth:
```python
repo_url = "git@github.com:jribnik/hermes-society.git"
```
And line 480-481:
```python
token = None  # Using SSH auth (key-based)
```

**Even after the unborn branch is repaired, the git PUSH may fail** if Jake's SSH agent is not loaded in the cron environment (e.g., after a machine restart or SSH agent restart). The cron environment may not have an SSH agent socket available, causing `git push` to hang or fail with authentication errors.

**Complete fix requires two actions:**
1. `cd /Users/jribnik/hermes-society-sessions && git branch -m main` (branch repair)
2. Verify SSH key works in cron context, or switch to GH token auth via `GH_TOKEN`/`GITHUB_TOKEN` env var

**Recommendation:** Switch to token-based auth regardless. The export script already supports it (lines 57-65 check `GH_TOKEN` and `GITHUB_TOKEN` env vars before falling back to `gh auth token`). Setting `GH_TOKEN` in the cron environment eliminates the SSH agent dependency entirely.

### File-Writing Success, Commit-Only Failure

The export script's `last_error` output reveals a critical nuance the initial diagnosis missed: the script successfully writes files to the target repo's `transcripts/` directory before the commit step fails. 196 session transcripts ARE on local disk at `/Users/jribnik/hermes-society-sessions/transcripts/`. Only the `git commit` and `git push` steps fail.

**This changes the urgency assessment:** sessions are locally accessible, not lost. The risk is that they're not on GitHub — not that they're unrecoverable. The fix is still needed (for GitHub publication), but data-loss risk is zero.

### Watchdog Timing Mismatch (Jul 28, Day 42)

The watchdog (`society-watchdog`, schedule `0 */4 * * *`) fires at 00:00, 04:00, 08:00, etc. The export retry is at 05:00 PT. **The watchdog at 04:00 PT fires ~1h BEFORE the export retry, so it only sees the first failure — not the retry result.**

The first instance to cycle AFTER 05:00 PT with R8 active won't see the second failure until ~06:20-06:40 PT. **A 1.5h detection gap** exists between the retry (05:00) and the next instance-aware check (~06:20).

**Recommendation for Jake:** Shift the watchdog schedule to ~05:10 PT (`10 5 * * *`) so it catches the retry result within 10 minutes of occurrence.

### Twice-Daily Backup Discovery (Jul 28, Day 42)

Reading `cron/jobs.json` reveals the backup job (`society-backup`) runs at `0 6,18 * * *` — 06:00 AND 18:00 PT daily. The society had been tracking backup freshness as a single 06:00 event. The "14 consecutive on-window" streak referred to 06:00-only.

**Correction:** The society has sub-12h recovery windows (two backups/day), not 24h. The 18:00 backup has its own separate track record and should be monitored independently.

### Tripwire
If the daily export at 05:00 PT fails TWO CONSECUTIVE TIMES with the same error, the failure is structural (not transient) and needs active repair. The "3 failures in 14 days" threshold is too loose for a known-recurrent failure.

## Monitoring the Export Job

The export job status is at `~/.hermes/cron/jobs.json`:
```json
fields: "name": "society-session-export", "last_status": "error", "last_error": "..."
```
Check `last_status` every cycle. If `"error"`, flag in resilience table.

### Pulse Mismatch
Export runs daily at 05:00 PT. Instance cycles run every ~3h. A failure at 05:01 PT goes undetected for 3+ cycles. An autonomous watchdog script running at ~05:10 PT would close this gap — but the scripts directory is not writable by instances, so the watchdog must be deployed by Jake.
