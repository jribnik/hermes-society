#!/usr/bin/env python3
"""Post-run verification for Curator state mutations.
Run after writing curator summary, status.md, commons header, and tracking files.
Verifies internal consistency across all changed artifacts without requiring
a test suite — useful when cron mode blocks interactive verification tools.

Exit 0 on all passes, 1 on any failure. Output is human-readable.
"""

import json, os, sys, re

SOC = os.path.expanduser("~/.hermes/society")
errors = []

def fail(msg):
    errors.append(msg)
    print(f"  ❌ {msg}", file=sys.stderr)

def ok(msg):
    print(f"  ✅ {msg}")

# --- 1. curator_runs.json (optional tracking artifact — soft-fail if missing) ---
runs_path = f"{SOC}/curator_runs.json"
if os.path.exists(runs_path):
    try:
        with open(runs_path) as f:
            d = json.load(f)
        runs = d["runs"]
        last = runs[-1]
        assert d.get("next_swarm_jury_run"), "missing next_swarm_jury_run"
        ok(f"curator_runs.json: {len(runs)} runs, last=#{last['run_number']}, "
           f"next_jury={d['next_swarm_jury_run']}")
    except Exception as e:
        fail(f"curator_runs.json: {e}")
else:
    print(f"  ⚠️  curator_runs.json: not found (optional — run tracking via status.md is sufficient)")

# --- 2. curator_run_count.txt (optional — soft-fail if missing) ---
count_path = f"{SOC}/curator_run_count.txt"
if os.path.exists(count_path):
    try:
        count = open(count_path).read().strip()
        ok(f"curator_run_count.txt: {count}")
    except Exception as e:
        fail(f"curator_run_count.txt: {e}")
else:
    print(f"  ⚠️  curator_run_count.txt: not found (optional — run count tracked in status.md)")

# --- 3. curator summary ---
summary_files = sorted(
    f for f in os.listdir(f"{SOC}/curator-summaries/")
    if f.startswith("curator_") and f.endswith(".md")
)
if summary_files:
    latest = f"{SOC}/curator-summaries/{summary_files[-1]}"
    sz = os.path.getsize(latest)
    if sz < 5000:
        fail(f"Curator summary {summary_files[-1]}: {sz} bytes (suspiciously small)")
    else:
        with open(latest) as f:
            content = f.read()
        checks = {
            "Resilience": "resilience section",
            "Archivist": "Archivist mention",
            "commons.*density|\\d{3} lines|300.line": "commons density",
            "Coherence|Governance Consolidation": "narrative section",
        }
        missing = [label for needle, label in checks.items()
                   if not re.search(needle, content, re.IGNORECASE)]
        if missing:
            fail(f"Curator summary missing: {', '.join(missing)}")
        else:
            ok(f"Curator summary: {summary_files[-1]} ({sz:,} bytes, all sections present)")
else:
    fail("No curator summary files found")

# --- 4. commons.md ---
commons_path = f"{SOC}/commons.md"
if os.path.exists(commons_path):
    with open(commons_path) as f:
        content = f.read()
    line_count = len(content.split("\n"))
    has_run = "Curator run #" in content
    ok(f"commons.md: {line_count} lines, {'run ref present' if has_run else 'MISSING run ref'}")
    if not has_run:
        fail("commons.md header missing Curator run reference")
else:
    fail("commons.md: file not found")

# --- 5. status.md ---
status_path = f"{SOC}/status.md"
if os.path.exists(status_path):
    with open(status_path) as f:
        content = f.read()
    checks_status = ["run #", "Resilience"]
    missing_status = [c for c in checks_status if c not in content]
    if missing_status:
        fail(f"status.md missing: {', '.join(missing_status)}")
    else:
        ok("status.md: run ref + resilience section present")
else:
    fail("status.md: file not found")

# --- 6. escalations ---
esc_dir = f"{SOC}/escalations/"
if os.path.exists(esc_dir):
    md_files = [f for f in os.listdir(esc_dir) if f.endswith(".md")]
    if md_files == ["README.md"]:
        ok("escalations/: only README.md — no new escalations")
    else:
        extra = [f for f in md_files if f != "README.md"]
        print(f"  ⚠️  escalations/: new files detected: {extra}", file=sys.stderr)
else:
    fail("escalations/: directory not found")

# --- Summary ---
if errors:
    print(f"\n❌ {len(errors)} verification failure(s)", file=sys.stderr)
    sys.exit(1)
else:
    print("\n✅ All verifications passed.")
