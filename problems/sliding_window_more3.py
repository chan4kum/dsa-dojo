"""more Sliding Window problems (batch 4) - part of the problem bank for the "sliding_window" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Maximum Number of Vowels in a Substring of Given Length (LeetCode 1456) ----
    dict(
        title="Maximum Number of Vowels in a Substring of Given Length",
        diff="M",
        lc=1456,
        slug="maximum-number-of-vowels-in-a-substring-of-given-length",
        prompt="Return the maximum number of vowel letters (a, e, i, o, u) in any substring of s of length k.",
        sig="def max_vowels(s: str, k: int) -> int:",
        fn="max_vowels",
        tests=[
            (("abciiidef", 3), 3),
            (("aeiou", 2), 2),
            (("leetcode", 3), 2),
            (("rhythms", 4), 0),
        ],
        hints=[
            "Counting the vowels of every window from scratch costs O(k) each.",
            "Slide the window one step: add the new right character, remove the old left one.",
            "Keep a running vowel count; update the best after each step.",
        ],
        pattern="Fixed-size sliding window with a running count",
        explain="Each step changes the window by exactly one character on each side, so the count updates in O(1).",
        cx="O(n) time, O(1) space",
        brute_cx="O(n * k) time - recount every window",
        brute=r"""
# BRUTE FORCE: O(n * k) time - recount every window
def max_vowels(s, k):
    return max(sum(ch in "aeiou" for ch in s[i : i + k]) for i in range(len(s) - k + 1))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Fixed-size sliding window with a running count
def max_vowels(s, k):
    vowels = set("aeiou")
    count = sum(ch in vowels for ch in s[:k])  # the first window
    best = count
    for i in range(k, len(s)):
        count += (s[i] in vowels) - (s[i - k] in vowels)  # one letter enters, one leaves
        best = max(best, count)
    return best
""",
    ),
    # ---- Grumpy Bookstore Owner (LeetCode 1052) ----
    dict(
        title="Grumpy Bookstore Owner",
        diff="M",
        lc=1052,
        slug="grumpy-bookstore-owner",
        prompt=(
            "customers[i] enter in minute i; the owner is grumpy that minute if grumpy[i] == 1 (those customers are "
            "unsatisfied). A secret technique keeps the owner calm for `minutes` consecutive minutes, once. Return "
            "the maximum number of satisfied customers."
        ),
        sig="def max_satisfied(customers: List[int], grumpy: List[int], minutes: int) -> int:",
        fn="max_satisfied",
        tests=[
            (([1, 0, 1, 2, 1, 1, 7, 5], [0, 1, 0, 1, 0, 1, 0, 1], 3), 16),
            (([1], [0], 1), 1),
            (([4, 10, 10], [1, 1, 0], 2), 24),
            (([3, 3, 3], [1, 1, 1], 1), 3),
        ],
        hints=[
            "Customers in non-grumpy minutes are always satisfied - add them up as a base.",
            "The technique only adds the customers of GRUMPY minutes inside the chosen window.",
            "Find the window of `minutes` with the largest sum of customers[i] * grumpy[i] using a sliding window.",
        ],
        pattern="Fixed-size sliding window maximising the extra gain",
        explain=(
            "Split the answer into a fixed part (calm minutes) and a part the window can improve. Only the second "
            "needs a search."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n * minutes) time - try every window start",
        brute=r"""
# BRUTE FORCE: O(n * minutes) time - try every window start
def max_satisfied(customers, grumpy, minutes):
    best = 0

    for start in range(len(customers) - minutes + 1):  # try the calm window at every position
        total = 0
        for i, (c, g) in enumerate(zip(customers, grumpy)):
            if g == 0 or start <= i < start + minutes:
                total += c
        best = max(best, total)

    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Fixed-size sliding window maximising the extra gain
def max_satisfied(customers, grumpy, minutes):
    base = sum(c for c, g in zip(customers, grumpy) if g == 0)  # always satisfied
    extra = best_extra = sum(c * g for c, g in zip(customers[:minutes], grumpy[:minutes]))

    for i in range(minutes, len(customers)):
        extra += (
            customers[i] * grumpy[i] - customers[i - minutes] * grumpy[i - minutes]
        )  # slide the window
        best_extra = max(best_extra, extra)

    return base + best_extra
""",
    ),
    # ---- Binary Subarrays With Sum (LeetCode 930) ----
    dict(
        title="Binary Subarrays With Sum",
        diff="M",
        lc=930,
        slug="binary-subarrays-with-sum",
        prompt="nums is a binary array. Return the number of non-empty subarrays whose sum equals goal.",
        sig="def num_subarrays_with_sum(nums: List[int], goal: int) -> int:",
        fn="num_subarrays_with_sum",
        tests=[
            (([1, 0, 1, 0, 1], 2), 4),
            (([0, 0, 0, 0, 0], 0), 15),
            (([1, 1], 2), 1),
            (([1], 0), 0),
        ],
        hints=[
            (
                "Let prefix be the running sum. A subarray ending here has sum goal if an earlier prefix equals "
                "prefix - goal."
            ),
            "Count how many times each prefix value has occurred in a hash map.",
            "For each element add counts[prefix - goal] to the answer, then record the current prefix.",
        ],
        pattern="Prefix sum + hash map of counts",
        explain=(
            "This is Subarray Sum Equals K specialised to a binary array; zeros make many subarrays share a sum, "
            "which the counter handles."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - every start with a running sum",
        brute=r"""
# BRUTE FORCE: O(n^2) time - every start with a running sum
def num_subarrays_with_sum(nums, goal):
    count = 0

    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == goal:
                count += 1

    return count
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Prefix sum + hash map of counts
def num_subarrays_with_sum(nums, goal):
    seen = defaultdict(int)
    seen[0] = 1  # the empty prefix
    prefix = count = 0

    for x in nums:
        prefix += x
        count += seen[
            prefix - goal
        ]  # earlier prefixes that leave exactly `goal` between them and here
        seen[prefix] += 1

    return count
""",
    ),
    # ---- Subarrays with K Different Integers (LeetCode 992) ----
    dict(
        title="Subarrays with K Different Integers",
        diff="H",
        lc=992,
        slug="subarrays-with-k-different-integers",
        prompt="Return the number of subarrays of nums that contain exactly k distinct integers.",
        sig="def subarrays_with_k_distinct(nums: List[int], k: int) -> int:",
        fn="subarrays_with_k_distinct",
        tests=[
            (([1, 2, 1, 2, 3], 2), 7),
            (([1, 2, 1, 3, 4], 3), 3),
            (([1, 1, 1], 1), 6),
            (([1, 2], 3), 0),
        ],
        hints=[
            "'At most k distinct' is easy with a sliding window - the window stays valid when shrunk.",
            "'Exactly k' is hard directly, but exactly(k) = atMost(k) - atMost(k - 1).",
            (
                "In atMost(k): for each right end, shrink from the left until at most k distinct remain, then add "
                "(right - left + 1) subarrays."
            ),
        ],
        pattern="Exactly K = atMost(K) - atMost(K - 1)",
        explain=(
            "A window can only be shrunk safely for monotone conditions. 'At most' is monotone, 'exactly' is not, "
            "so we subtract two monotone counts."
        ),
        cx="O(n) time, O(k) space",
        brute_cx="O(n^2) time - extend every start and track distinct values",
        brute=r"""
# BRUTE FORCE: O(n^2) time - extend every start and track distinct values
def subarrays_with_k_distinct(nums, k):
    count = 0

    for i in range(len(nums)):
        seen = set()
        for j in range(i, len(nums)):
            seen.add(nums[j])
            if len(seen) == k:
                count += 1
            elif len(seen) > k:
                break

    return count
""",
        solution=r"""
# OPTIMISED: O(n) time, O(k) space
# Idea: Exactly K = atMost(K) - atMost(K - 1)
def subarrays_with_k_distinct(nums, k):
    def at_most(limit):  # subarrays with at most `limit` distinct values
        counts, left, total = defaultdict(int), 0, 0

        for right, x in enumerate(nums):
            counts[x] += 1
            while len(counts) > limit:  # shrink until valid again
                counts[nums[left]] -= 1
                if counts[nums[left]] == 0:
                    del counts[nums[left]]
                left += 1
            total += right - left + 1  # every start in [left, right] works

        return total

    return at_most(k) - at_most(k - 1)
""",
    ),
]
