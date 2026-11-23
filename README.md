# DSA from first principles - concepts, hand-notes and a local practice trainer

Learn data structures & algorithms the way a good teacher would explain them: **concept first, pattern second, problem last** - from easy to hard, with paper-style notes, hand-traced examples, and problems you solve **on your own machine** with instant test feedback.

- No timeline. You move when you understand, not when a calendar says so.
- No dependencies. Python 3.9+ only.
- Every problem has a **brute-force AND an optimised Python solution**, both executed against tests (`python dsa.py selftest`) and cross-checked on random inputs (`python tools/fuzz.py`, `python tools/fuzz_diff.py`).
- Read `REVIEW.md` for an honest audit: what is strong, what was fixed, what is still missing.

## Quick start (2 minutes)

```bash
python dsa.py list                    # topics in learning order + your progress
python dsa.py notes two_pointers      # read the hand-notes for a topic
python dsa.py list two_pointers       # its practice ladder, easy -> hard
python dsa.py start two_pointers/2    # creates workspace/two_pointers_02_3sum.py
python workspace/two_pointers_02_3sum.py     # run YOUR solution against the tests
python dsa.py hint two_pointers/2     # progressive hints (3), then the pattern name
python dsa.py solution two_pointers/2 # brute force + optimised, explained (marks it for review)
python dsa.py quiz 10                 # pattern-recognition drill: name the pattern BEFORE the reveal
python dsa.py coverage                # which Blind-75 / classic problems are covered, and where
python dsa.py review                  # what to redo from a blank file
```

## The learning loop (what "hand notes" means here)
1. **Read** `notes/NN-topic.md`: the one idea, how to spot it, the paper recipe, a worked **hand trace**, a tested template, traps, self-check questions.
2. **Paper first.** Use the one-page template in `notes/00-foundations.md`: restate -> examples by hand -> brute force -> pattern -> invariant -> dry-run table -> complexity.
3. **Code locally** in `workspace/`, run, read the failing case, fix.
4. **Explain back**: answer the self-check questions out loud. If you cannot say *why* the pattern applies, you have not learned it.
5. **Spaced redo**: anything you peeked at appears in `python dsa.py review`.

## Where to start
- `notes/00-foundations.md` - cost model, constraints -> complexity, invariants, the paper method.
- [D01 mastery walkthrough](notes/00-d01.md) maps the 20 complexity, math, and recursion problems to Dojo IDs where available, with local labs and independent project checks.
- `notes/00-pattern-finder.md` - **how to recognise which pattern a problem wants** (constraints, input shape, wording, flowchart, confusable pairs, drill).
- Then topics `01 ... 20` in order. Each only needs ideas from the ones before it; each ends with **"Make it stay"** (picture, rule, why, teach-back, mistakes, when NOT to use).
- `notes/B2-interview-playbook-and-job-search.md` - how to run the interview, get unstuck, behavioural stories, the job-search pipeline, AI-engineer track.
- `notes/B3-coverage.md` - generated map of covered Blind-75 and frequently asked problems.

## What is inside

| # | Topic | Core idea |
|---|---|---|
| 01 | hashing | O(1) membership/lookup, canonical keys |
| 02 | prefix_sums | range sums, subarray = difference of prefixes |
| 03 | two_pointers | converging / same-direction pointers with a discard argument |
| 04 | sliding_window | contiguous ranges with an invariant |
| 05 | array_tricks | Kadane, XOR/sum invariants, cyclic placement |
| 06 | binary_search | monotone predicates, search on the answer |
| 07 | stack_monotonic | LIFO matching, next-greater, monotonic deque |
| 08 | linked_list | pointer surgery, fast/slow, dummy head |
| 09 | intervals | sort + sweep, greedy by end |
| 10 | greedy | local choice + a proof |
| 11 | heap | top-k, two heaps, k-way merge |
| 12 | trees | recursion, BFS, BST |
| 13 | backtracking | choose / explore / un-choose, pruning |
| 14 | graphs | BFS/DFS, topo sort, union-find, Dijkstra |
| 15 | dynamic_programming | state, last choice, base, order |
| 16 | bits_math | XOR, masks, fast power |
| 17 | strings | KMP, borders, hashing |
| 18 | design | LRU, trie, min-stack, median finder |
| 19 | divide_conquer | merge sort and counting while merging |
| 20 | matrix | coordinates, compose transforms, in-place encoding |
| B1 | AI & system design topic map | concepts + local mini-labs |
| B2 | interview playbook & job search | protocol, stuck-protocol, stories, pipeline |
| B3 | coverage map (generated) | Blind 75 + classics -> where each is taught |

**Current content:** 1000 problems, each with 3 hints, an explanation, a brute force (with cost), an optimised solution (with cost) and tests. Blind-75-style list: fully covered (see `notes/B3-coverage.md`).

## How the content is verified (run these yourself)
| Command | What it proves |
|---|---|
| `python3 dsa.py selftest` | every reference solution passes its tests and every brute force is correct |
| `python3 tools/fuzz_diff.py` | brute force and optimised solution agree on random inputs |
| `python3 tools/check_metadata.py` | every problem's LeetCode number, title, slug and difficulty (and every title in the "More:" lists) matches LeetCode data |
| `python3 tools/verify_claims.py` | the factual claims made in the tutorials (Python semantics, algorithm identities, speed rules) are true - each one is *executed* |

Time-sensitive material (AI/system-design map, interview formats) carries an "as of" date and source links at the bottom of the note.

## Repo layout
```
dsa.py                 CLI: list / notes / start / test / hint / solution / review / quiz / coverage / selftest
core.py                test engine + helpers (ListNode, TreeNode, list<->tree adapters)
problems/<topic>.py    problem data (+ <topic>_more*.py extra batches); each problem holds its brute force, optimised solution and complexity
notes/                 generated hand-notes (read these)
_src/                  note sources with {{trace}} / {{solution}} / {{ladder}} placeholders
tools/                 build_notes.py, traces.py (hand traces), anchors.py (teacher anchors), coverage.py + lists.py, fuzz.py, fuzz_diff.py
workspace/             your solutions (git-ignored)
```

## Adding problems (how the set grows toward 1000)
Add a dict to `problems/<topic>.py`:
```python
dict(title="...", diff="E|M|H", lc=<LeetCode number>, slug="<leetcode-slug>",
     prompt="<your OWN short paraphrase>", sig="def f(...):", fn="f",
     tests=[((args...), expected), ...],            # >= 3 tests; compare= "unordered"|"nested_unordered"|"float"
     hints=["nudge", "bigger nudge", "almost the answer"],   # exactly 3
     pattern="...", explain="...",
     brute=r'''def f(...): ...''', brute_cx="O(n^2) ...",       # naive but CORRECT (may time out on big inputs)
     solution=r'''def f(...): ...''', cx="O(n) ...")
```
Put new problems in `problems/<topic>_more*.py` (same `PROBLEMS = [...]` list). Several valid answers? use `check=lambda args, got: ...`; mutates an argument? use `inplace=<arg index>`. Then `python dsa.py selftest && python tools/fuzz_diff.py && python tools/build_notes.py`. Class-based problems use `kind="design"` (see `problems/design.py`); tree/linked-list problems use `adapt_in` / `adapt_out`.

**Code style (checked in CI):** `ruff check .` and `ruff format --check .` must pass (config in `ruff.toml`, 120 columns). The code inside the `brute` / `solution` strings is linted too: `python tools/lint_solutions.py`. After adding a problem run `python tools/format_problems.py` - it lays every problem out the same way and puts a plain-English header on each solution (`# OPTIMISED: O(n) time ... / Idea: ...`). Comment the *why*, not the *what*, inside solutions.

**Copyright note:** prompts are original paraphrases, not copied statements. Each problem links to the original on LeetCode for the official statement and examples.

## Roadmap of content (by topic, not by date)
Done: 20 DSA topics, 1000 problems with brute + optimised solutions, pattern finder, foundations, teacher anchors, interview playbook, coverage map, AI/system-design concept map.
Next (same format): more problems per topic (hard tiers, company-frequent sets), segment tree / SCC / Manacher notes, then full hand-notes + runnable labs for each block of the system-design and AI maps.
