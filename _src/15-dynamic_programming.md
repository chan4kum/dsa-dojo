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

{{trace:coin_dp}}

Longest Common Subsequence (2-D, two sequences):

{{trace:lcs_dp}}

## 6. Template
{{solution:dynamic_programming/3}}

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
{{ladder}}

**More:** 509 Fibonacci (E), 746 Min Cost Climbing Stairs (E), 213 House Robber II (M), 53 Maximum Subarray (M), 152 Maximum Product Subarray (M), 518 Coin Change II (M), 494 Target Sum (M), 62 Unique Paths (M), 64 Minimum Path Sum (M), 221 Maximal Square (M), 91 Decode Ways (M), 5 Longest Palindromic Substring (M), 516 Longest Palindromic Subsequence (M), 309 Best Time to Buy and Sell Stock with Cooldown (M), 188 Best Time to Buy and Sell Stock IV (H), 97 Interleaving String (M), 115 Distinct Subsequences (H), 10 Regular Expression Matching (H), 44 Wildcard Matching (H), 354 Russian Doll Envelopes (H), 1235 Maximum Profit in Job Scheduling (H), 943 Find the Shortest Superstring (H), 968 Binary Tree Cameras (H).
