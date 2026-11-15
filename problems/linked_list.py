from core import *

# Linked-list tests give plain Python lists; adapt_in builds the nodes and adapt_out turns the result back.

PROBLEMS = [
    dict(
        title="Reverse Linked List", diff="E", lc=206, slug="reverse-linked-list",
        prompt="Reverse a singly linked list and return the new head. Do it iteratively in O(1) extra space.",
        sig="def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:",
        fn="reverse_list",
        adapt_in=lambda a: (list_to_ll(a[0]),), adapt_out=ll_to_list,
        tests=[(([1, 2, 3, 4, 5],), [5, 4, 3, 2, 1]), (([1, 2],), [2, 1]), (([],), []), (([7],), [7])],
        hints=["Each node's `next` must end up pointing at the node BEFORE it.",
               "Walk with prev=None, cur=head. Before you overwrite cur.next, what must you save?",
               "nxt = cur.next; cur.next = prev; prev = cur; cur = nxt. Return prev."],
        pattern="Pointer re-wiring with prev/cur/next (three-pointer walk)",
        explain="""
        Draw the arrows on paper: at each step cur.next flips to point backwards. You lose the rest of the
        list the moment you overwrite cur.next, so save it first. When cur falls off the end, prev is the
        new head. O(n) time, O(1) space.""",
        solution=r'''
def reverse_list(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next        # save the rest of the list
        cur.next = prev       # flip the arrow
        prev, cur = cur, nxt
    return prev
''',
    ),
    dict(
        title="Middle of the Linked List", diff="E", lc=876, slug="middle-of-the-linked-list",
        prompt="Return the middle node of a linked list (the second middle if the length is even). "
               "Return the list from that node on.",
        sig="def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:",
        fn="middle_node",
        adapt_in=lambda a: (list_to_ll(a[0]),), adapt_out=ll_to_list,
        tests=[(([1, 2, 3, 4, 5],), [3, 4, 5]), (([1, 2, 3, 4, 5, 6],), [4, 5, 6]), (([1],), [1]), (([1, 2],), [2])],
        hints=["You do not know the length up front. Could you find the middle in one pass?",
               "Two runners: one moves 1 step, the other 2 steps per iteration.",
               "When fast reaches the end (fast is None or fast.next is None), slow is in the middle."],
        pattern="Fast & slow pointers (tortoise and hare)",
        explain="""
        The fast pointer covers twice the distance, so when it finishes the slow one is halfway. This same
        speed difference detects cycles (they must meet) - see Find the Duplicate Number below.""",
        solution=r'''
def middle_node(head):
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
''',
    ),
    dict(
        title="Remove Nth Node From End of List", diff="M", lc=19, slug="remove-nth-node-from-end-of-list",
        prompt="Delete the n-th node counting from the END of a linked list and return the head. One pass preferred.",
        sig="def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:",
        fn="remove_nth_from_end",
        adapt_in=lambda a: (list_to_ll(a[0]), a[1]), adapt_out=ll_to_list,
        tests=[(([1, 2, 3, 4, 5], 2), [1, 2, 3, 5]), (([1], 1), []), (([1, 2], 1), [1]), (([1, 2], 2), [2]),
               (([1, 2, 3], 3), [2, 3])],
        hints=["The n-th from the end is (length - n) from the start - but that needs the length.",
               "Make two pointers n nodes apart; when the front one reaches the end, the back one is where you need to be.",
               "Use a dummy node before head so removing the head needs no special case; stop `slow` at the node BEFORE the one to delete."],
        pattern="Two pointers with a fixed gap + dummy head node",
        explain="""
        Advance `fast` n steps from the dummy, then move both until fast.next is None: slow now sits just before
        the target. slow.next = slow.next.next deletes it. The dummy node removes the 'deleting the head' edge
        case. One pass, O(1) space.""",
        solution=r'''
def remove_nth_from_end(head, n):
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next      # unlink the target
    return dummy.next
''',
    ),
    dict(
        title="Find the Duplicate Number", diff="M", lc=287, slug="find-the-duplicate-number",
        prompt="An array of n+1 integers holds values in 1..n, with exactly one value repeated (maybe many times). "
               "Find it without modifying the array and using O(1) extra space.",
        sig="def find_duplicate(nums: List[int]) -> int:",
        fn="find_duplicate",
        tests=[(([1, 3, 4, 2, 2],), 2), (([3, 1, 3, 4, 2],), 3), (([1, 1],), 1), (([2, 2, 2, 2, 2],), 2),
               (([1, 4, 4, 2, 4],), 4)],
        hints=["Treat index i as a node with an edge i -> nums[i]. What does a repeated value create in that graph?",
               "Two indices pointing to the same node means a CYCLE, and the duplicate is the cycle's entrance.",
               "Floyd: find the meeting point with slow/fast, then restart one pointer from the start; they meet at the entrance."],
        pattern="Fast & slow pointers on an implicit linked list (Floyd cycle detection)",
        explain="""
        Values are in 1..n and there are n+1 slots, so following i -> nums[i] never leaves the array and must
        eventually cycle; the node with two incoming edges (the duplicate) is where the cycle begins.
        Phase 1 finds a meeting point inside the cycle; phase 2 (one pointer back to start, both at speed 1)
        meets exactly at the entrance. O(n) time, O(1) space.""",
        solution=r'''
def find_duplicate(nums):
    slow = fast = nums[0]
    while True:                         # phase 1: meet inside the cycle
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break
    slow = nums[0]                      # phase 2: walk to the cycle entrance
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]
    return slow
''',
    ),
    dict(
        title="Reverse Nodes in k-Group", diff="H", lc=25, slug="reverse-nodes-in-k-group",
        prompt="Reverse a linked list in blocks of k nodes. If fewer than k nodes remain at the end, leave them as they are.",
        sig="def reverse_k_group(head: Optional[ListNode], k: int) -> Optional[ListNode]:",
        fn="reverse_k_group",
        adapt_in=lambda a: (list_to_ll(a[0]), a[1]), adapt_out=ll_to_list,
        tests=[(([1, 2, 3, 4, 5], 2), [2, 1, 4, 3, 5]), (([1, 2, 3, 4, 5], 3), [3, 2, 1, 4, 5]), (([1, 2], 1), [1, 2]),
               (([1, 2, 3, 4], 4), [4, 3, 2, 1]), (([1], 2), [1])],
        hints=["First check that k nodes really exist ahead; if not, stop and attach the rest unchanged.",
               "Reverse exactly k nodes with the standard prev/cur loop, then reconnect the reversed block to the previous block's tail.",
               "Keep `group_prev` (node before the block). After reversing, the old first node becomes the block's tail: it is the new group_prev."],
        pattern="Sub-list reversal with a dummy head and boundary reconnection",
        explain="""
        Per block: locate the k-th node (kth), remember the node after it (group_next), reverse the k nodes
        with prev initialised to group_next (so the block's old head already points to the rest), then hook
        group_prev.next to the block's new head. O(n) time, O(1) space.""",
        solution=r'''
def reverse_k_group(head, k):
    dummy = ListNode(0, head)
    group_prev = dummy
    while True:
        kth = group_prev
        for _ in range(k):                # find the k-th node of this block
            kth = kth.next
            if not kth:
                return dummy.next         # fewer than k left: done
        group_next = kth.next
        prev, cur = group_next, group_prev.next
        while cur is not group_next:      # reverse the block
            nxt = cur.next
            cur.next = prev
            prev, cur = cur, nxt
        old_first = group_prev.next       # becomes the tail of the reversed block
        group_prev.next = kth
        group_prev = old_first
''',
    ),
]
