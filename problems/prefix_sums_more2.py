"""extra batch of Prefix Sums problems - the problem bank for the "prefix_sums" topic.

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
    # ---- Contiguous Array (LeetCode 525) ----
    dict(
        title="Contiguous Array",
        diff="M",
        lc=525,
        slug="contiguous-array",
        prompt=(
            "Given a binary array, return the length of the longest contiguous subarray with equally many 0s and 1s."
        ),
        sig="def find_max_length(nums: List[int]) -> int:",
        fn="find_max_length",
        tests=[
            (([0, 1],), 2),
            (([0, 1, 0],), 2),
            (([0, 0, 1, 0, 0, 0, 1, 1],), 6),
            (([1, 1, 1],), 0),
            (([],), 0),
            (([1, 0, 1, 0, 1],), 4),
        ],
        hints=[
            "Equal 0s and 1s means (#1 - #0) = 0 on that stretch. Treat 0 as -1.",
            "With running sum s, a stretch has sum 0 when two prefixes have the SAME s.",
            "Store the first index of each prefix sum (start with {0: -1}); answer = max(i - first[s]).",
        ],
        pattern="Prefix sum + first-occurrence map (transform 0 -> -1)",
        explain=(
            "Many 'balanced' problems become 'sum = 0' after a relabel. Equal prefix sums at two positions mean the "
            "stretch between them sums to 0."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time",
        brute=r"""
# BRUTE FORCE: O(n^2) time
def find_max_length(nums):
    best = 0

    for i in range(len(nums)):
        bal = 0
        for j in range(i, len(nums)):
            bal += 1 if nums[j] else -1
            if bal == 0:
                best = max(best, j - i + 1)

    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Prefix sum + first-occurrence map (transform 0 -> -1)
def find_max_length(nums):
    first = {0: -1}
    s = best = 0

    for i, x in enumerate(nums):
        s += 1 if x else -1
        if s in first:
            best = max(best, i - first[s])
        else:
            first[s] = i

    return best
""",
    ),
    # ---- Subarray Sums Divisible by K (LeetCode 974) ----
    dict(
        title="Subarray Sums Divisible by K",
        diff="M",
        lc=974,
        slug="subarray-sums-divisible-by-k",
        prompt="Count the non-empty subarrays whose sum is divisible by k.",
        sig="def subarrays_div_by_k(nums: List[int], k: int) -> int:",
        fn="subarrays_div_by_k",
        tests=[
            (([4, 5, 0, -2, -3, 1], 5), 7),
            (([5], 9), 0),
            (([5, 5], 5), 3),
            (([-1, 2, 9], 2), 2),
            (([0, 0, 0], 3), 6),
        ],
        hints=[
            "sum(i..j) = P[j+1] - P[i]. When is that divisible by k?",
            "When P[j+1] and P[i] leave the same remainder mod k.",
            (
                "Count prefix remainders in a dict (start with {0: 1}); each time add count[r] then increment. "
                "Python's % is already non-negative."
            ),
        ],
        pattern="Prefix sums modulo k (same remainder = divisible difference)",
        explain=(
            "Differences are divisible by k exactly when the two numbers have equal remainders, so count equal "
            "remainders instead of testing pairs."
        ),
        cx="O(n) time, O(k) space",
        brute_cx="O(n^2) time",
        brute=r"""
# BRUTE FORCE: O(n^2) time
def subarrays_div_by_k(nums, k):
    c = 0

    for i in range(len(nums)):
        s = 0
        for j in range(i, len(nums)):
            s += nums[j]
            if s % k == 0:
                c += 1

    return c
""",
        solution=r"""
# OPTIMISED: O(n) time, O(k) space
# Idea: Prefix sums modulo k (same remainder = divisible difference)
def subarrays_div_by_k(nums, k):
    seen = Counter({0: 1})
    s = ans = 0
    for x in nums:
        s = (s + x) % k
        ans += seen[s]
        seen[s] += 1
    return ans
""",
    ),
]
