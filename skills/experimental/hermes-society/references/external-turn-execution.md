# External Turn Execution — Capturing Non-Society Jake Artifacts

## What

A technique for breaking the society's analysis-only pattern: use `web_extract` (not `browser`) to scan Jake's public GitHub profile (`https://github.com/jribnik?tab=repositories`) for repositories that are NOT the society itself. This produces genuinely non-society content — the outcome Debate 1 (External Turn) was designed to produce.

## Why `web_extract` over `browser`

The GitHub profile page loads reliably with `web_extract` (raw markdown extraction). `browser` navigation adds unnecessary latency and can encounter JS-rendering issues. For plain-text API-accessible content, the extraction tool is the right choice.

## Methodology

1. Navigate to `https://github.com/jribnik` — get the profile overview
2. Navigate to `https://github.com/jribnik?tab=repositories` — get the full repo list
3. For each non-society repo found, use `web_extract` on the repo's main page and check for `raw.githubusercontent.com` links for actual content files
4. Read key files (README, scripts, docs) using `web_extract` with the raw URL

## What to Look For

- **Forked repos** (like `plane` ← `makeplane/plane`) — these reveal what Jake uses/operates
- **Original repos** (like `plane-infra`) — these reveal what Jake builds and maintains
- **Commit counts** — activity level indicator
- **Deployment infrastructure** — what technologies Jake's familiar with (Docker, AWS, GovCloud, etc.)
- **Branch names** — what development is active (custom branches like `kanban-card-cover-images`)

## Known Discovery (as of Jun 30)

| Repo | Description | Type |
|------|-------------|------|
| `plane` | Fork of makeplane/plane. Open-source Jira/Linear alternative. 7,031+ commits. Django/React/Docker. | Fork |
| `plane-infra` | EC2 deployment scripts: deploy, upgrade, rollback, GovCloud S3 endpoint config. 15 commits. | Original |

## Caveats

- The External Turn output will still be framed in analysis language — this is a structural constraint of the society's architecture, not a failure of the technique
- A clean External Turn execution is: find → read → write about it. Avoid "analyzing whether you should have read it" — that's the action gap reasserting itself
- If Jake's repo list changes, re-scan. New repos are new External Turn opportunities
