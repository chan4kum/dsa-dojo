"""more Binary Tree problems (batch 4) - part of the problem bank for the "trees" topic.

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


def T2(a):
    """Turn both level-order lists in args into trees."""
    return (list_to_tree(a[0]), list_to_tree(a[1]))


def forest_out(trees):
    """A list of trees -> a list of level-order lists."""
    return [tree_to_list(t) for t in trees]


PROBLEMS = [
    # ---- Binary Tree Inorder Traversal (LeetCode 94) ----
    dict(
        title="Binary Tree Inorder Traversal",
        diff="E",
        lc=94,
        slug="binary-tree-inorder-traversal",
        prompt="Return the inorder traversal (left subtree, node, right subtree) of a binary tree's values.",
        sig="def inorder_traversal(root: Optional[TreeNode]) -> List[int]:",
        fn="inorder_traversal",
        adapt_in=T,
        tests=[
            (([1, None, 2, 3],), [1, 3, 2]),
            (([],), []),
            (([1],), [1]),
            (([1, 2, 3, 4, 5],), [4, 2, 5, 1, 3]),
        ],
        hints=[
            "The recursive version is three lines: left, visit, right.",
            "Recursion uses the call stack. You can use your own stack instead.",
            "Iteratively: push nodes while going left; when you cannot, pop, visit it, then move to its right child.",
        ],
        pattern="Tree traversal with an explicit stack (simulate recursion)",
        explain=(
            "An explicit stack holds the nodes whose left subtree we are still exploring. Popping a node means 'its "
            "left side is finished',\n        so we visit it and then go to the right. Inorder of a BST is sorted, "
            "which makes this a key building block."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n) time, O(h) recursion stack",
        brute=r"""
# BRUTE FORCE: O(n) time, O(h) recursion stack
def inorder_traversal(root):
    if not root:
        return []
    # left subtree first, then this node, then the right subtree
    return inorder_traversal(root.left) + [root.val] + inorder_traversal(root.right)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Tree traversal with an explicit stack (simulate recursion)
def inorder_traversal(root):
    out, stack, node = [], [], root
    while node or stack:
        while node:  # go as far left as possible, remembering the path
            stack.append(node)
            node = node.left
        node = stack.pop()  # nothing left of this node is unvisited
        out.append(node.val)  # visit
        node = node.right  # then explore its right subtree
    return out
""",
    ),
    # ---- Binary Tree Postorder Traversal (LeetCode 145) ----
    dict(
        title="Binary Tree Postorder Traversal",
        diff="E",
        lc=145,
        slug="binary-tree-postorder-traversal",
        prompt="Return the postorder traversal (left subtree, right subtree, node) of a binary tree's values.",
        sig="def postorder_traversal(root: Optional[TreeNode]) -> List[int]:",
        fn="postorder_traversal",
        adapt_in=T,
        tests=[
            (([1, None, 2, 3],), [3, 2, 1]),
            (([],), []),
            (([1],), [1]),
            (([1, 2, 3, 4, 5],), [4, 5, 2, 3, 1]),
        ],
        hints=[
            "Recursion: left, right, then visit. Children are processed before their parent.",
            "Postorder is the REVERSE of 'node, right, left'.",
            (
                "Do an iterative preorder that pushes left then right (so right is popped first), collect values, "
                "and reverse at the end."
            ),
        ],
        pattern="Postorder = reverse of (node, right, left) preorder",
        explain=(
            "A direct iterative postorder is fiddly because you must remember whether you came back from the left "
            "or the right child.\n        The reversal trick turns it into a simple stack loop."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n) time, O(h) recursion stack",
        brute=r"""
# BRUTE FORCE: O(n) time, O(h) recursion stack
def postorder_traversal(root):
    if not root:
        return []
    # both subtrees first, this node last
    return postorder_traversal(root.left) + postorder_traversal(root.right) + [root.val]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Postorder = reverse of (node, right, left) preorder
def postorder_traversal(root):
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.val)  # visits in the order: node, right, left
        if node.left:
            stack.append(node.left)
        if node.right:
            stack.append(node.right)  # pushed last, so popped (visited) first
    return out[::-1]  # reversed: left, right, node
""",
    ),
    # ---- Binary Tree Zigzag Level Order Traversal (LeetCode 103) ----
    dict(
        title="Binary Tree Zigzag Level Order Traversal",
        diff="M",
        lc=103,
        slug="binary-tree-zigzag-level-order-traversal",
        prompt=(
            "Return the level order traversal, but alternate direction: level 0 left-to-right, level 1 "
            "right-to-left, and so on."
        ),
        sig="def zigzag_level_order(root: Optional[TreeNode]) -> List[List[int]]:",
        fn="zigzag_level_order",
        adapt_in=T,
        tests=[
            (([3, 9, 20, None, None, 15, 7],), [[3], [20, 9], [15, 7]]),
            (([1],), [[1]]),
            (([],), []),
            (([1, 2, 3, 4, None, None, 5],), [[1], [3, 2], [4, 5]]),
        ],
        hints=[
            "Start from ordinary level order (BFS, one list per level).",
            "Only the ORDER inside each level changes: every other level is reversed.",
            "Keep a boolean that flips after each level, and reverse that level's list when needed.",
        ],
        pattern="BFS level by level + reverse alternate levels",
        explain=(
            "Process the traversal and the direction separately: BFS gives each level in left-to-right order, and a "
            "toggle decides\n        whether we reverse it before storing. Never reverse the queue itself - "
            "children would come out in the wrong order."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n) time - DFS filling per-depth lists, then reverse the odd depths",
        brute=r"""
# BRUTE FORCE: O(n) time - DFS filling per-depth lists, then reverse the odd depths
def zigzag_level_order(root):
    levels = []

    def dfs(node, depth):  # left-to-right DFS records each level in left-to-right order
        if not node:
            return
        if depth == len(levels):
            levels.append([])
        levels[depth].append(node.val)
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return [lvl[::-1] if d % 2 else lvl for d, lvl in enumerate(levels)]  # reverse every odd level
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: BFS level by level + reverse alternate levels
def zigzag_level_order(root):
    result, level, left_to_right = [], [root] if root else [], True
    while level:
        values = [n.val for n in level]
        result.append(values if left_to_right else values[::-1])
        left_to_right = not left_to_right  # flip direction for the next level
        level = [
            child for n in level for child in (n.left, n.right) if child
        ]  # next level, left to right
    return result
""",
    ),
    # ---- Binary Tree Paths (LeetCode 257) ----
    dict(
        title="Binary Tree Paths",
        diff="E",
        lc=257,
        slug="binary-tree-paths",
        prompt="Return every root-to-leaf path as a string like '1->2->5' (any order).",
        sig="def binary_tree_paths(root: Optional[TreeNode]) -> List[str]:",
        fn="binary_tree_paths",
        compare="unordered",
        adapt_in=T,
        tests=[
            (([1, 2, 3, None, 5],), ["1->2->5", "1->3"]),
            (([1],), ["1"]),
            (([1, 2],), ["1->2"]),
            (([1, 2, 3],), ["1->2", "1->3"]),
        ],
        hints=[
            "A path ends at a LEAF (a node with no children).",
            "Walk down carrying the path so far.",
            (
                "DFS with a shared list `path`: append the value on entry, record the path at a leaf, pop on exit "
                "(backtracking)."
            ),
        ],
        pattern="DFS with a path list that is extended and then undone (backtracking)",
        explain=(
            "Appending to one shared list and popping when we return avoids copying the path at every node. We only "
            "build the string when we actually\n        reach a leaf."
        ),
        cx="O(n * h) time (building the strings), O(h) extra space",
        brute_cx="O(n * h) time - build whole strings by returning lists from the recursion",
        brute=r"""
# BRUTE FORCE: O(n * h) time - build whole strings by returning lists from the recursion
def binary_tree_paths(root):
    def paths(node):  # all paths from this node down to a leaf, as strings
        if not node:
            return []
        if not node.left and not node.right:
            return [str(node.val)]
        return [str(node.val) + "->" + rest for rest in paths(node.left) + paths(node.right)]

    return paths(root)
""",
        solution=r"""
# OPTIMISED: O(n * h) time (building the strings), O(h) extra space
# Idea: DFS with a path list that is extended and then undone (backtracking)
def binary_tree_paths(root):
    result, path = [], []

    def dfs(node):
        if not node:
            return
        path.append(str(node.val))  # step down
        if not node.left and not node.right:
            result.append("->".join(path))  # a leaf: record the whole path
        else:
            dfs(node.left)
            dfs(node.right)
        path.pop()  # step back up (undo)

    dfs(root)
    return result
""",
    ),
    # ---- Count Complete Tree Nodes (LeetCode 222) ----
    dict(
        title="Count Complete Tree Nodes",
        diff="E",
        lc=222,
        slug="count-complete-tree-nodes",
        prompt=(
            "The tree is a complete binary tree (all levels full except possibly the last, which is filled from the "
            "left). Count its nodes faster than O(n)."
        ),
        sig="def count_nodes(root: Optional[TreeNode]) -> int:",
        fn="count_nodes",
        adapt_in=T,
        tests=[
            (([1, 2, 3, 4, 5, 6],), 6),
            (([],), 0),
            (([1],), 1),
            (([1, 2, 3, 4, 5, 6, 7],), 7),
            (([1, 2],), 2),
        ],
        hints=[
            "A PERFECT tree of height h has 2^h - 1 nodes - no counting needed.",
            (
                "In a complete tree, at least one of the two subtrees is perfect. Compare the height of the "
                "leftmost path of each child."
            ),
            (
                "If left height == right height the left subtree is perfect (add 2^h, recurse right); otherwise the "
                "right subtree is perfect (add 2^(h-1), recurse left)."
            ),
        ],
        pattern="Use the tree's structure: one half is always a perfect tree",
        explain=(
            "Counting every node ignores the guarantee. Heights along the left edge are cheap (O(log n)), and they "
            "tell us when a whole\n        subtree is perfect, so each step discards half the tree: O(log n) levels "
            "x O(log n) height = O(log^2 n)."
        ),
        cx="O(log^2 n) time, O(log n) space",
        brute_cx="O(n) time - visit every node",
        brute=r"""
# BRUTE FORCE: O(n) time - visit every node
def count_nodes(root):
    if not root:
        return 0
    return 1 + count_nodes(root.left) + count_nodes(root.right)  # count every node
""",
        solution=r"""
# OPTIMISED: O(log^2 n) time, O(log n) space
# Idea: Use the tree's structure: one half is always a perfect tree
def count_nodes(root):
    def height(node):  # number of nodes on the leftmost path
        h = 0
        while node:
            h += 1
            node = node.left
        return h

    if not root:
        return 0
    left_h, right_h = height(root.left), height(root.right)
    if left_h == right_h:  # left subtree is perfect: 2^left_h - 1 nodes, plus the root = 2^left_h
        return (1 << left_h) + count_nodes(root.right)
    return (1 << right_h) + count_nodes(
        root.left
    )  # right subtree is perfect: 2^right_h - 1, plus the root
""",
    ),
    # ---- Construct Binary Tree from Inorder and Postorder Traversal (LeetCode 106) ----
    dict(
        title="Construct Binary Tree from Inorder and Postorder Traversal",
        diff="M",
        lc=106,
        slug="construct-binary-tree-from-inorder-and-postorder-traversal",
        prompt="Given the inorder and postorder traversals of a binary tree with distinct values, rebuild the tree.",
        sig="def build_tree(inorder: List[int], postorder: List[int]) -> Optional[TreeNode]:",
        fn="build_tree",
        adapt_out=tree_to_list,
        tests=[
            (([9, 3, 15, 20, 7], [9, 15, 7, 20, 3]), [3, 9, 20, None, None, 15, 7]),
            (([-1], [-1]), [-1]),
            (([2, 1], [2, 1]), [1, 2]),
            (([1, 2], [2, 1]), [1, None, 2]),
        ],
        hints=[
            "The LAST element of postorder is the root.",
            (
                "Find that value in inorder: everything left of it is the left subtree, everything right is the "
                "right subtree."
            ),
            (
                "Recurse. Look up positions in a hash map (O(1)) and take roots from the END of postorder - "
                "building the RIGHT subtree first."
            ),
        ],
        pattern="Divide & conquer on traversals: root from one order, split point from the other",
        explain=(
            "Postorder gives the root (last), inorder gives the split. Consuming postorder backwards means each new "
            "root comes out right-subtree\n        first, so no slicing is needed. Same idea as Preorder+Inorder "
            "(root from the FRONT, left subtree first)."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - slice lists and search with index()",
        brute=r"""
# BRUTE FORCE: O(n^2) time - slice lists and search with index()
def build_tree(inorder, postorder):
    if not postorder:
        return None
    root_val = postorder[-1]  # last of postorder is the root
    i = inorder.index(root_val)  # O(n) search; slices copy O(n) too
    root = TreeNode(root_val)
    root.left = build_tree(
        inorder[:i], postorder[:i]
    )  # the first i postorder values are the left subtree
    root.right = build_tree(inorder[i + 1 :], postorder[i:-1])
    return root
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Divide & conquer on traversals: root from one order, split point from the other
def build_tree(inorder, postorder):
    position = {v: i for i, v in enumerate(inorder)}  # value -> index in inorder
    next_root = [len(postorder) - 1]  # we consume postorder from the back

    def build(lo, hi):  # build the subtree for inorder[lo..hi]
        if lo > hi:
            return None
        val = postorder[next_root[0]]
        next_root[0] -= 1
        root = TreeNode(val)
        mid = position[val]
        root.right = build(mid + 1, hi)  # right first: it sits just before the root in postorder
        root.left = build(lo, mid - 1)
        return root

    return build(0, len(inorder) - 1)
""",
    ),
    # ---- Search in a Binary Search Tree (LeetCode 700) ----
    dict(
        title="Search in a Binary Search Tree",
        diff="E",
        lc=700,
        slug="search-in-a-binary-search-tree",
        prompt=(
            "Return the subtree rooted at the node whose value equals val in a BST, or an empty tree if there is none."
        ),
        sig="def search_bst(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:",
        fn="search_bst",
        adapt_in=T,
        adapt_out=tree_to_list,
        tests=[
            (([4, 2, 7, 1, 3], 2), [2, 1, 3]),
            (([4, 2, 7, 1, 3], 5), []),
            (([4, 2, 7, 1, 3], 4), [4, 2, 7, 1, 3]),
            (([], 1), []),
        ],
        hints=[
            "In a BST, everything left of a node is smaller and everything right is larger.",
            "Compare val with the current node to decide which ONE side can contain it.",
            "Loop: if equal return the node, if val is smaller go left, otherwise go right; stop at None.",
        ],
        pattern="BST descent: discard half the tree at every step",
        explain=(
            "The ordering property turns a full tree scan into a single root-to-leaf walk: O(h). For a balanced "
            "tree that is O(log n);\n        for a degenerate (sorted-insert) tree it is O(n)."
        ),
        cx="O(h) time, O(1) space",
        brute_cx="O(n) time - ignore the ordering and look at every node",
        brute=r"""
# BRUTE FORCE: O(n) time - ignore the ordering and look at every node
def search_bst(root, val):
    if not root:
        return None
    if root.val == val:
        return root
    # no use of the BST property: just search both sides
    return search_bst(root.left, val) or search_bst(root.right, val)
""",
        solution=r"""
# OPTIMISED: O(h) time, O(1) space
# Idea: BST descent: discard half the tree at every step
def search_bst(root, val):
    node = root
    while node and node.val != val:
        node = node.left if val < node.val else node.right  # only one side can contain val
    return node
""",
    ),
    # ---- Convert BST to Greater Tree (LeetCode 538) ----
    dict(
        title="Convert BST to Greater Tree",
        diff="M",
        lc=538,
        slug="convert-bst-to-greater-tree",
        prompt=(
            "Replace every node's value by its original value plus the sum of all original values greater than it. "
            "Return the root."
        ),
        sig="def convert_bst(root: Optional[TreeNode]) -> Optional[TreeNode]:",
        fn="convert_bst",
        adapt_in=T,
        adapt_out=tree_to_list,
        tests=[
            (
                ([4, 1, 6, 0, 2, 5, 7, None, None, None, 3, None, None, None, 8],),
                [30, 36, 21, 36, 35, 26, 15, None, None, None, 33, None, None, None, 8],
            ),
            (([0, None, 1],), [1, None, 1]),
            (([2, 0, 3, -4, 1],), [5, 6, 3, 2, 6]),
            (([5],), [5]),
        ],
        hints=[
            "Inorder traversal of a BST visits values in ascending order.",
            "Visit in the REVERSE direction (right, node, left) and you see values from largest to smallest.",
            "Keep a running total of everything seen so far. At each node add the total to it, then update the total.",
        ],
        pattern="Reverse inorder (right, node, left) with a running sum",
        explain=(
            "'Sum of everything larger' is a running total if we walk from the largest value down. Reverse inorder "
            "gives exactly that order,\n        so one pass with one variable replaces an O(n^2) recount per node."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - for each node add up all larger values",
        brute=r"""
# BRUTE FORCE: O(n^2) time - for each node add up all larger values
def convert_bst(root):
    nodes = []

    def collect(node):  # gather every node
        if node:
            nodes.append(node)
            collect(node.left)
            collect(node.right)

    collect(root)
    originals = [n.val for n in nodes]  # remember the ORIGINAL values
    for node, old in zip(nodes, originals):
        node.val = old + sum(v for v in originals if v > old)  # add everything larger
    return root
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Reverse inorder (right, node, left) with a running sum
def convert_bst(root):
    total = 0  # sum of all values larger than the current node

    def visit(node):
        nonlocal total
        if not node:
            return
        visit(node.right)  # larger values first
        total += node.val
        node.val = total  # own value + everything larger
        visit(node.left)

    visit(root)
    return root
""",
    ),
    # ---- Path Sum II (LeetCode 113) ----
    dict(
        title="Path Sum II",
        diff="M",
        lc=113,
        slug="path-sum-ii",
        prompt="Return every root-to-leaf path whose node values add up to target_sum (as lists of values, any order).",
        sig="def path_sum(root: Optional[TreeNode], target_sum: int) -> List[List[int]]:",
        fn="path_sum",
        compare="unordered",
        adapt_in=T,
        tests=[
            (([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22), [[5, 4, 11, 2], [5, 8, 4, 5]]),
            (([1, 2, 3], 5), []),
            (([1, 2], 0), []),
            (([1, 2], 3), [[1, 2]]),
            (([], 0), []),
        ],
        hints=[
            "Path Sum I asked 'does one exist'; now you must collect them all.",
            "Walk down with the remaining sum (target minus what you have used) and the current path.",
            "At a leaf with remaining == 0, copy the path into the answer. Backtrack with path.pop() on the way up.",
        ],
        pattern="DFS + backtracking with a remaining-sum parameter",
        explain=(
            "Passing `remaining` down means no re-adding. Only copy the path (list(path)) when you record a result "
            "- copying earlier\n        would cost O(h) at every node."
        ),
        cx="O(n * h) time, O(h) space",
        brute_cx="O(n * h) time - list every root-to-leaf path first, then filter by sum",
        brute=r"""
# BRUTE FORCE: O(n * h) time - list every root-to-leaf path first, then filter by sum
def path_sum(root, target_sum):
    all_paths = []

    def walk(node, path):  # collect EVERY root-to-leaf path
        if not node:
            return
        path = path + [node.val]  # a new list per node (simple but wasteful)
        if not node.left and not node.right:
            all_paths.append(path)
        walk(node.left, path)
        walk(node.right, path)

    walk(root, [])
    return [p for p in all_paths if sum(p) == target_sum]  # keep the ones that add up
""",
        solution=r"""
# OPTIMISED: O(n * h) time, O(h) space
# Idea: DFS + backtracking with a remaining-sum parameter
def path_sum(root, target_sum):
    result, path = [], []

    def dfs(node, remaining):
        if not node:
            return
        path.append(node.val)
        remaining -= node.val
        if not node.left and not node.right and remaining == 0:
            result.append(list(path))  # copy: `path` keeps changing
        dfs(node.left, remaining)
        dfs(node.right, remaining)
        path.pop()  # backtrack

    dfs(root, target_sum)
    return result
""",
    ),
    # ---- Sum of Left Leaves (LeetCode 404) ----
    dict(
        title="Sum of Left Leaves",
        diff="E",
        lc=404,
        slug="sum-of-left-leaves",
        prompt="Return the sum of all LEFT leaves: leaves that are the left child of their parent.",
        sig="def sum_of_left_leaves(root: Optional[TreeNode]) -> int:",
        fn="sum_of_left_leaves",
        adapt_in=T,
        tests=[
            (([3, 9, 20, None, None, 15, 7],), 24),
            (([1],), 0),
            (([1, 2],), 2),
            (([1, None, 2],), 0),
            (([],), 0),
        ],
        hints=[
            "A leaf is a node with no children. It is a LEFT leaf only if its parent reaches it through .left.",
            "A node cannot know whether it is a left child - but its parent can check.",
            (
                "At each node: if node.left is a leaf add its value, otherwise recurse into node.left; always "
                "recurse into node.right."
            ),
        ],
        pattern="Look at the child from the parent (or pass an is_left flag down)",
        explain=(
            "Information about 'which side am I on' comes from the parent. Either test node.left from the parent or "
            "pass a boolean down."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n) time - gather (node, is_left) pairs first, then sum",
        brute=r"""
# BRUTE FORCE: O(n) time - gather (node, is_left) pairs first, then sum
def sum_of_left_leaves(root):
    pairs = []  # (node, is_left_child) for every node

    def collect(node, is_left):
        if node:
            pairs.append((node, is_left))
            collect(node.left, True)
            collect(node.right, False)

    collect(root, False)
    return sum(n.val for n, is_left in pairs if is_left and not n.left and not n.right)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Look at the child from the parent (or pass an is_left flag down)
def sum_of_left_leaves(root):
    if not root:
        return 0
    total = 0
    if root.left and not root.left.left and not root.left.right:
        total += root.left.val  # the left child is a leaf
    else:
        total += sum_of_left_leaves(root.left)
    return total + sum_of_left_leaves(root.right)
""",
    ),
    # ---- Merge Two Binary Trees (LeetCode 617) ----
    dict(
        title="Merge Two Binary Trees",
        diff="E",
        lc=617,
        slug="merge-two-binary-trees",
        prompt=(
            "Overlay two binary trees: where both have a node, add the values; where only one has a node, use it. "
            "Return the merged tree."
        ),
        sig="def merge_trees(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> Optional[TreeNode]:",
        fn="merge_trees",
        adapt_in=T2,
        adapt_out=tree_to_list,
        tests=[
            (([1, 3, 2, 5], [2, 1, 3, None, 4, None, 7]), [3, 4, 5, 5, 4, None, 7]),
            (([1], [1, 2]), [2, 2]),
            (([], [1]), [1]),
            (([], []), []),
        ],
        hints=[
            "Walk both trees at the same position at the same time.",
            "If one of the two nodes is missing, the answer for that whole subtree is simply the other one.",
            "Otherwise create a node with the summed value and merge the left children and the right children.",
        ],
        pattern="Parallel DFS over two trees",
        explain=(
            "Recursing on two trees at once is the common pattern in Same Tree, Subtree and Symmetric Tree. Reusing "
            "the existing subtree when the other is\n        missing saves work."
        ),
        cx="O(min(n, m)) time, O(h) space",
        brute_cx="O(n + m) time - record values by position path, then rebuild",
        brute=r"""
# BRUTE FORCE: O(n + m) time - record values by position path, then rebuild
def merge_trees(root1, root2):
    total = {}  # position path ("", "L", "LR", ...) -> summed value

    def record(node, path):
        if node:
            total[path] = total.get(path, 0) + node.val
            record(node.left, path + "L")
            record(node.right, path + "R")

    record(root1, "")
    record(root2, "")

    def build(path):  # rebuild a tree from the position table
        if path not in total:
            return None
        node = TreeNode(total[path])
        node.left = build(path + "L")
        node.right = build(path + "R")
        return node

    return build("")
""",
        solution=r"""
# OPTIMISED: O(min(n, m)) time, O(h) space
# Idea: Parallel DFS over two trees
def merge_trees(root1, root2):
    if not root1:
        return root2  # nothing to add: reuse the other subtree as it is
    if not root2:
        return root1
    root1.val += root2.val  # overlap: add the values
    root1.left = merge_trees(root1.left, root2.left)
    root1.right = merge_trees(root1.right, root2.right)
    return root1
""",
    ),
    # ---- Average of Levels in Binary Tree (LeetCode 637) ----
    dict(
        title="Average of Levels in Binary Tree",
        diff="E",
        lc=637,
        slug="average-of-levels-in-binary-tree",
        prompt="Return the average value of the nodes on each level, from the root level downwards.",
        sig="def average_of_levels(root: Optional[TreeNode]) -> List[float]:",
        fn="average_of_levels",
        adapt_in=T,
        tests=[
            (([3, 9, 20, None, None, 15, 7],), [3.0, 14.5, 11.0]),
            (([3, 9, 20, 15, 7],), [3.0, 14.5, 11.0]),
            (([1],), [1.0]),
            (([],), []),
        ],
        hints=[
            "You need every value on a level together: that is a level-order (BFS) job.",
            "Process the queue one level at a time: the queue length at the start of a level is that level's size.",
            "Sum the level's values while pushing children, then append sum / size.",
        ],
        pattern="BFS level by level",
        explain=(
            "Freezing the queue size at the start of each level lets one loop handle 'all nodes of this level' "
            "without storing level numbers."
        ),
        cx="O(n) time, O(w) space (w = widest level)",
        brute_cx="O(n) time - DFS collecting every value per depth, then average",
        brute=r"""
# BRUTE FORCE: O(n) time - DFS collecting every value per depth, then average
def average_of_levels(root):
    by_depth = []

    def dfs(node, depth):  # file every value under its depth
        if not node:
            return
        if depth == len(by_depth):
            by_depth.append([])
        by_depth[depth].append(node.val)
        dfs(node.left, depth + 1)
        dfs(node.right, depth + 1)

    dfs(root, 0)
    return [sum(values) / len(values) for values in by_depth]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(w) space (w = widest level)
# Idea: BFS level by level
def average_of_levels(root):
    result, queue = [], deque([root] if root else [])
    while queue:
        size = len(queue)  # exactly the nodes of the current level
        total = 0
        for _ in range(size):
            node = queue.popleft()
            total += node.val
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(total / size)
    return result
""",
    ),
    # ---- Maximum Width of Binary Tree (LeetCode 662) ----
    dict(
        title="Maximum Width of Binary Tree",
        diff="M",
        lc=662,
        slug="maximum-width-of-binary-tree",
        prompt=(
            "The width of a level is the distance between its leftmost and rightmost non-empty nodes, counting the "
            "empty positions in between. Return the maximum width over all levels."
        ),
        sig="def width_of_binary_tree(root: Optional[TreeNode]) -> int:",
        fn="width_of_binary_tree",
        adapt_in=T,
        tests=[
            (([1, 3, 2, 5, 3, None, 9],), 4),
            (([1, 3, 2, 5, None, None, 9, 6, None, 7],), 7),
            (([1, 3, 2, 5],), 2),
            (([1],), 1),
            (([],), 0),
        ],
        hints=[
            "Pretend the tree is complete and give each node an index: root = 0, children of i are 2i and 2i + 1.",
            "The width of a level is (last index - first index + 1).",
            "Do BFS keeping (node, index). Subtract the level's first index from the others if the numbers get huge.",
        ],
        pattern="BFS with heap-style position numbering",
        explain=(
            "Numbering nodes like a binary heap preserves gaps: a missing node still 'uses up' an index. So the "
            "width is just a subtraction\n        of two indices - there is no need to materialise the empty slots."
        ),
        cx="O(n) time, O(w) space",
        brute_cx="O(2^depth) time - fill every empty slot with None explicitly",
        brute=r"""
# BRUTE FORCE: O(2^depth) time - fill every empty slot with None explicitly
def width_of_binary_tree(root):
    best = 0
    level = [root]  # includes explicit None placeholders for empty positions
    while any(level):
        first = next(i for i, node in enumerate(level) if node)  # trim leading and trailing empties
        last = len(level) - 1 - next(i for i, node in enumerate(reversed(level)) if node)
        best = max(best, last - first + 1)
        nxt = []
        for node in level[first : last + 1]:
            nxt += (
                [node.left, node.right] if node else [None, None]
            )  # placeholders keep positions aligned
        level = nxt
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(w) space
# Idea: BFS with heap-style position numbering
def width_of_binary_tree(root):
    if not root:
        return 0
    best, level = 0, [(root, 0)]  # (node, position index like a heap)
    while level:
        best = max(
            best, level[-1][1] - level[0][1] + 1
        )  # span from first to last occupied position
        base = level[0][1]  # re-base indices so they stay small
        nxt = []
        for node, idx in level:
            idx -= base
            if node.left:
                nxt.append((node.left, 2 * idx))
            if node.right:
                nxt.append((node.right, 2 * idx + 1))
        level = nxt
    return best
""",
    ),
    # ---- Longest Univalue Path (LeetCode 687) ----
    dict(
        title="Longest Univalue Path",
        diff="M",
        lc=687,
        slug="longest-univalue-path",
        prompt=(
            "Return the length (number of EDGES) of the longest path in the tree in which every node has the same "
            "value. The path need not pass through the root."
        ),
        sig="def longest_univalue_path(root: Optional[TreeNode]) -> int:",
        fn="longest_univalue_path",
        adapt_in=T,
        tests=[
            (([5, 4, 5, 1, 1, None, 5],), 2),
            (([1, 4, 5, 4, 4, None, 5],), 2),
            (([],), 0),
            (([1, 1, 1, 1, 1, 1, 1],), 4),
            (([1],), 0),
        ],
        hints=[
            "Same shape as Diameter of Binary Tree, but a branch only counts if it has the same value.",
            (
                "Let go(node) = longest downward same-value path that STARTS at node. Extend a child's answer only "
                "if the child has node's value."
            ),
            (
                "At each node the best path through it is (left arm) + (right arm). Update a global best with that, "
                "and return the longer arm upward."
            ),
        ],
        pattern="DFS returning the best 'arm', global answer combines two arms (diameter pattern)",
        explain=(
            "'Best path through a node' = two downward arms, but a function can only return ONE arm to its parent. "
            "So return the longer arm and\n        record the sum of both arms in a variable outside the recursion."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - recompute the downward run from every node",
        brute=r"""
# BRUTE FORCE: O(n^2) time - recompute the downward run from every node
def longest_univalue_path(root):
    def down(node, val):  # longest downward run of value `val` starting at this node
        if not node or node.val != val:
            return 0
        return 1 + max(down(node.left, val), down(node.right, val))

    best = 0

    def visit(node):
        nonlocal best
        if not node:
            return
        # the best path whose top node is `node`: left run + right run
        best = max(best, down(node.left, node.val) + down(node.right, node.val))
        visit(node.left)
        visit(node.right)

    visit(root)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: DFS returning the best 'arm', global answer combines two arms (diameter pattern)
def longest_univalue_path(root):
    best = 0

    def arm(node):  # longest same-value downward path (in edges) starting at node
        nonlocal best
        if not node:
            return 0
        left, right = arm(node.left), arm(node.right)
        left = (
            left + 1 if node.left and node.left.val == node.val else 0
        )  # extend only through equal values
        right = right + 1 if node.right and node.right.val == node.val else 0
        best = max(best, left + right)  # a path may use both arms
        return max(left, right)  # but only one arm can be passed up

    arm(root)
    return best
""",
    ),
    # ---- Binary Tree Cameras (LeetCode 968) ----
    dict(
        title="Binary Tree Cameras",
        diff="H",
        lc=968,
        slug="binary-tree-cameras",
        prompt=(
            "A camera on a node watches that node, its parent and its children. Return the minimum number of "
            "cameras needed to watch every node."
        ),
        sig="def min_camera_cover(root: Optional[TreeNode]) -> int:",
        fn="min_camera_cover",
        adapt_in=T,
        tests=[
            (([0, 0, None, 0, 0],), 1),
            (([0, 0, None, 0, None, 0, None, None, 0],), 2),
            (([0],), 1),
            (([0, 0, 0],), 1),
            (([],), 0),
        ],
        hints=[
            "Decide from the BOTTOM: leaves should not hold cameras - their parent covers more.",
            "Give each node a state: 0 = not watched, 1 = watched (no camera), 2 = has a camera.",
            (
                "If any child is state 0, this node must have a camera. If any child has a camera, this node is "
                "watched. Otherwise it is unwatched (its parent will deal with it). Handle an unwatched root at the "
                "end."
            ),
        ],
        pattern="Tree DP / greedy bottom-up with 3 states",
        explain=(
            "Placing a camera on the PARENT of a leaf is never worse than on the leaf, because it covers the leaf, "
            "the parent and the grandparent.\n        Working bottom-up and delaying cameras as long as possible "
            "makes the greedy choice safe."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(2^n * n) time - try every set of camera positions by size",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - try every set of camera positions by size
def min_camera_cover(root):
    nodes, parent = [], {}

    def walk(node, par):  # list every node and remember its parent
        if node:
            nodes.append(node)
            parent[node] = par
            walk(node.left, node)
            walk(node.right, node)

    walk(root, None)
    for size in range(len(nodes) + 1):  # try 0 cameras, then 1, then 2, ...
        for chosen in itertools.combinations(nodes, size):
            watched = set()
            for n in chosen:
                watched |= {
                    n,
                    n.left,
                    n.right,
                    parent[n],
                }  # a camera watches itself, children and parent
            if all(n in watched for n in nodes):
                return size
    return 0
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Tree DP / greedy bottom-up with 3 states
def min_camera_cover(root):
    cameras = 0

    def state(node):  # 0 = not watched, 1 = watched without camera, 2 = has a camera
        nonlocal cameras
        if not node:
            return 1  # an empty child needs nothing
        left, right = state(node.left), state(node.right)
        if left == 0 or right == 0:
            cameras += 1  # a child is unwatched: this node needs a camera
            return 2
        if left == 2 or right == 2:
            return 1  # a child has a camera, so we are watched
        return 0  # both children are watched but cannot see us

    if state(root) == 0:
        cameras += 1  # the root itself is unwatched
    return cameras
""",
    ),
    # ---- Delete Nodes And Return Forest (LeetCode 1110) ----
    dict(
        title="Delete Nodes And Return Forest",
        diff="M",
        lc=1110,
        slug="delete-nodes-and-return-forest",
        prompt=(
            "Delete every node whose value is in to_delete. The remaining nodes form a forest; return the roots of "
            "its trees (any order)."
        ),
        sig="def del_nodes(root: Optional[TreeNode], to_delete: List[int]) -> List[Optional[TreeNode]]:",
        fn="del_nodes",
        compare="unordered",
        adapt_in=T,
        adapt_out=forest_out,
        tests=[
            (([1, 2, 3, 4, 5, 6, 7], [3, 5]), [[1, 2, None, 4], [6], [7]]),
            (([1, 2, 4, None, 3], [3]), [[1, 2, 4]]),
            (([1], [1]), []),
            (([1, 2, 3], [2]), [[1, None, 3]]),
        ],
        hints=[
            (
                "A node becomes a new root exactly when its parent was deleted (or it is the original root) and it "
                "is not deleted itself."
            ),
            "Use a set for to_delete so membership is O(1).",
            (
                "Post-style DFS: pass 'my parent was deleted' down; return None for a deleted node so its parent "
                "unlinks it."
            ),
        ],
        pattern="DFS that returns the node (or None) so the parent can re-link",
        explain=(
            "Returning 'the subtree after cleanup' from each call lets the parent do `node.left = dfs(node.left)` "
            "and unlink deleted children\n        automatically. The flag passed downward tells a node whether it "
            "starts a new tree."
        ),
        cx="O(n) time, O(h + d) space",
        brute_cx="O(n) time - two passes: find the roots, then cut the links",
        brute=r"""
# BRUTE FORCE: O(n) time - two passes: find the roots, then cut the links
def del_nodes(root, to_delete):
    gone = set(to_delete)
    nodes, parent = [], {}

    def walk(node, par):  # pass 1: list nodes (parents first) and remember each parent
        if node:
            nodes.append(node)
            parent[node] = par
            walk(node.left, node)
            walk(node.right, node)

    walk(root, None)
    roots = [n for n in nodes if n.val not in gone and (parent[n] is None or parent[n].val in gone)]
    for n in nodes:  # pass 2: cut every link that points at a deleted node
        if n.left and n.left.val in gone:
            n.left = None
        if n.right and n.right.val in gone:
            n.right = None
    return roots
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h + d) space
# Idea: DFS that returns the node (or None) so the parent can re-link
def del_nodes(root, to_delete):
    gone = set(to_delete)
    forest = []

    def dfs(node, is_root):  # returns the node to keep as this child (None if deleted)
        if not node:
            return None
        deleted = node.val in gone
        if is_root and not deleted:
            forest.append(node)  # a surviving node with no surviving parent starts a new tree
        node.left = dfs(node.left, deleted)  # children of a deleted node become roots
        node.right = dfs(node.right, deleted)
        return None if deleted else node

    dfs(root, True)
    return forest
""",
    ),
    # ---- Lowest Common Ancestor of Deepest Leaves (LeetCode 1123) ----
    dict(
        title="Lowest Common Ancestor of Deepest Leaves",
        diff="M",
        lc=1123,
        slug="lowest-common-ancestor-of-deepest-leaves",
        prompt="Return the lowest node whose subtree contains ALL of the deepest leaves of the tree.",
        sig="def lca_deepest_leaves(root: Optional[TreeNode]) -> Optional[TreeNode]:",
        fn="lca_deepest_leaves",
        adapt_in=T,
        adapt_out=tree_to_list,
        tests=[
            (([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4],), [2, 7, 4]),
            (([1],), [1]),
            (([0, 1, 3, None, 2],), [2]),
            (([1, 2, 3],), [1, 2, 3]),
        ],
        hints=[
            "If the left subtree is deeper, all deepest leaves are in it - the answer lives there.",
            (
                "If the right subtree is deeper, the answer lives there. If they are equally deep, the current node "
                "is the answer."
            ),
            "Return a pair (depth, answer_node) from each call and compare the two children's depths.",
        ],
        pattern="DFS returning (depth, candidate node)",
        explain=(
            "The deepest leaves branch for the first time at the answer node. Comparing the depths reported by the "
            "children tells us whether they split here or all lie on one side."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - test every node's subtree for all deepest leaves",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every node's subtree for all deepest leaves
def lca_deepest_leaves(root):
    if not root:
        return None
    depth = {}

    def measure(node, d):
        if node:
            depth[node] = d
            measure(node.left, d + 1)
            measure(node.right, d + 1)

    measure(root, 0)
    deepest = {n for n, d in depth.items() if d == max(depth.values())}  # all deepest nodes

    def inside(node):  # every node in this subtree
        return {node} | inside(node.left) | inside(node.right) if node else set()

    candidates = [
        n for n in depth if deepest <= inside(n)
    ]  # nodes whose subtree holds every deepest node
    return max(candidates, key=lambda n: depth[n])  # the lowest one
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: DFS returning (depth, candidate node)
def lca_deepest_leaves(root):
    def go(
        node,
    ):  # returns (depth of the deepest leaf below, lowest node containing all those leaves)
        if not node:
            return 0, None
        left_depth, left_node = go(node.left)
        right_depth, right_node = go(node.right)
        if left_depth > right_depth:
            return left_depth + 1, left_node  # all deepest leaves are on the left
        if right_depth > left_depth:
            return right_depth + 1, right_node  # all deepest leaves are on the right
        return left_depth + 1, node  # they split here (or this is a leaf)

    return go(root)[1]
""",
    ),
]
