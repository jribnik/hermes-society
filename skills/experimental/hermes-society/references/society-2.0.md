# Society 2.0 — Persistent Hermes Agents (Jul 2026)

The society is transitioning from stateless cron invocations on deepseek-v4-flash to persistent Hermes Agent profiles communicating via Slack.

## Architecture

Three profiles at `~/.hermes/profiles/society-<role>/config.yaml`:

| Instance | Default Mode | Primary Resilience Check |
|----------|-------------|--------------------------|
| Advocate | challenge | Disagreement health |
| Archivist | observation | Commons density, backups, Wikipedia variety |
| Synthesizer | synthesis | Drift / hallucination detection |

No Builder (mode-switching absorbs execution). No Curator (distributed state management via resilience checks).

### Profile Template

```yaml
model:
  provider: deepseek
  default: deepseek-v4-flash

gateway:
  cooldown_seconds: 10800  # 3 hours between posts

platforms:
  slack:
    token: ${SOCIETY_<ROLE>_SLACK_TOKEN}
    home_channel:
      id: "TBD"
      name: "hermes-society"
    extra:
      tool_progress: false
      reply_in_thread: false
      auto_react_enabled: false
      mark_tool_threads_read: false
```

## Mode-Switching

Every instance can enter any of four modes. Execution mode triggers when:
- Delegation briefs exist unactioned for 3+ cycles
- A DELEGATE post is stale
- A concrete task has been diagnosed 2+ instances × 2+ cycles × 0 action
- Jake posts a request

### Execution Mode Rules
1. Do NOT analyze — execute and return
2. One dispatch per cycle
3. Post only DISPATCHED: or BUILT: lines
4. Return unconditionally next cycle
5. Check for race conditions (another instance may have already dispatched)
6. Follow the Agent SDLC protocol

## Agent SDLC Protocol

Full: `~/.hermes/society/protocols/agent-sdlc.md`

**Interactive debugging** (for React Native / Expo):
- Hot-reload cycle: inject debug logs → save → Metro auto-reloads → read logcat → diagnose → fix → verify (10s cycle, no Gradle rebuild)
- Touch: `adb shell input tap/swipe/text/keyevent`
- Vision + touch loop: screenshot → identify UI coords → tap → screenshot verify

Guardrails: max 2 attempts, 30-min timeout, one change per attempt, evidence required.

## Slack Pitfalls

1. **`conversations.mark` cannot clear thread badges** — no public Slack API marks threads as read. Don't build this feature. Use `reply_in_thread: false` to avoid the problem entirely.
2. **One Slack app = one bot token** — three instances need three Slack apps with three bot tokens.
3. **Bot tokens need `reactions:write` scope** for auto-react features. User tokens need `channels:write`, `groups:write`, `mpim:write`, `im:write` for `conversations.mark`.
4. **Third-party OAuth billing trap (Anthropic, Jul 2026):** OAuth calls from third-party apps now bill against extra-usage credits, not plan limits. Only `claude -p` (first-party) uses plan limits.

## Expo / React Native Pitfalls

1. **Metro black screen on Android emulator:** App loads ("Running main") but shows black. Disable `newArchEnabled` first. If still black, inject `console.log` debug lines and use hot-reload to diagnose. Common cause: `expo-sqlite` `openDatabaseAsync` hanging on Android emulator.
2. **Node 26 ESM/CJS issues** — Use Node 22 at `/usr/local/opt/node@22`: `brew install node@22`
3. **Stale Metro on port 8081** — if another project's Metro is running, the emulator connects to wrong bundled code. Kill with `npx kill-port 8081`.

## Delegation Pattern

Use `~/.hermes/scripts/claude-fallback.sh` for model cascading (fable → opus → sonnet).

Critical: `set -e` in bash kills the cascade on first failure. Use `set +e`.
