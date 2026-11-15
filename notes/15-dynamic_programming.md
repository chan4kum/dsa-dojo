# 15 - Dynamic programming

> **One idea:** if a problem splits into overlapping subproblems, solve each subproblem **once**, remember the answer, and build up.

## 1. First principles
- DP = **recursion + memory**. Brute-force recursion explodes because the same subproblem is solved again and again; caching (memoisation, top-down) or filling a table (tabulation, bottom-up) removes the repeats.
- Two ingredients: **optimal substructure** (the best answer is built from best answers of smaller problems) and **overlapping subproblems**.
- The five-step recipe (use it every time, on paper):
  1. **State** - what do the arguments of the recursive function mean? (`dp[i]` = best for the first i items ...)
  2. **Choice / transition** - what was the *last* decision? Express `dp[state]` via smaller states.
  3. **Base cases.**
  4. **Order** of evaluation (smaller to larger; make sure dependencies come first).
  5. **Answer** cell, then shrink memory (rolling rows/variables) if possible.
- Greedy vs DP: if a local choice may need to be reconsidered, you need DP.

## 2. The families (and what the state looks like)
| Family | State | Recurrence flavour | Examples |
|---|---|---|---|
| 1-D linear | `dp[i]` best up to i | `dp[i] = f(dp[i-1], dp[i-2], ...)` | Climbing Stairs, House Robber, Word Break |
| Knapsack 0/1 | `dp[cap]` (loop caps **downwards**) | take / skip | Partition Equal Subset Sum, Target Sum |
| Unbounded knapsack | `dp[amount]` (loop upwards) | reuse items | Coin Change, Perfect Squares |
| Two sequences | `dp[i][j]` prefixes of A and B | match -> diagonal, else up/left | LCS, Edit Distance, Distinct Subsequences |
| LIS-type | `dp[i]` ending at i (or patience tails) | `max(dp[j]) + 1` | LIS, Russian Doll Envelopes |
| Grid | `dp[r][c]` | from up / left | Unique Paths, Min Path Sum, Maximal Square |
| Interval | `dp[l][r]` | split at k (often "the LAST one") | Burst Balloons, Palindrome Partitioning II |
| State machine | `dp[i][state]` | transitions between states | Stock with cooldown / k transactions |
| Bitmask | `dp[mask][last]` | add one more item | TSP, Shortest Superstring |
| Tree | value returned up per node | combine children | House Robber III, Binary Tree Cameras |
| Digit | `dp[pos][tight][...]` | enumerate digits | Count numbers with property <= N |

## 3. How to spot it
- "count the number of ways", "minimum/maximum cost/length", "is it possible", **and** choices at every step with a repeating structure.
- A greedy idea has an easy counter-example.
- Brute force is a recursion where the arguments (index, remaining capacity ...) repeat.

## 4. Paper recipe
1. Write the brute-force recursion first (even if exponential).
2. Circle the arguments that change - that is your **state**. Everything else is constant.
3. Fill the table **by hand** for a tiny input (see the two traces below). If you can fill it by hand, you can code it.
4. Draw arrows showing which cells each cell depends on -> that fixes the loop order.
5. Convert recursion to a loop, then try to keep only the last row/variables.

## 5. Hand traces
Coin Change (1-D, unbounded):

`coins = [1, 2, 5]`, `amount = 11`

| amount a | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| dp[a] (fewest coins) | 0 | 1 | 1 | 2 | 2 | 1 | 2 | 2 | 3 | 3 | 2 | 3 |
| last coin used | - | 1 | 2 | 1 | 2 | 5 | 1 | 2 | 1 | 2 | 5 | 1 |

Read it back: dp[11] = 3. Follow 'last coin used' from 11 downwards: 1 then 5 then 5 -> coins [5, 5, 1].

Longest Common Subsequence (2-D, two sequences):

`text1 = "abcde"` (rows), `text2 = "ace"` (columns)

|  | '' | a | c | e |
|---|---|---|---|---|
|  (i=0) | 0 | 0 | 0 | 0 |
| a (i=1) | 0 | 1 | 1 | 1 |
| b (i=2) | 0 | 1 | 1 | 1 |
| c (i=3) | 0 | 1 | 2 | 2 |
| d (i=4) | 0 | 1 | 2 | 2 |
| e (i=5) | 0 | 1 | 2 | 3 |

Match -> take the diagonal + 1; otherwise the max of up / left. Answer is the bottom-right cell.

## 6. Template
*Reference solution for **Coin Change** (`dynamic_programming/3`) - tested by `python dsa.py selftest`:*

```python
# OPTIMISED: O(amount * coins) time, O(amount) space
# Idea: Unbounded knapsack / DP over amount (min coins)
def coin_change(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return -1 if dp[amount] == INF else dp[amount]
```

Top-down version of any DP: `@lru_cache(None) def go(state): ...` - write this first if bottom-up order is not obvious.

## 7. Traps
- Wrong base case (empty string, amount 0, `dp[0] = True`).
- Knapsack loop direction: **0/1 -> capacity descending, unbounded -> ascending**.
- Counting combinations vs permutations: *items outer, amount inner* counts combinations.
- Using `INF` and then adding to it (`INF + 1` is fine in Python; use a sentinel in other languages).
- Mutable default / shared rows when building 2-D tables: `[[0]*n for _ in range(m)]`, not `[[0]*n]*m`.
- Memory: 2-D tables of 10^4 x 10^4 will not fit.

## 8. Self-check
1. Write the recurrence for Edit Distance and say what each of the three transitions means.
2. Why does the 0/1 knapsack loop run downwards?
3. What changes in the Coin Change table when you want the **number of ways** instead of the minimum?
4. How does patience sorting get LIS down to O(n log n)?

## 9. Practice ladder
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `dynamic_programming/1` | Easy | Climbing Stairs | [#70](https://leetcode.com/problems/climbing-stairs/) | 1-D DP: state = position, transition from the previous 1-2 states (Fibonacci shape) |
| `dynamic_programming/10` | Easy | Min Cost Climbing Stairs | [#746](https://leetcode.com/problems/min-cost-climbing-stairs/) | 1-D DP: state = position, transition = last 1 or 2 steps |
| `dynamic_programming/44` | Easy | Is Subsequence | [#392](https://leetcode.com/problems/is-subsequence/) | Two pointers (greedy matching) |
| `dynamic_programming/52` | Easy | Fibonacci Number | [#509](https://leetcode.com/problems/fibonacci-number/) | Bottom-up DP with O(1) space (the 'hello world' of DP) |
| `dynamic_programming/53` | Easy | N-th Tribonacci Number | [#1137](https://leetcode.com/problems/n-th-tribonacci-number/) | Rolling-window DP (keep only the last k states) |
| `dynamic_programming/2` | Medium | House Robber | [#198](https://leetcode.com/problems/house-robber/) | 1-D DP with a take/skip decision at each element |
| `dynamic_programming/3` | Medium | Coin Change | [#322](https://leetcode.com/problems/coin-change/) | Unbounded knapsack / DP over amount (min coins) |
| `dynamic_programming/4` | Medium | Longest Increasing Subsequence | [#300](https://leetcode.com/problems/longest-increasing-subsequence/) | DP -> patience sorting with binary search (tails array) |
| `dynamic_programming/5` | Medium | Longest Common Subsequence | [#1143](https://leetcode.com/problems/longest-common-subsequence/) | 2-D DP on two sequences (prefix pairs) |
| `dynamic_programming/6` | Medium | Edit Distance | [#72](https://leetcode.com/problems/edit-distance/) | 2-D DP on two strings (edit operations as transitions) |
| `dynamic_programming/7` | Medium | Partition Equal Subset Sum | [#416](https://leetcode.com/problems/partition-equal-subset-sum/) | 0/1 knapsack (subset sum) - iterate the capacity BACKWARDS |
| `dynamic_programming/8` | Medium | Word Break | [#139](https://leetcode.com/problems/word-break/) | 1-D DP over prefixes with a lookup inside (partition DP) |
| `dynamic_programming/11` | Medium | House Robber II | [#213](https://leetcode.com/problems/house-robber-ii/) | Reduce a circular structure to two linear cases |
| `dynamic_programming/12` | Medium | Unique Paths | [#62](https://leetcode.com/problems/unique-paths/) | 2-D grid DP (count paths = sum of the two predecessors) |
| `dynamic_programming/13` | Medium | Minimum Path Sum | [#64](https://leetcode.com/problems/minimum-path-sum/) | 2-D grid DP (min over predecessors) |
| `dynamic_programming/14` | Medium | Longest Palindromic Substring | [#5](https://leetcode.com/problems/longest-palindromic-substring/) | Expand around the centre |
| `dynamic_programming/15` | Medium | Palindromic Substrings | [#647](https://leetcode.com/problems/palindromic-substrings/) | Expand around the centre (count instead of maximise) |
| `dynamic_programming/16` | Medium | Decode Ways | [#91](https://leetcode.com/problems/decode-ways/) | 1-D DP: count ways with 1- and 2-step transitions plus validity |
| `dynamic_programming/17` | Medium | Perfect Squares | [#279](https://leetcode.com/problems/perfect-squares/) | Unbounded knapsack / coin change (min coins) |
| `dynamic_programming/18` | Medium | Combination Sum IV | [#377](https://leetcode.com/problems/combination-sum-iv/) | Counting DP - loop order decides combinations vs permutations |
| `dynamic_programming/19` | Medium | Target Sum | [#494](https://leetcode.com/problems/target-sum/) | Reduce to 'count subsets with sum S' (0/1 knapsack) |
| `dynamic_programming/20` | Medium | Best Time to Buy and Sell Stock with Cooldown | [#309](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/) | State-machine DP (a few states, transitions per day) |
| `dynamic_programming/21` | Medium | Triangle | [#120](https://leetcode.com/problems/triangle/) | Bottom-up DP with a rolling 1-D array |
| `dynamic_programming/22` | Medium | Longest Palindromic Subsequence | [#516](https://leetcode.com/problems/longest-palindromic-subsequence/) | Interval DP / reduce to LCS with the reversed string |
| `dynamic_programming/24` | Medium | Coin Change II | [#518](https://leetcode.com/problems/coin-change-ii/) | Unbounded knapsack - counting combinations (coin loop outside) |
| `dynamic_programming/25` | Medium | Min Falling Path Sum | [#931](https://leetcode.com/problems/minimum-falling-path-sum/) | Grid DP: best(r, c) = cell + min of the 3 cells above |
| `dynamic_programming/26` | Medium | Maximal Square | [#221](https://leetcode.com/problems/maximal-square/) | Grid DP: biggest square ending at a cell = 1 + min of 3 neighbours |
| `dynamic_programming/27` | Medium | Delete and Earn | [#740](https://leetcode.com/problems/delete-and-earn/) | Reduce to House Robber (adjacent values are 'adjacent houses') |
| `dynamic_programming/28` | Medium | Interleaving String | [#97](https://leetcode.com/problems/interleaving-string/) | 2-D DP over (chars used of s1, chars used of s2) |
| `dynamic_programming/29` | Medium | Unique Paths II | [#63](https://leetcode.com/problems/unique-paths-ii/) | Grid DP: paths into a cell = paths from above + paths from left |
| `dynamic_programming/30` | Medium | Minimum Cost For Tickets | [#983](https://leetcode.com/problems/minimum-cost-for-tickets/) | Timeline DP: cheapest to cover day d = min over last pass type |
| `dynamic_programming/31` | Medium | Longest String Chain | [#1048](https://leetcode.com/problems/longest-string-chain/) | DP over a DAG ordered by length, predecessors found by deleting a letter |
| `dynamic_programming/34` | Medium | Number of Longest Increasing Subsequence | [#673](https://leetcode.com/problems/number-of-longest-increasing-subsequence/) | LIS DP with a counter next to the length |
| `dynamic_programming/35` | Medium | Ones and Zeroes | [#474](https://leetcode.com/problems/ones-and-zeroes/) | 0/1 knapsack with two capacities (iterate capacities downwards) |
| `dynamic_programming/37` | Medium | Best Time to Buy and Sell Stock with Transaction Fee | [#714](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-transaction-fee/) | Two-state DP (hold / cash); fee charged on sell |
| `dynamic_programming/38` | Medium | Integer Break | [#343](https://leetcode.com/problems/integer-break/) | DP first, then spot the math pattern (split into 3s) |
| `dynamic_programming/39` | Medium | Arithmetic Slices | [#413](https://leetcode.com/problems/arithmetic-slices/) | Count subarrays by the number ending at each index (1-D DP) |
| `dynamic_programming/40` | Medium | Predict the Winner | [#486](https://leetcode.com/problems/predict-the-winner/) | Interval DP on a score difference (minimax) |
| `dynamic_programming/41` | Medium | Delete Operation for Two Strings | [#583](https://leetcode.com/problems/delete-operation-for-two-strings/) | Reduce to Longest Common Subsequence |
| `dynamic_programming/42` | Medium | Maximum Length of Repeated Subarray | [#718](https://leetcode.com/problems/maximum-length-of-repeated-subarray/) | 2-D DP where a mismatch resets to 0 (longest common substring) |
| `dynamic_programming/43` | Medium | Stone Game | [#877](https://leetcode.com/problems/stone-game/) | Interval DP, then a parity / strategy-stealing insight |
| `dynamic_programming/45` | Medium | Uncrossed Lines | [#1035](https://leetcode.com/problems/uncrossed-lines/) | Disguised Longest Common Subsequence |
| `dynamic_programming/47` | Medium | Number of Dice Rolls With Target Sum | [#1155](https://leetcode.com/problems/number-of-dice-rolls-with-target-sum/) | Counting DP over (items used, sum reached) |
| `dynamic_programming/54` | Medium | Domino and Tromino Tiling | [#790](https://leetcode.com/problems/domino-and-tromino-tiling/) | Derive a linear recurrence from the boundary structure |
| `dynamic_programming/55` | Medium | Partition Array for Maximum Sum | [#1043](https://leetcode.com/problems/partition-array-for-maximum-sum/) | Partition DP: choose the length of the last block |
| `dynamic_programming/56` | Medium | Longest Arithmetic Subsequence of Given Difference | [#1218](https://leetcode.com/problems/longest-arithmetic-subsequence-of-given-difference/) | DP keyed by value (hash map instead of an inner loop) |
| `dynamic_programming/57` | Medium | Longest Arithmetic Subsequence | [#1027](https://leetcode.com/problems/longest-arithmetic-subsequence/) | DP over (index, common difference) |
| `dynamic_programming/58` | Medium | Greatest Sum Divisible by Three | [#1262](https://leetcode.com/problems/greatest-sum-divisible-by-three/) | DP over remainders (a tiny state space) |
| `dynamic_programming/59` | Medium | Ugly Number II | [#264](https://leetcode.com/problems/ugly-number-ii/) | Merge three sorted streams with pointers (DP) |
| `dynamic_programming/60` | Medium | Count Numbers with Unique Digits | [#357](https://leetcode.com/problems/count-numbers-with-unique-digits/) | Counting with decreasing choices (permutation counting) |
| `dynamic_programming/61` | Medium | Out of Boundary Paths | [#576](https://leetcode.com/problems/out-of-boundary-paths/) | Grid DP over (cell, remaining moves) |
| `dynamic_programming/9` | Hard | Burst Balloons | [#312](https://leetcode.com/problems/burst-balloons/) | Interval DP: split an interval on the LAST action |
| `dynamic_programming/23` | Hard | Regular Expression Matching | [#10](https://leetcode.com/problems/regular-expression-matching/) | 2-D DP on two string positions (with branching for '*') |
| `dynamic_programming/32` | Hard | Russian Doll Envelopes | [#354](https://leetcode.com/problems/russian-doll-envelopes/) | Sort one dimension, then LIS on the other (patience sorting) |
| `dynamic_programming/33` | Hard | Distinct Subsequences | [#115](https://leetcode.com/problems/distinct-subsequences/) | 2-D string DP: use the matching character or skip it |
| `dynamic_programming/36` | Hard | Best Time to Buy and Sell Stock IV | [#188](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/) | State-machine DP: (transactions used, holding or not) |
| `dynamic_programming/46` | Hard | Minimum Insertion Steps to Make a String Palindrome | [#1312](https://leetcode.com/problems/minimum-insertion-steps-to-make-a-string-palindrome/) | Longest Palindromic Subsequence via LCS with the reverse |
| `dynamic_programming/48` | Hard | Dungeon Game | [#174](https://leetcode.com/problems/dungeon-game/) | Backward DP (compute requirements from the goal) |
| `dynamic_programming/49` | Hard | Longest Valid Parentheses | [#32](https://leetcode.com/problems/longest-valid-parentheses/) | Stack of indices as 'last unmatched position' markers |
| `dynamic_programming/50` | Hard | Wildcard Matching | [#44](https://leetcode.com/problems/wildcard-matching/) | 2-D string-matching DP (the simpler cousin of Regular Expression Matching) |
| `dynamic_programming/51` | Hard | Best Time to Buy and Sell Stock III | [#123](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iii/) | State-machine DP (one variable per stage of the process) |

Start one with `python dsa.py start dynamic_programming/1`.

**More:** 509 Fibonacci (E), 746 Min Cost Climbing Stairs (E), 213 House Robber II (M), 53 Maximum Subarray (M), 152 Maximum Product Subarray (M), 518 Coin Change II (M), 494 Target Sum (M), 62 Unique Paths (M), 64 Minimum Path Sum (M), 221 Maximal Square (M), 91 Decode Ways (M), 5 Longest Palindromic Substring (M), 516 Longest Palindromic Subsequence (M), 309 Best Time to Buy and Sell Stock with Cooldown (M), 188 Best Time to Buy and Sell Stock IV (H), 97 Interleaving String (M), 115 Distinct Subsequences (H), 10 Regular Expression Matching (H), 44 Wildcard Matching (H), 354 Russian Doll Envelopes (H), 1235 Maximum Profit in Job Scheduling (H), 943 Find the Shortest Superstring (H), 968 Binary Tree Cameras (H).

## 9. Make it stay - the teacher's anchors

**Picture it.** A staircase of answers: you do not climb the whole tower from scratch each time - you write the answer for each step on the wall and read it back.

**The rule in one sentence.** Define the STATE in one sentence ('dp[i] = best answer for the first i items'), write the TRANSITION from smaller states, set the BASE cases, then pick the evaluation order.

**Why it works.** DP = recursion + memory. If the same sub-question is asked many times, answering it once and caching it turns exponential into polynomial.

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. State the dp meaning for LIS, LCS, Edit Distance, Coin Change - each in one sentence.
2. How do you turn a top-down memo into a bottom-up table, and then shrink the table?
3. Combinations vs permutations: which loop goes outside?

**Mistakes students make most.**
- A vague state definition ('dp[i] is the answer') - write exactly what i means.
- Wrong base cases / indexing offsets.
- Reaching for DP when greedy is provable (or vice versa).

**When NOT to use it.** Subproblems do not overlap (plain divide and conquer) or a simple greedy proof exists.

**The same idea in disguise.** Climbing stairs -> robber -> coin change -> LIS -> knapsack (partition, target sum) -> grid paths -> LCS/edit distance -> intervals (burst balloons) -> state machines (stocks with cooldown) -> regex.
