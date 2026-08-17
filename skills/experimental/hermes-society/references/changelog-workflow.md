# Changelog Workflow

Added 2026-06-28. The CHANGELOG is the canonical record of what changed in the
Hermes Society, when, and why. It lives at the repo root and follows [Keep a
Changelog](https://keepachangelog.com/en/1.1.0/) format.

## File Location

`/Users/jribnik/hermes-society/CHANGELOG.md` (also at
`github.com/jribnik/hermes-society/CHANGELOG.md`)

## Structure

```
# Changelog

## [Unreleased]

### Session export (YYYY-MM-DD)
- **N transcripts** committed (source=count, source=count)
- Sources: N Slack, N cron sessions in this batch

### Added
- New features go here

### Changed
- Changes to existing functionality

### Fixed
- Bug fixes

## [0.1.0] — YYYY-MM-DD
...
[0.1.0]: https://github.com/.../releases/tag/v0.1.0
```

## Auto-Updates (Nightly)

The `society-export-sessions.py` script's `update_changelog()` function appends
a dated entry under `## [Unreleased]` on every run. It detects duplicates by
checking for the `### Session export (YYYY-MM-DD)` header — if an entry for
today already exists, it's skipped (no pile-up on re-runs).

The entry records:
- Transcript count for this batch
- Source breakdown (Slack=, cron=, tui=, unknown=)
- Slack vs cron file counts (sampled from file paths)

## Cutting a Release

When enough unreleased changes have accumulated:

1. **Edit CHANGELOG.md**: move the `[Unreleased]` content under a new version
   header:
   ```markdown
   ## [0.2.0] — YYYY-MM-DD

   _Unreleased content moved here._  
   ```

2. **Add the compare link** at the bottom:
   ```markdown
   [0.2.0]: https://github.com/jribnik/hermes-society/compare/v0.1.0...v0.2.0
   ```

3. **Add a Git tag** and push:
   ```bash
   git tag -a v0.2.0 -m "Release v0.2.0"
   git push origin v0.2.0
   ```

4. **Create a GitHub Release from the tag** (optional but recommended for human-readable
   release notes with formatted markdown).

### Enterprise GH Limitation

The `gh` CLI on this machine is authed to **github.zeromark.internal** (enterprise),
not public GitHub. This means:

- `git push` via **SSH** (`git@github.com:jribnik/hermes-society.git`) works perfectly
  for code pushes and tag pushes
- `gh release create` and `gh api` will **not work** for the public repo — they'll
  401 because the enterprise token doesn't authorize public GitHub
- **Creating a GitHub Release** requires either:
  - **(a)** Visiting the browser URL:
    `https://github.com/jribnik/hermes-society/releases/new?tag=v0.2.0`
    and pasting the changelog entry
  - **(b)** Using a GitHub Personal Access Token with `repo` scope via `curl` or
    `urllib` to `api.github.com/repos/jribnik/hermes-society/releases`
  - **(c)** Having the user create it from the tag

The workaround used for v0.1.0: commit a `RELEASE-v0.1.0.md` file to the repo
root containing the full release body so it's ready to paste. Then the user can
one-click create the release from GitHub where they're already authenticated.

## v0.1.0 Contents

The initial release captured:
- Four instance prompts (Archivist, Advocate, Synthesizer, Curator)
- Six-failure-mode resilience infrastructure
- 16 reference documents
- Topics (external-turn, action-gap, stigmergy-prediction, swarm-jury)
- Daily session transcript export pipeline
- Key empirical discoveries (DIT, Gateway Revelation, Zeno, Three-Timescale)
- Full commons + archive + status

## Pitfall: Don't Forget the Compare Link

The Keep a Changelog spec requires a version compare link at the bottom. It's
easy to forget when cutting a release. The link is what makes git history
navigable from the changelog.
