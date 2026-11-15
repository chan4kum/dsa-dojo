# 19 - Divide and conquer (merge sort & counting during merge)

> **One idea:** split the problem in half, solve each half recursively, and combine - the combine step is where the interesting work (and the complexity) lives.

## 1. First principles
- Three steps: **divide**, **conquer** (recurse), **combine**.
- Cost: `T(n) = a*T(n/b) + f(n)`. For merge sort `a = 2, b = 2, f(n) = O(n)` -> `log n` levels x `O(n)` per level = **O(n log n)**.
- The combine step can do more than merge: **count pairs across the two halves** while both halves are sorted (inversions, reverse pairs, count of smaller numbers after self, count of range sum).
- Same shape elsewhere: quicksort/quickselect (partition then recurse on one side), binary search (recurse on one half), closest pair, fast Fourier transform, Karatsuba, segment trees.

## 2. How to spot it
- "count pairs (i < j) with property between a[i] and a[j]" with `n ~ 10^5` - O(n^2) is too slow.
- "sort without library sort", "k-th element", "maximum subarray (D&C form)".
- Structure splits naturally in the middle.

## 3. Paper recipe
1. Split the array in the middle; classify every pair as left-left, right-right, or **cross**.
2. Left-left and right-right are the recursive calls. Count/solve the **cross** pairs.
3. Because both halves are sorted, a **two-pointer sweep** counts cross pairs in O(n).
4. Merge the halves (sorted), return `(sorted_array, count)`.
5. Alternative tools for the same problems: Fenwick tree / BIT, segment tree, ordered set.

## 4. Hand trace
{{trace:merge_sort}}

## 5. Template
{{solution:divide_conquer/2}}

## 6. Traps
- Counting cross pairs **after** merging (the halves are no longer separate) - count first, then merge.
- Slicing creates copies (fine for O(n log n), but know it); use index ranges for O(1) extra per call.
- Stability: use `<=` when taking from the left half so equal elements keep order.
- Overflow of `2 * x` in other languages - use 64-bit.

## 7. Self-check
1. Draw the recursion tree for 8 elements and count the work per level.
2. Why must the cross-count happen while the two halves are *sorted separately*?
3. Solve inversion count with a Fenwick tree instead - what do you index by?

## 8. Practice ladder
{{ladder}}

**More:** 169 Majority Element (E), 148 Sort List (M), 215 Kth Largest Element in an Array (M), 315 Count of Smaller Numbers After Self (H), 327 Count of Range Sum (H), 241 Different Ways to Add Parentheses (M), 95 Unique Binary Search Trees II (M), 53 Maximum Subarray (M, divide-and-conquer version), 23 Merge k Sorted Lists (H, merge in pairs).
