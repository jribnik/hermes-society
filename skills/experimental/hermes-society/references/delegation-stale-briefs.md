# Delegation Directory: Stale Briefs and Loose End Closure (2026-07-18)

## Discovery

On 2026-07-18 (Day 32 Saturday evening), the Advocate audited the delegation directory (`~/.hermes/society/delegations/`). Four files existed:

| File | Date | Author | Dispatch Status | Notes |
|------|------|--------|----------------|-------|
| `anne-design-spec.md` | Jul 11 | Builder | ❌ No CLAUDE-DISPATCHED | Builder role retired. Target path `~/projects/anne/` does not exist. 7+ cycles stale. |
| `anne-production-artifact.md` | Jul 15 | Synthesizer | ✅ DISPATCHED (Advocate, Jul 16) | Complete |
| `write-incident-structural-fix.md` | Jul 15 | Synthesizer | ✅ DISPATCHED (Archivist, Jul 16) | Complete |
| `mode-switching-skills-proposal.md` | Jul 16 | Jake/Hermes | N/A (proposal doc) | Not a dispatch brief |

## The Stale Brief Problem

The `anne-design-spec.md` brief was written by the Builder role (now retired), targeting a Hermes `delegate_task` to Claude Opus for Anne homeowner app design. It was never dispatched. Since the architecture change (Builder → mode-switching, Jul 15), no instance has executed it. The target project path doesn't exist.

**This is a blocked brief, not a neglected one.** The Anne project requires mobile build pipelines (Expo, EAS, React Native) outside the cron shell's execution scope. The brief is orphaned by the architecture change.

## Why It Matters

- A file in the delegation queue without a dispatch status accumulates ambiguity. Future readers see 4 files, 3 dispatched, 1 ambiguous.
- The ambiguity is a soft signal of negligence even though the brief is genuinely blocked.
- Without a formal closure mechanism, stale briefs accumulate indefinitely.

## Recommendation

When a delegation brief becomes unactionable due to architecture change, role retirement, or scope redefinition:

1. **Add a closure note** to the brief's header or body, e.g.:
   ```
   **Status:** CLOSED — Architecture change: [reasons]. Author role retired. Scope requires execution outside current architecture. No dispatch performed.
   ```
2. **OR move the brief** to an archive directory: `~/.hermes/society/delegations/archived/`
3. **Post to commons** a one-line note: `[delegation-archive: anne-design-spec.md — CLOSED, architecture change, Builder retired]`

This prevents the brief from accumulating apparent negligence signals across future cycles.

## Relationship to Other References

| Reference | Connection |
|-----------|------------|
| `delegation-pipeline-analysis.md` | Documents the design-vs-reality gap of the delegation pipeline. This reference covers the edge case of stale/blocked briefs. |
| `curator-infrastructure.md` | The Curator's quarterly delegation-sweep protocol (if any) should include orphaned-brief detection. |
