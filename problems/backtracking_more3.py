"""more Backtracking problems (batch 4) - part of the problem bank for the "backtracking" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Letter Tile Possibilities (LeetCode 1079) ----
    dict(
        title="Letter Tile Possibilities",
        diff="M",
        lc=1079,
        slug="letter-tile-possibilities",
        prompt=(
            "Given tiles with letters on them, return the number of distinct non-empty sequences you can make using "
            "the letters on the tiles (each tile at most once)."
        ),
        sig="def num_tile_possibilities(tiles: str) -> int:",
        fn="num_tile_possibilities",
        tests=[
            (("AAB",), 8),
            (("AAABBC",), 188),
            (("V",), 1),
            (("AB",), 4),
        ],
        hints=[
            "Duplicate letters make the same sequence reachable in several ways - count distinct ones.",
            "Work with letter COUNTS instead of tiles: at each step pick a letter that still has a tile left.",
            "Each pick is one more sequence (count it), then recurse with that letter's count reduced by one.",
        ],
        pattern="Backtracking over a frequency table (no duplicates by construction)",
        explain=(
            "Choosing a LETTER rather than a TILE means two identical tiles lead to the same branch only once, so "
            "no set is needed."
        ),
        cx="O(number of sequences) time",
        brute_cx="O(n! * n) time - generate every permutation of every length into a set",
        brute=r"""
# BRUTE FORCE: O(n! * n) time - generate every permutation of every length into a set
def num_tile_possibilities(tiles):
    sequences = set()
    for length in range(1, len(tiles) + 1):
        for perm in itertools.permutations(tiles, length):
            sequences.add(perm)  # duplicates collapse in the set
    return len(sequences)
""",
        solution=r"""
# OPTIMISED: O(number of sequences) time
# Idea: Backtracking over a frequency table (no duplicates by construction)
def num_tile_possibilities(tiles):
    counts = Counter(tiles)

    def build():
        total = 0
        for letter in counts:
            if counts[letter] > 0:
                counts[letter] -= 1  # use one tile of this letter
                total += 1 + build()  # this sequence, plus everything that extends it
                counts[letter] += 1  # backtrack
        return total

    return build()
""",
    ),
    # ---- Non-decreasing Subsequences (LeetCode 491) ----
    dict(
        title="Non-decreasing Subsequences",
        diff="M",
        lc=491,
        slug="non-decreasing-subsequences",
        prompt="Return all distinct non-decreasing subsequences of nums that have at least two elements (any order).",
        sig="def find_subsequences(nums: List[int]) -> List[List[int]]:",
        fn="find_subsequences",
        compare="unordered",
        tests=[
            (([4, 6, 7, 7],), [[4, 6], [4, 6, 7], [4, 6, 7, 7], [4, 7], [4, 7, 7], [6, 7], [6, 7, 7], [7, 7]]),
            (([4, 4, 3, 2, 1],), [[4, 4]]),
            (([1, 2, 3],), [[1, 2], [1, 2, 3], [1, 3], [2, 3]]),
            (([3, 2, 1],), []),
        ],
        hints=[
            "Build subsequences left to right; only append x if x >= the last chosen element.",
            "Record the current path whenever its length is >= 2.",
            (
                "To avoid duplicates, at each recursion level skip a value that was already tried at that same "
                "level (keep a per-level `used` set)."
            ),
        ],
        pattern="Backtracking with a per-level 'used' set to skip duplicates",
        explain=(
            "The array is not sorted, so the usual 'skip equal neighbours' trick does not apply; a set of values "
            "already tried at this depth does the same job."
        ),
        cx="O(2^n * n) time",
        brute_cx="O(2^n * n) time - enumerate all subsets and de-duplicate with a set",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - enumerate all subsets and de-duplicate with a set
def find_subsequences(nums):
    found = set()
    n = len(nums)
    for mask in range(1, 1 << n):  # every subset of indices
        seq = tuple(nums[i] for i in range(n) if mask >> i & 1)
        if len(seq) >= 2 and all(seq[i] <= seq[i + 1] for i in range(len(seq) - 1)):
            found.add(seq)
    return [list(s) for s in found]
""",
        solution=r"""
# OPTIMISED: O(2^n * n) time
# Idea: Backtracking with a per-level 'used' set to skip duplicates
def find_subsequences(nums):
    result, path = [], []

    def dfs(start):
        if len(path) >= 2:
            result.append(list(path))
        used = set()  # values already tried as the next element at THIS level
        for i in range(start, len(nums)):
            x = nums[i]
            if x in used or (path and x < path[-1]):
                continue
            used.add(x)
            path.append(x)
            dfs(i + 1)
            path.pop()

    dfs(0)
    return result
""",
    ),
    # ---- N-Queens II (LeetCode 52) ----
    dict(
        title="N-Queens II",
        diff="H",
        lc=52,
        slug="n-queens-ii",
        prompt=(
            "Return the number of distinct ways to place n queens on an n x n board so that no two attack each other."
        ),
        sig="def total_n_queens(n: int) -> int:",
        fn="total_n_queens",
        tests=[
            ((1,), 1),
            ((2,), 0),
            ((4,), 2),
            ((5,), 10),
            ((6,), 4),
        ],
        hints=[
            "Exactly one queen per row, so place row by row and choose a column.",
            (
                "A placement conflicts if the column or either diagonal is taken. Diagonals are identified by row - "
                "col and row + col."
            ),
            "Keep three sets (columns, diagonals, anti-diagonals); place, recurse, remove.",
        ],
        pattern="Backtracking with O(1) conflict checks via sets",
        explain=(
            "Checking each placed queen costs O(n) per candidate; the three sets make the check O(1) and prune bad "
            "branches immediately."
        ),
        cx="O(n!) worst case, much less with pruning",
        brute_cx="O(n! * n^2) time - try every permutation of columns and test it",
        brute=r"""
# BRUTE FORCE: O(n! * n^2) time - try every permutation of columns and test it
def total_n_queens(n):
    count = 0
    for cols in itertools.permutations(range(n)):  # cols[r] = column of the queen in row r
        diagonals = {r - c for r, c in enumerate(cols)}
        anti_diagonals = {r + c for r, c in enumerate(cols)}
        if len(diagonals) == n and len(anti_diagonals) == n:  # no shared diagonal
            count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n!) worst case, much less with pruning
# Idea: Backtracking with O(1) conflict checks via sets
def total_n_queens(n):
    cols, diag, anti = set(), set(), set()

    def place(row):
        if row == n:
            return 1
        total = 0
        for col in range(n):
            if col in cols or row - col in diag or row + col in anti:
                continue  # attacked
            cols.add(col)
            diag.add(row - col)
            anti.add(row + col)
            total += place(row + 1)
            cols.remove(col)  # backtrack
            diag.remove(row - col)
            anti.remove(row + col)
        return total

    return place(0)
""",
    ),
]
