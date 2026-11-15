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

{{trace:reverse_ll}}

Cycle entrance on an implicit list (Find the Duplicate):

{{trace:floyd}}

## 5. Template
{{solution:linked_list/1}}

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
{{ladder}}

**More:** 21 Merge Two Sorted Lists (E), 141 Linked List Cycle (E), 142 Linked List Cycle II (M), 160 Intersection of Two Linked Lists (E), 234 Palindrome Linked List (E), 2 Add Two Numbers (M), 143 Reorder List (M), 92 Reverse Linked List II (M), 148 Sort List (M), 138 Copy List with Random Pointer (M), 23 Merge k Sorted Lists (H).
