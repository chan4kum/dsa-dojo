# 05 - Array tricks: Kadane, math/XOR invariants, in-place hashing

> **One idea:** use a property of the input (values live in 1..n, totals are known, pairs cancel) to avoid extra memory.

## 1. First principles
- **Kadane / "best ending here":** the best subarray ending at `i` either extends the best ending at `i-1` or restarts at `i`. One variable of state -> O(n), O(1).
- **Known universe:** if the values are exactly 0..n (one missing) the *sum* or *XOR* of what should be there minus what is there reveals the answer.
- **Cyclic sort / index = value-1:** when values are in `1..n`, the array itself can be the hash table: value `v` belongs at index `v-1`.

## 2. How to spot it
- "maximum sum **contiguous** subarray" -> Kadane.
- "values in the range 1..n", "find missing / duplicate", "O(1) extra space", "do not modify / may modify the array".
- A pairing structure ("every element twice except one") -> XOR.

## 3. Paper recipe
- **Kadane:** write `cur` and `best` columns next to the array; at each element ask "is carrying the past positive or negative?".
- **Cyclic placement:** for each `i`, while `a[i]` is in `1..n` and not at its home, swap it home. Draw the array after each swap.
- **Math:** write the expected total (e.g. `n(n+1)/2`) and the actual total; the difference is the answer.

## 4. Hand traces
Kadane:

`nums = [-2, 1, -3, 4, -1, 2, 1, -5, 4]`

| i | x | decision | best ending here | best overall |
|---|---|---|---|---|
| 0 | -2 | start | -2 | -2 |
| 1 | 1 | restart here | 1 | 1 |
| 2 | -3 | extend previous | -2 | 1 |
| 3 | 4 | restart here | 4 | 4 |
| 4 | -1 | extend previous | 3 | 4 |
| 5 | 2 | extend previous | 5 | 5 |
| 6 | 1 | extend previous | 6 | 6 |
| 7 | -5 | extend previous | 1 | 6 |
| 8 | 4 | extend previous | 5 | 6 |

Cyclic placement (First Missing Positive):

`nums = [3, 4, -1, 1]`; value v belongs at index v-1

| i | action | array after |
|---|---|---|
| 0 | swap positions 0 and 2 | [-1, 4, 3, 1] |
| 1 | swap positions 1 and 3 | [-1, 1, 3, 4] |
| 1 | swap positions 1 and 0 | [1, -1, 3, 4] |

Final scan: first index where `a[i] != i+1` is the answer -> **2**.

## 5. Template
*Reference solution for **First Missing Positive** (`array_tricks/3`) - tested by `python dsa.py selftest`:*

```python
# OPTIMISED: O(n) time, O(1) extra space (cyclic placement)
# Idea: Cyclic sort / in-place hashing (index = value - 1)
def first_missing_positive(nums):
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]  # send nums[i] to its home slot
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1
```

## 6. Traps
- Initialising Kadane with `0` instead of `nums[0]` (fails on all-negative input).
- Cyclic sort infinite loop when duplicates exist: always compare with the *destination* value (`a[a[i]-1] != a[i]`).
- Max-**product** subarray needs both a running max and min (a negative flips them).

## 7. Self-check
1. Why can the answer to First Missing Positive never exceed `n + 1`?
2. Modify Kadane to also return the subarray's start and end.
3. What is the circular-array variant (918) and how does "total - min subarray" help?

## 8. Practice ladder
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `array_tricks/2` | Easy | Missing Number | [#268](https://leetcode.com/problems/missing-number/) | Math / XOR cancellation (range is known, so use the invariant) |
| `array_tricks/5` | Easy | Majority Element | [#169](https://leetcode.com/problems/majority-element/) | Boyer-Moore voting (cancellation argument) |
| `array_tricks/10` | Easy | Find All Numbers Disappeared in an Array | [#448](https://leetcode.com/problems/find-all-numbers-disappeared-in-an-array/) | Index as hash: mark visited by negating in place |
| `array_tricks/11` | Easy | Max Consecutive Ones | [#485](https://leetcode.com/problems/max-consecutive-ones/) | Running streak counter |
| `array_tricks/12` | Easy | Pascal's Triangle | [#118](https://leetcode.com/problems/pascals-triangle/) | Build each row from the previous row |
| `array_tricks/13` | Easy | Pascal's Triangle II | [#119](https://leetcode.com/problems/pascals-triangle-ii/) | In-place DP row update (iterate backwards) |
| `array_tricks/14` | Easy | Third Maximum Number | [#414](https://leetcode.com/problems/third-maximum-number/) | Track the top-k with k variables |
| `array_tricks/15` | Easy | Maximum Product of Three Numbers | [#628](https://leetcode.com/problems/maximum-product-of-three-numbers/) | Consider both ends of the sorted order (negatives flip signs) |
| `array_tricks/1` | Medium | Maximum Subarray | [#53](https://leetcode.com/problems/maximum-subarray/) | Kadane's algorithm (1-D DP: best subarray ending here) |
| `array_tricks/4` | Medium | Maximum Product Subarray | [#152](https://leetcode.com/problems/maximum-product-subarray/) | Kadane variant tracking both max and min (negatives flip order) |
| `array_tricks/6` | Medium | Rotate Array | [#189](https://leetcode.com/problems/rotate-array/) | Triple reversal trick |
| `array_tricks/7` | Medium | Find All Duplicates in an Array | [#442](https://leetcode.com/problems/find-all-duplicates-in-an-array/) | Index-as-hash (sign marking) when values are in [1, n] |
| `array_tricks/8` | Medium | Next Permutation | [#31](https://leetcode.com/problems/next-permutation/) | Find the pivot, swap, reverse the suffix |
| `array_tricks/9` | Medium | Majority Element II | [#229](https://leetcode.com/problems/majority-element-ii/) | Boyer-Moore voting with two candidates |
| `array_tricks/16` | Medium | Non-decreasing Array | [#665](https://leetcode.com/problems/non-decreasing-array/) | One-pass greedy with a single allowed repair |
| `array_tricks/3` | Hard | First Missing Positive | [#41](https://leetcode.com/problems/first-missing-positive/) | Cyclic sort / in-place hashing (index = value - 1) |

Start one with `python dsa.py start array_tricks/1`.

**More:** 121 Best Time to Buy and Sell Stock (E), 152 Maximum Product Subarray (M), 918 Maximum Sum Circular Subarray (M), 442 Find All Duplicates (M), 448 Find All Numbers Disappeared (E), 287 Find the Duplicate Number (M), 645 Set Mismatch (E), 169 Majority Element (E, Boyer-Moore), 189 Rotate Array (M).

## 9. Make it stay - the teacher's anchors

**Picture it.** Kadane: walking along a road with a running balance. If your balance goes negative, you would be better off starting fresh from the next town.

**The rule in one sentence.** Ask 'what is the best answer ENDING at index i?' - often it depends only on the best ending at i-1.

**Why it works.** An optimal subarray never needs a negative-sum prefix (cut it and you do better), so a running total that goes below zero can be discarded.

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. Explain Kadane in one sentence without code.
2. Why must Maximum Product Subarray track a minimum too?
3. How can the input array itself act as a hash table when values lie in [1, n]?

**Mistakes students make most.**
- Initialising the best to 0 (breaks all-negative arrays).
- Forgetting that a negative flips max and min.
- Cyclic sort: advancing i after a swap instead of re-checking the swapped-in value.

**When NOT to use it.** The best subarray must have a fixed length or a constraint on sum - use a window/prefix sums instead.

**The same idea in disguise.** Max subarray -> max product -> best time to buy/sell (running min) -> circular subarray -> house robber (best ending at i with a skip).
