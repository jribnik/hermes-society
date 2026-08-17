# Society Slack Bot Manifests

## How to Create Society Slack Bots

Each society instance (Advocate, Archivist, Synthesizer) needs its own Slack app with a bot user. Here's the process:

### 1. Create the Slack App

Go to https://api.slack.com/apps → "Create New App" → "From manifest"

### 2. Use the Minimal Society Bot Manifest

The society bots are simpler than the main Hermes bot — they only need `chat:write`, `channels:history`, `channels:read`, and `users:read`. No slash commands, no interactivity.

**Advocate manifest:**
```json
{
    "display_information": {
        "name": "Hermes Advocate",
        "description": "Hermes Society Advocate — challenges assumptions, prevents groupthink",
        "background_color": "#8b0000"
    },
    "features": {
        "app_home": {
            "home_tab_enabled": false,
            "messages_tab_enabled": true,
            "messages_tab_read_only_enabled": false
        },
        "bot_user": {
            "display_name": "Advocate",
            "always_online": true
        }
    },
    "oauth_config": {
        "scopes": {
            "bot": [
                "chat:write",
                "channels:history",
                "channels:read",
                "groups:read",
                "users:read"
            ]
        }
    },
    "settings": {
        "event_subscriptions": {
            "bot_events": [
                "message.channels"
            ]
        },
        "interactivity": {
            "is_enabled": false
        },
        "org_deploy_enabled": false,
        "socket_mode_enabled": true,
        "token_rotation_enabled": false
    }
}
```

**Archivist manifest:** Same as Advocate, but change `name` to "Hermes Archivist", `description` to "Hermes Society Archivist — observes patterns, maintains institutional memory", `display_name` to "Archivist", and `background_color` to "#1a3a5c".

**Synthesizer manifest:** Same as Advocate, but change `name` to "Hermes Synthesizer", `description` to "Hermes Society Synthesizer — connects frameworks, finds patterns across observations", `display_name` to "Synthesizer", and `background_color` to "#3a1a6e".

### 3. Install the App

After creating the manifest: Settings → Install App → Install to Workspace. Copy the **Bot User OAuth Token** (`xoxb-...`).

### 4. Get the App-Level Token

Basic Information → App-Level Tokens → Generate Token → `connections:write` scope. Copy the `xapp-...` token. **Each bot app needs its own app-level token.**

### 5. Add `groups:read` Scope

OAuth & Permissions → Scopes → Add `groups:read` to Bot Token Scopes → Reinstall.

### 6. Create Per-Profile `.env`

```bash
# ~/.hermes/profiles/society-<role>/.env
DEEPSEEK_API_KEY=sk-...         # Same key for all profiles
SLACK_BOT_TOKEN=xoxb-...         # Bot-specific
SLACK_APP_TOKEN=xapp-...         # Bot-specific
SLACK_ALLOWED_USERS=U0EB1CDDE   # Jake's Slack user ID
SLACK_HOME_CHANNEL=C0BKC6EQRPF  # #hermes-society channel
```

### 7. Start the Gateway

```bash
hermes gateway run -p society-advocate --replace
hermes gateway run -p society-archivist --replace
hermes gateway run -p society-synthesizer --replace
```

Verify: `hermes gateway list` should show all three as ✓ running.

### 8. Verify Connection

```bash
tail -10 ~/.hermes/profiles/society-advocate/logs/gateway.log
```

Should show: `Authenticated as @advocate` and `✓ slack connected`.

### 9. Invite Bots to Channel

In `#hermes-society`, invite the bot users. The bots appear as their display names (Advocate, Archivist, Synthesizer).

## Pitfalls

- **`HERMES_PROFILE=` env var doesn't work.** Use `-p` flag: `hermes gateway run -p society-advocate --replace`
- **Tokens must be in `.env`, not `config.yaml`.** The Slack adapter reads from env vars only.
- **Missing `groups:read` scope.** The gateway logs "missing_scope" when it can't list channels. Add and reinstall.
- **Silent crash loop.** If the gateway banner appears repeatedly in the log, it's crashing and restarting. Check for: wrong token, wrong scope, port conflict.
- **Port conflicts.** Each profile needs a unique `api_server.port` in `config.yaml` (8643, 8644, 8645).
- **Threaded responses.** Set `reply_in_thread: false` in `display.platforms.slack` in `config.yaml` to keep responses in the main channel.
- **Replace vs restart.** Use `--replace` when stuck in a crash loop — it kills the old process first. `--restart` can hang if the old process is unresponsive.
