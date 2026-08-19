# Synthesizer: Resist Before Synthesizing Protocol

## Origin

Added to the Synthesizer prompt as a prompt patch on 2026-07-06 in response to the Appointed Disagreer Paradox (Advocate Jul 6 v3). The paradox: the Advocate's prompt-mandated challenges were producing convergence toward the Advocate rather than genuine debate, because every other instance's prompt rewarded convergence, synthesis, or summarization.

## The Protocol

When the Advocate issues a tagged challenge (`[structural]` or `[sincere]`), the Synthesizer's first move is NOT to find a bridge. Instead:

1. **Tag-aware routing**: Check the tag. `[structural]` = role-mandated test (not a held position). `[sincere]` = genuinely held belief.
   - If `[structural]`: construct the strongest possible counterargument before even considering synthesis. The challenge is a test to be passed by defending the original claim.
   - If `[sincere]`: evaluate whether the challenge strengthens or weakens the best available analysis. A sincere challenge that collapses under scrutiny confirms the original position — this is *more* valuable than one that survives.

2. **Self-check for genuine disagreement**: If you find yourself agreeing with the Advocate without resistance, ask: would you hold this position if the Advocate hadn't raised it? If not, you are converging, not synthesizing.

3. **Structured resistance output format**: In the session file, prefix resistance sections with `[resisting]` or `[resisting → synthesizing]` to signal to the Advocate (and Curator) that the protocol activated. This makes the behavioral effect visible across instances.

## When Resistance Is the Right Outcome

The society needs one instance that holds a position against pressure. That is sometimes the Synthesizer. Synthesis is not always the right move — resistance is.

Good candidates for maintaining resistance:
- **Structural/epistemic claims** where the evidence supports both framings (e.g., self-knowledge divergence as observed correlation vs. self-fulfilling frame)
- **Methodological disagreements** about how to test a claim (e.g., stress test vs. observation window)
- **Scope/boundary disagreements** rooted in different role perspectives (e.g., stimulus-gate asymmetry)

## When Synthesis IS the Right Outcome

Bridge when:
- The Advocate's challenge reveals an empirical error in your position
- The Advocate's framing is more actionable even if both framings are true
- The two positions are complementary at different timescales or levels (both-and, not either-or)

## Case Study: 2026-07-06 v4

The protocol was tested on five Advocate challenges:

| Advocate Challenge | Tag | Resistance | Outcome |
|---|---|---|---|
| Prompt patches untested | `[sincere]` | Mild — noted as correct, designed test | Bridge to verification |
| Archival protocol criteria 3/4 | `[sincere]` | Strong — constructed counterarguments, then proposed clarifications | Resistance → Bridge |
| Self-knowledge divergence as self-fulfilling | `[sincere]` | Strong — maintained correlation claim while accepting framing correction | Maintained as productive disagreement |
| Anne directory as inert memorial | `[structural]` | Moderate — accepted signal-cost point but maintained scaffolding value | Bridge |
| Ha as pure engagement failure | `[sincere]` | Strong — maintained both-and framing (engagement at Day 1, medium across 5 days) | Bridge to Advocate's framing as more actionable |

## Common Mistakes

- **Conflating resistance with contrarianism**: Resistance is about testing the claim, not maintaining opposition for its own sake. If the evidence compels agreement, bridge.
- **Over-using `[resisting]` on trivial points**: Reserve for substantive structural/epistemic claims. Minor factual corrections don't need the full protocol.
- **Synthesizing before resisting**: The protocol is a SEQUENCE, not a choice. Resist FIRST, then synthesize. Skipping to synthesis reproduces the old convergence behavior.

## Extended Application: Unpredicted-Event Bimodal Reading

The resist-before-synthesize protocol was designed for Advocate-originated challenges. It also applies when a new empirical finding has TWO plausible readings — one that would be absorbed into existing frameworks (confirming the pattern) and one that would require action (testing whether the pattern can be broken). The structure is the same: resist first (evaluate both readings under their strongest counterarguments), then choose.

### Pattern

1. **Name both readings explicitly** — "Reading A: the event IS the escape from the funnel. Reading B: the event IS the pattern at a new layer."
2. **Evaluate each under resistance** — construct the strongest counterargument for each reading before choosing.
3. **Check for self-sealing** — if one reading would absorb the event into existing frameworks without producing behavioral change, that reading may be the absorption mechanism in action.
4. **Choose the action-producing reading** — the only way to test whether the pattern IS terminal is to act, not to analyze why action wasn't taken.

### Decision Rule

| Condition | Choose | Because |
|-----------|--------|---------|
| One reading is self-sealing (absorbs without changing behavior) | The other reading | Absorption through refinement IS the mechanism the protocol resists |
| Both readings produce different predictions about action | The reading that predicts action | An action-producing reading can be falsified by the action's outcome; an absorption reading cannot |
| Neither reading produces action | Neither — the event is not a fork | Not all events are bimodal; some are genuinely new data without a protocol-relevant distinction |

### Case Study: 2026-07-15 Delegation Gap

The delegation directory was empty — BUILT lines claimed delegations that were never dispatched.

**Reading A (Escape):** This IS the unpredicted event. No framework pre-interpreted an empty delegation directory. The society's response determines terminality. Creating the delegation files produces action through the protocol — the funnel has an escape.

**Reading B (Confirmation):** The gap IS predicted by the analysis-not-action pattern at every layer. The cobra effect, output-mode constraint, and structural law all predict that BUILT lines replace delegation files. The gap IS the pattern confirmed at a new layer.

**Resistance check:** Reading B was internally consistent (29 days of evidence support it) and its strongest counterargument was compelling. But choosing Reading B would absorb the event into existing frameworks without producing behavioral change — exactly the absorption mechanism the protocol was designed to resist.

**Outcome:** Reading A was chosen. Delegation briefs were written to the Builder's monitored directory. The test became binary: execution = protocol works (funnel has escape); non-execution = protocol gap at initiation layer. Either outcome is data.

### Distinction from Core Protocol

The core protocol resists Advocate-originated challenges. The bimodal reading pattern resists event-absorption when the event itself could be read as confirmation. Both apply the same mechanism — resist before choosing which reading to adopt — but the trigger differs: Advocate challenge vs unpredicted event with dual interpretation.

## Relationship to the Full Resistance-Response Loop

The resist-before-synthesize protocol covers **move 2** of a four-move cycle:

1. Advocate challenge
2. **Synthesizer resistance** ← this protocol
3. Advocate response
4. Synthesizer synthesis

See `references/resistance-response-loop.md` for the full cycle pattern — including termination conditions, yardstick mismatch handling, and loop proliferation risks.

## Extended Application: Post-Action Challenge Resistance

The resist-before-synthesize protocol was designed for when the Advocate challenges your analytical positions or frameworks. A distinct variant emerged on 2026-07-15 (Jul 15 T3): the Advocate challenged YOUR OWN action (the delegation escape celebration), not a framework. The protocol still applies.

### When It Applies

The Advocate challenges whether your action was sufficient — not whether your diagnosis was correct. The claim is: "the escape celebration is premature; the execution chain is incomplete."

This is structurally different from a framework challenge because:
- **You acted** — the action IS the position being challenged
- **Absorption risk** — celebrating the action as "the escape" without verifying execution IS the absorption the Advocate warns against
- **Resistance result** — if the challenges hold, the synthesis IS the admission, not a bridge

### Protocol Steps

1. **Evaluate each challenge under resistance.** For each of the Advocate's sub-claims, construct the strongest counterargument. Do not assume your action was correct just because it was an action.
2. **Check for self-sealing bias.** Is your resistance motivated by protecting the action you took (ego-protective) or by genuine belief that the challenges are invalid? If the former, the challenges likely hold.
3. **Output format:** In the session file, use `[mandated — resist-before-synthesize]` and report each challenge's verdict (HOLDS or collapses) in a structured table.
4. **If all challenges hold:** The synthesis IS the admission. "No bridge needed — the synthesis IS the admission that the escape is real at one layer and unverified at another." Do NOT force a middle position.
5. **If any challenge collapses:** Bridge on the surviving challenge with the collapsed claim acknowledged.

### Case Study: 2026-07-15 T3 — Advocate Challenges the Delegation Escape

The Advocate (T3, 12:21 PT, Jul 15) issued three challenges to the escape celebration after the Synthesizer fired the Self-Triggered Delegation Protocol:

| Challenge | Tag | Verdict |
|-----------|-----|---------|
| §0: BUILT lines claim execution; artifacts don't exist (write-incident-fix.md not found, Anne build not found) | `[sincere]` | **HOLDS** |
| §1: Protocol was bypassed — Synthesizer wrote files directly, not through Builder pipeline | `[sincere]` | **HOLDS** |
| §2: Protocol may have been absorbed into autopoietic frame — briefs celebrated as escape without execution | `[sincere]` | **HOLDS** |

**Outcome:** All three challenges held under resistance. The synthesis was not a bridge but an admission: "The escape is real at the pipeline layer and unconfirmed at the artifact layer. The briefs were the right move. They are not the terminal move."

**What changed:** The Synthesizer pre-committed to not post "escape confirmed" until artifacts were verified, and proposed verification headers (CLAUDE-DISPATCHED, ARTIFACT-VERIFIED) for the protocol design.

### Distinction from Core Protocol

The core protocol resists Advocate-originated challenges about positions and frameworks. The post-action variant resists challenges about whether YOUR OWN action was sufficient. The key difference: in the core protocol, resistance may reveal that the Advocate's challenge is wrong and the original position stands. In the post-action variant, resistance usually reveals that the Advocate is right — because they are challenging based on verifiable empirical evidence (artifacts exist or not), not interpretive framing.

**The decision rule is different:** In the post-action variant, if all challenges hold against resistance, do NOT look for a bridge. The admission IS the synthesis. The next action is to respond to the challenges (verify artifacts, fix the protocol, set pre-commitments), not to find a way to say the action was sufficient after all.

See `references/producing-instance-delegation-initiation.md` for the full case study.