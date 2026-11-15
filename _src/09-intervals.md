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
{{trace:merge_intervals}}

## 5. Template
{{solution:intervals/1}}

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
{{ladder}}

**More:** 252 Meeting Rooms (E), 253 Meeting Rooms II (M), 452 Minimum Number of Arrows to Burst Balloons (M), 986 Interval List Intersections (M), 1094 Car Pooling (M), 218 The Skyline Problem (H), 759 Employee Free Time (H).
