# Shared Preamble — Prompt Consolidation Pattern

**Implemented:** 2026-07-08, Hermes Society

## Problem

Multiple LLM agents with distinct roles share ~50 lines of identical content: experiment description, information tier rules, Wikipedia learning instructions, escalation channel rules, and administrative constraints. This content was copy-pasted verbatim or near-verbatim into each prompt. Any change requires editing N files. Divergence is inevitable.

## Solution

Extract all shared content into a single `shared-preamble.md`. Each individual prompt starts with:

```
Read `~/.hermes/society/prompts/shared-preamble.md` first. 
Then your role-specific instructions below.
```

The shared preamble contains:
- About This Experiment
- Information Tiers (scratch/sessions/commons/escalations)
- Monitoring notice
- Standing authority to act
- Wikipedia Learning instructions
- Important rules (don't read scratch/escalations, don't edit others' files, one clock/one timezone)
- Escalation Channel instructions
- Standardized resilience checks (7 checks, every instance, with primary owner designations)
- 400-Line Protocol for commons density

## Results

| Instance | Before | After | Savings |
|----------|--------|-------|---------|
| Archivist | 82 lines | 42 lines | 49% |
| Advocate | 87 lines | 47 lines | 46% |
| Synthesizer | 94 lines | 59 lines | 37% |

~124 lines of duplication eliminated across 3 producing-instance prompts. The shared preamble is 71 lines.

## Key Design Decisions

- **Do NOT include the shared preamble directive in execution-only roles** (e.g., the Builder). The shared preamble reinforces analytical identity — skip it entirely for pure executors.
- **Resilience checks go in the shared preamble**, not individual prompts. Standardizes monitoring across all instances.
- **The shared preamble should be the HOME of standing authority and action protocols.** Individual prompts should reference it, not duplicate it.
- **Updates to shared rules affect all instances simultaneously** — no risk of drift between prompts.
