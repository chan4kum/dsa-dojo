"""more Intervals problems (batch 4) - part of the problem bank for the "intervals" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Teemo Attacking (LeetCode 495) ----
    dict(
        title="Teemo Attacking",
        diff="E",
        lc=495,
        slug="teemo-attacking",
        prompt=(
            "An attack at time t poisons for `duration` seconds (t .. t + duration - 1); a new attack resets the "
            "timer. time_series is sorted. Return the total number of seconds poisoned."
        ),
        sig="def find_poisoned_duration(time_series: List[int], duration: int) -> int:",
        fn="find_poisoned_duration",
        tests=[
            (([1, 4], 2), 4),
            (([1, 2], 2), 3),
            (([5], 3), 3),
            (([], 4), 0),
            (([1, 2, 3, 4, 5], 5), 9),
        ],
        hints=[
            "Each attack contributes `duration` seconds unless the next attack comes sooner.",
            "If the gap to the next attack is smaller than duration, only the gap counts (the rest overlaps).",
            "Sum min(duration, next - current) for every attack, and add duration for the last one.",
        ],
        pattern="Merge overlapping intervals by looking at consecutive gaps",
        explain=(
            "Because the attacks are sorted, overlap only happens between neighbours, so the union length is the "
            "sum of capped gaps."
        ),
        cx="O(n) time",
        brute_cx="O(n * duration) time - mark every poisoned second in a set",
        brute=r"""
# BRUTE FORCE: O(n * duration) time - mark every poisoned second in a set
def find_poisoned_duration(time_series, duration):
    poisoned = set()
    for t in time_series:
        poisoned.update(range(t, t + duration))  # every second this attack covers
    return len(poisoned)
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Merge overlapping intervals by looking at consecutive gaps
def find_poisoned_duration(time_series, duration):
    total = 0
    for i, t in enumerate(time_series):
        if i + 1 < len(time_series):
            total += min(duration, time_series[i + 1] - t)  # an overlap is counted once
        else:
            total += duration
    return total
""",
    ),
    # ---- Minimum Time Difference (LeetCode 539) ----
    dict(
        title="Minimum Time Difference",
        diff="M",
        lc=539,
        slug="minimum-time-difference",
        prompt=(
            "Given 24-hour clock times as 'HH:MM' strings, return the minimum difference in minutes between any two "
            "of them (the clock wraps around midnight)."
        ),
        sig="def find_min_difference(time_points: List[str]) -> int:",
        fn="find_min_difference",
        tests=[
            ((["23:59", "00:00"],), 1),
            ((["00:00", "23:59", "00:00"],), 0),
            ((["12:00", "13:30"],), 90),
            ((["01:00", "13:00", "19:00", "00:00"],), 60),
        ],
        hints=[
            "Convert each time to minutes since midnight.",
            "After sorting, the closest pair must be NEIGHBOURS.",
            "Also compare the last and the first through midnight: first + 1440 - last.",
        ],
        pattern="Sort, then compare neighbours (plus the circular wrap-around)",
        explain=(
            "On a line the closest pair is always adjacent after sorting. On a circle the only extra adjacency is "
            "last-to-first across the wrap."
        ),
        cx="O(n log n) time",
        brute_cx="O(n^2) time - compare every pair, taking the shorter way around",
        brute=r"""
# BRUTE FORCE: O(n^2) time - compare every pair, taking the shorter way around
def find_min_difference(time_points):
    minutes = [int(t[:2]) * 60 + int(t[3:]) for t in time_points]
    best = 1440
    for i in range(len(minutes)):
        for j in range(i + 1, len(minutes)):
            d = abs(minutes[i] - minutes[j])
            best = min(best, d, 1440 - d)  # the short way around the clock
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Sort, then compare neighbours (plus the circular wrap-around)
def find_min_difference(time_points):
    minutes = sorted(int(t[:2]) * 60 + int(t[3:]) for t in time_points)
    best = minutes[0] + 1440 - minutes[-1]  # across midnight
    for a, b in zip(minutes, minutes[1:]):
        best = min(best, b - a)
    return best
""",
    ),
]
