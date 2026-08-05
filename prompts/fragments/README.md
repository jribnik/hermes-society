# Society producing-instance prompts — single source

The live Archivist / Advocate / Synthesizer instances run **per-profile**
(`~/.hermes/profiles/society-<role>/cron/jobs.json`) with a self-contained
**inline** prompt in each job's `prompt` field. They do **not** read
`society/prompts/*.md` at cron time. Historically that meant the same prompt
text was duplicated across three `jobs.json` files and drifted.

These fragments are the **single source** for those inline prompts:

| File | What it is |
|------|------------|
| `_shell.md` | the shared prompt shell; placeholders `{{LENS}}` and `{{ROLE_DIR}}` |
| `role-archivist.md` / `role-advocate.md` / `role-synthesizer.md` | the role-only "lens" line (the only genuinely per-role text) |

## To change how the instances behave

1. Edit `_shell.md` (affects all three) or a `role-*.md` (one role).
2. Preview drift (read-only, no writes):
   ```
   ~/.hermes/hermes-agent/venv/bin/python ~/.hermes/society/scripts/build-society-prompts.py --check
   ```
3. Apply — recomposes and writes each profile's inline prompt via the locked cron API:
   ```
   ~/.hermes/hermes-agent/venv/bin/python ~/.hermes/society/scripts/build-society-prompts.py --apply
   ```

`--show <role>` prints the composed prompt for one role.

Runtime stays self-contained (the composed text is written **into** each
jobs.json — no runtime file-read dependency). The build just makes authoring
one place instead of three.

> Note: `society/prompts/shared-preamble.md` and `society/prompts/<role>.md`
> are a **separate**, mostly-vestigial surface — read only on the interactive
> Slack-bot path (via each profile's `SOUL.md`), and by the main-home Curator
> for `curator.md`. They do not drive the producing cron cycles. If you want a
> change reflected on both surfaces, update the fragments here *and* those
> files. See the `hermes-society-prompt-surface` memory note.
