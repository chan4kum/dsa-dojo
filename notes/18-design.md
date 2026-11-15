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
capacity 2; list shown **least recent -> most recent**

| op | cache state | note |
|---|---|---|
| put(1,1) | [(1, 1)] | - |
| put(2,2) | [(1, 1), (2, 2)] | - |
| get(1) | [(2, 2), (1, 1)] | -> 1 |
| put(3,3) | [(1, 1), (3, 3)] |   evict 2 |
| get(2) | [(1, 1), (3, 3)] | -> -1 |

## 5. Template
*Reference solution for **LRU Cache** (`design/2`) - tested by `python dsa.py selftest`:*

```python
# OPTIMISED: get/put O(1)
# Idea: Hash map + doubly linked list (or OrderedDict): O(1) ordered cache
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.d = OrderedDict()  # least recent first

    def get(self, key):
        if key not in self.d:
            return -1
        self.d.move_to_end(key)  # mark most recent
        return self.d[key]

    def put(self, key, value):
        if key in self.d:
            self.d.move_to_end(key)
        self.d[key] = value
        if len(self.d) > self.cap:
            self.d.popitem(last=False)  # evict least recent
```

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
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `design/5` | Easy | Kth Largest Element in a Stream | [#703](https://leetcode.com/problems/kth-largest-element-in-a-stream/) | Fixed-size min-heap = 'k largest so far' (root = k-th largest) |
| `design/6` | Easy | Implement Queue using Stacks | [#232](https://leetcode.com/problems/implement-queue-using-stacks/) | Two stacks + lazy transfer (amortised O(1)) |
| `design/1` | Medium | Min Stack | [#155](https://leetcode.com/problems/min-stack/) | Augmented stack: keep running aggregates next to each element |
| `design/2` | Medium | LRU Cache | [#146](https://leetcode.com/problems/lru-cache/) | Hash map + doubly linked list (or OrderedDict): O(1) ordered cache |
| `design/3` | Medium | Implement Trie (Prefix Tree) | [#208](https://leetcode.com/problems/implement-trie-prefix-tree/) | Trie (prefix tree): O(L) insert/search per word, shared prefixes |
| `design/7` | Medium | Time Based Key-Value Store | [#981](https://leetcode.com/problems/time-based-key-value-store/) | Hash map of sorted lists + binary search (floor lookup) |
| `design/8` | Medium | Design Add and Search Words Data Structure | [#211](https://leetcode.com/problems/design-add-and-search-words-data-structure/) | Trie + DFS branching on wildcards |
| `design/9` | Medium | Design Browser History | [#1472](https://leetcode.com/problems/design-browser-history/) | Array + cursor (truncate on write) |
| `design/10` | Medium | Range Sum Query - Mutable | [#307](https://leetcode.com/problems/range-sum-query-mutable/) | Fenwick tree / BIT (prefix sums with point updates) |
| `design/4` | Hard | Find Median from Data Stream | [#295](https://leetcode.com/problems/find-median-from-data-stream/) | Two heaps (max-heap of the lower half + min-heap of the upper half) |

Start one with `python dsa.py start design/1`.

**More:** 232 Implement Queue using Stacks (E), 705 Design HashSet (E), 706 Design HashMap (E), 380 Insert Delete GetRandom O(1) (M), 211 Design Add and Search Words (M), 355 Design Twitter (M), 981 Time Based Key-Value Store (M), 1146 Snapshot Array (M), 307 Range Sum Query - Mutable (M), 460 LFU Cache (H), 432 All O`one Data Structure (H), 297 Serialize and Deserialize Binary Tree (H).

## 9. Make it stay - the teacher's anchors

**Picture it.** A restaurant kitchen: the menu (interface) stays the same, but the layout behind it (hash map + linked list, heaps, tries) decides how fast every dish arrives.

**The rule in one sentence.** List the operations and their required complexities FIRST; then choose the structure(s) that give each operation its cost, usually by combining two structures.

**Why it works.** One structure rarely gives O(1) for everything, but two that cover for each other's weaknesses do (map = lookup, list = order; two heaps = median).

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. What does each of the two structures in LRU Cache do?
2. Why does a trie beat a hash set for prefix queries?
3. How do two heaps give the median in O(log n) per insert?

**Mistakes students make most.**
- Choosing the structure before listing the operations.
- Forgetting to keep the two structures in sync after delete/evict.
- Ignoring capacity and edge cases (empty, duplicates).

**When NOT to use it.** Simple data + few operations - a plain list or dict is enough; do not over-engineer.

**The same idea in disguise.** Min stack -> LRU -> trie -> median finder -> kth largest stream -> time-based key-value store -> Fenwick tree -> browser history.
