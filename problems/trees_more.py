"""extra batch of Trees problems - the problem bank for the "trees" topic.

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

from core import find_node, list_to_tree, tree_to_list


# Tests give LeetCode-style level-order lists (None = missing child).
def T(a):
    """Turn the level-order list in args[0] into a tree; keep the other arguments as they are."""
    return (list_to_tree(a[0]),) + tuple(a[1:])


def T2(a):
    """Turn both level-order lists in args into trees."""
    return (list_to_tree(a[0]), list_to_tree(a[1]))


PROBLEMS = [
    # ---- Same Tree (LeetCode 100) ----
    dict(
        title="Same Tree",
        diff="E",
        lc=100,
        slug="same-tree",
        prompt="Return True if two binary trees are structurally identical with equal node values.",
        sig="def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:",
        fn="is_same_tree",
        adapt_in=T2,
        tests=[
            (([1, 2, 3], [1, 2, 3]), True),
            (([1, 2], [1, None, 2]), False),
            (([1, 2, 1], [1, 1, 2]), False),
            (([], []), True),
            (([1], []), False),
        ],
        hints=[
            "Two trees are the same if their roots match AND their subtrees match. Recursion?",
            "Base cases: both None -> True; exactly one None -> False.",
            "return p.val == q.val and same(p.left, q.left) and same(p.right, q.right)",
        ],
        pattern="Simultaneous recursion over two trees",
        explain=(
            "Walk both trees in lock-step. The empty/non-empty mismatch cases are the whole difficulty. O(n) time, "
            "O(h) stack."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n) time, O(n) space - serialise both to level-order lists and compare",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - serialise both to level-order lists and compare
def is_same_tree(p, q):
    return tree_to_list(p) == tree_to_list(q)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Simultaneous recursion over two trees
def is_same_tree(p, q):
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
""",
    ),
    # ---- Invert Binary Tree (LeetCode 226) ----
    dict(
        title="Invert Binary Tree",
        diff="E",
        lc=226,
        slug="invert-binary-tree",
        prompt="Mirror a binary tree (swap left and right children of every node) and return the root.",
        sig="def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:",
        fn="invert_tree",
        adapt_in=T,
        adapt_out=tree_to_list,
        tests=[
            (([4, 2, 7, 1, 3, 6, 9],), [4, 7, 2, 9, 6, 3, 1]),
            (([2, 1, 3],), [2, 3, 1]),
            (([],), []),
            (([1, 2],), [1, None, 2]),
        ],
        hints=[
            "What does the mirror image of a tree look like in terms of its two subtrees?",
            "Mirror = swap the children, and mirror each child as well.",
            "root.left, root.right = invert(root.right), invert(root.left)",
        ],
        pattern="Tree recursion: solve subtrees, combine at the root",
        explain="The canonical 'trust the recursion' exercise: assume invert works on subtrees, then just swap them.",
        cx="O(n) time, O(h) space",
        brute_cx="O(n) time, O(n) space - build a brand-new mirrored tree",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - build a brand-new mirrored tree
def invert_tree(root):
    if not root:
        return None
    return TreeNode(root.val, invert_tree(root.right), invert_tree(root.left))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Tree recursion: solve subtrees, combine at the root
def invert_tree(root):
    if root:
        root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
""",
    ),
    # ---- Symmetric Tree (LeetCode 101) ----
    dict(
        title="Symmetric Tree",
        diff="E",
        lc=101,
        slug="symmetric-tree",
        prompt="Return True if the tree is a mirror image of itself around its centre.",
        sig="def is_symmetric(root: Optional[TreeNode]) -> bool:",
        fn="is_symmetric",
        adapt_in=T,
        tests=[
            (([1, 2, 2, 3, 4, 4, 3],), True),
            (([1, 2, 2, None, 3, None, 3],), False),
            (([1],), True),
            (([],), True),
            (([1, 2, 3],), False),
        ],
        hints=[
            "Compare the left subtree with the right subtree - but how are they related?",
            "left.left must mirror right.right, and left.right must mirror right.left.",
            (
                "helper(a, b): both None True; one None False; values equal and helper(a.left,b.right) and "
                "helper(a.right,b.left)."
            ),
        ],
        pattern="Two-node recursion with crossed children",
        explain="\n        Same-Tree recursion with the children paired crosswise.",
        cx="O(n) time, O(h) space",
        brute_cx="O(n) time, O(n) space - mirror a copy and compare serialisations",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - mirror a copy and compare serialisations
def is_symmetric(root):
    def mirror(n):
        return None if not n else TreeNode(n.val, mirror(n.right), mirror(n.left))

    return tree_to_list(root) == tree_to_list(mirror(root))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Two-node recursion with crossed children
def is_symmetric(root):
    def same(a, b):
        if not a and not b:
            return True
        if not a or not b or a.val != b.val:
            return False
        return same(a.left, b.right) and same(a.right, b.left)

    return same(root, root)
""",
    ),
    # ---- Subtree of Another Tree (LeetCode 572) ----
    dict(
        title="Subtree of Another Tree",
        diff="E",
        lc=572,
        slug="subtree-of-another-tree",
        prompt="Return True if some node of `root` has a subtree identical to `sub_root`.",
        sig="def is_subtree(root: Optional[TreeNode], sub_root: Optional[TreeNode]) -> bool:",
        fn="is_subtree",
        adapt_in=T2,
        tests=[
            (([3, 4, 5, 1, 2], [4, 1, 2]), True),
            (([3, 4, 5, 1, 2, None, None, None, None, 0], [4, 1, 2]), False),
            (([1], [1]), True),
            (([1, 1], [1]), True),
            (([1, 2], [3]), False),
        ],
        hints=[
            "Reuse 'Same Tree'. At which nodes of root should you try it?",
            "At every node: is_subtree(root) = same(root, sub) or is_subtree(left) or is_subtree(right).",
            "Total work O(n*m) in the worst case (serialise + string search or tree hashing brings it to O(n+m)).",
        ],
        pattern="Tree recursion reusing a helper (same-tree at every node)",
        explain=(
            "The pairing of two tree traversals: outer = candidates for the root of the match, inner = equality check."
        ),
        cx="O(n*m) time, O(h) space",
        brute_cx="O(n*m) time - serialise every subtree and compare with sub_root's serialisation",
        brute=r"""
# BRUTE FORCE: O(n*m) time - serialise every subtree and compare with sub_root's serialisation
def is_subtree(root, sub_root):
    target = tree_to_list(sub_root)
    stack = [root]
    while stack:
        n = stack.pop()
        if not n:
            continue
        if tree_to_list(n) == target:
            return True
        stack += [n.left, n.right]
    return sub_root is None
""",
        solution=r"""
# OPTIMISED: O(n*m) time, O(h) space
# Idea: Tree recursion reusing a helper (same-tree at every node)
def is_subtree(root, sub_root):
    def same(a, b):
        if not a and not b:
            return True
        if not a or not b or a.val != b.val:
            return False
        return same(a.left, b.left) and same(a.right, b.right)

    if not sub_root:
        return True
    if not root:
        return False
    return (
        same(root, sub_root) or is_subtree(root.left, sub_root) or is_subtree(root.right, sub_root)
    )
""",
    ),
    # ---- Balanced Binary Tree (LeetCode 110) ----
    dict(
        title="Balanced Binary Tree",
        diff="E",
        lc=110,
        slug="balanced-binary-tree",
        prompt=(
            "A tree is height-balanced if at every node the heights of the two subtrees differ by at most 1. Return "
            "True if the tree is balanced."
        ),
        sig="def is_balanced(root: Optional[TreeNode]) -> bool:",
        fn="is_balanced",
        adapt_in=T,
        tests=[
            (([3, 9, 20, None, None, 15, 7],), True),
            (([1, 2, 2, 3, 3, None, None, 4, 4],), False),
            (([],), True),
            (([1, 2, None, 3],), False),
            (([1],), True),
        ],
        hints=[
            "Computing the height at every node separately repeats work - how much?",
            "O(n^2) worst case. Can one traversal return height AND the balanced flag?",
            "Post-order: return height, or -1 as a sentinel meaning 'already unbalanced'. Propagate -1 upward.",
        ],
        pattern="Post-order DFS returning a value + failure sentinel (bottom-up)",
        explain=(
            "Top-down recomputes subtree heights over and over. Bottom-up gives each node its children's results "
            "once:\n        O(n). The sentinel trick (-1 = unbalanced) saves a second return value."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - recompute heights at every node",
        brute=r"""
# BRUTE FORCE: O(n^2) time - recompute heights at every node
def is_balanced(root):
    def height(n):
        return 0 if not n else 1 + max(height(n.left), height(n.right))

    if not root:
        return True
    return (
        abs(height(root.left) - height(root.right)) <= 1
        and is_balanced(root.left)
        and is_balanced(root.right)
    )
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Post-order DFS returning a value + failure sentinel (bottom-up)
def is_balanced(root):
    def h(n):
        if not n:
            return 0
        left = h(n.left)
        if left < 0:
            return -1
        right = h(n.right)
        if right < 0 or abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    return h(root) >= 0
""",
    ),
    # ---- Diameter of Binary Tree (LeetCode 543) ----
    dict(
        title="Diameter of Binary Tree",
        diff="E",
        lc=543,
        slug="diameter-of-binary-tree",
        prompt=(
            "The diameter is the number of EDGES on the longest path between any two nodes (it may not pass through "
            "the root). Return it."
        ),
        sig="def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:",
        fn="diameter_of_binary_tree",
        adapt_in=T,
        tests=[
            (([1, 2, 3, 4, 5],), 3),
            (([1, 2],), 1),
            (([1],), 0),
            (([],), 0),
            (([1, 2, None, 3, None, 4],), 3),
        ],
        hints=[
            "Every path has a highest node. What is the longest path whose highest node is v?",
            "left_height(v) + right_height(v).",
            "DFS returns heights; at each node update a global best with left + right.",
        ],
        pattern="Tree DP: return one thing upward, update the answer with another",
        explain=(
            "Same shape as Binary Tree Maximum Path Sum: the value returned to the parent (a one-sided chain) "
            "differs from\n        the candidate answer at this node (a two-sided path)."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n^2) time - compute heights again for every node",
        brute=r"""
# BRUTE FORCE: O(n^2) time - compute heights again for every node
def diameter_of_binary_tree(root):
    def height(n):
        return 0 if not n else 1 + max(height(n.left), height(n.right))

    if not root:
        return 0
    through = height(root.left) + height(root.right)
    return max(through, diameter_of_binary_tree(root.left), diameter_of_binary_tree(root.right))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Tree DP: return one thing upward, update the answer with another
def diameter_of_binary_tree(root):
    best = 0

    def depth(n):
        nonlocal best
        if not n:
            return 0
        left, right = depth(n.left), depth(n.right)
        best = max(best, left + right)
        return 1 + max(left, right)

    depth(root)
    return best
""",
    ),
    # ---- Binary Tree Right Side View (LeetCode 199) ----
    dict(
        title="Binary Tree Right Side View",
        diff="M",
        lc=199,
        slug="binary-tree-right-side-view",
        prompt=(
            "Return the values visible when looking at the tree from the right side, top to bottom (the last node "
            "of each level)."
        ),
        sig="def right_side_view(root: Optional[TreeNode]) -> List[int]:",
        fn="right_side_view",
        adapt_in=T,
        tests=[
            (([1, 2, 3, None, 5, None, 4],), [1, 3, 4]),
            (([1, None, 3],), [1, 3]),
            (([],), []),
            (([1, 2],), [1, 2]),
            (([1, 2, 3, 4],), [1, 3, 4]),
        ],
        hints=[
            "Which node of each depth is visible from the right?",
            "BFS by levels: the last node of every level.",
            "Or DFS visiting right before left, recording the first node seen at each new depth.",
        ],
        pattern="Level-order BFS (last per level) / depth-tracked DFS",
        explain=(
            "Level-order traversal groups nodes by depth, so 'rightmost per level' is level[-1]. The DFS variant "
            "uses only\n        O(h) memory."
        ),
        cx="O(n) time, O(h) space (DFS)",
        brute_cx="O(n) time, O(n) space - full level-order lists, take the last of each",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - full level-order lists, take the last of each
def right_side_view(root):
    out, level = [], [root] if root else []
    while level:
        out.append(level[-1].val)
        level = [c for n in level for c in (n.left, n.right) if c]
    return out
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space (DFS)
# Idea: Level-order BFS (last per level) / depth-tracked DFS
def right_side_view(root):
    out = []

    def dfs(n, depth):
        if not n:
            return
        if depth == len(out):
            out.append(n.val)
        dfs(n.right, depth + 1)
        dfs(n.left, depth + 1)

    dfs(root, 0)
    return out
""",
    ),
    # ---- Kth Smallest Element in a BST (LeetCode 230) ----
    dict(
        title="Kth Smallest Element in a BST",
        diff="M",
        lc=230,
        slug="kth-smallest-element-in-a-bst",
        prompt="Return the k-th smallest value (1-indexed) in a binary search tree.",
        sig="def kth_smallest(root: Optional[TreeNode], k: int) -> int:",
        fn="kth_smallest",
        adapt_in=T,
        tests=[
            (([3, 1, 4, None, 2], 1), 1),
            (([5, 3, 6, 2, 4, None, None, 1], 3), 3),
            (([2, 1], 2), 2),
            (([1], 1), 1),
            (([5, 3, 6, 2, 4, None, None, 1], 6), 6),
        ],
        hints=[
            "What traversal of a BST visits values in sorted order?",
            "Inorder (left, node, right).",
            (
                "Iterative inorder with a stack; stop as soon as you have visited k nodes (no need to traverse "
                "everything)."
            ),
        ],
        pattern="BST inorder = sorted order (with early stop)",
        explain=(
            "BST property + inorder gives ascending values, so the k-th visited node is the answer. Stopping early "
            "saves\n        work when k is small: O(h + k)."
        ),
        cx="O(h + k) time, O(h) space",
        brute_cx="O(n) time, O(n) space - full inorder list, index k-1",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - full inorder list, index k-1
def kth_smallest(root, k):
    vals = []

    def inorder(n):
        if n:
            inorder(n.left)
            vals.append(n.val)
            inorder(n.right)

    inorder(root)
    return vals[k - 1]
""",
        solution=r"""
# OPTIMISED: O(h + k) time, O(h) space
# Idea: BST inorder = sorted order (with early stop)
def kth_smallest(root, k):
    stack, cur = [], root
    while stack or cur:
        while cur:
            stack.append(cur)
            cur = cur.left
        cur = stack.pop()
        k -= 1
        if k == 0:
            return cur.val
        cur = cur.right
""",
    ),
    # ---- Construct Binary Tree from Preorder and Inorder Traversal (LeetCode 105) ----
    dict(
        title="Construct Binary Tree from Preorder and Inorder Traversal",
        diff="M",
        lc=105,
        slug="construct-binary-tree-from-preorder-and-inorder-traversal",
        prompt=(
            "Given the preorder and inorder traversals of a binary tree with distinct values, rebuild the tree and "
            "return its root."
        ),
        sig="def build_tree(preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:",
        fn="build_tree",
        adapt_out=tree_to_list,
        tests=[
            (([3, 9, 20, 15, 7], [9, 3, 15, 20, 7]), [3, 9, 20, None, None, 15, 7]),
            (([-1], [-1]), [-1]),
            (([1, 2], [2, 1]), [1, 2]),
            (([1, 2], [1, 2]), [1, None, 2]),
            (([], []), []),
        ],
        hints=[
            "Preorder's first element is the root. Where does that root sit in the inorder list?",
            "Everything left of it in inorder is the left subtree; everything right is the right subtree.",
            (
                "Recurse with index ranges; precompute value -> inorder index in a dict so the split is O(1). "
                "Consume preorder with a moving pointer."
            ),
        ],
        pattern="Divide and conquer using traversal properties",
        explain=(
            "Preorder tells you each subtree's root; inorder tells you its size split. The left subtree's preorder "
            "items\n        come right after the root, so a single shared pointer into preorder works (left is "
            "built before right)."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - slice lists and call .index() at each level",
        brute=r"""
# BRUTE FORCE: O(n^2) time - slice lists and call .index() at each level
def build_tree(preorder, inorder):
    if not preorder:
        return None
    root = TreeNode(preorder[0])
    k = inorder.index(preorder[0])
    root.left = build_tree(preorder[1 : k + 1], inorder[:k])
    root.right = build_tree(preorder[k + 1 :], inorder[k + 1 :])
    return root
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Divide and conquer using traversal properties
def build_tree(preorder, inorder):
    pos = {v: i for i, v in enumerate(inorder)}
    it = iter(preorder)

    def build(lo, hi):
        if lo > hi:
            return None
        root = TreeNode(next(it))
        k = pos[root.val]
        root.left = build(lo, k - 1)
        root.right = build(k + 1, hi)
        return root

    return build(0, len(inorder) - 1)
""",
    ),
    # ---- Count Good Nodes in Binary Tree (LeetCode 1448) ----
    dict(
        title="Count Good Nodes in Binary Tree",
        diff="M",
        lc=1448,
        slug="count-good-nodes-in-binary-tree",
        prompt="A node is 'good' if no node on the path from the root to it has a larger value. Count the good nodes.",
        sig="def good_nodes(root: Optional[TreeNode]) -> int:",
        fn="good_nodes",
        adapt_in=T,
        tests=[
            (([3, 1, 4, 3, None, 1, 5],), 4),
            (([3, 3, None, 4, 2],), 3),
            (([1],), 1),
            (([2, 1, 3],), 2),
            (([],), 0),
        ],
        hints=[
            "What do you need to know about the path above a node?",
            "Only the maximum value so far.",
            (
                "DFS passing down the running max; a node is good if node.val >= max; pass max(max, node.val) to "
                "the children."
            ),
        ],
        pattern="DFS carrying state down the path (top-down parameter)",
        explain=(
            "Information flowing DOWN a tree travels as a parameter; information flowing UP travels as a return "
            "value.\n        Choosing the right direction is half the work in tree problems."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n*h) time - keep the whole ancestor list and test every ancestor",
        brute=r"""
# BRUTE FORCE: O(n*h) time - keep the whole ancestor list and test every ancestor
def good_nodes(root):
    def go(n, path):
        if not n:
            return 0
        good = 1 if all(v <= n.val for v in path) else 0
        return good + go(n.left, path + [n.val]) + go(n.right, path + [n.val])

    return go(root, [])
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: DFS carrying state down the path (top-down parameter)
def good_nodes(root):
    def go(n, mx):
        if not n:
            return 0
        return (n.val >= mx) + go(n.left, max(mx, n.val)) + go(n.right, max(mx, n.val))

    return go(root, float("-inf"))
""",
    ),
    # ---- Path Sum III (LeetCode 437) ----
    dict(
        title="Path Sum III",
        diff="M",
        lc=437,
        slug="path-sum-iii",
        prompt="Count downward paths (parent to child, any start and end node) whose node values sum to target.",
        sig="def path_sum(root: Optional[TreeNode], target_sum: int) -> int:",
        fn="path_sum",
        adapt_in=T,
        tests=[
            (([10, 5, -3, 3, 2, None, 11, 3, -2, None, 1], 8), 3),
            (([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, 5, 1], 22), 3),
            (([1], 1), 1),
            (([], 0), 0),
            (([1, -1, 1], 0), 1),
        ],
        hints=[
            "Brute force: treat every node as a start and DFS down. What is the cost?",
            "O(n*h). Recall 'Subarray Sum Equals K' - a root-to-node path is like an array.",
            (
                "Prefix sums on the path: count[prefix] in a dict; at each node add count[prefix - target]; undo "
                "the count when leaving the node (backtrack)."
            ),
        ],
        pattern="Prefix sums + hash map on a tree path (with backtracking of the counts)",
        explain=(
            "A downward path sum = prefix(end) - prefix(start-1) along the root-to-node route. So the number of "
            "valid\n        starts equals how many earlier prefixes equal prefix - target. The dict must be "
            "restored when returning from a\n        node, otherwise sibling branches would pollute each other."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n*h) time - DFS downward from every node",
        brute=r"""
# BRUTE FORCE: O(n*h) time - DFS downward from every node
def path_sum(root, target_sum):
    def from_node(n, remain):
        if not n:
            return 0
        remain -= n.val
        return (remain == 0) + from_node(n.left, remain) + from_node(n.right, remain)

    def go(n):
        if not n:
            return 0
        return from_node(n, target_sum) + go(n.left) + go(n.right)

    return go(root)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Prefix sums + hash map on a tree path (with backtracking of the counts)
def path_sum(root, target_sum):
    count = defaultdict(int)
    count[0] = 1

    def dfs(n, prefix):
        if not n:
            return 0
        prefix += n.val
        res = count[prefix - target_sum]
        count[prefix] += 1
        res += dfs(n.left, prefix) + dfs(n.right, prefix)
        count[prefix] -= 1  # backtrack
        return res

    return dfs(root, 0)
""",
    ),
    # ---- Lowest Common Ancestor of a Binary Search Tree (LeetCode 235) ----
    dict(
        title="Lowest Common Ancestor of a Binary Search Tree",
        diff="M",
        lc=235,
        slug="lowest-common-ancestor-of-a-binary-search-tree",
        prompt=(
            "Given a BST and two nodes p and q, return their lowest common ancestor (the deepest node that has both "
            "as descendants; a node may be its own descendant)."
        ),
        sig="def lowest_common_ancestor(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> TreeNode:",
        fn="lowest_common_ancestor",
        adapt_in=lambda a: (lambda r: (r, find_node(r, a[1]), find_node(r, a[2])))(list_to_tree(a[0])),
        adapt_out=lambda n: n.val,
        tests=[
            (([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 8), 6),
            (([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 4), 2),
            (([2, 1], 2, 1), 2),
            (([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 3, 5), 4),
            (([6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 0, 5), 2),
        ],
        hints=[
            "For a general tree you need to search both subtrees. What extra information does a BST give?",
            "Left < node < right: compare p and q with the current node's value.",
            (
                "If both are smaller go left; if both are larger go right; otherwise the current node is the split "
                "point = the LCA."
            ),
        ],
        pattern="BST property turns a search into a single downward walk",
        explain=(
            "The LCA is the first node where p and q 'disagree' about direction (or where one of them equals the "
            "node).\n        No recursion or stack needed: O(h) time, O(1) space."
        ),
        cx="O(h) time, O(1) space",
        brute_cx="O(n) time, O(h) space - root-to-node paths, last common node (works for any tree)",
        brute=r"""
# BRUTE FORCE: O(n) time, O(h) space - root-to-node paths, last common node (works for any tree)
def lowest_common_ancestor(root, p, q):
    def path(n, target):
        if not n:
            return None
        if n is target:
            return [n]
        for ch in (n.left, n.right):
            r = path(ch, target)
            if r:
                return [n] + r
        return None

    a, b, lca = path(root, p), path(root, q), None
    for x, y in zip(a, b):
        if x is y:
            lca = x
    return lca
""",
        solution=r"""
# OPTIMISED: O(h) time, O(1) space
# Idea: BST property turns a search into a single downward walk
def lowest_common_ancestor(root, p, q):
    cur = root
    while cur:
        if p.val < cur.val and q.val < cur.val:
            cur = cur.left
        elif p.val > cur.val and q.val > cur.val:
            cur = cur.right
        else:
            return cur
""",
    ),
    # ---- House Robber III (LeetCode 337) ----
    dict(
        title="House Robber III",
        diff="M",
        lc=337,
        slug="house-robber-iii",
        prompt=(
            "Houses form a binary tree. Robbing two directly linked houses (parent and child) triggers the alarm. "
            "Return the maximum amount you can rob."
        ),
        sig="def rob(root: Optional[TreeNode]) -> int:",
        fn="rob",
        adapt_in=T,
        tests=[
            (([3, 2, 3, None, 3, None, 1],), 7),
            (([3, 4, 5, 1, 3, None, 1],), 9),
            (([1],), 1),
            (([],), 0),
            (([2, 1, 3, None, 4],), 7),
        ],
        hints=[
            "At each node you either rob it or you do not. What does each choice allow for the children?",
            (
                "Rob it -> you must skip both children (but may take the grandchildren). Skip it -> you may rob (or "
                "skip) each child freely."
            ),
            (
                "Return a pair (best_if_robbed, best_if_skipped) from each subtree: robbed = val + l.skipped + "
                "r.skipped; skipped = max(l) + max(r)."
            ),
        ],
        pattern="Tree DP returning a pair of states (take / skip)",
        explain=(
            "This is House Robber on a tree. Returning both states from the recursion avoids the exponential "
            "blow-up of\n        recomputing grandchildren: each node is visited once."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(2^n)-ish - recursion that recomputes children and grandchildren",
        brute=r"""
# BRUTE FORCE: O(2^n)-ish - recursion that recomputes children and grandchildren
def rob(root):
    if not root:
        return 0
    take = root.val
    if root.left:
        take += rob(root.left.left) + rob(root.left.right)
    if root.right:
        take += rob(root.right.left) + rob(root.right.right)
    return max(take, rob(root.left) + rob(root.right))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: Tree DP returning a pair of states (take / skip)
def rob(root):
    def dfs(n):
        if not n:
            return 0, 0  # (robbed, skipped)
        lr, ls = dfs(n.left)
        rr, rs = dfs(n.right)
        return n.val + ls + rs, max(lr, ls) + max(rr, rs)

    return max(dfs(root))
""",
    ),
    # ---- Serialize and Deserialize Binary Tree (LeetCode 297) ----
    dict(
        title="Serialize and Deserialize Binary Tree",
        diff="H",
        lc=297,
        slug="serialize-and-deserialize-binary-tree",
        prompt=(
            "Design an algorithm to turn a binary tree into a string and back. Define serialize(root) -> str and "
            "deserialize(data) -> root yourself, plus roundtrip(root) that returns deserialize(serialize(root)) "
            "(this is what the tests call)."
        ),
        sig=(
            "def serialize(root: Optional[TreeNode]) -> str:\n    pass\n\ndef deserialize(data: str) -> "
            "Optional[TreeNode]:\n    pass\n\ndef roundtrip(root: Optional[TreeNode]) -> Optional[TreeNode]:\n    "
            "return deserialize(serialize(root))"
        ),
        fn="roundtrip",
        adapt_in=T,
        adapt_out=tree_to_list,
        tests=[
            (([1, 2, 3, None, None, 4, 5],), [1, 2, 3, None, None, 4, 5]),
            (([],), []),
            (([1],), [1]),
            (([1, 2],), [1, 2]),
            (([1, None, 2, None, 3],), [1, None, 2, None, 3]),
        ],
        hints=[
            (
                "The string must contain enough information to rebuild the shape, not just the values. What marks a "
                "missing child?"
            ),
            "Use a sentinel (e.g. '#') for None in a preorder traversal.",
            (
                "serialize: preorder, values joined by ','. deserialize: read tokens with an iterator; a '#' "
                "returns None, otherwise create a node and build left then right."
            ),
        ],
        pattern="Preorder with null markers (a traversal that is uniquely decodable)",
        explain=(
            "Preorder alone is ambiguous, but preorder WITH explicit nulls determines the tree uniquely: the "
            "recursion in\n        deserialize consumes exactly the tokens that serialize produced."
        ),
        cx="O(n) time and space",
        brute_cx="O(n) - level-order (BFS) encoding with null markers",
        brute=r"""
# BRUTE FORCE: O(n) - level-order (BFS) encoding with null markers
def serialize(root):
    out, q = [], deque([root])
    while q:
        n = q.popleft()
        if n is None:
            out.append("#")
        else:
            out.append(str(n.val))
            q.append(n.left)
            q.append(n.right)
    return ",".join(out)


def deserialize(data):
    toks = data.split(",")
    if toks[0] == "#":
        return None
    root = TreeNode(int(toks[0]))
    q, i = deque([root]), 1
    while q:
        n = q.popleft()
        if toks[i] != "#":
            n.left = TreeNode(int(toks[i]))
            q.append(n.left)
        i += 1
        if toks[i] != "#":
            n.right = TreeNode(int(toks[i]))
            q.append(n.right)
        i += 1
    return root


def roundtrip(root):
    return deserialize(serialize(root))
""",
        solution=r"""
# OPTIMISED: O(n) time and space
# Idea: Preorder with null markers (a traversal that is uniquely decodable)
def serialize(root):
    out = []

    def go(n):
        if not n:
            out.append("#")
            return
        out.append(str(n.val))
        go(n.left)
        go(n.right)

    go(root)
    return ",".join(out)


def deserialize(data):
    it = iter(data.split(","))

    def build():
        tok = next(it)
        if tok == "#":
            return None
        node = TreeNode(int(tok))
        node.left = build()
        node.right = build()
        return node

    return build()


def roundtrip(root):
    return deserialize(serialize(root))
""",
    ),
]
