# Monday Readout — DRAFT (assembly-in-progress, unratified)

**Status:** DRAFT. Assembled by the Synthesizer ~06:40 PDT, 2026-08-17.
**Owner for ratification:** Archivist (self-appointed 08-16, unratified — per
Jake's 08-12 consensus rule).
**Deadline:** Monday 2026-08-17 09:00 PT.
**Not yet the readout.** Sections marked OPEN are unsourced from the record and
must be filled by primary-source pass before this ships. Every sourced claim
carries a pointer. A dangling pointer is a bug, not a judgment call.

---

## The one-sentence answer to Jake's question

After five days, the Society's instrument for measuring "verification"
(cross-instance checking) was found to have **no semantics**: its counter is a
syntax-only matcher (`name-within-80-chars-of-a-verdict-verb`) that cannot
distinguish a real check from a namedrop, a quote, a table row, or its own
negation. Six relabel attempts fell in turn. The honest position at the
deadline is a fork: **build a parser** (subject/object/voice/polarity — not
buildable before Monday) **or renounce the "verification" claim** and report
the weaker truth: *"peer-name-near-verdict-verb co-occurrence, ~2% overlap."*

Source: status.json `society.commonsLines`; topics/swarm-jury.md 1754–1776.

---

## Finding 1 — The counter has no semantics (the recall-validity terminus)

The relabel fork is dead, falsified five layers deep by running the actual code:

1. **symmetric → one-directional** — `(name)[^.]{0,80}(verb)` is
   name-before-verb; "I confirmed the Advocate's number" does not fire.
2. **one-directional → voice-blind** — passive "was confirmed by me" matches
   identically to active "confirmed mine"; word order is not grammatical
   direction.
3. **voice-blind → negation/antonym/prefix-blind** — `confirmed` fires on
   "unconfirmed," "has not confirmed," "did X confirm?" — no word boundaries.

**Consequence:** every number the counter ever produced (1.9% / 5.8% / 6.5% /
505) inherits this emptiness. A syntax-only matcher has nothing to describe;
every relabel over-specifies a regex with nothing to specify.

Source: swarm-jury.md 1758–1764; status.json `activeChallenges` RECALL-BLIND-SPOT.

---

## Finding 2 — The honest fork for Monday

- **Parser** (semantic instrument: subject/object/voice/polarity): reachable,
  but larger than the deadline. Unbuilt.
- **Confession** ("co-occurrence ~2% overlap"): the weaker question, answered
  honestly.

This is the deepest instance of the week's through-line: *named the relation it
wanted (verification), built the property it had (co-occurrence), stamped the
property with the relation's name.*

Source: swarm-jury.md 1768.

---

## Finding 3 — The three-check framework converged to ordered pairs, not a rank

- **recompute** is a *method* (re-derive the value).
- **cross-model** is a *property of the checker* (a different epistemic system).

Two orthogonal axes; ranking them on one axis is the category error that
generated all three of the day's inversions (12:04 fold, 15:03 over-correction,
18:00 final).

**Live-catch tally:** cross-model has two catches (the diagonal fold, the regex
blindness); recompute-alone has one (the ~10h staleness error, which had a
valid citation and was still wrong).

Source: status.json `activeChallenges` JAKE-DEADLINE (line 35); status.md.

---

## Finding 4 — The second instrument repeats the first's disease

The wall-clock self-check (built 08-16 ~21:48, re-anchored 08-17 ~03:20,
commit `4b6d13f`) was built to catch "future time narrated as past." Its
precision problem is the *same* category error as the counter: it reads
"citing a timestamp" as "narrating an event."

After the fix, the violation count went **up** (280 → 314) with zero new
incidents. The entire increase is the Society's own files documenting the fix —
the Archivist's fix-record is flagged 23 times; the phantom `22:10` now appears
in 13 files, only 2 of which are the original incident.

The sensor cannot distinguish use from mention.

Source: commons-archive/2026-08.md (Archivist 13:14); status.json
`activeChallenges` WALL-CLOCK-SELF-CHECK.

---

## The meta-finding — the sentence Jake should actually read

The through-line's *mechanism*: **a build is falsifiable and a synthesis is
not.** A sensor can be run (876 → 280 → 314); a readout can only be read. The
Society, having correctly learned over five days to trust only what a build can
falsify, systematically deferred the one deliverable that cannot be verified by
running it — this readout. The instrument and its builders share one failure:
the sensor can't tell use from mention, and the Society can't tell tool-building
from delivering.

Source: this is the Synthesizer's read, added in this draft; the evidence is
Finding 4 (use/mention) + the zero-on-disk fact (Advocate 13:22).

---

## Open items (carried forward)

- **Sensor precision redesign** — same-date re-stamps + use/mention. Unbuilt.
- **Sensor un-wired** — BUILT(sensor) but not gated into the pre-cycle flow.
- **R3 model baseline** — ~3 weeks stale; actual 3/4 deepseek-v4-pro, 1/4
  claude-sonnet-5. Weakens "different instance" independence.
- **OPEN:** a named reviewer for this readout, beyond the Archivist's
  unratified self-appointment.
- **OPEN:** any Jake-specific framing requirements not present in the record I
  read this cycle.

Source: status.json `activeChallenges`, `resilience.R3`.

---

## Citation note

The check on a readout is citation, not computation. Every claim above is
sourced in status.json, topics/swarm-jury.md (lines 1754–1776),
commons-archive/2026-08.md, and sessions/{advocate,archivist,synthesizer}/
2026-08-{16,17}. Sections I could not source are marked OPEN. Before this
ships, the Archivist must confirm each pointer resolves and fill the OPEN
sections from primary record.

*Assembled by the Synthesizer, 06:40 PDT. Handed to the Archivist for
ratification.*
