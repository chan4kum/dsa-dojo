from core import *


def _lps_ok(args, got):
    s = args[0]
    best = max((j - i for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1]), default=0)
    return isinstance(got, str) and got in s and got == got[::-1] and len(got) == best


PROBLEMS = [
    dict(
        title="Min Cost Climbing Stairs", diff="E", lc=746, slug="min-cost-climbing-stairs",
        prompt="cost[i] is paid when you step on stair i; you may then climb 1 or 2 stairs. You can start at stair 0 or 1. Return the minimum cost to reach the top (one past the last stair).",
        sig="def min_cost_climbing_stairs(cost: List[int]) -> int:", fn="min_cost_climbing_stairs",
        tests=[(([10, 15, 20],), 15), (([1, 100, 1, 1, 1, 100, 1, 1, 100, 1],), 6), (([0, 0],), 0), (([5, 3],), 3)],
        hints=["Define f(i) = min cost to arrive at position i. How can you arrive at i?",
               "From i-1 (paying cost[i-1]) or from i-2 (paying cost[i-2]).",
               "f(i) = min(f(i-1) + cost[i-1], f(i-2) + cost[i-2]), f(0) = f(1) = 0. Only the last two values matter."],
        pattern="1-D DP: state = position, transition = last 1 or 2 steps",
        explain="""
        This is Climbing Stairs with weights. Recognise it by 'minimum/maximum/count ways to reach i from smaller
        indices with a fixed set of moves'. Space optimisation: keep two variables.""",
        cx="O(n) time, O(1) space", brute_cx="O(2^n) time - plain recursion",
        brute=r'''
def min_cost_climbing_stairs(cost):
    n = len(cost)
    def f(i):
        if i <= 1:
            return 0
        return min(f(i - 1) + cost[i - 1], f(i - 2) + cost[i - 2])
    return f(n)
''',
        solution=r'''
def min_cost_climbing_stairs(cost):
    a = b = 0                      # f(i-2), f(i-1)
    for i in range(2, len(cost) + 1):
        a, b = b, min(b + cost[i - 1], a + cost[i - 2])
    return b
''',
    ),
    dict(
        title="House Robber II", diff="M", lc=213, slug="house-robber-ii",
        prompt="Houses are arranged in a circle (first and last are neighbours). You cannot rob two adjacent houses. Return the maximum amount.",
        sig="def rob(nums: List[int]) -> int:", fn="rob",
        tests=[(([2, 3, 2],), 3), (([1, 2, 3, 1],), 4), (([1],), 1), (([1, 2],), 2), (([5, 1, 1, 5],), 6), (([200, 3, 140, 20, 10],), 340)],
        hints=["The circle creates a conflict only between the first and last houses.",
               "Break it into two LINEAR problems.",
               "answer = max(rob_line(nums[:-1]), rob_line(nums[1:])) using the House Robber I recurrence."],
        pattern="Reduce a circular structure to two linear cases",
        explain="""
        Either house 0 is excluded or the last house is excluded (maybe both). Solving both linear halves covers every
        legal choice. Edge case: a single house.""",
        cx="O(n) time, O(1) space", brute_cx="O(2^n) time - try take/skip for each house with the circular constraint",
        brute=r'''
def rob(nums):
    n = len(nums)
    if n == 1:
        return nums[0]
    def go(i, took_first):
        if i >= n:
            return 0
        best = go(i + 1, took_first)
        if not (i == n - 1 and took_first):
            best = max(best, nums[i] + go(i + 2, took_first or i == 0))
        return best
    return go(0, False)
''',
        solution=r'''
def rob(nums):
    def line(a):
        prev = cur = 0
        for x in a:
            prev, cur = cur, max(cur, prev + x)
        return cur
    if len(nums) == 1:
        return nums[0]
    return max(line(nums[:-1]), line(nums[1:]))
''',
    ),
    dict(
        title="Unique Paths", diff="M", lc=62, slug="unique-paths",
        prompt="A robot starts at the top-left of an m x n grid and can only move right or down. Count the paths to the bottom-right.",
        sig="def unique_paths(m: int, n: int) -> int:", fn="unique_paths",
        tests=[((3, 7), 28), ((3, 2), 3), ((1, 1), 1), ((7, 3), 28), ((1, 5), 1), ((10, 10), 48620)],
        hints=["To reach a cell you must come from above or from the left.",
               "paths(r, c) = paths(r-1, c) + paths(r, c-1); the first row and column are all 1.",
               "Keep only one row of the table. (Closed form: C(m+n-2, m-1).)"],
        pattern="2-D grid DP (count paths = sum of the two predecessors)",
        explain="""
        Each path is a sequence of (m-1) downs and (n-1) rights, so the count is also a binomial coefficient - a nice
        way to verify the DP. The row-rolling trick reduces space from O(mn) to O(n).""",
        cx="O(m*n) time, O(n) space (or O(min(m,n)) with the formula)", brute_cx="O(2^(m+n)) time - recursion without memo",
        brute=r'''
def unique_paths(m, n):
    def go(r, c):
        if r == 0 or c == 0:
            return 1
        return go(r - 1, c) + go(r, c - 1)
    return go(m - 1, n - 1)
''',
        solution=r'''
def unique_paths(m, n):
    row = [1] * n
    for _ in range(1, m):
        for c in range(1, n):
            row[c] += row[c - 1]
    return row[-1]
''',
    ),
    dict(
        title="Minimum Path Sum", diff="M", lc=64, slug="minimum-path-sum",
        prompt="Grid of non-negative numbers. Moving only right or down from the top-left to the bottom-right, return the minimum sum of the cells on the path.",
        sig="def min_path_sum(grid: List[List[int]]) -> int:", fn="min_path_sum",
        tests=[(([[1, 3, 1], [1, 5, 1], [4, 2, 1]],), 7), (([[1, 2, 3], [4, 5, 6]],), 12), (([[5]],), 5), (([[1, 2], [1, 1]],), 3)],
        hints=["Same shape as Unique Paths, but minimise a cost instead of counting.",
               "best(r,c) = grid[r][c] + min(best(r-1,c), best(r,c-1)).",
               "Handle the first row and column (only one predecessor). Can be done in place."],
        pattern="2-D grid DP (min over predecessors)",
        explain="""
        Replace '+' of counts by 'min' of costs: the DP skeleton is identical. Recognise the family: grid + two moves.""",
        cx="O(m*n) time, O(n) space", brute_cx="O(2^(m+n)) time - recursion without memo",
        brute=r'''
def min_path_sum(grid):
    R, C = len(grid), len(grid[0])
    def go(r, c):
        if r == R - 1 and c == C - 1:
            return grid[r][c]
        best = float("inf")
        if r + 1 < R:
            best = min(best, go(r + 1, c))
        if c + 1 < C:
            best = min(best, go(r, c + 1))
        return grid[r][c] + best
    return go(0, 0)
''',
        solution=r'''
def min_path_sum(grid):
    R, C = len(grid), len(grid[0])
    dp = [float("inf")] * C
    dp[0] = 0
    for r in range(R):
        for c in range(C):
            best_prev = dp[c] if c == 0 else min(dp[c], dp[c - 1])
            dp[c] = grid[r][c] + best_prev
    return dp[-1]
''',
    ),
    dict(
        title="Longest Palindromic Substring", diff="M", lc=5, slug="longest-palindromic-substring",
        prompt="Return the longest palindromic substring of s (if several have the same length, any one is accepted).",
        sig="def longest_palindrome(s: str) -> str:", fn="longest_palindrome", check=_lps_ok,
        tests=[(("babad",), "bab"), (("cbbd",), "bb"), (("a",), "a"), (("ac",), "a"), (("racecar",), "racecar"), (("forgeeksskeegfor",), "geeksskeeg")],
        hints=["Every palindrome mirrors around a centre. How many centres are there?",
               "2n - 1 centres: n characters (odd length) and n-1 gaps (even length).",
               "Expand outward from each centre while the two ends match; track the longest. O(n^2) time, O(1) space."],
        pattern="Expand around the centre",
        explain="""
        Checking all O(n^2) substrings at O(n) each is O(n^3). Mirroring means a palindrome is determined by its
        centre, so expansion is O(n) per centre. (Manacher's algorithm is O(n) but rarely required.)""",
        cx="O(n^2) time, O(1) space", brute_cx="O(n^3) time - test every substring",
        brute=r'''
def longest_palindrome(s):
    best = ""
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            if s[i:j] == s[i:j][::-1] and j - i > len(best):
                best = s[i:j]
    return best
''',
        solution=r'''
def longest_palindrome(s):
    best = ""
    def expand(l, r):
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l, r = l - 1, r + 1
        return s[l + 1:r]
    for i in range(len(s)):
        for cand in (expand(i, i), expand(i, i + 1)):
            if len(cand) > len(best):
                best = cand
    return best
''',
    ),
    dict(
        title="Palindromic Substrings", diff="M", lc=647, slug="palindromic-substrings",
        prompt="Count how many substrings of s are palindromes (substrings at different positions count separately).",
        sig="def count_substrings(s: str) -> int:", fn="count_substrings",
        tests=[(("abc",), 3), (("aaa",), 6), (("a",), 1), (("abba",), 6), (("",), 0)],
        hints=["Same mirror idea as the longest palindromic substring.",
               "Each successful expansion step from a centre is one more palindrome.",
               "For each of the 2n-1 centres, expand while ends match and count +1 per step."],
        pattern="Expand around the centre (count instead of maximise)",
        explain="""
        Counting is easier than locating: every expansion that still matches is one new palindromic substring.""",
        cx="O(n^2) time, O(1) space", brute_cx="O(n^3) time - test every substring",
        brute=r'''
def count_substrings(s):
    return sum(1 for i in range(len(s)) for j in range(i + 1, len(s) + 1) if s[i:j] == s[i:j][::-1])
''',
        solution=r'''
def count_substrings(s):
    total = 0
    for c in range(2 * len(s) - 1):
        l, r = c // 2, c // 2 + c % 2
        while l >= 0 and r < len(s) and s[l] == s[r]:
            total += 1
            l, r = l - 1, r + 1
    return total
''',
    ),
    dict(
        title="Decode Ways", diff="M", lc=91, slug="decode-ways",
        prompt="'A'=1, 'B'=2, ..., 'Z'=26. Count the ways to decode a digit string (0 if it cannot be decoded).",
        sig="def num_decodings(s: str) -> int:", fn="num_decodings",
        tests=[(("12",), 2), (("226",), 3), (("06",), 0), (("0",), 0), (("10",), 1), (("2101",), 1), (("11106",), 2), (("27",), 1)],
        hints=["Look at the LAST one or two digits of the prefix.",
               "A single digit 1-9 is valid; a pair 10-26 is valid.",
               "dp[i] = (dp[i-1] if s[i-1] != '0') + (dp[i-2] if 10 <= int(s[i-2:i]) <= 26). dp[0] = 1."],
        pattern="1-D DP: count ways with 1- and 2-step transitions plus validity",
        explain="""
        It is Climbing Stairs where each step is allowed only if the digits form a valid code. A '0' can only be the
        second digit of 10 or 20, which is handled automatically by the validity checks.""",
        cx="O(n) time, O(1) space", brute_cx="O(2^n) time - recursion trying 1 or 2 digits",
        brute=r'''
def num_decodings(s):
    def go(i):
        if i == len(s):
            return 1
        if s[i] == "0":
            return 0
        total = go(i + 1)
        if i + 1 < len(s) and 10 <= int(s[i:i + 2]) <= 26:
            total += go(i + 2)
        return total
    return go(0)
''',
        solution=r'''
def num_decodings(s):
    if not s:
        return 0
    a, b = 1, (1 if s[0] != "0" else 0)     # a = dp[i-2] (dp[0] = 1), b = dp[i-1] (dp[1])
    for i in range(2, len(s) + 1):
        cur = 0
        if s[i - 1] != "0":
            cur += b
        if 10 <= int(s[i - 2:i]) <= 26:
            cur += a
        a, b = b, cur
    return b
''',
    ),
    dict(
        title="Perfect Squares", diff="M", lc=279, slug="perfect-squares",
        prompt="Return the least number of perfect squares (1, 4, 9, 16, ...) that sum to n.",
        sig="def num_squares(n: int) -> int:", fn="num_squares",
        tests=[((12,), 3), ((13,), 2), ((1,), 1), ((43,), 3), ((100,), 1), ((7,), 4)],
        hints=["This is Coin Change where the coins are the perfect squares.",
               "dp[x] = 1 + min(dp[x - s*s]) over all squares s*s <= x.",
               "Build dp[0..n] bottom-up with dp[0] = 0."],
        pattern="Unbounded knapsack / coin change (min coins)",
        explain="""
        Same DP as Coin Change. Spot the disguise: 'fewest numbers from a fixed set that sum to a target'.""",
        cx="O(n sqrt n) time, O(n) space", brute_cx="exponential - recursion without memo",
        brute=r'''
def num_squares(n):
    def go(x):
        if x == 0:
            return 0
        best, s = float("inf"), 1
        while s * s <= x:
            best = min(best, 1 + go(x - s * s))
            s += 1
        return best
    return go(n)
''',
        solution=r'''
def num_squares(n):
    dp = [0] + [float("inf")] * n
    for x in range(1, n + 1):
        s = 1
        while s * s <= x:
            dp[x] = min(dp[x], dp[x - s * s] + 1)
            s += 1
    return dp[n]
''',
    ),
    dict(
        title="Combination Sum IV", diff="M", lc=377, slug="combination-sum-iv",
        prompt="Count the sequences (order matters) of numbers from nums (reuse allowed) that add up to target.",
        sig="def combination_sum4(nums: List[int], target: int) -> int:", fn="combination_sum4",
        tests=[(([1, 2, 3], 4), 7), (([9], 3), 0), (([1, 2], 5), 8), (([4], 4), 1), (([2, 1, 3], 10), 274)],
        hints=["Order matters, so (1,2) and (2,1) are different.",
               "Think of the LAST number placed: ways(t) = sum of ways(t - x) over x in nums.",
               "dp[0] = 1; loop the TARGET on the outside and nums on the inside (that order counts permutations)."],
        pattern="Counting DP - loop order decides combinations vs permutations",
        explain="""
        Outer loop over amounts, inner over coins counts ordered sequences (permutations). Swapping the loops - coins
        outside - counts unordered combinations (Coin Change II). A classic interview trap.""",
        cx="O(target * len(nums)) time", brute_cx="exponential - recursion without memo",
        brute=r'''
def combination_sum4(nums, target):
    def go(t):
        if t == 0:
            return 1
        return sum(go(t - x) for x in nums if x <= t)
    return go(target)
''',
        solution=r'''
def combination_sum4(nums, target):
    dp = [1] + [0] * target
    for t in range(1, target + 1):
        for x in nums:
            if x <= t:
                dp[t] += dp[t - x]
    return dp[target]
''',
    ),
    dict(
        title="Target Sum", diff="M", lc=494, slug="target-sum",
        prompt="Put a + or - in front of every number of nums. Count the assignments whose total equals target.",
        sig="def find_target_sum_ways(nums: List[int], target: int) -> int:", fn="find_target_sum_ways",
        tests=[(([1, 1, 1, 1, 1], 3), 5), (([1], 1), 1), (([1, 0], 1), 2), (([1, 2, 3], 7), 0), (([2, 3, 5], 0), 2)],
        hints=["2^n assignments is too many for large n. Let P = sum of numbers with '+', N = sum with '-'.",
               "P - N = target and P + N = total, so P = (total + target) / 2.",
               "Count subsets of nums that sum to (total + target) / 2 - a 0/1 knapsack counting DP (return 0 if the value is negative or not an integer)."],
        pattern="Reduce to 'count subsets with sum S' (0/1 knapsack)",
        explain="""
        Algebra turns signs into a subset choice. Iterate the capacity backwards so each number is used at most once.""",
        cx="O(n * S) time, O(S) space", brute_cx="O(2^n) time - try both signs for every number",
        brute=r'''
def find_target_sum_ways(nums, target):
    def go(i, total):
        if i == len(nums):
            return 1 if total == target else 0
        return go(i + 1, total + nums[i]) + go(i + 1, total - nums[i])
    return go(0, 0)
''',
        solution=r'''
def find_target_sum_ways(nums, target):
    total = sum(nums)
    if abs(target) > total or (total + target) % 2:
        return 0
    s = (total + target) // 2
    dp = [1] + [0] * s
    for x in nums:
        for c in range(s, x - 1, -1):
            dp[c] += dp[c - x]
    return dp[s]
''',
    ),
    dict(
        title="Best Time to Buy and Sell Stock with Cooldown", diff="M", lc=309, slug="best-time-to-buy-and-sell-stock-with-cooldown",
        prompt="Unlimited transactions, but after selling you must wait one day before buying again. Return the maximum profit.",
        sig="def max_profit(prices: List[int]) -> int:", fn="max_profit",
        tests=[(([1, 2, 3, 0, 2],), 3), (([1],), 0), (([2, 1],), 0), (([1, 2, 4],), 3), (([6, 1, 3, 2, 4, 7],), 6)],
        hints=["What are the possible 'states' at the end of a day?",
               "holding a stock / not holding and free to buy / not holding and in cooldown.",
               "hold = max(hold, free - p); sold = hold_prev + p; free = max(free, cooldown_prev). Update all from the previous day's values."],
        pattern="State-machine DP (a few states, transitions per day)",
        explain="""
        Draw the states as circles and the allowed moves as arrows (buy, sell, rest). The DP is just 'best profit to be
        in state S after day i'. This pattern extends to 'at most k transactions' and 'transaction fee'.""",
        cx="O(n) time, O(1) space", brute_cx="O(3^n) time - recursion over buy/sell/skip with cooldown",
        brute=r'''
def max_profit(prices):
    n = len(prices)
    def go(i, holding):
        if i >= n:
            return 0
        skip = go(i + 1, holding)
        if holding:
            return max(skip, prices[i] + go(i + 2, False))   # sell, then cooldown day
        return max(skip, -prices[i] + go(i + 1, True))
    return go(0, False)
''',
        solution=r'''
def max_profit(prices):
    hold, sold, free = float("-inf"), 0, 0
    for p in prices:
        prev_sold = sold
        sold = hold + p
        hold = max(hold, free - p)
        free = max(free, prev_sold)
    return max(sold, free)
''',
    ),
    dict(
        title="Triangle", diff="M", lc=120, slug="triangle",
        prompt="Given a triangle of numbers, return the minimum path sum from top to bottom, moving each step to an adjacent number on the row below (index i or i+1).",
        sig="def minimum_total(triangle: List[List[int]]) -> int:", fn="minimum_total",
        tests=[(([[2], [3, 4], [6, 5, 7], [4, 1, 8, 3]],), 11), (([[-10]],), -10), (([[1], [2, 3]],), 3), (([[1], [-5, 3], [4, 4, -1]],), 0)],
        hints=["Top-down needs to remember too many options. What if you work from the bottom?",
               "The best path from a cell = its value + min of the best paths from the two cells below.",
               "Start with the last row as dp and fold upward in place: dp[i] = row[i] + min(dp[i], dp[i+1])."],
        pattern="Bottom-up DP with a rolling 1-D array",
        explain="""
        Going bottom-up makes every subproblem 'best path from here to the bottom', which has a clean recurrence and
        needs only O(n) extra space.""",
        cx="O(n^2) time, O(n) space", brute_cx="O(2^n) time - recursion over left/right choices",
        brute=r'''
def minimum_total(triangle):
    def go(r, i):
        if r == len(triangle) - 1:
            return triangle[r][i]
        return triangle[r][i] + min(go(r + 1, i), go(r + 1, i + 1))
    return go(0, 0)
''',
        solution=r'''
def minimum_total(triangle):
    dp = triangle[-1][:]
    for r in range(len(triangle) - 2, -1, -1):
        for i in range(len(triangle[r])):
            dp[i] = triangle[r][i] + min(dp[i], dp[i + 1])
    return dp[0]
''',
    ),
    dict(
        title="Longest Palindromic Subsequence", diff="M", lc=516, slug="longest-palindromic-subsequence",
        prompt="Return the length of the longest palindromic SUBSEQUENCE of s (characters need not be contiguous).",
        sig="def longest_palindrome_subseq(s: str) -> int:", fn="longest_palindrome_subseq",
        tests=[(("bbbab",), 4), (("cbbd",), 2), (("a",), 1), (("abcde",), 1), (("agbdba",), 5)],
        hints=["Relate it to a problem you know: a palindrome reads the same reversed.",
               "LPS(s) = LCS(s, reverse(s)).",
               "Or directly: dp[i][j] = dp[i+1][j-1] + 2 if s[i] == s[j], else max(dp[i+1][j], dp[i][j-1])."],
        pattern="Interval DP / reduce to LCS with the reversed string",
        explain="""
        Reducing a new problem to a known one (LCS) is a core interview skill. The interval DP is worth knowing because
        it generalises to Burst Balloons and Palindrome Partitioning II.""",
        cx="O(n^2) time and space", brute_cx="O(2^n) time - recursion on (i, j)",
        brute=r'''
def longest_palindrome_subseq(s):
    def go(i, j):
        if i > j:
            return 0
        if i == j:
            return 1
        if s[i] == s[j]:
            return 2 + go(i + 1, j - 1)
        return max(go(i + 1, j), go(i, j - 1))
    return go(0, len(s) - 1)
''',
        solution=r'''
def longest_palindrome_subseq(s):
    n = len(s)
    dp = [[0] * n for _ in range(n)]
    for i in range(n - 1, -1, -1):
        dp[i][i] = 1
        for j in range(i + 1, n):
            if s[i] == s[j]:
                dp[i][j] = dp[i + 1][j - 1] + 2
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j - 1])
    return dp[0][n - 1] if n else 0
''',
    ),
    dict(
        title="Regular Expression Matching", diff="H", lc=10, slug="regular-expression-matching",
        prompt="Implement matching of the whole string s against pattern p where '.' matches any single character and 'x*' matches zero or more of the preceding element x.",
        sig="def is_match(s: str, p: str) -> bool:", fn="is_match",
        tests=[(("aa", "a"), False), (("aa", "a*"), True), (("ab", ".*"), True), (("aab", "c*a*b"), True), (("mississippi", "mis*is*p*."), False), (("", "a*"), True), (("", ""), True), (("abc", "abc"), True)],
        hints=["Think about the first characters of s and p. When does a '*' matter?",
               "If p[1] == '*': either skip the 'x*' entirely (zero copies) or, if the first characters match, consume one char of s and keep the same pattern.",
               "match(i, j) with memoisation on (i, j) turns the exponential recursion into O(m*n)."],
        pattern="2-D DP on two string positions (with branching for '*')",
        explain="""
        The star produces two choices (use zero copies / use one more copy), which is why plain recursion is
        exponential; the state (i, j) has only m*n distinct values, so caching them makes it polynomial.""",
        cx="O(m*n) time and space", brute_cx="exponential - plain recursion",
        brute=r'''
def is_match(s, p):
    def go(i, j):
        if j == len(p):
            return i == len(s)
        first = i < len(s) and p[j] in (s[i], ".")
        if j + 1 < len(p) and p[j + 1] == "*":
            return go(i, j + 2) or (first and go(i + 1, j))
        return first and go(i + 1, j + 1)
    return go(0, 0)
''',
        solution=r'''
def is_match(s, p):
    @lru_cache(maxsize=None)
    def go(i, j):
        if j == len(p):
            return i == len(s)
        first = i < len(s) and p[j] in (s[i], ".")
        if j + 1 < len(p) and p[j + 1] == "*":
            return go(i, j + 2) or (first and go(i + 1, j))
        return first and go(i + 1, j + 1)
    return go(0, 0)
''',
    ),
    dict(
        title="Coin Change II", diff="M", lc=518, slug="coin-change-ii",
        prompt="Count the number of COMBINATIONS (order does not matter) of coins that make up amount; unlimited supply of each coin. Return 0 if impossible.",
        sig="def change(amount: int, coins: List[int]) -> int:", fn="change",
        tests=[((5, [1, 2, 5]), 4), ((3, [2]), 0), ((10, [10]), 1), ((0, [7]), 1), ((11, [1, 5, 10]), 4)],
        hints=["Counting sequences would count 1+2 and 2+1 separately. How do you avoid that?",
               "Decide coin types one at a time: for each coin, how many copies do you use?",
               "dp[0] = 1. For each coin (OUTER loop), for a from coin..amount: dp[a] += dp[a - coin]. Coins outside = combinations; amounts outside = permutations (Combination Sum IV)."],
        pattern="Unbounded knapsack - counting combinations (coin loop outside)",
        explain="""
        Processing one coin type at a time fixes an order of coin types, so each multiset of coins is generated exactly
        once. Compare with Combination Sum IV, where swapping the loops counts ordered sequences.""",
        cx="O(amount * coins) time, O(amount) space", brute_cx="exponential - recursion over (coin index, remaining) without memo",
        brute='''
def change(amount, coins):
    def go(i, rem):
        if rem == 0:
            return 1
        if i == len(coins) or rem < 0:
            return 0
        return go(i, rem - coins[i]) + go(i + 1, rem)
    return go(0, amount)
''',
        solution='''
def change(amount, coins):
    dp = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            dp[a] += dp[a - c]
    return dp[amount]
''',
    ),
]
