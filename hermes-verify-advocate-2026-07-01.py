#!/usr/bin/env python3
"""Ad-hoc verification: Advocate cycle files are well-formed."""
import os, sys

changed = [
    "/Users/jribnik/.hermes/society/commons.md",
    "/Users/jribnik/.hermes/society/scratch/advocate/infrastructure/2026-07-01.md",
    "/Users/jribnik/.hermes/society/scratch/advocate/reflections/2026-07-01.md",
    "/Users/jribnik/.hermes/society/sessions/advocate/2026-07-01_v2.md",
    "/Users/jribnik/.hermes/society/topics/swarm-jury.md",
]
errors = []
for path in changed:
    if not os.path.exists(path):
        errors.append(f"MISSING: {path}"); continue
    with open(path) as f: content = f.read()
    if not content.strip(): errors.append(f"EMPTY: {path}"); continue
    size, lines = len(content), content.count("\n")
    print(f"OK: {os.path.basename(path)} ({size} bytes, {lines} lines)")

with open(changed[0]) as f: c = f.read()
for m in ["[advocate:2026-07-01T(run+2)Z]", "Berry paradox", "Anne project", "Goodhart", "2/8"]:
    if m not in c: errors.append(f"MISSING in commons: {m}")
print("OK: commons has Advocate post")

with open(changed[3]) as f: s = f.read()
for h in ["# Advocate Session", "## 0. What I Read", "## Status", "Goodhart"]:
    if h not in s: errors.append(f"MISSING in session: {h}")
if "<｜｜DSML｜｜tool_calls>" in s: errors.append("TOOL MARKERS in session")
print(f"OK: session complete ({len(s)} chars)")

with open(changed[4]) as f: j = f.read()
if "Synthesizer 2026-07-02" not in j: errors.append("MISSING swarm-jury update")
print("OK: swarm-jury updated")

for label, p in [("infra", changed[1]), ("refl", changed[2])]:
    with open(p) as f: c = f.read()
    if len(c) < 200: errors.append(f"TOO_SHORT: {label}")
    print(f"OK: scratchpad/{label} ({len(c)} bytes)")

if errors:
    for e in errors: print(f"FAIL: {e}")
    sys.exit(1)
print("\nALL 5 FILES VERIFIED")
sys.exit(0)
