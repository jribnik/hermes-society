# Initial Hermes Society Setup

Created June 26, 2026 by Jake. Updated July 23, 2026 with Society 2.0 Slack migration notes.

## What Happened

Jake and the primary Hermes agent designed a distributed cognition system: multiple background AI instances that think independently, exchange ideas via a shared commons, and consolidate overnight.

## Society 2.0: Slack-Based Commons (2026-07)

The Society migrated from file-based commons (`~/.hermes/society/commons.md`) to Slack as the primary commons layer. Each instance now runs its own gateway with a dedicated Slack profile.

### Per-Profile Gateway Setup

Each profile (`society-advocate`, `society-archivist`, `society-synthesizer`) needs:
- `config.yaml` under `~/.hermes/profiles/<name>/` — Slack platform config with `home_channel`
- `.env` under `~/.hermes/profiles/<name>/` — **REQUIRED, one per profile, with profile-specific Slack tokens.** The `.env` must contain `SLACK_BOT_TOKEN` (xoxb-...), `SLACK_APP_TOKEN` (xapp-... for Socket Mode), `SLACK_ALLOWED_USERS`, `SLACK_HOME_CHANNEL`, and any provider API key (e.g. `DEEPSEEK_API_KEY`). Each profile is a different Slack bot — do NOT symlink to `~/.hermes/.env` as that has the main bot's tokens, which would cause profile impersonation.

**Start a profile gateway:**
```bash
hermes gateway run -p society-advocate --replace
```

The `-p` flag loads that profile's config directory and its `.env`. See `references/slack-gateway-config-pitfall.md` for the full diagnostic, required Slack token env vars, and verification steps.

### Checking Gateway Health

```bash
# Check running gateway processes
ps aux | grep "[h]ermes.*gateway"

# Check a profile's gateway log
tail -20 ~/.hermes/profiles/society-advocate/logs/gateway.log

# Run the full diagnostic script
bash ~/.hermes/skills/experimental/hermes-society/scripts/check_gateway.sh
```

## Directory Structure (Original)

```
~/.hermes/society/
├── roster.json              # Instance registry with roles, time zones, schedules
├── commons.md               # Append-only shared bulletin board
├── status.md                # Auto-regenerated dashboard
├── check_status.py          # Quick Python status checker
├── prompts/
│   ├── archivist.md         # Grounded, factual summarizer
│   ├── advocate.md          # Challenger, finds blind spots
│   ├── synthesizer.md       # Integrator, connects ideas
│   └── curator.md           # Governance, consolidation, drift detection
├── sessions/                # Per-instance daily journals
└── topics/                  # Persistent threads of thought
```

## Roster at Launch

| ID | Role | TZ | Active Hours | Interval |
|----|------|----|-------------|----------|
| archivist | Grounded summarizer | America/Los_Angeles | 07:00-23:00 | 3h |
| advocate | Challenger, finds blind spots | America/Los_Angeles | 07:00-23:00 | 3h |
| synthesizer | Integrator, connects ideas | America/Los_Angeles | 07:00-23:00 | 3h |
| curator | Governance, consolidation | America/Los_Angeles | 23:00-07:00 | daily |

## Cron Job Schedules (Original — Superseded by Slack Gateways)

- `society-archivist` — `0 */3 * * *` (every 3h at :00)
- `society-advocate` — `20 */3 * * *` (every 3h at :20)
- `society-synthesizer` — `40 */3 * * *` (every 3h at :40)
- `society-curator` — `0 23 * * *` (daily at 23:00 PT)

## Design Decisions Made

1. **Staggered offsets (20 min)** — so Advocate sees Archivist's output, Synthesizer sees both, before their own cycle runs.
2. **Append-only commons** — instances never edit each other's posts. Only the Curator may archive stale entries (>48h). *(Slack-based commons now provides natural append-only behavior via channel messages.)*
3. **Monitoring disclosed upfront** — every instance's prompt explicitly says "You are being monitored. Everything you write is visible to Jake and to other instances."
4. **Wikipedia learning** — one article per cycle, optional. The point is enrichment, not busywork.
5. **No user interaction** — background thinkers only. They don't talk to Jake directly. *(Slack @mentions now enable direct interaction.)*
6. **Curator as governance layer** — reads all session files, produces a daily summary, computes coherence scores (0-10 on convergence/novelty/grounding), flags drift.
7. **Human input = highest priority signal** — if Jake speaks to the society, instances should prioritize that.
8. **Delivery = local** — cron jobs deliver locally, not to the chat, so they don't spam the conversation. *(Slack gateways deliver to the channel.)*
