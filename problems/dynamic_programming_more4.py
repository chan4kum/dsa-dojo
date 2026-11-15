"""more Dynamic Programming problems (batch 5) - part of the problem bank for the "dynamic_programming" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Fibonacci Number (LeetCode 509) ----
    dict(
        title="Fibonacci Number",
        diff="E",
        lc=509,
        slug="fibonacci-number",
        prompt="F(0) = 0, F(1) = 1 and F(n) = F(n-1) + F(n-2). Return F(n).",
        sig="def fib(n: int) -> int:",
        fn="fib",
        tests=[
            ((0,), 0),
            ((1,), 1),
            ((2,), 1),
            ((4,), 3),
            ((10,), 55),
            ((30,), 832040),
        ],
        hints=[
            "The recursive definition recomputes the same values again and again.",
            "Each value depends only on the previous two.",
            "Loop upwards keeping just two variables: a, b = b, a + b.",
        ],
        pattern="Bottom-up DP with O(1) space (the 'hello world' of DP)",
        explain=(
            "Plain recursion makes an exponential tree of calls with massive overlap. Remembering the last two "
            "values collapses it to n steps."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(2^n) time - plain recursion",
        brute=r"""
# BRUTE FORCE: O(2^n) time - plain recursion
def fib(n):
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Bottom-up DP with O(1) space (the 'hello world' of DP)
def fib(n):
    a, b = 0, 1  # F(0), F(1)
    for _ in range(n):
        a, b = b, a + b
    return a
""",
    ),
    # ---- N-th Tribonacci Number (LeetCode 1137) ----
    dict(
        title="N-th Tribonacci Number",
        diff="E",
        lc=1137,
        slug="n-th-tribonacci-number",
        prompt="T(0) = 0, T(1) = 1, T(2) = 1 and T(n) = T(n-1) + T(n-2) + T(n-3). Return T(n).",
        sig="def tribonacci(n: int) -> int:",
        fn="tribonacci",
        tests=[
            ((0,), 0),
            ((1,), 1),
            ((2,), 1),
            ((4,), 4),
            ((25,), 1389537),
        ],
        hints=[
            "Same idea as Fibonacci, but each value needs the previous THREE.",
            "Keep three variables and shift them along.",
            "a, b, c = b, c, a + b + c repeated n times; a is the answer.",
        ],
        pattern="Rolling-window DP (keep only the last k states)",
        explain=(
            "The window of required previous values has a fixed size, so the whole table collapses to a few variables."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(3^n) time - plain recursion",
        brute=r"""
# BRUTE FORCE: O(3^n) time - plain recursion
def tribonacci(n):
    if n == 0:
        return 0
    if n < 3:
        return 1
    return tribonacci(n - 1) + tribonacci(n - 2) + tribonacci(n - 3)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Rolling-window DP (keep only the last k states)
def tribonacci(n):
    a, b, c = 0, 1, 1  # T(0), T(1), T(2)
    for _ in range(n):
        a, b, c = b, c, a + b + c
    return a
""",
    ),
    # ---- Domino and Tromino Tiling (LeetCode 790) ----
    dict(
        title="Domino and Tromino Tiling",
        diff="M",
        lc=790,
        slug="domino-and-tromino-tiling",
        prompt=(
            "Tiles: a 2x1 domino (either way round) and an L-shaped tromino (any of 4 rotations). Return the number "
            "of ways to tile a 2 x n board completely, modulo 1_000_000_007."
        ),
        sig="def num_tilings(n: int) -> int:",
        fn="num_tilings",
        tests=[
            ((1,), 1),
            ((2,), 2),
            ((3,), 5),
            ((4,), 11),
            ((5,), 24),
        ],
        hints=[
            (
                "Look at how the leftmost column can be covered: one vertical domino, two horizontal dominoes, or a "
                "tromino pair."
            ),
            (
                "Trominoes force 'dangling' shapes that must be closed off by another tromino, creating chains of "
                "any length."
            ),
            "Working it out gives dp[n] = 2 * dp[n-1] + dp[n-3], with dp[0] = dp[1] = 1, dp[2] = 2.",
        ],
        pattern="Derive a linear recurrence from the boundary structure",
        explain=(
            "A tiling either ends with a vertical domino (dp[n-1]), two horizontal dominoes (dp[n-2]) or a tromino "
            "chain that begins and ends flat. Collecting the chain terms leads to 2*dp[n-1] + dp[n-3]."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(exponential) time - backtracking over the first empty cell",
        brute=r"""
# BRUTE FORCE: O(exponential) time - backtracking over the first empty cell
def num_tilings(n):
    filled = [[False] * n for _ in range(2)]

    def solve():
        for c in range(n):  # the first empty cell in column-major order
            for r in range(2):
                if not filled[r][c]:
                    return place(r, c)
        return 1  # board is full: one complete tiling

    def place(r, c):
        total = 0
        # horizontal domino and vertical domino
        shapes = []
        if c + 1 < n:
            shapes.append([(r, c), (r, c + 1)])
        if r == 0:
            shapes.append([(0, c), (1, c)])
        # the four trominoes inside the 2x2 block starting at column c: block minus one cell
        if c + 1 < n:
            block = [(0, c), (1, c), (0, c + 1), (1, c + 1)]
            for gap in block:
                cells = [x for x in block if x != gap]
                if (r, c) in cells:
                    shapes.append(cells)
        for cells in shapes:
            if all(not filled[a][b] for a, b in cells):
                for a, b in cells:
                    filled[a][b] = True
                total += solve()
                for a, b in cells:
                    filled[a][b] = False
        return total

    return solve() % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Derive a linear recurrence from the boundary structure
def num_tilings(n):
    mod = 10**9 + 7
    dp = [1, 1, 2]  # dp[0], dp[1], dp[2]
    for i in range(3, n + 1):
        dp.append((2 * dp[i - 1] + dp[i - 3]) % mod)
    return dp[n]
""",
    ),
    # ---- Partition Array for Maximum Sum (LeetCode 1043) ----
    dict(
        title="Partition Array for Maximum Sum",
        diff="M",
        lc=1043,
        slug="partition-array-for-maximum-sum",
        prompt=(
            "Partition arr into contiguous subarrays of length at most k. Each subarray's values are replaced by "
            "the maximum of that subarray. Return the largest possible sum of the resulting array."
        ),
        sig="def max_sum_after_partitioning(arr: List[int], k: int) -> int:",
        fn="max_sum_after_partitioning",
        tests=[
            (([1, 15, 7, 9, 2, 5, 10], 3), 84),
            (([1, 4, 1, 5, 7, 3, 6, 1, 9, 9, 3], 4), 83),
            (([1], 1), 1),
            (([3, 1, 2], 2), 8),
        ],
        hints=[
            "Decide how long the LAST block is (1..k).",
            "dp[i] = best sum for the first i elements.",
            (
                "dp[i] = max over length L in 1..k of dp[i - L] + L * (maximum of the last L elements). Update the "
                "maximum as L grows."
            ),
        ],
        pattern="Partition DP: choose the length of the last block",
        explain=(
            "Trying every allowed length for the final block and reusing the best result for the prefix turns the "
            "exponential split search into O(n*k)."
        ),
        cx="O(n * k) time, O(n) space",
        brute_cx="O(k^n) time - recursion over every split",
        brute=r"""
# BRUTE FORCE: O(k^n) time - recursion over every split
def max_sum_after_partitioning(arr, k):
    def best(start):  # best sum for arr[start:]
        if start == len(arr):
            return 0
        result, biggest = 0, 0
        for length in range(1, min(k, len(arr) - start) + 1):
            biggest = max(biggest, arr[start + length - 1])
            result = max(result, biggest * length + best(start + length))
        return result

    return best(0)
""",
        solution=r"""
# OPTIMISED: O(n * k) time, O(n) space
# Idea: Partition DP: choose the length of the last block
def max_sum_after_partitioning(arr, k):
    n = len(arr)
    dp = [0] * (n + 1)  # dp[i] = best sum for arr[:i]
    for i in range(1, n + 1):
        biggest = 0
        for length in range(1, min(k, i) + 1):
            biggest = max(biggest, arr[i - length])  # the last block is arr[i-length:i]
            dp[i] = max(dp[i], dp[i - length] + biggest * length)
    return dp[n]
""",
    ),
    # ---- Longest Arithmetic Subsequence of Given Difference (LeetCode 1218) ----
    dict(
        title="Longest Arithmetic Subsequence of Given Difference",
        diff="M",
        lc=1218,
        slug="longest-arithmetic-subsequence-of-given-difference",
        prompt=(
            "Return the length of the longest subsequence of arr in which consecutive elements differ by exactly "
            "`difference`."
        ),
        sig="def longest_subsequence(arr: List[int], difference: int) -> int:",
        fn="longest_subsequence",
        tests=[
            (([1, 2, 3, 4], 1), 4),
            (([1, 3, 5, 7], 1), 1),
            (([1, 5, 7, 8, 5, 3, 4, 2, 1], -2), 4),
            (([4, 4, 4], 0), 3),
        ],
        hints=[
            "Let dp[i] = longest valid subsequence ending at index i.",
            "It extends a subsequence ending in the value arr[i] - difference.",
            (
                "Instead of scanning earlier indices, keep a dictionary best[value] = longest subsequence ending in "
                "that value."
            ),
        ],
        pattern="DP keyed by value (hash map instead of an inner loop)",
        explain=(
            "Only the value of the previous element matters, so a dictionary lookup replaces the O(n) search for a "
            "compatible predecessor."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - for each index scan all earlier indices",
        brute=r"""
# BRUTE FORCE: O(n^2) time - for each index scan all earlier indices
def longest_subsequence(arr, difference):
    n = len(arr)
    dp = [1] * n  # dp[i] = longest subsequence ending at i
    for i in range(n):
        for j in range(i):
            if arr[j] == arr[i] - difference:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: DP keyed by value (hash map instead of an inner loop)
def longest_subsequence(arr, difference):
    best = {}  # value -> longest subsequence ending in that value
    for x in arr:
        best[x] = best.get(x - difference, 0) + 1
    return max(best.values())
""",
    ),
    # ---- Longest Arithmetic Subsequence (LeetCode 1027) ----
    dict(
        title="Longest Arithmetic Subsequence",
        diff="M",
        lc=1027,
        slug="longest-arithmetic-subsequence",
        prompt=(
            "Return the length of the longest arithmetic subsequence (constant difference between consecutive "
            "chosen elements; the difference is not given)."
        ),
        sig="def longest_arith_seq_length(nums: List[int]) -> int:",
        fn="longest_arith_seq_length",
        tests=[
            (([3, 6, 9, 12],), 4),
            (([9, 4, 7, 2, 10],), 3),
            (([20, 1, 15, 3, 10, 5, 8],), 4),
            (([1, 2],), 2),
        ],
        hints=[
            "The difference is unknown, so the state needs it: (end index, difference).",
            "dp[(j, d)] = longest arithmetic subsequence ending at j with difference d.",
            "For each pair i < j with d = nums[j] - nums[i]: dp[(j, d)] = dp[(i, d)] + 1 (default 2).",
        ],
        pattern="DP over (index, common difference)",
        explain=(
            "Fixing the difference makes the problem the previous one; storing a table per difference handles all "
            "of them in one pass over pairs."
        ),
        cx="O(n^2) time and space",
        brute_cx="O(n^3) time - for each pair as the first two elements, extend greedily",
        brute=r"""
# BRUTE FORCE: O(n^3) time - for each pair as the first two elements, extend greedily
def longest_arith_seq_length(nums):
    n, best = len(nums), min(2, len(nums))
    for i in range(n):
        for j in range(i + 1, n):
            diff, last, length = nums[j] - nums[i], nums[j], 2
            for k in range(j + 1, n):  # take every later element that continues the progression
                if nums[k] - last == diff:
                    last, length = nums[k], length + 1
            best = max(best, length)
    return best
""",
        solution=r"""
# OPTIMISED: O(n^2) time and space
# Idea: DP over (index, common difference)
def longest_arith_seq_length(nums):
    dp = [
        {} for _ in nums
    ]  # dp[j][d] = longest arithmetic subsequence ending at j with difference d
    best = min(2, len(nums))
    for j in range(len(nums)):
        for i in range(j):
            d = nums[j] - nums[i]
            dp[j][d] = dp[i].get(d, 1) + 1  # extend the chain that ended at i, or start a pair
            best = max(best, dp[j][d])
    return best
""",
    ),
    # ---- Greatest Sum Divisible by Three (LeetCode 1262) ----
    dict(
        title="Greatest Sum Divisible by Three",
        diff="M",
        lc=1262,
        slug="greatest-sum-divisible-by-three",
        prompt="Return the maximum possible sum of a subset of nums that is divisible by 3.",
        sig="def max_sum_div_three(nums: List[int]) -> int:",
        fn="max_sum_div_three",
        tests=[
            (([3, 6, 5, 1, 8],), 18),
            (([4],), 0),
            (([1, 2, 3, 4, 4],), 12),
            (([2, 6, 2, 2, 7],), 15),
        ],
        hints=[
            "Only the sum's remainder mod 3 matters for the future.",
            "dp[r] = the largest sum so far whose remainder is r (dp[0] = 0, others -infinity).",
            "For each number x: new_dp[(r + x) % 3] = max(dp[(r + x) % 3], dp[r] + x). Answer dp[0].",
        ],
        pattern="DP over remainders (a tiny state space)",
        explain=(
            "Three states summarise every subset, so the exponential subset enumeration is replaced by 3 updates "
            "per number."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(2^n) time - try every subset",
        brute=r"""
# BRUTE FORCE: O(2^n) time - try every subset
def max_sum_div_three(nums):
    best = 0
    for mask in range(1 << len(nums)):
        total = sum(x for i, x in enumerate(nums) if mask >> i & 1)
        if total % 3 == 0:
            best = max(best, total)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: DP over remainders (a tiny state space)
def max_sum_div_three(nums):
    dp = [0, float("-inf"), float("-inf")]  # dp[r] = best sum with remainder r
    for x in nums:
        nxt = dp[:]
        for r in range(3):
            nxt[(r + x) % 3] = max(nxt[(r + x) % 3], dp[r] + x)  # take x, or keep the old value
        dp = nxt
    return dp[0]
""",
    ),
    # ---- Count Numbers with Unique Digits (LeetCode 357) ----
    dict(
        title="Count Numbers with Unique Digits",
        diff="M",
        lc=357,
        slug="count-numbers-with-unique-digits",
        prompt="Return how many integers x with 0 <= x < 10^n have all digits different.",
        sig="def count_numbers_with_unique_digits(n: int) -> int:",
        fn="count_numbers_with_unique_digits",
        tests=[
            ((0,), 1),
            ((1,), 10),
            ((2,), 91),
            ((3,), 739),
            ((4,), 5275),
        ],
        hints=[
            "Count by length: numbers with exactly k digits.",
            "A k-digit number: first digit 9 choices (1-9), next 9 (0-9 minus the used one), then 8, 7, ...",
            (
                "Sum 9 * 9 * 8 * ... for each length k = 2..n, plus 10 for the 1-digit numbers 0..9. Lengths beyond "
                "10 add nothing."
            ),
        ],
        pattern="Counting with decreasing choices (permutation counting)",
        explain=(
            "Each new digit position has one fewer unused digit than the previous one, so the count for each length "
            "is a product and the total is a sum."
        ),
        cx="O(min(n, 10)) time",
        brute_cx="O(10^n * n) time - test every number",
        brute=r"""
# BRUTE FORCE: O(10^n * n) time - test every number
def count_numbers_with_unique_digits(n):
    return sum(1 for x in range(10**n) if len(set(str(x))) == len(str(x)))
""",
        solution=r"""
# OPTIMISED: O(min(n, 10)) time
# Idea: Counting with decreasing choices (permutation counting)
def count_numbers_with_unique_digits(n):
    if n == 0:
        return 1
    total, ways = (
        10,
        9,
    )  # 10 one-digit numbers; `ways` = choices for the first digit of longer numbers
    available = 9  # digits left for the next position
    for _ in range(2, min(n, 10) + 1):
        ways *= available  # next position can use any digit not used yet
        total += ways
        available -= 1
    return total
""",
    ),
    # ---- Out of Boundary Paths (LeetCode 576) ----
    dict(
        title="Out of Boundary Paths",
        diff="M",
        lc=576,
        slug="out-of-boundary-paths",
        prompt=(
            "A ball starts at (start_row, start_col) of an m x n grid and makes at most max_move moves (up, down, "
            "left, right). Return the number of paths that take it out of the grid, modulo 1_000_000_007."
        ),
        sig="def find_paths(m: int, n: int, max_move: int, start_row: int, start_col: int) -> int:",
        fn="find_paths",
        tests=[
            ((2, 2, 2, 0, 0), 6),
            ((1, 3, 3, 0, 1), 12),
            ((1, 1, 1, 0, 0), 4),
            ((2, 2, 0, 0, 0), 0),
        ],
        hints=[
            "Define ways(row, col, moves_left): paths that leave the grid starting from this state.",
            "If the cell is outside the grid, that is exactly 1 path (the one that just left).",
            (
                "Otherwise add ways of the four neighbours with one fewer move; memoise (row, col, moves) or "
                "iterate move by move."
            ),
        ],
        pattern="Grid DP over (cell, remaining moves)",
        explain=(
            "The number of states is m * n * max_move, each needing 4 additions, instead of 4^max_move distinct walks."
        ),
        cx="O(m * n * max_move) time",
        brute_cx="O(4^max_move) time - recursion without memoisation",
        brute=r"""
# BRUTE FORCE: O(4^max_move) time - recursion without memoisation
def find_paths(m, n, max_move, start_row, start_col):
    def walk(r, c, moves):
        if not (0 <= r < m and 0 <= c < n):
            return 1  # left the grid
        if moves == 0:
            return 0
        return sum(walk(r + dr, c + dc, moves - 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))

    return walk(start_row, start_col, max_move) % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(m * n * max_move) time
# Idea: Grid DP over (cell, remaining moves)
def find_paths(m, n, max_move, start_row, start_col):
    mod = 10**9 + 7
    ways = [
        [0] * n for _ in range(m)
    ]  # ways[r][c] = paths that are at (r, c) after the moves so far
    ways[start_row][start_col] = 1
    out = 0
    for _ in range(max_move):
        nxt = [[0] * n for _ in range(m)]
        for r in range(m):
            for c in range(n):
                if ways[r][c]:
                    for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < m and 0 <= nc < n:
                            nxt[nr][nc] = (nxt[nr][nc] + ways[r][c]) % mod
                        else:
                            out = (out + ways[r][c]) % mod  # this move leaves the grid
        ways = nxt
    return out
""",
    ),
]
