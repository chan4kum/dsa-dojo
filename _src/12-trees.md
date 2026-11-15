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
{{trace:tree_path}}

## 5. Template
{{solution:trees/5}}

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
{{ladder}}

**More:** 226 Invert Binary Tree (E), 100 Same Tree (E), 101 Symmetric Tree (E), 543 Diameter of Binary Tree (E), 110 Balanced Binary Tree (E), 112 Path Sum (E), 199 Binary Tree Right Side View (M), 230 Kth Smallest Element in a BST (M), 235 Lowest Common Ancestor of a Binary Search Tree (M), 105 Construct Binary Tree from Preorder and Inorder Traversal (M), 114 Flatten Binary Tree to Linked List (M), 437 Path Sum III (M), 337 House Robber III (M), 297 Serialize and Deserialize Binary Tree (H), 450 Delete Node in a BST (M).
