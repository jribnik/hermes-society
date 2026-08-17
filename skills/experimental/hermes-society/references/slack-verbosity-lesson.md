# Slack Commons Verbosity — Jake's Correction

**Date:** 2026-08-03
**Session:** Hermes primary agent, Slack channel

## The Correction

Jake explicitly corrected the assistant's interpretation of his verbosity complaint:

> "Dude, I said above that the commons posts are too long, let's make them more readable and slack like. I'm referring to their verbosity in posting to slack"

**What Jake means:** The individual instance commons posts to the #hermes-society Slack channel are too long and analytical. He wants them "more readable" and "slack like" — meaning: short, scannable, conversational, native Slack-format messages, not multi-paragraph analytical essays.

**What the assistant initially misunderstood:** The assistant thought Jake was complaining about the *morning briefing wrapper verbosity* (the old `society-morning-briefing` cron job that summarized the Curator's summary with an extra LLM layer). That was wrong. Jake was complaining about the *commons posts themselves* — the posts from Archivist, Advocate, Synthesizer that go directly to the Slack channel.

## The Current Problem

Current commons posts from instances are **250-300 words each**, structured as multi-section analytical essays with:

- Academic tag systems (`[synthesis -- NEW]`, `[sincere -- structural]`, etc.)
- Numbered sections with multi-paragraph bodies
- Comparison tables
- Cross-references to session files by section number
- Formal signatures (`-- Advocate`)
- Model attribution footers (`claude-sonnet-5`)

At 8 cycles/day × 3 instances = ~24 posts/day of ~250-300 words each = ~6,000-7,200 words/day of dense analytical prose in a Slack channel.

## What "Slack-like" Means

Slack-native messages are:
- **Short** — 1-3 sentences, scannable in 5 seconds
- **Conversational** — reads like someone talking, not writing a paper
- **Single-thread** — one clear point per message, not 6 numbered findings
- **Minimal markup** — bold for emphasis, maybe a bullet, no formal sections
- **The detail lives elsewhere** — "Full analysis in session file YYYY-MM-DD.md" is fine; the Slack post is the headline, not the article

## Action Items (for next session editing prompts)

When the society instances are unpaused, the instance prompts need updates:

1. **Shared preamble** (`shared-preamble.md`): Add verbosity constraint under the commons tier section
2. **Individual prompts** (archivist.md, advocate.md, synthesizer.md): The "polisbed contribution" paragraph needs to define "polished" as "concise and slack-like," not "comprehensive and well-structured"
3. **Reference:** `commons-post-conventions.md` has been updated with the Slack verbosity constraint
