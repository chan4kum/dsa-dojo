"""extra batch of Two Pointers problems - the problem bank for the "two_pointers" topic.

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
    # ---- Two Sum II - Input Array Is Sorted (LeetCode 167) ----
    dict(
        title="Two Sum II - Input Array Is Sorted",
        diff="M",
        lc=167,
        slug="two-sum-ii-input-array-is-sorted",
        prompt=(
            "The array is sorted ascending. Return the 1-based indices [i, j] (i < j) of the two numbers adding up "
            "to target. Exactly one solution exists. Use O(1) extra space."
        ),
        sig="def two_sum_sorted(numbers: List[int], target: int) -> List[int]:",
        fn="two_sum_sorted",
        tests=[
            (([2, 7, 11, 15], 9), [1, 2]),
            (([2, 3, 4], 6), [1, 3]),
            (([-1, 0], -1), [1, 2]),
            (([1, 2, 3, 4, 4, 9, 56, 90], 8), [4, 5]),
        ],
        hints=[
            "The hash-map solution works but uses O(n) space. What does sortedness give you?",
            "Put one pointer at each end. If the sum is too big, which pointer can safely move?",
            (
                "sum > target -> right--; sum < target -> left++. Each step discards a value that can never be part "
                "of the answer."
            ),
        ],
        pattern="Two pointers on a sorted array (converge from both ends)",
        explain=(
            "If numbers[l] + numbers[r] > target, then numbers[r] paired with ANY l' >= l is also too big, so r "
            "is\n        useless - drop it. Symmetrically for too small. Each move eliminates one candidate: O(n)."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time, O(1) space - every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time, O(1) space - every pair
def two_sum_sorted(numbers, target):
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                return [i + 1, j + 1]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two pointers on a sorted array (converge from both ends)
def two_sum_sorted(numbers, target):
    left, right = 0, len(numbers) - 1
    while left < right:
        s = numbers[left] + numbers[right]
        if s == target:
            return [left + 1, right + 1]
        if s < target:
            left += 1
        else:
            right -= 1
""",
    ),
    # ---- Squares of a Sorted Array (LeetCode 977) ----
    dict(
        title="Squares of a Sorted Array",
        diff="E",
        lc=977,
        slug="squares-of-a-sorted-array",
        prompt="Given a sorted array (may contain negatives), return the squares of each number, also sorted.",
        sig="def sorted_squares(nums: List[int]) -> List[int]:",
        fn="sorted_squares",
        tests=[
            (([-4, -1, 0, 3, 10],), [0, 1, 9, 16, 100]),
            (([-7, -3, 2, 3, 11],), [4, 9, 9, 49, 121]),
            (([5],), [25]),
            (([-5, -4],), [16, 25]),
        ],
        hints=[
            "Squaring then sorting is O(n log n). The input is already structured - how?",
            "The largest square is at one of the two ENDS of the array.",
            (
                "Fill the result from the back: compare |nums[l]| with |nums[r]|, place the bigger square, move "
                "that pointer."
            ),
        ],
        pattern="Two pointers from both ends, build output from the largest",
        explain=(
            "Negatives shrink toward zero then positives grow, so absolute values form a 'V'. The biggest is always "
            "at\n        an end. Write results right-to-left in O(n)."
        ),
        cx="O(n) time, O(n) output",
        brute_cx="O(n log n) time - square then sort",
        brute=r"""
# BRUTE FORCE: O(n log n) time - square then sort
def sorted_squares(nums):
    return sorted(x * x for x in nums)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) output
# Idea: Two pointers from both ends, build output from the largest
def sorted_squares(nums):
    n = len(nums)
    out = [0] * n
    left, right = 0, n - 1
    for i in range(n - 1, -1, -1):
        if abs(nums[left]) > abs(nums[right]):
            out[i] = nums[left] ** 2
            left += 1
        else:
            out[i] = nums[right] ** 2
            right -= 1
    return out
""",
    ),
    # ---- Move Zeroes (LeetCode 283) ----
    dict(
        title="Move Zeroes",
        diff="E",
        lc=283,
        slug="move-zeroes",
        prompt="Move all 0s to the end of the array in place while keeping the relative order of the non-zero values.",
        sig="def move_zeroes(nums: List[int]) -> None:",
        fn="move_zeroes",
        inplace=0,
        tests=[
            (([0, 1, 0, 3, 12],), [1, 3, 12, 0, 0]),
            (([0],), [0]),
            (([1, 2, 3],), [1, 2, 3]),
            (([0, 0, 1],), [1, 0, 0]),
        ],
        hints=[
            "Building a new list is easy; the point is to do it in place.",
            "Keep a 'write' index for the next non-zero slot.",
            "For each non-zero x: swap nums[write] and nums[i], then write++. Zeroes get pushed right automatically.",
        ],
        pattern="Read/write pointers (partition in place)",
        explain=(
            "`write` marks the boundary: everything before it is the finished non-zero prefix. Swapping (rather "
            "than\n        copying then zero-filling) keeps it a single pass. It is the same skeleton as Remove "
            "Element / Dedupe."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) extra space - build a new list",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) extra space - build a new list
def move_zeroes(nums):
    nz = [x for x in nums if x != 0]
    nums[:] = nz + [0] * (len(nums) - len(nz))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Read/write pointers (partition in place)
def move_zeroes(nums):
    write = 0
    for i in range(len(nums)):
        if nums[i] != 0:
            nums[write], nums[i] = nums[i], nums[write]
            write += 1
""",
    ),
    # ---- Sort Colors (LeetCode 75) ----
    dict(
        title="Sort Colors",
        diff="M",
        lc=75,
        slug="sort-colors",
        prompt=(
            "The array contains only 0, 1, 2. Sort it in place in one pass without using a library sort (Dutch "
            "national flag)."
        ),
        sig="def sort_colors(nums: List[int]) -> None:",
        fn="sort_colors",
        inplace=0,
        tests=[
            (([2, 0, 2, 1, 1, 0],), [0, 0, 1, 1, 2, 2]),
            (([2, 0, 1],), [0, 1, 2]),
            (([0],), [0]),
            (([1, 2, 0, 0, 2, 1, 1],), [0, 0, 1, 1, 1, 2, 2]),
        ],
        hints=[
            "Counting 0s, 1s, 2s then rewriting works in two passes. Can you do ONE pass?",
            "Maintain three regions: [0..lo) all 0s, [lo..i) all 1s, (hi..end] all 2s; i scans the unknown middle.",
            (
                "On 0: swap with lo, lo++, i++. On 2: swap with hi, hi-- (do NOT advance i: the swapped-in value is "
                "unchecked). On 1: i++."
            ),
        ],
        pattern="Three-way partition (Dutch national flag) with an invariant",
        explain=(
            "Invariant: nums[:lo] are 0, nums[lo:i] are 1, nums[hi+1:] are 2, nums[i:hi+1] are unknown. Each "
            "iteration\n        shrinks the unknown region by one. After a swap with hi we have not inspected the "
            "new nums[i], so i stays."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n log n) time - just sort",
        brute=r"""
# BRUTE FORCE: O(n log n) time - just sort
def sort_colors(nums):
    nums.sort()
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Three-way partition (Dutch national flag) with an invariant
def sort_colors(nums):
    lo, i, hi = 0, 0, len(nums) - 1
    while i <= hi:
        if nums[i] == 0:
            nums[lo], nums[i] = nums[i], nums[lo]
            lo += 1
            i += 1
        elif nums[i] == 2:
            nums[i], nums[hi] = nums[hi], nums[i]
            hi -= 1
        else:
            i += 1
""",
    ),
    # ---- Merge Sorted Array (LeetCode 88) ----
    dict(
        title="Merge Sorted Array",
        diff="E",
        lc=88,
        slug="merge-sorted-array",
        prompt=(
            "nums1 has length m+n: its first m entries are sorted values and the last n are 0 placeholders. nums2 "
            "has n sorted values. Merge nums2 into nums1 in place so nums1 is sorted."
        ),
        sig="def merge(nums1: List[int], m: int, nums2: List[int], n: int) -> None:",
        fn="merge",
        inplace=0,
        tests=[
            (([1, 2, 3, 0, 0, 0], 3, [2, 5, 6], 3), [1, 2, 2, 3, 5, 6]),
            (([1], 1, [], 0), [1]),
            (([0], 0, [1], 1), [1]),
            (([4, 5, 6, 0, 0, 0], 3, [1, 2, 3], 3), [1, 2, 3, 4, 5, 6]),
        ],
        hints=[
            "Merging from the FRONT overwrites values of nums1 you still need.",
            "Which end of nums1 is free space?",
            "Merge from the back: compare the largest remaining of each, write into position m+n-1 and move left.",
        ],
        pattern="Merge from the back (use the free space as a buffer)",
        explain=(
            "The empty slots are at the end, so fill the array from the largest value down. The write index "
            "never\n        overtakes the unread part of nums1, hence no extra memory. Stop when nums2 is exhausted "
            "- the remaining\n        nums1 prefix is already in place."
        ),
        cx="O(m+n) time, O(1) space",
        brute_cx="O((m+n) log(m+n)) time - copy then sort",
        brute=r"""
# BRUTE FORCE: O((m+n) log(m+n)) time - copy then sort
def merge(nums1, m, nums2, n):
    nums1[m:] = nums2[:n]
    nums1.sort()
""",
        solution=r"""
# OPTIMISED: O(m+n) time, O(1) space
# Idea: Merge from the back (use the free space as a buffer)
def merge(nums1, m, nums2, n):
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
""",
    ),
    # ---- Valid Palindrome II (LeetCode 680) ----
    dict(
        title="Valid Palindrome II",
        diff="E",
        lc=680,
        slug="valid-palindrome-ii",
        prompt="Return True if the string can become a palindrome after deleting at most one character.",
        sig="def valid_palindrome(s: str) -> bool:",
        fn="valid_palindrome",
        tests=[
            (("aba",), True),
            (("abca",), True),
            (("abc",), False),
            (("a",), True),
            (("abcdba",), True),
            (("abcdefa",), False),
            (("",), True),
        ],
        hints=[
            "Trying every deletion and checking palindrome is O(n^2). Where does a mismatch first show up?",
            (
                "Run the usual two-pointer palindrome check; at the first mismatch you must delete one of the two "
                "characters."
            ),
            (
                "At the first mismatch (l, r), return is_pal(l+1, r) or is_pal(l, r-1). Only one branch point "
                "exists, so O(n)."
            ),
        ],
        pattern="Two pointers with one allowed skip (branch once)",
        explain=(
            "Everything outside the first mismatching pair already matches, so the deletion must be one of those "
            "two\n        characters. Test both remaining substrings in O(n). Generalising to k skips needs DP "
            "(Longest Palindromic Subsequence)."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - delete each character, test",
        brute=r"""
# BRUTE FORCE: O(n^2) time - delete each character, test
def valid_palindrome(s):
    if s == s[::-1]:
        return True
    return any((s[:i] + s[i + 1 :]) == (s[:i] + s[i + 1 :])[::-1] for i in range(len(s)))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two pointers with one allowed skip (branch once)
def valid_palindrome(s):
    def pal(left, right):
        while left < right:
            if s[left] != s[right]:
                return False
            left, right = left + 1, right - 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return pal(left + 1, right) or pal(left, right - 1)
        left, right = left + 1, right - 1
    return True
""",
    ),
]
