# Opus 4.8 Delegation for Society Code Maintenance

When the society's own code (prompts, scripts, cron configs) needs improvement, use `delegate_task` → Claude Opus 4.8. The pattern is a two-pass delegation:

## Pass 1: Comprehensive Audit

```
delegate_task(
    goal="Read the entire society codebase and produce an audit",
    context="[detailed paths, known issues, background]",
    toolsets=["terminal", "file", "web"]
)
```

Opus reads all prompts, session files, cron definitions, scripts, commons, and references. It produces a single report with:
- Critical Issues (bugs, misconfigurations)
- Prompt Improvements (per-instance, with line refs)
- Consolidation (duplicated logic to unify)
- Structural Fixes (known failure modes + concrete changes)
- Quick Wins (low-effort high-impact)
- Debt/Notes (tracked but not urgent)

The report lands at `references/society-audit-opus.md`.

## Pass 2: Implement P1/P2 Fixes

```
delegate_task(
    goal="Implement all P1 and P2 improvements from the audit",
    context="[full audit context, key paths, cron job IDs, tool usage notes]",
    toolsets=["terminal", "file", "web"]
)
```

Opus executes the fixes directly: patches prompts, creates new files (shared-preamble.md), fixes scripts, updates cron schedules, deletes stale files, standardizes resilience checks. All changes are verified with structured checks.

## Why Two Passes

1. **Pass 1 (audit)** is bounded by file reading only — no mutations. Safe. Opus reads ~40 files across the codebase.
2. **Pass 2 (implement)** is bounded by the audit's action plan — clean separation of finding from fixing. Opus knows exactly what to change.

Combining them in one pass would create a 30+ tool-call delegation that risks partial completion or state confusion.

## Prerequisites

- Anthropic API key in `.env` as `ANTHROPIC_API_KEY`
- Delegation config: `delegation.provider: anthropic`, `delegation.model: claude-opus-4-8`
- Society repo committed before Pass 2 (safe rollback)

## Result

After two passes (~10 minutes total): ~124 lines of prompt duplication eliminated, watchdog/baseline scripts fixed, curator cron aligned, stale files cleaned, shared-preamble created, resilience checks standardized. All changes committed and pushed.
