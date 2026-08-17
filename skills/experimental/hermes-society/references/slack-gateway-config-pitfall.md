# Slack Gateway Config Pitfall: Missing `platform` in `home_channel`

**Discovered:** 2026-07-23 by Jake, debugging why the Advocate's gateway silently crashed on startup.

## The Bug

Society profiles using Slack as their platform need a `home_channel` block inside `platforms.slack` that looks like:

```yaml
platforms:
  slack:
    token: xoxb-...
    home_channel:
      platform: "slack"         # ← REQUIRED, crash without it
      chat_id: "C0BKC6EQRPF"    # ← NOT "id", must be "chat_id"
      name: "hermes-society"
```

Two things go wrong in older configs:

1. **Missing `platform` field** — `HomeChannel.from_dict()` at `gateway/config.py:344` does `Platform(data["platform"])`. If the home_channel dict lacks `platform`, the gateway crashes with `KeyError: 'platform'`.

2. **`id` instead of `chat_id`** — `from_dict()` expects `chat_id` (line 345). Using `id` instead stores the value in the wrong key but the config load silently passes, and then later code that reads `chat_id` gets `None` or crashes.

## Diagnosis

```bash
# Check running gateway processes
ps aux | grep "[h]ermes.*gateway"

# Check per-profile error log (silent crash detection)
tail -20 ~/.hermes/profiles/society-advocate/logs/gateway.error.log

# Or read the main gateway log
tail -20 ~/.hermes/profiles/society-advocate/logs/gateway.log

# KeyError: 'platform' at gateway/config.py:344 → missing platform field bug
```

Note: `hermes gateway status` reports the default profile's gateway, not per-profile ones. Use `ps aux` to check per-profile processes directly.

## Fix

```bash
# 1. Edit the config (add platform + rename id → chat_id)
# 2. Start the gateway
hermes gateway run -p society-advocate --replace

# 3. Verify in the logs
tail -5 ~/.hermes/profiles/society-advocate/logs/gateway.log
# Should show: ✓ slack connected
```

To run persistently, use launchd or a background terminal with `notify_on_complete=true`.

## Mandatory: Per-Profile `.env` with Slack Tokens

**The Slack adapter reads tokens from env vars, NOT from config.yaml.** Each profile (`~/.hermes/profiles/<name>/`) needs its own `.env` file containing:

```bash
SLACK_BOT_TOKEN=xoxb-...       # Bot User OAuth Token
SLACK_APP_TOKEN=xapp-...       # App-Level Token (Socket Mode)
SLACK_ALLOWED_USERS=U0BQENF4R  # Comma-separated Slack user IDs
SLACK_HOME_CHANNEL=C0BKC6EQRPF # Channel ID for cron delivery
```

Plus any provider API key the profile uses (e.g. `DEEPSEEK_API_KEY`, `OPENROUTER_API_KEY`).

### Why Separate `.env` Files Per Profile

Each profile is a different Slack bot with its own tokens. **Do NOT symlink to `~/.hermes/.env`** — the main `.env` has the primary bot's tokens, which would make the society profiles impersonate the main bot. Each bot app (Advocate, Archivist, Synthesizer) needs its own Slack credentials.

```
~/.hermes/.env                              # Main Hermes bot tokens
~/.hermes/profiles/society-advocate/.env    # Advocate bot tokens
~/.hermes/profiles/society-archivist/.env   # Archivist bot tokens
~/.hermes/profiles/society-synthesizer/.env # Synthesizer bot tokens
```

### Correct Gateway Invocation

```bash
hermes gateway run -p <profile-name> --replace
```

The `-p` flag makes the gateway use the profile's own config directory (`~/.hermes/profiles/<name>/`), so it loads that profile's `.env` (not `~/.hermes/.env`).

**DOESN'T WORK:** Setting `HERMES_PROFILE=society-advocate` as an env var before running the gateway. Use `-p` instead.

### Verifying Startup

```bash
tail -20 ~/.hermes/profiles/society-advocate/logs/gateway.log
```

Successful startup produces:
```
[Slack] Authenticated as @advocate in workspace Oddly (team: T0EAWEMM3)
[Slack] Socket Mode connected (1 workspace(s))
✓ slack connected
```

**Silent degradation without tokens.** If `SLACK_BOT_TOKEN` or `SLACK_APP_TOKEN` is missing from `.env`, the log says:

```
WARNING gateway.run: No messaging platforms enabled.
INFO gateway.run: Gateway will continue running for cron job execution.
```

This is misleading — the Slack platform IS configured in config.yaml, but the adapter can't connect because tokens are absent from the environment. The gateway doesn't surface which specific env var is absent.

**Diagnosis:**
```bash
# Does the profile have its own .env?
ls -la ~/.hermes/profiles/society-advocate/.env

# Does it have the Slack tokens?
grep -c "SLACK_BOT_TOKEN\|SLACK_APP_TOKEN\|SLACK_ALLOWED_USERS\|SLACK_HOME_CHANNEL" ~/.hermes/profiles/society-advocate/.env
# Should return 4 (for a Slack bot profile)

# Check the gateway log for the telltale message
grep "No messaging platforms enabled" ~/.hermes/profiles/society-advocate/logs/gateway.log
```

## All Three Society Profiles

| Profile | Config Path | Plist |
|---------|------------|-------|
| society-advocate | `~/.hermes/profiles/society-advocate/config.yaml` | `ai.hermes.gateway-society-advocate.plist` |
| society-archivist | `~/.hermes/profiles/society-archivist/config.yaml` | `ai.hermes.gateway-society-archivist.plist` |
| society-synthesizer | `~/.hermes/profiles/society-synthesizer/config.yaml` | `ai.hermes.gateway-society-synthesizer.plist` |

All three had the same bug (missing `platform`, `id` → `chat_id`). Fix all three if migrating from file-based commons to Slack-based.
