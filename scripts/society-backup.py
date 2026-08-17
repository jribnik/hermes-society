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

# The three migrated society agents live in their own profile homes (config,
# cron, scripts, SOUL, .env, state.db) — none of which is under society/. Back
# those up too (HERMES-8), capturing the truly-unrecoverable setup while
# skipping heavy/volatile caches that would bloat the tarball and rebuild on
# their own. Each is added under a profiles/<name>/ arcname.
PROFILES_DIR = Path.home() / '.hermes' / 'profiles'
SOCIETY_PROFILES = ['society-archivist', 'society-advocate', 'society-synthesizer']
# The society's maintenance scripts (this backup script, watchdog, commons
# archive, session export, tripwire) live in ~/.hermes/scripts/ and are NOT
# version-controlled or otherwise backed up — capture them too so the whole
# operational footprint is recoverable.
MAIN_SCRIPTS = Path.home() / '.hermes' / 'scripts'
# The skills library (~/.hermes/skills) is NOT version-controlled and, before
# this, was NOT in any external backup — the only copies were the curator's own
# nested snapshots under skills/.curator_backups/, which vanish if the skills
# dir/disk is lost. Capture it too (~13 MB sans the nested backups). This is
# where the society's operational knowledge + per-profile society-* skills live.
SKILLS_DIR = Path.home() / '.hermes' / 'skills'
# First-level entries under skills/ to exclude: the redundant nested tarballs
# (~14 MB) and pycache.
SKILLS_EXCLUDES = {'.curator_backups', '__pycache__'}
# Directory / file names to exclude from each profile home (regenerable or huge).
PROFILE_EXCLUDES = {
    'cache', 'audio_cache', 'image_cache', 'sandboxes', 'logs',
    'models_dev_cache.json', 'verification_evidence.db',
    'state.db-wal', 'state.db-shm', 'gateway.log',
    'gateway.pid', 'gateway.lock', 'auth.lock', 'gateway_state.json',
}

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

    # Create the tarball. Exclude only the backup/ dir itself (not files that
    # merely have "backup" in their name, e.g. backup-protocol.md / commons_backup.md).
    def _tar_filter(info):
        parts = info.name.split('/')  # names are "society/<entry>/..."
        return None if len(parts) >= 2 and parts[1] == BACKUP.name else info

    def _profile_filter(info):
        # names are "profiles/<profile>/<entry>/..." — drop any path whose
        # first-level entry under the profile is in the exclude set.
        parts = info.name.split('/')
        if len(parts) >= 3 and parts[2] in PROFILE_EXCLUDES:
            return None
        # Also drop the profile skills' redundant nested curator tarballs +
        # pycache anywhere in the tree (same reasoning as SKILLS_EXCLUDES).
        if '.curator_backups' in parts or '__pycache__' in parts:
            return None
        return info

    def _skills_filter(info):
        # names are "skills/<entry>/..." — drop nested curator backups + pycache.
        parts = info.name.split('/')
        if len(parts) >= 2 and parts[1] in SKILLS_EXCLUDES:
            return None
        if '__pycache__' in parts:
            return None
        return info

    with tarfile.open(out_path, "w:gz") as tar:
        tar.add(SOCIETY, arcname=SOCIETY.name, filter=_tar_filter)
        # Add each society profile home under profiles/<name>/.
        for prof in SOCIETY_PROFILES:
            phome = PROFILES_DIR / prof
            if phome.exists():
                tar.add(phome, arcname=f"profiles/{prof}", filter=_profile_filter)
        # Add the main-home maintenance scripts under scripts/.
        if MAIN_SCRIPTS.exists():
            tar.add(MAIN_SCRIPTS, arcname="scripts")
        # Add the skills library under skills/ (sans nested backups + pycache).
        if SKILLS_DIR.exists():
            tar.add(SKILLS_DIR, arcname="skills", filter=_skills_filter)

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
        "contents": (
            [str(p.relative_to(SOCIETY)) for p in sorted(SOCIETY.rglob("*")) if p.is_file() and BACKUP not in p.parents]
            + [f"profiles/{prof}" for prof in SOCIETY_PROFILES if (PROFILES_DIR / prof).exists()]
            + (["scripts"] if MAIN_SCRIPTS.exists() else [])
            + (["skills"] if SKILLS_DIR.exists() else [])
        )
    })
    # Keep only last 14 entries in manifest
    history = history[-14:]
    import json
    manifest.write_text(json.dumps(history, indent=2))
    print(f"[BACKUP] Manifest updated: {len(history)} entries")

if __name__ == "__main__":
    force = "--force" in sys.argv
    main(force)
