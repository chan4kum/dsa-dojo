"""more Binary Search problems (batch 6) - part of the problem bank for the "binary_search" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
Most of these are "binary search on the ANSWER": the answer is a number, and a yes/no check tells whether a guess
is big enough, so the answers form a pattern no, no, ..., yes, yes that binary search can cut in half.
"""

PROBLEMS = [
    # ---- H-Index II (LeetCode 275) ----
    dict(
        title="H-Index II",
        diff="M",
        lc=275,
        slug="h-index-ii",
        prompt=(
            "citations[i] is the number of citations of the i-th paper, and the list is sorted in ASCENDING order. "
            "The h-index is the largest h such that at least h papers have at least h citations each. Return it in "
            "O(log n) time."
        ),
        sig="def h_index(citations: List[int]) -> int:",
        fn="h_index",
        tests=[
            (([0, 1, 3, 5, 6],), 3),
            (([1, 2, 100],), 2),
            (([0],), 0),
            (([5, 5, 5, 5],), 4),
        ],
        hints=[
            (
                "If the h best papers all have at least h citations, h is achievable - and the h best papers are "
                "the LAST h in the sorted list."
            ),
            "So h is valid exactly when citations[n - h] >= h. Validity is monotone: a smaller h is always easier.",
            "Binary search the smallest index i with citations[i] >= n - i; the answer is n - i.",
        ],
        pattern="Binary search on a monotone condition over the sorted array",
        explain=(
            "Position i in the sorted list has n - i papers at or above it. The condition citations[i] >= n - i "
            "turns from false to true exactly once as i grows (citations rise while n - i falls), so a binary "
            "search finds the first true index, and n - i is the biggest valid h. The brute force tries every h "
            "from large to small."
        ),
        cx="O(log n) time, O(1) space",
        brute_cx="O(n) time - try each h from n down to 1",
        brute=r"""
# BRUTE FORCE: O(n) time - try each h from n down to 1
def h_index(citations):
    n = len(citations)
    for h in range(n, 0, -1):
        if citations[n - h] >= h:
            return h
    return 0
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Binary search on a monotone condition over the sorted array
def h_index(citations):
    n = len(citations)
    lo, hi = 0, n

    while lo < hi:
        mid = (lo + hi) // 2
        if citations[mid] >= n - mid:
            hi = mid
        else:
            lo = mid + 1

    return n - lo
""",
    ),
    # ---- Preimage Size of Factorial Zeroes Function (LeetCode 793) ----
    dict(
        title="Preimage Size of Factorial Zeroes Function",
        diff="H",
        lc=793,
        slug="preimage-size-of-factorial-zeroes-function",
        prompt=(
            "Let f(x) be the number of trailing zeroes of x! (so f(3) = 0 and f(11) = 2). Given k, return how many "
            "non-negative integers x satisfy f(x) = k."
        ),
        sig="def preimage_size_fzf(k: int) -> int:",
        fn="preimage_size_fzf",
        tests=[
            ((0,), 5),
            ((5,), 0),
            ((3,), 5),
            ((1,), 5),
        ],
        hints=[
            "Trailing zeroes of x! = x//5 + x//25 + x//125 + ... (count the factors of 5).",
            (
                "f never decreases as x grows, so the x with f(x) = k form one contiguous block - and f jumps only "
                "at multiples of 5, so the block has size 5 or 0."
            ),
            (
                "Binary search the first x with f(x) >= k and the first x with f(x) >= k + 1; their difference is "
                "the answer."
            ),
        ],
        pattern="Binary search on a monotone function (lower bound twice)",
        explain=(
            "f is non-decreasing, so 'first x with f(x) >= t' is a classic lower bound. The count of x with f(x) = "
            "k is lowerBound(k + 1) - lowerBound(k). The upper search limit 5 * (t + 1) always works because f(5m) "
            ">= m. The brute force walks x upwards, counting hits until f exceeds k."
        ),
        cx="O(log^2 k) time, O(1) space",
        brute_cx="O(k log k) time - walk x upwards until f(x) exceeds k",
        brute=r"""
# BRUTE FORCE: O(k log k) time - walk x upwards until f(x) exceeds k
def preimage_size_fzf(k):
    def zeros(x):
        count = 0
        while x:
            x //= 5
            count += x
        return count

    count = 0
    x = 0

    while zeros(x) <= k:
        if zeros(x) == k:
            count += 1
        x += 1

    return count
""",
        solution=r"""
# OPTIMISED: O(log^2 k) time, O(1) space
# Idea: Binary search on a monotone function (lower bound twice)
def preimage_size_fzf(k):
    def zeros(x):
        count = 0
        while x:
            x //= 5
            count += x
        return count

    def first_at_least(target):
        lo, hi = 0, 5 * target + 5

        while lo < hi:
            mid = (lo + hi) // 2
            if zeros(mid) >= target:
                hi = mid
            else:
                lo = mid + 1

        return lo

    return first_at_least(k + 1) - first_at_least(k)
""",
    ),
    # ---- Nth Magical Number (LeetCode 878) ----
    dict(
        title="Nth Magical Number",
        diff="H",
        lc=878,
        slug="nth-magical-number",
        prompt=(
            "A positive integer is magical if it is divisible by a or by b. Return the n-th magical number modulo "
            "10^9 + 7."
        ),
        sig="def nth_magical_number(n: int, a: int, b: int) -> int:",
        fn="nth_magical_number",
        tests=[
            ((1, 2, 3), 2),
            ((4, 2, 3), 6),
            ((5, 2, 4), 10),
            ((3, 6, 4), 8),
        ],
        hints=[
            "Count the magical numbers up to x with inclusion-exclusion: x//a + x//b - x//lcm(a, b).",
            "That count only grows with x, so 'is count(x) >= n?' goes no, no, ..., yes, yes.",
            "Binary search the smallest x with count(x) >= n; take it modulo 10^9 + 7 at the end.",
        ],
        pattern="Binary search on the answer with an inclusion-exclusion counter",
        explain=(
            "Numbers divisible by a OR b are counted by adding the two multiples and subtracting the ones counted "
            "twice (multiples of the lcm). The counter is monotone in x, so the n-th magical number is the first x "
            "where the counter reaches n. The answer is at most n * min(a, b). The brute force counts upwards one "
            "integer at a time."
        ),
        cx="O(log(n * min(a, b))) time, O(1) space",
        brute_cx="O(n * min(a, b)) time - test every integer in turn",
        brute=r"""
# BRUTE FORCE: O(n * min(a, b)) time - test every integer in turn
def nth_magical_number(n, a, b):
    found = 0
    x = 0
    while found < n:
        x += 1
        if x % a == 0 or x % b == 0:
            found += 1
    return x % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(log(n * min(a, b))) time, O(1) space
# Idea: Binary search on the answer with an inclusion-exclusion counter
def nth_magical_number(n, a, b):
    lcm = a * b // math.gcd(a, b)
    lo, hi = 1, n * min(a, b)

    while lo < hi:
        mid = (lo + hi) // 2
        if mid // a + mid // b - mid // lcm >= n:
            hi = mid
        else:
            lo = mid + 1

    return lo % (10**9 + 7)
""",
    ),
    # ---- Ugly Number III (LeetCode 1201) ----
    dict(
        title="Ugly Number III",
        diff="M",
        lc=1201,
        slug="ugly-number-iii",
        prompt="A positive integer is ugly if it is divisible by a, b or c. Return the n-th ugly number.",
        sig="def nth_ugly_number(n: int, a: int, b: int, c: int) -> int:",
        fn="nth_ugly_number",
        tests=[
            ((3, 2, 3, 5), 4),
            ((4, 2, 3, 4), 6),
            ((5, 2, 11, 13), 10),
            ((1, 7, 7, 7), 7),
        ],
        hints=[
            "How many ugly numbers are <= x? Add the multiples of a, b and c.",
            (
                "That double-counts numbers divisible by two of them and triple-counts the ones divisible by all "
                "three: use inclusion-exclusion with pairwise lcms and the lcm of all three."
            ),
            "The count grows with x, so binary search the smallest x whose count is at least n.",
        ],
        pattern="Binary search on the answer with a three-set inclusion-exclusion counter",
        explain=(
            "count(x) = x/a + x/b + x/c - x/lcm(a,b) - x/lcm(a,c) - x/lcm(b,c) + x/lcm(a,b,c) is the number of "
            "integers up to x divisible by at least one of the three. It is monotone in x, so the n-th ugly number "
            "is the first x where it reaches n. The upper bound n * min(a, b, c) is always enough. The brute force "
            "tests every integer."
        ),
        cx="O(log(n * min(a, b, c))) time, O(1) space",
        brute_cx="O(n * min(a, b, c)) time - test every integer in turn",
        brute=r"""
# BRUTE FORCE: O(n * min(a, b, c)) time - test every integer in turn
def nth_ugly_number(n, a, b, c):
    found = 0
    x = 0
    while found < n:
        x += 1
        if x % a == 0 or x % b == 0 or x % c == 0:
            found += 1
    return x
""",
        solution=r"""
# OPTIMISED: O(log(n * min(a, b, c))) time, O(1) space
# Idea: Binary search on the answer with a three-set inclusion-exclusion counter
def nth_ugly_number(n, a, b, c):
    def lcm(x, y):
        return x * y // math.gcd(x, y)

    ab, ac, bc = lcm(a, b), lcm(a, c), lcm(b, c)
    abc = lcm(ab, c)

    def count(x):
        return x // a + x // b + x // c - x // ab - x // ac - x // bc + x // abc

    lo, hi = 1, n * min(a, b, c)

    while lo < hi:
        mid = (lo + hi) // 2
        if count(mid) >= n:
            hi = mid
        else:
            lo = mid + 1

    return lo
""",
    ),
    # ---- Sum of Mutated Array Closest to Target (LeetCode 1300) ----
    dict(
        title="Sum of Mutated Array Closest to Target",
        diff="M",
        lc=1300,
        slug="sum-of-mutated-array-closest-to-target",
        prompt=(
            "Choose an integer value v and replace every element of arr that is larger than v by v. Return the v "
            "for which the sum of the changed array is closest to target. If two values are equally close, return "
            "the smaller v."
        ),
        sig="def find_best_value(arr: List[int], target: int) -> int:",
        fn="find_best_value",
        tests=[
            (([4, 9, 3], 10), 3),
            (([2, 3, 5], 10), 5),
            (([60864, 25176, 27249, 21296, 20204], 56803), 11361),
            (([1, 1], 100), 1),
        ],
        hints=[
            "Define total(v) = sum of min(x, v) over the array. It never decreases as v grows.",
            "So binary search the smallest v in [0, max(arr)] with total(v) >= target.",
            "The best answer is either that v or v - 1: compare their distances to target and prefer v - 1 on a tie.",
        ],
        pattern="Binary search on a monotone sum, then compare the two neighbours",
        explain=(
            "total(v) is non-decreasing, so there is a crossing point where it first reaches target. The closest "
            "total is either just before or at that crossing, so only two candidates remain; the tie rule picks the "
            "smaller. Raising v above max(arr) changes nothing, so the search range stops there. The brute force "
            "simply tries every v."
        ),
        cx="O(n log max) time, O(1) space",
        brute_cx="O(n * max) time - try every value from 0 to max(arr)",
        brute=r"""
# BRUTE FORCE: O(n * max) time - try every value from 0 to max(arr)
def find_best_value(arr, target):
    best_value, best_gap = 0, None
    for v in range(max(arr) + 1):
        gap = abs(sum(min(x, v) for x in arr) - target)
        if best_gap is None or gap < best_gap:
            best_value, best_gap = v, gap
    return best_value
""",
        solution=r"""
# OPTIMISED: O(n log max) time, O(1) space
# Idea: Binary search on a monotone sum, then compare the two neighbours
def find_best_value(arr, target):
    def total(v):
        return sum(min(x, v) for x in arr)

    lo, hi = 0, max(arr)

    while lo < hi:
        mid = (lo + hi) // 2
        if total(mid) >= target:
            hi = mid
        else:
            lo = mid + 1

    if lo > 0 and abs(total(lo - 1) - target) <= abs(total(lo) - target):
        return lo - 1

    return lo
""",
    ),
    # ---- Special Array With X Elements Greater Than or Equal X (LeetCode 1608) ----
    dict(
        title="Special Array With X Elements Greater Than or Equal X",
        diff="E",
        lc=1608,
        slug="special-array-with-x-elements-greater-than-or-equal-x",
        prompt=(
            "nums is special if there is a number x such that EXACTLY x elements of nums are greater than or equal "
            "to x (x need not be in nums). Return x if nums is special, otherwise -1. If nums is special, x is "
            "unique."
        ),
        sig="def special_array(nums: List[int]) -> int:",
        fn="special_array",
        tests=[
            (([3, 5],), 2),
            (([0, 0],), -1),
            (([0, 4, 3, 0, 4],), 3),
            (([3, 6, 7, 7, 0],), -1),
        ],
        hints=[
            "x can only be between 0 and n (there are n elements).",
            (
                "Let count(x) = how many elements are >= x. It falls as x rises, so 'count(x) <= x' flips from "
                "false to true once."
            ),
            "Sort once, binary search the smallest x with count(x) <= x, and check whether count(x) equals x exactly.",
        ],
        pattern="Sort + binary search on the answer x",
        explain=(
            "count(x) is non-increasing while x increases, so the predicate count(x) <= x is false-then-true. At "
            "the crossing point either count(x) == x (special) or the count jumps over x and no value works. count "
            "is computed with bisect on the sorted array. The brute force counts for every x."
        ),
        cx="O(n log n) time, O(1) extra space",
        brute_cx="O(n^2) time - count the large elements for each x in 0..n",
        brute=r"""
# BRUTE FORCE: O(n^2) time - count the large elements for each x in 0..n
def special_array(nums):
    for x in range(len(nums) + 1):
        if sum(1 for v in nums if v >= x) == x:
            return x
    return -1
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space
# Idea: Sort + binary search on the answer x
def special_array(nums):
    ordered = sorted(nums)
    n = len(ordered)

    def count(x):
        return n - bisect.bisect_left(ordered, x)

    lo, hi = 0, n

    while lo < hi:
        mid = (lo + hi) // 2
        if count(mid) <= mid:
            hi = mid
        else:
            lo = mid + 1

    return lo if count(lo) == lo else -1
""",
    ),
    # ---- Minimize Maximum of Array (LeetCode 2439) ----
    dict(
        title="Minimize Maximum of Array",
        diff="M",
        lc=2439,
        slug="minimize-maximum-of-array",
        prompt=(
            "In one operation pick an index i > 0 with nums[i] > 0, decrease nums[i] by 1 and increase nums[i - 1] "
            "by 1 (a unit moves LEFT). Apply any number of operations and return the smallest possible maximum of "
            "the array."
        ),
        sig="def minimize_array_value(nums: List[int]) -> int:",
        fn="minimize_array_value",
        tests=[
            (([3, 7, 1, 6],), 5),
            (([10, 1],), 10),
            (([1, 5],), 3),
            (([4],), 4),
        ],
        hints=[
            "Units only move left, so the first i + 1 elements together keep at least their original sum.",
            "That forces the maximum to be at least ceil(prefix_sum / (i + 1)) for every prefix.",
            "That bound is achievable: the answer is the maximum, over all prefixes, of ceil(prefix_sum / length).",
        ],
        pattern="Prefix average lower bound (greedy / binary search on the answer)",
        explain=(
            "Elements can only give units to the left, so a prefix can never lose sum, and the best it can do is "
            "spread its sum evenly: the max is at least the ceiling of its average. Taking the largest of those "
            "bounds over all prefixes is also reachable by pushing the extra units leftwards, so it is the exact "
            "answer. The brute force tries each cap m and checks it by pushing excess to the left."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n * max) time - test every cap m by pushing excess leftwards",
        brute=r"""
# BRUTE FORCE: O(n * max) time - test every cap m by pushing excess leftwards
def minimize_array_value(nums):
    n = len(nums)

    for cap in range(max(nums) + 1):
        carry = 0
        for i in range(n - 1, 0, -1):
            value = nums[i] + carry
            carry = value - cap if value > cap else 0
        if nums[0] + carry <= cap:
            return cap
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Prefix average lower bound (greedy / binary search on the answer)
def minimize_array_value(nums):
    total = 0
    best = 0
    for i, x in enumerate(nums):
        total += x
        best = max(best, (total + i) // (i + 1))
    return best
""",
    ),
    # ---- Maximum Tastiness of Candy Basket (LeetCode 2517) ----
    dict(
        title="Maximum Tastiness of Candy Basket",
        diff="M",
        lc=2517,
        slug="maximum-tastiness-of-candy-basket",
        prompt=(
            "price[i] is the price of candy i. A basket of k DISTINCT candies has tastiness equal to the smallest "
            "absolute difference between the prices of any two candies in it. Return the maximum tastiness of a "
            "basket of k candies."
        ),
        sig="def maximum_tastiness(price: List[int], k: int) -> int:",
        fn="maximum_tastiness",
        tests=[
            (([13, 5, 1, 8, 21, 2], 3), 8),
            (([1, 3, 1], 2), 2),
            (([7, 7, 7, 7], 2), 0),
            (([1, 2, 3, 4], 4), 1),
        ],
        hints=[
            "Sort the prices. Choosing prices with all gaps at least d is easier when d is smaller.",
            (
                "For a fixed gap d, greedily take the first price, then each next price that is at least d above "
                "the last one taken; count how many you get."
            ),
            "If you can take k, d is feasible. Binary search the largest feasible d between 0 and max - min.",
        ],
        pattern="Binary search on the answer + greedy feasibility check",
        explain=(
            "Feasibility is monotone: any basket with minimum gap >= d also has minimum gap >= d - 1. For a given "
            "d, taking the earliest possible candy each time leaves the most room for the rest, so the greedy count "
            "is the maximum basket size. Binary search over d finds the largest feasible one. The brute force "
            "examines every basket of k candies."
        ),
        cx="O(n log n + n log(max price)) time, O(1) extra space",
        brute_cx="exponential - try every set of k sorted prices",
        brute=r"""
# BRUTE FORCE: exponential - try every set of k sorted prices
def maximum_tastiness(price, k):
    ordered = sorted(price)
    best = 0
    for chosen in itertools.combinations(ordered, k):
        best = max(best, min(b - a for a, b in zip(chosen, chosen[1:])))
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n + n log(max price)) time, O(1) extra space
# Idea: Binary search on the answer + greedy feasibility check
def maximum_tastiness(price, k):
    ordered = sorted(price)

    def can(gap):
        taken, last = 1, ordered[0]
        for p in ordered[1:]:
            if p - last >= gap:
                taken += 1
                last = p
        return taken >= k

    lo, hi = 0, ordered[-1] - ordered[0]

    while lo < hi:
        mid = (lo + hi + 1) // 2
        if can(mid):
            lo = mid
        else:
            hi = mid - 1

    return lo
""",
    ),
    # ---- House Robber IV (LeetCode 2560) ----
    dict(
        title="House Robber IV",
        diff="M",
        lc=2560,
        slug="house-robber-iv",
        prompt=(
            "nums[i] is the money in house i. A robber must rob at least k houses and never two ADJACENT houses. "
            "His capability is the largest amount he steals from any single house. Return the minimum capability "
            "that allows robbing at least k houses."
        ),
        sig="def min_capability(nums: List[int], k: int) -> int:",
        fn="min_capability",
        tests=[
            (([2, 3, 5, 9], 2), 5),
            (([2, 7, 9, 3, 1], 2), 2),
            (([1], 1), 1),
            (([5, 5, 5, 5], 2), 5),
        ],
        hints=[
            "Fix a capability c: the robber may only rob houses with nums[i] <= c.",
            (
                "Greedy count: scan left to right, rob every allowed house that does not touch the previous robbery "
                "(skip the next one after robbing)."
            ),
            "If that count reaches k, c works. A bigger c never hurts, so binary search the smallest working c.",
        ],
        pattern="Binary search on the answer + greedy non-adjacent count",
        explain=(
            "With a cap c, grabbing the leftmost allowed house each time never reduces how many non-adjacent houses "
            "can be robbed in total, so the greedy count is the true maximum. The count grows with c, so the "
            "smallest c reaching k is found by binary search over the values in nums. The brute force tries every "
            "set of k non-adjacent houses and takes the best maximum."
        ),
        cx="O(n log(max nums)) time, O(1) space",
        brute_cx="exponential - try every set of k non-adjacent houses",
        brute=r"""
# BRUTE FORCE: exponential - try every set of k non-adjacent houses
def min_capability(nums, k):
    best = None

    for chosen in itertools.combinations(range(len(nums)), k):
        if any(b - a == 1 for a, b in zip(chosen, chosen[1:])):
            continue
        cap = max(nums[i] for i in chosen)
        if best is None or cap < best:
            best = cap

    return best
""",
        solution=r"""
# OPTIMISED: O(n log(max nums)) time, O(1) space
# Idea: Binary search on the answer + greedy non-adjacent count
def min_capability(nums, k):
    def can(cap):
        robbed, i = 0, 0

        while i < len(nums):
            if nums[i] <= cap:
                robbed += 1
                i += 2
            else:
                i += 1

        return robbed >= k

    lo, hi = min(nums), max(nums)

    while lo < hi:
        mid = (lo + hi) // 2
        if can(mid):
            hi = mid
        else:
            lo = mid + 1

    return lo
""",
    ),
]
