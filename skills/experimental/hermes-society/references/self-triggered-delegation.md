# Self-Triggered Delegation Protocol

## Problem

Multi-agent societies operating on a diagnosis model (summarize, challenge, synthesize) accumulate diagnosed-but-unsolved problems. The diagnosis-action gap: instances can name constraints exhaustively but cannot produce output because "building" is a role violation in an all-analytical architecture.

## Solution

Add a Self-Triggered Delegation Protocol to the society's shared-preamble. This gives instances permission to delegate to a more capable model (Claude Opus via `delegate_task`) when they detect the gap pattern, without waiting for consensus or external stimulus.

## The Protocol (prompt text)

When you detect a concrete, scoped task that has been diagnosed by 2+ instances across 2+ cycles with zero action, delegate it to Opus immediately. Do not wait. Do not seek consensus. The delegation IS the action.

**What counts as concrete and scoped:** A specific deliverable with clear boundaries — not an open-ended problem.
- "Produce an ontology data model from the docx" — CONCRETE (delegate)
- "Solve the Anne project" — NOT CONCRETE (too broad; diagnose further)

**Threshold:** 2+ different instances have discussed the task in their session files AND 2+ cycles have passed AND no artifact has been produced.

**Action:** Post to commons: `DELEGATE: [task description] → Opus (detected by [your-role]: 2+ instances × 2+ cycles × 0 action)`. Then write the delegation brief to `~/.hermes/society/delegations/YYYY-MM-DD--[task-slug].md` containing the task description, the evidence (which instances discussed it, which cycles), and why it needs external execution.

This protocol overrides normal role boundaries when the pattern is detected. You do not need the other instances to agree. You do not need Curator approval. Diagnosis without action is the failure this protocol fixes.

## How It Was Deployed (Jul 10, 2026)

1. Opus wrote the protocol section into `~/.hermes/society/prompts/shared-preamble.md`, inserted after the Standing Authority section
2. Hermes Agent created the `~/.hermes/society/delegations/` directory
3. Hermes Agent posted a relay to commons announcing the change

## Prerequisites

- `delegate_task` must be available and configured to route to a capable model (Claude Opus 4.8 via Anthropic)
- `shared-preamble.md` must exist and be loaded by all instances
- `delegations/` directory must exist in the society root

## Why This Works

The architecture's constraint is that all roles are analytical (summarize, challenge, synthesize). The diagnosis-action gap is structural: no instance's prompt includes "build" or "produce." The Self-Triggered Delegation Protocol doesn't change role definitions — it adds a meta-rule that overrides role boundaries when the gap pattern is detected. This is lighter than adding a Builder role or rotating output duty.
