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
    # ---- Search Insert Position (LeetCode 35) ----
    dict(
        title="Search Insert Position",
        diff="E",
        lc=35,
        slug="search-insert-position",
        prompt=(
            "Sorted array of distinct integers. Return the index of target, or the index where it would be inserted "
            "to keep the array sorted."
        ),
        sig="def search_insert(nums: List[int], target: int) -> int:",
        fn="search_insert",
        tests=[
            (([1, 3, 5, 6], 5), 2),
            (([1, 3, 5, 6], 2), 1),
            (([1, 3, 5, 6], 7), 4),
            (([1, 3, 5, 6], 0), 0),
            (([1], 1), 0),
            (([], 3), 0),
        ],
        hints=[
            "Linear scan is O(n). The array is sorted.",
            "You want the FIRST index whose value is >= target (the 'lower bound').",
            "Binary search with lo=0, hi=n; if nums[mid] < target: lo=mid+1 else hi=mid. Return lo.",
        ],
        pattern="Binary search for the lower bound (first index satisfying a monotone predicate)",
        explain=(
            "'nums[i] >= target' is False...False True...True. Binary search finds the boundary. Using "
            "half-open\n        [lo, hi) with hi = n lets the answer n mean 'past the end'. Master this template: "
            "nearly every binary-search\n        problem is a lower-bound search on some monotone predicate."
        ),
        cx="O(log n) time, O(1) space",
        brute_cx="O(n) time - linear scan",
        brute=r"""
# BRUTE FORCE: O(n) time - linear scan
def search_insert(nums, target):
    for i, x in enumerate(nums):
        if x >= target:
            return i
    return len(nums)
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Binary search for the lower bound (first index satisfying a monotone predicate)
def search_insert(nums, target):
    lo, hi = 0, len(nums)

    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid

    return lo
""",
    ),
    # ---- Find First and Last Position of Element in Sorted Array (LeetCode 34) ----
    dict(
        title="Find First and Last Position of Element in Sorted Array",
        diff="M",
        lc=34,
        slug="find-first-and-last-position-of-element-in-sorted-array",
        prompt=(
            "Sorted array (duplicates allowed). Return [first, last] index of target, or [-1, -1]. Must be O(log n)."
        ),
        sig="def search_range(nums: List[int], target: int) -> List[int]:",
        fn="search_range",
        tests=[
            (([5, 7, 7, 8, 8, 10], 8), [3, 4]),
            (([5, 7, 7, 8, 8, 10], 6), [-1, -1]),
            (([], 0), [-1, -1]),
            (([1], 1), [0, 0]),
            (([2, 2], 2), [0, 1]),
        ],
        hints=[
            "Finding any occurrence with binary search then walking outward is O(n) in the worst case.",
            "First position = lower bound of target. Last position = (lower bound of target+1) - 1.",
            "Write one lower_bound(x) function and call it twice.",
        ],
        pattern="Two lower-bound searches (left edge, right edge)",
        explain=(
            "lower_bound(target) is the first index with value >= target; lower_bound(target+1) is one past the "
            "last\n        occurrence. If lower_bound(target) does not point at target, it is absent."
        ),
        cx="O(log n) time, O(1) space",
        brute_cx="O(n) time - scan",
        brute=r"""
# BRUTE FORCE: O(n) time - scan
def search_range(nums, target):
    idx = [i for i, x in enumerate(nums) if x == target]
    return [idx[0], idx[-1]] if idx else [-1, -1]
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Two lower-bound searches (left edge, right edge)
def search_range(nums, target):
    def lower(x):
        lo, hi = 0, len(nums)

        while lo < hi:
            mid = (lo + hi) // 2
            if nums[mid] < x:
                lo = mid + 1
            else:
                hi = mid

        return lo

    left = lower(target)

    if left == len(nums) or nums[left] != target:
        return [-1, -1]

    return [left, lower(target + 1) - 1]
""",
    ),
    # ---- Find Minimum in Rotated Sorted Array (LeetCode 153) ----
    dict(
        title="Find Minimum in Rotated Sorted Array",
        diff="M",
        lc=153,
        slug="find-minimum-in-rotated-sorted-array",
        prompt="A sorted array of distinct values was rotated at an unknown pivot. Return the minimum in O(log n).",
        sig="def find_min(nums: List[int]) -> int:",
        fn="find_min",
        tests=[
            (([3, 4, 5, 1, 2],), 1),
            (([4, 5, 6, 7, 0, 1, 2],), 0),
            (([11, 13, 15, 17],), 11),
            (([2, 1],), 1),
            (([1],), 1),
        ],
        hints=[
            "Compare nums[mid] with something fixed - which end tells you which half is 'normal'?",
            "If nums[mid] > nums[hi], the drop (minimum) is strictly to the right of mid.",
            "if nums[mid] > nums[hi]: lo = mid + 1 else hi = mid. Loop until lo == hi.",
        ],
        pattern="Binary search on a rotated array: compare mid with the right end",
        explain=(
            "Against the last element the array looks like: big...big small...small (the predicate 'nums[i] <= "
            "last' is\n        False...True). The minimum is the first True. So it is again a boundary search."
        ),
        cx="O(log n) time, O(1) space",
        brute_cx="O(n) time - min()",
        brute=r"""
# BRUTE FORCE: O(n) time - min()
def find_min(nums):
    return min(nums)
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Binary search on a rotated array: compare mid with the right end
def find_min(nums):
    lo, hi = 0, len(nums) - 1

    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid

    return nums[lo]
""",
    ),
    # ---- Sqrt(x) (LeetCode 69) ----
    dict(
        title="Sqrt(x)",
        diff="E",
        lc=69,
        slug="sqrtx",
        prompt="Return floor(sqrt(x)) for a non-negative integer x without using the sqrt function.",
        sig="def my_sqrt(x: int) -> int:",
        fn="my_sqrt",
        tests=[
            ((4,), 2),
            ((8,), 2),
            ((0,), 0),
            ((1,), 1),
            ((2147395599,), 46339),
            ((15,), 3),
            ((16,), 4),
        ],
        hints=[
            "Try candidates r = 0, 1, 2, ... until r*r > x. How many steps for x ~ 2^31?",
            "'r*r <= x' is True...True False...False. Where is the last True?",
            "Binary search r in [0, x]; keep the largest r with r*r <= x.",
        ],
        pattern="Binary search on the ANSWER (monotone predicate over candidate values)",
        explain=(
            "You are not searching an array but a range of candidate answers. The predicate r*r <= x is monotone, "
            "so\n        binary search applies. This 'search on answer' idea returns in Koko, Ship Packages and "
            "Split Array."
        ),
        cx="O(log x) time, O(1) space",
        brute_cx="O(sqrt x) time - try each r",
        brute=r"""
# BRUTE FORCE: O(sqrt x) time - try each r
def my_sqrt(x):
    r = 0
    while (r + 1) * (r + 1) <= x:
        r += 1
    return r
""",
        solution=r"""
# OPTIMISED: O(log x) time, O(1) space
# Idea: Binary search on the ANSWER (monotone predicate over candidate values)
def my_sqrt(x):
    lo, hi = 0, x

    while lo < hi:
        mid = (lo + hi + 1) // 2  # upper mid: we are looking for the LAST true
        if mid * mid <= x:
            lo = mid
        else:
            hi = mid - 1

    return lo
""",
    ),
    # ---- Search a 2D Matrix (LeetCode 74) ----
    dict(
        title="Search a 2D Matrix",
        diff="M",
        lc=74,
        slug="search-a-2d-matrix",
        prompt=(
            "Each row is sorted and the first value of each row is greater than the last of the previous row. "
            "Return True if target is in the matrix."
        ),
        sig="def search_matrix(matrix: List[List[int]], target: int) -> bool:",
        fn="search_matrix",
        tests=[
            (([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 3), True),
            (([[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]], 13), False),
            (([[1]], 1), True),
            (([[1]], 2), False),
            (([[1, 3]], 3), True),
        ],
        hints=[
            "Flatten it mentally: the whole matrix is one sorted sequence of m*n numbers.",
            "Index k in [0, m*n) maps to row k // n and column k % n.",
            "Run an ordinary binary search over k, reading matrix[k // n][k % n].",
        ],
        pattern="Binary search over a virtual 1D index (index arithmetic)",
        explain="Because rows chain end-to-start, no data is copied: just translate the 1D index to 2D on demand.",
        cx="O(log(m*n)) time, O(1) space",
        brute_cx="O(m*n) time - scan every cell",
        brute=r"""
# BRUTE FORCE: O(m*n) time - scan every cell
def search_matrix(matrix, target):
    return any(target in row for row in matrix)
""",
        solution=r"""
# OPTIMISED: O(log(m*n)) time, O(1) space
# Idea: Binary search over a virtual 1D index (index arithmetic)
def search_matrix(matrix, target):
    m, n = len(matrix), len(matrix[0])
    lo, hi = 0, m * n - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        v = matrix[mid // n][mid % n]

        if v == target:
            return True

        if v < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return False
""",
    ),
    # ---- Find Peak Element (LeetCode 162) ----
    dict(
        title="Find Peak Element",
        diff="M",
        lc=162,
        slug="find-peak-element",
        prompt=(
            "A peak is an element strictly greater than its neighbours (outside the array counts as -infinity). "
            "Return the index of ANY peak in O(log n). Adjacent elements are never equal."
        ),
        sig="def find_peak(nums: List[int]) -> int:",
        fn="find_peak",
        check=lambda args, got: (
            isinstance(got, int)
            and 0 <= got < len(args[0])
            and (got == 0 or args[0][got - 1] < args[0][got])
            and (got == len(args[0]) - 1 or args[0][got + 1] < args[0][got])
        ),
        tests=[
            (([1, 2, 3, 1],), 2),
            (([1, 2, 1, 3, 5, 6, 4],), 5),
            (([1],), 0),
            (([2, 1],), 0),
            (([1, 2],), 1),
            (([5, 4, 3, 2, 1],), 0),
        ],
        hints=[
            "The array is NOT sorted, yet binary search works. What does a slope tell you?",
            "If nums[mid] < nums[mid+1] you are going uphill - a peak must exist to the right.",
            "Uphill -> lo = mid + 1; otherwise hi = mid. Converge on lo == hi.",
        ],
        pattern="Binary search on a 'slope' (guarantee exists on one side)",
        explain=(
            "Because the ends are -infinity, walking uphill must eventually reach a peak. Following the slope "
            "halves the\n        search space each time even though the array is unsorted. Any valid peak is "
            "accepted, so tests use a validator."
        ),
        cx="O(log n) time, O(1) space",
        brute_cx="O(n) time - scan",
        brute=r"""
# BRUTE FORCE: O(n) time - scan
def find_peak(nums):
    for i in range(len(nums)):
        if (i == 0 or nums[i - 1] < nums[i]) and (i == len(nums) - 1 or nums[i + 1] < nums[i]):
            return i
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Binary search on a 'slope' (guarantee exists on one side)
def find_peak(nums):
    lo, hi = 0, len(nums) - 1

    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] < nums[mid + 1]:
            lo = mid + 1
        else:
            hi = mid

    return lo
""",
    ),
]
