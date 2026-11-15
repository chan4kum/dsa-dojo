# 06 - Binary search (on indices *and* on answers)

> **One idea:** if a yes/no question flips from "no" to "yes" exactly once along an ordered range, you can find the flip in O(log n).

## 1. First principles
- Binary search is not about sorted arrays; it is about a **monotone predicate** `P(x)`: `False ... False True ... True`.
- Each probe at `mid` throws away half of the candidates. n = 10^9 needs about 30 probes.
- Two loop shapes - pick one and never mix them:
  - **Closed `[lo, hi]`, `while lo <= hi`**, moves `mid+1` / `mid-1` -> find an exact element.
  - **Half-open `[lo, hi)`/boundary, `while lo < hi`**, `hi = mid` or `lo = mid + 1` -> find the *first True* (lower bound).
- **Search on the answer:** the range is the set of possible answers; the predicate is a cheap feasibility check.

## 2. How to spot it
- Sorted (or rotated-sorted) input and O(log n) required.
- "minimise the maximum", "maximise the minimum", "smallest x such that ...", "minimum speed/capacity/time".
- You can write `feasible(x)` in O(n) and it is monotone in x.

## 3. Paper recipe
1. Define the predicate in one sentence and state its direction (`False..True` or `True..False`).
2. Fix the search range `[lo, hi]` so that the answer is **guaranteed inside** (lowest possible answer, highest possible answer).
3. Write the loop: if `P(mid)` then `hi = mid` (keep mid) else `lo = mid + 1`.
4. Test with arrays of size 1, 2 and a target that is first / last / absent.
5. Complexity = `log(range) x cost of feasible()`.

## 4. Hand traces
Exact search:

`a = [-1, 0, 3, 5, 9, 12]`, `target = 9`

| lo | hi | mid | a[mid] | decision |
|---|---|---|---|---|
| 0 | 5 | 2 | 3 | too small -> lo = mid + 1 |
| 3 | 5 | 4 | 9 | == target -> return mid |

Search on the answer (Koko Eating Bananas):

`piles = [3, 6, 7, 11]`, `h = 8`; predicate: *can she finish at speed `mid`?*

| lo | hi | mid | hours needed | hours <= h ? |
|---|---|---|---|---|
| 1 | 11 | 6 | 6 | yes -> hi = mid |
| 1 | 6 | 3 | 10 | no -> lo = mid + 1 |
| 4 | 6 | 5 | 8 | yes -> hi = mid |
| 4 | 5 | 4 | 8 | yes -> hi = mid |

Answer: **4**

## 5. Template
*Reference solution for **Koko Eating Bananas** (`binary_search/3`) - tested by `python dsa.py selftest`:*

```python
# OPTIMISED: O(n log max(piles)) time, O(1) space
# Idea: Binary search on the ANSWER (monotonic feasibility predicate)
def min_eating_speed(piles, h):
    def feasible(k):
        return sum(-(-p // k) for p in piles) <= h  # ceil(p / k) without floats

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid  # mid works: try smaller (keep mid)
        else:
            lo = mid + 1
    return lo
```

## 6. Traps
- `mid = (lo + hi) // 2` is safe in Python; in Java/C++ use `lo + (hi - lo) // 2`.
- `while lo < hi` with `lo = mid` (no +1) loops forever when `lo + 1 == hi`.
- Wrong direction of the predicate -> returns the *last* True or an off-by-one answer.
- Rotated arrays: first decide **which half is sorted**.
- Using `lo <= hi` with `hi = mid` (infinite loop).

## 7. Self-check
1. What is the predicate for "first bad version"? For "find peak element"?
2. Why is the Koko range `[1, max(piles)]` and not `[1, sum(piles)]`?
3. Write `lower_bound` (first index >= x) and `upper_bound` (first index > x) in two lines each.

## 8. Practice ladder
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `binary_search/1` | Easy | Binary Search | [#704](https://leetcode.com/problems/binary-search/) | Binary search on a sorted index range |
| `binary_search/6` | Easy | Search Insert Position | [#35](https://leetcode.com/problems/search-insert-position/) | Binary search for the lower bound (first index satisfying a monotone predicate) |
| `binary_search/9` | Easy | Sqrt(x) | [#69](https://leetcode.com/problems/sqrtx/) | Binary search on the ANSWER (monotone predicate over candidate values) |
| `binary_search/12` | Easy | Valid Perfect Square | [#367](https://leetcode.com/problems/valid-perfect-square/) | Binary search on the answer (monotone predicate r*r vs num) |
| `binary_search/16` | Easy | Find Smallest Letter Greater Than Target | [#744](https://leetcode.com/problems/find-smallest-letter-greater-than-target/) | Upper-bound binary search (first element strictly greater) |
| `binary_search/22` | Easy | Kth Missing Positive Number | [#1539](https://leetcode.com/problems/kth-missing-positive-number/) | Binary search on 'how many are missing so far' |
| `binary_search/23` | Easy | Arranging Coins | [#441](https://leetcode.com/problems/arranging-coins/) | Binary search on the answer |
| `binary_search/25` | Easy | Find the Distance Value Between Two Arrays | [#1385](https://leetcode.com/problems/find-the-distance-value-between-two-arrays/) | Range-emptiness test with binary search |
| `binary_search/40` | Easy | Special Array With X Elements Greater Than or Equal X | [#1608](https://leetcode.com/problems/special-array-with-x-elements-greater-than-or-equal-x/) | Sort + binary search on the answer x |
| `binary_search/2` | Medium | Search in Rotated Sorted Array | [#33](https://leetcode.com/problems/search-in-rotated-sorted-array/) | Binary search with 'which half is sorted?' reasoning |
| `binary_search/3` | Medium | Koko Eating Bananas | [#875](https://leetcode.com/problems/koko-eating-bananas/) | Binary search on the ANSWER (monotonic feasibility predicate) |
| `binary_search/7` | Medium | Find First and Last Position of Element in Sorted Array | [#34](https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/) | Two lower-bound searches (left edge, right edge) |
| `binary_search/8` | Medium | Find Minimum in Rotated Sorted Array | [#153](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/) | Binary search on a rotated array: compare mid with the right end |
| `binary_search/10` | Medium | Search a 2D Matrix | [#74](https://leetcode.com/problems/search-a-2d-matrix/) | Binary search over a virtual 1D index (index arithmetic) |
| `binary_search/11` | Medium | Find Peak Element | [#162](https://leetcode.com/problems/find-peak-element/) | Binary search on a 'slope' (guarantee exists on one side) |
| `binary_search/13` | Medium | Capacity To Ship Packages Within D Days | [#1011](https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/) | Binary search on the answer + greedy feasibility check |
| `binary_search/14` | Medium | Single Element in a Sorted Array | [#540](https://leetcode.com/problems/single-element-in-a-sorted-array/) | Binary search on a structural invariant (pair parity) |
| `binary_search/15` | Medium | Find K Closest Elements | [#658](https://leetcode.com/problems/find-k-closest-elements/) | Binary search for a window start (compare the two boundary elements) |
| `binary_search/17` | Medium | Search in Rotated Sorted Array II | [#81](https://leetcode.com/problems/search-in-rotated-sorted-array-ii/) | Binary search on a rotated array (one half is always sorted) |
| `binary_search/19` | Medium | Minimum Number of Days to Make m Bouquets | [#1482](https://leetcode.com/problems/minimum-number-of-days-to-make-m-bouquets/) | Binary search on the answer + a greedy feasibility check |
| `binary_search/20` | Medium | Peak Index in a Mountain Array | [#852](https://leetcode.com/problems/peak-index-in-a-mountain-array/) | Binary search on a slope (rising vs falling) |
| `binary_search/21` | Medium | Find the Smallest Divisor Given a Threshold | [#1283](https://leetcode.com/problems/find-the-smallest-divisor-given-a-threshold/) | Binary search on the answer (monotone predicate) |
| `binary_search/24` | Medium | Most Profit Assigning Work | [#826](https://leetcode.com/problems/most-profit-assigning-work/) | Sort + prefix maximum + binary search |
| `binary_search/26` | Medium | Minimum Limit of Balls in a Bag | [#1760](https://leetcode.com/problems/minimum-limit-of-balls-in-a-bag/) | Binary search on the answer with a feasibility check |
| `binary_search/27` | Medium | Minimum Speed to Arrive on Time | [#1870](https://leetcode.com/problems/minimum-speed-to-arrive-on-time/) | Binary search on the answer (rounding up per leg) |
| `binary_search/28` | Medium | Minimum Time to Complete Trips | [#2187](https://leetcode.com/problems/minimum-time-to-complete-trips/) | Binary search on the answer (time) |
| `binary_search/29` | Medium | Maximum Candies Allocated to K Children | [#2226](https://leetcode.com/problems/maximum-candies-allocated-to-k-children/) | Binary search on the answer (maximise a feasible value) |
| `binary_search/30` | Medium | Successful Pairs of Spells and Potions | [#2300](https://leetcode.com/problems/successful-pairs-of-spells-and-potions/) | Sort once + binary search per query |
| `binary_search/31` | Medium | Magnetic Force Between Two Balls | [#1552](https://leetcode.com/problems/magnetic-force-between-two-balls/) | Binary search on the answer + greedy placement check |
| `binary_search/34` | Medium | Minimum Time to Repair Cars | [#2594](https://leetcode.com/problems/minimum-time-to-repair-cars/) | Binary search on the answer (time) |
| `binary_search/35` | Medium | H-Index II | [#275](https://leetcode.com/problems/h-index-ii/) | Binary search on a monotone condition over the sorted array |
| `binary_search/38` | Medium | Ugly Number III | [#1201](https://leetcode.com/problems/ugly-number-iii/) | Binary search on the answer with a three-set inclusion-exclusion counter |
| `binary_search/39` | Medium | Sum of Mutated Array Closest to Target | [#1300](https://leetcode.com/problems/sum-of-mutated-array-closest-to-target/) | Binary search on a monotone sum, then compare the two neighbours |
| `binary_search/41` | Medium | Minimize Maximum of Array | [#2439](https://leetcode.com/problems/minimize-maximum-of-array/) | Prefix average lower bound (greedy / binary search on the answer) |
| `binary_search/42` | Medium | Maximum Tastiness of Candy Basket | [#2517](https://leetcode.com/problems/maximum-tastiness-of-candy-basket/) | Binary search on the answer + greedy feasibility check |
| `binary_search/43` | Medium | House Robber IV | [#2560](https://leetcode.com/problems/house-robber-iv/) | Binary search on the answer + greedy non-adjacent count |
| `binary_search/4` | Hard | Split Array Largest Sum | [#410](https://leetcode.com/problems/split-array-largest-sum/) | Binary search on the answer + greedy feasibility check |
| `binary_search/5` | Hard | Median of Two Sorted Arrays | [#4](https://leetcode.com/problems/median-of-two-sorted-arrays/) | Binary search on a partition point (not on values) |
| `binary_search/18` | Hard | Find Minimum in Rotated Sorted Array II | [#154](https://leetcode.com/problems/find-minimum-in-rotated-sorted-array-ii/) | Binary search against the right end, with a safe shrink on ties |
| `binary_search/32` | Hard | Find K-th Smallest Pair Distance | [#719](https://leetcode.com/problems/find-k-th-smallest-pair-distance/) | Binary search on the answer + two-pointer counting |
| `binary_search/33` | Hard | Kth Smallest Number in Multiplication Table | [#668](https://leetcode.com/problems/kth-smallest-number-in-multiplication-table/) | Binary search on the value with a counting function |
| `binary_search/36` | Hard | Preimage Size of Factorial Zeroes Function | [#793](https://leetcode.com/problems/preimage-size-of-factorial-zeroes-function/) | Binary search on a monotone function (lower bound twice) |
| `binary_search/37` | Hard | Nth Magical Number | [#878](https://leetcode.com/problems/nth-magical-number/) | Binary search on the answer with an inclusion-exclusion counter |

Start one with `python dsa.py start binary_search/1`.

**More:** 35 Search Insert Position (E), 34 Find First and Last Position of Element in Sorted Array (M), 153 Find Minimum in Rotated Sorted Array (M), 74 Search a 2D Matrix (M), 162 Find Peak Element (M), 69 Sqrt(x) (E), 1011 Capacity To Ship Packages Within D Days (M), 981 Time Based Key-Value Store (M), 378 Kth Smallest Element in a Sorted Matrix (M), 719 Find K-th Smallest Pair Distance (H).

## 9. Make it stay - the teacher's anchors

**Picture it.** The number-guessing game: 'higher or lower?' halves the range every time - 1,000,000 possibilities in 20 questions.

**The rule in one sentence.** If a yes/no predicate flips from False to True exactly once over an ordered range, binary search finds the flip in O(log n) - on an array OR on the answer itself.

**Why it works.** Each probe at mid rules out half the range because monotonicity guarantees what lies on each side. Always ask: 'what is my predicate, and is it monotone?'

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. Write the predicate for 'first index >= target'.
2. Why is `lo < hi` with `hi = mid` safe and `lo <= hi` with `hi = mid` an infinite loop?
3. How do you recognise 'binary search on the answer'?

**Mistakes students make most.**
- Infinite loops from wrong mid rounding (use upper mid when lo = mid).
- Off-by-one on bounds (half-open [lo, hi) is the most reliable).
- Binary searching a non-monotone predicate.

**When NOT to use it.** You cannot define a monotone predicate, or n is tiny and a linear scan is clearer.

**The same idea in disguise.** Search -> first/last position -> rotated array -> peak -> Koko/ship packages/split array (search the answer) -> median of two sorted arrays (search the partition).
