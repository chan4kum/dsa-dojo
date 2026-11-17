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
# OPTIMISED: O(n * 2^n) time
# Idea: Backtracking: include/exclude decision tree (choose -> explore -> un-choose)
def subsets(nums):
    res, path = [], []

    def go(i):
        if i == len(nums):
            res.append(path[:])  # copy!
            return
        path.append(nums[i])  # choose
        go(i + 1)
        path.pop()  # un-choose
        go(i + 1)  # skip nums[i]

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
| `backtracking/34` | Easy | Binary Watch | [#401](https://leetcode.com/problems/binary-watch/) | Choose k of n positions (combinations), then validate |
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
| `backtracking/14` | Medium | Combination Sum III | [#216](https://leetcode.com/problems/combination-sum-iii/) | Backtracking with increasing start index and pruning |
| `backtracking/15` | Medium | Letter Case Permutation | [#784](https://leetcode.com/problems/letter-case-permutation/) | Binary decision per position (subset-style backtracking) |
| `backtracking/16` | Medium | Beautiful Arrangement | [#526](https://leetcode.com/problems/beautiful-arrangement/) | Backtracking with constraint pruning (permutation search) |
| `backtracking/17` | Medium | Partition to K Equal Sum Subsets | [#698](https://leetcode.com/problems/partition-to-k-equal-sum-subsets/) | Backtracking on bucket assignment with symmetry pruning |
| `backtracking/18` | Medium | Letter Tile Possibilities | [#1079](https://leetcode.com/problems/letter-tile-possibilities/) | Backtracking over a frequency table (no duplicates by construction) |
| `backtracking/19` | Medium | Non-decreasing Subsequences | [#491](https://leetcode.com/problems/non-decreasing-subsequences/) | Backtracking with a per-level 'used' set to skip duplicates |
| `backtracking/24` | Medium | Matchsticks to Square | [#473](https://leetcode.com/problems/matchsticks-to-square/) | Backtracking: assign each item to a bucket with pruning |
| `backtracking/25` | Medium | Numbers With Same Consecutive Differences | [#967](https://leetcode.com/problems/numbers-with-same-consecutive-differences/) | Backtracking: extend only with the digits that keep the constraint true |
| `backtracking/26` | Medium | Path with Maximum Gold | [#1219](https://leetcode.com/problems/path-with-maximum-gold/) | Grid backtracking: mark, explore, un-mark |
| `backtracking/27` | Medium | The k-th Lexicographical String of All Happy Strings of Length n | [#1415](https://leetcode.com/problems/the-k-th-lexicographical-string-of-all-happy-strings-of-length-n/) | Counting subtrees to skip branches (backtracking without enumerating) |
| `backtracking/28` | Medium | Maximum Length of a Concatenated String with Unique Characters | [#1239](https://leetcode.com/problems/maximum-length-of-a-concatenated-string-with-unique-characters/) | Subset search with bitmask conflict checks |
| `backtracking/30` | Medium | Split a String Into the Max Number of Unique Substrings | [#1593](https://leetcode.com/problems/split-a-string-into-the-max-number-of-unique-substrings/) | Backtracking over cut points with a 'used' set and a bound |
| `backtracking/31` | Medium | Gray Code | [#89](https://leetcode.com/problems/gray-code/) | Backtracking over a hypercube (or the reflected binary formula) |
| `backtracking/32` | Medium | Additive Number | [#306](https://leetcode.com/problems/additive-number/) | Choose the seed (first two parts), then verify deterministically |
| `backtracking/36` | Medium | Pyramid Transition Matrix | [#756](https://leetcode.com/problems/pyramid-transition-matrix/) | Backtracking row by row (with memoisation) |
| `backtracking/37` | Medium | Split Array into Fibonacci Sequence | [#842](https://leetcode.com/problems/split-array-into-fibonacci-sequence/) | Backtracking with pruning (prefix choices + forced sums) |
| `backtracking/40` | Medium | Splitting a String Into Descending Consecutive Values | [#1849](https://leetcode.com/problems/splitting-a-string-into-descending-consecutive-values/) | Backtracking on prefix choices with a forced next value |
| `backtracking/41` | Medium | Find Unique Binary String | [#1980](https://leetcode.com/problems/find-unique-binary-string/) | Backtracking/enumeration vs the diagonal argument |
| `backtracking/42` | Medium | Count Number of Maximum Bitwise-OR Subsets | [#2044](https://leetcode.com/problems/count-number-of-maximum-bitwise-or-subsets/) | Include / exclude backtracking carrying a running aggregate |
| `backtracking/43` | Medium | Next Greater Numerically Balanced Number | [#2048](https://leetcode.com/problems/next-greater-numerically-balanced-number/) | Enumerate all candidates (subset of digits + permutations), then binary search |
| `backtracking/45` | Medium | Fair Distribution of Cookies | [#2305](https://leetcode.com/problems/fair-distribution-of-cookies/) | Backtracking assignment with pruning (symmetry + bound) |
| `backtracking/46` | Medium | Maximum Rows Covered by Columns | [#2397](https://leetcode.com/problems/maximum-rows-covered-by-columns/) | Enumerate column subsets (bitmask) with a cheap subset test |
| `backtracking/47` | Medium | Generate Binary Strings Without Adjacent Zeros | [#3211](https://leetcode.com/problems/generate-binary-strings-without-adjacent-zeros/) | Backtracking that prunes invalid prefixes |
| `backtracking/5` | Hard | N-Queens | [#51](https://leetcode.com/problems/n-queens/) | Backtracking with O(1) conflict checks via sets (columns, diagonals) |
| `backtracking/20` | Hard | N-Queens II | [#52](https://leetcode.com/problems/n-queens-ii/) | Backtracking with O(1) conflict checks via sets |
| `backtracking/21` | Hard | Word Break II | [#140](https://leetcode.com/problems/word-break-ii/) | Backtracking over cut points + memoisation of suffix results |
| `backtracking/22` | Hard | Expression Add Operators | [#282](https://leetcode.com/problems/expression-add-operators/) | Backtracking with a running value and the last term (to handle * precedence) |
| `backtracking/23` | Hard | Remove Invalid Parentheses | [#301](https://leetcode.com/problems/remove-invalid-parentheses/) | Backtracking with a precomputed removal budget and pruning |
| `backtracking/29` | Hard | Unique Paths III | [#980](https://leetcode.com/problems/unique-paths-iii/) | Hamiltonian-style path counting by backtracking |
| `backtracking/33` | Hard | Reconstruct Itinerary | [#332](https://leetcode.com/problems/reconstruct-itinerary/) | Eulerian path (Hierholzer) / backtracking over tickets |
| `backtracking/35` | Hard | 24 Game | [#679](https://leetcode.com/problems/24-game/) | Backtracking over pairwise combinations |
| `backtracking/38` | Hard | Number of Squareful Arrays | [#996](https://leetcode.com/problems/number-of-squareful-arrays/) | Backtracking over multiset permutations with a validity filter |
| `backtracking/39` | Hard | Maximum Score Words Formed by Letters | [#1255](https://leetcode.com/problems/maximum-score-words-formed-by-letters/) | Include / exclude backtracking with a resource counter |
| `backtracking/44` | Hard | Maximum Good People Based on Statements | [#2151](https://leetcode.com/problems/maximum-good-people-based-on-statements/) | Subset enumeration / backtracking with consistency pruning |

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
