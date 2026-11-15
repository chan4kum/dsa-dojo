from core import *

# Matrix / simulation problems. `inplace=N` = the function mutates argument N instead of returning.

PROBLEMS = [
    dict(
        title="Rotate Image", diff="M", lc=48, slug="rotate-image",
        prompt="Rotate an n x n matrix 90 degrees clockwise IN PLACE (do not allocate another matrix).",
        sig="def rotate(matrix: List[List[int]]) -> None:",
        fn="rotate", inplace=0,
        tests=[(([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [[7, 4, 1], [8, 5, 2], [9, 6, 3]]),
               (([[1]],), [[1]]), (([[1, 2], [3, 4]],), [[3, 1], [4, 2]]),
               (([[5, 1, 9, 11], [2, 4, 8, 10], [13, 3, 6, 7], [15, 14, 12, 16]],),
                [[15, 13, 2, 5], [14, 3, 4, 1], [12, 6, 8, 9], [16, 7, 10, 11]])],
        hints=["Where does the cell at (r, c) end up after a clockwise rotation?",
               "(r, c) -> (c, n-1-r). Doing it cell by cell in place needs a 4-cycle swap. Is there something simpler?",
               "Transpose (swap across the main diagonal), then reverse every row."],
        pattern="Matrix transform = composition of simple transforms (transpose + reverse)",
        explain="""
        Clockwise rotation = transpose followed by a horizontal flip. Both are in-place swaps. Counter-clockwise
        = transpose then reverse the columns (or reverse rows first, then transpose).""",
        cx="O(n^2) time, O(1) extra space",
        brute_cx="O(n^2) time, O(n^2) extra space - build a new matrix",
        brute=r'''
def rotate(matrix):
    n = len(matrix)
    new = [[0] * n for _ in range(n)]
    for r in range(n):
        for c in range(n):
            new[c][n - 1 - r] = matrix[r][c]
    for r in range(n):
        matrix[r] = new[r]
''',
        solution=r'''
def rotate(matrix):
    n = len(matrix)
    for r in range(n):
        for c in range(r + 1, n):
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]   # transpose
    for row in matrix:
        row.reverse()                                                  # mirror left-right
''',
    ),
    dict(
        title="Spiral Matrix", diff="M", lc=54, slug="spiral-matrix",
        prompt="Return all elements of an m x n matrix in clockwise spiral order, starting at the top-left.",
        sig="def spiral_order(matrix: List[List[int]]) -> List[int]:",
        fn="spiral_order",
        tests=[(([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [1, 2, 3, 6, 9, 8, 7, 4, 5]),
               (([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12]],), [1, 2, 3, 4, 8, 12, 11, 10, 9, 5, 6, 7]),
               (([[1]],), [1]), (([[1, 2], [3, 4]],), [1, 2, 4, 3]), (([[1], [2], [3]],), [1, 2, 3])],
        hints=["Peel the matrix layer by layer. What four boundaries describe the current layer?",
               "Keep top, bottom, left, right. Walk the top row, right column, bottom row, left column, shrinking each bound after use.",
               "After the top row and the right column, re-check top <= bottom and left <= right before the other two sides (single row/column case)."],
        pattern="Boundary shrinking simulation",
        explain="""
        Four moving walls. After finishing a side, move that wall inward. The guard checks before the bottom and
        left sides prevent double-visiting when only one row or column remains.""",
        cx="O(m*n) time, O(1) extra space",
        brute_cx="O(m*n) time, O(m*n) space - direction vector with a visited grid",
        brute=r'''
def spiral_order(matrix):
    R, C = len(matrix), len(matrix[0])
    seen = [[False] * C for _ in range(R)]
    dirs = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    r = c = d = 0
    out = []
    for _ in range(R * C):
        out.append(matrix[r][c])
        seen[r][c] = True
        nr, nc = r + dirs[d][0], c + dirs[d][1]
        if not (0 <= nr < R and 0 <= nc < C and not seen[nr][nc]):
            d = (d + 1) % 4
            nr, nc = r + dirs[d][0], c + dirs[d][1]
        r, c = nr, nc
    return out
''',
        solution=r'''
def spiral_order(matrix):
    out = []
    top, bottom, left, right = 0, len(matrix) - 1, 0, len(matrix[0]) - 1
    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            out.append(matrix[top][c])
        top += 1
        for r in range(top, bottom + 1):
            out.append(matrix[r][right])
        right -= 1
        if top <= bottom:
            for c in range(right, left - 1, -1):
                out.append(matrix[bottom][c])
            bottom -= 1
        if left <= right:
            for r in range(bottom, top - 1, -1):
                out.append(matrix[r][left])
            left += 1
    return out
''',
    ),
    dict(
        title="Set Matrix Zeroes", diff="M", lc=73, slug="set-matrix-zeroes",
        prompt="If any cell of an m x n matrix is 0, set its entire row and column to 0. Do it in place.",
        sig="def set_zeroes(matrix: List[List[int]]) -> None:",
        fn="set_zeroes", inplace=0,
        tests=[(([[1, 1, 1], [1, 0, 1], [1, 1, 1]],), [[1, 0, 1], [0, 0, 0], [1, 0, 1]]),
               (([[0, 1, 2, 0], [3, 4, 5, 2], [1, 3, 1, 5]],), [[0, 0, 0, 0], [0, 4, 5, 0], [0, 3, 1, 0]]),
               (([[1]],), [[1]]), (([[0]],), [[0]]), (([[1, 0]],), [[0, 0]])],
        hints=["If you zero rows/columns while scanning, new zeros confuse the scan. Record first, apply later.",
               "Two sets (rows with a zero, columns with a zero) work in O(m + n) extra space.",
               "For O(1) space reuse the first row and first column as the markers; remember separately whether they themselves contained a zero."],
        pattern="Two-pass marking (use the input as its own bookkeeping)",
        explain="""
        Pass 1 collects which rows/columns must be cleared; pass 2 clears them. The O(1)-space version stores the
        flags in matrix[0][c] and matrix[r][0] and keeps two booleans for the first row/column themselves.""",
        cx="O(m*n) time, O(m+n) space (O(1) with the first-row/column trick)",
        brute_cx="O((m*n) * (m+n)) - zero as you find zeros, using a copy to read from",
        brute=r'''
def set_zeroes(matrix):
    orig = [row[:] for row in matrix]
    R, C = len(matrix), len(matrix[0])
    for r in range(R):
        for c in range(C):
            if orig[r][c] == 0:
                for k in range(C):
                    matrix[r][k] = 0
                for k in range(R):
                    matrix[k][c] = 0
''',
        solution=r'''
def set_zeroes(matrix):
    R, C = len(matrix), len(matrix[0])
    rows = {r for r in range(R) if 0 in matrix[r]}
    cols = {c for c in range(C) if any(matrix[r][c] == 0 for r in range(R))}
    for r in range(R):
        for c in range(C):
            if r in rows or c in cols:
                matrix[r][c] = 0
''',
    ),
    dict(
        title="Game of Life", diff="M", lc=289, slug="game-of-life",
        prompt="Apply one step of Conway's Game of Life to a grid of 0/1 cells (all cells update simultaneously): a live "
               "cell survives with 2 or 3 live neighbours, a dead cell becomes alive with exactly 3. Mutate the grid in place.",
        sig="def game_of_life(board: List[List[int]]) -> None:",
        fn="game_of_life", inplace=0,
        tests=[(([[0, 1, 0], [0, 0, 1], [1, 1, 1], [0, 0, 0]],), [[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 1, 0]]),
               (([[1, 1], [1, 0]],), [[1, 1], [1, 1]]), (([[1]],), [[0]]), (([[0, 0], [0, 0]],), [[0, 0], [0, 0]])],
        hints=["Updating cells one at a time corrupts the neighbour counts of later cells.",
               "Copy the board and read from the copy (O(mn) space), or encode both the old and the new state in each cell.",
               "In-place trick: use 2 = was alive, becomes dead; 3 = was dead, becomes alive; read old state with `v % 2`... then normalise at the end."],
        pattern="Simulation with simultaneous update (copy, or encode old+new state in the cell)",
        explain="""
        The key requirement is that every cell's next state depends only on the OLD grid. A read-only snapshot
        guarantees it; encoding transitions in extra bit values gives O(1) space.""",
        cx="O(m*n) time, O(1) space with state encoding",
        brute_cx="O(m*n) time, O(m*n) space - snapshot copy",
        brute=r'''
def game_of_life(board):
    old = [row[:] for row in board]
    R, C = len(old), len(old[0])
    for r in range(R):
        for c in range(C):
            live = sum(old[r + dr][c + dc] for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                       if (dr or dc) and 0 <= r + dr < R and 0 <= c + dc < C)
            board[r][c] = 1 if (live == 3 or (old[r][c] and live == 2)) else 0
''',
        solution=r'''
def game_of_life(board):
    R, C = len(board), len(board[0])
    for r in range(R):
        for c in range(C):
            live = sum(board[r + dr][c + dc] % 2 for dr in (-1, 0, 1) for dc in (-1, 0, 1)
                       if (dr or dc) and 0 <= r + dr < R and 0 <= c + dc < C)
            if board[r][c] == 1 and live in (2, 3):
                board[r][c] = 3                     # alive -> alive (bit 1 = next state)
            elif board[r][c] == 0 and live == 3:
                board[r][c] = 2                     # dead -> alive
    for r in range(R):
        for c in range(C):
            board[r][c] >>= 1                       # next state lives in the second bit
''',
    ),
    dict(
        title="Valid Sudoku", diff="M", lc=36, slug="valid-sudoku",
        prompt="Given a partially filled 9x9 Sudoku board ('.' = empty), decide whether the filled cells obey the rules: "
               "no repeated digit in any row, column or 3x3 box. (It need not be solvable.)",
        sig="def is_valid_sudoku(board: List[List[str]]) -> bool:",
        fn="is_valid_sudoku",
        tests=[((["53..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "....8..79"],), True),
               ((["83..7....", "6..195...", ".98....6.", "8...6...3", "4..8.3..1", "7...2...6", ".6....28.", "...419..5", "....8..79"],), False),
               ((["........."] * 9,), True),
               ((["11.......", ".........", ".........", ".........", ".........", ".........", ".........", ".........", "........."],), False)],
        hints=["There are 27 groups to check: 9 rows, 9 columns, 9 boxes.",
               "Track what you have seen in each row, column and box while scanning once.",
               "Box index of (r, c) is (r // 3) * 3 + c // 3. A set per row/column/box; if a digit is already in any of its three sets, invalid."],
        pattern="Hash sets keyed by row / column / box (index arithmetic)",
        explain="""
        One scan, three arrays of 9 sets. The only trick is the box index formula. Same idea validates N-Queens
        columns/diagonals (backtracking) and Sudoku solvers.""",
        cx="O(81) = O(1) time and space",
        brute_cx="O(81 * 27) - re-extract and test each of the 27 groups separately",
        brute=r'''
def is_valid_sudoku(board):
    def ok(cells):
        digits = [c for c in cells if c != "."]
        return len(digits) == len(set(digits))
    rows = [board[r] for r in range(9)]
    cols = [[board[r][c] for r in range(9)] for c in range(9)]
    boxes = [[board[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)] for br in (0, 3, 6) for bc in (0, 3, 6)]
    return all(ok(g) for g in rows + cols + boxes)
''',
        solution=r'''
def is_valid_sudoku(board):
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]
    for r in range(9):
        for c in range(9):
            d = board[r][c]
            if d == ".":
                continue
            b = (r // 3) * 3 + c // 3
            if d in rows[r] or d in cols[c] or d in boxes[b]:
                return False
            rows[r].add(d); cols[c].add(d); boxes[b].add(d)
    return True
''',
    ),
]
