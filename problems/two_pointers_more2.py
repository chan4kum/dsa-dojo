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
    # ---- Reverse String (LeetCode 344) ----
    dict(
        title="Reverse String",
        diff="E",
        lc=344,
        slug="reverse-string",
        prompt="Reverse a list of characters IN PLACE with O(1) extra space.",
        sig="def reverse_string(s: List[str]) -> None:",
        fn="reverse_string",
        inplace=0,
        tests=[
            ((list("hello"),), list("olleh")),
            ((list("Hannah"),), list("hannaH")),
            ((["a"],), ["a"]),
            (([],), []),
            ((list("ab"),), list("ba")),
        ],
        hints=[
            "Which two elements must swap places? The first and the last.",
            "Walk two pointers inward from both ends.",
            "while l < r: swap s[l], s[r]; l += 1; r -= 1.",
        ],
        pattern="Two pointers from both ends (swap inward)",
        explain="Mirror positions i and n-1-i trade values. Stop when the pointers meet - the middle element stays.",
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space (copy then write back)",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space (copy then write back)
def reverse_string(s):
    t = s[::-1]
    for i in range(len(s)):
        s[i] = t[i]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two pointers from both ends (swap inward)
def reverse_string(s):
    left, right = 0, len(s) - 1
    while left < right:
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
""",
    ),
    # ---- 3Sum Closest (LeetCode 16) ----
    dict(
        title="3Sum Closest",
        diff="M",
        lc=16,
        slug="3sum-closest",
        prompt="Return the sum of three numbers whose sum is closest to target (the tests have a unique closest sum).",
        sig="def three_sum_closest(nums: List[int], target: int) -> int:",
        fn="three_sum_closest",
        tests=[
            (([-1, 2, 1, -4], 1), 2),
            (([0, 0, 0], 1), 0),
            (([1, 1, 1, 0], -100), 2),
            (([1, 2, 5, 10, 11], 12), 13),
            (([-5, -3, 4, 9], 0), 1),
        ],
        hints=[
            "It is 3Sum, but you track the best distance instead of exact zeros.",
            "Sort, fix one number, then two pointers on the rest.",
            (
                "If the current sum is below target move l right, if above move r left; update best whenever |sum - "
                "target| improves."
            ),
        ],
        pattern="Sort + fix one + two pointers (optimise distance)",
        explain="Sorting makes the sum monotone in each pointer, so one pass over the pair finds the closest in O(n).",
        cx="O(n^2) time, O(1) extra space",
        brute_cx="O(n^3) time",
        brute=r"""
# BRUTE FORCE: O(n^3) time
def three_sum_closest(nums, target):
    best = None
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                s = nums[i] + nums[j] + nums[k]
                if best is None or abs(s - target) < abs(best - target):
                    best = s
    return best
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(1) extra space
# Idea: Sort + fix one + two pointers (optimise distance)
def three_sum_closest(nums, target):
    nums = sorted(nums)
    best = nums[0] + nums[1] + nums[2]
    for i in range(len(nums) - 2):
        left, right = i + 1, len(nums) - 1
        while left < right:
            s = nums[i] + nums[left] + nums[right]
            if abs(s - target) < abs(best - target):
                best = s
            if s < target:
                left += 1
            elif s > target:
                right -= 1
            else:
                return s
    return best
""",
    ),
    # ---- 4Sum (LeetCode 18) ----
    dict(
        title="4Sum",
        diff="M",
        lc=18,
        slug="4sum",
        prompt=(
            "Return all unique quadruplets that sum to target (order of quadruplets and of values inside each does "
            "not matter)."
        ),
        sig="def four_sum(nums: List[int], target: int) -> List[List[int]]:",
        fn="four_sum",
        compare="nested_unordered",
        tests=[
            (([1, 0, -1, 0, -2, 2], 0), [[-2, -1, 1, 2], [-2, 0, 0, 2], [-1, 0, 0, 1]]),
            (([2, 2, 2, 2, 2], 8), [[2, 2, 2, 2]]),
            (([1, 2, 3], 6), []),
            (([0, 0, 0, 0], 0), [[0, 0, 0, 0]]),
            (([], 0), []),
        ],
        hints=[
            "It generalises 3Sum: peel one more number with a loop.",
            "Sort; two nested loops fix a and b; the remaining pair is a two-pointer sweep.",
            "Skip duplicate values at every level (i, j, and both pointers) to avoid repeated quadruplets.",
        ],
        pattern="k-Sum reduction: sort, fix k-2 values, two pointers for the last pair",
        explain=(
            "kSum = (k-2) nested loops + one two-pointer sweep. Skipping equal neighbours at each level keeps "
            "results unique."
        ),
        cx="O(n^3) time, O(1) extra space",
        brute_cx="O(n^4) time (set of sorted tuples)",
        brute=r"""
# BRUTE FORCE: O(n^4) time (set of sorted tuples)
def four_sum(nums, target):
    n, seen = len(nums), set()
    for a in range(n):
        for b in range(a + 1, n):
            for c in range(b + 1, n):
                for d in range(c + 1, n):
                    if nums[a] + nums[b] + nums[c] + nums[d] == target:
                        seen.add(tuple(sorted((nums[a], nums[b], nums[c], nums[d]))))
    return [list(t) for t in seen]
""",
        solution=r"""
# OPTIMISED: O(n^3) time, O(1) extra space
# Idea: k-Sum reduction: sort, fix k-2 values, two pointers for the last pair
def four_sum(nums, target):
    nums.sort()
    n, out = len(nums), []
    for i in range(n - 3):
        if i and nums[i] == nums[i - 1]:
            continue
        for j in range(i + 1, n - 2):
            if j > i + 1 and nums[j] == nums[j - 1]:
                continue
            left, right = j + 1, n - 1
            while left < right:
                s = nums[i] + nums[j] + nums[left] + nums[right]
                if s < target:
                    left += 1
                elif s > target:
                    right -= 1
                else:
                    out.append([nums[i], nums[j], nums[left], nums[right]])
                    left += 1
                    right -= 1
                    while left < right and nums[left] == nums[left - 1]:
                        left += 1
    return out
""",
    ),
]
