"""more Greedy problems (batch 4) - part of the problem bank for the "greedy" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Two City Scheduling (LeetCode 1029) ----
    dict(
        title="Two City Scheduling",
        diff="M",
        lc=1029,
        slug="two-city-scheduling",
        prompt=(
            "2n people; costs[i] = [cost to fly person i to city A, cost to city B]. Exactly n people must go to "
            "each city. Return the minimum total cost."
        ),
        sig="def two_city_sched_cost(costs: List[List[int]]) -> int:",
        fn="two_city_sched_cost",
        tests=[
            (([[10, 20], [30, 200], [400, 50], [30, 20]],), 110),
            (([[259, 770], [448, 54], [926, 667], [184, 139], [840, 118], [577, 469]],), 1859),
            (([[10, 20], [30, 200]],), 50),
            (([[1, 1], [1, 1]],), 2),
        ],
        hints=[
            "Imagine sending everyone to city A first. Then choose n people to switch to B.",
            "Switching person i changes the total by (B - A). Pick the n people whose switch is the cheapest.",
            "Sort by (a - b): the first n go to A, the rest go to B.",
        ],
        pattern="Greedy by difference (opportunity cost)",
        explain=(
            "The decision for one person depends on how much better A is than B, not on absolute prices. Sorting by "
            "a - b puts the people who prefer A most first; the n most A-leaning go to A."
        ),
        cx="O(n log n) time",
        brute_cx="O(C(2n, n) * n) time - try every way of choosing who goes to A",
        brute=r"""
# BRUTE FORCE: O(C(2n, n) * n) time - try every way of choosing who goes to A
def two_city_sched_cost(costs):
    n = len(costs) // 2
    best = float("inf")
    for to_a in itertools.combinations(range(2 * n), n):  # every group of n people for city A
        chosen = set(to_a)
        total = sum(costs[i][0] if i in chosen else costs[i][1] for i in range(2 * n))
        best = min(best, total)
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Greedy by difference (opportunity cost)
def two_city_sched_cost(costs):
    ordered = sorted(
        costs, key=lambda c: c[0] - c[1]
    )  # people who save most by going to A come first
    n = len(costs) // 2
    return sum(c[0] for c in ordered[:n]) + sum(c[1] for c in ordered[n:])
""",
    ),
    # ---- Maximize Sum Of Array After K Negations (LeetCode 1005) ----
    dict(
        title="Maximize Sum Of Array After K Negations",
        diff="E",
        lc=1005,
        slug="maximize-sum-of-array-after-k-negations",
        prompt=(
            "Exactly k times, pick any index and negate nums[i] (the same index may be picked again). Return the "
            "largest possible sum."
        ),
        sig="def largest_sum_after_k_negations(nums: List[int], k: int) -> int:",
        fn="largest_sum_after_k_negations",
        tests=[
            (([4, 2, 3], 1), 5),
            (([3, -1, 0, 2], 3), 6),
            (([2, -3, -1, 5, -4], 2), 13),
            (([-8, 3, -5, -3, -5, -2], 6), 22),
        ],
        hints=[
            "Flipping a negative number up helps; flipping the MOST negative one helps most.",
            "Flip the smallest numbers while they are negative and k remains.",
            "If k is still odd afterwards, one flip is forced: flip the smallest absolute value (a 0 makes it free).",
        ],
        pattern="Greedy: spend each action on the best remaining gain",
        explain=(
            "Each negation of a negative x gains 2*|x|, so use them on the biggest |x| first. Two flips of the same "
            "number cancel, so only the parity of the leftover k matters."
        ),
        cx="O(n log n) time",
        brute_cx="O(n^k) time - try every index for each of the k negations",
        brute=r"""
# BRUTE FORCE: O(n^k) time - try every index for each of the k negations
def largest_sum_after_k_negations(nums, k):
    best = float("-inf")

    def go(arr, left):
        nonlocal best
        if left == 0:
            best = max(best, sum(arr))
            return
        for i in range(len(arr)):
            arr[i] = -arr[i]  # try negating index i ...
            go(arr, left - 1)
            arr[i] = -arr[i]  # ... then undo it

    go(list(nums), k)
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Greedy: spend each action on the best remaining gain
def largest_sum_after_k_negations(nums, k):
    nums = sorted(nums)
    for i in range(len(nums)):
        if k > 0 and nums[i] < 0:
            nums[i] = -nums[i]  # most negative first
            k -= 1
    # an odd leftover must negate one number: the smallest is cheapest to lose
    return sum(nums) - (2 * min(nums) if k % 2 else 0)
""",
    ),
    # ---- Largest Perimeter Triangle (LeetCode 976) ----
    dict(
        title="Largest Perimeter Triangle",
        diff="E",
        lc=976,
        slug="largest-perimeter-triangle",
        prompt=(
            "Given side lengths, return the largest perimeter of a triangle with non-zero area formed from three of "
            "them, or 0 if impossible."
        ),
        sig="def largest_perimeter(nums: List[int]) -> int:",
        fn="largest_perimeter",
        tests=[
            (([2, 1, 2],), 5),
            (([1, 2, 1, 10],), 0),
            (([3, 2, 3, 4],), 10),
            (([3, 6, 2, 3],), 8),
        ],
        hints=[
            "Three sides a <= b <= c form a triangle exactly when a + b > c.",
            "Larger sides give a larger perimeter, so look at the biggest sides first.",
            "Sort descending; for each i check nums[i] < nums[i+1] + nums[i+2]. The first success is the answer.",
        ],
        pattern="Sort, then test neighbours in a greedy order",
        explain=(
            "For a fixed longest side, the best partners are the next two largest values, because they make a + b "
            "as large as possible. If even those fail, no triple with this longest side works."
        ),
        cx="O(n log n) time",
        brute_cx="O(n^3) time - test every triple",
        brute=r"""
# BRUTE FORCE: O(n^3) time - test every triple
def largest_perimeter(nums):
    best = 0
    for a, b, c in itertools.combinations(nums, 3):
        x, y, z = sorted((a, b, c))
        if x + y > z:
            best = max(best, a + b + c)
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Sort, then test neighbours in a greedy order
def largest_perimeter(nums):
    nums = sorted(nums, reverse=True)
    for i in range(len(nums) - 2):
        if nums[i] < nums[i + 1] + nums[i + 2]:  # the three consecutive values form a triangle
            return nums[i] + nums[i + 1] + nums[i + 2]
    return 0
""",
    ),
    # ---- Array Partition (LeetCode 561) ----
    dict(
        title="Array Partition",
        diff="E",
        lc=561,
        slug="array-partition",
        prompt=(
            "Split 2n numbers into n pairs to maximise the sum of min(a, b) over the pairs. Return that maximum sum."
        ),
        sig="def array_pair_sum(nums: List[int]) -> int:",
        fn="array_pair_sum",
        tests=[
            (([1, 4, 3, 2],), 4),
            (([6, 2, 6, 5, 1, 2],), 9),
            (([1, 1],), 1),
            (([-3, -1, 2, 5],), -1),
        ],
        hints=[
            "In each pair only the smaller number counts, so the larger one is 'wasted'.",
            "Waste as little as possible: pair every number with its closest neighbour in value.",
            "Sort and add every element at an even index.",
        ],
        pattern="Sort, then pair neighbours",
        explain=(
            "After sorting, pairing (a0,a1), (a2,a3), ... wastes the smallest possible amount, because each larger "
            "partner is as close in value as it can be."
        ),
        cx="O(n log n) time",
        brute_cx="O((2n - 1)!!) time - try every way of pairing the numbers",
        brute=r"""
# BRUTE FORCE: O((2n - 1)!!) time - try every way of pairing the numbers
def array_pair_sum(nums):
    def best(rest):  # best sum of mins when pairing up the list `rest`
        if not rest:
            return 0
        first, others = rest[0], rest[1:]
        return max(
            min(first, others[i]) + best(others[:i] + others[i + 1 :]) for i in range(len(others))
        )

    return best(list(nums))
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Sort, then pair neighbours
def array_pair_sum(nums):
    return sum(sorted(nums)[::2])  # the smaller number of each neighbouring pair
""",
    ),
    # ---- Can Place Flowers (LeetCode 605) ----
    dict(
        title="Can Place Flowers",
        diff="E",
        lc=605,
        slug="can-place-flowers",
        prompt=(
            "flowerbed is a list of 0 (empty) and 1 (planted); no two flowers may be adjacent. Return True if n "
            "more flowers can be planted."
        ),
        sig="def can_place_flowers(flowerbed: List[int], n: int) -> bool:",
        fn="can_place_flowers",
        tests=[
            (([1, 0, 0, 0, 1], 1), True),
            (([1, 0, 0, 0, 1], 2), False),
            (([0], 1), True),
            (([0, 0, 0, 0, 0], 3), True),
            (([1], 0), True),
        ],
        hints=[
            "A spot is usable if it is empty and both neighbours (where they exist) are empty.",
            (
                "Scan left to right and plant as early as you can - planting earlier never blocks more spots than "
                "planting later."
            ),
            "Count the flowers you plant; stop early once the count reaches n.",
        ],
        pattern="Greedy left-to-right placement",
        explain=(
            "Planting at the first legal spot only blocks the next one, which a later plant would block as well (or "
            "worse). So earliest-first achieves the maximum."
        ),
        cx="O(n) time, O(1) extra space",
        brute_cx="O(2^n) time - try planting or skipping at every position",
        brute=r"""
# BRUTE FORCE: O(2^n) time - try planting or skipping at every position
def can_place_flowers(flowerbed, n):
    bed = list(flowerbed)

    def most(i):  # the most flowers that can still be planted from position i onwards
        if i >= len(bed):
            return 0
        left_free = i == 0 or bed[i - 1] == 0
        right_free = i == len(bed) - 1 or bed[i + 1] == 0
        skip = most(i + 1)
        if bed[i] == 0 and left_free and right_free:
            bed[i] = 1  # try planting here
            planted = 1 + most(i + 1)
            bed[i] = 0
            return max(skip, planted)
        return skip

    return most(0) >= n
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) extra space
# Idea: Greedy left-to-right placement
def can_place_flowers(flowerbed, n):
    bed, planted = list(flowerbed), 0
    for i in range(len(bed)):
        left_free = i == 0 or bed[i - 1] == 0
        right_free = i == len(bed) - 1 or bed[i + 1] == 0
        if bed[i] == 0 and left_free and right_free:
            bed[i] = 1  # plant now: it can only help
            planted += 1
    return planted >= n
""",
    ),
    # ---- Boats to Save People (LeetCode 881) ----
    dict(
        title="Boats to Save People",
        diff="M",
        lc=881,
        slug="boats-to-save-people",
        prompt=(
            "Each boat carries at most 2 people with total weight <= limit (every person weighs <= limit). Return "
            "the minimum number of boats."
        ),
        sig="def num_rescue_boats(people: List[int], limit: int) -> int:",
        fn="num_rescue_boats",
        tests=[
            (([1, 2], 3), 1),
            (([3, 2, 2, 1], 3), 3),
            (([3, 5, 3, 4], 5), 4),
            (([5, 1, 4, 2], 6), 2),
        ],
        hints=[
            "The heaviest person must take a boat. Who is the best partner for them?",
            "The lightest person - if even the lightest cannot join, nobody can.",
            "Sort; two pointers: always ship the heaviest, and also the lightest if they fit together.",
        ],
        pattern="Sort + two pointers (pair the heaviest with the lightest)",
        explain=(
            "If the heaviest cannot share with the lightest, they cannot share with anyone, so they go alone. If "
            "they can, taking the lightest along removes the easiest-to-pair person at no cost."
        ),
        cx="O(n log n) time",
        brute_cx="O(n!!) time - try every way of pairing people or sending them alone",
        brute=r"""
# BRUTE FORCE: O(n!!) time - try every way of pairing people or sending them alone
def num_rescue_boats(people, limit):
    def fewest(rest):  # fewest boats for the people in `rest`
        if not rest:
            return 0
        first, others = rest[0], rest[1:]
        best = 1 + fewest(others)  # the first person rides alone
        for i, other in enumerate(others):
            if first + other <= limit:
                best = min(
                    best, 1 + fewest(others[:i] + others[i + 1 :])
                )  # share a boat with one other person
        return best

    return fewest(list(people))
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Sort + two pointers (pair the heaviest with the lightest)
def num_rescue_boats(people, limit):
    people = sorted(people)
    lo, hi, boats = 0, len(people) - 1, 0
    while lo <= hi:
        if people[lo] + people[hi] <= limit:
            lo += 1  # the lightest person shares the boat
        hi -= 1  # the heaviest person always leaves
        boats += 1
    return boats
""",
    ),
    # ---- Split a String in Balanced Strings (LeetCode 1221) ----
    dict(
        title="Split a String in Balanced Strings",
        diff="E",
        lc=1221,
        slug="split-a-string-in-balanced-strings",
        prompt=(
            "s has equally many 'L' and 'R'. Split it into the maximum number of consecutive balanced substrings "
            "(equal L and R in each)."
        ),
        sig="def balanced_string_split(s: str) -> int:",
        fn="balanced_string_split",
        tests=[
            (("RLRRLLRLRL",), 4),
            (("RLRRRLLRLL",), 2),
            (("LLLLRRRR",), 1),
            (("RL",), 1),
        ],
        hints=[
            "Keep a running balance: +1 for 'R', -1 for 'L'.",
            "Whenever the balance returns to 0, the prefix so far is balanced.",
            "Cut greedily at every zero and count the cuts.",
        ],
        pattern="Running balance / greedy cut at every zero",
        explain=(
            "Cutting as soon as the balance hits zero can only create more pieces; a longer piece would simply "
            "contain this one plus more balanced content."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - DP over every possible cut position",
        brute=r"""
# BRUTE FORCE: O(n^2) time - DP over every possible cut position
def balanced_string_split(s):
    n = len(s)
    best = [-1] * (n + 1)  # best[i] = most pieces for s[:i] (-1 = impossible)
    best[0] = 0
    for i in range(1, n + 1):
        for j in range(i):
            piece = s[j:i]
            if best[j] >= 0 and piece.count("L") == piece.count("R"):
                best[i] = max(best[i], best[j] + 1)
    return best[n]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Running balance / greedy cut at every zero
def balanced_string_split(s):
    balance = pieces = 0
    for ch in s:
        balance += 1 if ch == "R" else -1
        if balance == 0:
            pieces += 1  # a balanced prefix ends here
    return pieces
""",
    ),
]
