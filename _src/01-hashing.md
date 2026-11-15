# 01 - Hashing (hash maps & sets)

> **One idea:** pay O(n) memory to turn "have I seen this before / how many of these?" from an O(n) scan into an O(1) lookup.

## 1. First principles
- A hash table turns a key into an array index with a hash function, so lookup, insert and delete cost **O(1) on average**.
- Everything you would otherwise find by *scanning* (is x in the list? how often did x occur? what was the index of x?) becomes a lookup.
- **Set** = only membership. **Dict** = membership + a stored value (index, count, list of items).
- Keys must be *hashable and stable*: numbers, strings, tuples yes; lists no (use `tuple(...)`).

## 2. How to spot it
- "find two/pairs that ...", "does a duplicate exist", "first non-repeating", "count occurrences", "group by ..."
- Your brute force has a nested loop where the inner loop only asks **"is there an element equal to F(x)?"**
- You want to compare structures (anagrams, same pattern) -> build a **canonical key** and group by it.

## 3. Paper recipe
1. Write the brute force: `for i: for j: if cond(i,j)`.
2. Rewrite `cond(i,j)` as `a[j] == F(a[i])` (e.g. `target - a[i]`).
3. Decide what the dict stores: value -> index, value -> count, signature -> list.
4. Decide the order: **look up first, then insert** (so you never match an element with itself).
5. Edge cases: empty input, all equal, negatives, duplicates.

## 4. Hand trace
{{trace:two_sum}}

## 5. Template
{{solution:hashing/1}}

Canonical-key grouping: `groups[tuple(sorted(w))].append(w)`. Run-start trick for sequences: only expand from `x` when `x-1` is absent.

## 6. Traps
- Inserting before looking up lets `x` pair with itself ([3] with target 6).
- Counting with `dict[k] += 1` needs `defaultdict(int)`/`Counter`.
- Mutable keys (lists) raise `TypeError`: convert to tuples.
- Worst case O(n) per op exists (collisions) but is ignorable in interviews; say "average O(1)".

## 7. Self-check (answer on paper, then check)
1. Why is `longest_consecutive` O(n) despite a `while` inside a `for`?
2. How would you group anagrams without sorting each word?
3. What changes if the array is already sorted? (Hint: two pointers, O(1) space.)

## 8. Practice ladder
{{ladder}}

**More of this pattern (LeetCode):** 217 Contains Duplicate (E), 242 Valid Anagram (E), 387 First Unique Character (E), 202 Happy Number (E), 205 Isomorphic Strings (E), 347 Top K Frequent (M), 454 4Sum II (M), 138 Copy List with Random Pointer (M), 36 Valid Sudoku (M), 560 Subarray Sum Equals K (M).
