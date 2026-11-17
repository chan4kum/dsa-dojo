"""Intervals problems - the problem bank for the "intervals" topic.

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
    # ---- Merge Intervals (LeetCode 56) ----
    dict(
        title="Merge Intervals",
        diff="M",
        lc=56,
        slug="merge-intervals",
        prompt=(
            "Given a list of [start, end] intervals, merge all that overlap and return the disjoint intervals "
            "sorted by start."
        ),
        sig="def merge(intervals: List[List[int]]) -> List[List[int]]:",
        fn="merge",
        tests=[
            (([[1, 3], [2, 6], [8, 10], [15, 18]],), [[1, 6], [8, 10], [15, 18]]),
            (([[1, 4], [4, 5]],), [[1, 5]]),
            (([[1, 4], [0, 4]],), [[0, 4]]),
            (([[1, 10], [2, 3], [4, 5]],), [[1, 10]]),
            (([[5, 6]],), [[5, 6]]),
        ],
        hints=[
            "If the intervals are in random order, overlaps can be anywhere. What ordering makes overlaps local?",
            "Sort by start. Then an interval can only overlap the LAST merged interval.",
            (
                "Overlap test: next.start <= last.end -> extend last.end = max(last.end, next.end); else start a "
                "new interval."
            ),
        ],
        pattern="Sort by start + sweep, merging into the last output interval",
        explain=(
            "After sorting by start, any interval that overlaps an earlier one must overlap the most recent "
            "merged\n        block (otherwise it starts after that block ends). So a single left-to-right sweep "
            "suffices. The max()\n        on the end handles an interval fully contained in the previous one. O(n "
            "log n) for the sort."
        ),
        cx="O(n log n) time",
        brute_cx="O(n^3) worst case - keep merging any overlapping pair",
        brute=r"""
# BRUTE FORCE: O(n^3) worst case - keep merging any overlapping pair
def merge(intervals):
    iv = [list(x) for x in intervals]
    changed = True

    while changed:
        changed = False

        for i in range(len(iv)):
            for j in range(i + 1, len(iv)):
                if iv[i][0] <= iv[j][1] and iv[j][0] <= iv[i][1]:
                    iv[i] = [min(iv[i][0], iv[j][0]), max(iv[i][1], iv[j][1])]
                    del iv[j]
                    changed = True
                    break

            if changed:
                break

    return sorted(iv)
""",
        solution=r"""
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
""",
    ),
    # ---- Insert Interval (LeetCode 57) ----
    dict(
        title="Insert Interval",
        diff="M",
        lc=57,
        slug="insert-interval",
        prompt=(
            "You have non-overlapping intervals sorted by start. Insert a new interval, merging if needed, and "
            "return the result (still sorted and non-overlapping)."
        ),
        sig="def insert(intervals: List[List[int]], new_interval: List[int]) -> List[List[int]]:",
        fn="insert",
        tests=[
            (([[1, 3], [6, 9]], [2, 5]), [[1, 5], [6, 9]]),
            (([[1, 2], [3, 5], [6, 7], [8, 10], [12, 16]], [4, 8]), [[1, 2], [3, 10], [12, 16]]),
            (([], [5, 7]), [[5, 7]]),
            (([[1, 5]], [2, 3]), [[1, 5]]),
            (([[1, 5]], [6, 8]), [[1, 5], [6, 8]]),
        ],
        hints=[
            "The list is already sorted, so you do not need to sort - think three phases.",
            "Phase 1: copy intervals that end before the new one starts. Phase 3: copy those that start after it ends.",
            "Phase 2: while an interval overlaps (start <= new.end), absorb it: new = [min(starts), max(ends)].",
        ],
        pattern="Linear scan in three phases (before / overlapping / after)",
        explain=(
            "Because input is sorted and disjoint, the intervals split into: strictly left of the new one, "
            "overlapping\n        it, strictly right of it - in that order. Merge the middle group into one "
            "interval. O(n) time."
        ),
        cx="O(n) time, O(n) output (input already sorted)",
        brute_cx="O(n log n) - append, re-sort, re-merge (ignores that input is sorted)",
        brute=r"""
# BRUTE FORCE: O(n log n) - append, re-sort, re-merge (ignores that input is sorted)
def insert(intervals, new_interval):
    iv = sorted([list(x) for x in intervals] + [list(new_interval)])
    out = []

    for s, e in iv:
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])

    return out
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) output (input already sorted)
# Idea: Linear scan in three phases (before / overlapping / after)
def insert(intervals, new_interval):
    out, i, n = [], 0, len(intervals)
    s, e = new_interval

    while i < n and intervals[i][1] < s:  # entirely before
        out.append(intervals[i])
        i += 1

    while i < n and intervals[i][0] <= e:  # overlapping -> absorb
        s = min(s, intervals[i][0])
        e = max(e, intervals[i][1])
        i += 1

    out.append([s, e])
    out.extend(intervals[i:])  # entirely after

    return out
""",
    ),
    # ---- Non-overlapping Intervals (LeetCode 435) ----
    dict(
        title="Non-overlapping Intervals",
        diff="M",
        lc=435,
        slug="non-overlapping-intervals",
        prompt=(
            "Return the minimum number of intervals to remove so that the remaining ones do not overlap (touching "
            "at an endpoint is fine)."
        ),
        sig="def erase_overlap_intervals(intervals: List[List[int]]) -> int:",
        fn="erase_overlap_intervals",
        tests=[
            (([[1, 2], [2, 3], [3, 4], [1, 3]],), 1),
            (([[1, 2], [1, 2], [1, 2]],), 2),
            (([[1, 2], [2, 3]],), 0),
            (([[1, 100], [11, 22], [1, 11], [2, 12]],), 2),
            (([[0, 2], [1, 3], [2, 4], [3, 5], [4, 6]],), 2),
        ],
        hints=[
            "Equivalent question: what is the MAXIMUM number of intervals you can keep?",
            "Greedy: always keep the interval that finishes earliest - it leaves the most room for the future.",
            "Sort by END. Keep an interval if its start >= the last kept end; otherwise count it as removed.",
        ],
        pattern="Greedy on interval END times (activity selection)",
        explain=(
            "Exchange argument: among overlapping candidates, the one ending first can replace any other in "
            "an\n        optimal schedule without causing a new conflict. So sort by end and take what fits. Answer "
            "= n - kept.\n        O(n log n)."
        ),
        cx="O(n log n) time (sort by end)",
        brute_cx="O(n^2) DP - longest non-overlapping chain",
        brute=r"""
# BRUTE FORCE: O(n^2) DP - longest non-overlapping chain
def erase_overlap_intervals(intervals):
    iv = sorted(intervals)
    n = len(iv)
    dp = [1] * n  # longest chain of non-overlapping intervals ending at i

    for i in range(n):
        for j in range(i):
            if iv[j][1] <= iv[i][0]:
                dp[i] = max(dp[i], dp[j] + 1)

    return n - max(dp, default=0)
""",
        solution=r"""
# OPTIMISED: O(n log n) time (sort by end)
# Idea: Greedy on interval END times (activity selection)
def erase_overlap_intervals(intervals):
    intervals = sorted(intervals, key=lambda x: x[1])
    end = float("-inf")
    removed = 0

    for s, e in intervals:
        if s >= end:
            end = e  # keep it
        else:
            removed += 1  # overlaps the interval we kept -> drop

    return removed
""",
    ),
]
