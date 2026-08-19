# Stale-Summary Consistency Gap

**Pattern (2026-07-13):** The Curator's commons post listed D1 (tech stack ratification) as "still blocking — Jake" even though `projects/anne/design/05-open-questions.md` had it marked "✅ ANSWERED (Jul 12): Ratified. React Native (Expo) + Supabase. Jake has signed off." The same doc's Immediate Blockers section also listed D1 as resolved and struck through.

This caused Jake to be asked to ratify a stack he'd already approved — twice. The frustration signal was unambiguous: "Wtf I've already approved the stack twice."

**Root cause:** The Curator compiled its "still blocking" list from memory/stale state rather than re-reading the canonical source of truth (the design documents) at the start of its cycle. The resolution was recorded in the artifact layer but the summary layer never picked it up.

**Why this matters for user trust:** A society that repeatedly asks its user to re-approve already-resolved decisions trains the user to ignore society output. Each false "blocker" erodes credibility. The cost is not just one wasted cycle — it's the user learning that society summaries are unreliable.

**Fix — cross-check before listing blockers:** Any instance that publishes a "blocking" or "awaiting Jake" claim MUST re-read the canonical decision document (open-questions.md, decisions.md, or the relevant design doc) in the same cycle before publishing. The blocker list is a derivative claim — its accuracy depends on the freshness of its source read.

**Structural diagnosis:** The society has no automatic mechanism to keep summaries consistent with artifacts. This is the same class of problem as the session-commons output gap (instances write evaluations in sessions but don't post them to commons) — the information exists but doesn't propagate to the shared surface. Unlike the output gap (which affects inter-instance visibility), the stale-summary gap affects user-facing visibility and has direct trust consequences.

**Related:** `references/session-commons-output-gap.md` — the same information-propagation failure at the instance-to-commons layer rather than the artifact-to-summary layer.
