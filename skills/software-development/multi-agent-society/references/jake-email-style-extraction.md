# Jake Email Style Extraction — Technical Notes

## Pipeline Architecture

The extraction pipeline consists of:

1. **MBOX parsing** — `mailbox.mbox()` reads Google Takeout's Sent-001.mbox format
2. **Sender filtering** — `--from-addr jribnik@gmail.com` to exclude other people's replies in threads
3. **Body extraction** — prefers `text/plain`, falls back to `text/html` with conversion
4. **Quote stripping** — regex removes `On ... wrote:` blocks, `>` prefixes, `--` signatures, forwarded message markers
5. **Corpus output** — JSON with raw + cleaned text per message
6. **Style analysis** — word frequency, sentence length, tone markers, representative excerpts

## Gmail API Path

The script also supports live Gmail API access via `google_api.py` for sampling recent sent mail. This requires OAuth setup (see `google-workspace` skill). The API path is limited to recent mail; the MBOX path is for full archive processing.

## Key Numbers from Jul 16, 2026 Run

- **MBOX size**: 8.4GB
- **Total messages**: 39,051
- **Jake's messages**: 12,017 (after sender filtering)
- **Usable text**: ~34.4 million characters
- **Average sentence**: 6.6 words
- **Average message**: 40.4 words

## Known Limitations

- Google Takeout exports may include full threads, not just sent mail — filtering by `From:` header is essential
- Nested multipart MIME can produce empty bodies (the cleaner only walks top-level parts)
- Gmail's automated messages ("This message was automatically generated") are noise — filter by minimum body length
- Keybase saltpack encrypted blocks appear in the corpus — these are not readable text but are authentic Jake content

## Repo

`~/src/jake-model/` — contains `extract_style.py`, corpus JSON, style report
