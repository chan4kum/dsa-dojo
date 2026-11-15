from core import *

S = SKIP

PROBLEMS = [
    dict(
        title="Kth Largest Element in a Stream", diff="E", lc=703, slug="kth-largest-element-in-a-stream", kind="design", cls="KthLargest",
        prompt="Maintain the k-th largest element of a growing stream. __init__(k, nums) starts with an initial list; add(val) inserts val and returns the current k-th largest.",
        sig="class KthLargest:\n    def __init__(self, k: int, nums: List[int]):\n        pass\n    def add(self, val: int) -> int:\n        pass",
        tests=[((3, [4, 5, 8, 2]), [("add", [3], 4), ("add", [5], 5), ("add", [10], 5), ("add", [9], 8), ("add", [4], 8)]),
               ((1, []), [("add", [-3], -3), ("add", [-2], -2), ("add", [-4], -2), ("add", [0], 0)]),
               ((2, [0]), [("add", [-1], -1), ("add", [1], 0), ("add", [-2], 0), ("add", [-4], 0), ("add", [3], 1)])],
        hints=["Sorting the whole list on every add costs O(n log n).",
               "Only the k largest elements ever matter.",
               "Keep a MIN-heap of size k: its root is the k-th largest. On add: push, and pop if size > k."],
        pattern="Fixed-size min-heap = 'k largest so far' (root = k-th largest)",
        explain="""
        The smallest of the k largest is the k-th largest. A min-heap exposes the smallest in O(1) and evicts it in
        O(log k) when something bigger arrives. Mirror image: a max-heap of size k tracks the k-th SMALLEST.""",
        cx="add: O(log k)", brute_cx="add: O(n log n) - keep a list, sort each time",
        brute=r'''
class KthLargest:
    def __init__(self, k, nums):
        self.k, self.a = k, list(nums)
    def add(self, val):
        self.a.append(val)
        return sorted(self.a, reverse=True)[self.k - 1]
''',
        solution=r'''
class KthLargest:
    def __init__(self, k, nums):
        self.k = k
        self.h = []
        for x in nums:
            self.add(x)

    def add(self, val):
        heapq.heappush(self.h, val)
        if len(self.h) > self.k:
            heapq.heappop(self.h)
        return self.h[0]
''',
    ),
    dict(
        title="Implement Queue using Stacks", diff="E", lc=232, slug="implement-queue-using-stacks", kind="design", cls="MyQueue",
        prompt="Implement a FIFO queue (push, pop, peek, empty) using only two stacks (list append/pop at the end).",
        sig="class MyQueue:\n    def __init__(self):\n        pass\n    def push(self, x: int) -> None:\n        pass\n    def pop(self) -> int:\n        pass\n    def peek(self) -> int:\n        pass\n    def empty(self) -> bool:\n        pass",
        tests=[((), [("push", [1], S), ("push", [2], S), ("peek", [], 1), ("pop", [], 1), ("empty", [], False), ("pop", [], 2), ("empty", [], True)]),
               ((), [("push", [5], S), ("pop", [], 5), ("push", [6], S), ("push", [7], S), ("pop", [], 6), ("peek", [], 7)]),
               ((), [("empty", [], True), ("push", [1], S), ("empty", [], False), ("pop", [], 1), ("empty", [], True)])],
        hints=["A stack reverses order; two stacks reverse it twice.",
               "Push onto an 'in' stack. For pop/peek you need the OLDEST element - the bottom of 'in'.",
               "When 'out' is empty, move everything from 'in' to 'out' (reversing it). Only then pop from 'out'. Each element moves at most once => amortised O(1)."],
        pattern="Two stacks + lazy transfer (amortised O(1))",
        explain="""
        Transferring only when 'out' is empty keeps the order correct (older items are always in 'out' before newer
        ones) and makes the total transfer cost proportional to the number of pushes.""",
        cx="amortised O(1) per op", brute_cx="pop/peek: O(n) - move everything back and forth every call",
        brute=r'''
class MyQueue:
    def __init__(self):
        self.a = []
    def push(self, x):
        self.a.append(x)
    def pop(self):
        b = []
        while len(self.a) > 1:
            b.append(self.a.pop())
        x = self.a.pop()
        while b:
            self.a.append(b.pop())
        return x
    def peek(self):
        b = []
        while self.a:
            b.append(self.a.pop())
        x = b[-1]
        while b:
            self.a.append(b.pop())
        return x
    def empty(self):
        return not self.a
''',
        solution=r'''
class MyQueue:
    def __init__(self):
        self.inp, self.out = [], []

    def push(self, x):
        self.inp.append(x)

    def _shift(self):
        if not self.out:
            while self.inp:
                self.out.append(self.inp.pop())

    def pop(self):
        self._shift()
        return self.out.pop()

    def peek(self):
        self._shift()
        return self.out[-1]

    def empty(self):
        return not self.inp and not self.out
''',
    ),
    dict(
        title="Time Based Key-Value Store", diff="M", lc=981, slug="time-based-key-value-store", kind="design", cls="TimeMap",
        prompt="set(key, value, timestamp) stores a value; get(key, timestamp) returns the value with the largest timestamp_prev <= timestamp for that key, or '' if none. Timestamps for a key arrive in increasing order.",
        sig="class TimeMap:\n    def __init__(self):\n        pass\n    def set(self, key: str, value: str, timestamp: int) -> None:\n        pass\n    def get(self, key: str, timestamp: int) -> str:\n        pass",
        tests=[((), [("set", ["foo", "bar", 1], S), ("get", ["foo", 1], "bar"), ("get", ["foo", 3], "bar"), ("set", ["foo", "bar2", 4], S), ("get", ["foo", 4], "bar2"), ("get", ["foo", 5], "bar2"), ("get", ["foo", 0], ""), ("get", ["x", 1], "")]),
               ((), [("set", ["a", "1", 10], S), ("set", ["a", "2", 20], S), ("get", ["a", 15], "1"), ("get", ["a", 20], "2"), ("get", ["a", 9], "")]),
               ((), [("set", ["k", "v", 5], S), ("set", ["j", "w", 6], S), ("get", ["k", 6], "v"), ("get", ["j", 5], "")])],
        hints=["Each key has its own history of (timestamp, value) pairs.",
               "Timestamps are appended in increasing order, so each history is already sorted.",
               "get = binary search for the last timestamp <= t (bisect_right - 1)."],
        pattern="Hash map of sorted lists + binary search (floor lookup)",
        explain="""
        'Latest entry not after t' is a floor query on a sorted list: bisect_right gives the insertion point, minus one
        is the answer. This 'versioned data' idea appears in many system designs (MVCC, event logs).""",
        cx="set O(1), get O(log n)", brute_cx="get: O(n) - scan the history",
        brute=r'''
class TimeMap:
    def __init__(self):
        self.d = defaultdict(list)
    def set(self, key, value, timestamp):
        self.d[key].append((timestamp, value))
    def get(self, key, timestamp):
        best = ""
        for t, v in self.d[key]:
            if t <= timestamp:
                best = v
        return best
''',
        solution=r'''
class TimeMap:
    def __init__(self):
        self.times = defaultdict(list)
        self.vals = defaultdict(list)

    def set(self, key, value, timestamp):
        self.times[key].append(timestamp)
        self.vals[key].append(value)

    def get(self, key, timestamp):
        i = bisect.bisect_right(self.times[key], timestamp)
        return self.vals[key][i - 1] if i else ""
''',
    ),
    dict(
        title="Design Add and Search Words Data Structure", diff="M", lc=211, slug="design-add-and-search-words-data-structure", kind="design", cls="WordDictionary",
        prompt="add_word(word) stores a word; search(word) returns True if any stored word matches, where '.' in the query matches any single letter.",
        sig="class WordDictionary:\n    def __init__(self):\n        pass\n    def add_word(self, word: str) -> None:\n        pass\n    def search(self, word: str) -> bool:\n        pass",
        tests=[((), [("add_word", ["bad"], S), ("add_word", ["dad"], S), ("add_word", ["mad"], S), ("search", ["pad"], False), ("search", ["bad"], True), ("search", [".ad"], True), ("search", ["b.."], True), ("search", ["b."], False), ("search", ["..."], True)]),
               ((), [("search", ["a"], False), ("add_word", ["a"], S), ("search", [".", ], True), ("search", ["a."], False)]),
               ((), [("add_word", ["at"], S), ("add_word", ["and"], S), ("add_word", ["an"], S), ("search", ["a"], False), ("search", [".at"], False), ("add_word", ["bat"], S), ("search", [".at"], True), ("search", ["an."], True), ("search", ["a.d."], False)])],
        hints=["A plain trie handles exact words. What changes when a character is '.'?",
               "At a '.', every child is a possibility.",
               "Recursive search(node, i): for '.' try all children; for a letter follow that child only; success at i == len(word) if the node is an end of a word."],
        pattern="Trie + DFS branching on wildcards",
        explain="""
        A trie shares prefixes, so a wildcard explores only existing branches. Worst case (all dots) visits every
        node; typical cases prune quickly.""",
        cx="add O(L); search O(L) typical, O(26^L) worst", brute_cx="search: O(total characters) - compare with every stored word",
        brute=r'''
class WordDictionary:
    def __init__(self):
        self.words = []
    def add_word(self, word):
        self.words.append(word)
    def search(self, word):
        return any(len(w) == len(word) and all(a == b or b == "." for a, b in zip(w, word)) for w in self.words)
''',
        solution=r'''
class WordDictionary:
    def __init__(self):
        self.root = {}

    def add_word(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True

    def search(self, word):
        def dfs(node, i):
            if i == len(word):
                return "$" in node
            ch = word[i]
            if ch == ".":
                return any(dfs(child, i + 1) for k, child in node.items() if k != "$")
            return ch in node and dfs(node[ch], i + 1)
        return dfs(self.root, 0)
''',
    ),
    dict(
        title="Design Browser History", diff="M", lc=1472, slug="design-browser-history", kind="design", cls="BrowserHistory",
        prompt="BrowserHistory(homepage); visit(url) navigates and clears forward history; back(steps) moves back at most `steps` pages and returns the current url; forward(steps) likewise forward.",
        sig="class BrowserHistory:\n    def __init__(self, homepage: str):\n        pass\n    def visit(self, url: str) -> None:\n        pass\n    def back(self, steps: int) -> str:\n        pass\n    def forward(self, steps: int) -> str:\n        pass",
        tests=[(("leetcode.com",), [("visit", ["google.com"], S), ("visit", ["facebook.com"], S), ("visit", ["youtube.com"], S), ("back", [1], "facebook.com"), ("back", [1], "google.com"), ("forward", [1], "facebook.com"), ("visit", ["linkedin.com"], S), ("forward", [2], "linkedin.com"), ("back", [2], "google.com"), ("back", [7], "leetcode.com")]),
               (("a",), [("back", [3], "a"), ("forward", [3], "a"), ("visit", ["b"], S), ("back", [1], "a"), ("forward", [5], "b")]),
               (("h",), [("visit", ["x"], S), ("visit", ["y"], S), ("back", [1], "x"), ("visit", ["z"], S), ("forward", [1], "z"), ("back", [2], "h")])],
        hints=["You need to move along a line of pages and drop the 'future' when visiting.",
               "An array plus a cursor works: history[0..cur] is the past, history[cur+1..] is the future.",
               "visit: truncate everything after cur and append. back/forward: clamp cur += or -= steps within [0, last]."],
        pattern="Array + cursor (truncate on write)",
        explain="""
        Two stacks (back / forward) also work, but the array with a moving index makes back(k) and forward(k) O(1)
        instead of O(k).""",
        cx="visit O(1) amortised, back/forward O(1)", brute_cx="back/forward: O(steps) - two stacks, move one page at a time",
        brute=r'''
class BrowserHistory:
    def __init__(self, homepage):
        self.back_st, self.fwd_st, self.cur = [], [], homepage
    def visit(self, url):
        self.back_st.append(self.cur)
        self.cur = url
        self.fwd_st = []
    def back(self, steps):
        while steps and self.back_st:
            self.fwd_st.append(self.cur)
            self.cur = self.back_st.pop()
            steps -= 1
        return self.cur
    def forward(self, steps):
        while steps and self.fwd_st:
            self.back_st.append(self.cur)
            self.cur = self.fwd_st.pop()
            steps -= 1
        return self.cur
''',
        solution=r'''
class BrowserHistory:
    def __init__(self, homepage):
        self.hist = [homepage]
        self.cur = 0

    def visit(self, url):
        del self.hist[self.cur + 1:]
        self.hist.append(url)
        self.cur += 1

    def back(self, steps):
        self.cur = max(0, self.cur - steps)
        return self.hist[self.cur]

    def forward(self, steps):
        self.cur = min(len(self.hist) - 1, self.cur + steps)
        return self.hist[self.cur]
''',
    ),
    dict(
        title="Range Sum Query - Mutable", diff="M", lc=307, slug="range-sum-query-mutable", kind="design", cls="NumArray",
        prompt="NumArray(nums) supports update(index, val) (set nums[index] = val) and sum_range(left, right) (inclusive sum). Both should be fast when there are many operations.",
        sig="class NumArray:\n    def __init__(self, nums: List[int]):\n        pass\n    def update(self, index: int, val: int) -> None:\n        pass\n    def sum_range(self, left: int, right: int) -> int:\n        pass",
        tests=[(([1, 3, 5],), [("sum_range", [0, 2], 9), ("update", [1, 2], S), ("sum_range", [0, 2], 8)]),
               (([5],), [("sum_range", [0, 0], 5), ("update", [0, -1], S), ("sum_range", [0, 0], -1)]),
               (([1, 2, 3, 4, 5, 6, 7, 8],), [("sum_range", [2, 5], 18), ("update", [3, 10], S), ("sum_range", [2, 5], 24), ("sum_range", [0, 7], 42), ("update", [0, 0], S), ("sum_range", [0, 1], 2)])],
        hints=["A prefix-sum array makes sum_range O(1) but update O(n). A plain array has the opposite trade-off.",
               "You want both operations in O(log n): store partial sums over power-of-two sized blocks.",
               "Fenwick tree (Binary Indexed Tree): tree[i] holds the sum of the range (i - lowbit(i), i]. update walks i += i & -i, query walks i -= i & -i."],
        pattern="Fenwick tree / BIT (prefix sums with point updates)",
        explain="""
        i & -i isolates the lowest set bit; each tree cell covers exactly that many elements below it. A prefix query
        hops down by removing the lowest bit (O(log n) cells), an update hops up by adding it. Segment trees solve the
        same problem with more generality (min/max/gcd).""",
        cx="update O(log n), sum_range O(log n)", brute_cx="update O(1), sum_range O(n) - plain array",
        brute='''
class NumArray:
    def __init__(self, nums):
        self.a = list(nums)
    def update(self, index, val):
        self.a[index] = val
    def sum_range(self, left, right):
        return sum(self.a[left:right + 1])
''',
        solution='''
class NumArray:
    def __init__(self, nums):
        self.n = len(nums)
        self.a = [0] * self.n
        self.t = [0] * (self.n + 1)           # 1-indexed Fenwick tree
        for i, x in enumerate(nums):
            self.update(i, x)

    def update(self, index, val):
        delta, self.a[index] = val - self.a[index], val
        i = index + 1
        while i <= self.n:
            self.t[i] += delta
            i += i & -i

    def _prefix(self, i):                      # sum of the first i elements
        s = 0
        while i > 0:
            s += self.t[i]
            i -= i & -i
        return s

    def sum_range(self, left, right):
        return self._prefix(right + 1) - self._prefix(left)
''',
    ),
]
