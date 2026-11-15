# 13 - Backtracking

> **One idea:** build a solution one decision at a time; when a partial solution can no longer work (or is complete), undo the last decision and try the next.

## 1. First principles
- It is a **DFS over a decision tree**. Each node is a partial solution, each edge is a choice, each leaf is a complete (or dead) solution.
- The template never changes: **choose -> explore -> un-choose**.
- `path` is shared and mutated in place, so (a) every `append` has a matching `pop`, (b) record **copies** (`path[:]`).
- **Pruning** is the whole game: stop as soon as the partial solution is impossible (sum exceeded, parentheses unbalanced, column attacked).
- Size of the tree tells the cost: subsets `2^n`, permutations `n!`, combinations `C(n,k)`, N-Queens far less than `n^n` thanks to pruning.

## 2. How to spot it
- "return **all** ...", "generate every ...", "list all valid ...".
- Small n (<= ~20) in the constraints.
- Constraints between choices (no two queens attack, sum equals target, no repeats).
- If you only need a **count/min/max** and subproblems repeat -> that is DP, not backtracking.

## 3. Paper recipe
1. Draw the decision tree for n = 3 on paper (like the trace below).
2. State: **what is a choice** at each level, and **when is a solution complete**.
3. Decide how to avoid duplicates: a `start` index for combinations, a `used[]` array for permutations, "skip equal neighbours after sorting" for repeated values.
4. Write the pruning conditions *before* the recursion.
5. Count the leaves to sanity-check complexity.

## 4. Hand trace (subsets of [1, 2, 3])
{{trace:subsets_tree}}

## 5. Template
{{solution:backtracking/1}}

Three shapes to memorise:
- **Include/exclude** (subsets): recurse on `i + 1` twice.
- **Pick-from-remaining** (permutations): loop over all unused items.
- **Pick-from-here-onwards** (combinations): `for i in range(start, n): ... go(i + 1)` (or `go(i)` if reuse allowed).

## 6. Traps
- Appending `path` instead of `path[:]` -> all results end up identical/empty.
- Missing the un-choose step.
- Duplicates in the input: sort first, then `if i > start and a[i] == a[i-1]: continue`.
- Pruning too late (after recursing) or not at all -> time-limit exceeded.
- Deep recursion on long inputs (use `sys.setrecursionlimit` or iterate).

## 7. Self-check
1. Draw the tree for permutations of [1,2,3]. How many leaves, and how many nodes in total?
2. How does a `start` index remove duplicate combinations?
3. Which conditions let Generate Parentheses prune to only valid prefixes?

## 8. Practice ladder
{{ladder}}

**More:** 90 Subsets II (M), 47 Permutations II (M), 77 Combinations (M), 40 Combination Sum II (M), 216 Combination Sum III (M), 17 Letter Combinations of a Phone Number (M), 79 Word Search (M), 131 Palindrome Partitioning (M), 93 Restore IP Addresses (M), 698 Partition to K Equal Sum Subsets (M), 37 Sudoku Solver (H).
