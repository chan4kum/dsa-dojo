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

from core import list_to_tree


def T(a):
    """Turn the level-order list in args[0] into a tree; keep the other arguments as they are."""
    return (list_to_tree(a[0]),) + tuple(a[1:])


def _bst_ok(args, got):
    """got is a TreeNode: height-balanced BST whose inorder equals the sorted input."""

    def ino(n):
        return ino(n.left) + [n.val] + ino(n.right) if n else []

    def bal(n):
        if not n:
            return 0
        left, right = bal(n.left), bal(n.right)
        return -1 if left < 0 or right < 0 or abs(left - right) > 1 else 1 + max(left, right)

    return ino(got) == args[0] and bal(got) >= 0


PROBLEMS = [
    # ---- Path Sum (LeetCode 112) ----
    dict(
        title="Path Sum",
        diff="E",
        lc=112,
        slug="path-sum",
        prompt="Is there a root-to-LEAF path whose node values add up to target?",
        sig="def has_path_sum(root: Optional[TreeNode], target: int) -> bool:",
        fn="has_path_sum",
        adapt_in=T,
        tests=[
            (([5, 4, 8, 11, None, 13, 4, 7, 2, None, None, None, 1], 22), True),
            (([1, 2, 3], 5), False),
            (([], 0), False),
            (([1, 2], 1), False),
            (([1], 1), True),
            (([-2, None, -3], -5), True),
        ],
        hints=[
            "Subtract the node value as you go down; what is left must be matched by the rest.",
            "At a LEAF, check remaining == node.val. A node with one child is not a leaf.",
            "return dfs(left, rem - val) or dfs(right, rem - val).",
        ],
        pattern="DFS carrying a running remainder (top-down)",
        explain=(
            "Pass state down the recursion instead of recomputing path sums. The base case is the leaf, not None, "
            "because the path must end at a leaf."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n*h) time - enumerate all root-to-leaf paths then sum",
        brute=r"""
# BRUTE FORCE: O(n*h) time - enumerate all root-to-leaf paths then sum
def has_path_sum(root, target):
    paths = []

    def go(n, path):
        if not n:
            return
        path = path + [n.val]
        if not n.left and not n.right:
            paths.append(path)
        go(n.left, path)
        go(n.right, path)

    go(root, [])
    return any(sum(p) == target for p in paths)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: DFS carrying a running remainder (top-down)
def has_path_sum(root, target):
    if not root:
        return False
    if not root.left and not root.right:
        return root.val == target
    rem = target - root.val
    return has_path_sum(root.left, rem) or has_path_sum(root.right, rem)
""",
    ),
    # ---- Minimum Depth of Binary Tree (LeetCode 111) ----
    dict(
        title="Minimum Depth of Binary Tree",
        diff="E",
        lc=111,
        slug="minimum-depth-of-binary-tree",
        prompt="Return the number of nodes on the shortest path from the root to a LEAF (0 for an empty tree).",
        sig="def min_depth(root: Optional[TreeNode]) -> int:",
        fn="min_depth",
        adapt_in=T,
        tests=[
            (([3, 9, 20, None, None, 15, 7],), 2),
            (([2, None, 3, None, 4, None, 5, None, 6],), 5),
            (([],), 0),
            (([1],), 1),
            (([1, 2],), 2),
        ],
        hints=[
            "Careful: a node with only one child is not a leaf, so min(left, right) is wrong when one side is empty.",
            "BFS level by level: the first leaf you meet gives the answer immediately.",
            "Recursive: if one child is missing use the other child's depth + 1.",
        ],
        pattern="BFS for the nearest leaf (early exit)",
        explain="Level-order reaches the shallowest leaf first, so you can stop without visiting the whole tree.",
        cx="O(n) time, O(w) space",
        brute_cx="O(n) time - full recursion over every node",
        brute=r"""
# BRUTE FORCE: O(n) time - full recursion over every node
def min_depth(root):
    if not root:
        return 0
    if not root.left:
        return 1 + min_depth(root.right)
    if not root.right:
        return 1 + min_depth(root.left)
    return 1 + min(min_depth(root.left), min_depth(root.right))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(w) space
# Idea: BFS for the nearest leaf (early exit)
def min_depth(root):
    if not root:
        return 0
    q, d = deque([root]), 1
    while q:
        for _ in range(len(q)):
            n = q.popleft()
            if not n.left and not n.right:
                return d
            if n.left:
                q.append(n.left)
            if n.right:
                q.append(n.right)
        d += 1
""",
    ),
    # ---- Sum Root to Leaf Numbers (LeetCode 129) ----
    dict(
        title="Sum Root to Leaf Numbers",
        diff="M",
        lc=129,
        slug="sum-root-to-leaf-numbers",
        prompt=(
            "Each root-to-leaf path of digits forms a number (e.g. 1->2->3 is 123). Return the sum of all such numbers."
        ),
        sig="def sum_numbers(root: Optional[TreeNode]) -> int:",
        fn="sum_numbers",
        adapt_in=T,
        tests=[
            (([1, 2, 3],), 25),
            (([4, 9, 0, 5, 1],), 1026),
            (([],), 0),
            (([5],), 5),
            (([1, 0],), 10),
        ],
        hints=[
            "Going down a level means value = value * 10 + digit.",
            "Pass the number formed so far as a parameter.",
            "At a leaf return the number; otherwise return the sum of both subtrees' results.",
        ],
        pattern="DFS carrying an accumulated value (top-down)",
        explain=(
            "The prefix of a path is summarised by one integer. Each step extends it, and leaves turn it into part "
            "of the answer."
        ),
        cx="O(n) time, O(h) space",
        brute_cx="O(n*h) time - collect all paths as strings",
        brute=r"""
# BRUTE FORCE: O(n*h) time - collect all paths as strings
def sum_numbers(root):
    paths = []

    def go(n, s):
        if not n:
            return
        s += str(n.val)
        if not n.left and not n.right:
            paths.append(s)
        go(n.left, s)
        go(n.right, s)

    go(root, "")
    return sum(int(p) for p in paths)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(h) space
# Idea: DFS carrying an accumulated value (top-down)
def sum_numbers(root):
    def go(n, acc):
        if not n:
            return 0
        acc = acc * 10 + n.val
        if not n.left and not n.right:
            return acc
        return go(n.left, acc) + go(n.right, acc)

    return go(root, 0)
""",
    ),
    # ---- Find Largest Value in Each Tree Row (LeetCode 515) ----
    dict(
        title="Find Largest Value in Each Tree Row",
        diff="M",
        lc=515,
        slug="find-largest-value-in-each-tree-row",
        prompt="Return the largest value on each level of the tree, top to bottom.",
        sig="def largest_values(root: Optional[TreeNode]) -> List[int]:",
        fn="largest_values",
        adapt_in=T,
        tests=[
            (([1, 3, 2, 5, 3, None, 9],), [1, 3, 9]),
            (([1, 2, 3],), [1, 3]),
            (([],), []),
            (([7],), [7]),
            (([0, -1, -3, None, -2],), [0, -1, -2]),
        ],
        hints=[
            "This is level-order traversal with a reduction per level.",
            "Process the queue one level at a time (take len(queue) as the level size).",
            "For each level track max(node values) and append to the answer.",
        ],
        pattern="BFS by levels (aggregate per level)",
        explain=(
            "Capture the queue length at the start of each level; exactly those nodes belong to the level, so you "
            "can reduce them."
        ),
        cx="O(n) time, O(w) space",
        brute_cx="O(n*h) time - compute each node's depth recursively and group",
        brute=r"""
# BRUTE FORCE: O(n*h) time - compute each node's depth recursively and group
def largest_values(root):
    best = {}

    def go(n, d):
        if not n:
            return
        best[d] = max(best.get(d, n.val), n.val)
        go(n.left, d + 1)
        go(n.right, d + 1)

    go(root, 0)
    return [best[d] for d in sorted(best)]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(w) space
# Idea: BFS by levels (aggregate per level)
def largest_values(root):
    if not root:
        return []
    out, q = [], deque([root])
    while q:
        m = None
        for _ in range(len(q)):
            n = q.popleft()
            m = n.val if m is None else max(m, n.val)
            if n.left:
                q.append(n.left)
            if n.right:
                q.append(n.right)
        out.append(m)
    return out
""",
    ),
    # ---- Convert Sorted Array to Binary Search Tree (LeetCode 108) ----
    dict(
        title="Convert Sorted Array to Binary Search Tree",
        diff="E",
        lc=108,
        slug="convert-sorted-array-to-binary-search-tree",
        prompt=(
            "Build a height-balanced BST from a sorted array (any valid tree is accepted; the tests check BST order "
            "and balance)."
        ),
        sig="def sorted_array_to_bst(nums: List[int]) -> Optional[TreeNode]:",
        fn="sorted_array_to_bst",
        check=_bst_ok,
        tests=[
            (([-10, -3, 0, 5, 9],), None),
            (([1, 3],), None),
            (([1],), None),
            (([1, 2, 3, 4, 5, 6, 7],), None),
            (([],), None),
        ],
        hints=[
            "Which element should be the root so both sides are about the same size?",
            "The middle element. Recurse on the left half and the right half.",
            (
                "build(lo, hi): if lo > hi return None; mid = (lo+hi)//2; root = Node(nums[mid]); recurse on (lo, "
                "mid-1) and (mid+1, hi)."
            ),
        ],
        pattern="Divide and conquer on the midpoint (balanced construction)",
        explain=(
            "Choosing the median as root halves the problem every time, so height is log n. Sorted order = inorder, "
            "which keeps the BST property."
        ),
        cx="O(n) time, O(log n) space",
        brute_cx=(
            "O(n^2) worst - insert one by one in a bad order gives a skewed tree (still a valid BST but NOT balanced)"
        ),
        brute=r"""
# BRUTE FORCE: O(n^2) worst - insert one by one in a bad order gives a skewed tree (still a valid BST but NOT balanced)
def sorted_array_to_bst(nums):
    # slicing version: same idea but copies sub-lists (O(n log n) extra work)
    if not nums:
        return None
    m = len(nums) // 2
    root = TreeNode(nums[m])
    root.left = sorted_array_to_bst(nums[:m])
    root.right = sorted_array_to_bst(nums[m + 1 :])
    return root
""",
        solution=r"""
# OPTIMISED: O(n) time, O(log n) space
# Idea: Divide and conquer on the midpoint (balanced construction)
def sorted_array_to_bst(nums):
    def build(lo, hi):
        if lo > hi:
            return None
        mid = (lo + hi) // 2
        node = TreeNode(nums[mid])
        node.left = build(lo, mid - 1)
        node.right = build(mid + 1, hi)
        return node

    return build(0, len(nums) - 1)
""",
    ),
]
