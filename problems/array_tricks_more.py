"""extra batch of Array Tricks problems - the problem bank for the "array_tricks" topic.

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
    # ---- Maximum Product Subarray (LeetCode 152) ----
    dict(
        title="Maximum Product Subarray",
        diff="M",
        lc=152,
        slug="maximum-product-subarray",
        prompt="Return the largest product of any contiguous non-empty subarray.",
        sig="def max_product(nums: List[int]) -> int:",
        fn="max_product",
        tests=[
            (([2, 3, -2, 4],), 6),
            (([-2, 0, -1],), 0),
            (([-2, 3, -4],), 24),
            (([-2],), -2),
            (([0, 2],), 2),
            (([-1, -2, -3, 0, 4],), 6),
        ],
        hints=[
            "Kadane's algorithm keeps one running best. Why does that fail for products?",
            "A very negative product times a negative number becomes very positive. So also track the minimum.",
            (
                "At each x keep (max_ending_here, min_ending_here); the new values are max/min of (x, x*old_max, "
                "x*old_min)."
            ),
        ],
        pattern="Kadane variant tracking both max and min (negatives flip order)",
        explain=(
            "Multiplying by a negative swaps the roles of the largest and smallest running product, so both must be "
            "kept.\n        A zero resets the run (x alone is always a candidate)."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - all subarrays",
        brute=r"""
# BRUTE FORCE: O(n^2) time - all subarrays
def max_product(nums):
    best = nums[0]
    for i in range(len(nums)):
        p = 1
        for j in range(i, len(nums)):
            p *= nums[j]
            best = max(best, p)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Kadane variant tracking both max and min (negatives flip order)
def max_product(nums):
    best = hi = lo = nums[0]
    for x in nums[1:]:
        cand = (x, hi * x, lo * x)
        hi, lo = max(cand), min(cand)
        best = max(best, hi)
    return best
""",
    ),
    # ---- Majority Element (LeetCode 169) ----
    dict(
        title="Majority Element",
        diff="E",
        lc=169,
        slug="majority-element",
        prompt="Return the element appearing more than n/2 times (it always exists).",
        sig="def majority_element(nums: List[int]) -> int:",
        fn="majority_element",
        tests=[
            (([3, 2, 3],), 3),
            (([2, 2, 1, 1, 1, 2, 2],), 2),
            (([1],), 1),
            (([5, 5, 5, 1, 2],), 5),
        ],
        hints=[
            "A hash map of counts gives O(n) time but O(n) space.",
            "The majority element outnumbers everything else combined. What if pairs of different elements 'cancel'?",
            (
                "Boyer-Moore voting: keep candidate and count; same value -> count+1, different -> count-1; at 0 "
                "take a new candidate."
            ),
        ],
        pattern="Boyer-Moore voting (cancellation argument)",
        explain=(
            "Cancel each pair of distinct elements. Since the majority has more than half, it survives all "
            "cancellations.\n        Constant space, one pass."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - count each element",
        brute=r"""
# BRUTE FORCE: O(n^2) time - count each element
def majority_element(nums):
    for x in nums:
        if nums.count(x) > len(nums) // 2:
            return x
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Boyer-Moore voting (cancellation argument)
def majority_element(nums):
    cand, count = None, 0
    for x in nums:
        if count == 0:
            cand = x
        count += 1 if x == cand else -1
    return cand
""",
    ),
    # ---- Rotate Array (LeetCode 189) ----
    dict(
        title="Rotate Array",
        diff="M",
        lc=189,
        slug="rotate-array",
        prompt="Rotate the array to the right by k steps, in place.",
        sig="def rotate(nums: List[int], k: int) -> None:",
        fn="rotate",
        inplace=0,
        tests=[
            (([1, 2, 3, 4, 5, 6, 7], 3), [5, 6, 7, 1, 2, 3, 4]),
            (([-1, -100, 3, 99], 2), [3, 99, -1, -100]),
            (([1], 5), [1]),
            (([1, 2], 3), [2, 1]),
        ],
        hints=[
            "Moving elements one step at a time k times is O(n*k). Think geometrically.",
            "k can exceed n; first take k %= n.",
            "Reverse the whole array, then reverse the first k and the last n-k elements.",
        ],
        pattern="Triple reversal trick",
        explain=(
            "Rotating right by k moves the last k elements to the front. Reversing everything puts them in front "
            "but\n        backwards; reversing each block fixes the order. O(n) time and O(1) space."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n*k) time - rotate by one k times",
        brute=r"""
# BRUTE FORCE: O(n*k) time - rotate by one k times
def rotate(nums, k):
    for _ in range(k % len(nums)):
        nums.insert(0, nums.pop())
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Triple reversal trick
def rotate(nums, k):
    n = len(nums)
    k %= n

    def rev(left, right):
        while left < right:
            nums[left], nums[right] = nums[right], nums[left]
            left, right = left + 1, right - 1

    rev(0, n - 1)
    rev(0, k - 1)
    rev(k, n - 1)
""",
    ),
    # ---- Find All Duplicates in an Array (LeetCode 442) ----
    dict(
        title="Find All Duplicates in an Array",
        diff="M",
        lc=442,
        slug="find-all-duplicates-in-an-array",
        prompt=(
            "nums has n integers, each in [1, n], each appearing once or twice. Return all values that appear "
            "twice, in O(n) time and O(1) extra space."
        ),
        sig="def find_duplicates(nums: List[int]) -> List[int]:",
        fn="find_duplicates",
        compare="unordered",
        tests=[
            (([4, 3, 2, 7, 8, 2, 3, 1],), [2, 3]),
            (([1, 1, 2],), [1]),
            (([1],), []),
            (([2, 2, 3, 3],), [2, 3]),
        ],
        hints=[
            "A set works in O(n) space. The values are in [1, n]: what does that let you use as a hash table?",
            "Use the array itself: value v 'lives' at index v-1.",
            "For each x, flip the sign of nums[abs(x)-1]. If it is already negative, abs(x) is a duplicate.",
        ],
        pattern="Index-as-hash (sign marking) when values are in [1, n]",
        explain=(
            "The input range equals the index range, so each index can store a one-bit 'seen' flag in the sign. "
            "Restore\n        signs afterwards if the caller needs the array unchanged."
        ),
        cx="O(n) time, O(1) extra space",
        brute_cx="O(n^2) time - count each value",
        brute=r"""
# BRUTE FORCE: O(n^2) time - count each value
def find_duplicates(nums):
    return [x for x in set(nums) if nums.count(x) == 2]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) extra space
# Idea: Index-as-hash (sign marking) when values are in [1, n]
def find_duplicates(nums):
    out = []
    for x in nums:
        i = abs(x) - 1
        if nums[i] < 0:
            out.append(abs(x))
        else:
            nums[i] = -nums[i]
    return out
""",
    ),
    # ---- Next Permutation (LeetCode 31) ----
    dict(
        title="Next Permutation",
        diff="M",
        lc=31,
        slug="next-permutation",
        prompt=(
            "Rearrange nums in place into the next lexicographically greater permutation; if none exists, into the "
            "lowest (sorted ascending)."
        ),
        sig="def next_permutation(nums: List[int]) -> None:",
        fn="next_permutation",
        inplace=0,
        tests=[
            (([1, 2, 3],), [1, 3, 2]),
            (([3, 2, 1],), [1, 2, 3]),
            (([1, 1, 5],), [1, 5, 1]),
            (([1, 3, 2],), [2, 1, 3]),
            (([2, 3, 1],), [3, 1, 2]),
            (([1],), [1]),
        ],
        hints=[
            "Write the permutations of [1,2,3] in order and study how each next one differs.",
            "Find the rightmost position i where nums[i] < nums[i+1] (the suffix after i is non-increasing).",
            (
                "Swap nums[i] with the smallest suffix value greater than it (found from the right), then reverse "
                "the suffix."
            ),
        ],
        pattern="Find the pivot, swap, reverse the suffix",
        explain=(
            "The longest non-increasing suffix is already the largest arrangement of those elements, so the "
            "next\n        permutation must change the element just before it. Replace it with the next larger "
            "value from the suffix\n        and make the suffix as small as possible (ascending = reverse of the "
            "descending suffix)."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n! * n) time - enumerate all permutations in order",
        brute=r"""
# BRUTE FORCE: O(n! * n) time - enumerate all permutations in order
def next_permutation(nums):
    perms = sorted(set(itertools.permutations(nums)))
    cur = tuple(nums)
    i = perms.index(cur)
    nums[:] = perms[(i + 1) % len(perms)]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Find the pivot, swap, reverse the suffix
def next_permutation(nums):
    i = len(nums) - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1
    if i >= 0:
        j = len(nums) - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]
    nums[i + 1 :] = reversed(nums[i + 1 :])
""",
    ),
]
