"""more Linked List problems (batch 5) - part of the problem bank for the "linked_list" topic.

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


PROBLEMS = [
    # ---- Double a Number Represented as a Linked List (LeetCode 2816) ----
    dict(
        title="Double a Number Represented as a Linked List",
        diff="M",
        lc=2816,
        slug="double-a-number-represented-as-a-linked-list",
        prompt=(
            "Each node holds one decimal digit; the list is a non-negative number with the most significant digit "
            "FIRST and no leading zeros (except the number 0 itself). Return the head of a list representing that "
            "number multiplied by 2."
        ),
        sig="def double_it(head: Optional[ListNode]) -> Optional[ListNode]:",
        fn="double_it",
        adapt_in=H,
        adapt_out=ll_to_list,
        tests=[
            (([1, 8, 9],), [3, 7, 8]),
            (([9, 9, 9],), [1, 9, 9, 8]),
            (([0],), [0]),
            (([5],), [1, 0]),
            (([4, 9, 5],), [9, 9, 0]),
        ],
        hints=[
            (
                "Doubling is normally done from the least significant digit, but this list starts at the most "
                "significant one."
            ),
            (
                "You could reverse the list, double with a carry, and reverse back. Or notice that the carry INTO a "
                "digit is just 1 when the NEXT digit is 5 or more."
            ),
            (
                "For each node: new digit = (digit * 2) % 10, plus 1 if the next node's digit is >= 5. If the first "
                "digit is >= 5, put a new leading node first."
            ),
        ],
        pattern="Look-ahead carry in a single pass",
        explain=(
            "When you double a digit string, the carry coming from the digit to the right is 1 exactly when that "
            "digit is 5 or more (2 * 5 = 10 and above). So every digit can compute its own result by peeking at the "
            "next node, with no reversing. A leading digit of 5+ overflows into a brand-new first digit. The brute "
            "force turns the list into an integer, doubles it and rebuilds a list."
        ),
        cx="O(n) time, O(1) extra space",
        brute_cx="O(n) time, O(n) space - convert to an integer and back",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - convert to an integer and back
def double_it(head):
    digits = []
    node = head
    while node:
        digits.append(str(node.val))
        node = node.next
    doubled = str(int("".join(digits)) * 2)
    dummy = ListNode(0)
    tail = dummy
    for ch in doubled:
        tail.next = ListNode(int(ch))
        tail = tail.next
    return dummy.next
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) extra space
# Idea: Look-ahead carry in a single pass
def double_it(head):
    if head.val >= 5:
        head = ListNode(0, head)
    node = head
    while node:
        node.val = node.val * 2 % 10
        if node.next and node.next.val >= 5:
            node.val += 1
        node = node.next
    return head
""",
    ),
]
