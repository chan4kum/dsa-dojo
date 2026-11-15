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

{{trace:kadane}}

Cyclic placement (First Missing Positive):

{{trace:cyclic}}

## 5. Template
{{solution:array_tricks/3}}

## 6. Traps
- Initialising Kadane with `0` instead of `nums[0]` (fails on all-negative input).
- Cyclic sort infinite loop when duplicates exist: always compare with the *destination* value (`a[a[i]-1] != a[i]`).
- Max-**product** subarray needs both a running max and min (a negative flips them).

## 7. Self-check
1. Why can the answer to First Missing Positive never exceed `n + 1`?
2. Modify Kadane to also return the subarray's start and end.
3. What is the circular-array variant (918) and how does "total - min subarray" help?

## 8. Practice ladder
{{ladder}}

**More:** 121 Best Time to Buy and Sell Stock (E), 152 Maximum Product Subarray (M), 918 Maximum Sum Circular Subarray (M), 442 Find All Duplicates (M), 448 Find All Numbers Disappeared (E), 287 Find the Duplicate Number (M), 645 Set Mismatch (E), 169 Majority Element (E, Boyer-Moore), 189 Rotate Array (M).
