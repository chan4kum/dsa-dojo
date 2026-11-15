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


def H(a):
    """Turn only the first argument (a plain list) into a linked list; keep the other arguments as they are."""
    return (list_to_ll(a[0]),) + tuple(a[1:])


def M(a):
    """For merge_in_between(list1, a, b, list2): build linked lists from arguments 0 and 3."""
    return (list_to_ll(a[0]), a[1], a[2], list_to_ll(a[3]))


def parts_out(parts):
    """Turn a list of heads (split_list_to_parts) into a list of plain lists."""
    return [ll_to_list(p) for p in parts]


PROBLEMS = [
    # ---- Convert Binary Number in a Linked List to Integer (LeetCode 1290) ----
    dict(
        title="Convert Binary Number in a Linked List to Integer",
        diff="E",
        lc=1290,
        slug="convert-binary-number-in-a-linked-list-to-integer",
        prompt=(
            "Each node holds 0 or 1; the list is a binary number with the most significant bit first. Return its "
            "decimal value."
        ),
        sig="def get_decimal_value(head: Optional[ListNode]) -> int:",
        fn="get_decimal_value",
        adapt_in=H,
        tests=[
            (([1, 0, 1],), 5),
            (([0],), 0),
            (([1],), 1),
            (([1, 0, 0, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0],), 18880),
            (([1, 1, 1],), 7),
        ],
        hints=[
            "You could copy the bits to a string and call int(s, 2).",
            "Reading left to right, each new bit shifts everything so far one place left and adds the bit.",
            "value = value * 2 + node.val - no list or string needed.",
        ],
        pattern="Horner's rule while walking the list",
        explain=(
            "Multiplying by 2 appends a zero bit, so 'value * 2 + bit' extends the number by one bit without "
            "knowing the length in advance."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - collect a bit string, then int(s, 2)",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - collect a bit string, then int(s, 2)
def get_decimal_value(head):
    bits = ""
    while head:
        bits += str(head.val)
        head = head.next
    return int(bits, 2)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Horner's rule while walking the list
def get_decimal_value(head):
    value = 0
    while head:
        value = value * 2 + head.val  # shift left, then add the new bit
        head = head.next
    return value
""",
    ),
    # ---- Delete the Middle Node of a Linked List (LeetCode 2095) ----
    dict(
        title="Delete the Middle Node of a Linked List",
        diff="M",
        lc=2095,
        slug="delete-the-middle-node-of-a-linked-list",
        prompt="Delete the middle node (index floor(n / 2), counting from 0) and return the head.",
        sig="def delete_middle(head: Optional[ListNode]) -> Optional[ListNode]:",
        fn="delete_middle",
        adapt_in=H,
        adapt_out=ll_to_list,
        tests=[
            (([1, 3, 4, 7, 1, 2, 6],), [1, 3, 4, 1, 2, 6]),
            (([1, 2, 3, 4],), [1, 2, 4]),
            (([2, 1],), [2]),
            (([1],), []),
            (([1, 2, 3],), [1, 3]),
        ],
        hints=[
            "You need the node BEFORE the middle, to relink around it.",
            "Fast/slow pointers: fast moves two steps for each of slow's one.",
            (
                "Start slow at a dummy node before the head; when fast reaches the end, slow.next is the middle: "
                "slow.next = slow.next.next."
            ),
        ],
        pattern="Fast and slow pointers with a dummy head",
        explain=(
            "When fast has travelled the whole list, slow has travelled half. Starting slow one node earlier "
            "(dummy) leaves it exactly at the predecessor of the middle."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - copy to a list, delete the index, rebuild",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - copy to a list, delete the index, rebuild
def delete_middle(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    del values[len(values) // 2]
    dummy = tail = ListNode()
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Fast and slow pointers with a dummy head
def delete_middle(head):
    dummy = ListNode(0, head)
    slow, fast = dummy, head
    while fast and fast.next:
        slow = slow.next  # one step
        fast = fast.next.next  # two steps
    slow.next = slow.next.next  # unlink the middle
    return dummy.next
""",
    ),
    # ---- Maximum Twin Sum of a Linked List (LeetCode 2130) ----
    dict(
        title="Maximum Twin Sum of a Linked List",
        diff="M",
        lc=2130,
        slug="maximum-twin-sum-of-a-linked-list",
        prompt=(
            "The list has even length n. The twin of node i is node n - 1 - i. Return the maximum of node + twin "
            "over all nodes."
        ),
        sig="def pair_sum(head: Optional[ListNode]) -> int:",
        fn="pair_sum",
        adapt_in=H,
        tests=[
            (([5, 4, 2, 1],), 6),
            (([4, 2, 2, 3],), 7),
            (([1, 100000],), 100001),
            (([1, 2, 3, 4, 5, 6],), 7),
        ],
        hints=[
            "Copying the values to an array makes twins easy: arr[i] + arr[n-1-i]. That costs O(n) space.",
            "Find the middle with fast/slow pointers and reverse the second half in place.",
            "Walk the first half and the reversed second half together; each pair is a twin pair.",
        ],
        pattern="Find middle + reverse second half",
        explain=(
            "Reversing the back half lines each node up with its twin, so one parallel walk replaces random access."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - copy the values into an array",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - copy the values into an array
def pair_sum(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    n = len(values)
    return max(values[i] + values[n - 1 - i] for i in range(n // 2))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Find middle + reverse second half
def pair_sum(head):
    slow = fast = head
    while fast and fast.next:
        slow, fast = slow.next, fast.next.next  # slow ends at the start of the second half
    prev = None
    while slow:  # reverse the second half in place
        slow.next, prev, slow = prev, slow, slow.next
    best, a, b = 0, head, prev
    while b:
        best = max(best, a.val + b.val)
        a, b = a.next, b.next
    return best
""",
    ),
    # ---- Split Linked List in Parts (LeetCode 725) ----
    dict(
        title="Split Linked List in Parts",
        diff="M",
        lc=725,
        slug="split-linked-list-in-parts",
        prompt=(
            "Split the list into k consecutive parts whose sizes differ by at most 1, with EARLIER parts never "
            "smaller than later ones. Parts may be empty (None). Return the k heads."
        ),
        sig="def split_list_to_parts(head: Optional[ListNode], k: int) -> List[Optional[ListNode]]:",
        fn="split_list_to_parts",
        adapt_in=H,
        adapt_out=parts_out,
        tests=[
            (([1, 2, 3], 5), [[1], [2], [3], [], []]),
            (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 3), [[1, 2, 3, 4], [5, 6, 7], [8, 9, 10]]),
            (([], 3), [[], [], []]),
            (([1, 2], 1), [[1, 2]]),
        ],
        hints=[
            "Count the nodes n first. Every part has n // k nodes, and the first n % k parts get one extra.",
            "For part i the length is n // k + (1 if i < n % k else 0).",
            (
                "Walk that many nodes, remember the next node, set the last node's next to None to cut, and "
                "continue from the remembered node."
            ),
        ],
        pattern="Measure first, then cut the list in place",
        explain=(
            "Knowing n up front fixes every part's size; cutting means setting one next pointer per part, so no "
            "nodes are copied."
        ),
        cx="O(n + k) time",
        brute_cx="O(n + k) time, O(n) space - copy the values out and rebuild each part",
        brute=r"""
# BRUTE FORCE: O(n + k) time, O(n) space - copy the values out and rebuild each part
def split_list_to_parts(head, k):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    size, extra = divmod(len(values), k)
    parts, pos = [], 0
    for i in range(k):
        length = size + (1 if i < extra else 0)
        dummy = tail = ListNode()
        for v in values[pos : pos + length]:
            tail.next = ListNode(v)
            tail = tail.next
        parts.append(dummy.next)
        pos += length
    return parts
""",
        solution=r"""
# OPTIMISED: O(n + k) time
# Idea: Measure first, then cut the list in place
def split_list_to_parts(head, k):
    n, node = 0, head
    while node:
        n += 1
        node = node.next
    size, extra = divmod(n, k)
    parts, node = [], head
    for i in range(k):
        length = size + (1 if i < extra else 0)
        part_head = node
        for _ in range(length - 1):  # stop on the part's last node
            node = node.next
        if node:  # cut the part off from the rest
            node.next, node = None, node.next
        parts.append(part_head)
    return parts
""",
    ),
    # ---- Next Greater Node In Linked List (LeetCode 1019) ----
    dict(
        title="Next Greater Node In Linked List",
        diff="M",
        lc=1019,
        slug="next-greater-node-in-linked-list",
        prompt=(
            "For each node return the value of the first node AFTER it with a strictly larger value, or 0 if there "
            "is none."
        ),
        sig="def next_larger_nodes(head: Optional[ListNode]) -> List[int]:",
        fn="next_larger_nodes",
        adapt_in=H,
        tests=[
            (([2, 1, 5],), [5, 5, 0]),
            (([2, 7, 4, 3, 5],), [7, 0, 5, 5, 0]),
            (([1],), [0]),
            (([3, 3],), [0, 0]),
        ],
        hints=[
            "Brute force: for every node scan the rest of the list - O(n^2).",
            "This is Next Greater Element on an array: copy the values out first.",
            (
                "Keep a stack of indices whose answer is still unknown (values non-increasing); a new bigger value "
                "resolves everything it beats."
            ),
        ],
        pattern="Monotonic stack",
        explain=(
            "Each index is pushed once and popped once, and it is popped exactly when its next greater value arrives."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - scan to the right for each node",
        brute=r"""
# BRUTE FORCE: O(n^2) time - scan to the right for each node
def next_larger_nodes(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    answer = []
    for i, v in enumerate(values):
        answer.append(next((w for w in values[i + 1 :] if w > v), 0))
    return answer
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic stack
def next_larger_nodes(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    answer, stack = [0] * len(values), []  # stack holds indices still waiting for a bigger value
    for i, v in enumerate(values):
        while stack and values[stack[-1]] < v:
            answer[stack.pop()] = v
        stack.append(i)
    return answer
""",
    ),
    # ---- Swapping Nodes in a Linked List (LeetCode 1721) ----
    dict(
        title="Swapping Nodes in a Linked List",
        diff="M",
        lc=1721,
        slug="swapping-nodes-in-a-linked-list",
        prompt=(
            "Swap the VALUES of the k-th node from the beginning and the k-th node from the end (1-indexed). Return "
            "the head."
        ),
        sig="def swap_nodes(head: Optional[ListNode], k: int) -> Optional[ListNode]:",
        fn="swap_nodes",
        adapt_in=H,
        adapt_out=ll_to_list,
        tests=[
            (([1, 2, 3, 4, 5], 2), [1, 4, 3, 2, 5]),
            (([7, 9, 6, 6, 7, 8, 3, 0, 9, 5], 5), [7, 9, 6, 6, 8, 7, 3, 0, 9, 5]),
            (([1], 1), [1]),
            (([1, 2], 1), [2, 1]),
            (([1, 2, 3], 2), [1, 2, 3]),
        ],
        hints=[
            "Finding the k-th from the end normally needs the length: two passes.",
            "One pass: move a pointer k - 1 steps to reach the k-th node from the start.",
            (
                "Then start a second pointer at the head and advance both until the first pointer's next is None - "
                "the second is now the k-th from the end."
            ),
        ],
        pattern="Two pointers with a fixed gap (one pass)",
        explain=(
            "When the lead pointer reaches the last node, the trailing pointer is exactly k - 1 nodes behind it, "
            "i.e. the k-th from the end."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - copy to a list, swap two indices, rebuild",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - copy to a list, swap two indices, rebuild
def swap_nodes(head, k):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    values[k - 1], values[-k] = values[-k], values[k - 1]
    dummy = tail = ListNode()
    for v in values:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two pointers with a fixed gap (one pass)
def swap_nodes(head, k):
    first = head
    for _ in range(k - 1):
        first = first.next  # k-th node from the start
    second, probe = head, first
    while probe.next:  # when probe is on the last node, second is k-th from the end
        probe = probe.next
        second = second.next
    first.val, second.val = second.val, first.val
    return head
""",
    ),
    # ---- Merge Nodes in Between Zeros (LeetCode 2181) ----
    dict(
        title="Merge Nodes in Between Zeros",
        diff="M",
        lc=2181,
        slug="merge-nodes-in-between-zeros",
        prompt=(
            "The list starts and ends with 0 and has no two adjacent zeros. Replace each stretch of non-zero nodes "
            "between two zeros by one node holding their sum; no zeros remain."
        ),
        sig="def merge_nodes(head: Optional[ListNode]) -> Optional[ListNode]:",
        fn="merge_nodes",
        adapt_in=H,
        adapt_out=ll_to_list,
        tests=[
            (([0, 3, 1, 0, 4, 5, 2, 0],), [4, 11]),
            (([0, 1, 0, 3, 0, 2, 2, 0],), [1, 3, 4]),
            (([0, 5, 0],), [5]),
            (([0, 1, 2, 3, 0],), [6]),
        ],
        hints=[
            "Each zero ends one group and starts the next.",
            "Add up values until you hit a zero, then output the running sum and reset it.",
            (
                "In place: reuse each segment's starting zero node as the carrier of the sum, and link the carriers "
                "together."
            ),
        ],
        pattern="Single pass with a running sum (reusing nodes)",
        explain="Zeros are separators; the sum for a group is complete exactly when the next zero arrives.",
        cx="O(n) time, O(1) extra space",
        brute_cx="O(n) time, O(n) space - split values into groups and rebuild",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - split values into groups and rebuild
def merge_nodes(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    sums, total = [], 0
    for v in values[1:]:
        if v == 0:
            sums.append(total)
            total = 0
        else:
            total += v
    dummy = tail = ListNode()
    for s in sums:
        tail.next = ListNode(s)
        tail = tail.next
    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) extra space
# Idea: Single pass with a running sum (reusing nodes)
def merge_nodes(head):
    write = head  # the node currently collecting a sum (it starts as a zero node)
    node = head.next
    while node:
        if node.val == 0:
            if node.next:
                write.next = node  # this zero node carries the next group's sum
                write = node
            else:
                write.next = None  # the final zero ends the list
        else:
            write.val += node.val
        node = node.next
    return head
""",
    ),
    # ---- Linked List Components (LeetCode 817) ----
    dict(
        title="Linked List Components",
        diff="M",
        lc=817,
        slug="linked-list-components",
        prompt=(
            "head holds distinct integers. nums is a subset of those values. Return the number of connected "
            "components of nums, where two values are connected if their nodes are adjacent in the list."
        ),
        sig="def num_components(head: Optional[ListNode], nums: List[int]) -> int:",
        fn="num_components",
        adapt_in=H,
        tests=[
            (([0, 1, 2, 3], [0, 1, 3]), 2),
            (([0, 1, 2, 3, 4], [0, 3, 1, 4]), 2),
            (([0], [0]), 1),
            (([1, 2, 3], [2]), 1),
            (([1, 2, 3, 4], [1, 3]), 2),
        ],
        hints=[
            "A component is a maximal run of consecutive list nodes whose values are all in nums.",
            "Count how many such runs START (or END).",
            "Put nums in a set; walk the list and count nodes that are in the set while the previous node was NOT.",
        ],
        pattern="Hash set + count run starts",
        explain="Counting the beginnings of runs counts the runs. The set makes each membership test O(1).",
        cx="O(n + m) time",
        brute_cx="O(n * m) time - membership tests in a list",
        brute=r"""
# BRUTE FORCE: O(n * m) time - membership tests in a list
def num_components(head, nums):
    count = 0
    while head:
        in_set = head.val in nums  # linear search in a list
        next_in_set = head.next is not None and head.next.val in nums
        if in_set and not next_in_set:
            count += 1  # this node ends a component
        head = head.next
    return count
""",
        solution=r"""
# OPTIMISED: O(n + m) time
# Idea: Hash set + count run starts
def num_components(head, nums):
    wanted = set(nums)
    count, in_run = 0, False
    while head:
        if head.val in wanted:
            if not in_run:
                count += 1  # a new component starts here
            in_run = True
        else:
            in_run = False
        head = head.next
    return count
""",
    ),
    # ---- Merge In Between Linked Lists (LeetCode 1669) ----
    dict(
        title="Merge In Between Linked Lists",
        diff="M",
        lc=1669,
        slug="merge-in-between-linked-lists",
        prompt=(
            "Remove the nodes of list1 from index a to index b (inclusive, 0-indexed) and put all of list2 in their "
            "place. Return list1's head. (1 <= a <= b < len(list1) - 1.)"
        ),
        sig=(
            "def merge_in_between(list1: Optional[ListNode], a: int, b: int, list2: Optional[ListNode]) -> "
            "Optional[ListNode]:"
        ),
        fn="merge_in_between",
        adapt_in=M,
        adapt_out=ll_to_list,
        tests=[
            (([10, 1, 13, 6, 9, 5], 3, 4, [1000000, 1000001, 1000002]), [10, 1, 13, 1000000, 1000001, 1000002, 5]),
            (
                ([0, 1, 2, 3, 4, 5, 6], 2, 5, [1000000, 1000001, 1000002, 1000003, 1000004]),
                [0, 1, 1000000, 1000001, 1000002, 1000003, 1000004, 6],
            ),
            (([1, 2, 3, 4], 1, 2, [9]), [1, 9, 4]),
        ],
        hints=[
            "You need two anchors in list1: the node at index a - 1 and the node at index b + 1.",
            "Also find the tail of list2.",
            "prev.next = list2; list2_tail.next = after. The removed nodes are simply skipped.",
        ],
        pattern="Splice a list between two anchor nodes",
        explain="Three pointer updates reconnect everything; the dropped middle of list1 is never touched.",
        cx="O(len(list1) + len(list2)) time, O(1) space",
        brute_cx="O(n + m) time, O(n + m) space - copy to Python lists, slice and rebuild",
        brute=r"""
# BRUTE FORCE: O(n + m) time, O(n + m) space - copy to Python lists, slice and rebuild
def merge_in_between(list1, a, b, list2):
    one, two = [], []
    while list1:
        one.append(list1.val)
        list1 = list1.next
    while list2:
        two.append(list2.val)
        list2 = list2.next
    merged = one[:a] + two + one[b + 1 :]
    dummy = tail = ListNode()
    for v in merged:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(len(list1) + len(list2)) time, O(1) space
# Idea: Splice a list between two anchor nodes
def merge_in_between(list1, a, b, list2):
    before = list1
    for _ in range(a - 1):
        before = before.next  # node at index a - 1
    after = before
    for _ in range(b - a + 2):
        after = after.next  # node at index b + 1
    before.next = list2
    tail = list2
    while tail.next:
        tail = tail.next
    tail.next = after
    return list1
""",
    ),
    # ---- Find the Minimum and Maximum Number of Nodes Between Critical Points (LeetCode 2058) ----
    dict(
        title="Find the Minimum and Maximum Number of Nodes Between Critical Points",
        diff="M",
        lc=2058,
        slug="find-the-minimum-and-maximum-number-of-nodes-between-critical-points",
        prompt=(
            "A critical point is a node (not the first or last) strictly greater than both neighbours (local "
            "maximum) or strictly smaller than both (local minimum). Return [min distance, max distance] between "
            "any two critical points (distance = difference of indices), or [-1, -1] if there are fewer than two."
        ),
        sig="def nodes_between_critical_points(head: Optional[ListNode]) -> List[int]:",
        fn="nodes_between_critical_points",
        adapt_in=H,
        tests=[
            (([3, 1],), [-1, -1]),
            (([5, 3, 1, 2, 5, 1, 2],), [1, 3]),
            (([1, 3, 2, 2, 3, 2, 2, 2, 7],), [3, 3]),
            (([2, 3, 3, 2],), [-1, -1]),
        ],
        hints=[
            "Walk with three consecutive values (prev, current, next) to classify each inner node.",
            "The maximum distance is last_critical - first_critical.",
            (
                "The minimum distance is the smallest gap between CONSECUTIVE critical points, so remember only the "
                "previous one."
            ),
        ],
        pattern="Single pass remembering first and previous special positions",
        explain=(
            "Extremes of distances between sorted positions are at the ends (max) and between neighbours (min), so "
            "no pairwise comparison is needed."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n + k^2) time, O(n) space - collect critical positions and compare every pair",
        brute=r"""
# BRUTE FORCE: O(n + k^2) time, O(n) space - collect critical positions and compare every pair
def nodes_between_critical_points(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    positions = [
        i
        for i in range(1, len(values) - 1)
        if (values[i] > values[i - 1] and values[i] > values[i + 1])
        or (values[i] < values[i - 1] and values[i] < values[i + 1])
    ]
    if len(positions) < 2:
        return [-1, -1]
    gaps = [
        positions[j] - positions[i]
        for i in range(len(positions))
        for j in range(i + 1, len(positions))
    ]
    return [min(gaps), max(gaps)]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Single pass remembering first and previous special positions
def nodes_between_critical_points(head):
    first = last = -1
    best_min = float("inf")
    prev, node, i = head, head.next, 1
    while node and node.next:
        nxt = node.next
        if (node.val > prev.val and node.val > nxt.val) or (
            node.val < prev.val and node.val < nxt.val
        ):
            if first == -1:
                first = i
            else:
                best_min = min(best_min, i - last)  # gap to the previous critical point
            last = i
        prev, node, i = node, nxt, i + 1
    if first == last:  # zero or one critical point
        return [-1, -1]
    return [best_min, last - first]
""",
    ),
    # ---- Remove Nodes From Linked List (LeetCode 2487) ----
    dict(
        title="Remove Nodes From Linked List",
        diff="M",
        lc=2487,
        slug="remove-nodes-from-linked-list",
        prompt=(
            "Remove every node that has a node with a strictly greater value somewhere to its right. Return the head."
        ),
        sig="def remove_nodes(head: Optional[ListNode]) -> Optional[ListNode]:",
        fn="remove_nodes",
        adapt_in=H,
        adapt_out=ll_to_list,
        tests=[
            (([5, 2, 13, 3, 8],), [13, 8]),
            (([1, 1, 1, 1],), [1, 1, 1, 1]),
            (([5, 4, 3],), [5, 4, 3]),
            (([1, 2, 3],), [3]),
            (([2],), [2]),
        ],
        hints=[
            "A node survives only if no larger value appears after it.",
            "So the survivors form a non-increasing sequence.",
            (
                "Process left to right with a stack: pop every smaller node before pushing the new one; finally "
                "link the stack nodes together."
            ),
        ],
        pattern="Monotonic (non-increasing) stack",
        explain=(
            "A new node with a larger value kills every smaller node still on the stack, since it is 'to their right'."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - for each node scan everything to its right",
        brute=r"""
# BRUTE FORCE: O(n^2) time - for each node scan everything to its right
def remove_nodes(head):
    values = []
    while head:
        values.append(head.val)
        head = head.next
    keep = [v for i, v in enumerate(values) if all(w <= v for w in values[i + 1 :])]
    dummy = tail = ListNode()
    for v in keep:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic (non-increasing) stack
def remove_nodes(head):
    stack, node = [], head
    while node:
        while stack and stack[-1].val < node.val:
            stack.pop()  # a bigger node to the right removes these
        stack.append(node)
        node = node.next
    for left, right in zip(stack, stack[1:]):
        left.next = right
    if stack:
        stack[-1].next = None
    return stack[0] if stack else None
""",
    ),
]
