# 12 - Trees (recursion, DFS, BFS, BST)

> **One idea:** a tree is a node plus two smaller trees. Solve the node by *trusting* the recursive answers for the children.

## 1. First principles
- Recursion on trees needs just two decisions: the **base case** (usually `None`) and the **combine step** at the node.
- Order of work decides the style:
  - **Post-order (children first):** the answer for a node depends on its children (height, diameter, max path sum, LCA).
  - **Pre-order (node first):** pass information *down* (path sum so far, range limits for BST validation).
  - **In-order:** on a BST this visits keys in sorted order.
  - **BFS / level-order:** a queue, process `len(queue)` nodes per level.
- **"Return one thing up, record another thing globally"** is the trick behind Diameter and Max Path Sum.
- BST property: left subtree < node < right subtree **for all descendants**, not just children.
- Recursion depth = tree height h; skewed tree -> h = n (mind Python's recursion limit, or go iterative).

## 2. How to spot it
- Input is `root`/`TreeNode`. Words: depth, height, path, ancestor, subtree, level, view, serialise.
- BST: "sorted", "k-th smallest", "validate", "successor", "insert/delete".

## 3. Paper recipe
1. Draw a small tree (5-7 nodes, include a skewed branch and a leaf).
2. Write what the function returns for a **leaf** and for **None**.
3. Write what it returns for a node *given* `f(left)` and `f(right)`. That one line is the algorithm.
4. Need a second quantity (global best)? Keep it in a `nonlocal` variable / one-element list.
5. Pass constraints down as parameters (`lo`, `hi`, `depth`, `target - node.val`).
6. For levels use BFS; for paths use DFS.

## 4. Hand trace (post-order, return up / record globally)
Tree `[-10, 9, 20, null, null, 15, 7]` (post-order: children are finished before their parent)

| node | left gain (>=0) | right gain (>=0) | bend here = val+l+r | returned upward = val+max(l,r) | best so far |
|---|---|---|---|---|---|
| 9 | 0 | 0 | 9 | 9 | 9 |
| 15 | 0 | 0 | 15 | 15 | 15 |
| 7 | 0 | 0 | 7 | 7 | 15 |
| 20 | 15 | 7 | 42 | 35 | 42 |
| -10 | 9 | 35 | 34 | 25 | 42 |

Answer: **42** (path 15 -> 20 -> 7; the root -10 would only hurt).

## 5. Template
*Reference solution for **Binary Tree Maximum Path Sum** (`trees/5`) - tested by `python dsa.py selftest`:*

```python
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
```

BFS skeleton: see `trees/2` (`for _ in range(len(q))` = one level).

## 6. Traps
- BST validation by checking only the parent's value (use bounds).
- Not handling `None` / a single node / skewed tree.
- Mutating shared lists in recursion without copying.
- Confusing **depth in edges vs nodes** - read the problem.
- Path problems: a path cannot branch; the *returned* value uses one child, the *recorded* value uses both.

## 7. Self-check
1. Write DFS pre-/in-/post-order both recursively and with an explicit stack.
2. Why does an in-order walk of a BST come out sorted?
3. In Max Path Sum, why do we clamp child gains with `max(.., 0)`?

## 8. Practice ladder
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `trees/1` | Easy | Maximum Depth of Binary Tree | [#104](https://leetcode.com/problems/maximum-depth-of-binary-tree/) | Tree recursion (post-order): answer(node) = f(answer(left), answer(right)) |
| `trees/6` | Easy | Same Tree | [#100](https://leetcode.com/problems/same-tree/) | Simultaneous recursion over two trees |
| `trees/7` | Easy | Invert Binary Tree | [#226](https://leetcode.com/problems/invert-binary-tree/) | Tree recursion: solve subtrees, combine at the root |
| `trees/8` | Easy | Symmetric Tree | [#101](https://leetcode.com/problems/symmetric-tree/) | Two-node recursion with crossed children |
| `trees/9` | Easy | Subtree of Another Tree | [#572](https://leetcode.com/problems/subtree-of-another-tree/) | Tree recursion reusing a helper (same-tree at every node) |
| `trees/10` | Easy | Balanced Binary Tree | [#110](https://leetcode.com/problems/balanced-binary-tree/) | Post-order DFS returning a value + failure sentinel (bottom-up) |
| `trees/11` | Easy | Diameter of Binary Tree | [#543](https://leetcode.com/problems/diameter-of-binary-tree/) | Tree DP: return one thing upward, update the answer with another |
| `trees/20` | Easy | Path Sum | [#112](https://leetcode.com/problems/path-sum/) | DFS carrying a running remainder (top-down) |
| `trees/21` | Easy | Minimum Depth of Binary Tree | [#111](https://leetcode.com/problems/minimum-depth-of-binary-tree/) | BFS for the nearest leaf (early exit) |
| `trees/24` | Easy | Convert Sorted Array to Binary Search Tree | [#108](https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/) | Divide and conquer on the midpoint (balanced construction) |
| `trees/2` | Medium | Binary Tree Level Order Traversal | [#102](https://leetcode.com/problems/binary-tree-level-order-traversal/) | BFS with a queue, one level per round (snapshot len(queue)) |
| `trees/3` | Medium | Validate Binary Search Tree | [#98](https://leetcode.com/problems/validate-binary-search-tree/) | Tree recursion passing constraints DOWN (top-down), or in-order traversal must be increasing |
| `trees/4` | Medium | Lowest Common Ancestor of a Binary Tree | [#236](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/) | Post-order tree recursion returning 'what I found below me' |
| `trees/12` | Medium | Binary Tree Right Side View | [#199](https://leetcode.com/problems/binary-tree-right-side-view/) | Level-order BFS (last per level) / depth-tracked DFS |
| `trees/13` | Medium | Kth Smallest Element in a BST | [#230](https://leetcode.com/problems/kth-smallest-element-in-a-bst/) | BST inorder = sorted order (with early stop) |
| `trees/14` | Medium | Construct Binary Tree from Preorder and Inorder Traversal | [#105](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/) | Divide and conquer using traversal properties |
| `trees/15` | Medium | Count Good Nodes in Binary Tree | [#1448](https://leetcode.com/problems/count-good-nodes-in-binary-tree/) | DFS carrying state down the path (top-down parameter) |
| `trees/16` | Medium | Path Sum III | [#437](https://leetcode.com/problems/path-sum-iii/) | Prefix sums + hash map on a tree path (with backtracking of the counts) |
| `trees/17` | Medium | Lowest Common Ancestor of a Binary Search Tree | [#235](https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/) | BST property turns a search into a single downward walk |
| `trees/18` | Medium | House Robber III | [#337](https://leetcode.com/problems/house-robber-iii/) | Tree DP returning a pair of states (take / skip) |
| `trees/22` | Medium | Sum Root to Leaf Numbers | [#129](https://leetcode.com/problems/sum-root-to-leaf-numbers/) | DFS carrying an accumulated value (top-down) |
| `trees/23` | Medium | Find Largest Value in Each Tree Row | [#515](https://leetcode.com/problems/find-largest-value-in-each-tree-row/) | BFS by levels (aggregate per level) |
| `trees/5` | Hard | Binary Tree Maximum Path Sum | [#124](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Tree DP: return one value upward, record a different value (the bend) in a global |
| `trees/19` | Hard | Serialize and Deserialize Binary Tree | [#297](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Preorder with null markers (a traversal that is uniquely decodable) |

Start one with `python dsa.py start trees/1`.

**More:** 226 Invert Binary Tree (E), 100 Same Tree (E), 101 Symmetric Tree (E), 543 Diameter of Binary Tree (E), 110 Balanced Binary Tree (E), 112 Path Sum (E), 199 Right Side View (M), 230 Kth Smallest in a BST (M), 235 LCA of a BST (M), 105 Construct from Preorder and Inorder (M), 114 Flatten to Linked List (M), 437 Path Sum III (M), 337 House Robber III (M), 297 Serialize and Deserialize (H), 450 Delete Node in a BST (M).

## 9. Make it stay - the teacher's anchors

**Picture it.** A company org chart: each manager only needs a report from direct reports. Information flows UP as return values, and instructions flow DOWN as parameters.

**The rule in one sentence.** Decide what each node must (1) receive from its parent and (2) return to its parent - then recursion writes itself.

**Why it works.** A tree is recursive by definition (a node + two trees), so a correct answer for the subtrees plus a combine step at the root is a proof by induction.

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. Which problems pass state DOWN (good nodes) and which return state UP (balanced tree)?
2. Why does a BST inorder give sorted order?
3. What is the difference between the value a node RETURNS and the candidate answer it RECORDS (diameter)?

**Mistakes students make most.**
- Forgetting the None base case.
- Validating a BST by comparing only with the parent (must carry a (low, high) range).
- Recomputing heights top-down (O(n^2)) instead of bottom-up.

**When NOT to use it.** The structure has cycles (it is a graph - add a visited set) or very deep chains risk recursion limits (use an explicit stack).

**The same idea in disguise.** Depth -> balanced -> diameter -> max path sum (return one-sided chain, record two-sided) -> LCA -> path sum III (prefix sums on a path) -> serialize (preorder + nulls).
