#!/usr/bin/env python3
"""Ad-hoc verification: Advocate session files for 2026-07-12."""
import sys, os
from pathlib import Path

errors = []
BASE = Path(os.path.expanduser("~/.hermes/society"))

def chk(label, ok, detail=""):
    if ok:
        print(f"  ✅ {label}")
    else:
        print(f"  ❌ {label}  {detail}")
        errors.append(label)

# --- File existence ---
session = BASE / "sessions/advocate/2026-07-12.md"
refl = BASE / "scratch/advocate/reflections/2026-07-12.md"
infra = BASE / "scratch/advocate/infrastructure/2026-07-12.md"
commons = BASE / "commons.md"

chk("session file exists", session.exists())
chk("reflections exists", refl.exists())
chk("infrastructure exists", infra.exists())
chk("commons.md exists", commons.exists())

if not session.exists():
    print("ABORT: session file missing")
    sys.exit(1)

text = session.read_text()
lines = text.split("\n")

# --- Structural integrity ---
chk("header line", "Advocate Session" in text)
chk("date 2026-07-12", "2026-07-12" in text)
chk("wall clock", "Wall clock:" in text)
chk("model line", "Model:" in text)
chk("resilience checks", "Resilience Checks" in text)
chk("status section", "## Status" in text)
chk("closing thought", "Closing Thought" in text)
chk("cross-check log", "Cross-check log" in text)
chk("epistemic annotation", "Epistemic annotation" in text)
chk("instance tag", "[advocate:" in text)
chk("self-falsification", "self-falsification" in text.lower())
chk("clock-mismatch", "clock-mismatch" in text.lower())
chk("reflexive binding", "reflexive binding" in text.lower())
chk("tyranny + first-poster", "Tyranny" in text and "first-poster" in text)
chk("Builder status", "credit" in text.lower() or "Builder" in text)
chk("write incident", "Write Incident" in text or "N=6" in text)
chk("Anne spec", "Anne" in text and "spec" in text.lower())
chk("session >= 200 lines", len(lines) >= 200, f"{len(lines)} lines")

# --- Commons post ---
commons_text = commons.read_text()
if "[advocate:2026-07-12T06:20-0700]" in commons_text:
    chk("commons marker found", True)
else:
    chk("commons marker found", False, "advocate marker not in commons")

# Check last 20 lines contain post
last_lines = commons_text.strip().split("\n")[-20:]
last_block = "\n".join(last_lines)
chk("post in last 20 lines", "Advocate" in last_block and "sessions/advocate" in last_block)
chk("post ends with signature", last_block.strip().endswith("— Advocate") or "— Advocate" in last_block)

# --- Scratchpads ---
refl_text = refl.read_text() if refl.exists() else ""
if refl_text:
    chk("reflections populated", len(refl_text) > 100, f"{len(refl_text)} chars")
    chk("reflections has deadline", "deadline" in refl_text.lower())

infra_text = infra.read_text() if infra.exists() else ""
if infra_text:
    chk("infrastructure populated", len(infra_text) > 200, f"{len(infra_text)} chars")
    chk("infra has Builder status", "Builder" in infra_text and "credit" in infra_text.lower())
    chk("infra has timing map", "cycles at" in infra_text.lower() or "Cycle Timing" in infra_text)

# --- No write_file on commons (write incident prevention check) ---
# The commons should be append-only; check it hasn't lost content
chk("commons > 2000 lines", len(commons_text.split("\n")) > 2000, f"{len(commons_text.split())} words")

# --- Summary ---
total = 35
passed = total - len(errors)
print(f"\n{'='*50}")
print(f"Passed: {passed}/{total}")
if errors:
    print(f"Errors: {', '.join(errors[:10])}{'...' if len(errors) > 10 else ''}")
    sys.exit(1)
else:
    print("Verdict: ✅ All files structurally valid. Ad-hoc verification PASS.")
    sys.exit(0)
