# Claude Code CLI — Remote OAuth Auth

How to authenticate `claude` CLI when the user isn't at their desktop (e.g., on phone).

## Background

Claude Code CLI supports three auth methods:
- **OAuth (browser)** — for Pro/Max subscriptions. Opens a browser, user signs in.
- **API key** — `ANTHROPIC_API_KEY` env var. Requires API billing (not Pro).
- **Third-party** — e.g., AWS Bedrock (`claude auth status` shows `authMethod: "third_party"`).

This reference covers the OAuth flow when the user is remote.

## The PKCE Trap

The OAuth URL is tied to a **specific CLI session** via PKCE (`code_challenge`). If you:
1. Run `claude auth login` → get URL with `code_challenge=A`
2. User opens URL on phone → gets authorization `code`
3. That code ONLY works with the CLI session that has `code_challenge=A`

If the CLI times out and you re-run `claude auth login`, you get a NEW URL with `code_challenge=B` — the old code won't work. **401 error = PKCE mismatch.**

## Correct Remote Flow

### Step 1: Start CLI in background PTY
```
terminal(command="claude auth login", background=true, pty=true, timeout=300)
```

### Step 2: Wait for the prompt (5s)
```
process(action="wait", session_id="<id>", timeout=5)
```

Output will show the URL and `Paste code here if prompted >`.

### Step 3: Give user the URL
Extract the full URL from the output and send it to the user. They open it on their phone, sign in to Anthropic, and get an authorization code.

### Step 4: Submit the code
```
process(action="submit", session_id="<id>", data="<code from user>")
```

### Step 5: Verify
```
process(action="wait", session_id="<id>", timeout=15)
```
Should exit 0. Then:
```
terminal(command="claude auth status")
```
Should show `"loggedIn": true` and `"authMethod": "oauth"` (or similar).

## Switching from Bedrock to OAuth

If currently authed via Bedrock:
```
claude auth logout    # clears third-party auth
claude auth login     # starts OAuth flow
```

## Verification
```
claude auth status
# Expected: {"loggedIn": true, "authMethod": "oauth", ...}
# NOT: {"authMethod": "third_party", "apiProvider": "bedrock"}
```
