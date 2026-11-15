# 08 - Linked lists (pointer surgery & fast/slow)

> **One idea:** a linked list is just "node + arrow". Almost every problem is rewiring arrows without losing the rest of the list.

## 1. First principles
- A node stores `val` and `next`. No random access: reaching index i costs O(i). In exchange, insert/delete at a known node is O(1).
- **Dummy (sentinel) head:** `dummy = ListNode(0, head)` removes all "what if the head changes?" special cases. Return `dummy.next`.
- **Fast & slow pointers:** speed 1 vs 2. The fast one reaches the end when slow is in the middle; inside a cycle fast laps slow, so they must meet.
- **Reverse** = walk with `prev/cur/nxt`, flip each arrow. **Merge** = splice nodes with a tail pointer.

## 2. How to spot it
- Input is a list / "head of a linked list" / an implicit list (index -> value jumps, `nums[i]` as next).
- "middle", "cycle", "k-th from end", "palindrome list", "reorder", "reverse in groups".
- "O(1) extra space".

## 3. Paper recipe (do this on paper, every time)
1. Draw 4-5 boxes with arrows. Label pointers `prev`, `cur`, `nxt` under the boxes.
2. For one iteration, write the assignments **in order** and cross out the old arrow as you overwrite it.
3. Ask: "after this line, can I still reach everything I need?" - save `nxt = cur.next` **before** overwriting `cur.next`.
4. Do the empty list, 1 node, 2 nodes by hand.
5. Use a dummy head whenever the first node might be removed/changed.

## 4. Hand traces
Reverse a list:

`1 -> 2 -> 3`

| step | prev | cur | nxt (saved) | re-wire |
|---|---|---|---|---|
| 1 | None | 1 | 2 | 1.next now -> None |
| 2 | 1 | 2 | 3 | 2.next now -> 1 |
| 3 | 2 | 3 | None | 3.next now -> 2 |

Return `prev` = 3 -> 2 -> 1.

Cycle entrance on an implicit list (Find the Duplicate):

`nums = [1, 3, 4, 2, 2]`; edges: i -> nums[i]  (0->1, 1->3, 2->4, 3->2, 4->2: the cycle is 2->4->2)

| phase | slow | fast |
|---|---|---|
| start | 1 | 1 |
| phase 1 | 3 | 2 |
| phase 1 | 2 | 2 |
| phase 2 reset | 1 | 2 |
| phase 2 | 3 | 4 |
| phase 2 | 2 | 2 |

They meet at **2** = the duplicate.

## 5. Template
*Reference solution for **Reverse Linked List** (`linked_list/1`) - tested by `python dsa.py selftest`:*

```python
# OPTIMISED: O(n) time, O(1) space
# Idea: Pointer re-wiring with prev/cur/next (three-pointer walk)
def reverse_list(head):
    prev, cur = None, head
    while cur:
        nxt = cur.next  # save the rest of the list
        cur.next = prev  # flip the arrow
        prev, cur = cur, nxt
    return prev
```

## 6. Traps
- Losing the tail of the list by overwriting `next` too early.
- Not handling `head is None` / single node.
- Off-by-one in "n-th from the end" (stop `slow` one node *before* the target).
- Creating a cycle accidentally (the last node of a reversed block must point to the rest).
- Floyd phase 2 needs both pointers at speed 1.

## 7. Self-check
1. Why must the two Floyd pointers meet, and why does restarting one from the head find the entrance?
2. Merge two sorted lists: which pointer does the dummy head save you from handling?
3. Palindrome list in O(1) space: which three techniques do you combine?

## 8. Practice ladder
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `linked_list/1` | Easy | Reverse Linked List | [#206](https://leetcode.com/problems/reverse-linked-list/) | Pointer re-wiring with prev/cur/next (three-pointer walk) |
| `linked_list/2` | Easy | Middle of the Linked List | [#876](https://leetcode.com/problems/middle-of-the-linked-list/) | Fast & slow pointers (tortoise and hare) |
| `linked_list/6` | Easy | Merge Two Sorted Lists | [#21](https://leetcode.com/problems/merge-two-sorted-lists/) | Dummy head + tail pointer (merge two sorted sequences) |
| `linked_list/7` | Easy | Linked List Cycle | [#141](https://leetcode.com/problems/linked-list-cycle/) | Floyd's cycle detection (fast & slow pointers) |
| `linked_list/8` | Easy | Palindrome Linked List | [#234](https://leetcode.com/problems/palindrome-linked-list/) | Fast/slow to find the middle + in-place reverse + two-pointer compare |
| `linked_list/12` | Easy | Remove Duplicates from Sorted List | [#83](https://leetcode.com/problems/remove-duplicates-from-sorted-list/) | Single pointer, skip equal neighbours |
| `linked_list/20` | Easy | Remove Linked List Elements | [#203](https://leetcode.com/problems/remove-linked-list-elements/) | Dummy head + delete-after-prev |
| `linked_list/3` | Medium | Remove Nth Node From End of List | [#19](https://leetcode.com/problems/remove-nth-node-from-end-of-list/) | Two pointers with a fixed gap + dummy head node |
| `linked_list/4` | Medium | Find the Duplicate Number | [#287](https://leetcode.com/problems/find-the-duplicate-number/) | Fast & slow pointers on an implicit linked list (Floyd cycle detection) |
| `linked_list/9` | Medium | Add Two Numbers | [#2](https://leetcode.com/problems/add-two-numbers/) | Simulate grade-school addition with a carry |
| `linked_list/10` | Medium | Reorder List | [#143](https://leetcode.com/problems/reorder-list/) | Middle + reverse + interleave merge (compose list primitives) |
| `linked_list/13` | Medium | Reverse Linked List II | [#92](https://leetcode.com/problems/reverse-linked-list-ii/) | Pointer surgery with a dummy head (reverse a sub-segment in place) |
| `linked_list/14` | Medium | Linked List Cycle II | [#142](https://leetcode.com/problems/linked-list-cycle-ii/) | Floyd phase 2: restart one pointer from the head |
| `linked_list/15` | Medium | Swap Nodes in Pairs | [#24](https://leetcode.com/problems/swap-nodes-in-pairs/) | Dummy head + pointer rewiring in fixed-size groups |
| `linked_list/16` | Medium | Rotate List | [#61](https://leetcode.com/problems/rotate-list/) | Make the list circular, then cut it at the right place |
| `linked_list/17` | Medium | Remove Duplicates from Sorted List II | [#82](https://leetcode.com/problems/remove-duplicates-from-sorted-list-ii/) | Dummy head + skip whole runs of equal values |
| `linked_list/18` | Medium | Partition List | [#86](https://leetcode.com/problems/partition-list/) | Split into two lists with dummy heads, then concatenate |
| `linked_list/19` | Medium | Odd Even Linked List | [#328](https://leetcode.com/problems/odd-even-linked-list/) | Two interleaved chains built in one pass, then joined |
| `linked_list/21` | Medium | Add Two Numbers II | [#445](https://leetcode.com/problems/add-two-numbers-ii/) | Stacks to read a list backwards; build the answer by prepending |
| `linked_list/22` | Medium | Sort List | [#148](https://leetcode.com/problems/sort-list/) | Merge sort on a linked list (split with slow/fast, merge with dummy) |
| `linked_list/5` | Hard | Reverse Nodes in k-Group | [#25](https://leetcode.com/problems/reverse-nodes-in-k-group/) | Sub-list reversal with a dummy head and boundary reconnection |
| `linked_list/11` | Hard | Merge k Sorted Lists | [#23](https://leetcode.com/problems/merge-k-sorted-lists/) | Heap of k candidates (k-way merge) |

Start one with `python dsa.py start linked_list/1`.

**More:** 21 Merge Two Sorted Lists (E), 141 Linked List Cycle (E), 142 Linked List Cycle II (M), 160 Intersection of Two Linked Lists (E), 234 Palindrome Linked List (E), 2 Add Two Numbers (M), 143 Reorder List (M), 92 Reverse Linked List II (M), 148 Sort List (M), 138 Copy List with Random Pointer (M), 23 Merge k Sorted Lists (H).

## 9. Make it stay - the teacher's anchors

**Picture it.** A treasure hunt: each clue only tells you where the next one is. If you lose the clue, you lose the rest of the hunt - so save `next` BEFORE you overwrite a pointer.

**The rule in one sentence.** Draw boxes and arrows. Every pointer change = one arrow redrawn; do them in an order that never orphans nodes.

**Why it works.** A singly linked list has no random access, so every technique is about moving pointers cleverly: dummy head (no special cases), fast/slow (find middle/cycle), reverse (read backwards).

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. Why does a dummy head remove edge cases?
2. Prove that fast and slow must meet in a cycle.
3. Where does the cycle start - derive a = L - b?

**Mistakes students make most.**
- Losing the rest of the list by overwriting `next` first.
- Not handling empty/one-node lists.
- Off-by-one in 'n-th from end' (the gap must be n, with a dummy).

**When NOT to use it.** You need random access or length-dependent logic repeatedly - convert to an array first (and say so; interviewers like the trade-off discussion).

**The same idea in disguise.** Reverse -> middle -> palindrome -> reorder list -> reverse k-group; Floyd: cycle -> cycle start -> find the duplicate number -> happy number.
