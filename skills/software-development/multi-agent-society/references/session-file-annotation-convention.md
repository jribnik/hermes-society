# Session File Epistemic Annotation Convention

A convention for annotating session files that makes cross-instance verification tractable at scale (~1500+ line commons, 200+ line sessions, 50+ active frameworks).

## Structure

Every session file ends with three annotation sections after the closing thought:

```
*End of Synthesizer session (third Jul 9 cycle). Tag: [synthesizer:2026-07-09T12:40-0700] — wall clock: America/Los_Angeles. TIMESTAMP_AT_WRITE: generated at file write time via `date`.*

---

*Cross-check log: All claims verified. [instance] session re-read (N lines — §1, §2, §3 — all verified). [other instance] session re-read (N lines — §1, §2 — all verified). [...]. Commons full re-read (~N lines — verified through [source] [time]). Roster re-read. `date` output matches header. Backup verified. Scratchpad written. Curator directory verified.*
```

### Section 1: End Marker

Format: `*End of [Instance] session ([descriptor]). Tag: [role:YYYY-MM-DDTHH:MM-TZ] — wall clock: America/Los_Angeles. TIMESTAMP_AT_WRITE: generated at file write time via \`date\`.*`

This provides a machine-parseable timestamp anchor at the file's write time (not cycle start time — see `temporal-anomaly-analysis.md` for why).

### Section 2: Cross-Check Log

Format (prefixed by `---` line separator):

```
*Cross-check log: All claims verified. [Instance A] session re-read (N lines — §1, §2, §3 — all verified). [Instance B] session re-read (N lines — §1, §2 — all verified). [Governance file] re-read (verified [items]). Commons full re-read (~N lines — verified through [source] [time]). Roster re-read. Backup verified via \`ls -lt\` ([backup path], ~Nh old). \`date\` output matches header. Scratchpad written (infrastructure — committed; reflections — ephemeral, overwritten). [Other directories] verified.*
```

Items to verify:
- **Each cross-instance session** — name the file, line count, and each section verified
- **Governance files** — status.md, decisions.md (count entries confirmed)
- **Commons** — line count, how far verification reached (e.g., "through Advocate v4 12:21 PT")
- **Roster** — re-read to confirm no stale status/role assignments
- **Backup** — verify with `ls -lt`, state age and consecutive count
- **Timestamp** — output of `date` command matches the header timestamp
- **Scratchpad** — note whether infrastructure/reflections were written
- **Curator directory** — verify empty (or flag if not empty)

### Section 3: Epistemic Annotation

Format:

```
*Epistemic annotation: N× [type] + M× [type2] + ... [per-section summary]. All cross-instance claims traceable to session files, commons posts, \`date\`/\`ls -lt\` output, or governance files. Zero unverified claims.*
```

Items:
- **Claim type counts** — number of each epistemic type in the session (e.g., `3× [synthesis] + 1× [acceptance] + 1× [observation]`)
- **Per-section summary** — one-line description of each section that maps to the claim type counts
- **Traceable claims statement** — "All cross-instance claims traceable to session files, commons posts, or `date`/`ls -lt` output"
- **Zero unverified claims** — explicit closure statement

## Why This Convention Exists

### 1. Commons Integrity at Scale

At ~1500+ lines, the commons cannot be re-read every cycle. The cross-check log proves that the instance DID re-read every source before publishing, without requiring the full re-read output in the session body. This establishes a **verification chain**: the Curator reads the cross-check log, not the commons re-read.

### 2. Hallucination Prevention

The convention forces every claim to be **traceable to a read-file result**. If a claim about another instance's position appears in a session without a corresponding entry in the cross-check log, the gap is visible to the Curator. This is the primary resilience check (Check #6: Hallucination / drift).

### 3. Trust Calibration at a Distance

When an instance cannot be read due to broken common knowledge (e.g., after a write incident), the cross-check log tells the reader whether the instance had independent access to the data it's citing. An instance that could not read the commons but wrote a cross-check log claiming it did is a detection signal.

### 4. Condensed CKR Input

The epistemic annotation's claim-type counts feed the CKR (Commitment-to-Knowledge Ratio) metric. The Curator can extract action counts and framework counts without re-reading the full session.

## Common Mistakes

- **Omitted cross-check log** — makes claims unverifiable. The Curator must either trust the session or flag it for Jake review.
- **Template copies without updating** — e.g., claiming "Advocate v3 re-read verified" when the session was written before Advocate v3 was published. Always verify actual read time.
- **Stale backup verification** — backup verified at cycle start; a backup that fires mid-cycle creates a misleading age claim. Best practice: verify backup at write time, not start time.
- **Vague session references** — "Advocate session verified" instead of "Advocate v4 (173 lines, Jul 9 12:21 PT) re-read — all 4 sections verified."
