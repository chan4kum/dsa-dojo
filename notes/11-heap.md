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

`nums = [3, 2, 1, 5, 6, 4]`, `k = 2` (min-heap of the k largest so far)

| x | eviction | heap after |
|---|---|---|
| 3 | - | [3] |
| 2 | - | [2, 3] |
| 1 | pop smallest = 1 | [2, 3] |
| 5 | pop smallest = 2 | [3, 5] |
| 6 | pop smallest = 3 | [5, 6] |
| 4 | pop smallest = 4 | [5, 6] |

Root `5` is the 2-nd largest.

Running median with two heaps:

stream `5, 2, 8, 1`

| add | lower half (max-heap) | upper half (min-heap) | median |
|---|---|---|---|
| 5 | [5] | [] | 5.0 |
| 2 | [2] | [5] | 3.5 |
| 8 | [2, 5] | [8] | 5.0 |
| 1 | [1, 2] | [5, 8] | 3.5 |

## 5. Template
*Reference solution for **Kth Largest Element in an Array** (`heap/1`) - tested by `python dsa.py selftest`:*

```python
# OPTIMISED: O(n log k) time (or O(n) average with quickselect), O(k) space
# Idea: Top-K with a size-k min-heap
def find_kth_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)  # evict the smallest of the k+1
    return heap[0]
```

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
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `heap/4` | Easy | Last Stone Weight | [#1046](https://leetcode.com/problems/last-stone-weight/) | Max-heap via negated values (repeated 'take the largest') |
| `heap/1` | Medium | Kth Largest Element in an Array | [#215](https://leetcode.com/problems/kth-largest-element-in-an-array/) | Top-K with a size-k min-heap |
| `heap/2` | Medium | Top K Frequent Elements | [#347](https://leetcode.com/problems/top-k-frequent-elements/) | Frequency map + heap (O(n log k)) or bucket sort (O(n)) |
| `heap/3` | Medium | Task Scheduler | [#621](https://leetcode.com/problems/task-scheduler/) | Greedy / counting argument on the most frequent task (a heap simulation also works) |
| `heap/5` | Medium | K Closest Points to Origin | [#973](https://leetcode.com/problems/k-closest-points-to-origin/) | Bounded heap of size k (top-k selection) |
| `heap/6` | Medium | Reorganize String | [#767](https://leetcode.com/problems/reorganize-string/) | Greedy with a max-heap (most frequent first, avoid the last used) |
| `heap/7` | Medium | Top K Frequent Words | [#692](https://leetcode.com/problems/top-k-frequent-words/) | Counter + top-k with a composite sort key |
| `heap/8` | Medium | Find K Pairs with Smallest Sums | [#373](https://leetcode.com/problems/find-k-pairs-with-smallest-sums/) | Best-first search with a heap over a sorted 2D implicit grid |
| `heap/9` | Medium | Ugly Number II | [#264](https://leetcode.com/problems/ugly-number-ii/) | k-way merge of implicit sorted sequences (multiples of earlier results) |
| `heap/10` | Medium | Kth Smallest Element in a Sorted Matrix | [#378](https://leetcode.com/problems/kth-smallest-element-in-a-sorted-matrix/) | k-way merge with a heap (or binary search on value) |

Start one with `python dsa.py start heap/1`.

**More:** 703 Kth Largest Element in a Stream (E), 1046 Last Stone Weight (E), 973 K Closest Points to Origin (M), 23 Merge k Sorted Lists (H), 295 Find Median from Data Stream (H), 373 Find K Pairs with Smallest Sums (M), 767 Reorganize String (M), 253 Meeting Rooms II (M), 502 IPO (H), 632 Smallest Range Covering Elements from K Lists (H), 355 Design Twitter (M).

## 9. Make it stay - the teacher's anchors

**Picture it.** A tournament bracket kept in a tree: the champion is always on top, and replacing it only requires replaying one root-to-leaf path.

**The rule in one sentence.** Repeatedly need the current min/max while things keep arriving? Use a heap: O(log n) per operation instead of O(n log n) re-sorting.

**Why it works.** A heap keeps only PARTIAL order (parent <= children), which is all you need for 'the best one', and that is why it is cheaper than a sorted list.

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. Why a MIN-heap of size k for the k LARGEST?
2. Heap vs sort vs quickselect: when each?
3. Why does Python store negatives for a max-heap?

**Mistakes students make most.**
- Comparing unorderable payloads on ties (add an index tie-breaker).
- Using a max-heap when a bounded min-heap is cheaper.
- Forgetting `heapify` is O(n).

**When NOT to use it.** You need the whole sorted order, or arbitrary-element deletion (use a sorted container or lazy deletion).

**The same idea in disguise.** Kth largest -> top K frequent -> merge K lists -> meeting rooms II -> task scheduler -> median of a stream (two heaps) -> smallest range.
