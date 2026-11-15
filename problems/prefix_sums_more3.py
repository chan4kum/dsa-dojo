"""more Prefix Sums problems (batch 4) - part of the problem bank for the "prefix_sums" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Running Sum of 1d Array (LeetCode 1480) ----
    dict(
        title="Running Sum of 1d Array",
        diff="E",
        lc=1480,
        slug="running-sum-of-1d-array",
        prompt="Return an array where result[i] = nums[0] + ... + nums[i].",
        sig="def running_sum(nums: List[int]) -> List[int]:",
        fn="running_sum",
        tests=[
            (([1, 2, 3, 4],), [1, 3, 6, 10]),
            (([1, 1, 1, 1, 1],), [1, 2, 3, 4, 5]),
            (([3, 1, 2, 10, 1],), [3, 4, 6, 16, 17]),
            (([],), []),
        ],
        hints=[
            "result[i] = result[i - 1] + nums[i].",
            "Keep one running total instead of re-adding the prefix every time.",
            "itertools.accumulate does exactly this.",
        ],
        pattern="Prefix sum (the base of every range-sum trick)",
        explain=(
            "Each prefix extends the previous one by a single element, so the whole array costs O(n) rather than "
            "O(n^2)."
        ),
        cx="O(n) time",
        brute_cx="O(n^2) time - re-add the entire prefix for every index",
        brute=r"""
# BRUTE FORCE: O(n^2) time - re-add the entire prefix for every index
def running_sum(nums):
    return [sum(nums[: i + 1]) for i in range(len(nums))]
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Prefix sum (the base of every range-sum trick)
def running_sum(nums):
    total, result = 0, []
    for x in nums:
        total += x
        result.append(total)
    return result
""",
    ),
    # ---- Sum of All Odd Length Subarrays (LeetCode 1588) ----
    dict(
        title="Sum of All Odd Length Subarrays",
        diff="E",
        lc=1588,
        slug="sum-of-all-odd-length-subarrays",
        prompt="Return the sum of all subarrays of arr that have odd length.",
        sig="def sum_odd_length_subarrays(arr: List[int]) -> int:",
        fn="sum_odd_length_subarrays",
        tests=[
            (([1, 4, 2, 5, 3],), 58),
            (([1, 2],), 3),
            (([10, 11, 12],), 66),
            (([7],), 7),
        ],
        hints=[
            "Brute force lists every odd-length subarray and adds it up.",
            "Count, for each element, how many odd-length subarrays contain it.",
            (
                "Element i has (i + 1) choices of start and (n - i) choices of end; about half of those "
                "combinations give an odd length: ((i + 1) * (n - i) + 1) // 2."
            ),
        ],
        pattern="Contribution counting: how many subarrays contain each element",
        explain=(
            "Rather than enumerate subarrays, count each element's appearances. Start/end choices are independent "
            "and the parity of the length splits them (almost) evenly, with the rounding up covering the odd count "
            "case."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^3) time - enumerate and sum every odd-length subarray",
        brute=r"""
# BRUTE FORCE: O(n^3) time - enumerate and sum every odd-length subarray
def sum_odd_length_subarrays(arr):
    total = 0
    for i in range(len(arr)):
        for j in range(i, len(arr), 2):  # j - i is even, so the length j - i + 1 is odd
            total += sum(arr[i : j + 1])
    return total
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Contribution counting: how many subarrays contain each element
def sum_odd_length_subarrays(arr):
    n = len(arr)
    return sum(x * (((i + 1) * (n - i) + 1) // 2) for i, x in enumerate(arr))
""",
    ),
]
