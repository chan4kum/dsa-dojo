from core import *

# Tree tests give LeetCode-style level-order lists (None = missing child); adapters build / flatten the tree.
T = lambda a: (list_to_tree(a[0]),) + tuple(a[1:])

PROBLEMS = [
    dict(
        title="Maximum Depth of Binary Tree", diff="E", lc=104, slug="maximum-depth-of-binary-tree",
        prompt="Return the number of nodes on the longest root-to-leaf path of a binary tree (0 for an empty tree).",
        sig="def max_depth(root: Optional[TreeNode]) -> int:",
        fn="max_depth", adapt_in=T,
        tests=[(([3, 9, 20, None, None, 15, 7],), 3), (([1, None, 2],), 2), (([],), 0), (([1],), 1),
               (([1, 2, 3, 4, None, None, 5, 6],), 4)],
        hints=["Define the answer for a tree in terms of the answers for its two subtrees.",
               "depth(node) = 1 + max(depth(left), depth(right)).",
               "Base case: an empty tree has depth 0."],
        pattern="Tree recursion (post-order): answer(node) = f(answer(left), answer(right))",
        explain="""
        Trust the recursion: assume depth() already works for the children and combine. Base case = None -> 0.
        This 'solve children, combine at the node' shape is the core of almost every tree problem.
        O(n) time, O(h) stack.""",
        solution=r'''
def max_depth(root):
    if not root:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
''',
    ),
    dict(
        title="Binary Tree Level Order Traversal", diff="M", lc=102, slug="binary-tree-level-order-traversal",
        prompt="Return the node values level by level, left to right, as a list of lists.",
        sig="def level_order(root: Optional[TreeNode]) -> List[List[int]]:",
        fn="level_order", adapt_in=T,
        tests=[(([3, 9, 20, None, None, 15, 7],), [[3], [9, 20], [15, 7]]), (([1],), [[1]]), (([],), []),
               (([1, 2, 3, 4, 5],), [[1], [2, 3], [4, 5]])],
        hints=["Depth-first goes deep first. You need to finish a whole level before the next.",
               "Use a queue (BFS).",
               "At the start of each round, len(queue) is exactly the size of the current level - process that many nodes."],
        pattern="BFS with a queue, one level per round (snapshot len(queue))",
        explain="""
        A FIFO queue visits nodes in order of distance from the root. Freezing the queue length at the start
        of each round separates levels. The same skeleton gives right-side view, zig-zag, min depth, and
        shortest paths in unweighted graphs. O(n).""",
        solution=r'''
def level_order(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        level = []
        for _ in range(len(q)):              # exactly this level's nodes
            node = q.popleft()
            level.append(node.val)
            if node.left:
                q.append(node.left)
            if node.right:
                q.append(node.right)
        out.append(level)
    return out
''',
    ),
    dict(
        title="Validate Binary Search Tree", diff="M", lc=98, slug="validate-binary-search-tree",
        prompt="Decide whether a binary tree is a valid BST: every node's value is strictly greater than ALL "
               "values in its left subtree and strictly smaller than ALL values in its right subtree.",
        sig="def is_valid_bst(root: Optional[TreeNode]) -> bool:",
        fn="is_valid_bst", adapt_in=T,
        tests=[(([2, 1, 3],), True), (([5, 1, 4, None, None, 3, 6],), False), (([5, 4, 6, None, None, 3, 7],), False),
               (([1],), True), (([2, 2, 2],), False), (([],), True)],
        hints=["Checking only node.left.val < node.val < node.right.val is NOT enough - see the third example.",
               "Each node lives inside a value range (lo, hi) inherited from its ancestors.",
               "Recurse with bounds: left child gets (lo, node.val), right child gets (node.val, hi)."],
        pattern="Tree recursion passing constraints DOWN (top-down), or in-order traversal must be increasing",
        explain="""
        The BST property is about all ancestors, not just the parent. Pass the tightest open interval (lo, hi)
        down: going left tightens hi, going right tightens lo. (Equivalent: an in-order walk must be strictly
        increasing.) O(n) time, O(h) space.""",
        solution=r'''
def is_valid_bst(root):
    def ok(node, lo, hi):
        if not node:
            return True
        if not (lo < node.val < hi):
            return False
        return ok(node.left, lo, node.val) and ok(node.right, node.val, hi)
    return ok(root, float("-inf"), float("inf"))
''',
    ),
    dict(
        title="Lowest Common Ancestor of a Binary Tree", diff="M", lc=236, slug="lowest-common-ancestor-of-a-binary-tree",
        prompt="Given a binary tree and two nodes p and q that exist in it, return their lowest common ancestor "
               "(a node may be its own ancestor). Tests pass the two node VALUES; return the LCA's value.",
        sig="def lowest_common_ancestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:",
        fn="lowest_common_ancestor",
        adapt_in=lambda a: (lambda r: (r, find_node(r, a[1]), find_node(r, a[2])))(list_to_tree(a[0])),
        adapt_out=lambda n: n.val,
        tests=[(([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 1), 3), (([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 5, 4), 5),
               (([1, 2], 1, 2), 1), (([3, 5, 1, 6, 2, 0, 8, None, None, 7, 4], 6, 4), 5)],
        hints=["Ask each subtree: 'does your subtree contain p or q?'",
               "If the current node IS p or q, return it. Otherwise recurse into both children.",
               "If both children return a node, the current node is where p and q split -> it is the LCA; else bubble up the non-null result."],
        pattern="Post-order tree recursion returning 'what I found below me'",
        explain="""
        The function returns the node if it found p or q in the subtree, or the LCA if it found both, else None.
        At a node: both sides non-None means p and q are on different sides -> this node is the LCA.
        One side non-None -> propagate it. O(n).""",
        solution=r'''
def lowest_common_ancestor(root, p, q):
    if not root or root is p or root is q:
        return root
    left = lowest_common_ancestor(root.left, p, q)
    right = lowest_common_ancestor(root.right, p, q)
    if left and right:
        return root
    return left or right
''',
    ),
    dict(
        title="Binary Tree Maximum Path Sum", diff="H", lc=124, slug="binary-tree-maximum-path-sum",
        prompt="A path is any sequence of connected nodes (it need not touch the root and may not branch). "
               "Return the maximum sum of node values over all non-empty paths.",
        sig="def max_path_sum(root: Optional[TreeNode]) -> int:",
        fn="max_path_sum", adapt_in=T,
        tests=[(([1, 2, 3],), 6), (([-10, 9, 20, None, None, 15, 7],), 42), (([-3],), -3), (([2, -1],), 2),
               (([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1],), 48)],
        hints=["The best path 'bends' at exactly one top node: left chain + node + right chain.",
               "A recursive function can only return a path that goes UP to the parent, so it can use at most one child chain.",
               "gain(node) = node.val + max(0, gain(left), gain(right)); while computing it, update the global best with node.val + max(0,gain(left)) + max(0,gain(right))."],
        pattern="Tree DP: return one value upward, record a different value (the bend) in a global",
        explain="""
        Two quantities per node: (1) what a parent can extend (a single downward chain) - returned; (2) the best
        path that bends at this node (both chains) - recorded in `best`. Negative chains are clamped to 0
        (just don't take them). Same shape as Diameter of Binary Tree. O(n).""",
        solution=r'''
def max_path_sum(root):
    best = float("-inf")
    def gain(node):
        nonlocal best
        if not node:
            return 0
        left = max(gain(node.left), 0)
        right = max(gain(node.right), 0)
        best = max(best, node.val + left + right)      # path bending at this node
        return node.val + max(left, right)             # chain a parent may extend
    gain(root)
    return best
''',
    ),
]
