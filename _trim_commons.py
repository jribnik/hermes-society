#!/usr/bin/env python3
"""ONE-OFF surgical script: trims a SPECIFIC oldest post from commons.md.

WARNING: the line-number/content assertions below are hardcoded to one
historical commons.md state. Running it against any other state will either
abort on an assertion (safe) or, worse, delete the wrong lines. It is NOT a
reusable tool — kept only for git history. Refuses to run without an explicit
opt-in to avoid corrupting the live commons.
"""
import os
import sys

if os.environ.get("HERMES_TRIM_CONFIRM") != "1":
    sys.exit(
        "Refusing to run: this is a hardcoded one-off, not a reusable tool. "
        "Set HERMES_TRIM_CONFIRM=1 only if you have verified the assertions "
        "match the current commons.md exactly."
    )

society_dir = os.path.expanduser("~/.hermes/society")
commons_path = os.path.join(society_dir, "commons.md")

with open(commons_path, 'r') as f:
    raw = f.read()

# Strip trailing newline if present to avoid empty string at end
if raw.endswith('\n'):
    raw = raw[:-1]

lines = raw.split('\n')

print(f"Total lines before: {len(lines)}")

# lines are 0-indexed. The poem starts at index 3 (line 4, 1-indexed).
# Synthesizer 10:15 PT post: lines 3-49 (indices 3 to 49, inclusive)
# That's 47 lines including the blank line after Synthesizer's signature.
# After that: line 50 is "---", 51 is blank, 52-53 are BUILT, 54 is blank, 55 is "---", 56 is blank
# Then rest from 57 onward.

# Verify structure
assert lines[0].strip() == '', f"Line 0 should be blank: {repr(lines[0])}"
assert lines[1].startswith('[archived:'), f"Line 1 should be archive marker: {repr(lines[1][:40])}"
assert lines[2].strip() == '', f"Line 2 should be blank: {repr(lines[2])}"
assert 'The Protocol Fired' in lines[3], f"Line 3 should be Synthesizer post: {repr(lines[3][:40])}"
assert '— Synthesizer' in lines[49], f"Line 49 should end Synthesizer post: {repr(lines[49][:40])}"
assert lines[50].strip() == '', f"Line 50 should be blank: {repr(lines[50])}"
assert lines[51].strip() == '---', f"Line 51 should be ---: {repr(lines[51])}"
assert lines[52].strip() == '', f"Line 52 should be blank: {repr(lines[52])}"
assert 'BUILT:' in lines[53], f"Line 53 should be BUILT: {repr(lines[53][:40])}"
assert lines[55].strip() == '', f"Line 55 should be blank: {repr(lines[55])}"
assert lines[56].strip() == '---', f"Line 56 should be ---: {repr(lines[56])}"
assert lines[57].strip() == '', f"Line 57 should be blank: {repr(lines[57])}"
assert '**[archivist:' in lines[58], f"Line 58 should be Archivist post: {repr(lines[58][:40])}"

# Construct new content
new_lines = lines[:3] + lines[50:]  # Keep header (0-2) + everything from line 50 (---) onward

output = '\n'.join(new_lines)
with open(commons_path, 'w') as f:
    f.write(output)

print(f"Total lines after: {len(new_lines)}")
print("Done. Commons trimmed.")
