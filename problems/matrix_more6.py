"""extra batch of Matrix / Grid problems - the problem bank for the "matrix" topic (batch 6).

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
    # ---- Range Addition II (LeetCode 598) ----
    dict(
        title="Range Addition II",
        diff="E",
        lc=598,
        slug="range-addition-ii",
        prompt=(
            "You start with an m x n matrix of zeros. Each operation [a, b] adds 1 to every cell (x, y) with 0 <= x "
            "< a and 0 <= y < b. After all operations, return how many cells hold the maximum value."
        ),
        sig="def max_count(m: int, n: int, ops: List[List[int]]) -> int:",
        fn="max_count",
        tests=[
            ((3, 3, [[2, 2], [3, 3]]), 4),
            ((3, 3, []), 9),
            ((4, 5, [[3, 3]]), 9),
            (
                (
                    3,
                    3,
                    [[2, 2], [3, 3], [3, 3], [3, 3], [2, 2], [3, 3], [3, 3], [3, 3], [2, 2], [3, 3], [3, 3], [3, 3]],
                ),
                4,
            ),
        ],
        hints=[
            "Every operation touches a rectangle anchored at the top-left corner (0, 0).",
            "Cell (0, 0) is covered by every operation, so it always holds the maximum value.",
            "The cells that equal the maximum are exactly those covered by ALL rectangles: a min(a) by min(b) block.",
        ],
        pattern="Intersection of rectangles that share a corner",
        explain=(
            "All rectangles are anchored at (0, 0), so a cell (x, y) is covered by operation [a, b] exactly when x "
            "< a and y < b. A cell covered by every operation therefore needs x < min(a) and y < min(b). Those "
            "cells receive the most increments, so counting them is min(a) * min(b). With no operations nothing "
            "changes and all m * n cells tie at 0."
        ),
        cx="O(k) time for k operations, O(1) space",
        brute_cx="O(k * m * n) time and O(m * n) space - actually apply every operation to the matrix",
        brute=r"""
# BRUTE FORCE: O(k * m * n) time and O(m * n) space - actually apply every operation to the matrix
def max_count(m, n, ops):
    grid = [[0] * n for _ in range(m)]
    for a, b in ops:
        for i in range(a):
            for j in range(b):
                grid[i][j] += 1
    best = max(max(row) for row in grid)
    return sum(row.count(best) for row in grid)
""",
        solution=r"""
# OPTIMISED: O(k) time for k operations, O(1) space
# Idea: Intersection of rectangles that share a corner
def max_count(m, n, ops):
    for a, b in ops:
        m = min(m, a)
        n = min(n, b)
    return m * n
""",
    ),
    # ---- Image Smoother (LeetCode 661) ----
    dict(
        title="Image Smoother",
        diff="E",
        lc=661,
        slug="image-smoother",
        prompt=(
            "Each output cell is the average (rounded DOWN) of the cell itself and its up-to-8 neighbours that "
            "exist inside the grid. Return the smoothed image."
        ),
        sig="def image_smoother(img: List[List[int]]) -> List[List[int]]:",
        fn="image_smoother",
        tests=[
            (([[1, 1, 1], [1, 0, 1], [1, 1, 1]],), [[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
            (
                ([[100, 200, 100], [200, 50, 200], [100, 200, 100]],),
                [[137, 141, 137], [141, 138, 141], [137, 141, 137]],
            ),
            (([[5]],), [[5]]),
            (([[1, 2]],), [[1, 1]]),
        ],
        hints=[
            "For one cell, the window is rows i-1..i+1 and columns j-1..j+1, clipped to the grid.",
            "Divide by the number of cells that are really inside the window - corners have 4, edges 6, the middle 9.",
            "To avoid re-adding 9 numbers per cell, build a 2D prefix-sum table and read each window sum in O(1).",
        ],
        pattern="2D prefix sums for window totals",
        explain=(
            "Let pre[i][j] be the sum of the rectangle from (0, 0) to (i-1, j-1). Then the sum of any rectangle is "
            "pre[r2][c2] - pre[r1][c2] - pre[r2][c1] + pre[r1][c1] (inclusion-exclusion). Clip the 3 x 3 window to "
            "the grid, read its sum and its cell count (rows x columns), and floor-divide. Each cell now costs O(1) "
            "instead of up to nine additions - the same trick works for windows of any size."
        ),
        cx="O(m * n) time and space",
        brute_cx="O(9 * m * n) = O(m * n) time - visit the nine neighbours of every cell",
        brute=r"""
# BRUTE FORCE: O(9 * m * n) = O(m * n) time - visit the nine neighbours of every cell
def image_smoother(img):
    m, n = len(img), len(img[0])
    out = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            total = count = 0
            for x in range(i - 1, i + 2):
                for y in range(j - 1, j + 2):
                    if 0 <= x < m and 0 <= y < n:
                        total += img[x][y]
                        count += 1
            out[i][j] = total // count
    return out
""",
        solution=r"""
# OPTIMISED: O(m * n) time and space
# Idea: 2D prefix sums for window totals
def image_smoother(img):
    m, n = len(img), len(img[0])
    pre = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m):
        for j in range(n):
            pre[i + 1][j + 1] = img[i][j] + pre[i][j + 1] + pre[i + 1][j] - pre[i][j]
    out = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            r1, r2 = max(0, i - 1), min(m, i + 2)
            c1, c2 = max(0, j - 1), min(n, j + 2)
            total = pre[r2][c2] - pre[r1][c2] - pre[r2][c1] + pre[r1][c1]
            out[i][j] = total // ((r2 - r1) * (c2 - c1))
    return out
""",
    ),
    # ---- Max Increase to Keep City Skyline (LeetCode 807) ----
    dict(
        title="Max Increase to Keep City Skyline",
        diff="M",
        lc=807,
        slug="max-increase-to-keep-city-skyline",
        prompt=(
            "grid[r][c] is a building height. The skyline seen from each of the four sides is the list of row "
            "maxima (east/west) and column maxima (north/south). You may raise any buildings by any amount as long "
            "as NONE of the four skylines changes. Return the largest possible total of added height."
        ),
        sig="def max_increase_keeping_skyline(grid: List[List[int]]) -> int:",
        fn="max_increase_keeping_skyline",
        tests=[
            (([[3, 0, 8, 4], [2, 4, 5, 7], [9, 2, 6, 3], [0, 3, 1, 0]],), 35),
            (([[0, 0, 0], [0, 0, 0], [0, 0, 0]],), 0),
            (([[1]],), 0),
            (([[1, 2], [3, 4]],), 1),
        ],
        hints=[
            "A building can never exceed the tallest building in its row or in its column.",
            "So each building can rise to min(row maximum, column maximum) - and every building can do this at once.",
            "Precompute the row maxima and column maxima once, then sum min(rowMax, colMax) - height over all cells.",
        ],
        pattern="Precompute row/column maxima, then a per-cell bound",
        explain=(
            "Raising a building above its row maximum would change the east/west skyline; above its column maximum "
            "would change the north/south one. So min(row max, column max) is a hard cap. The caps do not conflict: "
            "after raising every building to its cap, each row maximum and column maximum is unchanged (the "
            "original tallest building already sat at its own cap). Hence the answer is the sum of cap - height."
        ),
        cx="O(m * n) time, O(m + n) space",
        brute_cx="O(m * n * (m + n)) time - rescan the row and column for every cell",
        brute=r"""
# BRUTE FORCE: O(m * n * (m + n)) time - rescan the row and column for every cell
def max_increase_keeping_skyline(grid):
    m, n = len(grid), len(grid[0])
    total = 0
    for i in range(m):
        for j in range(n):
            row_max = max(grid[i])
            col_max = max(grid[k][j] for k in range(m))
            total += min(row_max, col_max) - grid[i][j]
    return total
""",
        solution=r"""
# OPTIMISED: O(m * n) time, O(m + n) space
# Idea: Precompute row/column maxima, then a per-cell bound
def max_increase_keeping_skyline(grid):
    row_max = [max(row) for row in grid]
    col_max = [max(col) for col in zip(*grid)]
    total = 0
    for i, row in enumerate(grid):
        for j, h in enumerate(row):
            total += min(row_max[i], col_max[j]) - h
    return total
""",
    ),
    # ---- Magic Squares In Grid (LeetCode 840) ----
    dict(
        title="Magic Squares In Grid",
        diff="M",
        lc=840,
        slug="magic-squares-in-grid",
        prompt=(
            "A 3 x 3 magic square contains each of the numbers 1..9 exactly once, and every row, every column and "
            "both diagonals sum to the same value. Count the 3 x 3 contiguous sub-grids of grid that are magic "
            "squares."
        ),
        sig="def num_magic_squares_inside(grid: List[List[int]]) -> int:",
        fn="num_magic_squares_inside",
        tests=[
            (([[4, 3, 8, 4], [9, 5, 1, 9], [2, 7, 6, 2]],), 1),
            (([[8]],), 0),
            (([[4, 3, 8], [9, 5, 1], [2, 7, 6]],), 1),
            (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), 0),
        ],
        hints=[
            "Only windows of exactly 3 x 3 matter, so there are at most (m-2) * (n-2) of them to inspect.",
            "The magic sum of 1..9 must be 15, and the centre of every 3 x 3 magic square is forced to be 5.",
            (
                "Walk the eight border cells clockwise: for a magic square the sequence is always a rotation of 4 3 "
                "8 1 6 7 2 9 (or its mirror image), with an even number in the top-left corner."
            ),
        ],
        pattern="Prune with a mathematical invariant, then verify the window",
        explain=(
            "Brute force checks every window against the definition: digits 1..9 once, then all eight line sums. "
            "The optimised version uses the structure of the only magic square: the 4 corners are the even numbers, "
            "the 4 edges the odd numbers, the centre is 5, and opposite cells sum to 10. Reading the border "
            "clockwise from a corner always yields a rotation of 43816729 or of its mirror 92761834. So a window is "
            "magic iff its centre is 5, its top-left corner is even and the border string occurs inside the doubled "
            "pattern - one O(1) string test per window."
        ),
        cx="O(m * n) time, O(1) space",
        brute_cx="O(m * n * 9) time - rebuild and sort the nine cells and sum every line for each window",
        brute=r"""
# BRUTE FORCE: O(m * n * 9) time - rebuild and sort the nine cells and sum every line for each window
def num_magic_squares_inside(grid):
    m, n = len(grid), len(grid[0])
    count = 0
    for i in range(m - 2):
        for j in range(n - 2):
            cells = [grid[i + a][j + b] for a in range(3) for b in range(3)]
            if sorted(cells) != list(range(1, 10)):
                continue
            rows = [sum(grid[i + a][j : j + 3]) for a in range(3)]
            cols = [sum(grid[i + a][j + b] for a in range(3)) for b in range(3)]
            d1 = sum(grid[i + a][j + a] for a in range(3))
            d2 = sum(grid[i + a][j + 2 - a] for a in range(3))
            if set(rows + cols + [d1, d2]) == {15}:
                count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(m * n) time, O(1) space
# Idea: Prune with a mathematical invariant, then verify the window
def num_magic_squares_inside(grid):
    m, n = len(grid), len(grid[0])
    cyc = "4381672943816729"
    rev = cyc[::-1]
    count = 0
    for i in range(m - 2):
        for j in range(n - 2):
            if grid[i + 1][j + 1] != 5 or grid[i][j] % 2 != 0:
                continue
            ring = [
                grid[i][j],
                grid[i][j + 1],
                grid[i][j + 2],
                grid[i + 1][j + 2],
                grid[i + 2][j + 2],
                grid[i + 2][j + 1],
                grid[i + 2][j],
                grid[i + 1][j],
            ]
            s = "".join(map(str, ring))
            if len(s) == 8 and (s in cyc or s in rev):
                count += 1
    return count
""",
    ),
    # ---- Spiral Matrix III (LeetCode 885) ----
    dict(
        title="Spiral Matrix III",
        diff="M",
        lc=885,
        slug="spiral-matrix-iii",
        prompt=(
            "You stand at (row_start, col_start) of a rows x cols grid facing east. Walk in an expanding clockwise "
            "spiral (the walk may leave the grid and come back). Return the coordinates of every grid cell in the "
            "order you first reach it."
        ),
        sig="def spiral_matrix_iii(rows: int, cols: int, row_start: int, col_start: int) -> List[List[int]]:",
        fn="spiral_matrix_iii",
        tests=[
            ((1, 4, 0, 0), [[0, 0], [0, 1], [0, 2], [0, 3]]),
            (
                (5, 6, 1, 4),
                [
                    [1, 4],
                    [1, 5],
                    [2, 5],
                    [2, 4],
                    [2, 3],
                    [1, 3],
                    [0, 3],
                    [0, 4],
                    [0, 5],
                    [3, 5],
                    [3, 4],
                    [3, 3],
                    [3, 2],
                    [2, 2],
                    [1, 2],
                    [0, 2],
                    [4, 5],
                    [4, 4],
                    [4, 3],
                    [4, 2],
                    [4, 1],
                    [3, 1],
                    [2, 1],
                    [1, 1],
                    [0, 1],
                    [4, 0],
                    [3, 0],
                    [2, 0],
                    [1, 0],
                    [0, 0],
                ],
            ),
            ((1, 1, 0, 0), [[0, 0]]),
            ((2, 1, 1, 0), [[1, 0], [0, 0]]),
        ],
        hints=[
            (
                "Ignore the grid for a moment: an expanding spiral walks 1 step east, 1 south, 2 west, 2 north, 3 "
                "east, 3 south..."
            ),
            "Each step length is used twice in a row, then it grows by one: lengths 1, 1, 2, 2, 3, 3, ...",
            "Keep walking those legs, and record a cell only when it lies inside the grid; stop at rows * cols cells.",
        ],
        pattern="Spiral walk with growing leg lengths; filter by bounds",
        explain=(
            "Directions rotate east -> south -> west -> north, and the leg length goes 1, 1, 2, 2, 3, 3, ... "
            "because each completed pair of turns widens the spiral by one ring. The spiral never skips a cell, so "
            "every grid cell is eventually visited; we just ignore the steps that fall outside. The walk is at most "
            "about (2 * max(rows, cols))^2 steps, which is why the start may be anywhere. The brute force instead "
            "walks cell by cell, turning right whenever the cell on the right is still unvisited."
        ),
        cx="O((max(rows, cols))^2) time, O(rows * cols) output space",
        brute_cx=(
            "O((max(rows, cols))^2) time and extra space - a visited set, turning right whenever that cell is free"
        ),
        brute=r"""
# BRUTE FORCE: O((max(rows, cols))^2) time and extra space - a visited set, turning right whenever that cell is free
def spiral_matrix_iii(rows, cols, row_start, col_start):
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    r, c, d = row_start, col_start, 0
    seen = {(r, c)}
    out = [[r, c]]
    c += 1
    seen.add((r, c))
    if 0 <= r < rows and 0 <= c < cols:
        out.append([r, c])
    while len(out) < rows * cols:
        nd = (d + 1) % 4
        if (r + dirs[nd][0], c + dirs[nd][1]) not in seen:
            d = nd
        r, c = r + dirs[d][0], c + dirs[d][1]
        seen.add((r, c))
        if 0 <= r < rows and 0 <= c < cols:
            out.append([r, c])
    return out
""",
        solution=r"""
# OPTIMISED: O((max(rows, cols))^2) time, O(rows * cols) output space
# Idea: Spiral walk with growing leg lengths; filter by bounds
def spiral_matrix_iii(rows, cols, row_start, col_start):
    out = [[row_start, col_start]]
    r, c = row_start, col_start
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    step, d = 1, 0
    while len(out) < rows * cols:
        for _ in range(2):
            dr, dc = dirs[d]
            for _ in range(step):
                r += dr
                c += dc
                if 0 <= r < rows and 0 <= c < cols:
                    out.append([r, c])
            d = (d + 1) % 4
        step += 1
    return out
""",
    ),
    # ---- Diagonal Traverse II (LeetCode 1424) ----
    dict(
        title="Diagonal Traverse II",
        diff="M",
        lc=1424,
        slug="diagonal-traverse-ii",
        prompt=(
            "nums is a 'jagged' 2D list: rows may have different lengths (each row has at least one element). "
            "Return all elements in diagonal order: diagonals by increasing i + j, and inside one diagonal from the "
            "bottom-left element up to the top-right one."
        ),
        sig="def find_diagonal_order(nums: List[List[int]]) -> List[int]:",
        fn="find_diagonal_order",
        tests=[
            (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [1, 4, 2, 7, 5, 3, 8, 6, 9]),
            (
                ([[1, 2, 3, 4, 5], [6, 7], [8], [9, 10, 11], [12, 13, 14, 15, 16]],),
                [1, 6, 2, 8, 7, 3, 9, 4, 12, 10, 5, 13, 11, 14, 15, 16],
            ),
            (([[1]],), [1]),
            (([[1, 2], [3]],), [1, 3, 2]),
        ],
        hints=[
            "Cells on the same diagonal share the same value of i + j.",
            "Inside one diagonal the order is by DEcreasing row i (equivalently increasing column j).",
            (
                "Bucket cells by i + j while visiting rows from the LAST row to the first; each bucket is then "
                "already in order."
            ),
        ],
        pattern="Group by diagonal index i + j",
        explain=(
            "A diagonal is the set of cells with equal i + j. In a rectangle you could walk it with a formula, but "
            "jagged rows make that awkward - so we bucket instead. Visiting rows from bottom to top and appending "
            "each cell to bucket i + j means a bucket receives its cells in decreasing i, exactly the required "
            "in-diagonal order. Concatenating buckets 0, 1, 2, ... finishes the job. Brute force collects (i + j, "
            "j, value) tuples and sorts them."
        ),
        cx="O(N) time and space for N cells",
        brute_cx="O(N log N) time - sort every cell by (i + j, j)",
        brute=r"""
# BRUTE FORCE: O(N log N) time - sort every cell by (i + j, j)
def find_diagonal_order(nums):
    cells = []
    for i, row in enumerate(nums):
        for j, v in enumerate(row):
            cells.append((i + j, j, v))
    cells.sort()
    return [v for _, _, v in cells]
""",
        solution=r"""
# OPTIMISED: O(N) time and space for N cells
# Idea: Group by diagonal index i + j
def find_diagonal_order(nums):
    width = max(len(row) for row in nums)
    buckets = [[] for _ in range(len(nums) + width - 1)]
    for i in range(len(nums) - 1, -1, -1):
        for j, v in enumerate(nums[i]):
            buckets[i + j].append(v)
    return [v for bucket in buckets for v in bucket]
""",
    ),
    # ---- Cherry Pickup II (LeetCode 1463) ----
    dict(
        title="Cherry Pickup II",
        diff="H",
        lc=1463,
        slug="cherry-pickup-ii",
        prompt=(
            "grid[r][c] is the number of cherries in a cell. Two robots start in the top row, one at column 0 and "
            "one at the last column. Each step both move down one row and may shift one column left, stay, or shift "
            "right (staying inside the grid). A cell's cherries are taken once, even if both robots stand there. "
            "Return the maximum total they can collect by the bottom row."
        ),
        sig="def cherry_pickup(grid: List[List[int]]) -> int:",
        fn="cherry_pickup",
        tests=[
            (([[3, 1, 1], [2, 5, 1], [1, 5, 5], [2, 1, 1]],), 24),
            (
                (
                    [
                        [1, 0, 0, 0, 0, 0, 1],
                        [2, 0, 0, 0, 0, 3, 0],
                        [2, 0, 9, 0, 0, 0, 0],
                        [0, 3, 0, 5, 4, 0, 0],
                        [1, 0, 2, 3, 0, 0, 6],
                    ],
                ),
                28,
            ),
            (([[1, 1], [1, 1]],), 4),
            (([[5, 3]],), 8),
            (([[1, 2, 3]],), 4),
        ],
        hints=[
            "Both robots always sit in the same row, so the state is (row, column of robot A, column of robot B).",
            (
                "Moving the robots together row by row avoids the 'I already took that cherry' problem: only equal "
                "columns clash."
            ),
            (
                "dp[a][b] = best total with the robots at columns a and b; the next row's value comes from the 9 "
                "previous column pairs."
            ),
        ],
        pattern="DP over rows with the pair of column positions as state",
        explain=(
            "If we planned each robot's whole path separately we would have to remember which cherries were already "
            "taken. Moving both robots in lock-step row by row removes that: in a row the only possible overlap is "
            "when both are in the same column, so add that cell once. The state is (row, a, b) with a, b < cols, "
            "and each state has 3 x 3 predecessors, giving O(rows * cols^2 * 9). Only the previous row is needed, "
            "so two cols x cols tables suffice. The brute force explores all 9^rows move combinations with plain "
            "recursion."
        ),
        cx="O(rows * cols^2) time, O(cols^2) space",
        brute_cx="O(9^rows) time - plain recursion over every joint move, no memoisation",
        brute=r"""
# BRUTE FORCE: O(9^rows) time - plain recursion over every joint move, no memoisation
def cherry_pickup(grid):
    rows, cols = len(grid), len(grid[0])

    def go(r, a, b):
        if a < 0 or b < 0 or a >= cols or b >= cols:
            return float("-inf")
        gain = grid[r][a] + (grid[r][b] if a != b else 0)
        if r == rows - 1:
            return gain
        return gain + max(go(r + 1, a + da, b + db) for da in (-1, 0, 1) for db in (-1, 0, 1))

    return go(0, 0, cols - 1)
""",
        solution=r"""
# OPTIMISED: O(rows * cols^2) time, O(cols^2) space
# Idea: DP over rows with the pair of column positions as state
def cherry_pickup(grid):
    rows, cols = len(grid), len(grid[0])
    NEG = float("-inf")
    dp = [[NEG] * cols for _ in range(cols)]
    dp[0][cols - 1] = grid[0][0] + (grid[0][cols - 1] if cols > 1 else 0)
    for r in range(1, rows):
        nxt = [[NEG] * cols for _ in range(cols)]
        for a in range(cols):
            for b in range(cols):
                best = NEG
                for pa in (a - 1, a, a + 1):
                    for pb in (b - 1, b, b + 1):
                        if 0 <= pa < cols and 0 <= pb < cols and dp[pa][pb] > best:
                            best = dp[pa][pb]
                if best != NEG:
                    nxt[a][b] = best + grid[r][a] + (grid[r][b] if a != b else 0)
        dp = nxt
    return max(max(row) for row in dp)
""",
    ),
    # ---- Cyclically Rotating a Grid (LeetCode 1914) ----
    dict(
        title="Cyclically Rotating a Grid",
        diff="M",
        lc=1914,
        slug="cyclically-rotating-a-grid",
        prompt=(
            "grid is m x n with m and n both even, so it splits into concentric rectangular layers. One cyclic "
            "rotation moves every element of a layer one position counter-clockwise along that layer. Apply k "
            "rotations to every layer and return the grid."
        ),
        sig="def rotate_grid(grid: List[List[int]], k: int) -> List[List[int]]:",
        fn="rotate_grid",
        tests=[
            (([[40, 10], [30, 20]], 1), [[10, 20], [40, 30]]),
            (
                ([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]], 2),
                [[3, 4, 8, 12], [2, 11, 10, 16], [1, 7, 6, 15], [5, 9, 13, 14]],
            ),
            (([[1, 2], [3, 4]], 4), [[1, 2], [3, 4]]),
            (([[1, 2], [3, 4]], 3), [[3, 1], [4, 2]]),
        ],
        hints=[
            "Treat each layer as a circular list: read its cells clockwise from the top-left corner of that layer.",
            "Rotating counter-clockwise by one means every value moves one slot EARLIER in that clockwise list.",
            "A layer with L cells returns to itself after L rotations, so rotate by k % L only - once, with a slice.",
        ],
        pattern="Flatten each ring into a list, rotate by k mod length, write back",
        explain=(
            "Layer l occupies rows l..m-1-l and columns l..n-1-l. Listing its cells clockwise (top row, right "
            "column, bottom row backwards, left column upwards) turns it into a circular array. A counter-clockwise "
            "rotation by k is a left shift by k of that array, and shifting by L is a no-op, so only k % L matters. "
            "The brute force literally performs k single-step rotations; the optimised version does one slice per "
            "ring. The rings are independent, so they are processed one after another."
        ),
        cx="O(m * n) time, O(m + n) extra space per ring",
        brute_cx="O(k * m * n) time - repeat the one-step rotation k times",
        brute=r"""
# BRUTE FORCE: O(k * m * n) time - repeat the one-step rotation k times
def rotate_grid(grid, k):
    m, n = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    for layer in range(min(m, n) // 2):
        top, left, bottom, right = layer, layer, m - 1 - layer, n - 1 - layer
        cells = [(top, c) for c in range(left, right + 1)]
        cells += [(r, right) for r in range(top + 1, bottom + 1)]
        cells += [(bottom, c) for c in range(right - 1, left - 1, -1)]
        cells += [(r, left) for r in range(bottom - 1, top, -1)]
        for _ in range(k):
            values = [out[r][c] for r, c in cells]
            values = values[1:] + values[:1]
            for (r, c), v in zip(cells, values):
                out[r][c] = v
    return out
""",
        solution=r"""
# OPTIMISED: O(m * n) time, O(m + n) extra space per ring
# Idea: Flatten each ring into a list, rotate by k mod length, write back
def rotate_grid(grid, k):
    m, n = len(grid), len(grid[0])
    out = [row[:] for row in grid]
    for layer in range(min(m, n) // 2):
        top, left, bottom, right = layer, layer, m - 1 - layer, n - 1 - layer
        cells = [(top, c) for c in range(left, right + 1)]
        cells += [(r, right) for r in range(top + 1, bottom + 1)]
        cells += [(bottom, c) for c in range(right - 1, left - 1, -1)]
        cells += [(r, left) for r in range(bottom - 1, top, -1)]
        values = [grid[r][c] for r, c in cells]
        shift = k % len(values)
        values = values[shift:] + values[:shift]
        for (r, c), v in zip(cells, values):
            out[r][c] = v
    return out
""",
    ),
    # ---- Convert 1D Array Into 2D Array (LeetCode 2022) ----
    dict(
        title="Convert 1D Array Into 2D Array",
        diff="E",
        lc=2022,
        slug="convert-1d-array-into-2d-array",
        prompt=(
            "Build an m x n matrix from the 1D list original by filling the first row left to right with the first "
            "n elements, then the second row, and so on. If original does not have exactly m * n elements, return "
            "an empty list."
        ),
        sig="def construct_2d_array(original: List[int], m: int, n: int) -> List[List[int]]:",
        fn="construct_2d_array",
        tests=[
            (([1, 2, 3, 4], 2, 2), [[1, 2], [3, 4]]),
            (([1, 2, 3], 1, 3), [[1, 2, 3]]),
            (([1, 2], 1, 1), []),
            (([1, 2, 3, 4, 5, 6], 3, 2), [[1, 2], [3, 4], [5, 6]]),
        ],
        hints=[
            "First check that len(original) == m * n - otherwise the answer is [].",
            "Row r is the block of n consecutive elements starting at index r * n.",
            "Slice: original[r * n : (r + 1) * n] for r in range(m).",
        ],
        pattern="Row-major index arithmetic (cell k -> row k // n, column k % n)",
        explain=(
            "Row-major filling means element k lands at row k // n and column k % n. Equivalently, row r is the "
            "slice [r * n, (r + 1) * n). The only validity condition is the total count, so check it first and "
            "return an empty list on a mismatch."
        ),
        cx="O(m * n) time and space",
        brute_cx="O(m * n) time - place elements one at a time using // and %",
        brute=r"""
# BRUTE FORCE: O(m * n) time - place elements one at a time using // and %
def construct_2d_array(original, m, n):
    if len(original) != m * n:
        return []
    out = [[0] * n for _ in range(m)]
    for k, v in enumerate(original):
        out[k // n][k % n] = v
    return out
""",
        solution=r"""
# OPTIMISED: O(m * n) time and space
# Idea: Row-major index arithmetic (cell k -> row k // n, column k % n)
def construct_2d_array(original, m, n):
    if len(original) != m * n:
        return []
    return [original[r * n : (r + 1) * n] for r in range(m)]
""",
    ),
    # ---- Minimum Cost Homecoming of a Robot in a Grid (LeetCode 2087) ----
    dict(
        title="Minimum Cost Homecoming of a Robot in a Grid",
        diff="M",
        lc=2087,
        slug="minimum-cost-homecoming-of-a-robot-in-a-grid",
        prompt=(
            "A robot at start_pos = [r, c] must reach home_pos in a grid with len(row_costs) rows and "
            "len(col_costs) columns, moving one cell up/down/left/right per step. Entering row r' costs "
            "row_costs[r'] and entering column c' costs col_costs[c']. Return the minimum total cost."
        ),
        sig=(
            "def min_cost(start_pos: List[int], home_pos: List[int], row_costs: List[int], col_costs: List[int]) -> "
            "int:"
        ),
        fn="min_cost",
        tests=[
            (([1, 0], [2, 3], [5, 4, 3], [8, 2, 6, 7]), 18),
            (([0, 0], [0, 0], [5], [26]), 0),
            (([2, 0], [0, 0], [1, 2, 3], [4]), 3),
            (([0, 0], [1, 2], [1, 5], [3, 4, 7]), 16),
        ],
        hints=[
            "A step costs only for the row or column you ENTER, never for the one you leave.",
            "Any path from start to home must enter every row strictly between them and the home row at least once.",
            (
                "Detours only add cost, so take the straight path: add the entered rows' costs and the entered "
                "columns' costs."
            ),
        ],
        pattern="Costs depend only on the entered line - the Manhattan path is optimal",
        explain=(
            "Every shortest (Manhattan) path enters each row between the start row (exclusive) and the home row "
            "(inclusive) exactly once, and each column between the start column (exclusive) and the home column "
            "(inclusive) exactly once - and any path must enter at least these. Since all costs are non-negative, "
            "wandering elsewhere cannot help. So the answer is the sum of those row costs plus those column costs, "
            "independent of the order of moves. Dijkstra over the grid (the brute force) confirms the same value."
        ),
        cx="O(m + n) time, O(1) space",
        brute_cx="O(m * n * log(m * n)) time - Dijkstra over every grid cell",
        brute=r"""
# BRUTE FORCE: O(m * n * log(m * n)) time - Dijkstra over every grid cell
def min_cost(start_pos, home_pos, row_costs, col_costs):
    rows, cols = len(row_costs), len(col_costs)
    start = (start_pos[0], start_pos[1])
    home = (home_pos[0], home_pos[1])
    dist = {start: 0}
    heap = [(0, start[0], start[1])]
    while heap:
        d, r, c = heapq.heappop(heap)
        if (r, c) == home:
            return d
        if d > dist[(r, c)]:
            continue
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                nd = d + (row_costs[nr] if dr else col_costs[nc])
                if nd < dist.get((nr, nc), float("inf")):
                    dist[(nr, nc)] = nd
                    heapq.heappush(heap, (nd, nr, nc))
    return 0
""",
        solution=r"""
# OPTIMISED: O(m + n) time, O(1) space
# Idea: Costs depend only on the entered line - the Manhattan path is optimal
def min_cost(start_pos, home_pos, row_costs, col_costs):
    r0, c0 = start_pos
    r1, c1 = home_pos
    total = 0
    step = 1 if r1 > r0 else -1
    for r in range(r0 + step, r1 + step, step):
        total += row_costs[r]
    step = 1 if c1 > c0 else -1
    for c in range(c0 + step, c1 + step, step):
        total += col_costs[c]
    return total
""",
    ),
    # ---- Count Artifacts That Can Be Extracted (LeetCode 2201) ----
    dict(
        title="Count Artifacts That Can Be Extracted",
        diff="M",
        lc=2201,
        slug="count-artifacts-that-can-be-extracted",
        prompt=(
            "An n x n grid hides rectangular artifacts; artifact [r1, c1, r2, c2] covers the cells from its "
            "top-left (r1, c1) to its bottom-right (r2, c2) and each covers at most four cells. You dig the cells "
            "in dig (all distinct). An artifact can be extracted once ALL of its cells are dug. Return how many "
            "artifacts can be extracted."
        ),
        sig="def dig_artifacts(n: int, artifacts: List[List[int]], dig: List[List[int]]) -> int:",
        fn="dig_artifacts",
        tests=[
            ((2, [[0, 0, 0, 0], [0, 1, 1, 1]], [[0, 0], [0, 1]]), 1),
            ((2, [[0, 0, 0, 0], [0, 1, 1, 1]], [[0, 0], [0, 1], [1, 1]]), 2),
            ((3, [[0, 0, 1, 1]], [[0, 0], [0, 1], [1, 0]]), 0),
            ((3, [[0, 0, 1, 1]], [[0, 0], [0, 1], [1, 0], [1, 1]]), 1),
        ],
        hints=[
            "An artifact is extractable exactly when every one of its cells has been dug.",
            (
                "Each artifact has at most 4 cells, so checking one costs O(1) if you can ask 'was this cell dug?' "
                "quickly."
            ),
            "Store the dug cells in a hash set of (row, col) and test each artifact's cells against it.",
        ],
        pattern="Hash set membership instead of an n x n board",
        explain=(
            "n can be large (up to 1000), so allocating an n x n boolean board costs O(n^2) memory even if only a "
            "few cells are dug. Because each artifact has at most four cells, a set of dug coordinates answers "
            "every membership test in O(1), giving O(dig + artifacts) time and space. The brute force builds the "
            "full board."
        ),
        cx="O(len(dig) + len(artifacts)) time and space",
        brute_cx="O(n^2 + len(dig) + total artifact area) time and O(n^2) space - build the whole n x n board",
        brute=r"""
# BRUTE FORCE: O(n^2 + len(dig) + total artifact area) time and O(n^2) space - build the whole n x n board
def dig_artifacts(n, artifacts, dig):
    board = [[False] * n for _ in range(n)]
    for r, c in dig:
        board[r][c] = True
    count = 0
    for r1, c1, r2, c2 in artifacts:
        if all(board[r][c] for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)):
            count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(len(dig) + len(artifacts)) time and space
# Idea: Hash set membership instead of an n x n board
def dig_artifacts(n, artifacts, dig):
    dug = {(r, c) for r, c in dig}
    count = 0
    for r1, c1, r2, c2 in artifacts:
        if all((r, c) in dug for r in range(r1, r2 + 1) for c in range(c1, c2 + 1)):
            count += 1
    return count
""",
    ),
    # ---- Delete Greatest Value in Each Row (LeetCode 2500) ----
    dict(
        title="Delete Greatest Value in Each Row",
        diff="E",
        lc=2500,
        slug="delete-greatest-value-in-each-row",
        prompt=(
            "Repeat until the grid is empty: from every row delete its greatest element, then add the largest of "
            "the values you just deleted to the answer. Return the answer."
        ),
        sig="def delete_greatest_value(grid: List[List[int]]) -> int:",
        fn="delete_greatest_value",
        tests=[
            (([[1, 2, 4], [3, 3, 1]],), 8),
            (([[10]],), 10),
            (([[1, 2], [3, 4]],), 7),
            (([[5, 5], [1, 1]],), 10),
        ],
        hints=[
            "Each round removes one element per row, always the current maximum of that row.",
            "If every row were sorted, round t would remove the t-th largest element of each row.",
            "Sort each row; the answer is the sum over columns of the maximum of that column.",
        ],
        pattern="Sort rows, then take column-wise maxima",
        explain=(
            "Deleting the greatest remaining value of a row, again and again, walks that row from its largest value "
            "down to its smallest. After sorting every row, round t deletes the t-th largest value of each row, "
            "i.e. one whole column of the sorted grid, and the round scores the maximum of that column. So sort "
            "each row and add up the column maxima. Simulating the deletions directly also works but re-scans every "
            "row each round."
        ),
        cx="O(m * n log n) time, O(1) extra space",
        brute_cx="O(m * n^2) time - find and remove the maximum of every row in every round",
        brute=r"""
# BRUTE FORCE: O(m * n^2) time - find and remove the maximum of every row in every round
def delete_greatest_value(grid):
    rows = [row[:] for row in grid]
    total = 0
    for _ in range(len(rows[0])):
        biggest = 0
        for row in rows:
            top = max(row)
            row.remove(top)
            biggest = max(biggest, top)
        total += biggest
    return total
""",
        solution=r"""
# OPTIMISED: O(m * n log n) time, O(1) extra space
# Idea: Sort rows, then take column-wise maxima
def delete_greatest_value(grid):
    rows = [sorted(row) for row in grid]
    return sum(max(col) for col in zip(*rows))
""",
    ),
    # ---- Check Knight Tour Configuration (LeetCode 2596) ----
    dict(
        title="Check Knight Tour Configuration",
        diff="M",
        lc=2596,
        slug="check-knight-tour-configuration",
        prompt=(
            "grid is n x n and holds each number 0..n*n-1 exactly once: grid[r][c] says in which step a knight "
            "visited cell (r, c). Return true if this is a valid knight's tour: the knight starts in the top-left "
            "cell (step 0) and every move from step k to step k + 1 is a legal knight move."
        ),
        sig="def check_valid_grid(grid: List[List[int]]) -> bool:",
        fn="check_valid_grid",
        tests=[
            (
                ([[0, 11, 16, 5, 20], [17, 4, 19, 10, 15], [12, 1, 8, 21, 6], [3, 18, 23, 14, 9], [24, 13, 2, 7, 22]],),
                True,
            ),
            (([[0, 3, 6], [5, 8, 1], [2, 7, 4]],), False),
            (([[1]],), False),
            (([[0]],), True),
        ],
        hints=[
            "The tour must start with step 0 in the top-left cell - check that first.",
            (
                "A knight move changes (row, column) by (+-1, +-2) or (+-2, +-1): the absolute differences, sorted, "
                "are [1, 2]."
            ),
            (
                "Record where each step number sits (position[step] = (row, col)), then check each consecutive pair "
                "of steps."
            ),
        ],
        pattern="Invert the grid into step -> position, then validate neighbours in the sequence",
        explain=(
            "The grid maps position -> step, but the knight rule talks about consecutive steps. Inverting it into "
            "pos[step] = (r, c) in one pass makes each check O(1): |dr| and |dc| must be {1, 2} in some order. "
            "Because the input is a permutation of 0..n*n-1, every step exists exactly once. The brute force "
            "re-searches the whole board for each step number, costing O(n^4)."
        ),
        cx="O(n^2) time and space",
        brute_cx="O(n^4) time - search the whole board for step k and step k + 1 every time",
        brute=r"""
# BRUTE FORCE: O(n^4) time - search the whole board for step k and step k + 1 every time
def check_valid_grid(grid):
    n = len(grid)
    if grid[0][0] != 0:
        return False

    def find(v):
        for r in range(n):
            for c in range(n):
                if grid[r][c] == v:
                    return r, c
        return None

    for k in range(n * n - 1):
        a, b = find(k), find(k + 1)
        if a is None or b is None:
            return False
        if sorted((abs(a[0] - b[0]), abs(a[1] - b[1]))) != [1, 2]:
            return False
    return True
""",
        solution=r"""
# OPTIMISED: O(n^2) time and space
# Idea: Invert the grid into step -> position, then validate neighbours in the sequence
def check_valid_grid(grid):
    n = len(grid)
    if grid[0][0] != 0:
        return False
    pos = [None] * (n * n)
    for r in range(n):
        for c in range(n):
            pos[grid[r][c]] = (r, c)
    for k in range(n * n - 1):
        dr = abs(pos[k][0] - pos[k + 1][0])
        dc = abs(pos[k][1] - pos[k + 1][1])
        if sorted((dr, dc)) != [1, 2]:
            return False
    return True
""",
    ),
    # ---- Difference of Number of Distinct Values on Diagonals (LeetCode 2711) ----
    dict(
        title="Difference of Number of Distinct Values on Diagonals",
        diff="M",
        lc=2711,
        slug="difference-of-number-of-distinct-values-on-diagonals",
        prompt=(
            "For each cell (r, c), let left_above be the number of DISTINCT values on the diagonal cells strictly "
            "above-left of it and right_below the number of distinct values strictly below-right of it (same "
            "diagonal). Return a matrix whose (r, c) entry is |left_above - right_below|."
        ),
        sig="def difference_of_distinct_values(grid: List[List[int]]) -> List[List[int]]:",
        fn="difference_of_distinct_values",
        tests=[
            (([[1, 2, 3], [3, 1, 5], [3, 2, 1]],), [[1, 1, 0], [1, 0, 1], [0, 1, 1]]),
            (([[1]],), [[0]]),
            (([[1, 1], [1, 1]],), [[1, 0], [0, 1]]),
            (([[1, 2]],), [[0, 0]]),
        ],
        hints=[
            "Cells on the same top-left-to-bottom-right diagonal share r - c; the diagonals are independent problems.",
            "Along one diagonal, 'distinct values before position k' is a running set size from the left.",
            (
                "Do one pass left-to-right storing the set size before each cell, and one pass right-to-left for "
                "the size after it."
            ),
        ],
        pattern="Prefix / suffix distinct counts along each diagonal",
        explain=(
            "Within a diagonal the cells form a 1D array, and the question becomes: for each index k, how many "
            "distinct values lie before it and after it? A running set gives the count before k in one forward "
            "pass; a second pass from the end gives the count after k. Doing this for every diagonal touches each "
            "cell a constant number of times. The brute force rebuilds both sets for every cell, costing O(min(m, "
            "n)) per cell."
        ),
        cx="O(m * n) time, O(min(m, n)) extra space per diagonal",
        brute_cx="O(m * n * min(m, n)) time - walk both directions from every cell",
        brute=r"""
# BRUTE FORCE: O(m * n * min(m, n)) time - walk both directions from every cell
def difference_of_distinct_values(grid):
    m, n = len(grid), len(grid[0])
    out = [[0] * n for _ in range(m)]
    for r in range(m):
        for c in range(n):
            before, after = set(), set()
            x, y = r - 1, c - 1
            while x >= 0 and y >= 0:
                before.add(grid[x][y])
                x -= 1
                y -= 1
            x, y = r + 1, c + 1
            while x < m and y < n:
                after.add(grid[x][y])
                x += 1
                y += 1
            out[r][c] = abs(len(before) - len(after))
    return out
""",
        solution=r"""
# OPTIMISED: O(m * n) time, O(min(m, n)) extra space per diagonal
# Idea: Prefix / suffix distinct counts along each diagonal
def difference_of_distinct_values(grid):
    m, n = len(grid), len(grid[0])
    out = [[0] * n for _ in range(m)]
    starts = [(0, c) for c in range(n)] + [(r, 0) for r in range(1, m)]
    for r0, c0 in starts:
        cells = []
        r, c = r0, c0
        while r < m and c < n:
            cells.append((r, c))
            r += 1
            c += 1
        size = len(cells)
        before = [0] * size
        seen = set()
        for k in range(size):
            before[k] = len(seen)
            seen.add(grid[cells[k][0]][cells[k][1]])
        seen = set()
        for k in range(size - 1, -1, -1):
            after = len(seen)
            out[cells[k][0]][cells[k][1]] = abs(before[k] - after)
            seen.add(grid[cells[k][0]][cells[k][1]])
    return out
""",
    ),
    # ---- Construct Product Matrix (LeetCode 2906) ----
    dict(
        title="Construct Product Matrix",
        diff="M",
        lc=2906,
        slug="construct-product-matrix",
        prompt=(
            "For an n x m matrix grid, build p where p[i][j] is the product of ALL other elements of grid (every "
            "element except grid[i][j]), taken modulo 12345. Division is not allowed - and 12345 is not prime, so "
            "modular inverses may not exist."
        ),
        sig="def construct_product_matrix(grid: List[List[int]]) -> List[List[int]]:",
        fn="construct_product_matrix",
        tests=[
            (([[1, 2], [3, 4]],), [[24, 12], [8, 6]]),
            (([[12345], [2], [1]],), [[2], [0], [0]]),
            (([[2, 3]],), [[3, 2]]),
            (([[7]],), [[1]]),
        ],
        hints=[
            "Flatten the matrix in row-major order: the task becomes 'product of the array except itself'.",
            "Division fails (zero or non-invertible values mod 12345), so use prefix products and suffix products.",
            "answer[i] = prefix[i] * suffix[i + 1] modulo 12345; compute the suffix on the fly in a backward sweep.",
        ],
        pattern="Prefix * suffix products (product of array except self) under a modulus",
        explain=(
            "The classic trick for 'product except self' avoids division: the product of everything before position "
            "i (prefix) times the product of everything after it (suffix). Reducing mod 12345 after every "
            "multiplication keeps numbers small, and since modular multiplication is associative the order does not "
            "matter. Flatten the grid so that 'before' and 'after' are well defined, then fold the result back into "
            "rows. A zero or a multiple of 12345 simply makes the relevant products 0 - no special case needed."
        ),
        cx="O(n * m) time and space",
        brute_cx="O((n * m)^2) time - multiply all other elements for every cell",
        brute=r"""
# BRUTE FORCE: O((n * m)^2) time - multiply all other elements for every cell
def construct_product_matrix(grid):
    mod = 12345
    n, m = len(grid), len(grid[0])
    flat = [v for row in grid for v in row]
    out_flat = []
    for i in range(len(flat)):
        p = 1
        for j in range(len(flat)):
            if j != i:
                p = p * flat[j] % mod
        out_flat.append(p)
    return [out_flat[i * m : (i + 1) * m] for i in range(n)]
""",
        solution=r"""
# OPTIMISED: O(n * m) time and space
# Idea: Prefix * suffix products (product of array except self) under a modulus
def construct_product_matrix(grid):
    mod = 12345
    n, m = len(grid), len(grid[0])
    flat = [v for row in grid for v in row]
    total = len(flat)
    prefix = [1] * (total + 1)
    for i, v in enumerate(flat):
        prefix[i + 1] = prefix[i] * v % mod
    out_flat = [0] * total
    suffix = 1
    for i in range(total - 1, -1, -1):
        out_flat[i] = prefix[i] * suffix % mod
        suffix = suffix * flat[i] % mod
    return [out_flat[i * m : (i + 1) * m] for i in range(n)]
""",
    ),
    # ---- Check if Grid Satisfies Conditions (LeetCode 3142) ----
    dict(
        title="Check if Grid Satisfies Conditions",
        diff="E",
        lc=3142,
        slug="check-if-grid-satisfies-conditions",
        prompt=(
            "Return true if every cell satisfies BOTH rules: it equals the cell directly below it (if there is "
            "one), and it differs from the cell directly to its right (if there is one)."
        ),
        sig="def satisfies_conditions(grid: List[List[int]]) -> bool:",
        fn="satisfies_conditions",
        tests=[
            (([[1, 0, 2], [1, 0, 2]],), True),
            (([[1, 1, 1], [0, 0, 0]],), False),
            (([[1], [2], [3]],), False),
            (([[5]],), True),
        ],
        hints=[
            "The 'equal to the cell below' rule, applied down a whole column, forces every column to be constant.",
            "So the grid is fully described by its first row; only that row needs the 'differs from the right' rule.",
            "Check every column against the first row's value, and compare neighbouring entries of the first row.",
        ],
        pattern="Collapse a local rule into a global invariant (constant columns)",
        explain=(
            "Equality with the cell below chains down each column, so all cells of a column are equal to its top "
            "cell. Then 'differs from the right neighbour' only has to be verified on one row, because every row "
            "repeats the same values. One scan checks column constancy and compares adjacent top-row cells. The "
            "brute force literally compares every pair of cells and applies the two rules to the adjacent ones."
        ),
        cx="O(m * n) time, O(1) space",
        brute_cx="O((m * n)^2) time - test every pair of cells against the two rules",
        brute=r"""
# BRUTE FORCE: O((m * n)^2) time - test every pair of cells against the two rules
def satisfies_conditions(grid):
    m, n = len(grid), len(grid[0])
    cells = [(i, j) for i in range(m) for j in range(n)]
    for a, b in cells:
        for c, d in cells:
            if b == d and c == a + 1 and grid[a][b] != grid[c][d]:
                return False
            if a == c and d == b + 1 and grid[a][b] == grid[c][d]:
                return False
    return True
""",
        solution=r"""
# OPTIMISED: O(m * n) time, O(1) space
# Idea: Collapse a local rule into a global invariant (constant columns)
def satisfies_conditions(grid):
    m, n = len(grid), len(grid[0])
    for j in range(n):
        for i in range(1, m):
            if grid[i][j] != grid[0][j]:
                return False
        if j + 1 < n and grid[0][j] == grid[0][j + 1]:
            return False
    return True
""",
    ),
    # ---- Maximum Difference Score in a Grid (LeetCode 3148) ----
    dict(
        title="Maximum Difference Score in a Grid",
        diff="M",
        lc=3148,
        slug="maximum-difference-score-in-a-grid",
        prompt=(
            "From any start cell you may make one or more moves; each move goes to ANY cell strictly below it in "
            "the same column or strictly to its right in the same row (not necessarily adjacent). A move from value "
            "x to value y scores y - x. Return the maximum total score over all paths with at least one move."
        ),
        sig="def max_score(grid: List[List[int]]) -> int:",
        fn="max_score",
        tests=[
            (([[9, 5, 7, 3], [8, 9, 6, 1], [6, 7, 14, 3], [2, 5, 3, 1]],), 9),
            (([[4, 3, 2], [3, 2, 1]],), -1),
            (([[1, 2]],), 1),
            (([[5], [3]],), -2),
        ],
        hints=[
            "The scores along a path telescope: (b - a) + (c - b) = c - a, so only the start and end values matter.",
            (
                "So the answer is max over pairs (start, end) with end below-right of start (not equal cells) of "
                "end - start."
            ),
            (
                "For each cell as the END, you want the smallest value in the rectangle above-left of it; keep a "
                "running 2D minimum."
            ),
        ],
        pattern="Telescoping sum, then a 2D running minimum DP",
        explain=(
            "Every intermediate value cancels, so a path from s to t scores t - s regardless of the route, and a "
            "single move already achieves it. We want max (t - s) over cells where t is weakly below and weakly "
            "right of s but t != s. Let mn[i][j] = min of all cells in rows <= i and columns <= j. For end cell (i, "
            "j) the best start is min(mn[i-1][j], mn[i][j-1]), which covers every rectangle cell except (i, j) "
            "itself. One pass fills mn and updates the answer. The brute force tries all start/end pairs."
        ),
        cx="O(m * n) time, O(n) extra space",
        brute_cx="O((m * n)^2) time - try every start cell with every reachable end cell",
        brute=r"""
# BRUTE FORCE: O((m * n)^2) time - try every start cell with every reachable end cell
def max_score(grid):
    m, n = len(grid), len(grid[0])
    best = float("-inf")
    for i in range(m):
        for j in range(n):
            for x in range(i, m):
                for y in range(j, n):
                    if (x, y) != (i, j):
                        best = max(best, grid[x][y] - grid[i][j])
    return best
""",
        solution=r"""
# OPTIMISED: O(m * n) time, O(n) extra space
# Idea: Telescoping sum, then a 2D running minimum DP
def max_score(grid):
    m, n = len(grid), len(grid[0])
    inf = float("inf")
    best = float("-inf")
    prev = [inf] * n
    for i in range(m):
        cur = [inf] * n
        for j in range(n):
            above = prev[j]
            left = cur[j - 1] if j > 0 else inf
            smallest = min(above, left)
            if smallest != inf:
                best = max(best, grid[i][j] - smallest)
            cur[j] = min(grid[i][j], smallest)
        prev = cur
    return best
""",
    ),
    # ---- Find the Minimum Area to Cover All Ones I (LeetCode 3195) ----
    dict(
        title="Find the Minimum Area to Cover All Ones I",
        diff="M",
        lc=3195,
        slug="find-the-minimum-area-to-cover-all-ones-i",
        prompt=(
            "grid is a binary matrix with at least one 1. Return the smallest area of an axis-aligned rectangle, "
            "with its sides along the grid lines, that contains all the 1s."
        ),
        sig="def minimum_area(grid: List[List[int]]) -> int:",
        fn="minimum_area",
        tests=[
            (([[0, 1, 0], [1, 0, 1]],), 6),
            (([[1, 0], [0, 0]],), 1),
            (([[0, 0, 1], [0, 0, 0]],), 1),
            (([[1, 1], [1, 1]],), 4),
        ],
        hints=[
            "A rectangle covers all the 1s exactly when it contains the topmost, bottommost, leftmost and rightmost 1.",
            "You do not need to try rectangles: the smallest one is forced by those four extremes.",
            "Track min/max row and min/max column among the 1s; the answer is (maxR - minR + 1) * (maxC - minC + 1).",
        ],
        pattern="Bounding box of the points",
        explain=(
            "Any rectangle containing all 1s must reach the minimum row, maximum row, minimum column and maximum "
            "column that occur among the 1s - and the rectangle spanning exactly those extremes already contains "
            "every 1, so it is the smallest. One scan finds the four extremes. The brute force tries every "
            "rectangle, checks that it holds all the 1s and keeps the smallest area."
        ),
        cx="O(m * n) time, O(1) space",
        brute_cx="O(m^2 * n^2 * m * n) time - try every rectangle and count the 1s inside",
        brute=r"""
# BRUTE FORCE: O(m^2 * n^2 * m * n) time - try every rectangle and count the 1s inside
def minimum_area(grid):
    m, n = len(grid), len(grid[0])
    ones = sum(map(sum, grid))
    best = m * n
    for r1 in range(m):
        for r2 in range(r1, m):
            for c1 in range(n):
                for c2 in range(c1, n):
                    inside = sum(grid[r][c] for r in range(r1, r2 + 1) for c in range(c1, c2 + 1))
                    if inside == ones:
                        best = min(best, (r2 - r1 + 1) * (c2 - c1 + 1))
    return best
""",
        solution=r"""
# OPTIMISED: O(m * n) time, O(1) space
# Idea: Bounding box of the points
def minimum_area(grid):
    rows = [r for r, row in enumerate(grid) if any(row)]
    cols = [c for c in range(len(grid[0])) if any(row[c] for row in grid)]
    return (rows[-1] - rows[0] + 1) * (cols[-1] - cols[0] + 1)
""",
    ),
    # ---- Count Submatrices With Equal Frequency of X and Y (LeetCode 3212) ----
    dict(
        title="Count Submatrices With Equal Frequency of X and Y",
        diff="M",
        lc=3212,
        slug="count-submatrices-with-equal-frequency-of-x-and-y",
        prompt=(
            "grid holds the characters 'X', 'Y' and '.'. Count the submatrices that contain the top-left cell "
            "grid[0][0], have equally many 'X' and 'Y', and contain at least one 'X'."
        ),
        sig="def number_of_submatrices(grid: List[List[str]]) -> int:",
        fn="number_of_submatrices",
        tests=[
            (([["X", "Y", "."], ["Y", ".", "."]],), 3),
            (([["X", "X"], ["X", "Y"]],), 0),
            (([[".", "."], [".", "."]],), 0),
            (([["X", "Y"]],), 1),
            (([["X"], ["Y"]],), 1),
        ],
        hints=[
            (
                "A submatrix that contains (0, 0) is fully described by its bottom-right corner (i, j) - there are "
                "m * n choices."
            ),
            "For each corner you need the number of X and Y in the rectangle (0, 0)..(i, j).",
            "Maintain two 2D prefix-sum tables (for X and Y) and count the corners with x == y and x > 0.",
        ],
        pattern="2D prefix counts anchored at the origin",
        explain=(
            "Every valid submatrix has (0, 0) as its top-left corner, so it is determined by its bottom-right "
            "corner. Let cx[i][j] and cy[i][j] be the number of X and Y in the prefix rectangle; each is built in "
            "O(1) per cell by inclusion-exclusion. A corner counts when cx == cy and cx > 0. The brute force "
            "recounts the whole rectangle for every corner."
        ),
        cx="O(m * n) time and space",
        brute_cx="O((m * n)^2) time - recount every prefix rectangle from scratch",
        brute=r"""
# BRUTE FORCE: O((m * n)^2) time - recount every prefix rectangle from scratch
def number_of_submatrices(grid):
    m, n = len(grid), len(grid[0])
    count = 0
    for i in range(m):
        for j in range(n):
            x = y = 0
            for r in range(i + 1):
                for c in range(j + 1):
                    if grid[r][c] == "X":
                        x += 1
                    elif grid[r][c] == "Y":
                        y += 1
            if x == y and x > 0:
                count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(m * n) time and space
# Idea: 2D prefix counts anchored at the origin
def number_of_submatrices(grid):
    m, n = len(grid), len(grid[0])
    cx = [[0] * (n + 1) for _ in range(m + 1)]
    cy = [[0] * (n + 1) for _ in range(m + 1)]
    count = 0
    for i in range(m):
        for j in range(n):
            cx[i + 1][j + 1] = cx[i][j + 1] + cx[i + 1][j] - cx[i][j] + (grid[i][j] == "X")
            cy[i + 1][j + 1] = cy[i][j + 1] + cy[i + 1][j] - cy[i][j] + (grid[i][j] == "Y")
            if cx[i + 1][j + 1] == cy[i + 1][j + 1] and cx[i + 1][j + 1] > 0:
                count += 1
    return count
""",
    ),
    # ---- Snake in Matrix (LeetCode 3248) ----
    dict(
        title="Snake in Matrix",
        diff="E",
        lc=3248,
        slug="snake-in-matrix",
        prompt=(
            "An n x n matrix numbers its cells grid[i][j] = i * n + j. A snake starts in cell 0 (top-left) and "
            "obeys a list of commands 'UP', 'DOWN', 'LEFT', 'RIGHT'; it never leaves the matrix. Return the number "
            "of the cell where the snake ends."
        ),
        sig="def final_position_of_snake(n: int, commands: List[str]) -> int:",
        fn="final_position_of_snake",
        tests=[
            ((2, ["RIGHT", "DOWN"]), 3),
            ((3, ["DOWN", "RIGHT", "UP"]), 1),
            ((2, ["DOWN", "RIGHT"]), 3),
            ((3, ["RIGHT", "RIGHT", "DOWN"]), 5),
        ],
        hints=[
            "Track the snake as a (row, column) pair starting at (0, 0).",
            "UP / DOWN change the row by -1 / +1, LEFT / RIGHT change the column by -1 / +1.",
            "At the end, the cell number is row * n + column - no matrix needs to be built.",
        ],
        pattern="Simulate with coordinates; map back with row * n + col",
        explain=(
            "Because the cell numbers are row-major, cell (r, c) is just r * n + c, so we never need the matrix. "
            "Walking the commands updates r and c in O(1) each, and the problem guarantees the snake stays in "
            "bounds. The brute force builds the numbered matrix and reads the final value out of it."
        ),
        cx="O(len(commands)) time, O(1) space",
        brute_cx="O(n^2 + len(commands)) time and O(n^2) space - build the numbered matrix first",
        brute=r"""
# BRUTE FORCE: O(n^2 + len(commands)) time and O(n^2) space - build the numbered matrix first
def final_position_of_snake(n, commands):
    grid = [[i * n + j for j in range(n)] for i in range(n)]
    r = c = 0
    for cmd in commands:
        if cmd == "UP":
            r -= 1
        elif cmd == "DOWN":
            r += 1
        elif cmd == "LEFT":
            c -= 1
        else:
            c += 1
    return grid[r][c]
""",
        solution=r"""
# OPTIMISED: O(len(commands)) time, O(1) space
# Idea: Simulate with coordinates; map back with row * n + col
def final_position_of_snake(n, commands):
    r = c = 0
    for cmd in commands:
        if cmd == "UP":
            r -= 1
        elif cmd == "DOWN":
            r += 1
        elif cmd == "LEFT":
            c -= 1
        else:
            c += 1
    return r * n + c
""",
    ),
]
