"""Design problems - the problem bank for the "design" topic.

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

from core import SKIP

# Design problems: `tests` = (constructor_args, [(method, args, expected_or_SKIP), ...]).
S = SKIP

PROBLEMS = [
    # ---- Min Stack (LeetCode 155) ----
    dict(
        title="Min Stack",
        diff="M",
        lc=155,
        slug="min-stack",
        prompt="Design a stack supporting push, pop, top and get_min, all in O(1).",
        sig=(
            "class MinStack:\n    def __init__(self):\n        pass\n    def push(self, val: int) -> None:\n        "
            "pass\ndef pop(self) -> None:\n        pass\n    def top(self) -> int:\n        pass\n    def "
            "get_min(self) -> int:\n        pass"
        ),
        kind="design",
        cls="MinStack",
        tests=[
            (
                (),
                [
                    ("push", [-2], S),
                    ("push", [0], S),
                    ("push", [-3], S),
                    ("get_min", [], -3),
                    ("pop", [], S),
                    ("top", [], 0),
                    ("get_min", [], -2),
                ],
            ),
            ((), [("push", [1], S), ("push", [1], S), ("get_min", [], 1), ("pop", [], S), ("get_min", [], 1)]),
            (
                (),
                [
                    ("push", [5], S),
                    ("push", [3], S),
                    ("push", [7], S),
                    ("get_min", [], 3),
                    ("pop", [], S),
                    ("pop", [], S),
                    ("get_min", [], 5),
                ],
            ),
        ],
        hints=[
            "The minimum can change every time you pop. What extra information must each stack entry carry?",
            "Store, alongside each value, the minimum of the stack AT THAT MOMENT.",
            "push(v): store (v, min(v, current_min)). get_min is the top entry's second field.",
        ],
        pattern="Augmented stack: keep running aggregates next to each element",
        explain=(
            "Popping restores the exact previous state, so the previous minimum must already be stored. Pair "
            "each\n        value with min-so-far. All operations O(1), O(n) space."
        ),
        cx="all operations O(1)",
        brute_cx="get_min is O(n) - scans the whole stack",
        brute=r"""
# BRUTE FORCE: get_min is O(n) - scans the whole stack
class MinStack:
    def __init__(self):
        self.a = []

    def push(self, val):
        self.a.append(val)

    def pop(self):
        self.a.pop()

    def top(self):
        return self.a[-1]

    def get_min(self):
        return min(self.a)
""",
        solution=r"""
# OPTIMISED: all operations O(1)
# Idea: Augmented stack: keep running aggregates next to each element
class MinStack:
    def __init__(self):
        self.stack = []  # (value, min so far)

    def push(self, val):
        cur_min = min(val, self.stack[-1][1]) if self.stack else val
        self.stack.append((val, cur_min))

    def pop(self):
        self.stack.pop()

    def top(self):
        return self.stack[-1][0]

    def get_min(self):
        return self.stack[-1][1]
""",
    ),
    # ---- LRU Cache (LeetCode 146) ----
    dict(
        title="LRU Cache",
        diff="M",
        lc=146,
        slug="lru-cache",
        prompt=(
            "Design a cache with a fixed capacity; get(key) returns the value or -1, put(key, value) "
            "inserts/updates and evicts the LEAST recently used key when over capacity. Both operations O(1)."
        ),
        sig=(
            "class LRUCache:\n    def __init__(self, capacity: int):\n        pass\n    def get(self, key: int) -> "
            "int:\n        pass\n    def put(self, key: int, value: int) -> None:\n        pass"
        ),
        kind="design",
        cls="LRUCache",
        tests=[
            (
                (2,),
                [
                    ("put", [1, 1], S),
                    ("put", [2, 2], S),
                    ("get", [1], 1),
                    ("put", [3, 3], S),
                    ("get", [2], -1),
                    ("put", [4, 4], S),
                    ("get", [1], -1),
                    ("get", [3], 3),
                    ("get", [4], 4),
                ],
            ),
            ((1,), [("put", [2, 1], S), ("get", [2], 1), ("put", [3, 2], S), ("get", [2], -1), ("get", [3], 2)]),
            (
                (2,),
                [
                    ("put", [2, 1], S),
                    ("put", [2, 2], S),
                    ("get", [2], 2),
                    ("put", [1, 1], S),
                    ("put", [4, 1], S),
                    ("get", [2], -1),
                ],
            ),
        ],
        hints=[
            "You need O(1) lookup by key AND O(1) 'move to most-recent' / 'remove oldest'.",
            "Hash map gives lookup; a doubly linked list gives O(1) reordering. The map points at list nodes.",
            (
                "In Python an OrderedDict does both: move_to_end(key) on every use, popitem(last=False) to evict. "
                "(In an interview, be ready to build the linked list by hand.)"
            ),
        ],
        pattern="Hash map + doubly linked list (or OrderedDict): O(1) ordered cache",
        explain=(
            "Order of use is maintained by the list: front = most recent, back = least recent. get and put "
            "both\n        'touch' the key (move to front). When size exceeds capacity remove the back node and its "
            "map entry.\n        OrderedDict hides exactly that structure."
        ),
        cx="get/put O(1)",
        brute_cx="O(n) per operation - linear search in a list",
        brute=r"""
# BRUTE FORCE: O(n) per operation - linear search in a list
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.items = []  # [key, value], least recent first

    def get(self, key):
        for i, (k, v) in enumerate(self.items):
            if k == key:
                self.items.append(self.items.pop(i))
                return v
        return -1

    def put(self, key, value):
        for i, (k, _) in enumerate(self.items):
            if k == key:
                self.items.pop(i)
                break
        self.items.append([key, value])
        if len(self.items) > self.cap:
            self.items.pop(0)
""",
        solution=r"""
# OPTIMISED: get/put O(1)
# Idea: Hash map + doubly linked list (or OrderedDict): O(1) ordered cache
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.d = OrderedDict()  # least recent first

    def get(self, key):
        if key not in self.d:
            return -1
        self.d.move_to_end(key)  # mark most recent
        return self.d[key]

    def put(self, key, value):
        if key in self.d:
            self.d.move_to_end(key)
        self.d[key] = value
        if len(self.d) > self.cap:
            self.d.popitem(last=False)  # evict least recent
""",
    ),
    # ---- Implement Trie (Prefix Tree) (LeetCode 208) ----
    dict(
        title="Implement Trie (Prefix Tree)",
        diff="M",
        lc=208,
        slug="implement-trie-prefix-tree",
        prompt="Implement a trie with insert(word), search(word) (exact match) and starts_with(prefix).",
        sig=(
            "class Trie:\n    def __init__(self):\n        pass\n    def insert(self, word: str) -> None:\n        "
            "pass\ndef search(self, word: str) -> bool:\n        pass\n    def starts_with(self, prefix: str) -> "
            "bool:\n        pass"
        ),
        kind="design",
        cls="Trie",
        tests=[
            (
                (),
                [
                    ("insert", ["apple"], S),
                    ("search", ["apple"], True),
                    ("search", ["app"], False),
                    ("starts_with", ["app"], True),
                    ("insert", ["app"], S),
                    ("search", ["app"], True),
                ],
            ),
            (
                (),
                [
                    ("search", ["a"], False),
                    ("starts_with", ["a"], False),
                    ("insert", ["a"], S),
                    ("search", ["a"], True),
                ],
            ),
            (
                (),
                [
                    ("insert", ["car"], S),
                    ("insert", ["cat"], S),
                    ("starts_with", ["ca"], True),
                    ("starts_with", ["cab"], False),
                    ("search", ["ca"], False),
                ],
            ),
        ],
        hints=[
            "A hash set of words answers search, but starts_with would scan every word.",
            "Store words character by character: each node maps a letter to a child node.",
            (
                "Mark the node where a word ends (e.g. a '$' key). search needs the end marker; starts_with only "
                "needs the path to exist."
            ),
        ],
        pattern="Trie (prefix tree): O(L) insert/search per word, shared prefixes",
        explain=(
            "Each root-to-node path spells a prefix. Cost depends on word length L, not the number of "
            "words.\n        Dict-of-dicts is the shortest Python implementation. Used for autocomplete, word "
            "search on grids,\n        longest-common-prefix, XOR tries."
        ),
        cx="insert/search/starts_with O(L)",
        brute_cx="starts_with is O(total characters) - scans every stored word",
        brute=r"""
# BRUTE FORCE: starts_with is O(total characters) - scans every stored word
class Trie:
    def __init__(self):
        self.words = set()

    def insert(self, word):
        self.words.add(word)

    def search(self, word):
        return word in self.words

    def starts_with(self, prefix):
        return any(w.startswith(prefix) for w in self.words)
""",
        solution=r"""
# OPTIMISED: insert/search/starts_with O(L)
# Idea: Trie (prefix tree): O(L) insert/search per word, shared prefixes
class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for ch in word:
            node = node.setdefault(ch, {})
        node["$"] = True  # end-of-word marker

    def _walk(self, s):
        node = self.root
        for ch in s:
            if ch not in node:
                return None
            node = node[ch]
        return node

    def search(self, word):
        node = self._walk(word)
        return node is not None and "$" in node

    def starts_with(self, prefix):
        return self._walk(prefix) is not None
""",
    ),
    # ---- Find Median from Data Stream (LeetCode 295) ----
    dict(
        title="Find Median from Data Stream",
        diff="H",
        lc=295,
        slug="find-median-from-data-stream",
        prompt=(
            "Design a structure with add_num(num) and find_median() for a stream of integers. find_median must be "
            "fast (O(1)) and add_num O(log n)."
        ),
        sig=(
            "class MedianFinder:\n    def __init__(self):\n        pass\n    def add_num(self, num: int) -> "
            "None:\n        pass\n    def find_median(self) -> float:\n        pass"
        ),
        kind="design",
        cls="MedianFinder",
        compare="float",
        tests=[
            (
                (),
                [
                    ("add_num", [1], S),
                    ("add_num", [2], S),
                    ("find_median", [], 1.5),
                    ("add_num", [3], S),
                    ("find_median", [], 2.0),
                ],
            ),
            ((), [("add_num", [5], S), ("find_median", [], 5.0)]),
            (
                (),
                [
                    ("add_num", [-1], S),
                    ("add_num", [-2], S),
                    ("add_num", [-3], S),
                    ("add_num", [-4], S),
                    ("add_num", [-5], S),
                    ("find_median", [], -3.0),
                ],
            ),
        ],
        hints=[
            "Keeping the whole list sorted makes each insert O(n). You only need the middle one or two elements.",
            "Split the data into a lower half and an upper half. The median sits at their boundary.",
            (
                "Max-heap (negated) for the lower half, min-heap for the upper half; keep sizes equal or lower = "
                "upper + 1; rebalance after each add."
            ),
        ],
        pattern="Two heaps (max-heap of the lower half + min-heap of the upper half)",
        explain=(
            "Invariant: every element in `lo` <= every element in `hi`, and len(lo) is len(hi) or "
            "len(hi)+1.\n        Push to lo, move lo's max to hi (keeps the order invariant), then rebalance sizes. "
            "The median is lo's\n        top (odd) or the mean of both tops (even). add O(log n), median O(1)."
        ),
        cx="add O(log n), find_median O(1) (two heaps)",
        brute_cx="find_median is O(n log n) - sorts on every query",
        brute=r"""
# BRUTE FORCE: find_median is O(n log n) - sorts on every query
class MedianFinder:
    def __init__(self):
        self.a = []

    def add_num(self, num):
        self.a.append(num)

    def find_median(self):
        s = sorted(self.a)
        n = len(s)
        return float(s[n // 2]) if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
""",
        solution=r"""
# OPTIMISED: add O(log n), find_median O(1) (two heaps)
# Idea: Two heaps (max-heap of the lower half + min-heap of the upper half)
class MedianFinder:
    def __init__(self):
        self.lo = []  # max-heap via negatives: lower half
        self.hi = []  # min-heap: upper half

    def add_num(self, num):
        heapq.heappush(self.lo, -num)
        heapq.heappush(self.hi, -heapq.heappop(self.lo))  # keep lo <= hi
        if len(self.hi) > len(self.lo):
            heapq.heappush(self.lo, -heapq.heappop(self.hi))  # keep lo the bigger half

    def find_median(self):
        if len(self.lo) > len(self.hi):
            return float(-self.lo[0])
        return (-self.lo[0] + self.hi[0]) / 2
""",
    ),
]
