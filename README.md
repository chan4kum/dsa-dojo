# DSA from first principles - concepts, hand-notes and a local practice trainer

Learn data structures & algorithms the way a good teacher would explain them: **concept first, pattern second, problem last** - from easy to hard, with paper-style notes, hand-traced examples, and problems you solve **on your own machine** with instant test feedback.

- No timeline. You move when you understand, not when a calendar says so.
- No dependencies. Python 3.9+ only.
- Every reference solution is **executed against tests** (`python dsa.py selftest`), and many are cross-checked against brute force (`python tools/fuzz.py`).

## Quick start (2 minutes)

```bash
python dsa.py list                    # topics in learning order + your progress
python dsa.py notes two_pointers      # read the hand-notes for a topic
python dsa.py list two_pointers       # its practice ladder, easy -> hard
python dsa.py start two_pointers/2    # creates workspace/two_pointers_02_3sum.py
python workspace/two_pointers_02_3sum.py     # run YOUR solution against the tests
python dsa.py hint two_pointers/2     # progressive hints (3), then the pattern name
python dsa.py solution two_pointers/2 # explained reference solution (marks it for review)
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
- `notes/00-pattern-finder.md` - **how to recognise which pattern a problem wants** (constraints, input shape, wording, flowchart, confusable pairs, drill).
- Then topics `01 ... 19` in order. Each only needs ideas from the ones before it.

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
| B1 | AI & system design topic map | concepts + local mini-labs |

**Current content:** 77 problems with hints, explanations and tests (this is batch 1 of a growing set - see below).

## Repo layout
```
dsa.py                 CLI: list / notes / start / test / hint / solution / review / selftest
core.py                test engine + helpers (ListNode, TreeNode, list<->tree adapters)
problems/<topic>.py    problem data: prompt, hints, explanation, reference solution, tests
notes/                 generated hand-notes (read these)
_src/                  note sources with {{trace}} / {{solution}} / {{ladder}} placeholders
tools/                 build_notes.py (regenerates notes), traces.py (hand-trace tables), fuzz.py
workspace/             your solutions (git-ignored)
```

## Adding problems (how the set grows toward 1000)
Add a dict to `problems/<topic>.py`:
```python
dict(title="...", diff="E|M|H", lc=<LeetCode number>, slug="<leetcode-slug>",
     prompt="<your OWN short paraphrase>", sig="def f(...):", fn="f",
     tests=[((args...), expected), ...],            # >= 3 tests; compare= "unordered"|"nested_unordered"|"float"
     hints=["nudge", "bigger nudge", "almost the answer"],   # exactly 3
     pattern="...", explain="...", solution=r'''def f(...): ...''')
```
Then `python dsa.py selftest && python tools/build_notes.py`. Class-based problems use `kind="design"` (see `problems/design.py`); tree/linked-list problems use `adapt_in` / `adapt_out`.

**Copyright note:** prompts are original paraphrases, not copied statements. Each problem links to the original on LeetCode for the official statement and examples.

## Roadmap of content (by topic, not by date)
Batch 1 (this): 19 DSA topics, 77 problems, pattern finder, foundations, AI/system-design concept map.
Next batches (same format): more problems per topic until ~1000 (adding monotone-DP variants, graph variants, hard tiers, company-frequent sets), then full hand-notes + runnable labs for each block of the system-design and AI maps.
