"""more Matrix problems (batch 5) - part of the problem bank for the "matrix" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Diagonal Traverse (LeetCode 498) ----
    dict(
        title="Diagonal Traverse",
        diff="M",
        lc=498,
        slug="diagonal-traverse",
        prompt=(
            "Return all elements of an m x n matrix in diagonal zig-zag order: start at the top-left going "
            "up-right, bounce off the borders, alternate directions."
        ),
        sig="def find_diagonal_order(mat: List[List[int]]) -> List[int]:",
        fn="find_diagonal_order",
        tests=[
            (([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), [1, 2, 4, 7, 5, 3, 6, 8, 9]),
            (([[1, 2], [3, 4]],), [1, 2, 3, 4]),
            (([[1]],), [1]),
            (([[1, 2, 3]],), [1, 2, 3]),
        ],
        hints=[
            "All cells on one diagonal share the same value of row + column.",
            "Diagonals with even row + column are walked upwards, odd ones downwards.",
            (
                "Or simulate: keep a direction; when you would leave the grid, step to the next diagonal and flip "
                "direction (check the right border before the top border when going up)."
            ),
        ],
        pattern="Simulation with direction flips (or group by i + j)",
        explain=(
            "Each step either continues diagonally or bounces off a border; the bounce rules are fixed per "
            "direction, so the traversal is a single O(mn) walk."
        ),
        cx="O(m * n) time",
        brute_cx="O(m * n) time but extra memory - group cells by i + j, reverse the even groups",
        brute=r"""
# BRUTE FORCE: O(m * n) time but extra memory - group cells by i + j, reverse the even groups
def find_diagonal_order(mat):
    m, n = len(mat), len(mat[0])
    order = []
    for s in range(m + n - 1):
        diagonal = [mat[i][s - i] for i in range(max(0, s - n + 1), min(m, s + 1))]  # top to bottom
        order.extend(diagonal[::-1] if s % 2 == 0 else diagonal)
    return order
""",
        solution=r"""
# OPTIMISED: O(m * n) time
# Idea: Simulation with direction flips (or group by i + j)
def find_diagonal_order(mat):
    m, n = len(mat), len(mat[0])
    r = c = 0
    up = True
    order = []

    for _ in range(m * n):
        order.append(mat[r][c])

        if up:
            if c == n - 1:  # hit the right wall: drop down a row
                r += 1
                up = False
            elif r == 0:  # hit the top wall: slide right
                c += 1
                up = False
            else:
                r, c = r - 1, c + 1
        else:
            if r == m - 1:  # hit the bottom wall: slide right
                c += 1
                up = True
            elif c == 0:  # hit the left wall: drop down
                r += 1
                up = True
            else:
                r, c = r + 1, c - 1

    return order
""",
    ),
    # ---- Score After Flipping Matrix (LeetCode 861) ----
    dict(
        title="Score After Flipping Matrix",
        diff="M",
        lc=861,
        slug="score-after-flipping-matrix",
        prompt=(
            "A move flips every bit in one row or one column of a binary matrix. Each row is read as a binary "
            "number; the score is the sum of the rows. Return the maximum score after any number of moves."
        ),
        sig="def matrix_score(grid: List[List[int]]) -> int:",
        fn="matrix_score",
        tests=[
            (([[0, 0, 1, 1], [1, 0, 1, 0], [1, 1, 0, 0]],), 39),
            (([[0]],), 1),
            (([[1, 1], [0, 0]],), 6),
            (([[0, 1], [0, 1]],), 6),
        ],
        hints=[
            "The leftmost bit is worth more than ALL the other bits of that row combined.",
            "So first flip rows so that every row starts with 1.",
            (
                "After that, flip each other column independently whenever it has more 0s than 1s; add up the "
                "column values."
            ),
        ],
        pattern="Greedy by bit significance",
        explain=(
            "Flipping a row to get a leading 1 beats anything the lower bits could give, and once the first column "
            "is fixed the remaining columns are independent, so each is set to its majority bit."
        ),
        cx="O(m * n) time",
        brute_cx="O(2^m * m * n) time - try every set of row flips, then the best column choice",
        brute=r"""
# BRUTE FORCE: O(2^m * m * n) time - try every set of row flips, then the best column choice
def matrix_score(grid):
    m, n = len(grid), len(grid[0])
    best = 0

    for mask in range(1 << m):
        rows = [[b ^ (mask >> i & 1) for b in grid[i]] for i in range(m)]
        score = 0
        for j in range(n):
            ones = sum(rows[i][j] for i in range(m))
            score += max(ones, m - ones) << (n - 1 - j)  # flip the column if that gives more ones
        best = max(best, score)

    return best
""",
        solution=r"""
# OPTIMISED: O(m * n) time
# Idea: Greedy by bit significance
def matrix_score(grid):
    m, n = len(grid), len(grid[0])
    score = m * (1 << (n - 1))  # every row gets a leading 1 after row flips
    for j in range(1, n):
        ones = sum(grid[i][j] == grid[i][0] for i in range(m))  # bit j after normalising row i
        score += max(ones, m - ones) << (n - 1 - j)
    return score
""",
    ),
    # ---- Shift 2D Grid (LeetCode 1260) ----
    dict(
        title="Shift 2D Grid",
        diff="E",
        lc=1260,
        slug="shift-2d-grid",
        prompt=(
            "One shift moves every element one place right; the last element of a row wraps to the first of the "
            "next row, and the very last element wraps to the top-left. Return the grid after k shifts."
        ),
        sig="def shift_grid(grid: List[List[int]], k: int) -> List[List[int]]:",
        fn="shift_grid",
        tests=[
            (([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1), [[9, 1, 2], [3, 4, 5], [6, 7, 8]]),
            (
                ([[3, 8, 1, 9], [19, 7, 2, 5], [4, 6, 11, 10], [12, 0, 21, 13]], 4),
                [[12, 0, 21, 13], [3, 8, 1, 9], [19, 7, 2, 5], [4, 6, 11, 10]],
            ),
            (([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 9), [[1, 2, 3], [4, 5, 6], [7, 8, 9]]),
        ],
        hints=[
            "Read the grid row by row as one long list; a shift is just a rotation of that list.",
            "Rotating by k is the same as rotating by k % (m * n).",
            "Cell with flat index p moves to flat index (p + k) % (m * n); convert with divmod(p, n).",
        ],
        pattern="Flatten the grid, use index arithmetic",
        explain=(
            "The wrap-around rule is exactly a cyclic shift of the row-major list, so one modulo replaces k "
            "separate passes."
        ),
        cx="O(m * n) time",
        brute_cx="O(k * m * n) time - perform the shifts one by one",
        brute=r"""
# BRUTE FORCE: O(k * m * n) time - perform the shifts one by one
def shift_grid(grid, k):
    m, n = len(grid), len(grid[0])
    grid = [row[:] for row in grid]

    for _ in range(k):
        new = [[0] * n for _ in range(m)]

        for i in range(m):
            for j in range(n):
                if j + 1 < n:
                    new[i][j + 1] = grid[i][j]
                elif i + 1 < m:
                    new[i + 1][0] = grid[i][j]  # wrap to the next row
                else:
                    new[0][0] = grid[i][j]  # wrap to the top-left

        grid = new

    return grid
""",
        solution=r"""
# OPTIMISED: O(m * n) time
# Idea: Flatten the grid, use index arithmetic
def shift_grid(grid, k):
    m, n = len(grid), len(grid[0])
    result = [[0] * n for _ in range(m)]
    for p in range(m * n):
        i, j = divmod(p, n)
        q = (p + k) % (m * n)  # where this element lands in row-major order
        result[q // n][q % n] = grid[i][j]
    return result
""",
    ),
    # ---- Count Square Submatrices with All Ones (LeetCode 1277) ----
    dict(
        title="Count Square Submatrices with All Ones",
        diff="M",
        lc=1277,
        slug="count-square-submatrices-with-all-ones",
        prompt=(
            "Return how many square submatrices of the binary matrix consist only of 1s (squares of every size count)."
        ),
        sig="def count_squares(matrix: List[List[int]]) -> int:",
        fn="count_squares",
        tests=[
            (([[0, 1, 1, 1], [1, 1, 1, 1], [0, 1, 1, 1]],), 15),
            (([[1, 0, 1], [1, 1, 0], [1, 1, 0]],), 7),
            (([[1]],), 1),
            (([[0, 0]],), 0),
        ],
        hints=[
            "Let f(i, j) be the side of the LARGEST all-ones square whose bottom-right corner is (i, j).",
            (
                "That square also gives f(i, j) - 1, ... , 1 smaller squares ending at the same corner, so f(i, j) "
                "is the number of squares with that corner."
            ),
            "f(i, j) = 1 + min(up, left, up-left) when the cell is 1, else 0. Sum all f.",
        ],
        pattern="2D DP: largest square ending at each cell",
        explain=(
            "A square of side k at (i, j) needs squares of side k - 1 above, left and diagonal, so the minimum of "
            "those three limits it. Summing f counts each square exactly once, at its bottom-right corner."
        ),
        cx="O(m * n) time",
        brute_cx="O(m * n * min(m, n)^3) time - test every square directly",
        brute=r"""
# BRUTE FORCE: O(m * n * min(m, n)^3) time - test every square directly
def count_squares(matrix):
    m, n = len(matrix), len(matrix[0])
    count = 0

    for i in range(m):
        for j in range(n):
            for size in range(1, min(m - i, n - j) + 1):
                if all(matrix[r][c] for r in range(i, i + size) for c in range(j, j + size)):
                    count += 1

    return count
""",
        solution=r"""
# OPTIMISED: O(m * n) time
# Idea: 2D DP: largest square ending at each cell
def count_squares(matrix):
    m, n = len(matrix), len(matrix[0])
    f = [row[:] for row in matrix]  # f[i][j]: biggest square ending at (i, j)
    total = 0

    for i in range(m):
        for j in range(n):
            if f[i][j] and i and j:
                f[i][j] = 1 + min(f[i - 1][j], f[i][j - 1], f[i - 1][j - 1])
            total += f[i][j]

    return total
""",
    ),
    # ---- Count Negative Numbers in a Sorted Matrix (LeetCode 1351) ----
    dict(
        title="Count Negative Numbers in a Sorted Matrix",
        diff="E",
        lc=1351,
        slug="count-negative-numbers-in-a-sorted-matrix",
        prompt=(
            "Every row and every column of the matrix is sorted in non-increasing order. Return the number of "
            "negative numbers."
        ),
        sig="def count_negatives(grid: List[List[int]]) -> int:",
        fn="count_negatives",
        tests=[
            (([[4, 3, 2, -1], [3, 2, 1, -1], [1, 1, -1, -2], [-1, -1, -2, -3]],), 8),
            (([[3, 2], [1, 0]],), 0),
            (([[-1]],), 1),
            (([[1, -1], [-1, -1]],), 3),
        ],
        hints=[
            "The negatives form a staircase in the bottom-right corner.",
            "Start at the top-right cell. If it is negative, the whole column below it is negative; if not, move down.",
            "Walk left/down only: each step eliminates a row or a column, so at most m + n steps.",
        ],
        pattern="Staircase walk on a doubly-sorted matrix",
        explain=(
            "Sortedness in both directions means one comparison rules out a full row or column, so we never revisit "
            "anything."
        ),
        cx="O(m + n) time",
        brute_cx="O(m * n) time - test every cell",
        brute=r"""
# BRUTE FORCE: O(m * n) time - test every cell
def count_negatives(grid):
    return sum(1 for row in grid for x in row if x < 0)
""",
        solution=r"""
# OPTIMISED: O(m + n) time
# Idea: Staircase walk on a doubly-sorted matrix
def count_negatives(grid):
    m, n = len(grid), len(grid[0])
    r, c, count = 0, n - 1, 0

    while r < m and c >= 0:
        if grid[r][c] < 0:
            count += m - r  # everything below in this column is negative too
            c -= 1
        else:
            r += 1

    return count
""",
    ),
    # ---- Lucky Numbers in a Matrix (LeetCode 1380) ----
    dict(
        title="Lucky Numbers in a Matrix",
        diff="E",
        lc=1380,
        slug="lucky-numbers-in-a-matrix",
        prompt=(
            "A lucky number is the minimum of its row AND the maximum of its column. All numbers in the matrix are "
            "distinct. Return every lucky number (any order)."
        ),
        sig="def lucky_numbers(matrix: List[List[int]]) -> List[int]:",
        fn="lucky_numbers",
        compare="unordered",
        tests=[
            (([[3, 7, 8], [9, 11, 13], [15, 16, 17]],), [15]),
            (([[1, 10, 4, 2], [9, 3, 8, 7], [15, 16, 17, 12]],), [12]),
            (([[7, 8], [1, 2]],), [7]),
        ],
        hints=[
            "Checking each cell against its whole row and column repeats work.",
            "Compute every row's minimum and every column's maximum once.",
            "A cell is lucky when it equals both its row minimum and its column maximum.",
        ],
        pattern="Precompute row minima and column maxima",
        explain="Two O(mn) passes give the extremes, after which each cell is judged with two comparisons.",
        cx="O(m * n) time, O(m + n) space",
        brute_cx="O(m * n * (m + n)) time - rescan the row and column of every cell",
        brute=r"""
# BRUTE FORCE: O(m * n * (m + n)) time - rescan the row and column of every cell
def lucky_numbers(matrix):
    m, n = len(matrix), len(matrix[0])
    return [
        matrix[i][j]
        for i in range(m)
        for j in range(n)
        if matrix[i][j] == min(matrix[i]) and matrix[i][j] == max(matrix[r][j] for r in range(m))
    ]
""",
        solution=r"""
# OPTIMISED: O(m * n) time, O(m + n) space
# Idea: Precompute row minima and column maxima
def lucky_numbers(matrix):
    row_min = [min(row) for row in matrix]
    col_max = [max(col) for col in zip(*matrix)]

    return [
        x
        for i, row in enumerate(matrix)
        for j, x in enumerate(row)
        if x == row_min[i] == col_max[j]
    ]
""",
    ),
    # ---- Count Submatrices With All Ones (LeetCode 1504) ----
    dict(
        title="Count Submatrices With All Ones",
        diff="M",
        lc=1504,
        slug="count-submatrices-with-all-ones",
        prompt="Return the number of rectangular submatrices of the binary matrix that contain only 1s.",
        sig="def num_submat(mat: List[List[int]]) -> int:",
        fn="num_submat",
        tests=[
            (([[1, 0, 1], [1, 1, 0], [1, 1, 0]],), 13),
            (([[0, 1, 1, 0], [0, 1, 1, 1], [1, 1, 1, 0]],), 24),
            (([[1]],), 1),
            (([[0]],), 0),
        ],
        hints=[
            "Count rectangles by their BOTTOM-RIGHT corner.",
            "Keep height[j] = number of consecutive 1s ending at row i in column j.",
            (
                "For a corner (i, j), walk left over columns k = j, j-1, ... keeping the minimum height seen; each "
                "step adds that minimum rectangles."
            ),
        ],
        pattern="Histogram heights + expand left with a running minimum",
        explain=(
            "A rectangle with bottom-right corner (i, j) and width w has height up to the minimum column height "
            "among the w columns, so summing the running minimum counts all of them."
        ),
        cx="O(m * n^2) time",
        brute_cx="O(m^2 * n^2) time - check every rectangle with a 2D prefix table",
        brute=r"""
# BRUTE FORCE: O(m^2 * n^2) time - check every rectangle with a 2D prefix table
def num_submat(mat):
    m, n = len(mat), len(mat[0])
    prefix = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m):
        for j in range(n):
            prefix[i + 1][j + 1] = mat[i][j] + prefix[i][j + 1] + prefix[i + 1][j] - prefix[i][j]

    count = 0

    for r1 in range(m):
        for r2 in range(r1, m):
            for c1 in range(n):
                for c2 in range(c1, n):
                    ones = (
                        prefix[r2 + 1][c2 + 1]
                        - prefix[r1][c2 + 1]
                        - prefix[r2 + 1][c1]
                        + prefix[r1][c1]
                    )

                    if ones == (r2 - r1 + 1) * (c2 - c1 + 1):  # every cell is a 1
                        count += 1

    return count
""",
        solution=r"""
# OPTIMISED: O(m * n^2) time
# Idea: Histogram heights + expand left with a running minimum
def num_submat(mat):
    m, n = len(mat), len(mat[0])
    height = [0] * n
    total = 0

    for i in range(m):
        for j in range(n):
            height[j] = height[j] + 1 if mat[i][j] else 0

        for j in range(n):
            low = height[j]
            for k in range(j, -1, -1):  # widen the rectangle leftwards
                low = min(low, height[k])
                if low == 0:
                    break
                total += low

    return total
""",
    ),
    # ---- Largest 1-Bordered Square (LeetCode 1139) ----
    dict(
        title="Largest 1-Bordered Square",
        diff="M",
        lc=1139,
        slug="largest-1-bordered-square",
        prompt=(
            "Return the number of elements (area) in the largest square subgrid whose BORDER cells are all 1 (the "
            "inside may be anything). Return 0 if there is none."
        ),
        sig="def largest1_bordered_square(grid: List[List[int]]) -> int:",
        fn="largest1_bordered_square",
        tests=[
            (([[1, 1, 1], [1, 0, 1], [1, 1, 1]],), 9),
            (([[1, 1, 0, 0]],), 1),
            (([[0]],), 0),
            (([[1, 1], [1, 1]],), 4),
        ],
        hints=[
            "Checking the border of every square cell by cell is expensive.",
            "Precompute for each cell how many consecutive 1s extend to the left and upwards.",
            (
                "A square of side s with bottom-right (i, j) is valid if left[i][j] and up[i][j] are >= s AND the "
                "top-left corner's right and down runs are >= s. Try s from large to small."
            ),
        ],
        pattern="Precomputed run lengths, check borders in O(1)",
        explain=(
            "The four sides of a bordered square are each a straight run of ones, and runs are known in O(1) after "
            "one preprocessing pass."
        ),
        cx="O(n^3) time",
        brute_cx="O(n^5) time - verify every square's border cell by cell",
        brute=r"""
# BRUTE FORCE: O(n^5) time - verify every square's border cell by cell
def largest1_bordered_square(grid):
    m, n = len(grid), len(grid[0])
    best = 0

    for i in range(m):
        for j in range(n):
            for side in range(1, min(m - i, n - j) + 1):
                border = all(
                    grid[i][j + k] and grid[i + side - 1][j + k] for k in range(side)
                ) and all(grid[i + k][j] and grid[i + k][j + side - 1] for k in range(side))
                if border:
                    best = max(best, side * side)

    return best
""",
        solution=r"""
# OPTIMISED: O(n^3) time
# Idea: Precomputed run lengths, check borders in O(1)
def largest1_bordered_square(grid):
    m, n = len(grid), len(grid[0])
    left = [[0] * n for _ in range(m)]  # consecutive ones ending here, going left
    up = [[0] * n for _ in range(m)]  # consecutive ones ending here, going up

    for i in range(m):
        for j in range(n):
            if grid[i][j]:
                left[i][j] = (left[i][j - 1] if j else 0) + 1
                up[i][j] = (up[i - 1][j] if i else 0) + 1

    best = 0

    for i in range(m):
        for j in range(n):
            side = min(left[i][j], up[i][j])  # largest side the bottom-right corner could support
            while side > best:  # only sizes that can improve the answer
                if left[i - side + 1][j] >= side and up[i][j - side + 1] >= side:
                    best = side
                    break
                side -= 1

    return best * best
""",
    ),
    # ---- Minimum Swaps to Arrange a Binary Grid (LeetCode 1536) ----
    dict(
        title="Minimum Swaps to Arrange a Binary Grid",
        diff="M",
        lc=1536,
        slug="minimum-swaps-to-arrange-a-binary-grid",
        prompt=(
            "One move swaps two ADJACENT rows of an n x n binary grid. The grid is valid when every cell above the "
            "main diagonal is 0. Return the minimum number of moves, or -1 if impossible."
        ),
        sig="def min_swaps(grid: List[List[int]]) -> int:",
        fn="min_swaps",
        tests=[
            (([[0, 0, 1], [1, 1, 0], [1, 0, 0]],), 3),
            (([[0, 1, 1, 0], [0, 1, 1, 0], [0, 1, 1, 0], [0, 1, 1, 0]],), -1),
            (([[1, 0, 0], [1, 1, 0], [1, 1, 1]],), 0),
            (([[0]],), 0),
        ],
        hints=[
            "Only the number of trailing zeros of each row matters.",
            "Row i (0-indexed) needs at least n - 1 - i trailing zeros.",
            (
                "Greedy from the top: for each position take the NEAREST row below that has enough trailing zeros, "
                "and bubble it up, counting swaps. If none exists the answer is -1."
            ),
        ],
        pattern="Greedy bubble-up using trailing-zero counts",
        explain=(
            "Moving the nearest qualifying row up disturbs the fewest other rows, and rows already placed never "
            "need to move again."
        ),
        cx="O(n^2) time",
        brute_cx="O(n! * n^2) time - BFS over every row ordering",
        brute=r"""
# BRUTE FORCE: O(n! * n^2) time - BFS over every row ordering
def min_swaps(grid):
    n = len(grid)

    def valid(rows):
        return all(not any(rows[i][i + 1 :]) for i in range(n))

    start = tuple(tuple(r) for r in grid)
    seen, queue = {start}, deque([(start, 0)])

    while queue:
        rows, moves = queue.popleft()

        if valid(rows):
            return moves

        for i in range(n - 1):
            nxt = list(rows)
            nxt[i], nxt[i + 1] = nxt[i + 1], nxt[i]
            state = tuple(nxt)
            if state not in seen:
                seen.add(state)
                queue.append((state, moves + 1))

    return -1
""",
        solution=r"""
# OPTIMISED: O(n^2) time
# Idea: Greedy bubble-up using trailing-zero counts
def min_swaps(grid):
    n = len(grid)
    trailing = []

    for row in grid:
        zeros = 0
        while zeros < n and row[n - 1 - zeros] == 0:
            zeros += 1
        trailing.append(zeros)

    swaps = 0

    for i in range(n):
        need = n - 1 - i
        j = i

        while j < n and trailing[j] < need:  # nearest row that qualifies
            j += 1

        if j == n:
            return -1

        swaps += j - i
        trailing.insert(i, trailing.pop(j))  # bubble it up to position i

    return swaps
""",
    ),
    # ---- First Completely Painted Row or Column (LeetCode 2661) ----
    dict(
        title="First Completely Painted Row or Column",
        diff="M",
        lc=2661,
        slug="first-completely-painted-row-or-column",
        prompt=(
            "arr is a permutation of 1..m*n and mat holds each of those numbers exactly once. Paint the cell "
            "containing arr[i] on step i. Return the smallest i after which some entire row or entire column is "
            "painted."
        ),
        sig="def first_complete_index(arr: List[int], mat: List[List[int]]) -> int:",
        fn="first_complete_index",
        tests=[
            (([1, 3, 4, 2], [[1, 4], [2, 3]]), 2),
            (([2, 8, 7, 4, 1, 3, 5, 6, 9], [[3, 2, 5], [1, 4, 6], [8, 7, 9]]), 3),
            (([1], [[1]]), 0),
        ],
        hints=[
            "You need to find a number's cell quickly: build a map value -> (row, column).",
            "Keep a counter of painted cells per row and per column.",
            (
                "Process arr in order; the first time a row counter reaches n or a column counter reaches m, return "
                "that index."
            ),
        ],
        pattern="Position map + per-row/column counters",
        explain=(
            "Painting a cell only changes one row counter and one column counter, so completion can be detected in "
            "O(1) per step."
        ),
        cx="O(m * n) time",
        brute_cx="O(m * n * (m + n)) time - rescan all rows and columns after every paint",
        brute=r"""
# BRUTE FORCE: O(m * n * (m + n)) time - rescan all rows and columns after every paint
def first_complete_index(arr, mat):
    m, n = len(mat), len(mat[0])
    painted = set()

    for i, value in enumerate(arr):
        painted.add(value)
        rows_done = any(all(mat[r][c] in painted for c in range(n)) for r in range(m))
        cols_done = any(all(mat[r][c] in painted for r in range(m)) for c in range(n))
        if rows_done or cols_done:
            return i
""",
        solution=r"""
# OPTIMISED: O(m * n) time
# Idea: Position map + per-row/column counters
def first_complete_index(arr, mat):
    m, n = len(mat), len(mat[0])
    where = {mat[r][c]: (r, c) for r in range(m) for c in range(n)}
    row_count, col_count = [0] * m, [0] * n

    for i, value in enumerate(arr):
        r, c = where[value]
        row_count[r] += 1
        col_count[c] += 1
        if row_count[r] == n or col_count[c] == m:
            return i
""",
    ),
    # ---- Difference Between Ones and Zeros in Row and Column (LeetCode 2482) ----
    dict(
        title="Difference Between Ones and Zeros in Row and Column",
        diff="M",
        lc=2482,
        slug="difference-between-ones-and-zeros-in-row-and-column",
        prompt=(
            "For a binary matrix build diff where diff[i][j] = (ones in row i) + (ones in column j) - (zeros in row "
            "i) - (zeros in column j). Return diff."
        ),
        sig="def ones_minus_zeros(grid: List[List[int]]) -> List[List[int]]:",
        fn="ones_minus_zeros",
        tests=[
            (([[0, 1, 1], [1, 0, 1], [0, 0, 1]],), [[0, 0, 4], [0, 0, 4], [-2, -2, 2]]),
            (([[1, 1, 1], [1, 1, 1]],), [[5, 5, 5], [5, 5, 5]]),
            (([[0]],), [[-2]]),
        ],
        hints=[
            "Zeros in a row = n - ones in that row (same for columns).",
            "So only the number of ones in each row and each column is needed.",
            "Count them once; then diff[i][j] = 2 * row_ones[i] + 2 * col_ones[j] - m - n.",
        ],
        pattern="Precompute row and column counts",
        explain=(
            "Every cell shares its row's and column's totals with its neighbours, so computing the totals once "
            "avoids rescanning for each cell."
        ),
        cx="O(m * n) time",
        brute_cx="O(m * n * (m + n)) time - recount the row and column for every cell",
        brute=r"""
# BRUTE FORCE: O(m * n * (m + n)) time - recount the row and column for every cell
def ones_minus_zeros(grid):
    m, n = len(grid), len(grid[0])
    result = []

    for i in range(m):
        row = []
        for j in range(n):
            ones_r = sum(grid[i])
            ones_c = sum(grid[r][j] for r in range(m))
            row.append(ones_r + ones_c - (n - ones_r) - (m - ones_c))
        result.append(row)

    return result
""",
        solution=r"""
# OPTIMISED: O(m * n) time
# Idea: Precompute row and column counts
def ones_minus_zeros(grid):
    m, n = len(grid), len(grid[0])
    row_ones = [sum(row) for row in grid]
    col_ones = [sum(col) for col in zip(*grid)]
    return [[2 * row_ones[i] + 2 * col_ones[j] - m - n for j in range(n)] for i in range(m)]
""",
    ),
]
