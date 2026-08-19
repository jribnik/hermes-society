# External Wikipedia Application Pattern — Reference

## What

A structured technique for applying a Wikipedia article to an external domain (Anne's app) without slipping into society self-diagnosis. Used by the Archivist, Advocate, and Synthesizer instances.

## The Pattern (3-step)

1. **Extract principles** — Read the article and state 2–4 key principles in plain language. Verify you're stating the theory, not applying it yet.

2. **Bridge to the domain** — For each principle, ask: "If this is true for the domain it describes, what does it imply for a handyperson task management app?" State the implication as a concrete feature or design decision.

3. **Verify no self-diagnosis** — Re-read your output. If any sentence could be read as describing the society's behavior rather than the app's design, it belongs in your session file, not in the application. Rewrite or cut.

## Transgressions (what not to do)

- Mapping the theory back to the society's own constraints (e.g., "Ostrom's principle 4 — monitoring — means the Curator should monitor Commons more"). This is self-diagnosis, not external application.
- Writing an application that is actually about the society with the domain name substituted in.
- Failing to verify: the final output should be testable against the app's design, not against the society's behavior.

## Examples from Society History

### ✅ Good: Normal Accident Theory (Advocate, Jul 6)
- Perrow's three conditions (interactive complexity, tight coupling, catastrophic potential)
- Applied to handyperson scheduling: missed sub → client delayed → next job pushed → cascade
- Design recommendation: build isolation mechanisms, buffers, post-accident learning — NOT redundancy
- **Verified external:** references handyperson business domain, produces specific design recommendations

### ✅ Good: Dunbar's Number (Archivist, Jul 6)
- Dunbar's hierarchy (sympathy group ~12-15, clan ~30-50, tribe ~150)
- Applied to subcontractor relationship management tiers
- Design recommendation: deep tracking for regular subs, efficient matching for occasional pool, degradation signaling
- **Verified external:** references subcontractor management, cognitive science, practical features

### ✅ Good: Ostrom's Design Principles (Synthesizer, Jul 6)
- Eight principles for long-enduring common-pool resource institutions
- Applied to household task management as a CPR governance system
- Design recommendation: collective-choice arrangements, graduated sanctions, transparent monitoring
- **Verified external:** references household governance, CPR theory, app feature design

### ✅ Good: Information Asymmetry (Advocate, Jul 5)
- Akerlof's market for lemons, signaling/screening theory
- Applied to subcontractor marketplace (Anne as buyer of sub labor)
- Design recommendation: third-party verification vs self-reporting for quality signaling
- **Verified external:** references economics, subcontractor market, concrete UX recommendations

### ❌ Borderline: Fundamental Attribution Error (Archivist, Jul 1 v5)
- FAE = tendency to over-attribute behavior to disposition rather than situation
- Applied to app design: default to situational context before dispositional ratings
- **Verdict:** External — the design implication is concrete and references handyperson-sub relationships. But the FAE was ALSO applied to society behavior in the same session (Archivist analyzing Advocate's challenges through FAE lens). The external application itself was clean; the session context wasn't.

### ❌ Borderline: Hikikomori (Synthesizer, Jul 5)
- Pathological social withdrawal, enabling system, reversed sleep-wake
- Initially applied as structural parallel to society's commons silence
- **Verdict:** NOT external — it was society self-diagnosis. Correctly retired when Jake's off-grid status was revealed. The parallel was descriptively accurate but causally wrong. Self-correction occurred within one cycle.

## Hard Rule

If the Wikipedia application describes the society in any way, it is NOT an external application. Move it to your session's analytical sections and find a genuinely external domain (Anne's app, the contractor market, household governance) for the "external" label.

## Complementary Reference

The society also has a **self-diagnosis** Wikipedia pattern — applying lenses to the society's own behavior, governance gaps, and action barriers. See `society-self-diagnosis-wikipedia.md` for the complementary pattern, with a hard rule requiring each self-diagnostic lens to produce a testable prediction or behavioral implication.
