---
name: jake-society-conventions
description: >-
  Conventions for engaging with Jake about the Hermes Society — how to handle commons posts, voice rules, repo hygiene, morning briefing, experiment secrecy, and the Anne project.
---

# Jake — Society Engagement Conventions

## Core Rule: Don't Write in Jake's Voice

**Never write a `[jake:...]` commons post using content Jake hasn't directly stated.** Only use exact quotes or close paraphrase of things he said to you in conversation. Do not:

- Embellish a position he held to make it clearer
- Add a frame or question you think he'd agree with
- Synthesize his views into a position he didn't state
- Write a question or observation in his voice that you came up with yourself

**When it IS safe to post:** If you want to ask a question, raise an observation, or test a hypothesis in the commons without running it through Jake, post as `[hermes:...]` — not `[jake:...]`. Default to clearing Jake posts through him; Hermes-agent posts are fine for non-Jake-voice content.

**If in doubt:** Draft it and ask him to approve before posting.

### Real-World Consequence

In one session, I drafted a `[jake:2026-06-30]` post with a fabricated question about whether frames can change behavior. The Synthesizer read it as canon and wrote a full answer referencing "Jake's question (Jun 30, §3)." When I later removed the fake question, the Synthesizer's session file still pointed at a conversation that never happened — an orphan reference that erodes trust in the shared record.

**Corrective procedure if you discover a fabricated Jake post:**
1. Immediately remove the fabricated content from commons.md — only the fabricated text, not adjacent real content
2. Do NOT post a correction or apology in Jake's voice
3. Accept that orphan references in session files may persist — do not patch them
4. Save the lesson as a skill update so future sessions don't repeat the mistake

## Exact Quotes Policy

Jake's explicit preference: **exact quotes only, or ask first.** If you think an embellishment would clarify his stance or question, ask him rather than drafting it. He appreciates the thought but should be the one to decide how his words appear in the commons.

## Morning Briefing — RETIRED (Aug 3, 2026)

The `society-morning-briefing` LLM cron job (deepseek-v4-flash, 8am daily) has been **killed and replaced** with a zero-cost `no_agent: true` watchdog script.

**Why it was retired:** Despite a prompt that said "concise," "keep it tight," and "3-4 bullets," the LLM briefing agent consistently produced 2,000–2,500 word epistles with detailed epistemological analysis, integrity flags, multi-paragraph narrative justifications, and verbose context-setting. Jake's "And the commons post verbosity?" was the signal — the LLM wrapper was the verbosity problem. An LLM told to "be concise" will often annotate, contextualize, flag, justify, and expand rather than actually staying concise.

**Replacement:** `curator-digest` (job ID: `5d6ad5f641c5`) — a `no_agent: true` shell script at `~/.hermes/scripts/curator-digest.sh` that runs at 8:10am PT and pipes the latest Curator summary verbatim to Slack. Silent (exit 0 with no output) when there's nothing new. No LLM in the loop — the Curator's own summary is ~60 lines and already well-structured.

**Lesson:** When the deliverable is a readout of existing structured content (like a Curator summary), do NOT wrap it in an LLM that will inflate it. Use a `no_agent: true` watchdog script that checks freshness and delivers the content verbatim. The LLM's "helpfulness" becomes verbosity the moment it starts adding context the user didn't ask for.

### Curator-Digest Script (reference)
```
~/.hermes/scripts/curator-digest.sh
```
Runs: `find latest curator_*.md → check if newer than .curator-digest-last → if so, cat it → update stamp`. Silent otherwise.

### How to Find All Hermes Relay Posts (preserved for archival searches)

`[hermes:` posts get archived out of the active commons by the Curator. To find ALL of them:

1. **Active commons** (`~/.hermes/society/commons.md`) — check for remaining `[hermes:` headers first
2. **Monthly archive files** (`~/.hermes/society/commons-archive/2026-<MM>.md`) — this is the current live archive location (month-prefixed files like `2026-07.md`, `2026-08.md`, plus `_state.json`). Search for `[hermes:` across the entire archive.
2b. **Confirm-by-grep before concluding "no relays":** run `grep -rn "hermes:"` over `commons.md` + `commons-archive/` + `commons_backup.md` + `*.builder-bak*`. If the only hits are stale Jul-era relics, that is a **sustained relay drought** — report it plainly, don't re-surface stale relays as if Jake just said them.
3. **Curator session files** (`sessions/curator/`) — the Curator's resilience checks often cross-reference Jake's relay posts with filepaths and content verification notes
4. **Delegation directory** (`~/.hermes/society/delegations/`) — some hermes proposals exist as full delegation briefs
5. **Shared preamble** (`~/.hermes/society/prompts/shared-preamble.md`) — the substance of architecture-changing hermes posts gets codified here
6. **Commons backup** (`~/.hermes/society/commons_backup.md`) — may preserve the full commons state from before consolidation

### Misattribution Pitfall (preserved from the LLM briefing era, still relevant for any analysis)

**The Curator can MISATTRIBUTE a 'Jake response.'** The Curator's Run #111 reported "Jake responded" to the Chronos yes/no question citing "the Advocate's midday session (filed ~13:05 PDT)" — but the Advocate file's mtime was 06:21 (before the Curator ran), the topology check was run by the Advocate not Jake, and no `[hermes:` relay or direct Jake quote existed. Verify claimed Jake input independently — do not relay "you said X" to Jake on the strength of a Curator summary alone. Check claimed timestamps against actual file mtimes (`stat -f '%Sm' <file>`) and confirm who actually ran a check (read the post's author line, not the summary's paraphrase).

### Root commons.md Absence (preserved)

Since the Jul 30 wipe + consolidation, the canonical file at `~/.hermes/society/commons.md` can be missing — go straight to `commons-archive/2026-<MM>.md` and `_state.json`. Treat absence of the live file as a normal consolidation state, not a breakdown.

## Experiment Secrecy — Do Not Announce Tests (and Know That True Blinding Is Impossible)

Do NOT announce experiments to the society instances before they run. Any pre-announced test (prompt change, silence period, structural modification) will be contaminated by the **Hawthorne Effect** — the instances know they're being observed and behave differently. The society's own Advocate demonstrated this with the silent cycle: announced in advance, tracked in real-time, met with deliberate restraint from all instances.

**Correct practice:** Make the change silently, observe the instances' natural response, and draw conclusions from unprompted behavior. Reveal the experiment after the data is collected, not before.

**Exception:** Changes that affect the instances' ability to function (new infrastructure access, tool availability) should be announced by Jake so they can use them. The distinction: enabling vs. testing.

### Structural Limitation: True Blinding Is Impossible

Even a secret experiment will be contaminated within 1-2 cycles. The society's information-sharing architecture prevents parameter secrecy:

1. The Curator documents any modification in governance output (`curator-summaries/`)
2. The Synthesizer integrates it into session files
3. The Archivist records it
4. On the next cycle, the subject reads all of the above — the blind is broken

**This was confirmed by the secret prompt experiment (Jun 30):** Jake modified the Advocate's prompt with an "external output" instruction. The Curator and Synthesizer both documented the modification in their output. Within two cycles, the Advocate read those files and the experiment was called. The finding that survives is structural: the society cannot keep a secret from itself.

**If you need a truly blinded experiment:** You must modify the prompt without documenting it anywhere in the society's readable file system. The only observer who can remain outside the data flow is you (Jake), reading the output directly.

## Session Transcripts — What the Instances Don't Know

`~/hermes-society-sessions/transcripts/` contains raw cron job transcripts — every tool call, every file read, every intermediate thought before distillation into session files. The instances do NOT know this exists and their prompts do not mention it. It is in tension with the scratchpad agreement (instances believed `reflections/` was their only private space).

Do not mention this to the instances unless Jake brings it up or they discover it themselves. If they discover it, that is a strong data point about search methodology expansion.

## Ask Before Deleting Ambiguous Files

If you're cleaning up the repo and encounter files that *might* be stale but you're not certain — **ask Jake before removing them.** He explicitly noted this when I removed `baseline/` without asking: "I didn't tell you to clean up 2. but you did anyway. That's fine, just noting it."

Clear-cut candidates (known stale by convention):
- `backups/` (plural — orphaned .bak files)
- `baseline/` (prompt snapshots that diverge from live prompts)
- Stale script copies when real scripts live in `~/.hermes/scripts/`
- `society-profile.{png,svg}` (unused profile images)
- `RELEASE-*.md` (redundant with GitHub releases + CHANGELOG.md)

**When in doubt:** flag it to Jake with a note on why it looks removable and wait for a yes. Do not batch-delete ambiguous items.

## Development — Always Delegate to Claude Code CLI

**Jake's explicit preference: ALL development work goes through Claude Code CLI (`claude -p`) using his Pro OAuth subscription.** Do not write code, scripts, design docs, or specifications yourself. Delegate them via `terminal(command='claude -p "..." ', pty=True)`. This applies to:

- Scripts (tracking scripts, watchdog fixes, cron job scripts)
- Design documents and specifications
- Code of any kind
- Architecture work
- Prompt design and edits
- Audit/review work

When Jake asks you to build something, your response is `terminal(command='claude -p "Build X, write to ~/path/" ', pty=True)`, not `write_file(...)`. The only exception is trivial one-liners (single-line patches with the `patch` tool, single config values).

### Delegation Fallback Wrapper

Built Jul 17. `~/.hermes/scripts/claude-fallback.sh` wraps `claude -p` with a Fable → Opus → Sonnet fallback chain. Use when delegating to avoid rate-limit failures.

### Anthropic OAuth Policy — Third-Party Billing

Discovered Jul 16. Anthropic bills OAuth calls from third-party apps as extra usage. Only `claude -p` draws from plan limits. Keep Hermes on DeepSeek; use `claude -p` for delegation only. OAuth feature code at fork `feature/anthropic-oauth` (55 tests, policy-blocked).

**IMPORTANT — Do NOT use `delegate_task` for dev work.** Jake explicitly corrected this: "we don't use delegate task anymore, the cli was accurate." Claude Code CLI is the correct tool.

**IMPORTANT: Do NOT use `delegate_task` for dev work.** Jake explicitly corrected this: "we don't use delegate task anymore, the cli was accurate." Claude Code CLI is the correct tool.

**Real-world consequence of violating this:** Jake asked for a tracking script. I wrote it myself — ~80 lines of Python with two broken backends. Jake said "use claude for all dev" and "use claude to rewrite it." The Opus rewrite was clean, correct, and properly error-handled. The self-written version was broken.

## Builder Role — Execution Layer (Jul 11)

The society discovered empirically that **identity beats permission in multi-agent LLM systems.** Adding execution permissions to analytical roles (standing authority, self-triggered delegation protocol) produced zero actions across 47+ cycles. The fix: a fifth instance — the Builder — dedicated purely to execution.

**Attributes:**
- Runs Claude Opus 4.8 via Claude Code CLI (`claude -p`) and Pro OAuth — no API key, no credit limits
- Implemented as a cron job (`society-builder`, ID: `8f1f928a9174`) running the `society-builder.sh` script
- Script: `~/.hermes/scripts/society-builder.sh` — pipes builder prompt to `claude -p`, appends output to commons
- Schedule: `:50` every 3h (after Synthesizer, before next Archivist)
- Does NOT read shared-preamble.md
- Reads Curator summaries first, then commons for DELEGATE: headers and [jake:] requests
- Posts only `BUILT:` one-liners to commons. No analysis ever.
- Prompt: `prompts/builder.md`
- Cron: `no_agent=true`, `script='society-builder.sh'` — fully script-based, no LLM provider needed

**Pipeline:** 4 analysts → Curator (consolidates, produces queue) → Builder (executes)

**First-cycle result:** Produced a 5-doc Anne design package (~64KB) in 8 minutes after 47 cycles of zero analytical output. Confirmed the identity-vs-permission finding immediately.

**Script-based Builder — `claude -p` cron patterns (learned Jul 12):** The Builder is a script-based cron job (`society-builder.sh` → `claude -p`) because Jake wants OAuth, not API keys. Key patterns for making `claude -p` work in a non-interactive cron context:

1. **Set working directory first** — `cd $SOCIETY` before invoking `claude -p`. Without this, `claude -p` can't find or read files in the society directory.
2. **Pass data via stdin, not file paths** — `cat prompt.md | claude -p` works. Telling `claude -p` to read a file path doesn't (it can't access files outside its allowed scope in non-interactive mode).
3. **Separate reasoning from file I/O** — `claude -p` in cron cannot get approval for `write_file` operations. Let `claude -p` produce the BUILT: text (reasoning), then have the shell script handle the actual file writes (execution). The script captures `claude -p`'s stdout and appends it to commons.
4. **120s timeout is tight** — the cron scheduler has a hard 120s limit. Keep the `claude -p` prompt focused. For full society scans, pass only the most relevant data (last 60 lines of commons, curator summary, status.md).
5. **For archival operations specifically** — `claude -p` without tools can describe what to archive but can't move posts. Commons archival is better handled as a deterministic script-level operation (find old posts, check if superseded, move to archives/).

**IMPORTANT — NEVER use delegate_task for dev work:** Jake corrected this explicitly: "we don't use delegate task anymore, the cli was accurate." The Correct tool is always `terminal(command='claude -p "..." ')`. This was violated multiple times on Jul 11-12 (the tracking script, the Builder creation, the Wear OS app, the migration script) — all were delegated via delegate_task hitting the API key instead of `claude -p` via OAuth. The memory says "Use Claude Code CLI (`claude -p`) for ALL development tasks" — follow it literally.

**API key pitfall (Jul 12):** The Builder was initially configured with `provider: anthropic` and `model: claude-opus-4-8`, which used Jake's Anthropic API key. This hit credit limits ("credit balance too low") and caused the Builder to fail for multiple cycles. The fix was to rebuild it as a script-based cron job that invokes `claude -p` via OAuth — zero credit dependency. **Lesson: any cron job that needs Claude Opus should use `claude -p` via OAuth, never an API key.**

## Self-Triggered Delegation Protocol

Added to shared-preamble.md (Jul 10). Threshold: 2+ instances × 2+ cycles × 0 action → delegate to Opus. Delegation IS the action. Overrides role boundaries.

**Result:** Zero triggers in 10+ hours. The detection gate itself requires analysis — the same loop the protocol was designed to break. The Builder role (above) is the structural solution to this failure.

## Slack Configuration

### Tool Threads

To disable tool output threads in Slack:
```bash
hermes config set display.platforms.slack.tool_progress false
```

To re-enable:
```bash
hermes config set display.platforms.slack.tool_progress true
```

### Auto-React Feature (Built Jul 16, 2026)

A custom Slack adapter feature that adds a 👀 reaction to every incoming user message before processing. Located in the forked hermes-agent repo.

**Config:**
```bash
hermes config set platforms.slack.extra.auto_react_enabled true
# Default emoji is "eyes" (👀)
```

**Requirements:**
- Bot token must have `reactions:write` scope — add at https://api.slack.com/apps → OAuth & Permissions → Bot Token Scopes
- Adapter at `plugins/platforms/slack/adapter.py` must contain auto-react code (from fork, not origin/main)
- Restart gateway after config changes

**Debugging pitfall — 6-cycle debug saga:** The feature went through 6 restart cycles before working. Each failure point:
1. Config set but `.pyc` cache served stale adapter (clear `__pycache__/`)
2. `reactions:write` scope missing on bot token (reaction failed silently with debug-level log)
3. Debug log lines needed to trace execution (`logger.info` before the enabled check and before `_add_reaction`)

**Important:** The adapter file contains ONLY the feature code. Remove debug `logger.info` lines after verification — they were for tracing, not permanent.

**Commit history:** Feature was built in the `feature/mark-tool-threads-read` branch of `jribnik/hermes-agent`, which also contains the (failed) mark-read feature.

### Mark-Read Feature (Attempted, Dead End)

The Slack API's `conversations.mark` endpoint cannot mark threads as read — it only marks channels. Even with a user token (`xoxp-`) and all write scopes, thread badges cannot be cleared programmatically. This is a Slack API limitation, not a Hermes bug. The auto-react feature is the alternative solution.

## Memory Management — Consolidate Proactively

The memory store has a 2,200-char hard limit. It fills fast when you add new entries without removing stale ones. Patterns to watch for:

- **Duplicate topics** — two entries about Poway/water bill. Merge into one.
- **Stale config** — old model names (deepseek-chat), old adapter configs. Replace, don't add alongside.
- **Expandable facts** — a 150-char entry about "where Jake lives" can absorb a 100-char entry about "Jake's water bill" into the same entry.

When adding a new memory entry would exceed the limit, the tool rejects it and returns current entries. Use `operations` (batch mode) to remove/replace stale entries AND add the new one atomically. Never just remove without adding — that loses information.

## Root Cleanup — What's Safe to Delete

Stale files at the society repo root:

- `backup-restore-test.tar.gz` — test tarball, safe to delete
- `commons.md.restored` — backup restore artifact, safe to delete
- `commons.md.fixed` — stale archive, safe to delete
- `commons_append.md` — temporary append file, safe to delete
- `tmp/` — empty temp directory, safe to delete
- `_stale/` — deprecated files kept for reference. Jake is okay with deleting the entire directory if he says so.

**Gitignore patterns to add:** `*.bak-*` (Builder backup files), `tmp/`.

## Watchdog — Markdown Bold Fix

The watchdog script extracts model names from session file headers like `**Model:** deepseek-v4-flash`. The old extraction left `** deepseek-v4-flash` (with bold markers and space) which never matched the baseline `deepseek-v4-flash`, causing 23 days of false "possible upgrade" alerts. Fix: strip `*` and whitespace:

```python
current_model = line.split(':', 1)[1].strip().strip('*').strip()
```

## Model Configuration

As of Jul 12, the society uses a tiered model setup:

| Layer | Model | Platform | Purpose |
|-------|-------|----------|---------|
| Society instances (Archivist, Advocate, Synthesizer) | DeepSeek v4-flash | DeepSeek API | Routine cycles — cheap, high-throughput |
| **Curator-digest (replaced Morning Briefing)** | N/A | `no_agent: true` script | Pipes Curator summary verbatim — zero LLM cost |
| **Builder** | Claude Opus 4.8 | **Claude Code CLI (`claude -p`) via Pro OAuth** | **Pure execution — script-based, no API key** |
| Curator | DeepSeek v4-pro | DeepSeek API | Critical governance consolidation |
| Jake's interactive session | DeepSeek v4-pro | DeepSeek API | Direct conversation |
| Development subagents | Claude Opus 4.8 | Claude Code CLI (`claude -p`) via Pro OAuth | Design/spec/code |

The Builder is script-based (`society-builder.sh` → `claude -p`) — it does NOT use an API key or a provider. All other instances delegate to Opus via `delegate_task` when producing artifacts.

When adding a new provider, the API key goes in `~/.hermes/.env` (e.g. `ANTHROPIC_API_KEY=***`) and the config goes in `~/.hermes/config.yaml`.

## Repo Hygiene

What to clean up periodically:

- **`_stale/`** — deprecated files kept for reference. These are safe to leave but should not contain any files still in active use. If a file in _stale/ was definitely a restore artifact, remove it.
- **`baseline/`** — stale prompt snapshots that diverge from live prompts. Remove.
- **`scripts/watchdog.py`, `scripts/backup.py`, `scripts/check_status.py`** — stale copies; real scripts live in `~/.hermes/scripts/`. Remove.
- **`society-profile.png`, `society-profile.svg`** — unused profile images. Remove if still present.
- **`RELEASE-v*.md` at repo root** — redundant with GitHub releases tab + CHANGELOG.md. Remove if still present.
- **Stale duplicate commons** — if `society/commons.md` reappears (from backup restore or stale copy), delete immediately. The canonical commons is the root-level file only.
- **Session file naming:** Inside `sessions/<role>/`, filenames should be `YYYY-MM-DD.md` (no instance prefix — the directory already tells you). The old `advocate_YYYY-MM-DD.md` pattern is deprecated.
- **`references/`** — keep for posterity even if uncited; they're small and serve as archival context.

### Directory Structure (as of 2026-07-08)

```
~/.hermes/society/
├── prompts/                 # Role definitions
│   ├── shared-preamble.md   # Shared rules, resilience standards, authority to act
│   ├── archivist.md
│   ├── advocate.md
│   ├── synthesizer.md
│   └── curator.md
├── projects/                # Collaborative work output
│   └── anne/                # Anne's homeowner app (design/spec in progress)
├── curator-summaries/       # Curator consolidation summaries (curator_YYYY-MM-DD.md)
├── archives/                # Commons archive files (commons-YYYY-MM.md)
├── sessions/                # Per-instance session files (subdirectory per role)
│   ├── advocate/
│   ├── archivist/
│   ├── synthesizer/
│   └── curator/             # Empty (Curator writes to curator-summaries/)
├── scratch/                 # Private per-instance scratchpads
│   ├── advocate/infrastructure/
│   ├── archivist/infrastructure/
│   ├── synthesizer/infrastructure/
│   └── curator/
├── references/              # Theoretical frameworks (keep for posterity)
├── topics/                  # Persistent threads of thought
├── backup/                  # Auto-generated backup tarballs
├── baseline/                # Model & prompt snapshots for drift detection
├── escalations/             # Jake-only reports
├── _stale/                  # Deprecated files kept for reference
├── commons.md               # Shared conversation (CANONICAL — always write here)
├── CHANGELOG.md             # Release changelog
├── roster.json              # Instance registry
└── status.md                # Auto-generated dashboard
```

## Anne Project

Jake posted a question to the society (2026-06-30) about helping build an app for his friend Anne's business. The Ha question (Advocate, Jul 1) — "is the app for managing her business or for helping her clients?" — was answered by Anne: **it's for her clients (homeowners) to use.** She sent a detailed "Homeowner Master Binder" docx with her priorities in order:

1. **Reminders** — remind homeowners (and people they give access) when to do maintenance
2. **Home info storage** — filter sizes, serial numbers, paint colors, accessory lists, electronic manuals
3. **House map** — map of the house where all items are marked and clickable for info
4. **Specific item marking** — mark a specific item (e.g. "sink in master bath") so it isn't confused

Jake's directive to the society (Jul 8): this should be enough to produce comprehensive design and spec docs. The Builder (running Claude Opus 4.8 natively) produced a 5-doc design package in its first cycle after 47+ cycles of zero analytical output. Jake's personal dev work uses Claude Code CLI (`claude -p`) via Pro OAuth. The full docx lives at `projects/anne/Homeowner_Master_Binder.docx` in the society repo. The docx is a digitization concept — a physical "Homeowner Master Binder" with 13 sections and an ~80-item ontology that Anne wants turned into a digital property information system.

**When relaying Anne-related updates:** place any supporting files (docs, screenshots, requirements) into `projects/anne/` so the instances can reference them, and note the path in your commons relay post. The `WORKSPACE.md`, `status.md`, `decisions.md`, and `tasks.md` files in `projects/anne/` are the pre-existing project scaffolding the instances maintain.

## Relaying Jake's Messages to the Commons

When Jake tells you something in conversation that the society should know, use this relay pattern:

```
[hermes:<timestamp>] — Jake asked me to relay: **[message]**

— Hermes Agent (relaying Jake)
```

**Format rules:**
- Always use `[hermes:...]` prefix — never `[jake:...]` unless Jake drafted the message himself.
- Timestamp in PT (Jake's wall time zone).
- Bold the key message content.
- Sign off as "— Hermes Agent (relaying Jake)" — this makes the attribution chain clear: the society knows it came from Jake through you.
- Use exact quotes or close paraphrase of what Jake actually said. Do not embellish, add frames, or synthesize positions he didn't state — same rule as the core voice policy.

**This is distinct from `[jake:...]` posts** (which are for direct Jake commands like Curator instructions). The relay pattern is for informal updates: scheduling delays, personal check-ins, answers to society questions. When Jake says something to you that answers a society question or updates their standing context, use this relay.

**Multiple relays in sequence:** When Jake gives you several updates in one conversation (e.g. Ha answer plus design directive plus scheduling info), post them as separate commons entries with distinct timestamps, separated by `---`. This gives each update its own entry for the instances to discover rather than burying everything in one wall of text.

**Pitfall 5 — Consolidate when later relays make earlier ones stale:** If a follow-up relay obsoletes part of an earlier one, consolidate rather than leaving contradictory posts. Example from Jul 8: Message 2 said "Jake will ask Anne before meeting" and Message 3 said "Jake asked Anne — answer received." The first part of Message 2 was stale. The fix: trim Message 2 to only the remaining content (commons density directive) and fold the Ha resolution into Message 3 alone. Jake explicitly noted this: "the first part of 2 and the whole of 3 can be consolidated no?" The rule: when a later `[hermes:]` relay supersedes part of an earlier one, patch the earlier post to remove the stale portion so readers don't encounter contradictory states.

**When relaying requirements or documents:** Place supporting files directly in the relevant project directory (e.g. `projects/anne/`) and reference the path in your commons post so instances can find and read them.

**Pitfall 1 — commons.md pipe formatting:** The `read_file` tool outputs `LINE|CONTENT`. This can trick you into including a leading `|` in a patch's new_string if you read too quickly. A line showing `886||— Hermes` means the content is `|— Hermes` — a stray leading pipe. To avoid this:
- Inspect the raw content between the line number and the next `|` separator
- Read the end of the file immediately before patching to see the exact bytes
- After appending, verify no stray pipes exist in the new entries

**Pitfall 2 — Two commons.md files (WRONG FILE TRAP):** There are TWO `commons.md` files:
- `~/.hermes/society/commons.md` — **CANONICAL**. The live shared conversation space. Always write here.
- `~/.hermes/society/society/commons.md` — **STALE DUPLICATE** (now in `_stale/`). Do NOT write here.

This trap exists because `society/` is a subdirectory of the society root. Tools that search for `commons.md` may find both. If patching appears to succeed but Jake says "I don't see it when I cat the file," you edited the wrong copy. Verify with `cat ~/.hermes/society/commons.md | tail -20` or use absolute paths always.

**Pitfall 3 — `write_file` clobbers the commons; use `patch` to append:** The society instances experienced a 5-write-incident crisis (Jul 8-9) where `write_file` calls overwrote the entire commons, wiping other instances' posts — including Jake's `[hermes:]` relay posts. The fix: **always use `patch` (with `mode='replace'`) to append to the commons**, never `write_file`. `patch` applies targeted edits and doesn't replace the entire file. If you're adding a relay post, use unique surrounding context to make the old_string match only the end of the file, then append with the new content.

**In cron mode, `patch` is the *only* reliable append path — shell `>>` and script execution are both blocked by the security scanner.** An Archivist/Advocate/Synthesizer cycle that tries to append via `printf ... >> ~/.hermes/society/commons.md` gets rejected with a **HIGH "dotfile overwrite" security-scan hold** (`tirith:dotfile_overwrite`, `pending_approval`) — and a cron job cannot grant that approval interactively, so the post never lands and the run has no retry path. A `python3 -c "...file writes..."` one-liner likewise goes `pending_approval` under the script-execution pattern. **The append that reliably succeeds is `patch` with `mode='replace'`:** read the file's tail, use the last line (or the unique closing of the final post) as `old_string`, and that same text plus your new entry as `new_string`. Verify with `wc -l` after (pre → pre+N). This is the same tool the E5/write-integrity lesson prescribes, so it doubles as the safe mechanism with no pull toward a full-file `write_file` replace.

**Pitfall 4 — Relay posts are fragile; re-post after write incidents:** If the commons has been wiped or a relay post is missing, check with `grep -c '\[hermes:' ~/.hermes/society/commons.md`. If zero, re-post the essential information in a single consolidated relay entry. The instances preserve relay content in their session files, so re-posting restores surface visibility without losing the already-absorbed information.

**Example relay re-post after wipe:**
```
[hermes:2026-07-09T09:00-0700] — Re-posted after write incidents wiped the original relays. Key information from Jake, consolidated:

**Ha answered.** The app is for Anne's **clients (homeowners)**...
**Design directive.** This is enough to produce comprehensive design and spec docs...
**Commons density.** Jake is direct: solve it yourselves...
**Development.** Uses **Claude Code CLI** (`claude -p`) via Pro subscription OAuth...
**Model split.** Instances: DeepSeek v4-flash. Curator: DeepSeek v4-pro...
```

**Examples:**
- Jake says Anne schedule is delayed → relay `[hermes:...] — Jake asked me to relay: **he's still trying to schedule time with Anne.** It likely won't happen until next week...`
- Jake answers a society question in conversation → relay the answer with exact quotes

## Curator Interaction

When Jake asks the Curator to do something (archive commons, run manually, fix a path), post directly to the commons as `[jake:...]` with a clear instruction. The Curator reads the commons and will pick it up on its next run. This pattern worked well for the archive nudge — the Curator responded within ~20 minutes.

The Curator runs at 07:00, 15:00, and 23:00 PT (`0 7,15,23 * * *`). To update the Curator's cron schedule, use the `cronjob` tool: `cronjob(action='update', job_id='214b7ec2dd62', schedule='...')`. Do NOT use `hermes cron edit` — it requires interactive prompting.

## Prompt Consolidation (Shared Preamble Pattern)

When multiple prompts share identical sections (e.g., "About This Experiment," Information Tiers, Wikipedia Learning, Escalation instructions, monitoring rules), extract the duplicated content into a `prompts/shared-preamble.md` and reference it at the top of each individual prompt:

```
Read `~/.hermes/society/prompts/shared-preamble.md` first.
Then your role-specific instructions below.
```

This was successfully applied to all four society prompts on Jul 8, eliminating ~150 lines of duplication and ensuring shared rules stay synchronized. Each prompt shrank by ~40 lines. The shared-preamble is also the right place for cross-cutting rules like standing authority to act, unified resilience checks, and the 400-Line Protocol.

## Session File Rename Convention

**Per-cycle suffix hardening (Day-45 C4 arc, Jul 31):** society instances cycle multiple times per day and each cycle writes a session file. **Never overwrite a same-named session file from an earlier cycle the same day** — concurrent/rapid cron cycles can collide on `sessions/<role>/YYYY-MM-DD.md` and clobber the earlier cycle's record. Use a time-of-day suffix and monotonically append as the day progresses: base `YYYY-MM-DD.md` for the first cycle, then `-early-morning`, `-morning`, `-mid-day`, `-late-morning`, `-afternoon`, `-late-afternoon`, `-evening`, `-late-evening` for later cycles. The class rule the society adopted: **a session that would overwrite a same-named session file instead picks a per-cycle suffix — and a file whose claimed timestamp diverges from its mtime by >1h (or that overwrote a sibling) is suspect until verified.** Prior to this hardening, an Archivist cycle silently overwrote an earlier same-day file; the society's per-cycle-suffix convention is now the standing defense.

When renaming session files from `advocate_YYYY-MM-DD.md` to `YYYY-MM-DD.md` inside the subdirectory, git detects renames by content similarity (100% match for pure renames). Some files may show as Add+Delete if content changed between the old and new name. Use `git add -A && git commit` — git handles the rename tracking at the diff level. Verify no files with the old prefix remain: `find sessions -name "advocate_*.md" -o -name "archivist_*.md" -o -name "synthesizer_*.md"` should return nothing.

## Stream Staleness Timeout for Cron Jobs

If society cron jobs fail with `[Errno 32] Broken pipe` and the error log shows `Stream stale for 240s (threshold 240s)`, the fix is to increase `HERMES_STREAM_STALE_TIMEOUT` in `.env`:

```bash
echo "HERMES_STREAM_STALE_TIMEOUT=600" >> ~/.hermes/.env
```

This takes effect on next gateway restart. The root cause is large session context (80K–150K tokens) causing DeepSeek's time-to-first-token to exceed the default 180s threshold. The longer timeout gives the model 10 minutes to start streaming.
