# 18 - Data-structure design (LRU, Trie, Min Stack, Median Finder)

> **One idea:** combine two simple structures so that each operation you need is O(1) or O(log n).

## 1. First principles
- A design problem lists the operations and their required complexity. Work backwards: **which structure gives each operation cheaply?** Then glue them together.
- Useful pairings:
  | Need | Combination |
  |---|---|
  | O(1) lookup **and** O(1) ordered removal (LRU) | hash map -> doubly linked list nodes (or `OrderedDict`) |
  | O(1) min/max with push/pop | stack of `(value, running min)` |
  | O(1) random pick + O(1) insert/delete | array + `value -> index` map (swap with last on delete) |
  | prefix search / autocomplete | **trie** (dict of dicts) |
  | running median | two heaps |
  | range sum with updates | Fenwick tree / segment tree |
  | frequency buckets (LFU) | map key->freq + map freq->ordered keys |
  | time-based versions | map key -> sorted list of (time, value) + binary search |
- **Invariants** keep the glue correct: "the list order is exactly the recency order", "`lo` <= `hi` and sizes differ by at most 1".

## 2. How to spot it
- "Design a ... class with methods ...", "all operations in O(1)".
- The names: Cache, Iterator, Stream, Counter, Logger, Twitter feed, Autocomplete.

## 3. Paper recipe
1. List every operation and its target complexity in a small table.
2. Pick a structure per operation, then ask "what does it cost to keep the *other* structure consistent?".
3. Write the **invariant** in one sentence.
4. Walk a short sequence of calls by hand, showing the internal state after each call (see the LRU trace).
5. Handle the edges: empty, capacity 1, duplicate keys, key not found.

## 4. Hand trace
{{trace:lru}}

## 5. Template
{{solution:design/2}}

Interview note: be ready to write the doubly linked list **by hand** (head/tail sentinels, `_remove(node)`, `_add_front(node)`) - `OrderedDict` hides it.

## 6. Traps
- Updating one structure but forgetting the other (map and list drift apart).
- Not moving a key to "most recent" on **get** as well as **put**.
- Eviction after insert vs before insert at capacity boundaries.
- Thread-safety is a follow-up question: mention locks / sharding.

## 7. Self-check
1. What invariant does the linked list maintain in LRU?
2. How do you delete from the middle of an array in O(1) (Randomized Set)?
3. How would LFU differ from LRU in what you store?

## 8. Practice ladder
{{ladder}}

**More:** 232 Implement Queue using Stacks (E), 705 Design HashSet (E), 706 Design HashMap (E), 380 Insert Delete GetRandom O(1) (M), 211 Design Add and Search Words Data Structure (M), 355 Design Twitter (M), 981 Time Based Key-Value Store (M), 1146 Snapshot Array (M), 307 Range Sum Query - Mutable (M), 460 LFU Cache (H), 432 All O`one Data Structure (H), 297 Serialize and Deserialize Binary Tree (H).
