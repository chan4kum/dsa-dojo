"""Builds notes/B3-coverage.md: which well-known problems this repo already teaches (and where)."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "tools"))
from lists import BLIND75, FREQUENT  # noqa: E402

from dsa import TOPICS, load  # noqa: E402


def have():
    out = {}
    for t in TOPICS:
        for n, p in enumerate(load(t), 1):
            out.setdefault(p["lc"], f"{t}/{n}")
    return out


def table(groups, h):
    rows, tot, got, missing = [], 0, 0, []
    for g, nums in groups.items():
        cells = []
        for n in nums:
            tot += 1
            if n in h:
                got += 1
                cells.append(f"`{n}` -> `{h[n]}`")
            else:
                cells.append(f"~~{n}~~")
                missing.append(n)
        rows.append(f"| {g} | " + ", ".join(cells) + " |")
    return "| group | LeetCode # -> where it is taught |\n|---|---|\n" + "\n".join(rows), got, tot, missing


def render():
    h = have()
    t1, g1, n1, m1 = table(BLIND75, h)
    t2, g2, n2, m2 = table(FREQUENT, h)
    own = len(h)
    return f"""# B3 - Coverage map (generated - do not edit by hand)

> Honest accounting: this repo teaches **{own} distinct problems** in depth (concept, hints, brute force, optimised
> solution, tests). The big public lists below show what is covered. A struck-through number is **not in the repo
> yet** - but it is almost always a *variation of a pattern that is*; the last column of the pattern finder
> (`notes/00-pattern-finder.md`) tells you which.

## Blind 75 (community list, with a couple of popular swaps): {g1}/{n1} covered
{t1}

## Frequently asked classics: {g2}/{n2} covered
{t2}

## How to use the gaps
For each struck-through problem: name its pattern from the pattern finder, open the matching topic note, and solve it on
LeetCode **after** doing that topic's ladder - treat it as a transfer test, not new material.
Missing from Blind 75: {", ".join(map(str, m1)) or "none"}.
"""


if __name__ == "__main__":
    print(render())
