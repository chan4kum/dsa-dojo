"""more Hashing problems (batch 4) - part of the problem bank for the "hashing" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Intersection of Two Arrays (LeetCode 349) ----
    dict(
        title="Intersection of Two Arrays",
        diff="E",
        lc=349,
        slug="intersection-of-two-arrays",
        prompt="Return the distinct values that appear in both arrays (any order).",
        sig="def intersection(nums1: List[int], nums2: List[int]) -> List[int]:",
        fn="intersection",
        compare="unordered",
        tests=[
            (([1, 2, 2, 1], [2, 2]), [2]),
            (([4, 9, 5], [9, 4, 9, 8, 4]), [4, 9]),
            (([1], [2]), []),
            (([], [1]), []),
        ],
        hints=[
            "Checking every pair is O(n * m).",
            "A hash set answers 'is x in the other array?' in O(1).",
            "Put one array in a set and keep the values of the other that it contains - or just use set intersection.",
        ],
        pattern="Hash set membership",
        explain=(
            "Sets remove duplicates automatically and give O(1) lookups, turning a quadratic comparison into one "
            "linear pass."
        ),
        cx="O(n + m) time, O(n) space",
        brute_cx="O(n * m) time - compare every pair",
        brute=r"""
# BRUTE FORCE: O(n * m) time - compare every pair
def intersection(nums1, nums2):
    result = []
    for a in nums1:
        for b in nums2:
            if a == b and a not in result:
                result.append(a)
    return result
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(n) space
# Idea: Hash set membership
def intersection(nums1, nums2):
    return list(set(nums1) & set(nums2))
""",
    ),
    # ---- Intersection of Two Arrays II (LeetCode 350) ----
    dict(
        title="Intersection of Two Arrays II",
        diff="E",
        lc=350,
        slug="intersection-of-two-arrays-ii",
        prompt=(
            "Return the intersection of two arrays as a multiset: each value appears as many times as it appears in "
            "BOTH arrays (any order)."
        ),
        sig="def intersect(nums1: List[int], nums2: List[int]) -> List[int]:",
        fn="intersect",
        compare="unordered",
        tests=[
            (([1, 2, 2, 1], [2, 2]), [2, 2]),
            (([4, 9, 5], [9, 4, 9, 8, 4]), [4, 9]),
            (([1], [2]), []),
            (([1, 1], [1]), [1]),
        ],
        hints=[
            "Duplicates now matter: a value should appear min(count in nums1, count in nums2) times.",
            "Count one array with a Counter.",
            "Walk the other array; if the counter still has the value, output it and decrement the counter.",
        ],
        pattern="Frequency counter consumed as you match",
        explain=(
            "Decrementing the counter on every match makes sure a value is never matched more times than it occurs "
            "in the first array."
        ),
        cx="O(n + m) time, O(min(n, m)) space",
        brute_cx="O(n * m) time - find and remove each match from a copy",
        brute=r"""
# BRUTE FORCE: O(n * m) time - find and remove each match from a copy
def intersect(nums1, nums2):
    remaining, result = list(nums2), []
    for x in nums1:
        if x in remaining:
            remaining.remove(x)  # use this occurrence up
            result.append(x)
    return result
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(min(n, m)) space
# Idea: Frequency counter consumed as you match
def intersect(nums1, nums2):
    counts, result = Counter(nums1), []
    for x in nums2:
        if counts[x] > 0:
            counts[x] -= 1
            result.append(x)
    return result
""",
    ),
]
