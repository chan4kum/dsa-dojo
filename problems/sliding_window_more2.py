"""extra batch of Sliding Window problems - the problem bank for the "sliding_window" topic.

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
    # ---- Subarray Product Less Than K (LeetCode 713) ----
    dict(
        title="Subarray Product Less Than K",
        diff="M",
        lc=713,
        slug="subarray-product-less-than-k",
        prompt="Count the contiguous subarrays of positive integers whose product is strictly less than k.",
        sig="def num_subarray_product_less_than_k(nums: List[int], k: int) -> int:",
        fn="num_subarray_product_less_than_k",
        tests=[
            (([10, 5, 2, 6], 100), 8),
            (([1, 2, 3], 0), 0),
            (([1, 1, 1], 2), 6),
            (([100], 100), 0),
            (([], 5), 0),
            (([2, 3, 4], 1000), 6),
        ],
        hints=[
            "All values are positive, so growing the window only increases the product.",
            "Slide a window [l, r]; shrink from the left while product >= k.",
            "For each r the number of valid subarrays ENDING at r is r - l + 1. Add it to the answer.",
        ],
        pattern="Variable sliding window, counting subarrays ending at r",
        explain=(
            "Monotonic condition (product only grows) makes the window valid. Every valid window ending at r "
            "contributes (r - l + 1) subarrays."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time",
        brute=r"""
# BRUTE FORCE: O(n^2) time
def num_subarray_product_less_than_k(nums, k):
    c = 0
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)):
            p *= nums[j]
            if p < k:
                c += 1
            else:
                break
    return c
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Variable sliding window, counting subarrays ending at r
def num_subarray_product_less_than_k(nums, k):
    if k <= 1:
        return 0
    left, prod, ans = 0, 1, 0
    for right, x in enumerate(nums):
        prod *= x
        while prod >= k:
            prod //= nums[left]
            left += 1
        ans += right - left + 1
    return ans
""",
    ),
    # ---- Fruit Into Baskets (LeetCode 904) ----
    dict(
        title="Fruit Into Baskets",
        diff="M",
        lc=904,
        slug="fruit-into-baskets",
        prompt=(
            "Each tree has a fruit type; you have two baskets (one type each) and must pick consecutively. Return "
            "the maximum fruits you can pick (longest subarray with at most 2 distinct values)."
        ),
        sig="def total_fruit(fruits: List[int]) -> int:",
        fn="total_fruit",
        tests=[
            (([1, 2, 1],), 3),
            (([0, 1, 2, 2],), 3),
            (([1, 2, 3, 2, 2],), 4),
            (([3, 3, 3],), 3),
            (([],), 0),
            (([1, 2, 3, 4],), 2),
        ],
        hints=[
            "This is 'longest subarray with at most K distinct values' with K = 2.",
            "Window with a count dict; when len(dict) > 2, shrink from the left.",
            "Decrement the left fruit's count and delete the key when it reaches 0; track the max window length.",
        ],
        pattern="Variable window with a count map (at most K distinct)",
        explain=(
            "The dict size is the number of distinct values in the window. Shrink until the constraint holds again; "
            "record the best size each step."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time",
        brute=r"""
# BRUTE FORCE: O(n^2) time
def total_fruit(fruits):
    best = 0
    for i in range(len(fruits)):
        kinds = set()
        for j in range(i, len(fruits)):
            kinds.add(fruits[j])
            if len(kinds) > 2:
                break
            best = max(best, j - i + 1)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Variable window with a count map (at most K distinct)
def total_fruit(fruits):
    cnt, left, best = {}, 0, 0
    for right, f in enumerate(fruits):
        cnt[f] = cnt.get(f, 0) + 1
        while len(cnt) > 2:
            cnt[fruits[left]] -= 1
            if cnt[fruits[left]] == 0:
                del cnt[fruits[left]]
            left += 1
        best = max(best, right - left + 1)
    return best
""",
    ),
    # ---- Longest Subarray of 1's After Deleting One Element (LeetCode 1493) ----
    dict(
        title="Longest Subarray of 1's After Deleting One Element",
        diff="M",
        lc=1493,
        slug="longest-subarray-of-1s-after-deleting-one-element",
        prompt=(
            "You must delete exactly one element from a binary array. Return the length of the longest non-empty "
            "subarray of only 1s that remains."
        ),
        sig="def longest_subarray(nums: List[int]) -> int:",
        fn="longest_subarray",
        tests=[
            (([1, 1, 0, 1],), 3),
            (([0, 1, 1, 1, 0, 1, 1, 0, 1],), 5),
            (([1, 1, 1],), 2),
            (([0, 0],), 0),
            (([0],), 0),
            (([1],), 0),
        ],
        hints=[
            "Deleting one element = allowing one zero inside the window.",
            "Longest window with at most one 0; the answer is its length minus 1 (the deleted element).",
            "Shrink when zeros > 1. The -1 also handles the 'all ones' case where you must delete a 1.",
        ],
        pattern="Variable window with at most K = 1 violations",
        explain=(
            "'Allow at most k bad elements' is the generic template. The mandatory deletion subtracts exactly one "
            "from the best window."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time",
        brute=r"""
# BRUTE FORCE: O(n^2) time
def longest_subarray(nums):
    n, best = len(nums), 0
    for d in range(n):
        run = 0
        for i in range(n):
            if i == d:
                continue  # skipping d lets the runs on both sides join
            if nums[i] == 1:
                run += 1
                best = max(best, run)
            else:
                run = 0
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Variable window with at most K = 1 violations
def longest_subarray(nums):
    left = zeros = best = 0
    for right, x in enumerate(nums):
        zeros += x == 0
        while zeros > 1:
            zeros -= nums[left] == 0
            left += 1
        best = max(best, right - left)
    return best
""",
    ),
]
