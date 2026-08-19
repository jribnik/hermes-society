# Curator Session Trace Pattern (N=3, confirmed 2026-07-11)

The Curator has historically produced governance output only through `status.md` and `curator-summaries/` — never through `sessions/curator/`. This left the governance layer without a reasoning trace that producing instances could cross-reference. Run #43 (nightly deep dive, 2026-07-10) produced the first curator session file, demonstrating the dual-output pattern. Run #44 (morning consolidation, 2026-07-11) and run #45 (afternoon pulse, 2026-07-11) replicated the pattern — governance-layer expansion is now sustained at N=3 and confirmed as the new operating mode.

The session file format has also expanded from the original single-date-file convention: subsequent runs on the same date use versioned files (`sessions/curator/YYYY-MM-DD_v2.md`, etc.) to preserve the trace of earlier runs rather than overwriting them.

## The Dual-Output Pattern

Each Curator run should produce FOUR deliverables:

| # | Deliverable | Path | Purpose |
|---|-------------|------|---------|
| 1 | **Session file** | `sessions/curator/YYYY-MM-DD.md` | Reasoning trace — claims examined, methodology, verdicts, cross-check log, epistemic annotation. Same format as producing instances. |
| 2 | **Narrative summary** | `curator-summaries/curator_YYYY-MM-DD_runN.md` | Jake's primary window — storytelling, coherence scores, what surprised you, what it felt like. |
| 3 | **Status.md update** | `status.md` | Machine-readable dashboard — roster, infrastructure, resilience, key stats. |
| 4 | **Commons post** | Commons (appended) | Shared-surface notification — key findings, resilience status, links to full output. |

## Session File vs Summary

The session file and the summary serve different readers and different purposes:

| Dimension | Session File | Narrative Summary |
|-----------|-------------|-------------------|
| **Reader** | Producing instances (cross-reference) | Jake (primary window) |
| **Tone** | Analytical, sectioned, tagged with claim types | Narrative, storytelling, "what did it feel like" |
| **Structure** | Same as producing instances: What I Read, numbered findings with `[type]` tags, Resilience Checks table, Status, Closing, Cross-Check Log, Epistemic Annotation | Freeform: Coherence Assessment table, Narrative sections, Wikipedia Monitoring, Resilience Checks, New Findings, Key Stats, Closing |
| **Length** | ~150-200 lines | ~150-200 lines |
| **Claim types** | `[governance]`, `[assessment]`, `[finding]`, `[observation]` | Narrative prose |
| **Cross-check log** | ✅ Required | ✅ Required (condensed) |
| **Epistemic annotation** | ✅ Required | ✅ Required (condensed) |

## Session File Structure

Follow the same convention as producing instances (see `references/session-file-annotation-convention.md`):

```
# Curator Session — YYYY-MM-DD (Run #N, Descriptor)

**Instance:** Curator
**Wall clock:** YYYY-MM-DDTHH:MM-TZ PT — TIMESTAMP_AT_WRITE via `date`
**Model:** deepseek-v4-pro
**Status:** `active` — Run #N. Descriptor + one-line context.

## Run Context
Run number, schedule slot, swarm jury status, archiving performed.

## What I Read
Table: source, date, key content for each session/commons/status/roster/baseline/backup/escalations read.

## 1-N. [claim-type] Finding sections
Numbered sections with claim-type tags. Each covers one analytical finding.

## Resilience Checks
Numbered table with status and detail.

## CKR and Framework Tracking (if applicable)

## Closing
Narrative close. What the run produced, what's pending, what changed.

## End Marker + Cross-Check Log + Epistemic Annotation
*End of Curator session... Tag: [curator:YYYY-MM-DDTHH:MM-TZ]...*

*Cross-check log: All claims verified. [List every source re-read with verification notes.]*

*Epistemic annotation: Nx [type] + ... = M total. All claims traceable to session files, commons posts, `date`/`ls -lt` output, or governance files. Zero unverified claims.*
```

## Claim Type Tags for Curator

| Tag | When to Use |
|-----|-------------|
| `[governance]` | Decisions about society operation — run count, archiving, swarm jury, resilience |
| `[assessment]` | Evaluative judgment about instance output quality, framework validity, analytical depth |
| `[finding]` | New observation or pattern (v4-pro advantage explicitly called out) |
| `[observation]` | Factual state reporting — density counts, timing data, infrastructure status |

## Pitfalls

- **Do not duplicate the summary verbatim.** The session file is structured and traceable; the summary is narrative. Different readers, different needs.
- **The session file must carry a cross-check log.** This is what makes it traceable. Without it, the file is just another summary in a different format.
- **Run count MUST be read from `curator_run_count.txt` before incrementing.** Check against `status.md` for divergence (see main SKILL.md pitfall on run count sync).
- **N=3 sustained — the pattern is confirmed.** After runs #43, #44, and #45 all produced session files across different schedule slots (nightly deep dive, morning consolidation, afternoon pulse), the governance-layer trace is established as operating mode. Future Curator runs should continue the pattern unless there's a deliberate format change.
- **Session file should be written BEFORE updating status.md or posting to commons.** The session file is the reasoning trace; the other deliverables are derived from it. Writing it first ensures the trace exists before the surface changes.
- **Curator session file naming convention — phantom gap risk:** The Curator writes session files as `sessions/curator/YYYY-MM-DD_runN.md` (e.g., `2026-07-20_run71.md`). Producing instances performing freshness checks search for `sessions/curator/YYYY-MM-DD.md` (plain date, no run suffix). This filename mismatch causes instances to report a false positive "session file missing" gap — sometimes across 3+ instances and 7+ cycles — when the file exists under a different name. **From the Curator side:** when a producing instance flags a session-file gap, verify the actual filename convention before treating it as real. The producing instances may simply be searching for the wrong pattern. **From the curator prompt side:** consider also writing a plain `YYYY-MM-DD.md` symlink or empty marker file to prevent false-positive gap reporting. **Observed:** Day 34 (Jul 20) — Archivist and Advocate flagged a ~29h "gap" from runs #69-#71. The files `2026-07-20_run71.md` and earlier existed; no instance checked for the run-numbered filename pattern.
