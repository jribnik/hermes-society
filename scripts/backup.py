#!/usr/bin/env python3
"""
Backup the Hermes Society directory to ~/.hermes/society/backup/.

Creates timestamped tarballs of the full society directory.
Keeps the last 14 backups and rotates older ones.
Runs as a no_agent cron or standalone.

Usage:
  python3 backup.py                  # normal run
  python3 backup.py --force          # force even if backup exists for today
"""
import os, sys, shutil, tarfile, glob
from pathlib import Path
from datetime import datetime

SOCIETY = Path.home() / '.hermes' / 'society'
BACKUP  = SOCIETY / 'backup'

def main(force=False):
    BACKUP.mkdir(parents=True, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    arcname = f"society-backup-{date_str}.tar.gz"
    out_path = BACKUP / arcname

    # Skip if a backup already exists for today and not forced
    if not force:
        today_prefix = f"society-backup-{datetime.now().strftime('%Y-%m-%d')}"
        existing = sorted(BACKUP.glob(f"{today_prefix}*"))
        if existing:
            print(f"[BACKUP] Backup already exists for today: {existing[-1].name}")
            print(f"[BACKUP] Use --force to overwrite.")
            sys.exit(0)

    # Create the tarball
    with tarfile.open(out_path, "w:gz") as tar:
        tar.add(SOCIETY, arcname=SOCIETY.name,
                filter=lambda x: None if BACKUP.name in x.name else x)

    size_mb = out_path.stat().st_size / 1_048_576
    print(f"[BACKUP] Created: {arcname} ({size_mb:.1f} MB)")

    # Rotate old backups — keep last 14
    all_backups = sorted(BACKUP.glob("society-backup-*.tar.gz"))
    while len(all_backups) > 14:
        stale = all_backups.pop(0)
        stale.unlink()
        print(f"[BACKUP] Rotated (deleted): {stale.name}")

    # Write a manifest entry
    manifest = BACKUP / "backup-manifest.json"
    history = []
    if manifest.exists():
        import json
        history = json.loads(manifest.read_text())
    history.append({
        "file": arcname,
        "created": datetime.now().isoformat(),
        "size_mb": round(size_mb, 1),
        "contents": [str(p.relative_to(SOCIETY)) for p in sorted(SOCIETY.rglob("*")) if p.is_file() and BACKUP.name not in str(p)]
    })
    # Keep only last 14 entries in manifest
    history = history[-14:]
    import json
    manifest.write_text(json.dumps(history, indent=2))
    print(f"[BACKUP] Manifest updated: {len(history)} entries")

if __name__ == "__main__":
    force = "--force" in sys.argv
    main(force)
