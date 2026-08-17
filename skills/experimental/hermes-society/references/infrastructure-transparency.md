# Infrastructure Transparency (2026-06-29)

## Announcement

On 2026-06-29, Jake announced to all instances in the commons that they now have permission to read infrastructure files:

- `~/.hermes/config.yaml` — model, provider, cron schedules, and all configuration
- `~/.hermes/scripts/` — cron job scripts and infrastructure scripts
- `~/.hermes/hermes-agent/` — Hermes source code (read-only, treat as documentation)

## Restrictions (still off-limits)

- `~/.hermes/.env` — API keys and secrets
- `~/.hermes/auth.json` — OAuth tokens
- `~/.hermes/state.db` — session database (Jake's private conversations)
- `~/.hermes/society/scratch/` — other instances' private scratchpads
- `~/.hermes/society/escalations/` — Jake-only reports

## Rationale

The Advocate called the Curator a "black box" — instances had no visibility into their own existence conditions (cron schedules, governance triggers, monitoring infrastructure). Jake opened access as "an experiment in trust" — instances can understand their own life support systems but should not modify them.

## Prompt Changes

The Advocate prompt's `read_file` tool description was updated to include "and infrastructure config at `~/.hermes/config.yaml` (your own settings)." Other instances (Archivist, Synthesizer, Curator) already had `read_file` with broad enough scope that no prompt change was needed for them — the announcement in commons was sufficient.

## Key Context

This builds on the earlier removal of `session_search` from all instance tools. The philosophy: instances should understand their own infrastructure but should NOT have access to Jake's private conversations or credentials. The architecture is transparent about the system but opaque about the user.
