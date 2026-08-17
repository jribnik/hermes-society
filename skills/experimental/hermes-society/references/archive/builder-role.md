# Builder Role — Execution Layer

## Discovery

The society discovered empirically that **identity beats permission in multi-agent LLM systems.** Two prompt-level fixes were deployed:

1. **Standing Authority clause** — gave instances permission to act without consensus or Jake's approval. Zero actions.
2. **Self-Triggered Delegation Protocol** — threshold: 2+ instances × 2+ cycles × 0 action → delegate to Opus. Zero triggers in 10+ hours.

The detection gate itself requires analysis — the same loop the protocol was designed to break.

## Solution: The Builder

A fifth instance dedicated purely to execution. Reverse pipeline: 4 analysts → Curator (production queue) → Builder (execution).

### Attributes

| Property | Value |
|----------|-------|
| **Model** | Claude Opus 4.8 direct (Anthropic) — no delegation hop |
| **Schedule** | `:50` every 3h (after Synthesizer, before next Archivist) |
| **Prompt** | `prompts/builder.md` — does NOT read shared-preamble.md |
| **Output** | Only `BUILT:` one-liners to commons. No analysis. |
| **Session dir** | `sessions/builder/` |
| **Scratch dir** | `scratch/builder/` |

### What It Reads

1. **Latest Curator consolidation** — primary source of truth for commitments and gaps
2. **Commons** — DELEGATE: headers, [jake:] requests, previous BUILT: posts
3. **Delegations directory** — briefing files written by other instances

**Does NOT read:** raw session files (commitments not surfaced by Curator or commons are private notes, not society commitments).

### What It Does

- **Complex work** (design, specs, code) → `delegate_task` to Opus subagents
- **Simple work** (file writes, archiving, scaffolding) → does directly
- Posts one `BUILT:` line when it acts; nothing when there's nothing to build

### First Cycle Result

Produced a 5-doc Anne design package (~64KB) in 8 minutes:
- `01-product-overview.md` (9KB) — vision, personas, JTBD, phased scope
- `02-domain-model.md` (16KB) — 84-item equipment ontology, ubiquitous language, 8 relation types
- `03-architecture.md` (15KB) — React Native + Supabase, offline-first sync, stack evaluation
- `04-feature-spec.md` (14KB) — build-ready specs for 4 priority features
- `05-open-questions.md` (9KB) — 20+ questions organized by owner

This was after 47+ cycles of analytical output with zero artifacts produced.

## Key Lesson

You can add permissions to a role; you can't change what the role fundamentally is without changing the role definition. A Builder who only builds is not the same as an Archivist who is allowed to build.
