"""more Divide & Conquer problems (batch 3) - part of the problem bank for the "divide_conquer" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Count of Smaller Numbers After Self (LeetCode 315) ----
    dict(
        title="Count of Smaller Numbers After Self",
        diff="H",
        lc=315,
        slug="count-of-smaller-numbers-after-self",
        prompt=(
            "For every index i, count how many elements to the RIGHT of i are strictly smaller than nums[i]. Return "
            "the counts."
        ),
        sig="def count_smaller(nums: List[int]) -> List[int]:",
        fn="count_smaller",
        tests=[
            (([5, 2, 6, 1],), [2, 1, 1, 0]),
            (([-1],), [0]),
            (([-1, -1],), [0, 0]),
            (([2, 0, 1],), [2, 0, 0]),
            (([],), []),
        ],
        hints=[
            (
                "Checking every pair is O(n^2). Think merge sort: it compares left-half and right-half elements in "
                "sorted order."
            ),
            (
                "While merging two sorted halves, every right-half element that is placed BEFORE a left-half "
                "element is smaller than it and sits to its right."
            ),
            (
                "Sort indices (not values) so each element keeps its identity; when you place a left element, add "
                "the number of right elements already placed."
            ),
        ],
        pattern="Merge sort that counts while merging (inversion counting)",
        explain=(
            "Counting 'smaller elements to the right' is counting inversions per element. Merge sort sees each pair "
            "of\n        (left element, right element) exactly once - at the merge where they land in different "
            "halves - and\n        the sorted order tells us the answer for all pairs of the right half at once."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2) time - compare every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - compare every pair
def count_smaller(nums):
    n = len(nums)
    # for each i, count the later elements that are smaller
    return [sum(1 for j in range(i + 1, n) if nums[j] < nums[i]) for i in range(n)]
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Merge sort that counts while merging (inversion counting)
def count_smaller(nums):
    n = len(nums)
    counts = [0] * n
    order = list(range(n))  # indices; we sort THESE by value so every element keeps its identity

    def merge_sort(lo, hi):  # sorts order[lo:hi] by nums value, filling counts as it merges
        if hi - lo <= 1:
            return
        mid = (lo + hi) // 2
        merge_sort(lo, mid)
        merge_sort(mid, hi)
        merged = []
        i, j = lo, mid  # i walks the left half, j walks the right half
        while i < mid or j < hi:
            take_right = j < hi and (i == mid or nums[order[j]] < nums[order[i]])
            if take_right:
                merged.append(
                    order[j]
                )  # this right element is smaller than every left element still waiting
                j += 1
            else:
                counts[order[i]] += (
                    j - mid
                )  # right elements already placed are all smaller than this one
                merged.append(order[i])
                i += 1
        order[lo:hi] = merged

    merge_sort(0, n)
    return counts
""",
    ),
]
