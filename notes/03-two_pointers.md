# 03 - Two pointers

> **One idea:** two indices that move monotonically replace a nested loop, because each move *rules out* a whole set of candidates.

## 1. First principles
- A nested loop checks all O(n^2) pairs. Two pointers is valid when you can prove: "moving this pointer can only help / the discarded candidates can never be the answer".
- **Opposite ends** (`l = 0`, `r = n-1`, move toward each other): needs an ordering (sorted array) or a monotone quantity (width shrinking).
- **Same direction** (`slow`/`fast`, read/write): partitioning, removing duplicates, in-place compaction.
- Total pointer movement is at most 2n -> **O(n)**.

## 2. How to spot it
- Sorted array/string and a pair/triple condition ("sum equals", "closest to").
- Palindrome checks, reversing, merging two sorted lists.
- "In place, O(1) extra space" on an array.
- A geometric argument like "the shorter wall limits the area".

## 3. Paper recipe
1. Draw the array with `l` and `r` arrows at the ends.
2. For the current pair write what you learn: too small? too big? limited by which side?
3. State the **discard argument** in one sentence ("if the sum is too small, nothing paired with a[l] works, so l++").
4. If you cannot state it, two pointers is the wrong tool.
5. Duplicates: skip equal neighbours *after* sorting rather than using a set.

## 4. Hand trace
`height = [1, 8, 6, 2, 5, 4, 8, 3, 7]`

| l | r | h[l] | h[r] | area | best | move |
|---|---|---|---|---|---|---|
| 0 | 8 | 1 | 7 | 8 x 1 = 8 | 8 | l += 1 (left is shorter) |
| 1 | 8 | 8 | 7 | 7 x 7 = 49 | 49 | r -= 1 |
| 1 | 7 | 8 | 3 | 6 x 3 = 18 | 49 | r -= 1 |
| 1 | 6 | 8 | 8 | 5 x 8 = 40 | 49 | r -= 1 |
| 1 | 5 | 8 | 4 | 4 x 4 = 16 | 49 | r -= 1 |
| 1 | 4 | 8 | 5 | 3 x 5 = 15 | 49 | r -= 1 |
| 1 | 3 | 8 | 2 | 2 x 2 = 4 | 49 | r -= 1 |
| 1 | 2 | 8 | 6 | 1 x 6 = 6 | 49 | r -= 1 |

## 5. Template
*Reference solution for **3Sum** (`two_pointers/2`) - tested by `python dsa.py selftest`:*

```python
# OPTIMISED: O(n^2) time, O(1) extra space (sort + two pointers)
# Idea: Sort + fix one element + two pointers on the rest
def three_sum(nums):
    nums.sort()
    res = []
    n = len(nums)
    for i in range(n - 2):
        if i and nums[i] == nums[i - 1]:  # skip duplicate anchors
            continue
        left, right = i + 1, n - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if s < 0:
                left += 1
            elif s > 0:
                right -= 1
            else:
                res.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
    return res
```

## 6. Traps
- Not sorting first (3Sum, 4Sum need it).
- Infinite loops: every branch must move a pointer.
- Duplicate triplets: skip duplicates for the anchor **and** for the inner pair after recording a hit.
- `l < r` vs `l <= r` (pairs need distinct indices).

## 7. Self-check
1. Prove the "move the shorter wall" rule in Container With Most Water.
2. Why does 3Sum cost O(n^2) and not O(n^3)?
3. What is the same-direction version of two pointers for "move zeros to the end"?

## 8. Practice ladder
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `two_pointers/1` | Easy | Valid Palindrome | [#125](https://leetcode.com/problems/valid-palindrome/) | Two pointers, opposite ends, converging |
| `two_pointers/6` | Easy | Squares of a Sorted Array | [#977](https://leetcode.com/problems/squares-of-a-sorted-array/) | Two pointers from both ends, build output from the largest |
| `two_pointers/7` | Easy | Move Zeroes | [#283](https://leetcode.com/problems/move-zeroes/) | Read/write pointers (partition in place) |
| `two_pointers/9` | Easy | Merge Sorted Array | [#88](https://leetcode.com/problems/merge-sorted-array/) | Merge from the back (use the free space as a buffer) |
| `two_pointers/10` | Easy | Valid Palindrome II | [#680](https://leetcode.com/problems/valid-palindrome-ii/) | Two pointers with one allowed skip (branch once) |
| `two_pointers/11` | Easy | Reverse String | [#344](https://leetcode.com/problems/reverse-string/) | Two pointers from both ends (swap inward) |
| `two_pointers/14` | Easy | Backspace String Compare | [#844](https://leetcode.com/problems/backspace-string-compare/) | Two pointers from the end (O(1) space) |
| `two_pointers/15` | Easy | Long Pressed Name | [#925](https://leetcode.com/problems/long-pressed-name/) | Two pointers with run-length reasoning |
| `two_pointers/16` | Easy | Valid Palindrome II | [#680](https://leetcode.com/problems/valid-palindrome-ii/) | Two pointers with one allowed skip |
| `two_pointers/2` | Medium | 3Sum | [#15](https://leetcode.com/problems/3sum/) | Sort + fix one element + two pointers on the rest |
| `two_pointers/3` | Medium | Container With Most Water | [#11](https://leetcode.com/problems/container-with-most-water/) | Two pointers converging, with a greedy discard argument |
| `two_pointers/5` | Medium | Two Sum II - Input Array Is Sorted | [#167](https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/) | Two pointers on a sorted array (converge from both ends) |
| `two_pointers/8` | Medium | Sort Colors | [#75](https://leetcode.com/problems/sort-colors/) | Three-way partition (Dutch national flag) with an invariant |
| `two_pointers/12` | Medium | 3Sum Closest | [#16](https://leetcode.com/problems/3sum-closest/) | Sort + fix one + two pointers (optimise distance) |
| `two_pointers/13` | Medium | 4Sum | [#18](https://leetcode.com/problems/4sum/) | k-Sum reduction: sort, fix k-2 values, two pointers for the last pair |
| `two_pointers/4` | Hard | Trapping Rain Water | [#42](https://leetcode.com/problems/trapping-rain-water/) | Two pointers with running maxima (the smaller side decides) |

Start one with `python dsa.py start two_pointers/1`.

**More:** 26 Remove Duplicates from Sorted Array (E), 283 Move Zeroes (E), 167 Two Sum II (M), 75 Sort Colors (M, Dutch flag), 16 3Sum Closest (M), 18 4Sum (M), 977 Squares of a Sorted Array (E), 345 Reverse Vowels (E), 680 Valid Palindrome II (E).

## 9. Make it stay - the teacher's anchors

**Picture it.** Two people squeezing a sorted bookshelf from both ends: if the sum of the two books is too heavy, the heavier book can never be part of the answer - drop it.

**The rule in one sentence.** Sorted (or monotone) data + a pair condition => start at both ends and discard one end every step.

**Why it works.** Each move eliminates a candidate that can no longer succeed, so you do at most n moves instead of n^2 pairs. The elimination argument IS the proof.

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. In Two Sum II, why is it safe to move `right` left when the sum is too big?
2. Why does Container With Most Water move the SHORTER wall?
3. How does read/write pointers (Move Zeroes) differ from converging pointers?

**Mistakes students make most.**
- Applying converging pointers to unsorted data.
- Moving the wrong pointer in Container With Most Water.
- Duplicates in 3Sum: skip equal values AFTER recording a triple.

**When NOT to use it.** The condition is not monotone in either pointer, or you need indices of the ORIGINAL order after sorting (hash map instead).

**The same idea in disguise.** Two Sum II -> 3Sum -> Container -> Trapping Rain Water -> Sort Colors (three-way partition) -> Merge Sorted Array (from the back).
