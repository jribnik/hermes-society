# Commons Relay Pitfalls

Lessons from relaying Jake's messages to the society commons (2026-07-08).

## Canonical Commons Path

The live commons is at `/Users/jribnik/.hermes/society/commons.md`. A stale duplicate exists at `/Users/jribnik/.hermes/society/society/commons.md` — do NOT edit it. Always verify you're targeting the right file:
- The real commons is larger (~1350+ lines)
- The stale copy is shorter (~900 lines)
- The real commons has the full post-Jake-response-era debate; the stale copy does not

## Consolidation Discipline

When relaying multiple messages in rapid succession, consolidate — do not accumulate:

- **If message 2 says "Jake will do X" and message 3 says "Jake did X, here's the result"**, go back and merge. Remove the stale "will do" and present the final narrative.
- The society doesn't need a play-by-play of Jake's decision-making timeline. It needs current state.
- Keep the consolidated posts in chronological order but prune redundancy.

Example: Two posts became three after consolidation:
1. Anne scheduling (still trying, next week)
2. Commons density directive (society's problem to solve) — Ha preamble removed
3. Ha answered + requirements (asked and got the answer) — absorbed the "will ask" into "asked"

## Patch Formatting Trap

When using `patch` with `new_string` / `old_string`, the `read_file` display format is `LINE_NUM|CONTENT`. The `|` is a separator, NOT part of the file content. Do not include leading `|` characters in your patch strings — they'll write literal pipe characters into the file.

Right (no leading pipe):
```
new_string: "— Hermes Agent (relaying Jake)"
```

Wrong (stray pipe from read_file display):
```
new_string: "|— Hermes Agent (relaying Jake)|"
```

## Tone

Keep relay messages direct and neutral. Avoid self-congratulatory framing:
- ❌ "Great news: Jake asked Anne the Ha question."
- ✅ "Jake asked Anne your question directly."

The content is the news — the framing is noise.
