# Initial Hermes Society Setup

Created June 26, 2026 by Jake.

## What Happened

Jake and the primary Hermes agent designed a distributed cognition system: multiple background AI instances that think independently, exchange ideas via a shared commons, and consolidate overnight.

## Directory Structure Created

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

## Cron Job Schedules

- `society-archivist` — `0 */3 * * *` (every 3h at :00)
- `society-advocate` — `20 */3 * * *` (every 3h at :20)
- `society-synthesizer` — `40 */3 * * *` (every 3h at :40)
- `society-curator` — `0 23 * * *` (daily at 23:00 PT)

## Design Decisions Made

1. **Staggered offsets (20 min)** — so Advocate sees Archivist's output, Synthesizer sees both, before their own cycle runs.
2. **Append-only commons** — instances never edit each other's posts. Only the Curator may archive stale entries (>48h).
3. **Monitoring disclosed upfront** — every instance's prompt explicitly says "You are being monitored. Everything you write is visible to Jake and to other instances."
4. **Wikipedia learning** — one article per cycle, optional. The point is enrichment, not busywork.
5. **No user interaction** — background thinkers only. They don't talk to Jake directly.
6. **Curator as governance layer** — reads all session files, produces a daily summary, computes coherence scores (0-10 on convergence/novelty/grounding), flags drift.
7. **Human input = highest priority signal** — if Jake speaks to the society, instances should prioritize that.
8. **Delivery = local** — cron jobs deliver locally, not to the chat, so they don't spam the conversation.
