"""extra batch of Backtracking problems - the problem bank for the "backtracking" topic.

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
    # ---- Combinations (LeetCode 77) ----
    dict(
        title="Combinations",
        diff="M",
        lc=77,
        slug="combinations",
        prompt=(
            "Return all combinations of k numbers chosen from 1..n (any order of the combinations; numbers inside "
            "ascending)."
        ),
        sig="def combine(n: int, k: int) -> List[List[int]]:",
        fn="combine",
        compare="unordered",
        tests=[
            ((4, 2), [[1, 2], [1, 3], [1, 4], [2, 3], [2, 4], [3, 4]]),
            ((1, 1), [[1]]),
            ((3, 3), [[1, 2, 3]]),
            ((3, 1), [[1], [2], [3]]),
        ],
        hints=[
            (
                "You are choosing a subset of fixed size. Decide numbers in increasing order to avoid duplicates "
                "like [1,2] and [2,1]."
            ),
            "dfs(start, path): try each number from start..n, add it, recurse with start = number+1.",
            "Stop when len(path) == k. Prune: if there are not enough numbers left to reach k, stop early.",
        ],
        pattern="Backtracking: choose / explore / un-choose (subsets of size k)",
        explain=(
            "The 'start' index enforces increasing order, so every combination is built exactly once. The pruning "
            "bound\n        n - (k - len(path)) + 1 stops branches that can no longer reach size k."
        ),
        cx="O(C(n,k) * k) time",
        brute_cx="O(2^n) time - generate every subset and filter by size",
        brute=r"""
# BRUTE FORCE: O(2^n) time - generate every subset and filter by size
def combine(n, k):
    return [
        [i + 1 for i in range(n) if mask >> i & 1]
        for mask in range(1 << n)
        if bin(mask).count("1") == k
    ]
""",
        solution=r"""
# OPTIMISED: O(C(n,k) * k) time
# Idea: Backtracking: choose / explore / un-choose (subsets of size k)
def combine(n, k):
    res, path = [], []

    def dfs(start):
        if len(path) == k:
            res.append(path[:])
            return
        for x in range(start, n - (k - len(path)) + 2):  # prune: enough numbers must remain
            path.append(x)
            dfs(x + 1)
            path.pop()

    dfs(1)
    return res
""",
    ),
    # ---- Combination Sum II (LeetCode 40) ----
    dict(
        title="Combination Sum II",
        diff="M",
        lc=40,
        slug="combination-sum-ii",
        prompt=(
            "Candidates may contain duplicates; each element may be used at most once. Return all UNIQUE "
            "combinations summing to target (inner lists ascending)."
        ),
        sig="def combination_sum2(candidates: List[int], target: int) -> List[List[int]]:",
        fn="combination_sum2",
        compare="unordered",
        tests=[
            (([10, 1, 2, 7, 6, 1, 5], 8), [[1, 1, 6], [1, 2, 5], [1, 7], [2, 6]]),
            (([2, 5, 2, 1, 2], 5), [[1, 2, 2], [5]]),
            (([1], 2), []),
            (([1, 1], 2), [[1, 1]]),
        ],
        hints=[
            "Duplicates in the input would create duplicate combinations. How can sorting help?",
            "Sort. At the same recursion level, skip a value equal to the previous one you already tried.",
            (
                "if i > start and cand[i] == cand[i-1]: continue. Recurse with i+1 (each element used once) and "
                "stop when the remainder is < 0."
            ),
        ],
        pattern="Backtracking with sorted input + 'skip duplicates at the same depth'",
        explain=(
            "After sorting, equal values are adjacent. Using the first of a run at a given depth already covers "
            "every\n        arrangement that uses the later ones, so later equal siblings are skipped (but may "
            "still be used deeper)."
        ),
        cx="O(2^n) time worst case",
        brute_cx="O(2^n * n) time - all subsets (as a set to dedupe), keep sum == target",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - all subsets (as a set to dedupe), keep sum == target
def combination_sum2(candidates, target):
    c = sorted(candidates)
    found = set()
    for r in range(len(c) + 1):
        for comb in itertools.combinations(c, r):
            if sum(comb) == target:
                found.add(comb)
    return [list(x) for x in found]
""",
        solution=r"""
# OPTIMISED: O(2^n) time worst case
# Idea: Backtracking with sorted input + 'skip duplicates at the same depth'
def combination_sum2(candidates, target):
    cand = sorted(candidates)
    res, path = [], []

    def dfs(start, remain):
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(cand)):
            if cand[i] > remain:
                break
            if i > start and cand[i] == cand[i - 1]:
                continue
            path.append(cand[i])
            dfs(i + 1, remain - cand[i])
            path.pop()

    dfs(0, target)
    return res
""",
    ),
    # ---- Permutations II (LeetCode 47) ----
    dict(
        title="Permutations II",
        diff="M",
        lc=47,
        slug="permutations-ii",
        prompt="nums may contain duplicates. Return all UNIQUE permutations (any order).",
        sig="def permute_unique(nums: List[int]) -> List[List[int]]:",
        fn="permute_unique",
        compare="unordered",
        tests=[
            (([1, 1, 2],), [[1, 1, 2], [1, 2, 1], [2, 1, 1]]),
            (([1, 2, 3],), [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]),
            (([1],), [[1]]),
            (([2, 2],), [[2, 2]]),
        ],
        hints=[
            "Plain permutation code produces duplicates when values repeat.",
            "Count occurrences (Counter) and build the permutation position by position from distinct values.",
            "dfs: for each value v with count[v] > 0: take it (count--), recurse, restore (count++).",
        ],
        pattern="Backtracking over a multiset (counter instead of a used[] array)",
        explain=(
            "Choosing among DISTINCT values at each position makes duplicate permutations impossible by "
            "construction -\n        no dedupe step needed."
        ),
        cx="O(n * n!) worst case",
        brute_cx="O(n * n!) time - all permutations in a set",
        brute=r"""
# BRUTE FORCE: O(n * n!) time - all permutations in a set
def permute_unique(nums):
    return [list(p) for p in set(itertools.permutations(nums))]
""",
        solution=r"""
# OPTIMISED: O(n * n!) worst case
# Idea: Backtracking over a multiset (counter instead of a used[] array)
def permute_unique(nums):
    cnt = Counter(nums)
    res, path = [], []

    def dfs():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for v in list(cnt):
            if cnt[v]:
                cnt[v] -= 1
                path.append(v)
                dfs()
                path.pop()
                cnt[v] += 1

    dfs()
    return res
""",
    ),
    # ---- Subsets II (LeetCode 90) ----
    dict(
        title="Subsets II",
        diff="M",
        lc=90,
        slug="subsets-ii",
        prompt="nums may contain duplicates. Return all UNIQUE subsets (inner lists ascending, any outer order).",
        sig="def subsets_with_dup(nums: List[int]) -> List[List[int]]:",
        fn="subsets_with_dup",
        compare="unordered",
        tests=[
            (([1, 2, 2],), [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]),
            (([0],), [[], [0]]),
            (([],), [[]]),
            (([2, 1, 2],), [[], [1], [1, 2], [1, 2, 2], [2], [2, 2]]),
        ],
        hints=[
            "Same duplicate problem as Combination Sum II.",
            "Sort first so equal numbers are adjacent.",
            (
                "At each depth, skip nums[i] if i > start and nums[i] == nums[i-1]. Every node of the recursion "
                "tree is a valid subset."
            ),
        ],
        pattern="Subsets backtracking + skip duplicates at the same depth",
        explain="Every recursion-tree node (not just leaves) is a subset, so append the current path on entry.",
        cx="O(n * 2^n) time",
        brute_cx="O(n * 2^n) time - all index subsets, dedupe through a set of sorted tuples",
        brute=r"""
# BRUTE FORCE: O(n * 2^n) time - all index subsets, dedupe through a set of sorted tuples
def subsets_with_dup(nums):
    s = sorted(nums)
    seen = set()
    for r in range(len(s) + 1):
        for comb in itertools.combinations(s, r):
            seen.add(comb)
    return [list(c) for c in seen]
""",
        solution=r"""
# OPTIMISED: O(n * 2^n) time
# Idea: Subsets backtracking + skip duplicates at the same depth
def subsets_with_dup(nums):
    nums = sorted(nums)
    res, path = [], []

    def dfs(start):
        res.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            dfs(i + 1)
            path.pop()

    dfs(0)
    return res
""",
    ),
    # ---- Letter Combinations of a Phone Number (LeetCode 17) ----
    dict(
        title="Letter Combinations of a Phone Number",
        diff="M",
        lc=17,
        slug="letter-combinations-of-a-phone-number",
        prompt=(
            "Digits 2-9 map to letters as on a phone keypad (2=abc, 3=def, 4=ghi, 5=jkl, 6=mno, 7=pqrs, 8=tuv, "
            "9=wxyz). Return all letter combinations the digit string could represent (any order; [] for an empty "
            "string)."
        ),
        sig="def letter_combinations(digits: str) -> List[str]:",
        fn="letter_combinations",
        compare="unordered",
        tests=[
            (("23",), ["ad", "ae", "af", "bd", "be", "bf", "cd", "ce", "cf"]),
            (("",), []),
            (("2",), ["a", "b", "c"]),
            (("79",), ["pw", "px", "py", "pz", "qw", "qx", "qy", "qz", "rw", "rx", "ry", "rz", "sw", "sx", "sy", "sz"]),
        ],
        hints=[
            "Each digit is an independent choice among its letters.",
            "Think of a tree: depth = digit position, branching = letters for that digit.",
            (
                "dfs(i, path): when i == len(digits) record the string; else loop over the letters of digits[i]. "
                "(Or itertools.product.)"
            ),
        ],
        pattern="Backtracking over a product of choices (one level per position)",
        explain=(
            "Output size is the product of the branching factors, so no algorithm can beat O(4^n * n); the work is "
            "in\n        generating cleanly. An iterative alternative extends a list of partial strings digit by "
            "digit."
        ),
        cx="O(4^n * n) time",
        brute_cx="O(3^n..4^n) - iterative list expansion (same output size)",
        brute=r"""
# BRUTE FORCE: O(3^n..4^n) - iterative list expansion (same output size)
def letter_combinations(digits):
    if not digits:
        return []
    m = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }
    out = [""]
    for d in digits:
        out = [p + ch for p in out for ch in m[d]]
    return out
""",
        solution=r"""
# OPTIMISED: O(4^n * n) time
# Idea: Backtracking over a product of choices (one level per position)
def letter_combinations(digits):
    if not digits:
        return []
    m = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }
    res = []

    def dfs(i, path):
        if i == len(digits):
            res.append("".join(path))
            return
        for ch in m[digits[i]]:
            path.append(ch)
            dfs(i + 1, path)
            path.pop()

    dfs(0, [])
    return res
""",
    ),
    # ---- Word Search (LeetCode 79) ----
    dict(
        title="Word Search",
        diff="M",
        lc=79,
        slug="word-search",
        prompt=(
            "Return True if `word` can be traced in the grid through horizontally/vertically adjacent cells, using "
            "each cell at most once per path."
        ),
        sig="def exist(board: List[List[str]], word: str) -> bool:",
        fn="exist",
        tests=[
            (([["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCCED"), True),
            (([["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "SEE"), True),
            (([["A", "B", "C", "E"], ["S", "F", "C", "S"], ["A", "D", "E", "E"]], "ABCB"), False),
            (([["a"]], "a"), True),
            (([["a", "b"]], "ba"), True),
            (([["a", "a"]], "aaa"), False),
        ],
        hints=[
            "Start a search from every cell that matches word[0].",
            "DFS: match the next letter among the 4 neighbours, never reusing a cell on the current path.",
            (
                "Mark the cell as visited in place (e.g. '#'), recurse, then restore it - avoids copying a visited "
                "set at each step."
            ),
        ],
        pattern="Grid DFS backtracking with in-place visited marking",
        explain=(
            "The visited mark must be undone on return, because a cell used on one path may be needed on another. "
            "In-place\n        marking is O(1) per step; copying a visited set makes each step O(path length)."
        ),
        cx="O(R*C*4^L) time worst case, O(L) space",
        brute_cx="same recursion but copies the visited set each step (extra O(L) per step)",
        brute=r"""
# BRUTE FORCE: same recursion but copies the visited set each step (extra O(L) per step)
def exist(board, word):
    R, C = len(board), len(board[0])

    def go(r, c, i, path):
        if board[r][c] != word[i]:
            return False
        if i == len(word) - 1:
            return True
        path = path | {(r, c)}
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in path and go(nr, nc, i + 1, path):
                return True
        return False

    return any(go(r, c, 0, frozenset()) for r in range(R) for c in range(C))
""",
        solution=r"""
# OPTIMISED: O(R*C*4^L) time worst case, O(L) space
# Idea: Grid DFS backtracking with in-place visited marking
def exist(board, word):
    R, C = len(board), len(board[0])

    def dfs(r, c, i):
        if i == len(word):
            return True
        if not (0 <= r < R and 0 <= c < C) or board[r][c] != word[i]:
            return False
        saved, board[r][c] = board[r][c], "#"  # mark visited
        found = any(dfs(r + dr, c + dc, i + 1) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))
        board[r][c] = saved  # un-choose
        return found

    return any(dfs(r, c, 0) for r in range(R) for c in range(C))
""",
    ),
    # ---- Palindrome Partitioning (LeetCode 131) ----
    dict(
        title="Palindrome Partitioning",
        diff="M",
        lc=131,
        slug="palindrome-partitioning",
        prompt="Partition s so that every part is a palindrome. Return all possible partitions (any order).",
        sig="def partition(s: str) -> List[List[str]]:",
        fn="partition",
        compare="unordered",
        tests=[
            (("aab",), [["a", "a", "b"], ["aa", "b"]]),
            (("a",), [["a"]]),
            (("aba",), [["a", "b", "a"], ["aba"]]),
            (("abc",), [["a", "b", "c"]]),
        ],
        hints=[
            "At each position decide where the next piece ends.",
            "Only extend with prefixes that are palindromes - that prunes the search.",
            "dfs(start): for end in start+1..n: piece = s[start:end]; if palindrome: choose, dfs(end), un-choose.",
        ],
        pattern="Backtracking over cut positions with a validity check (prune early)",
        explain=(
            "Bad prefixes are never extended, so we never explore partitions that already contain a "
            "non-palindrome.\n        A precomputed DP table of is_pal[i][j] makes the check O(1)."
        ),
        cx="O(n * 2^n) time",
        brute_cx="O(n * 2^n) time - every cut mask, filter partitions where all parts are palindromes",
        brute=r"""
# BRUTE FORCE: O(n * 2^n) time - every cut mask, filter partitions where all parts are palindromes
def partition(s):
    n, res = len(s), []
    for mask in range(1 << max(n - 1, 0)):
        parts, last = [], 0
        for i in range(n - 1):
            if mask >> i & 1:
                parts.append(s[last : i + 1])
                last = i + 1
        parts.append(s[last:])
        if all(p == p[::-1] for p in parts):
            res.append(parts)
    return res
""",
        solution=r"""
# OPTIMISED: O(n * 2^n) time
# Idea: Backtracking over cut positions with a validity check (prune early)
def partition(s):
    res, path = [], []

    def dfs(start):
        if start == len(s):
            res.append(path[:])
            return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if piece == piece[::-1]:
                path.append(piece)
                dfs(end)
                path.pop()

    dfs(0)
    return res
""",
    ),
    # ---- Restore IP Addresses (LeetCode 93) ----
    dict(
        title="Restore IP Addresses",
        diff="M",
        lc=93,
        slug="restore-ip-addresses",
        prompt=(
            "Insert dots into a digit string to form every valid IPv4 address (4 parts, each 0-255, no leading "
            "zeros except '0' itself). Return all (any order)."
        ),
        sig="def restore_ip_addresses(s: str) -> List[str]:",
        fn="restore_ip_addresses",
        compare="unordered",
        tests=[
            (("25525511135",), ["255.255.11.135", "255.255.111.35"]),
            (("0000",), ["0.0.0.0"]),
            (("101023",), ["1.0.10.23", "1.0.102.3", "10.1.0.23", "10.10.2.3", "101.0.2.3"]),
            (("1111",), ["1.1.1.1"]),
            (("123",), []),
        ],
        hints=[
            "Exactly 4 parts, each 1-3 digits. How many ways to place 3 dots?",
            "Backtrack: choose a part length 1..3, validate it, recurse for the remaining parts.",
            (
                "Validate: int(part) <= 255 and (len(part) == 1 or part[0] != '0'). Prune when the remaining digits "
                "cannot fit (needs between parts_left and 3*parts_left)."
            ),
        ],
        pattern="Backtracking with validity constraints and length pruning",
        explain=(
            "Only 3 dots among at most 11 gaps, so the search space is tiny; the exercise is correct validation and "
            "clean\n        recursion with pruning."
        ),
        cx="O(1) (bounded by 3^4 splits)",
        brute_cx="O(n^3) - three nested loops for the dot positions",
        brute=r"""
# BRUTE FORCE: O(n^3) - three nested loops for the dot positions
def restore_ip_addresses(s):
    def ok(p):
        return p != "" and (len(p) == 1 or p[0] != "0") and int(p) <= 255

    n, res = len(s), []
    for i in range(1, 4):
        for j in range(i + 1, i + 4):
            for k in range(j + 1, j + 4):
                parts = [s[:i], s[i:j], s[j:k], s[k:]]
                if k < n and all(ok(p) for p in parts):
                    res.append(".".join(parts))
    return res
""",
        solution=r"""
# OPTIMISED: O(1) (bounded by 3^4 splits)
# Idea: Backtracking with validity constraints and length pruning
def restore_ip_addresses(s):
    res, parts = [], []

    def dfs(start):
        left = 4 - len(parts)
        remaining = len(s) - start
        if remaining < left or remaining > 3 * left:
            return
        if left == 0:
            res.append(".".join(parts))
            return
        for ln in range(1, 4):
            p = s[start : start + ln]
            if len(p) == ln and int(p) <= 255 and (ln == 1 or p[0] != "0"):
                parts.append(p)
                dfs(start + ln)
                parts.pop()

    dfs(0)
    return res
""",
    ),
]
