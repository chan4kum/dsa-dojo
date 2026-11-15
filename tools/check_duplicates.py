"""Fail if two problems share a LeetCode number or a title.

Run after adding problems: python3 tools/check_duplicates.py
"""

import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
by_lc, by_title = {}, {}
for path in sorted((ROOT / "problems").glob("*.py")):
    text = path.read_text()
    for m in re.finditer(r'title="([^"]+)",\s*\n\s*diff="[EMH]",\s*\n\s*lc=(\d+)', text):
        title, lc = m.group(1), m.group(2)
        by_lc.setdefault(lc, []).append((title, path.name))
        by_title.setdefault(title, []).append(path.name)

bad = {k: v for k, v in by_lc.items() if len(v) > 1}
bad_titles = {k: v for k, v in by_title.items() if len(v) > 1}
for lc, entries in sorted(bad.items(), key=lambda kv: int(kv[0])):
    print(f"DUPLICATE LeetCode {lc}: {entries}")
for title, files in bad_titles.items():
    print(f"DUPLICATE title {title!r}: {files}")
print(f"check_duplicates: {len(by_lc)} distinct LeetCode numbers, {len(bad) + len(bad_titles)} duplicates")
sys.exit(1 if bad or bad_titles else 0)
