"""extra batch of Matrix / Grid problems - the problem bank for the "matrix" topic (batch 5).

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
    # ---- Reshape the Matrix (LeetCode 566) ----
    dict(
        title="Reshape the Matrix",
        diff="E",
        lc=566,
        slug="reshape-the-matrix",
        prompt=(
            "Reshape the m x n matrix mat into an r x c matrix, reading and writing in row-major order. If the "
            "reshape is impossible (different number of cells), return mat unchanged."
        ),
        sig="def matrix_reshape(mat: List[List[int]], r: int, c: int) -> List[List[int]]:",
        fn="matrix_reshape",
        tests=[
            (([[1, 2], [3, 4]], 1, 4), [[1, 2, 3, 4]]),
            (([[1, 2], [3, 4]], 2, 4), [[1, 2], [3, 4]]),
            (([[1, 2, 3]], 3, 1), [[1], [2], [3]]),
            (([[1, 2], [3, 4]], 4, 1), [[1], [2], [3], [4]]),
        ],
        hints=[
            "A reshape is only possible when m * n == r * c.",
            "Think of the matrix as one long list: cell k of that list is row k // width, column k % width.",
            "For every k, copy mat[k // n][k % n] into out[k // c][k % c].",
        ],
        pattern="Flat index <-> (row, column) conversion with // and %",
        explain=(
            "Row-major order numbers the cells 0..m*n-1; cell k sits at (k // n, k % n) in an n-column matrix and "
            "at (k // c, k % c) in a c-column one. Copying cell k from the old coordinates to the new ones reshapes "
            "the matrix without building an intermediate list."
        ),
        cx="O(m * n) time, O(m * n) output space",
        brute_cx="O(m * n) time and an extra flat list - flatten first, then cut into rows",
        brute=r"""
# BRUTE FORCE: O(m * n) time and an extra flat list - flatten first, then cut into rows
def matrix_reshape(mat, r, c):
    flat = [x for row in mat for x in row]
    if len(flat) != r * c:
        return mat
    return [flat[i * c : (i + 1) * c] for i in range(r)]
""",
        solution=r"""
# OPTIMISED: O(m * n) time, O(m * n) output space
# Idea: Flat index <-> (row, column) conversion with // and %
def matrix_reshape(mat, r, c):
    m, n = len(mat), len(mat[0])
    if m * n != r * c:
        return mat
    out = [[0] * c for _ in range(r)]
    for k in range(m * n):
        out[k // c][k % c] = mat[k // n][k % n]
    return out
""",
    ),
    # ---- Image Overlap (LeetCode 835) ----
    dict(
        title="Image Overlap",
        diff="M",
        lc=835,
        slug="image-overlap",
        prompt=(
            "img1 and img2 are n x n binary matrices. You may slide (translate, no rotation) img1 over img2 in any "
            "direction; cells that move outside are dropped. Return the largest number of positions where both "
            "images have a 1 after some translation."
        ),
        sig="def largest_overlap(img1: List[List[int]], img2: List[List[int]]) -> int:",
        fn="largest_overlap",
        tests=[
            (([[1, 1, 0], [0, 1, 0], [0, 1, 0]], [[0, 0, 0], [0, 1, 1], [0, 0, 1]]), 3),
            (([[1]], [[1]]), 1),
            (([[0]], [[0]]), 0),
            (([[1, 0], [0, 0]], [[0, 0], [0, 1]]), 1),
        ],
        hints=[
            "Trying every shift and recounting the overlap costs O(n^4).",
            "A shift (dx, dy) makes a 1 from img1 land on a 1 from img2 exactly when (x2 - x1, y2 - y1) == (dx, dy).",
            (
                "List the 1s of each image, count the difference vector of every pair of 1s in a dictionary; the "
                "most common vector is the answer."
            ),
        ],
        pattern="Count translation vectors between pairs of points",
        explain=(
            "A translation aligns a 1 of img1 with a 1 of img2 precisely for the pairs whose coordinate difference "
            "equals that translation. So the overlap for translation t equals the number of pairs with difference "
            "t, and the best translation is the most frequent difference. Only the 1s matter, so the work is (ones "
            "in img1) * (ones in img2)."
        ),
        cx="O(k1 * k2) time with k1, k2 = number of ones; O(k1 * k2) space",
        brute_cx="O(n^4) time - try every translation and count overlapping ones",
        brute=r"""
# BRUTE FORCE: O(n^4) time - try every translation and count overlapping ones
def largest_overlap(img1, img2):
    n = len(img1)
    best = 0
    for dx in range(-n + 1, n):
        for dy in range(-n + 1, n):
            count = 0
            for i in range(n):
                for j in range(n):
                    if 0 <= i + dx < n and 0 <= j + dy < n and img1[i][j] and img2[i + dx][j + dy]:
                        count += 1
            best = max(best, count)
    return best
""",
        solution=r"""
# OPTIMISED: O(k1 * k2) time with k1, k2 = number of ones; O(k1 * k2) space
# Idea: Count translation vectors between pairs of points
def largest_overlap(img1, img2):
    n = len(img1)
    ones1 = [(i, j) for i in range(n) for j in range(n) if img1[i][j]]
    ones2 = [(i, j) for i in range(n) for j in range(n) if img2[i][j]]
    shifts = Counter((c - a, d - b) for a, b in ones1 for c, d in ones2)
    return max(shifts.values(), default=0)
""",
    ),
    # ---- Projection Area of 3D Shapes (LeetCode 883) ----
    dict(
        title="Projection Area of 3D Shapes",
        diff="E",
        lc=883,
        slug="projection-area-of-3d-shapes",
        prompt=(
            "grid[i][j] is the height of a tower of unit cubes on cell (i, j). Return the total area of the shadows "
            "(projections) onto the xy plane (top), the yz plane (front) and the zx plane (side)."
        ),
        sig="def projection_area(grid: List[List[int]]) -> int:",
        fn="projection_area",
        tests=[
            (([[1, 2], [3, 4]],), 17),
            (([[2]],), 5),
            (([[1, 0], [0, 2]],), 8),
            (([[0]],), 0),
        ],
        hints=[
            "Top view: one unit of area for every non-empty cell.",
            (
                "Front view: the shadow of each row is as tall as its tallest tower; side view: each column's "
                "tallest tower."
            ),
            "Answer = (cells > 0) + sum of row maximums + sum of column maximums.",
        ],
        pattern="Three independent projections: count, row max, column max",
        explain=(
            "Seen from above a cell is dark if it holds any cube. Seen from the front, each row is a silhouette as "
            "tall as its tallest tower, and from the side each column is as tall as its tallest tower. Adding the "
            "three areas gives the answer."
        ),
        cx="O(n^2) time, O(1) extra space",
        brute_cx="O(n^2 * h) time - build every unit cube and count distinct shadow cells per plane",
        brute=r"""
# BRUTE FORCE: O(n^2 * h) time - build every unit cube and count distinct shadow cells per plane
def projection_area(grid):
    cubes = [(i, j, k) for i, row in enumerate(grid) for j, h in enumerate(row) for k in range(h)]
    top = {(i, j) for i, j, _ in cubes}
    front = {(i, k) for i, _, k in cubes}
    side = {(j, k) for _, j, k in cubes}
    return len(top) + len(front) + len(side)
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(1) extra space
# Idea: Three independent projections: count, row max, column max
def projection_area(grid):
    top = sum(1 for row in grid for h in row if h)
    rows = sum(max(row) for row in grid)
    cols = sum(max(col) for col in zip(*grid))
    return top + rows + cols
""",
    ),
    # ---- Surface Area of 3D Shapes (LeetCode 892) ----
    dict(
        title="Surface Area of 3D Shapes",
        diff="E",
        lc=892,
        slug="surface-area-of-3d-shapes",
        prompt=(
            "grid[i][j] is the number of unit cubes stacked on cell (i, j). The towers touch their neighbours. "
            "Return the total surface area of the resulting solid, including the bottom faces."
        ),
        sig="def surface_area(grid: List[List[int]]) -> int:",
        fn="surface_area",
        tests=[
            (([[1, 2], [3, 4]],), 34),
            (([[1, 1, 1], [1, 0, 1], [1, 1, 1]],), 32),
            (([[2, 2, 2], [2, 1, 2], [2, 2, 2]],), 46),
            (([[2]],), 10),
            (([[0]],), 0),
        ],
        hints=[
            "A single tower of height v (v > 0) has 4v side faces plus a top and a bottom: 4v + 2.",
            (
                "Two touching towers hide faces from each other: the smaller one's whole side facing the other, on "
                "both towers."
            ),
            (
                "For every pair of neighbouring cells subtract 2 * min(v1, v2). Check each pair once (right and "
                "down neighbours)."
            ),
        ],
        pattern="Sum of independent towers minus hidden shared faces",
        explain=(
            "Start with every tower as if it stood alone: 4v + 2 faces for v > 0. When two towers are neighbours, a "
            "contact area of min(v1, v2) unit squares is glued shut on each side, removing 2 * min(v1, v2) faces. "
            "Considering each neighbouring pair once avoids double subtraction."
        ),
        cx="O(n^2) time, O(1) space",
        brute_cx="O(n^2 * h) time - make a set of cubes and count faces whose neighbour cell is empty",
        brute=r"""
# BRUTE FORCE: O(n^2 * h) time - make a set of cubes and count faces whose neighbour cell is empty
def surface_area(grid):
    cubes = {(i, j, k) for i, row in enumerate(grid) for j, h in enumerate(row) for k in range(h)}
    faces = 0
    for i, j, k in cubes:
        for di, dj, dk in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)):
            if (i + di, j + dj, k + dk) not in cubes:
                faces += 1
    return faces
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(1) space
# Idea: Sum of independent towers minus hidden shared faces
def surface_area(grid):
    n = len(grid)
    total = 0
    for i in range(n):
        for j in range(n):
            v = grid[i][j]
            if v:
                total += 4 * v + 2
                if i > 0:
                    total -= 2 * min(v, grid[i - 1][j])
                if j > 0:
                    total -= 2 * min(v, grid[i][j - 1])
    return total
""",
    ),
    # ---- As Far from Land as Possible (LeetCode 1162) ----
    dict(
        title="As Far from Land as Possible",
        diff="M",
        lc=1162,
        slug="as-far-from-land-as-possible",
        prompt=(
            "grid is n x n with 0 = water and 1 = land. Find a water cell whose Manhattan distance to the nearest "
            "land cell is as large as possible and return that distance, or -1 if the grid has no water or no land."
        ),
        sig="def max_distance(grid: List[List[int]]) -> int:",
        fn="max_distance",
        tests=[
            (([[1, 0, 1], [0, 0, 0], [1, 0, 1]],), 2),
            (([[1, 0, 0], [0, 0, 0], [0, 0, 0]],), 4),
            (([[1, 1], [1, 1]],), -1),
            (([[0, 0], [0, 0]],), -1),
            (([[0, 1], [0, 0]],), 2),
        ],
        hints=[
            "Running a BFS from every water cell is O(n^4).",
            "Reverse the search: start from ALL land cells at once.",
            (
                "Multi-source BFS: every water cell is reached for the first time by its nearest land; the last "
                "level reached is the answer."
            ),
        ],
        pattern="Multi-source BFS (distance to nearest source)",
        explain=(
            "Putting all land cells into the BFS queue at distance 0 makes the BFS expand like a wave from every "
            "island simultaneously. A water cell is first reached by the wave of its nearest land, so its recorded "
            "distance is exactly its Manhattan distance to the nearest land (4-direction moves). The largest "
            "recorded distance is the answer."
        ),
        cx="O(n^2) time, O(n^2) space",
        brute_cx="O(n^4) time - for every water cell scan every land cell",
        brute=r"""
# BRUTE FORCE: O(n^4) time - for every water cell scan every land cell
def max_distance(grid):
    n = len(grid)
    land = [(i, j) for i in range(n) for j in range(n) if grid[i][j]]
    water = [(i, j) for i in range(n) for j in range(n) if not grid[i][j]]
    if not land or not water:
        return -1
    return max(min(abs(i - a) + abs(j - b) for a, b in land) for i, j in water)
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n^2) space
# Idea: Multi-source BFS (distance to nearest source)
def max_distance(grid):
    n = len(grid)
    dist = [[-1] * n for _ in range(n)]
    queue = deque()
    for i in range(n):
        for j in range(n):
            if grid[i][j]:
                dist[i][j] = 0
                queue.append((i, j))
    if len(queue) in (0, n * n):
        return -1
    farthest = 0
    while queue:
        i, j = queue.popleft()
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < n and 0 <= b < n and dist[a][b] == -1:
                dist[a][b] = dist[i][j] + 1
                farthest = dist[a][b]
                queue.append((a, b))
    return farthest
""",
    ),
    # ---- Find Winner on a Tic Tac Toe Game (LeetCode 1275) ----
    dict(
        title="Find Winner on a Tic Tac Toe Game",
        diff="E",
        lc=1275,
        slug="find-winner-on-a-tic-tac-toe-game",
        prompt=(
            "Players A (moves 0, 2, 4, ...) and B (moves 1, 3, ...) place marks on a 3 x 3 board; moves[i] = [row, "
            "col] and the game is valid (it stops at a win). Return 'A' or 'B' if someone has won, 'Draw' if the "
            "board is full with no winner, otherwise 'Pending'."
        ),
        sig="def tictactoe(moves: List[List[int]]) -> str:",
        fn="tictactoe",
        tests=[
            (([[0, 0], [2, 0], [1, 1], [2, 1], [2, 2]],), "A"),
            (([[0, 0], [1, 1], [0, 1], [0, 2], [1, 0], [2, 0]],), "B"),
            (([[0, 0], [1, 1], [2, 0], [1, 0], [1, 2], [2, 1], [0, 1], [0, 2], [2, 2]],), "Draw"),
            (([[0, 0], [1, 1]],), "Pending"),
        ],
        hints=[
            "A win needs three marks on one of 8 lines: 3 rows, 3 columns, 2 diagonals.",
            "Instead of rescanning the board, keep a counter per line for each player.",
            (
                "On each move bump the counters of its row, column and (if on one) diagonal; the first counter that "
                "reaches 3 decides the winner."
            ),
        ],
        pattern="Per-line counters instead of rescanning the grid",
        explain=(
            "A move can only complete lines passing through its own cell: its row, its column, and at most the two "
            "diagonals. Counting marks per line and per player makes each move O(1), and the first counter to reach "
            "3 names the winner immediately. If nobody wins, the game is a draw only once all 9 cells are used."
        ),
        cx="O(n) time for n moves, O(1) space",
        brute_cx="O(n * 8) time - rebuild the board and test all 8 lines after each move",
        brute=r"""
# BRUTE FORCE: O(n * 8) time - rebuild the board and test all 8 lines after each move
def tictactoe(moves):
    board = [[""] * 3 for _ in range(3)]
    lines = (
        [[(i, j) for j in range(3)] for i in range(3)]
        + [[(i, j) for i in range(3)] for j in range(3)]
        + [[(i, i) for i in range(3)], [(i, 2 - i) for i in range(3)]]
    )
    for t, (r, c) in enumerate(moves):
        mark = "AB"[t % 2]
        board[r][c] = mark
        if any(all(board[i][j] == mark for i, j in line) for line in lines):
            return mark
    return "Draw" if len(moves) == 9 else "Pending"
""",
        solution=r"""
# OPTIMISED: O(n) time for n moves, O(1) space
# Idea: Per-line counters instead of rescanning the grid
def tictactoe(moves):
    score = [[0] * 8 for _ in range(2)]
    for t, (r, c) in enumerate(moves):
        player = t % 2
        lines = (r, 3 + c) + ((6,) if r == c else ()) + ((7,) if r + c == 2 else ())
        for line in lines:
            score[player][line] += 1
            if score[player][line] == 3:
                return "AB"[player]
    return "Draw" if len(moves) == 9 else "Pending"
""",
    ),
    # ---- Sort the Matrix Diagonally (LeetCode 1329) ----
    dict(
        title="Sort the Matrix Diagonally",
        diff="M",
        lc=1329,
        slug="sort-the-matrix-diagonally",
        prompt=(
            "A matrix diagonal runs from top-left to bottom-right. Sort every diagonal of mat in ascending order "
            "and return the resulting matrix."
        ),
        sig="def diagonal_sort(mat: List[List[int]]) -> List[List[int]]:",
        fn="diagonal_sort",
        tests=[
            (([[3, 3, 1, 1], [2, 2, 1, 2], [1, 1, 1, 2]],), [[1, 1, 1, 1], [1, 2, 2, 2], [1, 2, 3, 3]]),
            (
                (
                    [
                        [11, 25, 66, 1, 69, 7],
                        [23, 55, 17, 45, 15, 52],
                        [75, 31, 36, 44, 58, 8],
                        [22, 27, 33, 25, 68, 4],
                        [84, 28, 14, 11, 5, 50],
                    ],
                ),
                [
                    [5, 17, 4, 1, 52, 7],
                    [11, 11, 25, 45, 8, 69],
                    [14, 23, 25, 44, 58, 15],
                    [22, 27, 31, 36, 50, 66],
                    [84, 28, 75, 33, 55, 68],
                ],
            ),
            (([[5]],), [[5]]),
            (([[2, 1]],), [[2, 1]]),
        ],
        hints=[
            "All cells on one diagonal share the same value of row - column.",
            "Group the values by row - column, sort each group.",
            "Walk the matrix again and write each diagonal's values back in order (pop from the sorted group).",
        ],
        pattern="Group by i - j (diagonal id), sort, write back",
        explain=(
            "The quantity i - j is constant along a top-left to bottom-right diagonal, so it is a perfect key for "
            "grouping. Sorting each group independently and refilling the cells in scan order puts the sorted "
            "values back onto the same diagonal positions."
        ),
        cx="O(m * n * log(min(m, n))) time, O(m * n) space",
        brute_cx="O(m * n * min(m, n)) time - bubble-sort neighbours along each diagonal until nothing changes",
        brute=r"""
# BRUTE FORCE: O(m * n * min(m, n)) time - bubble-sort neighbours along each diagonal until nothing changes
def diagonal_sort(mat):
    out = [row[:] for row in mat]
    m, n = len(out), len(out[0])
    changed = True
    while changed:
        changed = False
        for i in range(m - 1):
            for j in range(n - 1):
                if out[i][j] > out[i + 1][j + 1]:
                    out[i][j], out[i + 1][j + 1] = out[i + 1][j + 1], out[i][j]
                    changed = True
    return out
""",
        solution=r"""
# OPTIMISED: O(m * n * log(min(m, n))) time, O(m * n) space
# Idea: Group by i - j (diagonal id), sort, write back
def diagonal_sort(mat):
    m, n = len(mat), len(mat[0])
    groups = defaultdict(list)
    for i in range(m):
        for j in range(n):
            groups[i - j].append(mat[i][j])
    for values in groups.values():
        values.sort(reverse=True)
    out = [[0] * n for _ in range(m)]
    for i in range(m):
        for j in range(n):
            out[i][j] = groups[i - j].pop()
    return out
""",
    ),
    # ---- Where Will the Ball Fall (LeetCode 1706) ----
    dict(
        title="Where Will the Ball Fall",
        diff="M",
        lc=1706,
        slug="where-will-the-ball-fall",
        prompt=(
            "Each cell of the m x n grid is a diagonal board: 1 leans like '\\' (pushes a ball right) and -1 leans "
            "like '/' (pushes it left). A ball dropped at the top of column j falls row by row; it gets stuck if it "
            "hits a wall or a 'V' shape (two boards leaning into each other). Return, for every column, the column "
            "where the ball falls out of the bottom, or -1 if it gets stuck."
        ),
        sig="def find_ball(grid: List[List[int]]) -> List[int]:",
        fn="find_ball",
        tests=[
            (
                ([[1, 1, 1, -1, -1], [1, 1, 1, -1, -1], [-1, -1, -1, 1, 1], [1, 1, 1, 1, -1], [-1, -1, -1, -1, -1]],),
                [1, -1, -1, -1, -1],
            ),
            (([[-1]],), [-1]),
            (
                ([[1, 1, 1, 1, 1, 1], [-1, -1, -1, -1, -1, -1], [1, 1, 1, 1, 1, 1], [-1, -1, -1, -1, -1, -1]],),
                [0, 1, 2, 3, 4, -1],
            ),
            (([[1]],), [-1]),
        ],
        hints=[
            "In a row, a ball at column c moves by grid[r][c] (+1 right, -1 left).",
            (
                "It is stuck if the target column is outside the grid, or the board in the target column leans the "
                "other way (a V)."
            ),
            "Simulate row by row. A -1 stays -1 for all later rows.",
        ],
        pattern="Row-by-row simulation with a stuck check",
        explain=(
            "The next column is c + grid[r][c]. The ball passes only if that column exists and its board has the "
            "same slope (grid[r][c + d] == grid[r][c]); otherwise it hits a wall or a V and stops forever. Updating "
            "all ball positions together row by row is a single pass over the grid."
        ),
        cx="O(m * n) time, O(n) space",
        brute_cx="O(m * n) time - drop each ball separately with recursion",
        brute=r"""
# BRUTE FORCE: O(m * n) time - drop each ball separately with recursion
def find_ball(grid):
    m, n = len(grid), len(grid[0])

    def fall(r, c):
        if r == m:
            return c
        nxt = c + grid[r][c]
        if nxt < 0 or nxt >= n or grid[r][nxt] != grid[r][c]:
            return -1
        return fall(r + 1, nxt)

    return [fall(0, c) for c in range(n)]
""",
        solution=r"""
# OPTIMISED: O(m * n) time, O(n) space
# Idea: Row-by-row simulation with a stuck check
def find_ball(grid):
    n = len(grid[0])
    pos = list(range(n))
    for row in grid:
        nxt = []
        for c in pos:
            if c < 0:
                nxt.append(-1)
                continue
            target = c + row[c]
            nxt.append(target if 0 <= target < n and row[target] == row[c] else -1)
        pos = nxt
    return pos
""",
    ),
    # ---- Rotating the Box (LeetCode 1861) ----
    dict(
        title="Rotating the Box",
        diff="M",
        lc=1861,
        slug="rotating-the-box",
        prompt=(
            "box is an m x n grid of '#' (stone), '*' (fixed obstacle) and '.' (empty). Rotate the box 90 degrees "
            "clockwise. Stones then fall 'down' (which was toward the right before the rotation) until they hit an "
            "obstacle, the bottom or another stone; obstacles do not move. Return the n x m box after the rotation."
        ),
        sig="def rotate_the_box(box: List[List[str]]) -> List[List[str]]:",
        fn="rotate_the_box",
        tests=[
            (([["#", ".", "#"]],), [["."], ["#"], ["#"]]),
            (
                ([["#", ".", "*", "."], ["#", "#", "*", "."]],),
                [["#", "."], ["#", "#"], ["*", "*"], [".", "."]],
            ),
            (
                (
                    [
                        ["#", "#", "*", ".", "*", "."],
                        ["#", "#", "#", "*", ".", "."],
                        ["#", ".", "#", "#", "*", "."],
                    ],
                ),
                [
                    [".", "#", "#"],
                    ["#", "#", "#"],
                    ["#", "#", "*"],
                    ["#", "*", "."],
                    ["*", ".", "*"],
                    [".", ".", "."],
                ],
            ),
        ],
        hints=[
            "Do the gravity step BEFORE rotating: stones slide to the right inside each row.",
            (
                "Scan each row from the right with a 'write' pointer for the next free slot; an obstacle resets the "
                "pointer just left of it; a stone is moved to the pointer."
            ),
            "Then rotate: the cell at (i, j) goes to (j, m - 1 - i).",
        ],
        pattern="Two-pointer gravity per row, then rotate by index mapping",
        explain=(
            "After a clockwise rotation, 'down' corresponds to 'right' in the original rows, so gravity can be "
            "applied inside each row first. From the right, a pointer marks the rightmost free slot; each stone is "
            "moved there and the pointer steps left, while an obstacle moves the pointer to just left of itself. "
            "Rotation is then pure index mapping."
        ),
        cx="O(m * n) time, O(m * n) space",
        brute_cx="O(m * n^2) time - swap stones one step at a time until nothing moves, then rotate with zip",
        brute=r"""
# BRUTE FORCE: O(m * n^2) time - swap stones one step at a time until nothing moves, then rotate with zip
def rotate_the_box(box):
    rows = [list(row) for row in box]
    moved = True
    while moved:
        moved = False
        for row in rows:
            for j in range(len(row) - 1):
                if row[j] == "#" and row[j + 1] == ".":
                    row[j], row[j + 1] = ".", "#"
                    moved = True
    return [list(col) for col in zip(*rows[::-1])]
""",
        solution=r"""
# OPTIMISED: O(m * n) time, O(m * n) space
# Idea: Two-pointer gravity per row, then rotate by index mapping
def rotate_the_box(box):
    m, n = len(box), len(box[0])
    out = [["."] * m for _ in range(n)]
    for i, original in enumerate(box):
        row = list(original)
        write = n - 1
        for j in range(n - 1, -1, -1):
            if row[j] == "*":
                write = j - 1
            elif row[j] == "#":
                row[j] = "."
                row[write] = "#"
                write -= 1
        for j in range(n):
            out[j][m - 1 - i] = row[j]
    return out
""",
    ),
    # ---- Determine Whether Matrix Can Be Obtained By Rotation (LeetCode 1886) ----
    dict(
        title="Determine Whether Matrix Can Be Obtained By Rotation",
        diff="E",
        lc=1886,
        slug="determine-whether-matrix-can-be-obtained-by-rotation",
        prompt=(
            "Return True if the n x n binary matrix mat can be turned into target by rotating it in 90-degree steps "
            "(0, 1, 2 or 3 times)."
        ),
        sig="def find_rotation(mat: List[List[int]], target: List[List[int]]) -> bool:",
        fn="find_rotation",
        tests=[
            (([[0, 1], [1, 0]], [[1, 0], [0, 1]]), True),
            (([[0, 1], [1, 1]], [[1, 0], [0, 1]]), False),
            (([[0, 0, 0], [0, 1, 0], [1, 1, 1]], [[1, 1, 1], [0, 1, 0], [0, 0, 0]]), True),
            (([[1]], [[1]]), True),
        ],
        hints=[
            "Only 4 orientations exist - after 4 rotations you are back where you started.",
            "A clockwise rotation maps the cell (i, j) to (j, n - 1 - i).",
            "Rotate up to 3 times, comparing with target each time (zip(*m[::-1]) is a one-line clockwise rotation).",
        ],
        pattern="Try all 4 rotations",
        explain=(
            "Rotation by 90 degrees has order 4, so checking the matrix at 0, 90, 180 and 270 degrees covers every "
            "possibility. A clockwise rotation is the transpose of the vertically flipped matrix, which "
            "zip(*m[::-1]) computes directly."
        ),
        cx="O(n^2) time, O(n^2) space",
        brute_cx="O(n^2) time per rotation, building each rotation with explicit index formulas",
        brute=r"""
# BRUTE FORCE: O(n^2) time per rotation, building each rotation with explicit index formulas
def find_rotation(mat, target):
    n = len(mat)
    current = [row[:] for row in mat]
    for _ in range(4):
        if current == target:
            return True
        rotated = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                rotated[j][n - 1 - i] = current[i][j]
        current = rotated
    return False
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n^2) space
# Idea: Try all 4 rotations
def find_rotation(mat, target):
    current = [list(row) for row in mat]
    for _ in range(4):
        if current == target:
            return True
        current = [list(row) for row in zip(*current[::-1])]
    return False
""",
    ),
    # ---- Find All Groups of Farmland (LeetCode 1992) ----
    dict(
        title="Find All Groups of Farmland",
        diff="M",
        lc=1992,
        slug="find-all-groups-of-farmland",
        prompt=(
            "land is an m x n grid where 1 is farmland and 0 is forest. Farmland forms rectangular groups that "
            "never touch each other (not even side by side). Return [r1, c1, r2, c2] (top-left and bottom-right "
            "corner) for every group, in any order."
        ),
        sig="def find_farmland(land: List[List[int]]) -> List[List[int]]:",
        fn="find_farmland",
        compare="unordered",
        tests=[
            (([[1, 0, 0], [0, 1, 1], [0, 1, 1]],), [[0, 0, 0, 0], [1, 1, 2, 2]]),
            (([[1, 1], [1, 1]],), [[0, 0, 1, 1]]),
            (([[0]],), []),
            (([[1, 0, 1]],), [[0, 0, 0, 0], [0, 2, 0, 2]]),
        ],
        hints=[
            "Every group is a solid rectangle, so it is fully described by its top-left and bottom-right corners.",
            "A cell is a top-left corner exactly when it is 1 and has no 1 above it and no 1 to its left.",
            "From a top-left corner walk right while 1 to find the last column, and down while 1 to find the last row.",
        ],
        pattern="Find rectangle corners by scanning (no flood fill needed)",
        explain=(
            "Because groups are solid rectangles that do not touch, the top-left corner of each is the unique cell "
            "with no farmland above or to its left, and the rectangle extends right and down along 1s. Scanning "
            "row-major finds every top-left corner once, and the walks together cost one visit per boundary cell."
        ),
        cx="O(m * n) time, O(1) extra space",
        brute_cx="O(m * n) time - flood fill every group and record its minimum and maximum coordinates",
        brute=r"""
# BRUTE FORCE: O(m * n) time - flood fill every group and record its minimum and maximum coordinates
def find_farmland(land):
    m, n = len(land), len(land[0])
    seen = set()
    groups = []
    for i in range(m):
        for j in range(n):
            if land[i][j] and (i, j) not in seen:
                stack = [(i, j)]
                seen.add((i, j))
                cells = []
                while stack:
                    a, b = stack.pop()
                    cells.append((a, b))
                    for x, y in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                        if 0 <= x < m and 0 <= y < n and land[x][y] and (x, y) not in seen:
                            seen.add((x, y))
                            stack.append((x, y))
                rows = [a for a, _ in cells]
                cols = [b for _, b in cells]
                groups.append([min(rows), min(cols), max(rows), max(cols)])
    return groups
""",
        solution=r"""
# OPTIMISED: O(m * n) time, O(1) extra space
# Idea: Find rectangle corners by scanning (no flood fill needed)
def find_farmland(land):
    m, n = len(land), len(land[0])
    groups = []
    for i in range(m):
        for j in range(n):
            if land[i][j] and (i == 0 or not land[i - 1][j]) and (j == 0 or not land[i][j - 1]):
                r, c = i, j
                while r + 1 < m and land[r + 1][j]:
                    r += 1
                while c + 1 < n and land[i][c + 1]:
                    c += 1
                groups.append([i, j, r, c])
    return groups
""",
    ),
    # ---- Check if Every Row and Column Contains All Numbers (LeetCode 2133) ----
    dict(
        title="Check if Every Row and Column Contains All Numbers",
        diff="E",
        lc=2133,
        slug="check-if-every-row-and-column-contains-all-numbers",
        prompt=(
            "matrix is n x n with values in 1..n. Return True if every row and every column contains each of the "
            "numbers 1..n (it is 'valid')."
        ),
        sig="def check_valid(matrix: List[List[int]]) -> bool:",
        fn="check_valid",
        tests=[
            (([[1, 2, 3], [3, 1, 2], [2, 3, 1]],), True),
            (([[1, 1, 1], [1, 2, 3], [1, 2, 3]],), False),
            (([[1]],), True),
            (([[1, 2], [1, 2]],), False),
        ],
        hints=[
            "A row of n values in 1..n contains every number iff it has n DISTINCT values.",
            "Check each row with set(row) and each column the same way.",
            "zip(*matrix) gives the columns.",
        ],
        pattern="Distinct-count check per row and column",
        explain=(
            "With n cells and only the values 1..n available, 'contains every number' is equivalent to 'has n "
            "distinct values' (pigeonhole). One set per row and one per column decides validity."
        ),
        cx="O(n^2) time, O(n) space",
        brute_cx="O(n^3) time - search every row and column for every number 1..n",
        brute=r"""
# BRUTE FORCE: O(n^3) time - search every row and column for every number 1..n
def check_valid(matrix):
    n = len(matrix)
    for v in range(1, n + 1):
        for i in range(n):
            if v not in matrix[i] or v not in [matrix[r][i] for r in range(n)]:
                return False
    return True
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n) space
# Idea: Distinct-count check per row and column
def check_valid(matrix):
    n = len(matrix)
    return all(len(set(row)) == n for row in matrix) and all(
        len(set(col)) == n for col in zip(*matrix)
    )
""",
    ),
    # ---- Count Unguarded Cells in the Grid (LeetCode 2257) ----
    dict(
        title="Count Unguarded Cells in the Grid",
        diff="M",
        lc=2257,
        slug="count-unguarded-cells-in-the-grid",
        prompt=(
            "On an m x n grid, guards and walls occupy distinct cells. A guard sees every cell in the four straight "
            "directions until the line of sight hits a wall or another guard. Return the number of cells that are "
            "neither occupied nor seen by any guard."
        ),
        sig="def count_unguarded(m: int, n: int, guards: List[List[int]], walls: List[List[int]]) -> int:",
        fn="count_unguarded",
        tests=[
            ((4, 6, [[0, 0], [1, 1], [2, 3]], [[0, 1], [2, 2], [1, 4]]), 7),
            ((3, 3, [[1, 1]], [[0, 1], [1, 0], [2, 1], [1, 2]]), 4),
            ((1, 3, [[0, 0]], []), 0),
            ((1, 3, [[0, 0]], [[0, 1]]), 1),
        ],
        hints=[
            "Casting a ray from every guard costs O(guards * (m + n)).",
            (
                "Sweep each row left-to-right and right-to-left (then each column top-to-bottom and bottom-to-top) "
                "with a flag 'a guard is looking along this line'."
            ),
            "A guard sets the flag, a wall clears it, and an empty cell is marked seen while the flag is on.",
        ],
        pattern="Four directional sweeps with a 'visible' flag",
        explain=(
            "A cell is seen if, looking left, right, up or down, the nearest occupied cell in that direction is a "
            "guard. A sweep in one direction carries a flag that a guard turns on and a wall turns off, so every "
            "empty cell is classified in one linear pass per direction. Another guard on the line keeps the flag "
            "on, which is correct because that guard sees onward itself."
        ),
        cx="O(m * n) time, O(m * n) space",
        brute_cx="O(g * (m + n)) time - cast a ray from each guard in the 4 directions until blocked",
        brute=r"""
# BRUTE FORCE: O(g * (m + n)) time - cast a ray from each guard in the 4 directions until blocked
def count_unguarded(m, n, guards, walls):
    blocked = {(r, c) for r, c in walls} | {(r, c) for r, c in guards}
    seen = set()
    for r, c in guards:
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            a, b = r + dr, c + dc
            while 0 <= a < m and 0 <= b < n and (a, b) not in blocked:
                seen.add((a, b))
                a, b = a + dr, b + dc
    return m * n - len(blocked) - len(seen)
""",
        solution=r"""
# OPTIMISED: O(m * n) time, O(m * n) space
# Idea: Four directional sweeps with a 'visible' flag
def count_unguarded(m, n, guards, walls):
    grid = [[0] * n for _ in range(m)]
    for r, c in guards:
        grid[r][c] = 1
    for r, c in walls:
        grid[r][c] = 2
    seen = [[False] * n for _ in range(m)]

    def sweep(cells):
        watching = False
        for r, c in cells:
            if grid[r][c] == 1:
                watching = True
            elif grid[r][c] == 2:
                watching = False
            elif watching:
                seen[r][c] = True

    for r in range(m):
        sweep((r, c) for c in range(n))
        sweep((r, c) for c in range(n - 1, -1, -1))
    for c in range(n):
        sweep((r, c) for r in range(m))
        sweep((r, c) for r in range(m - 1, -1, -1))
    return sum(1 for r in range(m) for c in range(n) if grid[r][c] == 0 and not seen[r][c])
""",
    ),
    # ---- Largest Local Values in a Matrix (LeetCode 2373) ----
    dict(
        title="Largest Local Values in a Matrix",
        diff="E",
        lc=2373,
        slug="largest-local-values-in-a-matrix",
        prompt=(
            "For an n x n grid return the (n - 2) x (n - 2) matrix maxLocal where maxLocal[i][j] is the largest "
            "value in the 3 x 3 window of grid whose top-left corner is (i, j)."
        ),
        sig="def largest_local(grid: List[List[int]]) -> List[List[int]]:",
        fn="largest_local",
        tests=[
            (([[9, 9, 8, 1], [5, 6, 2, 6], [8, 2, 6, 4], [6, 2, 2, 2]],), [[9, 9], [8, 6]]),
            (
                ([[1, 1, 1, 1, 1], [1, 1, 1, 1, 1], [1, 1, 2, 1, 1], [1, 1, 1, 1, 1], [1, 1, 1, 1, 1]],),
                [[2, 2, 2], [2, 2, 2], [2, 2, 2]],
            ),
            (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [[9]]),
        ],
        hints=[
            "Taking max over 9 cells for each of (n-2)^2 windows is fine but repeats work.",
            "A 3 x 3 maximum is the maximum of three row-wise maxima.",
            "First compute the horizontal 3-wide maximum of every row, then take the vertical 3-high maximum of those.",
        ],
        pattern="Separable sliding-window maximum (rows, then columns)",
        explain=(
            "max over a 3 x 3 window = max over 3 rows of (max over 3 columns). Computing the horizontal maxima "
            "once per row and reusing them for three different windows cuts the comparisons from 9 to about 5 per "
            "window; for large windows the same idea underlies faster 2D sliding maxima."
        ),
        cx="O(n^2) time, O(n^2) space",
        brute_cx="O(9 * n^2) time - take the maximum of each 3 x 3 window directly",
        brute=r"""
# BRUTE FORCE: O(9 * n^2) time - take the maximum of each 3 x 3 window directly
def largest_local(grid):
    n = len(grid)
    return [
        [max(grid[i + a][j + b] for a in range(3) for b in range(3)) for j in range(n - 2)]
        for i in range(n - 2)
    ]
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n^2) space
# Idea: Separable sliding-window maximum (rows, then columns)
def largest_local(grid):
    n = len(grid)
    row_max = [[max(row[j : j + 3]) for j in range(n - 2)] for row in grid]
    return [
        [max(row_max[i][j], row_max[i + 1][j], row_max[i + 2][j]) for j in range(n - 2)]
        for i in range(n - 2)
    ]
""",
    ),
    # ---- Matrix Similarity After Cyclic Shifts (LeetCode 2946) ----
    dict(
        title="Matrix Similarity After Cyclic Shifts",
        diff="E",
        lc=2946,
        slug="matrix-similarity-after-cyclic-shifts",
        prompt=(
            "Shift every even-indexed row of mat left and every odd-indexed row right, cyclically, by k positions. "
            "Return True if the resulting matrix equals the original mat."
        ),
        sig="def are_similar(mat: List[List[int]], k: int) -> bool:",
        fn="are_similar",
        tests=[
            (([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 4), False),
            (([[1, 2, 1, 2], [5, 5, 5, 5], [6, 3, 6, 3]], 2), True),
            (([[2, 2], [2, 2]], 3), True),
            (([[1, 2]], 2), True),
            (([[1, 2]], 1), False),
        ],
        hints=[
            "Simulating k single shifts per row works but k can exceed the row length.",
            "Shifting by k is the same as shifting by k % n.",
            (
                "A left shift and a right shift by the same amount both give the original row exactly when row[j] "
                "== row[(j + k) % n] for all j - the direction does not matter."
            ),
        ],
        pattern="Cyclic shift equals identity iff the row is periodic with that shift",
        explain=(
            "A cyclic shift by s maps position j to j + s (mod n). The row is unchanged exactly when every element "
            "equals the one s places away, and that condition is symmetric: shifting left by k and right by k are "
            "inverse permutations, so the row is fixed by one exactly when it is fixed by the other. Hence only k % "
            "n and the comparison row[j] == row[(j + k) % n] matter."
        ),
        cx="O(m * n) time, O(1) space",
        brute_cx="O(m * n * k) time - perform the k single-step shifts row by row and compare",
        brute=r"""
# BRUTE FORCE: O(m * n * k) time - perform the k single-step shifts row by row and compare
def are_similar(mat, k):
    for i, row in enumerate(mat):
        shifted = list(row)
        for _ in range(k):
            if i % 2 == 0:
                shifted = shifted[1:] + shifted[:1]
            else:
                shifted = shifted[-1:] + shifted[:-1]
        if shifted != row:
            return False
    return True
""",
        solution=r"""
# OPTIMISED: O(m * n) time, O(1) space
# Idea: Cyclic shift equals identity iff the row is periodic with that shift
def are_similar(mat, k):
    n = len(mat[0])
    return all(row[j] == row[(j + k) % n] for row in mat for j in range(n))
""",
    ),
    # ---- Find Missing and Repeated Values (LeetCode 2965) ----
    dict(
        title="Find Missing and Repeated Values",
        diff="E",
        lc=2965,
        slug="find-missing-and-repeated-values",
        prompt=(
            "grid is n x n and should contain each of 1..n^2 exactly once, but one value a appears twice and one "
            "value b is missing. Return [a, b]."
        ),
        sig="def find_missing_and_repeated_values(grid: List[List[int]]) -> List[int]:",
        fn="find_missing_and_repeated_values",
        tests=[
            (([[1, 3], [2, 2]],), [2, 4]),
            (([[9, 1, 7], [8, 9, 2], [3, 4, 6]],), [9, 5]),
            (([[1, 1], [3, 4]],), [1, 2]),
        ],
        hints=[
            "Flatten the grid and compare with the full set 1..n^2.",
            "Sum of all cells minus sum of the DISTINCT cells = the repeated value a.",
            "Expected sum n^2 (n^2 + 1) / 2 minus the distinct sum = the missing value b.",
        ],
        pattern="Sum arithmetic with a set (no sorting, no counting dictionary)",
        explain=(
            "Let S be the sum of all cells and D the sum of the distinct values. The duplicate is counted once too "
            "often, so a = S - D. Every number except b appears among the distinct values, so the full sum minus D "
            "equals b."
        ),
        cx="O(n^2) time, O(n^2) space",
        brute_cx="O(n^4) time - count each of 1..n^2 in the flattened grid",
        brute=r"""
# BRUTE FORCE: O(n^4) time - count each of 1..n^2 in the flattened grid
def find_missing_and_repeated_values(grid):
    flat = [x for row in grid for x in row]
    repeated = missing = 0
    for v in range(1, len(flat) + 1):
        c = flat.count(v)
        if c == 2:
            repeated = v
        elif c == 0:
            missing = v
    return [repeated, missing]
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n^2) space
# Idea: Sum arithmetic with a set (no sorting, no counting dictionary)
def find_missing_and_repeated_values(grid):
    flat = [x for row in grid for x in row]
    distinct = sum(set(flat))
    total = len(flat) * (len(flat) + 1) // 2
    return [sum(flat) - distinct, total - distinct]
""",
    ),
    # ---- Sum of Matrix After Queries (LeetCode 2718) ----
    dict(
        title="Sum of Matrix After Queries",
        diff="M",
        lc=2718,
        slug="sum-of-matrix-after-queries",
        prompt=(
            "Start with an n x n matrix of zeros. Each query [type, index, val] sets every cell of row `index` "
            "(type 0) or of column `index` (type 1) to val. Apply the queries in order and return the sum of all "
            "cells."
        ),
        sig="def matrix_sum_queries(n: int, queries: List[List[int]]) -> int:",
        fn="matrix_sum_queries",
        tests=[
            ((3, [[0, 0, 1], [1, 2, 2], [0, 2, 3], [1, 0, 4]]), 23),
            ((3, [[0, 0, 4], [0, 1, 2], [1, 0, 1], [0, 2, 3], [1, 2, 1]]), 17),
            ((1, [[0, 0, 5]]), 5),
            ((2, [[0, 0, 3], [0, 0, 1]]), 2),
        ],
        hints=[
            "Simulating every query costs O(n) each; most of that work is later overwritten.",
            "Process the queries in REVERSE: the last write to a cell is the one that counts.",
            (
                "In reverse, the first time you see a row (column), it still has n - (columns already painted) "
                "cells that nobody overwrote later; add val times that many. Ignore repeats."
            ),
        ],
        pattern="Process in reverse: the last write wins",
        explain=(
            "Going backwards, a row query affects exactly the cells in columns that no later column-query has "
            "claimed, which is n - len(painted_cols) cells - and only if this row was not painted by a later query. "
            "Each row and column is therefore counted at most once, which turns an O(q * n) simulation into O(q)."
        ),
        cx="O(q) time, O(n) space",
        brute_cx="O(q * n + n^2) time - actually paint the matrix and add it up",
        brute=r"""
# BRUTE FORCE: O(q * n + n^2) time - actually paint the matrix and add it up
def matrix_sum_queries(n, queries):
    matrix = [[0] * n for _ in range(n)]
    for kind, index, value in queries:
        for k in range(n):
            if kind == 0:
                matrix[index][k] = value
            else:
                matrix[k][index] = value
    return sum(map(sum, matrix))
""",
        solution=r"""
# OPTIMISED: O(q) time, O(n) space
# Idea: Process in reverse: the last write wins
def matrix_sum_queries(n, queries):
    rows, cols = set(), set()
    total = 0
    for kind, index, value in reversed(queries):
        if kind == 0:
            if index not in rows:
                total += value * (n - len(cols))
                rows.add(index)
        elif index not in cols:
            total += value * (n - len(rows))
            cols.add(index)
    return total
""",
    ),
]
