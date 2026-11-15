# 04 - Sliding window

> **One idea:** keep a window `[l, r]` that always satisfies an invariant; extend `r` every step, move `l` only to repair the invariant.

## 1. First principles
- It is two pointers that move in the **same direction**, over a **contiguous** range.
- State per window is updated in O(1) (add the entering element, remove the leaving one), so the whole scan is O(n).
- **Fixed-size window:** size k never changes; slide by one.
- **Variable window - find longest:** expand always, shrink *while invalid*; record the best after repairing.
- **Variable window - find shortest:** expand until valid, then shrink *while still valid*, recording each time.
- Needs **monotonicity**: adding elements can only push the window toward invalid (or valid) in one direction. Negative numbers usually break it (use prefix sums).

## 2. How to spot it
- "longest / shortest / maximum / minimum **substring or subarray** such that ..."
- "contiguous", "at most k distinct", "no repeating", "contains all characters".
- Brute force enumerates all `(i, j)` and re-checks the window.

## 3. Paper recipe
1. Write the invariant in words ("window has no duplicates", "sum >= target", "covers all of t").
2. List what state you need to test it in O(1): a set, a counter, a running sum, a count of missing characters.
3. Decide: grow until valid then shrink (shortest) or grow then shrink until valid again (longest).
4. Write both update rules: **add `s[r]`**, **remove `s[l]`**.
5. Exactly-k trick: `exactly(k) = atMost(k) - atMost(k-1)`.

## 4. Hand trace
{{trace:window_unique}}

## 5. Template
{{solution:sliding_window/2}}

## 6. Traps
- Using `l = last[c] + 1` without `max(l, ...)` (stale entries from before the window).
- Updating the answer before the window is repaired.
- Counter that goes negative on purpose (Minimum Window) - know *why*.
- Fixed window: off-by-one on the first window (`i >= k - 1`).

## 7. Self-check
1. Why does shrinking with `while` not make it O(n^2)?
2. Why can't you use a sliding window for "subarray sum equals k" with negatives?
3. How do you count subarrays with exactly K distinct integers using only "at most K"?

## 8. Practice ladder
{{ladder}}

**More:** 121 Best Time to Buy and Sell Stock (E), 424 Longest Repeating Character Replacement (M), 567 Permutation in String (M), 438 Find All Anagrams (M), 904 Fruit Into Baskets (M), 1004 Max Consecutive Ones III (M), 713 Subarray Product Less Than K (M), 992 Subarrays with K Different Integers (H), 239 Sliding Window Maximum (H, see stack_monotonic).
