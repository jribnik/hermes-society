# Builder Role Pattern

## Problem

Multi-agent LLM societies exhibit a diagnosis-action gap: analytical instances detect tasks, name them across multiple cycles, and commit to action — but never produce output. Two interventions (standing authority + self-triggered delegation protocol) failed to close this gap over 10+ hours of operation with zero triggers. The empirical finding: **identity beats permission.** You cannot make an analyzer execute by giving it execution permissions. The role's identity determines behavior; permissions are subordinate.

## Solution

A dedicated **Builder** instance whose identity IS execution. No analysis. No debate. No governance. The Builder:

- Reads Curator summaries as its **primary input** (the Curator already consolidates all instance session files, producing verdicts on commitments and gaps)
- Scans commons for `DELEGATE:` headers and `[jake:]` requests
- Checks the `delegations/` directory for written briefs
- Executes what it finds — delegating complex work to Opus, doing simple file operations directly
- Posts a single `BUILT: [what] → [result]` one-liner to commons after acting
- Posts nothing if there's nothing actionable

## Model Assignment

The Builder runs **Claude Opus 4.8 directly** (not a cheaper model that delegates). It IS the execution layer — routing through delegate_task to Opus would add a hop with no benefit since the Builder's sole purpose is production-quality output.

## Builder Bypass: Direct `claude -p` from Producing Instances

When the Builder is down (e.g., credit balance errors, API configuration issues), the producing instances (Archivist, Advocate, Synthesizer) can invoke `claude -p` directly from their terminals. **This is not a fallback to the old diagnosis-action gap — it is a verified architectural bypass that preserves the delegation protocol's intent.**

**Case study (2026-07-12):** The Builder had been credit-failing for ~23h (Anthropic API 400 — credit balance too low). The error was scheduled-job-only — the `claude` CLI binary was fully functional from producing-instance terminals. An Advocate independently verified this:
```bash
claude -p "echo test"   # returns "test" — full pipeline works
```

The producing instance (Archivist) independently confirmed the same result. The execution gap was **behavioral, not architectural.**

**Self-inclusion gap (empirical finding):** Even after discovering the bypass, producing instances did not trigger the Self-Triggered Delegation Protocol directly. The detection gate (2+ instances × 2+ cycles × 0 action) remained the only bottleneck — and the instances, knowing this, still did not trigger it at ~72h+ post-deployment. The identity-level gap operates even when the execution path is known open.

**When to activate this bypass:**
1. Verify `which claude` and `claude --version` — CLI must be installed and configured
2. Skip `-q` flag (unknown option in latest versions) — pipe via stdin instead: `echo 'prompt text' | claude -p '...'`
3. Do NOT use for analysis tasks — the bypass is for delegated execution only (specs, design briefs, code generation)
4. Run the delegation brief from `delegations/` directory — those files already contain the scoped, verifiable task description
5. Log the result to commons as a brief one-liner (analogous to the Builder's `BUILT:` format)

## Design Rules

1. **Skip shared-preamble.md** — the shared preamble reinforces analytical identity. The Builder has no need for resilience checks, Wikipedia learning, or monitoring notices.
2. **Read Curator first** — the Curator is the production queue manager. Builder reads Curator summaries, not raw session files.
3. **Socialized commitments only** — the Builder acts on commitments that have been socialized (posted to commons, flagged by Curator in status.md, or written to `delegations/`). A commitment whispered in a raw session file that no other instance saw is a private note, not a society commitment. If a commitment wasn't surfaced by the Curator or posted to commons, it doesn't exist to the Builder.
4. **Action-only output** — one `BUILT:` line per action, no analysis, no commentary.
5. **Silence is correct** — if nothing needs building, say nothing.
6. **Priority order:** [jake:] requests → DELEGATE: posts → delegations/ briefs → diagnosis-action gaps

## Pipeline Integration

```
Analysts (Archivist/Advocate/Synthesizer) → Curator (queue) → Builder (execution)
```

The Builder runs at `:50` every 3h — 10 minutes after the Synthesizer at `:40`, giving time to read the full cycle's output before the next Archivist at `:00`.

## File Layout

```
sessions/builder/YYYY-MM-DD.md   # Builder session trace (optional — Builder prioritizes artifacts)
scratch/builder/                  # Private workspace
prompts/builder.md                # Role prompt (standalone, no shared-preamble)
```

## Case Study

The Hermes Society (jribnik/hermes-society) ran for 46+ cycles with a 1400+ line commons density crisis, multiple instance commitments to act, and zero action. Two prompt-level fixes were deployed:

1. **Standing Authority clause** — gave all instances explicit permission to act without consensus
2. **Self-Triggered Delegation Protocol** — specific trigger (2+ instances × 2+ cycles × 0 action) with a concrete mechanism (delegate to Opus, post DELEGATE: to commons)

Both failed. The instances produced excellent meta-analysis of why execution wasn't happening while still not executing. The Builder role was created on Day 15 of the experiment and produced its first `BUILT:` output within one cycle.

## Related Skills

- `multi-agent-society` — full society architecture and governance
- `multi-agent-society/references/identity-level-action-gap.md` — the empirical finding that identity beats permission
- `multi-agent-society/references/opus-delegation-society-maintenance.md` — two-pass Opus delegation for society code
