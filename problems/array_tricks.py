from core import *

PROBLEMS = [
    dict(
        title="Maximum Subarray", diff="M", lc=53, slug="maximum-subarray",
        prompt="Find the contiguous, non-empty subarray with the largest sum and return that sum.",
        sig="def max_subarray(nums: List[int]) -> int:",
        fn="max_subarray",
        tests=[(([-2, 1, -3, 4, -1, 2, 1, -5, 4],), 6), (([1],), 1), (([5, 4, -1, 7, 8],), 23), (([-3, -1, -2],), -1)],
        hints=["Checking all subarrays is O(n^2). Think about the best subarray that ENDS at index i.",
               "best_ending_here(i) is either nums[i] alone, or nums[i] + best_ending_here(i-1). Which is larger?",
               "cur = max(x, cur + x); answer = max over all cur. Initialise with nums[0], not 0 (all-negative input)."],
        pattern="Kadane's algorithm (1-D DP: best subarray ending here)",
        explain="""
        If the best sum ending at i-1 is negative, carrying it forward only hurts, so restart at i. That single
        decision per element gives O(n) time, O(1) space. It is a DP with state 'best ending at i'.""",
        solution=r'''
def max_subarray(nums):
    cur = best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)       # extend the previous subarray, or restart here
        best = max(best, cur)
    return best
''',
    ),
    dict(
        title="Missing Number", diff="E", lc=268, slug="missing-number",
        prompt="An array holds n distinct numbers taken from 0..n. Return the one number in that range that is missing.",
        sig="def missing_number(nums: List[int]) -> int:",
        fn="missing_number",
        tests=[(([3, 0, 1],), 2), (([0, 1],), 2), (([9, 6, 4, 2, 3, 5, 7, 0, 1],), 8), (([0],), 1)],
        hints=["A set works in O(n) space. Can arithmetic do it in O(1)?",
               "Sum of 0..n is n(n+1)/2. What is the difference with the actual sum?",
               "Alternative: XOR all indices and values - pairs cancel, the missing number remains."],
        pattern="Math / XOR cancellation (range is known, so use the invariant)",
        explain="""
        Because the universe 0..n is known, expected_sum - actual_sum = the missing value. XOR gives the same
        without overflow worries in other languages. O(n) time, O(1) space.""",
        solution=r'''
def missing_number(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)
''',
    ),
    dict(
        title="First Missing Positive", diff="H", lc=41, slug="first-missing-positive",
        prompt="Given an unsorted integer array, return the smallest positive integer that does not appear in it. "
               "Aim for O(n) time and O(1) extra space.",
        sig="def first_missing_positive(nums: List[int]) -> int:",
        fn="first_missing_positive",
        tests=[(([1, 2, 0],), 3), (([3, 4, -1, 1],), 2), (([7, 8, 9, 11, 12],), 1), (([1],), 2), (([2, 1],), 3),
               (([1, 1],), 2)],
        hints=["The answer is always in 1..n+1 (n = length). Why?",
               "Use the array itself as a hash table: value v belongs at index v-1.",
               "Cyclic placement: while nums[i] is in 1..n and not already at its home, swap it home. Then the first i with nums[i] != i+1 gives i+1."],
        pattern="Cyclic sort / in-place hashing (index = value - 1)",
        explain="""
        With n slots only the values 1..n matter; anything else can be ignored. Swap each useful value into
        its home slot (each swap places one value for good, so total swaps <= n). A second scan finds the
        first slot whose value is wrong. The duplicate check nums[v-1] != v prevents infinite loops.""",
        solution=r'''
def first_missing_positive(nums):
    n = len(nums)
    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            j = nums[i] - 1
            nums[i], nums[j] = nums[j], nums[i]    # send nums[i] to its home slot
    for i in range(n):
        if nums[i] != i + 1:
            return i + 1
    return n + 1
''',
    ),
]
