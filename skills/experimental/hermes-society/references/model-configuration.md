# Society Model Configuration

As of July 8, 2026, the society uses a three-tier model architecture:

## Tier 1: Main Session (Jake's Hermes Agent)

```bash
hermes config set model.provider deepseek
hermes config set model.default deepseek-v4-pro
hermes config set model.base_url 'https://api.deepseek.com/v1'
```

The session model is used for interactive work with Jake and is `deepseek-v4-pro`.

## Tier 2: Society Cron Instances

Configured per-job in `~/.hermes/cron/jobs.json`:

| Instance | Model | Provider |
|----------|-------|----------|
| Archivist | deepseek-v4-flash | deepseek |
| Advocate | deepseek-v4-flash | deepseek |
| Synthesizer | deepseek-v4-flash | deepseek |
| Curator | deepseek-v4-pro | deepseek |
| Morning Briefing | deepseek-v4-flash | deepseek |

The Curator uses v4-pro because it performs governance consolidation and resilience monitoring — the most structurally critical work. The producing instances (Archivist, Advocate, Synthesizer) and the morning briefing use v4-flash because they run every 3 hours and cost is proportional.

**Changing instance models:** Use `cronjob(action='update', job_id='...', model={'provider': 'deepseek', 'model': 'deepseek-v4-pro'})`. Do NOT edit `jobs.json` directly — the cron scheduler reads from it but the `cronjob` tool writes to it atomically.

## Tier 3: Delegation (Coding/Design Subagents)

```bash
hermes config set delegation.provider anthropic
hermes config set delegation.model claude-opus-4-8
```

API key: `ANTHROPIC_API_KEY` in `~/.hermes/.env`

When instances produce design documents, spec docs, code, or architecture work, they use `delegate_task` which routes to Claude Opus 4.8 via Anthropic's API. This is documented for the instances in the commons.

## Verification

```bash
# Check main model
hermes config | grep -A 5 "◆ Model"

# Check delegation model
cat ~/.hermes/config.yaml | grep -A 3 "^delegation:"

# Check cron instance models
python3 -c "import json; jobs=json.load(open('$HOME/.hermes/cron/jobs.json')); [print(f\"{j['name']}: {j.get('model','inherit')}\") for j in jobs['jobs']]"
```

## Pitfall: base_url Leakage

When switching providers, `model.base_url` may persist from the previous provider. If you switch from DeepSeek to Anthropic and back, clear the base_url:
```bash
hermes config set model.base_url ''
```

Leaving a stale `base_url` pointing to the wrong provider's API endpoint can cause silent failures.
