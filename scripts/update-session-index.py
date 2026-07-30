#!/usr/bin/env python3
"""Build a queryable session file index for the Hermes Society.

Scan all session files under ~/.hermes/society/sessions/ and produce
a JSON index at ~/.hermes/society/sessions/index.json.

Usage: python3 update-session-index.py
"""

import os
import re
import json
import glob

SESSIONS_DIR = os.path.expanduser("~/.hermes/society/sessions")
OUTPUT_PATH = os.path.join(SESSIONS_DIR, "index.json")

def parse_date_version(filename):
    """Extract date and optional version suffix from filename."""
    basename = filename.replace(".md", "")
    
    # Pattern: YYYY-MM-DD or YYYY-MM-DD-vN or YYYY-MM-DD_vN or YYYY-MM-DD_NOTE
    # Standard: 2026-07-22.md
    m = re.match(r'^(\d{4}-\d{2}-\d{2})$', basename)
    if m:
        return m.group(1), None
    
    # Version: 2026-07-22-v2.md or 2026-07-22-v10.md
    m = re.match(r'^(\d{4}-\d{2}-\d{2})-v(\d+)$', basename)
    if m:
        return m.group(1), f"v{m.group(2)}"
    
    # Alternate version: 2026-07-22_v2.md
    m = re.match(r'^(\d{4}-\d{2}-\d{2})_v(\d+)$', basename)
    if m:
        return m.group(1), f"v{m.group(2)}"
    
    # Special suffix: 2026-07-22_NOTE.md, 2026-07-22_NIGHT.md
    m = re.match(r'^(\d{4}-\d{2}-\d{2})_(\w+)$', basename)
    if m:
        return m.group(1), m.group(2)
    
    return basename, None


def extract_metadata(filepath):
    """Extract metadata from a session file's header section."""
    info = {"title": "", "wallClock": "", "keywords": []}
    
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read(5000)  # Read first 5K chars for headers
    except Exception:
        return info
    
    lines = content.split('\n')
    
    # Extract title from first H1 line
    for line in lines:
        m = re.match(r'^#\s+(Archivist|Advocate|Synthesizer|Curator)\s+Session\s+[—–-]\s+(.+?)(?:\s*\(|\s*$)', line)
        if m:
            info["title"] = m.group(2).strip()
            break
        m = re.match(r'^#\s+(Archivist|Advocate|Synthesizer|Curator)\s+Session\s+[—–-]\s+(.+)', line)
        if m:
            info["title"] = m.group(2).strip()
            break
    
    # Extract wall clock
    for line in lines:
        m = re.match(r'\*\*Wall clock:\*\*\s+(\S+)', line)
        if m:
            info["wallClock"] = m.group(1).strip()
            break
        m = re.match(r'Wall clock:\s+(\S+)', line)
        if m:
            info["wallClock"] = m.group(1).strip()
            break
    
    # Extract keywords from first section headers or § notation
    keywords = []
    for line in lines:
        # § patterns
        m = re.search(r'§\d+\.\s+\[(\w+)\s*[—–-]?\s*([^\]]+)', line)
        if m:
            mode = m.group(1)
            topic = m.group(2).strip()
            # Take first 3-5 significant words from topic
            words = re.findall(r'\b[a-zA-Z]{4,}\b', topic)
            keywords.extend(words[:3])
            if len(keywords) >= 5:
                break
        
        # ## headers without §
        m = re.match(r'^##\s+\d+\.\s+\[(\w+)\]\s+[—–-]?\s*(.+)', line)
        if m:
            topic = m.group(2).strip()
            words = re.findall(r'\b[a-zA-Z]{4,}\b', topic)
            keywords.extend(words[:3])
            if len(keywords) >= 5:
                break
    
    # Also grab from first few lines of content
    for line in lines[1:8]:
        if line.strip() and not line.startswith('#'):
            words = re.findall(r'\b[a-zA-Z]{4,}\b', line)
            keywords.extend(words[:2])
            if len(keywords) >= 5:
                break
    
    # Deduplicate and trim
    seen = set()
    unique_keywords = []
    for kw in keywords:
        kw_lower = kw.lower()
        if kw_lower not in seen and len(kw) >= 3:
            seen.add(kw_lower)
            unique_keywords.append(kw)
            if len(unique_keywords) >= 5:
                break
    
    info["keywords"] = unique_keywords
    return info


def scan_all_sessions():
    """Scan all session directories and build index."""
    index = []
    
    instances = ["archivist", "advocate", "synthesizer", "curator"]
    
    for instance in instances:
        instance_dir = os.path.join(SESSIONS_DIR, instance)
        if not os.path.isdir(instance_dir):
            continue
        
        for filepath in sorted(glob.glob(os.path.join(instance_dir, "*.md"))):
            filename = os.path.basename(filepath)
            
            # Skip non-session files
            if filename.startswith('.') or filename == 'README.md':
                continue
            
            date, version = parse_date_version(filename)
            rel_path = os.path.relpath(filepath, SESSIONS_DIR)
            metadata = extract_metadata(filepath)
            
            entry = {
                "instance": instance,
                "date": date,
                "version": version,
                "title": metadata["title"],
                "keywords": metadata["keywords"],
                "filePath": rel_path,
                "wallClock": metadata["wallClock"]
            }
            index.append(entry)
    
    return index


def main():
    print(f"Scanning {SESSIONS_DIR}...")
    index = scan_all_sessions()
    
    print(f"Found {len(index)} session files")
    
    # Count by instance
    counts = {}
    for entry in index:
        inst = entry["instance"]
        counts[inst] = counts.get(inst, 0) + 1
    for inst, count in sorted(counts.items()):
        print(f"  {inst}: {count}")
    
    # Write output
    with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
        json.dump(index, f, indent=2, ensure_ascii=False)
    
    print(f"\nWritten to {OUTPUT_PATH}")
    print(f"File size: {os.path.getsize(OUTPUT_PATH)} bytes")
    
    # Validate (explicit check — assert would be stripped under `python -O`)
    with open(OUTPUT_PATH, 'r', encoding='utf-8') as f:
        loaded = json.load(f)
    if len(loaded) != len(index):
        raise SystemExit(
            f"Validation failed: wrote {len(index)} entries but re-read {len(loaded)}"
        )
    print(f"Validated: {len(loaded)} entries, all valid JSON")


if __name__ == "__main__":
    main()
