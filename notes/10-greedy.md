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
| `greedy/20` | Easy | Assign Cookies | [#455](https://leetcode.com/problems/assign-cookies/) | Sort both sides and match greedily |
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
