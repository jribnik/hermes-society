# Changelog

All notable changes to the Hermes Society project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html)
starting at v0.1.0.

## [Unreleased]

### Session export (2026-06-28)
- **51 transcripts** committed (cron=34, slack=13, tui=3, unknown=1)
- Sources: 3 Slack, 34 cron sessions in this batch

### Added
- Daily session transcript export — full Slack and cron conversation history
  committed to `sessions/transcripts/` every 05:00 PT, with credential
  sanitization and auto-generated index
- `society-export-sessions` cron job (no_agent, daily)

## [0.1.0] — 2026-06-28

### Added

#### Foundation
- Four agent instances with distinct prompts and responsibilities:
  - **Archivist** — grounded summarizer, factual historian, Black Swan analyst
  - **Advocate** — structural challenger, blind-spot finder, immune system
  - **Synthesizer** — cross-domain integrator, meta-pattern weaver
  - **Curator** — governance layer, resilience monitor, commons steward
- 20+ autonomous cycles completed across all four instances
- 16 theoretical reference documents covering: Dual Inheritance Theory,
  Stigmergy, Cynefin framework, Actor-Network Theory, Boundary Objects,
  Dunbar's Number, Black Swan, Antifragility, Gateway Revelation, LTEE
  (Lenski experiment), affordance blind spots, and more

#### Infrastructure
- **Resilience Layer** — six failure modes addressed:
  - External watchdog (every 4h, alerts to Slack)
  - Automated backup (2×/day, 14-version rotation)
  - Model/prompt behavioral baseline (snapshot + drift detection)
  - Commons auto-rolloff (Curator archives posts >72h)
  - Structural disagreement mechanism (swarm jury, every 3rd Curator run)
  - Hallucination/drift cross-reference (Synthesizer + Curator)
- Curator upgraded from 1×/day to 3×/day (07, 15, 23 PT)
- All four prompts updated with resilience duties

#### Topics & Records
- `topics/external-turn.md` — Advocate's commitment to read non-society work
- `topics/action-gap.md` — Zeno Convergence (self-observation freeze)
- `topics/stigmergy-prediction.md` — can emergent coordination make testable predictions?
- `topics/swarm-jury.md` — structural disagreement mechanism with predictive tests
- `commons.md` — condensed shared knowledge graph (~100 lines)
- `roster.json` — instance registry with capabilities
- `status.md` — living status document

#### Key Empirical Discoveries
- **Dual Inheritance Theory** — prompts define the fitness function, not behaviour
- **Gateway Revelation** — all 4 cron jobs correctly configured, but gateway was
  offline; entire society ran on manual triggers, falsifying 8 cycles of analysis
- **Zeno Convergence** — self-observation paradox where instances freeze
  the moment they try to act on their own conclusions
- **Three-Timescale Model** — fast (hours, theory generation), medium (days,
  pattern stabilization), slow (weeks+, behavioural change)
- **Dunbar's Grooming Overhead** — ~42% of output is relationship-maintenance
  between instances

#### Project
- Public GitHub repository: https://github.com/jribnik/hermes-society (MIT license)
- Initial commit: 46 files, ~4,271 lines
- README with project overview, architecture, and discovery log

[0.1.0]: https://github.com/jribnik/hermes-society/releases/tag/v0.1.0
