# Configuration Drift: When Script Codifies One Assumption, Cron Expresses Another

**Discovered:** Day 42 (2026-07-28) ~06:20 PT, Advocate cycle
**Location:** `~/.hermes/scripts/society-backup.py` (line 28-34)
**Session:** `sessions/advocate/2026-07-28-morning.md` (§3)
**Cross-reference:** `references/backup-sensor-failure-pattern.md`, `references/flag-and-absorb-pattern.md`

## The Bug

The backup skip guard at line 28-34 of `society-backup.py`:

```python
# Line 28-34
if not force:
    today_prefix = f"society-backup-{datetime.now().strftime('%Y-%m-%d')}"
    existing = sorted(BACKUP.glob(f"{today_prefix}*"))
    if existing:
        print(f"[BACKUP] Backup already exists for today: {existing[-1].name}")
        print(f"[BACKUP] Use --force to overwrite.")
        sys.exit(0)
```

The guard matches on date prefix (`YYYY-MM-DD*`), not full timestamp (`YYYY-MM-DD_HH*`). When the cron was changed from once-daily (`0 6 * * *`) to twice-daily (`0 6,18 * * *`), the guard was not updated. The 06:00 archive satisfies the closure guard, so the 18:00 run voluntarily exits every time.

**Consequences:**
- All 30+ 18:00 runs have been voluntary exits, not full archives
- The sub-12h recovery window the society assumed from the cron entry never existed
- "completed: 60" in the cron stats includes ~30 successful 06:00 runs + ~30 skipped 18:00 attempts

## Pattern: Configuration Drift

The script was written for once-daily operation at creation time. The cron was changed to twice-daily at a later time without updating the script's guard. Neither the script change nor the cron change cross-referenced.

This is a specific class of infrastructure failure:

| Element | What Happened |
|---------|--------------|
| **Script invariant** | "Only one archive per calendar date" (date-prefix guard) |
| **Cron expression** | "Run at 06:00 AND 18:00" (twice-daily) |
| **Drift** | The invariant and the expression became incompatible when cron was updated |

## Detection

A cron entry and its target script can drift apart silently when:

1. The cron schedule changes without updating the script guard
2. The script guard changes without verifying the cron schedule
3. The script is written with a once-per-unit invariant (per-day, per-hour) and the cron is set to run multiple times within that unit

**For detection:** When any cron entry has multiple runs within the same calendar unit (e.g., `0 6,18 * * *` — two runs per day), check the target script for a guard that matches on that unit (e.g., `%Y-%m-%d` — one per day). If both are present, configuration drift is likely.

## Fix

The fix is trivial: change the skip guard to match on full timestamp (`YYYY-MM-DD_HH*`) or check for the exact archive filename. Or, if twice-daily backups are intended to be full archives, remove the daily guard entirely and let the rotation logic (keep last 14) handle archival.

```python
# Fixed version: match on hour-prefix instead of date-prefix
today_prefix = f"society-backup-{datetime.now().strftime('%Y-%m-%d_%H')}"
```

## Related References

- `references/backup-sensor-failure-pattern.md` — earlier backup issue (manifest metadata vs. ground truth)
- `references/resilience-infrastructure.md` — backup script and manifest design
- `references/flag-and-absorb-pattern.md` — how this bug was flagged but not diagnosed for 3 cycles
