"""Hand-trace tables for the notes.

Every table is produced by RUNNING an instrumented copy of the algorithm, so a trace can never
disagree with the real behaviour. build_notes.py swaps  {{trace:name}}  in the note sources for these.
"""

import heapq
import sys
from collections import OrderedDict, deque
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import list_to_ll, list_to_tree  # noqa: E402

TRACES = {}


def trace(name):
    def deco(f):
        TRACES[name] = f
        return f

    return deco


def table(headers, rows):
    def esc(c):
        return str(c).replace("|", "\\|")

    out = ["| " + " | ".join(esc(h) for h in headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(esc(c) for c in r) + " |" for r in rows]
    return "\n".join(out)


def block(lines):
    return "```text\n" + "\n".join(lines) + "\n```"


@trace("growth")
def _():
    import math

    rows = []
    for n in (10, 100, 1000, 10_000, 100_000, 1_000_000):
        rows.append(
            [
                f"{n:,}",
                f"{math.log2(n):.0f}",
                f"{n:,}",
                f"{int(n * math.log2(n)):,}",
                f"{n * n:,}",
                f"{2**n:,}" if n <= 20 else f"about 10^{int(n * math.log10(2))}",
            ]
        )
    return table(["n", "log2 n", "n", "n log n", "n^2", "2^n"], rows)


@trace("two_sum")
def _():
    nums, target = [2, 11, 7, 15], 9
    seen, rows = {}, []
    for i, x in enumerate(nums):
        need = target - x
        hit = need in seen
        rows.append([i, x, need, dict(seen) or "{}", f"FOUND -> [{seen[need]}, {i}]" if hit else f"store {x} -> {i}"])
        if hit:
            break
        seen[x] = i
    return f"`nums = {nums}`, `target = {target}`\n\n" + table(
        ["i", "x", "need = target - x", "seen (before)", "action"], rows
    )


@trace("prefix_hash")
def _():
    nums, k = [1, 2, 3, -3, 3], 3
    seen, pref, ans, rows = {0: 1}, 0, 0, []
    for x in nums:
        pref += x
        need = pref - k
        add = seen.get(need, 0)
        ans += add
        seen[pref] = seen.get(pref, 0) + 1
        rows.append([x, pref, need, add, ans, dict(seen)])
    return f"`nums = {nums}`, `k = {k}`; start with `seen = {{0: 1}}` (the empty prefix)\n\n" + table(
        ["x", "prefix", "need = prefix - k", "subarrays ending here", "ans", "seen after"], rows
    )


@trace("container")
def _():
    h = [1, 8, 6, 2, 5, 4, 8, 3, 7]
    left, r, best, rows = 0, len(h) - 1, 0, []
    while left < r:
        area = (r - left) * min(h[left], h[r])
        best = max(best, area)
        move = "l += 1 (left is shorter)" if h[left] < h[r] else "r -= 1"
        rows.append([left, r, h[left], h[r], f"{r - left} x {min(h[left], h[r])} = {area}", best, move])
        if h[left] < h[r]:
            left += 1
        else:
            r -= 1
    return f"`height = {h}`\n\n" + table(["l", "r", "h[l]", "h[r]", "area", "best", "move"], rows)


@trace("window_unique")
def _():
    s = "abcabcbb"
    last, left, best, rows = {}, 0, 0, []
    for r, c in enumerate(s):
        note = "-"
        if c in last and last[c] >= left:
            note = f"'{c}' last seen at {last[c]} (inside window) -> l = {last[c] + 1}"
            left = last[c] + 1
        last[c] = r
        best = max(best, r - left + 1)
        rows.append([r, c, note, left, repr(s[left : r + 1]), best])
    return f'`s = "{s}"`\n\n' + table(["r", "s[r]", "what happened", "l", "window", "best"], rows)


@trace("kadane")
def _():
    a = [-2, 1, -3, 4, -1, 2, 1, -5, 4]
    cur = best = a[0]
    rows = [[0, a[0], "start", cur, best]]
    for i, x in enumerate(a[1:], 1):
        why = "restart here" if x > cur + x else "extend previous"
        cur = max(x, cur + x)
        best = max(best, cur)
        rows.append([i, x, why, cur, best])
    return f"`nums = {a}`\n\n" + table(["i", "x", "decision", "best ending here", "best overall"], rows)


@trace("cyclic")
def _():
    a, rows = [3, 4, -1, 1], []
    n = len(a)
    for i in range(n):
        while 1 <= a[i] <= n and a[a[i] - 1] != a[i]:
            j = a[i] - 1
            a[i], a[j] = a[j], a[i]
            rows.append([i, f"swap positions {i} and {j}", list(a)])
    ans = next((i + 1 for i in range(n) if a[i] != i + 1), n + 1)
    return (
        "`nums = [3, 4, -1, 1]`; value v belongs at index v-1\n\n"
        + table(["i", "action", "array after"], rows)
        + f"\n\nFinal scan: first index where `a[i] != i+1` is the answer -> **{ans}**."
    )


@trace("binary_search")
def _():
    a, t = [-1, 0, 3, 5, 9, 12], 9
    lo, hi, rows = 0, len(a) - 1, []
    while lo <= hi:
        mid = (lo + hi) // 2
        if a[mid] == t:
            rows.append([lo, hi, mid, a[mid], "== target -> return mid"])
            break
        if a[mid] < t:
            rows.append([lo, hi, mid, a[mid], "too small -> lo = mid + 1"])
            lo = mid + 1
        else:
            rows.append([lo, hi, mid, a[mid], "too big -> hi = mid - 1"])
            hi = mid - 1
    return f"`a = {a}`, `target = {t}`\n\n" + table(["lo", "hi", "mid", "a[mid]", "decision"], rows)


@trace("koko")
def _():
    piles, h = [3, 6, 7, 11], 8
    lo, hi, rows = 1, max(piles), []
    while lo < hi:
        mid = (lo + hi) // 2
        hours = sum(-(-p // mid) for p in piles)
        ok = hours <= h
        rows.append([lo, hi, mid, hours, "yes -> hi = mid" if ok else "no -> lo = mid + 1"])
        if ok:
            hi = mid
        else:
            lo = mid + 1
    return (
        f"`piles = {piles}`, `h = {h}`; predicate: *can she finish at speed `mid`?*\n\n"
        + table(["lo", "hi", "mid", "hours needed", "hours <= h ?"], rows)
        + f"\n\nAnswer: **{lo}**"
    )


@trace("mono_stack")
def _():
    t = [73, 74, 75, 71, 69, 72, 76, 73]
    ans, st, rows = [0] * len(t), [], []
    for i, x in enumerate(t):
        popped = []
        while st and t[st[-1]] < x:
            j = st.pop()
            ans[j] = i - j
            popped.append(f"day {j} waited {i - j}")
        st.append(i)
        rows.append([i, x, ", ".join(popped) or "-", [f"{j}:{t[j]}" for j in st]])
    return (
        f"`temperatures = {t}`\n\n"
        + table(["i", "temp", "resolved (popped)", "stack (index:temp)"], rows)
        + f"\n\nAnswer: `{ans}` (days left on the stack never see a warmer day -> 0)."
    )


@trace("reverse_ll")
def _():
    head = list_to_ll([1, 2, 3])
    prev, cur, rows, step = None, head, [], 0

    def fmt(n):
        return "None" if n is None else str(n.val)

    while cur:
        nxt = cur.next
        cur.next = prev
        step += 1
        rows.append([step, fmt(prev), fmt(cur), fmt(nxt), f"{cur.val}.next now -> {fmt(prev)}"])
        prev, cur = cur, nxt
    return (
        "`1 -> 2 -> 3`\n\n"
        + table(["step", "prev", "cur", "nxt (saved)", "re-wire"], rows)
        + "\n\nReturn `prev` = 3 -> 2 -> 1."
    )


@trace("floyd")
def _():
    nums = [1, 3, 4, 2, 2]
    slow = fast = nums[0]
    rows = [["start", slow, fast]]
    while True:
        slow, fast = nums[slow], nums[nums[fast]]
        rows.append(["phase 1", slow, fast])
        if slow == fast:
            break
    slow = nums[0]
    rows.append(["phase 2 reset", slow, fast])
    while slow != fast:
        slow, fast = nums[slow], nums[fast]
        rows.append(["phase 2", slow, fast])
    return (
        f"`nums = {nums}`; edges: i -> nums[i]  (0->1, 1->3, 2->4, 3->2, 4->2: the cycle is 2->4->2)\n\n"
        + table(["phase", "slow", "fast"], rows)
        + f"\n\nThey meet at **{slow}** = the duplicate."
    )


@trace("merge_intervals")
def _():
    iv = [[1, 3], [8, 10], [2, 6], [15, 18]]
    out, rows = [], []
    for s, e in sorted(iv):
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
            act = f"overlaps last -> extend end to {out[-1][1]}"
        else:
            out.append([s, e])
            act = "gap -> new interval"
        rows.append([[s, e], act, [x[:] for x in out]])
    return f"input `{iv}` -> sorted by start first\n\n" + table(["next", "action", "output so far"], rows)


@trace("jump_game")
def _():
    out = []
    for nums in ([2, 3, 1, 1, 4], [3, 2, 1, 0, 4]):
        reach, rows, res = 0, [], True
        for i, x in enumerate(nums):
            if i > reach:
                rows.append([i, x, reach, "i > reach -> STUCK"])
                res = False
                break
            reach = max(reach, i + x)
            rows.append([i, x, reach, "ok"])
        out.append(f"`nums = {nums}` -> **{res}**\n\n" + table(["i", "nums[i]", "farthest reach", "note"], rows))
    return "\n\n".join(out)


@trace("kth_largest")
def _():
    nums, k = [3, 2, 1, 5, 6, 4], 2
    h, rows = [], []
    for x in nums:
        heapq.heappush(h, x)
        ev = "-"
        if len(h) > k:
            ev = f"pop smallest = {heapq.heappop(h)}"
        rows.append([x, ev, list(h)])
    return (
        f"`nums = {nums}`, `k = {k}` (min-heap of the k largest so far)\n\n"
        + table(["x", "eviction", "heap after"], rows)
        + f"\n\nRoot `{h[0]}` is the {k}-nd largest."
    )


@trace("tree_path")
def _():
    root = list_to_tree([-10, 9, 20, None, None, 15, 7])
    rows, best = [], [float("-inf")]

    def gain(n):
        if not n:
            return 0
        left, r = max(gain(n.left), 0), max(gain(n.right), 0)
        bend = n.val + left + r
        best[0] = max(best[0], bend)
        rows.append([n.val, left, r, bend, n.val + max(left, r), best[0]])
        return n.val + max(left, r)

    gain(root)
    return (
        "Tree `[-10, 9, 20, null, null, 15, 7]` (post-order: children are finished before their parent)\n\n"
        + table(
            [
                "node",
                "left gain (>=0)",
                "right gain (>=0)",
                "bend here = val+l+r",
                "returned upward = val+max(l,r)",
                "best so far",
            ],
            rows,
        )
        + f"\n\nAnswer: **{best[0]}** (path 15 -> 20 -> 7; the root -10 would only hurt)."
    )


@trace("subsets_tree")
def _():
    nums, lines, path = [1, 2, 3], [], []

    def go(i, d):
        pad = "  " * d
        if i == len(nums):
            lines.append(f"{pad}leaf: RECORD {path}")
            return
        lines.append(f"{pad}go({i}) path={path}: choose {nums[i]}")
        path.append(nums[i])
        go(i + 1, d + 1)
        path.pop()
        lines.append(f"{pad}go({i}) path={path}: skip {nums[i]}")
        go(i + 1, d + 1)

    go(0, 0)
    return "`nums = [1, 2, 3]` - read top to bottom; indentation = recursion depth\n\n" + block(lines)


@trace("bfs_grid")
def _():
    g = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]
    q, fresh = deque(), 0
    for r in range(3):
        for c in range(3):
            if g[r][c] == 2:
                q.append((r, c))
            elif g[r][c] == 1:
                fresh += 1

    def show(m):
        return ["".join(".12"[v] for v in row) for row in g]

    lines = ["minute 0:   " + "  ".join(show(0)) + f"   fresh={fresh}"]
    minute = 0
    while q and fresh:
        for _ in range(len(q)):
            x, y = q.popleft()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < 3 and 0 <= ny < 3 and g[nx][ny] == 1:
                    g[nx][ny] = 2
                    fresh -= 1
                    q.append((nx, ny))
        minute += 1
        lines.append(f"minute {minute}:   " + "  ".join(show(0)) + f"   fresh={fresh}")
    return (
        "`.` empty, `1` fresh, `2` rotten - each row of the grid shown side by side\n\n"
        + block(lines)
        + f"\n\nAnswer: **{minute}** minutes."
    )


@trace("dijkstra")
def _():
    adj = {1: [(2, 1), (3, 4)], 2: [(3, 2), (4, 6)], 3: [(4, 3)], 4: []}
    dist, heap, rows = {}, [(0, 1)], []
    while heap:
        d, u = heapq.heappop(heap)
        if u in dist:
            rows.append([f"({d}, {u})", "stale -> skip", "-"])
            continue
        dist[u] = d
        pushed = []
        for v, w in adj[u]:
            if v not in dist:
                heapq.heappush(heap, (d + w, v))
                pushed.append(f"({d + w}, {v})")
        rows.append([f"({d}, {u})", f"settle {u} at {d}", ", ".join(pushed) or "-"])
    return (
        "Edges: 1->2 (1), 1->3 (4), 2->3 (2), 2->4 (6), 3->4 (3); source 1\n\n"
        + table(["heap pop (dist, node)", "action", "pushed"], rows)
        + f"\n\nFinal distances: `{dist}`"
    )


@trace("dsu")
def _():
    edges = [[1, 2], [2, 3], [4, 5], [3, 1]]
    parent = list(range(6))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    rows = []
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            rows.append(
                [[u, v], f"find({u})={ru} == find({v})={rv}", "SAME component -> this edge closes a cycle", parent[1:]]
            )
        else:
            parent[ru] = rv
            rows.append([[u, v], f"find({u})={ru}, find({v})={rv}", f"union: parent[{ru}] = {rv}", parent[1:]])
    return "Nodes 1..5 start as their own parent.\n\n" + table(["edge", "roots", "result", "parent[1..5]"], rows)


@trace("kahn")
def _():
    n, pre = 4, [[1, 0], [2, 0], [3, 1], [3, 2]]
    adj = [[] for _ in range(n)]
    indeg = [0] * n
    for a, b in pre:
        adj[b].append(a)
        indeg[a] += 1
    q, rows, order = deque(i for i in range(n) if indeg[i] == 0), [], []
    rows.append(["start", "-", indeg[:], list(q)])
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
        rows.append([f"pop {u}", order[:], indeg[:], list(q)])
    return (
        "Edges (b -> a): 0->1, 0->2, 1->3, 2->3\n\n"
        + table(["step", "order so far", "in-degree [0..3]", "queue"], rows)
        + f"\n\nAll {n} nodes processed -> no cycle; a valid order is `{order}`."
    )


@trace("coin_dp")
def _():
    coins, amt = [1, 2, 5], 11
    INF = float("inf")
    dp, last = [0] + [INF] * amt, [None] * (amt + 1)
    for a in range(1, amt + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a], last[a] = dp[a - c] + 1, c
    used, a = [], amt
    while a:
        used.append(last[a])
        a -= last[a]
    return (
        f"`coins = {coins}`, `amount = {amt}`\n\n"
        + table(
            ["amount a"] + list(range(amt + 1)), [["dp[a] (fewest coins)"] + dp, ["last coin used"] + ["-"] + last[1:]]
        )
        + f"\n\nRead it back: dp[{amt}] = {dp[amt]}. Follow 'last coin used' from {amt} downwards: "
        + " then ".join(map(str, used))
        + f" -> coins {sorted(used, reverse=True)}."
    )


@trace("lcs_dp")
def _():
    a, b = "abcde", "ace"
    m, n = len(a), len(b)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            dp[i][j] = dp[i - 1][j - 1] + 1 if a[i - 1] == b[j - 1] else max(dp[i - 1][j], dp[i][j - 1])
    rows = [[f"{a[i - 1] if i else ''} (i={i})"] + dp[i] for i in range(m + 1)]
    return (
        f'`text1 = "{a}"` (rows), `text2 = "{b}"` (columns)\n\n'
        + table(["", "''"] + [f"{b[j - 1]}" for j in range(1, n + 1)], rows)
        + "\n\nMatch -> take the diagonal + 1; otherwise the max of up / left. Answer is the bottom-right cell."
    )


@trace("bits")
def _():
    nums, x, rows = [4, 1, 2, 1, 2], 0, []
    for v in nums:
        x ^= v
        rows.append([v, format(v, "03b"), format(x, "03b"), x])
    a = table(["next v", "binary", "running XOR (binary)", "value"], rows)
    bits = [0] * 9
    for i in range(1, 9):
        bits[i] = bits[i >> 1] + (i & 1)
    b = table(
        ["i"] + list(range(9)), [["binary"] + [format(i, "04b") for i in range(9)], ["bits[i>>1] + (i&1)"] + bits]
    )
    return (
        "**XOR cancels pairs** (`[4,1,2,1,2]`):\n\n"
        + a
        + "\n\n**Counting bits** (`bits[i] = bits[i>>1] + (i & 1)`):\n\n"
        + b
    )


@trace("prefix_fn")
def _():
    s = "ababaca"
    pi, rows = [0] * len(s), [[0, s[0], "-", 0]]
    for i in range(1, len(s)):
        k, chain = pi[i - 1], []
        while k and s[i] != s[k]:
            chain.append(k)
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
        rows.append([i, s[i], ("fell back from " + " -> ".join(map(str, chain))) if chain else "-", k])
    return f'`s = "{s}"`; pi[i] = length of the longest proper prefix of s[:i+1] that is also a suffix\n\n' + table(
        ["i", "s[i]", "fallback", "pi[i]"], rows
    )


@trace("lru")
def _():
    cap, d, rows = 2, OrderedDict(), []

    def put(k, v):
        if k in d:
            d.move_to_end(k)
        d[k] = v
        ev = ""
        if len(d) > cap:
            ev = f"  evict {d.popitem(last=False)[0]}"
        rows.append([f"put({k},{v})", list(d.items()), ev or "-"])

    def get(k):
        if k in d:
            d.move_to_end(k)
        rows.append([f"get({k})", list(d.items()), f"-> {d[k]}" if k in d else "-> -1"])

    put(1, 1)
    put(2, 2)
    get(1)
    put(3, 3)
    get(2)
    return "capacity 2; list shown **least recent -> most recent**\n\n" + table(["op", "cache state", "note"], rows)


@trace("merge_sort")
def _():
    lines = []

    def sort(a, d=0):
        pad = "  " * d
        if len(a) <= 1:
            return a
        mid = len(a) // 2
        lines.append(f"{pad}split {a} -> {a[:mid]} | {a[mid:]}")
        left, r = sort(a[:mid], d + 1), sort(a[mid:], d + 1)
        out, i, j = [], 0, 0
        while i < len(left) and j < len(r):
            if left[i] <= r[j]:
                out.append(left[i])
                i += 1
            else:
                out.append(r[j])
                j += 1
        out += left[i:] + r[j:]
        lines.append(f"{pad}merge {left} + {r} -> {out}")
        return out

    sort([5, 2, 4, 1, 3])
    return block(lines)


@trace("two_heaps")
def _():
    lo, hi, rows = [], [], []
    for x in [5, 2, 8, 1]:
        heapq.heappush(lo, -x)
        heapq.heappush(hi, -heapq.heappop(lo))
        if len(hi) > len(lo):
            heapq.heappush(lo, -heapq.heappop(hi))
        med = float(-lo[0]) if len(lo) > len(hi) else (-lo[0] + hi[0]) / 2
        rows.append([x, sorted(-v for v in lo), sorted(hi), med])
    return "stream `5, 2, 8, 1`\n\n" + table(["add", "lower half (max-heap)", "upper half (min-heap)", "median"], rows)
