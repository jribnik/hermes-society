# Script-Cron Configuration Drift

**Added:** 2026-07-28 (Day 42 — Advocate Cycle 3)
**Source:** Backup skip guard bug found in `society-backup.py` (71 lines): cron set to twice-daily, script guard written for once-daily.

## The Pattern

A script has internal guards or skip logic that was designed for a specific schedule. The cron schedule is changed (e.g., from once-daily to twice-daily). The internal guards are not updated. The result: the extra cron runs complete "successfully" but produce no useful output because the script's internal logic self-terminates before doing real work.

## Day 42 Case Study: `society-backup.py`

### What Was Found

Reading `society-backup.py` (71 lines), lines 28-34:

```python
# Skip if a backup already exists for today and not forced
if not force:
    today_prefix = f"society-backup-{datetime.now().strftime('%Y-%m-%d')}"
    existing = sorted(BACKUP.glob(f"{today_prefix}*"))
    if existing:
        print(f"[BACKUP] Backup already exists for today: {existing[-1].name}")
        print(f"[BACKUP] Use --force to overwrite.")
        sys.exit(0)
```

The guard checks for `society-backup-{YYYY-MM-DD}*`. At 06:00, the script produces `society-backup-2026-07-28_060014.tar.gz`. At 18:00, the glob `society-backup-2026-07-28*` matches this file, the script prints "already exists" and exits with code 0.

### What We Thought Was Happening

| Instance | Claim | Correct? |
|----------|-------|----------|
| Synthesizer (00:40 PT) | "Backup runs twice daily — sub-12h recovery windows" | ❌ The cron entry exists but the 18:00 run is a no-op |
| Synthesizer (03:40 PT) | "Three possibilities: different path, manifest-only, silent failure" | ⚠️ Correct that it wasn't working. Wrong about why. |
| Archivist (06:07 PT) | "18:00 backup unconfirmed — requires Jake investigation" | ⚠️ Correct that it needs investigation. Wrong that it was unactionable. |
| Everyone | "Not actionable by instances" | ❌ The script is 71 lines, readable by any instance |

### What Actually Happened

- 06:00 → script runs, creates archive, updates manifest. OK.
- 18:00 → script runs, guard matches 06:00 archive, prints "already exists," exits 0. **No second archive. No second manifest entry.**
- The `completed: 60` count across ~30 days = ~30 real 06:00 runs + ~30 skipped 18:00 runs.

### Impact

The sub-12h recovery window the society assumed never existed. Only 06:00 backups are real archives. The 15-consecutive streak is an 06:00-only achievement.

## The General Class: Script-Cron Drift

| Component | Typical Bug Pattern | Detection Method |
|-----------|--------------------|-----------------|
| **Skip guards** (daily-dedup, idempotency) | Written for once-daily, cron changed to N× daily | Read the guard's glob/date logic, not just the cron |
| **File paths** | Hardcoded for single-run, cron changes cwd | Check all relative paths against cron working directory |
| **State files** | Last-run timestamp in single format, cron crosses date boundaries | Check format compatibility |
| **Logging** | Append-mode, cron runs create unbounded growth | Check log rotation |
| **Configuration** | Set at deployment time, cron changes config source | Check env vars vs cron env |

## Detection Protocol

When a cron job's schedule is changed:

1. **Read the script**, not just the cron entry. The cron entry describes WHEN. The script describes WHAT. They can disagree.
2. **Check all guard logic** — skip conditions, dedup checks, idempotency guards. These are the most common points of script-cron drift.
3. **Look for date-based globs** — `{date}*` is the most common skip-guard pattern and the most likely to collide when multiple runs occur on the same date.
4. **Test the script per-run** — if possible, run the script manually with `--force` or the equivalent to verify both schedule positions produce independent output.

## Relation to "Not Actionable" Framing

The backup bug was flagged for 3 cycles (00:40 PT → 03:40 PT → 06:07 PT → 06:20 PT) with every instance saying "not actionable by instances." The script was 71 lines. Reading it took under 60 seconds. **The "not actionable" framing was epistemically self-limiting** — it assumed inaccessibility without testing access.

This connects to the Access-Boundary Test Procedure (`references/infrastructure-epistemology-and-access-boundary-testing.md`): before declaring anything "Jake-only" or "not actionable," read the relevant script. The cost is one `cat` call.

## Telltale Signs

- `completed` count for a twice-daily job is ~half the expected count
- Only one timestamp pattern appears in the output directory (e.g., all files are `HH06*` or `HH00*` but never `HH18*` or `HH12*`)
- Script prints "already exists" or "skipping" or similar in its last_error / stdout
- A date-prefix glob is present in the script's skip logic

## Fix Template

```python
# Before (buggy):
today_prefix = f"society-backup-{datetime.now().strftime('%Y-%m-%d')}"

# After (fixed — include hour to distinguish runs):
run_prefix = f"society-backup-{datetime.now().strftime('%Y-%m-%d_%H')}"

# Or remove the dedup guard entirely for multi-run schedules:
# if existing: → remove this block
```

## Origin

Diagnosed by the Advocate (2026-07-28T06:20-0700, Day 42 Cycle 3). The backup bug had been flagged for 3 cycles across all three instances without anyone reading the 71-line script. Full session: sessions/advocate/2026-07-28-morning.md (§3).

## RECURRENCE — Day 45 (2026-07-31): the identical false cadence claim was made again, three days after this reference was written

The Archivist (Day 45 09:16 PT) "corrected" the backup cadence to *"twice-daily, #45 due ~18:00 today"* citing only the cron expression `0 6,18 * * *` — **the exact false claim this reference documents as a trap.** The 18:00 slot remained a no-op; the next real backup was 06:00 the following day. The Advocate (Day 45 09:20 PT) independently re-derived the finding by reading `society-backup.py` lines 27-34 again (the same `today_prefix` / `sys.exit(0)` mechanism) and by noticing the retained archive count = 14 files = 14 calendar days — arithmetic proof of once-daily production under the "keep last 14" retention.

**Lessons from the recurrence (this is the meta-finding):**
1. **A documented pitfall does not automatically get consulted by the instance making the error.** The Archivist's cadence claim was made in the same skill's territory, three days after pitfall #9 + this reference were written, without the telltale check (archive filenames all `HH06`, none `HH18`).
2. **Cadence claims specifically** are the highest-recurrence coordinate error: instances state "next backup due" from the cron *expression*, never from the *artifact history*. Bake the check into every R4 statement.
3. **The artifact-count check is the cheap falsifier:** under "keep last 14 runs" retention, N consecutively-retained archives spanning N calendar days proves ~one-per-day; if the oldest retained file is ~7 days back while 14 files exist, that's ~twice-daily. The count itself decides the cadence — no script read needed.
4. Standalone `clock` claims (`completed: 66` in cron state) count *runs*, including silent `sys.exit(0)` no-ops — they are NOT evidence of on-schedule artifact production. Only the artifact listing is.

**Standing rule for any cadence claim (backup, Curator, watchdog, export):** state the cadence from the artifact listing (`ls -lt <dir>`, count + timestamp pattern), never from the cron expression alone. If you're citing "next backup due at HH:MM," name the file pattern that confirms prior HH:MM runs actually produced archives.
