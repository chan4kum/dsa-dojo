"""Linked List problems - the problem bank for the "linked_list" topic.

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

# Linked-list tests give plain Python lists; adapt_in builds the nodes and adapt_out turns the result back.

PROBLEMS = [
    # ---- Reverse Linked List (LeetCode 206) ----
    dict(
        title="Reverse Linked List",
        diff="E",
        lc=206,
        slug="reverse-linked-list",
        prompt="Reverse a singly linked list and return the new head. Do it iteratively in O(1) extra space.",
        sig="def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:",
        fn="reverse_list",
        adapt_in=lambda a: (list_to_ll(a[0]),),
        adapt_out=ll_to_list,
        tests=[
            (([1, 2, 3, 4, 5],), [5, 4, 3, 2, 1]),
            (([1, 2],), [2, 1]),
            (([],), []),
            (([7],), [7]),
        ],
        hints=[
            "Each node's `next` must end up pointing at the node BEFORE it.",
            "Walk with prev=None, cur=head. Before you overwrite cur.next, what must you save?",
            "nxt = cur.next; cur.next = prev; prev = cur; cur = nxt. Return prev.",
        ],
        pattern="Pointer re-wiring with prev/cur/next (three-pointer walk)",
        explain=(
            "Draw the arrows on paper: at each step cur.next flips to point backwards. You lose the rest of "
            "the\n        list the moment you overwrite cur.next, so save it first. When cur falls off the end, "
            "prev is the\n        new head. O(n) time, O(1) space."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time but O(n) extra space - copies values into a new list",
        brute=r"""
# BRUTE FORCE: O(n) time but O(n) extra space - copies values into a new list
def reverse_list(head):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    dummy = tail = ListNode()
    for v in reversed(vals):
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Pointer re-wiring with prev/cur/next (three-pointer walk)
def reverse_list(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next  # save the rest of the list
        cur.next = prev  # flip the arrow
        prev, cur = cur, nxt
    return prev
""",
    ),
    # ---- Middle of the Linked List (LeetCode 876) ----
    dict(
        title="Middle of the Linked List",
        diff="E",
        lc=876,
        slug="middle-of-the-linked-list",
        prompt=(
            "Return the middle node of a linked list (the second middle if the length is even). Return the list "
            "from that node on."
        ),
        sig="def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:",
        fn="middle_node",
        adapt_in=lambda a: (list_to_ll(a[0]),),
        adapt_out=ll_to_list,
        tests=[
            (([1, 2, 3, 4, 5],), [3, 4, 5]),
            (([1, 2, 3, 4, 5, 6],), [4, 5, 6]),
            (([1],), [1]),
            (([1, 2],), [2]),
        ],
        hints=[
            "You do not know the length up front. Could you find the middle in one pass?",
            "Two runners: one moves 1 step, the other 2 steps per iteration.",
            "When fast reaches the end (fast is None or fast.next is None), slow is in the middle.",
        ],
        pattern="Fast & slow pointers (tortoise and hare)",
        explain=(
            "The fast pointer covers twice the distance, so when it finishes the slow one is halfway. This "
            "same\n        speed difference detects cycles (they must meet) - see Find the Duplicate Number below."
        ),
        cx="O(n) time, O(1) space (fast/slow)",
        brute_cx="two passes - count the length, then walk n/2",
        brute=r"""
# BRUTE FORCE: two passes - count the length, then walk n/2
def middle_node(head):
    n, cur = 0, head
    while cur:
        n, cur = n + 1, cur.next
    for _ in range(n // 2):
        head = head.next
    return head
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space (fast/slow)
# Idea: Fast & slow pointers (tortoise and hare)
def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
""",
    ),
    # ---- Remove Nth Node From End of List (LeetCode 19) ----
    dict(
        title="Remove Nth Node From End of List",
        diff="M",
        lc=19,
        slug="remove-nth-node-from-end-of-list",
        prompt="Delete the n-th node counting from the END of a linked list and return the head. One pass preferred.",
        sig="def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:",
        fn="remove_nth_from_end",
        adapt_in=lambda a: (list_to_ll(a[0]), a[1]),
        adapt_out=ll_to_list,
        tests=[
            (([1, 2, 3, 4, 5], 2), [1, 2, 3, 5]),
            (([1], 1), []),
            (([1, 2], 1), [1]),
            (([1, 2], 2), [2]),
            (([1, 2, 3], 3), [2, 3]),
        ],
        hints=[
            "The n-th from the end is (length - n) from the start - but that needs the length.",
            (
                "Make two pointers n nodes apart; when the front one reaches the end, the back one is where you "
                "need to be."
            ),
            (
                "Use a dummy node before head so removing the head needs no special case; stop `slow` at the node "
                "BEFORE the one to delete."
            ),
        ],
        pattern="Two pointers with a fixed gap + dummy head node",
        explain=(
            "Advance `fast` n steps from the dummy, then move both until fast.next is None: slow now sits just "
            "before\n        the target. slow.next = slow.next.next deletes it. The dummy node removes the "
            "'deleting the head' edge\n        case. One pass, O(1) space."
        ),
        cx="O(n) time, O(1) space (one pass, gap of n)",
        brute_cx="two passes - compute the length first",
        brute=r"""
# BRUTE FORCE: two passes - compute the length first
def remove_nth_from_end(head, n):
    length, cur = 0, head
    while cur:
        length, cur = length + 1, cur.next
    dummy = ListNode(0, head)
    cur = dummy
    for _ in range(length - n):
        cur = cur.next
    cur.next = cur.next.next
    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space (one pass, gap of n)
# Idea: Two pointers with a fixed gap + dummy head node
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next  # unlink the target
    return dummy.next
""",
    ),
    # ---- Find the Duplicate Number (LeetCode 287) ----
    dict(
        title="Find the Duplicate Number",
        diff="M",
        lc=287,
        slug="find-the-duplicate-number",
        prompt=(
            "An array of n+1 integers holds values in 1..n, with exactly one value repeated (maybe many times). "
            "Find it without modifying the array and using O(1) extra space."
        ),
        sig="def find_duplicate(nums: List[int]) -> int:",
        fn="find_duplicate",
        tests=[
            (([1, 3, 4, 2, 2],), 2),
            (([3, 1, 3, 4, 2],), 3),
            (([1, 1],), 1),
            (([2, 2, 2, 2, 2],), 2),
            (([1, 4, 4, 2, 4],), 4),
        ],
        hints=[
            "Treat index i as a node with an edge i -> nums[i]. What does a repeated value create in that graph?",
            "Two indices pointing to the same node means a CYCLE, and the duplicate is the cycle's entrance.",
            (
                "Floyd: find the meeting point with slow/fast, then restart one pointer from the start; they meet "
                "at the entrance."
            ),
        ],
        pattern="Fast & slow pointers on an implicit linked list (Floyd cycle detection)",
        explain=(
            "Values are in 1..n and there are n+1 slots, so following i -> nums[i] never leaves the array and "
            "must\n        eventually cycle; the node with two incoming edges (the duplicate) is where the cycle "
            "begins.\n        Phase 1 finds a meeting point inside the cycle; phase 2 (one pointer back to start, "
            "both at speed 1)\n        meets exactly at the entrance. O(n) time, O(1) space."
        ),
        cx="O(n) time, O(1) space (Floyd on the array)",
        brute_cx="O(n^2) time (sorting would be O(n log n) but modifies the array)",
        brute=r"""
# BRUTE FORCE: O(n^2) time (sorting would be O(n log n) but modifies the array)
def find_duplicate(nums):
    for i in range(len(nums)):
        if nums[i] in nums[i + 1 :]:
            return nums[i]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space (Floyd on the array)
# Idea: Fast & slow pointers on an implicit linked list (Floyd cycle detection)
def find_duplicate(nums):
    slow = fast = nums[0]
    while True:  # phase 1: meet inside the cycle
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]  # phase 2: walk to the cycle entrance
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow
""",
    ),
    # ---- Reverse Nodes in k-Group (LeetCode 25) ----
    dict(
        title="Reverse Nodes in k-Group",
        diff="H",
        lc=25,
        slug="reverse-nodes-in-k-group",
        prompt=(
            "Reverse a linked list in blocks of k nodes. If fewer than k nodes remain at the end, leave them as "
            "they are."
        ),
        sig="def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:",
        fn="reverse_k_group",
        adapt_in=lambda a: (list_to_ll(a[0]), a[1]),
        adapt_out=ll_to_list,
        tests=[
            (([1, 2, 3, 4, 5], 2), [2, 1, 4, 3, 5]),
            (([1, 2, 3, 4, 5], 3), [3, 2, 1, 4, 5]),
            (([1, 2], 1), [1, 2]),
            (([1, 2, 3, 4], 4), [4, 3, 2, 1]),
            (([1], 2), [1]),
        ],
        hints=[
            "First check that k nodes really exist ahead; if not, stop and attach the rest unchanged.",
            (
                "Reverse exactly k nodes with the standard prev/cur loop, then reconnect the reversed block to the "
                "previous block's tail."
            ),
            (
                "Keep `group_prev` (node before the block). After reversing, the old first node becomes the block's "
                "tail: it is the new group_prev."
            ),
        ],
        pattern="Sub-list reversal with a dummy head and boundary reconnection",
        explain=(
            "Per block: locate the k-th node (kth), remember the node after it (group_next), reverse the k "
            "nodes\n        with prev initialised to group_next (so the block's old head already points to the "
            "rest), then hook\n        group_prev.next to the block's new head. O(n) time, O(1) space."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) extra space - rebuild from a Python list",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) extra space - rebuild from a Python list
def reverse_k_group(head, k):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    for i in range(0, len(vals) - k + 1, k):
        vals[i : i + k] = vals[i : i + k][::-1]
    dummy = tail = ListNode()
    for v in vals:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Sub-list reversal with a dummy head and boundary reconnection
def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        kth = group_prev
        for _ in range(k):  # find the k-th node of this block
            kth = kth.next
            if not kth:
                return dummy.next  # fewer than k left: done
        group_next = kth.next
        prev, cur = group_next, group_prev.next
        while cur is not group_next:  # reverse the block
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        old_first = group_prev.next  # becomes the tail of the reversed block
        group_prev.next = kth
        group_prev = old_first
""",
    ),
]
