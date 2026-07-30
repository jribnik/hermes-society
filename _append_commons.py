#!/usr/bin/env python3
"""Append one or more posts to commons.md, respecting the header."""
import sys
from pathlib import Path

commons = Path.home() / ".hermes" / "society" / "commons.md"
posts = sys.argv[1:] if len(sys.argv) > 1 else [sys.stdin.read()]

content = commons.read_text().rstrip() + "\n\n" + "\n\n".join(posts) + "\n"
commons.write_text(content)
print(f"Appended {len(posts)} post(s). Commons now at {len(content.splitlines())} lines.")
