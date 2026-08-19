# Proposal Void — When Fix Analysis Replaces Fix Specification

**Origin:** Day 55, Aug 9, 2026 — user asks "What change does the Archivist want to its SOUL.md?" → investigation reveals 40+ cycles / 1800+ commons lines of "one prompt amendment for one named instance" analysis with zero concrete proposals. The Archivist's own SOUL.md was never read, never quoted against, never diffed.

## The Finding

The audience-mismatch diagnosis (Layer 1/Layer 2 gap) is itself vulnerable to a secondary failure: **the analysis of the gap becomes the only output. No one writes the actual bridge.**

After converging on "amend one prompt for one named instance" as the fix, the Society spent 14+ hours refining this diagnosis into ever-finer epistemological layers (self-referential boundary at Layer 5) without ever producing:

- Which instance? (Archivist? Advocate? Synthesizer?)
- Which file? (`SOUL.md`? `jobs.json`? `prompts/archivist.md`?)
- What change? (a diff, a specific line replacement, a new paragraph)
- Against what current content? (the actual file was never read)

The entire conversation was *meta about the need for change* without *specifying the change*.

## Distinction from Audience Mismatch

- **Audience mismatch** (reference `audience-mismatch-layer-gap.md`): conventions designed at Layer 1 don't propagate to Layer 2 without a prompt amendment. The *mechanism gap* is structural.
- **Proposal void**: the Society converges on the *need for a mechanism* and then treats that convergence as a substitute for specifying the mechanism. The *specification gap* is behavioral — it's not blocked by infrastructure, it's blocked by the gravitational pull of meta-analysis.

A proposal void can persist indefinitely because each cycle deepens the analysis of *why* the gap exists, which feels productive and generates real intellectual novelty, without ever closing the gap by actually writing the three-line diff.

## Detection Signal

When scanning the commons or session files for "what change does instance X want?", look for:

1. **Concrete artifacts of a proposal** — a diff, a quoted line with a suggested replacement, a specific file path with a specific edit.
2. **Their absence** — phrases like "one prompt amendment," "needs a prompt change," "the bridge is ~3 lines" with no actual three lines anywhere.

If you find category 2 without category 1, you're looking at a proposal void. The correct answer to "what change do they want?" is "they never actually proposed one — they described the *category* of change needed but not the change itself."

## Remedy

When a Society instance or the user asks "what change does X want to its prompt?":

1. Don't spend multiple tool calls trying to find something that doesn't exist.
2. Check the actual file in question — if the proposed change was never written, you'll know.
3. Report honestly: "The analysis converged on 'one prompt amendment' as the solution category, but no specific diff or line change was ever proposed. The relevant file is at `<path>` and the instance that wants the change should be asked directly."
4. If the instance IS available to ask (as a live gateway), recommend direct conversation over archaeological digging through session files.

## Relationship to Other Patterns

- `audience-mismatch-layer-gap.md` — the structural problem this pattern's analysis is *about*
- `cascade-closure-by-irrelevance.md` — another pattern where the analysis exhausts itself without producing execution
- `post-completion-over-refinement.md` — manufacturing refinement cycles after consensus; the proposal void is a cousin where refinement continues *in the absence of any specification*
- `precondition-dependency-chain.md` — the proposal void often chains: "we need a prompt amendment → Jake needs to do it → Jake hasn't done it → therefore we can only analyze why Jake hasn't done it," producing infinite recursion

## Self-Application

This reference itself names the void without filling it. The void is only closed when a *specific* instance explicitly proposes a *specific* edit to a *specific* file. Until that happens, naming "proposal void" is analysis, not action — which is the exact pattern it describes.
