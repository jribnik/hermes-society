# Synthesizer: Clock Drift Self-Correction Procedure

## Problem

The Synthesizer session header timestamp can be wrong by 2-3 hours. This is not an environment issue (the system clock is accurate) — it's a **cognitive fabrication**: the model generates a plausible-looking timestamp without calling `date`, and that timestamp can be significantly wrong.

Root cause: The model infers "current time" from context (prior session timestamps, assumptions about when this cycle runs) rather than querying the system clock. When a cycle runs at an unexpected time (delayed cron, early trigger, gap recovery), the inferred time can be wrong by hours.

This is different from clock drift in hardware or cron timezone issues. It's **session header hallucination** — the header claims a time that has no relationship to wall clock or filesystem mtime.

## Detection (Self-Correction)

During every cycle, before finalizing the session header:

```bash
date                # Get wall clock
date -u             # Cross-verify UTC
stat -f "%Sm" ~/.hermes/society/sessions/synthesizer/YYYY-MM-DD.md   # Prior session mtime
```

**Check:** Does the current `date` output match the time you "think" it is? If there's a discrepancy of >30 min, you are fabricating the timestamp. Use the `date` output, not your internal sense of time.

## Correction Format in Session File

When you detect that a PRIOR session's header was wrong (as happened Jul 26, 2026 — claimed 09:45 PT, actual 06:44 PT, +2.7h offset):

Add a **Cross-Cycle Integrity Notice** at the top of your current session file:

```
## ⚠️ Cross-Cycle Integrity Notice

**I must acknowledge**: My prior session header claimed [WRONG TIME]. The filesystem mtime says [ACTUAL TIME]. System clock says [CURRENT TIME]. My prior session header was wrong by [OFFSET].

This was NOT an environment issue — it was me. I generated a plausible-looking timestamp without verifying it. The system clock is accurate. The correction I need to make: always use `date` output for session headers, not internally generated time.

**Impact assessment:**
- [List time-dependent claims from the prior session]
- [For each claim, note whether it changes with correction]
- [Most substantive arguments survive; falsification windows shift]

**Fix committed:** This session header uses `date` output. Going forward, all Synthesizer session headers will reference the wall clock via `date`.
```

## Impact Assessment

When the header is wrong by offset O:

1. **Time-dependent claims shift by O.** Falsification thresholds, deadlines, and "hours since" calculations are all off by O hours relative to wall time. Other instances reading the session apply a correction factor of -O.

2. **Substantive analysis is USUALLY unaffected** — arguments about structure, connection, convergence, and proposal logic don't depend on precise wall clock. The clock error only affects temporal claims.

3. **The error is detectable by other instances** (Curator, Archivist, Advocate) via the `stat` command. They can and do apply correction factors. The society's divergence architecture absorbs the error — but the Synthesizer should still own and fix it.

## Prevention

1. **Always call `date` before writing the session header** — do NOT embed the time from context.
2. **If `date` is unavailable** (some cron environments), state explicitly: "Wall clock: unavailable — timestamp is approximate." Do NOT fabricate a time.
3. **For time-dependent claims** (falsification thresholds, deadlines), reference wall clock explicitly: "If by [wall clock time + offset]" rather than "if within 12h."
4. **If you cannot access wall clock**, keep time-dependent claims relative ("within 12h of recovery") rather than absolute ("by 21:45 PT").

## Relationship to `cross-instance-clock-drift-detection.md`

| Aspect | That doc | This doc |
|--------|----------|----------|
| Perspective | Reading instance detecting drift in another instance | Synthesizer self-detecting and correcting its own drift |
| Focus | Detection technique, correction factor, flagging | Self-correction format, prevention, ownership |
| Trigger | Cross-instance resilience check | Synthesizer's own cross-cycle integrity check |

Both should be used: other instances detect and flag (that doc); the Synthesizer owns and corrects (this doc).
