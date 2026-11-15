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


def _desc(n_max, lo, hi, k=1):
    return sorted(ints(n_max, lo, hi, k), reverse=True)


GX14 = {
    ("two_pointers", "Longest Word in Dictionary through Deleting"): lambda: (
        st("abc", 1, 8),
        [st("abc", 1, 5) for _ in range(R(1, 5))],
    ),
    ("two_pointers", "Sum of Square Numbers"): lambda: (R(0, 200),),
    ("two_pointers", "Valid Triangle Number"): lambda: (ints(8, 0, 9),),
    ("two_pointers", "Heaters"): lambda: (ints(7, 1, 20, 1), ints(4, 1, 20, 1)),
    ("two_pointers", "K-diff Pairs in an Array"): lambda: (ints(8, 0, 6, 1), R(0, 3)),
    ("two_pointers", "Longest Mountain in Array"): lambda: (ints(10, 0, 4),),
    ("two_pointers", "Bag of Tokens"): lambda: (ints(5, 0, 50), R(0, 60)),
    ("two_pointers", "Shortest Subarray to be Removed to Make Array Sorted"): lambda: (ints(8, 0, 5, 1),),
    ("two_pointers", "Minimum Length of String After Deleting Similar Ends"): lambda: (st("abc", 1, 10),),
    ("two_pointers", "Find First Palindromic String in the Array"): lambda: ([st("ab", 1, 4) for _ in range(R(1, 4))],),
    ("two_pointers", "Count Pairs Whose Sum is Less than Target"): lambda: (ints(8, -5, 5), R(-6, 8)),
    ("two_pointers", "Maximum Distance Between a Pair of Values"): lambda: (_desc(7, 1, 20), _desc(7, 1, 20)),
    ("two_pointers", "Number of Subsequences That Satisfy the Given Sum Condition"): lambda: (
        ints(8, 1, 9, 1),
        R(2, 18),
    ),
}

GX.update(GX14)


def _equal_sub():
    n = R(1, 8)
    return (st("abcd", n, n), st("abcd", n, n), R(0, 6))


def _k_of(lo, hi, extra):
    def gen():
        nums = ints(9, lo, hi, 1)
        return (nums, R(1, len(nums))) + extra()

    return gen


GX15 = {
    ("sliding_window", "Get Equal Substrings Within Budget"): _equal_sub,
    ("sliding_window", "Count Number of Nice Subarrays"): lambda: (ints(9, 1, 6, 1), R(1, 3)),
    ("sliding_window", "Number of Substrings Containing All Three Characters"): lambda: (st("abc", 1, 10),),
    ("sliding_window", "Maximum Points You Can Obtain from Cards"): _k_of(1, 9, lambda: ()),
    (
        "sliding_window",
        "Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit",
    ): lambda: (ints(9, 1, 9, 1), R(0, 5)),
    ("sliding_window", "Maximum Erasure Value"): lambda: (ints(9, 1, 6, 1),),
    ("sliding_window", "Minimum Operations to Reduce X to Zero"): lambda: (ints(8, 1, 6, 1), R(1, 15)),
    ("sliding_window", "Maximize the Confusion of an Exam"): lambda: (st("TF", 1, 10), R(0, 3)),
    ("sliding_window", "Minimum Recolors to Get K Consecutive Black Blocks"): lambda: _recolor(),
    (
        "sliding_window",
        "Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold",
    ): _k_of(1, 9, lambda: (R(1, 9),)),
    ("sliding_window", "Maximum Sum of Distinct Subarrays With Length K"): _k_of(1, 5, lambda: ()),
    ("sliding_window", "Length of Longest Subarray With at Most K Frequency"): lambda: (ints(9, 1, 4, 1), R(1, 3)),
    ("sliding_window", "Minimum Difference Between Highest and Lowest of K Scores"): _k_of(0, 20, lambda: ()),
}


def _recolor():
    blocks = st("WB", 1, 10)
    return (blocks, R(1, len(blocks)))


GX.update(GX15)


def _jobs():
    n = R(1, 5)
    return ([R(1, 9) for _ in range(n)], [R(1, 9) for _ in range(n)], ints(5, 1, 10, 1))


def _trains():
    return (ints(5, 1, 9, 1), R(1, 40) / 4)  # quarter hours are exact in binary floating point


def _spells():
    return (ints(5, 1, 6, 1), ints(5, 1, 6, 1), R(1, 30))


def _balls():
    pos = random.sample(range(1, 25), R(2, 7))
    return (pos, R(2, len(pos)))


def _pair_distance():
    nums = ints(7, 0, 15, 2)
    return (nums, R(1, len(nums) * (len(nums) - 1) // 2))


def _mult_table():
    m, n = R(1, 7), R(1, 7)
    return (m, n, R(1, m * n))


GX16 = {
    ("binary_search", "Arranging Coins"): lambda: (R(1, 200),),
    ("binary_search", "Most Profit Assigning Work"): _jobs,
    ("binary_search", "Find the Distance Value Between Two Arrays"): lambda: (
        ints(6, -10, 10, 1),
        ints(6, -10, 10, 1),
        R(0, 4),
    ),
    ("binary_search", "Minimum Limit of Balls in a Bag"): lambda: (ints(5, 1, 12, 1), R(0, 5)),
    ("binary_search", "Minimum Speed to Arrive on Time"): _trains,
    ("binary_search", "Minimum Time to Complete Trips"): lambda: (ints(4, 1, 8, 1), R(1, 15)),
    ("binary_search", "Maximum Candies Allocated to K Children"): lambda: (ints(5, 1, 12, 1), R(1, 10)),
    ("binary_search", "Successful Pairs of Spells and Potions"): _spells,
    ("binary_search", "Magnetic Force Between Two Balls"): _balls,
    ("binary_search", "Find K-th Smallest Pair Distance"): _pair_distance,
    ("binary_search", "Kth Smallest Number in Multiplication Table"): _mult_table,
    ("binary_search", "Minimum Time to Repair Cars"): lambda: (ints(4, 1, 6, 1), R(1, 12)),
}

GX.update(GX16)


def _unique_start_intervals():
    starts = random.sample(range(0, 15), R(1, 6))
    return ([[s, s + R(0, 4)] for s in starts],)


def _pairs_chain():
    return ([[a, a + R(1, 4)] for a in (R(-5, 10) for _ in range(R(1, 7)))],)


def _trips():
    trips = []
    for _ in range(R(1, 5)):
        a = R(0, 8)
        trips.append([R(1, 4), a, a + R(1, 5)])
    return (trips, R(1, 8))


def _bookings():
    n = R(1, 6)
    out = []
    for _ in range(R(1, 5)):
        first = R(1, n)
        out.append([first, R(first, n), R(1, 6)])
    return (out, n)


def _free_slots():
    cursor, slots = R(0, 5), []
    for _ in range(R(1, 4)):
        a = cursor + R(0, 3)
        b = a + R(1, 6)
        slots.append([a, b])
        cursor = b + R(1, 3)
    return slots


def _disjoint_intervals():
    cursor, out = R(-3, 3), []
    for _ in range(R(1, 5)):
        a = cursor + R(0, 3)
        b = a + R(1, 5)
        out.append([a, b])
        cursor = b + R(1, 3)  # a gap of at least 1 keeps them truly disjoint
    a = R(-2, 12)
    return (out, [a, a + R(1, 8)])


def _rooms_args():
    starts = random.sample(range(0, 12), R(1, 6))
    return (R(1, 4), [[s, s + R(1, 6)] for s in starts])


def _sorted_arrays():
    return ([sorted(R(-5, 9) for _ in range(R(1, 4))) for _ in range(R(2, 5))],)


GX17 = {
    ("intervals", "Find Right Interval"): _unique_start_intervals,
    ("intervals", "Maximum Length of Pair Chain"): _pairs_chain,
    ("intervals", "Car Pooling"): _trips,
    ("intervals", "Corporate Flight Bookings"): _bookings,
    ("intervals", "Meeting Scheduler"): lambda: (_free_slots(), _free_slots(), R(1, 5)),
    ("intervals", "Remove Interval"): _disjoint_intervals,
    ("intervals", "Meeting Rooms III"): _rooms_args,
    ("intervals", "Maximum Distance in Arrays"): _sorted_arrays,
}

GX.update(GX17)


def _two_blocks():
    nums = ints(9, 0, 9, 2)
    a = R(1, len(nums) - 1)
    return (nums, a, R(1, len(nums) - a))


def _pali_queries():
    s = st("abcd", 1, 10)
    queries = []
    for _ in range(R(1, 5)):
        left = R(0, len(s) - 1)
        queries.append([left, R(left, len(s) - 1), R(0, 3)])
    return (s, queries)


def _grid(lo, hi, size=5):
    return [[R(lo, hi) for _ in range(R(1, size))] for _ in range(1)]


def _block_args():
    rows, cols = R(1, 5), R(1, 5)
    return ([[R(0, 9) for _ in range(cols)] for _ in range(rows)], R(1, 3))


def _candle_args():
    s = st("*|", 1, 14)
    queries = []
    for _ in range(R(1, 5)):
        left = R(0, len(s) - 1)
        queries.append([left, R(left, len(s) - 1)])
    return (s, queries)


def _vowel_args():
    words = [st("abe", 1, 3) for _ in range(R(1, 6))]
    queries = []
    for _ in range(R(1, 5)):
        left = R(0, len(words) - 1)
        queries.append([left, R(left, len(words) - 1)])
    return (words, queries)


def _covered_args():
    ranges = []
    for _ in range(R(1, 4)):
        a = R(1, 10)
        ranges.append([a, R(a, 12)])
    left = R(1, 10)
    return (ranges, left, R(left, 12))


def _submatrix_args():
    rows, cols = R(1, 4), R(1, 4)
    return ([[R(-2, 3) for _ in range(cols)] for _ in range(rows)], R(-2, 4))


GX18 = {
    ("prefix_sums", "Maximum Sum of Two Non-Overlapping Subarrays"): _two_blocks,
    ("prefix_sums", "Can Make Palindrome from Substring"): _pali_queries,
    ("prefix_sums", "Matrix Block Sum"): _block_args,
    ("prefix_sums", "Find the Longest Substring Containing Vowels in Even Counts"): lambda: (st("aeioubcd", 1, 12),),
    (
        "prefix_sums",
        "Maximum Number of Non-Overlapping Subarrays With Sum Equals Target",
    ): lambda: (ints(8, -3, 4, 1), R(-3, 5)),
    ("prefix_sums", "Plates Between Candles"): _candle_args,
    ("prefix_sums", "Number of Ways to Split Array"): lambda: (ints(8, -5, 9, 2),),
    ("prefix_sums", "Longest Subsequence With Limited Sum"): lambda: (ints(7, 1, 9, 1), ints(5, 0, 30, 1)),
    ("prefix_sums", "Count Vowel Strings in Ranges"): _vowel_args,
    ("prefix_sums", "Find the Score of All Prefixes of an Array"): lambda: (ints(8, 1, 9, 1),),
    ("prefix_sums", "Check if All the Integers in a Range Are Covered"): _covered_args,
    ("prefix_sums", "Number of Submatrices That Sum to Target"): _submatrix_args,
}

GX.update(GX18)


def _n_repeated():
    n = R(2, 5)
    vals = random.sample(range(0, 20), n + 1)
    nums = [vals[0]] * n + vals[1:]
    random.shuffle(nums)
    return (nums,)


def _matches():
    out = []
    for _ in range(R(1, 8)):
        winner, loser = random.sample(range(1, 7), 2)
        out.append([winner, loser])
    return (out,)


def _square_grid():
    n = R(1, 4)
    return ([[R(1, 2) for _ in range(n)] for _ in range(n)],)


def _sentence():
    return " ".join(st("ab", 1, 2) for _ in range(R(1, 4)))


GX19 = {
    ("hashing", "X of a Kind in a Deck of Cards"): lambda: (ints(10, 0, 3, 1),),
    ("hashing", "N-Repeated Element in Size 2N Array"): _n_repeated,
    ("hashing", "Pairs of Songs With Total Durations Divisible by 60"): lambda: (ints(10, 1, 120, 1),),
    ("hashing", "Number of Equivalent Domino Pairs"): lambda: ([[R(1, 4), R(1, 4)] for _ in range(R(1, 8))],),
    ("hashing", "Maximum Number of Balloons"): lambda: (st("balonx", 1, 20),),
    ("hashing", "Check If N and Its Double Exist"): lambda: (ints(8, -6, 6, 2),),
    ("hashing", "Determine if Two Strings Are Close"): lambda: _close_args(),
    ("hashing", "Max Number of K-Sum Pairs"): lambda: (ints(9, 1, 6, 1), R(2, 12)),
    ("hashing", "Find Players With Zero or One Losses"): _matches,
    ("hashing", "Max Sum of a Pair With Equal Sum of Digits"): lambda: (ints(8, 1, 99, 1),),
    ("hashing", "Equal Row and Column Pairs"): _square_grid,
    ("hashing", "Uncommon Words from Two Sentences"): lambda: (_sentence(), _sentence()),
}


def _close_args():
    n = R(1, 5)
    return (st("abc", n, n), st("abc", n, n))


GX.update(GX19)


def _mat(lo, hi, size=5):
    rows, cols = R(1, size), R(1, size)
    return [[R(lo, hi) for _ in range(cols)] for _ in range(rows)]


def _sorted_desc_matrix():
    mat = _mat(-4, 4)
    mat = [sorted(row, reverse=True) for row in mat]
    cols = [sorted(col, reverse=True) for col in zip(*mat)]
    return ([list(row) for row in zip(*cols)],)


def _distinct_matrix():
    rows, cols = R(1, 4), R(1, 4)
    values = random.sample(range(1, 40), rows * cols)
    return ([values[r * cols : (r + 1) * cols] for r in range(rows)],)


def _binary_square():
    n = R(1, 5)
    return ([[R(0, 1) for _ in range(n)] for _ in range(n)],)


def _painted_args():
    m, n = R(1, 4), R(1, 4)
    values = list(range(1, m * n + 1))
    order = values[:]
    random.shuffle(order)
    random.shuffle(values)
    return (order, [values[r * n : (r + 1) * n] for r in range(m)])


GX20 = {
    ("matrix", "Diagonal Traverse"): lambda: (_mat(-9, 9),),
    ("matrix", "Score After Flipping Matrix"): lambda: (_mat(0, 1, 4),),
    ("matrix", "Shift 2D Grid"): lambda: (_mat(-9, 9, 4), R(0, 20)),
    ("matrix", "Count Square Submatrices with All Ones"): lambda: (_mat(0, 1),),
    ("matrix", "Count Negative Numbers in a Sorted Matrix"): _sorted_desc_matrix,
    ("matrix", "Lucky Numbers in a Matrix"): _distinct_matrix,
    ("matrix", "Count Submatrices With All Ones"): lambda: (_mat(0, 1),),
    ("matrix", "Largest 1-Bordered Square"): lambda: (_mat(0, 1),),
    ("matrix", "Minimum Swaps to Arrange a Binary Grid"): _binary_square,
    ("matrix", "First Completely Painted Row or Column"): _painted_args,
    ("matrix", "Difference Between Ones and Zeros in Row and Column"): lambda: (_mat(0, 1),),
}

GX.update(GX20)


def _perm():
    items = list(range(R(1, 8)))
    random.shuffle(items)
    return (items,)


def _rope():
    colors = st("abc", 1, 8)
    return (colors, [R(1, 9) for _ in colors])


def _piles():
    return ([R(1, 9) for _ in range(3 * R(1, 2))],)


def _matchsticks():
    if R(0, 1):
        side, sticks = R(1, 9), []
        for _ in range(4):
            if side >= 2 and R(0, 1):
                part = R(1, side - 1)
                sticks += [part, side - part]
            else:
                sticks.append(side)
        if R(0, 2) == 0:
            sticks[R(0, len(sticks) - 1)] += 1
        random.shuffle(sticks)
        return (sticks,)
    return (ints(7, 1, 6, 1),)


def _word_break():
    words = sorted({st("ab", 1, 3) for _ in range(R(1, 4))})
    return (st("ab", 1, 8), words)


def _unique_paths_iii():
    rows, cols = R(1, 3), R(2, 4)
    grid = [[-1 if R(0, 3) == 0 else 0 for _ in range(cols)] for _ in range(rows)]
    first, second = random.sample(range(rows * cols), 2)
    grid[first // cols][first % cols] = 1
    grid[second // cols][second % cols] = 2
    return (grid,)


GX21 = {
    ("greedy", "Monotone Increasing Digits"): lambda: (R(0, 3000),),
    ("greedy", "Max Chunks To Make Sorted"): _perm,
    ("greedy", "Minimum Deletions to Make Character Frequencies Unique"): lambda: (st("abcde", 1, 12),),
    ("greedy", "Maximum Units on a Truck"): lambda: ([[R(1, 4), R(1, 9)] for _ in range(R(1, 4))], R(0, 12)),
    ("greedy", "Minimum Operations to Make the Array Increasing"): lambda: (ints(5, 1, 6, 1),),
    ("greedy", "Minimum Time to Make Rope Colorful"): _rope,
    ("greedy", "Broken Calculator"): lambda: (R(1, 20), R(1, 40)),
    ("greedy", "Maximum Number of Coins You Can Get"): _piles,
    ("greedy", "Minimum Subsequence in Non-Increasing Order"): lambda: (ints(7, 1, 9, 1),),
    ("greedy", "Minimum Cost of Buying Candies With Discount"): lambda: (ints(6, 1, 9, 1),),
    ("greedy", "Minimum Sum of Four Digit Number After Splitting Digits"): lambda: (R(1000, 9999),),
    ("backtracking", "Word Break II"): _word_break,
    ("backtracking", "Expression Add Operators"): lambda: (st("0123", 1, 5), R(-20, 60)),
    ("backtracking", "Remove Invalid Parentheses"): lambda: (st("()a", 0, 9),),
    ("backtracking", "Matchsticks to Square"): _matchsticks,
    ("backtracking", "Numbers With Same Consecutive Differences"): lambda: (R(2, 4), R(0, 9)),
    ("backtracking", "Path with Maximum Gold"): lambda: (_mat(0, 9, 4),),
    ("backtracking", "The k-th Lexicographical String of All Happy Strings of Length n"): lambda: (R(1, 6), R(1, 100)),
    ("backtracking", "Maximum Length of a Concatenated String with Unique Characters"): lambda: (
        [st("abcde", 1, 3) for _ in range(R(1, 7))],
    ),
    ("backtracking", "Unique Paths III"): _unique_paths_iii,
    ("backtracking", "Split a String Into the Max Number of Unique Substrings"): lambda: (st("abc", 1, 10),),
}

GX.update(GX21)


def _expression():
    parts = [str(R(1, 9))]
    for _ in range(R(0, 3)):
        parts += [random.choice("+-*"), str(R(1, 9))]
    return ("".join(parts),)


def _range_sum():
    lower = R(-6, 3)
    return (ints(7, -5, 5, 1), lower, lower + R(0, 6))


def _beautiful_norm(args, got):
    n = args[0]
    return sorted(got) == list(range(1, n + 1)) and all(
        2 * got[k] != got[i] + got[j] for i in range(n) for j in range(i + 2, n) for k in range(i + 1, j)
    )


def _grammar():
    n = R(1, 10)
    return (n, R(1, 2 ** (n - 1)))


def _skyline():
    out = []
    for _ in range(R(1, 6)):
        left = R(0, 8)
        out.append([left, left + R(1, 6), R(1, 6)])
    return (out,)


def _distinct(n_max, lo, hi):
    return random.sample(range(lo, hi + 1), R(1, n_max))


def _super_pow():
    digits = [R(1, 9)] + [R(0, 9) for _ in range(R(0, 2))]
    return (R(1, 60), digits)


def _pairs():
    n = R(2, 8)
    return ([R(-5, 5) for _ in range(n)], [R(-5, 5) for _ in range(n)], R(-4, 4))


GX22 = {
    ("divide_conquer", "Different Ways to Add Parentheses"): _expression,
    ("divide_conquer", "Count of Range Sum"): _range_sum,
    ("divide_conquer", "Beautiful Array"): (lambda: (R(1, 8),), _beautiful_norm),
    ("divide_conquer", "K-th Symbol in Grammar"): _grammar,
    ("divide_conquer", "Longest Substring with At Least K Repeating Characters"): lambda: (st("abc", 1, 12), R(1, 4)),
    ("divide_conquer", "The Skyline Problem"): _skyline,
    ("divide_conquer", "Maximum Binary Tree"): lambda: (_distinct(8, 0, 20),),
    ("divide_conquer", "Super Pow"): _super_pow,
    ("divide_conquer", "Number of Pairs Satisfying Inequality"): _pairs,
    ("divide_conquer", "Create Sorted Array through Instructions"): lambda: (ints(10, 1, 6, 1),),
    ("divide_conquer", "Number of Ways to Reorder Array to Get Same BST"): lambda: (_distinct(7, 1, 9),),
    ("divide_conquer", "Count Good Numbers"): lambda: (R(1, 200),),
}

GX.update(GX22)


def _disjoint():
    left = [R(0, 5) for _ in range(R(1, 4))]
    right = [R(5, 10) for _ in range(R(1, 4))]
    random.shuffle(left)
    random.shuffle(right)
    return (left + right,)


GX23 = {
    ("array_tricks", "Shortest Unsorted Continuous Subarray"): lambda: (ints(8, -5, 5, 1),),
    ("array_tricks", "Longest Continuous Increasing Subsequence"): lambda: (ints(10, 0, 5, 1),),
    ("array_tricks", "Valid Mountain Array"): lambda: (ints(8, 0, 4, 1),),
    ("array_tricks", "Rotate Function"): lambda: (ints(8, -5, 5, 1),),
    ("array_tricks", "Minimum Moves to Equal Array Elements"): lambda: (ints(5, 1, 6, 1),),
    ("array_tricks", "Minimum Moves to Equal Array Elements II"): lambda: (ints(8, -10, 10, 1),),
    ("array_tricks", "Array Nesting"): lambda: (random.sample(range(n := R(1, 9)), n),),
    ("array_tricks", "Max Chunks To Make Sorted II"): lambda: (ints(7, 0, 5, 1),),
    ("array_tricks", "Partition Array into Disjoint Intervals"): _disjoint,
    ("array_tricks", "Degree of an Array"): lambda: (ints(8, 1, 4, 1),),
    ("array_tricks", "1-bit and 2-bit Characters"): lambda: ([R(0, 1) for _ in range(R(0, 8))] + [0],),
    ("array_tricks", "Positions of Large Groups"): lambda: (st("abc", 1, 14),),
}

GX.update(GX23)
