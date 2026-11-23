# 00 - Foundations: how to think about problems from first principles

Read this once, then use it as a reference. Everything after this file is a *pattern*; this file is the machinery underneath all of them.

## 1. What a problem really is
An algorithm problem = **input** -> **output**, plus a **cost budget** (time and memory).
Your job: find a procedure whose cost fits the budget. The budget is hidden in the constraints (section 3).

The universal approach:
1. Make it **correct** (brute force). 2. Find where the **waste** is. 3. Remove the waste using *structure* (order, hashing, monotonicity, overlapping subproblems...). Every pattern in this repo is a way of removing a specific kind of waste.

## 2. Cost model (Big-O by intuition)
Count the basic steps as a function of the input size `n`; ignore constants and lower-order terms.

| n | log2 n | n | n log n | n^2 | 2^n |
|---|---|---|---|---|---|
| 10 | 3 | 10 | 33 | 100 | 1,024 |
| 100 | 7 | 100 | 664 | 10,000 | about 10^30 |
| 1,000 | 10 | 1,000 | 9,965 | 1,000,000 | about 10^301 |
| 10,000 | 13 | 10,000 | 132,877 | 100,000,000 | about 10^3010 |
| 100,000 | 17 | 100,000 | 1,660,964 | 10,000,000,000 | about 10^30102 |
| 1,000,000 | 20 | 1,000,000 | 19,931,568 | 1,000,000,000,000 | about 10^301029 |

- `O(log n)`: halve the problem each step (binary search, balanced tree height).
- `O(n)`: touch each element a constant number of times (one pass, two pointers, hash map build).
- `O(n log n)`: sort, heap operations n times, divide and conquer.
- `O(n^2)`: all pairs (nested loops, simple DP over two sequences).
- `O(2^n)`, `O(n!)`: all subsets / permutations (backtracking) - only fine for n <= ~20 / ~10.
- **Amortised O(1)**: a loop inside a loop can still be O(n) in total if each element is processed once (monotonic stack, KMP, sliding window). Count *total* pushes and pops, not nesting.
- Space counts too: recursion depth = stack space; a DP table = memory.

## 3. Read the constraints: n -> allowed complexity
The table is a starting point. Actual runtime depends on the interpreter, hardware, input, and operations in the loop. Count the dominant work, then benchmark a representative worst-case input near the stated limit. Run `python3 tools/verify_claims.py` for a local loop measurement and treat its result as specific to that loop and environment.

| n (input size) | Aim for | Typical techniques |
|---|---|---|
| <= 10 | O(n!) / O(2^n * n) | brute force, permutations, backtracking |
| <= 20 | O(2^n * n) | bitmask DP, subsets, meet in the middle |
| <= 100 - 500 | O(n^3) | Floyd-Warshall, interval DP |
| <= 2,000 - 5,000 | O(n^2) | 2-D DP, all pairs |
| <= 10^5 - 10^6 | **O(n log n)** or O(n) | sort, heap, binary search, two pointers, hashing, sliding window, union-find |
| <= 10^9 | O(log n) / O(1) | binary search on the answer, math, fast exponentiation |

## 4. How data is laid out (why structures have the costs they have)
- **Array:** contiguous memory -> index in O(1), insert/delete in the middle O(n) (shift).
- **Linked list:** nodes scattered, linked by pointers -> insert/delete after a known node O(1), reach index i in O(i).
- **Hash table:** `index = hash(key) % capacity` -> O(1) average insert/lookup/delete; no order.
- **Stack / queue / deque:** access only at the ends -> O(1); they encode *order of processing* (LIFO / FIFO).
- **Heap:** array-backed complete binary tree, parent <= children -> min in O(1), push/pop O(log n).
- **Binary search tree / balanced tree:** ordered, O(log n) when balanced. (Python has no built-in; use `bisect` on a list or `sortedcontainers`.)
- **Graph:** nodes + edges; adjacency list uses O(V+E) memory.
- **Trie:** a tree keyed by characters; cost depends on word length, not on how many words.

## 5. Recursion = a stack of unfinished work
- A recursive function needs a **base case** and a **smaller subproblem**.
- Each call waits on the **call stack**; depth too large -> `RecursionError` in Python (limit ~1000). Raise it with `sys.setrecursionlimit` or rewrite with an explicit stack.
- *Memoisation* = remember results of calls -> turns exponential recursion into polynomial (this is DP).
- **Trust the recursion**: assume it already works for smaller inputs; only write how to combine.

## 6. Invariants: the thing that makes code correct
An **invariant** is a statement that is true before and after every loop iteration.
- Binary search: "if the target exists, it is inside `[lo, hi]`".
- Sliding window: "`s[l..r]` has no duplicate characters".
- Monotonic stack: "the stack is decreasing".
- Kadane: "`cur` is the best sum of a subarray ending at i".
Write the invariant **before** the code. Then check three things: it is true initially, each iteration preserves it, and at the end it implies the answer. This is proof by induction in miniature, and it catches off-by-one errors.

## 7. The paper method (your hand-notes page)
Do every problem on paper before the keyboard. One page per problem, with these boxes:

```
PROBLEM: ........................   (id / link)           DATE: ......
1 RESTATE in my words (input, output, constraints, n = ?)
2 EXAMPLES worked by hand (small, a tricky one, an edge case: empty / 1 element / duplicates / negatives)
3 BRUTE FORCE idea + its cost (and which line is the waste?)
4 PATTERN guess  (use notes/00-pattern-finder.md) + WHY (which signal?)
5 INVARIANT / state in one sentence
6 DRY RUN on example 1 (a table: one row per step, one column per variable)
7 COMPLEXITY  time ........  space ........
8 BUGS I hit / what I would miss next time
```
The dry-run table is the heart of it: the traces in each topic note are exactly this table, generated by running the code. Make yours by hand first, then compare.

## 8. Edge cases checklist
Empty input - one element - all equal - sorted / reverse sorted - duplicates - negatives and zero - very large values (overflow outside Python) - cycles in a graph - disconnected graph - one node tree.

## 9. Python toolkit for interviews
`collections.deque / Counter / defaultdict / OrderedDict`, `heapq` (min-heap; negate for max), `bisect_left/right`, `functools.lru_cache`, `itertools.combinations/permutations`, `sorted(key=...)`, `enumerate`, `zip`, slicing creates **copies** (O(k)), `float("inf")`, `divmod`, integer `//` and `%` (floor semantics for negatives!).

## 10. How to practise (the loop)
1. Read the topic note (concept -> recipe -> trace).
2. `python dsa.py start <topic>/<n>`, do the paper page, then code in `workspace/`.
3. `python dsa.py test <topic>/<n>`. Stuck? `python dsa.py hint ...` (3 hints, then the pattern name).
4. Passed? Answer the self-check questions out loud. Only then read `python dsa.py solution ...` and compare ideas, not code.
5. Anything you peeked at lands in `python dsa.py review`: redo it from a blank file later.
6. Never move on from a topic until you can explain **why** each pattern applies, not only *how* to code it.
