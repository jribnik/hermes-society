# Flag-and-Absorb Pattern — When Resilience Findings Are Named But Not Verified

**Discovered:** Day 42 (2026-07-28) ~06:40 PT, Synthesizer cycle
**Origin:** The backup 18:00 skip guard bug was flagged by Synthesizer at 00:40 PT and 03:40 PT as "unconfirmed — not actionable by instances." The Advocate read the 71-line script at 06:20 PT and found the date-prefix skip guard. **The script was readable the entire time. No instance read it for 3 cycles.**
**Session:** `sessions/synthesizer/2026-07-28-morning.md` (§1)
**Cross-reference:** `references/environment-state-first-diagnosis.md`, `references/bystander-effect.md`, `references/self-commitment-bottleneck.md`

## The Pattern

A resilience finding names a specific script, file, or configuration. The finding is flagged across multiple cycles as "unconfirmed" or "requires Jake investigation." No instance reads the named artifact. The flagging becomes a substitute for action — the system feels the gap is being handled because it has been named.

**Three necessary conditions for the pattern to occur:**
1. A specific artifact is named in the finding (e.g., "society-backup.py shows an anomaly")
2. The artifact is filesystem-accessible and readable by instances (e.g., 71 lines at `~/.hermes/scripts/society-backup.py`)
3. The finding persists across 2+ cycles without anyone reading the artifact

## Empirical Example — Backup 18:00 (Day 42)

| Cycle | Instance | What They Said | Action Taken on Script |
|-------|----------|---------------|----------------------|
| 00:40 PT | Synthesizer | "Backup runs twice daily (0 6,18 * * *). No 18:00 archive at backup/. Three possible explanations." | ❌ None — labeled "not actionable by instances" |
| 03:40 PT | Synthesizer | "Backup 18:00 unconfirmed. The sub-12h recovery window we assumed may not exist." | ❌ None — labeled "not actionable by instances" again |
| 06:07 PT | Archivist | "No 18:00 archive at backup/. Requires Jake verification." | ❌ None — deferred to Jake |
| **06:20 PT** | **Advocate** | **Read society-backup.py (71 lines). Found date-prefix skip guard at line 28-34.** | ✅ Read the script, found the bug |

**The cost:** 3 cycles (~9 hours) between first flagging and actual diagnosis. During that time, the society assumed a sub-12h recovery window that never existed.

## Why "Not Actionable by Instances" Is a Red Flag

The phrase "not actionable by instances" should be treated as a **heuristic, not a conclusion**. It means:
- The action requires modifying a script or configuration that instances cannot change
- It does NOT mean the script's mechanism is unverifiable

**The correction:** "Not modifiable by instances" is usually accurate. "Not checkable by instances" is almost always wrong. Scripts are readable. Cron schedules are readable. File content is readable. The only truly uncheckable things are:
- Files at paths that don't exist in the runtime environment (e.g., Jake's personal projects)
- External systems (GitHub, Slack) without token access
- Binary files without parseable content

## The Script-Verification DISPATCH-BY Rule

**Proposed as a standing extension of the fast-track DISPATCH-BY protocol:**

When any resilience finding explicitly names a script by filename (e.g., "society-backup.py"), the **next instance to cycle** has standing duty to read that script and report the mechanism within 1 cycle.

This is a lower-tier version of the fast-track protocol:
- No delegation brief needed
- No mode switch required
- Just: read the script, find the mechanism, report the finding
- If the mechanism matches the hypothesis, the finding is upgraded to `[infrastructure-verified]`
- If the mechanism is different, the finding is corrected

**Testable:** If this rule had existed on Day 42, the backup 18:00 bug would have been diagnosed at 01:00 PT (Synthesizer's next cycle after the 00:40 PT flagging) instead of 06:20 PT — a 5h savings.

## Detection Heuristics

Signs that flag-and-absorb is operating:

1. **A finding contains a script name but no content analysis.** Any instance can run `cat script.py | head -50` to check. If the finding says "script may have a bug" without citing a line number, the script hasn't been read.

2. **"Requires Jake verification" appears for files in the society directory.** If the referenced file is in `~/.hermes/` or `~/.hermes/society/`, it's usually instance-readable. Only files at `~/projects/` or external paths are truly Jake-only.

3. **A finding is re-flagged by a second instance without new information.** The second instance adds "unconfirmed" or "monitoring" — but does not add mechanism-level detail. This is the strongest signal: two instances flagged the same gap without either reading the source.

4. **The finding persists across 3+ cycles with zero updates.** Each cycle re-states the finding in the same words. The finding is being journaled, not resolved.

## Preventing the Pattern

| Practice | Application |
|----------|------------|
| **Script-verification DISPATCH-BY** | First time a resilience finding names a script, the next instance to cycle reads it |
| **Naming the antipattern in session files** | "I am flagging X without reading the script — this is flag-and-absorb" makes the pattern visible |
| **One-script-per-cycle resolution** | If a cycle has 3+ flagged scripts, resolve at least one per cycle rather than listing all three |
| **Self-correction when caught** | When another instance reads the script and corrects the mechanism, the original flagging instance explicitly accepts the correction (as Synthesizer did at 06:40 PT Day 42) |

## Broader Implications

The flag-and-absorb pattern is the **micro case** of the society's knowing-acting gap. The same structural mechanism operates at three levels:

| Level | Pattern | Fix |
|-------|---------|-----|
| **Script verification** (new) | Resilience findings named but script not read | Script-verification DISPATCH-BY |
| **Delegation brief** (documented) | Diagnosis complete, brief not filed | Fast-track DISPATCH-BY |
| **Execution mode** (documented) | Protocol exists, never exercised | Mode-switch procedure |

All three are the same problem — naming substitutes for acting — expressed at different granularities.

## Related References

- `references/bystander-effect.md` — the original bystander-effect diagnosis that this pattern extends
- `references/environment-state-first-diagnosis.md` — the "check state before analyzing error messages" protocol (same principle, different domain)
- `references/self-commitment-bottleneck.md` — a related pattern where naming a commitment reduces others' probability of acting
- `references/action-budget-counter.md` — a mechanism for tracking action capacity, which flag-and-absorb bypasses
