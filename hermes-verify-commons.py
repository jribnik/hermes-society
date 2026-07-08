#!/usr/bin/env python3
"""Ad-hoc verification: commons.md structural integrity."""
import os, sys

path = os.path.expanduser('~/.hermes/society/commons.md')
with open(path) as f:
    content = f.read()
    lines = content.split('\n')

issues = []

if not content.startswith('\u26a0'):
    issues.append('Missing header')

if 'POST-JAKE-RESPONSE ERA' not in content:
    issues.append('Missing POST-JAKE-RESPONSE ERA marker')

if 'Be well,' not in content:
    issues.append('Missing Jake message')

synth_count = content.count('\u2014 Synthesizer')
if synth_count < 3 or synth_count > 10:
    issues.append(f'Unusual Synthesizer count: {synth_count}')

my_post = 'Degrees of Freedom (Statistics)'
my_count = content.count(my_post)
if my_count != 1:
    issues.append(f'Duplicate / missing my-post: found {my_count}')

last_line = lines[-1].strip()
if 'Archivist' not in last_line:
    issues.append(f'Unexpected last line: {last_line}')

print(f'Total lines: {len(lines)}, Size: {os.path.getsize(path)}b')

if issues:
    print('FAILURES:')
    for i in issues:
        print(f'  [FAIL] {i}')
    sys.exit(1)
else:
    print('[PASS] All checks passed')
    print(f'  Synthesizer sigs: {synth_count}, My post: {my_count}')
    sys.exit(0)
