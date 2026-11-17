"""more Matrix problems (batch 3) - part of the problem bank for the "matrix" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Search a 2D Matrix II (LeetCode 240) ----
    dict(
        title="Search a 2D Matrix II",
        diff="M",
        lc=240,
        slug="search-a-2d-matrix-ii",
        prompt=(
            "Every row and every column of the matrix is sorted ascending (but a row does not continue from the "
            "previous one). Return True if target is present."
        ),
        sig="def search_matrix(matrix: List[List[int]], target: int) -> bool:",
        fn="search_matrix",
        tests=[
            (
                (
                    [
                        [1, 4, 7, 11, 15],
                        [2, 5, 8, 12, 19],
                        [3, 6, 9, 16, 22],
                        [10, 13, 14, 17, 24],
                        [18, 21, 23, 26, 30],
                    ],
                    5,
                ),
                True,
            ),
            (
                (
                    [
                        [1, 4, 7, 11, 15],
                        [2, 5, 8, 12, 19],
                        [3, 6, 9, 16, 22],
                        [10, 13, 14, 17, 24],
                        [18, 21, 23, 26, 30],
                    ],
                    20,
                ),
                False,
            ),
            (([[1]], 1), True),
            (([[1]], 2), False),
            (([[1, 3], [2, 4]], 3), True),
        ],
        hints=[
            "Start in a corner where moving in one direction increases values and the other decreases them.",
            "The top-right corner works: left is smaller, down is larger.",
            (
                "If the current value is too big move left; too small, move down; equal means found. Each step "
                "removes a whole row or column."
            ),
        ],
        pattern="Staircase search from the top-right corner",
        explain=(
            "From the top-right, a value larger than target means the entire column below is even larger, so the "
            "column\n        is discarded; a smaller value discards its whole row. At most R + C steps are ever "
            "needed."
        ),
        cx="O(R + C) time, O(1) space",
        brute_cx="O(R*C) time - look at every cell",
        brute=r"""
# BRUTE FORCE: O(R*C) time - look at every cell
def search_matrix(matrix, target):
    return any(target in row for row in matrix)  # check every row, cell by cell
""",
        solution=r"""
# OPTIMISED: O(R + C) time, O(1) space
# Idea: Staircase search from the top-right corner
def search_matrix(matrix, target):
    row, col = 0, len(matrix[0]) - 1  # start at the top-right corner

    while row < len(matrix) and col >= 0:
        value = matrix[row][col]
        if value == target:
            return True
        if value > target:
            col -= 1  # everything below in this column is even larger: drop the column
        else:
            row += 1  # everything to the left in this row is even smaller: drop the row

    return False
""",
    ),
    # ---- Spiral Matrix II (LeetCode 59) ----
    dict(
        title="Spiral Matrix II",
        diff="M",
        lc=59,
        slug="spiral-matrix-ii",
        prompt="Return an n x n matrix filled with 1..n*n in clockwise spiral order, starting at the top-left.",
        sig="def generate_matrix(n: int) -> List[List[int]]:",
        fn="generate_matrix",
        tests=[
            ((3,), [[1, 2, 3], [8, 9, 4], [7, 6, 5]]),
            ((1,), [[1]]),
            ((2,), [[1, 2], [4, 3]]),
            ((4,), [[1, 2, 3, 4], [12, 13, 14, 5], [11, 16, 15, 6], [10, 9, 8, 7]]),
        ],
        hints=[
            "Walk right, down, left, up repeatedly, writing 1, 2, 3, ...",
            "Keep four boundaries (top, bottom, left, right). After each side, shrink the boundary you just used.",
            (
                "Stop when the boundaries cross. Guard the left and up sides with an if, for the single-row / "
                "single-column middle."
            ),
        ],
        pattern="Shrinking boundaries (layer by layer)",
        explain=(
            "Each pass writes one outer ring: top row, right column, bottom row, left column. After a ring, "
            "the\n        rectangle that is still empty is smaller by one on each side. This is the same walk as "
            "'Spiral Matrix', writing instead of reading."
        ),
        cx="O(n^2) time, O(1) extra space",
        brute_cx="O(n^2) time - same, but turn when blocked (uses the grid itself as a visited marker)",
        brute=r"""
# BRUTE FORCE: O(n^2) time - same, but turn when blocked (uses the grid itself as a visited marker)
def generate_matrix(n):
    grid = [[0] * n for _ in range(n)]  # 0 means "not written yet"
    row = col = 0
    d_row, d_col = 0, 1  # start by moving right

    for value in range(1, n * n + 1):
        grid[row][col] = value
        next_row, next_col = row + d_row, col + d_col
        blocked = not (0 <= next_row < n and 0 <= next_col < n) or grid[next_row][next_col] != 0
        if blocked:
            d_row, d_col = d_col, -d_row  # turn clockwise: right -> down -> left -> up
            next_row, next_col = row + d_row, col + d_col
        row, col = next_row, next_col

    return grid
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(1) extra space
# Idea: Shrinking boundaries (layer by layer)
def generate_matrix(n):
    grid = [[0] * n for _ in range(n)]
    top, bottom, left, right = 0, n - 1, 0, n - 1  # the still-empty rectangle
    value = 1

    while top <= bottom and left <= right:
        for c in range(left, right + 1):  # top row, left -> right
            grid[top][c] = value
            value += 1

        top += 1

        for r in range(top, bottom + 1):  # right column, top -> bottom
            grid[r][right] = value
            value += 1

        right -= 1

        if top <= bottom:
            for c in range(right, left - 1, -1):  # bottom row, right -> left
                grid[bottom][c] = value
                value += 1
            bottom -= 1

        if left <= right:
            for r in range(bottom, top - 1, -1):  # left column, bottom -> top
                grid[r][left] = value
                value += 1
            left += 1

    return grid
""",
    ),
    # ---- Transpose Matrix (LeetCode 867) ----
    dict(
        title="Transpose Matrix",
        diff="E",
        lc=867,
        slug="transpose-matrix",
        prompt="Return the transpose of a (possibly non-square) matrix: rows become columns and columns become rows.",
        sig="def transpose(matrix: List[List[int]]) -> List[List[int]]:",
        fn="transpose",
        tests=[
            (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [[1, 4, 7], [2, 5, 8], [3, 6, 9]]),
            (([[1, 2, 3], [4, 5, 6]],), [[1, 4], [2, 5], [3, 6]]),
            (([[1]],), [[1]]),
            (([[1, 2]],), [[1], [2]]),
        ],
        hints=[
            "The value at row r, column c moves to row c, column r.",
            "The result has as many rows as the input has columns, and vice versa.",
            "Build it column by column: the new row c is the old column c read top to bottom.",
        ],
        pattern="Swap the roles of row and column index",
        explain=(
            "For a non-square matrix you cannot swap in place - the shape changes - so allocate the new matrix. "
            "In\n        Python zip(*matrix) does exactly this: it pairs up the first elements of every row, then "
            "the second..."
        ),
        cx="O(R*C) time, O(R*C) space",
        brute_cx="O(R*C) time - explicit nested index loops",
        brute=r"""
# BRUTE FORCE: O(R*C) time - explicit nested index loops
def transpose(matrix):
    rows, cols = len(matrix), len(matrix[0])
    result = [[0] * rows for _ in range(cols)]  # shape flips to cols x rows
    for r in range(rows):
        for c in range(cols):
            result[c][r] = matrix[r][c]  # (r, c) moves to (c, r)
    return result
""",
        solution=r"""
# OPTIMISED: O(R*C) time, O(R*C) space
# Idea: Swap the roles of row and column index
def transpose(matrix):
    # zip(*matrix) takes the first item of every row, then the second item of every row, ...
    return [list(column) for column in zip(*matrix)]
""",
    ),
    # ---- Matrix Diagonal Sum (LeetCode 1572) ----
    dict(
        title="Matrix Diagonal Sum",
        diff="E",
        lc=1572,
        slug="matrix-diagonal-sum",
        prompt=(
            "Return the sum of the main diagonal and the anti-diagonal of a square matrix; the centre cell (odd "
            "size) is counted once."
        ),
        sig="def diagonal_sum(mat: List[List[int]]) -> int:",
        fn="diagonal_sum",
        tests=[
            (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), 25),
            (([[1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1]],), 8),
            (([[5]],), 5),
            (([[1, 2], [3, 4]],), 10),
        ],
        hints=[
            "Cell (i, i) is on the main diagonal; cell (i, n-1-i) is on the anti-diagonal.",
            "You only need one cell per row from each diagonal, not a scan of the whole matrix.",
            "Add both cells for every row, then subtract the centre once if n is odd (it was added twice).",
        ],
        pattern="Index arithmetic: visit only the diagonal cells",
        explain=(
            "Know the coordinates instead of searching for them. The two diagonals meet only at the centre cell of "
            "an odd\n        matrix, which is the one place we must avoid double counting."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - test every cell",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every cell
def diagonal_sum(mat):
    n = len(mat)
    total = 0

    for i in range(n):
        for j in range(n):
            if (
                i == j or i + j == n - 1
            ):  # on either diagonal (an 'or', so the centre is counted once)
                total += mat[i][j]

    return total
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Index arithmetic: visit only the diagonal cells
def diagonal_sum(mat):
    n = len(mat)
    total = sum(
        mat[i][i] + mat[i][n - 1 - i] for i in range(n)
    )  # one cell of each diagonal per row
    if n % 2:
        total -= mat[n // 2][n // 2]  # the centre was added twice
    return total
""",
    ),
]
