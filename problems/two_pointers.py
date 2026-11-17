"""Two Pointers problems - the problem bank for the "two_pointers" topic.

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
    # ---- Valid Palindrome (LeetCode 125) ----
    dict(
        title="Valid Palindrome",
        diff="E",
        lc=125,
        slug="valid-palindrome",
        prompt=(
            "Decide whether a string reads the same forwards and backwards after you drop every non-alphanumeric "
            "character and ignore letter case."
        ),
        sig="def is_palindrome(s: str) -> bool:",
        fn="is_palindrome",
        tests=[
            (("A man, a plan, a canal: Panama",), True),
            (("race a car",), False),
            ((" ",), True),
            (("0P",), False),
            (("ab_a",), True),
        ],
        hints=[
            "Building a cleaned reversed copy works, but can you do it with O(1) extra space?",
            "Put one pointer at each end; they walk toward each other comparing characters.",
            "Skip non-alphanumeric characters on either side before comparing lowercase versions.",
        ],
        pattern="Two pointers, opposite ends, converging",
        explain=(
            "A palindrome is symmetric around its centre, so compare the i-th from the left with the i-th from "
            "the\n        right. Skip junk with inner while-loops. Each pointer moves at most n steps: O(n) time, "
            "O(1) space."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - builds a cleaned reversed copy",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - builds a cleaned reversed copy
def is_palindrome(s):
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two pointers, opposite ends, converging
def is_palindrome(s):
    left, right = 0, len(s) - 1

    while left < right:
        while left < right and not s[left].isalnum():
            left += 1

        while left < right and not s[right].isalnum():
            right -= 1

        if s[left].lower() != s[right].lower():
            return False

        left += 1
        right -= 1

    return True
""",
    ),
    # ---- 3Sum (LeetCode 15) ----
    dict(
        title="3Sum",
        diff="M",
        lc=15,
        slug="3sum",
        prompt=(
            "Return all unique triplets of numbers from the array that sum to zero. The result must not contain "
            "duplicate triplets."
        ),
        sig="def three_sum(nums: List[int]) -> List[List[int]]:",
        fn="three_sum",
        compare="nested_unordered",
        tests=[
            (([-1, 0, 1, 2, -1, -4],), [[-1, -1, 2], [-1, 0, 1]]),
            (([0, 1, 1],), []),
            (([0, 0, 0],), [[0, 0, 0]]),
            (([0, 0, 0, 0],), [[0, 0, 0]]),
            (([-2, 0, 1, 1, 2],), [[-2, 0, 2], [-2, 1, 1]]),
        ],
        hints=[
            "Fix one number; the problem becomes 'find two numbers summing to its negative'.",
            (
                "Sort first. For the remaining pair use two pointers (sum too small -> move left up, too big -> "
                "right down)."
            ),
            (
                "Duplicates: skip equal values for the fixed number, and after finding a triplet skip equal "
                "left/right values."
            ),
        ],
        pattern="Sort + fix one element + two pointers on the rest",
        explain=(
            "Sorting makes 'sum too small / too big' a directional signal, which is what lets two pointers "
            "prune\n        the O(n^2) pairs down to O(n). The outer loop contributes another factor n, so O(n^2) "
            "total.\n        Duplicate handling is done by skipping equal neighbours, not by a set, so there is no "
            "extra memory."
        ),
        cx="O(n^2) time, O(1) extra space (sort + two pointers)",
        brute_cx="O(n^3) - all triples, a set removes duplicates",
        brute=r"""
# BRUTE FORCE: O(n^3) - all triples, a set removes duplicates
def three_sum(nums):
    res = set()
    n = len(nums)

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    res.add(tuple(sorted((nums[i], nums[j], nums[k]))))

    return [list(t) for t in res]
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(1) extra space (sort + two pointers)
# Idea: Sort + fix one element + two pointers on the rest
def three_sum(nums):
    nums.sort()
    res = []
    n = len(nums)

    for i in range(n - 2):
        if i and nums[i] == nums[i - 1]:  # skip duplicate anchors
            continue

        left, right = i + 1, n - 1

        while left < right:
            s = nums[i] + nums[left] + nums[right]

            if s < 0:
                left += 1
            elif s > 0:
                right -= 1
            else:
                res.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1

    return res
""",
    ),
    # ---- Container With Most Water (LeetCode 11) ----
    dict(
        title="Container With Most Water",
        diff="M",
        lc=11,
        slug="container-with-most-water",
        prompt=(
            "Vertical lines have the given heights at x = 0..n-1. Choose two lines that, with the x-axis, hold the "
            "most water, and return that area."
        ),
        sig="def max_area(height: List[int]) -> int:",
        fn="max_area",
        tests=[
            (([1, 8, 6, 2, 5, 4, 8, 3, 7],), 49),
            (([1, 1],), 1),
            (([4, 3, 2, 1, 4],), 16),
            (([1, 2, 1],), 2),
        ],
        hints=[
            "Area = width * min(left height, right height). Brute force is O(n^2).",
            "Start with the widest container (both ends). Which end can you safely discard, and why?",
            "Move the shorter line inward: keeping it can never beat the current area because width only shrinks.",
        ],
        pattern="Two pointers converging, with a greedy discard argument",
        explain=(
            "At the widest pair, the shorter side limits the height. Any narrower container that KEEPS that "
            "shorter\n        line has smaller width and no greater height, so it cannot win - the short line is "
            "useless and can be\n        dropped. Repeating that gives O(n) with a proof of correctness (exchange "
            "argument)."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) - every pair of lines",
        brute=r"""
# BRUTE FORCE: O(n^2) - every pair of lines
def max_area(height):
    best = 0
    for i in range(len(height)):
        for j in range(i + 1, len(height)):
            best = max(best, (j - i) * min(height[i], height[j]))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two pointers converging, with a greedy discard argument
def max_area(height):
    left, right = 0, len(height) - 1
    best = 0

    while left < right:
        best = max(best, (right - left) * min(height[left], height[right]))
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return best
""",
    ),
    # ---- Trapping Rain Water (LeetCode 42) ----
    dict(
        title="Trapping Rain Water",
        diff="H",
        lc=42,
        slug="trapping-rain-water",
        prompt=(
            "Bars of the given heights (width 1) stand side by side. After rain, how many units of water are "
            "trapped between the bars?"
        ),
        sig="def trap(height: List[int]) -> int:",
        fn="trap",
        tests=[
            (([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],), 6),
            (([4, 2, 0, 3, 2, 5],), 9),
            (([],), 0),
            (([1, 2, 3],), 0),
            (([3, 0, 3],), 3),
        ],
        hints=[
            "Water above bar i = min(tallest bar to its left, tallest to its right) - height[i] (if positive).",
            "You can precompute left-max and right-max arrays (O(n) space). Can you avoid them?",
            "Two pointers: process the side with the smaller max; that side's water level is already determined.",
        ],
        pattern="Two pointers with running maxima (the smaller side decides)",
        explain=(
            "Water over a bar is bounded by the lower of the two walls around it. If left_max <= right_max, "
            "the\n        left bar's level is fixed by left_max no matter what is further right (the right wall is "
            "at least as\n        tall), so settle the left bar and advance; symmetric otherwise. O(n) time, O(1) "
            "space."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) - recomputes the tallest wall on each side of every bar",
        brute=r"""
# BRUTE FORCE: O(n^2) - recomputes the tallest wall on each side of every bar
def trap(height):
    total = 0
    for i in range(len(height)):
        left = max(height[: i + 1])
        right = max(height[i:])
        total += min(left, right) - height[i]
    return total
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two pointers with running maxima (the smaller side decides)
def trap(height):
    left, right = 0, len(height) - 1
    lmax = rmax = water = 0

    while left < right:
        if height[left] < height[right]:
            lmax = max(lmax, height[left])
            water += lmax - height[left]
            left += 1
        else:
            rmax = max(rmax, height[right])
            water += rmax - height[right]
            right -= 1

    return water
""",
    ),
]
