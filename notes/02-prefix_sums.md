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
`nums = [1, 2, 3, -3, 3]`, `k = 3`; start with `seen = {0: 1}` (the empty prefix)

| x | prefix | need = prefix - k | subarrays ending here | ans | seen after |
|---|---|---|---|---|---|
| 1 | 1 | -2 | 0 | 0 | {0: 1, 1: 1} |
| 2 | 3 | 0 | 1 | 1 | {0: 1, 1: 1, 3: 1} |
| 3 | 6 | 3 | 1 | 2 | {0: 1, 1: 1, 3: 1, 6: 1} |
| -3 | 3 | 0 | 1 | 3 | {0: 1, 1: 1, 3: 2, 6: 1} |
| 3 | 6 | 3 | 2 | 5 | {0: 1, 1: 1, 3: 2, 6: 2} |

## 5. Template
*Reference solution for **Subarray Sum Equals K** (`prefix_sums/3`) - tested by `python dsa.py selftest`:*

```python
def subarray_sum(nums, k):
    seen = defaultdict(int)
    seen[0] = 1                      # empty prefix
    pref = ans = 0
    for x in nums:
        pref += x
        ans += seen[pref - k]        # earlier prefixes that make a subarray of sum k ending here
        seen[pref] += 1
    return ans
```

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
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `prefix_sums/1` | Easy | Find Pivot Index | [#724](https://leetcode.com/problems/find-pivot-index/) | Prefix sum (running total) with total-minus-left trick |
| `prefix_sums/2` | Medium | Product of Array Except Self | [#238](https://leetcode.com/problems/product-of-array-except-self/) | Prefix / suffix accumulation (prefix idea works for any associative operation) |
| `prefix_sums/3` | Medium | Subarray Sum Equals K | [#560](https://leetcode.com/problems/subarray-sum-equals-k/) | Prefix sum + hash map of counts ('how many earlier prefixes equal current - k?') |

Start one with `python dsa.py start prefix_sums/1`.

**More:** 303 Range Sum Query Immutable (E), 304 Range Sum Query 2D (M), 525 Contiguous Array (M), 974 Subarray Sums Divisible by K (M), 1109 Corporate Flight Bookings (M), 1094 Car Pooling (M), 523 Continuous Subarray Sum (M).

## 9. Make it stay - the teacher's anchors

**Picture it.** Mile markers on a highway. The distance between markers 12 and 47 is marker(47) - marker(12): you never re-drive the road.

**The rule in one sentence.** A range sum is a difference of two prefix sums: sum(l..r) = P[r+1] - P[l].

**Why it works.** Every prefix already contains everything before it, so subtracting the shorter prefix cancels the shared part and leaves exactly the range.

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. Write sum(i..j) using P. What is P[0] and why do we need it?
2. How does 'subarray sum = k' become a Two Sum problem on prefixes?
3. What do you store in the dictionary and why do we insert P[0] = 0 first?

**Mistakes students make most.**
- Off-by-one between P of length n+1 and the array of length n.
- Forgetting the empty prefix (misses subarrays that start at index 0).
- Using a sliding window when negatives exist (windows need non-negative numbers; prefix + hash does not).

**When NOT to use it.** You only need ONE range query (just loop), or updates are interleaved with queries (use a Fenwick tree / segment tree, see Range Sum Query - Mutable).

**The same idea in disguise.** Range sum -> pivot index -> product except self (prefix AND suffix products) -> subarray sum divisible by k (prefix mod k) -> path sum on a tree (prefix sums down the path).
