# 10 - Greedy

> **One idea:** make the locally best choice, and *prove* it never hurts the final answer.

## 1. First principles
- Greedy is DP where you can throw away all but one option at each step.
- It works when the problem has the **greedy-choice property** (some optimal solution contains the local best choice) and **optimal substructure**.
- Proof tools you can do in your head:
  - **Exchange argument:** take any optimal solution, swap in the greedy choice, show it is no worse.
  - **"Stays ahead":** show the greedy partial solution is always at least as good as any other at every step.
  - **Frontier/summary argument:** one number (farthest reach, current tank) captures all possibilities.
- If you can find a counter-example in 2 minutes with a tiny input, it is **not** greedy - use DP.

## 2. How to spot it
- "minimum number of ...", "maximum number of ... that fit", "is it possible to reach / complete".
- Sorting + one sweep solves it; or a running frontier (`farthest`, `tank`, `end`).
- Choices are *independent* once you pick an order.

## 3. Paper recipe
1. Try 3 small inputs by hand and guess a rule ("always take the earliest-finishing").
2. Attack the rule with an adversarial input (equal values, big then small, zeros).
3. Write the one-sentence proof (exchange / stays-ahead). No proof -> suspect DP.
4. Decide the sort key (if any) and the state variable(s) you carry.
5. Code the single pass; test empty / single / all-equal.

## 4. Hand trace
`nums = [2, 3, 1, 1, 4]` -> **True**

| i | nums[i] | farthest reach | note |
|---|---|---|---|
| 0 | 2 | 2 | ok |
| 1 | 3 | 4 | ok |
| 2 | 1 | 4 | ok |
| 3 | 1 | 4 | ok |
| 4 | 4 | 8 | ok |

`nums = [3, 2, 1, 0, 4]` -> **False**

| i | nums[i] | farthest reach | note |
|---|---|---|---|
| 0 | 3 | 3 | ok |
| 1 | 2 | 3 | ok |
| 2 | 1 | 3 | ok |
| 3 | 0 | 3 | ok |
| 4 | 4 | 3 | i > reach -> STUCK |

## 5. Template
*Reference solution for **Jump Game** (`greedy/1`) - tested by `python dsa.py selftest`:*

```python
# OPTIMISED: O(n) time, O(1) space
# Idea: Greedy: maintain the farthest reachable frontier
def can_jump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
    return True
```

## 6. Traps
- Assuming greedy works because it passes the samples (Coin Change with [1,3,4] and amount 6).
- Sorting by the wrong key.
- Missing the global feasibility check (Gas Station: total gas >= total cost).
- Ties: decide what to do when two choices look equal.

## 7. Self-check
1. Give a counter-example showing greedy fails for Coin Change with coins [1,3,4].
2. State the exchange argument for "sort intervals by end".
3. Which pattern in this repo is greedy + a heap? (Task Scheduler, Reorganize String, Meeting Rooms II.)

## 8. Practice ladder
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `greedy/6` | Easy | Assign Cookies | [#455](https://leetcode.com/problems/assign-cookies/) | Greedy matching after sorting (smallest sufficient) |
| `greedy/10` | Easy | Lemonade Change | [#860](https://leetcode.com/problems/lemonade-change/) | Greedy: spend the least flexible bill first |
| `greedy/14` | Easy | Maximize Sum Of Array After K Negations | [#1005](https://leetcode.com/problems/maximize-sum-of-array-after-k-negations/) | Greedy: spend each action on the best remaining gain |
| `greedy/15` | Easy | Largest Perimeter Triangle | [#976](https://leetcode.com/problems/largest-perimeter-triangle/) | Sort, then test neighbours in a greedy order |
| `greedy/16` | Easy | Array Partition | [#561](https://leetcode.com/problems/array-partition/) | Sort, then pair neighbours |
| `greedy/17` | Easy | Can Place Flowers | [#605](https://leetcode.com/problems/can-place-flowers/) | Greedy left-to-right placement |
| `greedy/19` | Easy | Split a String in Balanced Strings | [#1221](https://leetcode.com/problems/split-a-string-in-balanced-strings/) | Running balance / greedy cut at every zero |
| `greedy/23` | Easy | Maximum Units on a Truck | [#1710](https://leetcode.com/problems/maximum-units-on-a-truck/) | Greedy: fill the scarce resource with the best value per slot first |
| `greedy/24` | Easy | Minimum Operations to Make the Array Increasing | [#1827](https://leetcode.com/problems/minimum-operations-to-make-the-array-increasing/) | Greedy: raise each element by the minimum necessary, left to right |
| `greedy/28` | Easy | Minimum Subsequence in Non-Increasing Order | [#1403](https://leetcode.com/problems/minimum-subsequence-in-non-increasing-order/) | Greedy: take the largest values first until the target is beaten |
| `greedy/29` | Easy | Minimum Cost of Buying Candies With Discount | [#2144](https://leetcode.com/problems/minimum-cost-of-buying-candies-with-discount/) | Greedy: group the most expensive items together |
| `greedy/30` | Easy | Minimum Sum of Four Digit Number After Splitting Digits | [#2160](https://leetcode.com/problems/minimum-sum-of-four-digit-number-after-splitting-digits/) | Greedy: smallest digits get the biggest place values |
| `greedy/33` | Easy | Delete Columns to Make Sorted | [#944](https://leetcode.com/problems/delete-columns-to-make-sorted/) | Independent per-column check |
| `greedy/1` | Medium | Jump Game | [#55](https://leetcode.com/problems/jump-game/) | Greedy: maintain the farthest reachable frontier |
| `greedy/2` | Medium | Gas Station | [#134](https://leetcode.com/problems/gas-station/) | Greedy with a 'discard the failed prefix' argument |
| `greedy/3` | Medium | Partition Labels | [#763](https://leetcode.com/problems/partition-labels/) | Greedy interval extension using last occurrences |
| `greedy/4` | Medium | Best Time to Buy and Sell Stock II | [#122](https://leetcode.com/problems/best-time-to-buy-and-sell-stock-ii/) | Greedy: capture every local gain |
| `greedy/5` | Medium | Jump Game II | [#45](https://leetcode.com/problems/jump-game-ii/) | Greedy BFS over index ranges (implicit layers) |
| `greedy/7` | Medium | Hand of Straights | [#846](https://leetcode.com/problems/hand-of-straights/) | Greedy from the smallest + frequency map |
| `greedy/8` | Medium | Valid Parenthesis String | [#678](https://leetcode.com/problems/valid-parenthesis-string/) | Greedy with a range of possible states |
| `greedy/11` | Medium | Queue Reconstruction by Height | [#406](https://leetcode.com/problems/queue-reconstruction-by-height/) | Greedy insertion order (place the constraint-free ones first) |
| `greedy/12` | Medium | Wiggle Subsequence | [#376](https://leetcode.com/problems/wiggle-subsequence/) | Greedy: count direction changes (peaks and valleys) |
| `greedy/13` | Medium | Two City Scheduling | [#1029](https://leetcode.com/problems/two-city-scheduling/) | Greedy by difference (opportunity cost) |
| `greedy/18` | Medium | Boats to Save People | [#881](https://leetcode.com/problems/boats-to-save-people/) | Sort + two pointers (pair the heaviest with the lightest) |
| `greedy/20` | Medium | Monotone Increasing Digits | [#738](https://leetcode.com/problems/monotone-increasing-digits/) | Greedy: lower the first bad digit, then maximise the suffix |
| `greedy/21` | Medium | Max Chunks To Make Sorted | [#769](https://leetcode.com/problems/max-chunks-to-make-sorted/) | Greedy: cut as soon as the prefix is self-contained |
| `greedy/22` | Medium | Minimum Deletions to Make Character Frequencies Unique | [#1647](https://leetcode.com/problems/minimum-deletions-to-make-character-frequencies-unique/) | Greedy: sort frequencies, lower each to the highest unused value |
| `greedy/25` | Medium | Minimum Time to Make Rope Colorful | [#1578](https://leetcode.com/problems/minimum-time-to-make-rope-colorful/) | Greedy: in each group keep the most expensive item |
| `greedy/26` | Medium | Broken Calculator | [#991](https://leetcode.com/problems/broken-calculator/) | Greedy on the reversed process |
| `greedy/27` | Medium | Maximum Number of Coins You Can Get | [#1561](https://leetcode.com/problems/maximum-number-of-coins-you-can-get/) | Greedy after sorting: pair the best with the next best |
| `greedy/31` | Medium | Dota2 Senate | [#649](https://leetcode.com/problems/dota2-senate/) | Greedy with two queues (earliest voter bans) |
| `greedy/32` | Medium | Advantage Shuffle | [#870](https://leetcode.com/problems/advantage-shuffle/) | Sort both sides, match smallest winner to smallest target |
| `greedy/34` | Medium | String Without AAA or BBB | [#984](https://leetcode.com/problems/string-without-aaa-or-bbb/) | Greedy: spend the majority letter, obey the run limit |
| `greedy/35` | Medium | Previous Permutation With One Swap | [#1053](https://leetcode.com/problems/previous-permutation-with-one-swap/) | Greedy swap at the rightmost descent |
| `greedy/36` | Medium | Break a Palindrome | [#1328](https://leetcode.com/problems/break-a-palindrome/) | Greedy: earliest improvement, else smallest damage at the end |
| `greedy/37` | Medium | Max Difference You Can Get From Changing an Integer | [#1432](https://leetcode.com/problems/max-difference-you-can-get-from-changing-an-integer/) | Greedy on the most significant digit |
| `greedy/38` | Medium | Least Number of Unique Integers after K Removals | [#1481](https://leetcode.com/problems/least-number-of-unique-integers-after-k-removals/) | Greedy on frequencies: remove rarest values first |
| `greedy/39` | Medium | Smallest String With A Given Numeric Value | [#1663](https://leetcode.com/problems/smallest-string-with-a-given-numeric-value/) | Greedy: fill from the back |
| `greedy/40` | Medium | Partitioning Into Minimum Number Of Deci-Binary Numbers | [#1689](https://leetcode.com/problems/partitioning-into-minimum-number-of-deci-binary-numbers/) | Max digit (lower bound that is achievable) |
| `greedy/41` | Medium | Maximum Element After Decreasing and Rearranging | [#1846](https://leetcode.com/problems/maximum-element-after-decreasing-and-rearranging/) | Sort + greedy cap by the previous element |
| `greedy/42` | Medium | Merge Triplets to Form Target Triplet | [#1899](https://leetcode.com/problems/merge-triplets-to-form-target-triplet/) | Filter unusable items, then check coverage |
| `greedy/43` | Medium | Maximum Number of Weeks for Which You Can Work | [#1953](https://leetcode.com/problems/maximum-number-of-weeks-for-which-you-can-work/) | Largest pile vs everything else |
| `greedy/44` | Medium | Minimum Number of Swaps to Make the String Balanced | [#1963](https://leetcode.com/problems/minimum-number-of-swaps-to-make-the-string-balanced/) | Count unmatched closers; one swap fixes two |
| `greedy/45` | Medium | The Number of Weak Characters in the Game | [#1996](https://leetcode.com/problems/the-number-of-weak-characters-in-the-game/) | Sort one dimension, sweep the other |
| `greedy/46` | Medium | Remove Colored Pieces if Both Neighbors are the Same Color | [#2038](https://leetcode.com/problems/remove-colored-pieces-if-both-neighbors-are-the-same-color/) | Independent move counts decide a game |
| `greedy/47` | Medium | Destroying Asteroids | [#2126](https://leetcode.com/problems/destroying-asteroids/) | Sort ascending, grow as you go |
| `greedy/48` | Medium | Maximum Bags With Full Capacity of Rocks | [#2279](https://leetcode.com/problems/maximum-bags-with-full-capacity-of-rocks/) | Sort costs, take the cheapest first |
| `greedy/49` | Medium | Partition Array Such That Maximum Difference Is K | [#2294](https://leetcode.com/problems/partition-array-such-that-maximum-difference-is-k/) | Sort + greedy interval cover |
| `greedy/50` | Medium | Optimal Partition of String | [#2405](https://leetcode.com/problems/optimal-partition-of-string/) | Greedy: extend until a repeat forces a cut |
| `greedy/9` | Hard | Candy | [#135](https://leetcode.com/problems/candy/) | Two-pass greedy (satisfy left constraints, then right constraints) |

Start one with `python dsa.py start greedy/1`.

**More:** 455 Assign Cookies (E), 860 Lemonade Change (E), 45 Jump Game II (M), 1029 Two City Scheduling (M), 406 Queue Reconstruction by Height (M), 621 Task Scheduler (M), 135 Candy (H), 330 Patching Array (H), 767 Reorganize String (M), 402 Remove K Digits (M).

## 9. Make it stay - the teacher's anchors

**Picture it.** Always picking the cheapest checkout lane: great when your choice cannot hurt later choices, disastrous when it can (coin change with 1, 3, 4).

**The rule in one sentence.** Make the locally best choice ONLY IF you can prove it never hurts the future (exchange argument / stays-ahead).

**Why it works.** The proof is the algorithm: take any optimal solution, swap in the greedy choice, show it is no worse.

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. Give a counter-example where greedy fails (coin change).
2. State the exchange argument for 'sort by end time'.
3. What state do you carry in Jump Game?

**Mistakes students make most.**
- Believing the samples instead of attacking the idea with adversarial input.
- Sorting by the wrong key.
- Skipping the global feasibility check (Gas Station).

**When NOT to use it.** Choices interact (knapsack-like) - use DP. If you cannot say why greedy is safe in one sentence, it probably is not.

**The same idea in disguise.** Jump game -> gas station -> partition labels -> candy (two passes) -> task scheduler (heap + greedy) -> valid parenthesis string (range of states).
