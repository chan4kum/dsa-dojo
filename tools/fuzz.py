"""Randomised cross-check of reference solutions against brute force (extra confidence beyond the fixed tests).

python tools/fuzz.py
"""

import itertools
import random
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import compile_solution  # noqa: E402
from dsa import load  # noqa: E402

random.seed(7)


def sol(topic, title):
    for p in load(topic):
        if p["title"] == title:
            return compile_solution(textwrap.dedent(p["solution"]))[p.get("fn")]
    raise KeyError(title)


def rl(n, lo, hi):
    return [random.randint(lo, hi) for _ in range(random.randint(0, n))]


checks = []


def check(name, fn):
    checks.append((name, fn))


def f_three_sum():
    f = sol("two_pointers", "3Sum")
    a = rl(9, -4, 4)
    exp = sorted({tuple(sorted(c)) for c in itertools.combinations(a, 3) if sum(c) == 0})
    got = sorted(tuple(sorted(t)) for t in f(a[:]))
    assert got == exp and len(got) == len(set(got)), (a, got, exp)


def f_trap():
    f = sol("two_pointers", "Trapping Rain Water")
    h = rl(10, 0, 6)
    exp = sum(max(0, min(max(h[: i + 1]), max(h[i:])) - h[i]) for i in range(len(h)))
    assert f(h) == exp, h


def f_container():
    f = sol("two_pointers", "Container With Most Water")
    h = [random.randint(0, 9) for _ in range(random.randint(2, 9))]
    exp = max((j - i) * min(h[i], h[j]) for i in range(len(h)) for j in range(i + 1, len(h)))
    assert f(h) == exp, h


def f_min_window():
    f = sol("sliding_window", "Minimum Window Substring")
    s = "".join(random.choice("abc") for _ in range(random.randint(0, 9)))
    t = "".join(random.choice("abc") for _ in range(random.randint(1, 3)))
    from collections import Counter

    best = None
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            c = Counter(s[i:j])
            if all(c[k] >= v for k, v in Counter(t).items()):
                if best is None or j - i < len(best):
                    best = s[i:j]
    got = f(s, t)
    assert len(got) == len(best or ""), (s, t, got, best)


def f_longest_unique():
    f = sol("sliding_window", "Longest Substring Without Repeating Characters")
    s = "".join(random.choice("abcd") for _ in range(random.randint(0, 10)))
    exp = max([j - i for i in range(len(s)) for j in range(i, len(s) + 1) if len(set(s[i:j])) == j - i] or [0])
    assert f(s) == exp, s


def f_subarray_k():
    f = sol("prefix_sums", "Subarray Sum Equals K")
    a, k = rl(9, -3, 3), random.randint(-3, 3)
    exp = sum(1 for i in range(len(a)) for j in range(i, len(a)) if sum(a[i : j + 1]) == k)
    assert f(a, k) == exp, (a, k)


def f_rect():
    f = sol("stack_monotonic", "Largest Rectangle in Histogram")
    h = rl(9, 0, 6)
    exp = max([min(h[i:j]) * (j - i) for i in range(len(h)) for j in range(i + 1, len(h) + 1)] or [0])
    assert f(h) == exp, h


def f_sliding_max():
    f = sol("stack_monotonic", "Sliding Window Maximum")
    a = [random.randint(-5, 5) for _ in range(random.randint(1, 10))]
    k = random.randint(1, len(a))
    assert f(a, k) == [max(a[i : i + k]) for i in range(len(a) - k + 1)], (a, k)


def f_rotated():
    f = sol("binary_search", "Search in Rotated Sorted Array")
    a = sorted(random.sample(range(-20, 20), random.randint(1, 10)))
    r = random.randint(0, len(a) - 1)
    a = a[r:] + a[:r]
    t = random.randint(-22, 22)
    assert f(a, t) == (a.index(t) if t in a else -1), (a, t)


def f_median():
    f = sol("binary_search", "Median of Two Sorted Arrays")
    a, b = sorted(rl(6, -9, 9)), sorted(rl(6, -9, 9))
    if not a and not b:
        return
    m = sorted(a + b)
    n = len(m)
    exp = m[n // 2] if n % 2 else (m[n // 2 - 1] + m[n // 2]) / 2
    assert abs(f(a, b) - exp) < 1e-9, (a, b)


def f_split():
    f = sol("binary_search", "Split Array Largest Sum")
    a = [random.randint(0, 9) for _ in range(random.randint(1, 8))]
    a[0] = max(a[0], 1)
    k = random.randint(1, len(a))
    best = min(
        max(sum(a[x:y]) for x, y in zip((0,) + c, c + (len(a),)))
        for c in itertools.combinations(range(1, len(a)), k - 1)
    )
    assert f(a, k) == best, (a, k)


def f_coin():
    f = sol("dynamic_programming", "Coin Change")
    coins = random.sample(range(1, 8), random.randint(1, 3))
    amt = random.randint(0, 25)
    INF = 99
    dp = [0] + [INF] * amt
    for a in range(1, amt + 1):
        dp[a] = min([dp[a - c] + 1 for c in coins if c <= a] or [INF])
    assert f(coins, amt) == (dp[amt] if dp[amt] < INF else -1), (coins, amt)


def f_lis():
    f = sol("dynamic_programming", "Longest Increasing Subsequence")
    a = rl(9, 0, 6)
    best = 0
    for r in range(len(a) + 1):
        for c in itertools.combinations(a, r):
            if all(x < y for x, y in zip(c, c[1:])):
                best = max(best, r)
    assert f(a) == best, a


def f_edit():
    f = sol("dynamic_programming", "Edit Distance")
    a = "".join(random.choice("ab") for _ in range(random.randint(0, 5)))
    b = "".join(random.choice("ab") for _ in range(random.randint(0, 5)))
    from functools import lru_cache

    @lru_cache(None)
    def d(i, j):
        if i == 0:
            return j
        if j == 0:
            return i
        return min(d(i - 1, j) + 1, d(i, j - 1) + 1, d(i - 1, j - 1) + (a[i - 1] != b[j - 1]))

    assert f(a, b) == d(len(a), len(b)), (a, b)


def f_burst():
    f = sol("dynamic_programming", "Burst Balloons")
    a = [random.randint(1, 6) for _ in range(random.randint(0, 6))]
    best = 0
    for order in itertools.permutations(range(len(a))):
        arr, tot = a[:], 0
        idx = list(range(len(a)))
        for o in order:
            p = idx.index(o)
            left = arr[p - 1] if p > 0 else 1
            r = arr[p + 1] if p + 1 < len(arr) else 1
            tot += left * arr[p] * r
            del arr[p]
            del idx[p]
        best = max(best, tot)
    assert f(a) == best, a


def f_reverse_pairs():
    f = sol("divide_conquer", "Reverse Pairs")
    a = rl(10, -9, 9)
    exp = sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > 2 * a[j])
    assert f(a) == exp, a


def f_first_missing():
    f = sol("array_tricks", "First Missing Positive")
    a = rl(8, -2, 9)
    exp = next(i for i in range(1, 100) if i not in a)
    assert f(a[:]) == exp, a


def f_gas():
    f = sol("greedy", "Gas Station")
    n = random.randint(1, 6)
    g = [random.randint(0, 5) for _ in range(n)]
    c = [random.randint(0, 5) for _ in range(n)]
    ok = [s for s in range(n) if all(sum(g[(s + k) % n] - c[(s + k) % n] for k in range(m + 1)) >= 0 for m in range(n))]
    got = f(g, c)
    assert (got == -1 and not ok) or got in ok, (g, c, got, ok)


def f_sum_two():
    f = sol("bits_math", "Sum of Two Integers")
    a, b = random.randint(-1000, 1000), random.randint(-1000, 1000)
    assert f(a, b) == a + b, (a, b)


def f_kmp():
    f = sol("strings", "Find the Index of the First Occurrence in a String")
    h = "".join(random.choice("ab") for _ in range(random.randint(0, 12)))
    n = "".join(random.choice("ab") for _ in range(random.randint(1, 4)))
    assert f(h, n) == h.find(n), (h, n)


def f_merge_intervals():
    f = sol("intervals", "Merge Intervals")
    iv = []
    for _ in range(random.randint(1, 6)):
        s = random.randint(0, 10)
        iv.append([s, s + random.randint(0, 4)])
    pts = set()
    for s, e in iv:
        pts.update(range(s * 2, e * 2 + 1))  # doubled so touching [1,2],[2,3] merges but [1,2],[3,4] doesn't
    got = f([x[:] for x in iv])
    assert all(a[1] < b[0] for a, b in zip(got, got[1:])), (iv, got)
    covered = set()
    for s, e in got:
        covered.update(range(s * 2, e * 2 + 1))
    assert covered == pts, (iv, got)


for name, fn in list(globals().items()):
    if name.startswith("f_"):
        check(name[2:], fn)

bad = 0
for name, fn in checks:
    for _ in range(300):
        try:
            fn()
        except AssertionError as e:
            print("MISMATCH", name, e)
            bad += 1
            break
print(f"fuzz: {len(checks) - bad}/{len(checks)} checks clean (300 random cases each)")
sys.exit(1 if bad else 0)
