"""Verify problem metadata against independent public LeetCode data.

What is checked (for every problem in problems/*.py):
  * the LeetCode number exists and its official title matches ours (case/punctuation-insensitive)
  * our `slug` equals the slug LeetCode uses in the problem URL
  * our difficulty letter (E/M/H) equals the official difficulty
and for every "NNN Title (E|M|H)" mention in _src/*.md ("More:" lists) the same three facts.

Sources, in order of trust:
  1. PRIMARY  - github.com/neenza/leetcode-problems (merged_problems.json): an export of LeetCode's own problem data
                (frontend id, title, URL slug, difficulty) for the free problems.
  2. FALLBACK - the problem table of github.com/kamyu104/LeetCode-Solutions, used ONLY for problems missing from the
                primary (premium or newer ones). It has known typos and author-assigned difficulties, so for those
                problems only number + title are compared and the result is reported as "secondary source only".

Usage:  python3 tools/check_metadata.py [--official FILE.json] [--secondary FILE.md]
Exit status 1 when any mismatch against the primary source is found.
"""

import argparse
import glob
import importlib
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
OFFICIAL_URL = "https://raw.githubusercontent.com/neenza/leetcode-problems/master/merged_problems.json"
SECONDARY_URLS = [
    "https://raw.githubusercontent.com/kamyu104/LeetCode-Solutions/master/" + name
    for name in ("0001-1000.md", "1001-2000.md", "2001-3000.md", "README.md")
]
ROW = re.compile(r"^(\d+)\s*\|\s*\[(.+?)\]\(https://leetcode\.com/problems/([^/)]+)/?\)(.*)$")
LEVEL = {"Easy": "E", "Medium": "M", "Hard": "H"}

# Premium / dataset-gap problems, confirmed one by one against LeetCode's problem list
# (huggingface.co/datasets/kaysss/leetcode-problem-set, an export of LeetCode's own API) on 2026-11-15.
CONFIRMED_EXTRA = {
    252: ("Meeting Rooms", "meeting-rooms", "E"),
    253: ("Meeting Rooms II", "meeting-rooms-ii", "M"),
    261: ("Graph Valid Tree", "graph-valid-tree", "M"),
    269: ("Alien Dictionary", "alien-dictionary", "H"),
    271: ("Encode and Decode Strings", "encode-and-decode-strings", "M"),
    323: (
        "Number of Connected Components in an Undirected Graph",
        "number-of-connected-components-in-an-undirected-graph",
        "M",
    ),
    359: ("Logger Rate Limiter", "logger-rate-limiter", "E"),
    436: ("Find Right Interval", "find-right-interval", "M"),
    759: ("Employee Free Time", "employee-free-time", "H"),
    1229: ("Meeting Scheduler", "meeting-scheduler", "M"),
    1244: ("Design A Leaderboard", "design-a-leaderboard", "M"),
    1272: ("Remove Interval", "remove-interval", "M"),
}


def norm(title):
    """Lower-case and keep only letters/digits so punctuation differences do not matter."""
    return re.sub(r"[^a-z0-9]+", "", title.lower())


def fetch(url):
    return urllib.request.urlopen(url, timeout=120).read().decode("utf-8")


def load_official(path):
    """frontend id -> (title, slug, difficulty letter) from LeetCode's own data."""
    data = json.loads(open(path, encoding="utf-8").read() if path else fetch(OFFICIAL_URL))
    return {int(q["frontend_id"]): (q["title"], q["problem_slug"], LEVEL[q["difficulty"]]) for q in data["questions"]}


def load_secondary(path):
    """number -> (title, slug, letter) from the community table (fallback only)."""
    text = open(path, encoding="utf-8").read() if path else "\n".join(fetch(u) for u in SECONDARY_URLS)
    index = {}
    for line in text.splitlines():
        m = ROW.match(line.strip())
        if not m:
            continue
        level = re.search(r"\b(Easy|Medium|Hard)\b", m.group(4))
        if level:
            index[int(m.group(1))] = (m.group(2), m.group(3), LEVEL[level.group(1)])
    return index


MORE_LINE = re.compile(r"^(\*\*More[^*]*\*\*) (.*?)(\.?)$", re.M)
CHUNK = re.compile(r"^(\d{1,4}) (.+?) \((E|M|H)(?:, ([^)]*))?\)$")


def more_mentions(text):
    """Yield (match, [(number, title, level, note), ...]) for every '**More ...:**' line of a tutorial."""
    for m in MORE_LINE.finditer(text):
        items = []
        for chunk in re.split(r", (?=\d{1,4} [A-Z0-9])", m.group(2)):
            c = CHUNK.match(chunk.strip())
            if c is None:
                raise ValueError(f"cannot parse mention: {chunk!r}")
            items.append((int(c.group(1)), c.group(2), c.group(3), c.group(4)))
        yield m, items


def our_problems():
    for path in sorted(glob.glob(os.path.join(ROOT, "problems", "*.py"))):
        stem = os.path.basename(path)[:-3]
        if stem.startswith("_") or stem == "__init__":
            continue
        for p in importlib.import_module("problems." + stem).PROBLEMS:
            yield stem, p


def rewrite_notes(official):
    """Replace every 'More:' title/difficulty that the primary source knows with the official one."""
    changed = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "_src", "*.md"))):
        text = open(path, encoding="utf-8").read()
        out, last = [], 0
        for m, items in more_mentions(text):
            fixed = []
            for num, title, level, note in items:
                ref = official.get(num)
                if ref:
                    title, level = ref[0], ref[2]
                fixed.append(f"{num} {title} ({level}{', ' + note if note else ''})")
            out.append(text[last : m.start()] + m.group(1) + " " + ", ".join(fixed) + m.group(3))
            last = m.end()
        new = "".join(out) + text[last:]
        if new != text:
            changed += 1
            open(path, "w", encoding="utf-8").write(new)
    print(f"rewrote the More: line in {changed} tutorial file(s)")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--official")
    ap.add_argument("--secondary")
    ap.add_argument("--rewrite-notes", action="store_true", help="rewrite More: lines with the official titles")
    args = ap.parse_args()
    official = load_official(args.official)
    official.update(CONFIRMED_EXTRA)
    secondary = load_secondary(args.secondary)
    if args.rewrite_notes:
        return rewrite_notes(official)
    print(f"primary source: {len(official)} problems; fallback source: {len(secondary)} problems")
    bad, soft, checked = [], [], 0
    seen_soft = set()

    def judge(where, number, title, slug, level):
        """Compare one (number, title[, slug, level]) claim; returns nothing, fills bad/soft."""
        ref = official.get(number)
        if ref is not None:
            if norm(ref[0]) != norm(title):
                bad.append(f"{where}: LC {number} title '{title}' != official '{ref[0]}'")
            if slug is not None and ref[1] != slug:
                bad.append(f"{where}: LC {number} slug '{slug}' != official '{ref[1]}'")
            if level is not None and ref[2] != level:
                bad.append(f"{where}: LC {number} '{title}' difficulty {level} != official {ref[2]}")
            return
        ref = secondary.get(number)
        if ref is None:
            soft.append(f"{where}: LC {number} '{title}' is in neither source (cannot verify)")
        elif norm(ref[0]) != norm(title):
            bad.append(f"{where}: LC {number} title '{title}' != secondary '{ref[0]}'")
        elif number not in seen_soft:
            seen_soft.add(number)
            soft.append(f"LC {number} '{title}': verified by the secondary source only (premium or very new)")

    for stem, p in our_problems():
        checked += 1
        judge(stem, p["lc"], p["title"], p["slug"], p["diff"])
    note_checked = 0
    for path in sorted(glob.glob(os.path.join(ROOT, "_src", "*.md"))):
        text = open(path, encoding="utf-8").read()
        for _, items in more_mentions(text):
            for num, title, level, _ in items:
                note_checked += 1
                judge(os.path.basename(path), num, title, None, level)
    print(f"checked {checked} problems and {note_checked} tutorial mentions")
    for line in soft:
        print("NOTE", line)
    for line in bad:
        print("MISMATCH", line)
    print("OK: all metadata matches" if not bad else f"{len(bad)} mismatch(es)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
