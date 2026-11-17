"""more Array problems (batch 4) - part of the problem bank for the "array_tricks" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Majority Element II (LeetCode 229) ----
    dict(
        title="Majority Element II",
        diff="M",
        lc=229,
        slug="majority-element-ii",
        prompt="Return all elements that appear MORE than n/3 times (any order). Aim for O(n) time and O(1) space.",
        sig="def majority_element(nums: List[int]) -> List[int]:",
        fn="majority_element",
        compare="unordered",
        tests=[
            (([3, 2, 3],), [3]),
            (([1],), [1]),
            (([1, 2],), [1, 2]),
            (([1, 1, 1, 3, 3, 2, 2, 2],), [1, 2]),
        ],
        hints=[
            "At most TWO values can appear more than n/3 times.",
            (
                "Boyer-Moore voting generalises: keep two candidates with two counters; a different value cancels "
                "one vote from each."
            ),
            "A candidate is only a candidate - do a second pass counting each and keep those with count > n/3.",
        ],
        pattern="Boyer-Moore voting with two candidates",
        explain=(
            "Each cancellation removes three distinct values (one vote each from two candidates plus the newcomer). "
            "A value appearing more than n/3 times cannot be fully cancelled, so it survives as a candidate."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - count everything in a hash map",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - count everything in a hash map
def majority_element(nums):
    counts = Counter(nums)
    return [value for value, c in counts.items() if c > len(nums) // 3]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Boyer-Moore voting with two candidates
def majority_element(nums):
    cand1 = cand2 = None
    count1 = count2 = 0

    for x in nums:
        if x == cand1:
            count1 += 1
        elif x == cand2:
            count2 += 1
        elif count1 == 0:
            cand1, count1 = x, 1
        elif count2 == 0:
            cand2, count2 = x, 1
        else:
            count1 -= 1  # three different values cancel each other
            count2 -= 1

    return [c for c in (cand1, cand2) if c is not None and nums.count(c) > len(nums) // 3]
""",
    ),
    # ---- Find All Numbers Disappeared in an Array (LeetCode 448) ----
    dict(
        title="Find All Numbers Disappeared in an Array",
        diff="E",
        lc=448,
        slug="find-all-numbers-disappeared-in-an-array",
        prompt=(
            "nums has n values, each in 1..n. Return every number in 1..n that does not appear (any order). Use "
            "O(1) extra space."
        ),
        sig="def find_disappeared_numbers(nums: List[int]) -> List[int]:",
        fn="find_disappeared_numbers",
        compare="unordered",
        tests=[
            (([4, 3, 2, 7, 8, 2, 3, 1],), [5, 6]),
            (([1, 1],), [2]),
            (([1],), []),
            (([2, 2, 2],), [1, 3]),
        ],
        hints=[
            "A set of the numbers makes it easy - but uses O(n) space.",
            "The values are valid INDICES (value - 1), so the array itself can be the 'seen' table.",
            (
                "For each x, make nums[abs(x) - 1] negative. Afterwards the indices still positive are the missing "
                "numbers."
            ),
        ],
        pattern="Index as hash: mark visited by negating in place",
        explain=(
            "When values are confined to 1..n the array positions act as a free boolean array. Using the sign as "
            "the flag keeps the original value readable with abs()."
        ),
        cx="O(n) time, O(1) extra space",
        brute_cx="O(n) time, O(n) space - a set and a scan",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - a set and a scan
def find_disappeared_numbers(nums):
    seen = set(nums)
    return [i for i in range(1, len(nums) + 1) if i not in seen]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) extra space
# Idea: Index as hash: mark visited by negating in place
def find_disappeared_numbers(nums):
    nums = list(nums)  # keep the caller's list intact
    for x in nums:
        index = abs(x) - 1
        nums[index] = -abs(nums[index])  # mark "value index+1 was seen"
    return [i + 1 for i, x in enumerate(nums) if x > 0]  # never marked: missing
""",
    ),
    # ---- Max Consecutive Ones (LeetCode 485) ----
    dict(
        title="Max Consecutive Ones",
        diff="E",
        lc=485,
        slug="max-consecutive-ones",
        prompt="Given a binary array, return the maximum number of consecutive 1s.",
        sig="def find_max_consecutive_ones(nums: List[int]) -> int:",
        fn="find_max_consecutive_ones",
        tests=[
            (([1, 1, 0, 1, 1, 1],), 3),
            (([1, 0, 1, 1, 0, 1],), 2),
            (([0],), 0),
            (([1, 1, 1],), 3),
        ],
        hints=[
            "Keep a counter of the current run of 1s.",
            "A 1 extends the run; a 0 resets it to 0.",
            "Update the best answer after every element.",
        ],
        pattern="Running streak counter",
        explain="One variable for the current streak and one for the best is all the state this needs.",
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - extend a run from every starting index",
        brute=r"""
# BRUTE FORCE: O(n^2) time - extend a run from every starting index
def find_max_consecutive_ones(nums):
    best = 0
    for i in range(len(nums)):
        j = i
        while j < len(nums) and nums[j] == 1:  # extend the run starting at i
            j += 1
        best = max(best, j - i)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Running streak counter
def find_max_consecutive_ones(nums):
    best = run = 0
    for x in nums:
        run = run + 1 if x == 1 else 0
        best = max(best, run)
    return best
""",
    ),
    # ---- Pascal's Triangle (LeetCode 118) ----
    dict(
        title="Pascal's Triangle",
        diff="E",
        lc=118,
        slug="pascals-triangle",
        prompt="Return the first num_rows rows of Pascal's triangle.",
        sig="def generate(num_rows: int) -> List[List[int]]:",
        fn="generate",
        tests=[
            ((5,), [[1], [1, 1], [1, 2, 1], [1, 3, 3, 1], [1, 4, 6, 4, 1]]),
            ((1,), [[1]]),
            ((2,), [[1], [1, 1]]),
        ],
        hints=[
            "Each row starts and ends with 1.",
            "Every inner number is the sum of the two numbers above it.",
            "Build each row from the previous one: row[i] = prev[i - 1] + prev[i].",
        ],
        pattern="Build each row from the previous row",
        explain=(
            "The recurrence C(n, k) = C(n-1, k-1) + C(n-1, k) is exactly Pascal's rule, so no factorials are needed."
        ),
        cx="O(n^2) time and output size",
        brute_cx="O(n^3) time - compute every entry independently with factorials",
        brute=r"""
# BRUTE FORCE: O(n^3) time - compute every entry independently with factorials
def generate(num_rows):
    return [
        [math.factorial(n) // (math.factorial(k) * math.factorial(n - k)) for k in range(n + 1)]
        for n in range(num_rows)
    ]
""",
        solution=r"""
# OPTIMISED: O(n^2) time and output size
# Idea: Build each row from the previous row
def generate(num_rows):
    rows = [[1]]
    for _ in range(1, num_rows):
        prev = rows[-1]
        rows.append([1] + [prev[i - 1] + prev[i] for i in range(1, len(prev))] + [1])
    return rows
""",
    ),
    # ---- Pascal's Triangle II (LeetCode 119) ----
    dict(
        title="Pascal's Triangle II",
        diff="E",
        lc=119,
        slug="pascals-triangle-ii",
        prompt="Return row row_index (0-indexed) of Pascal's triangle using only O(row_index) extra space.",
        sig="def get_row(row_index: int) -> List[int]:",
        fn="get_row",
        tests=[
            ((3,), [1, 3, 3, 1]),
            ((0,), [1]),
            ((1,), [1, 1]),
            ((5,), [1, 5, 10, 10, 5, 1]),
        ],
        hints=[
            "You do not need to keep the previous rows - only the current one.",
            "Update the row IN PLACE: row[j] += row[j - 1].",
            "Go right to left, otherwise you overwrite a value you still need.",
        ],
        pattern="In-place DP row update (iterate backwards)",
        explain=(
            "Going from the right means row[j - 1] still holds the previous row's value when row[j] is updated, the "
            "same trick as 1-D knapsack."
        ),
        cx="O(n^2) time, O(n) space",
        brute_cx="O(n^2) time, O(n^2) space - build every row and keep them all",
        brute=r"""
# BRUTE FORCE: O(n^2) time, O(n^2) space - build every row and keep them all
def get_row(row_index):
    rows = [[1]]
    for _ in range(row_index):
        prev = rows[-1]
        rows.append([1] + [prev[i - 1] + prev[i] for i in range(1, len(prev))] + [1])
    return rows[row_index]
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n) space
# Idea: In-place DP row update (iterate backwards)
def get_row(row_index):
    row = [1] * (row_index + 1)
    for i in range(2, row_index + 1):
        for j in range(i - 1, 0, -1):  # right to left keeps row[j - 1] as the OLD value
            row[j] += row[j - 1]
    return row
""",
    ),
    # ---- Third Maximum Number (LeetCode 414) ----
    dict(
        title="Third Maximum Number",
        diff="E",
        lc=414,
        slug="third-maximum-number",
        prompt=(
            "Return the third DISTINCT maximum of nums. If there are fewer than three distinct values, return the "
            "maximum."
        ),
        sig="def third_max(nums: List[int]) -> int:",
        fn="third_max",
        tests=[
            (([3, 2, 1],), 1),
            (([1, 2],), 2),
            (([2, 2, 3, 1],), 1),
            (([1, 1, 2],), 2),
            (([5, 2, 4, 1, 3, 6, 0],), 4),
        ],
        hints=[
            "Sorting a set of the values works in O(n log n).",
            "You only ever need the top three distinct values: keep three variables.",
            (
                "For each x: skip it if it equals one of the three; otherwise insert it into the right slot and "
                "shift the others down."
            ),
        ],
        pattern="Track the top-k with k variables",
        explain="For a small fixed k, a handful of variables beats sorting: one pass, constant space.",
        cx="O(n) time, O(1) space",
        brute_cx="O(n log n) time - sort the distinct values",
        brute=r"""
# BRUTE FORCE: O(n log n) time - sort the distinct values
def third_max(nums):
    distinct = sorted(set(nums), reverse=True)
    return distinct[2] if len(distinct) >= 3 else distinct[0]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Track the top-k with k variables
def third_max(nums):
    first = second = third = None

    for x in nums:
        if x in (first, second, third):
            continue  # only distinct values count

        if first is None or x > first:
            first, second, third = x, first, second
        elif second is None or x > second:
            second, third = x, second
        elif third is None or x > third:
            third = x

    return third if third is not None else first
""",
    ),
    # ---- Maximum Product of Three Numbers (LeetCode 628) ----
    dict(
        title="Maximum Product of Three Numbers",
        diff="E",
        lc=628,
        slug="maximum-product-of-three-numbers",
        prompt="Return the maximum product of any three numbers in nums (length >= 3).",
        sig="def maximum_product(nums: List[int]) -> int:",
        fn="maximum_product",
        tests=[
            (([1, 2, 3],), 6),
            (([1, 2, 3, 4],), 24),
            (([-1, -2, -3],), -6),
            (([-100, -98, -1, 2, 3, 4],), 39200),
        ],
        hints=[
            "The three largest numbers are one candidate.",
            (
                "Two big negatives multiply to a big positive - the other candidate is the two SMALLEST numbers "
                "times the largest."
            ),
            "Answer = max(top3 product, two smallest * largest).",
        ],
        pattern="Consider both ends of the sorted order (negatives flip signs)",
        explain=(
            "A maximum product of three uses either three large positives or one large positive and two very "
            "negative numbers. No other combination can win."
        ),
        cx="O(n) time",
        brute_cx="O(n^3) time - every triple",
        brute=r"""
# BRUTE FORCE: O(n^3) time - every triple
def maximum_product(nums):
    return max(a * b * c for a, b, c in itertools.combinations(nums, 3))
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Consider both ends of the sorted order (negatives flip signs)
def maximum_product(nums):
    top3 = heapq.nlargest(3, nums)  # the three biggest
    low2 = heapq.nsmallest(2, nums)  # the two most negative
    return max(top3[0] * top3[1] * top3[2], low2[0] * low2[1] * top3[0])
""",
    ),
    # ---- Non-decreasing Array (LeetCode 665) ----
    dict(
        title="Non-decreasing Array",
        diff="M",
        lc=665,
        slug="non-decreasing-array",
        prompt="Return True if nums can become non-decreasing by changing AT MOST ONE element.",
        sig="def check_possibility(nums: List[int]) -> bool:",
        fn="check_possibility",
        tests=[
            (([4, 2, 3],), True),
            (([4, 2, 1],), False),
            (([3, 4, 2, 3],), False),
            (([1],), True),
            (([5, 7, 1, 8],), True),
        ],
        hints=[
            "Find the first place where nums[i] > nums[i + 1]; a second such place means False.",
            "At that place you can lower nums[i] or raise nums[i + 1].",
            (
                "Prefer lowering nums[i] to nums[i + 1] when nums[i - 1] <= nums[i + 1]; otherwise you must raise "
                "nums[i + 1] to nums[i]."
            ),
        ],
        pattern="One-pass greedy with a single allowed repair",
        explain=(
            "Lowering the earlier element is the less harmful repair because it only affects the past, which has "
            "already been checked. Only when that would break the previous element do we raise the later one."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - try setting each element to a neighbour's value and re-check",
        brute=r"""
# BRUTE FORCE: O(n^2) time - try setting each element to a neighbour's value and re-check
def check_possibility(nums):
    def sorted_ok(arr):
        return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))

    if sorted_ok(nums):
        return True

    for i in range(len(nums)):
        for neighbour in (i - 1, i + 1):  # change nums[i] to a neighbour's value
            if 0 <= neighbour < len(nums):
                trial = list(nums)
                trial[i] = nums[neighbour]
                if sorted_ok(trial):
                    return True

    return False
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: One-pass greedy with a single allowed repair
def check_possibility(nums):
    nums, repairs = list(nums), 0

    for i in range(len(nums) - 1):
        if nums[i] > nums[i + 1]:
            repairs += 1
            if repairs > 1:
                return False
            if i == 0 or nums[i - 1] <= nums[i + 1]:
                nums[i] = nums[i + 1]  # lower the earlier value
            else:
                nums[i + 1] = nums[i]  # otherwise raise the later value

    return True
""",
    ),
]
