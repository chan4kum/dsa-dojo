"""extra batch of Intervals problems - the problem bank for the "intervals" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
Optional keys: compare (how to compare answers), adapt_in/adapt_out (convert lists <-> linked lists / trees),
check (validate any correct answer), inplace (which argument is mutated).
"""

PROBLEMS = [
    # ---- Meeting Rooms (LeetCode 252) ----
    dict(
        title="Meeting Rooms",
        diff="E",
        lc=252,
        slug="meeting-rooms",
        prompt=(
            "Given meeting time intervals [start, end), can one person attend all of them (no overlaps)? A meeting "
            "ending at t and another starting at t do not overlap."
        ),
        sig="def can_attend_meetings(intervals: List[List[int]]) -> bool:",
        fn="can_attend_meetings",
        tests=[
            (([[0, 30], [5, 10], [15, 20]],), False),
            (([[7, 10], [2, 4]],), True),
            (([],), True),
            (([[1, 2], [2, 3]],), True),
            (([[1, 5], [2, 3]],), False),
        ],
        hints=[
            "Which pairs could possibly overlap if you ordered meetings by start time?",
            "Only neighbours in sorted order - if the sort order is by start.",
            "Sort by start; if any meeting starts before the previous one ends, return False.",
        ],
        pattern="Sort by start, compare neighbours",
        explain=(
            "After sorting by start time, if meeting i overlaps meeting j > i+1 then it also overlaps i+1. So "
            "checking\n        adjacent pairs is enough."
        ),
        cx="O(n log n) time, O(1) extra space",
        brute_cx="O(n^2) time - compare every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - compare every pair
def can_attend_meetings(intervals):
    for i in range(len(intervals)):
        for j in range(i + 1, len(intervals)):
            a, b = intervals[i], intervals[j]
            if a[0] < b[1] and b[0] < a[1]:
                return False
    return True
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space
# Idea: Sort by start, compare neighbours
def can_attend_meetings(intervals):
    iv = sorted(intervals)
    return all(iv[i][1] <= iv[i + 1][0] for i in range(len(iv) - 1))
""",
    ),
    # ---- Meeting Rooms II (LeetCode 253) ----
    dict(
        title="Meeting Rooms II",
        diff="M",
        lc=253,
        slug="meeting-rooms-ii",
        prompt="Return the minimum number of conference rooms needed so that all meetings [start, end) can take place.",
        sig="def min_meeting_rooms(intervals: List[List[int]]) -> int:",
        fn="min_meeting_rooms",
        tests=[
            (([[0, 30], [5, 10], [15, 20]],), 2),
            (([[7, 10], [2, 4]],), 1),
            (([[1, 5], [2, 6], [3, 7]],), 3),
            (([[1, 2], [2, 3]],), 1),
            (([],), 0),
        ],
        hints=[
            "The answer is the maximum number of meetings happening at the same instant.",
            "Look at start and end times separately, as events on a timeline.",
            (
                "Sort starts and ends; sweep: if the next start < earliest unfinished end, you need a room, else "
                "reuse one. (Or: a min-heap of end times.)"
            ),
        ],
        pattern="Sweep line over events / min-heap of end times",
        explain=(
            "Each start is +1 room, each end is -1. The peak of the running count is the answer. Equal times: "
            "process the\n        end first (touching meetings share a room). The heap version pops the "
            "earliest-ending meeting if it ended in time."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2) time - for each start count meetings active at that moment",
        brute=r"""
# BRUTE FORCE: O(n^2) time - for each start count meetings active at that moment
def min_meeting_rooms(intervals):
    best = 0
    for s, _ in intervals:
        best = max(best, sum(1 for a, b in intervals if a <= s < b))
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Sweep line over events / min-heap of end times
def min_meeting_rooms(intervals):
    heap = []  # end times of meetings in progress
    for s, e in sorted(intervals):
        if heap and heap[0] <= s:
            heapq.heapreplace(heap, e)  # reuse the room that freed up
        else:
            heapq.heappush(heap, e)  # need a new room
    return len(heap)
""",
    ),
    # ---- Minimum Number of Arrows to Burst Balloons (LeetCode 452) ----
    dict(
        title="Minimum Number of Arrows to Burst Balloons",
        diff="M",
        lc=452,
        slug="minimum-number-of-arrows-to-burst-balloons",
        prompt=(
            "Balloons are horizontal segments [xstart, xend]. An arrow shot straight up at x bursts every balloon "
            "with xstart <= x <= xend. Return the minimum arrows needed."
        ),
        sig="def find_min_arrow_shots(points: List[List[int]]) -> int:",
        fn="find_min_arrow_shots",
        tests=[
            (([[10, 16], [2, 8], [1, 6], [7, 12]],), 2),
            (([[1, 2], [3, 4], [5, 6], [7, 8]],), 4),
            (([[1, 2], [2, 3], [3, 4], [4, 5]],), 2),
            (([[1, 2]],), 1),
            (([[2, 3], [2, 3]],), 1),
        ],
        hints=[
            "This is an interval-scheduling problem in disguise (compare Non-overlapping Intervals).",
            "Sort by END coordinate. The first balloon's end is the best place to shoot.",
            (
                "Shoot at the current end; skip every balloon whose start <= that end. The next balloon with a "
                "larger start needs a new arrow."
            ),
        ],
        pattern="Greedy on interval END (sort by end)",
        explain=(
            "Shooting at the smallest end bursts the first balloon and the maximum number of others that overlap it "
            "- an\n        exchange argument shows no better place exists. Count how often the greedy has to start "
            "a new group."
        ),
        cx="O(n log n) time, O(1) space",
        brute_cx="O(n^2) time - repeatedly shoot at the smallest remaining end, remove everything hit",
        brute=r"""
# BRUTE FORCE: O(n^2) time - repeatedly shoot at the smallest remaining end, remove everything hit
def find_min_arrow_shots(points):
    left = [list(p) for p in points]
    arrows = 0
    while left:
        x = min(e for _, e in left)
        left = [p for p in left if not (p[0] <= x <= p[1])]
        arrows += 1
    return arrows
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) space
# Idea: Greedy on interval END (sort by end)
def find_min_arrow_shots(points):
    arrows, last_end = 0, float("-inf")
    for s, e in sorted(points, key=lambda p: p[1]):
        if s > last_end:
            arrows += 1
            last_end = e
    return arrows
""",
    ),
    # ---- Interval List Intersections (LeetCode 986) ----
    dict(
        title="Interval List Intersections",
        diff="M",
        lc=986,
        slug="interval-list-intersections",
        prompt=(
            "Two lists of closed intervals, each sorted and internally disjoint. Return their intersection (also "
            "sorted)."
        ),
        sig="def interval_intersection(first_list: List[List[int]], second_list: List[List[int]]) -> List[List[int]]:",
        fn="interval_intersection",
        tests=[
            (
                ([[0, 2], [5, 10], [13, 23], [24, 25]], [[1, 5], [8, 12], [15, 24], [25, 26]]),
                [[1, 2], [5, 5], [8, 10], [15, 23], [24, 24], [25, 25]],
            ),
            (([], [[1, 2]]), []),
            (([[1, 3]], [[2, 5]]), [[2, 3]]),
            (([[1, 7]], [[3, 4], [5, 6]]), [[3, 4], [5, 6]]),
        ],
        hints=[
            "Two intervals intersect in [max(starts), min(ends)] when that range is non-empty.",
            "Use a pointer into each list - like the merge step of merge sort.",
            (
                "After handling a pair, advance the pointer of the interval that ENDS first (the other may still "
                "intersect later ones)."
            ),
        ],
        pattern="Two pointers over two sorted interval lists",
        explain=(
            "The interval that finishes first can never intersect anything further in the other list, so discard "
            "it.\n        Each step discards one interval: O(m+n)."
        ),
        cx="O(m+n) time",
        brute_cx="O(m*n) time - test every pair",
        brute=r"""
# BRUTE FORCE: O(m*n) time - test every pair
def interval_intersection(first_list, second_list):
    out = []
    for a, b in first_list:
        for c, d in second_list:
            lo, hi = max(a, c), min(b, d)
            if lo <= hi:
                out.append([lo, hi])
    return sorted(out)
""",
        solution=r"""
# OPTIMISED: O(m+n) time
# Idea: Two pointers over two sorted interval lists
def interval_intersection(first_list, second_list):
    i = j = 0
    out = []

    while i < len(first_list) and j < len(second_list):
        lo = max(first_list[i][0], second_list[j][0])
        hi = min(first_list[i][1], second_list[j][1])

        if lo <= hi:
            out.append([lo, hi])

        if first_list[i][1] < second_list[j][1]:
            i += 1
        else:
            j += 1

    return out
""",
    ),
]
