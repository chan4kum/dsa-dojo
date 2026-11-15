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
    # ---- Summary Ranges (LeetCode 228) ----
    dict(
        title="Summary Ranges",
        diff="E",
        lc=228,
        slug="summary-ranges",
        prompt=(
            "Given a sorted list of distinct integers, return the smallest list of ranges covering exactly the "
            "numbers, formatted 'a->b' or 'a'."
        ),
        sig="def summary_ranges(nums: List[int]) -> List[str]:",
        fn="summary_ranges",
        tests=[
            (([0, 1, 2, 4, 5, 7],), ["0->2", "4->5", "7"]),
            (([0, 2, 3, 4, 6, 8, 9],), ["0", "2->4", "6", "8->9"]),
            (([],), []),
            (([5],), ["5"]),
            (([-1, 0, 1],), ["-1->1"]),
        ],
        hints=[
            "A range ends where the next number is not previous + 1.",
            "Walk once with a start pointer and extend while consecutive.",
            "On a break, emit start if start == end else 'start->end', then start a new range.",
        ],
        pattern="Linear scan grouping consecutive runs",
        explain=(
            "Sorted + distinct means one pass suffices; each element either extends the current run or starts a new "
            "one."
        ),
        cx="O(n) time",
        brute_cx="O(n^2) time (re-scan forward from each start)",
        brute=r"""
# BRUTE FORCE: O(n^2) time (re-scan forward from each start)
def summary_ranges(nums):
    out, i = [], 0
    while i < len(nums):
        j = i
        while j + 1 < len(nums) and nums[j + 1] == nums[j] + 1:
            j += 1
        out.append(str(nums[i]) if i == j else f"{nums[i]}->{nums[j]}")
        i = j + 1
    return out
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Linear scan grouping consecutive runs
def summary_ranges(nums):
    out = []
    start = None
    for i, x in enumerate(nums):
        if start is None:
            start = x
        if i + 1 == len(nums) or nums[i + 1] != x + 1:
            out.append(str(start) if start == x else f"{start}->{x}")
            start = None
    return out
""",
    ),
    # ---- Remove Covered Intervals (LeetCode 1288) ----
    dict(
        title="Remove Covered Intervals",
        diff="M",
        lc=1288,
        slug="remove-covered-intervals",
        prompt=(
            "Interval [a,b) is covered by [c,d) if c <= a and b <= d. Return how many intervals remain after "
            "removing all covered ones."
        ),
        sig="def remove_covered_intervals(intervals: List[List[int]]) -> int:",
        fn="remove_covered_intervals",
        tests=[
            (([[1, 4], [3, 6], [2, 8]],), 2),
            (([[1, 4], [2, 3]],), 1),
            (([[1, 2], [1, 4], [3, 4]],), 1),
            (([[0, 10], [5, 12]],), 2),
            (([[1, 4]],), 1),
        ],
        hints=[
            "Sort so that checking only the previous interval's end is enough.",
            "Sort by start ascending, and by end DESCENDING for equal starts (so the bigger one comes first).",
            "Keep the max end so far; an interval is covered when its end <= that max.",
        ],
        pattern="Sort (start asc, end desc) + running max end",
        explain=(
            "After sorting, any covering interval appears earlier. The farthest end seen so far decides if the "
            "current one is swallowed."
        ),
        cx="O(n log n) time",
        brute_cx="O(n^2) time",
        brute=r"""
# BRUTE FORCE: O(n^2) time
def remove_covered_intervals(intervals):
    n = len(intervals)
    keep = 0
    for i in range(n):
        a, b = intervals[i]
        covered = any(j != i and intervals[j][0] <= a and b <= intervals[j][1] for j in range(n))
        keep += not covered
    return keep
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Sort (start asc, end desc) + running max end
def remove_covered_intervals(intervals):
    intervals = sorted(intervals, key=lambda x: (x[0], -x[1]))
    keep, far = 0, -1
    for _start, end in intervals:
        if end > far:
            keep += 1
            far = end
    return keep
""",
    ),
]
