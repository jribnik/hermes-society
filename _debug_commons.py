#!/usr/bin/env python3
"""Debug commons.md line structure."""
with open('/Users/jribnik/.hermes/society/commons.md', 'r') as f:
    raw = f.read()
if raw.endswith('\n'):
    raw = raw[:-1]
lines = raw.split('\n')
print(f'Total: {len(lines)}')
for i in range(46, 62):
    content = lines[i] if lines[i] else '(empty)'
    print(f'{i}: {content[:80]}')
