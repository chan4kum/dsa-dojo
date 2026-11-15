"""more Design problems (batch 5) - part of the problem bank for the "design" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
Design problems are classes: tests are (constructor args, [(method, args, expected)]); S means "do not check
this return value" (for methods that return nothing or something random).
"""

from core import SKIP

S = SKIP

PROBLEMS = [
    # ---- Insert Delete GetRandom O(1) (LeetCode 380) ----
    dict(
        title="Insert Delete GetRandom O(1)",
        diff="M",
        lc=380,
        slug="insert-delete-getrandom-o1",
        prompt=(
            "Implement RandomizedSet: insert(val) -> True if it was absent, remove(val) -> True if it was present, "
            "getRandom() -> a random element, each element equally likely. All in average O(1)."
        ),
        sig=(
            "class RandomizedSet:\n    def __init__(self):\n        pass\n    def insert(self, val: int) -> "
            "bool:\n        pass\n    def remove(self, val: int) -> bool:\n        pass\n    def getRandom(self) -> "
            "int:\n        pass"
        ),
        kind="design",
        cls="RandomizedSet",
        tests=[
            (
                (),
                [
                    ("insert", [1], True),
                    ("remove", [2], False),
                    ("insert", [2], True),
                    ("getRandom", [], S),
                    ("remove", [1], True),
                    ("insert", [2], False),
                    ("getRandom", [], 2),
                ],
            ),
            (
                (),
                [
                    ("insert", [5], True),
                    ("insert", [5], False),
                    ("remove", [5], True),
                    ("remove", [5], False),
                    ("insert", [7], True),
                    ("getRandom", [], 7),
                ],
            ),
            (
                (),
                [
                    ("remove", [3], False),
                    ("insert", [3], True),
                    ("getRandom", [], 3),
                    ("remove", [3], True),
                    ("insert", [3], True),
                ],
            ),
        ],
        hints=[
            "A set gives O(1) insert and remove, but you cannot pick a random element from it in O(1).",
            "A list gives O(1) random access, but removing from the middle is O(n).",
            (
                "Keep BOTH: a list of values plus a dict value -> index. To remove, swap the element with the last "
                "one, pop the end and fix the dict."
            ),
        ],
        pattern="Array + hash map with swap-with-last deletion",
        explain=(
            "Deleting the LAST list element is O(1), so we move the victim there first. The dict always knows where "
            "each value lives, which makes the swap and the membership test O(1)."
        ),
        cx="O(1) average per operation",
        brute_cx="O(n) for remove - searching and deleting inside a plain list",
        brute=r"""
# BRUTE FORCE: O(n) for remove - searching and deleting inside a plain list
class RandomizedSet:
    def __init__(self):
        self.items = []

    def insert(self, val):
        if val in self.items:  # linear scan
            return False
        self.items.append(val)
        return True

    def remove(self, val):
        if val not in self.items:
            return False
        self.items.remove(val)  # linear scan + shift
        return True

    def getRandom(self):
        return random.choice(self.items)
""",
        solution=r"""
# OPTIMISED: O(1) average per operation
# Idea: Array + hash map with swap-with-last deletion
class RandomizedSet:
    def __init__(self):
        self.items = []
        self.index = {}  # value -> position in self.items

    def insert(self, val):
        if val in self.index:
            return False
        self.index[val] = len(self.items)
        self.items.append(val)
        return True

    def remove(self, val):
        if val not in self.index:
            return False
        pos, last = self.index[val], self.items[-1]
        self.items[pos] = last  # overwrite the victim with the last value
        self.index[last] = pos
        self.items.pop()  # O(1) removal from the end
        del self.index[val]
        return True

    def getRandom(self):
        return random.choice(self.items)
""",
    ),
    # ---- Design Circular Deque (LeetCode 641) ----
    dict(
        title="Design Circular Deque",
        diff="M",
        lc=641,
        slug="design-circular-deque",
        prompt=(
            "Implement a fixed-capacity double-ended queue MyCircularDeque(k) with insertFront, insertLast (True if "
            "done), deleteFront, deleteLast (True if done), getFront, getRear (-1 if empty), isEmpty and isFull."
        ),
        sig=(
            "class MyCircularDeque:\n    def __init__(self, k: int):\n        pass\n    def insertFront(self, "
            "value: int) -> bool:\n        pass\n    def insertLast(self, value: int) -> bool:\n        pass\n    "
            "def deleteFront(self) -> bool:\n        pass\n    def deleteLast(self) -> bool:\n        pass\n    def "
            "getFront(self) -> int:\n        pass\n    def getRear(self) -> int:\n        pass\n    def "
            "isEmpty(self) -> bool:\n        pass\n    def isFull(self) -> bool:\n        pass"
        ),
        kind="design",
        cls="MyCircularDeque",
        tests=[
            (
                (3,),
                [
                    ("insertLast", [1], True),
                    ("insertLast", [2], True),
                    ("insertFront", [3], True),
                    ("insertFront", [4], False),
                    ("getRear", [], 2),
                    ("isFull", [], True),
                    ("deleteLast", [], True),
                    ("insertFront", [4], True),
                    ("getFront", [], 4),
                ],
            ),
            (
                (1,),
                [
                    ("isEmpty", [], True),
                    ("insertFront", [7], True),
                    ("isFull", [], True),
                    ("insertLast", [8], False),
                    ("getFront", [], 7),
                    ("getRear", [], 7),
                    ("deleteFront", [], True),
                    ("isEmpty", [], True),
                    ("getFront", [], -1),
                    ("deleteLast", [], False),
                ],
            ),
            (
                (2,),
                [
                    ("insertLast", [1], True),
                    ("insertFront", [2], True),
                    ("deleteFront", [], True),
                    ("getFront", [], 1),
                    ("deleteFront", [], True),
                    ("deleteFront", [], False),
                    ("getRear", [], -1),
                ],
            ),
        ],
        hints=[
            "Allocate an array of exactly k slots and remember how many are used.",
            "Keep a `front` index. The rear slot is (front + size - 1) % k.",
            (
                "insertFront moves front one step back (mod k); deleteFront moves it one step forward; size tracks "
                "full/empty."
            ),
        ],
        pattern="Circular buffer with modular indexing",
        explain=(
            "Modulo arithmetic lets both ends wrap around the array, so every operation touches one slot and "
            "updates two integers - no shifting of elements."
        ),
        cx="O(1) per operation, O(k) space",
        brute_cx="O(k) per operation at the front - a Python list with insert(0, x) / pop(0)",
        brute=r"""
# BRUTE FORCE: O(k) per operation at the front - a Python list with insert(0, x) / pop(0)
class MyCircularDeque:
    def __init__(self, k):
        self.k = k
        self.items = []

    def insertFront(self, value):
        if len(self.items) == self.k:
            return False
        self.items.insert(0, value)  # shifts every element
        return True

    def insertLast(self, value):
        if len(self.items) == self.k:
            return False
        self.items.append(value)
        return True

    def deleteFront(self):
        if not self.items:
            return False
        self.items.pop(0)
        return True

    def deleteLast(self):
        if not self.items:
            return False
        self.items.pop()
        return True

    def getFront(self):
        return self.items[0] if self.items else -1

    def getRear(self):
        return self.items[-1] if self.items else -1

    def isEmpty(self):
        return not self.items

    def isFull(self):
        return len(self.items) == self.k
""",
        solution=r"""
# OPTIMISED: O(1) per operation, O(k) space
# Idea: Circular buffer with modular indexing
class MyCircularDeque:
    def __init__(self, k):
        self.k = k
        self.data = [0] * k
        self.front = 0  # index of the first element
        self.size = 0

    def insertFront(self, value):
        if self.isFull():
            return False
        self.front = (self.front - 1) % self.k  # step back, wrapping around
        self.data[self.front] = value
        self.size += 1
        return True

    def insertLast(self, value):
        if self.isFull():
            return False
        self.data[(self.front + self.size) % self.k] = value  # first free slot after the rear
        self.size += 1
        return True

    def deleteFront(self):
        if self.isEmpty():
            return False
        self.front = (self.front + 1) % self.k
        self.size -= 1
        return True

    def deleteLast(self):
        if self.isEmpty():
            return False
        self.size -= 1
        return True

    def getFront(self):
        return -1 if self.isEmpty() else self.data[self.front]

    def getRear(self):
        return -1 if self.isEmpty() else self.data[(self.front + self.size - 1) % self.k]

    def isEmpty(self):
        return self.size == 0

    def isFull(self):
        return self.size == self.k
""",
    ),
    # ---- Snapshot Array (LeetCode 1146) ----
    dict(
        title="Snapshot Array",
        diff="M",
        lc=1146,
        slug="snapshot-array",
        prompt=(
            "SnapshotArray(length) starts with zeros. set(index, val) changes a cell, snap() freezes the array and "
            "returns the snapshot id (0, 1, 2, ...), get(index, snap_id) returns the cell's value at that snapshot."
        ),
        sig=(
            "class SnapshotArray:\n    def __init__(self, length: int):\n        pass\n    def set(self, index: "
            "int, val: int) -> None:\n        pass\n    def snap(self) -> int:\n        pass\n    def get(self, "
            "index: int, snap_id: int) -> int:\n        pass"
        ),
        kind="design",
        cls="SnapshotArray",
        tests=[
            (
                (3,),
                [("set", [0, 5], S), ("snap", [], 0), ("set", [0, 6], S), ("get", [0, 0], 5)],
            ),
            (
                (2,),
                [
                    ("snap", [], 0),
                    ("set", [1, 4], S),
                    ("snap", [], 1),
                    ("set", [1, 9], S),
                    ("snap", [], 2),
                    ("get", [1, 0], 0),
                    ("get", [1, 1], 4),
                    ("get", [1, 2], 9),
                    ("get", [0, 2], 0),
                ],
            ),
            (
                (1,),
                [
                    ("set", [0, 1], S),
                    ("set", [0, 2], S),
                    ("snap", [], 0),
                    ("get", [0, 0], 2),
                    ("snap", [], 1),
                    ("get", [0, 1], 2),
                ],
            ),
        ],
        hints=[
            "Copying the whole array on every snap() wastes memory when few cells change.",
            "Per index, store only the CHANGES as (snap_id, value) pairs, in increasing snap_id order.",
            (
                "get(index, snap_id): binary search that index's history for the last change with id <= snap_id "
                "(default 0)."
            ),
        ],
        pattern="Versioned storage: per-key change log + binary search",
        explain=(
            "Only cells that were written cost memory, and each lookup is a bisect over that cell's short history "
            "instead of a copy of the whole array."
        ),
        cx="set O(1) amortised, snap O(1), get O(log h) where h = writes to that cell",
        brute_cx="snap O(n) time and space - copy the entire array each time",
        brute=r"""
# BRUTE FORCE: snap O(n) time and space - copy the entire array each time
class SnapshotArray:
    def __init__(self, length):
        self.current = [0] * length
        self.snapshots = []

    def set(self, index, val):
        self.current[index] = val

    def snap(self):
        self.snapshots.append(self.current[:])  # full copy
        return len(self.snapshots) - 1

    def get(self, index, snap_id):
        return self.snapshots[snap_id][index]
""",
        solution=r"""
# OPTIMISED: set O(1) amortised, snap O(1), get O(log h) where h = writes to that cell
# Idea: Versioned storage: per-key change log + binary search
class SnapshotArray:
    def __init__(self, length):
        self.history = [
            [(0, 0)] for _ in range(length)
        ]  # per cell: (snap_id, value), sorted by snap_id
        self.snap_id = 0

    def set(self, index, val):
        log = self.history[index]
        if log[-1][0] == self.snap_id:
            log[-1] = (self.snap_id, val)  # overwrite a write made in the same snapshot period
        else:
            log.append((self.snap_id, val))

    def snap(self):
        self.snap_id += 1
        return self.snap_id - 1

    def get(self, index, snap_id):
        log = self.history[index]
        pos = (
            bisect.bisect_right(log, (snap_id, float("inf"))) - 1
        )  # last change with id <= snap_id
        return log[pos][1]
""",
    ),
    # ---- Design Linked List (LeetCode 707) ----
    dict(
        title="Design Linked List",
        diff="M",
        lc=707,
        slug="design-linked-list",
        prompt=(
            "Implement a singly linked list MyLinkedList with get(index) (-1 if invalid), addAtHead(val), "
            "addAtTail(val), addAtIndex(index, val) (does nothing if index > length) and deleteAtIndex(index) (does "
            "nothing if invalid)."
        ),
        sig=(
            "class MyLinkedList:\n    def __init__(self):\n        pass\n    def get(self, index: int) -> "
            "int:\n        pass\n    def addAtHead(self, val: int) -> None:\n        pass\n    def addAtTail(self, "
            "val: int) -> None:\n        pass\n    def addAtIndex(self, index: int, val: int) -> None:\n        "
            "pass\n    def deleteAtIndex(self, index: int) -> None:\n        pass"
        ),
        kind="design",
        cls="MyLinkedList",
        tests=[
            (
                (),
                [
                    ("addAtHead", [1], S),
                    ("addAtTail", [3], S),
                    ("addAtIndex", [1, 2], S),
                    ("get", [1], 2),
                    ("deleteAtIndex", [1], S),
                    ("get", [1], 3),
                ],
            ),
            (
                (),
                [
                    ("get", [0], -1),
                    ("addAtIndex", [1, 5], S),
                    ("addAtIndex", [0, 5], S),
                    ("get", [0], 5),
                    ("addAtIndex", [1, 6], S),
                    ("get", [1], 6),
                    ("deleteAtIndex", [5], S),
                    ("deleteAtIndex", [0], S),
                    ("get", [0], 6),
                ],
            ),
            (
                (),
                [
                    ("addAtTail", [4], S),
                    ("addAtHead", [3], S),
                    ("addAtIndex", [2, 9], S),
                    ("get", [2], 9),
                    ("deleteAtIndex", [2], S),
                    ("get", [2], -1),
                ],
            ),
        ],
        hints=[
            "Use a dummy head node so inserting or deleting at position 0 is not a special case.",
            "To act at index i, walk i steps from the dummy to reach the node BEFORE position i.",
            (
                "Insert: new.next = prev.next; prev.next = new. Delete: prev.next = prev.next.next. Track the size "
                "to validate indexes."
            ),
        ],
        pattern="Singly linked list with a sentinel (dummy) node",
        explain=(
            "The sentinel gives every real node a predecessor, so one uniform splice handles head, middle and tail."
        ),
        cx="O(n) for index operations, O(1) for addAtHead",
        brute_cx="O(n) per index operation - Python list with insert / pop",
        brute=r"""
# BRUTE FORCE: O(n) per index operation - Python list with insert / pop
class MyLinkedList:
    def __init__(self):
        self.items = []

    def get(self, index):
        return self.items[index] if 0 <= index < len(self.items) else -1

    def addAtHead(self, val):
        self.items.insert(0, val)

    def addAtTail(self, val):
        self.items.append(val)

    def addAtIndex(self, index, val):
        if 0 <= index <= len(self.items):
            self.items.insert(index, val)

    def deleteAtIndex(self, index):
        if 0 <= index < len(self.items):
            self.items.pop(index)
""",
        solution=r"""
# OPTIMISED: O(n) for index operations, O(1) for addAtHead
# Idea: Singly linked list with a sentinel (dummy) node
class MyLinkedList:
    class _Node:
        def __init__(self, val=0, nxt=None):
            self.val, self.next = val, nxt

    def __init__(self):
        self.dummy = self._Node()
        self.size = 0

    def _before(self, index):  # the node just before position `index`
        node = self.dummy
        for _ in range(index):
            node = node.next
        return node

    def get(self, index):
        if not 0 <= index < self.size:
            return -1
        return self._before(index).next.val

    def addAtHead(self, val):
        self.addAtIndex(0, val)

    def addAtTail(self, val):
        self.addAtIndex(self.size, val)

    def addAtIndex(self, index, val):
        if not 0 <= index <= self.size:
            return
        prev = self._before(index)
        prev.next = self._Node(val, prev.next)  # splice the new node in
        self.size += 1

    def deleteAtIndex(self, index):
        if not 0 <= index < self.size:
            return
        prev = self._before(index)
        prev.next = prev.next.next  # unlink the victim
        self.size -= 1
""",
    ),
    # ---- Design Front Middle Back Queue (LeetCode 1670) ----
    dict(
        title="Design Front Middle Back Queue",
        diff="M",
        lc=1670,
        slug="design-front-middle-back-queue",
        prompt=(
            "Implement FrontMiddleBackQueue with pushFront, pushMiddle, pushBack and popFront, popMiddle, popBack "
            "(-1 if empty). For an even number of elements the 'middle' is the FRONT one of the two middle "
            "positions when popping; pushMiddle inserts at index len // 2."
        ),
        sig=(
            "class FrontMiddleBackQueue:\n    def __init__(self):\n        pass\n    def pushFront(self, val: int) "
            "-> None:\n        pass\n    def pushMiddle(self, val: int) -> None:\n        pass\n    def "
            "pushBack(self, val: int) -> None:\n        pass\n    def popFront(self) -> int:\n        pass\n    def "
            "popMiddle(self) -> int:\n        pass\n    def popBack(self) -> int:\n        pass"
        ),
        kind="design",
        cls="FrontMiddleBackQueue",
        tests=[
            (
                (),
                [
                    ("pushFront", [1], S),
                    ("pushBack", [2], S),
                    ("pushMiddle", [3], S),
                    ("pushMiddle", [4], S),
                    ("popFront", [], 1),
                    ("popMiddle", [], 3),
                    ("popMiddle", [], 4),
                    ("popBack", [], 2),
                    ("popFront", [], -1),
                ],
            ),
            (
                (),
                [
                    ("pushMiddle", [1], S),
                    ("pushMiddle", [2], S),
                    ("pushMiddle", [3], S),
                    ("pushMiddle", [4], S),
                    ("popMiddle", [], 4),
                    ("popMiddle", [], 3),
                    ("popBack", [], 1),
                    ("popFront", [], 2),
                    ("popMiddle", [], -1),
                ],
            ),
            (
                (),
                [
                    ("pushBack", [1], S),
                    ("pushBack", [2], S),
                    ("pushBack", [3], S),
                    ("popMiddle", [], 2),
                    ("popBack", [], 3),
                    ("popFront", [], 1),
                    ("popBack", [], -1),
                ],
            ),
        ],
        hints=[
            (
                "Operations at three positions of a sequence: a plain list makes the middle O(1) to find but O(n) "
                "to change."
            ),
            (
                "Split the queue into two deques, `left` (front half) and `right` (back half), so the middle is "
                "where they meet."
            ),
            (
                "Keep len(left) <= len(right) <= len(left) + 1 and rebalance by moving one element across after "
                "every operation."
            ),
        ],
        pattern="Two deques meeting in the middle",
        explain=(
            "Each end of the structure and the middle are all at the boundary of some deque, so every operation is "
            "one deque call plus at most one rebalancing move."
        ),
        cx="O(1) per operation",
        brute_cx="O(n) per operation - a plain list with insert and pop at arbitrary positions",
        brute=r"""
# BRUTE FORCE: O(n) per operation - a plain list with insert and pop at arbitrary positions
class FrontMiddleBackQueue:
    def __init__(self):
        self.items = []

    def pushFront(self, val):
        self.items.insert(0, val)

    def pushMiddle(self, val):
        self.items.insert(len(self.items) // 2, val)

    def pushBack(self, val):
        self.items.append(val)

    def popFront(self):
        return self.items.pop(0) if self.items else -1

    def popMiddle(self):
        return self.items.pop((len(self.items) - 1) // 2) if self.items else -1

    def popBack(self):
        return self.items.pop() if self.items else -1
""",
        solution=r"""
# OPTIMISED: O(1) per operation
# Idea: Two deques meeting in the middle
class FrontMiddleBackQueue:
    def __init__(self):
        self.left, self.right = (
            deque(),
            deque(),
        )  # invariant: len(left) <= len(right) <= len(left) + 1

    def _rebalance(self):
        while len(self.left) > len(self.right):
            self.right.appendleft(self.left.pop())
        while len(self.right) > len(self.left) + 1:
            self.left.append(self.right.popleft())

    def pushFront(self, val):
        self.left.appendleft(val)
        self._rebalance()

    def pushMiddle(self, val):
        if len(self.left) == len(self.right):
            self.left.append(val)  # lands at index len // 2 after rebalancing
        else:
            self.right.appendleft(val)
        self._rebalance()

    def pushBack(self, val):
        self.right.append(val)
        self._rebalance()

    def popFront(self):
        if not self.right:
            return -1
        val = self.left.popleft() if self.left else self.right.popleft()
        self._rebalance()
        return val

    def popMiddle(self):
        if not self.right:
            return -1
        # middle index is (n - 1) // 2: last of left when the sizes are equal, else first of right
        val = self.left.pop() if len(self.left) == len(self.right) else self.right.popleft()
        self._rebalance()
        return val

    def popBack(self):
        if not self.right:
            return -1
        val = self.right.pop()
        self._rebalance()
        return val
""",
    ),
    # ---- LFU Cache (LeetCode 460) ----
    dict(
        title="LFU Cache",
        diff="H",
        lc=460,
        slug="lfu-cache",
        prompt=(
            "Implement LFUCache(capacity) with get(key) (-1 if absent) and put(key, value). When full, put evicts "
            "the least FREQUENTLY used key; ties are broken by evicting the least RECENTLY used among them. get and "
            "put both count as a use. Capacity 0 stores nothing. Aim for O(1) operations."
        ),
        sig=(
            "class LFUCache:\n    def __init__(self, capacity: int):\n        pass\n    def get(self, key: int) -> "
            "int:\n        pass\n    def put(self, key: int, value: int) -> None:\n        pass"
        ),
        kind="design",
        cls="LFUCache",
        tests=[
            (
                (2,),
                [
                    ("put", [1, 1], S),
                    ("put", [2, 2], S),
                    ("get", [1], 1),
                    ("put", [3, 3], S),
                    ("get", [2], -1),
                    ("get", [3], 3),
                    ("put", [4, 4], S),
                    ("get", [1], -1),
                    ("get", [3], 3),
                    ("get", [4], 4),
                ],
            ),
            ((0,), [("put", [0, 0], S), ("get", [0], -1), ("put", [1, 1], S), ("get", [1], -1)]),
            (
                (1,),
                [
                    ("put", [1, 10], S),
                    ("put", [2, 20], S),
                    ("get", [1], -1),
                    ("get", [2], 20),
                    ("put", [2, 30], S),
                    ("get", [2], 30),
                ],
            ),
            (
                (2,),
                [
                    ("put", [1, 1], S),
                    ("put", [2, 2], S),
                    ("put", [1, 5], S),
                    ("put", [3, 3], S),
                    ("get", [2], -1),
                    ("get", [1], 5),
                    ("get", [3], 3),
                ],
            ),
        ],
        hints=[
            "Each key needs a value, a use-count and a 'last used' stamp.",
            "Brute force: on eviction scan all keys for the smallest (count, last used). That is O(capacity) per put.",
            (
                "For O(1): map frequency -> OrderedDict of keys (oldest first), and track min_freq; a use moves a "
                "key to the next frequency's dict."
            ),
        ],
        pattern="Frequency buckets of LRU-ordered keys + min-frequency pointer",
        explain=(
            "Every key lives in the bucket for its use-count, ordered by recency. The eviction victim is the oldest "
            "key in the min_freq bucket. min_freq only resets to 1 on insertion, or moves up by one when its bucket "
            "empties."
        ),
        cx="O(1) per operation",
        brute_cx="O(capacity) per eviction - scan every key",
        brute=r"""
# BRUTE FORCE: O(capacity) per eviction - scan every key
class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.clock = 0
        self.data = {}  # key -> [value, use count, last-used time]

    def _touch(self, key):
        self.clock += 1
        self.data[key][1] += 1
        self.data[key][2] = self.clock

    def get(self, key):
        if key not in self.data:
            return -1
        self._touch(key)
        return self.data[key][0]

    def put(self, key, value):
        if self.capacity == 0:
            return
        if key in self.data:
            self.data[key][0] = value
            self._touch(key)
            return
        if len(self.data) == self.capacity:
            victim = min(self.data, key=lambda k: (self.data[k][1], self.data[k][2]))
            del self.data[victim]
        self.clock += 1
        self.data[key] = [value, 1, self.clock]
""",
        solution=r"""
# OPTIMISED: O(1) per operation
# Idea: Frequency buckets of LRU-ordered keys + min-frequency pointer
class LFUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.values = {}  # key -> value
        self.freq = {}  # key -> use count
        self.buckets = defaultdict(OrderedDict)  # count -> keys in LRU order (oldest first)
        self.min_freq = 0

    def _use(self, key):
        f = self.freq[key]
        del self.buckets[f][key]
        if not self.buckets[f]:
            del self.buckets[f]
            if self.min_freq == f:
                self.min_freq += 1  # the smallest bucket just emptied
        self.freq[key] = f + 1
        self.buckets[f + 1][key] = None

    def get(self, key):
        if key not in self.values:
            return -1
        self._use(key)
        return self.values[key]

    def put(self, key, value):
        if self.capacity == 0:
            return
        if key in self.values:
            self.values[key] = value
            self._use(key)
            return
        if len(self.values) == self.capacity:
            victim, _ = self.buckets[self.min_freq].popitem(
                last=False
            )  # least recent among the least frequent
            if not self.buckets[self.min_freq]:
                del self.buckets[self.min_freq]
            del self.values[victim], self.freq[victim]
        self.values[key] = value
        self.freq[key] = 1
        self.buckets[1][key] = None
        self.min_freq = 1
""",
    ),
    # ---- Design Authentication Manager (LeetCode 1797) ----
    dict(
        title="Design Authentication Manager",
        diff="M",
        lc=1797,
        slug="design-authentication-manager",
        prompt=(
            "AuthenticationManager(timeToLive): generate(tokenId, currentTime) creates a token expiring at "
            "currentTime + timeToLive; renew(tokenId, currentTime) resets the expiry only if the token is still "
            "unexpired; countUnexpiredTokens(currentTime) counts tokens with expiry > currentTime. A token expiring "
            "at time t is already expired at t. Call times strictly increase."
        ),
        sig=(
            "class AuthenticationManager:\n    def __init__(self, timeToLive: int):\n        pass\n    def "
            "generate(self, tokenId: str, currentTime: int) -> None:\n        pass\n    def renew(self, tokenId: "
            "str, currentTime: int) -> None:\n        pass\n    def countUnexpiredTokens(self, currentTime: int) -> "
            "int:\n        pass"
        ),
        kind="design",
        cls="AuthenticationManager",
        tests=[
            (
                (5,),
                [
                    ("generate", ["aaa", 2], S),
                    ("countUnexpiredTokens", [6], 1),
                    ("generate", ["bbb", 7], S),
                    ("renew", ["aaa", 8], S),
                    ("renew", ["bbb", 10], S),
                    ("countUnexpiredTokens", [15], 0),
                ],
            ),
            (
                (3,),
                [
                    ("generate", ["a", 1], S),
                    ("generate", ["b", 2], S),
                    ("countUnexpiredTokens", [3], 2),
                    ("renew", ["b", 4], S),
                    ("renew", ["a", 5], S),
                    ("countUnexpiredTokens", [6], 1),
                    ("countUnexpiredTokens", [7], 0),
                ],
            ),
            (
                (10,),
                [
                    ("generate", ["x", 0], S),
                    ("generate", ["y", 1], S),
                    ("renew", ["x", 5], S),
                    ("countUnexpiredTokens", [11], 1),
                    ("countUnexpiredTokens", [14], 1),
                    ("countUnexpiredTokens", [15], 0),
                ],
            ),
        ],
        hints=[
            "Store each token's expiry time in a dictionary.",
            "Counting = how many expiry times are strictly greater than currentTime. Scanning everything is O(n).",
            (
                "Times only increase, so an OrderedDict kept in expiry order lets you pop expired tokens from the "
                "front and just return its length."
            ),
        ],
        pattern="Hash map ordered by expiry + lazy eviction",
        explain=(
            "generate and renew always assign the LATEST expiry, so moving the token to the end of an OrderedDict "
            "keeps it sorted. Expired tokens collect at the front and are deleted once, giving amortised O(1)."
        ),
        cx="O(1) amortised per operation",
        brute_cx="O(n) per countUnexpiredTokens - scan every token",
        brute=r"""
# BRUTE FORCE: O(n) per countUnexpiredTokens - scan every token
class AuthenticationManager:
    def __init__(self, timeToLive):
        self.ttl = timeToLive
        self.expiry = {}

    def generate(self, tokenId, currentTime):
        self.expiry[tokenId] = currentTime + self.ttl

    def renew(self, tokenId, currentTime):
        if tokenId in self.expiry and self.expiry[tokenId] > currentTime:
            self.expiry[tokenId] = currentTime + self.ttl

    def countUnexpiredTokens(self, currentTime):
        return sum(1 for t in self.expiry.values() if t > currentTime)
""",
        solution=r"""
# OPTIMISED: O(1) amortised per operation
# Idea: Hash map ordered by expiry + lazy eviction
class AuthenticationManager:
    def __init__(self, timeToLive):
        self.ttl = timeToLive
        self.expiry = OrderedDict()  # tokenId -> expiry time, oldest expiry first

    def _drop_expired(self, now):
        while self.expiry and next(iter(self.expiry.values())) <= now:
            self.expiry.popitem(last=False)

    def generate(self, tokenId, currentTime):
        self.expiry[tokenId] = currentTime + self.ttl
        self.expiry.move_to_end(tokenId)  # newest expiry goes last

    def renew(self, tokenId, currentTime):
        self._drop_expired(currentTime)
        if tokenId in self.expiry:  # still unexpired
            self.expiry[tokenId] = currentTime + self.ttl
            self.expiry.move_to_end(tokenId)

    def countUnexpiredTokens(self, currentTime):
        self._drop_expired(currentTime)
        return len(self.expiry)
""",
    ),
    # ---- Logger Rate Limiter (LeetCode 359) ----
    dict(
        title="Logger Rate Limiter",
        diff="E",
        lc=359,
        slug="logger-rate-limiter",
        prompt=(
            "Logger.shouldPrintMessage(timestamp, message) returns True if the message may be printed now, i.e. the "
            "same message was not printed in the previous 10 seconds (it can print again at timestamp + 10). Only "
            "printed messages update the history. Timestamps never decrease."
        ),
        sig=(
            "class Logger:\n    def __init__(self):\n        pass\n    def shouldPrintMessage(self, timestamp: int, "
            "message: str) -> bool:\n        pass"
        ),
        kind="design",
        cls="Logger",
        tests=[
            (
                (),
                [
                    ("shouldPrintMessage", [1, "foo"], True),
                    ("shouldPrintMessage", [2, "bar"], True),
                    ("shouldPrintMessage", [3, "foo"], False),
                    ("shouldPrintMessage", [8, "bar"], False),
                    ("shouldPrintMessage", [10, "foo"], False),
                    ("shouldPrintMessage", [11, "foo"], True),
                ],
            ),
            (
                (),
                [
                    ("shouldPrintMessage", [0, "a"], True),
                    ("shouldPrintMessage", [5, "a"], False),
                    ("shouldPrintMessage", [10, "a"], True),
                    ("shouldPrintMessage", [19, "a"], False),
                    ("shouldPrintMessage", [20, "a"], True),
                ],
            ),
            (
                (),
                [
                    ("shouldPrintMessage", [1, "x"], True),
                    ("shouldPrintMessage", [1, "y"], True),
                    ("shouldPrintMessage", [1, "x"], False),
                ],
            ),
        ],
        hints=[
            "You only care about the LAST time each message was printed.",
            "Store message -> next allowed timestamp (or the last printed timestamp) in a dictionary.",
            "If timestamp >= allowed (or the message is new), print it and set allowed = timestamp + 10.",
        ],
        pattern="Hash map of last-seen time",
        explain="A single dictionary entry per message replaces scanning the whole print history.",
        cx="O(1) per call",
        brute_cx="O(history) per call - scan every message printed so far",
        brute=r"""
# BRUTE FORCE: O(history) per call - scan every message printed so far
class Logger:
    def __init__(self):
        self.printed = []  # (timestamp, message) pairs that were printed

    def shouldPrintMessage(self, timestamp, message):
        for t, m in self.printed:
            if m == message and timestamp - t < 10:
                return False
        self.printed.append((timestamp, message))
        return True
""",
        solution=r"""
# OPTIMISED: O(1) per call
# Idea: Hash map of last-seen time
class Logger:
    def __init__(self):
        self.next_allowed = {}  # message -> earliest timestamp it may print again

    def shouldPrintMessage(self, timestamp, message):
        if timestamp < self.next_allowed.get(message, 0):
            return False
        self.next_allowed[message] = timestamp + 10
        return True
""",
    ),
    # ---- Design A Leaderboard (LeetCode 1244) ----
    dict(
        title="Design A Leaderboard",
        diff="M",
        lc=1244,
        slug="design-a-leaderboard",
        prompt=(
            "Leaderboard: addScore(playerId, score) adds score to the player (creating the player with that score "
            "if new), top(K) returns the sum of the K highest scores, reset(playerId) sets that player's score to 0 "
            "(the player stays on the board)."
        ),
        sig=(
            "class Leaderboard:\n    def __init__(self):\n        pass\n    def addScore(self, playerId: int, "
            "score: int) -> None:\n        pass\n    def top(self, K: int) -> int:\n        pass\n    def "
            "reset(self, playerId: int) -> None:\n        pass"
        ),
        kind="design",
        cls="Leaderboard",
        tests=[
            (
                (),
                [
                    ("addScore", [1, 73], S),
                    ("addScore", [2, 56], S),
                    ("addScore", [3, 39], S),
                    ("addScore", [4, 51], S),
                    ("addScore", [5, 4], S),
                    ("top", [1], 73),
                    ("reset", [1], S),
                    ("reset", [2], S),
                    ("addScore", [2, 51], S),
                    ("top", [3], 141),
                ],
            ),
            (
                (),
                [
                    ("addScore", [1, 10], S),
                    ("addScore", [1, 5], S),
                    ("addScore", [2, 20], S),
                    ("top", [1], 20),
                    ("top", [2], 35),
                    ("reset", [2], S),
                    ("top", [2], 15),
                ],
            ),
            (
                (),
                [
                    ("addScore", [7, 3], S),
                    ("top", [1], 3),
                    ("reset", [7], S),
                    ("top", [1], 0),
                    ("addScore", [7, 4], S),
                    ("top", [1], 4),
                ],
            ),
        ],
        hints=[
            "A dictionary playerId -> score handles addScore and reset in O(1).",
            "top(K) needs the K largest values: sorting everything works but is O(n log n).",
            "heapq.nlargest(K, scores.values()) selects the K best in O(n log K).",
        ],
        pattern="Hash map + heap selection for top-K",
        explain=(
            "Updates are constant time; the expensive query only keeps a heap of size K instead of sorting all scores."
        ),
        cx="addScore/reset O(1), top O(n log K)",
        brute_cx="top O(n log n) - sort all scores",
        brute=r"""
# BRUTE FORCE: top O(n log n) - sort all scores
class Leaderboard:
    def __init__(self):
        self.scores = {}

    def addScore(self, playerId, score):
        self.scores[playerId] = self.scores.get(playerId, 0) + score

    def top(self, K):
        return sum(sorted(self.scores.values(), reverse=True)[:K])

    def reset(self, playerId):
        self.scores[playerId] = 0
""",
        solution=r"""
# OPTIMISED: addScore/reset O(1), top O(n log K)
# Idea: Hash map + heap selection for top-K
class Leaderboard:
    def __init__(self):
        self.scores = defaultdict(int)

    def addScore(self, playerId, score):
        self.scores[playerId] += score

    def top(self, K):
        return sum(heapq.nlargest(K, self.scores.values()))  # heap of size K, not a full sort

    def reset(self, playerId):
        self.scores[playerId] = 0
""",
    ),
]
