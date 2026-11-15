"""more Dynamic Programming problems (batch 3) - part of the problem bank for the "dynamic_programming" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Minimum Falling Path Sum (LeetCode 931) ----
    dict(
        title="Minimum Falling Path Sum",
        diff="M",
        lc=931,
        slug="minimum-falling-path-sum",
        prompt=(
            "In an n x n grid you start anywhere in the top row and move down one row at a time, to the cell "
            "directly below or diagonally below-left/right. Return the smallest possible sum of the cells visited."
        ),
        sig="def min_falling_path_sum(matrix: List[List[int]]) -> int:",
        fn="min_falling_path_sum",
        tests=[
            (([[2, 1, 3], [6, 5, 4], [7, 8, 9]],), 13),
            (([[-19, 57], [-40, -5]],), -59),
            (([[5]],), 5),
            (([[1, 2], [3, 4]],), 4),
        ],
        hints=[
            "Ask: what is the cheapest way to ARRIVE at cell (r, c)?",
            "You can only have come from (r-1, c-1), (r-1, c) or (r-1, c+1) - take the cheapest of those.",
            "Process row by row. Row r only needs row r-1, so you can keep a single 1-D array.",
        ],
        pattern="Grid DP: best(r, c) = cell + min of the 3 cells above",
        explain=(
            "A path is decided one row at a time and the future never depends on how you got here, only on "
            "where\n        you are. That is the signature of DP: store the best cost to reach each cell of the "
            "previous row."
        ),
        cx="O(n^2) time, O(n) space",
        brute_cx="O(3^n) time - try every path",
        brute=r"""
# BRUTE FORCE: O(3^n) time - try every path
def min_falling_path_sum(matrix):
    n = len(matrix)

    def go(r, c):  # cheapest path from cell (r, c) down to the last row
        if r == n - 1:
            return matrix[r][c]
        options = [go(r + 1, nc) for nc in (c - 1, c, c + 1) if 0 <= nc < n]
        return matrix[r][c] + min(options)

    return min(go(0, c) for c in range(n))
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n) space
# Idea: Grid DP: best(r, c) = cell + min of the 3 cells above
def min_falling_path_sum(matrix):
    n = len(matrix)
    prev = matrix[0][:]  # prev[c] = cheapest cost to arrive at column c of the row above
    for r in range(1, n):
        cur = []
        for c in range(n):
            # neighbours in the previous row that can reach column c
            best_above = min(prev[max(0, c - 1) : min(n, c + 2)])
            cur.append(matrix[r][c] + best_above)
        prev = cur
    return min(prev)
""",
    ),
    # ---- Maximal Square (LeetCode 221) ----
    dict(
        title="Maximal Square",
        diff="M",
        lc=221,
        slug="maximal-square",
        prompt="Given a grid of '0'/'1' characters, return the AREA of the largest square made only of '1's.",
        sig="def maximal_square(matrix: List[List[str]]) -> int:",
        fn="maximal_square",
        tests=[
            (
                (
                    [
                        ["1", "0", "1", "0", "0"],
                        ["1", "0", "1", "1", "1"],
                        ["1", "1", "1", "1", "1"],
                        ["1", "0", "0", "1", "0"],
                    ],
                ),
                4,
            ),
            (([["0", "1"], ["1", "0"]],), 1),
            (([["0"]],), 0),
            (([["1"]],), 1),
            (([["1", "1"], ["1", "1"]],), 4),
        ],
        hints=[
            "Let side(r, c) = side of the biggest all-1 square whose BOTTOM-RIGHT corner is (r, c).",
            (
                "If the cell is '0' it is 0. Otherwise the square is limited by the squares ending just above, just "
                "left, and diagonally up-left."
            ),
            "side(r, c) = 1 + min(side(r-1, c), side(r, c-1), side(r-1, c-1)). Answer = max side squared.",
        ],
        pattern="Grid DP: biggest square ending at a cell = 1 + min of 3 neighbours",
        explain=(
            "A square of side k ending at (r, c) needs squares of side k-1 ending at the three neighbours (up, "
            "left, up-left).\n        The weakest neighbour limits the size, which is why we take the min."
        ),
        cx="O(R*C) time, O(C) space",
        brute_cx="O(R*C*min(R,C)^2) time - grow a square from every cell and check it",
        brute=r"""
# BRUTE FORCE: O(R*C*min(R,C)^2) time - grow a square from every cell and check it
def maximal_square(matrix):
    rows, cols = len(matrix), len(matrix[0])
    best = 0
    for r in range(rows):
        for c in range(cols):
            side = 1
            # keep growing the square whose top-left corner is (r, c) while it stays all '1'
            while r + side <= rows and c + side <= cols:
                if all(matrix[i][j] == "1" for i in range(r, r + side) for j in range(c, c + side)):
                    best = max(best, side)
                    side += 1
                else:
                    break
    return best * best
""",
        solution=r"""
# OPTIMISED: O(R*C) time, O(C) space
# Idea: Grid DP: biggest square ending at a cell = 1 + min of 3 neighbours
def maximal_square(matrix):
    cols = len(matrix[0])
    prev = [0] * (cols + 1)  # prev[c+1] = side of best square ending at (row above, column c)
    best = 0
    for row in matrix:
        cur = [0] * (cols + 1)
        for c in range(cols):
            if row[c] == "1":
                # limited by the weakest of: left, above, above-left
                cur[c + 1] = 1 + min(cur[c], prev[c + 1], prev[c])
                best = max(best, cur[c + 1])
        prev = cur
    return best * best
""",
    ),
    # ---- Delete and Earn (LeetCode 740) ----
    dict(
        title="Delete and Earn",
        diff="M",
        lc=740,
        slug="delete-and-earn",
        prompt=(
            "Pick any number x from the array and earn x points; then every x-1 and x+1 in the array is deleted. "
            "Repeat. Return the maximum points you can earn."
        ),
        sig="def delete_and_earn(nums: List[int]) -> int:",
        fn="delete_and_earn",
        tests=[
            (([3, 4, 2],), 6),
            (([2, 2, 3, 3, 3, 4],), 9),
            (([1],), 1),
            (([1, 1, 1, 2, 4, 5, 5, 5, 6],), 18),
            (([],), 0),
        ],
        hints=[
            (
                "Taking a value means taking ALL copies of it (they are worth the same and deleting neighbours does "
                "not hurt them)."
            ),
            "Group by value: points[v] = v * count(v). Taking v forbids v-1 and v+1.",
            "That is House Robber on the values 0..max: you cannot take two adjacent values.",
        ],
        pattern="Reduce to House Robber (adjacent values are 'adjacent houses')",
        explain=(
            "The trick is the reduction. Once you total the points per value, 'taking v kills v-1 and v+1' is "
            "exactly\n        'robbing house v kills houses v-1 and v+1'. Always ask: is this a problem I already "
            "know in disguise?"
        ),
        cx="O(n + max(nums)) time, O(max(nums)) space",
        brute_cx="exponential - try every value to take next",
        brute=r"""
# BRUTE FORCE: exponential - try every value to take next
def delete_and_earn(nums):
    def best(remaining):  # best score from the numbers still in the array
        if not remaining:
            return 0
        top = 0
        for v in set(remaining):
            earned = v * remaining.count(v)
            left = tuple(x for x in remaining if x not in (v - 1, v, v + 1))
            top = max(top, earned + best(left))
        return top

    return best(tuple(nums))
""",
        solution=r"""
# OPTIMISED: O(n + max(nums)) time, O(max(nums)) space
# Idea: Reduce to House Robber (adjacent values are 'adjacent houses')
def delete_and_earn(nums):
    if not nums:
        return 0
    points = [0] * (max(nums) + 1)
    for x in nums:
        points[x] += x  # all copies of value x together are worth x * count
    take, skip = 0, 0  # best total if we take / skip the previous value
    for p in points:
        take, skip = skip + p, max(take, skip)  # taking v is only allowed after skipping v-1
    return max(take, skip)
""",
    ),
    # ---- Interleaving String (LeetCode 97) ----
    dict(
        title="Interleaving String",
        diff="M",
        lc=97,
        slug="interleaving-string",
        prompt=(
            "Return True if s3 can be formed by interleaving s1 and s2: both are split into pieces and merged "
            "keeping the left-to-right order inside each string."
        ),
        sig="def is_interleave(s1: str, s2: str, s3: str) -> bool:",
        fn="is_interleave",
        tests=[
            (("aabcc", "dbbca", "aadbbcbcac"), True),
            (("aabcc", "dbbca", "aadbbbaccc"), False),
            (("", "", ""), True),
            (("a", "", "a"), True),
            (("a", "b", "ab"), True),
            (("ab", "", "ba"), False),
        ],
        hints=[
            "The lengths must add up first: len(s1) + len(s2) == len(s3).",
            "State (i, j): you have used i characters of s1 and j of s2, so you are at s3[i + j].",
            "ok(i, j) is true if s3[i+j] matches s1[i] and ok(i+1, j), or matches s2[j] and ok(i, j+1). Memoise it.",
        ],
        pattern="2-D DP over (chars used of s1, chars used of s2)",
        explain=(
            "Position in s3 is determined by (i, j), so only those two numbers describe the situation. There "
            "are\n        (m+1)*(n+1) such situations - far fewer than the 2^(m+n) ways of choosing letters."
        ),
        cx="O(m*n) time, O(n) space",
        brute_cx="O(2^(m+n)) time - try both choices at every character",
        brute=r"""
# BRUTE FORCE: O(2^(m+n)) time - try both choices at every character
def is_interleave(s1, s2, s3):
    if len(s1) + len(s2) != len(s3):
        return False

    def go(i, j):  # can s1[i:] and s2[j:] be interleaved into s3[i + j:]?
        k = i + j
        if k == len(s3):
            return True
        if i < len(s1) and s1[i] == s3[k] and go(i + 1, j):
            return True
        if j < len(s2) and s2[j] == s3[k] and go(i, j + 1):
            return True
        return False

    return go(0, 0)
""",
        solution=r"""
# OPTIMISED: O(m*n) time, O(n) space
# Idea: 2-D DP over (chars used of s1, chars used of s2)
def is_interleave(s1, s2, s3):
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False
    ok = [False] * (n + 1)  # ok[j] = s1[:i] and s2[:j] can form s3[:i + j]
    ok[0] = True
    for j in range(1, n + 1):  # row i = 0: only s2 is used
        ok[j] = ok[j - 1] and s2[j - 1] == s3[j - 1]
    for i in range(1, m + 1):
        ok[0] = ok[0] and s1[i - 1] == s3[i - 1]  # column j = 0: only s1 is used
        for j in range(1, n + 1):
            from_s1 = ok[j] and s1[i - 1] == s3[i + j - 1]  # last char came from s1
            from_s2 = ok[j - 1] and s2[j - 1] == s3[i + j - 1]  # last char came from s2
            ok[j] = from_s1 or from_s2
    return ok[n]
""",
    ),
    # ---- Unique Paths II (LeetCode 63) ----
    dict(
        title="Unique Paths II",
        diff="M",
        lc=63,
        slug="unique-paths-ii",
        prompt=(
            "A robot moves only right or down from the top-left to the bottom-right of a grid. Cells marked 1 are "
            "obstacles it cannot enter. Return the number of distinct paths."
        ),
        sig="def unique_paths_with_obstacles(grid: List[List[int]]) -> int:",
        fn="unique_paths_with_obstacles",
        tests=[
            (([[0, 0, 0], [0, 1, 0], [0, 0, 0]],), 2),
            (([[0, 1], [0, 0]],), 1),
            (([[1]],), 0),
            (([[0]],), 1),
            (([[0, 0], [1, 1], [0, 0]],), 0),
        ],
        hints=[
            "A cell can only be reached from the cell above it or the cell to its left.",
            "paths(r, c) = paths(r-1, c) + paths(r, c-1), but an obstacle cell has 0 paths.",
            "Fill the grid row by row; one 1-D array is enough because you only look one row back.",
        ],
        pattern="Grid DP: paths into a cell = paths from above + paths from left",
        explain=(
            "Counting paths is addition: every path to (r, c) ends with a step from above or from the left, and "
            "those\n        two groups never overlap. Obstacles simply zero a cell."
        ),
        cx="O(R*C) time, O(C) space",
        brute_cx="O(2^(R+C)) time - walk every path",
        brute=r"""
# BRUTE FORCE: O(2^(R+C)) time - walk every path
def unique_paths_with_obstacles(grid):
    rows, cols = len(grid), len(grid[0])

    def go(r, c):  # number of ways to get from (r, c) to the bottom-right corner
        if r >= rows or c >= cols or grid[r][c] == 1:
            return 0
        if r == rows - 1 and c == cols - 1:
            return 1
        return go(r + 1, c) + go(r, c + 1)

    return go(0, 0)
""",
        solution=r"""
# OPTIMISED: O(R*C) time, O(C) space
# Idea: Grid DP: paths into a cell = paths from above + paths from left
def unique_paths_with_obstacles(grid):
    cols = len(grid[0])
    ways = [0] * cols  # ways[c] = number of paths into column c of the current row
    ways[0] = 1  # one way to stand on the start (if it is not blocked, handled below)
    for row in grid:
        for c in range(cols):
            if row[c] == 1:
                ways[c] = 0  # an obstacle cannot be entered
            elif c > 0:
                ways[c] += ways[c - 1]  # from above (already in ways[c]) + from the left
    return ways[-1]
""",
    ),
    # ---- Minimum Cost For Tickets (LeetCode 983) ----
    dict(
        title="Minimum Cost For Tickets",
        diff="M",
        lc=983,
        slug="minimum-cost-for-tickets",
        prompt=(
            "You travel on the given sorted days of the year. A 1-day, 7-day and 30-day pass cost costs[0], "
            "costs[1], costs[2]. Return the minimum total cost to cover every travel day."
        ),
        sig="def mincost_tickets(days: List[int], costs: List[int]) -> int:",
        fn="mincost_tickets",
        tests=[
            (([1, 4, 6, 7, 8, 20], [2, 7, 15]), 11),
            (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 30, 31], [2, 7, 15]), 17),
            (([1], [2, 7, 15]), 2),
            (([1, 100], [2, 7, 15]), 4),
        ],
        hints=[
            "Decide the cheapest cost to be covered up to each day, going forward in time.",
            "If you do not travel on day d it is free: cost(d) = cost(d-1).",
            (
                "Otherwise cost(d) = min(cost(d-1) + c1, cost(d-7) + c7, cost(d-30) + c30), with negative days "
                "treated as 0."
            ),
        ],
        pattern="Timeline DP: cheapest to cover day d = min over last pass type",
        explain=(
            "The last pass you buy must end on (or cover) day d. Try each of the three passes, jump back by its "
            "length\n        and reuse the answer already computed there."
        ),
        cx="O(last day) time and space",
        brute_cx="O(3^n) time - try each pass for every travel day",
        brute=r"""
# BRUTE FORCE: O(3^n) time - try each pass for every travel day
def mincost_tickets(days, costs):
    def go(i):  # cheapest way to cover days[i:]
        if i == len(days):
            return 0
        best = float("inf")
        for span, price in zip((1, 7, 30), costs):
            j = i
            while j < len(days) and days[j] < days[i] + span:  # first day this pass does not cover
                j += 1
            best = min(best, price + go(j))
        return best

    return go(0)
""",
        solution=r"""
# OPTIMISED: O(last day) time and space
# Idea: Timeline DP: cheapest to cover day d = min over last pass type
def mincost_tickets(days, costs):
    travel = set(days)
    last = days[-1]
    cost = [0] * (last + 1)  # cost[d] = cheapest way to cover all travel days up to day d
    for d in range(1, last + 1):
        if d not in travel:
            cost[d] = cost[d - 1]  # nothing to pay for a day we do not travel
            continue
        cost[d] = min(
            cost[d - 1] + costs[0],  # 1-day pass today
            cost[max(0, d - 7)] + costs[1],  # a 7-day pass ending today
            cost[max(0, d - 30)] + costs[2],  # a 30-day pass ending today
        )
    return cost[last]
""",
    ),
    # ---- Longest String Chain (LeetCode 1048) ----
    dict(
        title="Longest String Chain",
        diff="M",
        lc=1048,
        slug="longest-string-chain",
        prompt=(
            "A word a is a predecessor of b if inserting exactly one letter anywhere in a gives b. Return the "
            "length of the longest chain w1 -> w2 -> ... where each word is a predecessor of the next."
        ),
        sig="def longest_str_chain(words: List[str]) -> int:",
        fn="longest_str_chain",
        tests=[
            ((["a", "b", "ba", "bca", "bda", "bdca"],), 4),
            ((["xbc", "pcxbcf", "xb", "cxbc", "pcxbc"],), 5),
            ((["abcd", "dbqca"],), 1),
            ((["a"],), 1),
        ],
        hints=[
            "A chain always grows by one letter, so process the words from shortest to longest.",
            "For a word w, its possible predecessors are w with one letter deleted - only len(w) candidates.",
            "best[w] = 1 + max(best[w without letter i]) over i; store best in a dictionary.",
        ],
        pattern="DP over a DAG ordered by length, predecessors found by deleting a letter",
        explain=(
            "Instead of comparing every pair of words (O(n^2) pair checks), generate the few possible predecessors "
            "of\n        each word and look them up in a hash map. Sorting by length guarantees they are ready."
        ),
        cx="O(n * L^2) time (L = word length), O(n) space",
        brute_cx="O(n^2 * L) per level and exponential recursion - compare every pair",
        brute=r"""
# BRUTE FORCE: O(n^2 * L) per level and exponential recursion - compare every pair
def longest_str_chain(words):
    def is_predecessor(a, b):  # can b be made by inserting one letter into a?
        if len(a) + 1 != len(b):
            return False
        return any(b[:i] + b[i + 1 :] == a for i in range(len(b)))

    def chain_ending_at(w):  # longest chain whose LAST word is w
        best = 1
        for v in words:
            if is_predecessor(v, w):
                best = max(best, 1 + chain_ending_at(v))
        return best

    return max(chain_ending_at(w) for w in words)
""",
        solution=r"""
# OPTIMISED: O(n * L^2) time (L = word length), O(n) space
# Idea: DP over a DAG ordered by length, predecessors found by deleting a letter
def longest_str_chain(words):
    best = {}  # best[w] = longest chain that ends with word w
    for w in sorted(words, key=len):  # shorter words first, so predecessors are already known
        best[w] = 1 + max((best.get(w[:i] + w[i + 1 :], 0) for i in range(len(w))), default=0)
    return max(best.values())
""",
    ),
    # ---- Russian Doll Envelopes (LeetCode 354) ----
    dict(
        title="Russian Doll Envelopes",
        diff="H",
        lc=354,
        slug="russian-doll-envelopes",
        prompt=(
            "Envelope [w, h] fits inside another only if BOTH its width and height are strictly smaller. Return the "
            "maximum number of envelopes you can nest one inside the next."
        ),
        sig="def max_envelopes(envelopes: List[List[int]]) -> int:",
        fn="max_envelopes",
        tests=[
            (([[5, 4], [6, 4], [6, 7], [2, 3]],), 3),
            (([[1, 1], [1, 1], [1, 1]],), 1),
            (([[4, 5], [4, 6], [6, 7], [2, 3], [1, 1]],), 4),
            (([[1, 3], [3, 5], [6, 7], [6, 8], [8, 4], [9, 5]],), 3),
        ],
        hints=[
            "Sort by width. Then you only have to worry about heights: you want an increasing sequence of heights.",
            (
                "Equal widths cannot nest. Sort equal widths by height DESCENDING so two of them can never both "
                "join an increasing run."
            ),
            (
                "Now it is Longest Increasing Subsequence on the heights - use the O(n log n) 'tails' array with "
                "binary search."
            ),
        ],
        pattern="Sort one dimension, then LIS on the other (patience sorting)",
        explain=(
            "Two-dimensional dominance becomes one-dimensional once one axis is sorted. The descending tie-break "
            "is\n        the subtle part: it makes equal-width envelopes impossible to chain."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2) time - LIS by checking every earlier envelope",
        brute=r"""
# BRUTE FORCE: O(n^2) time - LIS by checking every earlier envelope
def max_envelopes(envelopes):
    envs = sorted(envelopes)  # by width, then height
    best = [1] * len(envs)  # best[i] = longest nest ending with envelope i as the OUTERMOST
    for i in range(len(envs)):
        for j in range(i):
            if envs[j][0] < envs[i][0] and envs[j][1] < envs[i][1]:  # strictly smaller in both
                best[i] = max(best[i], best[j] + 1)
    return max(best, default=0)
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Sort one dimension, then LIS on the other (patience sorting)
def max_envelopes(envelopes):
    # width ascending; for equal widths, height DESCENDING so they cannot extend each other
    envelopes = sorted(envelopes, key=lambda e: (e[0], -e[1]))
    tails = []  # tails[k] = smallest possible last height of an increasing run of length k + 1
    for _, h in envelopes:
        i = bisect.bisect_left(tails, h)  # first run we can replace / extend
        if i == len(tails):
            tails.append(h)
        else:
            tails[i] = h
    return len(tails)
""",
    ),
    # ---- Distinct Subsequences (LeetCode 115) ----
    dict(
        title="Distinct Subsequences",
        diff="H",
        lc=115,
        slug="distinct-subsequences",
        prompt=(
            "Count how many different subsequences of s are equal to t (choosing different positions counts as "
            "different)."
        ),
        sig="def num_distinct(s: str, t: str) -> int:",
        fn="num_distinct",
        tests=[
            (("rabbbit", "rabbit"), 3),
            (("babgbag", "bag"), 5),
            (("a", "a"), 1),
            (("abc", ""), 1),
            (("", "a"), 0),
            (("aaa", "aa"), 3),
        ],
        hints=[
            "State (i, j): number of ways s[:i] contains t[:j] as a subsequence.",
            "If s[i-1] != t[j-1] you cannot use that character: ways(i, j) = ways(i-1, j).",
            (
                "If they match you may use it or not: ways(i, j) = ways(i-1, j-1) + ways(i-1, j). Empty t has "
                "exactly 1 way."
            ),
        ],
        pattern="2-D string DP: use the matching character or skip it",
        explain=(
            "Every subsequence either uses the last character of s (only possible when it matches t's last "
            "character)\n        or does not. The two groups are disjoint, so the counts add. Update j downwards to "
            "reuse one row."
        ),
        cx="O(m*n) time, O(n) space",
        brute_cx="O(2^m) time - try keeping or dropping every character",
        brute=r"""
# BRUTE FORCE: O(2^m) time - try keeping or dropping every character
def num_distinct(s, t):
    def go(i, j):  # ways to build t[j:] from s[i:]
        if j == len(t):
            return 1  # nothing left to build: the empty choice works
        if i == len(s):
            return 0
        ways = go(i + 1, j)  # skip s[i]
        if s[i] == t[j]:
            ways += go(i + 1, j + 1)  # use s[i] for t[j]
        return ways

    return go(0, 0)
""",
        solution=r"""
# OPTIMISED: O(m*n) time, O(n) space
# Idea: 2-D string DP: use the matching character or skip it
def num_distinct(s, t):
    ways = [1] + [0] * len(t)  # ways[j] = number of ways the prefix of s read so far builds t[:j]
    for ch in s:
        for j in range(len(t), 0, -1):  # go right-to-left so ways[j-1] is still the OLD value
            if ch == t[j - 1]:
                ways[j] += ways[j - 1]
    return ways[len(t)]
""",
    ),
    # ---- Number of Longest Increasing Subsequence (LeetCode 673) ----
    dict(
        title="Number of Longest Increasing Subsequence",
        diff="M",
        lc=673,
        slug="number-of-longest-increasing-subsequence",
        prompt="Return how many strictly increasing subsequences have the maximum possible length.",
        sig="def find_number_of_lis(nums: List[int]) -> int:",
        fn="find_number_of_lis",
        tests=[
            (([1, 3, 5, 4, 7],), 2),
            (([2, 2, 2, 2, 2],), 5),
            (([1],), 1),
            (([1, 2, 4, 3, 5, 4, 7, 2],), 3),
            (([],), 0),
        ],
        hints=[
            "Track two numbers per index: the LIS length ending there, and how many LIS of that length end there.",
            "For each j < i with nums[j] < nums[i]: a longer length replaces the count, an equal length adds to it.",
            "At the end add up the counts of every index whose length equals the global maximum.",
        ],
        pattern="LIS DP with a counter next to the length",
        explain=(
            "Plain LIS stores only lengths. To count, store (length, count): when you find a longer chain, restart "
            "the\n        count from the predecessor's; when you find an equally long chain, add the predecessor's "
            "count."
        ),
        cx="O(n^2) time, O(n) space",
        brute_cx="O(2^n * n) time - enumerate every subsequence",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - enumerate every subsequence
def find_number_of_lis(nums):
    n = len(nums)
    best_len, count = 0, 0
    for mask in range(1, 1 << n):  # every non-empty subsequence
        sub = [nums[i] for i in range(n) if mask >> i & 1]
        if all(sub[k] < sub[k + 1] for k in range(len(sub) - 1)):  # strictly increasing?
            if len(sub) > best_len:
                best_len, count = len(sub), 1
            elif len(sub) == best_len:
                count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n) space
# Idea: LIS DP with a counter next to the length
def find_number_of_lis(nums):
    n = len(nums)
    length = [1] * n  # length[i] = LIS length ending exactly at i
    count = [1] * n  # count[i]  = how many LIS of that length end at i
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                if length[j] + 1 > length[i]:  # found a longer chain: restart the count
                    length[i], count[i] = length[j] + 1, count[j]
                elif length[j] + 1 == length[i]:  # another chain of the same length: add them
                    count[i] += count[j]
    longest = max(length, default=0)
    return sum(c for l_, c in zip(length, count) if l_ == longest)
""",
    ),
    # ---- Ones and Zeroes (LeetCode 474) ----
    dict(
        title="Ones and Zeroes",
        diff="M",
        lc=474,
        slug="ones-and-zeroes",
        prompt=(
            "Each string in strs is made of '0' and '1'. Return the size of the largest subset of strs that uses at "
            "most m zeros and at most n ones in total."
        ),
        sig="def find_max_form(strs: List[str], m: int, n: int) -> int:",
        fn="find_max_form",
        tests=[
            ((["10", "0001", "111001", "1", "0"], 5, 3), 4),
            ((["10", "0", "1"], 1, 1), 2),
            ((["00", "000"], 1, 10), 0),
            ((["0", "1"], 0, 0), 0),
            ((["0", "0", "1", "1"], 2, 1), 3),
        ],
        hints=[
            (
                "Each string is an item you take once, costing some zeros and some ones: a 0/1 knapsack with TWO "
                "capacities."
            ),
            "dp[z][o] = largest subset using at most z zeros and o ones.",
            "For each string update dp from big capacities to small so the string is used at most once.",
        ],
        pattern="0/1 knapsack with two capacities (iterate capacities downwards)",
        explain=(
            "Knapsack with two limits just means a 2-D table. Looping the capacities in DESCENDING order is what "
            "stops\n        one string from being counted twice in the same round."
        ),
        cx="O(len(strs) * m * n) time, O(m*n) space",
        brute_cx="O(2^len(strs)) time - try every subset",
        brute=r"""
# BRUTE FORCE: O(2^len(strs)) time - try every subset
def find_max_form(strs, m, n):
    def go(i, zeros_left, ones_left):  # best subset size using strs[i:]
        if i == len(strs):
            return 0
        best = go(i + 1, zeros_left, ones_left)  # skip this string
        z, o = strs[i].count("0"), strs[i].count("1")
        if z <= zeros_left and o <= ones_left:  # or take it if it still fits
            best = max(best, 1 + go(i + 1, zeros_left - z, ones_left - o))
        return best

    return go(0, m, n)
""",
        solution=r"""
# OPTIMISED: O(len(strs) * m * n) time, O(m*n) space
# Idea: 0/1 knapsack with two capacities (iterate capacities downwards)
def find_max_form(strs, m, n):
    dp = [
        [0] * (n + 1) for _ in range(m + 1)
    ]  # dp[z][o] = best subset size with budget z zeros, o ones
    for s in strs:
        zeros, ones = s.count("0"), s.count("1")
        for z in range(m, zeros - 1, -1):  # descending: each string is used at most once
            for o in range(n, ones - 1, -1):
                dp[z][o] = max(dp[z][o], dp[z - zeros][o - ones] + 1)
    return dp[m][n]
""",
    ),
    # ---- Best Time to Buy and Sell Stock IV (LeetCode 188) ----
    dict(
        title="Best Time to Buy and Sell Stock IV",
        diff="H",
        lc=188,
        slug="best-time-to-buy-and-sell-stock-iv",
        prompt=(
            "prices[i] is the price on day i. You may complete at most k transactions (buy then sell). Return the "
            "maximum profit."
        ),
        sig="def max_profit(k: int, prices: List[int]) -> int:",
        fn="max_profit",
        tests=[
            ((2, [2, 4, 1]), 2),
            ((2, [3, 2, 6, 5, 0, 3]), 7),
            ((1, [1, 2]), 1),
            ((0, [1, 2]), 0),
            ((100, [1, 2, 3, 4, 5]), 4),
            ((2, []), 0),
        ],
        hints=[
            "Track the state after each transaction: money while HOLDING a share vs money when NOT holding one.",
            (
                "buy[t] = best balance while holding during transaction t; sell[t] = best balance after completing "
                "t transactions."
            ),
            (
                "Each price updates: buy[t] = max(buy[t], sell[t-1] - price); sell[t] = max(sell[t], buy[t] + "
                "price). If k is huge cap it at n // 2."
            ),
        ],
        pattern="State-machine DP: (transactions used, holding or not)",
        explain=(
            "Model a tiny machine with states 'holding after t buys' and 'cash after t sells' and update them once "
            "per\n        day. Capping k at n // 2 is valid because you can never profit from more than that many "
            "trades."
        ),
        cx="O(n * k) time, O(k) space",
        brute_cx="O(2^n) time - decide buy / sell / wait every day",
        brute=r"""
# BRUTE FORCE: O(2^n) time - decide buy / sell / wait every day
def max_profit(k, prices):
    def go(day, left, holding):  # best future profit; `left` = buys still allowed
        if day == len(prices) or (left == 0 and not holding):
            return 0
        best = go(day + 1, left, holding)  # do nothing today
        if holding:
            best = max(best, prices[day] + go(day + 1, left, False))  # sell
        elif left > 0:
            best = max(
                best, -prices[day] + go(day + 1, left - 1, True)
            )  # buy (uses one transaction)
        return best

    return go(0, k, False)
""",
        solution=r"""
# OPTIMISED: O(n * k) time, O(k) space
# Idea: State-machine DP: (transactions used, holding or not)
def max_profit(k, prices):
    k = min(k, len(prices) // 2)  # more transactions than n // 2 can never help
    if k == 0:
        return 0
    buy = [float("-inf")] * (k + 1)  # buy[t]  = best balance while holding a share in transaction t
    sell = [0] * (k + 1)  # sell[t] = best balance after finishing t transactions
    for price in prices:
        for t in range(1, k + 1):
            buy[t] = max(buy[t], sell[t - 1] - price)  # open transaction t
            sell[t] = max(sell[t], buy[t] + price)  # close transaction t
    return sell[k]
""",
    ),
    # ---- Best Time to Buy and Sell Stock with Transaction Fee (LeetCode 714) ----
    dict(
        title="Best Time to Buy and Sell Stock with Transaction Fee",
        diff="M",
        lc=714,
        slug="best-time-to-buy-and-sell-stock-with-transaction-fee",
        prompt=(
            "You may buy and sell as often as you like (one share at a time) but pay a fee on every transaction. "
            "Return the maximum profit."
        ),
        sig="def max_profit(prices: List[int], fee: int) -> int:",
        fn="max_profit",
        tests=[
            (([1, 3, 2, 8, 4, 9], 2), 8),
            (([1, 3, 7, 5, 10, 3], 3), 6),
            (([1], 0), 0),
            (([5, 4, 3], 1), 0),
            (([], 2), 0),
        ],
        hints=[
            "Only two states matter each day: you hold a share, or you do not.",
            "cash = best money without a share; hold = best money while holding one.",
            "Each day: cash = max(cash, hold + price - fee); hold = max(hold, cash_before - price).",
        ],
        pattern="Two-state DP (hold / cash); fee charged on sell",
        explain=(
            "Any number of transactions means no counter is needed - just two running values. Charging the fee "
            "when\n        you sell is enough, because every buy is eventually matched by a sell."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(2^n) time - buy / sell / wait every day",
        brute=r"""
# BRUTE FORCE: O(2^n) time - buy / sell / wait every day
def max_profit(prices, fee):
    def go(day, holding):  # best profit from `day` onwards
        if day == len(prices):
            return 0
        best = go(day + 1, holding)  # wait
        if holding:
            best = max(best, prices[day] - fee + go(day + 1, False))  # sell and pay the fee
        else:
            best = max(best, -prices[day] + go(day + 1, True))  # buy
        return best

    return go(0, False)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two-state DP (hold / cash); fee charged on sell
def max_profit(prices, fee):
    cash, hold = 0, float("-inf")  # cash: no share in hand; hold: one share in hand
    for price in prices:
        cash, hold = (
            max(cash, hold + price - fee),
            max(hold, cash - price),
        )  # both use yesterday's values
    return cash
""",
    ),
]
