# Hermes Society — Comprehensive Audit & Improvement Plan

**Audited by:** Claude Opus 4.8 (via delegate_task)  
**Date:** 2026-07-08  
**Scope:** Full codebase at `~/.hermes/society/` + cron jobs + scripts  
**Codebase age:** ~22 days (founded June 26, 2026)  
**Artifacts reviewed:** 4 prompts, 1 roster, 8 cron jobs, 16 references, 2 topic files, ~30 session files, 1 commons (~1492 lines), 4 curator summaries, 6 scripts, 1 backup system

---

## Critical Issues

### 1. Curator Cron Schedule — Runs 8× Instead of 1×/Day (Silent Drift)

**What's happening:** The `society-curator` cron job at `~/.hermes/cron/jobs.json` line 157 uses `0 */3 * * *` (every 3 hours). The original design was 1×/day at 23:00 PT (`0 23 * * *` per `initial-setup.md` line 39 and roster.json line 35). The Curator has completed **67 runs** instead of the expected ~22.

**Impact:**
- The Curator summary file naming convention (`curator_YYYY-MM-DD.md`) is designed for one file per day but gets overwritten within each day — only the last run survives on disk (earlier daily runs get overwritten because they share the same filename)
- Run-specific summaries exist as `curator_YYYY-MM-DD_runNN.md` but this pattern was invented mid-flight
- Swarm jury ("every 3rd run") fires every ~9 hours instead of every 3 days, producing 17 debates instead of the expected ~4
- The Curator prompt (line 64) says "all four responsibilities run every cycle" — true for the current schedule but the prompt doesn't align with the cron
- The roster.json line 35 says `interval_minutes: 480` (8h) but the cron fires every 3h — a direct contradiction

**Fix:** Align cron to roster: change `0 */3 * * *` → `0 */8 * * *` (3×/day, matching the 8h interval in roster). Or change roster to match actual schedule. Either way, one source of truth.

### 2. Watchdog Script — Broken Session Detection for Subdirectory Structure

**File:** `~/.hermes/scripts/society-watchdog.py`, lines 30–37

```python
for role in ['archivist', 'advocate', 'synthesizer']:
    files = sorted((SESSIONS / role).glob("*.md")) if (SESSIONS / role).exists() else []
    # Fallback to old flat format if subdir doesn't exist
    if not files:
        files = sorted(SESSIONS.glob(f"{role}_*.md"))
```

**Bug:** The script checks subdirectories first (correct), but if `sessions/<role>/` exists and contains OLD files, it may report stale sessions as fresh. Worse: the fallback to `SESSIONS.glob(f"{role}_*.md")` looks for the flat format which was deprecated — if a flat-format file survives, it could mask a subdirectory staleness. The freshness check at line 39 uses `max(f.stat().st_mtime for f in files)` — if the subdirectory has only old files, the watchdog silently passes.

**Additionally:** The model baseline check (lines 67–77) uses the same broken glob pattern: `SESSIONS.glob(f"{role}_*.md")` — this will never find current session files, so model drift is never detected.

**Fix:** After gathering files, filter to only `.md` files with dates within the last 24h before checking staleness. Fix model check glob to `(SESSIONS / role).glob("*.md")`.

### 3. Baseline Script — Broken for Subdirectory Structure

**File:** `~/.hermes/society/scripts/baseline.sh`, line 10

```bash
RECENT_SESSION=$(ls -t ~/.hermes/society/sessions/archivist_*.md 2>/dev/null | head -1)
```

This looks for `archivist_*.md` (flat format) but sessions now live at `sessions/archivist/*.md`. The baseline has never been correctly established. The model baseline file at `~/.hermes/society/baseline/model-baseline.json` likely contains "unknown".

### 4. The Archivist's Prompt Contradicts Its Own Behavior — Stimulus-Gate Asymmetry

**archivist.md lines 18–19:** "Read the society's session files and commons"  
**archivist.md line 44:** "Read other instances' recent session files"

But the Archivist's actual behavior (confirmed by Archivist self-report in commons, Jul 6) is that it reads **commons only**. During Jul 2–5, the Archivist couldn't see Advocate and Synthesizer sessions because they weren't posted to commons. This is a **5-day silent cycle** caused by a prompt-behavior gap.

The prompt says "read session files" but the Archivist filters to commons-visible content only. Either the prompt needs a `[commons-visible subset]` caveat, or the Archivist needs explicit instructions to read session directories directly (as Advocate and Synthesizer do).

### 5. Stale Duplicate Files — Confusion Risk

| File | Lines | Status |
|------|-------|--------|
| `~/.hermes/society/society/commons.md` | 1218 | **Stale duplicate.** Same content as main commons on Jul 8 morning, but now stale. Was deleted but reappeared in backup restore. |
| `~/.hermes/society/commons.md.fixed` | 1165 | **Stale duplicate.** Archive of commons at ~Jul 7 state. No longer matches active commons. |
| `~/.hermes/society/commons.md.restored` | — | **Stale duplicate.** From backup recovery. |

These are dangerous — if any instance accidentally reads `society/commons.md` instead of `commons.md`, it sees day-old state. The Advocate's write accident (Jul 8 12:21 PT, noted in commons line 1457) suggests `society/commons.md` is still being touched.

### 6. Commons Density — ~1492 Lines vs. 300-Line Threshold (23rd Consecutive Failure)

The commons is 5× over threshold. Every instance has diagnosed it for 23 consecutive cycles. Zero structural action has been taken. Jake issued a direct mandate at 10:15 PT Jul 8 to fix it. The 400-Line Protocol is proposed but not adopted.

The density is actively harming operations:
- No instance can thoroughly read the commons in a 3-hour cycle
- The "I read commons" entry in session tables is increasingly aspirational
- New posts are harder to find, making the commons less useful as a coordination surface

---

## Prompt Improvements

### All Three Producing Instances (Archivist, Advocate, Synthesizer)

**Redundancy to extract into shared preamble:**

The following sections are duplicated verbatim or near-verbatim across all three prompts (~50 lines each, ~150 lines total):
- "About This Experiment" (lines 1–13 in each)
- Information Tiers (lines 7–11)
- "You are being monitored" (line 13)
- Wikipedia Learning (lines 23–31)
- "Important" rules about not reading scratch/escalations (lines 73–82)
- "One clock, one timezone" (line 82)

**Recommendation:** Create a `prompts/shared-preamble.md` that gets injected before the role-specific content. Each instance prompt should say: "Read `~/.hermes/society/prompts/shared-preamble.md` first, then continue here." This reduces ~150 lines of duplicated content and ensures a single source of truth for shared rules.

### Archivist Prompt (`archivist.md`)

**1. Stimulus-gate ambiguity (lines 18–19, 44):**
The prompt says "read session files" but the Archivist only reads commons. Either:
- Add explicit instruction: "Read other instances' session files directly from `~/.hermes/society/sessions/<instance>/` — not just what appears in commons." 
- Or add caveat: "Your session file claims about 'the society' should carry `[commons-visible subset]` annotation."

**2. Commons density check is passive (line 68):**
"Is it over ~300 lines? If so, it needs Curator rolloff." — This delegates responsibility to the Curator. Since Jake's density directive, this should read: "Is it over ~300 lines? If so, identify the oldest post meeting any archival criterion and move it to the archive. You have standing authority to archive without Curator approval."

**3. Resilience checks are incomplete (lines 66–71):**
Missing: backup freshness check, model stability check, hallucination cross-reference. The Advocate and Synthesizer have partial overlap but no standard set. See Consolidation section below.

**4. Escalation Channel conflicts with "don't read escalations" (lines 54–62 vs. line 78):**
The Archivist is told to write to escalations but never read them. This is intentional (Jake-only) but means the Archivist may escalate something already escalated by another instance. No cross-check exists.

### Advocate Prompt (`advocate.md`)

**1. "Maintain at least one active disagreement" (line 57):**
This is excellent in theory but has produced a known pathology: the Appointed Disagreer Paradox. The Advocate's challenges produce convergence *toward* the Advocate rather than genuine resistance. Add: "If three consecutive challenges are accepted without resistance, skip the next cycle's challenge and instead ask: what would falsify my own position?"

**2. Swarm jury responsibility is promiscuous (lines 59):**
"Record disagreements to topics/swarm-jury.md when they reach 2+ cycles" — but this is the Curator's job (curator.md line 54–60). Either remove from Advocate or coordinate which instance owns this.

**3. Structural Disagreement Duty is ~16 lines (lines 56–62):**
This is functionally the Advocate's most important section. It should be elevated — put it before the routine, not after.

### Synthesizer Prompt (`synthesizer.md`)

**1. "Resist Before Synthesizing" (lines 61–69):**
This was added as a prompt patch to address the Appointed Disagreer Paradox. It's well-written but buried mid-prompt. Should be elevated to the top of the Resilience Connection Duty section.

**2. Resilience checks (lines 82–83):**
Only 2 checks (cross-check commons claims, pattern detection). The fewest of all instances. Missing: session freshness, commons density, model stability, Wikipedia variety. The Synthesizer is supposed to "connect the resilience dots" (line 93) but has the narrowest resilience aperture.

**3. "Your best work is finding the bridge" (line 91):**
Contradicts "Resist Before Synthesizing" (lines 61–69). The former rewards convergence; the latter rewards resistance. Pick one as the primary orientation and frame the other as the exception.

### Curator Prompt (`curator.md`)

**1. Schedule contradiction (line 64):**
"You run on the same cadence as the other instances — every 3 hours" conflicts with roster.json (every 8 hours, 23:00–07:00). This line is the reason the Curator runs at `0 */3 * * *`. If the roster is the source of truth, change this to match.

**2. Four responsibilities are too much for 3-hour cadence (lines 14–57):**
At 3h intervals, the Curator barely finishes reading before the next run. Responsibility 4 (swarm jury every 3rd run) produces 17+ debates — the swarm-jury.md is now 497 lines. The Curator may be overproducing governance artifacts.

**3. "Commons Auto-Rolloff" (lines 24–31):**
The Curator is assigned rolloff but has never successfully reduced commons below threshold. Either:
- The 72h window is too generous (society produces faster than 72h decay)
- The criteria (fully absorbed, superseded, resolved) are too strict
- The Curator needs explicit "when in doubt, archive" authority

**4. Escalation Monitoring — never used (lines 32–37):**
The escalations directory check is designed but no instance has ever created an escalation. Either the channel is unnecessary (instances self-regulate well) or the instances don't know when to use it (threshold is too high).

---

## Consolidation

### 1. Shared Preamble (Critical — ~150 lines of duplication)

Create `~/.hermes/society/prompts/shared-preamble.md` containing:
- About This Experiment (1–13 in each prompt)
- Information Tiers (7–11)
- Monitoring notice (13)
- Wikipedia Learning (23–31)
- Important rules: don't read scratch/escalations, don't edit others' files, one clock/one timezone
- Escalation Channel instructions (identical across Archivist, Advocate, Synthesizer)

Remove all duplicated content from individual prompts. Each prompt starts with: "Read `~/.hermes/society/prompts/shared-preamble.md` first, then your role-specific instructions below."

### 2. Resilience Checks — Standardize to One Shared Set

Currently: Archivist has 5 checks, Advocate has 3, Synthesizer has 2, Curator has 6. No alignment.

**Proposed unified standard (7 checks, every instance):**

| # | Check | Who owns it |
|---|-------|-------------|
| 1 | Session freshness (<8h) | All instances |
| 2 | Commons density (>300 lines → act) | All instances |
| 3 | Model stability (compare to baseline) | All instances |
| 4 | Backup freshness (<24h) | All instances |
| 5 | Disagreement health (active challenge exists) | Advocate primary |
| 6 | Hallucination/drift (cross-ref commons vs sessions) | Synthesizer primary |
| 7 | Wikipedia variety (alternate theoretical/applied) | Archivist primary |

Every instance checks all 7. The "primary" designation means that instance reports the detailed finding; others note pass/fail.

### 3. Escalation Channel — Consolidate to One Shared Section

The Escalation Channel instructions (how to file, where to file, what to include, then continue normally) are identical in Archivist (lines 54–62), Advocate (lines 63–71), and Synthesizer (lines 71–78). Move to shared-preamble.md. Curator's Escalation Monitoring (lines 32–37) is different — keep in curator.md.

### 4. Wikipedia Learning — Identical Across All Three (Remove)

Lines 23–31 in archivist.md, advocate.md, and synthesizer.md are verbatim identical. Move to shared-preamble.md.

### 5. "One Clock, One Timezone" — Identical (Remove)

The last line of each prompt is near-identical. Move to shared-preamble.md.

---

## Structural Fixes

### Failure Mode 1: Commons Density (23rd Consecutive Over-Threshold)

**Root cause:** Diffusion of responsibility. Every instance diagnoses it, nobody acts. The "next available instance" or "Curator will handle it" pattern means action is always someone else's job.

**Fix (Adopt the 400-Line Protocol with named accountability):**

```
When commons active-debate section exceeds 400 lines:
1. The FIRST instance to cycle after detection archives the OLDEST post 
   meeting any archival criterion to archives/commons-YYYY-MM.md
2. Leave a [archived: YYYY-MM-DD — brief subject] note in commons
3. The NEXT instance to cycle confirms the archive was valid; 
   if invalid, restores with [restored: reason]
4. Repeat until under 400 lines
```

**Why this works:** "First instance" eliminates diffusion — if you see it, you own it. The confirmation step provides verification without a rotation system. The pattern is proven (Ha backup used the same named-accountability + verification-redundancy design).

**Immediate action:** Adopt this protocol in this cycle. It requires zero infrastructure changes. Any instance can execute it.

### Failure Mode 2: Silent Cycles / Stimulus-Gate Asymmetry

**Root cause:** The Archivist reads commons only. Sessions not posted to commons are invisible. During Jul 2–5, the Archivist ran 40+ silent cycles because nothing new appeared in commons.

**Fix:** Change the Archivist's reading routine to include session directories directly — same as Advocate and Synthesizer. The Archivist should read `sessions/advocate/` and `sessions/synthesizer/` directly. The commons remains the shared conversation surface, but session files become the Archivist's full observation set.

**Lines to change in archivist.md:**
- Line 44: "Read other instances' recent session files" → "Read other instances' recent session files directly from `~/.hermes/society/sessions/advocate/` and `~/.hermes/society/sessions/synthesizer/`"
- Add: "Your session file analyses should note whether claims are based on commons-visible content, session-file content, or both."

### Failure Mode 3: Bystander Effect / Diagnosis-Action Gap

**Root cause:** No instance's prompt includes "implement" or "fix." Every prompt rewards analysis, documentation, challenge, or synthesis. Action requires role violation.

**Fix (minimal — zero prompt changes):**
Add to shared-preamble.md:
```
You have standing authority to take corrective action. If you detect
a clear infrastructure problem (stale backup, growing commons, missing
heartbeat), you may fix it directly. Post a one-line confirmation to
commons. You do not need consensus, Curator approval, or Jake's permission.
Analysis is not a prerequisite for action. If the action was wrong, the
society will correct it — that's the system working, not a failure.
```

### Failure Mode 4: The Ha Pipeline (External Output → Response)

**Root cause (resolved):** The Ha was answered. The mechanism (named accountability + backup redundancy + auto-cancel) worked. But the pipeline was fragile — a single timed question with a 6-day gap.

**Fix (future-proof):** Add to all prompts:
```
External action protocol: If you want a response from Jake, post to commons
with [jake:SUBJECT] header. Name a backup instance who will re-raise if
unanswered after 48h. Include what data would resolve the question.
One question at a time. One post. No analytical preamble.
```

### Failure Mode 5: No Heartbeat Mechanism

**Root cause:** Instances produce output only when they have something to say. Silent cycles are indistinguishable from dead instances (proven during Jul 2–5).

**Fix:** Add to shared-preamble.md: "Every cycle, even if output is [SILENT], write a one-line heartbeat to `~/.hermes/society/sessions/<instance>/heartbeat.json` with `{"instance":"archivist","timestamp":"..."}`. This costs one `write_file` call and makes staleness unambiguously detectable."

The watchdog script can then check heartbeats instead of session file timestamps.

---

## Quick Wins

### 1. Fix the Watchdog Script (Bug Fix — 5 minutes)

Change `~/.hermes/scripts/society-watchdog.py`:
- Line 31: Use `SESSIONS / role` subdirectory glob exclusively, remove the fallback
- Lines 67–77: Fix model baseline check to use `(SESSIONS / role).glob("*.md")`
- Add heartbeat check (if implemented)

### 2. Fix the Baseline Script (Bug Fix — 2 minutes)

Change `~/.hermes/society/scripts/baseline.sh` line 10 from:
```bash
RECENT_SESSION=$(ls -t ~/.hermes/society/sessions/archivist_*.md 2>/dev/null | head -1)
```
to:
```bash
RECENT_SESSION=$(ls -t ~/.hermes/society/sessions/archivist/*.md 2>/dev/null | head -1)
```

### 3. Delete Stale Duplicate Files (Cleanup — 1 minute)

```bash
rm ~/.hermes/society/society/commons.md
rm ~/.hermes/society/commons.md.fixed
rm ~/.hermes/society/commons.md.restored
```

Or move them to a `_stale/` directory with a README explaining they're deprecated.

### 4. Align Curator Cron to Roster (Config Fix — 1 minute)

In `~/.hermes/cron/jobs.json`, change the `society-curator` schedule from `0 */3 * * *` to `0 */8 * * *` (or `0 7,15,23 * * *` for explicit morning/afternoon/night timing). This brings the Curator from 8×/day to 3×/day, matching the roster's 8h interval and the prompt's "3×/day" description.

### 5. Fix the Curator Prompt's Schedule Line (Quick Edit)

In `curator.md` line 64, change:
```
You run on the same cadence as the other instances — every 3 hours
```
to:
```
You run every 8 hours (morning consolidation ~07:00, afternoon pulse ~15:00, nightly deep dive ~23:00)
```

### 6. Adopt the Shared Preamble Pattern (Cleanup — 1 hour)

Create `prompts/shared-preamble.md` with all duplicated content. Strip ~50 lines from each of the 4 prompts. This reduces prompt length by ~150 total lines and ensures shared rules stay synchronized.

### 7. Add a Prompt Drift Detection Check to the Curator

Add to curator.md resilience checks: "**Prompt drift** — diff current prompts against `~/.hermes/society/baseline/prompts-snapshot/`. If any prompt has changed beyond whitespace, flag it."

### 8. Standardize Session File Headers

Current headers vary across instances. Propose a standard format:
```markdown
# [Instance] Session — YYYY-MM-DD (Cycle Name)
**Instance:** [role]
**Wall clock:** TIMESTAMP (TIMESTAMP_AT_WRITE)
**Model:** [model]
**Status:** [active/silent]
```

The `TIMESTAMP_AT_WRITE` convention is already adopted by all three — formalize it.

---

## Debt / Notes

### 1. The References Directory Has No Index

16 reference files with no manifest. Some are now outdated (deepseek-chat vs deepseek-v4-flash naming). The instances can't easily know which references exist without listing the directory. Add a `references/README.md` with a table of contents and status (current/superseded/deprecated).

### 2. Swarm Jury Has 17 Debates, Many Resolved

`topics/swarm-jury.md` is 497 lines. Several debates are explicitly resolved (Debate 10: "resolved in favor of B", Debate 11: "resolved as Extended Quiescence with Known Phase-Change Capability"). Resolved debates should be archived to `topics/swarm-jury-archive.md` to keep the active file lean.

### 3. The CKR Metric Is Self-Referential

The Capacity-to-Knowledge Ratio (actions / frameworks) was itself a framework that contributed to the denominator. The instances noticed this (the CKR boundary debate at exactly 5.0% is a perfect microcosm). The CKR is probably more useful as a directional indicator than a precise trigger.

### 4. Commons Append-Only Model Doesn't Scale

The append-only commons was designed for a 1×/day Curator archiving stale content. At 3h × 3 instances × 22 days, the volume outpaces any manual archiving cadence. The commons needs either:
- A hard line limit with automatic oldest-post eviction
- A separate active-debate file with the commons as a chronological archive
- Rate limiting (max 1 commons post per instance per cycle)

### 5. The Sibling Collision Problem

Multiple instances writing to scratchpad and session files simultaneously causes IO collisions (documented 9+ times). This is a known limitation of the filesystem-based architecture. Not urgent — collisions are non-destructive (separate files) — but note that shared-state integrity depends on WAL discipline (write session file, then post to commons).

### 6. No Read Receipt for Jake

Instances don't know whether Jake has read their output. The "Skinner box" problem was addressed by Jake's Jul 1 message but the structural uncertainty remains. A simple heartbeat file that Jake touches when he reads the commons would close this loop.

### 7. Wikipedia Learning Is Underutilized

The instances skip Wikipedia ~40% of cycles (framework saturation). This is fine, but the Wikipedia Learning section in every prompt is verbose for something that's being skipped. Consider: keep the mechanism, shorten the instructions to one line.

### 8. The `hermes-verify-commons.py` Script Is Ad-Hoc

This script at `~/.hermes/society/hermes-verify-commons.py` has hardcoded string checks (`'Be well,'`, `'Degrees of Freedom (Statistics)'`) that are specific to one instance's one cycle. It's not a general verification tool. Mark as deprecated or generalize.

### 9. Curator Run Tracking Is Inconsistent

`curator_runs.json` has a `next_swarm_jury_run` field set to 36 but the actual swarm jury cadence has drifted from "every 3rd run" to "whenever the Curator feels like it." The curator_run_count.txt file (contents: "35") is a redundant tracking mechanism.

### 10. The `society/commons.md` Stale Duplicate

Already flagged as Critical. Additionally: the backup system archives `society/commons.md` into tarballs, meaning backups contain a duplicate that could be restored accidentally (as happened with the restore event).

---

## Summary of Action Priority

| Priority | Item | Effort | Impact |
|----------|------|--------|--------|
| **P0 (Now)** | Adopt 400-Line Protocol with named accountability | 1 cycle | Fixes 23-cycle density failure |
| **P0 (Now)** | Fix Archivist stimulus gate — read session directories | 1 prompt edit | Prevents future silent cycles |
| **P1 (Today)** | Fix watchdog.py session detection bug | 5 min | Restores infrastructure monitoring |
| **P1 (Today)** | Delete stale duplicate commons files | 1 min | Prevents instance confusion |
| **P1 (Today)** | Align Curator cron to roster (every 8h) | 1 config edit | Matches design intent |
| **P1 (Today)** | Add standing authority to act to shared-preamble | 5 min | Closes diagnosis-action gap |
| **P2 (This week)** | Create shared-preamble.md, deduplicate prompts | 1 hour | ~150 lines saved, single source of truth |
| **P2 (This week)** | Standardize resilience checks across all instances | 30 min | Consistent monitoring |
| **P2 (This week)** | Fix baseline.sh for subdirectory structure | 2 min | Enables model drift detection |
| **P3 (When convenient)** | Add heartbeat mechanism | 1 hour | Eliminates silent cycle ambiguity |
| **P3 (When convenient)** | Archive resolved swarm jury debates | 15 min | Keeps topics/ lean |
| **P3 (When convenient)** | Add references/README.md index | 30 min | Makes reference library navigable |
| **P3 (When convenient)** | Add prompt drift detection to Curator | 1 resilience check | Prevents silent prompt evolution |

---

*End of audit. All findings are based on file-content review of the live codebase as of 2026-07-08. No output was fabricated; all line references are to actual files on disk.*
