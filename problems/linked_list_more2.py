"""more Linked List problems (batch 4) - part of the problem bank for the "linked_list" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
Tests use plain Python lists; adapt_in builds the linked list(s), adapt_out turns the answer back into a list.
"""

from core import list_to_ll, ll_to_list


def L(a):
    """Turn every plain list in args into a linked list."""
    return tuple(list_to_ll(x) for x in a)


def H(a):
    """Turn only the first argument (a plain list) into a linked list; keep the other arguments as they are."""
    return (list_to_ll(a[0]),) + tuple(a[1:])


PROBLEMS = [
    # ---- Swap Nodes in Pairs (LeetCode 24) ----
    dict(
        title="Swap Nodes in Pairs",
        diff="M",
        lc=24,
        slug="swap-nodes-in-pairs",
        prompt=(
            "Swap every two adjacent nodes of the list and return the new head. Change links, not the stored values."
        ),
        sig="def swap_pairs(head: Optional[ListNode]) -> Optional[ListNode]:",
        fn="swap_pairs",
        adapt_in=H,
        adapt_out=ll_to_list,
        tests=[
            (([1, 2, 3, 4],), [2, 1, 4, 3]),
            (([],), []),
            (([1],), [1]),
            (([1, 2, 3],), [2, 1, 3]),
        ],
        hints=[
            "Work on two nodes at a time: first and second. After the swap, second points to first.",
            "A dummy node before the head means the head never needs a special case.",
            (
                "Keep `prev` = node before the pair. Set prev.next = second, first.next = second.next, second.next "
                "= first, then prev = first."
            ),
        ],
        pattern="Dummy head + pointer rewiring in fixed-size groups",
        explain=(
            "Pointer surgery is easiest if you name the three nodes you touch (prev, first, second) and rewire in a "
            "fixed order\n        so no node is ever lost. The dummy head removes the special case for the first "
            "pair."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - copy the values out and rebuild",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - copy the values out and rebuild
def swap_pairs(head):
    values = []

    while head:  # copy the values into a list
        values.append(head.val)
        head = head.next

    for i in range(0, len(values) - 1, 2):  # swap each adjacent pair of values
        values[i], values[i + 1] = values[i + 1], values[i]

    dummy = tail = ListNode()

    for v in values:  # build a brand-new list
        tail.next = ListNode(v)
        tail = tail.next

    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Dummy head + pointer rewiring in fixed-size groups
def swap_pairs(head):
    dummy = ListNode(0, head)
    prev = dummy  # the node just before the pair being swapped

    while prev.next and prev.next.next:
        first, second = prev.next, prev.next.next
        first.next = second.next  # first now skips over second
        second.next = first  # second points back at first
        prev.next = second  # the node before the pair now points at second
        prev = first  # first is the last node of the swapped pair

    return dummy.next
""",
    ),
    # ---- Rotate List (LeetCode 61) ----
    dict(
        title="Rotate List",
        diff="M",
        lc=61,
        slug="rotate-list",
        prompt="Rotate the list to the right by k places (the last k nodes move to the front) and return the new head.",
        sig="def rotate_right(head: Optional[ListNode], k: int) -> Optional[ListNode]:",
        fn="rotate_right",
        adapt_in=H,
        adapt_out=ll_to_list,
        tests=[
            (([1, 2, 3, 4, 5], 2), [4, 5, 1, 2, 3]),
            (([0, 1, 2], 4), [2, 0, 1]),
            (([], 0), []),
            (([1], 5), [1]),
            (([1, 2], 2), [1, 2]),
        ],
        hints=[
            "Rotating by the list length changes nothing, so only k % n matters.",
            "After rotating, the new tail is the node at position n - k % n - 1 and the new head is the node after it.",
            "Join the old tail to the old head to make a ring, walk to the new tail, then cut the ring.",
        ],
        pattern="Make the list circular, then cut it at the right place",
        explain=(
            "A rotation is just choosing a different starting point on a cycle. Closing the list into a ring, "
            "walking n - k%n steps\n        and cutting there is simpler than shuffling nodes one by one."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n * k) time - move the last node to the front k times",
        brute=r"""
# BRUTE FORCE: O(n * k) time - move the last node to the front k times
def rotate_right(head, k):
    if not head or not head.next:
        return head

    for _ in range(k):  # rotate by one place, k times
        prev, cur = None, head
        while cur.next:  # find the last node and the one before it
            prev, cur = cur, cur.next
        prev.next = None  # detach the last node...
        cur.next = head  # ...and put it in front
        head = cur

    return head
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Make the list circular, then cut it at the right place
def rotate_right(head, k):
    if not head or not head.next or k == 0:
        return head

    tail, n = head, 1

    while tail.next:  # find the tail and the length
        tail = tail.next
        n += 1

    k %= n

    if k == 0:
        return head

    tail.next = head  # close the list into a ring
    new_tail = head

    for _ in range(n - k - 1):  # walk to the node that will become the tail
        new_tail = new_tail.next

    new_head = new_tail.next
    new_tail.next = None  # cut the ring

    return new_head
""",
    ),
    # ---- Remove Duplicates from Sorted List II (LeetCode 82) ----
    dict(
        title="Remove Duplicates from Sorted List II",
        diff="M",
        lc=82,
        slug="remove-duplicates-from-sorted-list-ii",
        prompt=(
            "The list is sorted. Delete EVERY node whose value appears more than once (keep only values that occur "
            "exactly once)."
        ),
        sig="def delete_duplicates(head: Optional[ListNode]) -> Optional[ListNode]:",
        fn="delete_duplicates",
        adapt_in=H,
        adapt_out=ll_to_list,
        tests=[
            (([1, 2, 3, 3, 4, 4, 5],), [1, 2, 5]),
            (([1, 1, 1, 2, 3],), [2, 3]),
            (([],), []),
            (([1, 1],), []),
            (([1, 2, 2],), [1]),
        ],
        hints=[
            "Because the list is sorted, equal values sit next to each other.",
            "A dummy head helps: the first nodes might be deleted too.",
            (
                "Keep `prev` (last kept node). If cur and cur.next are equal, skip ALL nodes with that value, then "
                "set prev.next to what follows; otherwise advance prev."
            ),
        ],
        pattern="Dummy head + skip whole runs of equal values",
        explain=(
            "Unlike Remove Duplicates I, a value that repeats disappears completely, so we need the node BEFORE the "
            "run to reconnect\n        around it - that is what the dummy head and `prev` give us."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - count values then rebuild",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - count values then rebuild
def delete_duplicates(head):
    counts = {}
    node = head

    while node:  # how many times does each value occur?
        counts[node.val] = counts.get(node.val, 0) + 1
        node = node.next

    dummy = tail = ListNode()
    node = head

    while node:
        if counts[node.val] == 1:  # keep only values that occur once
            tail.next = ListNode(node.val)
            tail = tail.next
        node = node.next

    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Dummy head + skip whole runs of equal values
def delete_duplicates(head):
    dummy = ListNode(0, head)
    prev = dummy  # last node we are sure to keep
    cur = head

    while cur:
        if cur.next and cur.next.val == cur.val:
            dup = cur.val
            while cur and cur.val == dup:  # skip the entire run of this value
                cur = cur.next
            prev.next = cur  # reconnect around the removed run
        else:
            prev = cur  # cur is unique: keep it
            cur = cur.next

    return dummy.next
""",
    ),
    # ---- Partition List (LeetCode 86) ----
    dict(
        title="Partition List",
        diff="M",
        lc=86,
        slug="partition-list",
        prompt=(
            "Rearrange the list so all nodes with value < x come before nodes with value >= x, keeping the original "
            "relative order inside each group."
        ),
        sig="def partition(head: Optional[ListNode], x: int) -> Optional[ListNode]:",
        fn="partition",
        adapt_in=H,
        adapt_out=ll_to_list,
        tests=[
            (([1, 4, 3, 2, 5, 2], 3), [1, 2, 2, 4, 3, 5]),
            (([2, 1], 2), [1, 2]),
            (([], 1), []),
            (([3, 1], 5), [3, 1]),
            (([5, 4, 3], 3), [5, 4, 3]),
        ],
        hints=[
            "Two groups, each keeping its original order. Think: two separate lists, then glue.",
            "Walk the list once, appending each node to the 'small' list or the 'large' list.",
            "Use a dummy head for each list. At the end small.tail.next = large.head and large.tail.next = None.",
        ],
        pattern="Split into two lists with dummy heads, then concatenate",
        explain=(
            "A stable partition is just two queues: send each node to one of them in the order you meet it, then "
            "join the queues. Remember to\n        terminate the large list - otherwise the old next pointers can "
            "create a cycle."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - collect values, rebuild",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - collect values, rebuild
def partition(head, x):
    values = []

    while head:
        values.append(head.val)
        head = head.next

    ordered = [v for v in values if v < x] + [v for v in values if v >= x]  # stable partition
    dummy = tail = ListNode()

    for v in ordered:
        tail.next = ListNode(v)
        tail = tail.next

    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Split into two lists with dummy heads, then concatenate
def partition(head, x):
    small_head = small = ListNode()  # nodes with value < x
    large_head = large = ListNode()  # nodes with value >= x

    while head:
        if head.val < x:
            small.next = head
            small = small.next
        else:
            large.next = head
            large = large.next
        head = head.next

    large.next = None  # cut off the tail so the list cannot loop back
    small.next = large_head.next  # glue: small list, then large list

    return small_head.next
""",
    ),
    # ---- Odd Even Linked List (LeetCode 328) ----
    dict(
        title="Odd Even Linked List",
        diff="M",
        lc=328,
        slug="odd-even-linked-list",
        prompt=(
            "Group all nodes at ODD positions (1st, 3rd, ...) together, followed by the nodes at EVEN positions, "
            "keeping relative order. Use O(1) extra space."
        ),
        sig="def odd_even_list(head: Optional[ListNode]) -> Optional[ListNode]:",
        fn="odd_even_list",
        adapt_in=H,
        adapt_out=ll_to_list,
        tests=[
            (([1, 2, 3, 4, 5],), [1, 3, 5, 2, 4]),
            (([2, 1, 3, 5, 6, 4, 7],), [2, 3, 6, 7, 1, 5, 4]),
            (([],), []),
            (([1],), [1]),
            (([1, 2],), [1, 2]),
        ],
        hints=[
            "Positions, not values, decide the groups.",
            "Keep two pointers: odd (building the odd chain) and even (building the even chain).",
            (
                "Repeat odd.next = even.next; odd = odd.next; even.next = odd.next; even = even.next. At the end "
                "odd.next = head of the even chain."
            ),
        ],
        pattern="Two interleaved chains built in one pass, then joined",
        explain=(
            "Every second node already forms the even chain; relinking each node to the one two steps ahead "
            "separates the chains\n        without allocating anything. Save the head of the even chain before you "
            "start."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - copy values by position",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - copy values by position
def odd_even_list(head):
    values = []

    while head:
        values.append(head.val)
        head = head.next

    ordered = values[0::2] + values[1::2]  # odd positions (index 0, 2, ...) then even positions
    dummy = tail = ListNode()

    for v in ordered:
        tail.next = ListNode(v)
        tail = tail.next

    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two interleaved chains built in one pass, then joined
def odd_even_list(head):
    if not head or not head.next:
        return head

    odd, even = head, head.next
    even_head = even  # remember where the even chain starts

    while even and even.next:
        odd.next = even.next  # odd skips over the even node
        odd = odd.next
        even.next = odd.next  # even skips over the odd node
        even = even.next

    odd.next = even_head  # attach the even chain after the odd chain

    return head
""",
    ),
    # ---- Remove Linked List Elements (LeetCode 203) ----
    dict(
        title="Remove Linked List Elements",
        diff="E",
        lc=203,
        slug="remove-linked-list-elements",
        prompt="Remove every node whose value equals val and return the new head.",
        sig="def remove_elements(head: Optional[ListNode], val: int) -> Optional[ListNode]:",
        fn="remove_elements",
        adapt_in=H,
        adapt_out=ll_to_list,
        tests=[
            (([1, 2, 6, 3, 4, 5, 6], 6), [1, 2, 3, 4, 5]),
            (([], 1), []),
            (([7, 7, 7, 7], 7), []),
            (([1, 2], 3), [1, 2]),
        ],
        hints=[
            "Deleting a node means the node BEFORE it must point past it.",
            "The head itself may need deleting - a dummy node in front removes that special case.",
            "Walk with `prev`; if prev.next.val == val set prev.next = prev.next.next, else advance prev.",
        ],
        pattern="Dummy head + delete-after-prev",
        explain=(
            "The dummy head is the standard trick for 'the first node may change'. Always test prev.next so you can "
            "unlink it without a back pointer."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - rebuild from a filtered list of values",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - rebuild from a filtered list of values
def remove_elements(head, val):
    kept = []

    while head:
        if head.val != val:
            kept.append(head.val)
        head = head.next

    dummy = tail = ListNode()

    for v in kept:
        tail.next = ListNode(v)
        tail = tail.next

    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Dummy head + delete-after-prev
def remove_elements(head, val):
    dummy = ListNode(0, head)
    prev = dummy

    while prev.next:
        if prev.next.val == val:
            prev.next = prev.next.next  # unlink the node
        else:
            prev = prev.next  # keep it and move on

    return dummy.next
""",
    ),
    # ---- Add Two Numbers II (LeetCode 445) ----
    dict(
        title="Add Two Numbers II",
        diff="M",
        lc=445,
        slug="add-two-numbers-ii",
        prompt=(
            "Two non-negative integers are stored as linked lists with the MOST significant digit first. Return "
            "their sum as a list in the same format."
        ),
        sig="def add_two_numbers(l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:",
        fn="add_two_numbers",
        adapt_in=L,
        adapt_out=ll_to_list,
        tests=[
            (([7, 2, 4, 3], [5, 6, 4]), [7, 8, 0, 7]),
            (([2, 4, 3], [5, 6, 4]), [8, 0, 7]),
            (([0], [0]), [0]),
            (([9, 9], [1]), [1, 0, 0]),
        ],
        hints=[
            "Addition starts at the least significant digit, which is at the END of these lists.",
            "You cannot walk a singly linked list backwards - but a stack reverses the order for you.",
            (
                "Push digits of both lists on stacks, pop together adding with a carry, and prepend each result "
                "digit to the answer list."
            ),
        ],
        pattern="Stacks to read a list backwards; build the answer by prepending",
        explain=(
            "Add Two Numbers I gave us digits in reverse order for free. Here a stack (or reversing the lists) "
            "recreates that order,\n        and prepending to the result keeps the final digits in the right order "
            "without a second reversal."
        ),
        cx="O(m + n) time, O(m + n) space",
        brute_cx="O(m + n) time - convert to Python ints, add, convert back",
        brute=r"""
# BRUTE FORCE: O(m + n) time - convert to Python ints, add, convert back
def add_two_numbers(l1, l2):
    def to_int(node):
        number = 0
        while node:
            number = number * 10 + node.val  # read the digits left to right
            node = node.next
        return number

    total = to_int(l1) + to_int(l2)
    dummy = tail = ListNode()

    for digit in str(total):  # write the digits back out
        tail.next = ListNode(int(digit))
        tail = tail.next

    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(m + n) time, O(m + n) space
# Idea: Stacks to read a list backwards; build the answer by prepending
def add_two_numbers(l1, l2):
    a, b = [], []

    while l1:  # stacks hold the digits so we can pop the LEAST significant first
        a.append(l1.val)
        l1 = l1.next

    while l2:
        b.append(l2.val)
        l2 = l2.next

    head, carry = None, 0

    while a or b or carry:
        total = carry + (a.pop() if a else 0) + (b.pop() if b else 0)
        carry, digit = divmod(total, 10)
        head = ListNode(digit, head)  # prepend: new digit goes in FRONT of what we built

    return head
""",
    ),
    # ---- Sort List (LeetCode 148) ----
    dict(
        title="Sort List",
        diff="M",
        lc=148,
        slug="sort-list",
        prompt="Sort a linked list in ascending order, ideally in O(n log n) time.",
        sig="def sort_list(head: Optional[ListNode]) -> Optional[ListNode]:",
        fn="sort_list",
        adapt_in=H,
        adapt_out=ll_to_list,
        tests=[
            (([4, 2, 1, 3],), [1, 2, 3, 4]),
            (([-1, 5, 3, 4, 0],), [-1, 0, 3, 4, 5]),
            (([],), []),
            (([1],), [1]),
            (([2, 2, 1, 1],), [1, 1, 2, 2]),
        ],
        hints=[
            (
                "Arrays can be sorted with quicksort/heap sort using random access. A linked list has none - which "
                "sort needs only sequential access?"
            ),
            "Merge sort: split the list in half (slow/fast pointers), sort each half, merge two sorted lists.",
            (
                "Find the middle, cut the list there (middle.next = None), recurse on both halves, and merge with "
                "the Merge Two Sorted Lists routine."
            ),
        ],
        pattern="Merge sort on a linked list (split with slow/fast, merge with dummy)",
        explain=(
            "Merge sort only walks forward, so it suits linked lists perfectly and needs no extra array. The two "
            "building blocks - finding the\n        middle and merging two sorted lists - are problems you have "
            "already solved."
        ),
        cx="O(n log n) time, O(log n) recursion stack",
        brute_cx="O(n log n) time, O(n) space - copy to a Python list and sort",
        brute=r"""
# BRUTE FORCE: O(n log n) time, O(n) space - copy to a Python list and sort
def sort_list(head):
    values = []

    while head:
        values.append(head.val)
        head = head.next

    values.sort()  # let Python do the sorting
    dummy = tail = ListNode()

    for v in values:
        tail.next = ListNode(v)
        tail = tail.next

    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(log n) recursion stack
# Idea: Merge sort on a linked list (split with slow/fast, merge with dummy)
def sort_list(head):
    if not head or not head.next:
        return head

    slow, fast = head, head.next  # find the end of the first half

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    second, slow.next = slow.next, None  # cut the list into two halves
    left, right = sort_list(head), sort_list(second)
    dummy = tail = ListNode()

    while left and right:  # merge two sorted lists
        if left.val <= right.val:
            tail.next, left = left, left.next
        else:
            tail.next, right = right, right.next
        tail = tail.next

    tail.next = left or right  # attach the leftover

    return dummy.next
""",
    ),
]
