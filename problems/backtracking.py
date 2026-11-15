from core import *

PROBLEMS = [
    dict(
        title="Subsets", diff="M", lc=78, slug="subsets",
        prompt="Given distinct integers, return every possible subset (the power set), in any order.",
        sig="def subsets(nums: List[int]) -> List[List[int]]:",
        fn="subsets", compare="nested_unordered",
        tests=[(([1, 2, 3],), [[], [1], [2], [3], [1, 2], [1, 3], [2, 3], [1, 2, 3]]), (([0],), [[], [0]]), (([],), [[]]),
               (([4, 5],), [[], [4], [5], [4, 5]])],
        hints=["For each element there are exactly two choices. How many leaves does that decision tree have?",
               "Recurse on index i: first INCLUDE nums[i] (append to path), recurse, then undo (pop) and EXCLUDE it, recurse.",
               "Record a copy of the path when i == len(nums)."],
        pattern="Backtracking: include/exclude decision tree (choose -> explore -> un-choose)",
        explain="""
        Backtracking = DFS over a tree of partial decisions. The shared `path` list is mutated in place, so
        every 'choose' must be matched by an 'un-choose' when returning, and results must store COPIES.
        2^n subsets, so O(n * 2^n).""",
        solution=r'''
def subsets(nums):
    res, path = [], []
    def go(i):
        if i == len(nums):
            res.append(path[:])          # copy!
            return
        path.append(nums[i])             # choose
        go(i + 1)
        path.pop()                       # un-choose
        go(i + 1)                        # skip nums[i]
    go(0)
    return res
''',
    ),
    dict(
        title="Permutations", diff="M", lc=46, slug="permutations",
        prompt="Return all orderings of a list of distinct integers.",
        sig="def permute(nums: List[int]) -> List[List[int]]:",
        fn="permute", compare="unordered",
        tests=[(([1, 2, 3],), [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]), (([0, 1],), [[0, 1], [1, 0]]),
               (([1],), [[1]])],
        hints=["Build the permutation position by position. At each position, which values are allowed?",
               "Any value not yet used. Track usage with a boolean array (or a set).",
               "choose x (mark used, append) -> recurse -> un-choose; record when len(path) == n."],
        pattern="Backtracking with a 'used' set: n! leaves",
        explain="""
        Unlike subsets, every element must be placed, and ORDER matters, so at each depth we try every unused
        element. n! results, each of length n: O(n * n!).""",
        solution=r'''
def permute(nums):
    res, path = [], []
    used = [False] * len(nums)
    def go():
        if len(path) == len(nums):
            res.append(path[:])
            return
        for i, x in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(x)
            go()
            path.pop()
            used[i] = False
    go()
    return res
''',
    ),
    dict(
        title="Combination Sum", diff="M", lc=39, slug="combination-sum",
        prompt="Given distinct positive integers and a target, return all unique combinations that sum to the target. "
               "The same number may be used unlimited times.",
        sig="def combination_sum(candidates: List[int], target: int) -> List[List[int]]:",
        fn="combination_sum", compare="nested_unordered",
        tests=[(([2, 3, 6, 7], 7), [[2, 2, 3], [7]]), (([2, 3, 5], 8), [[2, 2, 2, 2], [2, 3, 3], [3, 5]]), (([2], 1), []),
               (([1], 2), [[1, 1]])],
        hints=["To avoid counting [2,3] and [3,2] twice, impose an order on choices.",
               "Recurse with a `start` index: from position `start` you may pick candidates[i] for i >= start.",
               "Picking candidates[i] again is allowed, so recurse with i (not i+1). Prune when the remaining sum goes negative."],
        pattern="Backtracking over combinations: a start index prevents permutations of the same set",
        explain="""
        Combinations are unordered, so only ever move forward in the candidate list. Reusing an element means
        the recursive call keeps the same start. Sorting lets you `break` as soon as a candidate exceeds the
        remainder.""",
        solution=r'''
def combination_sum(candidates, target):
    candidates = sorted(candidates)
    res, path = [], []
    def go(start, remain):
        if remain == 0:
            res.append(path[:])
            return
        for i in range(start, len(candidates)):
            if candidates[i] > remain:
                break                     # sorted: nothing later can fit
            path.append(candidates[i])
            go(i, remain - candidates[i])   # i, not i+1: reuse allowed
            path.pop()
    go(0, target)
    return res
''',
    ),
    dict(
        title="Generate Parentheses", diff="M", lc=22, slug="generate-parentheses",
        prompt="Return all strings of n pairs of parentheses that are well-formed.",
        sig="def generate_parenthesis(n: int) -> List[str]:",
        fn="generate_parenthesis", compare="unordered",
        tests=[((3,), ["((()))", "(()())", "(())()", "()(())", "()()()"]), ((1,), ["()"]), ((2,), ["(())", "()()"])],
        hints=["Generating all 2^(2n) strings and filtering works but wastes time. Can you prune while building?",
               "You may add '(' if you still have opens left; you may add ')' only if there are more opens than closes so far.",
               "Track counts `open` and `close`; the string is complete when its length is 2n."],
        pattern="Backtracking with constraint pruning (only build valid prefixes)",
        explain="""
        A prefix can be completed to a valid string iff close <= open <= n. By only taking moves that keep that
        true, every branch of the recursion ends in an answer - the count is the n-th Catalan number.""",
        solution=r'''
def generate_parenthesis(n):
    res = []
    def go(s, opened, closed):
        if len(s) == 2 * n:
            res.append(s)
            return
        if opened < n:
            go(s + "(", opened + 1, closed)
        if closed < opened:
            go(s + ")", opened, closed + 1)
    go("", 0, 0)
    return res
''',
    ),
    dict(
        title="N-Queens", diff="H", lc=51, slug="n-queens",
        prompt="Place n queens on an n x n board so none attack each other. Return every distinct board as a list of "
               "row strings using 'Q' and '.'.",
        sig="def solve_n_queens(n: int) -> List[List[str]]:",
        fn="solve_n_queens", compare="unordered",
        tests=[((4,), [[".Q..", "...Q", "Q...", "..Q."], ["..Q.", "Q...", "...Q", ".Q.."]]), ((1,), [["Q"]]),
               ((2,), []), ((3,), [])],
        hints=["One queen per row. So decide a column for each row in turn.",
               "A new queen conflicts if its column, or either diagonal, is taken. Which quantities identify a diagonal?",
               "On '/' diagonals row+col is constant; on '\\' diagonals row-col is constant. Keep three sets."],
        pattern="Backtracking with O(1) conflict checks via sets (columns, diagonals)",
        explain="""
        Row-by-row placement removes the row conflict by construction. Sets of used columns, r-c and r+c make
        each validity test O(1). The search prunes dead branches early, far fewer than n^n placements.""",
        solution=r'''
def solve_n_queens(n):
    cols, d1, d2 = set(), set(), set()
    placed, res = [], []
    def go(r):
        if r == n:
            res.append(["." * c + "Q" + "." * (n - c - 1) for c in placed])
            return
        for c in range(n):
            if c in cols or (r - c) in d1 or (r + c) in d2:
                continue
            cols.add(c); d1.add(r - c); d2.add(r + c); placed.append(c)
            go(r + 1)
            placed.pop(); cols.remove(c); d1.remove(r - c); d2.remove(r + c)
    go(0)
    return res
''',
    ),
]
