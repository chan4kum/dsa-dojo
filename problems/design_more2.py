"""more Design problems (batch 4) - part of the problem bank for the "design" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

from core import SKIP

S = SKIP

PROBLEMS = [
    # ---- Design HashMap (LeetCode 706) ----
    dict(
        title="Design HashMap",
        diff="E",
        lc=706,
        slug="design-hashmap",
        prompt=(
            "Implement a hash map without built-in hash tables: put(key, value), get(key) (-1 if absent) and "
            "remove(key)."
        ),
        sig=(
            "class MyHashMap:\n    def __init__(self):\n        pass\n    def put(self, key: int, value: int) -> "
            "None:\n        pass\n    def get(self, key: int) -> int:\n        pass\n    def remove(self, key: int) "
            "-> None:\n        pass"
        ),
        kind="design",
        cls="MyHashMap",
        tests=[
            (
                (),
                [
                    ("put", [1, 1], S),
                    ("put", [2, 2], S),
                    ("get", [1], 1),
                    ("get", [3], -1),
                    ("put", [2, 1], S),
                    ("get", [2], 1),
                    ("remove", [2], S),
                    ("get", [2], -1),
                ],
            ),
            ((), [("get", [5], -1), ("put", [1000000, 7], S), ("get", [1000000], 7), ("remove", [1000000], S)]),
            (
                (),
                [
                    ("put", [1, 10], S),
                    ("put", [1, 20], S),
                    ("get", [1], 20),
                    ("remove", [1], S),
                    ("remove", [1], S),
                    ("get", [1], -1),
                ],
            ),
        ],
        hints=[
            "A hash function maps a key to a bucket index: index = key % size.",
            "Different keys can land in the same bucket (a collision) - each bucket must hold several pairs.",
            (
                "Use an array of ~1000 buckets, each a small list of [key, value] pairs; scan only the one bucket "
                "for every operation."
            ),
        ],
        pattern="Hash table with separate chaining",
        explain=(
            "The modulo spreads keys over the buckets, so a lookup scans only the short chain in one bucket instead "
            "of all keys. Average O(1) while the chains stay short."
        ),
        cx="O(n / buckets) average per operation",
        brute_cx="O(n) per operation - one flat list of pairs",
        brute=r"""
# BRUTE FORCE: O(n) per operation - one flat list of pairs
class MyHashMap:
    def __init__(self):
        self.pairs = []  # every [key, value] pair in one list

    def put(self, key, value):
        for pair in self.pairs:
            if pair[0] == key:
                pair[1] = value
                return
        self.pairs.append([key, value])

    def get(self, key):
        for k, v in self.pairs:
            if k == key:
                return v
        return -1

    def remove(self, key):
        self.pairs = [p for p in self.pairs if p[0] != key]
""",
        solution=r"""
# OPTIMISED: O(n / buckets) average per operation
# Idea: Hash table with separate chaining
class MyHashMap:
    SIZE = 1009  # a prime number of buckets spreads keys evenly

    def __init__(self):
        self.buckets = [[] for _ in range(self.SIZE)]

    def put(self, key, value):
        bucket = self.buckets[key % self.SIZE]
        for pair in bucket:
            if pair[0] == key:
                pair[1] = value  # overwrite an existing key
                return
        bucket.append([key, value])

    def get(self, key):
        for k, v in self.buckets[key % self.SIZE]:
            if k == key:
                return v
        return -1

    def remove(self, key):
        bucket = self.buckets[key % self.SIZE]
        bucket[:] = [pair for pair in bucket if pair[0] != key]
""",
    ),
    # ---- Design HashSet (LeetCode 705) ----
    dict(
        title="Design HashSet",
        diff="E",
        lc=705,
        slug="design-hashset",
        prompt="Implement a set without built-in hash tables: add(key), remove(key) and contains(key).",
        sig=(
            "class MyHashSet:\n    def __init__(self):\n        pass\n    def add(self, key: int) -> None:\n        "
            "pass\n    def remove(self, key: int) -> None:\n        pass\n    def contains(self, key: int) -> "
            "bool:\n        pass"
        ),
        kind="design",
        cls="MyHashSet",
        tests=[
            (
                (),
                [
                    ("add", [1], S),
                    ("add", [2], S),
                    ("contains", [1], True),
                    ("contains", [3], False),
                    ("add", [2], S),
                    ("contains", [2], True),
                    ("remove", [2], S),
                    ("contains", [2], False),
                ],
            ),
            ((), [("remove", [9], S), ("contains", [9], False), ("add", [9], S), ("contains", [9], True)]),
            (
                (),
                [
                    ("add", [1000], S),
                    ("add", [1], S),
                    ("contains", [1000], True),
                    ("remove", [1000], S),
                    ("contains", [1000], False),
                    ("contains", [1], True),
                ],
            ),
        ],
        hints=[
            "A set is a hash map with no values.",
            "Hash the key to a bucket with key % size; keep the keys of that bucket in a list.",
            "add must not insert duplicates: check the bucket first.",
        ],
        pattern="Hash table with separate chaining (keys only)",
        explain="Same idea as the hash map: a modulo picks the bucket, and only that bucket's few keys are scanned.",
        cx="O(n / buckets) average per operation",
        brute_cx="O(n) per operation - one flat list",
        brute=r"""
# BRUTE FORCE: O(n) per operation - one flat list
class MyHashSet:
    def __init__(self):
        self.items = []

    def add(self, key):
        if key not in self.items:  # O(n) scan
            self.items.append(key)

    def remove(self, key):
        if key in self.items:
            self.items.remove(key)

    def contains(self, key):
        return key in self.items
""",
        solution=r"""
# OPTIMISED: O(n / buckets) average per operation
# Idea: Hash table with separate chaining (keys only)
class MyHashSet:
    SIZE = 1009

    def __init__(self):
        self.buckets = [[] for _ in range(self.SIZE)]

    def add(self, key):
        bucket = self.buckets[key % self.SIZE]
        if key not in bucket:
            bucket.append(key)

    def remove(self, key):
        bucket = self.buckets[key % self.SIZE]
        if key in bucket:
            bucket.remove(key)

    def contains(self, key):
        return key in self.buckets[key % self.SIZE]
""",
    ),
    # ---- Design Circular Queue (LeetCode 622) ----
    dict(
        title="Design Circular Queue",
        diff="M",
        lc=622,
        slug="design-circular-queue",
        prompt=(
            "Implement a fixed-capacity circular queue: enQueue(x) and deQueue() return whether they succeeded; "
            "Front()/Rear() return -1 when empty; isEmpty() and isFull()."
        ),
        sig=(
            "class MyCircularQueue:\n    def __init__(self, k: int):\n        pass\n    def enQueue(self, value: "
            "int) -> bool:\n        pass\n    def deQueue(self) -> bool:\n        pass\n    def Front(self) -> "
            "int:\n        pass\n    def Rear(self) -> int:\n        pass\n    def isEmpty(self) -> bool:\n        "
            "pass\n    def isFull(self) -> bool:\n        pass"
        ),
        kind="design",
        cls="MyCircularQueue",
        tests=[
            (
                (3,),
                [
                    ("enQueue", [1], True),
                    ("enQueue", [2], True),
                    ("enQueue", [3], True),
                    ("enQueue", [4], False),
                    ("Rear", [], 3),
                    ("isFull", [], True),
                    ("deQueue", [], True),
                    ("enQueue", [4], True),
                    ("Rear", [], 4),
                    ("Front", [], 2),
                ],
            ),
            (
                (1,),
                [
                    ("Front", [], -1),
                    ("Rear", [], -1),
                    ("deQueue", [], False),
                    ("isEmpty", [], True),
                    ("enQueue", [7], True),
                    ("Front", [], 7),
                ],
            ),
            (
                (2,),
                [
                    ("enQueue", [1], True),
                    ("deQueue", [], True),
                    ("enQueue", [2], True),
                    ("enQueue", [3], True),
                    ("isFull", [], True),
                    ("Front", [], 2),
                    ("Rear", [], 3),
                ],
            ),
        ],
        hints=[
            "A plain list with pop(0) is O(n) per dequeue. A ring buffer avoids moving elements.",
            "Keep a fixed array, a head index and a count. The tail position is (head + count - 1) % capacity.",
            "Enqueue writes at (head + count) % capacity; dequeue just moves head = (head + 1) % capacity.",
        ],
        pattern="Ring buffer (head index + size, indices taken modulo capacity)",
        explain=(
            "Storing the count (instead of tail) avoids the classic full-versus-empty ambiguity when head equals "
            "tail. Every operation is O(1) with no shifting."
        ),
        cx="O(1) per operation",
        brute_cx="O(n) per dequeue - list with pop(0)",
        brute=r"""
# BRUTE FORCE: O(n) per dequeue - list with pop(0)
class MyCircularQueue:
    def __init__(self, k):
        self.k, self.items = k, []

    def enQueue(self, value):
        if len(self.items) == self.k:
            return False
        self.items.append(value)
        return True

    def deQueue(self):
        if not self.items:
            return False
        self.items.pop(0)  # shifts every element: O(n)
        return True

    def Front(self):
        return self.items[0] if self.items else -1

    def Rear(self):
        return self.items[-1] if self.items else -1

    def isEmpty(self):
        return not self.items

    def isFull(self):
        return len(self.items) == self.k
""",
        solution=r"""
# OPTIMISED: O(1) per operation
# Idea: Ring buffer (head index + size, indices taken modulo capacity)
class MyCircularQueue:
    def __init__(self, k):
        self.data = [0] * k
        self.head = 0  # index of the front element
        self.count = 0

    def enQueue(self, value):
        if self.isFull():
            return False
        self.data[(self.head + self.count) % len(self.data)] = value
        self.count += 1
        return True

    def deQueue(self):
        if self.isEmpty():
            return False
        self.head = (self.head + 1) % len(self.data)
        self.count -= 1
        return True

    def Front(self):
        return -1 if self.isEmpty() else self.data[self.head]

    def Rear(self):
        return -1 if self.isEmpty() else self.data[(self.head + self.count - 1) % len(self.data)]

    def isEmpty(self):
        return self.count == 0

    def isFull(self):
        return self.count == len(self.data)
""",
    ),
    # ---- Implement Stack using Queues (LeetCode 225) ----
    dict(
        title="Implement Stack using Queues",
        diff="E",
        lc=225,
        slug="implement-stack-using-queues",
        prompt=(
            "Implement a LIFO stack (push, pop, top, empty) using only queue operations (append to the back, pop "
            "from the front, size)."
        ),
        sig=(
            "class MyStack:\n    def __init__(self):\n        pass\n    def push(self, x: int) -> None:\n        "
            "pass\n    def pop(self) -> int:\n        pass\n    def top(self) -> int:\n        pass\n    def "
            "empty(self) -> bool:\n        pass"
        ),
        kind="design",
        cls="MyStack",
        tests=[
            ((), [("push", [1], S), ("push", [2], S), ("top", [], 2), ("pop", [], 2), ("empty", [], False)]),
            (
                (),
                [
                    ("push", [5], S),
                    ("pop", [], 5),
                    ("empty", [], True),
                    ("push", [6], S),
                    ("push", [7], S),
                    ("pop", [], 7),
                    ("top", [], 6),
                ],
            ),
            (
                (),
                [
                    ("push", [1], S),
                    ("push", [2], S),
                    ("push", [3], S),
                    ("pop", [], 3),
                    ("pop", [], 2),
                    ("top", [], 1),
                    ("empty", [], False),
                ],
            ),
        ],
        hints=[
            "A queue gives the OLDEST element first; a stack needs the NEWEST.",
            "After pushing x to the back, rotate the older elements behind it so x reaches the front.",
            (
                "push: append x, then move the previous n elements from the front to the back. pop/top are then "
                "simple front operations."
            ),
        ],
        pattern="Queue rotation to reverse order",
        explain=(
            "Rotating after each push keeps the queue in stack order at all times, so pop and top are O(1) while "
            "push pays O(n)."
        ),
        cx="push O(n), pop/top/empty O(1)",
        brute_cx="pop/top O(n) - two queues, move all but the last element",
        brute=r"""
# BRUTE FORCE: pop/top O(n) - two queues, move all but the last element
class MyStack:
    def __init__(self):
        self.main, self.helper = deque(), deque()

    def push(self, x):
        self.main.append(x)

    def pop(self):
        while len(self.main) > 1:
            self.helper.append(self.main.popleft())  # move everything except the newest element
        value = self.main.popleft()
        self.main, self.helper = self.helper, self.main
        return value

    def top(self):
        value = self.pop()
        self.main.append(value)
        return value

    def empty(self):
        return not self.main
""",
        solution=r"""
# OPTIMISED: push O(n), pop/top/empty O(1)
# Idea: Queue rotation to reverse order
class MyStack:
    def __init__(self):
        self.queue = deque()

    def push(self, x):
        self.queue.append(x)
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())  # rotate so the newest value is at the front

    def pop(self):
        return self.queue.popleft()

    def top(self):
        return self.queue[0]

    def empty(self):
        return not self.queue
""",
    ),
    # ---- Online Stock Span (LeetCode 901) ----
    dict(
        title="Online Stock Span",
        diff="M",
        lc=901,
        slug="online-stock-span",
        prompt=(
            "next(price) is called once per day. Return the span: the number of consecutive days up to and "
            "including today whose price was <= today's price."
        ),
        sig=(
            "class StockSpanner:\n    def __init__(self):\n        pass\n    def next(self, price: int) -> "
            "int:\n        pass"
        ),
        kind="design",
        cls="StockSpanner",
        tests=[
            (
                (),
                [
                    ("next", [100], 1),
                    ("next", [80], 1),
                    ("next", [60], 1),
                    ("next", [70], 2),
                    ("next", [60], 1),
                    ("next", [75], 4),
                    ("next", [85], 6),
                ],
            ),
            ((), [("next", [5], 1), ("next", [5], 2), ("next", [6], 3), ("next", [1], 1)]),
            ((), [("next", [1], 1), ("next", [2], 2), ("next", [3], 3), ("next", [2], 1), ("next", [4], 5)]),
        ],
        hints=[
            "A day's span reuses the spans of the days it absorbs.",
            "Keep a stack of (price, span) with strictly decreasing prices.",
            (
                "For a new price, pop every entry with price <= it and add their spans to today's span; then push "
                "(price, span)."
            ),
        ],
        pattern="Monotonic stack that merges spans",
        explain=(
            "Each price is pushed once and popped at most once, so the amortised cost per call is O(1), even though "
            "a single call may pop many entries."
        ),
        cx="O(1) amortised per call",
        brute_cx="O(n) per call - walk back through the history",
        brute=r"""
# BRUTE FORCE: O(n) per call - walk back through the history
class StockSpanner:
    def __init__(self):
        self.prices = []

    def next(self, price):
        self.prices.append(price)
        span, i = 1, len(self.prices) - 2
        while i >= 0 and self.prices[i] <= price:  # count back while the price is not higher
            span += 1
            i -= 1
        return span
""",
        solution=r"""
# OPTIMISED: O(1) amortised per call
# Idea: Monotonic stack that merges spans
class StockSpanner:
    def __init__(self):
        self.stack = []  # (price, span) with decreasing prices

    def next(self, price):
        span = 1
        while self.stack and self.stack[-1][0] <= price:
            span += self.stack.pop()[1]  # absorb the whole earlier span in one step
        self.stack.append((price, span))
        return span
""",
    ),
    # ---- Number of Recent Calls (LeetCode 933) ----
    dict(
        title="Number of Recent Calls",
        diff="E",
        lc=933,
        slug="number-of-recent-calls",
        prompt=(
            "ping(t) records a request at time t (milliseconds; t strictly increases). Return how many requests "
            "happened in the inclusive range [t - 3000, t]."
        ),
        sig=(
            "class RecentCounter:\n    def __init__(self):\n        pass\n    def ping(self, t: int) -> "
            "int:\n        pass"
        ),
        kind="design",
        cls="RecentCounter",
        tests=[
            ((), [("ping", [1], 1), ("ping", [100], 2), ("ping", [3001], 3), ("ping", [3002], 3)]),
            ((), [("ping", [3000], 1), ("ping", [6000], 2), ("ping", [6001], 2), ("ping", [9002], 1)]),
            ((), [("ping", [10], 1), ("ping", [3010], 2), ("ping", [3011], 2), ("ping", [6011], 2)]),
        ],
        hints=[
            "Times only increase, so old requests only ever expire from the FRONT.",
            "Keep the pings in a queue.",
            (
                "On each ping append t, then pop from the front while the front is < t - 3000. The queue length is "
                "the answer."
            ),
        ],
        pattern="Sliding window over a time-ordered queue",
        explain=(
            "Because t strictly increases, once a request leaves the window it never returns, so popping from the "
            "front is enough and each request is handled once."
        ),
        cx="O(1) amortised per call",
        brute_cx="O(n) per call - count over the whole history",
        brute=r"""
# BRUTE FORCE: O(n) per call - count over the whole history
class RecentCounter:
    def __init__(self):
        self.times = []

    def ping(self, t):
        self.times.append(t)
        return sum(1 for x in self.times if t - 3000 <= x <= t)
""",
        solution=r"""
# OPTIMISED: O(1) amortised per call
# Idea: Sliding window over a time-ordered queue
class RecentCounter:
    def __init__(self):
        self.queue = deque()

    def ping(self, t):
        self.queue.append(t)
        while self.queue[0] < t - 3000:
            self.queue.popleft()  # expired request
        return len(self.queue)
""",
    ),
    # ---- Product of the Last K Numbers (LeetCode 1352) ----
    dict(
        title="Product of the Last K Numbers",
        diff="M",
        lc=1352,
        slug="product-of-the-last-k-numbers",
        prompt=(
            "add(num) appends a number to a stream. getProduct(k) returns the product of the last k numbers (the "
            "stream always has at least k numbers; the product fits in 32 bits)."
        ),
        sig=(
            "class ProductOfNumbers:\n    def __init__(self):\n        pass\n    def add(self, num: int) -> "
            "None:\n        pass\n    def getProduct(self, k: int) -> int:\n        pass"
        ),
        kind="design",
        cls="ProductOfNumbers",
        tests=[
            (
                (),
                [
                    ("add", [3], S),
                    ("add", [0], S),
                    ("add", [2], S),
                    ("add", [5], S),
                    ("add", [4], S),
                    ("getProduct", [2], 20),
                    ("getProduct", [3], 40),
                    ("getProduct", [4], 0),
                    ("add", [8], S),
                    ("getProduct", [2], 32),
                ],
            ),
            ((), [("add", [2], S), ("add", [3], S), ("getProduct", [1], 3), ("getProduct", [2], 6)]),
            (
                (),
                [
                    ("add", [0], S),
                    ("add", [4], S),
                    ("getProduct", [1], 4),
                    ("getProduct", [2], 0),
                    ("add", [5], S),
                    ("getProduct", [2], 20),
                ],
            ),
        ],
        hints=[
            "Recomputing the product of k numbers costs O(k) per query.",
            "Prefix products let you divide: product of the last k = prefix[-1] / prefix[-1-k].",
            (
                "A zero breaks division: when you add 0, reset the prefix list to [1]. If k reaches back past the "
                "reset, the answer is 0."
            ),
        ],
        pattern="Prefix products with a reset on zero",
        explain=(
            "Everything before the last zero is irrelevant for any query that stays after it, and any query that "
            "spans the zero is 0. Resetting on zero keeps division safe."
        ),
        cx="O(1) per operation",
        brute_cx="O(k) per query - multiply the last k numbers",
        brute=r"""
# BRUTE FORCE: O(k) per query - multiply the last k numbers
class ProductOfNumbers:
    def __init__(self):
        self.nums = []

    def add(self, num):
        self.nums.append(num)

    def getProduct(self, k):
        product = 1
        for x in self.nums[-k:]:
            product *= x
        return product
""",
        solution=r"""
# OPTIMISED: O(1) per operation
# Idea: Prefix products with a reset on zero
class ProductOfNumbers:
    def __init__(self):
        self.prefix = [
            1
        ]  # prefix[i] = product of the numbers since the last zero, up to the i-th one

    def add(self, num):
        if num == 0:
            self.prefix = [1]  # a zero kills every product that spans it
        else:
            self.prefix.append(self.prefix[-1] * num)

    def getProduct(self, k):
        if k >= len(self.prefix):
            return 0  # the window reaches back past the last zero
        return self.prefix[-1] // self.prefix[-1 - k]
""",
    ),
    # ---- Peeking Iterator (LeetCode 284) ----
    dict(
        title="Peeking Iterator",
        diff="M",
        lc=284,
        slug="peeking-iterator",
        prompt=(
            "Wrap a list iterator so it also supports peek() (look at the next value without consuming it). "
            "Implement next(), peek() and hasNext()."
        ),
        sig=(
            "class PeekingIterator:\n    def __init__(self, nums: List[int]):\n        pass\n    def peek(self) -> "
            "int:\n        pass\n    def next(self) -> int:\n        pass\n    def hasNext(self) -> bool:\n        "
            "pass"
        ),
        kind="design",
        cls="PeekingIterator",
        tests=[
            (
                ([1, 2, 3],),
                [("next", [], 1), ("peek", [], 2), ("next", [], 2), ("next", [], 3), ("hasNext", [], False)],
            ),
            (
                ([5],),
                [("peek", [], 5), ("peek", [], 5), ("hasNext", [], True), ("next", [], 5), ("hasNext", [], False)],
            ),
            (
                ([7, 8],),
                [("hasNext", [], True), ("peek", [], 7), ("next", [], 7), ("next", [], 8), ("hasNext", [], False)],
            ),
        ],
        hints=[
            "A normal iterator can only move forward, so peeking would consume the value.",
            "Keep one value of look-ahead in a variable.",
            "peek returns the cached value; next returns it and refills the cache from the underlying iterator.",
        ],
        pattern="One-element look-ahead buffer",
        explain=(
            "Caching exactly one upcoming value separates 'look' from 'consume' without copying the whole sequence."
        ),
        cx="O(1) per operation, O(1) extra space",
        brute_cx="O(n) extra space - copy every value into a list up front",
        brute=r"""
# BRUTE FORCE: O(n) extra space - copy every value into a list up front
class PeekingIterator:
    def __init__(self, nums):
        self.items = list(nums)  # copy everything
        self.pos = 0

    def peek(self):
        return self.items[self.pos]

    def next(self):
        value = self.items[self.pos]
        self.pos += 1
        return value

    def hasNext(self):
        return self.pos < len(self.items)
""",
        solution=r"""
# OPTIMISED: O(1) per operation, O(1) extra space
# Idea: One-element look-ahead buffer
class PeekingIterator:
    _END = object()  # marks "no more values"

    def __init__(self, nums):
        self.it = iter(nums)
        self.cached = next(self.it, self._END)  # one value of look-ahead

    def peek(self):
        return self.cached

    def next(self):
        value = self.cached
        self.cached = next(self.it, self._END)
        return value

    def hasNext(self):
        return self.cached is not self._END
""",
    ),
    # ---- Range Sum Query - Immutable (LeetCode 303) ----
    dict(
        title="Range Sum Query - Immutable",
        diff="E",
        lc=303,
        slug="range-sum-query-immutable",
        prompt=(
            "Given an array, answer many sumRange(left, right) queries (inclusive) quickly. The array never changes."
        ),
        sig=(
            "class NumArray:\n    def __init__(self, nums: List[int]):\n        pass\n    def sumRange(self, left: "
            "int, right: int) -> int:\n        pass"
        ),
        kind="design",
        cls="NumArray",
        tests=[
            (([-2, 0, 3, -5, 2, -1],), [("sumRange", [0, 2], 1), ("sumRange", [2, 5], -1), ("sumRange", [0, 5], -3)]),
            (([4],), [("sumRange", [0, 0], 4)]),
            (([1, 2, 3, 4],), [("sumRange", [1, 2], 5), ("sumRange", [0, 3], 10), ("sumRange", [3, 3], 4)]),
        ],
        hints=[
            "Summing a slice for every query costs O(n) each.",
            "Precompute prefix[i] = sum of the first i numbers.",
            "sumRange(l, r) = prefix[r + 1] - prefix[l].",
        ],
        pattern="Prefix sums",
        explain=(
            "Preprocessing pays O(n) once so that every query is a subtraction. This is the foundation of Subarray "
            "Sum Equals K and the 2-D version below."
        ),
        cx="O(n) build, O(1) per query",
        brute_cx="O(n) per query - sum the slice",
        brute=r"""
# BRUTE FORCE: O(n) per query - sum the slice
class NumArray:
    def __init__(self, nums):
        self.nums = list(nums)

    def sumRange(self, left, right):
        return sum(self.nums[left : right + 1])
""",
        solution=r"""
# OPTIMISED: O(n) build, O(1) per query
# Idea: Prefix sums
class NumArray:
    def __init__(self, nums):
        self.prefix = [0]  # prefix[i] = sum of nums[:i]
        for x in nums:
            self.prefix.append(self.prefix[-1] + x)

    def sumRange(self, left, right):
        return self.prefix[right + 1] - self.prefix[left]
""",
    ),
    # ---- Range Sum Query 2D - Immutable (LeetCode 304) ----
    dict(
        title="Range Sum Query 2D - Immutable",
        diff="M",
        lc=304,
        slug="range-sum-query-2d-immutable",
        prompt=(
            "Given a matrix, answer many sumRegion(row1, col1, row2, col2) queries (sum of the inclusive rectangle) "
            "quickly. The matrix never changes."
        ),
        sig=(
            "class NumMatrix:\n    def __init__(self, matrix: List[List[int]]):\n        pass\n    def "
            "sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:\n        pass"
        ),
        kind="design",
        cls="NumMatrix",
        tests=[
            (
                ([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]],),
                [("sumRegion", [2, 1, 4, 3], 8), ("sumRegion", [1, 1, 2, 2], 11), ("sumRegion", [1, 2, 2, 4], 12)],
            ),
            (([[7]],), [("sumRegion", [0, 0, 0, 0], 7)]),
            (
                ([[1, 2], [3, 4]],),
                [("sumRegion", [0, 0, 1, 1], 10), ("sumRegion", [0, 1, 1, 1], 6), ("sumRegion", [1, 0, 1, 0], 3)],
            ),
        ],
        hints=[
            "Summing the rectangle cell by cell costs O(area) per query.",
            "Let prefix[r][c] = sum of the rectangle from (0, 0) to (r - 1, c - 1).",
            "Inclusion-exclusion: sum = P[r2+1][c2+1] - P[r1][c2+1] - P[r2+1][c1] + P[r1][c1].",
        ],
        pattern="2-D prefix sums (inclusion-exclusion)",
        explain=(
            "Subtracting the two strips above and to the left removes the corner twice, so we add it back once. "
            "Each query is four lookups."
        ),
        cx="O(m*n) build, O(1) per query",
        brute_cx="O(area) per query - add up every cell",
        brute=r"""
# BRUTE FORCE: O(area) per query - add up every cell
class NumMatrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def sumRegion(self, row1, col1, row2, col2):
        return sum(sum(row[col1 : col2 + 1]) for row in self.matrix[row1 : row2 + 1])
""",
        solution=r"""
# OPTIMISED: O(m*n) build, O(1) per query
# Idea: 2-D prefix sums (inclusion-exclusion)
class NumMatrix:
    def __init__(self, matrix):
        rows, cols = len(matrix), len(matrix[0])
        self.p = [[0] * (cols + 1) for _ in range(rows + 1)]
        for r in range(rows):
            for c in range(cols):
                self.p[r + 1][c + 1] = (
                    self.p[r][c + 1] + self.p[r + 1][c] - self.p[r][c] + matrix[r][c]
                )

    def sumRegion(self, row1, col1, row2, col2):
        p = self.p
        return p[row2 + 1][col2 + 1] - p[row1][col2 + 1] - p[row2 + 1][col1] + p[row1][col1]
""",
    ),
]
