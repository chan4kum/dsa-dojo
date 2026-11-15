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
`nums = [1, 2, 3]` - read top to bottom; indentation = recursion depth

```text
go(0) path=[]: choose 1
  go(1) path=[1]: choose 2
    go(2) path=[1, 2]: choose 3
      leaf: RECORD [1, 2, 3]
    go(2) path=[1, 2]: skip 3
      leaf: RECORD [1, 2]
  go(1) path=[1]: skip 2
    go(2) path=[1]: choose 3
      leaf: RECORD [1, 3]
    go(2) path=[1]: skip 3
      leaf: RECORD [1]
go(0) path=[]: skip 1
  go(1) path=[]: choose 2
    go(2) path=[2]: choose 3
      leaf: RECORD [2, 3]
    go(2) path=[2]: skip 3
      leaf: RECORD [2]
  go(1) path=[]: skip 2
    go(2) path=[]: choose 3
      leaf: RECORD [3]
    go(2) path=[]: skip 3
      leaf: RECORD []
```

## 5. Template
*Reference solution for **Subsets** (`backtracking/1`) - tested by `python dsa.py selftest`:*

```python
def subsets(nums):
    res, path = [], []
    def go(i):
        if i == len(nums):
            res.append(path[:])          # copy!
            return
        path.append(nums[i])             # choose
        go(i + 1)
        path.pop()                       # un-choose
        go(i + 1)                        # skip nums[i]
    go(0)
    return res
```

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
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `backtracking/1` | Medium | Subsets | [#78](https://leetcode.com/problems/subsets/) | Backtracking: include/exclude decision tree (choose -> explore -> un-choose) |
| `backtracking/2` | Medium | Permutations | [#46](https://leetcode.com/problems/permutations/) | Backtracking with a 'used' set: n! leaves |
| `backtracking/3` | Medium | Combination Sum | [#39](https://leetcode.com/problems/combination-sum/) | Backtracking over combinations: a start index prevents permutations of the same set |
| `backtracking/4` | Medium | Generate Parentheses | [#22](https://leetcode.com/problems/generate-parentheses/) | Backtracking with constraint pruning (only build valid prefixes) |
| `backtracking/6` | Medium | Combinations | [#77](https://leetcode.com/problems/combinations/) | Backtracking: choose / explore / un-choose (subsets of size k) |
| `backtracking/7` | Medium | Combination Sum II | [#40](https://leetcode.com/problems/combination-sum-ii/) | Backtracking with sorted input + 'skip duplicates at the same depth' |
| `backtracking/8` | Medium | Permutations II | [#47](https://leetcode.com/problems/permutations-ii/) | Backtracking over a multiset (counter instead of a used[] array) |
| `backtracking/9` | Medium | Subsets II | [#90](https://leetcode.com/problems/subsets-ii/) | Subsets backtracking + skip duplicates at the same depth |
| `backtracking/10` | Medium | Letter Combinations of a Phone Number | [#17](https://leetcode.com/problems/letter-combinations-of-a-phone-number/) | Backtracking over a product of choices (one level per position) |
| `backtracking/11` | Medium | Word Search | [#79](https://leetcode.com/problems/word-search/) | Grid DFS backtracking with in-place visited marking |
| `backtracking/12` | Medium | Palindrome Partitioning | [#131](https://leetcode.com/problems/palindrome-partitioning/) | Backtracking over cut positions with a validity check (prune early) |
| `backtracking/13` | Medium | Restore IP Addresses | [#93](https://leetcode.com/problems/restore-ip-addresses/) | Backtracking with validity constraints and length pruning |
| `backtracking/5` | Hard | N-Queens | [#51](https://leetcode.com/problems/n-queens/) | Backtracking with O(1) conflict checks via sets (columns, diagonals) |

Start one with `python dsa.py start backtracking/1`.

**More:** 90 Subsets II (M), 47 Permutations II (M), 77 Combinations (M), 40 Combination Sum II (M), 216 Combination Sum III (M), 17 Letter Combinations of a Phone Number (M), 79 Word Search (M), 131 Palindrome Partitioning (M), 93 Restore IP Addresses (M), 698 Partition to K Equal Sum Subsets (M), 37 Sudoku Solver (H).

## 9. Make it stay - the teacher's anchors

**Picture it.** Walking a maze with chalk: choose a corridor, mark it, explore; if it dead-ends, rub out the mark and go back to the last junction.

**The rule in one sentence.** choose -> explore -> UN-choose. The recursion tree is the search space; prune branches that cannot succeed.

**Why it works.** Undoing the choice restores the exact previous state, so siblings do not see each other's decisions. Pruning cuts whole subtrees before you explore them.

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. Draw the recursion tree for subsets of [1,2,3].
2. How do you avoid duplicates when the input has repeats?
3. Why do we copy `path` when we record a result?

**Mistakes students make most.**
- Appending `path` itself instead of `path[:]`.
- Forgetting to undo the choice.
- No pruning/sorting so duplicates explode.

**When NOT to use it.** Overlapping subproblems exist (the same state is reached many ways) - memoise it and you are doing DP.

**The same idea in disguise.** Subsets -> permutations -> combination sum -> parentheses -> word search -> N-Queens -> palindrome partitioning -> restore IP addresses.
