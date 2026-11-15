"""Differential fuzzing: for the extra problems, run the BRUTE solution and the OPTIMISED solution on random small
inputs and require identical answers. If a brute and an optimised solution ever disagree, one of them is wrong.

    python tools/fuzz_diff.py
"""

import copy
import random
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fuzz_gens_more import GX  # noqa: E402

from core import compile_solution, equal  # noqa: E402
from dsa import TOPICS, load  # noqa: E402

random.seed(11)
R = random.randint


def ints(n, lo, hi, k=0):
    return [R(lo, hi) for _ in range(R(k, n))]


def st(alpha, lo, hi):
    return "".join(random.choice(alpha) for _ in range(R(lo, hi)))


def sorted_ints(n, lo, hi, k=0):
    return sorted(ints(n, lo, hi, k))


def two_sum_ii():
    while True:  # the problem promises EXACTLY one valid pair
        a = sorted_ints(8, -9, 9, 2)
        i, j = sorted(random.sample(range(len(a)), 2))
        t = a[i] + a[j]
        if sum(1 for x in range(len(a)) for y in range(x + 1, len(a)) if a[x] + a[y] == t) == 1:
            return (a, t)


def _merge():
    a, b = sorted(ints(5, 0, 9)), sorted(ints(5, 0, 9))
    return (a + [0] * len(b), len(a), b, len(b))


def intervals(n=6, hi=12, min_len=1):
    out = []
    for _ in range(R(0, n)):
        s = R(0, hi)
        out.append([s, s + R(min_len, 5)])
    return out


def disjoint_sorted():
    pts = sorted(random.sample(range(40), R(0, 5) * 2))
    return [[pts[i], pts[i + 1]] for i in range(0, len(pts), 2)]


G = {
    ("two_pointers", "Two Sum II - Input Array Is Sorted"): two_sum_ii,
    ("two_pointers", "Squares of a Sorted Array"): lambda: (sorted_ints(7, -9, 9, 1),),
    ("two_pointers", "Move Zeroes"): lambda: (ints(8, 0, 3),),
    ("two_pointers", "Sort Colors"): lambda: (ints(10, 0, 2),),
    ("two_pointers", "Merge Sorted Array"): _merge,
    ("two_pointers", "Valid Palindrome II"): lambda: (st("abc", 0, 9),),
    ("sliding_window", "Best Time to Buy and Sell Stock"): lambda: (ints(8, 0, 9),),
    ("sliding_window", "Longest Repeating Character Replacement"): lambda: (st("AB", 0, 9), R(0, 3)),
    ("sliding_window", "Permutation in String"): lambda: (st("abc", 1, 3), st("abc", 0, 9)),
    ("sliding_window", "Find All Anagrams in a String"): lambda: (st("abc", 0, 9), st("abc", 1, 3)),
    ("sliding_window", "Max Consecutive Ones III"): lambda: ([R(0, 1) for _ in range(R(0, 10))], R(0, 3)),
    ("array_tricks", "Maximum Product Subarray"): lambda: (ints(7, -3, 3, 1),),
    ("array_tricks", "Rotate Array"): lambda: (ints(7, 0, 9, 1), R(0, 12)),
    ("array_tricks", "Next Permutation"): lambda: (ints(6, 0, 3, 1),),
    ("binary_search", "Search Insert Position"): lambda: (sorted(random.sample(range(20), R(0, 8))), R(-1, 21)),
    ("binary_search", "Find First and Last Position of Element in Sorted Array"): lambda: (
        sorted_ints(8, 0, 5),
        R(0, 6),
    ),
    ("binary_search", "Sqrt(x)"): lambda: (R(0, 5000),),
    ("binary_search", "Find Minimum in Rotated Sorted Array"): lambda: _rot(),
    ("stack_monotonic", "Asteroid Collision"): lambda: ([x for x in ints(8, -6, 6) if x],),
    ("stack_monotonic", "Remove K Digits"): lambda: (lambda s: (s, R(0, len(s))))(st("0123456789", 1, 7)),
    ("stack_monotonic", "Next Greater Element II"): lambda: (ints(7, 0, 5),),
    ("stack_monotonic", "Car Fleet"): lambda: (lambda pos: (20, pos, [R(1, 5) for _ in pos]))(
        random.sample(range(0, 19), R(0, 6))
    ),
    ("greedy", "Best Time to Buy and Sell Stock II"): lambda: (ints(8, 0, 9),),
    ("greedy", "Jump Game II"): lambda: ([R(1, 4) for _ in range(R(1, 7))],),
    ("greedy", "Assign Cookies"): lambda: (ints(6, 1, 5), ints(6, 1, 5)),
    ("greedy", "Hand of Straights"): lambda: (ints(9, 1, 5), R(1, 3)),
    ("greedy", "Valid Parenthesis String"): lambda: (st("()*", 0, 9),),
    ("greedy", "Candy"): lambda: (ints(7, 0, 4),),
    ("heap", "Last Stone Weight"): lambda: (ints(7, 1, 12),),
    ("intervals", "Meeting Rooms"): lambda: (intervals(),),
    ("intervals", "Meeting Rooms II"): lambda: (intervals(),),
    ("intervals", "Minimum Number of Arrows to Burst Balloons"): lambda: (intervals(min_len=0),),
    ("intervals", "Interval List Intersections"): lambda: (disjoint_sorted(), disjoint_sorted()),
    ("dynamic_programming", "Min Cost Climbing Stairs"): lambda: (ints(8, 0, 9, 2),),
    ("dynamic_programming", "House Robber II"): lambda: (ints(8, 0, 9, 1),),
    ("dynamic_programming", "Unique Paths"): lambda: (R(1, 6), R(1, 6)),
    ("dynamic_programming", "Palindromic Substrings"): lambda: (st("ab", 0, 9),),
    ("dynamic_programming", "Decode Ways"): lambda: (st("0123", 1, 8),),
    ("dynamic_programming", "Perfect Squares"): lambda: (R(1, 18),),
    ("dynamic_programming", "Combination Sum IV"): lambda: (sorted(random.sample(range(1, 6), R(1, 3))), R(0, 9)),
    ("dynamic_programming", "Target Sum"): lambda: (ints(6, 0, 5, 1), R(-8, 8)),
    ("dynamic_programming", "Best Time to Buy and Sell Stock with Cooldown"): lambda: (ints(7, 0, 9),),
    ("dynamic_programming", "Longest Palindromic Subsequence"): lambda: (st("abc", 1, 9),),
    ("dynamic_programming", "Regular Expression Matching"): lambda: (st("ab", 0, 5), st("ab.*", 0, 5)),
    ("dynamic_programming", "Coin Change II"): lambda: (R(0, 9), sorted(random.sample(range(1, 6), R(1, 3)))),
    ("bits_math", "Count Primes"): lambda: (R(0, 300),),
    ("bits_math", "Happy Number"): lambda: (R(1, 400),),
    ("bits_math", "Plus One"): lambda: (([R(1, 9)] + [R(0, 9) for _ in range(R(0, 4))]) if R(0, 9) else [0],),
    ("bits_math", "Reverse Integer"): lambda: (R(-(10**10), 10**10),),
    ("bits_math", "Hamming Distance"): lambda: (R(0, 255), R(0, 255)),
    ("bits_math", "Number of 1 Bits"): lambda: (R(0, 2**31),),
    ("bits_math", "Reverse Bits"): lambda: (R(0, 2**32 - 1),),
    ("strings", "String to Integer (atoi)"): lambda: (st(" +-0123x", 0, 8),),
    ("strings", "Add Strings"): lambda: (
        st("0123456789", 1, 6).lstrip("0") or "0",
        st("0123456789", 1, 6).lstrip("0") or "0",
    ),
    ("strings", "Multiply Strings"): lambda: (
        st("0123456789", 1, 5).lstrip("0") or "0",
        st("0123456789", 1, 5).lstrip("0") or "0",
    ),
    ("strings", "Roman to Integer"): lambda: (R_roman(),),
    ("matrix", "Spiral Matrix"): lambda: ([[R(0, 9) for _ in range(c)] for c in [R(1, 4)] for _ in range(R(1, 4))],),
    ("matrix", "Rotate Image"): lambda: ([[R(0, 9) for _ in range(n)] for n in [R(1, 5)] for _ in range(n)],),
    ("matrix", "Set Matrix Zeroes"): lambda: (
        [[R(0, 3) for _ in range(c)] for c in [R(1, 4)] for _ in range(R(1, 4))],
    ),
    ("matrix", "Game of Life"): lambda: ([[R(0, 1) for _ in range(c)] for c in [R(1, 5)] for _ in range(R(1, 5))],),
    ("binary_search", "Search a 2D Matrix"): lambda: _grid_sorted(),
}


# ---------------------------------------------------------------------------------------------------------------
# Second batch. Each entry is  (topic, title): generator   or   (topic, title): (generator, normalise)
# `normalise(args, result)` turns a result into something comparable when several answers are equally correct.
# ---------------------------------------------------------------------------------------------------------------
def rand_tree_list(max_nodes=9):
    """A random binary tree as a LeetCode-style level-order list (None = missing child)."""
    n = R(0, max_nodes)
    if n == 0:
        return []
    nodes = [[R(-5, 9), None, None]]
    slots = [(0, 1), (0, 2)]
    for _ in range(n - 1):
        parent, side = slots.pop(random.randrange(len(slots)))
        nodes.append([R(-5, 9), None, None])
        nodes[parent][side] = len(nodes) - 1
        slots += [(len(nodes) - 1, 1), (len(nodes) - 1, 2)]
    out, q = [], [0]
    while q:
        i = q.pop(0)
        if i is None:
            out.append(None)
            continue
        out.append(nodes[i][0])
        q += [nodes[i][1], nodes[i][2]]
    while out and out[-1] is None:
        out.pop()
    return out


def digit_tree_list():
    return [None if v is None else abs(v) % 10 for v in rand_tree_list()]


def grid01(max_r=4, max_c=4):
    c = R(1, max_c)
    return [[R(0, 1) for _ in range(c)] for _ in range(R(1, max_r))]


def pairs_with_single():
    vals = sorted(random.sample(range(30), R(1, 6)))
    single = random.choice(vals)
    return ([v for v in vals for _ in range(1 if v == single else 2)],)


def closest_k():
    a = sorted_ints(8, 0, 9, 1)
    return (a, R(1, len(a)), R(-2, 12))


def calc_expr():
    s = str(R(0, 9))
    for _ in range(R(0, 5)):
        op = random.choice("+-*/")
        s += random.choice(["", " "]) + op + str(R(1, 9) if op == "/" else R(0, 9))
    return (s,)


def people():
    hs = [R(1, 4) for _ in range(R(0, 6))]
    order = hs[:]
    random.shuffle(order)
    return ([[h, sum(1 for q in order[:i] if q >= h)] for i, h in enumerate(order)],)


def queue_norm(args, got):
    ok = all(sum(1 for q in got[:i] if q[0] >= h) == k for i, (h, k) in enumerate(got))
    return (sorted(map(tuple, got)), ok)


def sorted_matrix():
    n = R(1, 4)
    m = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            m[i][j] = max(m[i - 1][j] if i else 0, m[i][j - 1] if j else 0) + R(0, 3)
    return (m, R(1, n * n))


def trust_graph():
    n = R(1, 5)
    return (n, [[a, b] for a in range(1, n + 1) for b in range(1, n + 1) if a != b and R(0, 2) == 0])


def digraph():
    n = R(1, 6)
    return ([random.sample(range(n), R(0, min(n, 3))) for _ in range(n)],)


def dist_norm(target):
    return lambda args, got: abs(got - args[1])


G2 = {
    ("hashing", "First Unique Character in a String"): lambda: (st("abc", 0, 9),),
    ("hashing", "Ransom Note"): lambda: (st("abc", 0, 6), st("abc", 0, 9)),
    ("hashing", "Contains Duplicate II"): lambda: (ints(8, 0, 4), R(0, 4)),
    ("hashing", "4Sum II"): lambda: (lambda n: tuple([R(-2, 2) for _ in range(n)] for _ in range(4)))(R(1, 4)),
    ("hashing", "Word Pattern"): lambda: (st("ab", 1, 4), " ".join(random.choice(["x", "y"]) for _ in range(R(1, 4)))),
    ("prefix_sums", "Contiguous Array"): lambda: ([R(0, 1) for _ in range(R(0, 10))],),
    ("prefix_sums", "Subarray Sums Divisible by K"): lambda: (ints(8, -5, 5, 1), R(1, 5)),
    ("sliding_window", "Subarray Product Less Than K"): lambda: ([R(1, 5) for _ in range(R(0, 7))], R(0, 40)),
    ("sliding_window", "Fruit Into Baskets"): lambda: (ints(9, 0, 3),),
    ("sliding_window", "Longest Subarray of 1's After Deleting One Element"): lambda: (
        [R(0, 1) for _ in range(R(1, 9))],
    ),
    ("two_pointers", "Reverse String"): lambda: (list(st("abc", 0, 8)),),
    ("two_pointers", "3Sum Closest"): (lambda: (ints(7, -9, 9, 3), R(-9, 9)), dist_norm(None)),
    ("two_pointers", "4Sum"): lambda: (ints(7, -3, 3), R(-3, 3)),
    ("binary_search", "Valid Perfect Square"): lambda: (R(1, 3000),),
    ("binary_search", "Capacity To Ship Packages Within D Days"): lambda: (ints(8, 1, 9, 1), R(1, 5)),
    ("binary_search", "Single Element in a Sorted Array"): pairs_with_single,
    ("binary_search", "Find K Closest Elements"): closest_k,
    ("binary_search", "Find Smallest Letter Greater Than Target"): lambda: (
        sorted(st("abcdefg", 1, 6)),
        random.choice("abcdefg"),
    ),
    ("stack_monotonic", "Next Greater Element I"): lambda: (lambda b: (random.sample(b, R(0, len(b))), b))(
        random.sample(range(10), R(1, 7))
    ),
    ("stack_monotonic", "Remove All Adjacent Duplicates In String"): lambda: (st("ab", 0, 9),),
    ("stack_monotonic", "Validate Stack Sequences"): lambda: (lambda a: (a, random.sample(a, len(a))))(
        list(range(R(0, 6)))
    ),
    ("stack_monotonic", "Simplify Path"): lambda: (
        "/" + "/".join(random.choice(["a", "b", "..", ".", "", "c"]) for _ in range(R(0, 7))),
    ),
    ("stack_monotonic", "Basic Calculator II"): calc_expr,
    ("stack_monotonic", "132 Pattern"): lambda: (ints(7, -4, 4),),
    ("stack_monotonic", "Remove Duplicate Letters"): lambda: (st("abcd", 0, 8),),
    ("intervals", "Summary Ranges"): lambda: (sorted(random.sample(range(-5, 15), R(0, 8))),),
    ("intervals", "Remove Covered Intervals"): lambda: (
        [list(x) for x in {tuple(i) for i in intervals(6, 10)}],
    ),  # LeetCode guarantees distinct intervals
    ("greedy", "Lemonade Change"): lambda: ([random.choice([5, 5, 10, 20]) for _ in range(R(0, 9))],),
    ("greedy", "Queue Reconstruction by Height"): (people, queue_norm),
    ("greedy", "Wiggle Subsequence"): lambda: (ints(9, 0, 5),),
    ("heap", "Ugly Number II"): lambda: (R(1, 60),),
    ("heap", "Kth Smallest Element in a Sorted Matrix"): sorted_matrix,
    ("trees", "Path Sum"): lambda: (rand_tree_list(), R(-8, 20)),
    ("trees", "Minimum Depth of Binary Tree"): lambda: (rand_tree_list(),),
    ("trees", "Sum Root to Leaf Numbers"): lambda: (digit_tree_list(),),
    ("trees", "Find Largest Value in Each Tree Row"): lambda: (rand_tree_list(),),
    ("backtracking", "Combination Sum III"): lambda: (R(1, 4), R(1, 20)),
    ("backtracking", "Letter Case Permutation"): lambda: (st("a1B2", 0, 5),),
    ("backtracking", "Beautiful Arrangement"): lambda: (R(1, 7),),
    ("backtracking", "Partition to K Equal Sum Subsets"): lambda: (ints(7, 1, 5, 1), R(1, 3)),
    ("graphs", "Island Perimeter"): lambda: (grid01(),),
    ("graphs", "Flood Fill"): lambda: (lambda g: (g, R(0, len(g) - 1), R(0, len(g[0]) - 1), R(0, 2)))(
        [[R(0, 2) for _ in range(c)] for c in [R(1, 4)] for _ in range(R(1, 4))]
    ),
    ("graphs", "Shortest Path in Binary Matrix"): lambda: (
        lambda n: ([[R(0, 3) == 0 and 1 or 0 for _ in range(n)] for _ in range(n)],)
    )(R(1, 4)),
    ("graphs", "Find the Town Judge"): trust_graph,
    ("graphs", "Min Cost to Connect All Points"): lambda: ([[R(0, 9), R(0, 9)] for _ in range(R(1, 6))],),
    ("graphs", "Find Eventual Safe States"): digraph,
}


def _grid(rows, cols, lo, hi):
    return [[R(lo, hi) for _ in range(R(*cols))] for _ in range(R(*rows))]


def _rect(rows, cols):
    return [[R(0, 9) for _ in range(cols)] for _ in range(rows)]


def _square_grid(lo, hi):
    n = R(1, 4)
    return [[R(lo, hi) for _ in range(n)] for _ in range(n)]


def _words_chain():
    pool = ["a", "b", "ab", "ba", "abc", "bac", "abcd", "bcd", "cd", "c"]
    return (random.sample(pool, R(1, 8)),)


G3 = {
    ("dynamic_programming", "Minimum Falling Path Sum"): lambda: (_square_grid(-9, 9),),
    ("dynamic_programming", "Maximal Square"): lambda: (
        (lambda r, c: ([[random.choice("01") for _ in range(c)] for _ in range(r)],))(R(1, 5), R(1, 5)),
    )[0],
    ("dynamic_programming", "Delete and Earn"): lambda: (ints(7, 1, 6),),
    ("dynamic_programming", "Interleaving String"): lambda: (
        lambda a, b: (a, b, "".join(random.sample(a + b, len(a + b))) if R(0, 1) else a + b)
    )(st("ab", 0, 4), st("ab", 0, 4)),
    ("dynamic_programming", "Unique Paths II"): lambda: (
        lambda r, c: ([[1 if R(0, 4) == 0 else 0 for _ in range(c)] for _ in range(r)],)
    )(R(1, 5), R(1, 5)),
    ("dynamic_programming", "Minimum Cost For Tickets"): lambda: (
        sorted(random.sample(range(1, 40), R(1, 8))),
        [R(1, 5), R(3, 9), R(6, 15)],
    ),
    ("dynamic_programming", "Longest String Chain"): _words_chain,
    ("dynamic_programming", "Russian Doll Envelopes"): lambda: ([[R(1, 6), R(1, 6)] for _ in range(R(1, 8))],),
    ("dynamic_programming", "Distinct Subsequences"): lambda: (st("ab", 0, 8), st("ab", 0, 3)),
    ("dynamic_programming", "Number of Longest Increasing Subsequence"): lambda: (ints(9, 0, 5),),
    ("dynamic_programming", "Ones and Zeroes"): lambda: (
        [st("01", 1, 4) for _ in range(R(1, 6))],
        R(0, 4),
        R(0, 4),
    ),
    ("dynamic_programming", "Best Time to Buy and Sell Stock IV"): lambda: (R(0, 3), ints(8, 0, 9)),
    ("dynamic_programming", "Best Time to Buy and Sell Stock with Transaction Fee"): lambda: (ints(8, 0, 9), R(0, 3)),
}


def _two_singles():
    vals = random.sample(range(-20, 21), R(3, 8))
    a, b, pairs = vals[0], vals[1], vals[2:]
    nums = [a, b] + [v for v in pairs for _ in range(2)]
    random.shuffle(nums)
    return (nums,)


def _one_single():
    vals = random.sample(range(-20, 21), R(1, 6))
    nums = [vals[0]] + [v for v in vals[1:] for _ in range(3)]
    random.shuffle(nums)
    return (nums,)


def _range_and():
    left = R(0, 300)
    return (left, left + R(0, 300))


def _palindrome_num():
    return (R(-30, 3000) if R(0, 1) else int(str(R(1, 999)) + str(R(1, 999))[::-1]),)


G4 = {
    ("bits_math", "Single Number III"): _two_singles,
    ("bits_math", "Single Number II"): _one_single,
    ("bits_math", "Bitwise AND of Numbers Range"): _range_and,
    ("bits_math", "Factorial Trailing Zeroes"): lambda: (R(0, 200),),
    ("bits_math", "Palindrome Number"): _palindrome_num,
    ("bits_math", "Excel Sheet Column Title"): lambda: (R(1, 900),),
    ("bits_math", "Excel Sheet Column Number"): lambda: ("".join(random.choice("ABCXYZ") for _ in range(R(1, 3))),),
    ("bits_math", "Power of Three"): lambda: (3 ** R(0, 8) if R(0, 1) else R(-5, 100),),
    ("bits_math", "Ugly Number"): lambda: (R(-5, 300),),
    ("bits_math", "Integer to Roman"): lambda: (R(1, 3999),),
}


def _sorted_matrix():
    rows, cols = R(1, 4), R(1, 4)
    m = [[0] * cols for _ in range(rows)]
    for i in range(rows):
        for j in range(cols):
            m[i][j] = max(m[i - 1][j] if i else 0, m[i][j - 1] if j else 0) + R(0, 3)
    return (m, R(0, 12))


G5 = {
    ("strings", "Reverse Vowels of a String"): lambda: (st("aeibcAE", 0, 9),),
    ("strings", "Repeated Substring Pattern"): lambda: (st("ab", 1, 3) * R(1, 4) if R(0, 1) else st("abc", 1, 7),),
    ("strings", "Count Binary Substrings"): lambda: (st("01", 1, 12),),
    ("strings", "Count and Say"): lambda: (R(1, 12),),
    ("strings", "Zigzag Conversion"): lambda: (st("abcdef", 1, 12), R(1, 5)),
    ("strings", "Longest Palindrome"): lambda: (st("abAB", 0, 12),),
    ("strings", "Repeated DNA Sequences"): lambda: (st("AC", 0, 18),),
    ("matrix", "Search a 2D Matrix II"): _sorted_matrix,
    ("matrix", "Spiral Matrix II"): lambda: (R(1, 6),),
    ("matrix", "Transpose Matrix"): lambda: (_rect(R(1, 4), R(1, 4)),),
    ("matrix", "Matrix Diagonal Sum"): lambda: (_square_grid(0, 9),),
    ("divide_conquer", "Count of Smaller Numbers After Self"): lambda: (ints(9, -4, 4),),
}


def R_roman():
    vals = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]
    n, out = R(1, 3999), ""
    for v, s in vals:
        while n >= v:
            out += s
            n -= v
    return out


def _rot():
    a = sorted(random.sample(range(30), R(1, 8)))
    k = R(0, len(a) - 1)
    return (a[k:] + a[:k],)


def _grid_sorted():
    r, c = R(1, 4), R(1, 4)
    vals = sorted(random.sample(range(40), r * c))
    return ([vals[i * c : (i + 1) * c] for i in range(r)], R(0, 40))


def main():
    bad = ran = 0
    by_title = {(t, p["title"]): p for t in TOPICS for p in load(t)}
    for key, entry in {**G, **G2, **G3, **G4, **G5, **GX}.items():
        gen, norm = entry if isinstance(entry, tuple) else (entry, None)
        p = by_title.get(key)
        if p is None or not p.get("brute"):
            print("missing", key)
            bad += 1
            continue
        fn = p["fn"]
        opt = compile_solution(textwrap.dedent(p["solution"]))[fn]
        brute = compile_solution(textwrap.dedent(p["brute"]))[fn]
        ran += 1
        for _ in range(250):
            args = gen()
            a, b = copy.deepcopy(args), copy.deepcopy(args)
            if p.get("adapt_in"):
                a, b = p["adapt_in"](a), p["adapt_in"](b)
            ro, rb = opt(*a), brute(*b)
            if "inplace" in p:
                ro, rb = a[p["inplace"]], b[p["inplace"]]
            if p.get("adapt_out"):
                ro, rb = p["adapt_out"](ro), p["adapt_out"](rb)
            if norm:
                ro, rb = norm(args, ro), norm(args, rb)
            if not equal(ro, rb, p.get("compare", "exact")):
                print(f"MISMATCH {key[1]}: input {args} optimised={ro} brute={rb}")
                bad += 1
                break
    print(f"fuzz_diff: {ran - bad}/{ran} brute-vs-optimised checks agree (250 random cases each)")
    sys.exit(1 if bad else 0)


main()
