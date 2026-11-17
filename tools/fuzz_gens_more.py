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


def _iv(lo, hi, span, k=1, n_max=5, min_len=0):
    out = []
    for _ in range(R(k, n_max)):
        left = R(lo, hi)
        out.append([left, left + R(min_len, span)])
    return out


def _rects():
    out = []
    for _ in range(R(1, 4)):
        x, y = R(0, 6), R(0, 6)
        out.append([x, y, x + R(1, 4), y + R(1, 4)])
    return (out,)


def _jobs():
    n = R(1, 7)
    start = [R(1, 8) for _ in range(n)]
    return (start, [s + R(1, 5) for s in start], [R(1, 9) for _ in range(n)])


def _taps():
    n = R(1, 6)
    return (n, [R(0, 3) for _ in range(n + 1)])


def _events():
    out = []
    for _ in range(R(1, 6)):
        s = R(1, 8)
        out.append([s, s + R(0, 4), R(1, 9)])
    return (out,)


def _shifts():
    s = st("abcxyz", 1, 8)
    out = []
    for _ in range(R(0, 5)):
        a = R(0, len(s) - 1)
        out.append([a, R(a, len(s) - 1), R(0, 1)])
    return (s, out)


GX24 = {
    ("intervals", "Set Intersection Size At Least Two"): lambda: (
        [[a, a + R(1, 4)] for a in [R(1, 5) for _ in range(R(1, 4))]],
    ),
    ("intervals", "Rectangle Area II"): _rects,
    ("intervals", "Minimum Interval to Include Each Query"): lambda: (_iv(1, 8, 4), ints(6, 1, 12, 1)),
    ("intervals", "Count Ways to Group Overlapping Ranges"): lambda: (_iv(1, 10, 4, 1, 7),),
    ("intervals", "Points That Intersect With Cars"): lambda: (_iv(1, 15, 6),),
    ("intervals", "Number of Flowers in Full Bloom"): lambda: (_iv(1, 10, 5), [R(1, 14) for _ in range(R(1, 6))]),
    ("intervals", "Maximum Profit in Job Scheduling"): _jobs,
    ("intervals", "Video Stitching"): lambda: (_iv(0, 8, 4, 1, 6), R(1, 10)),
    ("intervals", "Minimum Number of Taps to Open to Water a Garden"): _taps,
    ("intervals", "Two Best Non-Overlapping Events"): _events,
    ("intervals", "Shifting Letters II"): _shifts,
}

GX.update(GX24)


def _interesting():
    modulo = R(1, 5)
    return (ints(8, 0, 9, 1), modulo, R(0, modulo - 1))


def _queries(n):
    out = []
    for _ in range(R(1, 5)):
        left = R(0, n - 1)
        out.append([left, R(left, n - 1)])
    return out


def _xor_queries():
    arr = ints(8, 0, 15, 1)
    return (arr, _queries(len(arr)))


def _sorted_ints():
    return (sorted(ints(8, 0, 12, 1)),)


def _k_radius():
    return (ints(9, 0, 20, 1), R(0, 3))


GX25 = {
    ("prefix_sums", "Continuous Subarray Sum"): lambda: (ints(8, 0, 9, 2), R(1, 7)),
    ("prefix_sums", "Make Sum Divisible by P"): lambda: (ints(8, 1, 9, 1), R(1, 9)),
    ("prefix_sums", "Count Triplets That Can Form Two Arrays of Equal XOR"): lambda: (ints(7, 0, 7, 1),),
    ("prefix_sums", "XOR Queries of a Subarray"): _xor_queries,
    ("prefix_sums", "Find Two Non-overlapping Sub-arrays Each With Target Sum"): lambda: (ints(9, 1, 5, 1), R(1, 8)),
    ("prefix_sums", "Number of Sub-arrays With Odd Sum"): lambda: (ints(9, 1, 9, 1),),
    ("prefix_sums", "Find the Highest Altitude"): lambda: (ints(8, -6, 6),),
    ("prefix_sums", "Range Product Queries of Powers"): lambda: _power_queries(),
    ("prefix_sums", "Find the Middle Index in Array"): lambda: (ints(7, -3, 3, 1),),
    ("prefix_sums", "Left and Right Sum Differences"): lambda: (ints(8, 0, 9, 1),),
    ("prefix_sums", "Maximum Absolute Sum of Any Subarray"): lambda: (ints(8, -6, 6, 1),),
    ("prefix_sums", "Unique Length-3 Palindromic Subsequences"): lambda: (st("abc", 1, 12),),
    ("prefix_sums", "K Radius Subarray Averages"): _k_radius,
    ("prefix_sums", "Sum of Absolute Differences in a Sorted Array"): _sorted_ints,
    ("prefix_sums", "Count of Interesting Subarrays"): _interesting,
    ("prefix_sums", "Count the Number of Beautiful Subarrays"): lambda: (ints(8, 0, 7, 1),),
    ("prefix_sums", "Sum of Floored Pairs"): lambda: (ints(8, 1, 20, 1),),
}


def _power_queries():
    n = R(1, 200)
    bits = bin(n).count("1")
    return (n, _queries(bits))


GX.update(GX25)


def _happy_norm(args, got):
    ok = not any(ch * 3 in got for ch in "abc") and all(got.count(ch) <= n for ch, n in zip("abc", args))
    return (ok, len(got))


def _topk_norm(args, got):
    nums, k = args
    rest = iter(nums)
    return (len(got), sum(got), all(x in rest for x in got))


def _barcodes():
    while True:
        a = ints(7, 1, 3, 1)
        if max(a.count(v) for v in a) <= (len(a) + 1) // 2:
            return (a,)


def _barcodes_norm(args, got):
    return (sorted(got) == sorted(args[0]), all(got[i] != got[i + 1] for i in range(len(got) - 1)))


def _pass_ratio():
    classes = []
    for _ in range(R(1, 3)):
        total = R(1, 6)
        classes.append([R(0, total), total])
    return (classes, R(0, 4))


def _hire_costs():
    n = R(1, 8)
    return (ints(n, 1, 20, n), R(1, n), R(1, 4))


def _two_arrays():
    n = R(1, 6)
    return ([R(1, 9) for _ in range(n)], [R(1, 9) for _ in range(n)], R(1, n))


def _performance():
    n = R(1, 6)
    return (n, [R(1, 9) for _ in range(n)], [R(1, 9) for _ in range(n)], R(1, n))


def _hire_workers():
    n = R(1, 6)
    return ([R(1, 9) for _ in range(n)], [R(1, 20) for _ in range(n)], R(1, n))


def _sorted_subsums():
    nums = ints(6, 1, 9, 1)
    total = len(nums) * (len(nums) + 1) // 2
    left = R(1, total)
    return (nums, len(nums), left, R(left, total))


def _orders():
    return ([[R(1, 6), R(1, 5), R(0, 1)] for _ in range(R(1, 7))],)


def _height_map():
    rows, cols = R(1, 4), R(1, 4)
    return ([[R(0, 5) for _ in range(cols)] for _ in range(rows)],)


GX26 = {
    ("heap", "Longest Happy String"): (lambda: (R(0, 5), R(0, 5), R(0, 5)), _happy_norm),
    ("heap", "Jump Game VI"): lambda: (ints(8, -6, 6, 1), R(1, 4)),
    ("heap", "Maximum Average Pass Ratio"): _pass_ratio,
    ("heap", "Maximum Product After K Increments"): lambda: (ints(4, 0, 5, 1), R(0, 4)),
    ("heap", "Total Cost to Hire K Workers"): _hire_costs,
    ("heap", "Maximum Subsequence Score"): _two_arrays,
    ("heap", "Maximum Performance of a Team"): _performance,
    ("heap", "Find Subsequence of Length K With the Largest Sum"): (
        lambda: (lambda a: (a, R(1, len(a))))(ints(8, -5, 5, 1)),
        _topk_norm,
    ),
    ("heap", "Super Ugly Number"): lambda: (R(1, 14), [2, *random.sample([3, 5, 7, 11, 13], R(0, 2))]),
    ("heap", "Range Sum of Sorted Subarray Sums"): _sorted_subsums,
    ("heap", "Number of Orders in the Backlog"): _orders,
    ("heap", "Distant Barcodes"): (_barcodes, _barcodes_norm),
    ("heap", "Minimum Cost to Hire K Workers"): _hire_workers,
    ("heap", "Minimize Deviation in Array"): lambda: (ints(4, 1, 12, 1),),
    ("heap", "Split Array into Consecutive Subsequences"): lambda: (sorted(ints(8, 1, 5, 1)),),
    ("heap", "Trapping Rain Water II"): _height_map,
}

GX.update(GX26)


def _bin_square(n):
    return [[R(0, 1) for _ in range(n)] for _ in range(n)]


def _overlap():
    n = R(1, 4)
    return (_bin_square(n), _bin_square(n))


def _ttt_moves():
    cells = [[i, j] for i in range(3) for j in range(3)]
    random.shuffle(cells)
    moves = []
    for cell in cells:
        moves.append(cell)
        mine = {tuple(c) for c in moves[len(moves) - 1 :: -2]}
        lines = [[(i, j) for j in range(3)] for i in range(3)] + [[(i, j) for i in range(3)] for j in range(3)]
        lines += [[(0, 0), (1, 1), (2, 2)], [(0, 2), (1, 1), (2, 0)]]
        if any(all(p in mine for p in line) for line in lines) or R(0, 5) == 0:
            break
    return (moves,)


def _farmland():
    m, n = R(1, 6), R(1, 6)
    grid = [[0] * n for _ in range(m)]
    for _ in range(R(0, 3)):
        r1, c1 = R(0, m - 1), R(0, n - 1)
        r2, c2 = R(r1, min(m - 1, r1 + 2)), R(c1, min(n - 1, c1 + 2))
        near = [(r, c) for r in range(max(0, r1 - 1), min(m, r2 + 2)) for c in range(max(0, c1 - 1), min(n, c2 + 2))]
        if all(grid[r][c] == 0 for r, c in near):
            for r in range(r1, r2 + 1):
                for c in range(c1, c2 + 1):
                    grid[r][c] = 1
    return (grid,)


def _valid_matrix():
    n = R(1, 4)
    grid = [[(i + j) % n + 1 for j in range(n)] for i in range(n)]
    if R(0, 1):
        grid[R(0, n - 1)][R(0, n - 1)] = R(1, n)
    return (grid,)


def _unguarded():
    m, n = R(1, 5), R(1, 5)
    cells = [[r, c] for r in range(m) for c in range(n)]
    random.shuffle(cells)
    g, w = R(1, max(1, len(cells) // 2)), R(0, len(cells) // 3)
    guards = cells[:g]
    return (m, n, guards, cells[g : g + w])


def _local_grid():
    n = R(3, 6)
    return ([[R(0, 9) for _ in range(n)] for _ in range(n)],)


def _similar():
    n = R(1, 4)
    return ([[R(1, 2) for _ in range(n)] for _ in range(R(1, 3))], R(1, 6))


def _missing_repeated():
    n = R(2, 4)
    vals = list(range(1, n * n + 1))
    random.shuffle(vals)
    p, q = random.sample(range(len(vals)), 2)
    vals[q] = vals[p]
    return ([vals[i * n : (i + 1) * n] for i in range(n)],)


def _sum_queries():
    n = R(1, 4)
    return (n, [[R(0, 1), R(0, n - 1), R(0, 5)] for _ in range(R(1, 6))])


def _box():
    m, n = R(1, 4), R(1, 5)
    return ([[random.choice("#.*") for _ in range(n)] for _ in range(m)],)


def _ball_grid():
    m, n = R(1, 4), R(1, 5)
    return ([[random.choice([1, -1]) for _ in range(n)] for _ in range(m)],)


def _same_pair():
    a = _bin_square(R(1, 3))
    target = [row[:] for row in a]
    for _ in range(R(0, 3)):
        target = [list(row) for row in zip(*target[::-1])]
    if R(0, 2) == 0:
        i, j = R(0, len(a) - 1), R(0, len(a) - 1)
        target[i][j] ^= 1
    return (a, target)


GX27 = {
    ("matrix", "Reshape the Matrix"): lambda: ([[R(0, 9) for _ in range(R(1, 3))]] * R(1, 3), R(1, 4), R(1, 4)),
    ("matrix", "Image Overlap"): _overlap,
    ("matrix", "Projection Area of 3D Shapes"): lambda: ([[R(0, 4) for _ in range(3)] for _ in range(3)],),
    ("matrix", "Surface Area of 3D Shapes"): lambda: ([[R(0, 4) for _ in range(3)] for _ in range(3)],),
    ("matrix", "As Far from Land as Possible"): lambda: (_bin_square(R(1, 5)),),
    ("matrix", "Find Winner on a Tic Tac Toe Game"): _ttt_moves,
    ("matrix", "Sort the Matrix Diagonally"): lambda: ([[R(1, 9) for _ in range(R(1, 5))]] * R(1, 4),),
    ("matrix", "Where Will the Ball Fall"): _ball_grid,
    ("matrix", "Rotating the Box"): _box,
    ("matrix", "Determine Whether Matrix Can Be Obtained By Rotation"): lambda: (lambda a: (a, a))(
        _bin_square(R(1, 3))
    ),
    ("matrix", "Find All Groups of Farmland"): _farmland,
    ("matrix", "Check if Every Row and Column Contains All Numbers"): _valid_matrix,
    ("matrix", "Count Unguarded Cells in the Grid"): _unguarded,
    ("matrix", "Largest Local Values in a Matrix"): _local_grid,
    ("matrix", "Matrix Similarity After Cyclic Shifts"): _similar,
    ("matrix", "Find Missing and Repeated Values"): _missing_repeated,
    ("matrix", "Sum of Matrix After Queries"): _sum_queries,
}

GX.update(GX27)


def _fs():
    lines, depth, last_dir = [], 0, True
    for t in range(R(1, 7)):
        if t:
            depth = R(0, depth + 1 if last_dir else depth)
        is_file = R(0, 2) == 0
        name = "f" * R(1, 3) + ".x" if is_file else "d" * R(1, 3)
        lines.append("\t" * depth + name)
        last_dir = not is_file
    return ("\n".join(lines),)


def _set_mismatch():
    n = R(2, 6)
    nums = list(range(1, n + 1))
    i, j = random.sample(range(n), 2)
    nums[i] = nums[j]
    random.shuffle(nums)
    return (nums,)


def _orders():
    return ([[random.choice("XYZ"), str(R(1, 12)), random.choice(["Tea", "Cake", "Soup"])] for _ in range(R(1, 7))],)


def _path_pairs():
    values = random.sample(range(-5, 10), R(2, 6))
    pairs = [[values[i], values[i + 1]] if R(0, 1) else [values[i + 1], values[i]] for i in range(len(values) - 1)]
    random.shuffle(pairs)
    return (pairs,)


def _restore_norm(args, got):
    pairs = args[0]
    wanted = sorted(sorted(p) for p in pairs)
    return len(got) == len(pairs) + 1 and sorted(sorted(got[i : i + 2]) for i in range(len(got) - 1)) == wanted


def _brackets():
    s = "".join(random.choice(["x", "y", "(a)", "(b)", "(c)"]) for _ in range(R(1, 6)))
    return (s, [[k, "v" + k] for k in random.sample("abc", R(0, 3))])


def _edges():
    n = R(2, 6)
    return ([random.choice([j for j in range(n) if j != i]) for i in range(n)],)


def _creators():
    n = R(1, 6)
    return (
        [random.choice("abc") for _ in range(n)],
        random.sample(["p", "q", "r", "s", "t", "u"], n),
        [R(0, 5) for _ in range(n)],
    )


def _cpdomains():
    pool = ["a.b.com", "b.com", "c.org", "x.a.b.com", "org"]
    return ([f"{R(1, 9)} {random.choice(pool)}" for _ in range(R(1, 5))],)


GX28 = {
    ("hashing", "Longest Absolute File Path"): _fs,
    ("hashing", "Set Mismatch"): _set_mismatch,
    ("hashing", "Find and Replace Pattern"): lambda: ([st("abc", 3, 3) for _ in range(R(0, 5))], st("abc", 3, 3)),
    ("hashing", "Array of Doubled Pairs"): lambda: ([R(-4, 4) for _ in range(2 * R(1, 4))],),
    ("hashing", "Divide Array in Sets of K Consecutive Numbers"): lambda: (ints(8, 1, 5, 1), R(1, 3)),
    ("hashing", "Display Table of Food Orders in a Restaurant"): _orders,
    ("hashing", "Making File Names Unique"): lambda: (
        [random.choice(["a", "a(1)", "a(2)", "b", "a(1)(1)"]) for _ in range(R(1, 7))],
    ),
    ("hashing", "Restore the Array From Adjacent Pairs"): (_path_pairs, _restore_norm),
    ("hashing", "Evaluate the Bracket Pairs of a String"): _brackets,
    ("hashing", "Count Nice Pairs in an Array"): lambda: (ints(7, 0, 200, 1),),
    ("hashing", "Number of Pairs of Interchangeable Rectangles"): lambda: (
        [[R(1, 6), R(1, 6)] for _ in range(R(1, 7))],
    ),
    ("hashing", "Longest Palindrome by Concatenating Two Letter Words"): lambda: (
        [random.choice(["ab", "ba", "aa", "bb"]) for _ in range(R(1, 5))],
    ),
    ("hashing", "Find All Lonely Numbers in the Array"): lambda: (ints(8, 0, 6, 1),),
    ("hashing", "Minimum Consecutive Cards to Pick Up"): lambda: (ints(8, 0, 5, 1),),
    ("hashing", "Node With Highest Edge Score"): _edges,
    ("hashing", "Most Popular Video Creator"): _creators,
    ("hashing", "Subdomain Visit Count"): _cpdomains,
}

GX.update(GX28)


def _blank_pair(blank):
    start = st("LR" + blank, 1, 6)
    if R(0, 2) == 0:
        return (start, "".join(random.sample(start, len(start))))
    end = start
    for _ in range(R(0, 5)):
        i = R(0, len(end) - 1) if len(end) > 1 else 0
        pair = end[i : i + 2]
        if pair == blank + "L":
            end = end[:i] + "L" + blank + end[i + 2 :]
        elif pair == "R" + blank:
            end = end[:i] + blank + "R" + end[i + 2 :]
    return (start, end)


def _plants():
    return (ints(7, 1, 5, 1), R(5, 8), R(5, 8))


def _fair_pairs():
    low = R(-4, 4)
    return (ints(8, -5, 5, 2), low, low + R(0, 6))


def _strongest():
    arr = ints(8, -5, 9, 1)
    return (arr, R(1, len(arr)))


def _sorted_distinct():
    return sorted(random.sample(range(1, 12), R(1, 6)))


def _good_subarray():
    nums = ints(8, 1, 6, 1)
    return (nums, R(0, len(nums) - 1))


def _signs():
    m = R(1, 4)
    nums = [R(1, 5) for _ in range(m)] + [-R(1, 5) for _ in range(m)]
    random.shuffle(nums)
    return (nums,)


GX29 = {
    ("two_pointers", "Swap Adjacent in LR String"): lambda: _blank_pair("X"),
    ("two_pointers", "Friends Of Appropriate Ages"): lambda: (ints(8, 1, 120, 1),),
    ("two_pointers", "3Sum With Multiplicity"): lambda: (ints(9, 0, 6, 3), R(0, 15)),
    ("two_pointers", "Reverse Prefix of Word"): lambda: (st("abc", 1, 7), random.choice("abcd")),
    ("two_pointers", "Watering Plants II"): _plants,
    ("two_pointers", "Find All K-Distant Indices in an Array"): lambda: (ints(9, 0, 3, 1), R(0, 3), R(0, 4)),
    ("two_pointers", "Move Pieces to Obtain a String"): lambda: _blank_pair("_"),
    ("two_pointers", "Maximum Matching of Players With Trainers"): lambda: (ints(5, 1, 6, 1), ints(5, 1, 6, 1)),
    ("two_pointers", "Count the Number of Fair Pairs"): _fair_pairs,
    ("two_pointers", "Make String a Subsequence Using Cyclic Increments"): lambda: (st("abz", 1, 6), st("abcz", 1, 3)),
    ("two_pointers", "Append Characters to String to Make Subsequence"): lambda: (st("abc", 1, 6), st("abc", 1, 5)),
    ("two_pointers", "The k Strongest Values in an Array"): _strongest,
    ("two_pointers", "Get the Maximum Score"): lambda: (_sorted_distinct(), _sorted_distinct()),
    ("two_pointers", "Maximum Score of a Good Subarray"): _good_subarray,
    ("two_pointers", "Partition Array According to Given Pivot"): lambda: (ints(8, -3, 3, 1), R(-3, 3)),
    ("two_pointers", "Rearrange Array Elements by Sign"): _signs,
    ("two_pointers", "Remove Palindromic Subsequences"): lambda: (st("ab", 0, 6),),
}

GX.update(GX29)


def _max_freq():
    low = R(1, 4)
    return (st("abc", 1, 9), R(1, 3), low, low + R(0, 2))


def _beautiful():
    return ("".join("".join(sorted(st("aeiou", 1, 6))) for _ in range(R(1, 3))),)


def _semi_win():
    nums = ints(9, 1, 5, 1)
    k = R(1, len(nums))
    return (nums, R(1, k), k)


def _power_array():
    nums = [R(1, 4)]
    for _ in range(R(1, 8)):
        nums.append(nums[-1] + random.choice([1, 1, 1, -1, 0, 2]))
    return (nums, R(1, len(nums)))


GX30 = {
    ("sliding_window", "Longest Turbulent Subarray"): lambda: (ints(9, 0, 5, 1),),
    ("sliding_window", "Swap For Longest Repeated Character Substring"): lambda: (st("abc", 1, 8),),
    ("sliding_window", "Replace the Substring for Balanced String"): lambda: (
        st("QWER", *(2 * [random.choice([4, 8])])),
    ),
    ("sliding_window", "Maximum Number of Occurrences of a Substring"): _max_freq,
    ("sliding_window", "Frequency of the Most Frequent Element"): lambda: (ints(7, 1, 8, 1), R(0, 8)),
    ("sliding_window", "Longest Substring Of All Vowels in Order"): _beautiful,
    ("sliding_window", "Substrings of Size Three with Distinct Characters"): lambda: (st("abc", 1, 9),),
    ("sliding_window", "Minimum Swaps to Group All 1's Together II"): lambda: (ints(10, 0, 1, 1),),
    ("sliding_window", "Longest Nice Subarray"): lambda: (ints(7, 1, 15, 1),),
    ("sliding_window", "Take K of Each Character From Left and Right"): lambda: (st("abc", 1, 9), R(0, 3)),
    ("sliding_window", "Find the Longest Semi-Repetitive Substring"): lambda: (st("123", 1, 9),),
    ("sliding_window", "Continuous Subarrays"): lambda: (ints(8, 1, 6, 1),),
    ("sliding_window", "Count Complete Subarrays in an Array"): lambda: (ints(8, 1, 4, 1),),
    ("sliding_window", "Maximum Sum of Almost Unique Subarray"): _semi_win,
    ("sliding_window", "Count Subarrays Where Max Element Appears at Least K Times"): lambda: (
        ints(8, 1, 4, 1),
        R(1, 4),
    ),
    ("sliding_window", "Maximum Length Substring With Two Occurrences"): lambda: (st("abc", 1, 9),),
    ("sliding_window", "Find the Power of K-Size Subarrays I"): _power_array,
}

GX.update(GX30)


def _bt_gray_norm(args, res):
    size = 1 << args[0]
    ok = isinstance(res, list) and len(res) == size and len(set(res)) == size and res[0] == 0
    ok = ok and all(0 <= x < size for x in res)
    return ok and all(bin(res[i] ^ res[(i + 1) % size]).count("1") == 1 for i in range(size))


def _bt_itinerary():
    cities = ["JFK", "A", "B", "C"]
    current, tickets = "JFK", []
    for _ in range(R(1, 6)):
        nxt = random.choice(cities)
        tickets.append([current, nxt])
        current = nxt
    random.shuffle(tickets)
    return (tickets,)


def _bt_pyramid():
    return (st("ABC", 2, 4), ["".join(random.choices("ABC", k=3)) for _ in range(R(0, 8))])


def _bt_fib_gen():
    if R(0, 1):
        parts = [R(0, 9), R(0, 9)]
        for _ in range(R(1, 3)):
            parts.append(parts[-1] + parts[-2])
        return ("".join(map(str, parts)),)
    return (st("0123", 3, 8),)


def _bt_fib_norm(args, res):
    if not res:
        return "none"
    num = args[0]
    valid = len(res) >= 3 and "".join(map(str, res)) == num and all(p <= 2**31 - 1 for p in res)
    valid = valid and all(res[i] + res[i + 1] == res[i + 2] for i in range(len(res) - 2))
    return "ok" if valid else "bad"


def _bt_words():
    words = [st("abc", 1, 3) for _ in range(R(1, 5))]
    return (words, list(st("abc", 0, 8)), [R(0, 5) for _ in range(3)] + [0] * 23)


def _bt_descending():
    if R(0, 1):
        top = R(1, 12)
        parts = ["0" * R(0, 1) + str(v) for v in range(top, max(top - R(1, 3), -1), -1)]
        return ("".join(parts),)
    return (st("0123", 2, 8),)


def _bt_unique_gen():
    n = R(1, 5)
    return (random.sample([format(i, f"0{n}b") for i in range(2**n)], n),)


def _bt_unique_norm(args, res):
    nums = args[0]
    return isinstance(res, str) and len(res) == len(nums) and set(res) <= {"0", "1"} and res not in nums


def _bt_statements():
    n = R(1, 4)
    return ([[2 if i == j else R(0, 2) for j in range(n)] for i in range(n)],)


def _bt_columns():
    m, n = R(1, 5), R(1, 5)
    return ([[R(0, 1) for _ in range(n)] for _ in range(m)], R(1, n))


GX31 = {
    ("backtracking", "Gray Code"): (lambda: (R(1, 3),), _bt_gray_norm),
    ("backtracking", "Additive Number"): lambda: (st("0123", 3, 8),),
    ("backtracking", "Reconstruct Itinerary"): _bt_itinerary,
    ("backtracking", "Binary Watch"): lambda: (R(0, 10),),
    ("backtracking", "24 Game"): lambda: ([R(1, 9) for _ in range(4)],),
    ("backtracking", "Pyramid Transition Matrix"): _bt_pyramid,
    ("backtracking", "Split Array into Fibonacci Sequence"): (_bt_fib_gen, _bt_fib_norm),
    ("backtracking", "Number of Squareful Arrays"): lambda: (ints(6, 1, 20, 1),),
    ("backtracking", "Maximum Score Words Formed by Letters"): _bt_words,
    ("backtracking", "Splitting a String Into Descending Consecutive Values"): _bt_descending,
    ("backtracking", "Find Unique Binary String"): (_bt_unique_gen, _bt_unique_norm),
    ("backtracking", "Count Number of Maximum Bitwise-OR Subsets"): lambda: (ints(8, 1, 8, 1),),
    ("backtracking", "Next Greater Numerically Balanced Number"): lambda: (R(0, 10000),),
    ("backtracking", "Maximum Good People Based on Statements"): _bt_statements,
    ("backtracking", "Fair Distribution of Cookies"): lambda: (ints(7, 1, 9, 1), R(1, 3)),
    ("backtracking", "Maximum Rows Covered by Columns"): _bt_columns,
    ("backtracking", "Generate Binary Strings Without Adjacent Zeros"): lambda: (R(1, 8),),
}

GX.update(GX31)


def _s_justify():
    words = [st("ab", 1, 4) for _ in range(R(1, 7))]
    return (words, R(max(map(len, words)), 10))


def _s_digits_words():
    names = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
    letters = list("".join(random.choice(names) for _ in range(R(1, 5))))
    random.shuffle(letters)
    return ("".join(letters),)


def _s_fraction_sum():
    out = ""
    for k in range(R(1, 4)):
        sign = random.choice(["-", ""]) if k == 0 else random.choice(["+", "-"])
        out += f"{sign}{R(1, 9)}/{R(1, 9)}"
    return (out,)


def _s_comments():
    pieces = ["a", "b", "//", "/*", "*/", " ", "x"]
    lines = ["".join(random.choice(pieces) for _ in range(R(0, 5))) for _ in range(R(1, 5))]
    text, i, in_block = "\n".join(lines), 0, False
    while i < len(text):
        if in_block:
            in_block = text[i : i + 2] != "*/"
            i += 1 if in_block else 2
        elif text.startswith("//", i):
            i = text.find("\n", i) if "\n" in text[i:] else len(text)
        elif text.startswith("/*", i):
            in_block, i = True, i + 2
        else:
            i += 1
    if in_block:
        lines[-1] += "*/"
    return (lines,)


def _s_custom():
    return ("".join(random.sample("abcd", R(0, 4))), st("abcde", 0, 8))


def _s_replace():
    s = st("ab", 1, 8)
    ops, i = [], 0
    while i < len(s) and len(ops) < 3:
        length = R(1, min(3, len(s) - i))
        source = s[i : i + length] if R(0, 1) else st("ab", length, length)
        ops.append((i, source, st("xy", 0, 3)))
        i += length + R(0, 1)
    random.shuffle(ops)
    return (s, [o[0] for o in ops], [o[1] for o in ops], [o[2] for o in ops])


def _s_buddy():
    s = st("ab", 0, 6)
    goal = list(s)
    if len(goal) > 1 and R(0, 3):
        i, j = random.sample(range(len(goal)), 2)
        goal[i], goal[j] = goal[j], goal[i]
    elif R(0, 2) == 0:
        goal = list(st("ab", len(s), len(s)))
    return (s, "".join(goal))


def _s_decode():
    s = random.choice("abc") + "".join(random.choice(["a", "b", "2", "3", "4"]) for _ in range(R(0, 6)))
    size = 0
    for ch in s:
        size = size * int(ch) if ch.isdigit() else size + 1
    return (s, R(1, min(size, 60)))


def _s_logs():
    logs = []
    for _ in range(R(1, 6)):
        ident = random.choice("abc") + str(R(1, 3))
        body = " ".join(random.choice("xyz") for _ in range(R(1, 3))) if R(0, 1) else f"{R(1, 9)} {R(1, 9)}"
        logs.append(f"{ident} {body}")
    return (logs,)


def _s_lus():
    return ([st("ab", 1, 5) for _ in range(R(2, 4))],)


def _s_replacement():
    pairs = [[random.choice("abc"), random.choice("abc")] for _ in range(R(0, 4))]
    return (st("abc", 1, 8), st("abc", 1, 4), pairs)


def _s_parts():
    if R(0, 1):
        pattern = [1] + [R(0, 1) for _ in range(R(0, 2))]
        arr = []
        for _ in range(3):
            arr += [0] * R(0, 2) + pattern
        return (arr,)
    return ([R(0, 1) for _ in range(R(3, 9))],)


def _s_three_norm(args, res):
    arr = args[0]
    if list(res) == [-1, -1]:
        return "none"
    i, j = res
    parts = (arr[: i + 1], arr[i + 1 : j], arr[j:])
    if not all(parts):
        return "bad"
    values = {int("".join(map(str, p)), 2) for p in parts}
    return "ok" if len(values) == 1 else "bad"


def _s_custom_norm(args, res):
    order, s = args
    if sorted(res) != sorted(s):
        return False
    rank = {c: i for i, c in enumerate(order)}
    ranks = [rank[c] for c in res if c in rank]
    return ranks == sorted(ranks)


GX32 = {
    ("strings", "Text Justification"): _s_justify,
    ("strings", "Fraction to Recurring Decimal"): lambda: (R(-30, 30), random.choice([-1, 1]) * R(1, 30)),
    ("strings", "Largest Number"): lambda: (ints(6, 0, 100, 1),),
    ("strings", "Integer to English Words"): lambda: (R(0, 10 ** R(1, 9)),),
    ("strings", "Reconstruct Original Digits from English"): _s_digits_words,
    ("strings", "Longest Uncommon Subsequence II"): _s_lus,
    ("strings", "Optimal Division"): lambda: (ints(6, 2, 9, 1),),
    ("strings", "Fraction Addition and Subtraction"): _s_fraction_sum,
    ("strings", "Remove Comments"): _s_comments,
    ("strings", "Rotated Digits"): lambda: (R(1, 2000),),
    ("strings", "Custom Sort String"): (_s_custom, _s_custom_norm),
    ("strings", "Find And Replace in String"): _s_replace,
    ("strings", "Buddy Strings"): _s_buddy,
    ("strings", "Decoded String at Index"): _s_decode,
    ("strings", "Reorder Data in Log Files"): _s_logs,
    ("strings", "Remove Letter To Equalize Frequency"): lambda: (st("abc", 2, 8),),
    ("strings", "Using a Robot to Print the Lexicographically Smallest String"): lambda: (st("abc", 1, 7),),
    ("strings", "Match Substring After Replacement"): _s_replacement,
    ("strings", "Three Equal Parts"): (_s_parts, _s_three_norm),
    ("strings", "Compare Strings by Frequency of the Smallest Character"): lambda: (
        [st("abc", 1, 5) for _ in range(R(0, 3))],
        [st("abc", 1, 5) for _ in range(R(1, 4))],
    ),
}

GX.update(GX32)


def _st_baseball():
    ops, size = [], 0
    for _ in range(R(1, 9)):
        choices = ["num"] + (["C", "D"] if size >= 1 else []) + (["+"] if size >= 2 else [])
        pick = random.choice(choices)
        if pick == "num":
            ops.append(str(R(-9, 9)))
            size += 1
        elif pick == "C":
            ops.append("C")
            size -= 1
        else:
            ops.append(pick)
            size += 1
    return (ops,)


def _st_parens_ok(s, got):
    """Valid brackets, a subsequence of s, and the minimum number of removals."""
    it = iter(s)
    if not all(c in it for c in got):
        return False
    bal = opens = bad = 0
    for c in got:
        bal += (c == "(") - (c == ")")
        if bal < 0:
            return False
    for c in s:
        if c == "(":
            opens += 1
        elif c == ")":
            if opens:
                opens -= 1
            else:
                bad += 1
    return bal == 0 and len(got) == len(s) - opens - bad


def _st_parens_norm(args, result):
    return _st_parens_ok(args[0], result)


def _st_threshold_norm(args, result):
    return result == -1


def _st_robots():
    n = R(1, 6)
    return (random.sample(range(1, 30), n), ints(n, 1, 9, n), "".join(random.choice("LR") for _ in range(n)))


GX33 = {
    ("stack_monotonic", "Baseball Game"): _st_baseball,
    ("stack_monotonic", "Shortest Subarray with Sum at Least K"): lambda: (ints(8, -5, 9, 1), R(1, 15)),
    ("stack_monotonic", "Minimum Cost Tree From Leaf Values"): lambda: (ints(7, 1, 9, 2),),
    ("stack_monotonic", "Minimum Remove to Make Valid Parentheses"): (
        lambda: (st("ab()", 0, 10),),
        _st_parens_norm,
    ),
    ("stack_monotonic", "Sum of Subarray Ranges"): lambda: (ints(8, -5, 5, 1),),
    ("stack_monotonic", "Replace Non-Coprime Numbers in Array"): lambda: (ints(8, 1, 12, 1),),
    ("stack_monotonic", "Steps to Make Array Non-decreasing"): lambda: (ints(10, 1, 9, 1),),
    ("stack_monotonic", "Subarray With Elements Greater Than Varying Threshold"): (
        lambda: (ints(7, 1, 10, 1), R(1, 30)),
        _st_threshold_norm,
    ),
    ("stack_monotonic", "Construct Smallest Number From DI String"): lambda: (st("ID", 1, 8),),
    ("stack_monotonic", "Next Greater Element IV"): lambda: (ints(9, 0, 8, 1),),
    ("stack_monotonic", "Robot Collisions"): _st_robots,
    ("stack_monotonic", "Beautiful Towers I"): lambda: (ints(8, 1, 9, 1),),
    (
        "stack_monotonic",
        "Find the Number of Subarrays Where Boundary Elements Are Maximum",
    ): lambda: (ints(10, 1, 4, 1),),
}

GX.update(GX33)


def _bs_candy():
    prices = ints(8, 1, 30, 2)
    return (prices, R(2, len(prices)))


def _bs_robber():
    n = R(1, 8)
    return ([R(1, 20) for _ in range(n)], R(1, (n + 1) // 2))


GX34 = {
    ("binary_search", "H-Index II"): lambda: (sorted(ints(8, 0, 10, 1)),),
    ("binary_search", "Preimage Size of Factorial Zeroes Function"): lambda: (R(0, 60),),
    ("binary_search", "Nth Magical Number"): lambda: (R(1, 30), R(2, 6), R(2, 6)),
    ("binary_search", "Ugly Number III"): lambda: (R(1, 30), R(1, 6), R(1, 6), R(1, 6)),
    ("binary_search", "Sum of Mutated Array Closest to Target"): lambda: (ints(6, 1, 20, 1), R(1, 60)),
    ("binary_search", "Special Array With X Elements Greater Than or Equal X"): lambda: (ints(8, 0, 10, 1),),
    ("binary_search", "Minimize Maximum of Array"): lambda: (ints(8, 0, 12, 1),),
    ("binary_search", "Maximum Tastiness of Candy Basket"): _bs_candy,
    ("binary_search", "House Robber IV"): _bs_robber,
}

GX.update(GX34)


GX35 = {
    ("linked_list", "Double a Number Represented as a Linked List"): lambda: (
        [R(1, 9)] + [R(0, 9) for _ in range(R(0, 7))],
    ),
}

GX.update(GX35)


def _special_tree():
    """Every node has 0 or 2 children and holds the minimum of its children (LeetCode 671's guarantee)."""

    def build(depth):
        if depth == 0 or random.random() < 0.3:
            return TreeNode(R(1, 5))
        left, right = build(depth - 1), build(depth - 1)
        return TreeNode(min(left.val, right.val), left, right)

    return (tree_to_list(build(R(0, 3))),)


def _all_nodes(root):
    nodes, stack = [], [root]
    while stack:
        node = stack.pop()
        nodes.append(node)
        stack += [c for c in (node.left, node.right) if c]
    return nodes


def _nonempty_root(n_max=8):
    root = None
    while root is None:
        root = rand_tree(n_max, 0, 0)
    return root


def _coins_tree():
    root = _nonempty_root()
    nodes = _all_nodes(root)
    for _ in nodes:
        random.choice(nodes).val += 1
    return (tree_to_list(root),)


def _tree_min2(lo=1, hi=9):
    while True:
        lst = tree_list(9, lo, hi)
        if sum(v is not None for v in lst) >= 2:
            return lst


def _game_args():
    root = _nonempty_root(9)
    nodes = _all_nodes(root)
    labels = list(range(1, len(nodes) + 1))
    random.shuffle(labels)
    for node, label in zip(nodes, labels):
        node.val = label
    return (tree_to_list(root), len(nodes), R(1, len(nodes)))


GX36 = {
    ("trees", "Second Minimum Node In a Binary Tree"): _special_tree,
    ("trees", "Minimum Distance Between BST Nodes"): lambda: (_bst_min2(),),
    ("trees", "Binary Tree Pruning"): lambda: (tree_list(9, 0, 1),),
    ("trees", "Distribute Coins in Binary Tree"): _coins_tree,
    ("trees", "Sum of Root To Leaf Binary Numbers"): lambda: (_nonempty_tree(9, 0, 1),),
    ("trees", "Binary Search Tree to Greater Sum Tree"): lambda: (_bst_nonempty(),),
    ("trees", "Delete Leaves With a Given Value"): lambda: (tree_list(9, 1, 3), R(1, 3)),
    ("trees", "Maximum Product of Splitted Binary Tree"): lambda: (_tree_min2(1, 9),),
    ("trees", "Longest ZigZag Path in a Binary Tree"): lambda: (_nonempty_tree(10, 1, 1),),
    ("trees", "Pseudo-Palindromic Paths in a Binary Tree"): lambda: (_nonempty_tree(9, 1, 4),),
    ("trees", "Number of Good Leaf Nodes Pairs"): lambda: (_nonempty_tree(9, 1, 1), R(1, 6)),
    ("trees", "Even Odd Tree"): lambda: (_nonempty_tree(10, 1, 12),),
    ("trees", "Kth Largest Sum in a Binary Tree"): lambda: (_nonempty_tree(10, 1, 9), R(1, 5)),
    ("trees", "Reverse Odd Levels of Binary Tree"): lambda: ([R(0, 9) for _ in range(2 ** R(1, 4) - 1)],),
    ("trees", "Cousins in Binary Tree II"): lambda: (_nonempty_tree(10, 1, 9),),
    (
        "trees",
        "Minimum Number of Operations to Sort a Binary Tree by Level",
    ): lambda: (_nonempty_tree(9, 1, 40, unique=True),),
    ("trees", "Binary Tree Coloring Game"): _game_args,
    ("trees", "Construct String from Binary Tree"): lambda: (_nonempty_tree(9, 0, 9),),
    ("trees", "Maximum Sum BST in Binary Tree"): lambda: (_nonempty_tree(9, -4, 9),),
    ("trees", "Vertical Order Traversal of a Binary Tree"): lambda: (_nonempty_tree(10, 0, 9),),
}

GX.update(GX36)


def _g_pairs(n, k):
    """Up to k distinct unordered node pairs (as lists) from nodes 0..n-1."""
    pairs = [[i, j] for i in range(n) for j in range(i + 1, n)]
    random.shuffle(pairs)
    return pairs[: R(0, k)]


def _g_tree(n):
    return [[i, R(0, i - 1)] for i in range(1, n)]


def _g_connected(n, offset=0, hi=5, extra=3):
    """A connected weighted graph: random tree plus a few extra distinct edges, nodes offset..offset+n-1."""
    pairs = {tuple(sorted(e)) for e in _g_tree(n)}
    pairs |= {tuple(p) for p in _g_pairs(n, extra)}
    return [[u + offset, v + offset, R(1, hi)] for u, v in sorted(pairs)]


def _g_water():
    n = R(1, 4)
    values = list(range(n * n))
    random.shuffle(values)
    return ([values[i * n : (i + 1) * n] for i in range(n)],)


def _g_alt():
    n = R(1, 5)
    return (
        n,
        [[R(0, n - 1), R(0, n - 1)] for _ in range(R(0, 5))],
        [[R(0, n - 1), R(0, n - 1)] for _ in range(R(0, 5))],
    )


def _g_dag():
    n = R(1, 7)
    return (n, [p for p in _g_pairs(n, 10)])


def _g_secret():
    n = R(2, 6)
    meetings = []
    for _ in range(R(0, 6)):
        x, y = random.sample(range(n), 2)
        meetings.append([x, y, R(1, 4)])
    return (n, meetings, R(1, n - 1))


def _g_goodpaths():
    n = R(1, 7)
    return ([R(1, 3) for _ in range(n)], _g_tree(n))


def _g_restricted():
    n = R(2, 7)
    return (n, _g_tree(n), random.sample(range(1, n), R(0, n - 1)))


def _g_disappear():
    n = R(1, 5)
    edges = [p + [R(1, 5)] for p in _g_pairs(n, 6)]
    return (n, edges, [R(1, 10) for _ in range(n)])


def _g_roads_queries():
    n = R(3, 7)
    queries = []
    for _ in range(R(1, 4)):
        u = R(0, n - 3)
        queries.append([u, R(u + 2, n - 1)])
    return (n, queries)


def _g_apples():
    n = R(1, 8)
    return (n, _g_tree(n), [random.random() < 0.5 for _ in range(n)])


def _g_safest():
    n = R(1, 4)
    grid = [[R(0, 1) for _ in range(n)] for _ in range(n)]
    grid[R(0, n - 1)][R(0, n - 1)] = 1
    return (grid,)


def _g_slashes():
    n = R(1, 4)
    return (["".join(random.choice(" /\\") for _ in range(n)) for _ in range(n)],)


def _g_nc(lo, hi, offset=0, weight=5):
    n = R(lo, hi)
    return (n, _g_connected(n, offset, weight))


def _g_graph(lo, hi, k):
    n = R(lo, hi)
    return (n, _g_pairs(n, k))


def _g_star():
    n = R(1, 6)
    return ([R(-5, 9) for _ in range(n)], _g_pairs(n, 6), R(0, 4))


GX37 = {
    ("graphs", "Swim in Rising Water"): _g_water,
    ("graphs", "Regions Cut By Slashes"): _g_slashes,
    ("graphs", "Shortest Path with Alternating Colors"): _g_alt,
    ("graphs", "Minimum Number of Vertices to Reach All Nodes"): _g_dag,
    ("graphs", "Number of Restricted Paths From First to Last Node"): lambda: _g_nc(2, 6, 1),
    ("graphs", "Find All People With Secret"): _g_secret,
    ("graphs", "Detonate the Maximum Bombs"): lambda: ([[R(0, 8), R(0, 8), R(1, 4)] for _ in range(R(1, 6))],),
    ("graphs", "Count Unreachable Pairs of Nodes in an Undirected Graph"): lambda: _g_graph(1, 7, 6),
    ("graphs", "Number of Good Paths"): _g_goodpaths,
    ("graphs", "Minimum Score of a Path Between Two Cities"): lambda: _g_nc(2, 6, 1, 9),
    ("graphs", "Minimum Fuel Cost to Report to the Capital"): lambda: (_g_tree(R(1, 8)), R(1, 5)),
    ("graphs", "Maximum Star Sum of a Graph"): _g_star,
    ("graphs", "Reachable Nodes With Restrictions"): _g_restricted,
    ("graphs", "Count the Number of Complete Components"): lambda: _g_graph(1, 6, 8),
    ("graphs", "Find Minimum Time to Visit Disappearing Nodes"): _g_disappear,
    ("graphs", "Shortest Distance After Road Addition Queries I"): _g_roads_queries,
    ("graphs", "Minimum Time to Collect All Apples in a Tree"): _g_apples,
    ("graphs", "Number of Ways to Arrive at Destination"): lambda: _g_nc(2, 6, 0),
    ("graphs", "Find the Safest Path in a Grid"): _g_safest,
    ("graphs", "Shortest Cycle in a Graph"): lambda: _g_graph(1, 7, 9),
}

GX.update(GX37)


def _gr_adv():
    n = R(1, 6)
    return ([R(0, 9) for _ in range(n)], [R(0, 9) for _ in range(n)])


def _gr_adv_norm(args, result):
    """Advantage count of the answer, or None if it is not a rearrangement of nums1."""
    if not isinstance(result, list) or sorted(result) != sorted(args[0]):
        return None
    return sum(x > y for x, y in zip(result, args[1]))


def _gr_cols():
    rows, width = R(1, 4), R(1, 4)
    return (["".join(random.choice("abcd") for _ in range(width)) for _ in range(rows)],)


def _gr_ab():
    while True:
        a, b = R(0, 6), R(0, 6)
        if a + b and max(a, b) <= 2 * (min(a, b) + 1):
            return (a, b)


def _gr_ab_norm(args, result):
    a, b = args
    return (
        isinstance(result, str)
        and len(result) == a + b
        and result.count("a") == a
        and result.count("b") == b
        and "aaa" not in result
        and "bbb" not in result
    )


def _gr_pal():
    n = R(1, 7)
    half = [random.choice("abc") for _ in range((n + 1) // 2)]
    return ("".join(half + half[: n // 2][::-1]),)


def _gr_uniq():
    arr = ints(8, 1, 5, 1)
    return (arr, R(0, len(arr)))


def _gr_numeric():
    n = R(1, 6)
    return (n, R(n, 26 * n))


def _gr_triplets():
    triplets = [[R(1, 4) for _ in range(3)] for _ in range(R(1, 5))]
    return (triplets, [R(1, 4) for _ in range(3)])


def _gr_brackets():
    n = R(1, 4)
    chars = ["["] * n + ["]"] * n
    random.shuffle(chars)
    return ("".join(chars),)


def _gr_pieces():
    pool = random.choice(["AB", "AAAB", "ABBB"])
    return ("".join(random.choice(pool) for _ in range(R(1, 10))),)


def _gr_bags():
    n = R(1, 6)
    capacity = [R(1, 6) for _ in range(n)]
    return (capacity, [R(0, c) for c in capacity], R(0, 10))


GX38 = {
    ("greedy", "Dota2 Senate"): lambda: ("".join(random.choice("RD") for _ in range(R(1, 9))),),
    ("greedy", "Advantage Shuffle"): (_gr_adv, _gr_adv_norm),
    ("greedy", "Delete Columns to Make Sorted"): _gr_cols,
    ("greedy", "String Without AAA or BBB"): (_gr_ab, _gr_ab_norm),
    ("greedy", "Previous Permutation With One Swap"): lambda: (ints(7, 1, 5, 1),),
    ("greedy", "Break a Palindrome"): _gr_pal,
    ("greedy", "Max Difference You Can Get From Changing an Integer"): lambda: (R(1, 99999),),
    ("greedy", "Least Number of Unique Integers after K Removals"): _gr_uniq,
    ("greedy", "Smallest String With A Given Numeric Value"): _gr_numeric,
    ("greedy", "Partitioning Into Minimum Number Of Deci-Binary Numbers"): lambda: (str(R(1, 99999999)),),
    ("greedy", "Maximum Element After Decreasing and Rearranging"): lambda: (ints(8, 1, 12, 1),),
    ("greedy", "Merge Triplets to Form Target Triplet"): _gr_triplets,
    ("greedy", "Maximum Number of Weeks for Which You Can Work"): lambda: (ints(4, 1, 4, 1),),
    ("greedy", "Minimum Number of Swaps to Make the String Balanced"): _gr_brackets,
    ("greedy", "The Number of Weak Characters in the Game"): lambda: ([[R(1, 5), R(1, 5)] for _ in range(R(1, 8))],),
    ("greedy", "Remove Colored Pieces if Both Neighbors are the Same Color"): _gr_pieces,
    ("greedy", "Destroying Asteroids"): lambda: (R(1, 10), ints(6, 1, 20, 1)),
    ("greedy", "Maximum Bags With Full Capacity of Rocks"): _gr_bags,
    ("greedy", "Partition Array Such That Maximum Difference Is K"): lambda: (ints(7, 1, 9, 1), R(0, 4)),
    ("greedy", "Optimal Partition of String"): lambda: ("".join(random.choice("abcd") for _ in range(R(1, 10))),),
}

GX.update(GX38)


def _dp_frog():
    return ([0] + sorted(random.sample(range(1, 14), R(1, 7))),)


def _dp_wrap():
    return ("".join(random.choice("abcz") for _ in range(R(1, 10))),)


def _dp_inverse():
    n = R(1, 6)
    return (n, R(0, n * (n - 1) // 2 + 1))


def _dp_strings():
    return (
        "".join(random.choice("abc") for _ in range(R(1, 6))),
        "".join(random.choice("abc") for _ in range(R(1, 6))),
    )


def _dp_swap():
    n = R(1, 7)
    x = sorted(random.sample(range(20), n))
    y = sorted(random.sample(range(20), n))
    for i in range(n):
        if random.random() < 0.5:
            x[i], y[i] = y[i], x[i]
    return (x, y)


def _dp_averages():
    return ([R(1, 9) for _ in range(R(1, 6))], R(1, 4))


def _dp_game():
    k = R(0, 6)
    return (R(0, 10), k, R(1, 4))


def _dp_books():
    return ([[R(1, 4), R(1, 5)] for _ in range(R(1, 6))], R(4, 8))


GX39 = {
    ("dynamic_programming", "Frog Jump"): _dp_frog,
    ("dynamic_programming", "Unique Substrings in Wraparound String"): _dp_wrap,
    ("dynamic_programming", "Student Attendance Record II"): lambda: (R(1, 8),),
    ("dynamic_programming", "Non-negative Integers without Consecutive Ones"): lambda: (R(1, 300),),
    ("dynamic_programming", "K Inverse Pairs Array"): _dp_inverse,
    ("dynamic_programming", "2 Keys Keyboard"): lambda: (R(1, 30),),
    ("dynamic_programming", "Minimum ASCII Delete Sum for Two Strings"): _dp_strings,
    ("dynamic_programming", "Champagne Tower"): lambda: (lambda row: (R(0, 20), row, R(0, row)))(R(0, 5)),
    ("dynamic_programming", "Minimum Swaps To Make Sequences Increasing"): _dp_swap,
    ("dynamic_programming", "Soup Servings"): lambda: (R(1, 150),),
    ("dynamic_programming", "Largest Sum of Averages"): _dp_averages,
    ("dynamic_programming", "Binary Trees With Factors"): lambda: (random.sample(range(2, 25), R(1, 6)),),
    ("dynamic_programming", "New 21 Game"): _dp_game,
    ("dynamic_programming", "Flip String to Monotone Increasing"): lambda: (
        "".join(random.choice("01") for _ in range(R(1, 10))),
    ),
    ("dynamic_programming", "Knight Dialer"): lambda: (R(1, 8),),
    ("dynamic_programming", "Distinct Subsequences II"): lambda: (
        "".join(random.choice("abc") for _ in range(R(1, 9))),
    ),
    ("dynamic_programming", "Last Stone Weight II"): lambda: (ints(8, 1, 12, 1),),
    ("dynamic_programming", "Filling Bookcase Shelves"): _dp_books,
    ("dynamic_programming", "Count Vowels Permutation"): lambda: (R(1, 7),),
    ("dynamic_programming", "Count Sorted Vowel Strings"): lambda: (R(1, 10),),
}

GX.update(GX39)
