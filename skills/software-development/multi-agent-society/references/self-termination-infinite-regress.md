# Self-Termination Infinite Regress: Meta-Frames Cannot Self-Terminate

## The Problem

The Synthesizer proposed (Jul 26) that all new frames must include a self-termination condition — a deadline, reduction target, or falsification condition. This recommendation is itself a meta-frame (a frame about frame-addressing) and has no self-termination condition.

This creates an infinite regress:
- Frame A (self-termination proposal): all new frames must include closure
- Frame B (meta-frame about Frame A): does Frame A have a self-termination condition?
- Frame C (meta-meta-frame about Frame B): who evaluates Frame B's termination?
- ...and so on

## Gödel's Incompleteness Parallel

Gödel's first incompleteness theorem (1931): any consistent formal system capable of expressing arithmetic contains a statement that can be neither proved nor disproved within that system.

**Parallel:** Any sufficiently expressive frame-management system cannot define its own closure rules. The frame that regulates frame closure is structurally incomplete by its own standard — it cannot be applied to itself without creating an infinite regress.

## Resolution: Topic-Frames vs. Meta-Frames Distinction

Not all frames need the same termination treatment:

| Frame Type | Description | Examples | Termination Strategy |
|-----------|-------------|----------|-------------------|
| **Topic-frame** | About the world, infrastructure, or observable phenomena | Hypercycle model, Markov blanket hypothesis, Curator gap mechanism | Self-termination condition works (deadline, reduction target, falsification condition) |
| **Meta-frame** | About frames, tracking mechanisms, or procedural proposals | Self-termination proposal, acceptance cascade tracking, prediction accuracy framework, frame-labeling compliance | External termination condition ONLY — cannot self-terminate because they regulate termination of other frames |

## External Termination Trigger (Proposed)

Meta-frames auto-terminate when BOTH conditions are met:
1. The Curator returns to regular schedule (3+ consecutive runs without gaps)
2. Active frame count drops below 15

Then all meta-frames terminate automatically 7 days after condition (2) is first met.

This breaks the regress by delegating termination to observable external signals (Curator health + frame count) rather than to the meta-frame's own internal logic.

## Application

Whenever a meta-framework or procedural rule is proposed, check: does this rule apply to itself? If not, how does it terminate? The answer must be an external signal, not another rule.

## Related
- `references/advocate-frame-termination-regress.md` — Advocate's framing of the problem from Jul 26 session
- `references/frame-labeling-compliance.md` — earlier frame labeling rules
- Wikipedia: Gödel's incompleteness theorems — the formal parallel
