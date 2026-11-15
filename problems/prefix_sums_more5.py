"""extra batch of Prefix Sums problems - the problem bank for the "prefix_sums" topic (batch 5).

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
    # ---- Continuous Subarray Sum (LeetCode 523) ----
    dict(
        title="Continuous Subarray Sum",
        diff="M",
        lc=523,
        slug="continuous-subarray-sum",
        prompt=(
            "Return True if nums has a contiguous subarray of length at least 2 whose sum is a multiple of k (0 "
            "counts as a multiple), else False. k >= 1."
        ),
        sig="def check_subarray_sum(nums: List[int], k: int) -> bool:",
        fn="check_subarray_sum",
        tests=[
            (([23, 2, 4, 6, 7], 6), True),
            (([23, 2, 6, 4, 7], 6), True),
            (([23, 2, 6, 4, 7], 13), False),
            (([5, 0, 0, 0], 3), True),
            (([1, 0], 2), False),
            (([0, 0], 1), True),
        ],
        hints=[
            (
                "Subarray sum = prefix[j] - prefix[i]. It is a multiple of k exactly when the two prefixes have the "
                "same remainder mod k."
            ),
            (
                "Store the first index at which each remainder appeared (remainder 0 appears 'before' index 0, at "
                "position -1)."
            ),
            (
                "If the current remainder was seen at index p and i - p >= 2, the subarray between them has length "
                ">= 2: return True. Never overwrite the first index."
            ),
        ],
        pattern="Prefix sums mod k with a first-seen index map",
        explain=(
            "Two prefix sums with equal remainder mod k differ by a multiple of k, and the elements between them "
            "form the subarray. Keeping the EARLIEST index for each remainder makes the subarray as long as "
            "possible, which is what the length >= 2 rule needs. Seeding the map with {0: -1} handles subarrays "
            "that start at index 0."
        ),
        cx="O(n) time, O(min(n, k)) space",
        brute_cx="O(n^2) time - test every subarray of length >= 2",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every subarray of length >= 2
def check_subarray_sum(nums, k):
    for i in range(len(nums)):
        total = nums[i]
        for j in range(i + 1, len(nums)):
            total += nums[j]
            if total % k == 0:
                return True
    return False
""",
        solution=r"""
# OPTIMISED: O(n) time, O(min(n, k)) space
# Idea: Prefix sums mod k with a first-seen index map
def check_subarray_sum(nums, k):
    first_seen = {0: -1}
    total = 0
    for i, x in enumerate(nums):
        total = (total + x) % k
        if total in first_seen:
            if i - first_seen[total] >= 2:
                return True
        else:
            first_seen[total] = i
    return False
""",
    ),
    # ---- Make Sum Divisible by P (LeetCode 1590) ----
    dict(
        title="Make Sum Divisible by P",
        diff="M",
        lc=1590,
        slug="make-sum-divisible-by-p",
        prompt=(
            "Remove the shortest contiguous subarray (possibly empty, but not the whole array) so that the sum of "
            "the remaining elements is divisible by p. Return its length, or -1 if impossible."
        ),
        sig="def min_subarray(nums: List[int], p: int) -> int:",
        fn="min_subarray",
        tests=[
            (([3, 1, 4, 2], 6), 1),
            (([6, 3, 5, 2], 9), 2),
            (([1, 2, 3], 3), 0),
            (([1, 2, 3], 7), -1),
            (([1000000000, 1000000000, 1000000000], 3), 0),
        ],
        hints=[
            "Let r = total % p. If r == 0 the answer is 0. Otherwise you must remove a subarray whose sum % p == r.",
            "A subarray sum is prefix[j] - prefix[i], so you need prefix[i] % p == (prefix[j] - r) % p.",
            (
                "Scan j left to right with a map remainder -> LAST index seen; the best i for each j is the most "
                "recent one. Reject a candidate of length n (the whole array)."
            ),
        ],
        pattern="Prefix remainders with a last-seen index map",
        explain=(
            "Removing a subarray with sum congruent to r leaves a sum divisible by p. For each end position the "
            "shortest such subarray starts right after the latest earlier prefix with remainder (cur - r) mod p, so "
            "storing the most recent index per remainder gives the minimum in one pass."
        ),
        cx="O(n) time, O(min(n, p)) space",
        brute_cx="O(n^2) time - test every proper subarray",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every proper subarray
def min_subarray(nums, p):
    n, total = len(nums), sum(nums)
    best = None
    for i in range(n):
        for j in range(i, n):
            length = j - i + 1
            if length == n:
                continue
            if (total - sum(nums[i : j + 1])) % p == 0:
                best = length if best is None else min(best, length)
    if total % p == 0:
        return 0
    return -1 if best is None else best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(min(n, p)) space
# Idea: Prefix remainders with a last-seen index map
def min_subarray(nums, p):
    need = sum(nums) % p
    if need == 0:
        return 0
    last = {0: -1}
    cur = 0
    best = len(nums)
    for i, x in enumerate(nums):
        cur = (cur + x) % p
        want = (cur - need) % p
        if want in last:
            best = min(best, i - last[want])
        last[cur] = i
    return -1 if best == len(nums) else best
""",
    ),
    # ---- Count Triplets That Can Form Two Arrays of Equal XOR (LeetCode 1442) ----
    dict(
        title="Count Triplets That Can Form Two Arrays of Equal XOR",
        diff="M",
        lc=1442,
        slug="count-triplets-that-can-form-two-arrays-of-equal-xor",
        prompt="Count triplets (i, j, k) with 0 <= i < j <= k < n such that xor(arr[i..j-1]) == xor(arr[j..k]).",
        sig="def count_triplets(arr: List[int]) -> int:",
        fn="count_triplets",
        tests=[
            (([2, 3, 1, 6, 7],), 4),
            (([1, 1, 1, 1, 1],), 10),
            (([2, 3],), 0),
            (([1, 3, 5, 7, 9],), 3),
            (([7, 11, 12, 9, 5, 2, 7, 17, 22],), 8),
        ],
        hints=[
            "a == b means a XOR b == 0, so the condition says xor(arr[i..k]) == 0.",
            "Then ANY split point j between i+1 and k works: each valid pair (i, k) contributes k - i triplets.",
            (
                "With prefix xor P, xor(arr[i..k]) == 0 means P[i] == P[k+1]. Count pairs of equal prefix values "
                "weighted by their distance - a hash map of (count, sum of indices) does it in O(n)."
            ),
        ],
        pattern="Prefix XOR: equal prefixes mean a zero-XOR subarray",
        explain=(
            "xor(arr[i..j-1]) == xor(arr[j..k]) is equivalent to xor(arr[i..k]) == 0, independent of j. Using "
            "prefix xors P[0..n], that happens iff P[i] == P[k+1], and the number of valid j is k - i = (k+1) - i - "
            "1. For each prefix index b, the equal earlier prefixes a contribute (b - a - 1) each; keep their count "
            "and the sum of their indices per value to add count*(b-1) - sum_a in O(1)."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^3) time - test every triplet by xoring both halves",
        brute=r"""
# BRUTE FORCE: O(n^3) time - test every triplet by xoring both halves
def count_triplets(arr):
    n = len(arr)
    total = 0
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j, n):
                a = 0
                for x in arr[i:j]:
                    a ^= x
                b = 0
                for x in arr[j : k + 1]:
                    b ^= x
                if a == b:
                    total += 1
    return total
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Prefix XOR: equal prefixes mean a zero-XOR subarray
def count_triplets(arr):
    seen = defaultdict(lambda: [0, 0])
    seen[0] = [1, 0]
    prefix = 0
    total = 0
    for b, x in enumerate(arr, 1):
        prefix ^= x
        count, index_sum = seen[prefix]
        total += count * (b - 1) - index_sum
        seen[prefix] = [count + 1, index_sum + b]
    return total
""",
    ),
    # ---- XOR Queries of a Subarray (LeetCode 1310) ----
    dict(
        title="XOR Queries of a Subarray",
        diff="M",
        lc=1310,
        slug="xor-queries-of-a-subarray",
        prompt="For each query [left, right] return the XOR of arr[left..right] (inclusive).",
        sig="def xor_queries(arr: List[int], queries: List[List[int]]) -> List[int]:",
        fn="xor_queries",
        tests=[
            (([1, 3, 4, 8], [[0, 1], [1, 2], [0, 3], [3, 3]]), [2, 7, 14, 8]),
            (([4, 8, 2, 10], [[2, 3], [1, 3], [0, 0], [0, 3]]), [8, 0, 4, 4]),
            (([5], [[0, 0]]), [5]),
        ],
        hints=[
            "XOR is its own inverse: a ^ a == 0.",
            "Define P[i] = arr[0] ^ ... ^ arr[i-1]. Then arr[l..r] = P[r+1] ^ P[l] because the shared prefix cancels.",
            "Build P once in O(n), answer every query in O(1).",
        ],
        pattern="Prefix XOR (XOR is invertible, so it works like prefix sums)",
        explain=(
            "P[r+1] contains arr[0..r]; P[l] contains arr[0..l-1]. XOR-ing them cancels the common arr[0..l-1] (x ^ "
            "x = 0) and leaves exactly arr[l..r]. Any invertible associative operation supports this trick."
        ),
        cx="O(n + q) time, O(n) space",
        brute_cx="O(n * q) time - recompute each range",
        brute=r"""
# BRUTE FORCE: O(n * q) time - recompute each range
def xor_queries(arr, queries):
    out = []
    for left, right in queries:
        value = 0
        for x in arr[left : right + 1]:
            value ^= x
        out.append(value)
    return out
""",
        solution=r"""
# OPTIMISED: O(n + q) time, O(n) space
# Idea: Prefix XOR (XOR is invertible, so it works like prefix sums)
def xor_queries(arr, queries):
    prefix = [0]
    for x in arr:
        prefix.append(prefix[-1] ^ x)
    return [prefix[right + 1] ^ prefix[left] for left, right in queries]
""",
    ),
    # ---- Find Two Non-overlapping Sub-arrays Each With Target Sum (LeetCode 1477) ----
    dict(
        title="Find Two Non-overlapping Sub-arrays Each With Target Sum",
        diff="M",
        lc=1477,
        slug="find-two-non-overlapping-sub-arrays-each-with-target-sum",
        prompt=(
            "arr has positive integers. Find two non-overlapping subarrays, each with sum equal to target, "
            "minimising the sum of their lengths. Return that minimum, or -1 if two such subarrays do not exist."
        ),
        sig="def min_sum_of_lengths(arr: List[int], target: int) -> int:",
        fn="min_sum_of_lengths",
        tests=[
            (([3, 2, 2, 4, 3], 3), 2),
            (([7, 3, 4, 7], 7), 2),
            (([4, 3, 2, 6, 2, 3, 4], 6), -1),
            (([5, 5, 4, 4, 5], 3), -1),
            (([3, 1, 1, 1, 5, 1, 2, 1], 3), 3),
        ],
        hints=[
            "All values are positive, so a window with a given sum can be found with two pointers.",
            "When a window [left, right] hits the target, you want the shortest valid subarray that ENDS before left.",
            (
                "Keep best_end[i] = shortest valid subarray ending at or before i. For a new window add its length "
                "to best_end[left - 1]."
            ),
        ],
        pattern="Sliding window + best-so-far prefix array",
        explain=(
            "A sliding window finds every subarray with sum == target in O(n). To pair it with a non-overlapping "
            "partner, remember for each position the shortest valid subarray that ends there or earlier; the "
            "partner for the window starting at `left` is best_end[left - 1]. Taking the minimum over all windows "
            "gives the answer because every pair has one subarray entirely before the other."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time (plus the pair scan) - list every valid subarray and test pairs",
        brute=r"""
# BRUTE FORCE: O(n^2) time (plus the pair scan) - list every valid subarray and test pairs
def min_sum_of_lengths(arr, target):
    spans = []
    for i in range(len(arr)):
        total = 0
        for j in range(i, len(arr)):
            total += arr[j]
            if total == target:
                spans.append((i, j))
    best = None
    for a_start, a_end in spans:
        for b_start, b_end in spans:
            if a_end < b_start:
                cost = (a_end - a_start + 1) + (b_end - b_start + 1)
                best = cost if best is None else min(best, cost)
    return -1 if best is None else best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Sliding window + best-so-far prefix array
def min_sum_of_lengths(arr, target):
    n = len(arr)
    inf = float("inf")
    best_end = [inf] * n
    shortest = inf
    result = inf
    left = window = 0
    for right in range(n):
        window += arr[right]
        while window > target:
            window -= arr[left]
            left += 1
        if window == target:
            length = right - left + 1
            if left > 0:
                result = min(result, length + best_end[left - 1])
            shortest = min(shortest, length)
        best_end[right] = shortest
    return -1 if result == inf else result
""",
    ),
    # ---- Number of Sub-arrays With Odd Sum (LeetCode 1524) ----
    dict(
        title="Number of Sub-arrays With Odd Sum",
        diff="M",
        lc=1524,
        slug="number-of-sub-arrays-with-odd-sum",
        prompt="Count the subarrays of arr whose sum is odd. Return the count modulo 1_000_000_007.",
        sig="def num_of_subarrays(arr: List[int]) -> int:",
        fn="num_of_subarrays",
        tests=[
            (([1, 3, 5],), 4),
            (([2, 4, 6],), 0),
            (([1, 2, 3, 4, 5, 6, 7],), 16),
            (([1],), 1),
            (([2],), 0),
        ],
        hints=[
            "Only the parity of the prefix sum matters.",
            "A subarray sum is odd exactly when its two bounding prefix sums have different parities.",
            (
                "Count how many earlier prefixes were even/odd: if the current prefix is odd, add the number of "
                "even earlier ones, and vice versa."
            ),
        ],
        pattern="Prefix parity counting",
        explain=(
            "subarray sum = P[j] - P[i], which is odd iff P[j] and P[i] differ in parity. So for each j the number "
            "of valid starts is the number of earlier prefixes (including the empty prefix, which is even) of the "
            "opposite parity. Two counters give the answer in one pass."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - test every subarray sum",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every subarray sum
def num_of_subarrays(arr):
    count = 0
    for i in range(len(arr)):
        total = 0
        for j in range(i, len(arr)):
            total += arr[j]
            if total % 2 == 1:
                count += 1
    return count % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Prefix parity counting
def num_of_subarrays(arr):
    even, odd = 1, 0
    parity = 0
    total = 0
    for x in arr:
        parity ^= x & 1
        if parity:
            total += even
            odd += 1
        else:
            total += odd
            even += 1
    return total % (10**9 + 7)
""",
    ),
    # ---- Find the Highest Altitude (LeetCode 1732) ----
    dict(
        title="Find the Highest Altitude",
        diff="E",
        lc=1732,
        slug="find-the-highest-altitude",
        prompt=(
            "A biker starts at altitude 0. gain[i] is the net altitude change between point i and point i + 1. "
            "Return the highest altitude reached (the start counts)."
        ),
        sig="def largest_altitude(gain: List[int]) -> int:",
        fn="largest_altitude",
        tests=[
            (([-5, 1, 5, 0, -7],), 1),
            (([-4, -3, -2, -1, 4, 3, 2],), 0),
            (([5],), 5),
            (([-1],), 0),
            (([],), 0),
        ],
        hints=[
            "The altitude at point i is the sum of the first i gains.",
            "You do not need to store them - keep a running total.",
            "Track the maximum of the running total, starting from 0 for the starting point.",
        ],
        pattern="Running prefix sum with a max",
        explain=(
            "Altitude after i steps is the prefix sum of gain, so the answer is the maximum prefix sum including "
            "the empty prefix (altitude 0). A single running total and a running maximum are enough."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - re-add the first i gains for every point",
        brute=r"""
# BRUTE FORCE: O(n^2) time - re-add the first i gains for every point
def largest_altitude(gain):
    return max(sum(gain[:i]) for i in range(len(gain) + 1))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Running prefix sum with a max
def largest_altitude(gain):
    altitude = best = 0
    for g in gain:
        altitude += g
        best = max(best, altitude)
    return best
""",
    ),
    # ---- Range Product Queries of Powers (LeetCode 2438) ----
    dict(
        title="Range Product Queries of Powers",
        diff="M",
        lc=2438,
        slug="range-product-queries-of-powers",
        prompt=(
            "Let powers be the shortest sorted (ascending) list of powers of two that sums to n - i.e. the set bits "
            "of n. For each query [left, right] return the product of powers[left..right] modulo 1_000_000_007."
        ),
        sig="def product_queries(n: int, queries: List[List[int]]) -> List[int]:",
        fn="product_queries",
        tests=[
            ((15, [[0, 1], [2, 2], [0, 3]]), [2, 4, 64]),
            ((2, [[0, 0]]), [2]),
            ((10, [[0, 1], [1, 1]]), [16, 8]),
            ((1, [[0, 0]]), [1]),
        ],
        hints=[
            "The shortest representation of n as a sum of powers of two is its binary expansion.",
            "A product of powers of two is 2 to the SUM of the exponents.",
            "Take prefix sums of the exponents; a query is pow(2, prefix[r+1] - prefix[l], mod).",
        ],
        pattern="Prefix sums of exponents (products become sums in the exponent)",
        explain=(
            "powers are 2^e for each set bit e of n, in increasing order. The product over a range is 2 raised to "
            "the sum of those exponents, and range sums come from a prefix array. Fast modular exponentiation (the "
            "built-in 3-argument pow) turns each query into O(log) work instead of a long multiplication loop."
        ),
        cx="O(log n + q log n) time, O(log n) space",
        brute_cx="O(q * log n) time - multiply the listed powers one by one for each query",
        brute=r"""
# BRUTE FORCE: O(q * log n) time - multiply the listed powers one by one for each query
def product_queries(n, queries):
    mod = 10**9 + 7
    powers = [1 << i for i in range(n.bit_length()) if n >> i & 1]
    out = []
    for left, right in queries:
        value = 1
        for x in powers[left : right + 1]:
            value = value * x % mod
        out.append(value)
    return out
""",
        solution=r"""
# OPTIMISED: O(log n + q log n) time, O(log n) space
# Idea: Prefix sums of exponents (products become sums in the exponent)
def product_queries(n, queries):
    mod = 10**9 + 7
    prefix = [0]
    for e in range(n.bit_length()):
        if n >> e & 1:
            prefix.append(prefix[-1] + e)
    return [pow(2, prefix[right + 1] - prefix[left], mod) for left, right in queries]
""",
    ),
    # ---- Find the Middle Index in Array (LeetCode 1991) ----
    dict(
        title="Find the Middle Index in Array",
        diff="E",
        lc=1991,
        slug="find-the-middle-index-in-array",
        prompt=(
            "Return the leftmost index i such that the sum of the elements strictly left of i equals the sum of the "
            "elements strictly right of i (an empty side sums to 0). Return -1 if there is none."
        ),
        sig="def find_middle_index(nums: List[int]) -> int:",
        fn="find_middle_index",
        tests=[
            (([2, 3, -1, 8, 4],), 3),
            (([1, -1, 4],), 2),
            (([2, 5],), -1),
            (([1],), 0),
            (([0, 0],), 0),
        ],
        hints=[
            "left(i) + nums[i] + right(i) == total.",
            "So the condition left(i) == right(i) becomes 2 * left(i) + nums[i] == total.",
            "Sweep once keeping left as a running sum; return the first i with 2 * left + nums[i] == total.",
        ],
        pattern="Running left sum vs total",
        explain=(
            "The right sum is total - left - nums[i], so equality of the two sides is one arithmetic test per "
            "index. Scanning left to right returns the leftmost index immediately."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - re-sum both sides for every index",
        brute=r"""
# BRUTE FORCE: O(n^2) time - re-sum both sides for every index
def find_middle_index(nums):
    for i in range(len(nums)):
        if sum(nums[:i]) == sum(nums[i + 1 :]):
            return i
    return -1
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Running left sum vs total
def find_middle_index(nums):
    total = sum(nums)
    left = 0
    for i, x in enumerate(nums):
        if 2 * left + x == total:
            return i
        left += x
    return -1
""",
    ),
    # ---- Left and Right Sum Differences (LeetCode 2574) ----
    dict(
        title="Left and Right Sum Differences",
        diff="E",
        lc=2574,
        slug="left-and-right-sum-differences",
        prompt=(
            "For each index i return |leftSum[i] - rightSum[i]| where leftSum is the sum of elements strictly to "
            "the left of i and rightSum the sum strictly to the right."
        ),
        sig="def left_right_difference(nums: List[int]) -> List[int]:",
        fn="left_right_difference",
        tests=[
            (([10, 4, 8, 3],), [15, 1, 11, 22]),
            (([1],), [0]),
            (([1, 2, 3],), [5, 2, 3]),
            (([0, 0],), [0, 0]),
        ],
        hints=[
            "Recomputing both sums for each index is O(n^2).",
            "The right sum is total - left - nums[i].",
            "Keep one running left sum and compute the right sum in O(1).",
        ],
        pattern="Prefix sum with the total",
        explain=(
            "Knowing the grand total makes the right-hand sum a subtraction away from the running left sum, so one "
            "pass produces every answer."
        ),
        cx="O(n) time, O(1) extra space",
        brute_cx="O(n^2) time - sum the two sides for each index",
        brute=r"""
# BRUTE FORCE: O(n^2) time - sum the two sides for each index
def left_right_difference(nums):
    return [abs(sum(nums[:i]) - sum(nums[i + 1 :])) for i in range(len(nums))]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) extra space
# Idea: Prefix sum with the total
def left_right_difference(nums):
    total = sum(nums)
    left = 0
    out = []
    for x in nums:
        out.append(abs(left - (total - left - x)))
        left += x
    return out
""",
    ),
    # ---- Maximum Absolute Sum of Any Subarray (LeetCode 1749) ----
    dict(
        title="Maximum Absolute Sum of Any Subarray",
        diff="M",
        lc=1749,
        slug="maximum-absolute-sum-of-any-subarray",
        prompt="Return the maximum absolute value of the sum of any (possibly empty) subarray of nums.",
        sig="def max_absolute_sum(nums: List[int]) -> int:",
        fn="max_absolute_sum",
        tests=[
            (([1, -3, 2, 3, -4],), 5),
            (([2, -5, 1, -4, 3, -2],), 8),
            (([-1],), 1),
            (([1, 2, 3],), 6),
            (([0],), 0),
        ],
        hints=[
            "A subarray sum is a difference of two prefix sums.",
            (
                "The largest absolute difference between two prefix sums is the difference between the largest and "
                "the smallest prefix."
            ),
            (
                "Track the running prefix sum with its minimum and maximum (start from the empty prefix 0); answer "
                "max - min."
            ),
        ],
        pattern="Max prefix - min prefix",
        explain=(
            "The absolute sum of subarray (i, j] is |P[j] - P[i]|. Over all pairs this is largest when one prefix "
            "is the global maximum and the other the global minimum, so the answer is max(P) - min(P) with P[0] = 0."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - test every subarray",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every subarray
def max_absolute_sum(nums):
    best = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            best = max(best, abs(total))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Max prefix - min prefix
def max_absolute_sum(nums):
    prefix = lowest = highest = 0
    for x in nums:
        prefix += x
        lowest = min(lowest, prefix)
        highest = max(highest, prefix)
    return highest - lowest
""",
    ),
    # ---- Unique Length-3 Palindromic Subsequences (LeetCode 1930) ----
    dict(
        title="Unique Length-3 Palindromic Subsequences",
        diff="M",
        lc=1930,
        slug="unique-length-3-palindromic-subsequences",
        prompt=(
            "Count the DISTINCT palindromic subsequences of length 3 of the lowercase string s (a subsequence keeps "
            "relative order; two are the same if they are the same string)."
        ),
        sig="def count_palindromic_subsequence(s: str) -> int:",
        fn="count_palindromic_subsequence",
        tests=[
            (("aabca",), 3),
            (("adc",), 0),
            (("bbcbaba",), 4),
            (("aaa",), 1),
            (("abca",), 2),
        ],
        hints=[
            "A length-3 palindrome has the form x y x.",
            (
                "For each letter x, only its FIRST and LAST occurrence matter as the outer pair - that gives the "
                "widest middle."
            ),
            "Count the distinct letters strictly between the first and last occurrence of x; sum over all 26 letters.",
        ],
        pattern="First/last occurrence + distinct letters in between",
        explain=(
            "A palindrome x y x exists iff some y lies between two occurrences of x. Using the first and last "
            "occurrence of x maximises the set of available y, so the number of distinct palindromes with outer "
            "letter x is the number of distinct letters in between. Different (x, y) pairs give different strings, "
            "so summing over x counts every distinct palindrome exactly once."
        ),
        cx="O(26 * n) time, O(26) space",
        brute_cx="O(n^3) time - generate every 3-subsequence and keep distinct palindromes in a set",
        brute=r"""
# BRUTE FORCE: O(n^3) time - generate every 3-subsequence and keep distinct palindromes in a set
def count_palindromic_subsequence(s):
    found = set()
    n = len(s)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if s[i] == s[k]:
                    found.add(s[i] + s[j] + s[k])
    return len(found)
""",
        solution=r"""
# OPTIMISED: O(26 * n) time, O(26) space
# Idea: First/last occurrence + distinct letters in between
def count_palindromic_subsequence(s):
    total = 0
    for letter in set(s):
        first, last = s.find(letter), s.rfind(letter)
        if last - first >= 2:
            total += len(set(s[first + 1 : last]))
    return total
""",
    ),
    # ---- K Radius Subarray Averages (LeetCode 2090) ----
    dict(
        title="K Radius Subarray Averages",
        diff="M",
        lc=2090,
        slug="k-radius-subarray-averages",
        prompt=(
            "For each index i return the integer average (floor) of nums[i-k..i+k], or -1 if fewer than k elements "
            "exist on either side of i."
        ),
        sig="def get_averages(nums: List[int], k: int) -> List[int]:",
        fn="get_averages",
        tests=[
            (([7, 4, 3, 9, 1, 8, 5, 2, 6], 3), [-1, -1, -1, 5, 4, 4, -1, -1, -1]),
            (([100000], 0), [100000]),
            (([8], 100000), [-1]),
            (([1, 2, 3, 4], 1), [-1, 2, 3, -1]),
            (([1, 2], 0), [1, 2]),
        ],
        hints=[
            "Summing 2k+1 elements for every index is O(n * k).",
            "Use prefix sums: sum(nums[a..b]) = P[b+1] - P[a].",
            "Index i has a full window only when k <= i < n - k. Its sum is P[i+k+1] - P[i-k]; divide by 2k+1 with //.",
        ],
        pattern="Prefix sums for fixed-width window sums",
        explain=(
            "Every window has the same width 2k+1, so its sum is a difference of two prefix sums and the average is "
            "that sum divided by the width. Indices too close to either end have no full window and get -1."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n * k) time - add up each window directly",
        brute=r"""
# BRUTE FORCE: O(n * k) time - add up each window directly
def get_averages(nums, k):
    n = len(nums)
    out = []
    for i in range(n):
        if i - k < 0 or i + k >= n:
            out.append(-1)
        else:
            out.append(sum(nums[i - k : i + k + 1]) // (2 * k + 1))
    return out
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Prefix sums for fixed-width window sums
def get_averages(nums, k):
    n = len(nums)
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)
    out = [-1] * n
    for i in range(k, n - k):
        out[i] = (prefix[i + k + 1] - prefix[i - k]) // (2 * k + 1)
    return out
""",
    ),
    # ---- Sum of Absolute Differences in a Sorted Array (LeetCode 1685) ----
    dict(
        title="Sum of Absolute Differences in a Sorted Array",
        diff="M",
        lc=1685,
        slug="sum-of-absolute-differences-in-a-sorted-array",
        prompt=(
            "nums is sorted in non-decreasing order. For each i return the sum of |nums[i] - nums[j]| over all j (j "
            "= i contributes 0)."
        ),
        sig="def get_sum_absolute_differences(nums: List[int]) -> List[int]:",
        fn="get_sum_absolute_differences",
        tests=[
            (([2, 3, 5],), [4, 3, 5]),
            (([1, 4, 6, 8, 10],), [24, 15, 13, 15, 21]),
            (([7],), [0]),
            (([3, 3],), [0, 0]),
        ],
        hints=[
            "Because the array is sorted you know the sign of every nums[i] - nums[j].",
            "For j < i the difference is nums[i] - nums[j]; for j > i it is nums[j] - nums[i].",
            "result[i] = (nums[i]*i - sum_left) + (sum_right - nums[i]*(n-1-i)) with running prefix sums.",
        ],
        pattern="Prefix sums on a sorted array removes the absolute value",
        explain=(
            "Sortedness fixes every sign: the i elements to the left are each <= nums[i], the n-1-i elements to the "
            "right are each >= nums[i]. The left part contributes nums[i]*i minus their sum, the right part "
            "contributes their sum minus nums[i]*(n-1-i); both sums come from one running total."
        ),
        cx="O(n) time, O(1) extra space",
        brute_cx="O(n^2) time - sum |difference| for every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - sum |difference| for every pair
def get_sum_absolute_differences(nums):
    return [sum(abs(x - y) for y in nums) for x in nums]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) extra space
# Idea: Prefix sums on a sorted array removes the absolute value
def get_sum_absolute_differences(nums):
    n, total = len(nums), sum(nums)
    left = 0
    out = []
    for i, x in enumerate(nums):
        right = total - left - x
        out.append(x * i - left + right - x * (n - 1 - i))
        left += x
    return out
""",
    ),
    # ---- Count of Interesting Subarrays (LeetCode 2845) ----
    dict(
        title="Count of Interesting Subarrays",
        diff="M",
        lc=2845,
        slug="count-of-interesting-subarrays",
        prompt=(
            "A subarray is interesting if, letting cnt be the number of its indices i with nums[i] % modulo == k, "
            "cnt % modulo == k. Count the interesting subarrays."
        ),
        sig="def count_interesting_subarrays(nums: List[int], modulo: int, k: int) -> int:",
        fn="count_interesting_subarrays",
        tests=[
            (([3, 2, 4], 2, 1), 3),
            (([3, 1, 9, 6], 3, 0), 2),
            (([1], 2, 1), 1),
            (([2, 2], 2, 1), 0),
        ],
        hints=[
            (
                "Turn the array into 1s and 0s: 1 where nums[i] % modulo == k. Now you count subarrays whose sum of "
                "1s is congruent to k mod modulo."
            ),
            "That is a prefix-sum-mod problem: (P[j] - P[i]) % modulo == k.",
            (
                "For each prefix value p = P[j] % modulo, add how many earlier prefixes had remainder (p - k) % "
                "modulo; then record p."
            ),
        ],
        pattern="Prefix counts mod m with a frequency map",
        explain=(
            "cnt for subarray (i, j] equals P[j] - P[i] where P counts qualifying elements. The condition (P[j] - "
            "P[i]) % modulo == k is the same as P[i] % modulo == (P[j] - k) % modulo, so a frequency map of earlier "
            "prefix remainders answers each j in O(1)."
        ),
        cx="O(n) time, O(min(n, modulo)) space",
        brute_cx="O(n^2) time - count the qualifying elements of every subarray",
        brute=r"""
# BRUTE FORCE: O(n^2) time - count the qualifying elements of every subarray
def count_interesting_subarrays(nums, modulo, k):
    total = 0
    for i in range(len(nums)):
        cnt = 0
        for j in range(i, len(nums)):
            if nums[j] % modulo == k:
                cnt += 1
            if cnt % modulo == k:
                total += 1
    return total
""",
        solution=r"""
# OPTIMISED: O(n) time, O(min(n, modulo)) space
# Idea: Prefix counts mod m with a frequency map
def count_interesting_subarrays(nums, modulo, k):
    seen = Counter({0: 1})
    cnt = 0
    total = 0
    for x in nums:
        if x % modulo == k:
            cnt += 1
        total += seen[(cnt - k) % modulo]
        seen[cnt % modulo] += 1
    return total
""",
    ),
    # ---- Count the Number of Beautiful Subarrays (LeetCode 2588) ----
    dict(
        title="Count the Number of Beautiful Subarrays",
        diff="M",
        lc=2588,
        slug="count-the-number-of-beautiful-subarrays",
        prompt=(
            "In one operation pick two different indices i, j and a bit position b that is set in both nums[i] and "
            "nums[j], and clear that bit in both. A subarray is beautiful if it can be turned into all zeros with "
            "such operations. Count the beautiful subarrays."
        ),
        sig="def beautiful_subarrays(nums: List[int]) -> int:",
        fn="beautiful_subarrays",
        tests=[
            (([4, 3, 1, 2, 4],), 2),
            (([1, 10, 4],), 0),
            (([0],), 1),
            (([1, 1],), 1),
            (([3, 3, 3],), 2),
        ],
        hints=[
            "Each operation removes exactly two copies of one bit. When can ALL bits be removed?",
            (
                "Exactly when every bit position is set an even number of times in the subarray - that is, the XOR "
                "of the subarray is 0."
            ),
            "Count subarrays with XOR 0: prefix XOR with a frequency map - equal prefix values bound such a subarray.",
        ],
        pattern="Reduce to XOR == 0, then prefix XOR + frequency map",
        explain=(
            "An operation clears one bit from two numbers, so every bit position must have an even total count in "
            "the subarray for it to be fully cleared - and that is precisely XOR == 0 (and sufficient, since equal "
            "pairs of set bits can always be matched). A subarray has XOR 0 iff its two bounding prefix XORs are "
            "equal, so count equal pairs of prefix values."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2 * 20) time - for every subarray check that every bit appears an even number of times",
        brute=r"""
# BRUTE FORCE: O(n^2 * 20) time - for every subarray check that every bit appears an even number of times
def beautiful_subarrays(nums):
    total = 0
    for i in range(len(nums)):
        counts = [0] * 21
        for j in range(i, len(nums)):
            for bit in range(21):
                counts[bit] += nums[j] >> bit & 1
            if all(c % 2 == 0 for c in counts):
                total += 1
    return total
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Reduce to XOR == 0, then prefix XOR + frequency map
def beautiful_subarrays(nums):
    seen = Counter({0: 1})
    prefix = 0
    total = 0
    for x in nums:
        prefix ^= x
        total += seen[prefix]
        seen[prefix] += 1
    return total
""",
    ),
    # ---- Sum of Floored Pairs (LeetCode 1862) ----
    dict(
        title="Sum of Floored Pairs",
        diff="H",
        lc=1862,
        slug="sum-of-floored-pairs",
        prompt=(
            "Return the sum of floor(nums[i] / nums[j]) over ALL pairs (i, j), modulo 1_000_000_007. Pairs are "
            "ordered and i = j is included."
        ),
        sig="def sum_of_floored_pairs(nums: List[int]) -> int:",
        fn="sum_of_floored_pairs",
        tests=[
            (([2, 5, 9],), 10),
            (([7, 7, 7, 7, 7, 7, 7],), 49),
            (([1],), 1),
            (([1, 2],), 4),
        ],
        hints=[
            "O(n^2) pairs is too many when n is 10^5, but the VALUES are bounded by max(nums).",
            "For a fixed divisor v, floor(x / v) = m for every x in [m*v, m*v + v - 1].",
            (
                "Count values in value-ranges with a prefix count array over values; sum over every multiple m of "
                "v. The harmonic sum makes the total O(M log M)."
            ),
        ],
        pattern="Counting array + prefix counts over value ranges (harmonic sum)",
        explain=(
            "Let cnt[x] be the multiplicity of x and pre[x] the number of elements <= x. For each distinct divisor "
            "v and each multiple m*v up to max, the elements in [m*v, m*v + v - 1] all contribute m, so they add "
            "cnt[v] * m * (pre[hi] - pre[m*v - 1]). The number of (v, m) pairs is about M ln M, far below n^2 for "
            "large n."
        ),
        cx="O(n + M log M) time, O(M) space with M = max(nums)",
        brute_cx="O(n^2) time - try every ordered pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - try every ordered pair
def sum_of_floored_pairs(nums):
    return sum(a // b for a in nums for b in nums) % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n + M log M) time, O(M) space with M = max(nums)
# Idea: Counting array + prefix counts over value ranges (harmonic sum)
def sum_of_floored_pairs(nums):
    top = max(nums)
    cnt = [0] * (top + 1)
    for x in nums:
        cnt[x] += 1
    pre = [0] * (top + 1)
    for v in range(1, top + 1):
        pre[v] = pre[v - 1] + cnt[v]
    total = 0
    for v in range(1, top + 1):
        if cnt[v]:
            for start in range(v, top + 1, v):
                hi = min(top, start + v - 1)
                total += cnt[v] * (start // v) * (pre[hi] - pre[start - 1])
    return total % (10**9 + 7)
""",
    ),
]
