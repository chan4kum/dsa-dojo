from core import *

PROBLEMS = [
    dict(
        title="Merge Intervals", diff="M", lc=56, slug="merge-intervals",
        prompt="Given a list of [start, end] intervals, merge all that overlap and return the disjoint intervals "
               "sorted by start.",
        sig="def merge(intervals: List[List[int]]) -> List[List[int]]:",
        fn="merge",
        tests=[(([[1, 3], [2, 6], [8, 10], [15, 18]],), [[1, 6], [8, 10], [15, 18]]), (([[1, 4], [4, 5]],), [[1, 5]]),
               (([[1, 4], [0, 4]],), [[0, 4]]), (([[1, 10], [2, 3], [4, 5]],), [[1, 10]]), (([[5, 6]],), [[5, 6]])],
        hints=["If the intervals are in random order, overlaps can be anywhere. What ordering makes overlaps local?",
               "Sort by start. Then an interval can only overlap the LAST merged interval.",
               "Overlap test: next.start <= last.end -> extend last.end = max(last.end, next.end); else start a new interval."],
        pattern="Sort by start + sweep, merging into the last output interval",
        explain="""
        After sorting by start, any interval that overlaps an earlier one must overlap the most recent merged
        block (otherwise it starts after that block ends). So a single left-to-right sweep suffices. The max()
        on the end handles an interval fully contained in the previous one. O(n log n) for the sort.""",
        solution=r'''
def merge(intervals):
    out = []
    for s, e in sorted(intervals):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
''',
    ),
    dict(
        title="Insert Interval", diff="M", lc=57, slug="insert-interval",
        prompt="You have non-overlapping intervals sorted by start. Insert a new interval, merging if needed, "
               "and return the result (still sorted and non-overlapping).",
        sig="def insert(intervals: List[List[int]], new_interval: List[int]) -> List[List[int]]:",
        fn="insert",
        tests=[(([[1, 3], [6, 9]], [2, 5]), [[1, 5], [6, 9]]),
               (([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]), [[1, 2], [3, 10], [12, 16]]),
               (([], [5, 7]), [[5, 7]]), (([[1, 5]], [2, 3]), [[1, 5]]), (([[1, 5]], [6, 8]), [[1, 5], [6, 8]])],
        hints=["The list is already sorted, so you do not need to sort - think three phases.",
               "Phase 1: copy intervals that end before the new one starts. Phase 3: copy those that start after it ends.",
               "Phase 2: while an interval overlaps (start <= new.end), absorb it: new = [min(starts), max(ends)]."],
        pattern="Linear scan in three phases (before / overlapping / after)",
        explain="""
        Because input is sorted and disjoint, the intervals split into: strictly left of the new one, overlapping
        it, strictly right of it - in that order. Merge the middle group into one interval. O(n) time.""",
        solution=r'''
def insert(intervals, new_interval):
    out, i, n = [], 0, len(intervals)
    s, e = new_interval
    while i < n and intervals[i][1] < s:          # entirely before
        out.append(intervals[i])
        i += 1
    while i < n and intervals[i][0] <= e:         # overlapping -> absorb
        s = min(s, intervals[i][0])
        e = max(e, intervals[i][1])
        i += 1
    out.append([s, e])
    out.extend(intervals[i:])                     # entirely after
    return out
''',
    ),
    dict(
        title="Non-overlapping Intervals", diff="M", lc=435, slug="non-overlapping-intervals",
        prompt="Return the minimum number of intervals to remove so that the remaining ones do not overlap "
               "(touching at an endpoint is fine).",
        sig="def erase_overlap_intervals(intervals: List[List[int]]) -> int:",
        fn="erase_overlap_intervals",
        tests=[(([[1, 2], [2, 3], [3, 4], [1, 3]],), 1), (([[1, 2], [1, 2], [1, 2]],), 2), (([[1, 2], [2, 3]],), 0),
               (([[1, 100], [11, 22], [1, 11], [2, 12]],), 2), (([[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]],), 2)],
        hints=["Equivalent question: what is the MAXIMUM number of intervals you can keep?",
               "Greedy: always keep the interval that finishes earliest - it leaves the most room for the future.",
               "Sort by END. Keep an interval if its start >= the last kept end; otherwise count it as removed."],
        pattern="Greedy on interval END times (activity selection)",
        explain="""
        Exchange argument: among overlapping candidates, the one ending first can replace any other in an
        optimal schedule without causing a new conflict. So sort by end and take what fits. Answer = n - kept.
        O(n log n).""",
        solution=r'''
def erase_overlap_intervals(intervals):
    intervals = sorted(intervals, key=lambda x: x[1])
    end = float("-inf")
    removed = 0
    for s, e in intervals:
        if s >= end:
            end = e              # keep it
        else:
            removed += 1         # overlaps the interval we kept -> drop
    return removed
''',
    ),
]
