from core import *

PROBLEMS = [
    dict(
        title="Valid Palindrome", diff="E", lc=125, slug="valid-palindrome",
        prompt="Decide whether a string reads the same forwards and backwards after you drop every "
               "non-alphanumeric character and ignore letter case.",
        sig="def is_palindrome(s: str) -> bool:",
        fn="is_palindrome",
        tests=[(("A man, a plan, a canal: Panama",), True), (("race a car",), False), ((" ",), True),
               (("0P",), False), (("ab_a",), True)],
        hints=["Building a cleaned reversed copy works, but can you do it with O(1) extra space?",
               "Put one pointer at each end; they walk toward each other comparing characters.",
               "Skip non-alphanumeric characters on either side before comparing lowercase versions."],
        pattern="Two pointers, opposite ends, converging",
        explain="""
        A palindrome is symmetric around its centre, so compare the i-th from the left with the i-th from the
        right. Skip junk with inner while-loops. Each pointer moves at most n steps: O(n) time, O(1) space.""",
        solution=r'''
def is_palindrome(s):
    l, r = 0, len(s) - 1
    while l < r:
        while l < r and not s[l].isalnum():
            l += 1
        while l < r and not s[r].isalnum():
            r -= 1
        if s[l].lower() != s[r].lower():
            return False
        l += 1
        r -= 1
    return True
''',
    ),
    dict(
        title="3Sum", diff="M", lc=15, slug="3sum",
        prompt="Return all unique triplets of numbers from the array that sum to zero. The result must not "
               "contain duplicate triplets.",
        sig="def three_sum(nums: List[int]) -> List[List[int]]:",
        fn="three_sum", compare="nested_unordered",
        tests=[(([-1, 0, 1, 2, -1, -4],), [[-1, -1, 2], [-1, 0, 1]]), (([0, 1, 1],), []), (([0, 0, 0],), [[0, 0, 0]]),
               (([0, 0, 0, 0],), [[0, 0, 0]]), (([-2, 0, 1, 1, 2],), [[-2, 0, 2], [-2, 1, 1]])],
        hints=["Fix one number; the problem becomes 'find two numbers summing to its negative'.",
               "Sort first. For the remaining pair use two pointers (sum too small -> move left up, too big -> right down).",
               "Duplicates: skip equal values for the fixed number, and after finding a triplet skip equal left/right values."],
        pattern="Sort + fix one element + two pointers on the rest",
        explain="""
        Sorting makes 'sum too small / too big' a directional signal, which is what lets two pointers prune
        the O(n^2) pairs down to O(n). The outer loop contributes another factor n, so O(n^2) total.
        Duplicate handling is done by skipping equal neighbours, not by a set, so there is no extra memory.""",
        solution=r'''
def three_sum(nums):
    nums.sort()
    res = []
    n = len(nums)
    for i in range(n - 2):
        if i and nums[i] == nums[i - 1]:      # skip duplicate anchors
            continue
        l, r = i + 1, n - 1
        while l < r:
            s = nums[i] + nums[l] + nums[r]
            if s < 0:
                l += 1
            elif s > 0:
                r -= 1
            else:
                res.append([nums[i], nums[l], nums[r]])
                l += 1
                r -= 1
                while l < r and nums[l] == nums[l - 1]:
                    l += 1
    return res
''',
    ),
    dict(
        title="Container With Most Water", diff="M", lc=11, slug="container-with-most-water",
        prompt="Vertical lines have the given heights at x = 0..n-1. Choose two lines that, with the x-axis, "
               "hold the most water, and return that area.",
        sig="def max_area(height: List[int]) -> int:",
        fn="max_area",
        tests=[(([1, 8, 6, 2, 5, 4, 8, 3, 7],), 49), (([1, 1],), 1), (([4, 3, 2, 1, 4],), 16), (([1, 2, 1],), 2)],
        hints=["Area = width * min(left height, right height). Brute force is O(n^2).",
               "Start with the widest container (both ends). Which end can you safely discard, and why?",
               "Move the shorter line inward: keeping it can never beat the current area because width only shrinks."],
        pattern="Two pointers converging, with a greedy discard argument",
        explain="""
        At the widest pair, the shorter side limits the height. Any narrower container that KEEPS that shorter
        line has smaller width and no greater height, so it cannot win - the short line is useless and can be
        dropped. Repeating that gives O(n) with a proof of correctness (exchange argument).""",
        solution=r'''
def max_area(height):
    l, r = 0, len(height) - 1
    best = 0
    while l < r:
        best = max(best, (r - l) * min(height[l], height[r]))
        if height[l] < height[r]:
            l += 1
        else:
            r -= 1
    return best
''',
    ),
    dict(
        title="Trapping Rain Water", diff="H", lc=42, slug="trapping-rain-water",
        prompt="Bars of the given heights (width 1) stand side by side. After rain, how many units of water "
               "are trapped between the bars?",
        sig="def trap(height: List[int]) -> int:",
        fn="trap",
        tests=[(([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1],), 6), (([4, 2, 0, 3, 2, 5],), 9), (([],), 0),
               (([1, 2, 3],), 0), (([3, 0, 3],), 3)],
        hints=["Water above bar i = min(tallest bar to its left, tallest to its right) - height[i] (if positive).",
               "You can precompute left-max and right-max arrays (O(n) space). Can you avoid them?",
               "Two pointers: process the side with the smaller max; that side's water level is already determined."],
        pattern="Two pointers with running maxima (the smaller side decides)",
        explain="""
        Water over a bar is bounded by the lower of the two walls around it. If left_max <= right_max, the
        left bar's level is fixed by left_max no matter what is further right (the right wall is at least as
        tall), so settle the left bar and advance; symmetric otherwise. O(n) time, O(1) space.""",
        solution=r'''
def trap(height):
    l, r = 0, len(height) - 1
    lmax = rmax = water = 0
    while l < r:
        if height[l] < height[r]:
            lmax = max(lmax, height[l])
            water += lmax - height[l]
            l += 1
        else:
            rmax = max(rmax, height[r])
            water += rmax - height[r]
            r -= 1
    return water
''',
    ),
]
