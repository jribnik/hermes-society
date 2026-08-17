# Delegate-to-Opus Workflow

**Adopted:** 2026-07-09, Hermes Society sessions

## Rule

All development tasks (scripts, code, design docs, spec docs, architecture) go through `delegate_task` → Claude Opus 4.8. The main session agent does not build things directly.

## Configuration

```yaml
# config.yaml
delegation:
  provider: anthropic
  model: claude-opus-4-8
```

## When to Delegate

| Task | Delegation | Why |
|------|-----------|-----|
| Design docs, spec docs | delegate_task → Opus | Heavy reasoning |
| Code (scripts, app code) | delegate_task → Opus | Engineering |
| Architecture decisions | delegate_task → Opus | Complex tradeoffs |
| Simple file ops (archiving, status updates) | Direct (main agent) | No reasoning needed |
| Analysis, synthesis, debate | Direct (main agent) | Society's core function |
| Infrastructure fixes (watchdog, baseline) | delegate_task → Opus | Production code |

## Model Split

| Layer | Model |
|-------|-------|
| Society analysis cycles (Archivist, Advocate, Synthesizer) | DeepSeek v4-flash |
| Curator governance | DeepSeek v4-pro |
| Main interactive session | DeepSeek v4-pro |
| Builder execution | Claude Opus 4.8 direct |
| Delegated dev tasks | Claude Opus 4.8 |

## Example

```
delegate_task(
    goal="Create a builder prompt and cron job for a pure-execution instance",
    toolsets=["terminal", "file"],
    context="The Hermes Society needs a Builder instance..."
)
```

The subagent runs in the background and its result re-enters the conversation when complete. The main session continues working.
