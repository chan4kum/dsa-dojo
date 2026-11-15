# 02 - Prefix sums (and prefix anything)

> **One idea:** precompute running totals once; then *any* range query becomes a subtraction.

## 1. First principles
- Let `P[i] = a[0] + ... + a[i-1]` (with `P[0] = 0`). Then `sum(a[l..r]) = P[r+1] - P[l]`.
- A subarray sum is a **difference of two prefix values**. Problems about subarrays become problems about *pairs of prefix values*.
- Works for any associative, invertible-ish operation: sum, XOR, product (careful with zeros), counts per letter.
- The mirror image is the **difference array**: to add `v` to range `[l, r]` do `d[l] += v; d[r+1] -= v`, then prefix-sum `d`.

## 2. How to spot it
- "sum of subarray / range", "number of subarrays with sum k / divisible by k", "equal number of 0s and 1s".
- Many range queries or many range updates on a static array.
- "Everything except me" (left part x right part).

## 3. Paper recipe
1. Write the array and its prefix array underneath it (leave a leading 0).
2. Express the target as `P[r+1] - P[l] = k` -> rearrange to `P[l] = P[r+1] - k`.
3. That is **Two Sum on prefix values**: keep a dict `prefix value -> count` while scanning.
4. Seed the dict with `{0: 1}` so subarrays starting at index 0 count.
5. Negatives allowed? Then sliding window is **wrong**; prefix + hash map is right.

## 4. Hand trace
{{trace:prefix_hash}}

## 5. Template
{{solution:prefix_sums/3}}

Static range query: `P = [0]; for x in a: P.append(P[-1] + x)` then `P[r+1] - P[l]`.

## 6. Traps
- Forgetting the leading `0` prefix (off-by-one on the first element).
- Updating the dict **before** querying it (counts the empty subarray when `k = 0`).
- Divisible-by-k: Python's `%` is already non-negative; in C++/Java normalise negatives.
- Sliding window with negative numbers.

## 7. Self-check
1. Why is `{0: 1}` the right seed? Test it on `nums=[3], k=3`.
2. Turn "count subarrays with equal 0s and 1s" into this pattern (map 0 -> -1).
3. How do you do range **updates** in O(1) each?

## 8. Practice ladder
{{ladder}}

**More:** 303 Range Sum Query - Immutable (E), 304 Range Sum Query 2D - Immutable (M), 525 Contiguous Array (M), 974 Subarray Sums Divisible by K (M), 1109 Corporate Flight Bookings (M), 1094 Car Pooling (M), 523 Continuous Subarray Sum (M).
