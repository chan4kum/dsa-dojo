"""Random-input generators for tools/fuzz_diff.py (batch 4 onwards).

GX maps (topic, problem title) -> a function returning one random argument tuple.
A value may also be (generator, normaliser) when answers need normalising before they are compared.
"""

import random
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from core import TreeNode, tree_to_list  # noqa: E402

R = random.randint


def ints(n, lo, hi, k=0):
    return [R(lo, hi) for _ in range(R(k, n))]


def st(alpha, lo, hi):
    return "".join(random.choice(alpha) for _ in range(R(lo, hi)))


def rand_tree(n_max, lo=0, hi=9, unique=False):
    """A random binary tree (any shape) with up to n_max nodes; returns the root (or None)."""
    n = R(0, n_max)
    if n == 0:
        return None
    values = random.sample(range(lo, lo + max(hi - lo + 1, n)), n) if unique else [R(lo, hi) for _ in range(n)]
    root = TreeNode(values[0])
    free = [(root, "left"), (root, "right")]  # empty child slots
    for v in values[1:]:
        node, side = free.pop(R(0, len(free) - 1))
        child = TreeNode(v)
        setattr(node, side, child)
        free += [(child, "left"), (child, "right")]
    return root


def tree_list(n_max, lo=0, hi=9, unique=False):
    return tree_to_list(rand_tree(n_max, lo, hi, unique))


def bst_list(n_max):
    """A random binary SEARCH tree (distinct values) as a level-order list."""
    values = random.sample(range(0, 40), R(0, n_max))
    root = None
    for v in values:
        if root is None:
            root = TreeNode(v)
            continue
        node = root
        while True:
            side = "left" if v < node.val else "right"
            if getattr(node, side) is None:
                setattr(node, side, TreeNode(v))
                break
            node = getattr(node, side)
    return tree_to_list(root)


def traversals():
    """(inorder, postorder) of a random tree with distinct values."""
    root = rand_tree(9, 0, 30, unique=True)
    ino, post = [], []

    def walk(n):
        if n:
            walk(n.left)
            ino.append(n.val)
            walk(n.right)
            post.append(n.val)

    walk(root)
    return (ino, post)


def digits():
    n = R(1, 5)
    return [R(1, 9)] + [R(0, 9) for _ in range(n - 1)] if R(0, 5) else [0]


def path_sum_args():
    lst = tree_list(9, 0, 5)
    return (lst, R(0, 15))


def delete_args():
    lst = tree_list(9, 1, 20, unique=True)
    vals = [v for v in lst if v is not None]
    return (lst, random.sample(vals, R(0, len(vals))) if vals else [])


GX = {
    ("linked_list", "Swap Nodes in Pairs"): lambda: (ints(8, 0, 9),),
    ("linked_list", "Rotate List"): lambda: (ints(8, 0, 9), R(0, 12)),
    ("linked_list", "Remove Duplicates from Sorted List II"): lambda: (sorted(ints(9, 0, 4)),),
    ("linked_list", "Partition List"): lambda: (ints(8, 0, 9), R(0, 9)),
    ("linked_list", "Odd Even Linked List"): lambda: (ints(8, 0, 9),),
    ("linked_list", "Remove Linked List Elements"): lambda: (ints(8, 0, 4), R(0, 4)),
    ("linked_list", "Add Two Numbers II"): lambda: (digits(), digits()),
    ("linked_list", "Sort List"): lambda: (ints(8, -5, 5),),
    ("trees", "Binary Tree Inorder Traversal"): lambda: (tree_list(10),),
    ("trees", "Binary Tree Postorder Traversal"): lambda: (tree_list(10),),
    ("trees", "Binary Tree Zigzag Level Order Traversal"): lambda: (tree_list(10),),
    ("trees", "Binary Tree Paths"): lambda: (tree_list(9),),
    ("trees", "Count Complete Tree Nodes"): lambda: (list(range(1, R(0, 20) + 1)),),
    ("trees", "Construct Binary Tree from Inorder and Postorder Traversal"): traversals,
    ("trees", "Search in a Binary Search Tree"): lambda: (bst_list(9), R(0, 39)),
    ("trees", "Convert BST to Greater Tree"): lambda: (bst_list(9),),
    ("trees", "Path Sum II"): path_sum_args,
    ("trees", "Sum of Left Leaves"): lambda: (tree_list(10),),
    ("trees", "Merge Two Binary Trees"): lambda: (tree_list(8), tree_list(8)),
    ("trees", "Average of Levels in Binary Tree"): lambda: (tree_list(10),),
    ("trees", "Maximum Width of Binary Tree"): lambda: (tree_list(10),),
    ("trees", "Longest Univalue Path"): lambda: (tree_list(10, 0, 2),),
    ("trees", "Binary Tree Cameras"): lambda: (tree_list(9),),
    ("trees", "Delete Nodes And Return Forest"): delete_args,
    ("trees", "Lowest Common Ancestor of Deepest Leaves"): lambda: (tree_list(10, 0, 20, unique=True),),
}


def _undirected(n, k):
    edges = set()
    for _ in range(R(0, k)):
        if n > 1:
            u, v = random.sample(range(n), 2)
            edges.add((min(u, v), max(u, v)))
    return [list(e) for e in sorted(edges)]


def _adj(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    return adj


def path_args():
    n = R(1, 8)
    return (n, _undirected(n, 10), R(0, n - 1), R(0, n - 1))


def dag_args():
    n = R(2, 7)
    return ([[j for j in range(i + 1, n) if R(0, 9) < 4] for i in range(n)],)


def bipartite_args():
    n = R(1, 8)
    return (_adj(n, _undirected(n, 10)),)


def division_args():
    names = "abcde"
    hidden = {c: random.choice([0.25, 0.5, 1.0, 2.0, 4.0, 8.0]) for c in names}
    eqs, vals = [], []
    for _ in range(R(1, 5)):
        a, b = random.sample(names, 2)
        eqs.append([a, b])
        vals.append(hidden[a] / hidden[b])
    qs = [[random.choice("abcdez"), random.choice("abcdez")] for _ in range(R(1, 5))]
    return (eqs, vals, qs)


def stones_args():
    cells = random.sample([(r, c) for r in range(5) for c in range(5)], R(1, 8))
    return ([list(c) for c in cells],)


def equality_args():
    return ([f"{random.choice('abcd')}{random.choice(['==', '!='])}{random.choice('abcd')}" for _ in range(R(1, 6))],)


def effort_args():
    rows, cols = R(1, 4), R(1, 4)
    return ([[R(1, 9) for _ in range(cols)] for _ in range(rows)],)


def city_args():
    n = R(1, 6)
    edges = [[u, v, R(1, 5)] for u, v in _undirected(n, 9)]
    return (n, edges, R(1, 8))


def probability_args():
    n = R(2, 6)
    edges = _undirected(n, 8)
    probs = [random.choice([0.125, 0.25, 0.5, 1.0]) for _ in edges]
    start, end = random.sample(range(n), 2)
    return (n, edges, probs, start, end)


def mht_args():
    n = R(1, 9)
    return (n, [[i, R(0, i - 1)] for i in range(1, n)])


GX2 = {
    ("graphs", "Find if Path Exists in Graph"): path_args,
    ("graphs", "All Paths From Source to Target"): dag_args,
    ("graphs", "Is Graph Bipartite?"): bipartite_args,
    ("graphs", "Evaluate Division"): division_args,
    ("graphs", "Most Stones Removed with Same Row or Column"): stones_args,
    ("graphs", "Satisfiability of Equality Equations"): equality_args,
    ("graphs", "Path With Minimum Effort"): effort_args,
    (
        "graphs",
        "Find the City With the Smallest Number of Neighbors at a Threshold Distance",
    ): city_args,
    ("graphs", "Path with Maximum Probability"): probability_args,
    ("graphs", "Minimum Height Trees"): mht_args,
}
GX.update(GX2)


def stone_args():
    while True:
        piles = [R(1, 9) for _ in range(2 * R(1, 4))]
        if sum(piles) % 2:
            return (piles,)


def dungeon_args():
    return ([[R(-9, 9) for _ in range(3)] for _ in range(R(1, 4))],)


GX3 = {
    ("dynamic_programming", "Integer Break"): lambda: (R(2, 13),),
    ("dynamic_programming", "Arithmetic Slices"): lambda: (ints(10, -3, 6),),
    ("dynamic_programming", "Predict the Winner"): lambda: ([R(0, 9) for _ in range(R(1, 9))],),
    ("dynamic_programming", "Delete Operation for Two Strings"): lambda: (st("abc", 0, 7), st("abc", 0, 7)),
    ("dynamic_programming", "Maximum Length of Repeated Subarray"): lambda: (ints(8, 0, 3), ints(8, 0, 3)),
    ("dynamic_programming", "Stone Game"): stone_args,
    ("dynamic_programming", "Is Subsequence"): lambda: (st("abc", 0, 4), st("abc", 0, 8)),
    ("dynamic_programming", "Uncrossed Lines"): lambda: (ints(7, 1, 4), ints(7, 1, 4)),
    ("dynamic_programming", "Minimum Insertion Steps to Make a String Palindrome"): lambda: (st("abc", 1, 9),),
    ("dynamic_programming", "Number of Dice Rolls With Target Sum"): lambda: (R(1, 4), R(1, 5), R(1, 16)),
    ("dynamic_programming", "Dungeon Game"): dungeon_args,
    ("dynamic_programming", "Longest Valid Parentheses"): lambda: (st("()", 0, 12),),
    ("dynamic_programming", "Wildcard Matching"): lambda: (st("ab", 0, 6), st("ab?*", 0, 6)),
    ("dynamic_programming", "Best Time to Buy and Sell Stock III"): lambda: (ints(9, 0, 9),),
}
GX.update(GX3)


def rotated(n_max=8):
    arr = sorted(ints(n_max, 0, 4, 1))
    k = R(0, len(arr) - 1)
    return arr[k:] + arr[:k]


def mountain():
    n = R(3, 9)
    vals = random.sample(range(40), n)
    peak = max(vals)
    rest = [v for v in vals if v != peak]
    random.shuffle(rest)
    i = R(1, len(rest) - 1)
    return sorted(rest[:i]) + [peak] + sorted(rest[i:], reverse=True)


def balanced_str():
    k = R(1, 5)
    chars = list("L" * k + "R" * k)
    random.shuffle(chars)
    return ("".join(chars),)


def paren_valid():
    out, depth = [], 0
    for _ in range(R(1, 6) * 2):
        if depth == 0 or (R(0, 1) and len(out) < 10):
            out.append("(")
            depth += 1
        else:
            out.append(")")
            depth -= 1
    out += [")"] * depth
    return ("".join(out),)


def calc_expr(depth=0):
    parts = [random.choice(["", "-"]) if depth else ""]
    n_terms = R(1, 3)
    out = ""
    for t in range(n_terms):
        if t:
            out += random.choice([" + ", "-", " - ", "+"])
        if depth < 2 and R(0, 2) == 0:
            out += "(" + calc_expr(depth + 1) + ")"
        else:
            out += str(R(0, 20))
    return parts[0] + out


def version_str():
    return ".".join(("0" * R(0, 2)) + str(R(0, 12)) for _ in range(R(1, 4)))


def last_word_args():
    return (st("ab ", 0, 8) + "a" + st(" ", 0, 3),)


def _flowerbed():
    bed = []
    for _ in range(R(1, 9)):
        bed.append(1 if (not bed or bed[-1] == 0) and R(0, 3) == 0 else 0)
    return bed


GX4 = {
    ("greedy", "Two City Scheduling"): lambda: ([[R(1, 30), R(1, 30)] for _ in range(2 * R(1, 4))],),
    ("greedy", "Maximize Sum Of Array After K Negations"): lambda: (ints(6, -6, 6, 1), R(1, 4)),
    ("greedy", "Largest Perimeter Triangle"): lambda: (ints(8, 1, 9, 3),),
    ("greedy", "Array Partition"): lambda: ([R(-9, 9) for _ in range(2 * R(1, 4))],),
    ("greedy", "Can Place Flowers"): lambda: (_flowerbed(), R(0, 4)),
    ("greedy", "Boats to Save People"): lambda: _boats(),
    ("greedy", "Split a String in Balanced Strings"): balanced_str,
    ("greedy", "Assign Cookies"): lambda: (ints(5, 1, 5), ints(5, 1, 5)),
    ("binary_search", "Search in Rotated Sorted Array II"): lambda: (rotated(), R(0, 5)),
    ("binary_search", "Find Minimum in Rotated Sorted Array II"): lambda: (rotated(),),
    ("binary_search", "Minimum Number of Days to Make m Bouquets"): lambda: (ints(8, 1, 9, 1), R(1, 3), R(1, 3)),
    ("binary_search", "Peak Index in a Mountain Array"): lambda: (mountain(),),
    ("binary_search", "Find the Smallest Divisor Given a Threshold"): lambda: _divisor(),
    ("binary_search", "Kth Missing Positive Number"): lambda: _missing(),
    ("stack_monotonic", "Remove Outermost Parentheses"): paren_valid,
    ("stack_monotonic", "Minimum Add to Make Parentheses Valid"): lambda: (st("()", 0, 10),),
    ("stack_monotonic", "Sum of Subarray Minimums"): lambda: (ints(9, 1, 9, 1),),
    ("stack_monotonic", "Maximal Rectangle"): lambda: (
        [[random.choice("01") for _ in range(3)] for _ in range(R(1, 4))],
    ),
    ("stack_monotonic", "Basic Calculator"): lambda: (calc_expr(),),
    ("stack_monotonic", "Make The String Great"): lambda: (st("aAbB", 0, 10),),
    ("strings", "Length of Last Word"): last_word_args,
    ("strings", "Compare Version Numbers"): lambda: (version_str(), version_str()),
    ("strings", "Number of Segments in a String"): lambda: (st("ab ", 0, 10),),
    ("strings", "Reverse String II"): lambda: (st("abcd", 0, 10), R(1, 5)),
    ("strings", "Reverse Words in a String III"): lambda: (" ".join(st("abc", 1, 5) for _ in range(R(1, 4))),),
    ("strings", "Merge Strings Alternately"): lambda: (st("abc", 0, 6), st("xyz", 0, 6)),
    ("strings", "Shortest Palindrome"): lambda: (st("ab", 0, 9),),
}


def _bin_grid():
    return [[random.choice("01") for _ in range(3)] for _ in range(R(1, 4))]


def _boats():
    limit = R(3, 8)
    return ([R(1, limit) for _ in range(R(1, 7))], limit)


def _divisor():
    nums = ints(6, 1, 9, 1)
    return (nums, R(len(nums), len(nums) * 9))


def _missing():
    arr = sorted(random.sample(range(1, 15), R(1, 7)))
    return (arr, R(1, 8))


GX.update(GX4)


GX5 = {
    ("array_tricks", "Majority Element II"): lambda: (ints(9, 0, 3, 1),),
    ("array_tricks", "Find All Numbers Disappeared in an Array"): lambda: _disappeared(),
    ("array_tricks", "Max Consecutive Ones"): lambda: (ints(10, 0, 1, 1),),
    ("array_tricks", "Pascal's Triangle"): lambda: (R(1, 8),),
    ("array_tricks", "Pascal's Triangle II"): lambda: (R(0, 9),),
    ("array_tricks", "Third Maximum Number"): lambda: (ints(7, -4, 6, 1),),
    ("array_tricks", "Maximum Product of Three Numbers"): lambda: (ints(8, -9, 9, 3),),
    ("array_tricks", "Non-decreasing Array"): lambda: (ints(7, 0, 6, 1),),
}


def _disappeared():
    n = R(1, 8)
    return ([R(1, n) for _ in range(n)],)


GX.update(GX5)


def _toeplitz():
    rows, cols = R(1, 4), R(1, 4)
    if R(0, 1):
        return ([[R(0, 2) for _ in range(cols)] for _ in range(rows)],)
    first = [R(0, 3) for _ in range(rows + cols - 1)]
    return ([[first[c - r + rows - 1] for c in range(cols)] for r in range(rows)],)


def _times():
    return (["%02d:%02d" % (R(0, 23), R(0, 59)) for _ in range(R(2, 6))],)


def _poison():
    return (sorted(set(ints(6, 1, 15, 1))), R(1, 5))


def _ipo():
    n = R(1, 6)
    return (R(1, 4), R(0, 4), [R(0, 9) for _ in range(n)], [R(0, 6) for _ in range(n)])


def _vowels():
    s = st("abcde", 1, 9)
    return (s, R(1, len(s)))


def _isomorphic():
    n = R(1, 7)
    return (st("abc", n, n), st("xyz", n, n))


def _word_pattern():
    return (st("ab", 1, 5), " ".join(random.choice(["x", "y", "z"]) for _ in range(R(1, 5))))


def _grumpy():
    n = R(1, 8)
    return ([R(0, 9) for _ in range(n)], [R(0, 1) for _ in range(n)], R(1, n))


def _odd_cells_args():
    m, n = R(1, 5), R(1, 5)
    return (m, n, [[R(0, m - 1), R(0, n - 1)] for _ in range(R(0, 5))])


GX6 = {
    ("sliding_window", "Maximum Number of Vowels in a Substring of Given Length"): _vowels,
    ("sliding_window", "Grumpy Bookstore Owner"): _grumpy,
    ("sliding_window", "Binary Subarrays With Sum"): lambda: (ints(9, 0, 1, 1), R(0, 3)),
    ("sliding_window", "Subarrays with K Different Integers"): lambda: (ints(8, 1, 3, 1), R(1, 3)),
    ("heap", "IPO"): _ipo,
    ("backtracking", "Letter Tile Possibilities"): lambda: (st("ABC", 1, 6),),
    ("backtracking", "Non-decreasing Subsequences"): lambda: (ints(8, 0, 3, 1),),
    ("backtracking", "N-Queens II"): lambda: (R(1, 7),),
    ("hashing", "Intersection of Two Arrays"): lambda: (ints(6, 0, 5), ints(6, 0, 5)),
    ("hashing", "Intersection of Two Arrays II"): lambda: (ints(6, 0, 5), ints(6, 0, 5)),
    ("hashing", "First Unique Character in a String"): lambda: (st("abc", 1, 8),),
    ("hashing", "Isomorphic Strings"): _isomorphic,
    ("hashing", "Word Pattern"): _word_pattern,
    ("matrix", "Toeplitz Matrix"): _toeplitz,
    ("matrix", "Flipping an Image"): lambda: (_square01(),),
    ("matrix", "Cells with Odd Values in a Matrix"): _odd_cells_args,
    ("matrix", "Special Positions in a Binary Matrix"): lambda: (_bin_rect(),),
    ("two_pointers", "Backspace String Compare"): lambda: (st("ab#", 0, 8), st("ab#", 0, 8)),
    ("two_pointers", "Long Pressed Name"): lambda: _long_pressed(),
    ("two_pointers", "Valid Palindrome II"): lambda: (st("ab", 1, 9),),
    ("intervals", "Teemo Attacking"): _poison,
    ("intervals", "Minimum Time Difference"): _times,
    ("prefix_sums", "Running Sum of 1d Array"): lambda: (ints(8, -5, 5),),
    ("prefix_sums", "Sum of All Odd Length Subarrays"): lambda: (ints(9, 1, 9, 1),),
}


def _square01():
    n = R(1, 4)
    return [[R(0, 1) for _ in range(n)] for _ in range(n)]


def _bin_rect():
    return [[R(0, 1) for _ in range(3)] for _ in range(R(1, 4))]


def _long_pressed():
    name = st("abc", 1, 5)
    typed = "".join(ch * R(1, 2) for ch in name) if R(0, 2) else st("abc", 1, 7)
    return (name, typed)


GX.update(GX6)


def _bst_min2():
    while True:
        lst = bst_list(9)
        if len([v for v in lst if v is not None]) >= 2:
            return lst


def _nonempty_tree(n_max=9, lo=0, hi=9, unique=False):
    while True:
        lst = tree_list(n_max, lo, hi, unique)
        if lst:
            return lst


def _bst_nonempty():
    while True:
        lst = bst_list(9)
        if lst:
            return lst


def _cousin_args():
    while True:
        lst = tree_list(9, 0, 30, unique=True)
        vals = [v for v in lst if v is not None]
        if len(vals) >= 2:
            x, y = random.sample(vals, 2)
            return (lst, x, y)


def _row_args():
    return (_nonempty_tree(8), R(0, 9), R(1, 4))


GX7 = {
    ("trees", "Binary Tree Preorder Traversal"): lambda: (tree_list(10),),
    ("trees", "Minimum Absolute Difference in BST"): lambda: (_bst_min2(),),
    ("trees", "Binary Tree Tilt"): lambda: (tree_list(10),),
    ("trees", "Two Sum IV - Input is a BST"): lambda: (bst_list(9), R(0, 70)),
    ("trees", "Trim a Binary Search Tree"): lambda: _trim_args(),
    ("trees", "Leaf-Similar Trees"): lambda: (tree_list(7, 0, 2), tree_list(7, 0, 2)),
    ("trees", "Range Sum of BST"): lambda: _range_args(),
    ("trees", "Univalued Binary Tree"): lambda: (_nonempty_tree(8, 0, 1),),
    ("trees", "Cousins in Binary Tree"): _cousin_args,
    ("trees", "Maximum Difference Between Node and Ancestor"): lambda: (_nonempty_tree(10),),
    ("trees", "Deepest Leaves Sum"): lambda: (_nonempty_tree(10),),
    ("trees", "Sum of Nodes with Even-Valued Grandparent"): lambda: (tree_list(10, 1, 9),),
    ("trees", "Maximum Level Sum of a Binary Tree"): lambda: (_nonempty_tree(10, -5, 5),),
    ("trees", "Construct Binary Search Tree from Preorder Traversal"): lambda: (_preorder_of_bst(),),
    ("trees", "Add One Row to Tree"): lambda: _row_args(),
    ("trees", "Increasing Order Search Tree"): lambda: (bst_list(9),),
}


def _trim_args():
    low = R(0, 30)
    return (bst_list(9), low, low + R(0, 25))


def _range_args():
    low = R(0, 30)
    return (bst_list(9), low, low + R(0, 25))


GX.update(GX7)


def _preorder_of_bst():
    from core import list_to_tree

    def walk(n):
        return [n.val] + walk(n.left) + walk(n.right) if n else []

    return walk(list_to_tree(_bst_nonempty()))


def _two_islands():
    while True:
        rows, cols = R(2, 4), R(2, 4)
        grid = [[R(0, 1) for _ in range(cols)] for _ in range(rows)]
        seen, count = set(), 0
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] and (r, c) not in seen:
                    count += 1
                    stack = [(r, c)]
                    seen.add((r, c))
                    while stack:
                        a, b = stack.pop()
                        for x, y in ((a + 1, b), (a - 1, b), (a, b + 1), (a, b - 1)):
                            if 0 <= x < rows and 0 <= y < cols and grid[x][y] and (x, y) not in seen:
                                seen.add((x, y))
                                stack.append((x, y))
        if count == 2:
            return (grid,)


def _pairs_1(n, k, base=0):
    edges = set()
    for _ in range(R(0, k)):
        if n > 1:
            a, b = random.sample(range(base, base + n), 2)
            edges.add((min(a, b), max(a, b)))
    return [list(e) for e in sorted(edges)]


def _swap_args():
    s = st("abcd", 1, 7)
    n = len(s)
    return (s, [[R(0, n - 1), R(0, n - 1)] for _ in range(R(0, 5))])


def _prereq_args():
    n = R(1, 6)
    pre = [[a, b] for a in range(n) for b in range(a + 1, n) if R(0, 3) == 0]
    return (n, pre, [[R(0, n - 1), R(0, n - 1)] for _ in range(R(1, 5))])


def _inform_args():
    n = R(1, 7)
    order = list(range(n))
    random.shuffle(order)
    manager = [-1] * n
    for i in range(1, n):
        manager[order[i]] = order[R(0, i - 1)]
    return (n, order[0], manager, [R(0, 5) for _ in range(n)])


def _reorder_args():
    n = R(2, 7)
    edges = []
    for i in range(1, n):
        j = R(0, i - 1)
        edges.append([i, j] if R(0, 1) else [j, i])
    return (n, edges)


GX8 = {
    ("graphs", "Shortest Bridge"): _two_islands,
    ("graphs", "Smallest String With Swaps"): _swap_args,
    ("graphs", "Number of Operations to Make Network Connected"): lambda: (lambda n: (n, _pairs_1(n, 8)))(R(1, 7)),
    ("graphs", "Possible Bipartition"): lambda: (lambda n: (n, _pairs_1(n, 8, 1)))(R(1, 7)),
    ("graphs", "Course Schedule IV"): _prereq_args,
    ("graphs", "Time Needed to Inform All Employees"): _inform_args,
    ("graphs", "Reorder Routes to Make All Paths Lead to the City Zero"): _reorder_args,
    ("graphs", "Number of Enclaves"): lambda: (_enclave_grid(),),
    ("dynamic_programming", "Fibonacci Number"): lambda: (R(0, 14),),
    ("dynamic_programming", "N-th Tribonacci Number"): lambda: (R(0, 14),),
    ("dynamic_programming", "Domino and Tromino Tiling"): lambda: (R(1, 7),),
    ("dynamic_programming", "Partition Array for Maximum Sum"): lambda: (ints(8, 0, 9, 1), R(1, 4)),
    ("dynamic_programming", "Longest Arithmetic Subsequence of Given Difference"): lambda: (ints(8, 0, 5, 1), R(-2, 2)),
    ("dynamic_programming", "Longest Arithmetic Subsequence"): lambda: (ints(8, 0, 9, 1),),
    ("dynamic_programming", "Greatest Sum Divisible by Three"): lambda: (ints(9, 1, 9, 1),),
    ("dynamic_programming", "Count Numbers with Unique Digits"): lambda: (R(0, 4),),
    ("dynamic_programming", "Out of Boundary Paths"): lambda: (R(1, 3), R(1, 3), R(0, 4), 0, 0),
}


def _enclave_grid():
    rows, cols = R(1, 5), R(1, 5)
    return [[R(0, 1) for _ in range(cols)] for _ in range(rows)]


GX.update(GX8)


def _digits_k():
    n = R(1, 6)
    num = [R(1, 9)] + [R(0, 9) for _ in range(n - 1)] if n > 1 else [R(0, 9)]
    return (num, R(1, 5000))


def _divide_args():
    divisor = 0
    while divisor == 0:
        divisor = R(-50, 50)
    return (R(-2000, 2000), divisor)


def _span():
    a = R(1, 500)
    return (a, a + R(0, 60))


GX9 = {
    ("bits_math", "Power of Four"): lambda: (R(-5, 300),),
    ("bits_math", "Convert a Number to Hexadecimal"): lambda: (R(-(2**31), 2**31 - 1) if R(0, 1) else R(-1000, 1000),),
    ("bits_math", "Number Complement"): lambda: (R(1, 1000),),
    ("bits_math", "Binary Number with Alternating Bits"): lambda: (R(1, 200),),
    ("bits_math", "Prime Number of Set Bits in Binary Representation"): lambda: (lambda a: (a, a + R(0, 60)))(
        R(1, 500)
    ),
    ("bits_math", "Binary Gap"): lambda: (R(1, 5000),),
    ("bits_math", "Number of Steps to Reduce a Number to Zero"): lambda: (R(0, 10000),),
    ("bits_math", "Add to Array-Form of Integer"): _digits_k,
    ("bits_math", "Base 7"): lambda: (R(-5000, 5000),),
    ("bits_math", "Add Digits"): lambda: (R(0, 100000),),
    ("bits_math", "Minimum Bit Flips to Convert Number"): lambda: (R(0, 1000), R(0, 1000)),
    ("bits_math", "Divide Two Integers"): _divide_args,
    ("bits_math", "XOR Operation in an Array"): lambda: (R(1, 12), R(0, 40)),
}

GX.update(GX9)


def _bits(n_max=8):
    n = R(1, n_max)
    if n == 1:
        return random.choice("01")
    return "1" + "".join(random.choice("01") for _ in range(n - 1))  # no leading zeros


def _gcd_strings():
    base = st("AB", 1, 3)
    if R(0, 1):
        return (base * R(1, 4), base * R(1, 4))
    return (st("AB", 1, 6), st("AB", 1, 6))


def _anagram_pair():
    n = R(1, 8)
    return (st("abc", n, n), st("abc", n, n))


def _find_diff():
    base = st("abc", 0, 8)
    chars = list(base + random.choice("abc"))
    random.shuffle(chars)
    return (base, "".join(chars))


def _halves():
    n = R(1, 4) * 2
    return (st("aeAEbB", n, n),)


GX10 = {
    ("strings", "Add Binary"): lambda: (_bits(), _bits()),
    ("strings", "License Key Formatting"): lambda: (st("ab-C", 0, 12), R(1, 4)),
    ("strings", "Detect Capital"): lambda: (st("aAbB", 1, 6),),
    ("strings", "Student Attendance Record I"): lambda: (st("ALP", 1, 8),),
    ("strings", "Greatest Common Divisor of Strings"): _gcd_strings,
    ("strings", "Minimum Number of Steps to Make Two Strings Anagram"): _anagram_pair,
    ("strings", "Increasing Decreasing String"): lambda: (st("abcd", 1, 10),),
    ("strings", "Consecutive Characters"): lambda: (st("abc", 1, 12),),
    ("strings", "Largest Substring Between Two Equal Characters"): lambda: (st("abc", 1, 10),),
    ("strings", "Determine if String Halves Are Alike"): _halves,
    ("strings", "Count Number of Homogenous Substrings"): lambda: (st("ab", 1, 10),),
    ("strings", "Find the Difference"): _find_diff,
    ("strings", "Longest Uncommon Subsequence I"): lambda: (st("ab", 1, 5), st("ab", 1, 5)),
    ("strings", "Find Common Characters"): lambda: ([st("abc", 1, 5) for _ in range(R(1, 4))],),
}

GX.update(GX10)


def _split_args():
    return (ints(10, 0, 9), R(1, 6))


def _swap_k():
    lst = ints(8, 0, 9, 1)
    return (lst, R(1, len(lst)))


def _zero_segments():
    out = [0]
    for _ in range(R(1, 4)):
        out += [R(1, 3) for _ in range(R(1, 3))] + [0]
    return (out,)


def _components():
    n = R(1, 8)
    values = random.sample(range(12), n)
    return (values, random.sample(values, R(1, n)))


def _merge_between():
    n = R(4, 8)
    a = R(1, n - 2)
    return (list(range(n)), a, R(a, n - 2), ints(4, 0, 9, 1))


GX11 = {
    ("linked_list", "Convert Binary Number in a Linked List to Integer"): lambda: (ints(10, 0, 1, 1),),
    ("linked_list", "Delete the Middle Node of a Linked List"): lambda: (ints(8, 0, 9, 1),),
    ("linked_list", "Maximum Twin Sum of a Linked List"): lambda: ([R(1, 9) for _ in range(R(1, 4) * 2)],),
    ("linked_list", "Split Linked List in Parts"): _split_args,
    ("linked_list", "Next Greater Node In Linked List"): lambda: (ints(8, 1, 9, 1),),
    ("linked_list", "Swapping Nodes in a Linked List"): _swap_k,
    ("linked_list", "Merge Nodes in Between Zeros"): _zero_segments,
    ("linked_list", "Linked List Components"): _components,
    ("linked_list", "Merge In Between Linked Lists"): _merge_between,
    (
        "linked_list",
        "Find the Minimum and Maximum Number of Nodes Between Critical Points",
    ): lambda: (ints(10, 1, 5, 1),),
    ("linked_list", "Remove Nodes From Linked List"): lambda: (ints(8, 1, 9, 1),),
}

GX.update(GX11)


def _weak_rows():
    m, n = R(1, 6), R(1, 6)
    mat = [[1] * c + [0] * (n - c) for c in (R(0, n) for _ in range(m))]
    return (mat, R(1, m))


def _build_args():
    return (ints(8, 1, 20, 1), R(0, 15), R(0, 3))


def _events_args():
    out = []
    for _ in range(R(1, 7)):
        start = R(1, 6)
        out.append([start, start + R(0, 4)])
    return (out,)


def _refuel_args():
    target = R(1, 60)
    positions = sorted(random.sample(range(1, target), min(R(0, 5), target - 1))) if target > 1 else []
    return (target, R(1, 30), [[p, R(1, 30)] for p in positions])


def _cpu_args():
    return ([[R(1, 8), R(1, 4)] for _ in range(R(1, 6))],)


def _prime_fraction():
    arr = [1] + sorted(random.sample([2, 3, 5, 7, 11, 13], R(1, 5)))
    return (arr, R(1, len(arr) * (len(arr) - 1) // 2))


def _intervals_args():
    out = []
    for _ in range(R(1, 7)):
        start = R(1, 10)
        out.append([start, start + R(0, 5)])
    return (out,)


GX12 = {
    ("heap", "The K Weakest Rows in a Matrix"): _weak_rows,
    ("heap", "Furthest Building You Can Reach"): _build_args,
    ("heap", "Minimum Operations to Halve Array Sum"): lambda: (ints(8, 1, 30, 1),),
    ("heap", "Maximal Score After Applying K Operations"): lambda: (ints(7, 1, 30, 1), R(1, 8)),
    ("heap", "Remove Stones to Minimize the Total"): lambda: (ints(7, 1, 30, 1), R(1, 8)),
    ("heap", "Relative Ranks"): lambda: (random.sample(range(30), R(1, 8)),),
    ("heap", "Maximum Product of Two Elements in an Array"): lambda: (ints(8, 1, 20, 2),),
    ("heap", "Maximum Number of Events That Can Be Attended"): _events_args,
    ("heap", "Minimum Number of Refueling Stops"): _refuel_args,
    ("heap", "Single-Threaded CPU"): _cpu_args,
    ("heap", "Divide Intervals Into Minimum Number of Groups"): _intervals_args,
    ("heap", "K-th Smallest Prime Fraction"): _prime_fraction,
}

GX.update(GX12)


def _balanced(max_pairs):
    n = R(1, max_pairs)
    opens_left, depth, out = n, 0, []
    while opens_left or depth:
        if opens_left and (depth == 0 or R(0, 1)):
            out.append("(")
            opens_left -= 1
            depth += 1
        else:
            out.append(")")
            depth -= 1
    return out


def _paren_letters():
    chars = _balanced(4)
    for _ in range(R(0, 5)):
        chars.insert(R(0, len(chars)), random.choice("abc"))
    return ("".join(chars),)


def _stars_args():
    out, kept = [], 0
    for _ in range(R(1, 10)):
        if kept and R(0, 2) == 0:
            out.append("*")
            kept -= 1
        else:
            out.append(random.choice("abc"))
            kept += 1
    return ("".join(out),)


def _exclusive_args():
    n, logs, stack, t, calls_left = R(1, 3), [], [], 0, R(1, 5)
    while calls_left or stack:
        if calls_left and (not stack or R(0, 1)):
            f = R(0, n - 1)
            logs.append(f"{f}:start:{t}")
            stack.append(f)
            calls_left -= 1
            t += R(0, 2)  # the next event may happen in the same unit
        else:
            logs.append(f"{stack.pop()}:end:{t}")
            t += R(1, 2)  # an end occupies unit t, so the next event is later
    return (n, logs)


def _competitive_args():
    nums = ints(8, 0, 9, 1)
    return (nums, R(1, len(nums)))


GX13 = {
    ("stack_monotonic", "Remove All Adjacent Duplicates in String II"): lambda: (st("ab", 1, 12), R(2, 4)),
    ("stack_monotonic", "Score of Parentheses"): lambda: ("".join(_balanced(5)),),
    ("stack_monotonic", "Reverse Substrings Between Each Pair of Parentheses"): _paren_letters,
    ("stack_monotonic", "Removing Stars From a String"): _stars_args,
    ("stack_monotonic", "Exclusive Time of Functions"): _exclusive_args,
    ("stack_monotonic", "Longest Well-Performing Interval"): lambda: (ints(10, 0, 12, 1),),
    ("stack_monotonic", "Maximum Width Ramp"): lambda: (ints(9, 0, 9, 2),),
    ("stack_monotonic", "Find the Most Competitive Subsequence"): _competitive_args,
    ("stack_monotonic", "Number of Visible People in a Queue"): lambda: (random.sample(range(1, 30), R(1, 8)),),
    ("stack_monotonic", "Final Prices With a Special Discount in a Shop"): lambda: (ints(8, 1, 10, 1),),
    ("stack_monotonic", "Minimum String Length After Removing Substrings"): lambda: (st("ABCD", 1, 10),),
}

GX.update(GX13)
