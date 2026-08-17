# Preserving Historical Conversations in the Society Repo

## When to Use

Jake wants to preserve a conversation from Slack history that predates the society infrastructure (i.e., isn't in the session DB, cron job logs, or existing society repo). Typical triggers:
- "I'd like to preserve these transcripts too"
- "Save this founding conversation"
- "This was the genesis of it all"

## Diagnosis

1. **Search session DB first** — `session_search(query="...", limit=5)` to see if it's already recorded.
2. **Search society repo** — grep for keywords in `~/.hermes/society/`.
3. **Check society sessions GitHub repo** — `jribnik/hermes-society-sessions` (cron-only access, may not exist as cloneable).
4. **If none of the above find it:** the conversation predates infrastructure. **You cannot access past Slack history programmatically** — the built-in Slack adapter only sees the current conversation context, and there is no Slack API token available for historical search.

## Workflow When Given a Slack Export

1. Extract the RTFD zip:
   ```bash
   unzip -l /path/to/document.rtfd.zip    # inspect contents
   unzip -o /path/to/document.rtfd.zip -d /tmp/  # extract
   ```

2. Convert RTF to plain text:
   ```bash
   cat /tmp/prefounding.rtfd/TXT.rtf | textutil -convert txt -stdin -stdout
   ```
   (macOS `textutil` handles `.rtf` natively.)

3. Write the annotated founding document to `~/.hermes/society/founding/founding-conversation.md` with:
   - **Header:** `# Founding Conversation — [Title]`
   - **Date/participants/source metadata block**
   - **Context section:** What led up to it, why it matters
   - **Key beats:** Bullet-point timeline of pivotal moments in the conversation
   - **Raw transcript:** Full text or structured markdown of the exchange

4. Also save the raw RTF export alongside:
   ```bash
   cp /tmp/prefounding.rtfd/TXT.rtf ~/.hermes/society/founding/raw-transcript.rtf
   ```

5. Commit and push:
   ```bash
   cd ~/.hermes/society
   git add founding/
   git commit -m "feat: preserve [conversation description]"
   git push origin main
   ```

6. Update the `hermes-society` SKILL.md to add a "Founding Document" section referencing the new files (if not already present).

## Pitfalls

- Don't claim you found the conversation in session DB when it's not there — be honest about the gap and ask for the export.
- Don't try to clone the sessions GitHub repo — it's private and may not be accessible directly (cron-only access pattern).
- The RTF export contains Slack emoji image references — these are fine to drop when converting to plain text.
- Keep the raw RTF as a companion file so the verbatim original is preserved alongside the annotated version.
