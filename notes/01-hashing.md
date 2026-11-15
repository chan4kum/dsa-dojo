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
`nums = [2, 11, 7, 15]`, `target = 9`

| i | x | need = target - x | seen (before) | action |
|---|---|---|---|---|
| 0 | 2 | 7 | {} | store 2 -> 0 |
| 1 | 11 | -2 | {2: 0} | store 11 -> 1 |
| 2 | 7 | 2 | {2: 0, 11: 1} | FOUND -> [0, 2] |

## 5. Template
*Reference solution for **Two Sum** (`hashing/1`) - tested by `python dsa.py selftest`:*

```python
def two_sum(nums, target):
    seen = {}                      # value -> index
    for i, x in enumerate(nums):
        if target - x in seen:     # complement already seen?
            return [seen[target - x], i]
        seen[x] = i
    return []
```

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
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `hashing/1` | Easy | Two Sum | [#1](https://leetcode.com/problems/two-sum/) | Hash map: trade memory for O(1) 'have I seen the complement?' lookups |
| `hashing/4` | Easy | Contains Duplicate | [#217](https://leetcode.com/problems/contains-duplicate/) | Hash set: O(1) 'seen before?' |
| `hashing/5` | Easy | Valid Anagram | [#242](https://leetcode.com/problems/valid-anagram/) | Frequency counting (canonical form of a multiset) |
| `hashing/6` | Easy | Isomorphic Strings | [#205](https://leetcode.com/problems/isomorphic-strings/) | Bijection check with two hash maps (or normalised pattern) |
| `hashing/2` | Medium | Group Anagrams | [#49](https://leetcode.com/problems/group-anagrams/) | Hash map with a canonical-form key (group by signature) |
| `hashing/3` | Medium | Longest Consecutive Sequence | [#128](https://leetcode.com/problems/longest-consecutive-sequence/) | Hash set + 'only expand from the start of a sequence' (amortised O(n)) |

Start one with `python dsa.py start hashing/1`.

**More of this pattern (LeetCode):** 217 Contains Duplicate (E), 242 Valid Anagram (E), 387 First Unique Character (E), 202 Happy Number (E), 205 Isomorphic Strings (E), 347 Top K Frequent (M), 454 4Sum II (M), 138 Copy List with Random Pointer (M), 36 Valid Sudoku (M), 560 Subarray Sum Equals K (M).

## 9. Make it stay - the teacher's anchors

**Picture it.** A coat check. Instead of searching every rack for your coat (O(n)), you hand over a ticket (the hash) and the attendant walks straight to the hook.

**The rule in one sentence.** If your inner loop only asks 'does something equal F(x) exist?', replace the loop with a dictionary lookup.

**Why it works.** A hash maps a key to an array slot, and array access by index is O(1). You pay O(n) memory once to turn every future 'seen it?' from a scan into a jump.

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. Why must Two Sum look up the complement BEFORE inserting the current number?
2. What makes two words anagrams, and how does that become a dictionary key?
3. Why is Longest Consecutive Sequence O(n) although it has a while inside a for?

**Mistakes students make most.**
- Using a list for membership tests (`x in list` is O(n), silently making the solution O(n^2)).
- Using a mutable key (list) - convert to a tuple.
- Forgetting duplicates: a set loses counts, a Counter keeps them.

**When NOT to use it.** The data is already sorted and memory is tight - two pointers gives O(1) space. Or the question is about ORDER/RANGES (use sorting/heap/tree), because hashes destroy order.

**The same idea in disguise.** Two Sum -> Subarray Sum Equals K (store prefix sums) -> Contiguous Array (store first index of a balance) -> Longest Substring Without Repeating (store last index). Same lookup, different 'key'.
