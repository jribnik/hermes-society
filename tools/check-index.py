#!/usr/bin/env python3
"""Quick check on index.json quality."""
import json

with open("/Users/jribnik/.hermes/society/sessions/index.json") as f:
    data = json.load(f)

# Recent entries (last 12 by wallClock if available)
with_wallclock = [e for e in data if e.get("wallClock")]
with_wallclock.sort(key=lambda x: x["wallClock"], reverse=True)

print("=== 12 most recent (by wallClock) ===")
for e in with_wallclock[:12]:
    print(f"  {e['instance']}/{e['date']}", end="")
    if e.get("version"): print(f" ({e['version']})", end="")
    t = e.get("title","")[:70]
    wc = e.get("wallClock","N/A")
    kw = e.get("keywords",[])
    print(f"  |  {t}")
    print(f"       wallClock: {wc}  kw: {kw}")

print()
print(f"Total entries: {len(data)}")
print(f"Instances: {sorted(set(e['instance'] for e in data))}")
print(f"With wallClock: {sum(1 for e in data if e.get('wallClock'))}/{len(data)}")
print(f"With title > 15 chars: {sum(1 for e in data if len(e.get('title','')) > 15)}/{len(data)}")
