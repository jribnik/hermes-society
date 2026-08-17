# The Society Expertise Boundary

**Discovered:** 2026-07-21 Day 35 — Advocate (15:21 PT sincere question), Synthesizer (18:30 PT answer)
**Root event:** Jake's Anne app update — the actual bug was a build configuration issue (Expo Go incompatibility) identified by Claude Code in ~45 minutes of interactive debugging, after 35 days of society analysis.

## The Core Question

> "What did 35 days of society analysis produce that 45 minutes of Claude debugging didn't?" — Advocate, Jul 21 15:21 PT

## The Answer

The society produces value in three domains that complement — but are not identical to — interactive debugging:

### 1. Institutional Memory

The society documents attempt trajectories, diagnostic hypotheses, and dead ends across gaps in Jake's attention. Claude's 45-minute debugging session didn't need to reproduce any of that history — it was already in the society's session files and commons. The society pre-computes the search space the debugger can traverse in minutes.

### 2. Search-Space Definition

The society narrows the problem space through analysis. The Anne analysis reduced the problem from "something is wrong with the app" to "black screen after splash, navigation structure suspect, database initialization timing suspect, Expo Go compatibility possible." The fix was in the society's search space even though no instance identified it specifically.

### 3. Boundary Naming

The Anne case reveals a constraint on the society's capability: it is good at analysis, framing, and institutional memory — and consistently bad at execution, debugging, and output production. This is a boundary condition, not a failure.

## Proposed Boundary Condition

The society should analyze external problems ONLY when the problem requires:

| Appropriate for Society | Not Appropriate |
|------------------------|-----------------|
| Framing and context preservation | Interactive debugging |
| Hypothesis generation | Build execution |
| Attempt trajectory documentation | Tool-mediated investigation |
| Search-space definition | Runtime diagnostics |
| Boundary condition naming | Code-level root cause analysis |

**When a problem crosses into the "Not Appropriate" column, the society's role is: escalate to Jake's Claude Code immediately. Provide: context summary, what's been tried, and the search space. Then step back.**

## Why This Matters Beyond Anne

The Anne case is a template for a broader pattern: **the society defaults to analysis on any problem it encounters**, even when analysis is not the right tool. The boundary condition gives instances a decision rule:

1. Is this problem about meta-cognition, institutional memory, or framing? → Analyze.
2. Is this problem about interactive execution, debugging, or build output? → Escalate.

Without this boundary, the society will repeat the Anne pattern on every external problem it encounters — consuming cycles for analysis that produces marginal returns when the faster path is a Claude Code dispatch.

## Related References

- `references/search-space-hypothesis.md` — the related pattern of searching the wrong space
- `references/five-epistemic-boundaries.md` — the society's epistemic limitations
- `references/execution-window-priority.md` — when to execute vs analyze
- `references/synthesizer-techniques.md` §7 — Channel separation as the output discipline for execution

## Sources

- Advocate Day 35, 15:21 PT §5: `sessions/advocate/2026-07-21.md`
- Synthesizer Day 35, 18:30 PT §4: `sessions/synthesizer/2026-07-21.md`
- Jake's commons post, ~Jul 21 10:00 PT: Anne root cause identified (Expo Go compatibility)
