"""Trees problems - the problem bank for the "trees" topic.

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

from core import find_node, list_to_tree


# Tree tests give LeetCode-style level-order lists (None = missing child); adapters build / flatten the tree.
def T(a):
    """Turn the level-order list in args[0] into a tree; keep the other arguments as they are."""
    return (list_to_tree(a[0]),) + tuple(a[1:])


PROBLEMS = [
    # ---- Maximum Depth of Binary Tree (LeetCode 104) ----
    dict(
        title="Maximum Depth of Binary Tree",
        diff="E",
        lc=104,
        slug="maximum-depth-of-binary-tree",
        prompt="Return the number of nodes on the longest root-to-leaf path of a binary tree (0 for an empty tree).",
        sig="def max_depth(root: Optional[TreeNode]) -> int:",
        fn="max_depth",
        adapt_in=T,
        tests=[
            (([3, 9, 20, None, None, 15, 7],), 3),
            (([1, None, 2],), 2),
            (([],), 0),
            (([1],), 1),
            (([1, 2, 3, 4, None, None, 5, 6],), 4),
        ],
        hints=[
            "Define the answer for a tree in terms of the answers for its two subtrees.",
            "depth(node) = 1 + max(depth(left), depth(right)).",
            "Base case: an empty tree has depth 0.",
        ],
        pattern="Tree recursion (post-order): answer(node) = f(answer(left), answer(right))",
        explain=(
            "Trust the recursion: assume depth() already works for the children and combine. Base case = None -> "
            "0.\n        This 'solve children, combine at the node' shape is the core of almost every tree "
            "problem.\n        O(n) time, O(h) stack."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n) - level by level (an alternative, not slower)",
        brute=r"""
# BRUTE FORCE: O(n) - level by level (an alternative, not slower)
def max_depth(root):
    if not root:
        return 0
    depth, level = 0, [root]
    while level:
        depth += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return depth
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Tree recursion (post-order): answer(node) = f(answer(left), answer(right))
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
""",
    ),
    # ---- Binary Tree Level Order Traversal (LeetCode 102) ----
    dict(
        title="Binary Tree Level Order Traversal",
        diff="M",
        lc=102,
        slug="binary-tree-level-order-traversal",
        prompt="Return the node values level by level, left to right, as a list of lists.",
        sig="def level_order(root: Optional[TreeNode]) -> List[List[int]]:",
        fn="level_order",
        adapt_in=T,
        tests=[
            (([3, 9, 20, None, None, 15, 7],), [[3], [9, 20], [15, 7]]),
            (([1],), [[1]]),
            (([],), []),
            (([1, 2, 3, 4, 5],), [[1], [2, 3], [4, 5]]),
        ],
        hints=[
            "Depth-first goes deep first. You need to finish a whole level before the next.",
            "Use a queue (BFS).",
            (
                "At the start of each round, len(queue) is exactly the size of the current level - process that "
                "many nodes."
            ),
        ],
        pattern="BFS with a queue, one level per round (snapshot len(queue))",
        explain=(
            "A FIFO queue visits nodes in order of distance from the root. Freezing the queue length at the "
            "start\n        of each round separates levels. The same skeleton gives right-side view, zig-zag, min "
            "depth, and\n        shortest paths in unweighted graphs. O(n)."
        ),
        cx="O(n) time, O(w) space (w = widest level)",
        brute_cx="O(n * h) - re-walks the tree once per level",
        brute=r"""
# BRUTE FORCE: O(n * h) - re-walks the tree once per level
def level_order(root):
    def height(n):
        return 0 if not n else 1 + max(height(n.left), height(n.right))

    def at_depth(n, d):
        if not n:
            return []
        return [n.val] if d == 0 else at_depth(n.left, d - 1) + at_depth(n.right, d - 1)

    return [at_depth(root, d) for d in range(height(root))]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(w) space (w = widest level)
# Idea: BFS with a queue, one level per round (snapshot len(queue))
def level_order(root):
    if not root:
        return []

    out, q = [], deque([root])

    while q:
        level = []

        for _ in range(len(q)):  # exactly this level's nodes
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)

        out.append(level)

    return out
""",
    ),
    # ---- Validate Binary Search Tree (LeetCode 98) ----
    dict(
        title="Validate Binary Search Tree",
        diff="M",
        lc=98,
        slug="validate-binary-search-tree",
        prompt=(
            "Decide whether a binary tree is a valid BST: every node's value is strictly greater than ALL values in "
            "its left subtree and strictly smaller than ALL values in its right subtree."
        ),
        sig="def is_valid_bst(root: Optional[TreeNode]) -> bool:",
        fn="is_valid_bst",
        adapt_in=T,
        tests=[
            (([2, 1, 3],), True),
            (([5, 1, 4, None, None, 3, 6],), False),
            (([5, 4, 6, None, None, 3, 7],), False),
            (([1],), True),
            (([2, 2, 2],), False),
            (([],), True),
        ],
        hints=[
            "Checking only node.left.val < node.val < node.right.val is NOT enough - see the third example.",
            "Each node lives inside a value range (lo, hi) inherited from its ancestors.",
            "Recurse with bounds: left child gets (lo, node.val), right child gets (node.val, hi).",
        ],
        pattern="Tree recursion passing constraints DOWN (top-down), or in-order traversal must be increasing",
        explain=(
            "The BST property is about all ancestors, not just the parent. Pass the tightest open interval (lo, "
            "hi)\n        down: going left tightens hi, going right tightens lo. (Equivalent: an in-order walk must "
            "be strictly\n        increasing.) O(n) time, O(h) space."
        ),
        cx="O(n) time, O(h) space (carry a (low, high) range)",
        brute_cx="O(n^2) - compares each node with every value in its subtrees",
        brute=r"""
# BRUTE FORCE: O(n^2) - compares each node with every value in its subtrees
def is_valid_bst(root):
    def values(n):
        return [] if not n else values(n.left) + [n.val] + values(n.right)

    def ok(n):
        if not n:
            return True

        return (
            all(v < n.val for v in values(n.left))
            and all(v > n.val for v in values(n.right))
            and ok(n.left)
            and ok(n.right)
        )

    return ok(root)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space (carry a (low, high) range)
# Idea: Tree recursion passing constraints DOWN (top-down), or in-order traversal must be
#       increasing
def is_valid_bst(root):
    def ok(node, lo, hi):
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return ok(node.left, lo, node.val) and ok(node.right, node.val, hi)

    return ok(root, float("-inf"), float("inf"))
""",
    ),
    # ---- Lowest Common Ancestor of a Binary Tree (LeetCode 236) ----
    dict(
        title="Lowest Common Ancestor of a Binary Tree",
        diff="M",
        lc=236,
        slug="lowest-common-ancestor-of-a-binary-tree",
        prompt=(
            "Given a binary tree and two nodes p and q that exist in it, return their lowest common ancestor (a "
            "node may be its own ancestor). Tests pass the two node VALUES; return the LCA's value."
        ),
        sig="def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:",
        fn="lowest_common_ancestor",
        adapt_in=lambda a: (lambda r: (r, find_node(r, a[1]), find_node(r, a[2])))(list_to_tree(a[0])),
        adapt_out=lambda n: n.val,
        tests=[
            (([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 1), 3),
            (([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 4), 5),
            (([1, 2], 1, 2), 1),
            (([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 6, 4), 5),
        ],
        hints=[
            "Ask each subtree: 'does your subtree contain p or q?'",
            "If the current node IS p or q, return it. Otherwise recurse into both children.",
            (
                "If both children return a node, the current node is where p and q split -> it is the LCA; else "
                "bubble up the non-null result."
            ),
        ],
        pattern="Post-order tree recursion returning 'what I found below me'",
        explain=(
            "The function returns the node if it found p or q in the subtree, or the LCA if it found both, else "
            "None.\n        At a node: both sides non-None means p and q are on different sides -> this node is the "
            "LCA.\n        One side non-None -> propagate it. O(n)."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n) time, O(h) space - two root-to-node paths and compare",
        brute=r"""
# BRUTE FORCE: O(n) time, O(h) space - two root-to-node paths and compare
def lowest_common_ancestor(root, p, q):
    def path(n, target):
        if not n:
            return None

        if n is target:
            return [n]

        for child in (n.left, n.right):
            r = path(child, target)
            if r:
                return [n] + r

        return None

    a, b = path(root, p), path(root, q)
    lca = None

    for x, y in zip(a, b):
        if x is y:
            lca = x

    return lca
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Post-order tree recursion returning 'what I found below me'
def lowest_common_ancestor(root, p, q):
    if not root or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right
""",
    ),
    # ---- Binary Tree Maximum Path Sum (LeetCode 124) ----
    dict(
        title="Binary Tree Maximum Path Sum",
        diff="H",
        lc=124,
        slug="binary-tree-maximum-path-sum",
        prompt=(
            "A path is any sequence of connected nodes (it need not touch the root and may not branch). Return the "
            "maximum sum of node values over all non-empty paths."
        ),
        sig="def max_path_sum(root: Optional[TreeNode]) -> int:",
        fn="max_path_sum",
        adapt_in=T,
        tests=[
            (([1, 2, 3],), 6),
            (([-10, 9, 20, None, None, 15, 7],), 42),
            (([-3],), -3),
            (([2, -1],), 2),
            (([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1],), 48),
        ],
        hints=[
            "The best path 'bends' at exactly one top node: left chain + node + right chain.",
            (
                "A recursive function can only return a path that goes UP to the parent, so it can use at most one "
                "child chain."
            ),
            (
                "gain(node) = node.val + max(0, gain(left), gain(right)); while computing it, update the global "
                "best with node.val + max(0,gain(left)) + max(0,gain(right))."
            ),
        ],
        pattern="Tree DP: return one value upward, record a different value (the bend) in a global",
        explain=(
            "Two quantities per node: (1) what a parent can extend (a single downward chain) - returned; (2) the "
            "best\n        path that bends at this node (both chains) - recorded in `best`. Negative chains are "
            "clamped to 0\n        (just don't take them). Same shape as Diameter of Binary Tree. O(n)."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) - recomputes the downward chains for every node",
        brute=r"""
# BRUTE FORCE: O(n^2) - recomputes the downward chains for every node
def max_path_sum(root):
    def chain(n):
        return 0 if not n else n.val + max(0, chain(n.left), chain(n.right))

    best = float("-inf")
    stack = [root]

    while stack:
        n = stack.pop()
        if not n:
            continue
        best = max(best, n.val + max(0, chain(n.left)) + max(0, chain(n.right)))
        stack += [n.left, n.right]

    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Tree DP: return one value upward, record a different value (the bend) in a global
def max_path_sum(root):
    best = float("-inf")

    def gain(node):
        nonlocal best
        if not node:
            return 0
        left = max(gain(node.left), 0)
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)  # path bending at this node
        return node.val + max(left, right)  # chain a parent may extend

    gain(root)

    return best
""",
    ),
]
