"""more Matrix problems (batch 4) - part of the problem bank for the "matrix" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Toeplitz Matrix (LeetCode 766) ----
    dict(
        title="Toeplitz Matrix",
        diff="E",
        lc=766,
        slug="toeplitz-matrix",
        prompt="Return True if every diagonal (top-left to bottom-right) of the matrix contains one repeated value.",
        sig="def is_toeplitz_matrix(matrix: List[List[int]]) -> bool:",
        fn="is_toeplitz_matrix",
        tests=[
            (([[1, 2, 3, 4], [5, 1, 2, 3], [9, 5, 1, 2]],), True),
            (([[1, 2], [2, 2]],), False),
            (([[1]],), True),
            (([[1, 2, 3]],), True),
        ],
        hints=[
            "A diagonal is constant exactly when every cell equals the cell diagonally above-left of it.",
            "So you never need to walk whole diagonals.",
            "Check matrix[r][c] == matrix[r - 1][c - 1] for all r, c >= 1.",
        ],
        pattern="Local neighbour check instead of whole-line scans",
        explain=(
            "Equality is transitive, so comparing each cell to its up-left neighbour proves the whole diagonal equal."
        ),
        cx="O(m*n) time, O(1) space",
        brute_cx="O(m*n*min(m, n)) time - walk each diagonal from its start",
        brute=r"""
# BRUTE FORCE: O(m*n*min(m, n)) time - walk each diagonal from its start
def is_toeplitz_matrix(matrix):
    rows, cols = len(matrix), len(matrix[0])
    starts = [(0, c) for c in range(cols)] + [
        (r, 0) for r in range(1, rows)
    ]  # the first cell of each diagonal
    for r, c in starts:
        value = matrix[r][c]
        while r < rows and c < cols:  # walk the whole diagonal
            if matrix[r][c] != value:
                return False
            r, c = r + 1, c + 1
    return True
""",
        solution=r"""
# OPTIMISED: O(m*n) time, O(1) space
# Idea: Local neighbour check instead of whole-line scans
def is_toeplitz_matrix(matrix):
    return all(
        matrix[r][c] == matrix[r - 1][c - 1]
        for r in range(1, len(matrix))
        for c in range(1, len(matrix[0]))
    )
""",
    ),
    # ---- Flipping an Image (LeetCode 832) ----
    dict(
        title="Flipping an Image",
        diff="E",
        lc=832,
        slug="flipping-an-image",
        prompt=(
            "For a binary square matrix: flip each row horizontally (reverse it), then invert it (0 <-> 1). Return "
            "the result."
        ),
        sig="def flip_and_invert_image(image: List[List[int]]) -> List[List[int]]:",
        fn="flip_and_invert_image",
        tests=[
            (([[1, 1, 0], [1, 0, 1], [0, 0, 0]],), [[1, 0, 0], [0, 1, 0], [1, 1, 1]]),
            (
                ([[1, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0]],),
                [[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 1], [1, 0, 1, 0]],
            ),
            (([[1]],), [[0]]),
        ],
        hints=[
            "Doing it in two passes (reverse, then invert) is fine.",
            "One pass: the new value at position i is 1 - old value at position n - 1 - i.",
            "With two pointers, swap-and-invert both ends together; the middle element of an odd row is just inverted.",
        ],
        pattern="Fuse two passes into one with two pointers",
        explain=(
            "Reverse-then-invert is the same as writing, at each position, the inverted value from the mirrored "
            "position."
        ),
        cx="O(m*n) time",
        brute_cx="O(m*n) time - two separate passes (reverse, then invert)",
        brute=r"""
# BRUTE FORCE: O(m*n) time - two separate passes (reverse, then invert)
def flip_and_invert_image(image):
    flipped = [row[::-1] for row in image]  # pass 1: reverse every row
    return [[1 - v for v in row] for row in flipped]  # pass 2: invert every value
""",
        solution=r"""
# OPTIMISED: O(m*n) time
# Idea: Fuse two passes into one with two pointers
def flip_and_invert_image(image):
    result = [list(row) for row in image]
    for row in result:
        lo, hi = 0, len(row) - 1
        while lo <= hi:
            row[lo], row[hi] = (
                1 - row[hi],
                1 - row[lo],
            )  # swap and invert in one step (works when lo == hi too)
            lo += 1
            hi -= 1
    return result
""",
    ),
    # ---- Cells with Odd Values in a Matrix (LeetCode 1252) ----
    dict(
        title="Cells with Odd Values in a Matrix",
        diff="E",
        lc=1252,
        slug="cells-with-odd-values-in-a-matrix",
        prompt=(
            "Start with an m x n matrix of zeros. For each [r, c] in indices, add 1 to every cell of row r and to "
            "every cell of column c. Return how many cells are odd at the end."
        ),
        sig="def odd_cells(m: int, n: int, indices: List[List[int]]) -> int:",
        fn="odd_cells",
        tests=[
            ((2, 3, [[0, 1], [1, 1]]), 6),
            ((2, 2, [[1, 1], [0, 0]]), 0),
            ((1, 1, [[0, 0]]), 0),
            ((3, 3, [[0, 0]]), 4),
        ],
        hints=[
            "Simulating every increment costs O(m + n) per index.",
            "A cell's final value = (increments to its row) + (increments to its column). Only parity matters.",
            (
                "Count rows with an odd number of increments (R) and columns with an odd number (C). A cell is odd "
                "when exactly one of its row/column is odd: R*(n - C) + C*(m - R)."
            ),
        ],
        pattern="Track parities instead of simulating",
        explain=(
            "Odd + even = odd, odd + odd = even. Counting rows/columns with odd counts gives the answer by simple "
            "multiplication."
        ),
        cx="O(len(indices) + m + n) time",
        brute_cx="O(len(indices) * (m + n) + m*n) time - actually apply every increment",
        brute=r"""
# BRUTE FORCE: O(len(indices) * (m + n) + m*n) time - actually apply every increment
def odd_cells(m, n, indices):
    grid = [[0] * n for _ in range(m)]
    for r, c in indices:
        for j in range(n):
            grid[r][j] += 1  # the whole row
        for i in range(m):
            grid[i][c] += 1  # the whole column
    return sum(v % 2 for row in grid for v in row)
""",
        solution=r"""
# OPTIMISED: O(len(indices) + m + n) time
# Idea: Track parities instead of simulating
def odd_cells(m, n, indices):
    row_odd, col_odd = [0] * m, [0] * n
    for r, c in indices:
        row_odd[r] ^= 1  # flip the parity of this row
        col_odd[c] ^= 1
    rows, cols = sum(row_odd), sum(col_odd)
    return rows * (n - cols) + cols * (
        m - rows
    )  # a cell is odd when exactly one of row/column is odd
""",
    ),
    # ---- Special Positions in a Binary Matrix (LeetCode 1582) ----
    dict(
        title="Special Positions in a Binary Matrix",
        diff="E",
        lc=1582,
        slug="special-positions-in-a-binary-matrix",
        prompt=(
            "A cell is special if it holds 1 and every other cell in its row and column is 0. Return the number of "
            "special cells."
        ),
        sig="def num_special(mat: List[List[int]]) -> int:",
        fn="num_special",
        tests=[
            (([[1, 0, 0], [0, 0, 1], [1, 0, 0]],), 1),
            (([[1, 0, 0], [0, 1, 0], [0, 0, 1]],), 3),
            (([[0, 0], [0, 0]],), 0),
            (([[1, 1], [0, 0]],), 0),
        ],
        hints=[
            "Re-checking a row and column for every 1 costs O(m + n) each.",
            "Precompute the sum of every row and every column once.",
            "A cell is special iff it is 1 and its row sum and column sum are both 1.",
        ],
        pattern="Precompute row and column aggregates",
        explain="One pass builds the sums; a second pass asks O(1) questions about each cell.",
        cx="O(m*n) time, O(m + n) space",
        brute_cx="O(m*n*(m + n)) time - scan the row and column of every 1",
        brute=r"""
# BRUTE FORCE: O(m*n*(m + n)) time - scan the row and column of every 1
def num_special(mat):
    rows, cols, count = len(mat), len(mat[0]), 0
    for r in range(rows):
        for c in range(cols):
            if mat[r][c] == 1:
                others = sum(mat[r][j] for j in range(cols) if j != c) + sum(
                    mat[i][c] for i in range(rows) if i != r
                )
                if others == 0:
                    count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(m*n) time, O(m + n) space
# Idea: Precompute row and column aggregates
def num_special(mat):
    row_sum = [sum(row) for row in mat]
    col_sum = [sum(col) for col in zip(*mat)]
    return sum(
        1
        for r, row in enumerate(mat)
        for c, v in enumerate(row)
        if v == 1 and row_sum[r] == 1 and col_sum[c] == 1
    )
""",
    ),
]
