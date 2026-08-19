# Anthropic OAuth — Third-Party Billing Policy

## The Problem (Discovered Jul 16, 2026)

Anthropic changed their OAuth token billing policy. When a third-party app (like Hermes Agent) uses an OAuth token obtained from Claude Pro, Anthropic now bills against **extra usage** credits rather than the Pro plan's included quota. 

Error message from the gateway:

```
ERROR agent.conversation_loop: Non-retryable client error: Error code: 400 - 
{'type': 'error', 'error': {'type': 'invalid_request_error', 
'message': 'Third-party apps now draw from your extra usage, not your plan limits. 
Add more at claude.ai/settings/usage and keep going.'}}
```

## What Works, What Doesn't

- **`claude -p` (Claude Code CLI)** — ✅ First-party, draws from plan limits. Only safe path for Pro OAuth.
- **Hermes Provider with OAuth** — ❌ Third-party, bills against extra usage.
- **Hermes Provider with API key** — ✅ Works normally (billed against API key balance)

## What We Tried

- Built complete OAuth auth handler (194 lines, 55 tests) in `feature/anthropic-oauth`
- Set `providers.anthropic.auth_type = oauth_claude_code` in config
- Tried Fable 5 → Opus 4.8 → Sonnet 5 via OAuth — all work technically but bill extra usage
- Removed Anthropic API key from `.env` to force OAuth-only path — still bills extra usage
- The API key race condition: with both OAuth and API key configured, the key wins and bills API credits silently

## Feature Status

Built, tested, policy-blocked. Code at `jribnik/hermes-agent` branch `feature/anthropic-oauth`. Key files:
- `providers/auth/anthropic_oauth.py` — reads `~/.claude/.credentials.json`, refreshes tokens
- `hermes_cli/providers.py` — OAuth handler registry
- `hermes_cli/runtime_provider.py` — credential resolution

## Jake's Working Config (as of Jul 17, 2026)

- **Primary model**: DeepSeek v4-pro (funded)
- **Fallback**: Claude Sonnet 5 via API key (rarely triggered)  
- **Delegation**: `claude -p` via `claude-fallback.sh` (Pro OAuth, draws from plan)
- **Fallback chain for delegation**: Fable → Opus → Sonnet
