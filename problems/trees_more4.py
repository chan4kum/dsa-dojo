"""more Binary Tree problems (batch 5) - part of the problem bank for the "trees" topic.

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


PROBLEMS = [
    # ---- Binary Tree Preorder Traversal (LeetCode 144) ----
    dict(
        title="Binary Tree Preorder Traversal",
        diff="E",
        lc=144,
        slug="binary-tree-preorder-traversal",
        prompt="Return the preorder traversal (node, left subtree, right subtree) of a binary tree's values.",
        sig="def preorder_traversal(root: Optional[TreeNode]) -> List[int]:",
        fn="preorder_traversal",
        adapt_in=T,
        tests=[
            (([1, None, 2, 3],), [1, 2, 3]),
            (([],), []),
            (([1, 2, 3, 4, 5],), [1, 2, 4, 5, 3]),
            (([1],), [1]),
        ],
        hints=[
            "Recursion: visit the node, then the left subtree, then the right subtree.",
            "Replace the call stack with your own stack.",
            "Pop a node, record it, push its RIGHT child first and then its LEFT child so left is popped next.",
        ],
        pattern="Iterative DFS with an explicit stack",
        explain=(
            "Preorder visits a node before its children, so a stack that always processes the most recently pushed "
            "node reproduces the recursion. Pushing right before left keeps the left subtree on top."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n) time, O(h) recursion stack (list concatenation makes it O(n^2) in the worst case)",
        brute=r"""
# BRUTE FORCE: O(n) time, O(h) recursion stack (list concatenation makes it O(n^2) in the worst case)
def preorder_traversal(root):
    if not root:
        return []
    return [root.val] + preorder_traversal(root.left) + preorder_traversal(root.right)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Iterative DFS with an explicit stack
def preorder_traversal(root):
    out, stack = [], [root] if root else []
    while stack:
        node = stack.pop()
        out.append(node.val)  # visit before the children
        if node.right:
            stack.append(node.right)  # pushed first, so popped last
        if node.left:
            stack.append(node.left)
    return out
""",
    ),
    # ---- Minimum Absolute Difference in BST (LeetCode 530) ----
    dict(
        title="Minimum Absolute Difference in BST",
        diff="E",
        lc=530,
        slug="minimum-absolute-difference-in-bst",
        prompt=(
            "Return the minimum absolute difference between the values of any two different nodes of a BST (it has "
            "at least 2 nodes)."
        ),
        sig="def get_minimum_difference(root: Optional[TreeNode]) -> int:",
        fn="get_minimum_difference",
        adapt_in=T,
        tests=[
            (([4, 2, 6, 1, 3],), 1),
            (([1, 0, 48, None, None, 12, 49],), 1),
            (([236, 104, 701, None, 227, None, 911],), 9),
            (([5, 2, 9],), 3),
        ],
        hints=[
            "Comparing every pair of nodes works but is O(n^2).",
            "Inorder traversal of a BST gives sorted values.",
            "In a sorted sequence the closest pair is ADJACENT, so keep the previous value while traversing inorder.",
        ],
        pattern="Inorder traversal = sorted order; compare neighbours",
        explain=(
            "The BST property gives us sorting for free. In sorted order the minimum gap is always between two "
            "consecutive values, so one running 'previous' variable replaces all pair checks."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - compare every pair of values",
        brute=r"""
# BRUTE FORCE: O(n^2) time - compare every pair of values
def get_minimum_difference(root):
    values = []

    def collect(node):
        if node:
            values.append(node.val)
            collect(node.left)
            collect(node.right)

    collect(root)
    return min(abs(a - b) for a, b in itertools.combinations(values, 2))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Inorder traversal = sorted order; compare neighbours
def get_minimum_difference(root):
    best, prev = float("inf"), None
    stack, node = [], root
    while node or stack:  # iterative inorder: values come out sorted
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        if prev is not None:
            best = min(best, node.val - prev)  # only neighbours in sorted order matter
        prev = node.val
        node = node.right
    return best
""",
    ),
    # ---- Binary Tree Tilt (LeetCode 563) ----
    dict(
        title="Binary Tree Tilt",
        diff="E",
        lc=563,
        slug="binary-tree-tilt",
        prompt=(
            "The tilt of a node is |sum of its left subtree - sum of its right subtree|. Return the sum of the "
            "tilts of all nodes."
        ),
        sig="def find_tilt(root: Optional[TreeNode]) -> int:",
        fn="find_tilt",
        adapt_in=T,
        tests=[
            (([1, 2, 3],), 1),
            (([4, 2, 9, 3, 5, None, 7],), 15),
            (([21, 7, 14, 1, 1, 2, 2, 3, 3],), 9),
            (([],), 0),
        ],
        hints=[
            "A node's tilt needs the sums of both subtrees.",
            "Recomputing each subtree sum from scratch is O(n^2) on a skewed tree.",
            "Post-order: each call returns its subtree sum and adds its tilt to a running total as a side effect.",
        ],
        pattern="Post-order DFS returning an aggregate while updating a global",
        explain=(
            "The subtree sum of a node is exactly what its parent needs from it, so returning the sum lets every "
            "node compute its tilt with no extra traversal."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - re-sum both subtrees for every node",
        brute=r"""
# BRUTE FORCE: O(n^2) time - re-sum both subtrees for every node
def find_tilt(root):
    def total(node):
        return node.val + total(node.left) + total(node.right) if node else 0

    def tilt(node):
        if not node:
            return 0
        return abs(total(node.left) - total(node.right)) + tilt(node.left) + tilt(node.right)

    return tilt(root)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Post-order DFS returning an aggregate while updating a global
def find_tilt(root):
    tilt_sum = 0

    def subtree_sum(node):
        nonlocal tilt_sum
        if not node:
            return 0
        left, right = subtree_sum(node.left), subtree_sum(node.right)
        tilt_sum += abs(left - right)  # this node's tilt
        return left + right + node.val  # what the parent needs

    subtree_sum(root)
    return tilt_sum
""",
    ),
    # ---- Two Sum IV - Input is a BST (LeetCode 653) ----
    dict(
        title="Two Sum IV - Input is a BST",
        diff="E",
        lc=653,
        slug="two-sum-iv-input-is-a-bst",
        prompt="Return True if two different nodes of the BST have values that add up to k.",
        sig="def find_target(root: Optional[TreeNode], k: int) -> bool:",
        fn="find_target",
        adapt_in=T,
        tests=[
            (([5, 3, 6, 2, 4, None, 7], 9), True),
            (([5, 3, 6, 2, 4, None, 7], 28), False),
            (([2, 1, 3], 4), True),
            (([1], 2), False),
        ],
        hints=[
            "This is Two Sum, with the numbers stored in a tree.",
            "Visit every node; for value v ask 'have I already seen k - v?'.",
            "Keep a hash set of values seen so far (any traversal works).",
        ],
        pattern="Two Sum with a hash set while traversing",
        explain="The tree shape is irrelevant to the complement check; the set remembers everything visited so far.",
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - test every pair of nodes",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every pair of nodes
def find_target(root, k):
    values = []

    def collect(node):
        if node:
            values.append(node.val)
            collect(node.left)
            collect(node.right)

    collect(root)
    return any(a + b == k for a, b in itertools.combinations(values, 2))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Two Sum with a hash set while traversing
def find_target(root, k):
    seen = set()
    stack = [root] if root else []
    while stack:
        node = stack.pop()
        if k - node.val in seen:
            return True  # the partner was visited earlier
        seen.add(node.val)
        stack += [child for child in (node.left, node.right) if child]
    return False
""",
    ),
    # ---- Trim a Binary Search Tree (LeetCode 669) ----
    dict(
        title="Trim a Binary Search Tree",
        diff="M",
        lc=669,
        slug="trim-a-binary-search-tree",
        prompt=(
            "Remove every node whose value is outside [low, high], keeping the relative structure of the remaining "
            "nodes. Return the new root."
        ),
        sig="def trim_bst(root: Optional[TreeNode], low: int, high: int) -> Optional[TreeNode]:",
        fn="trim_bst",
        adapt_in=T,
        adapt_out=tree_to_list,
        tests=[
            (([1, 0, 2], 1, 2), [1, None, 2]),
            (([3, 0, 4, None, 2, None, None, 1], 1, 3), [3, 2, None, 1]),
            (([1], 1, 2), [1]),
            (([5, 3, 8], 6, 9), [8]),
        ],
        hints=[
            "If a node is below low, its whole LEFT subtree is below low too - the answer lives in its right subtree.",
            "Symmetrically, a node above high is replaced by what remains of its left subtree.",
            "Otherwise keep the node and trim both children recursively.",
        ],
        pattern="Recursion that returns the replacement subtree",
        explain=(
            "The BST ordering lets one comparison discard an entire subtree. Returning the trimmed subtree lets the "
            "parent re-link to it, so no parent pointers are needed."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - re-insert every surviving value in the original preorder",
        brute=r"""
# BRUTE FORCE: O(n^2) time - re-insert every surviving value in the original preorder
def trim_bst(root, low, high):
    preorder = []

    def walk(node):
        if node:
            preorder.append(node.val)
            walk(node.left)
            walk(node.right)

    walk(root)
    new_root = None
    for v in preorder:
        if low <= v <= high:  # inserting in preorder rebuilds the same shape
            if not new_root:
                new_root = TreeNode(v)
                continue
            cur = new_root
            while True:
                side = "left" if v < cur.val else "right"
                if getattr(cur, side) is None:
                    setattr(cur, side, TreeNode(v))
                    break
                cur = getattr(cur, side)
    return new_root
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Recursion that returns the replacement subtree
def trim_bst(root, low, high):
    if not root:
        return None
    if root.val < low:
        return trim_bst(root.right, low, high)  # this node and its left subtree are too small
    if root.val > high:
        return trim_bst(root.left, low, high)  # this node and its right subtree are too big
    root.left = trim_bst(root.left, low, high)
    root.right = trim_bst(root.right, low, high)
    return root
""",
    ),
    # ---- Leaf-Similar Trees (LeetCode 872) ----
    dict(
        title="Leaf-Similar Trees",
        diff="E",
        lc=872,
        slug="leaf-similar-trees",
        prompt=(
            "The leaf value sequence of a tree is its leaves read from left to right. Return True if two trees have "
            "the same leaf value sequence."
        ),
        sig="def leaf_similar(root1: Optional[TreeNode], root2: Optional[TreeNode]) -> bool:",
        fn="leaf_similar",
        adapt_in=T2,
        tests=[
            (
                (
                    [3, 5, 1, 6, 2, 9, 8, None, None, 7, 4],
                    [3, 5, 1, 6, 7, 4, 2, None, None, None, None, None, None, 9, 8],
                ),
                True,
            ),
            (([1, 2, 3], [1, 3, 2]), False),
            (([1], [1]), True),
            (([1, 2], [2, 2]), True),
        ],
        hints=[
            "A leaf has no children; collect them in DFS order (left before right).",
            "Compare the two sequences.",
            "To stop early, walk both trees lazily with generators and compare leaf by leaf.",
        ],
        pattern="DFS leaf collection; generators for early exit",
        explain=(
            "Left-to-right DFS visits leaves in sequence order. Generators let the comparison stop at the first "
            "difference."
        ),
        cx="O(n + m) time, O(h) space",
        brute_cx="O(n + m) time, O(n + m) space - build both full leaf lists first",
        brute=r"""
# BRUTE FORCE: O(n + m) time, O(n + m) space - build both full leaf lists first
def leaf_similar(root1, root2):
    def leaves(node):
        if not node:
            return []
        if not node.left and not node.right:
            return [node.val]
        return leaves(node.left) + leaves(node.right)

    return leaves(root1) == leaves(root2)
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(h) space
# Idea: DFS leaf collection; generators for early exit
def leaf_similar(root1, root2):
    def leaf_iter(root):
        stack = [root] if root else []
        while stack:
            node = stack.pop()
            if not node.left and not node.right:
                yield node.val
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)  # popped first, so leaves come out left to right

    end = object()
    return all(
        a == b for a, b in itertools.zip_longest(leaf_iter(root1), leaf_iter(root2), fillvalue=end)
    )
""",
    ),
    # ---- Range Sum of BST (LeetCode 938) ----
    dict(
        title="Range Sum of BST",
        diff="E",
        lc=938,
        slug="range-sum-of-bst",
        prompt="Return the sum of the values of all BST nodes whose value is in the inclusive range [low, high].",
        sig="def range_sum_bst(root: Optional[TreeNode], low: int, high: int) -> int:",
        fn="range_sum_bst",
        adapt_in=T,
        tests=[
            (([10, 5, 15, 3, 7, None, 18], 7, 15), 32),
            (([10, 5, 15, 3, 7, 13, 18, 1, None, 6], 6, 10), 23),
            (([1], 1, 1), 1),
            (([8, 3, 10], 11, 20), 0),
        ],
        hints=[
            "Visiting every node and testing the range is O(n).",
            "Use the BST property: if node.val < low, nothing in the left subtree can qualify.",
            "If node.val > high, skip the right subtree. Otherwise add node.val and explore both sides.",
        ],
        pattern="DFS with BST pruning",
        explain="Whole subtrees outside the range are skipped, so only nodes on the boundary paths are visited.",
        cx="O(n) worst case, O(h + k) typical",
        brute_cx="O(n) time - visit every node",
        brute=r"""
# BRUTE FORCE: O(n) time - visit every node
def range_sum_bst(root, low, high):
    if not root:
        return 0
    own = root.val if low <= root.val <= high else 0
    return own + range_sum_bst(root.left, low, high) + range_sum_bst(root.right, low, high)
""",
        solution=r"""
# OPTIMISED: O(n) worst case, O(h + k) typical
# Idea: DFS with BST pruning
def range_sum_bst(root, low, high):
    total, stack = 0, [root] if root else []
    while stack:
        node = stack.pop()
        if low <= node.val <= high:
            total += node.val
        if node.left and node.val > low:  # smaller values may still be in range
            stack.append(node.left)
        if node.right and node.val < high:  # bigger values may still be in range
            stack.append(node.right)
    return total
""",
    ),
    # ---- Univalued Binary Tree (LeetCode 965) ----
    dict(
        title="Univalued Binary Tree",
        diff="E",
        lc=965,
        slug="univalued-binary-tree",
        prompt="Return True if every node of the (non-empty) binary tree has the same value.",
        sig="def is_unival_tree(root: Optional[TreeNode]) -> bool:",
        fn="is_unival_tree",
        adapt_in=T,
        tests=[
            (([1, 1, 1, 1, 1, None, 1],), True),
            (([2, 2, 2, 5, 2],), False),
            (([1],), True),
            (([3, 3, 4],), False),
        ],
        hints=[
            "Compare every node with the root's value.",
            "You can stop at the first different value.",
            "DFS with a stack; return False as soon as node.val != root.val.",
        ],
        pattern="DFS with early exit",
        explain="Collecting everything first wastes work when the first mismatch is near the root.",
        cx="O(n) time, O(h) space",
        brute_cx="O(n) time, O(n) space - collect every value into a set",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - collect every value into a set
def is_unival_tree(root):
    values = set()

    def collect(node):
        if node:
            values.add(node.val)
            collect(node.left)
            collect(node.right)

    collect(root)
    return len(values) == 1
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: DFS with early exit
def is_unival_tree(root):
    stack = [root]
    while stack:
        node = stack.pop()
        if node.val != root.val:
            return False  # first mismatch ends the search
        stack += [child for child in (node.left, node.right) if child]
    return True
""",
    ),
    # ---- Cousins in Binary Tree (LeetCode 993) ----
    dict(
        title="Cousins in Binary Tree",
        diff="E",
        lc=993,
        slug="cousins-in-binary-tree",
        prompt=(
            "Two nodes (with distinct values x and y) are cousins if they are at the same depth but have different "
            "parents. Return whether x and y are cousins."
        ),
        sig="def is_cousins(root: Optional[TreeNode], x: int, y: int) -> bool:",
        fn="is_cousins",
        adapt_in=T,
        tests=[
            (([1, 2, 3, 4], 4, 3), False),
            (([1, 2, 3, None, 4, None, 5], 5, 4), True),
            (([1, 2, 3, None, 4], 2, 3), False),
            (([1, 2, 3, 4, 5, 6, 7], 4, 6), True),
        ],
        hints=[
            "You need each target's depth AND parent.",
            "BFS level by level: both values must appear in the same level.",
            (
                "While expanding a node, check whether its two children are exactly x and y - that would make them "
                "siblings, not cousins."
            ),
        ],
        pattern="BFS level scan with a sibling check",
        explain=(
            "A level-order scan answers 'same depth' for free; the sibling test happens when the parent is expanded."
        ),
        cx="O(n) time, O(w) space",
        brute_cx="O(n) time - record depth and parent of every node in a dictionary",
        brute=r"""
# BRUTE FORCE: O(n) time - record depth and parent of every node in a dictionary
def is_cousins(root, x, y):
    info = {}  # value -> (depth, parent value)

    def walk(node, depth, parent):
        if node:
            info[node.val] = (depth, parent)
            walk(node.left, depth + 1, node.val)
            walk(node.right, depth + 1, node.val)

    walk(root, 0, None)
    (dx, px), (dy, py) = info[x], info[y]
    return dx == dy and px != py
""",
        solution=r"""
# OPTIMISED: O(n) time, O(w) space
# Idea: BFS level scan with a sibling check
def is_cousins(root, x, y):
    level = [root]
    while level:
        for node in level:
            kids = {c.val for c in (node.left, node.right) if c}
            if x in kids and y in kids:
                return False  # siblings share a parent
        values = {n.val for n in level}
        if x in values and y in values:
            return True  # same depth, different parents
        if x in values or y in values:
            return False  # found at different depths
        level = [c for n in level for c in (n.left, n.right) if c]
    return False
""",
    ),
    # ---- Maximum Difference Between Node and Ancestor (LeetCode 1026) ----
    dict(
        title="Maximum Difference Between Node and Ancestor",
        diff="M",
        lc=1026,
        slug="maximum-difference-between-node-and-ancestor",
        prompt="Return the maximum |a.val - b.val| over all pairs where a is an ancestor of b.",
        sig="def max_ancestor_diff(root: Optional[TreeNode]) -> int:",
        fn="max_ancestor_diff",
        adapt_in=T,
        tests=[
            (([8, 3, 10, 1, 6, None, 14, None, None, 4, 7, 13],), 7),
            (([1, None, 2, None, 0, 3],), 3),
            (([5],), 0),
            (([1, 5],), 4),
        ],
        hints=[
            "For a fixed node, the best ancestor is either the smallest or the largest value on its root path.",
            "So carry down (min so far, max so far) along the path.",
            "At each node update the answer with max(|v - min|, |v - max|), then update min and max and recurse.",
        ],
        pattern="Carry path statistics downward",
        explain=(
            "Instead of comparing a node with every ancestor, keep only the extremes of the path; the best partner "
            "is always an extreme."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n * h) time - compare each node with every ancestor on its path",
        brute=r"""
# BRUTE FORCE: O(n * h) time - compare each node with every ancestor on its path
def max_ancestor_diff(root):
    best = 0

    def walk(node, ancestors):
        nonlocal best
        if not node:
            return
        for a in ancestors:
            best = max(best, abs(a - node.val))
        walk(node.left, ancestors + [node.val])
        walk(node.right, ancestors + [node.val])

    walk(root, [])
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Carry path statistics downward
def max_ancestor_diff(root):
    best = 0
    stack = [(root, root.val, root.val)] if root else []  # (node, min on path, max on path)
    while stack:
        node, lo, hi = stack.pop()
        best = max(best, abs(node.val - lo), abs(node.val - hi))
        lo, hi = min(lo, node.val), max(hi, node.val)
        for child in (node.left, node.right):
            if child:
                stack.append((child, lo, hi))
    return best
""",
    ),
    # ---- Deepest Leaves Sum (LeetCode 1302) ----
    dict(
        title="Deepest Leaves Sum",
        diff="M",
        lc=1302,
        slug="deepest-leaves-sum",
        prompt="Return the sum of the values of the leaves on the deepest level of the tree.",
        sig="def deepest_leaves_sum(root: Optional[TreeNode]) -> int:",
        fn="deepest_leaves_sum",
        adapt_in=T,
        tests=[
            (([1, 2, 3, 4, 5, None, 6, 7, None, None, None, None, 8],), 15),
            (([6, 7, 8, 2, 7, 1, 3, 9, None, 1, 4, None, None, None, 5],), 19),
            (([1],), 1),
            (([1, 2],), 2),
        ],
        hints=[
            "The deepest level is the LAST level of a BFS.",
            "Process the tree level by level, summing each level.",
            "Keep only the most recent level's sum - the last one computed is the answer.",
        ],
        pattern="BFS, keep the last level",
        explain="Every node on the last level is automatically a leaf, so the level sum equals the deepest-leaves sum.",
        cx="O(n) time, O(w) space",
        brute_cx="O(n) time - DFS recording depths, then sum the maximum depth",
        brute=r"""
# BRUTE FORCE: O(n) time - DFS recording depths, then sum the maximum depth
def deepest_leaves_sum(root):
    sums = {}  # depth -> sum of the nodes at that depth

    def walk(node, depth):
        if node:
            sums[depth] = sums.get(depth, 0) + node.val
            walk(node.left, depth + 1)
            walk(node.right, depth + 1)

    walk(root, 0)
    return sums[max(sums)]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(w) space
# Idea: BFS, keep the last level
def deepest_leaves_sum(root):
    level, total = [root] if root else [], 0
    while level:
        total = sum(node.val for node in level)  # overwritten until the last level
        level = [child for node in level for child in (node.left, node.right) if child]
    return total
""",
    ),
    # ---- Sum of Nodes with Even-Valued Grandparent (LeetCode 1315) ----
    dict(
        title="Sum of Nodes with Even-Valued Grandparent",
        diff="M",
        lc=1315,
        slug="sum-of-nodes-with-even-valued-grandparent",
        prompt="Return the sum of the values of all nodes whose grandparent has an even value (0 if there are none).",
        sig="def sum_even_grandparent(root: Optional[TreeNode]) -> int:",
        fn="sum_even_grandparent",
        adapt_in=T,
        tests=[
            (([6, 7, 8, 2, 7, 1, 3, 9, None, 1, 4, None, None, None, 5],), 18),
            (([1],), 0),
            (([2, 3, 4, 5],), 5),
            (([1, 2, 3],), 0),
        ],
        hints=[
            "A node needs to know its parent and grandparent.",
            "Pass them down as parameters (or push them on the DFS stack).",
            "When grandparent is not None and even, add node.val.",
        ],
        pattern="DFS carrying parent and grandparent",
        explain=(
            "Parent pointers are not stored in the nodes, so we hand the two ancestors down with every recursive call."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n) time, O(n) space - build a parent dictionary first, then look two levels up",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - build a parent dictionary first, then look two levels up
def sum_even_grandparent(root):
    parent, nodes = {}, []

    def walk(node, par):
        if node:
            parent[node] = par
            nodes.append(node)
            walk(node.left, node)
            walk(node.right, node)

    walk(root, None)
    total = 0
    for node in nodes:
        p = parent[node]
        g = parent[p] if p else None
        if g and g.val % 2 == 0:
            total += node.val
    return total
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: DFS carrying parent and grandparent
def sum_even_grandparent(root):
    total = 0
    stack = [(root, None, None)] if root else []  # (node, parent, grandparent)
    while stack:
        node, parent, grand = stack.pop()
        if grand and grand.val % 2 == 0:
            total += node.val
        for child in (node.left, node.right):
            if child:
                stack.append((child, node, parent))
    return total
""",
    ),
    # ---- Maximum Level Sum of a Binary Tree (LeetCode 1161) ----
    dict(
        title="Maximum Level Sum of a Binary Tree",
        diff="M",
        lc=1161,
        slug="maximum-level-sum-of-a-binary-tree",
        prompt=(
            "Levels are numbered from 1 at the root. Return the smallest level number whose nodes have the largest sum."
        ),
        sig="def max_level_sum(root: Optional[TreeNode]) -> int:",
        fn="max_level_sum",
        adapt_in=T,
        tests=[
            (([1, 7, 0, 7, -8, None, None],), 2),
            (([989, None, 10250, 98693, -89388, None, None, None, -32127],), 2),
            (([1],), 1),
            (([-5, 2, 2],), 2),
        ],
        hints=[
            "Compute the sum of every level.",
            "BFS handles one level per loop iteration.",
            "Update the best only when a level sum is STRICTLY greater, so ties keep the smaller level number.",
        ],
        pattern="BFS with per-level aggregation",
        explain="The strict inequality keeps the earliest level among equals, matching 'smallest level'.",
        cx="O(n) time, O(w) space",
        brute_cx="O(n) time - DFS filling per-depth sums, then scan them",
        brute=r"""
# BRUTE FORCE: O(n) time - DFS filling per-depth sums, then scan them
def max_level_sum(root):
    sums = []

    def walk(node, depth):
        if node:
            if depth == len(sums):
                sums.append(0)
            sums[depth] += node.val
            walk(node.left, depth + 1)
            walk(node.right, depth + 1)

    walk(root, 0)
    return sums.index(max(sums)) + 1  # index() returns the first (smallest) level
""",
        solution=r"""
# OPTIMISED: O(n) time, O(w) space
# Idea: BFS with per-level aggregation
def max_level_sum(root):
    best_sum, best_level, level_no = float("-inf"), 1, 0
    level = [root] if root else []
    while level:
        level_no += 1
        total = sum(node.val for node in level)
        if total > best_sum:  # strictly greater: ties keep the earlier level
            best_sum, best_level = total, level_no
        level = [child for node in level for child in (node.left, node.right) if child]
    return best_level
""",
    ),
    # ---- Construct Binary Search Tree from Preorder Traversal (LeetCode 1008) ----
    dict(
        title="Construct Binary Search Tree from Preorder Traversal",
        diff="M",
        lc=1008,
        slug="construct-binary-search-tree-from-preorder-traversal",
        prompt="Given the preorder traversal of a BST (distinct values), rebuild the BST.",
        sig="def bst_from_preorder(preorder: List[int]) -> Optional[TreeNode]:",
        fn="bst_from_preorder",
        adapt_out=tree_to_list,
        tests=[
            (([8, 5, 1, 7, 10, 12],), [8, 5, 10, 1, 7, None, 12]),
            (([1, 3],), [1, None, 3]),
            (([1],), [1]),
            (([3, 2, 1],), [3, 2, None, 1]),
        ],
        hints=[
            "Inserting the values one by one into a BST rebuilds it - but that is O(n^2) for a skewed tree.",
            "The first value is the root; later values must lie inside an allowed (low, high) range.",
            (
                "Keep an index into preorder. build(bound): create a node while preorder[i] < bound; left child "
                "gets bound = node.val, right gets the parent's bound."
            ),
        ],
        pattern="Recursive build with upper bounds (one pass)",
        explain=(
            "Each value is consumed exactly once. The bound tells a call when its subtree is complete, replacing "
            "any search for the split point."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - insert every value starting from the root",
        brute=r"""
# BRUTE FORCE: O(n^2) time - insert every value starting from the root
def bst_from_preorder(preorder):
    root = None
    for v in preorder:
        node = TreeNode(v)
        if not root:
            root = node
            continue
        cur = root
        while True:  # walk down from the root for every insertion
            if v < cur.val:
                if cur.left is None:
                    cur.left = node
                    break
                cur = cur.left
            else:
                if cur.right is None:
                    cur.right = node
                    break
                cur = cur.right
    return root
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Recursive build with upper bounds (one pass)
def bst_from_preorder(preorder):
    i = 0

    def build(bound):  # build the subtree whose values are all < bound
        nonlocal i
        if i == len(preorder) or preorder[i] > bound:
            return None
        node = TreeNode(preorder[i])
        i += 1
        node.left = build(node.val)  # left values are smaller than this node
        node.right = build(bound)  # right values are smaller than the inherited bound
        return node

    return build(float("inf"))
""",
    ),
    # ---- Add One Row to Tree (LeetCode 623) ----
    dict(
        title="Add One Row to Tree",
        diff="M",
        lc=623,
        slug="add-one-row-to-tree",
        prompt=(
            "Add a row of nodes with value val at the given depth (root has depth 1). Every node at depth - 1 gets "
            "new left and right children holding val; its old children become the children of the new nodes. If "
            "depth is 1, val becomes the new root with the old tree as its left child."
        ),
        sig="def add_one_row(root: Optional[TreeNode], val: int, depth: int) -> Optional[TreeNode]:",
        fn="add_one_row",
        adapt_in=T,
        adapt_out=tree_to_list,
        tests=[
            (([4, 2, 6, 3, 1, 5], 1, 2), [4, 1, 1, 2, None, None, 6, 3, 1, 5]),
            (([4, 2, None, 3, 1], 1, 3), [4, 2, None, 1, 1, 3, None, None, 1]),
            (([1, 2, 3], 5, 1), [5, 1, None, 2, 3]),
            (([1], 7, 2), [1, 7, 7]),
        ],
        hints=[
            "Handle depth == 1 separately: create a new root.",
            "Otherwise find all nodes at depth - 1.",
            "For each of them: new_left = Node(val, left=old_left); new_right = Node(val, right=old_right).",
        ],
        pattern="Level-targeted tree surgery (BFS or DFS with a depth counter)",
        explain=(
            "Only the nodes at depth - 1 change, so reach exactly that level and re-attach the old children below "
            "the new nodes."
        ),
        cx="O(n) time",
        brute_cx="O(n) time - BFS to the target level",
        brute=r"""
# BRUTE FORCE: O(n) time - BFS to the target level
def add_one_row(root, val, depth):
    if depth == 1:
        return TreeNode(val, left=root)
    level = [root]
    for _ in range(depth - 2):  # walk down to depth - 1
        level = [c for n in level for c in (n.left, n.right) if c]
    for node in level:
        node.left = TreeNode(val, left=node.left)
        node.right = TreeNode(val, right=node.right)
    return root
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Level-targeted tree surgery (BFS or DFS with a depth counter)
def add_one_row(root, val, depth):
    if depth == 1:
        return TreeNode(val, left=root)

    def insert(node, level):
        if not node:
            return
        if level == depth - 1:
            node.left = TreeNode(val, left=node.left)  # old children move under the new nodes
            node.right = TreeNode(val, right=node.right)
            return
        insert(node.left, level + 1)
        insert(node.right, level + 1)

    insert(root, 1)
    return root
""",
    ),
    # ---- Increasing Order Search Tree (LeetCode 897) ----
    dict(
        title="Increasing Order Search Tree",
        diff="E",
        lc=897,
        slug="increasing-order-search-tree",
        prompt=(
            "Rearrange a BST so that, in inorder, the leftmost node is the new root and every node has no left "
            "child and only one right child. Return the new root."
        ),
        sig="def increasing_bst(root: Optional[TreeNode]) -> Optional[TreeNode]:",
        fn="increasing_bst",
        adapt_in=T,
        adapt_out=tree_to_list,
        tests=[
            (
                ([5, 3, 6, 2, 4, None, 8, 1, None, None, None, 7, 9],),
                [1, None, 2, None, 3, None, 4, None, 5, None, 6, None, 7, None, 8, None, 9],
            ),
            (([5, 1, 7],), [1, None, 5, None, 7]),
            (([2],), [2]),
            (([],), []),
        ],
        hints=[
            "An inorder walk of a BST yields the values in increasing order.",
            "Simple way: collect the values and build a right-leaning chain.",
            (
                "In place: during the inorder walk keep a `tail` pointer; for each node set node.left = None and "
                "tail.right = node."
            ),
        ],
        pattern="Inorder traversal with relinking",
        explain=(
            "Reusing the original nodes avoids allocation: each node is detached from its left child and appended "
            "to the growing chain."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n) time, O(n) space - collect values, then build brand-new nodes",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - collect values, then build brand-new nodes
def increasing_bst(root):
    values = []

    def inorder(node):
        if node:
            inorder(node.left)
            values.append(node.val)
            inorder(node.right)

    inorder(root)
    dummy = tail = TreeNode(0)
    for v in values:
        tail.right = TreeNode(v)
        tail = tail.right
    return dummy.right
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Inorder traversal with relinking
def increasing_bst(root):
    dummy = tail = TreeNode(0)
    stack, node = [], root
    while node or stack:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        right = node.right  # remember it before relinking
        node.left = None
        tail.right = node  # append to the chain
        tail = node
        node = right
    return dummy.right
""",
    ),
]
