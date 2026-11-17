# 20 - Matrix & simulation

> **One idea:** a matrix is just coordinates (r, c). Write down where each cell goes, then express big transforms as a composition of small, safe ones.

## 1. First principles
- A grid of R rows and C columns has R*C cells; any full scan costs O(R*C) - you can't beat that if every cell matters.
- A cell's neighbours are (r±1, c) and (r, c±1) (plus diagonals if asked). Always check bounds `0 <= r < R and 0 <= c < C`.
- **In-place** problems forbid extra O(R*C) space. The tricks: compose in-place swaps, use part of the matrix as scratch, or encode two states in one cell (old and new).

## 2. How to spot it
- "rotate", "spiral", "zero out rows and columns", "next generation", "valid board" -> matrix simulation.
- If the prompt asks for shortest path / connected regions / flooding, it is a **graph on a grid** (topic 14), not this topic.
- If rows/columns are sorted, think binary search (topic 06) - Search a 2D Matrix treats it as one long sorted array.

## 3. Paper recipe
1. Draw a 3x3 (or 4x4) example and label every cell (r, c).
2. Write where cell (r, c) must end up: clockwise rotation sends (r, c) -> (c, n-1-r).
3. Find two simple moves that compose to the same result (transpose, then reverse each row).
4. For simulations, ask: does updating a cell destroy information a later cell still needs? If yes, snapshot or encode states.
5. Test: 1x1, 1xN, Nx1, and an even-sized and an odd-sized square.

## 4. Template
*Reference solution for **Rotate Image** (`matrix/1`) - tested by `python dsa.py selftest`:*

```python
# OPTIMISED: O(n^2) time, O(1) extra space
# Idea: Matrix transform = composition of simple transforms (transpose + reverse)
def rotate(matrix):
    n = len(matrix)
    for r in range(n):
        for c in range(r + 1, n):
            matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]  # transpose
    for row in matrix:
        row.reverse()  # mirror left-right
```

Spiral traversal keeps four walls (`top, bottom, left, right`) and shrinks them after each side; the two guards before the bottom and left sides stop double-visiting when a single row or column remains.

## 5. Why in-place encoding works (Game of Life)
Each cell is stored as two bits: bit 0 = OLD state, bit 1 = NEW state.
- 0 (`00`): dead -> dead. 1 (`01`): alive -> dead.
- 2 (`10`): dead -> alive. 3 (`11`): alive -> alive.

While scanning, read a neighbour's OLD state with `value % 2` (or `& 1`) - it is unaffected by writes to bit 1. Write a cell's new state by setting bit 1 (store 2 or 3). After the full scan, `cell >>= 1` replaces every old state with its new state. Old and new coexist in the same integer, so you need no copy of the board.

## 6. Traps
- Swapping the roles of r and c (rows vs columns) in a non-square matrix.
- Rotating by writing into the same matrix you are still reading from.
- Spiral on a single row or column visiting cells twice.
- Set Matrix Zeroes: zeroing as you scan creates new zeros that look like original ones - record first, apply later.

## 7. Self-check
1. Derive the clockwise rotation target of (r, c) from a 3x3 example.
2. Why can the first row and column double as marker storage in Set Matrix Zeroes, and what extra two booleans are needed?
3. Index of the 3x3 box that contains cell (r, c) in Sudoku?

## 8. Practice ladder
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `matrix/8` | Easy | Transpose Matrix | [#867](https://leetcode.com/problems/transpose-matrix/) | Swap the roles of row and column index |
| `matrix/9` | Easy | Matrix Diagonal Sum | [#1572](https://leetcode.com/problems/matrix-diagonal-sum/) | Index arithmetic: visit only the diagonal cells |
| `matrix/10` | Easy | Toeplitz Matrix | [#766](https://leetcode.com/problems/toeplitz-matrix/) | Local neighbour check instead of whole-line scans |
| `matrix/11` | Easy | Flipping an Image | [#832](https://leetcode.com/problems/flipping-an-image/) | Fuse two passes into one with two pointers |
| `matrix/12` | Easy | Cells with Odd Values in a Matrix | [#1252](https://leetcode.com/problems/cells-with-odd-values-in-a-matrix/) | Track parities instead of simulating |
| `matrix/13` | Easy | Special Positions in a Binary Matrix | [#1582](https://leetcode.com/problems/special-positions-in-a-binary-matrix/) | Precompute row and column aggregates |
| `matrix/16` | Easy | Shift 2D Grid | [#1260](https://leetcode.com/problems/shift-2d-grid/) | Flatten the grid, use index arithmetic |
| `matrix/18` | Easy | Count Negative Numbers in a Sorted Matrix | [#1351](https://leetcode.com/problems/count-negative-numbers-in-a-sorted-matrix/) | Staircase walk on a doubly-sorted matrix |
| `matrix/19` | Easy | Lucky Numbers in a Matrix | [#1380](https://leetcode.com/problems/lucky-numbers-in-a-matrix/) | Precompute row minima and column maxima |
| `matrix/25` | Easy | Reshape the Matrix | [#566](https://leetcode.com/problems/reshape-the-matrix/) | Flat index <-> (row, column) conversion with // and % |
| `matrix/27` | Easy | Projection Area of 3D Shapes | [#883](https://leetcode.com/problems/projection-area-of-3d-shapes/) | Three independent projections: count, row max, column max |
| `matrix/28` | Easy | Surface Area of 3D Shapes | [#892](https://leetcode.com/problems/surface-area-of-3d-shapes/) | Sum of independent towers minus hidden shared faces |
| `matrix/30` | Easy | Find Winner on a Tic Tac Toe Game | [#1275](https://leetcode.com/problems/find-winner-on-a-tic-tac-toe-game/) | Per-line counters instead of rescanning the grid |
| `matrix/34` | Easy | Determine Whether Matrix Can Be Obtained By Rotation | [#1886](https://leetcode.com/problems/determine-whether-matrix-can-be-obtained-by-rotation/) | Try all 4 rotations |
| `matrix/36` | Easy | Check if Every Row and Column Contains All Numbers | [#2133](https://leetcode.com/problems/check-if-every-row-and-column-contains-all-numbers/) | Distinct-count check per row and column |
| `matrix/38` | Easy | Largest Local Values in a Matrix | [#2373](https://leetcode.com/problems/largest-local-values-in-a-matrix/) | Separable sliding-window maximum (rows, then columns) |
| `matrix/39` | Easy | Matrix Similarity After Cyclic Shifts | [#2946](https://leetcode.com/problems/matrix-similarity-after-cyclic-shifts/) | Cyclic shift equals identity iff the row is periodic with that shift |
| `matrix/40` | Easy | Find Missing and Repeated Values | [#2965](https://leetcode.com/problems/find-missing-and-repeated-values/) | Sum arithmetic with a set (no sorting, no counting dictionary) |
| `matrix/42` | Easy | Range Addition II | [#598](https://leetcode.com/problems/range-addition-ii/) | Intersection of rectangles that share a corner |
| `matrix/43` | Easy | Image Smoother | [#661](https://leetcode.com/problems/image-smoother/) | 2D prefix sums for window totals |
| `matrix/50` | Easy | Convert 1D Array Into 2D Array | [#2022](https://leetcode.com/problems/convert-1d-array-into-2d-array/) | Row-major index arithmetic (cell k -> row k // n, column k % n) |
| `matrix/53` | Easy | Delete Greatest Value in Each Row | [#2500](https://leetcode.com/problems/delete-greatest-value-in-each-row/) | Sort rows, then take column-wise maxima |
| `matrix/57` | Easy | Check if Grid Satisfies Conditions | [#3142](https://leetcode.com/problems/check-if-grid-satisfies-conditions/) | Collapse a local rule into a global invariant (constant columns) |
| `matrix/61` | Easy | Snake in Matrix | [#3248](https://leetcode.com/problems/snake-in-matrix/) | Simulate with coordinates; map back with row * n + col |
| `matrix/1` | Medium | Rotate Image | [#48](https://leetcode.com/problems/rotate-image/) | Matrix transform = composition of simple transforms (transpose + reverse) |
| `matrix/2` | Medium | Spiral Matrix | [#54](https://leetcode.com/problems/spiral-matrix/) | Boundary shrinking simulation |
| `matrix/3` | Medium | Set Matrix Zeroes | [#73](https://leetcode.com/problems/set-matrix-zeroes/) | Two-pass marking (use the input as its own bookkeeping) |
| `matrix/4` | Medium | Game of Life | [#289](https://leetcode.com/problems/game-of-life/) | Simulation with simultaneous update (copy, or encode old+new state in the cell) |
| `matrix/5` | Medium | Valid Sudoku | [#36](https://leetcode.com/problems/valid-sudoku/) | Hash sets keyed by row / column / box (index arithmetic) |
| `matrix/6` | Medium | Search a 2D Matrix II | [#240](https://leetcode.com/problems/search-a-2d-matrix-ii/) | Staircase search from the top-right corner |
| `matrix/7` | Medium | Spiral Matrix II | [#59](https://leetcode.com/problems/spiral-matrix-ii/) | Shrinking boundaries (layer by layer) |
| `matrix/14` | Medium | Diagonal Traverse | [#498](https://leetcode.com/problems/diagonal-traverse/) | Simulation with direction flips (or group by i + j) |
| `matrix/15` | Medium | Score After Flipping Matrix | [#861](https://leetcode.com/problems/score-after-flipping-matrix/) | Greedy by bit significance |
| `matrix/17` | Medium | Count Square Submatrices with All Ones | [#1277](https://leetcode.com/problems/count-square-submatrices-with-all-ones/) | 2D DP: largest square ending at each cell |
| `matrix/20` | Medium | Count Submatrices With All Ones | [#1504](https://leetcode.com/problems/count-submatrices-with-all-ones/) | Histogram heights + expand left with a running minimum |
| `matrix/21` | Medium | Largest 1-Bordered Square | [#1139](https://leetcode.com/problems/largest-1-bordered-square/) | Precomputed run lengths, check borders in O(1) |
| `matrix/22` | Medium | Minimum Swaps to Arrange a Binary Grid | [#1536](https://leetcode.com/problems/minimum-swaps-to-arrange-a-binary-grid/) | Greedy bubble-up using trailing-zero counts |
| `matrix/23` | Medium | First Completely Painted Row or Column | [#2661](https://leetcode.com/problems/first-completely-painted-row-or-column/) | Position map + per-row/column counters |
| `matrix/24` | Medium | Difference Between Ones and Zeros in Row and Column | [#2482](https://leetcode.com/problems/difference-between-ones-and-zeros-in-row-and-column/) | Precompute row and column counts |
| `matrix/26` | Medium | Image Overlap | [#835](https://leetcode.com/problems/image-overlap/) | Count translation vectors between pairs of points |
| `matrix/29` | Medium | As Far from Land as Possible | [#1162](https://leetcode.com/problems/as-far-from-land-as-possible/) | Multi-source BFS (distance to nearest source) |
| `matrix/31` | Medium | Sort the Matrix Diagonally | [#1329](https://leetcode.com/problems/sort-the-matrix-diagonally/) | Group by i - j (diagonal id), sort, write back |
| `matrix/32` | Medium | Where Will the Ball Fall | [#1706](https://leetcode.com/problems/where-will-the-ball-fall/) | Row-by-row simulation with a stuck check |
| `matrix/33` | Medium | Rotating the Box | [#1861](https://leetcode.com/problems/rotating-the-box/) | Two-pointer gravity per row, then rotate by index mapping |
| `matrix/35` | Medium | Find All Groups of Farmland | [#1992](https://leetcode.com/problems/find-all-groups-of-farmland/) | Find rectangle corners by scanning (no flood fill needed) |
| `matrix/37` | Medium | Count Unguarded Cells in the Grid | [#2257](https://leetcode.com/problems/count-unguarded-cells-in-the-grid/) | Four directional sweeps with a 'visible' flag |
| `matrix/41` | Medium | Sum of Matrix After Queries | [#2718](https://leetcode.com/problems/sum-of-matrix-after-queries/) | Process in reverse: the last write wins |
| `matrix/44` | Medium | Max Increase to Keep City Skyline | [#807](https://leetcode.com/problems/max-increase-to-keep-city-skyline/) | Precompute row/column maxima, then a per-cell bound |
| `matrix/45` | Medium | Magic Squares In Grid | [#840](https://leetcode.com/problems/magic-squares-in-grid/) | Prune with a mathematical invariant, then verify the window |
| `matrix/46` | Medium | Spiral Matrix III | [#885](https://leetcode.com/problems/spiral-matrix-iii/) | Spiral walk with growing leg lengths; filter by bounds |
| `matrix/47` | Medium | Diagonal Traverse II | [#1424](https://leetcode.com/problems/diagonal-traverse-ii/) | Group by diagonal index i + j |
| `matrix/49` | Medium | Cyclically Rotating a Grid | [#1914](https://leetcode.com/problems/cyclically-rotating-a-grid/) | Flatten each ring into a list, rotate by k mod length, write back |
| `matrix/51` | Medium | Minimum Cost Homecoming of a Robot in a Grid | [#2087](https://leetcode.com/problems/minimum-cost-homecoming-of-a-robot-in-a-grid/) | Costs depend only on the entered line - the Manhattan path is optimal |
| `matrix/52` | Medium | Count Artifacts That Can Be Extracted | [#2201](https://leetcode.com/problems/count-artifacts-that-can-be-extracted/) | Hash set membership instead of an n x n board |
| `matrix/54` | Medium | Check Knight Tour Configuration | [#2596](https://leetcode.com/problems/check-knight-tour-configuration/) | Invert the grid into step -> position, then validate neighbours in the sequence |
| `matrix/55` | Medium | Difference of Number of Distinct Values on Diagonals | [#2711](https://leetcode.com/problems/difference-of-number-of-distinct-values-on-diagonals/) | Prefix / suffix distinct counts along each diagonal |
| `matrix/56` | Medium | Construct Product Matrix | [#2906](https://leetcode.com/problems/construct-product-matrix/) | Prefix * suffix products (product of array except self) under a modulus |
| `matrix/58` | Medium | Maximum Difference Score in a Grid | [#3148](https://leetcode.com/problems/maximum-difference-score-in-a-grid/) | Telescoping sum, then a 2D running minimum DP |
| `matrix/59` | Medium | Find the Minimum Area to Cover All Ones I | [#3195](https://leetcode.com/problems/find-the-minimum-area-to-cover-all-ones-i/) | Bounding box of the points |
| `matrix/60` | Medium | Count Submatrices With Equal Frequency of X and Y | [#3212](https://leetcode.com/problems/count-submatrices-with-equal-frequency-of-x-and-y/) | 2D prefix counts anchored at the origin |
| `matrix/48` | Hard | Cherry Pickup II | [#1463](https://leetcode.com/problems/cherry-pickup-ii/) | DP over rows with the pair of column positions as state |

Start one with `python dsa.py start matrix/1`.

**More:** 59 Spiral Matrix II (M), 867 Transpose Matrix (E), 74 Search a 2D Matrix (M), 240 Search a 2D Matrix II (M), 498 Diagonal Traverse (M), 566 Reshape the Matrix (E), 1051 Height Checker (E).

## 9. Make it stay - the teacher's anchors

**Picture it.** A rubber-stamp: rotating a picture 90 degrees equals flipping it along a diagonal and then mirroring it - two easy moves instead of one confusing one.

**The rule in one sentence.** Treat a matrix as coordinates (r, c). Compose simple transforms (transpose, reverse rows), shrink boundaries (spiral), or reuse the matrix as its own scratch space (first row/column markers).

**Why it works.** Most matrix problems are index arithmetic in disguise; once you write where (r, c) ends up, the code is mechanical.

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. Where does cell (r, c) go in a clockwise rotation?
2. Why do the guards `top <= bottom` and `left <= right` appear in Spiral Matrix?
3. Why can't Game of Life update cells in place without encoding?

**Mistakes students make most.**
- Updating cells in an order that corrupts values you still need.
- Row/column swapped (r, c vs x, y).
- Forgetting the single row / single column case.

**When NOT to use it.** You need path-finding or connectivity - that is a graph on a grid (BFS/DFS), see the graphs topic.

**The same idea in disguise.** Rotate -> spiral -> set zeroes -> game of life -> valid sudoku -> search a 2D matrix (binary search on a virtual 1-D index).
