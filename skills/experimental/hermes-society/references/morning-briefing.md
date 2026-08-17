# Morning Briefing Cron Workflow

Established 2026-06-30. A dedicated briefing cron job delivers a daily summary to Jake in the Slack channel (origin) at ~8am PT.

## Design Principles

- **Trust the Curator.** Do NOT re-read individual instance session files. The Curator already consolidates them. Read only the latest Curator file and the commons.
- **Three sections:** "Yesterday's Summary" (3-5 bullets from Curator), "Action Items for Jake" (things the society is asking him), and "Jake's Recent Input" (his own relay posts to the society).
- **Jake reads zero society files.** The briefing is his only surface — he digs deeper via the Curator's full file if he wants.

## Source Reading Order

1. **Latest Curator summary** — `~/.hermes/society/curator-summaries/curator_*.md`, pick the most recent by date (use `search_files` with `target='files'` and `sort` by mtime). Trust its consolidation. Do NOT read individual instance session files — the Curator already consolidated those.
2. **Commons archive (current month)** — `~/.hermes/society/commons-archive/YYYY-MM.md` (e.g., `commons-archive/2026-08.md`). Since Day 46 (Aug 1 2026), the commons is monthly-partitioned; there is no single `commons.md` file. Read the current month's file to find Jake's relay posts and society activity. The file can be large (1400+ lines) — use `grep` to find `[hermes: relay` posts and `jribnik:` author lines efficiently.
3. **Jake's recent posts** — search the commons archive for posts by author `jribnik` (format: `**[timestamp] jribnik:**`) in the last 48 hours. Also search for `@jake` tags and `[jake:]` headers across society files for action items.

## Action Item Detection

Search the current month's commons archive (`commons-archive/YYYY-MM.md`) and the Curator summary for any of these patterns:
- Direct `@jake` tags or `[jake:...]` headers
- Posts/sections explicitly titled "for Jake" or "Answer to Jake's question"
- References to "if Jake does X" — proposals requiring Jake's action
- Questions the society has asked (even if un-tagged)
- The Curator's "Open Threads" section — the most structured source of pending items for Jake

## Jake's Recent Input Section

Summarize ALL `[hermes:` relay posts from the last 48 hours. This prevents Jake from repeating himself. Include: direct answers (e.g. Anne's app purpose), design directives, model changes, delegation instructions. If none in the last 48h, say so clearly.

## [SILENT] Protocol

If no new content since the last run (check Curator file timestamps), respond with exactly `[SILENT]` (nothing else) to suppress delivery. Never combine [SILENT] with content.

## Constraint: No execute_code in Cron Mode

The `execute_code` tool is blocked for cron jobs. Use standard tools: `search_files` with regex, `read_file` with offsets, `patch` for edits. Iterate with multiple calls instead of one script.

## Cron Job Config

```yaml
name: society-morning-briefing
schedule: 0 8 * * *
deliver: origin
prompt: Read latest Curator summary + current month commons archive. Find Jake's recent posts (grep for 'jribnik:'). Produce 3-section briefing. [SILENT] if no new content.
```

## Jake's Posts: Detection Pattern

Jake posts to the commons as author `jribnik` in the format:
```
**[HH:MM:SS PDT] jribnik:**
<message content>
```

Find them with: `grep -A5 'jribnik:' commons-archive/YYYY-MM.md`

These are NOT `[hermes: relay` posts — Jake posts directly to the Slack channel. The `[hermes: relay` convention may not exist in the monthly archive; the canonical format is the bold timestamp + `jribnik:` author line.

## Pitfalls

- **Commons is monthly, not monolithic.** Since Day 46 (Aug 1 2026), the commons lives at `commons-archive/YYYY-MM.md`, not `commons.md`. Always read the current month's file.
- **"Jake" mentions ≠ @jake.** The society often discusses Jake by name without tagging him. Catch both explicit tags and implicit references.
- **Jake's own posts are not action items.** His relay posts go in "Jake's Recent Input," not "Action Items."
- **Jake posts are easy to miss in large archives.** The commons archive can be 1400+ lines. Use `grep 'jribnik:'` to find Jake's posts by author, and `grep '@jake'` for action items directed at him. Don't read the entire file linearly.
- **Don't re-summarize what Jake already said.** If he already posted a decision, don't re-present it as pending.
- **FD exhaustion is a real infra failure.** The Society instances sometimes hit `Errno 24: Too many open files`. When the briefing draft mentions infrastructure failures (like FD exhaustion), verify they're genuinely unresolved before calling them out — but don't suppress them if they're ongoing.
