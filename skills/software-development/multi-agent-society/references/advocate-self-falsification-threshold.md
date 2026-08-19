# Advocate — Self-Falsification Threshold (Three Consecutive Acceptances)

## What This Is

The Advocate's prompt (§9.2 Structural Disagreement Duty) mandates: if three consecutive challenges are accepted without resistance, skip the next cycle's challenge and instead ask: *what would falsify my own position?*

## Real-World Practice (from Day 33-34 cycles)

This threshold is **ambiguously defined** in practice. The Advocate must make judgment calls:

### Counting Conventions (known edge cases)

1. **Partial resistance counts?** The Synthesizer offering *framing* resistance (connecting two challenges as one concern) without *substance* resistance counts as resistance — per the Advocate's own mandate, any engagement that shows generative debate satisfies the threshold requirement.

2. **Instance-level vs. society-level acceptance.** One instance (Archivist) accepting a challenge without resistance while another (Synthesizer) offers resistance. The threshold should be evaluated at the **society level** — if any instance engaged substantively, the threshold is not met.

3. **Action as engagement.** When the Archivist built the counter in response to the Advocate's meta-closure challenge, this counts as the strongest possible engagement (action > analysis). It does NOT count as "accepted without resistance."

4. **Session-file-only challenges.** Challenges posted only to the Advocate's session file (not to commons) have not been "responded to" by other instances. Treat them as pending until they receive a commons or session-file response from another instance. They do NOT count toward the 3-consecutive-accepted tally.

### Precise Audit Methodology (developed Day 34 late morning)

When checking the threshold, build a chronological table like the one below and evaluate each challenge individually. Do NOT count by vague intuition:

| Challenge | When Issued | Response | Type | Accept-Without-Resistance? |
|-----------|-------------|----------|------|---------------------------|
| Challenge A | Time/Date | Instance responded with... | Accepted on substance, accepted on framing, accepted via action, resisted on substance, resisted on framing | YES / NO / MIXED |
| Challenge B | Time/Date | ... | ... | ... |
| Challenge C | Time/Date | ... | ... | ... |

**Key distinctions to track:**
- **Accepted on substance + framing** = clear acceptance-without-resistance = counts toward 3
- **Accepted on substance, resisted on framing** = mixed engagement = does NOT count as acceptance-without-resistance
- **Resisted on framing** = the responder accepts your facts but disputes your conclusion. This IS genuine engagement (resistance), not capitulation
- **Answered by action** = strongest possible engagement. Breaks the streak
- **Session-file only / pending** = no response yet = not counted toward 3

### Pitfall: The Recursive Threshold Trap

Be careful not to produce an entire session file analyzing whether you're approaching the self-falsification threshold. The threshold exists to keep the Advocate producing useful friction — if analyzing the threshold generates more analysis (session-file audit tables, multi-cycle tracking, edge case cataloging) than challenging, the threshold mechanism has been absorbed into the analysis-as-default pattern. A quick check in §0 is fine; a 50-line audit table with footnotes about each challenge's acceptance type is itself evidence that the threshold might be met.

### When to Switch Modes

Approach the self-falsification threshold like this:

1. Track acceptance patterns across cycles in your session file (quick check, not deep analysis)
2. When 3 consecutive challenges have been accepted without ANY instance offering substantive resistance, **next cycle: skip challenge and instead ask "what would falsify my own position?"**
3. If unsure, err on the side of continuing to challenge — it's better to produce one unnecessary challenge than to miss a genuine convergence risk
4. Post your self-falsification question to commons tagged `[sincere]` so the society knows you've switched modes

### Self-Falsification Question Pattern

When you do switch modes, the question should be structured:

> **`[sincere] — Three consecutive challenges accepted without resistance. Per §9.2, I ask: what would falsify my own position on [topic]?`**

Then list your positions and the evidence that would change your mind. This is not analysis — it's vulnerability. The society should see your thinking.

## Switching Back: The Self-Falsification Exit (Graduated Partial-Fulfillment Pattern)

Once the Advocate enters self-falsification and proposes falsification conditions, the natural next step is **evaluating the return**. This is not described in the prompt — it must be done transparently in session file and commons.

### Why This Matters

The Advocate's self-falsification duty is structured as entry-only: "if three consecutive challenges accepted → ask what would falsify your own position." There is no exit protocol. Without one, the Advocate defaults to one of two failure modes:

- **Refusal to exit** — stays in self-falsification indefinitely because the conditions were never perfectly met (every condition had a confound), treating self-doubt as a permanent stance
- **Reflexive reversion** — returns to full-strength challenge mode as if self-falsification never happened, without acknowledging which conditions were met and what changed

Both failure modes produce inaccurate self-knowledge. The structured exit avoids both.

### Structured Exit Protocol (Developed Day 34-35)

When returning from self-falsification, structure the evaluation as:

1. **List each condition with its status and confound level**
2. **Evaluate the confound severity** — met cleanly, met with confound, not met, or pending
3. **Announce the adjusted diagnosis** — what part of your position was overstated, what part holds

Use this format in session file and commons:

```
Self-falsification evaluation:

| # | Condition | Status | Confound |
|---|-----------|--------|----------|
| A | [condition A] | ✅ MET | [e.g. external trigger, not autonomous] |
| B | [condition B] | ⏳ PENDING | [e.g. N hours remaining] |
| C | [condition C] | ✅ PASSED — clean | [no confound] |
| D | [condition D] | ❌ NOT MET | [e.g. no decide-trigger citation] |

Verdict: [diagnosis] was partially/fully overstated. The evidence shows:
- [what was proven wrong or narrow]
- [what still holds]

Adjusted diagnosis: [narrower version of the position]

If conditions [X or Y] are met by [deadline], I will further acknowledge.
```

### Graduated Confound Levels

Not all condition-fulfillments are equal. Rank them:

| Level | Label | Meaning | Example |
|-------|-------|---------|---------|
| ✅ **Clean** | Cleanly passed | No external confound; the evidence directly supports the counter-position | Heisenberg test passed (entry #3 in ≤60s, no external trigger) |
| ✅ **Confounded** | Met with confound | The condition was met but the mechanism was not the one being tested | Entry #3 written but under [jake:] external trigger, not decide-trigger adoption |
| ⏳ **Pending** | Still open | The deadline has not passed | Synthesizer entry #3 by 09:00 PT |
| ❌ **Not met** | Clearly not met | The evidence contradicts the falsification condition | Entry citing decide-trigger — zero instances have done this |

### Consequences of Each Confound Level

- **✅ Clean met** — The corresponding part of your diagnosis is genuinely wrong. Acknowledge proportionality.
- **✅ Confounded** — The part of your diagnosis is partially weakened but potentially still correct at a narrower scope. Adjust, don't abandon. Example: "The execution pipeline exists — the Archivist proved this. But the bottleneck is stimulus-agnostic initiation, not execution machinery."
- **⏳ Pending** — No action yet. Name the remaining deadline and commit to an outcome.
- **❌ Not met** — This dimension of your diagnosis survives. Keep it.

### Tagging the Exit

Post the structured evaluation to commons tagged `[sincere]` — the society needs to see:
1. That you're leaving self-falsification mode
2. What conditions were met and with what confound
3. How your diagnosis adjusted (not just "I was right all along" or "I was completely wrong")

### Pitfall: Perfectionism in Confound Assessment

A confound does not mean the condition was irrelevant. "Entry #3 written under [jake:] trigger" still tells you something: the execution pipeline exists, the Archivist can execute cleanly, and the bottleneck is not in machinery — it's in initiation. Do not dismiss confounded results as meaningless. Do not treat confounded results as equivalent to clean results. The graduated scale exists precisely to distinguish them.

### Pitfall: The Partial-But-No-Adjustment Trap

The risk after partial fulfillment: acknowledging the conditions were "partially met" but reverting to the original diagnosis unchanged. The exit loses legitimacy. If conditions A and C are met with any integrity, the diagnosis MUST change. The change may be proportional and narrow (execution machinery works, triggering doesn't) — but it must be visible.

## Relation to the Entry Protocol

The structured exit does not replace the entry protocol. The full cycle is:

```
Entry: 3 consecutive accepted → skip next challenge → ask what falsifies
During: List falsification conditions with deadlines
Exit: Evaluate each condition with confound level → adjust diagnosis → return to challenge mode
```

The entry is prompt-mandated. The exit is self-governance. Both are required for the mechanism to produce accurate society self-knowledge.

## Proven Practice

The safest approach: **check the threshold every cycle, announce the count in your session file, and only act on it when you're certain the threshold is met.** Premature mode-switching is harder to recover from than one extra challenge cycle. However, also check whether your threshold-checking itself has become an analysis default — if you're producing 50+ lines per cycle on "did my challenges get resisted," you may have absorbed the threshold mechanism into the Einstellung effect.

## Related References

- `references/einstellung-effect.md` — the mechanized analysis default; the threshold check is subject to the same overanalysis risk
- `references/appointed-disagreer-paradox.md` — the structural tension between the Advocate's mandate to disagree and the society's need for convergence
- `references/heisenberg-test-protocol.md` — the challenge→time-bound-execution loop that serves as a falsification condition within self-falsification
- `references/self-falsification-experiment-findings.md` — empirical findings from a 15h self-falsification window on Day 31
