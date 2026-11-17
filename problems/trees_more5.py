"""more Binary Tree problems (batch 6) - part of the problem bank for the "trees" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
Tests give LeetCode-style level-order lists (None = missing child); adapt_in builds the tree(s) and adapt_out turns a
returned tree back into a list.
"""

from core import list_to_tree, tree_to_list


def T(a):
    """Turn the level-order list in args[0] into a tree; keep the other arguments as they are."""
    return (list_to_tree(a[0]),) + tuple(a[1:])


PROBLEMS = [
    # ---- Second Minimum Node In a Binary Tree (LeetCode 671) ----
    dict(
        title="Second Minimum Node In a Binary Tree",
        diff="E",
        lc=671,
        slug="second-minimum-node-in-a-binary-tree",
        prompt=(
            "Every node of this non-empty tree has either 0 or 2 children, and a node with two children holds the "
            "smaller of its children's values (so the root holds the minimum of the whole tree). Return the second "
            "smallest DISTINCT value in the tree, or -1 if there is none."
        ),
        sig="def find_second_minimum_value(root: Optional[TreeNode]) -> int:",
        fn="find_second_minimum_value",
        adapt_in=T,
        tests=[
            (([2, 2, 5, None, None, 5, 7],), 5),
            (([2, 2, 2],), -1),
            (([5, 8, 5],), 8),
            (([1, 1, 3, 1, 1, 3, 4, 3, 1, 1, 1, 3, 8, 4, 8, 3, 3, 1, 6, 2, 1],), 2),
        ],
        hints=[
            (
                "The root is the overall minimum, so the answer is the smallest value that is strictly bigger than "
                "the root."
            ),
            "You do not have to look at every node: a node's children are never smaller than it.",
            (
                "Walk the tree; the moment a node's value is bigger than the root, record it as a candidate and do "
                "NOT go below it (everything under it is at least as big)."
            ),
        ],
        pattern="Tree traversal with pruning using the heap-like property",
        explain=(
            "The property 'parent = min(children)' means values only grow going down. Any node bigger than the root "
            "is a candidate for the second minimum, and nothing beneath it can beat it, so that branch is cut. "
            "Branches equal to the root are explored further. The brute force collects every value and sorts the "
            "distinct ones."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n log n) time - collect all values, sort the distinct ones",
        brute=r"""
# BRUTE FORCE: O(n log n) time - collect all values, sort the distinct ones
def find_second_minimum_value(root):
    values = set()
    stack = [root]
    while stack:
        node = stack.pop()
        if node:
            values.add(node.val)
            stack.append(node.left)
            stack.append(node.right)
    ordered = sorted(values)
    return ordered[1] if len(ordered) > 1 else -1
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Tree traversal with pruning using the heap-like property
def find_second_minimum_value(root):
    smallest = root.val
    best = -1
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        if node.val > smallest:
            if best == -1 or node.val < best:
                best = node.val
            continue
        stack.append(node.left)
        stack.append(node.right)
    return best
""",
    ),
    # ---- Minimum Distance Between BST Nodes (LeetCode 783) ----
    dict(
        title="Minimum Distance Between BST Nodes",
        diff="E",
        lc=783,
        slug="minimum-distance-between-bst-nodes",
        prompt=(
            "Given the root of a binary search tree with at least two nodes, return the minimum difference between "
            "the values of any two different nodes."
        ),
        sig="def min_diff_in_bst(root: Optional[TreeNode]) -> int:",
        fn="min_diff_in_bst",
        adapt_in=T,
        tests=[
            (([4, 2, 6, 1, 3],), 1),
            (([1, 0, 48, None, None, 12, 49],), 1),
            (([10, 5, 15],), 5),
            (([90, 69, None, 49, 89, None, 52],), 1),
        ],
        hints=[
            "Comparing every pair works but is O(n^2).",
            "In a BST, an inorder walk visits the values in sorted order.",
            (
                "In sorted order the closest pair is always two neighbours, so track the previous value during the "
                "inorder walk and keep the smallest gap."
            ),
        ],
        pattern="Inorder traversal gives sorted order; compare neighbours",
        explain=(
            "The smallest difference between any two numbers in a set is always between two numbers that are "
            "adjacent once sorted. A BST inorder traversal produces that sorted order for free, so one pass with a "
            "'previous value' variable is enough. The brute force compares all pairs."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - compare every pair of values",
        brute=r"""
# BRUTE FORCE: O(n^2) time - compare every pair of values
def min_diff_in_bst(root):
    values = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node:
            values.append(node.val)
            stack.append(node.left)
            stack.append(node.right)
    best = float("inf")
    for i in range(len(values)):
        for j in range(i + 1, len(values)):
            best = min(best, abs(values[i] - values[j]))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Inorder traversal gives sorted order; compare neighbours
def min_diff_in_bst(root):
    best = float("inf")
    prev = None
    stack = []
    node = root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev is not None:
            best = min(best, node.val - prev)
        prev = node.val
        node = node.right
    return best
""",
    ),
    # ---- Binary Tree Pruning (LeetCode 814) ----
    dict(
        title="Binary Tree Pruning",
        diff="M",
        lc=814,
        slug="binary-tree-pruning",
        prompt=(
            "Every node holds 0 or 1. Remove every subtree that does not contain a 1 and return the pruned tree "
            "(possibly empty)."
        ),
        sig="def prune_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:",
        fn="prune_tree",
        adapt_in=T,
        adapt_out=tree_to_list,
        tests=[
            (([1, None, 0, 0, 1],), [1, None, 0, None, 1]),
            (([1, 0, 1, 0, 0, 0, 1],), [1, None, 1, None, 1]),
            (([1, 1, 0, 1, 1, 0, 1, 0],), [1, 1, 0, 1, 1, None, 1]),
            (([0, 0, 0],), []),
            (([0],), []),
        ],
        hints=[
            "A subtree should be kept only if somewhere inside it there is a 1.",
            (
                "Asking 'does this subtree contain a 1?' for every node separately repeats work - the children "
                "already know the answer."
            ),
            "Prune bottom-up: first prune both children, then delete the current node if it became a leaf holding 0.",
        ],
        pattern="Postorder recursion (decide after the children are done)",
        explain=(
            "A node with value 0 is useless exactly when both of its pruned subtrees are empty. Handling the "
            "children first (postorder) lets each node make that decision in O(1). The brute force asks 'is there a "
            "1 below here?' separately at every node, rescanning subtrees each time."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - a fresh subtree scan at every node",
        brute=r"""
# BRUTE FORCE: O(n^2) time - a fresh subtree scan at every node
def prune_tree(root):
    def has_one(node):
        if not node:
            return False
        return node.val == 1 or has_one(node.left) or has_one(node.right)

    def build(node):
        if not node or not has_one(node):
            return None
        node.left = build(node.left)
        node.right = build(node.right)
        return node

    return build(root)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Postorder recursion (decide after the children are done)
def prune_tree(root):
    def prune(node):
        if not node:
            return None
        node.left = prune(node.left)
        node.right = prune(node.right)
        if node.val == 0 and not node.left and not node.right:
            return None
        return node

    return prune(root)
""",
    ),
    # ---- Distribute Coins in Binary Tree (LeetCode 979) ----
    dict(
        title="Distribute Coins in Binary Tree",
        diff="M",
        lc=979,
        slug="distribute-coins-in-binary-tree",
        prompt=(
            "A binary tree has n nodes and n coins in total, spread so that node.val coins sit on each node. In one "
            "move you may push one coin from a node to its parent or to one of its children. Return the minimum "
            "number of moves after which every node holds exactly one coin."
        ),
        sig="def distribute_coins(root: Optional[TreeNode]) -> int:",
        fn="distribute_coins",
        adapt_in=T,
        tests=[
            (([3, 0, 0],), 2),
            (([0, 3, 0],), 3),
            (([1, 0, 2],), 2),
            (([1, 0, 0, None, 3],), 4),
        ],
        hints=[
            "Look at one edge parent-child. How many coins must cross it?",
            (
                "The subtree below the edge holds some coins and needs one per node, so exactly |coins - nodes| "
                "coins must cross, in whichever direction."
            ),
            (
                "Compute for every node the 'excess' of its subtree (coins minus nodes) bottom-up and add up the "
                "absolute excess of each child."
            ),
        ],
        pattern="Postorder excess / flow across each edge",
        explain=(
            "Coins can only cross an edge in a number equal to the imbalance of the subtree below it, and no coin "
            "ever needs to cross an edge in both directions, so the minimum number of moves is the sum over edges "
            "of |excess of the child's subtree|. A postorder pass returns each subtree's excess. The brute force "
            "recomputes the subtree totals for every edge separately."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - recount every subtree from scratch",
        brute=r"""
# BRUTE FORCE: O(n^2) time - recount every subtree from scratch
def distribute_coins(root):
    def totals(node):
        coins = size = 0
        stack = [node]
        while stack:
            current = stack.pop()
            coins += current.val
            size += 1
            for child in (current.left, current.right):
                if child:
                    stack.append(child)
        return coins, size

    moves = 0
    stack = [root]
    while stack:
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                coins, size = totals(child)
                moves += abs(coins - size)
                stack.append(child)
    return moves
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Postorder excess / flow across each edge
def distribute_coins(root):
    moves = 0

    def excess(node):
        nonlocal moves
        if not node:
            return 0
        left = excess(node.left)
        right = excess(node.right)
        moves += abs(left) + abs(right)
        return node.val + left + right - 1

    excess(root)
    return moves
""",
    ),
    # ---- Sum of Root To Leaf Binary Numbers (LeetCode 1022) ----
    dict(
        title="Sum of Root To Leaf Binary Numbers",
        diff="E",
        lc=1022,
        slug="sum-of-root-to-leaf-binary-numbers",
        prompt=(
            "Every node holds 0 or 1. Each root-to-leaf path read from the root is a binary number (most "
            "significant bit first). Return the sum of those numbers over all leaves."
        ),
        sig="def sum_root_to_leaf(root: Optional[TreeNode]) -> int:",
        fn="sum_root_to_leaf",
        adapt_in=T,
        tests=[
            (([1, 0, 1, 0, 1, 0, 1],), 22),
            (([0],), 0),
            (([1, 1],), 3),
            (([1, 0, 1],), 5),
        ],
        hints=[
            "You could write each path as a string and convert it with int(s, 2).",
            "Going one level down shifts the number so far left by one bit and appends the new bit.",
            "Carry value = value * 2 + node.val down the tree; when you reach a leaf, add the value to the total.",
        ],
        pattern="DFS carrying a running value (Horner's rule)",
        explain=(
            "Appending a bit to a binary number is value * 2 + bit, so the number for each path is built while "
            "walking down, without storing the path. At each leaf the finished number is added to the total. The "
            "brute force builds every path as a string and converts it."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n * h) time - build and convert a string per leaf",
        brute=r"""
# BRUTE FORCE: O(n * h) time - build and convert a string per leaf
def sum_root_to_leaf(root):
    total = 0
    stack = [(root, "")]
    while stack:
        node, path = stack.pop()
        path += str(node.val)
        if not node.left and not node.right:
            total += int(path, 2)
        for child in (node.left, node.right):
            if child:
                stack.append((child, path))
    return total
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: DFS carrying a running value (Horner's rule)
def sum_root_to_leaf(root):
    total = 0
    stack = [(root, 0)]
    while stack:
        node, value = stack.pop()
        value = value * 2 + node.val
        if not node.left and not node.right:
            total += value
        else:
            if node.left:
                stack.append((node.left, value))
            if node.right:
                stack.append((node.right, value))
    return total
""",
    ),
    # ---- Binary Search Tree to Greater Sum Tree (LeetCode 1038) ----
    dict(
        title="Binary Search Tree to Greater Sum Tree",
        diff="M",
        lc=1038,
        slug="binary-search-tree-to-greater-sum-tree",
        prompt=(
            "Given a BST with distinct values, replace every node's value by the sum of all values in the tree that "
            "are greater than or equal to it. Return the modified tree."
        ),
        sig="def bst_to_gst(root: Optional[TreeNode]) -> Optional[TreeNode]:",
        fn="bst_to_gst",
        adapt_in=T,
        adapt_out=tree_to_list,
        tests=[
            (([0, None, 1],), [1, None, 1]),
            (([1, 0, 2],), [3, 3, 2]),
            (
                ([4, 1, 6, 0, 2, 5, 7, None, None, None, 3, None, None, None, 8],),
                [30, 36, 21, 36, 35, 26, 15, None, None, None, 33, None, None, None, 8],
            ),
        ],
        hints=[
            "Brute force: for each node, add up every value that is >= its own.",
            "A reverse inorder walk (right, node, left) visits values from largest to smallest.",
            (
                "Keep a running total during that walk: add the node's old value to the total, then store the total "
                "as its new value."
            ),
        ],
        pattern="Reverse inorder traversal with a running sum",
        explain=(
            "'Sum of all values >= v' for the nodes visited from the largest to the smallest is just the running "
            "total of what has been seen so far, including itself. Reverse inorder visits a BST in that descending "
            "order, so the whole conversion is one pass. The brute force rescans all values for each node."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - re-add all larger values for every node",
        brute=r"""
# BRUTE FORCE: O(n^2) time - re-add all larger values for every node
def bst_to_gst(root):
    nodes = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node:
            nodes.append(node)
            stack.append(node.left)
            stack.append(node.right)
    originals = [node.val for node in nodes]
    for node, value in zip(nodes, originals):
        node.val = sum(other for other in originals if other >= value)
    return root
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Reverse inorder traversal with a running sum
def bst_to_gst(root):
    total = 0
    stack = []
    node = root
    while stack or node:
        while node:
            stack.append(node)
            node = node.right
        node = stack.pop()
        total += node.val
        node.val = total
        node = node.left
    return root
""",
    ),
    # ---- Delete Leaves With a Given Value (LeetCode 1325) ----
    dict(
        title="Delete Leaves With a Given Value",
        diff="M",
        lc=1325,
        slug="delete-leaves-with-a-given-value",
        prompt=(
            "Delete every leaf whose value equals target. A node that becomes a leaf because its children were "
            "deleted is also deleted if its value equals target - keep going until no such leaf is left. Return the "
            "new root."
        ),
        sig="def remove_leaf_nodes(root: Optional[TreeNode], target: int) -> Optional[TreeNode]:",
        fn="remove_leaf_nodes",
        adapt_in=T,
        adapt_out=tree_to_list,
        tests=[
            (([1, 2, 3, 2, None, 2, 4], 2), [1, None, 3, None, 4]),
            (([1, 3, 3, 3, 2], 3), [1, 3, None, None, 2]),
            (([1, 2, None, 2, None, 2], 2), [1]),
            (([1, 1, 1], 1), []),
        ],
        hints=[
            "Deleting a leaf can turn its parent into a new leaf - which might also have to go.",
            "That cascade goes from the bottom up, so handle the children BEFORE deciding about the current node.",
            (
                "Recurse: node.left = clean(node.left), node.right = clean(node.right); then if the node is now a "
                "leaf with value target return None, else return the node."
            ),
        ],
        pattern="Postorder recursion that returns the (possibly deleted) subtree",
        explain=(
            "Letting each call return its replacement subtree (or None) makes deletion trivial: the parent just "
            "stores what the child returned. Because children are processed first, a parent sees its new shape and "
            "handles the cascade in one pass. The brute force repeats full scans, removing leaves, until a scan "
            "removes nothing."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n * h) time - repeat full scans until nothing changes",
        brute=r"""
# BRUTE FORCE: O(n * h) time - repeat full scans until nothing changes
def remove_leaf_nodes(root, target):
    changed = True
    while changed:
        changed = False
        if root and not root.left and not root.right and root.val == target:
            return None
        stack = [root] if root else []
        while stack:
            node = stack.pop()
            for side in ("left", "right"):
                child = getattr(node, side)
                if child:
                    if not child.left and not child.right and child.val == target:
                        setattr(node, side, None)
                        changed = True
                    else:
                        stack.append(child)
    return root
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Postorder recursion that returns the (possibly deleted) subtree
def remove_leaf_nodes(root, target):
    def clean(node):
        if not node:
            return None
        node.left = clean(node.left)
        node.right = clean(node.right)
        if not node.left and not node.right and node.val == target:
            return None
        return node

    return clean(root)
""",
    ),
    # ---- Maximum Product of Splitted Binary Tree (LeetCode 1339) ----
    dict(
        title="Maximum Product of Splitted Binary Tree",
        diff="M",
        lc=1339,
        slug="maximum-product-of-splitted-binary-tree",
        prompt=(
            "Remove exactly one edge so the tree splits into two trees. Return the maximum possible product of the "
            "sums of the two parts, modulo 10^9 + 7. (Compare the true products first, take the modulo only at the "
            "end.) The tree has at least two nodes."
        ),
        sig="def max_product(root: Optional[TreeNode]) -> int:",
        fn="max_product",
        adapt_in=T,
        tests=[
            (([1, 2, 3, 4, 5, 6],), 110),
            (([1, None, 2, 3, 4, None, None, 5, 6],), 90),
            (([2, 3, 9, 10, 7, 8, 6, 5, 4, 11, 1],), 1025),
            (([1, 1],), 1),
        ],
        hints=[
            "Cutting the edge above a node splits the tree into that node's subtree and everything else.",
            "If the whole tree sums to total and a subtree sums to s, the product is s * (total - s).",
            (
                "One postorder pass computes every subtree sum (store them in a list); then pick the s that "
                "maximises s * (total - s)."
            ),
        ],
        pattern="Subtree sums via postorder, then maximise over cut points",
        explain=(
            "Every possible cut corresponds to one non-root node, whose subtree sum s gives the product s * (total "
            "- s). A single postorder computes all subtree sums at once (the last one is the total). Comparing real "
            "values and taking the modulo only at the end avoids wrong maximums. The brute force re-sums each "
            "subtree separately."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - sum each subtree from scratch",
        brute=r"""
# BRUTE FORCE: O(n^2) time - sum each subtree from scratch
def max_product(root):
    def subtree_sum(node):
        total = 0
        stack = [node]
        while stack:
            current = stack.pop()
            total += current.val
            for child in (current.left, current.right):
                if child:
                    stack.append(child)
        return total

    whole = subtree_sum(root)
    best = 0
    stack = [root]
    while stack:
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                part = subtree_sum(child)
                best = max(best, part * (whole - part))
                stack.append(child)
    return best % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Subtree sums via postorder, then maximise over cut points
def max_product(root):
    sums = []

    def total(node):
        if not node:
            return 0
        s = node.val + total(node.left) + total(node.right)
        sums.append(s)
        return s

    whole = total(root)
    return max(s * (whole - s) for s in sums) % (10**9 + 7)
""",
    ),
    # ---- Longest ZigZag Path in a Binary Tree (LeetCode 1372) ----
    dict(
        title="Longest ZigZag Path in a Binary Tree",
        diff="M",
        lc=1372,
        slug="longest-zigzag-path-in-a-binary-tree",
        prompt=(
            "A ZigZag path picks a start node and a direction (left or right), moves to that child, then switches "
            "direction at every step. Its length is the number of nodes visited minus one. Return the length of the "
            "longest ZigZag path in the tree."
        ),
        sig="def longest_zig_zag(root: Optional[TreeNode]) -> int:",
        fn="longest_zig_zag",
        adapt_in=T,
        tests=[
            (([1, None, 1, 1, 1, None, None, 1, 1, None, 1, None, None, None, 1],), 3),
            (([1, 1, 1, None, 1, None, None, 1, 1, None, 1],), 4),
            (([1],), 0),
            (([1, 1],), 1),
        ],
        hints=[
            (
                "Brute force: from every node and for both first directions, walk alternating left/right as far as "
                "you can."
            ),
            (
                "Each node only needs two numbers: the longest zigzag starting at it that goes LEFT first, and the "
                "one that goes RIGHT first."
            ),
            (
                "left_first(node) = right_first(node.left) + 1 and right_first(node) = left_first(node.right) + 1; "
                "a missing child gives -1 so a node with no child has length 0."
            ),
        ],
        pattern="Tree DP returning two values per node",
        explain=(
            "Going left from a node, the path must continue by going right from the left child, so the longest "
            "'left-first' zigzag at a node equals 1 + the longest 'right-first' zigzag at its left child (and "
            "symmetrically). Each node combines its children's two numbers in O(1), and the answer is the best "
            "value seen anywhere. The brute force walks the alternating path again from every start."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n * h) time - walk the zigzag from every node in both directions",
        brute=r"""
# BRUTE FORCE: O(n * h) time - walk the zigzag from every node in both directions
def longest_zig_zag(root):
    best = 0
    stack = [root]
    while stack:
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                stack.append(child)
        for first in ("left", "right"):
            current, direction, steps = node, first, 0
            while getattr(current, direction):
                current = getattr(current, direction)
                steps += 1
                direction = "right" if direction == "left" else "left"
            best = max(best, steps)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Tree DP returning two values per node
def longest_zig_zag(root):
    best = 0

    def go(node):
        nonlocal best
        if not node:
            return -1, -1
        left_child = go(node.left)
        right_child = go(node.right)
        left_first = left_child[1] + 1
        right_first = right_child[0] + 1
        best = max(best, left_first, right_first)
        return left_first, right_first

    go(root)
    return best
""",
    ),
    # ---- Pseudo-Palindromic Paths in a Binary Tree (LeetCode 1457) ----
    dict(
        title="Pseudo-Palindromic Paths in a Binary Tree",
        diff="M",
        lc=1457,
        slug="pseudo-palindromic-paths-in-a-binary-tree",
        prompt=(
            "Node values are digits 1-9. A root-to-leaf path is pseudo-palindromic if its values can be REARRANGED "
            "into a palindrome. Return how many root-to-leaf paths are pseudo-palindromic."
        ),
        sig="def pseudo_palindromic_paths(root: Optional[TreeNode]) -> int:",
        fn="pseudo_palindromic_paths",
        adapt_in=T,
        tests=[
            (([2, 3, 1, 3, 1, None, 1],), 2),
            (([2, 1, 1, 1, 3, None, None, None, None, None, 1],), 1),
            (([9],), 1),
            (([1, 2],), 0),
        ],
        hints=[
            (
                "A multiset of values can be rearranged into a palindrome iff at most one value occurs an odd "
                "number of times."
            ),
            "Only the PARITY of each digit's count matters - that is one bit per digit 1..9.",
            (
                "Carry a bitmask down the tree, flipping bit v at each node with XOR; at a leaf the path qualifies "
                "if mask & (mask - 1) == 0 (zero or one bit set)."
            ),
        ],
        pattern="DFS with a parity bitmask",
        explain=(
            "A palindrome arrangement needs every digit to appear an even number of times, except possibly one. "
            "XOR-ing 1 << digit toggles that digit's parity, so the mask records exactly which digits are odd. 'At "
            "most one bit set' is the classic test mask & (mask - 1) == 0. The brute force builds each path and "
            "counts digits with a Counter."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n * h) time - build each path and count its digits",
        brute=r"""
# BRUTE FORCE: O(n * h) time - build each path and count its digits
def pseudo_palindromic_paths(root):
    count = 0
    stack = [(root, [])]
    while stack:
        node, path = stack.pop()
        path = path + [node.val]
        if not node.left and not node.right:
            odd = sum(1 for c in Counter(path).values() if c % 2)
            if odd <= 1:
                count += 1
        for child in (node.left, node.right):
            if child:
                stack.append((child, path))
    return count
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: DFS with a parity bitmask
def pseudo_palindromic_paths(root):
    count = 0
    stack = [(root, 0)]
    while stack:
        node, mask = stack.pop()
        mask ^= 1 << node.val
        if not node.left and not node.right:
            if mask & (mask - 1) == 0:
                count += 1
        else:
            if node.left:
                stack.append((node.left, mask))
            if node.right:
                stack.append((node.right, mask))
    return count
""",
    ),
    # ---- Number of Good Leaf Nodes Pairs (LeetCode 1530) ----
    dict(
        title="Number of Good Leaf Nodes Pairs",
        diff="M",
        lc=1530,
        slug="number-of-good-leaf-nodes-pairs",
        prompt=(
            "A pair of DIFFERENT leaves is good if the length of the shortest path between them (counted in edges) "
            "is at most distance. Return the number of good leaf pairs."
        ),
        sig="def count_pairs(root: Optional[TreeNode], distance: int) -> int:",
        fn="count_pairs",
        adapt_in=T,
        tests=[
            (([1, 2, 3, None, 4], 3), 1),
            (([1, 2, 3, 4, 5, 6, 7], 3), 2),
            (([7, 1, 4, 6, None, 5, 3, None, None, None, None, None, 2], 3), 1),
            (([1, 1, 1], 1), 0),
        ],
        hints=[
            (
                "Any two leaves meet at their lowest common ancestor; the path between them is (depth below it on "
                "one side) + (depth on the other side)."
            ),
            "For each node, keep an array cnt[d] = number of leaves exactly d edges below it, for d up to distance.",
            (
                "At a node, combine the left array and the right array: a pair (i, j) is good if i + j + 2 <= "
                "distance. Then shift both arrays by one (add 1 edge) and merge them for the parent."
            ),
        ],
        pattern="Postorder with distance histograms of leaves",
        explain=(
            "Each good pair is counted once, at the lowest common ancestor of its two leaves, where the left leaf "
            "is i edges below the left child and the right leaf j below the right child, so the distance is i + j + "
            "2. Histograms are capped at the given distance, so each merge costs O(distance^2) and the total is O(n "
            "* distance^2). The brute force finds every pair's distance via their root paths."
        ),
        cx="O(n * distance^2) time, O(n * distance) space",
        brute_cx="O(L^2 * h) time (L leaves) - measure every pair through its root paths",
        brute=r"""
# BRUTE FORCE: O(L^2 * h) time (L leaves) - measure every pair through its root paths
def count_pairs(root, distance):
    paths = []
    stack = [(root, [root])]
    while stack:
        node, path = stack.pop()
        if not node.left and not node.right:
            paths.append(path)
        for child in (node.left, node.right):
            if child:
                stack.append((child, path + [child]))
    total = 0
    for i in range(len(paths)):
        for j in range(i + 1, len(paths)):
            a, b = paths[i], paths[j]
            shared = 0
            while shared < min(len(a), len(b)) and a[shared] is b[shared]:
                shared += 1
            if (len(a) - shared) + (len(b) - shared) <= distance:
                total += 1
    return total
""",
        solution=r"""
# OPTIMISED: O(n * distance^2) time, O(n * distance) space
# Idea: Postorder with distance histograms of leaves
def count_pairs(root, distance):
    total = 0

    def go(node):
        nonlocal total
        if not node:
            return [0] * (distance + 1)
        if not node.left and not node.right:
            leaf = [0] * (distance + 1)
            leaf[0] = 1
            return leaf
        left = go(node.left)
        right = go(node.right)
        for i in range(distance + 1):
            for j in range(distance + 1):
                if i + j + 2 <= distance:
                    total += left[i] * right[j]
        merged = [0] * (distance + 1)
        for i in range(distance):
            merged[i + 1] = left[i] + right[i]
        return merged

    go(root)
    return total
""",
    ),
    # ---- Even Odd Tree (LeetCode 1609) ----
    dict(
        title="Even Odd Tree",
        diff="M",
        lc=1609,
        slug="even-odd-tree",
        prompt=(
            "A tree is Even-Odd if on every EVEN-indexed level (root is level 0) all values are odd and strictly "
            "increasing from left to right, and on every ODD-indexed level all values are even and strictly "
            "decreasing from left to right. Return whether the tree is Even-Odd."
        ),
        sig="def is_even_odd_tree(root: Optional[TreeNode]) -> bool:",
        fn="is_even_odd_tree",
        adapt_in=T,
        tests=[
            (([1, 10, 4, 3, None, 7, 9, 12, 8, 6, None, None, 2],), True),
            (([5, 4, 2, 3, 3, 7],), False),
            (([5, 9, 1, 3, 5, 7],), False),
            (([1],), True),
        ],
        hints=[
            "The rules are about whole levels read left to right, so you need level order.",
            "Process the tree level by level with a queue, remembering the previous value on the current level.",
            (
                "On even levels require odd values and value > previous; on odd levels require even values and "
                "value < previous. Return False at the first violation."
            ),
        ],
        pattern="BFS level by level with a running 'previous' value",
        explain=(
            "A queue visits each level from left to right, so comparing each value with the one just before it on "
            "the same level checks the monotonic rule, and the parity rule depends only on the level number. "
            "Stopping at the first violation keeps it fast. The brute force first collects all levels with a "
            "depth-first walk and then checks each list."
        ),
        cx="O(n) time, O(w) space (w = tree width)",
        brute_cx="O(n) time, O(n) space - gather every level first, then check",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - gather every level first, then check
def is_even_odd_tree(root):
    levels = {}

    def walk(node, depth):
        if not node:
            return
        levels.setdefault(depth, []).append(node.val)
        walk(node.left, depth + 1)
        walk(node.right, depth + 1)

    walk(root, 0)
    for depth, values in levels.items():
        if depth % 2 == 0:
            if any(v % 2 == 0 for v in values):
                return False
            if any(values[i] >= values[i + 1] for i in range(len(values) - 1)):
                return False
        else:
            if any(v % 2 == 1 for v in values):
                return False
            if any(values[i] <= values[i + 1] for i in range(len(values) - 1)):
                return False
    return True
""",
        solution=r"""
# OPTIMISED: O(n) time, O(w) space (w = tree width)
# Idea: BFS level by level with a running 'previous' value
def is_even_odd_tree(root):
    queue = deque([root])
    level = 0
    while queue:
        prev = None
        for _ in range(len(queue)):
            node = queue.popleft()
            v = node.val
            if level % 2 == 0:
                if v % 2 == 0 or (prev is not None and v <= prev):
                    return False
            else:
                if v % 2 == 1 or (prev is not None and v >= prev):
                    return False
            prev = v
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        level += 1
    return True
""",
    ),
    # ---- Kth Largest Sum in a Binary Tree (LeetCode 2583) ----
    dict(
        title="Kth Largest Sum in a Binary Tree",
        diff="M",
        lc=2583,
        slug="kth-largest-sum-in-a-binary-tree",
        prompt=(
            "The level sum is the sum of the values of all nodes on one level. Return the k-th LARGEST level sum "
            "(equal sums count separately), or -1 if the tree has fewer than k levels."
        ),
        sig="def kth_largest_level_sum(root: Optional[TreeNode], k: int) -> int:",
        fn="kth_largest_level_sum",
        adapt_in=T,
        tests=[
            (([5, 8, 9, 2, 1, 3, 7, 4, 6], 2), 13),
            (([1, 2, None, 3], 1), 3),
            (([1, 2, 3], 4), -1),
            (([5], 1), 5),
        ],
        hints=[
            "First compute the sum of every level with a level-order traversal.",
            "Then it is a 'k-th largest in a list' question - sorting all sums works.",
            (
                "To avoid sorting everything, keep a min-heap of size k: push each sum and pop the smallest when "
                "the heap grows past k; the top is the answer if the heap holds k values."
            ),
        ],
        pattern="BFS level sums + size-k min-heap",
        explain=(
            "Level order gives each level's total in one pass. The k-th largest of a stream of numbers is the "
            "smallest value inside a min-heap that keeps only the k biggest so far. If there are fewer than k "
            "levels the heap never fills and the answer is -1. The brute force gathers all sums and sorts them."
        ),
        cx="O(n + L log k) time (L levels), O(w + k) space",
        brute_cx="O(n + L log L) time - sort all level sums",
        brute=r"""
# BRUTE FORCE: O(n + L log L) time - sort all level sums
def kth_largest_level_sum(root, k):
    sums = {}

    def walk(node, depth):
        if not node:
            return
        sums[depth] = sums.get(depth, 0) + node.val
        walk(node.left, depth + 1)
        walk(node.right, depth + 1)

    walk(root, 0)
    ordered = sorted(sums.values(), reverse=True)
    return ordered[k - 1] if len(ordered) >= k else -1
""",
        solution=r"""
# OPTIMISED: O(n + L log k) time (L levels), O(w + k) space
# Idea: BFS level sums + size-k min-heap
def kth_largest_level_sum(root, k):
    heap = []
    queue = deque([root])
    while queue:
        level_sum = 0
        for _ in range(len(queue)):
            node = queue.popleft()
            level_sum += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        heapq.heappush(heap, level_sum)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0] if len(heap) == k else -1
""",
    ),
    # ---- Reverse Odd Levels of Binary Tree (LeetCode 2415) ----
    dict(
        title="Reverse Odd Levels of Binary Tree",
        diff="M",
        lc=2415,
        slug="reverse-odd-levels-of-binary-tree",
        prompt=(
            "The tree is PERFECT (every level is full). Reverse the node VALUES on every odd-numbered level (the "
            "root is level 0) and return the root."
        ),
        sig="def reverse_odd_levels(root: Optional[TreeNode]) -> Optional[TreeNode]:",
        fn="reverse_odd_levels",
        adapt_in=T,
        adapt_out=tree_to_list,
        tests=[
            (([2, 3, 5, 8, 13, 21, 34],), [2, 5, 3, 8, 13, 21, 34]),
            (([7, 13, 11],), [7, 11, 13]),
            (([0, 1, 2, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2],), [0, 2, 1, 0, 0, 0, 0, 2, 2, 2, 2, 1, 1, 1, 1]),
            (([1],), [1]),
        ],
        hints=[
            "Level order gives you each level as a list - reversing the values of a list is easy.",
            (
                "Without lists: in a perfect tree the mirror partner of a node on a level is reached by going "
                "left-then-right paths in opposite order."
            ),
            (
                "Recurse on a pair (a, b) of mirror nodes: on odd levels swap their values, then recurse on "
                "(a.left, b.right) and (a.right, b.left)."
            ),
        ],
        pattern="Mirror-pair recursion on a perfect tree",
        explain=(
            "Reversing a level pairs the i-th node with the i-th from the end, and in a perfect tree those are "
            "exactly the mirror images of each other, which a simultaneous walk on (a, b) with the child pairs "
            "(a.left, b.right) and (a.right, b.left) visits. Swapping values only on odd levels finishes the job in "
            "O(n) with no extra lists. The brute force collects each level into a list and rewrites it reversed."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n) time, O(n) space - gather each level, reverse its values, write them back",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - gather each level, reverse its values, write them back
def reverse_odd_levels(root):
    level = [root]
    depth = 0
    while level and level[0] is not None:
        if depth % 2 == 1:
            values = [node.val for node in level][::-1]
            for node, value in zip(level, values):
                node.val = value
        nxt = []
        for node in level:
            if node.left:
                nxt.append(node.left)
            if node.right:
                nxt.append(node.right)
        level = nxt
        depth += 1
    return root
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Mirror-pair recursion on a perfect tree
def reverse_odd_levels(root):
    def swap(a, b, level):
        if not a:
            return
        if level % 2 == 1:
            a.val, b.val = b.val, a.val
        swap(a.left, b.right, level + 1)
        swap(a.right, b.left, level + 1)

    swap(root.left, root.right, 1)
    return root
""",
    ),
    # ---- Cousins in Binary Tree II (LeetCode 2641) ----
    dict(
        title="Cousins in Binary Tree II",
        diff="M",
        lc=2641,
        slug="cousins-in-binary-tree-ii",
        prompt=(
            "Replace the value of every node by the sum of the values of all its COUSINS (nodes on the same level "
            "that have a different parent). The root has no cousins, so it becomes 0. Return the root."
        ),
        sig="def replace_value_in_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:",
        fn="replace_value_in_tree",
        adapt_in=T,
        adapt_out=tree_to_list,
        tests=[
            (([5, 4, 9, 1, 10, None, 7],), [0, 0, 0, 7, 7, None, 11]),
            (([3, 1, 2],), [0, 0, 0]),
            (([1],), [0]),
            (([1, 2, 3, 4, 5, 6, 7],), [0, 0, 0, 13, 13, 9, 9]),
        ],
        hints=[
            "Cousins = everyone on the level except the node itself and its sibling.",
            (
                "So new value = (sum of the whole level) - (sum of the node and its sibling), and node and sibling "
                "share a parent."
            ),
            (
                "Go level by level. For the next level compute its total first; then for each parent, sum its "
                "children, and give each child level_total - children_sum."
            ),
        ],
        pattern="BFS with level totals and sibling sums",
        explain=(
            "For a node at some level, its cousins are all of that level's nodes minus itself and its sibling, "
            "which are exactly the children of its parent. A BFS sums the next level once, and each parent "
            "subtracts the sum of its own children from that total to get the common new value for them. The brute "
            "force scans the whole level for every node to find the siblings."
        ),
        cx="O(n) time, O(w) space",
        brute_cx="O(n * w) time - scan the level for each node",
        brute=r"""
# BRUTE FORCE: O(n * w) time - scan the level for each node
def replace_value_in_tree(root):
    level = [(root, None)]
    new_values = {}
    while level:
        total = sum(node.val for node, _ in level)
        for node, parent in level:
            siblings = sum(other.val for other, p in level if p is parent)
            new_values[id(node)] = total - siblings
        nxt = []
        nodes = [node for node, _ in level]
        for node in nodes:
            for child in (node.left, node.right):
                if child:
                    nxt.append((child, node))
        level = nxt
    stack = [root]
    while stack:
        node = stack.pop()
        node.val = new_values[id(node)]
        for child in (node.left, node.right):
            if child:
                stack.append(child)
    return root
""",
        solution=r"""
# OPTIMISED: O(n) time, O(w) space
# Idea: BFS with level totals and sibling sums
def replace_value_in_tree(root):
    root.val = 0
    level = [root]
    while level:
        nxt = []
        for node in level:
            for child in (node.left, node.right):
                if child:
                    nxt.append(child)
        total = sum(child.val for child in nxt)
        for node in level:
            children = [c for c in (node.left, node.right) if c]
            siblings = sum(c.val for c in children)
            for c in children:
                c.val = total - siblings
        level = nxt
    return root
""",
    ),
    # ---- Minimum Number of Operations to Sort a Binary Tree by Level (LeetCode 2471) ----
    dict(
        title="Minimum Number of Operations to Sort a Binary Tree by Level",
        diff="M",
        lc=2471,
        slug="minimum-number-of-operations-to-sort-a-binary-tree-by-level",
        prompt=(
            "All node values are distinct. In one operation you may swap the values of ANY two nodes on the same "
            "level. Return the minimum number of operations so that every level, read left to right, is in strictly "
            "increasing order."
        ),
        sig="def minimum_operations(root: Optional[TreeNode]) -> int:",
        fn="minimum_operations",
        adapt_in=T,
        tests=[
            (([1, 4, 3, 7, 6, 8, 5, None, None, None, None, 9, None, 10],), 3),
            (([1, 3, 2, 7, 6, 5, 4],), 3),
            (([1, 2, 3, 4, 5, 6],), 0),
            (([1],), 0),
        ],
        hints=[
            "Levels are independent: sort each level separately and add up the swaps.",
            (
                "Minimum swaps to sort an array of distinct values = n - (number of cycles of the permutation that "
                "sends each element to its sorted position)."
            ),
            "For a level, find each element's target index (rank), then count the cycles with a visited array.",
        ],
        pattern="Level order + minimum swaps to sort (permutation cycles)",
        explain=(
            "Each swap can fix at most one cycle's worth of misplacement: a cycle of length c needs exactly c - 1 "
            "swaps, so the level needs n minus the number of cycles. The ranking of a level's values gives the "
            "permutation. The brute force simulates a selection sort and counts the swaps it makes (each swap puts "
            "one value in its final place, which reaches the same optimum)."
        ),
        cx="O(n log n) time (sorting each level), O(w) space",
        brute_cx="O(n * w) time - simulate selection sort on every level",
        brute=r"""
# BRUTE FORCE: O(n * w) time - simulate selection sort on every level
def minimum_operations(root):
    swaps = 0
    level = [root]
    while level:
        values = [node.val for node in level]
        for i in range(len(values)):
            j = min(range(i, len(values)), key=lambda k: values[k])
            if j != i:
                values[i], values[j] = values[j], values[i]
                swaps += 1
        nxt = []
        for node in level:
            for child in (node.left, node.right):
                if child:
                    nxt.append(child)
        level = nxt
    return swaps
""",
        solution=r"""
# OPTIMISED: O(n log n) time (sorting each level), O(w) space
# Idea: Level order + minimum swaps to sort (permutation cycles)
def minimum_operations(root):
    swaps = 0
    level = [root]
    while level:
        values = [node.val for node in level]
        order = sorted(range(len(values)), key=lambda i: values[i])
        seen = [False] * len(values)
        for start in range(len(values)):
            if seen[start] or order[start] == start:
                continue
            length = 0
            i = start
            while not seen[i]:
                seen[i] = True
                i = order[i]
                length += 1
            swaps += length - 1
        nxt = []
        for node in level:
            for child in (node.left, node.right):
                if child:
                    nxt.append(child)
        level = nxt
    return swaps
""",
    ),
    # ---- Binary Tree Coloring Game (LeetCode 1145) ----
    dict(
        title="Binary Tree Coloring Game",
        diff="M",
        lc=1145,
        slug="binary-tree-coloring-game",
        prompt=(
            "A binary tree has n nodes with distinct values 1..n. Player 1 colours node x red. Player 2 then "
            "colours some other node y blue. After that the players alternate (Player 1 first); on a turn a player "
            "colours an uncoloured node ADJACENT to a node of their own colour (parent or child), and a player who "
            "cannot move passes. The player with more nodes wins. Return True if Player 2 can pick a y that "
            "guarantees a win."
        ),
        sig="def btree_game_winning_move(root: Optional[TreeNode], n: int, x: int) -> bool:",
        fn="btree_game_winning_move",
        adapt_in=T,
        tests=[
            (([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], 11, 3), True),
            (([1, 2, 3], 3, 1), False),
            (([1, 2, 3], 3, 2), True),
            (([1], 1, 1), False),
        ],
        hints=[
            (
                "Removing node x splits the tree into at most three regions: x's left subtree, x's right subtree, "
                "and everything else (the part above x)."
            ),
            (
                "Whatever y Player 2 picks lies in exactly one region and wins that whole region (Player 1 cannot "
                "enter it any sooner)."
            ),
            (
                "So Player 2 should take the largest region; they win if it holds more than n / 2 nodes. Compute "
                "the sizes of x's two subtrees; the third is n - left - right - 1."
            ),
        ],
        pattern="Subtree sizes: the biggest of three regions",
        explain=(
            "Removing x splits the tree into up to three regions. If Player 2 picks the neighbour of x that leads "
            "into a region, Player 1 can only reach that region through x, which is already taken, so Player 2 wins "
            "the whole region. The best choice is the biggest region, and a win needs strictly more than half of "
            "the n nodes. The brute force tries every y and counts the nodes closer to y than to x."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - for each y, count the nodes closer to y than to x",
        brute=r"""
# BRUTE FORCE: O(n^2) time - for each y, count the nodes closer to y than to x
def btree_game_winning_move(root, n, x):
    graph = defaultdict(list)
    stack = [root]
    while stack:
        node = stack.pop()
        for child in (node.left, node.right):
            if child:
                graph[node.val].append(child.val)
                graph[child.val].append(node.val)
                stack.append(child)

    def distances(start):
        dist = {start: 0}
        queue = deque([start])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        return dist

    from_x = distances(x)
    for y in range(1, n + 1):
        if y == x:
            continue
        from_y = distances(y)
        mine = sum(1 for v in range(1, n + 1) if from_y[v] < from_x[v])
        if 2 * mine > n:
            return True
    return False
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Subtree sizes: the biggest of three regions
def btree_game_winning_move(root, n, x):
    sizes = [0, 0]

    def count(node):
        if not node:
            return 0
        left = count(node.left)
        right = count(node.right)
        if node.val == x:
            sizes[0], sizes[1] = left, right
        return 1 + left + right

    count(root)
    biggest = max(sizes[0], sizes[1], n - sizes[0] - sizes[1] - 1)
    return 2 * biggest > n
""",
    ),
    # ---- Construct String from Binary Tree (LeetCode 606) ----
    dict(
        title="Construct String from Binary Tree",
        diff="M",
        lc=606,
        slug="construct-string-from-binary-tree",
        prompt=(
            "Return the preorder string of the tree: each node's value, then its left subtree wrapped in "
            "parentheses, then its right subtree wrapped in parentheses. Leave out every empty pair of parentheses "
            "that is not needed to keep the tree unambiguous - an empty LEFT child is written '()' only when there "
            "is a right child."
        ),
        sig="def tree2str(root: Optional[TreeNode]) -> str:",
        fn="tree2str",
        adapt_in=T,
        tests=[
            (([1, 2, 3, 4],), "1(2(4))(3)"),
            (([1, 2, 3, None, 4],), "1(2()(4))(3)"),
            (([1],), "1"),
            (([1, None, 2],), "1()(2)"),
        ],
        hints=[
            "Preorder: write the node value first, then the children.",
            (
                "A missing right child needs no parentheses at all; a missing left child needs '()' only when a "
                "right child exists."
            ),
            "Recurse: s = str(val); if left or right: s += '(' + go(left) + ')'; if right: s += '(' + go(right) + ')'.",
        ],
        pattern="Preorder recursion with a conditional formatting rule",
        explain=(
            "The string is the preorder with brackets that mark where each subtree starts and ends. A missing right "
            "child is implied by there being no second bracket pair, but a missing left child must be marked by "
            "'()' so the right child is not mistaken for the left. The brute force does the same with an explicit "
            "stack of tokens instead of recursion."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n) time - explicit stack holding nodes and bracket tokens",
        brute=r"""
# BRUTE FORCE: O(n) time - explicit stack holding nodes and bracket tokens
def tree2str(root):
    out = []
    stack = [root]
    while stack:
        item = stack.pop()
        if isinstance(item, str):
            out.append(item)
            continue
        if item is None:
            continue
        out.append(str(item.val))
        if item.right:
            stack.append(")")
            stack.append(item.right)
            stack.append("(")
        if item.left:
            stack.append(")")
            stack.append(item.left)
            stack.append("(")
        elif item.right:
            stack.append(")")
            stack.append("(")
    return "".join(out)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Preorder recursion with a conditional formatting rule
def tree2str(root):
    def go(node):
        if not node:
            return ""
        text = str(node.val)
        if node.left or node.right:
            text += "(" + go(node.left) + ")"
        if node.right:
            text += "(" + go(node.right) + ")"
        return text

    return go(root)
""",
    ),
    # ---- Maximum Sum BST in Binary Tree (LeetCode 1373) ----
    dict(
        title="Maximum Sum BST in Binary Tree",
        diff="H",
        lc=1373,
        slug="maximum-sum-bst-in-binary-tree",
        prompt=(
            "Return the maximum sum of the values of any subtree of the given tree that is also a valid binary "
            "search tree (left values < node < right values, strictly, all the way down). An empty BST has sum 0, "
            "so the answer is never negative."
        ),
        sig="def max_sum_bst(root: Optional[TreeNode]) -> int:",
        fn="max_sum_bst",
        adapt_in=T,
        tests=[
            (([1, 4, 3, 2, 4, 2, 5, None, None, None, None, None, None, 4, 6],), 20),
            (([4, 3, None, 1, 2],), 2),
            (([-4, -2, -5],), 0),
            (([5, 4, 8, 3, None, 6, 3],), 7),
        ],
        hints=[
            (
                "Brute force: for every node test 'is its whole subtree a BST?' (inorder strictly increasing) and "
                "add up its values."
            ),
            (
                "That repeats work. Let each subtree report to its parent four facts: is it a BST, its minimum, its "
                "maximum, and its sum."
            ),
            (
                "A node is a BST root if both children are BSTs, left max < node.val < right min; then its sum is "
                "left + right + val - update the best answer."
            ),
        ],
        pattern="Postorder returning (is_bst, min, max, sum) per subtree",
        explain=(
            "Whether a node roots a BST depends only on whether both child subtrees are BSTs and on the extreme "
            "values on each side, so every node can decide in O(1) from what the children return. The empty subtree "
            "reports min = +infinity and max = -infinity so it never blocks the check. Tracking the largest sum "
            "seen at any valid root gives the answer. The brute force validates each subtree on its own."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - validate and sum every subtree separately",
        brute=r"""
# BRUTE FORCE: O(n^2) time - validate and sum every subtree separately
def max_sum_bst(root):
    best = 0
    nodes = []
    stack = [root]
    while stack:
        node = stack.pop()
        if node:
            nodes.append(node)
            stack.append(node.left)
            stack.append(node.right)
    for top in nodes:
        values = []
        walk = []
        current = top
        while walk or current:
            while current:
                walk.append(current)
                current = current.left
            current = walk.pop()
            values.append(current.val)
            current = current.right
        if all(values[i] < values[i + 1] for i in range(len(values) - 1)):
            best = max(best, sum(values))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Postorder returning (is_bst, min, max, sum) per subtree
def max_sum_bst(root):
    best = 0
    inf = float("inf")

    def go(node):
        nonlocal best
        if not node:
            return True, inf, -inf, 0
        left_ok, left_min, left_max, left_sum = go(node.left)
        right_ok, right_min, right_max, right_sum = go(node.right)
        if left_ok and right_ok and left_max < node.val < right_min:
            total = left_sum + right_sum + node.val
            best = max(best, total)
            return True, min(left_min, node.val), max(right_max, node.val), total
        return False, 0, 0, 0

    go(root)
    return best
""",
    ),
    # ---- Vertical Order Traversal of a Binary Tree (LeetCode 987) ----
    dict(
        title="Vertical Order Traversal of a Binary Tree",
        diff="H",
        lc=987,
        slug="vertical-order-traversal-of-a-binary-tree",
        prompt=(
            "Give the root position (row 0, column 0); a left child is at (row + 1, column - 1) and a right child "
            "at (row + 1, column + 1). Return the nodes grouped by COLUMN from the leftmost to the rightmost "
            "column; within a column, list nodes from top to bottom (smaller row first), and nodes sharing both row "
            "and column in increasing order of value."
        ),
        sig="def vertical_traversal(root: Optional[TreeNode]) -> List[List[int]]:",
        fn="vertical_traversal",
        adapt_in=T,
        tests=[
            (([3, 9, 20, None, None, 15, 7],), [[9], [3, 15], [20], [7]]),
            (([1, 2, 3, 4, 5, 6, 7],), [[4], [2], [1, 5, 6], [3], [7]]),
            (([1, 2, 3, 4, 6, 5, 7],), [[4], [2], [1, 5, 6], [3], [7]]),
            (([1],), [[1]]),
        ],
        hints=[
            "Give every node three numbers: (column, row, value).",
            (
                "Traverse the tree once, recording a triple for each node (the traversal order does not matter if "
                "you sort afterwards)."
            ),
            "Sort all triples by (column, row, value) and group consecutive triples with the same column.",
        ],
        pattern="Coordinates + sort + group",
        explain=(
            "The required order is exactly the lexicographic order of (column, row, value), so recording the "
            "coordinates during any traversal and sorting once gives the answer; grouping by column finishes it. "
            "That is O(n log n) for the sort. The brute force scans all recorded nodes once for each column in the "
            "range and sorts each column's nodes separately."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n * width) time - gather every column separately by scanning all nodes",
        brute=r"""
# BRUTE FORCE: O(n * width) time - gather every column separately by scanning all nodes
def vertical_traversal(root):
    items = []
    stack = [(root, 0, 0)]
    while stack:
        node, row, col = stack.pop()
        items.append((row, col, node.val))
        if node.left:
            stack.append((node.left, row + 1, col - 1))
        if node.right:
            stack.append((node.right, row + 1, col + 1))
    low = min(col for _, col, _ in items)
    high = max(col for _, col, _ in items)
    result = []
    for col in range(low, high + 1):
        in_column = sorted((row, value) for row, c, value in items if c == col)
        result.append([value for _, value in in_column])
    return result
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Coordinates + sort + group
def vertical_traversal(root):
    items = []
    queue = deque([(root, 0, 0)])
    while queue:
        node, row, col = queue.popleft()
        items.append((col, row, node.val))
        if node.left:
            queue.append((node.left, row + 1, col - 1))
        if node.right:
            queue.append((node.right, row + 1, col + 1))
    items.sort()
    result = []
    last_col = None
    for col, _, value in items:
        if col != last_col:
            result.append([])
            last_col = col
        result[-1].append(value)
    return result
""",
    ),
]
