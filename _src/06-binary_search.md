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

{{trace:binary_search}}

Search on the answer (Koko Eating Bananas):

{{trace:koko}}

## 5. Template
{{solution:binary_search/3}}

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
{{ladder}}

**More:** 35 Search Insert Position (E), 34 First and Last Position (M), 153 Find Minimum in Rotated Sorted Array (M), 74 Search a 2D Matrix (M), 162 Find Peak Element (M), 69 Sqrt(x) (E), 1011 Capacity to Ship Packages (M), 981 Time Based Key-Value Store (M), 378 Kth Smallest in Sorted Matrix (M), 719 Find K-th Smallest Pair Distance (H).
