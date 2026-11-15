# 09 - Intervals

> **One idea:** sort intervals by start (or end); after sorting, overlaps become *local*, so one sweep is enough.

## 1. First principles
- An interval is `[start, end]`. Two intervals overlap iff `a.start <= b.end and b.start <= a.end`.
- **Sort by start** -> to merge, compare the next interval only with the last merged one.
- **Sort by end** -> greedy "keep the interval that finishes first" (activity selection).
- **Sweep line:** turn each interval into two events (`+1` at start, `-1` at end), sort the events, and track the running count - gives "max overlap", rooms, car pooling.
- Decide upfront whether touching endpoints (`[1,2]`,`[2,3]`) overlap.

## 2. How to spot it
- Pairs like `[l, r]`, meetings, calendar, schedule, ranges, booking.
- "merge", "insert", "minimum removals to avoid overlap", "minimum rooms/platforms", "can attend all".

## 3. Paper recipe
1. Draw the intervals as segments on a number line.
2. Choose the sort key: start (merge/insert/intersect) or end (max kept / min arrows).
3. Write the overlap test with your touching rule.
4. Sweep once, maintaining `last` (merge) or `end` (greedy) or a counter (events).
5. Check: single interval, fully nested interval, identical intervals, touching intervals.

## 4. Hand trace
input `[[1, 3], [8, 10], [2, 6], [15, 18]]` -> sorted by start first

| next | action | output so far |
|---|---|---|
| [1, 3] | gap -> new interval | [[1, 3]] |
| [2, 6] | overlaps last -> extend end to 6 | [[1, 6]] |
| [8, 10] | gap -> new interval | [[1, 6], [8, 10]] |
| [15, 18] | gap -> new interval | [[1, 6], [8, 10], [15, 18]] |

## 5. Template
*Reference solution for **Merge Intervals** (`intervals/1`) - tested by `python dsa.py selftest`:*

```python
# OPTIMISED: O(n log n) time
# Idea: Sort by start + sweep, merging into the last output interval
def merge(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
```

Sweep-line skeleton (max overlap), valid Python:
```python
events = sorted([(s, 1) for s, e in intervals] + [(e, -1) for s, e in intervals])
running = best = 0
for _, delta in events:
    running += delta
    best = max(best, running)
```
Tuples sort by time then delta, so at equal time the `-1` sorts before `+1`: touching intervals such as `[1,2]` and `[2,3]` do **not** overlap. If the problem treats touching as overlapping (closed intervals), flip the tie-break (`+1` first).

## 6. Traps
- Forgetting `max(last.end, e)` (nested intervals).
- Mutating the input list while iterating.
- Tie-breaking in events (end before start or start before end?) - read the problem.
- Sorting by the wrong key for the greedy variant.

## 7. Self-check
1. Why does sorting by *end* give the max number of non-overlapping intervals? (exchange argument)
2. How do you find free time between meetings from the merged list?
3. Minimum meeting rooms: heap of end times or sweep line - when would you choose each?

## 8. Practice ladder
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `intervals/4` | Easy | Meeting Rooms | [#252](https://leetcode.com/problems/meeting-rooms/) | Sort by start, compare neighbours |
| `intervals/8` | Easy | Summary Ranges | [#228](https://leetcode.com/problems/summary-ranges/) | Linear scan grouping consecutive runs |
| `intervals/10` | Easy | Teemo Attacking | [#495](https://leetcode.com/problems/teemo-attacking/) | Merge overlapping intervals by looking at consecutive gaps |
| `intervals/1` | Medium | Merge Intervals | [#56](https://leetcode.com/problems/merge-intervals/) | Sort by start + sweep, merging into the last output interval |
| `intervals/2` | Medium | Insert Interval | [#57](https://leetcode.com/problems/insert-interval/) | Linear scan in three phases (before / overlapping / after) |
| `intervals/3` | Medium | Non-overlapping Intervals | [#435](https://leetcode.com/problems/non-overlapping-intervals/) | Greedy on interval END times (activity selection) |
| `intervals/5` | Medium | Meeting Rooms II | [#253](https://leetcode.com/problems/meeting-rooms-ii/) | Sweep line over events / min-heap of end times |
| `intervals/6` | Medium | Minimum Number of Arrows to Burst Balloons | [#452](https://leetcode.com/problems/minimum-number-of-arrows-to-burst-balloons/) | Greedy on interval END (sort by end) |
| `intervals/7` | Medium | Interval List Intersections | [#986](https://leetcode.com/problems/interval-list-intersections/) | Two pointers over two sorted interval lists |
| `intervals/9` | Medium | Remove Covered Intervals | [#1288](https://leetcode.com/problems/remove-covered-intervals/) | Sort (start asc, end desc) + running max end |
| `intervals/11` | Medium | Minimum Time Difference | [#539](https://leetcode.com/problems/minimum-time-difference/) | Sort, then compare neighbours (plus the circular wrap-around) |
| `intervals/12` | Medium | Find Right Interval | [#436](https://leetcode.com/problems/find-right-interval/) | Sort once + binary search per query |
| `intervals/13` | Medium | Maximum Length of Pair Chain | [#646](https://leetcode.com/problems/maximum-length-of-pair-chain/) | Greedy: sort by end, take the earliest finisher |
| `intervals/14` | Medium | Car Pooling | [#1094](https://leetcode.com/problems/car-pooling/) | Difference array / sweep line |
| `intervals/15` | Medium | Corporate Flight Bookings | [#1109](https://leetcode.com/problems/corporate-flight-bookings/) | Difference array |
| `intervals/16` | Medium | Meeting Scheduler | [#1229](https://leetcode.com/problems/meeting-scheduler/) | Two pointers over two sorted interval lists |
| `intervals/17` | Medium | Remove Interval | [#1272](https://leetcode.com/problems/remove-interval/) | Per-interval case analysis |
| `intervals/19` | Medium | Maximum Distance in Arrays | [#624](https://leetcode.com/problems/maximum-distance-in-arrays/) | Running min/max across a scan |
| `intervals/18` | Hard | Meeting Rooms III | [#2402](https://leetcode.com/problems/meeting-rooms-iii/) | Simulation with two heaps |

Start one with `python dsa.py start intervals/1`.

**More:** 252 Meeting Rooms (E), 253 Meeting Rooms II (M), 452 Minimum Number of Arrows to Burst Balloons (M), 986 Interval List Intersections (M), 1094 Car Pooling (M), 218 The Skyline Problem (H), 759 Employee Free Time (H).

## 9. Make it stay - the teacher's anchors

**Picture it.** A calendar: sort meetings by start time and the whole picture falls out; overlaps can only happen between neighbours.

**The rule in one sentence.** Sort first (by start to merge, by END to pick the maximum non-overlapping set), then sweep once.

**Why it works.** After sorting by start, if interval i overlaps some later interval j, it already overlaps i+1. Sorting by end makes the earliest finisher the safest greedy pick (exchange argument).

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. Which sort key for merging, which for scheduling - and why?
2. How does a min-heap give the number of rooms needed?
3. What does 'touching' intervals mean for <= vs <?

**Mistakes students make most.**
- Choosing the wrong sort key.
- Mutating the input intervals unexpectedly.
- Treating [1,2] and [2,3] as overlapping when the problem says they are not (or vice versa).

**When NOT to use it.** Intervals arrive online with deletions (use a balanced tree/sorted container).

**The same idea in disguise.** Merge -> insert -> non-overlapping -> meeting rooms I/II -> arrows to burst balloons -> interval intersections -> employee free time.
