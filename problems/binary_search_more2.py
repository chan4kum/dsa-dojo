"""extra batch of Binary Search problems - the problem bank for the "binary_search" topic.

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
    # ---- Valid Perfect Square (LeetCode 367) ----
    dict(
        title="Valid Perfect Square",
        diff="E",
        lc=367,
        slug="valid-perfect-square",
        prompt="Return True if num is a perfect square. Do not use sqrt/pow built-ins.",
        sig="def is_perfect_square(num: int) -> bool:",
        fn="is_perfect_square",
        tests=[
            ((16,), True),
            ((14,), False),
            ((1,), True),
            ((808201,), True),
            ((2147395600,), True),
            ((2,), False),
        ],
        hints=[
            "Which integers could possibly be the root? A whole range, and the squares of that range are ordered.",
            "Binary search the root r in [1, num] comparing r*r with num.",
            "lo=1, hi=num: if mid*mid == num return True; smaller -> lo=mid+1; bigger -> hi=mid-1.",
        ],
        pattern="Binary search on the answer (monotone predicate r*r vs num)",
        explain="r*r is increasing in r, so 'is r big enough?' is monotone - the shape binary search needs.",
        cx="O(log n) time, O(1) space",
        brute_cx="O(sqrt n) time",
        brute=r"""
# BRUTE FORCE: O(sqrt n) time
def is_perfect_square(num):
    r = 1
    while r * r < num:
        r += 1
    return r * r == num
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Binary search on the answer (monotone predicate r*r vs num)
def is_perfect_square(num):
    lo, hi = 1, num

    while lo <= hi:
        mid = (lo + hi) // 2
        sq = mid * mid

        if sq == num:
            return True

        if sq < num:
            lo = mid + 1
        else:
            hi = mid - 1

    return False
""",
    ),
    # ---- Capacity To Ship Packages Within D Days (LeetCode 1011) ----
    dict(
        title="Capacity To Ship Packages Within D Days",
        diff="M",
        lc=1011,
        slug="capacity-to-ship-packages-within-d-days",
        prompt=(
            "Packages must ship in the given order, loading up to the ship's capacity each day. Return the least "
            "capacity that ships everything within `days` days."
        ),
        sig="def ship_within_days(weights: List[int], days: int) -> int:",
        fn="ship_within_days",
        tests=[
            (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 5), 15),
            (([3, 2, 2, 4, 1, 4], 3), 6),
            (([1, 2, 3, 1, 1], 4), 3),
            (([5], 1), 5),
            (([2, 2, 2], 3), 2),
        ],
        hints=[
            "Given a capacity C, can you check feasibility with one greedy pass?",
            "Feasibility is monotone: bigger capacity never hurts. So binary search C.",
            "C ranges from max(weights) to sum(weights). Count days greedily; if days_needed <= days, try smaller.",
        ],
        pattern="Binary search on the answer + greedy feasibility check",
        explain="When 'is X enough?' is monotone and cheap to test, search X instead of the solution itself.",
        cx="O(n log(sum)) time, O(1) space",
        brute_cx="O(n * sum) time",
        brute=r"""
# BRUTE FORCE: O(n * sum) time
def ship_within_days(weights, days):
    cap = max(weights)

    while True:
        d, load = 1, 0

        for w in weights:
            if load + w > cap:
                d += 1
                load = 0
            load += w

        if d <= days:
            return cap

        cap += 1
""",
        solution=r"""
# OPTIMISED: O(n log(sum)) time, O(1) space
# Idea: Binary search on the answer + greedy feasibility check
def ship_within_days(weights, days):
    def need(cap):
        d, load = 1, 0
        for w in weights:
            if load + w > cap:
                d += 1
                load = 0
            load += w
        return d

    lo, hi = max(weights), sum(weights)

    while lo < hi:
        mid = (lo + hi) // 2
        if need(mid) <= days:
            hi = mid
        else:
            lo = mid + 1

    return lo
""",
    ),
    # ---- Single Element in a Sorted Array (LeetCode 540) ----
    dict(
        title="Single Element in a Sorted Array",
        diff="M",
        lc=540,
        slug="single-element-in-a-sorted-array",
        prompt=(
            "Every value appears exactly twice except one that appears once; the array is sorted. Find it in O(log "
            "n) time."
        ),
        sig="def single_non_duplicate(nums: List[int]) -> int:",
        fn="single_non_duplicate",
        tests=[
            (([1, 1, 2, 3, 3, 4, 4, 8, 8],), 2),
            (([3, 3, 7, 7, 10, 11, 11],), 10),
            (([1],), 1),
            (([1, 2, 2],), 1),
            (([1, 1, 2],), 2),
        ],
        hints=[
            "Before the single element pairs start at even indices; after it they start at odd indices.",
            "Look at mid: is its twin on the right or left? That tells which side holds the single.",
            (
                "Force mid to be even (mid -= mid % 2). If nums[mid] == nums[mid+1] the single is to the right (lo "
                "= mid+2) else hi = mid."
            ),
        ],
        pattern="Binary search on a structural invariant (pair parity)",
        explain=(
            "The invariant 'pairs start on even indices' holds left of the odd one out and breaks right after it - "
            "a monotone boundary."
        ),
        cx="O(log n) time, O(1) space",
        brute_cx="O(n) time (XOR all values)",
        brute=r"""
# BRUTE FORCE: O(n) time (XOR all values)
def single_non_duplicate(nums):
    r = 0
    for x in nums:
        r ^= x
    return r
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Binary search on a structural invariant (pair parity)
def single_non_duplicate(nums):
    lo, hi = 0, len(nums) - 1

    while lo < hi:
        mid = (lo + hi) // 2
        mid -= mid % 2
        if nums[mid] == nums[mid + 1]:
            lo = mid + 2
        else:
            hi = mid

    return nums[lo]
""",
    ),
    # ---- Find K Closest Elements (LeetCode 658) ----
    dict(
        title="Find K Closest Elements",
        diff="M",
        lc=658,
        slug="find-k-closest-elements",
        prompt=(
            "Given a sorted array, return the k elements closest to x, sorted ascending. On ties the smaller "
            "element wins."
        ),
        sig="def find_closest_elements(arr: List[int], k: int, x: int) -> List[int]:",
        fn="find_closest_elements",
        tests=[
            (([1, 2, 3, 4, 5], 4, 3), [1, 2, 3, 4]),
            (([1, 2, 3, 4, 5], 4, -1), [1, 2, 3, 4]),
            (([1, 1, 2, 3, 4, 5], 3, 3), [2, 3, 4]),
            (([1, 3], 1, 2), [1]),
            (([0, 0, 1, 2, 3, 3, 4, 7, 7, 8], 3, 5), [3, 3, 4]),
        ],
        hints=[
            "The answer is a contiguous window of length k in the sorted array.",
            "Binary search the window's left edge L in [0, n-k].",
            "Compare x - arr[mid] with arr[mid+k] - x: if the left end is farther, move lo = mid+1, else hi = mid.",
        ],
        pattern="Binary search for a window start (compare the two boundary elements)",
        explain=(
            "Sortedness means the k closest are adjacent. Shifting the window right is better exactly when its new "
            "right end is closer than its old left end."
        ),
        cx="O(log(n-k) + k) time",
        brute_cx="O(n log n) time (sort by distance)",
        brute=r"""
# BRUTE FORCE: O(n log n) time (sort by distance)
def find_closest_elements(arr, k, x):
    return sorted(sorted(arr, key=lambda v: (abs(v - x), v))[:k])
""",
        solution=r"""
# OPTIMISED: O(log(n-k) + k) time
# Idea: Binary search for a window start (compare the two boundary elements)
def find_closest_elements(arr, k, x):
    lo, hi = 0, len(arr) - k

    while lo < hi:
        mid = (lo + hi) // 2
        if x - arr[mid] > arr[mid + k] - x:
            lo = mid + 1
        else:
            hi = mid

    return arr[lo : lo + k]
""",
    ),
    # ---- Find Smallest Letter Greater Than Target (LeetCode 744) ----
    dict(
        title="Find Smallest Letter Greater Than Target",
        diff="E",
        lc=744,
        slug="find-smallest-letter-greater-than-target",
        prompt=(
            "Given a sorted list of lowercase letters (wrapping around), return the smallest letter strictly "
            "greater than target; wrap to the first if none."
        ),
        sig="def next_greatest_letter(letters: List[str], target: str) -> str:",
        fn="next_greatest_letter",
        tests=[
            ((["c", "f", "j"], "a"), "c"),
            ((["c", "f", "j"], "c"), "f"),
            ((["x", "x", "y", "y"], "z"), "x"),
            ((["a", "b"], "b"), "a"),
            ((["e", "e", "e", "k", "q"], "e"), "k"),
        ],
        hints=[
            "You want the first element > target: an upper bound.",
            "bisect_right(letters, target) gives that index.",
            "If the index equals len(letters) wrap to 0 (use % len).",
        ],
        pattern="Upper-bound binary search (first element strictly greater)",
        explain="Lower bound = first >= x, upper bound = first > x. Wrapping around is just the index modulo n.",
        cx="O(log n) time, O(1) space",
        brute_cx="O(n) time",
        brute=r"""
# BRUTE FORCE: O(n) time
def next_greatest_letter(letters, target):
    for c in letters:
        if c > target:
            return c
    return letters[0]
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Upper-bound binary search (first element strictly greater)
def next_greatest_letter(letters, target):
    lo, hi = 0, len(letters)

    while lo < hi:
        mid = (lo + hi) // 2
        if letters[mid] <= target:
            lo = mid + 1
        else:
            hi = mid

    return letters[lo % len(letters)]
""",
    ),
]
