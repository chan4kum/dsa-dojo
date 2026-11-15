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
    while True:                                   # the problem promises EXACTLY one valid pair
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
    ("binary_search", "Find First and Last Position of Element in Sorted Array"): lambda: (sorted_ints(8, 0, 5), R(0, 6)),
    ("binary_search", "Sqrt(x)"): lambda: (R(0, 5000),),
    ("binary_search", "Find Minimum in Rotated Sorted Array"): lambda: _rot(),
    ("stack_monotonic", "Asteroid Collision"): lambda: ([x for x in ints(8, -6, 6) if x],),
    ("stack_monotonic", "Remove K Digits"): lambda: (lambda s: (s, R(0, len(s))))(st("0123456789", 1, 7)),
    ("stack_monotonic", "Next Greater Element II"): lambda: (ints(7, 0, 5),),
    ("stack_monotonic", "Car Fleet"): lambda: (lambda pos: (20, pos, [R(1, 5) for _ in pos]))(random.sample(range(0, 19), R(0, 6))),
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
    ("bits_math", "Reverse Integer"): lambda: (R(-10 ** 10, 10 ** 10),),
    ("bits_math", "Hamming Distance"): lambda: (R(0, 255), R(0, 255)),
    ("bits_math", "Number of 1 Bits"): lambda: (R(0, 2 ** 31),),
    ("bits_math", "Reverse Bits"): lambda: (R(0, 2 ** 32 - 1),),
    ("strings", "String to Integer (atoi)"): lambda: (st(" +-0123x", 0, 8),),
    ("strings", "Add Strings"): lambda: (st("0123456789", 1, 6).lstrip("0") or "0", st("0123456789", 1, 6).lstrip("0") or "0"),
    ("strings", "Multiply Strings"): lambda: (st("0123456789", 1, 5).lstrip("0") or "0", st("0123456789", 1, 5).lstrip("0") or "0"),
    ("strings", "Roman to Integer"): lambda: (R_roman(),),
    ("matrix", "Spiral Matrix"): lambda: ([[R(0, 9) for _ in range(c)] for c in [R(1, 4)] for _ in range(R(1, 4))],),
    ("matrix", "Rotate Image"): lambda: ([[R(0, 9) for _ in range(n)] for n in [R(1, 5)] for _ in range(n)],),
    ("matrix", "Set Matrix Zeroes"): lambda: ([[R(0, 3) for _ in range(c)] for c in [R(1, 4)] for _ in range(R(1, 4))],),
    ("matrix", "Game of Life"): lambda: ([[R(0, 1) for _ in range(c)] for c in [R(1, 5)] for _ in range(R(1, 5))],),
    ("binary_search", "Search a 2D Matrix"): lambda: _grid_sorted(),
}


def R_roman():
    vals = [(1000, "M"), (900, "CM"), (500, "D"), (400, "CD"), (100, "C"), (90, "XC"), (50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]
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
    return ([vals[i * c:(i + 1) * c] for i in range(r)], R(0, 40))


def main():
    bad = ran = 0
    by_title = {(t, p["title"]): p for t in TOPICS for p in load(t)}
    for key, gen in G.items():
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
            ro, rb = opt(*a), brute(*b)
            if "inplace" in p:
                ro, rb = a[p["inplace"]], b[p["inplace"]]
            if not equal(ro, rb, p.get("compare", "exact")):
                print(f"MISMATCH {key[1]}: input {args} optimised={ro} brute={rb}")
                bad += 1
                break
    print(f"fuzz_diff: {ran - bad}/{ran} brute-vs-optimised checks agree (250 random cases each)")
    sys.exit(1 if bad else 0)


main()
