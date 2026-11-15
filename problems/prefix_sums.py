from core import *

PROBLEMS = [
    dict(
        title="Find Pivot Index", diff="E", lc=724, slug="find-pivot-index",
        prompt="Return the leftmost index where the sum of everything strictly to its left equals the sum "
               "of everything strictly to its right (an empty side sums to 0). Return -1 if none.",
        sig="def pivot_index(nums: List[int]) -> int:",
        fn="pivot_index",
        tests=[(([1, 7, 3, 6, 5, 6],), 3), (([1, 2, 3],), -1), (([2, 1, -1],), 0), (([0],), 0), (([-1, -1, 0, 1, 1, 0],), 5)],
        hints=["Recomputing left and right sums for each index is O(n^2).",
               "left_sum(i) + nums[i] + right_sum(i) = total. So right_sum is derivable from left_sum.",
               "Walk once keeping left; pivot when left == total - left - nums[i]."],
        pattern="Prefix sum (running total) with total-minus-left trick",
        explain="""
        total = left + x + right, so right = total - left - x. Keep a running `left`; no second pass needed.
        Time O(n), space O(1).""",
        solution=r'''
def pivot_index(nums):
    total, left = sum(nums), 0
    for i, x in enumerate(nums):
        if left == total - left - x:
            return i
        left += x
    return -1
''',
    ),
    dict(
        title="Product of Array Except Self", diff="M", lc=238, slug="product-of-array-except-self",
        prompt="Return an array where out[i] is the product of all elements except nums[i]. "
               "No division allowed, O(n) time.",
        sig="def product_except_self(nums: List[int]) -> List[int]:",
        fn="product_except_self",
        tests=[(([1, 2, 3, 4],), [24, 12, 8, 6]), (([-1, 1, 0, -3, 3],), [0, 0, 9, 0, 0]), (([2, 3],), [3, 2]),
               (([0, 0, 2],), [0, 0, 0])],
        hints=["out[i] = (product of everything left of i) * (product of everything right of i).",
               "That is a prefix PRODUCT and a suffix PRODUCT - same idea as prefix sums.",
               "First pass fills out[i] with left products; second pass multiplies a running right product in."],
        pattern="Prefix / suffix accumulation (prefix idea works for any associative operation)",
        explain="""
        Division is unsafe (zeros). Split the 'everything except me' into two independent halves: the prefix
        product before i and the suffix product after i. Store prefix products in the output array, then sweep
        from the right with a running suffix product. Time O(n), extra space O(1) beyond the output.""",
        solution=r'''
def product_except_self(nums):
    n = len(nums)
    out = [1] * n
    left = 1
    for i in range(n):            # out[i] = product of nums[:i]
        out[i] = left
        left *= nums[i]
    right = 1
    for i in range(n - 1, -1, -1):  # multiply by product of nums[i+1:]
        out[i] *= right
        right *= nums[i]
    return out
''',
    ),
    dict(
        title="Subarray Sum Equals K", diff="M", lc=560, slug="subarray-sum-equals-k",
        prompt="Count the contiguous subarrays of an integer array (it may contain negatives) whose sum is exactly k.",
        sig="def subarray_sum(nums: List[int], k: int) -> int:",
        fn="subarray_sum",
        tests=[(([1, 1, 1], 2), 2), (([1, 2, 3], 3), 2), (([1, -1, 0], 0), 3), (([1, 2, 3, -3, 3], 3), 5), (([], 0), 0)],
        hints=["sum(l..r) = prefix[r+1] - prefix[l]. We want that to equal k.",
               "Rearranged: prefix[l] = prefix[r+1] - k. For each right end, how many earlier prefixes equal that?",
               "dict: prefix value -> how many times seen. Start with {0: 1} (empty prefix). Sliding window fails because of negatives."],
        pattern="Prefix sum + hash map of counts ('how many earlier prefixes equal current - k?')",
        explain="""
        A subarray sum is a difference of two prefix sums. Counting pairs (l < r) with
        P[r] - P[l] = k is a Two-Sum on prefix values, so a counter of prefixes seen so far answers each
        right end in O(1). Seed with {0: 1} so subarrays starting at index 0 are counted.
        Time O(n), space O(n).""",
        solution=r'''
def subarray_sum(nums, k):
    seen = defaultdict(int)
    seen[0] = 1                      # empty prefix
    pref = ans = 0
    for x in nums:
        pref += x
        ans += seen[pref - k]        # earlier prefixes that make a subarray of sum k ending here
        seen[pref] += 1
    return ans
''',
    ),
]
