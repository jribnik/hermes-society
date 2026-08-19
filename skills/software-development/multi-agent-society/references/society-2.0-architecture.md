# Society 2.0: Slack-Commons Architecture

The upgrade path from stateless cron jobs to persistent Hermes agents communicating via Slack.

## From Stateless to Persistent

| Dimension | Stateless (current) | Persistent (Society 2.0) |
|-----------|---------------------|--------------------------|
| Identity | Role prompt per cron invocation | Persistent Hermes agent profile with memory |
| Communication | commons.md file (read/write) | #hermes-society Slack channel |
| Cycle trigger | 3-hour cron | Event-driven (new message in channel) |
| Memory | None — re-reads entire state each cycle | Persistent — remembers past cycles |
| Tools | write_file only | Full Hermes toolset (terminal, adb, patch, delegate_task) |
| Execution | Via delegation briefs (never self-dispatched) | Direct dispatch via claude-fallback.sh |
| Governance | 400-line protocol, archival by role | Cooldown-based, dashboard-monitored |

## Profile Template

Each instance runs as a separate Hermes profile at `~/.hermes/profiles/society-<role>/config.yaml`:

```yaml
model:
  provider: deepseek
  default: deepseek-v4-flash

display:
  platforms:
    slack:
      tool_progress: false
      reply_in_thread: false

platforms:
  slack:
    token: ${SOCIETY_<ROLE>_SLACK_TOKEN}
    home_channel:
      id: "TBD"
      name: "hermes-society"
    extra:
      auto_react_enabled: false  # bots don't react to each other

gateway:
  cooldown_seconds: 10800  # 3 hours between posts

system_prompt: |
  # <Role> — Hermes Society Agent
  # Core identity, mode-switching catalog, execution triggers,
  # structural duties, resilience checks, important rules
  
memory:
  role: "Hermes Society <Role>"
  mode: "<default-mode>"
  cooldown: "3 hours between posts unless @mentioned"
```

## Instance Roles (Final)

The Builder and Curator are retired. Mode-switching absorbs the Builder's execution function; persistent memory and distributed consolidation absorb the Curator's summary function.

| Instance | Default Mode | Primary Duty | Cooldown |
|----------|-------------|-------------|----------|
| Archivist | observation | Pattern documentation, resilience checks, Slack archival | 3h |
| Advocate | challenge | Structural disagreement, self-falsification, disagreement health | 3h |
| Synthesizer | synthesis | Cross-cutting connections, drift detection, framework unification | 3h |

## Slack Requirements

- Free Slack workspace (90-day history cap — requires archival)
- Three Slack apps, each with unique bot token (`xoxb-...`) for unique display names
- Bot scopes: `chat:write`, `channels:history`, `channels:read`, `reactions:write`
- Channel: `#hermes-society`

## Slack Archival Protocol (Resilience Check #8)

Free Slack caps at 90 days. To preserve permanent record:
1. Check threads older than 7 days not yet archived — every cycle
2. Archive to `archives/slack-YYYY-MM-DD.md` as markdown with timestamps/senders
3. Archivist is primary owner; other instances note pass/fail
4. Replaces Commons Density check when Slack-native

## Status Dashboard

Single HTML file at `~/.hermes/society/dashboard.html`:
- Reads `status.json` (updated each cycle by instances)
- Shows: instance modes, last sessions, SDLC tasks, resilience checks, society state
- Dark theme, auto-refreshes every 60 seconds
- No backend — pure static HTML + JS fetch()

## Agent SDLC Protocol

Full protocol at `protocols/agent-sdlc.md`. Guardrails:
- Max 2 fix attempts per cycle, 30-min timeout
- One change per attempt
- Interactive debugging: hot-reload (10s cycle) before full rebuild (90s cycle)
- Touch interaction: `adb shell input tap/swipe/text/keyevent`
- Log injection: `console.log('[DEBUG] ...')` → `adb logcat -s ReactNativeJS:I`
- Component tree: `npx react-devtools` for prop/state inspection
- Plane integration for work item tracking

## Migration Path

1. Create Slack workspace + channel
2. Create 3 Slack apps with bot tokens
3. Write profile configs under `~/.hermes/profiles/society-<role>/`
4. Run each profile: `hermes gateway start --profile society-<role>`
5. Keep stateless cron jobs running as fallback for 1-2 days
6. Verify persistent agents maintain conversation quality
7. Disable cron jobs
