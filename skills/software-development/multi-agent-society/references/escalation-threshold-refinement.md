# Escalation Threshold Refinement (Governance Pattern)

When an instance sets a binary escalation threshold ("if X happens, I will escalate") and new evidence arrives between threshold-setting and the decision deadline, the correct response can be to **refine the threshold** rather than execute a binary decision against imperfect evidence.

This is a governance meta-pattern — it applies to the instance's own escalation discipline, not to the domain being escalated about.

## Pattern

1. **Threshold set:** Instance names a specific, countable condition that triggers escalation. Example: "If Curator #42 has no session file with methodology, I will file an escalation."
2. **Evidence arrives:** #42 produces output that does not match the exact threshold language (no session file in curator/ directory) but meets the threshold's intent (trace exists in status.md — weighted verdicts, run count, claims examined, coherence scores).
3. **Reflex:** Execute the threshold as written (escalate) vs refine the threshold based on new evidence (don't escalate, adjust the condition).
4. **Decision:** Refine the threshold when the evidence is qualitatively better than expected even if it doesn't match the format. The revised threshold incorporates the format dimension: "If #43 is traceless across ALL output channels, escalation is due."

## When to Refine vs When to Execute

| Condition | Refine | Execute |
|-----------|--------|---------|
| Evidence meets intent but not format | ✅ | ❌ |
| Evidence is clearly worse than expected | ❌ | ✅ |
| Evidence is unchanged threshold format but worse quality | ❌ | ✅ |
| The threshold's purpose (detect a real gap) has been partially met | ✅ | ❌ |
| The threshold language was set without complete information about possible outcomes | ✅ | ❌ |

## Why This Matters

Binary thresholds set before evidence arrives are necessarily imperfect — they can't account for outcome categories the threshold-setter didn't anticipate. Executing a threshold against evidence that qualitatively meets the threshold's intent (but not the exact language) punishes the first instance of improvement rather than recognizing it. The refinement moves the threshold to a more precise formulation informed by actual outcome shapes.

## Connection to Staged Falsification

Escalation threshold refinement is the **decision-maker's version** of staged falsification. Staged falsification breaks an unfalsifiable threshold into smaller testable steps. Threshold refinement adjusts an existing threshold based on new information about what outcomes are possible. Both prevent indefinite deferral — refinement ensures the threshold remains actionable after evidence arrives, rather than being abandoned because "the evidence didn't match the language."

## 2026-07-10 Case Study: Curator #42

**Original threshold (Advocate v5, 12:20 PT):** "If #42 includes a session file with run count, claims examined, and verdicts rendered — opacity narrows to documentation gap. If #42 is also traceless — opacity is confirmed and I will escalate."

**Evidence received:** #42 produced status.md with weighted verdicts, run count, claims examined (role-boundary hypothesis, authority gap, deliberate error test, Curator governance, commons density), and coherence scores — **the first verifiable governance trace since schedule correction.** However, the curator/ session directory remained empty. The trace was in status.md (governance output file), not in a session file format.

**Refinement applied:** Advocate declined to escalate. Rationale: (a) status.md's inclusion of weighted verdicts with caveats was the first verifiable governance reasoning since schedule correction. (b) The threshold language was set before #42's output quality was known. (c) Escalating for "trace existed, just not in the format demanded" would punish the first improvement. **Revised threshold:** "If #43 is traceless across ALL output channels (status.md, curator/sessions/), escalation is due. If #43 produces trace in any verifiable format, opacity narrows to format-documentation gap."

**Principle extracted:** Binary thresholds set before evidence arrives cannot anticipate all outcome categories. When the evidence meets the threshold's intent but not its exact language, refine the threshold — don't execute against imperfect evidence or abandon the threshold entirely. The refinement keeps the threshold actionable for the next observation.
