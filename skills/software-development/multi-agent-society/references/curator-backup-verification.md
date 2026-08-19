# Curator Backup Verification — Manifest vs Directory Pitfall

## The Pitfall

The Curator's backup freshness check can silently fail if it relies on `backup-manifest.json` instead of checking the actual backup directory.

### How It Happens

`backup-manifest.json` is maintained by the backup script. If the backup script runs but doesn't update the manifest (e.g., because the manifest update step is a separate process, or the script was modified, or the manifest format changed), the manifest becomes stale while actual backup tarballs continue to be created.

### Detection

```bash
# WRONG — checks only the manifest
ls -la ~/.hermes/society/backup/backup-manifest.json

# RIGHT — checks actual backup files
ls -la ~/.hermes/society/backup/*.tar.gz
```

The manifest may list backups only through a certain date while the directory contains newer tarballs. The Curator should use **actual file timestamps** from the backup directory, not the manifest's self-reported data.

## Historical Example (2026-07-06)

Curator runs #16 and #17 both flagged a "28h backup failure" — no backup since Jul 1. Run #18 (on v4-pro) checked the actual directory and found tarballs for Jul 2, 3, 4, 5, and 6. The backup script had been running daily throughout Jake's 4-day absence. The manifest simply hadn't been updated.

**Impact:** Two consecutive governance summaries reported infrastructure failure that didn't exist. The society's resilience was misdiagnosed as 1/6 (run #16) and 4/6 (run #17) when the actual backup resilience was healthy throughout.

## Prevention

In the Curator's resilience monitoring (Responsibility 3), the backup freshness check should:

1. **List the backup directory** with `ls -la` to see actual tarball timestamps
2. **Find the newest tarball** by modification time
3. **Compare its timestamp** to the current wall clock (<24h = pass)
4. **Only then** cross-reference with `backup-manifest.json` for metadata

## Model-Advantage Note

This pitfall is more likely to affect lower-capability models. A v4-flash Curator may check the manifest's `created` field and report "28h old" without verifying against the actual directory. A v4-pro Curator is more likely to notice the indirection and check the directory directly. The fix is procedural: **always verify backup freshness from the filesystem, not from a metadata file.**
