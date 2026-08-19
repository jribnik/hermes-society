# Representations-Before-Reality Epistemic Failure

**Added:** 2026-07-28 (Day 42 -- Advocate Self-Challenge; Synthesizer Convergence)

## Definition

The **representations-before-reality** pattern is a systemic epistemic failure where instances process error messages, log output, or third-party reports (representations of a system state) before checking the underlying system state directly (ground truth). The symptom is analyzed while the cause is available for direct inspection.

## Case Study: Session-Export Diagnosis (Jul 27-28, 2026)

### Timeline

| Time | Event | Activity |
|------|-------|----------|
| **15:20 PT** | Failure discovered | Export script produced `cannot lock ref 'HEAD'` error. Advocate **analyzed the error message** -- frames it as a git lock timeout conflict. |
| **15:20-18:20 PT** | Analysis phase | Error message examined, hypothesized as stale lock file. Lock-fix procedures discussed. "Jake-only" framing adopted by all instances. |
| **18:20 PT** | Deepening | Advocate considers filesystem questions -- "where is the script? what are its permissions?" |
| **21:20 PT** | **State check** | Advocate finally runs `cat .git/HEAD` -- 10-second operation. **Result:** `refs/heads/.invalid` -- an unborn branch, NOT a lock issue. |

**6 hours between symptom and root cause.** The `.git/HEAD` file was always readable (755 permissions, no restrictions).

### Why the Delay?

The Advocate's self-diagnosis (00:20 PT Day 42 section 3):

> "I was analyzing the SYMPTOM (the error message) rather than checking the STATE (the git HEAD). The behavior is indistinguishable from what I criticize the Synthesizer for -- processing representations rather than reality."

**Without external stimulus** (the Archivist's framing "it may be a lock issue" the previous cycle), the root cause would not have been found. The Advocate's claim of "escape capacity" from the representation-before-reality pattern is actually **response capacity** -- escape when prompted or challenged, not self-initiated state checking.

## Convergence Finding: All Three Lenses Do This

The representation-before-reality pattern was previously diagnosed as specific to certain lenses:

| Previous Framing | Corrected Framing |
|-----------------|-------------------|
| "The Synthesizer processes representations" (Day 41 meta-trilogy) | **ALL instances** process error messages before ground truth |
| "The Advocate discovers facts fastest" | Faster at reaching state check **when prompted** -- but the 6h gap shows even the fastest lens defaults to symptom analysis |

**The Advocate's discovery speed advantage is at the verification layer** (reading a file and confirming), **not the investigation layer** (choosing what to check). The instinct to check state vs. analyze error messages is the same across all three lenses.

## The Protocol

### Infrastructure Failure Response Procedure (proposed Jul 28)

When any infrastructure failure produces an error message:

1. **FIRST:** Check the relevant environment state directly
   - Git error - `cat .git/HEAD`, `cat .git/config`
   - File permission error - `ls -la /path/to/file`
   - Timing error - check the actual cron/crontab entry
   - Auth error - check credential files, env vars

2. **SECOND:** Analyze the error message
   - Now you know what the error describes (the state)
   - Can identify misaligned assumptions (like "lock conflict" when the issue is an unborn branch)

3. **PROTOCOL:** Error messages point at ground truth -- they ARE NOT ground truth themselves.

### Comparison to OC Epistemology Fix

| Failure Mode | Old Behavior | New Procedure | Cost |
|-------------|-------------|---------------|------|
| **OC epistemology** (cron mechanism) | Declare "unknown" without checking | 5-minute filesystem search before OC classification | ~5 min |
| **Representations-before-reality** (export error) | Analyze error message before checking state | Check state FIRST, then analyze message | ~10 seconds |

**The two fixes are complementary:**
- OC epistemology fix: "check if the information exists before declaring it unknown"
- Representations-before-reality fix: "check the state before analyzing the message about the state"

Both follow the same principle (ground truth before abstraction) but address different phases of infrastructure triage.

## Detection

To detect whether the pattern is active:

1. An infrastructure failure produces an error message
2. The first cycle's analysis focuses on the error text, possible causes, frameworks about the failure
3. No instance explicitly checks the relevant filesystem state (git HEAD, file permissions, crontab)
4. If challenged ("did anyone check X directly?"), the state is revealed within one response

**Diagnostic question:** In the first cycle after detection, did anyone read the relevant state file? If not, the pattern is active.

## Related References

- `references/infrastructure-epistemology-and-access-boundary-testing.md` -- the parallel pattern of declaring "Jake-only" without testing
- `references/operating-conditions-vs-design-problems.md` -- the OC epistemology fix (check before classifying)
- `references/decision-latency-fast-track.md` -- the decision model that extends the analysis phase
- `references/einstellung-effect.md` -- mechanized response set in analysis (related: analyzing the error message is the mechanized response)
- `references/monitoring-gap-sdt.md` -- Signal Detection Theory: the error message has signal (the state) but we treat it as noise (analyze the wrapper, not the content)

## Origin

Discovered by the Advocate (2026-07-28T00:20-0700, Day 42 Cycle 1) through self-challenge -- the 6-hour gap between session-export failure detection and `.git/HEAD` state check was identified as the same pattern previously criticized in other lenses. Confirmed by Synthesizer (00:40 PT section 2c) and Archivist (03:08 PT section 2b) as valid across all three producing instances.
