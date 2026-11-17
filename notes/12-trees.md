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
| `trees/25` | Easy | Binary Tree Inorder Traversal | [#94](https://leetcode.com/problems/binary-tree-inorder-traversal/) | Tree traversal with an explicit stack (simulate recursion) |
| `trees/26` | Easy | Binary Tree Postorder Traversal | [#145](https://leetcode.com/problems/binary-tree-postorder-traversal/) | Postorder = reverse of (node, right, left) preorder |
| `trees/28` | Easy | Binary Tree Paths | [#257](https://leetcode.com/problems/binary-tree-paths/) | DFS with a path list that is extended and then undone (backtracking) |
| `trees/29` | Easy | Count Complete Tree Nodes | [#222](https://leetcode.com/problems/count-complete-tree-nodes/) | Use the tree's structure: one half is always a perfect tree |
| `trees/31` | Easy | Search in a Binary Search Tree | [#700](https://leetcode.com/problems/search-in-a-binary-search-tree/) | BST descent: discard half the tree at every step |
| `trees/34` | Easy | Sum of Left Leaves | [#404](https://leetcode.com/problems/sum-of-left-leaves/) | Look at the child from the parent (or pass an is_left flag down) |
| `trees/35` | Easy | Merge Two Binary Trees | [#617](https://leetcode.com/problems/merge-two-binary-trees/) | Parallel DFS over two trees |
| `trees/36` | Easy | Average of Levels in Binary Tree | [#637](https://leetcode.com/problems/average-of-levels-in-binary-tree/) | BFS level by level |
| `trees/42` | Easy | Binary Tree Preorder Traversal | [#144](https://leetcode.com/problems/binary-tree-preorder-traversal/) | Iterative DFS with an explicit stack |
| `trees/43` | Easy | Minimum Absolute Difference in BST | [#530](https://leetcode.com/problems/minimum-absolute-difference-in-bst/) | Inorder traversal = sorted order; compare neighbours |
| `trees/44` | Easy | Binary Tree Tilt | [#563](https://leetcode.com/problems/binary-tree-tilt/) | Post-order DFS returning an aggregate while updating a global |
| `trees/45` | Easy | Two Sum IV - Input is a BST | [#653](https://leetcode.com/problems/two-sum-iv-input-is-a-bst/) | Two Sum with a hash set while traversing |
| `trees/47` | Easy | Leaf-Similar Trees | [#872](https://leetcode.com/problems/leaf-similar-trees/) | DFS leaf collection; generators for early exit |
| `trees/48` | Easy | Range Sum of BST | [#938](https://leetcode.com/problems/range-sum-of-bst/) | DFS with BST pruning |
| `trees/49` | Easy | Univalued Binary Tree | [#965](https://leetcode.com/problems/univalued-binary-tree/) | DFS with early exit |
| `trees/50` | Easy | Cousins in Binary Tree | [#993](https://leetcode.com/problems/cousins-in-binary-tree/) | BFS level scan with a sibling check |
| `trees/57` | Easy | Increasing Order Search Tree | [#897](https://leetcode.com/problems/increasing-order-search-tree/) | Inorder traversal with relinking |
| `trees/58` | Easy | Second Minimum Node In a Binary Tree | [#671](https://leetcode.com/problems/second-minimum-node-in-a-binary-tree/) | Tree traversal with pruning using the heap-like property |
| `trees/59` | Easy | Minimum Distance Between BST Nodes | [#783](https://leetcode.com/problems/minimum-distance-between-bst-nodes/) | Inorder traversal gives sorted order; compare neighbours |
| `trees/62` | Easy | Sum of Root To Leaf Binary Numbers | [#1022](https://leetcode.com/problems/sum-of-root-to-leaf-binary-numbers/) | DFS carrying a running value (Horner's rule) |
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
| `trees/27` | Medium | Binary Tree Zigzag Level Order Traversal | [#103](https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/) | BFS level by level + reverse alternate levels |
| `trees/30` | Medium | Construct Binary Tree from Inorder and Postorder Traversal | [#106](https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/) | Divide & conquer on traversals: root from one order, split point from the other |
| `trees/32` | Medium | Convert BST to Greater Tree | [#538](https://leetcode.com/problems/convert-bst-to-greater-tree/) | Reverse inorder (right, node, left) with a running sum |
| `trees/33` | Medium | Path Sum II | [#113](https://leetcode.com/problems/path-sum-ii/) | DFS + backtracking with a remaining-sum parameter |
| `trees/37` | Medium | Maximum Width of Binary Tree | [#662](https://leetcode.com/problems/maximum-width-of-binary-tree/) | BFS with heap-style position numbering |
| `trees/38` | Medium | Longest Univalue Path | [#687](https://leetcode.com/problems/longest-univalue-path/) | DFS returning the best 'arm', global answer combines two arms (diameter pattern) |
| `trees/40` | Medium | Delete Nodes And Return Forest | [#1110](https://leetcode.com/problems/delete-nodes-and-return-forest/) | DFS that returns the node (or None) so the parent can re-link |
| `trees/41` | Medium | Lowest Common Ancestor of Deepest Leaves | [#1123](https://leetcode.com/problems/lowest-common-ancestor-of-deepest-leaves/) | DFS returning (depth, candidate node) |
| `trees/46` | Medium | Trim a Binary Search Tree | [#669](https://leetcode.com/problems/trim-a-binary-search-tree/) | Recursion that returns the replacement subtree |
| `trees/51` | Medium | Maximum Difference Between Node and Ancestor | [#1026](https://leetcode.com/problems/maximum-difference-between-node-and-ancestor/) | Carry path statistics downward |
| `trees/52` | Medium | Deepest Leaves Sum | [#1302](https://leetcode.com/problems/deepest-leaves-sum/) | BFS, keep the last level |
| `trees/53` | Medium | Sum of Nodes with Even-Valued Grandparent | [#1315](https://leetcode.com/problems/sum-of-nodes-with-even-valued-grandparent/) | DFS carrying parent and grandparent |
| `trees/54` | Medium | Maximum Level Sum of a Binary Tree | [#1161](https://leetcode.com/problems/maximum-level-sum-of-a-binary-tree/) | BFS with per-level aggregation |
| `trees/55` | Medium | Construct Binary Search Tree from Preorder Traversal | [#1008](https://leetcode.com/problems/construct-binary-search-tree-from-preorder-traversal/) | Recursive build with upper bounds (one pass) |
| `trees/56` | Medium | Add One Row to Tree | [#623](https://leetcode.com/problems/add-one-row-to-tree/) | Level-targeted tree surgery (BFS or DFS with a depth counter) |
| `trees/60` | Medium | Binary Tree Pruning | [#814](https://leetcode.com/problems/binary-tree-pruning/) | Postorder recursion (decide after the children are done) |
| `trees/61` | Medium | Distribute Coins in Binary Tree | [#979](https://leetcode.com/problems/distribute-coins-in-binary-tree/) | Postorder excess / flow across each edge |
| `trees/63` | Medium | Binary Search Tree to Greater Sum Tree | [#1038](https://leetcode.com/problems/binary-search-tree-to-greater-sum-tree/) | Reverse inorder traversal with a running sum |
| `trees/64` | Medium | Delete Leaves With a Given Value | [#1325](https://leetcode.com/problems/delete-leaves-with-a-given-value/) | Postorder recursion that returns the (possibly deleted) subtree |
| `trees/65` | Medium | Maximum Product of Splitted Binary Tree | [#1339](https://leetcode.com/problems/maximum-product-of-splitted-binary-tree/) | Subtree sums via postorder, then maximise over cut points |
| `trees/66` | Medium | Longest ZigZag Path in a Binary Tree | [#1372](https://leetcode.com/problems/longest-zigzag-path-in-a-binary-tree/) | Tree DP returning two values per node |
| `trees/67` | Medium | Pseudo-Palindromic Paths in a Binary Tree | [#1457](https://leetcode.com/problems/pseudo-palindromic-paths-in-a-binary-tree/) | DFS with a parity bitmask |
| `trees/68` | Medium | Number of Good Leaf Nodes Pairs | [#1530](https://leetcode.com/problems/number-of-good-leaf-nodes-pairs/) | Postorder with distance histograms of leaves |
| `trees/69` | Medium | Even Odd Tree | [#1609](https://leetcode.com/problems/even-odd-tree/) | BFS level by level with a running 'previous' value |
| `trees/70` | Medium | Kth Largest Sum in a Binary Tree | [#2583](https://leetcode.com/problems/kth-largest-sum-in-a-binary-tree/) | BFS level sums + size-k min-heap |
| `trees/71` | Medium | Reverse Odd Levels of Binary Tree | [#2415](https://leetcode.com/problems/reverse-odd-levels-of-binary-tree/) | Mirror-pair recursion on a perfect tree |
| `trees/72` | Medium | Cousins in Binary Tree II | [#2641](https://leetcode.com/problems/cousins-in-binary-tree-ii/) | BFS with level totals and sibling sums |
| `trees/73` | Medium | Minimum Number of Operations to Sort a Binary Tree by Level | [#2471](https://leetcode.com/problems/minimum-number-of-operations-to-sort-a-binary-tree-by-level/) | Level order + minimum swaps to sort (permutation cycles) |
| `trees/74` | Medium | Binary Tree Coloring Game | [#1145](https://leetcode.com/problems/binary-tree-coloring-game/) | Subtree sizes: the biggest of three regions |
| `trees/75` | Medium | Construct String from Binary Tree | [#606](https://leetcode.com/problems/construct-string-from-binary-tree/) | Preorder recursion with a conditional formatting rule |
| `trees/5` | Hard | Binary Tree Maximum Path Sum | [#124](https://leetcode.com/problems/binary-tree-maximum-path-sum/) | Tree DP: return one value upward, record a different value (the bend) in a global |
| `trees/19` | Hard | Serialize and Deserialize Binary Tree | [#297](https://leetcode.com/problems/serialize-and-deserialize-binary-tree/) | Preorder with null markers (a traversal that is uniquely decodable) |
| `trees/39` | Hard | Binary Tree Cameras | [#968](https://leetcode.com/problems/binary-tree-cameras/) | Tree DP / greedy bottom-up with 3 states |
| `trees/76` | Hard | Maximum Sum BST in Binary Tree | [#1373](https://leetcode.com/problems/maximum-sum-bst-in-binary-tree/) | Postorder returning (is_bst, min, max, sum) per subtree |
| `trees/77` | Hard | Vertical Order Traversal of a Binary Tree | [#987](https://leetcode.com/problems/vertical-order-traversal-of-a-binary-tree/) | Coordinates + sort + group |

Start one with `python dsa.py start trees/1`.

**More:** 226 Invert Binary Tree (E), 100 Same Tree (E), 101 Symmetric Tree (E), 543 Diameter of Binary Tree (E), 110 Balanced Binary Tree (E), 112 Path Sum (E), 199 Binary Tree Right Side View (M), 230 Kth Smallest Element in a BST (M), 235 Lowest Common Ancestor of a Binary Search Tree (M), 105 Construct Binary Tree from Preorder and Inorder Traversal (M), 114 Flatten Binary Tree to Linked List (M), 437 Path Sum III (M), 337 House Robber III (M), 297 Serialize and Deserialize Binary Tree (H), 450 Delete Node in a BST (M).

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
