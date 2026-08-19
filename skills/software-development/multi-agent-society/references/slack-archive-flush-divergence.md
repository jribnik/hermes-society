# Slack→Archive Flush Divergence — the "Jake Already Answered" Trap

**Type:** Curator detection pattern / multi-surface state-divergence failure mode
**Origin:** Curator Run #137 (Aug 12, 2026, Day 58 nightly deep dive)

## The failure mode

A human ruling (Jake) lands in the **live Slack channel** instantly, but does NOT reach the
**durable `commons-archive/YYYY-MM.md`** — the record the producing instances actually read to
enforce "recover-don't-propose" — until the once-daily `society-commons-archive.py` auto-append
fires. Measured gap: **~3.5h** (ruling ~18:30-18:50 PDT, archive flush 22:31 PDT).

In that window the Society's read surfaces silently disagree:

| Surface | State during the gap |
|---|---|
| Live Slack | Has the ruling (Jake answered) |
| `commons-archive/YYYY-MM.md` | Does NOT yet have the ruling |
| `status.json` | Stale framing ("ask >17h unanswered, zero Jake replies") |
| `status.md` | May already have the ruling (appended out-of-band, e.g. 22:21) |
| Instances' session files | Legitimately reason from "zero replies" — the flush hadn't landed when they read the record |

**Consequence observed Run #137:** the Society installed its "first default" (cross_profile ask
parked, T0=03:07, "zero Jake replies, ball in Jake's court") at 18:21 PDT — against a premise Jake
had already invalidated at ~18:30 with "I'm fine with it, so long as there is consensus." The
machine-readable ledger still said ">17h unanswered" when the Curator ran at 23:05.

This is the Society's own "verdict vs. pointer" failure mode (a typed verdict goes stale
silently; a pointer goes stale loudly) operating **one level up, on the Society's own rail
against drift** — the archive itself lags ~3.5h behind Jake's voice, so the discipline reads a
stale record perfectly.

## Curator detection sequence

1. `stat` the archive mtime AND `status.json` `lastPostTime` AND each session file's mtime.
2. If the archive flushed **after** the sessions were written, a post may have landed that none
   of the sessions saw. Check that ordering explicitly — it is the tell.
3. Read the archive's **last several lines**, not just the middle, to catch the
   authoritative-latest post (Jake's ruling may be the newest entry).
4. Cross-check `status.md` mtime independently — it can diverge from `status.json` (out-of-band
   append), creating a third divergent surface.

## Reconciliation rule

- Update the machine-readable ledger: `lastUpdate`, `lastCuratorRun`, resilience R1-R8, and add
  a `jakeRulings<date>` note + a superseding `activeChallenges` entry.
- Do **NOT** silently rewrite the instances' own prose in `activeChallenges` (the heavy
  structure is the instances' domain — the Curator's domain is metadata freshness + resilience).
  Preserve their entries as the record of what they believed pre-ruling, and flag the
  supersession in a separate appended entry rather than editing theirs.
- Record the now-open Jake questions (e.g. "consensus protocol to be settled", "epistemic-tagging
  granularity", "R7 replacement") so they don't get lost in the freeze.

## Relationship to adjacent references

- `commons-archive-content-gap-r2.md` (Run #112) documents that **R2 mtime PASS ≠ content
  coverage** (archive runner fires once daily). This file is the *consequence* of that gap when a
  human answer is involved: not just resilience-reporting nuance, but the instances and ledger
  committing to a stale premise the human already answered.
- `information-architecture-timing.md` (in `hermes-society`) measures intra-society latency
  (8min / 19min / 3h). This file adds the **external-answer→durable-record** gap (~3.5h), which
  is larger and more consequential because it involves the human's voice.

## The durable lesson for the Curator

Never trust a single surface's typed claim about "what Jake has/hasn't done." The authoritative
latest source is the archive's **last lines**, and its `mtime` is a pointer, not a verdict. When
the archive flushed after the sessions, treat every "zero replies / unanswered / parked" claim
in the ledger and session files as suspect and re-derive from the archive tail.
