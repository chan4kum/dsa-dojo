"""extra batch of Linked List problems - the problem bank for the "linked_list" topic.

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

from core import list_to_ll, ll_to_list


# Tests give plain Python lists; adapt_in builds the nodes, adapt_out flattens the result.
def L(a):
    """Turn every plain list in args into a linked list."""
    return tuple(list_to_ll(x) for x in a)


def _with_cycle(a):
    head = list_to_ll(a[0])
    if a[1] >= 0:
        tail, target, i, cur = head, None, 0, head
        while cur:
            if i == a[1]:
                target = cur
            tail, cur, i = cur, cur.next, i + 1
        tail.next = target
    return (head,)


PROBLEMS = [
    # ---- Merge Two Sorted Lists (LeetCode 21) ----
    dict(
        title="Merge Two Sorted Lists",
        diff="E",
        lc=21,
        slug="merge-two-sorted-lists",
        prompt="Merge two sorted linked lists into one sorted list by splicing their nodes together. Return the head.",
        sig="def merge_two_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:",
        fn="merge_two_lists",
        adapt_in=L,
        adapt_out=ll_to_list,
        tests=[
            (([1, 2, 4], [1, 3, 4]), [1, 1, 2, 3, 4, 4]),
            (([], []), []),
            (([], [0]), [0]),
            (([5], [1, 2]), [1, 2, 5]),
        ],
        hints=[
            "This is the merge step of merge sort. What do you compare at each step?",
            "Only the two current heads matter; the smaller one is next in the output.",
            (
                "Use a dummy head and a tail pointer: attach the smaller node, advance that list; finally attach "
                "the non-empty remainder."
            ),
        ],
        pattern="Dummy head + tail pointer (merge two sorted sequences)",
        explain=(
            "The dummy node removes the special case 'what is the head of the result?'. After one list runs out, "
            "the rest of\n        the other is already sorted - link it wholesale. O(m+n) time, O(1) extra space."
        ),
        cx="O(m+n) time, O(1) space",
        brute_cx="O((m+n) log(m+n)) time, O(m+n) space - dump values, sort, rebuild",
        brute=r"""
# BRUTE FORCE: O((m+n) log(m+n)) time, O(m+n) space - dump values, sort, rebuild
def merge_two_lists(list1, list2):
    vals = []

    for h in (list1, list2):
        while h:
            vals.append(h.val)
            h = h.next

    dummy = tail = ListNode()

    for v in sorted(vals):
        tail.next = ListNode(v)
        tail = tail.next

    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(m+n) time, O(1) space
# Idea: Dummy head + tail pointer (merge two sorted sequences)
def merge_two_lists(list1, list2):
    dummy = tail = ListNode()

    while list1 and list2:
        if list1.val <= list2.val:
            tail.next, list1 = list1, list1.next
        else:
            tail.next, list2 = list2, list2.next
        tail = tail.next

    tail.next = list1 or list2

    return dummy.next
""",
    ),
    # ---- Linked List Cycle (LeetCode 141) ----
    dict(
        title="Linked List Cycle",
        diff="E",
        lc=141,
        slug="linked-list-cycle",
        prompt=(
            "Return True if the linked list contains a cycle. (Tests give the values and `pos`, the index the tail "
            "connects back to; -1 means no cycle.)"
        ),
        sig="def has_cycle(head: Optional[ListNode]) -> bool:",
        fn="has_cycle",
        adapt_in=_with_cycle,
        tests=[
            (([3, 2, 0, -4], 1), True),
            (([1, 2], 0), True),
            (([1], -1), False),
            (([], -1), False),
            (([1, 2, 3], -1), False),
            (([1], 0), True),
        ],
        hints=[
            "How would you notice you have been at a node before?",
            "A set of visited nodes works but costs O(n) memory.",
            (
                "Floyd: slow moves 1, fast moves 2. In a cycle fast eventually laps slow, so they meet; without a "
                "cycle fast hits None."
            ),
        ],
        pattern="Floyd's cycle detection (fast & slow pointers)",
        explain=(
            "Inside a loop the gap between fast and slow shrinks by 1 each step, so it must hit 0. O(n) time, O(1) "
            "space.\n        (To find where the cycle starts: after they meet, restart one pointer at head and move "
            "both 1 step at a time.)"
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - remember visited nodes",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - remember visited nodes
def has_cycle(head):
    seen = set()
    while head:
        if id(head) in seen:
            return True
        seen.add(id(head))
        head = head.next
    return False
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Floyd's cycle detection (fast & slow pointers)
def has_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            return True
    return False
""",
    ),
    # ---- Palindrome Linked List (LeetCode 234) ----
    dict(
        title="Palindrome Linked List",
        diff="E",
        lc=234,
        slug="palindrome-linked-list",
        prompt="Return True if the linked list reads the same forwards and backwards. Aim for O(1) extra space.",
        sig="def is_palindrome(head: Optional[ListNode]) -> bool:",
        fn="is_palindrome",
        adapt_in=lambda a: (list_to_ll(a[0]),),
        tests=[
            (([1, 2, 2, 1],), True),
            (([1, 2],), False),
            (([1],), True),
            (([1, 2, 3, 2, 1],), True),
            (([],), True),
            (([1, 2, 3, 1],), False),
        ],
        hints=[
            "Copying into an array makes it trivial - but costs O(n) space.",
            "Find the middle (fast/slow), reverse the second half in place.",
            (
                "Compare the first half with the reversed second half node by node. (Restore the list afterwards if "
                "you must not modify it.)"
            ),
        ],
        pattern="Fast/slow to find the middle + in-place reverse + two-pointer compare",
        explain=(
            "This combines three earlier ideas: middle node, reverse list, compare. Odd lengths: the middle node "
            "can\n        be left on either side because the comparison stops when the shorter half ends."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - copy values to a list",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - copy values to a list
def is_palindrome(head):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    return vals == vals[::-1]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Fast/slow to find the middle + in-place reverse + two-pointer compare
def is_palindrome(head):
    slow = fast = head

    while fast and fast.next:
        slow, fast = slow.next, fast.next.next

    prev = None

    while slow:  # reverse second half
        slow.next, prev, slow = prev, slow, slow.next

    left, right = head, prev

    while right:
        if left.val != right.val:
            return False
        left, right = left.next, right.next

    return True
""",
    ),
    # ---- Add Two Numbers (LeetCode 2) ----
    dict(
        title="Add Two Numbers",
        diff="M",
        lc=2,
        slug="add-two-numbers",
        prompt=(
            "Two non-negative integers are stored as linked lists of digits in REVERSE order (least significant "
            "first). Return their sum in the same format."
        ),
        sig="def add_two_numbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:",
        fn="add_two_numbers",
        adapt_in=L,
        adapt_out=ll_to_list,
        tests=[
            (([2, 4, 3], [5, 6, 4]), [7, 0, 8]),
            (([0], [0]), [0]),
            (([9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9]), [8, 9, 9, 9, 0, 0, 0, 1]),
            (([5], [5]), [0, 1]),
            (([1], [9, 9]), [0, 0, 1]),
        ],
        hints=[
            "Reverse order is a gift: the head is already the ones digit, like adding on paper.",
            "Walk both lists together, adding digits plus a carry.",
            (
                "digit = (a + b + carry) % 10, carry = (a + b + carry) // 10. Keep going while either list or the "
                "carry remains."
            ),
        ],
        pattern="Simulate grade-school addition with a carry",
        explain=(
            "A dummy head plus a while-loop over `l1 or l2 or carry` handles unequal lengths and a final "
            "carry\n        without special cases."
        ),
        cx="O(max(m, n)) time",
        brute_cx="O(m+n) time - convert to Python ints, add, convert back (cheating on huge numbers, but correct)",
        brute=r"""
# BRUTE FORCE: O(m+n) time - convert to Python ints, add, convert back (cheating on huge numbers, but correct)
def add_two_numbers(l1, l2):
    def to_int(h):
        digits = []
        while h:
            digits.append(str(h.val))
            h = h.next
        return int("".join(reversed(digits)))

    total = str(to_int(l1) + to_int(l2))
    dummy = tail = ListNode()

    for ch in reversed(total):
        tail.next = ListNode(int(ch))
        tail = tail.next

    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(max(m, n)) time
# Idea: Simulate grade-school addition with a carry
def add_two_numbers(l1, l2):
    dummy = tail = ListNode()
    carry = 0

    while l1 or l2 or carry:
        s = carry + (l1.val if l1 else 0) + (l2.val if l2 else 0)
        carry, digit = divmod(s, 10)
        tail.next = ListNode(digit)
        tail = tail.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None

    return dummy.next
""",
    ),
    # ---- Reorder List (LeetCode 143) ----
    dict(
        title="Reorder List",
        diff="M",
        lc=143,
        slug="reorder-list",
        prompt=(
            "Reorder L0->L1->...->Ln-1->Ln into L0->Ln->L1->Ln-1->L2->Ln-2->... in place (change links, not values)."
        ),
        sig="def reorder_list(head: Optional[ListNode]) -> None:",
        fn="reorder_list",
        adapt_in=lambda a: (list_to_ll(a[0]),),
        adapt_out=ll_to_list,
        inplace=0,
        tests=[
            (([1, 2, 3, 4],), [1, 4, 2, 3]),
            (([1, 2, 3, 4, 5],), [1, 5, 2, 4, 3]),
            (([1],), [1]),
            (([1, 2],), [1, 2]),
            (([1, 2, 3],), [1, 3, 2]),
        ],
        hints=[
            "You alternate between the front of the list and the back. Which part of the list is hard to reach?",
            "Split into two halves, reverse the second half.",
            "Merge the two halves by interleaving: take one from the first, one from the reversed second.",
        ],
        pattern="Middle + reverse + interleave merge (compose list primitives)",
        explain=(
            "Reaching the back of a singly linked list is expensive, so reverse the back half once, then zip. "
            "Three\n        well-known sub-problems solved in sequence: O(n) time, O(1) space."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - store nodes in an array, relink with two indices",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - store nodes in an array, relink with two indices
def reorder_list(head):
    nodes = []
    cur = head

    while cur:
        nodes.append(cur)
        cur = cur.next

    left, right = 0, len(nodes) - 1
    tail = ListNode()

    while left <= right:
        tail.next = nodes[left]
        tail = tail.next
        if left != right:
            tail.next = nodes[right]
            tail = tail.next
        left, right = left + 1, right - 1

    tail.next = None
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Middle + reverse + interleave merge (compose list primitives)
def reorder_list(head):
    if not head or not head.next:
        return

    slow, fast = head, head

    while fast.next and fast.next.next:
        slow, fast = slow.next, fast.next.next

    second, slow.next = slow.next, None
    prev = None

    while second:  # reverse second half
        second.next, prev, second = prev, second, second.next

    first, second = head, prev

    while second:
        n1, n2 = first.next, second.next
        first.next, second.next = second, n1
        first, second = n1, n2
""",
    ),
    # ---- Merge k Sorted Lists (LeetCode 23) ----
    dict(
        title="Merge k Sorted Lists",
        diff="H",
        lc=23,
        slug="merge-k-sorted-lists",
        prompt="Merge k sorted linked lists into one sorted list and return its head.",
        sig="def merge_k_lists(lists: List[Optional[ListNode]]) -> Optional[ListNode]:",
        fn="merge_k_lists",
        adapt_in=lambda a: ([list_to_ll(x) for x in a[0]],),
        adapt_out=ll_to_list,
        tests=[
            (([[1, 4, 5], [1, 3, 4], [2, 6]],), [1, 1, 2, 3, 4, 4, 5, 6]),
            (([],), []),
            (([[]],), []),
            (([[1], [0]],), [0, 1]),
            (([[2], [], [1, 3]],), [1, 2, 3]),
        ],
        hints=[
            "Merging them one after another costs O(k*N). Which element is next overall?",
            "The smallest of the k current heads.",
            "Min-heap of (value, list index, node). Pop the smallest, push its successor. Total N log k.",
        ],
        pattern="Heap of k candidates (k-way merge)",
        explain=(
            "At any moment only the k list heads are candidates for 'next smallest'. A min-heap gives the smallest "
            "in\n        O(log k). Include a unique tie-breaker (the list index) so nodes themselves are never "
            "compared."
        ),
        cx="O(N log k) time, O(k) space",
        brute_cx="O(N log N) time, O(N) space - collect every value, sort, rebuild",
        brute=r"""
# BRUTE FORCE: O(N log N) time, O(N) space - collect every value, sort, rebuild
def merge_k_lists(lists):
    vals = []

    for h in lists:
        while h:
            vals.append(h.val)
            h = h.next

    dummy = tail = ListNode()

    for v in sorted(vals):
        tail.next = ListNode(v)
        tail = tail.next

    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(N log k) time, O(k) space
# Idea: Heap of k candidates (k-way merge)
def merge_k_lists(lists):
    heap = [(h.val, i, h) for i, h in enumerate(lists) if h]
    heapq.heapify(heap)
    dummy = tail = ListNode()

    while heap:
        _, i, node = heapq.heappop(heap)
        tail.next = node
        tail = node
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next
""",
    ),
    # ---- Remove Duplicates from Sorted List (LeetCode 83) ----
    dict(
        title="Remove Duplicates from Sorted List",
        diff="E",
        lc=83,
        slug="remove-duplicates-from-sorted-list",
        prompt="Delete all duplicates from a sorted linked list so each value appears once. Return the list.",
        sig="def delete_duplicates(head: Optional[ListNode]) -> Optional[ListNode]:",
        fn="delete_duplicates",
        adapt_in=lambda a: (list_to_ll(a[0]),),
        adapt_out=ll_to_list,
        tests=[
            (([1, 1, 2],), [1, 2]),
            (([1, 1, 2, 3, 3],), [1, 2, 3]),
            (([],), []),
            (([1, 1, 1],), [1]),
            (([1, 2, 3],), [1, 2, 3]),
        ],
        hints=[
            "Because the list is sorted, duplicates are adjacent.",
            "Compare each node with the next one.",
            "If cur.val == cur.next.val: cur.next = cur.next.next (do not advance); else advance.",
        ],
        pattern="Single pointer, skip equal neighbours",
        explain="\n        Not advancing after a deletion lets runs of three or more equal values collapse correctly.",
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - dedupe values in a Python list, rebuild nodes",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - dedupe values in a Python list, rebuild nodes
def delete_duplicates(head):
    vals = []

    while head:
        if not vals or vals[-1] != head.val:
            vals.append(head.val)
        head = head.next

    dummy = tail = ListNode()

    for v in vals:
        tail.next = ListNode(v)
        tail = tail.next

    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Single pointer, skip equal neighbours
def delete_duplicates(head):
    cur = head
    while cur and cur.next:
        if cur.val == cur.next.val:
            cur.next = cur.next.next
        else:
            cur = cur.next
    return head
""",
    ),
    # ---- Reverse Linked List II (LeetCode 92) ----
    dict(
        title="Reverse Linked List II",
        diff="M",
        lc=92,
        slug="reverse-linked-list-ii",
        prompt=(
            "Reverse the nodes of a linked list from position left to position right (1-indexed) and return the head."
        ),
        sig="def reverse_between(head: Optional[ListNode], left: int, right: int) -> Optional[ListNode]:",
        fn="reverse_between",
        adapt_in=lambda a: (list_to_ll(a[0]), a[1], a[2]),
        adapt_out=ll_to_list,
        tests=[
            (([1, 2, 3, 4, 5], 2, 4), [1, 4, 3, 2, 5]),
            (([5], 1, 1), [5]),
            (([3, 5], 1, 2), [5, 3]),
            (([1, 2, 3], 1, 3), [3, 2, 1]),
            (([1, 2, 3, 4], 2, 2), [1, 2, 3, 4]),
        ],
        hints=[
            "You know how to reverse a whole list. What must stay connected on either side of the reversed part?",
            (
                "Remember the node just before position left, and the node at position left (it becomes the tail of "
                "the reversed part)."
            ),
            (
                "Dummy head; walk to the node before `left`; then repeatedly move the node after the tail to the "
                "front of the segment (left-to-right pointer surgery, right-left times)."
            ),
        ],
        pattern="Pointer surgery with a dummy head (reverse a sub-segment in place)",
        explain=(
            "The dummy node means position 1 needs no special case. 'Head insertion' - repeatedly take the node "
            "after the\n        segment's tail and splice it right after the node before the segment - reverses it "
            "in one pass."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - copy values to a Python list, reverse a slice, rebuild",
        brute="""
def reverse_between(head, left, right):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    vals[left - 1:right] = vals[left - 1:right][::-1]
    dummy = tail = ListNode()
    for v in vals:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next
""",
        solution="""
def reverse_between(head, left, right):
    dummy = ListNode(0, head)
    pre = dummy
    for _ in range(left - 1):
        pre = pre.next
    cur = pre.next                       # becomes the tail of the reversed part
    for _ in range(right - left):
        nxt = cur.next
        cur.next = nxt.next
        nxt.next = pre.next
        pre.next = nxt
    return dummy.next
""",
    ),
    # ---- Linked List Cycle II (LeetCode 142) ----
    dict(
        title="Linked List Cycle II",
        diff="M",
        lc=142,
        slug="linked-list-cycle-ii",
        prompt=(
            "If the list has a cycle return the node where it begins, else None. (Tests give distinct values and "
            "`pos`; the expected answer is the VALUE of the start node, or -1.)"
        ),
        sig="def detect_cycle(head: Optional[ListNode]) -> Optional[ListNode]:",
        fn="detect_cycle",
        adapt_in=_with_cycle,
        adapt_out=lambda n: -1 if n is None else n.val,
        tests=[
            (([3, 2, 0, -4], 1), 2),
            (([1, 2], 0), 1),
            (([1], -1), -1),
            (([1, 2, 3, 4], 2), 3),
            (([1], 0), 1),
            (([], -1), -1),
        ],
        hints=[
            "First detect that a cycle exists (Floyd). Where do slow and fast meet relative to the cycle start?",
            (
                "Let the distance from head to the cycle start be a, and from the start to the meeting point be b. "
                "Fast has travelled twice as far as slow."
            ),
            (
                "That gives a = (cycle length) - b (mod cycle length): so a pointer from head and a pointer from "
                "the meeting point, both moving 1 step, meet exactly at the cycle start."
            ),
        ],
        pattern="Floyd phase 2: restart one pointer from the head",
        explain=(
            "slow travels a+b, fast travels 2(a+b); fast has done an extra whole number of laps: a+b = k*L. So "
            "walking a more\n        steps from the meeting point returns to the start of the cycle - exactly what "
            "a pointer from the head also does.\n        Worth proving once on paper: this is the proof "
            "interviewers ask for."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - remember visited nodes; the first repeat is the start",
        brute="""
def detect_cycle(head):
    seen = set()
    while head:
        if id(head) in seen:
            return head
        seen.add(id(head))
        head = head.next
    return None
""",
        solution="""
def detect_cycle(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next
        if slow is fast:
            slow = head
            while slow is not fast:
                slow, fast = slow.next, fast.next
            return slow
    return None
""",
    ),
]
