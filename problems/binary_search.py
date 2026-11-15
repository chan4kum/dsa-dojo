"""Binary Search problems - the problem bank for the "binary_search" topic.

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
    # ---- Binary Search (LeetCode 704) ----
    dict(
        title="Binary Search",
        diff="E",
        lc=704,
        slug="binary-search",
        prompt=(
            "Given a sorted array of distinct integers and a target, return the target's index or -1. Must be O(log n)."
        ),
        sig="def search(nums: List[int], target: int) -> int:",
        fn="search",
        tests=[
            (([-1, 0, 3, 5, 9, 12], 9), 4),
            (([-1, 0, 3, 5, 9, 12], 2), -1),
            (([5], 5), 0),
            (([5], 3), -1),
            (([1, 2], 2), 1),
        ],
        hints=[
            "Each comparison with the middle element lets you throw away half of the remaining range.",
            (
                "Keep a closed range [lo, hi]; mid = (lo+hi)//2; if nums[mid] < target the answer (if any) is right "
                "of mid."
            ),
            "Loop while lo <= hi, and always move past mid (mid+1 / mid-1) or you can loop forever.",
        ],
        pattern="Binary search on a sorted index range",
        explain=(
            "The invariant: if target exists, it lies inside [lo, hi]. Each step cuts the range at least in half, "
            "so\n        O(log n). The two classic bugs are infinite loops (not moving past mid) and off-by-one on "
            "the loop\n        condition - decide on closed [lo, hi] vs half-open [lo, hi) once and stay consistent."
        ),
        cx="O(log n) time, O(1) space",
        brute_cx="O(n) - linear scan ignores the sorted order",
        brute=r"""
# BRUTE FORCE: O(n) - linear scan ignores the sorted order
def search(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Binary search on a sorted index range
def search(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    return -1
""",
    ),
    # ---- Search in Rotated Sorted Array (LeetCode 33) ----
    dict(
        title="Search in Rotated Sorted Array",
        diff="M",
        lc=33,
        slug="search-in-rotated-sorted-array",
        prompt=(
            "A sorted array of distinct values was rotated at an unknown pivot (e.g. [4,5,6,7,0,1,2]). Find a "
            "target's index in O(log n), or -1."
        ),
        sig="def search_rotated(nums: List[int], target: int) -> int:",
        fn="search_rotated",
        tests=[
            (([4, 5, 6, 7, 0, 1, 2], 0), 4),
            (([4, 5, 6, 7, 0, 1, 2], 3), -1),
            (([1], 0), -1),
            (([1], 1), 0),
            (([3, 1], 1), 1),
            (([5, 1, 3], 5), 0),
        ],
        hints=[
            "After splitting at mid, at least one half is still perfectly sorted. Which one, and how can you tell?",
            "If nums[lo] <= nums[mid], the left half [lo..mid] is sorted; otherwise the right half is.",
            (
                "Check whether target lies inside the sorted half's value range; if yes go there, else go to the "
                "other half."
            ),
        ],
        pattern="Binary search with 'which half is sorted?' reasoning",
        explain=(
            "Rotation breaks global order but not local order: one of the two halves around mid is always "
            "sorted.\n        In the sorted half we can test membership by comparing against its endpoints, so we "
            "always know which\n        half to keep. O(log n)."
        ),
        cx="O(log n) time, O(1) space",
        brute_cx="O(n) - linear scan",
        brute=r"""
# BRUTE FORCE: O(n) - linear scan
def search_rotated(nums, target):
    return nums.index(target) if target in nums else -1
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Binary search with 'which half is sorted?' reasoning
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid
        if nums[lo] <= nums[mid]:  # left half sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # right half sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return -1
""",
    ),
    # ---- Koko Eating Bananas (LeetCode 875) ----
    dict(
        title="Koko Eating Bananas",
        diff="M",
        lc=875,
        slug="koko-eating-bananas",
        prompt=(
            "Piles of bananas must all be eaten within h hours. Each hour you pick one pile and eat up to k bananas "
            "from it. Return the smallest integer speed k that finishes in time."
        ),
        sig="def min_eating_speed(piles: List[int], h: int) -> int:",
        fn="min_eating_speed",
        tests=[
            (([3, 6, 7, 11], 8), 4),
            (([30, 11, 23, 4, 20], 5), 30),
            (([30, 11, 23, 4, 20], 6), 23),
            (([1], 1), 1),
            (([1000000000], 2), 500000000),
        ],
        hints=[
            "Try to answer the opposite question: given a speed k, can she finish in h hours?",
            "If speed k works, every larger speed works too. That monotonic yes/no is what you can binary search.",
            "Search k in [1, max(piles)] for the smallest k with sum(ceil(p/k)) <= h.",
        ],
        pattern="Binary search on the ANSWER (monotonic feasibility predicate)",
        explain=(
            "We are not searching an array; we are searching the space of answers. feasible(k) is "
            "False...False\n        True...True, so the boundary is found with a lower-bound style search. Cost: "
            "O(n log max(piles)).\n        Spot it by: 'minimise the maximum / smallest value such that ...' plus "
            "an easy O(n) check."
        ),
        cx="O(n log max(piles)) time, O(1) space",
        brute_cx="O(max(piles) * n) - tries every speed in turn",
        brute=r"""
# BRUTE FORCE: O(max(piles) * n) - tries every speed in turn
def min_eating_speed(piles, h):
    k = 1
    while sum(-(-p // k) for p in piles) > h:
        k += 1
    return k
""",
        solution=r"""
# OPTIMISED: O(n log max(piles)) time, O(1) space
# Idea: Binary search on the ANSWER (monotonic feasibility predicate)
def min_eating_speed(piles, h):
    def feasible(k):
        return sum(-(-p // k) for p in piles) <= h  # ceil(p / k) without floats

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if feasible(mid):
            hi = mid  # mid works: try smaller (keep mid)
        else:
            lo = mid + 1
    return lo
""",
    ),
    # ---- Split Array Largest Sum (LeetCode 410) ----
    dict(
        title="Split Array Largest Sum",
        diff="H",
        lc=410,
        slug="split-array-largest-sum",
        prompt=(
            "Split an array of non-negative integers into k non-empty contiguous parts so that the largest part-sum "
            "is as small as possible. Return that minimised largest sum."
        ),
        sig="def split_array(nums: List[int], k: int) -> int:",
        fn="split_array",
        tests=[
            (([7, 2, 5, 10, 8], 2), 18),
            (([1, 2, 3, 4, 5], 2), 9),
            (([1, 4, 4], 3), 4),
            (([10], 1), 10),
            (([2, 3, 1, 2, 4, 3], 5), 4),
        ],
        hints=[
            "'Minimise the maximum' is the classic signal for binary search on the answer.",
            "Given a cap C, greedily pack elements into a part until adding the next would exceed C; count parts.",
            "feasible(C) = parts needed <= k. Search C in [max(nums), sum(nums)].",
        ],
        pattern="Binary search on the answer + greedy feasibility check",
        explain=(
            "The answer lies between max(nums) (a part must hold the biggest element) and sum(nums) (one "
            "part).\n        For a cap C, greedy packing minimises the number of parts, so feasibility is monotone "
            "in C. Binary\n        search the smallest feasible C. Time O(n log(sum)). (A DP exists but is O(k "
            "n^2).)"
        ),
        cx="O(n log sum) time, O(1) space",
        brute_cx="O(sum * n) - tries every cap upward",
        brute=r"""
# BRUTE FORCE: O(sum * n) - tries every cap upward
def split_array(nums, k):
    def parts(cap):
        c, cur = 1, 0
        for x in nums:
            if cur + x > cap:
                c, cur = c + 1, x
            else:
                cur += x
        return c

    cap = max(nums)
    while parts(cap) > k:
        cap += 1
    return cap
""",
        solution=r"""
# OPTIMISED: O(n log sum) time, O(1) space
# Idea: Binary search on the answer + greedy feasibility check
def split_array(nums, k):
    def parts_needed(cap):
        parts, cur = 1, 0
        for x in nums:
            if cur + x > cap:
                parts += 1
                cur = x
            else:
                cur += x
        return parts

    lo, hi = max(nums), sum(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if parts_needed(mid) <= k:
            hi = mid
        else:
            lo = mid + 1
    return lo
""",
    ),
    # ---- Median of Two Sorted Arrays (LeetCode 4) ----
    dict(
        title="Median of Two Sorted Arrays",
        diff="H",
        lc=4,
        slug="median-of-two-sorted-arrays",
        prompt="Given two sorted arrays, return the median of all their elements combined, in O(log(min(m, n))) time.",
        sig="def find_median(a: List[int], b: List[int]) -> float:",
        fn="find_median",
        compare="float",
        tests=[
            (([1, 3], [2]), 2.0),
            (([1, 2], [3, 4]), 2.5),
            (([], [1]), 1.0),
            (([0, 0], [0, 0]), 0.0),
            (([2], []), 2.0),
            (([1, 3, 5, 7], [2, 4, 6]), 4.0),
        ],
        hints=[
            "The median splits the merged order into a left half and a right half of (almost) equal size.",
            "Choose how many elements i of the SMALLER array go left; then j = half - i come from the other one.",
            "Binary search i until max(left parts) <= min(right parts): aL <= bR and bL <= aR.",
        ],
        pattern="Binary search on a partition point (not on values)",
        explain=(
            "A correct split satisfies: everything on the left <= everything on the right. Since each array "
            "is\n        sorted, only the cross checks aL <= bR and bL <= aR are needed. If aL > bR we took too "
            "many from a\n        -> move i left; else move right. Use +/-infinity sentinels for empty sides."
        ),
        cx="O(log min(m, n)) time, O(1) space",
        brute_cx="O((m+n) log(m+n)) - merge and sort",
        brute=r"""
# BRUTE FORCE: O((m+n) log(m+n)) - merge and sort
def find_median(a, b):
    m = sorted(a + b)
    n = len(m)
    return float(m[n // 2]) if n % 2 else (m[n // 2 - 1] + m[n // 2]) / 2
""",
        solution=r"""
# OPTIMISED: O(log min(m, n)) time, O(1) space
# Idea: Binary search on a partition point (not on values)
def find_median(a, b):
    if len(a) > len(b):
        a, b = b, a
    m, n = len(a), len(b)
    half = (m + n + 1) // 2
    lo, hi = 0, m
    while lo <= hi:
        i = (lo + hi) // 2  # elements taken from a
        j = half - i  # elements taken from b
        aL = a[i - 1] if i > 0 else float("-inf")
        aR = a[i] if i < m else float("inf")
        bL = b[j - 1] if j > 0 else float("-inf")
        bR = b[j] if j < n else float("inf")
        if aL <= bR and bL <= aR:
            if (m + n) % 2:
                return float(max(aL, bL))
            return (max(aL, bL) + min(aR, bR)) / 2
        if aL > bR:
            hi = i - 1
        else:
            lo = i + 1
""",
    ),
]
