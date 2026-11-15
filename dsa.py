#!/usr/bin/env python3
"""dsa.py - local, self-paced DSA trainer. No dependencies, Python 3.9+.

  python dsa.py list [topic]          topics, or the problems of one topic, with your status
  python dsa.py notes <topic>         read the hand-notes for a topic (concept -> recipe -> traced example)
  python dsa.py start <topic>/<n>     create workspace/<file>.py - a stub you solve locally
  python dsa.py test <file | id>      run your solution against the tests
  python dsa.py hint <topic>/<n>      next hint (3 levels, then the pattern name)
  python dsa.py solution <id>         explained reference solution (marks the problem for review)
  python dsa.py review                problems you peeked at / haven't solved -> redo from a blank file
  python dsa.py selftest              run every reference solution (what CI runs)

Your progress lives in .progress.json (git-ignored).
"""

import argparse
import importlib
import json
import re
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
from core import run_problem  # noqa: E402

PROGRESS = ROOT / ".progress.json"
WORKSPACE = ROOT / "workspace"

# Concept order: each topic only needs ideas from the ones before it.
TOPICS = [
    "hashing",
    "prefix_sums",
    "two_pointers",
    "sliding_window",
    "array_tricks",
    "binary_search",
    "stack_monotonic",
    "linked_list",
    "intervals",
    "greedy",
    "heap",
    "trees",
    "backtracking",
    "graphs",
    "dynamic_programming",
    "bits_math",
    "strings",
    "design",
    "divide_conquer",
    "matrix",
]
DIFF = {"E": "Easy", "M": "Medium", "H": "Hard"}


def load(topic):
    """Load a topic: the base file plus its `_more*` batches. Every problem carries its own brute force and cost."""
    probs = list(importlib.import_module(f"problems.{topic}").PROBLEMS)
    for suffix in ("_more", "_more2", "_more3", "_more4"):
        name = f"problems.{topic}{suffix}"
        try:
            probs += importlib.import_module(name).PROBLEMS
        except ModuleNotFoundError as e:
            if e.name != name:
                raise
    return probs


def by_difficulty(probs):
    """(1-based id, problem) pairs ordered easy -> hard, ids unchanged."""
    order = {"E": 0, "M": 1, "H": 2}
    return sorted(enumerate(probs, 1), key=lambda t: (order[t[1]["diff"]], t[0]))


def get(pid):
    m = re.fullmatch(r"([a-z_]+)/(\d+)", pid)
    if not m or m.group(1) not in TOPICS:
        sys.exit(f"Unknown id '{pid}'. Use <topic>/<n>, e.g. two_pointers/3  (see: python dsa.py list)")
    probs = load(m.group(1))
    n = int(m.group(2))
    if not 1 <= n <= len(probs):
        sys.exit(f"{m.group(1)} has {len(probs)} problems (1..{len(probs)}).")
    return m.group(1), n, probs[n - 1]


def progress():
    return json.loads(PROGRESS.read_text()) if PROGRESS.exists() else {}


def save(pr):
    PROGRESS.write_text(json.dumps(pr, indent=1))


def icon(rec):
    if not rec:
        return "[ ]"
    if rec.get("solved") and not rec.get("peeked"):
        return "[x]"
    if rec.get("solved"):
        return "[~]"  # solved, but after peeking at the solution -> redo later
    if rec.get("peeked"):
        return "[?]"
    return "[.]"


def slug(title):
    return re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")


def url(p):
    return f"https://leetcode.com/problems/{p['slug']}/"


# ------------------------------------------------------------------ commands
def cmd_list(args):
    pr = progress()
    if not args.topic:
        print("\nTOPICS (in learning order)   legend: [x] solved  [~] solved after peeking  [?] peeked  [.] tried\n")
        total = done = 0
        for i, t in enumerate(TOPICS, 1):
            probs = load(t)
            s = sum(1 for n in range(1, len(probs) + 1) if pr.get(f"{t}/{n}", {}).get("solved"))
            total, done = total + len(probs), done + s
            print(f"  {i:>2}. {t:<20} {s:>2}/{len(probs):<2}   notes/{i:02d}-{t}.md")
        print(f"\n  total {done}/{total}\n")
        return
    probs = load(args.topic)
    print(f"\n{args.topic}\n")
    for n, p in by_difficulty(probs):
        print(
            f"  {icon(pr.get(f'{args.topic}/{n}'))} {args.topic}/{n:<3} {DIFF[p['diff']]:<7} "
            f"LC#{p['lc']:<5} {p['title']}"
        )
    print()


def cmd_notes(args):
    if args.topic not in TOPICS:
        sys.exit("Unknown topic. See: python dsa.py list")
    f = ROOT / "notes" / f"{TOPICS.index(args.topic) + 1:02d}-{args.topic}.md"
    print(f.read_text(encoding="utf-8") if f.exists() else "(notes not generated yet: run python tools/build_notes.py)")


def cmd_start(args):
    topic, n, p = get(args.id)
    WORKSPACE.mkdir(exist_ok=True)
    path = WORKSPACE / f"{topic}_{n:02d}_{slug(p['title'])}.py"
    if path.exists():
        print(f"Already exists: {path}  (delete it to start from a blank file)")
        return
    prompt = "\n".join("# " + left for left in textwrap.wrap(p["prompt"], 92))
    sig = textwrap.dedent(p["sig"]).strip("\n")
    stub = f"""# PROBLEM: {topic}/{n}
# {p["title"]}  ({DIFF[p["diff"]]})   LeetCode #{p["lc"]}   {url(p)}
#
{prompt}
#
# ON PAPER FIRST (see notes/{TOPICS.index(topic) + 1:02d}-{topic}.md):
#   1 restate in your words   2 solve 2-3 examples by hand   3 brute force + its cost
#   4 which pattern & why     5 the invariant                6 dry-run your idea   7 complexity
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))
from core import *   # List, Optional, ListNode, TreeNode, heapq, deque, Counter, ...


{sig}
    pass   # <- your code


if __name__ == "__main__":
    from dsa import run_file
    run_file(__file__)
"""
    path.write_text(stub, encoding="utf-8")
    pr = progress()
    pr.setdefault(args.id, {})["started"] = True
    save(pr)
    print(
        f"Created {path.relative_to(ROOT)}\nSolve it, then run:  python {path.relative_to(ROOT)}\n"
        f"Stuck? python dsa.py hint {args.id}"
    )


def run_file(file):
    src = Path(file).read_text(encoding="utf-8")
    m = re.search(r"# PROBLEM: ([a-z_]+/\d+)", src)
    if not m:
        sys.exit("No '# PROBLEM: topic/n' header found - was this file made by `dsa.py start`?")
    check(m.group(1), src)


def check(pid, src):
    topic, n, p = get(pid)
    print(f"\n{p['title']}  ({DIFF[p['diff']]})  [{pid}]")
    passed, total = run_problem(p, src)
    pr = progress()
    rec = pr.setdefault(pid, {})
    rec["attempts"] = rec.get("attempts", 0) + 1
    if passed == total:
        rec["solved"] = True
        print(f"\n  ALL {total} TESTS PASS. Before moving on, answer out loud / on paper:")
        print("   - What is the time and space complexity, and which line dominates?")
        print("   - What is the invariant that makes it correct?")
        print("   - Which input would break a naive version of this? (empty, 1 element, duplicates, negatives)")
        print(f"   - Then compare with: python dsa.py solution {pid}   (marks it for review)\n")
    else:
        print(f"\n  {passed}/{total} passed. Need a nudge?  python dsa.py hint {pid}\n")
    save(pr)


def cmd_test(args):
    t = args.target
    if t.endswith(".py") or Path(t).exists():
        return run_file(t)
    topic, n, p = get(t)
    cands = sorted(WORKSPACE.glob(f"{topic}_{n:02d}_*.py"))
    if not cands:
        sys.exit(f"No workspace file yet. Run: python dsa.py start {t}")
    run_file(cands[0])


def cmd_hint(args):
    topic, n, p = get(args.id)
    pr = progress()
    rec = pr.setdefault(args.id, {})
    k = rec.get("hints", 0)
    hints = p["hints"]
    if k < len(hints):
        print(f"\nHint {k + 1}/{len(hints)}: {hints[k]}\n")
        rec["hints"] = k + 1
    else:
        print(
            f"\nNo more hints. The pattern is: {p['pattern']}\nRead: notes/{TOPICS.index(topic) + 1:02d}-{topic}.md\n"
        )
    save(pr)


def cmd_solution(args):
    topic, n, p = get(args.id)
    print(f"\n{p['title']}  ({DIFF[p['diff']]})  {url(p)}\n\nPattern: {p['pattern']}\n")
    print(textwrap.dedent(p["explain"]).strip(), "\n")
    if p.get("brute"):
        print(
            f"BRUTE FORCE  ({p.get('brute_cx', '')})\n```python\n" + textwrap.dedent(p["brute"]).strip("\n") + "\n```\n"
        )
    print(
        f"OPTIMISED  ({p.get('cx', 'see explanation')})\n```python\n"
        + textwrap.dedent(p["solution"]).strip("\n")
        + "\n```\n"
    )
    pr = progress()
    pr.setdefault(args.id, {})["peeked"] = True
    save(pr)
    print("(marked for review - redo it from a blank file in a few days)\n")


def cmd_review(args):
    pr = progress()
    rows = [k for k, v in pr.items() if v.get("peeked") or (v.get("attempts") and not v.get("solved"))]
    if not rows:
        print("Nothing to review. Nice.")
        return
    print("\nRedo these from a blank file (delete the workspace file first). Remove the mark by solving cleanly.\n")
    for k in sorted(rows):
        topic, n, p = get(k)
        print(f"  {icon(pr[k])} {k:<22} {p['title']}")
    print()


def cmd_quiz(args):
    """Pattern drill: read a problem, name the pattern BEFORE seeing it (the #1 interview skill)."""
    import random

    pool = []
    pr = progress()
    for t in TOPICS:
        if args.topic and t != args.topic:
            continue
        for n, p in enumerate(load(t), 1):
            pool.append((f"{t}/{n}", p))
    if not pool:
        sys.exit("no such topic")
    random.shuffle(pool)
    interactive = sys.stdin.isatty()
    score = 0
    for key, p in pool[: args.count]:
        print("=" * 72)
        print(f"{p['title']}   [{DIFF[p['diff']]}]")
        print(textwrap.fill(p["prompt"], 72))
        print("=" * 72)
        if interactive:
            input(
                (
                    "1) Which PATTERN does this smell like?  2) Brute-force cost?  3) Target cost?   (think / write "
                    "it, then press Enter) "
                )
            )
        print(f"PATTERN : {p['pattern']}")
        if p.get("brute_cx"):
            print(f"BRUTE   : {p['brute_cx']}")
        if p.get("cx"):
            print(f"TARGET  : {p['cx']}")
        print(f"1st HINT: {p['hints'][0]}")
        if interactive:
            got = input("Did you name the pattern (y/n)? ").strip().lower() == "y"
            score += got
            if not got:
                pr.setdefault(key, {})["peeked"] = True  # goes into `review`
        print()
    if interactive:
        save(pr)
        print(
            f"Pattern recognition: {score}/{min(args.count, len(pool))}. "
            "Missed ones were added to `python dsa.py review`."
        )


def cmd_coverage(args):
    sys.path.insert(0, str(ROOT / "tools"))
    import coverage

    print(coverage.render())


def cmd_selftest(args):
    bad = 0
    count = 0
    brutes = 0
    missing_brute = []
    for t in TOPICS:
        for n, p in enumerate(load(t), 1):
            count += 1
            problems = [
                f
                for f in (
                    "title",
                    "diff",
                    "lc",
                    "slug",
                    "prompt",
                    "sig",
                    "tests",
                    "hints",
                    "pattern",
                    "explain",
                    "solution",
                )
                if f not in p
            ]
            if problems:
                print(f"{t}/{n}: missing fields {problems}")
                bad += 1
                continue
            if len(p["tests"]) < 3 or len(p["hints"]) != 3:
                print(f"{t}/{n} {p['title']}: needs >=3 tests and exactly 3 hints")
                bad += 1
            if p.get("kind") != "design" and "fn" not in p:
                print(f"{t}/{n}: missing fn")
                bad += 1
                continue
            passed, total = run_problem(p, textwrap.dedent(p["solution"]), verbose=False)
            if passed != total:
                print(f"FAIL {t}/{n} {p['title']}: {passed}/{total}")
                run_problem(p, textwrap.dedent(p["solution"]), verbose=True)
                bad += 1
            if p.get("brute"):
                st = {}
                bp, bt = run_problem(p, textwrap.dedent(p["brute"]), verbose=False, timeout=1.0, stats=st)
                if bp + st["timeouts"] != bt:  # brute may be too slow on big tests, but must never be WRONG
                    print(f"BRUTE WRONG {t}/{n} {p['title']}: {bp}/{bt} (timeouts {st['timeouts']})")
                    run_problem(p, textwrap.dedent(p["brute"]), verbose=True, timeout=1.0)
                    bad += 1
                brutes += 1
            else:
                missing_brute.append(f"{t}/{n}")
    print(
        f"\nselftest: {count - bad}/{count} problems OK; {brutes} with a verified brute force"
        + (f"; no brute yet: {len(missing_brute)}" if missing_brute else "")
    )
    sys.exit(1 if bad else 0)


def main():
    ap = argparse.ArgumentParser(
        prog="dsa.py", description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("list")
    s.add_argument("topic", nargs="?")
    s.set_defaults(f=cmd_list)
    s = sub.add_parser("notes")
    s.add_argument("topic")
    s.set_defaults(f=cmd_notes)
    s = sub.add_parser("start")
    s.add_argument("id")
    s.set_defaults(f=cmd_start)
    s = sub.add_parser("test")
    s.add_argument("target")
    s.set_defaults(f=cmd_test)
    s = sub.add_parser("hint")
    s.add_argument("id")
    s.set_defaults(f=cmd_hint)
    s = sub.add_parser("solution")
    s.add_argument("id")
    s.set_defaults(f=cmd_solution)
    s = sub.add_parser("review")
    s.set_defaults(f=cmd_review)
    s = sub.add_parser("quiz")
    s.add_argument("count", nargs="?", type=int, default=5)
    s.add_argument("--topic")
    s.set_defaults(f=cmd_quiz)
    s = sub.add_parser("coverage")
    s.set_defaults(f=cmd_coverage)
    s = sub.add_parser("selftest")
    s.set_defaults(f=cmd_selftest)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
