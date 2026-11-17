"""extra batch of Divide & Conquer problems - the problem bank for the "divide_conquer" topic (batch 3).

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

from core import tree_to_list


def _beautiful_ok(args, got):
    """True if `got` is a permutation of 1..n with no i < k < j where 2 * got[k] == got[i] + got[j]."""
    n = args[0]
    if not isinstance(got, list) or sorted(got) != list(range(1, n + 1)):
        return False
    return all(2 * got[k] != got[i] + got[j] for i in range(n) for j in range(i + 2, n) for k in range(i + 1, j))


PROBLEMS = [
    # ---- Different Ways to Add Parentheses (LeetCode 241) ----
    dict(
        title="Different Ways to Add Parentheses",
        diff="M",
        lc=241,
        slug="different-ways-to-add-parentheses",
        prompt=(
            "expression has digits and the operators +, - and *. Group it with parentheses in every possible way "
            "and return the results of all groupings (duplicates kept, any order)."
        ),
        sig="def diff_ways_to_compute(expression: str) -> List[int]:",
        fn="diff_ways_to_compute",
        compare="unordered",
        tests=[
            (("2-1-1",), [0, 2]),
            (("2*3-4*5",), [-34, -14, -10, -10, 10]),
            (("11",), [11]),
            (("1+1",), [2]),
            (("3-2*2",), [2, -1]),
        ],
        hints=[
            "Whatever the grouping, exactly one operator is evaluated LAST.",
            (
                "Pick each operator as the last one: all results of the left part combined with all results of the "
                "right part."
            ),
            (
                "The same substring is solved many times (3-2*2 inside longer inputs) - cache the result list per "
                "substring."
            ),
        ],
        pattern="Divide and conquer on the last operator + memoisation of substrings",
        explain=(
            "Every full parenthesisation has one top-level operator that splits the string into a left and a right "
            "expression. Solving each side recursively and combining every left value with every right value yields "
            "all results. Substrings repeat across different splits, so memoising by substring removes the repeated "
            "work (the number of results is a Catalan number, so the output itself stays exponential)."
        ),
        cx="O(Catalan(n)) time - proportional to the number of results; memo avoids recomputing substrings",
        brute_cx="same recursion without caching: sub-expressions are recomputed for every split",
        brute=r"""
# BRUTE FORCE: same recursion without caching: sub-expressions are recomputed for every split
def diff_ways_to_compute(expression):
    if expression.isdigit():
        return [int(expression)]

    results = []

    for i, ch in enumerate(expression):
        if ch in "+-*":
            for a in diff_ways_to_compute(expression[:i]):
                for b in diff_ways_to_compute(expression[i + 1 :]):
                    results.append(a + b if ch == "+" else a - b if ch == "-" else a * b)

    return results
""",
        solution=r"""
# OPTIMISED: O(Catalan(n)) time - proportional to the number of results; memo avoids recomputing substrings
# Idea: Divide and conquer on the last operator + memoisation of substrings
def diff_ways_to_compute(expression):
    @lru_cache(None)
    def ways(text):
        if text.isdigit():
            return (int(text),)

        results = []

        for i, ch in enumerate(text):
            if ch in "+-*":
                for a in ways(text[:i]):
                    for b in ways(text[i + 1 :]):
                        results.append(a + b if ch == "+" else a - b if ch == "-" else a * b)

        return tuple(results)

    return list(ways(expression))
""",
    ),
    # ---- Count of Range Sum (LeetCode 327) ----
    dict(
        title="Count of Range Sum",
        diff="H",
        lc=327,
        slug="count-of-range-sum",
        prompt="Count the contiguous subarrays of nums whose sum lies in the inclusive range [lower, upper].",
        sig="def count_range_sum(nums: List[int], lower: int, upper: int) -> int:",
        fn="count_range_sum",
        tests=[
            (([-2, 5, -1], -2, 2), 3),
            (([0], 0, 0), 1),
            (([0, 0], 0, 0), 3),
            (([1, 2, 3], 3, 5), 3),
            (([5], 6, 10), 0),
        ],
        hints=[
            (
                "Subarray sum = prefix[j] - prefix[i]. You are counting pairs i < j of prefix sums with a bounded "
                "difference."
            ),
            (
                "Sort-based counting: if two halves are each sorted, for every element on the left the matching "
                "right elements form a contiguous window."
            ),
            (
                "Merge-sort the prefix sums; before merging, slide two pointers over the sorted right half to count "
                "prefix[j] - prefix[i] in [lower, upper]."
            ),
        ],
        pattern="Merge sort on prefix sums, counting cross pairs",
        explain=(
            "With prefix sums p, the answer is the number of pairs i < j with lower <= p[j] - p[i] <= upper. Split "
            "the array of prefix sums in two; pairs inside a half are counted recursively, and pairs across the "
            "halves are counted while both halves are sorted: as p[i] grows, the window of right-half values within "
            "[p[i] + lower, p[i] + upper] only moves right, so two pointers suffice."
        ),
        cx="O(n log^2 n) time with the simple re-sort (O(n log n) with a true merge), O(n) space",
        brute_cx="O(n^2) time - test every subarray",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every subarray
def count_range_sum(nums, lower, upper):
    count = 0

    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if lower <= total <= upper:
                count += 1

    return count
""",
        solution=r"""
# OPTIMISED: O(n log^2 n) time with the simple re-sort (O(n log n) with a true merge), O(n) space
# Idea: Merge sort on prefix sums, counting cross pairs
def count_range_sum(nums, lower, upper):
    prefix = [0]

    for x in nums:
        prefix.append(prefix[-1] + x)

    def sort_and_count(lo, hi):
        if hi - lo <= 1:
            return 0

        mid = (lo + hi) // 2
        count = sort_and_count(lo, mid) + sort_and_count(mid, hi)
        start = end = mid

        for i in range(lo, mid):
            while start < hi and prefix[start] - prefix[i] < lower:
                start += 1
            while end < hi and prefix[end] - prefix[i] <= upper:
                end += 1
            count += end - start

        prefix[lo:hi] = sorted(prefix[lo:hi])

        return count

    return sort_and_count(0, len(prefix))
""",
    ),
    # ---- Beautiful Array (LeetCode 932) ----
    dict(
        title="Beautiful Array",
        diff="M",
        lc=932,
        slug="beautiful-array",
        prompt=(
            "A permutation of 1..n is beautiful if there are no indices i < k < j with 2 * a[k] == a[i] + a[j]. "
            "Return any beautiful array of length n."
        ),
        sig="def beautiful_array(n: int) -> List[int]:",
        fn="beautiful_array",
        check=_beautiful_ok,
        tests=[
            ((1,), [1]),
            ((2,), [1, 2]),
            ((4,), [1, 3, 2, 4]),
            ((5,), [1, 5, 3, 2, 4]),
            ((6,), [1, 5, 3, 2, 6, 4]),
        ],
        hints=[
            (
                "The forbidden pattern says a[k] is the average of two others; averages of two numbers with "
                "different parity are not integers."
            ),
            (
                "If you put all odd numbers on one side and all even numbers on the other, no k in the middle can "
                "be the average of an odd and an even."
            ),
            (
                "Build recursively: a beautiful array stays beautiful under x -> 2x - 1 (odds) and x -> 2x (evens). "
                "Concatenate the two images."
            ),
        ],
        pattern="Divide and conquer: affine maps keep the property, parity separates the halves",
        explain=(
            "If A is beautiful, then 2*A - 1 (all odd) and 2*A (all even) are beautiful too, because the condition "
            "is preserved by x -> a*x + b. Putting the odd copy before the even copy means any triple that crosses "
            "the boundary has an odd and an even endpoint whose sum is odd, so it cannot equal 2 * a[k]. Grow from "
            "[1] and discard values above n."
        ),
        cx="O(n) time (sizes double each round), O(n) space",
        brute_cx="O(n! * n^3) time - try every permutation",
        brute=r"""
# BRUTE FORCE: O(n! * n^3) time - try every permutation
def beautiful_array(n):
    for perm in itertools.permutations(range(1, n + 1)):
        if all(
            2 * perm[k] != perm[i] + perm[j]
            for i in range(n)
            for j in range(i + 2, n)
            for k in range(i + 1, j)
        ):
            return list(perm)
""",
        solution=r"""
# OPTIMISED: O(n) time (sizes double each round), O(n) space
# Idea: Divide and conquer: affine maps keep the property, parity separates the halves
def beautiful_array(n):
    result = [1]
    while len(result) < n:
        result = [2 * x - 1 for x in result] + [2 * x for x in result]
    return [x for x in result if x <= n]
""",
    ),
    # ---- K-th Symbol in Grammar (LeetCode 779) ----
    dict(
        title="K-th Symbol in Grammar",
        diff="M",
        lc=779,
        slug="k-th-symbol-in-grammar",
        prompt=(
            "Row 1 is '0'. Each next row replaces every 0 by '01' and every 1 by '10'. Return the k-th symbol "
            "(1-indexed) of row n."
        ),
        sig="def kth_grammar(n: int, k: int) -> int:",
        fn="kth_grammar",
        tests=[
            ((1, 1), 0),
            ((2, 1), 0),
            ((2, 2), 1),
            ((3, 3), 1),
            ((4, 5), 1),
            ((4, 4), 0),
        ],
        hints=[
            "Row n has 2^(n-1) symbols - building the row is hopeless for n = 30.",
            "Symbol k of row n comes from symbol (k + 1) // 2 of row n - 1.",
            (
                "If k is odd you are the first child (same symbol as the parent); if k is even you are the second "
                "child (the opposite symbol)."
            ),
        ],
        pattern="Divide and conquer: go back to the parent, flip on even positions",
        explain=(
            "Every symbol of row n-1 produces two children, so position k descends from position ceil(k/2). The "
            "left child equals the parent and the right child is its complement, so the answer is the parent's "
            "value, flipped when k is even. The recursion has depth n and does O(1) work per level."
        ),
        cx="O(n) time, O(n) recursion depth",
        brute_cx="O(2^n) time and space - build the whole row",
        brute=r"""
# BRUTE FORCE: O(2^n) time and space - build the whole row
def kth_grammar(n, k):
    row = "0"
    for _ in range(n - 1):
        row = "".join("01" if ch == "0" else "10" for ch in row)
    return int(row[k - 1])
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) recursion depth
# Idea: Divide and conquer: go back to the parent, flip on even positions
def kth_grammar(n, k):
    if n == 1:
        return 0
    parent = kth_grammar(n - 1, (k + 1) // 2)
    return parent if k % 2 == 1 else 1 - parent
""",
    ),
    # ---- Longest Substring with At Least K Repeating Characters (LeetCode 395) ----
    dict(
        title="Longest Substring with At Least K Repeating Characters",
        diff="M",
        lc=395,
        slug="longest-substring-with-at-least-k-repeating-characters",
        prompt=(
            "Return the length of the longest substring of s in which every character that appears occurs at least "
            "k times (0 if there is none)."
        ),
        sig="def longest_substring(s: str, k: int) -> int:",
        fn="longest_substring",
        tests=[
            (("aaabb", 3), 3),
            (("ababbc", 2), 5),
            (("a", 2), 0),
            (("aaabbb", 3), 6),
            (("abcde", 2), 0),
            (("bbaaacbd", 3), 3),
        ],
        hints=[
            "A character that occurs fewer than k times in the whole string can never be part of the answer.",
            "Such a character cuts the string into independent pieces.",
            (
                "Split at every too-rare character and solve each piece recursively; a piece with no rare character "
                "is itself valid."
            ),
        ],
        pattern="Divide and conquer: split on the characters that cannot be inside any answer",
        explain=(
            "If some character appears fewer than k times in the current segment, no valid substring can contain "
            "it, so the answer lies entirely in one of the pieces on either side. If no such character exists the "
            "whole segment is valid. Each split removes a character class, so the recursion depth is at most 26."
        ),
        cx="O(26 * n) time, O(26) extra space per level",
        brute_cx="O(n^2 * 26) time - count characters of every substring",
        brute=r"""
# BRUTE FORCE: O(n^2 * 26) time - count characters of every substring
def longest_substring(s, k):
    best = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            counts = Counter(s[i:j])
            if min(counts.values()) >= k:
                best = max(best, j - i)
    return best
""",
        solution=r"""
# OPTIMISED: O(26 * n) time, O(26) extra space per level
# Idea: Divide and conquer: split on the characters that cannot be inside any answer
def longest_substring(s, k):
    def solve(lo, hi):
        if hi - lo < k:
            return 0
        counts = Counter(s[lo:hi])
        for i in range(lo, hi):
            if counts[s[i]] < k:
                return max(solve(lo, i), solve(i + 1, hi))
        return hi - lo

    return solve(0, len(s))
""",
    ),
    # ---- The Skyline Problem (LeetCode 218) ----
    dict(
        title="The Skyline Problem",
        diff="H",
        lc=218,
        slug="the-skyline-problem",
        prompt=(
            "buildings[i] = [left, right, height]. Return the skyline as the list of 'key points' [x, height] where "
            "the height of the outline changes (the last point has height 0)."
        ),
        sig="def get_skyline(buildings: List[List[int]]) -> List[List[int]]:",
        fn="get_skyline",
        tests=[
            (
                ([[2, 9, 10], [3, 7, 15], [5, 12, 12], [15, 20, 10], [19, 24, 8]],),
                [[2, 10], [3, 15], [7, 12], [12, 0], [15, 10], [20, 8], [24, 0]],
            ),
            (([[0, 2, 3], [2, 5, 3]],), [[0, 3], [5, 0]]),
            (([[1, 2, 1], [1, 2, 2], [1, 2, 3]],), [[1, 3], [2, 0]]),
            (([[0, 1, 1]],), [[0, 1], [1, 0]]),
        ],
        hints=[
            "The outline can only change at a building's left or right edge.",
            "At each such x, the height is the maximum height among buildings covering x.",
            (
                "Sweep the edges in order with a max-heap of (height, right edge); lazily drop buildings whose "
                "right edge has passed; emit a point whenever the top height changes."
            ),
        ],
        pattern="Sweep line with a max-heap (lazy deletion)",
        explain=(
            "Only the 2n edge coordinates matter. Processing them in sorted order (taller starts first at equal x, "
            "starts before ends), keep a heap of the buildings that have started. Buildings whose right edge is <= "
            "x are discarded when they reach the top (lazy deletion). The current skyline height is the heap top (0 "
            "if empty), and a key point is output whenever that height differs from the previous one."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2) time - at every edge coordinate scan all buildings for the maximum covering height",
        brute=r"""
# BRUTE FORCE: O(n^2) time - at every edge coordinate scan all buildings for the maximum covering height
def get_skyline(buildings):
    xs = sorted({x for left, right, _ in buildings for x in (left, right)})
    result = []
    for x in xs:
        height = max((h for left, right, h in buildings if left <= x < right), default=0)
        if not result or result[-1][1] != height:
            result.append([x, height])
    return result
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Sweep line with a max-heap (lazy deletion)
def get_skyline(buildings):
    events = sorted(
        [(left, -h, right) for left, right, h in buildings]
        + [(right, 0, 0) for _, right, _ in buildings]
    )
    result = []
    heap = [(0, float("inf"))]

    for x, neg_h, right in events:
        while heap[0][1] <= x:
            heapq.heappop(heap)
        if neg_h:
            heapq.heappush(heap, (neg_h, right))
        height = -heap[0][0]
        if not result or result[-1][1] != height:
            result.append([x, height])

    return result
""",
    ),
    # ---- Maximum Binary Tree (LeetCode 654) ----
    dict(
        title="Maximum Binary Tree",
        diff="M",
        lc=654,
        slug="maximum-binary-tree",
        prompt=(
            "Build a tree from distinct numbers: the root is the maximum, its left subtree is built from the "
            "numbers to the left of the maximum and its right subtree from the numbers to the right (recursively). "
            "Return the root."
        ),
        sig="def construct_maximum_binary_tree(nums: List[int]) -> Optional[TreeNode]:",
        fn="construct_maximum_binary_tree",
        adapt_out=tree_to_list,
        tests=[
            (([3, 2, 1, 6, 0, 5],), [6, 3, 5, None, 2, 0, None, None, 1]),
            (([3, 2, 1],), [3, None, 2, None, 1]),
            (([1],), [1]),
            (([1, 2],), [2, 1]),
            (([2, 1],), [2, None, 1]),
        ],
        hints=[
            "The definition is already recursive: find the maximum, split, recurse.",
            (
                "Finding the maximum each time is O(n) per call, so O(n^2) on sorted input. Can the maximums be "
                "found while scanning once?"
            ),
            (
                "Scan left to right with a stack of decreasing values: a new value pops smaller ones (they become "
                "its left child) and becomes the right child of the stack top."
            ),
        ],
        pattern="Divide and conquer, optimised by a monotonic stack",
        explain=(
            "Recursing on the maximum costs O(n) per level. A monotonic decreasing stack builds the same tree in "
            "one pass: when x arrives, everything it pops is smaller and sits to its left, so the last popped node "
            "becomes x's left child; if a larger element remains on the stack, x becomes that element's right child."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time worst case - rescan for the maximum in every segment",
        brute=r"""
# BRUTE FORCE: O(n^2) time worst case - rescan for the maximum in every segment
def construct_maximum_binary_tree(nums):
    if not nums:
        return None
    i = nums.index(max(nums))
    root = TreeNode(nums[i])
    root.left = construct_maximum_binary_tree(nums[:i])
    root.right = construct_maximum_binary_tree(nums[i + 1 :])
    return root
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Divide and conquer, optimised by a monotonic stack
def construct_maximum_binary_tree(nums):
    stack = []

    for x in nums:
        node = TreeNode(x)
        last = None

        while stack and stack[-1].val < x:
            last = stack.pop()

        node.left = last

        if stack:
            stack[-1].right = node

        stack.append(node)

    return stack[0] if stack else None
""",
    ),
    # ---- Super Pow (LeetCode 372) ----
    dict(
        title="Super Pow",
        diff="M",
        lc=372,
        slug="super-pow",
        prompt=(
            "Compute a^b mod 1337 where b is a huge non-negative integer given as a list of its decimal digits "
            "(most significant first)."
        ),
        sig="def super_pow(a: int, b: List[int]) -> int:",
        fn="super_pow",
        tests=[
            ((2, [3]), 8),
            ((2, [1, 0]), 1024),
            ((1, [4, 3, 3, 8, 5, 2]), 1),
            ((2147483647, [2, 0, 0]), 1198),
        ],
        hints=[
            "You cannot turn b into an integer exponent loop: it may have thousands of digits.",
            "a^(10*q + d) = (a^q)^10 * a^d.",
            (
                "Process the digits left to right: result = result^10 * a^digit (mod 1337), using fast "
                "exponentiation for each power."
            ),
        ],
        pattern="Divide and conquer on the exponent (square/ten-fold per digit)",
        explain=(
            "Writing b = 10*q + d with d the last digit gives a^b = (a^q)^10 * a^d. So the answer for the digit "
            "prefix is the answer for the shorter prefix raised to the tenth power times a^d, all mod 1337. Each "
            "digit costs O(log 10) multiplications, so the work is linear in the number of digits."
        ),
        cx="O(len(b)) time, O(1) space",
        brute_cx="O(a^b) size - build the full integer power, then take the remainder",
        brute=r"""
# BRUTE FORCE: O(a^b) size - build the full integer power, then take the remainder
def super_pow(a, b):
    exponent = int("".join(map(str, b)))
    return a**exponent % 1337
""",
        solution=r"""
# OPTIMISED: O(len(b)) time, O(1) space
# Idea: Divide and conquer on the exponent (square/ten-fold per digit)
def super_pow(a, b):
    mod = 1337

    def power(base, exp):
        base %= mod
        out = 1

        while exp:
            if exp & 1:
                out = out * base % mod
            base = base * base % mod
            exp >>= 1

        return out

    result = 1

    for digit in b:
        result = power(result, 10) * power(a, digit) % mod

    return result
""",
    ),
    # ---- Number of Pairs Satisfying Inequality (LeetCode 2426) ----
    dict(
        title="Number of Pairs Satisfying Inequality",
        diff="H",
        lc=2426,
        slug="number-of-pairs-satisfying-inequality",
        prompt="Count pairs i < j with nums1[i] - nums1[j] <= nums2[i] - nums2[j] + diff.",
        sig="def number_of_pairs(nums1: List[int], nums2: List[int], diff: int) -> int:",
        fn="number_of_pairs",
        tests=[
            (([3, 2, 5], [2, 2, 1], 1), 3),
            (([3, -1], [-2, 2], -1), 0),
            (([1, 1], [1, 1], 0), 1),
            (([0, 0, 0], [0, 0, 0], -1), 0),
        ],
        hints=[
            "Move everything with index i to one side: (nums1[i] - nums2[i]) <= (nums1[j] - nums2[j]) + diff.",
            "Let d[i] = nums1[i] - nums2[i]. Count pairs i < j with d[i] <= d[j] + diff - an inversion-style count.",
            (
                "Merge sort d: when both halves are sorted, a pointer over the left half counts how many d[i] <= "
                "d[j] + diff for each right element, in linear time."
            ),
        ],
        pattern="Merge sort counting of cross pairs (inversion-count family)",
        explain=(
            "After substituting d[i] = nums1[i] - nums2[i] the condition is d[i] <= d[j] + diff for i < j. "
            "Splitting by index keeps the 'i before j' requirement: pairs fully inside a half are handled "
            "recursively, pairs across the halves have i in the left and j in the right. With both halves sorted, "
            "as d[j] increases the allowed left prefix only grows, so one moving pointer counts them all."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2) time - test every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every pair
def number_of_pairs(nums1, nums2, diff):
    count = 0
    for i in range(len(nums1)):
        for j in range(i + 1, len(nums1)):
            if nums1[i] - nums1[j] <= nums2[i] - nums2[j] + diff:
                count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Merge sort counting of cross pairs (inversion-count family)
def number_of_pairs(nums1, nums2, diff):
    d = [a - b for a, b in zip(nums1, nums2)]

    def sort_and_count(arr):
        if len(arr) <= 1:
            return arr, 0

        mid = len(arr) // 2
        left, x = sort_and_count(arr[:mid])
        right, y = sort_and_count(arr[mid:])
        count = x + y
        p = 0

        for value in right:
            while p < len(left) and left[p] <= value + diff:
                p += 1
            count += p

        return sorted(left + right), count

    return sort_and_count(d)[1]
""",
    ),
    # ---- Create Sorted Array through Instructions (LeetCode 1649) ----
    dict(
        title="Create Sorted Array through Instructions",
        diff="H",
        lc=1649,
        slug="create-sorted-array-through-instructions",
        prompt=(
            "Insert the numbers of instructions one by one into a sorted array. The cost of inserting x is "
            "min(count of existing elements strictly less than x, count strictly greater than x). Return the total "
            "cost modulo 1_000_000_007."
        ),
        sig="def create_sorted_array(instructions: List[int]) -> int:",
        fn="create_sorted_array",
        tests=[
            (([1, 5, 6, 2],), 1),
            (([1, 2, 3, 6, 5, 4],), 3),
            (([1, 3, 3, 3, 2, 4, 2, 1, 2],), 4),
            (([1],), 0),
            (([2, 2, 2],), 0),
        ],
        hints=[
            (
                "For each x you need 'how many earlier values are < x' and '> x' - counting by scanning the earlier "
                "values is O(n^2)."
            ),
            (
                "That is a prefix count over values that changes as you insert: a Fenwick (binary indexed) tree "
                "answers and updates in O(log V)."
            ),
            "less = query(x - 1); greater = inserted_so_far - query(x); add min(less, greater), then add(x).",
        ],
        pattern="Counting with a Fenwick tree (online cousin of merge-sort counting)",
        explain=(
            "The cost needs, for each x, the number of already-inserted values below x and above x. A Fenwick tree "
            "over the value range stores counts so both prefix queries and the insertion update take O(log V); the "
            "number above x is total_inserted - (number <= x)."
        ),
        cx="O(n log V) time, O(V) space",
        brute_cx="O(n^2) time - scan all earlier values for every instruction",
        brute=r"""
# BRUTE FORCE: O(n^2) time - scan all earlier values for every instruction
def create_sorted_array(instructions):
    total = 0
    for i, x in enumerate(instructions):
        earlier = instructions[:i]
        less = sum(1 for y in earlier if y < x)
        greater = sum(1 for y in earlier if y > x)
        total += min(less, greater)
    return total % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n log V) time, O(V) space
# Idea: Counting with a Fenwick tree (online cousin of merge-sort counting)
def create_sorted_array(instructions):
    size = max(instructions) + 1
    tree = [0] * (size + 1)

    def add(i):
        while i <= size:
            tree[i] += 1
            i += i & -i

    def query(i):
        total = 0
        while i > 0:
            total += tree[i]
            i -= i & -i
        return total

    cost = 0

    for done, x in enumerate(instructions):
        less = query(x - 1)
        greater = done - query(x)
        cost += min(less, greater)
        add(x)

    return cost % (10**9 + 7)
""",
    ),
    # ---- Number of Ways to Reorder Array to Get Same BST (LeetCode 1569) ----
    dict(
        title="Number of Ways to Reorder Array to Get Same BST",
        diff="H",
        lc=1569,
        slug="number-of-ways-to-reorder-array-to-get-same-bst",
        prompt=(
            "nums is a permutation of 1..n inserted one by one into an empty BST. Count the other orderings of nums "
            "that produce exactly the same BST. Return the count modulo 1_000_000_007."
        ),
        sig="def num_of_ways(nums: List[int]) -> int:",
        fn="num_of_ways",
        tests=[
            (([2, 1, 3],), 1),
            (([3, 4, 5, 1, 2],), 5),
            (([1, 2, 3],), 0),
            (([3, 1, 2, 5, 4, 6],), 19),
            (([1],), 0),
        ],
        hints=[
            "The first element is the root; smaller values go to its left subtree, larger to its right.",
            (
                "Any ordering works as long as the left values keep their relative order, the right values keep "
                "theirs, and the root comes first. The two groups can be interleaved freely."
            ),
            (
                "ways(arr) = C(len(left) + len(right), len(left)) * ways(left) * ways(right); the answer is "
                "ways(nums) - 1 (do not count the original)."
            ),
        ],
        pattern="Divide and conquer with binomial interleavings",
        explain=(
            "A BST is fixed once each subtree is fixed. The orderings that give it are the ways to merge an "
            "ordering of the left subtree with an ordering of the right subtree after the root: choose which "
            "positions of the remaining len(left)+len(right) slots go to the left group, C(total, len(left)), then "
            "multiply by the ways inside each group. Subtract 1 for the original order."
        ),
        cx="O(n^2) time (list splits), O(n) recursion depth",
        brute_cx="O(n! * n) time - try every ordering and compare tree shapes",
        brute=r"""
# BRUTE FORCE: O(n! * n) time - try every ordering and compare tree shapes
def num_of_ways(nums):
    def shape(order):
        root = None

        for x in order:
            if root is None:
                root = [x, None, None]
                continue

            node = root

            while True:
                side = 1 if x < node[0] else 2
                if node[side] is None:
                    node[side] = [x, None, None]
                    break
                node = node[side]

        def freeze(node):
            return None if node is None else (node[0], freeze(node[1]), freeze(node[2]))

        return freeze(root)

    target = shape(nums)
    same = sum(1 for perm in itertools.permutations(nums) if shape(perm) == target)

    return (same - 1) % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n^2) time (list splits), O(n) recursion depth
# Idea: Divide and conquer with binomial interleavings
def num_of_ways(nums):
    mod = 10**9 + 7

    def ways(arr):
        if len(arr) <= 2:
            return 1
        left = [x for x in arr if x < arr[0]]
        right = [x for x in arr if x > arr[0]]
        return math.comb(len(left) + len(right), len(left)) * ways(left) % mod * ways(right) % mod

    return (ways(nums) - 1) % mod
""",
    ),
    # ---- Count Good Numbers (LeetCode 1922) ----
    dict(
        title="Count Good Numbers",
        diff="M",
        lc=1922,
        slug="count-good-numbers",
        prompt=(
            "A digit string of length n is good if digits at even indices (0-based) are even and digits at odd "
            "indices are prime (2, 3, 5, 7). Return how many good strings of length n exist, modulo 1_000_000_007."
        ),
        sig="def count_good_numbers(n: int) -> int:",
        fn="count_good_numbers",
        tests=[
            ((1,), 5),
            ((4,), 400),
            ((50,), 564908303),
            ((2,), 20),
            ((3,), 100),
        ],
        hints=[
            "Even positions have 5 choices (0,2,4,6,8); odd positions have 4 choices (2,3,5,7).",
            "The count is 5^(number of even positions) * 4^(number of odd positions).",
            "n can be 10^15: compute the powers by repeated squaring (divide and conquer on the exponent).",
        ],
        pattern="Fast exponentiation (halve the exponent)",
        explain=(
            "Positions are independent, so the answer is a product: 5 for each even index, 4 for each odd index, "
            "i.e. 5^ceil(n/2) * 4^floor(n/2). Multiplying n times is far too slow for n = 10^15, but x^e can be "
            "computed with O(log e) multiplications because x^e = (x^(e/2))^2 (times x when e is odd)."
        ),
        cx="O(log n) time, O(1) space",
        brute_cx="O(n) time - multiply the choice count position by position",
        brute=r"""
# BRUTE FORCE: O(n) time - multiply the choice count position by position
def count_good_numbers(n):
    result = 1
    for i in range(n):
        result = result * (5 if i % 2 == 0 else 4) % (10**9 + 7)
    return result
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Fast exponentiation (halve the exponent)
def count_good_numbers(n):
    mod = 10**9 + 7

    def power(base, exp):
        out = 1
        while exp:
            if exp & 1:
                out = out * base % mod
            base = base * base % mod
            exp >>= 1
        return out

    return power(5, (n + 1) // 2) * power(4, n // 2) % mod
""",
    ),
]
