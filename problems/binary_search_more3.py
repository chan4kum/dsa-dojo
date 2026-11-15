"""more Binary Search problems (batch 4) - part of the problem bank for the "binary_search" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Search in Rotated Sorted Array II (LeetCode 81) ----
    dict(
        title="Search in Rotated Sorted Array II",
        diff="M",
        lc=81,
        slug="search-in-rotated-sorted-array-ii",
        prompt=(
            "A sorted array (possibly with duplicates) was rotated at an unknown pivot. Return True if target is in it."
        ),
        sig="def search_rotated(nums: List[int], target: int) -> bool:",
        fn="search_rotated",
        tests=[
            (([2, 5, 6, 0, 0, 1, 2], 0), True),
            (([2, 5, 6, 0, 0, 1, 2], 3), False),
            (([1, 0, 1, 1, 1], 0), True),
            (([1], 0), False),
        ],
        hints=[
            "Without duplicates one half is always sorted - you can tell which by comparing nums[lo] and nums[mid].",
            "With duplicates, nums[lo] == nums[mid] == nums[hi] hides which half is sorted.",
            (
                "In that case shrink both ends by one (lo += 1, hi -= 1) and continue; otherwise use the sorted "
                "half to decide."
            ),
        ],
        pattern="Binary search on a rotated array (one half is always sorted)",
        explain=(
            "Duplicates can make the sorted half impossible to identify, so the worst case degrades to O(n) (e.g. "
            "all ones with a single zero). On typical data it stays O(log n)."
        ),
        cx="O(log n) average, O(n) worst case",
        brute_cx="O(n) time - linear scan",
        brute=r"""
# BRUTE FORCE: O(n) time - linear scan
def search_rotated(nums, target):
    return target in nums
""",
        solution=r"""
# OPTIMISED: O(log n) average, O(n) worst case
# Idea: Binary search on a rotated array (one half is always sorted)
def search_rotated(nums, target):
    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return True
        if nums[lo] == nums[mid] == nums[hi]:
            lo, hi = lo + 1, hi - 1  # cannot tell which half is sorted: shrink
        elif nums[lo] <= nums[mid]:  # the left half is sorted
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:  # the right half is sorted
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1
    return False
""",
    ),
    # ---- Find Minimum in Rotated Sorted Array II (LeetCode 154) ----
    dict(
        title="Find Minimum in Rotated Sorted Array II",
        diff="H",
        lc=154,
        slug="find-minimum-in-rotated-sorted-array-ii",
        prompt="A sorted array (possibly with duplicates) was rotated. Return its minimum element.",
        sig="def find_min(nums: List[int]) -> int:",
        fn="find_min",
        tests=[
            (([1, 3, 5],), 1),
            (([2, 2, 2, 0, 1],), 0),
            (([3, 1, 3],), 1),
            (([1],), 1),
            (([10, 1, 10, 10, 10],), 1),
        ],
        hints=[
            "Compare nums[mid] with nums[hi] (the right end).",
            (
                "If nums[mid] > nums[hi] the minimum is to the right of mid; if nums[mid] < nums[hi] it is at mid "
                "or to the left."
            ),
            (
                "If they are EQUAL we cannot tell - discard just nums[hi] (hi -= 1); the minimum is not lost "
                "because nums[mid] still holds the same value."
            ),
        ],
        pattern="Binary search against the right end, with a safe shrink on ties",
        explain=(
            "The equal case is the only one that cannot halve the range. Dropping one copy of a duplicated value is "
            "safe because an equal value remains at mid, so the minimum survives. Worst case O(n)."
        ),
        cx="O(log n) average, O(n) worst case",
        brute_cx="O(n) time - scan for the minimum",
        brute=r"""
# BRUTE FORCE: O(n) time - scan for the minimum
def find_min(nums):
    return min(nums)
""",
        solution=r"""
# OPTIMISED: O(log n) average, O(n) worst case
# Idea: Binary search against the right end, with a safe shrink on ties
def find_min(nums):
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1  # the minimum is strictly right of mid
        elif nums[mid] < nums[hi]:
            hi = mid  # mid could be the minimum
        else:
            hi -= 1  # a tie: dropping one copy of the value is safe
    return nums[lo]
""",
    ),
    # ---- Minimum Number of Days to Make m Bouquets (LeetCode 1482) ----
    dict(
        title="Minimum Number of Days to Make m Bouquets",
        diff="M",
        lc=1482,
        slug="minimum-number-of-days-to-make-m-bouquets",
        prompt=(
            "Flower i blooms on day bloom_day[i]. A bouquet needs k ADJACENT bloomed flowers. Return the earliest "
            "day you can make m bouquets, or -1 if impossible."
        ),
        sig="def min_days(bloom_day: List[int], m: int, k: int) -> int:",
        fn="min_days",
        tests=[
            (([1, 10, 3, 10, 2], 3, 1), 3),
            (([1, 10, 3, 10, 2], 3, 2), -1),
            (([7, 7, 7, 7, 12, 7, 7], 2, 3), 12),
            (([1, 10, 2, 9, 3, 8, 4, 7, 5, 6], 4, 2), 9),
        ],
        hints=[
            "If m * k > n it is impossible: return -1.",
            "Feasibility is monotone: if you can make m bouquets on day d, you can on every later day.",
            (
                "Binary search the day. To test a day, sweep the array counting runs of bloomed flowers, forming a "
                "bouquet every k."
            ),
        ],
        pattern="Binary search on the answer + a greedy feasibility check",
        explain=(
            "The answer is one of the bloom days. A yes/no test for a given day is a single greedy scan, and "
            "because the test is monotone in the day, binary search finds the first 'yes'."
        ),
        cx="O(n log(max day)) time",
        brute_cx="O(n * D) time - test each distinct bloom day in increasing order",
        brute=r"""
# BRUTE FORCE: O(n * D) time - test each distinct bloom day in increasing order
def min_days(bloom_day, m, k):
    def bouquets(day):
        count = run = 0
        for b in bloom_day:
            run = run + 1 if b <= day else 0  # current streak of bloomed flowers
            if run == k:
                count += 1
                run = 0
        return count

    for day in sorted(set(bloom_day)):  # try the days in increasing order
        if bouquets(day) >= m:
            return day
    return -1
""",
        solution=r"""
# OPTIMISED: O(n log(max day)) time
# Idea: Binary search on the answer + a greedy feasibility check
def min_days(bloom_day, m, k):
    if m * k > len(bloom_day):
        return -1

    def enough(day):  # can we make m bouquets by this day?
        count = run = 0
        for b in bloom_day:
            run = run + 1 if b <= day else 0
            if run == k:
                count += 1
                run = 0
        return count >= m

    lo, hi = min(bloom_day), max(bloom_day)
    while lo < hi:
        mid = (lo + hi) // 2
        if enough(mid):
            hi = mid  # mid works: look for something earlier
        else:
            lo = mid + 1
    return lo
""",
    ),
    # ---- Peak Index in a Mountain Array (LeetCode 852) ----
    dict(
        title="Peak Index in a Mountain Array",
        diff="M",
        lc=852,
        slug="peak-index-in-a-mountain-array",
        prompt=(
            "arr strictly increases to one peak and then strictly decreases (length >= 3). Return the index of the "
            "peak."
        ),
        sig="def peak_index_in_mountain_array(arr: List[int]) -> int:",
        fn="peak_index_in_mountain_array",
        tests=[
            (([0, 1, 0],), 1),
            (([0, 2, 1, 0],), 1),
            (([0, 10, 5, 2],), 1),
            (([3, 4, 5, 1],), 2),
        ],
        hints=[
            "A linear scan finds the maximum in O(n) - good, but the structure allows better.",
            "Look at arr[mid] and arr[mid + 1]: if it is still rising, the peak is to the right.",
            "If arr[mid] > arr[mid + 1], mid could be the peak, so keep it (hi = mid). Stop when lo == hi.",
        ],
        pattern="Binary search on a slope (rising vs falling)",
        explain=(
            "The sequence of comparisons 'arr[i] < arr[i+1]' is True...True, False...False. Binary search finds the "
            "boundary where it flips, and that boundary is the peak."
        ),
        cx="O(log n) time",
        brute_cx="O(n) time - find the index of the maximum",
        brute=r"""
# BRUTE FORCE: O(n) time - find the index of the maximum
def peak_index_in_mountain_array(arr):
    return arr.index(max(arr))
""",
        solution=r"""
# OPTIMISED: O(log n) time
# Idea: Binary search on a slope (rising vs falling)
def peak_index_in_mountain_array(arr):
    lo, hi = 0, len(arr) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] < arr[mid + 1]:
            lo = mid + 1  # still climbing: the peak is to the right
        else:
            hi = mid  # descending: mid may be the peak
    return lo
""",
    ),
    # ---- Find the Smallest Divisor Given a Threshold (LeetCode 1283) ----
    dict(
        title="Find the Smallest Divisor Given a Threshold",
        diff="M",
        lc=1283,
        slug="find-the-smallest-divisor-given-a-threshold",
        prompt=(
            "Choose a positive integer divisor d, divide every number by d rounding UP, and add the results. Return "
            "the smallest d for which the sum is <= threshold."
        ),
        sig="def smallest_divisor(nums: List[int], threshold: int) -> int:",
        fn="smallest_divisor",
        tests=[
            (([1, 2, 5, 9], 6), 5),
            (([44, 22, 33, 11, 1], 5), 44),
            (([2, 3, 5, 7, 11], 11), 3),
            (([19], 5), 4),
        ],
        hints=[
            "A bigger divisor makes the sum smaller (or equal) - the property is monotone.",
            "The answer is between 1 and max(nums).",
            (
                "Binary search d; to test d compute sum(ceil(x / d)) and compare with the threshold. ceil(x / d) = "
                "(x + d - 1) // d."
            ),
        ],
        pattern="Binary search on the answer (monotone predicate)",
        explain=(
            "Whenever 'is x big enough?' flips from False to True exactly once, you can binary search x instead of "
            "scanning. Each check costs one pass over the array."
        ),
        cx="O(n log max) time",
        brute_cx="O(n * max) time - try d = 1, 2, 3, ...",
        brute=r"""
# BRUTE FORCE: O(n * max) time - try d = 1, 2, 3, ...
def smallest_divisor(nums, threshold):
    d = 1
    while sum(-(-x // d) for x in nums) > threshold:  # -(-x // d) is ceil(x / d)
        d += 1
    return d
""",
        solution=r"""
# OPTIMISED: O(n log max) time
# Idea: Binary search on the answer (monotone predicate)
def smallest_divisor(nums, threshold):
    lo, hi = 1, max(nums)
    while lo < hi:
        mid = (lo + hi) // 2
        if sum((x + mid - 1) // mid for x in nums) <= threshold:
            hi = mid  # mid is good enough; try smaller
        else:
            lo = mid + 1
    return lo
""",
    ),
    # ---- Kth Missing Positive Number (LeetCode 1539) ----
    dict(
        title="Kth Missing Positive Number",
        diff="E",
        lc=1539,
        slug="kth-missing-positive-number",
        prompt=(
            "arr is a sorted list of distinct positive integers. Return the k-th positive integer that is missing "
            "from arr."
        ),
        sig="def find_kth_positive(arr: List[int], k: int) -> int:",
        fn="find_kth_positive",
        tests=[
            (([2, 3, 4, 7, 11], 5), 9),
            (([1, 2, 3, 4], 2), 6),
            (([5], 1), 1),
            (([1, 3], 1), 2),
        ],
        hints=[
            "At index i, exactly arr[i] - (i + 1) positive numbers are missing before arr[i].",
            "That count never decreases as i grows - binary search for the first index where it reaches k.",
            "If lo is the number of elements with missing-count < k, the answer is lo + k.",
        ],
        pattern="Binary search on 'how many are missing so far'",
        explain=(
            "Counting the elements that still have fewer than k numbers missing before them tells how far the k-th "
            "gap is shifted: answer = k + (number of such elements)."
        ),
        cx="O(log n) time",
        brute_cx="O(n + k) time - walk through 1, 2, 3, ... counting missing numbers",
        brute=r"""
# BRUTE FORCE: O(n + k) time - walk through 1, 2, 3, ... counting missing numbers
def find_kth_positive(arr, k):
    present, n = set(arr), 0
    while True:
        n += 1
        if n not in present:
            k -= 1  # one more missing number found
            if k == 0:
                return n
""",
        solution=r"""
# OPTIMISED: O(log n) time
# Idea: Binary search on 'how many are missing so far'
def find_kth_positive(arr, k):
    lo, hi = 0, len(arr)
    while lo < hi:
        mid = (lo + hi) // 2
        if arr[mid] - (mid + 1) < k:  # fewer than k numbers missing before arr[mid]
            lo = mid + 1
        else:
            hi = mid
    return lo + k  # lo elements precede the k-th gap
""",
    ),
]
