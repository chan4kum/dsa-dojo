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
{{trace:container}}

## 5. Template
{{solution:two_pointers/2}}

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
{{ladder}}

**More:** 26 Remove Duplicates from Sorted Array (E), 283 Move Zeroes (E), 167 Two Sum II - Input Array Is Sorted (M), 75 Sort Colors (M, Dutch flag), 16 3Sum Closest (M), 18 4Sum (M), 977 Squares of a Sorted Array (E), 345 Reverse Vowels of a String (E), 680 Valid Palindrome II (E).
