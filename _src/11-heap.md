# 11 - Heaps / priority queues (Top-K, two heaps, k-way merge)

> **One idea:** a heap gives you the min (or max) of a changing collection in O(log n), without keeping everything sorted.

## 1. First principles
- A binary heap is a complete tree stored in an array where each parent <= its children (min-heap). `heappush`/`heappop` cost O(log n), peek is O(1), `heapify` of n items is O(n).
- Python has only a **min-heap** (`heapq`). For a max-heap push `-x`. For custom order push tuples `(priority, tiebreak, item)`.
- **Top-K largest -> keep a MIN-heap of size k** (the root is the weakest of the k; evict it). Top-K smallest -> max-heap of size k.
- **Two heaps** (max-heap for the lower half + min-heap for the upper half) maintain a running median.
- **k-way merge:** a heap of the current head of each sorted source.
- **Lazy deletion:** instead of removing from the middle, mark stale and skip when popped (Dijkstra does this).

## 2. How to spot it
- "k-th largest/smallest", "top k frequent", "k closest".
- "repeatedly take the smallest/largest and process" (merge, schedule, stones, Huffman).
- "median of a stream", "sliding window median".
- Shortest path with weights (Dijkstra's frontier is a heap).

## 3. Paper recipe
1. Say what you repeatedly need: the min? the max? both ends?
2. Decide heap type and **size** (bounded size k gives O(n log k)).
3. Decide what goes in the entries: `(key, ...)`; negate for max.
4. Write the loop: push, (evict if size > k), read the root.
5. Compare with sort (O(n log n)) and quickselect (O(n) average) - say why the heap wins (streaming, small k).

## 4. Hand traces
Top-K with a bounded min-heap:

{{trace:kth_largest}}

Running median with two heaps:

{{trace:two_heaps}}

## 5. Template
{{solution:heap/1}}

## 6. Traps
- Forgetting to negate for max-heap (and to negate back on pop).
- `heapq` compares tuples element-wise; if priorities tie it compares the next field (may be uncomparable) - add a counter tiebreak.
- Using a max-heap of size k for top-k *largest* (should be a min-heap).
- Re-heapifying inside a loop (O(n) each time).

## 7. Self-check
1. Why is the heap for the k-th largest a *min*-heap?
2. Complexity of building a heap of n items by pushing vs `heapify`?
3. How does the two-heap invariant (`len(lo) == len(hi)` or `+1`) give the median in O(1)?

## 8. Practice ladder
{{ladder}}

**More:** 703 Kth Largest Element in a Stream (E), 1046 Last Stone Weight (E), 973 K Closest Points to Origin (M), 23 Merge k Sorted Lists (H), 295 Find Median from Data Stream (H), 373 Find K Pairs with Smallest Sums (M), 767 Reorganize String (M), 253 Meeting Rooms II (M), 502 IPO (H), 632 Smallest Range Covering Elements from K Lists (H), 355 Design Twitter (M).
