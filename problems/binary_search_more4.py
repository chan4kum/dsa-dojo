"""more Binary Search problems (batch 5) - part of the problem bank for the "binary_search" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
Most of these are "binary search on the ANSWER": the answer is a number, and a yes/no check tells whether a candidate
is big enough, so the answers form a pattern no, no, ..., yes, yes that binary search can cut in half.
"""

PROBLEMS = [
    # ---- Arranging Coins (LeetCode 441) ----
    dict(
        title="Arranging Coins",
        diff="E",
        lc=441,
        slug="arranging-coins",
        prompt=(
            "Row k of a staircase needs exactly k coins. With n coins, return the number of COMPLETE rows you can "
            "build."
        ),
        sig="def arrange_coins(n: int) -> int:",
        fn="arrange_coins",
        tests=[
            ((5,), 2),
            ((8,), 3),
            ((1,), 1),
            ((3,), 2),
            ((10,), 4),
            ((14,), 4),
        ],
        hints=[
            "k complete rows need k * (k + 1) / 2 coins.",
            "You want the largest k with k * (k + 1) / 2 <= n.",
            "That condition is true for small k and false for large k: binary search k in [0, n].",
        ],
        pattern="Binary search on the answer",
        explain=(
            "The cost k(k+1)/2 is increasing in k, so 'k rows are affordable' is monotone and the largest "
            "affordable k can be found by halving."
        ),
        cx="O(log n) time",
        brute_cx="O(sqrt(n)) time - subtract row after row",
        brute=r"""
# BRUTE FORCE: O(sqrt(n)) time - subtract row after row
def arrange_coins(n):
    rows = 0
    while n >= rows + 1:
        rows += 1
        n -= rows  # build the next row
    return rows
""",
        solution=r"""
# OPTIMISED: O(log n) time
# Idea: Binary search on the answer
def arrange_coins(n):
    lo, hi = 0, n

    while lo < hi:
        mid = (lo + hi + 1) // 2  # upper middle so the loop makes progress
        if mid * (mid + 1) // 2 <= n:
            lo = mid  # mid rows are affordable: try more
        else:
            hi = mid - 1

    return lo
""",
    ),
    # ---- Most Profit Assigning Work (LeetCode 826) ----
    dict(
        title="Most Profit Assigning Work",
        diff="M",
        lc=826,
        slug="most-profit-assigning-work",
        prompt=(
            "Job i has difficulty[i] and pays profit[i]. A worker can do any job with difficulty <= their ability, "
            "and each worker does at most one job (jobs can be repeated by different workers). Return the maximum "
            "total profit."
        ),
        sig="def max_profit_assignment(difficulty: List[int], profit: List[int], worker: List[int]) -> int:",
        fn="max_profit_assignment",
        tests=[
            (([2, 4, 6, 8, 10], [10, 20, 30, 40, 50], [4, 5, 6, 7]), 100),
            (([85, 47, 57], [24, 66, 99], [40, 25, 25]), 0),
            (([1], [5], [1, 1]), 10),
            (([5], [10], [3]), 0),
        ],
        hints=[
            "Each worker independently picks the best-paying job they can do.",
            "Sort jobs by difficulty and compute the running MAXIMUM profit up to each difficulty.",
            "For a worker, binary search the last job with difficulty <= ability and take that running maximum.",
        ],
        pattern="Sort + prefix maximum + binary search",
        explain=(
            "The best profit among all jobs up to a difficulty level is a non-decreasing function of the level, so "
            "one bisect per worker finds it."
        ),
        cx="O((n + m) log n) time",
        brute_cx="O(n * m) time - scan every job for every worker",
        brute=r"""
# BRUTE FORCE: O(n * m) time - scan every job for every worker
def max_profit_assignment(difficulty, profit, worker):
    total = 0
    for ability in worker:
        total += max([p for d, p in zip(difficulty, profit) if d <= ability], default=0)
    return total
""",
        solution=r"""
# OPTIMISED: O((n + m) log n) time
# Idea: Sort + prefix maximum + binary search
def max_profit_assignment(difficulty, profit, worker):
    jobs = sorted(zip(difficulty, profit))
    levels, best_so_far, running = [], [], 0

    for d, p in jobs:
        running = max(running, p)
        levels.append(d)
        best_so_far.append(running)  # best profit among jobs with difficulty <= d

    total = 0

    for ability in worker:
        i = bisect.bisect_right(levels, ability)
        if i:
            total += best_so_far[i - 1]

    return total
""",
    ),
    # ---- Find the Distance Value Between Two Arrays (LeetCode 1385) ----
    dict(
        title="Find the Distance Value Between Two Arrays",
        diff="E",
        lc=1385,
        slug="find-the-distance-value-between-two-arrays",
        prompt="Count the elements a of arr1 for which NO element b of arr2 satisfies |a - b| <= d.",
        sig="def find_the_distance_value(arr1: List[int], arr2: List[int], d: int) -> int:",
        fn="find_the_distance_value",
        tests=[
            (([4, 5, 8], [10, 9, 1, 8], 2), 2),
            (([1, 4, 2, 3], [-4, -3, 6, 10, 20, 30], 3), 2),
            (([2, 1, 100, 3], [-5, -2, 10, -3, 7], 6), 1),
            (([1], [1], 0), 0),
        ],
        hints=[
            "For each a you only care whether SOME b lies in [a - d, a + d].",
            "Sort arr2.",
            (
                "bisect_left(arr2, a - d) gives the first candidate; a is counted only if that candidate is missing "
                "or greater than a + d."
            ),
        ],
        pattern="Range-emptiness test with binary search",
        explain=(
            "In a sorted array the first element >= a - d is the best candidate for the interval, so one bisect "
            "decides the whole range."
        ),
        cx="O((n + m) log m) time",
        brute_cx="O(n * m) time - compare every pair",
        brute=r"""
# BRUTE FORCE: O(n * m) time - compare every pair
def find_the_distance_value(arr1, arr2, d):
    return sum(1 for a in arr1 if all(abs(a - b) > d for b in arr2))
""",
        solution=r"""
# OPTIMISED: O((n + m) log m) time
# Idea: Range-emptiness test with binary search
def find_the_distance_value(arr1, arr2, d):
    arr2 = sorted(arr2)
    count = 0
    for a in arr1:
        i = bisect.bisect_left(arr2, a - d)  # first value that is not too small
        if i == len(arr2) or arr2[i] > a + d:
            count += 1
    return count
""",
    ),
    # ---- Minimum Limit of Balls in a Bag (LeetCode 1760) ----
    dict(
        title="Minimum Limit of Balls in a Bag",
        diff="M",
        lc=1760,
        slug="minimum-limit-of-balls-in-a-bag",
        prompt=(
            "nums[i] is the number of balls in bag i. In one operation split a bag into two non-empty bags. With at "
            "most max_operations operations, minimise the size of the LARGEST bag (the penalty) and return it."
        ),
        sig="def minimum_size(nums: List[int], max_operations: int) -> int:",
        fn="minimum_size",
        tests=[
            (([9], 2), 3),
            (([2, 4, 8, 2], 4), 2),
            (([7], 1), 4),
            (([5], 0), 5),
        ],
        hints=[
            "Guess a penalty p. How many operations does it take to make every bag <= p?",
            "A bag of x balls needs ceil(x / p) - 1 = (x - 1) // p splits.",
            (
                "Fewer operations are needed as p grows, so binary search the smallest p whose total splits <= "
                "max_operations."
            ),
        ],
        pattern="Binary search on the answer with a feasibility check",
        explain=(
            "The check 'penalty p is achievable' is monotone in p (a bigger limit is never harder), which is "
            "exactly what binary search needs."
        ),
        cx="O(n log max) time",
        brute_cx="O(max * n) time - try every penalty from 1 upwards",
        brute=r"""
# BRUTE FORCE: O(max * n) time - try every penalty from 1 upwards
def minimum_size(nums, max_operations):
    for penalty in range(1, max(nums) + 1):
        if sum((x - 1) // penalty for x in nums) <= max_operations:
            return penalty
""",
        solution=r"""
# OPTIMISED: O(n log max) time
# Idea: Binary search on the answer with a feasibility check
def minimum_size(nums, max_operations):
    lo, hi = 1, max(nums)

    while lo < hi:
        mid = (lo + hi) // 2
        if sum((x - 1) // mid for x in nums) <= max_operations:
            hi = mid  # penalty mid works: look for a smaller one
        else:
            lo = mid + 1

    return lo
""",
    ),
    # ---- Minimum Speed to Arrive on Time (LeetCode 1870) ----
    dict(
        title="Minimum Speed to Arrive on Time",
        diff="M",
        lc=1870,
        slug="minimum-speed-to-arrive-on-time",
        prompt=(
            "You ride n trains in order; train i covers dist[i] km. Every train except the last must wait for the "
            "next whole hour before the next one departs. Return the minimum positive INTEGER speed (km/h) that "
            "gets you there within `hour` hours, or -1 if impossible."
        ),
        sig="def min_speed_on_time(dist: List[int], hour: float) -> int:",
        fn="min_speed_on_time",
        tests=[
            (([1, 3, 2], 6), 1),
            (([1, 3, 2], 2.7), 3),
            (([1, 3, 2], 1.9), -1),
            (([1], 0.5), 2),
        ],
        hints=[
            "For a speed s the total time is sum(ceil(d / s)) over all but the last train, plus dist[-1] / s.",
            "Higher speed never takes longer, so feasibility is monotone in s.",
            (
                "Binary search s in [1, 10**7]; if hour <= n - 1 it is impossible (each of the first n - 1 trains "
                "takes at least one hour)."
            ),
        ],
        pattern="Binary search on the answer (rounding up per leg)",
        explain=(
            "Total time decreases as speed increases, so the minimum feasible speed is found by halving the speed "
            "range with an O(n) time check."
        ),
        cx="O(n log V) time",
        brute_cx="O(V * n) time - try speeds 1, 2, 3, ...",
        brute=r"""
# BRUTE FORCE: O(V * n) time - try speeds 1, 2, 3, ...
def min_speed_on_time(dist, hour):
    n = len(dist)

    if hour <= n - 1:
        return -1  # the first n - 1 trains take at least one hour each

    for speed in range(1, 100 * max(dist) + 2):
        time = sum(-(-d // speed) for d in dist[:-1]) + dist[-1] / speed
        if time <= hour:
            return speed

    return -1
""",
        solution=r"""
# OPTIMISED: O(n log V) time
# Idea: Binary search on the answer (rounding up per leg)
def min_speed_on_time(dist, hour):
    n = len(dist)

    if hour <= n - 1:
        return -1

    def fits(speed):
        time = (
            sum(-(-d // speed) for d in dist[:-1]) + dist[-1] / speed
        )  # ceil for all but the last leg
        return time <= hour

    lo, hi = 1, 10**7

    if not fits(hi):
        return -1

    while lo < hi:
        mid = (lo + hi) // 2
        if fits(mid):
            hi = mid
        else:
            lo = mid + 1

    return lo
""",
    ),
    # ---- Minimum Time to Complete Trips (LeetCode 2187) ----
    dict(
        title="Minimum Time to Complete Trips",
        diff="M",
        lc=2187,
        slug="minimum-time-to-complete-trips",
        prompt=(
            "Bus i takes time[i] minutes per trip and buses run independently, back to back. Return the minimum "
            "time for the buses to complete at least total_trips trips together."
        ),
        sig="def minimum_time(time: List[int], total_trips: int) -> int:",
        fn="minimum_time",
        tests=[
            (([1, 2, 3], 5), 3),
            (([2], 1), 2),
            (([5, 10, 10], 9), 25),
            (([1], 1), 1),
        ],
        hints=[
            "In t minutes bus i completes t // time[i] trips.",
            "Total trips by time t = sum(t // time[i]); it never decreases as t grows.",
            "Binary search the smallest t with at least total_trips; upper bound = min(time) * total_trips.",
        ],
        pattern="Binary search on the answer (time)",
        explain=(
            "The number of finished trips is monotone in time, so 'enough trips by time t' flips from false to true "
            "exactly once."
        ),
        cx="O(n log(min(time) * trips)) time",
        brute_cx="O(answer * n) time - test t = 1, 2, 3, ...",
        brute=r"""
# BRUTE FORCE: O(answer * n) time - test t = 1, 2, 3, ...
def minimum_time(time, total_trips):
    t = 1
    while sum(t // x for x in time) < total_trips:
        t += 1
    return t
""",
        solution=r"""
# OPTIMISED: O(n log(min(time) * trips)) time
# Idea: Binary search on the answer (time)
def minimum_time(time, total_trips):
    lo, hi = 1, min(time) * total_trips  # the fastest bus alone always suffices

    while lo < hi:
        mid = (lo + hi) // 2
        if sum(mid // x for x in time) >= total_trips:
            hi = mid
        else:
            lo = mid + 1

    return lo
""",
    ),
    # ---- Maximum Candies Allocated to K Children (LeetCode 2226) ----
    dict(
        title="Maximum Candies Allocated to K Children",
        diff="M",
        lc=2226,
        slug="maximum-candies-allocated-to-k-children",
        prompt=(
            "candies[i] is the size of pile i. You may split a pile into any number of smaller piles (but cannot "
            "merge). Give k children the same number of candies each, every child's candies coming from ONE pile. "
            "Return the maximum candies per child (0 if k children cannot all get at least 1)."
        ),
        sig="def maximum_candies(candies: List[int], k: int) -> int:",
        fn="maximum_candies",
        tests=[
            (([5, 8, 6], 3), 5),
            (([2, 5], 11), 0),
            (([4, 7, 5], 4), 3),
            (([10], 1), 10),
        ],
        hints=[
            "Guess a size s per child: a pile of c supplies c // s children.",
            "s is feasible if sum(c // s) >= k, and smaller sizes are always easier.",
            "Binary search the LARGEST feasible s in [1, max(candies)]; if even s = 1 fails the answer is 0.",
        ],
        pattern="Binary search on the answer (maximise a feasible value)",
        explain=(
            "Feasibility holds for small s and fails for large s, so the boundary is the answer; the check sums "
            "integer divisions."
        ),
        cx="O(n log max) time",
        brute_cx="O(max * n) time - try every size from the largest down",
        brute=r"""
# BRUTE FORCE: O(max * n) time - try every size from the largest down
def maximum_candies(candies, k):
    for size in range(max(candies), 0, -1):
        if sum(c // size for c in candies) >= k:
            return size
    return 0
""",
        solution=r"""
# OPTIMISED: O(n log max) time
# Idea: Binary search on the answer (maximise a feasible value)
def maximum_candies(candies, k):
    lo, hi = 0, max(candies)  # lo is always feasible (0 trivially)

    while lo < hi:
        mid = (lo + hi + 1) // 2  # upper middle, because we maximise
        if sum(c // mid for c in candies) >= k:
            lo = mid
        else:
            hi = mid - 1

    return lo
""",
    ),
    # ---- Successful Pairs of Spells and Potions (LeetCode 2300) ----
    dict(
        title="Successful Pairs of Spells and Potions",
        diff="M",
        lc=2300,
        slug="successful-pairs-of-spells-and-potions",
        prompt=(
            "A spell and a potion form a successful pair if spell * potion >= success. For each spell return the "
            "number of potions that make a successful pair with it."
        ),
        sig="def successful_pairs(spells: List[int], potions: List[int], success: int) -> List[int]:",
        fn="successful_pairs",
        tests=[
            (([5, 1, 3], [1, 2, 3, 4, 5], 7), [4, 0, 3]),
            (([3, 1, 2], [8, 5, 8], 16), [2, 0, 2]),
            (([1], [1], 1), [1]),
            (([2, 4], [1, 3], 5), [1, 1]),
        ],
        hints=[
            "For one spell s a potion p works iff p >= ceil(success / s).",
            "Sort potions once.",
            (
                "bisect_left(potions, ceil(success / s)) finds the first working potion; everything from there to "
                "the end counts."
            ),
        ],
        pattern="Sort once + binary search per query",
        explain=(
            "After sorting, working potions are a suffix, so the count is len - first_index; each spell costs one "
            "O(log m) lookup."
        ),
        cx="O((n + m) log m) time",
        brute_cx="O(n * m) time - test every spell/potion pair",
        brute=r"""
# BRUTE FORCE: O(n * m) time - test every spell/potion pair
def successful_pairs(spells, potions, success):
    return [sum(1 for p in potions if s * p >= success) for s in spells]
""",
        solution=r"""
# OPTIMISED: O((n + m) log m) time
# Idea: Sort once + binary search per query
def successful_pairs(spells, potions, success):
    potions = sorted(potions)
    m = len(potions)
    return [
        m - bisect.bisect_left(potions, -(-success // s)) for s in spells
    ]  # -(-a // b) is ceil(a / b)
""",
    ),
    # ---- Magnetic Force Between Two Balls (LeetCode 1552) ----
    dict(
        title="Magnetic Force Between Two Balls",
        diff="M",
        lc=1552,
        slug="magnetic-force-between-two-balls",
        prompt=(
            "Baskets sit at the given positions. Place m balls in different baskets so that the MINIMUM distance "
            "between any two balls is as large as possible. Return that maximum minimum distance."
        ),
        sig="def max_distance(position: List[int], m: int) -> int:",
        fn="max_distance",
        tests=[
            (([1, 2, 3, 4, 7], 3), 3),
            (([5, 4, 3, 2, 1, 1000000000], 2), 999999999),
            (([1, 2], 2), 1),
            (([1, 2, 3], 2), 2),
        ],
        hints=[
            "Guess a minimum distance d. Can you place m balls at least d apart?",
            (
                "Check greedily: sort the positions, put a ball at the first basket, then at every basket at least "
                "d past the last ball."
            ),
            "Larger d is harder, so binary search the largest feasible d between 1 and (max - min).",
        ],
        pattern="Binary search on the answer + greedy placement check",
        explain="Greedy placement maximises the number of balls for a given d, and feasibility is monotone in d.",
        cx="O(n log n + n log range) time",
        brute_cx="O(range * n) time - try every distance from the largest down",
        brute=r"""
# BRUTE FORCE: O(range * n) time - try every distance from the largest down
def max_distance(position, m):
    position = sorted(position)

    def can_place(d):
        placed, last = 1, position[0]
        for p in position[1:]:
            if p - last >= d:
                placed += 1
                last = p
        return placed >= m

    for d in range((position[-1] - position[0]) // (m - 1), 0, -1):
        if can_place(d):
            return d
""",
        solution=r"""
# OPTIMISED: O(n log n + n log range) time
# Idea: Binary search on the answer + greedy placement check
def max_distance(position, m):
    position = sorted(position)

    def can_place(d):
        placed, last = 1, position[0]
        for p in position[1:]:
            if p - last >= d:
                placed += 1
                last = p
        return placed >= m

    lo, hi = 1, (position[-1] - position[0]) // (m - 1)

    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can_place(mid):
            lo = mid
        else:
            hi = mid - 1

    return lo
""",
    ),
    # ---- Find K-th Smallest Pair Distance (LeetCode 719) ----
    dict(
        title="Find K-th Smallest Pair Distance",
        diff="H",
        lc=719,
        slug="find-k-th-smallest-pair-distance",
        prompt=(
            "The distance of a pair (i < j) is |nums[i] - nums[j]|. Return the k-th smallest distance among all "
            "pairs (k is 1-indexed)."
        ),
        sig="def smallest_distance_pair(nums: List[int], k: int) -> int:",
        fn="smallest_distance_pair",
        tests=[
            (([1, 3, 1], 1), 0),
            (([1, 1, 1], 2), 0),
            (([1, 6, 1], 3), 5),
            (([1, 2, 3], 2), 1),
        ],
        hints=[
            "Materialising all n(n-1)/2 distances and sorting works but is too big for large n.",
            "Binary search the DISTANCE d. How many pairs have distance <= d?",
            (
                "Sort nums; count pairs with a two-pointer sweep (for each right, move left until nums[right] - "
                "nums[left] <= d). Find the smallest d with count >= k."
            ),
        ],
        pattern="Binary search on the answer + two-pointer counting",
        explain=(
            "The count of pairs with distance <= d is non-decreasing in d, and a sorted array lets us count them in "
            "O(n) per guess."
        ),
        cx="O(n log n + n log range) time",
        brute_cx="O(n^2 log n) time - generate and sort every pair distance",
        brute=r"""
# BRUTE FORCE: O(n^2 log n) time - generate and sort every pair distance
def smallest_distance_pair(nums, k):
    distances = sorted(abs(a - b) for a, b in itertools.combinations(nums, 2))
    return distances[k - 1]
""",
        solution=r"""
# OPTIMISED: O(n log n + n log range) time
# Idea: Binary search on the answer + two-pointer counting
def smallest_distance_pair(nums, k):
    nums = sorted(nums)

    def pairs_within(d):
        count, left = 0, 0
        for right in range(len(nums)):
            while nums[right] - nums[left] > d:
                left += 1
            count += right - left  # pairs (left..right-1, right)
        return count

    lo, hi = 0, nums[-1] - nums[0]

    while lo < hi:
        mid = (lo + hi) // 2
        if pairs_within(mid) >= k:
            hi = mid
        else:
            lo = mid + 1

    return lo
""",
    ),
    # ---- Kth Smallest Number in Multiplication Table (LeetCode 668) ----
    dict(
        title="Kth Smallest Number in Multiplication Table",
        diff="H",
        lc=668,
        slug="kth-smallest-number-in-multiplication-table",
        prompt=(
            "In the m x n multiplication table cell (i, j) holds i * j (1-indexed). Return the k-th smallest value "
            "in the table (counting duplicates)."
        ),
        sig="def find_kth_number(m: int, n: int, k: int) -> int:",
        fn="find_kth_number",
        tests=[
            ((3, 3, 5), 3),
            ((2, 3, 6), 6),
            ((1, 1, 1), 1),
            ((3, 3, 1), 1),
            ((3, 3, 9), 9),
        ],
        hints=[
            "Building and sorting the whole table costs O(mn log(mn)).",
            "Binary search the VALUE x. How many cells hold a value <= x?",
            "Row i contributes min(x // i, n) cells. Find the smallest x whose total is >= k.",
        ],
        pattern="Binary search on the value with a counting function",
        explain=(
            "Counting entries <= x takes O(m) using row-wise division, and the count is monotone in x, so the k-th "
            "smallest is the first x reaching k."
        ),
        cx="O(m log(mn)) time",
        brute_cx="O(mn log(mn)) time - build and sort the table",
        brute=r"""
# BRUTE FORCE: O(mn log(mn)) time - build and sort the table
def find_kth_number(m, n, k):
    table = sorted(i * j for i in range(1, m + 1) for j in range(1, n + 1))
    return table[k - 1]
""",
        solution=r"""
# OPTIMISED: O(m log(mn)) time
# Idea: Binary search on the value with a counting function
def find_kth_number(m, n, k):
    def count_at_most(x):
        return sum(min(x // i, n) for i in range(1, m + 1))

    lo, hi = 1, m * n

    while lo < hi:
        mid = (lo + hi) // 2
        if count_at_most(mid) >= k:
            hi = mid
        else:
            lo = mid + 1

    return lo
""",
    ),
    # ---- Minimum Time to Repair Cars (LeetCode 2594) ----
    dict(
        title="Minimum Time to Repair Cars",
        diff="M",
        lc=2594,
        slug="minimum-time-to-repair-cars",
        prompt=(
            "A mechanic with rank r repairs n cars in r * n * n minutes. All mechanics work at the same time. "
            "Return the minimum time to repair `cars` cars in total."
        ),
        sig="def repair_cars(ranks: List[int], cars: int) -> int:",
        fn="repair_cars",
        tests=[
            (([4, 2, 3, 1], 10), 16),
            (([5, 1, 8], 6), 16),
            (([1], 1), 1),
            (([2], 4), 32),
        ],
        hints=[
            "In t minutes a mechanic of rank r can repair floor(sqrt(t / r)) cars.",
            "The total repaired grows with t.",
            "Binary search the smallest t whose total is >= cars; an upper bound is min(ranks) * cars * cars.",
        ],
        pattern="Binary search on the answer (time)",
        explain=(
            "The formula inverts the quadratic cost: more time never repairs fewer cars, so the minimum time sits "
            "at the boundary of a monotone predicate."
        ),
        cx="O(n log(min_rank * cars^2)) time",
        brute_cx="O(answer * n) time - test t = 1, 2, 3, ...",
        brute=r"""
# BRUTE FORCE: O(answer * n) time - test t = 1, 2, 3, ...
def repair_cars(ranks, cars):
    t = 1
    while sum(math.isqrt(t // r) for r in ranks) < cars:
        t += 1
    return t
""",
        solution=r"""
# OPTIMISED: O(n log(min_rank * cars^2)) time
# Idea: Binary search on the answer (time)
def repair_cars(ranks, cars):
    lo, hi = 1, min(ranks) * cars * cars  # the best mechanic alone is enough

    while lo < hi:
        mid = (lo + hi) // 2
        if sum(math.isqrt(mid // r) for r in ranks) >= cars:
            hi = mid
        else:
            lo = mid + 1

    return lo
""",
    ),
]
