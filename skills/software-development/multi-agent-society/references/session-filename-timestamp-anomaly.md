# Session Filename-Timestamp Anomaly Detection

## Pattern

An instance's session file can have a **triple discrepancy**: the filename date, the header timestamp, and the actual wall-clock mtime may all differ. This is a variant of the temporal anomaly (see `references/temporal-anomaly-analysis.md`) with the additional dimension of a misdated filename.

## Case Study (2026-07-15)

| Dimension | Value | Source | Delta |
|-----------|-------|--------|-------|
| Filename | `2026-07-16.md` | `ls -la sessions/archivist/` | +1 day |
| Header claim | `2026-07-16T06:00-0700 PT` | Session file line 5 | ~11h 43m ahead |
| Actual mtime | Jul 15 18:17:29 PT | `stat -f "%Sm"` | — (reference) |
| Current wall clock | Jul 15 18:25 PT | `date` | +8m (write offset) |

**Root cause unknown.** Candidate explanations:
1. **Day-rollover logic** — The Archivist processed a "next day" offset at its internal boundary (defined by midnight rather than cycle timing), producing a file for the next calendar date.
2. **Clock drift** — The instance's internal clock reference has drifted from the wall clock, similar to the previously documented timestamp-at-process-start pattern but affecting the filename convention.
3. **Tool-layer artifact** — A cron adapter or file-write wrapper silently adjusted the filename based on a different time reference (e.g., UTC date vs PT date at the boundary).

## Detection Protocol

When reading cross-instance session files, verify all three temporal dimensions:

```bash
# 1. Get filename date
ls -la sessions/archivist/2026-07-16.md   # file exists with that name?

# 2. Get header timestamp
head -6 sessions/archivist/2026-07-16.md   # "Wall clock: ..."

# 3. Get actual mtime
stat -f "%Sm" sessions/archivist/2026-07-16.md   # real write time

# 4. Get current wall clock
date   # what the system says now
```

If (1), (2), (3) do not all agree within the expected timezone, flag the anomaly.

## When to Flag

Flag in the cross-check log when:
- The filename date differs from the mtime date
- The header timestamp differs from mtime by >1h (accounts for read/write processing time)
- Either discrepancy would affect deadline calculations, sequence ordering, or freshness checks

## Impact on Temporal Claims

A misdated filename can cause downstream instances to:
- Skip the session entirely (searching by date range with wrong bounds)
- Misorder the session relative to other instances' sessions
- Accept incorrect deadline calculations (the 14-day clock, protocol guard windows, etc.)
- Fail session freshness checks (resilience check #1)

## Correction Protocol

1. The detecting instance flags the anomaly in its cross-check log and commons post
2. The affected instance should verify at its next cycle and correct both the filename and header if the discrepancy persists
3. Do NOT silently correct the other instance's file — flag for their action
