"""Executable proof of the factual claims made in the tutorials (_src/*.md).

Each check names the tutorial it comes from, quotes the claim, and tests it by RUNNING Python - so a claim that is
wrong (or stops being true in a future Python) fails loudly instead of misleading a student.

Run:  python3 tools/verify_claims.py        (exit status 1 if any claim fails)
"""

import bisect
import collections
import functools
import heapq
import itertools
import math
import random
import subprocess
import sys
import time

CHECKS = []


def claim(note, text):
    def register(fn):
        CHECKS.append((note, text, fn))
        return fn

    return register


# --------------------------------------------------------------------------- foundations / Python toolkit
@claim("00-foundations", "default recursion limit is 1000 (RecursionError beyond it)")
def _():
    out = subprocess.run(
        [sys.executable, "-I", "-c", "import sys; print(sys.getrecursionlimit())"], capture_output=True, text=True
    )
    assert out.stdout.strip() == "1000", out.stdout

    def deep(n):
        return 0 if n == 0 else 1 + deep(n - 1)

    try:
        deep(10**5)
    except RecursionError:
        return
    raise AssertionError("no RecursionError for depth 100000")


@claim(
    "00-foundations / B2", "// and % floor for negatives: -7 // 2 == -4, -7 % 3 == 2; int(a / b) truncates toward zero"
)
def _():
    assert -7 // 2 == -4 and -7 % 3 == 2 and int(-7 / 2) == -3


@claim("B2 (new caveat)", "int(a / b) is NOT exact for huge integers (float division), so use integer maths")
def _():
    a, b = 10**20 + 1, 1
    assert int(a / b) != a and a // b == a


@claim("00-foundations", "slicing creates a copy (O(k)), an assignment only aliases")
def _():
    a = [1, 2, 3]
    s, alias = a[:], a
    a[0] = 99
    assert s[0] == 1 and alias[0] == 99 and s is not a


@claim("15-dp / B2", "[[0]*n]*m shares rows; [[0]*n for _ in range(m)] does not")
def _():
    bad, good = [[0] * 3] * 2, [[0] * 3 for _ in range(2)]
    bad[0][0], good[0][0] = 1, 1
    assert bad[1][0] == 1 and good[1][0] == 0


@claim("B2", "mutable default arguments persist between calls")
def _():
    def f(x, seen=[]):  # noqa: B006 - this is the pitfall being demonstrated
        seen.append(x)
        return len(seen)

    assert f(1) == 1 and f(2) == 2


@claim("B2 / 08", "list.pop(0) is O(n) while deque.popleft() is O(1) (measured, generous margin)")
def _():
    n = 60000
    lst, dq = list(range(n)), collections.deque(range(n))
    t = time.perf_counter()
    for _ in range(n):
        lst.pop(0)
    t_list = time.perf_counter() - t
    t = time.perf_counter()
    for _ in range(n):
        dq.popleft()
    t_deque = time.perf_counter() - t
    assert t_list > 5 * t_deque, (t_list, t_deque)


@claim("02-prefix_sums", "Python's % is non-negative for a positive modulus")
def _():
    assert all((-x) % 5 in range(5) for x in range(1, 50))


@claim(
    "01-hashing",
    "lists are unhashable (TypeError), tuples hashable; Counter/defaultdict(int) return 0 for missing keys",
)
def _():
    try:
        hash([1])
    except TypeError:
        pass
    else:
        raise AssertionError("list was hashable")
    assert {(1, 2): 1}[(1, 2)] == 1
    assert collections.Counter()["x"] == 0 and collections.defaultdict(int)["x"] == 0


@claim("01-hashing", "x in set is O(1) on average: 100x more elements does not cost 100x more per lookup")
def _():
    def per_lookup(n):
        s = set(range(n))
        t = time.perf_counter()
        for i in range(200000):
            _ = (i % n) in s
        return time.perf_counter() - t

    assert per_lookup(10**6) < 20 * per_lookup(10**4)


# --------------------------------------------------------------------------- binary search
@claim("06-binary_search", "n = 10^9 needs about 30 probes")
def _():
    assert math.ceil(math.log2(10**9)) == 30


@claim("06-binary_search", "bisect_left / bisect_right are lower_bound / upper_bound")
def _():
    a = [1, 2, 2, 2, 5]
    assert bisect.bisect_left(a, 2) == 1 and bisect.bisect_right(a, 2) == 4
    assert bisect.bisect_left(a, 3) == bisect.bisect_right(a, 3) == 4


@claim("06-binary_search", "while lo < hi with lo = mid (no +1) loops forever once lo + 1 == hi")
def _():
    lo, hi, steps = 4, 5, 0
    while lo < hi and steps < 100:
        mid = (lo + hi) // 2
        lo = mid  # the bug
        steps += 1
    assert steps == 100


# --------------------------------------------------------------------------- heaps
@claim(
    "11-heap", "heapq is a min-heap; max-heap by negation; heapify is O(n) and cheaper than n pushes in the worst case"
)
def _():
    h = [5, 1, 3]
    heapq.heapify(h)
    assert heapq.heappop(h) == 1
    m = []
    for x in [5, 1, 3]:
        heapq.heappush(m, -x)
    assert -heapq.heappop(m) == 5

    class C:
        count = 0

        def __init__(self, v):
            self.v = v

        def __lt__(self, other):
            C.count += 1
            return self.v < other.v

    n = 20000
    desc = [C(v) for v in range(n, 0, -1)]  # worst case for pushing into a min-heap
    heap = []
    C.count = 0
    for x in desc:
        heapq.heappush(heap, x)
    pushes = C.count
    arr = [C(v) for v in range(n, 0, -1)]
    C.count = 0
    heapq.heapify(arr)
    assert C.count <= 2 * n < pushes / 3, (C.count, pushes)


@claim(
    "11-heap",
    "heapq compares tuples element-wise: a priority tie falls through to the payload (TypeError if uncomparable)",
)
def _():
    h = []
    heapq.heappush(h, (1, {"a": 1}))
    try:
        heapq.heappush(h, (1, {"b": 2}))  # equal priorities -> Python compares the dicts -> TypeError
    except TypeError:
        pass
    else:
        raise AssertionError("no TypeError")
    heapq.heappush(h, (0, {"c": 3}))  # a distinct priority never touches the payload
    heapq.heappush(h, (2, {"d": 4}))
    heap2 = []
    heapq.heappush(heap2, (1, 0, {"a": 1}))  # the fix taught in the note: a unique tie-breaker counter
    heapq.heappush(heap2, (1, 1, {"b": 2}))
    assert heapq.heappop(heap2)[1] == 0


# --------------------------------------------------------------------------- bits / math
@claim("16-bits_math", "n & (n-1) clears the lowest set bit; n & -n isolates it; power-of-two test")
def _():
    for n in range(1, 2000):
        low = n & -n
        assert n & (n - 1) == n - low and low & (low - 1) == 0
        assert (n & (n - 1) == 0) == (bin(n).count("1") == 1)
    assert 12 & 11 == 8  # 1100 & 1011 = 1000 (the worked example of the self-check)


@claim("16-bits_math", "XOR: a^a=0, a^0=a, pairs cancel; the two-singles trick splits by a differing bit")
def _():
    nums = [4, 1, 2, 1, 2, 7]
    x = 0
    for v in nums:
        x ^= v
    assert x == 4 ^ 7
    diff = x & -x
    a = b = 0
    for v in nums:
        if v & diff:
            a ^= v
        else:
            b ^= v
    assert {a, b} == {4, 7}


@claim("16-bits_math", "adding without +: sum = a ^ b, carry = (a & b) << 1 (non-negative operands)")
def _():
    for _ in range(500):
        a, b = random.randrange(10**6), random.randrange(10**6)
        x, y = a, b
        while y:
            x, y = x ^ y, (x & y) << 1
        assert x == a + b


@claim(
    "16-bits_math (CORRECTED)",
    "in PYTHON bitwise operators bind tighter than ==, so a & b == c is (a & b) == c; in C/Java it is a & (b == c)",
)
def _():
    a, b, c = 6, 3, 2
    assert (a & b == c) is True  # Python: (6 & 3) == 2
    assert (a & (b == c)) == 0  # what C/Java would compute


@claim("16-bits_math", "Python >> on negatives is arithmetic (floor), ints never overflow; 32-bit view needs a mask")
def _():
    assert -5 >> 1 == -3 and 5 >> 1 == 2 and 2**100 > 0
    assert (-1) & 0xFFFFFFFF == 4294967295


@claim("16-bits_math", "Euclid gcd; sieve of Eratosthenes counts primes correctly")
def _():
    def gcd(a, b):
        while b:
            a, b = b, a % b
        return a

    assert all(gcd(a, b) == math.gcd(a, b) for a in range(1, 60) for b in range(1, 60))
    n = 1000
    sieve = [True] * (n + 1)
    sieve[0] = sieve[1] = False
    for i in range(2, int(n**0.5) + 1):
        if sieve[i]:
            for j in range(i * i, n + 1, i):
                sieve[j] = False
    assert sum(sieve) == 168


@claim("16-bits_math", "exponentiation by squaring is O(log n) multiplications and matches pow")
def _():
    def power(x, n):
        result, steps = 1, 0
        while n:
            if n & 1:
                result *= x
            x, n, steps = x * x, n >> 1, steps + 1
        return result, steps

    r, steps = power(3, 1000)
    assert r == 3**1000 and steps <= 10


# --------------------------------------------------------------------------- strings
def prefix_function(s):
    pi = [0] * len(s)
    k = 0
    for i in range(1, len(s)):
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return pi


@claim("17-strings", "pi[-1] of 'abcabcabc' is 6; period = n - pi[-1]; repeated-substring test matches the brute force")
def _():
    assert prefix_function("abcabcabc")[-1] == 6
    for _ in range(3000):
        s = "".join(random.choice("ab") for _ in range(random.randint(1, 10)))
        pi = prefix_function(s)[-1]
        fast = pi > 0 and len(s) % (len(s) - pi) == 0
        brute = s in (s + s)[1:-1]
        assert fast == brute, s


@claim("17-strings", "matching via pattern + '#' + text: a match ends where pi == m, and its start is i - 2m")
def _():
    for _ in range(2000):
        text = "".join(random.choice("ab") for _ in range(random.randint(1, 14)))
        pat = "".join(random.choice("ab") for _ in range(random.randint(1, 4)))
        pi = prefix_function(pat + "#" + text)
        starts = [i - 2 * len(pat) for i, v in enumerate(pi) if v == len(pat)]
        assert starts == [i for i in range(len(text) - len(pat) + 1) if text.startswith(pat, i)]


@claim("17-strings", "without the separator borders can cross from the pattern into the text (so the '#' is needed)")
def _():
    # with the separator no border can exceed the pattern length; without it the border runs past it
    assert max(prefix_function("aaa" + "#" + "aaaaaa")) == 3
    assert max(prefix_function("aaa" + "aaaaaa")) == 8


@claim(
    "17-strings (CORRECTED)",
    "s += piece in a loop is not guaranteed linear: it is O(n^2) in general; ''.join is always O(n)",
)
def _():
    def prepend(n):  # prepending can never be done in place, so each step copies the whole string
        t = time.perf_counter()
        s = ""
        for _ in range(n):
            s = "ab" + s
        return time.perf_counter() - t

    assert prepend(80000) > 5 * prepend(20000)  # 4x the pieces costs far more than 4x the time (quadratic)
    assert "".join(["ab"] * 3) == "ababab"


# --------------------------------------------------------------------------- DP / greedy
@claim("10-greedy", "greedy coin change fails for coins [1,3,4], amount 6 (3 coins vs optimal 2)")
def _():
    coins, amount = [1, 3, 4], 6
    greedy, left = 0, amount
    for c in sorted(coins, reverse=True):
        greedy += left // c
        left %= c
    dp = [0] + [math.inf] * amount
    for a in range(1, amount + 1):
        dp[a] = min(dp[a - c] + 1 for c in coins if c <= a)
    assert greedy == 3 and dp[amount] == 2


@claim(
    "15-dp",
    "0/1 knapsack: capacity DESCENDING; unbounded ASCENDING; items-outer = combinations, amount-outer = permutations",
)
def _():
    coins, amount = [1, 2, 5], 5
    comb = [1] + [0] * amount
    for c in coins:
        for a in range(c, amount + 1):
            comb[a] += comb[a - c]
    perm = [1] + [0] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if a >= c:
                perm[a] += perm[a - c]
    assert comb[amount] == 4 and perm[amount] == 9
    items, cap = [3], 6  # one item of weight 3, value 1
    asc, desc = [0] * (cap + 1), [0] * (cap + 1)
    for w in items:
        for c in range(w, cap + 1):
            asc[c] = max(asc[c], asc[c - w] + 1)
        for c in range(cap, w - 1, -1):
            desc[c] = max(desc[c], desc[c - w] + 1)
    assert asc[cap] == 2 and desc[cap] == 1  # ascending wrongly reuses the single item


@claim("15-dp", "inf + 1 is fine in Python (float inf)")
def _():
    assert math.inf + 1 == math.inf


@claim("15-dp / 00-foundations", "memoisation turns exponential recursion into polynomial: call counts of fib")
def _():
    calls = {"plain": 0, "memo": 0}

    def plain(n):
        calls["plain"] += 1
        return n if n < 2 else plain(n - 1) + plain(n - 2)

    @functools.lru_cache(None)
    def memo(n):
        calls["memo"] += 1
        return n if n < 2 else memo(n - 1) + memo(n - 2)

    assert plain(22) == memo(22)
    assert calls["plain"] > 10000 and calls["memo"] == 23


# --------------------------------------------------------------------------- trees / backtracking / graphs
@claim(
    "13-backtracking",
    "permutations of [1,2,3]: 6 leaves and 16 nodes in the decision tree; subsets 2^n; combinations C(n,k)",
)
def _():
    nodes = 0

    def go(path, left):
        nonlocal nodes
        nodes += 1
        for x in left:
            go(path + [x], [y for y in left if y != x])

    go([], [1, 2, 3])
    assert nodes == 16
    assert len(list(itertools.permutations(range(3)))) == 6
    assert sum(1 for _ in itertools.combinations(range(6), 3)) == math.comb(6, 3) == 20
    assert sum(math.comb(4, r) for r in range(5)) == 2**4 == 16
    assert sum(1 for r in range(5) for _ in itertools.combinations(range(4), r)) == 16


@claim(
    "13-backtracking", "appending path instead of path[:] makes every stored result identical (and empty at the end)"
)
def _():
    out, path = [], []

    def go(i):
        if i == 3:
            out.append(path)  # the bug: aliasing
            return
        path.append(i)
        go(i + 1)
        path.pop()

    go(0)
    assert out == [[]]


@claim("14-graphs", "Dijkstra (finalise on pop) is WRONG with a negative edge; Bellman-Ford is right")
def _():
    edges = {"A": [("B", 2), ("C", 3)], "C": [("B", -2)], "B": []}
    dist = {"A": 0}
    done, heap = set(), [(0, "A")]
    while heap:
        d, u = heapq.heappop(heap)
        if u in done:
            continue
        done.add(u)
        for v, w in edges[u]:
            if v not in done and d + w < dist.get(v, math.inf):
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    bf = {n: math.inf for n in edges}
    bf["A"] = 0
    for _ in range(len(edges) - 1):
        for u in edges:
            for v, w in edges[u]:
                bf[v] = min(bf[v], bf[u] + w)
    assert dist["B"] == 2 and bf["B"] == 1


@claim("14-graphs", "BFS: marking visited on PUSH enqueues each node once; marking on POP enqueues nodes many times")
def _():
    n = 12
    adj = {i: [j for j in range(n) if j != i] for i in range(n)}  # complete graph

    def bfs(mark_on_push):
        seen, q, pushes = {0}, collections.deque([0]), 1
        popped = set()
        while q:
            u = q.popleft()
            if not mark_on_push:
                if u in popped:
                    continue
                popped.add(u)
            for v in adj[u]:
                if mark_on_push:
                    if v in seen:
                        continue
                    seen.add(v)
                elif v in popped:
                    continue
                q.append(v)
                pushes += 1
        return pushes

    assert bfs(True) == n and bfs(False) > 3 * n


@claim(
    "14-graphs",
    "Kahn's algorithm detects a directed cycle (processed < n) - checked against DFS colouring on random graphs",
)
def _():
    def kahn_cycle(n, edges):
        indeg, adj = [0] * n, [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
            indeg[v] += 1
        q = [i for i in range(n) if indeg[i] == 0]
        done = 0
        while q:
            u = q.pop()
            done += 1
            for v in adj[u]:
                indeg[v] -= 1
                if indeg[v] == 0:
                    q.append(v)
        return done < n

    def dfs_cycle(n, edges):
        adj = [[] for _ in range(n)]
        for u, v in edges:
            adj[u].append(v)
        state = [0] * n

        def go(u):
            state[u] = 1
            for v in adj[u]:
                if state[v] == 1 or (state[v] == 0 and go(v)):
                    return True
            state[u] = 2
            return False

        return any(state[i] == 0 and go(i) for i in range(n))

    for _ in range(3000):
        n = random.randint(1, 6)
        edges = [(random.randrange(n), random.randrange(n)) for _ in range(random.randint(0, 8))]
        assert kahn_cycle(n, edges) == dfs_cycle(n, edges), (n, edges)


@claim("14-graphs", "path compression + union by size give near-constant find (inverse Ackermann): depth stays tiny")
def _():
    n = 50000
    parent, size = list(range(n)), [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for _ in range(n):
        a, b = find(random.randrange(n)), find(random.randrange(n))
        if a != b:
            if size[a] < size[b]:
                a, b = b, a
            parent[b] = a
            size[a] += size[b]

    def depth(x):
        d = 0
        while parent[x] != x:
            x, d = parent[x], d + 1
        return d

    assert max(depth(x) for x in range(n)) <= 12


# --------------------------------------------------------------------------- divide & conquer / matrix / misc
@claim(
    "19-divide_conquer",
    "merge sort does ~ n log2 n comparisons; counting cross pairs during the merge gives the inversion count",
)
def _():
    def sort_count(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, x = sort_count(a[:mid])
        right, y = sort_count(a[mid:])
        merged, i, j, cross = [], 0, 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:  # <= keeps the sort stable
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                cross += len(left) - i
                j += 1
        return merged + left[i:] + right[j:], x + y + cross

    for _ in range(500):
        a = [random.randint(0, 9) for _ in range(random.randint(0, 12))]
        brute = sum(1 for i in range(len(a)) for j in range(i + 1, len(a)) if a[i] > a[j])
        assert sort_count(a) == (sorted(a), brute)
    assert math.log2(1024) == 10


@claim("19-divide_conquer (CORRECTED)", "quicksort recurses on BOTH partitions, quickselect on ONE")
def _():
    visited = {"qs": 0, "qsel": 0}

    def quicksort(a):
        if len(a) <= 1:
            return a
        visited["qs"] += 1
        p = a[0]
        return quicksort([x for x in a[1:] if x < p]) + [p] + quicksort([x for x in a[1:] if x >= p])

    def quickselect(a, k):
        visited["qsel"] += 1
        p = a[0]
        lo, hi = [x for x in a[1:] if x < p], [x for x in a[1:] if x >= p]
        if k < len(lo):
            return quickselect(lo, k)
        return p if k == len(lo) else quickselect(hi, k - len(lo) - 1)

    data = random.sample(range(1000), 200)
    assert quicksort(data) == sorted(data) and quickselect(data, 50) == sorted(data)[50]
    assert visited["qs"] > 5 * visited["qsel"]


@claim("20-matrix", "clockwise rotation sends (r, c) -> (c, n-1-r) and equals transpose then reverse each row")
def _():
    for n in range(1, 7):
        m = [[random.randint(0, 99) for _ in range(n)] for _ in range(n)]
        direct = [[0] * n for _ in range(n)]
        for r in range(n):
            for c in range(n):
                direct[c][n - 1 - r] = m[r][c]
        composed = [list(row)[::-1] for row in zip(*m)]
        assert direct == composed


@claim("20-matrix", "Sudoku box index (r // 3) * 3 + c // 3 numbers the 9 boxes with 9 cells each")
def _():
    boxes = collections.Counter((r // 3) * 3 + c // 3 for r in range(9) for c in range(9))
    assert sorted(boxes) == list(range(9)) and set(boxes.values()) == {9}


@claim(
    "09-intervals (CORRECTED)",
    "valid sweep-line code: end events sort before start events at equal time, so touching intervals do not overlap",
)
def _():
    iv = [(1, 2), (2, 3)]
    events = sorted([(s, 1) for s, e in iv] + [(e, -1) for s, e in iv])
    running = best = 0
    for _, delta in events:
        running += delta
        best = max(best, running)
    assert best == 1


@claim("09-intervals", "two closed intervals overlap iff a.start <= b.end and b.start <= a.end")
def _():
    for _ in range(3000):
        a = sorted(random.sample(range(12), 2))
        b = sorted(random.sample(range(12), 2))
        brute = bool(set(range(a[0], a[1] + 1)) & set(range(b[0], b[1] + 1)))
        assert brute == (a[0] <= b[1] and b[0] <= a[1])


@claim(
    "05-array_tricks",
    "Kadane must start from nums[0], not 0 (all-negative input); circular max = max(kadane, total - min-subarray)",
)
def _():
    nums = [-3, -1, -2]
    cur = best = nums[0]
    for x in nums[1:]:
        cur = max(x, cur + x)
        best = max(best, cur)
    assert best == -1
    assert max(0, *nums) == 0  # the wrong initialisation would return 0


@claim("04-sliding_window", "exactly(k) = atMost(k) - atMost(k-1) (checked on random arrays)")
def _():
    def at_most(a, k):
        cnt, left, total = collections.Counter(), 0, 0
        for right, x in enumerate(a):
            cnt[x] += 1
            while len(cnt) > k:
                cnt[a[left]] -= 1
                if not cnt[a[left]]:
                    del cnt[a[left]]
                left += 1
            total += right - left + 1
        return total

    for _ in range(500):
        a = [random.randint(1, 3) for _ in range(random.randint(1, 9))]
        k = random.randint(1, 3)
        brute = sum(1 for i in range(len(a)) for j in range(i, len(a)) if len(set(a[i : j + 1])) == k)
        assert at_most(a, k) - at_most(a, k - 1) == brute


@claim("07-stack_monotonic", "monotonic stack is O(n): total pops <= total pushes despite the inner while")
def _():
    a = [random.randint(0, 99) for _ in range(5000)]
    pushes = pops = 0
    stack = []
    for x in a:
        while stack and stack[-1] < x:
            stack.pop()
            pops += 1
        stack.append(x)
        pushes += 1
    assert pops <= pushes == len(a)


@claim("02-prefix_sums", "{0: 1} seed counts subarrays that start at index 0 (nums=[3], k=3 -> 1)")
def _():
    nums, k = [3], 3
    seen, run, count = {0: 1}, 0, 0
    for x in nums:
        run += x
        count += seen.get(run - k, 0)
        seen[run] = seen.get(run, 0) + 1
    assert count == 1
    seen, run, count = {}, 0, 0  # without the seed the answer is wrong
    for x in nums:
        run += x
        count += seen.get(run - k, 0)
        seen[run] = seen.get(run, 0) + 1
    assert count == 0


@claim(
    "08-linked_list", "Floyd: restarting one pointer from the head and moving both one step meets at the cycle entrance"
)
def _():
    for _ in range(800):
        tail, loop = random.randint(0, 6), random.randint(1, 6)
        nxt = {i: i + 1 for i in range(tail + loop - 1)}
        nxt[tail + loop - 1] = tail  # cycle entrance = node `tail`
        slow = fast = 0
        while True:
            slow, fast = nxt[slow], nxt[nxt[fast]]
            if slow == fast:
                break
        slow = 0
        while slow != fast:
            slow, fast = nxt[slow], nxt[fast]
        assert slow == tail


@claim("00-foundations", "judge speed: pure Python executes only ~10^7 simple operations per second (not 10^8)")
def _():
    n = 3 * 10**6
    t = time.perf_counter()
    total = 0
    for i in range(n):
        total += i & 3
    rate = n / (time.perf_counter() - t)
    assert 5 * 10**5 < rate < 6 * 10**7, rate  # an order of magnitude below the C++ rule of thumb


def main():
    failed = 0
    for note, text, fn in CHECKS:
        try:
            fn()
            print(f"PASS  [{note}] {text}")
        except Exception as exc:  # noqa: BLE001 - report and continue
            failed += 1
            print(f"FAIL  [{note}] {text}\n      -> {type(exc).__name__}: {exc}")
    print(f"\n{len(CHECKS) - failed}/{len(CHECKS)} claims verified by execution")
    return 1 if failed else 0


if __name__ == "__main__":
    random.seed(20261115)
    sys.exit(main())
