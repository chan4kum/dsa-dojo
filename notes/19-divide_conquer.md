# 19 - Divide and conquer (merge sort & counting during merge)

> **One idea:** split the problem in half, solve each half recursively, and combine - the combine step is where the interesting work (and the complexity) lives.

## 1. First principles
- Three steps: **divide**, **conquer** (recurse), **combine**.
- Cost: `T(n) = a*T(n/b) + f(n)`. For merge sort `a = 2, b = 2, f(n) = O(n)` -> `log n` levels x `O(n)` per level = **O(n log n)**.
- The combine step can do more than merge: **count pairs across the two halves** while both halves are sorted (inversions, reverse pairs, count of smaller numbers after self, count of range sum).
- Same shape elsewhere: quicksort (partition, then recurse on **both** sides) and quickselect (partition, then recurse on **one** side only, which is why it is O(n) on average), binary search (recurse on one half), closest pair, fast Fourier transform, Karatsuba, segment trees.

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
```text
split [5, 2, 4, 1, 3] -> [5, 2] | [4, 1, 3]
  split [5, 2] -> [5] | [2]
  merge [5] + [2] -> [2, 5]
  split [4, 1, 3] -> [4] | [1, 3]
    split [1, 3] -> [1] | [3]
    merge [1] + [3] -> [1, 3]
  merge [4] + [1, 3] -> [1, 3, 4]
merge [2, 5] + [1, 3, 4] -> [1, 2, 3, 4, 5]
```

## 5. Template
*Reference solution for **Reverse Pairs** (`divide_conquer/2`) - tested by `python dsa.py selftest`:*

```python
# OPTIMISED: O(n log n) time (count while merging)
# Idea: Divide & conquer with counting during merge sort (inversion-count family)
def reverse_pairs(nums):
    def sort(a):
        if len(a) <= 1:
            return a, 0

        mid = len(a) // 2
        left, x = sort(a[:mid])
        right, y = sort(a[mid:])
        count = x + y
        j = 0

        for v in left:  # cross pairs: v > 2 * right[j]
            while j < len(right) and v > 2 * right[j]:
                j += 1
            count += j

        merged, i, j = [], 0, 0

        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1

        merged += left[i:] + right[j:]

        return merged, count

    return sort(list(nums))[1]
```

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
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `divide_conquer/1` | Medium | Sort an Array | [#912](https://leetcode.com/problems/sort-an-array/) | Divide & conquer: split, solve halves, merge in O(n) -> O(n log n) |
| `divide_conquer/4` | Medium | Different Ways to Add Parentheses | [#241](https://leetcode.com/problems/different-ways-to-add-parentheses/) | Divide and conquer on the last operator + memoisation of substrings |
| `divide_conquer/6` | Medium | Beautiful Array | [#932](https://leetcode.com/problems/beautiful-array/) | Divide and conquer: affine maps keep the property, parity separates the halves |
| `divide_conquer/7` | Medium | K-th Symbol in Grammar | [#779](https://leetcode.com/problems/k-th-symbol-in-grammar/) | Divide and conquer: go back to the parent, flip on even positions |
| `divide_conquer/8` | Medium | Longest Substring with At Least K Repeating Characters | [#395](https://leetcode.com/problems/longest-substring-with-at-least-k-repeating-characters/) | Divide and conquer: split on the characters that cannot be inside any answer |
| `divide_conquer/10` | Medium | Maximum Binary Tree | [#654](https://leetcode.com/problems/maximum-binary-tree/) | Divide and conquer, optimised by a monotonic stack |
| `divide_conquer/11` | Medium | Super Pow | [#372](https://leetcode.com/problems/super-pow/) | Divide and conquer on the exponent (square/ten-fold per digit) |
| `divide_conquer/15` | Medium | Count Good Numbers | [#1922](https://leetcode.com/problems/count-good-numbers/) | Fast exponentiation (halve the exponent) |
| `divide_conquer/2` | Hard | Reverse Pairs | [#493](https://leetcode.com/problems/reverse-pairs/) | Divide & conquer with counting during merge sort (inversion-count family) |
| `divide_conquer/3` | Hard | Count of Smaller Numbers After Self | [#315](https://leetcode.com/problems/count-of-smaller-numbers-after-self/) | Merge sort that counts while merging (inversion counting) |
| `divide_conquer/5` | Hard | Count of Range Sum | [#327](https://leetcode.com/problems/count-of-range-sum/) | Merge sort on prefix sums, counting cross pairs |
| `divide_conquer/9` | Hard | The Skyline Problem | [#218](https://leetcode.com/problems/the-skyline-problem/) | Sweep line with a max-heap (lazy deletion) |
| `divide_conquer/12` | Hard | Number of Pairs Satisfying Inequality | [#2426](https://leetcode.com/problems/number-of-pairs-satisfying-inequality/) | Merge sort counting of cross pairs (inversion-count family) |
| `divide_conquer/13` | Hard | Create Sorted Array through Instructions | [#1649](https://leetcode.com/problems/create-sorted-array-through-instructions/) | Counting with a Fenwick tree (online cousin of merge-sort counting) |
| `divide_conquer/14` | Hard | Number of Ways to Reorder Array to Get Same BST | [#1569](https://leetcode.com/problems/number-of-ways-to-reorder-array-to-get-same-bst/) | Divide and conquer with binomial interleavings |

Start one with `python dsa.py start divide_conquer/1`.

**More:** 169 Majority Element (E), 148 Sort List (M), 215 Kth Largest Element in an Array (M), 315 Count of Smaller Numbers After Self (H), 327 Count of Range Sum (H), 241 Different Ways to Add Parentheses (M), 95 Unique Binary Search Trees II (M), 53 Maximum Subarray (M, divide-and-conquer version), 23 Merge k Sorted Lists (H, merge in pairs).

## 9. Make it stay - the teacher's anchors

**Picture it.** Sorting a library: split the shelves between helpers, each sorts their part, then you merge two sorted shelves - merging is easy, splitting is free.

**The rule in one sentence.** Split into independent halves, solve each recursively, combine cheaply. Cost: T(n) = 2T(n/2) + O(n) => O(n log n).

**Why it works.** Halving gives log n levels, and each level does O(n) total work in the combine step.

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. Write the recurrence for merge sort and solve it by drawing the tree.
2. How does merge sort count inversions (Reverse Pairs) for free?
3. When does divide and conquer differ from DP?

**Mistakes students make most.**
- Combine step slower than O(n) (e.g. repeated slicing).
- Forgetting base cases (size 0/1).
- Assuming subproblems are independent when they overlap (use DP).

**When NOT to use it.** Subproblems overlap - memoise instead. Or a simple scan already solves it.

**The same idea in disguise.** Merge sort -> count inversions / reverse pairs -> quickselect -> closest pair -> build tree from traversals -> median of two sorted arrays.
