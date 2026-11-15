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
| `matrix/1` | Medium | Rotate Image | [#48](https://leetcode.com/problems/rotate-image/) | Matrix transform = composition of simple transforms (transpose + reverse) |
| `matrix/2` | Medium | Spiral Matrix | [#54](https://leetcode.com/problems/spiral-matrix/) | Boundary shrinking simulation |
| `matrix/3` | Medium | Set Matrix Zeroes | [#73](https://leetcode.com/problems/set-matrix-zeroes/) | Two-pass marking (use the input as its own bookkeeping) |
| `matrix/4` | Medium | Game of Life | [#289](https://leetcode.com/problems/game-of-life/) | Simulation with simultaneous update (copy, or encode old+new state in the cell) |
| `matrix/5` | Medium | Valid Sudoku | [#36](https://leetcode.com/problems/valid-sudoku/) | Hash sets keyed by row / column / box (index arithmetic) |
| `matrix/6` | Medium | Search a 2D Matrix II | [#240](https://leetcode.com/problems/search-a-2d-matrix-ii/) | Staircase search from the top-right corner |
| `matrix/7` | Medium | Spiral Matrix II | [#59](https://leetcode.com/problems/spiral-matrix-ii/) | Shrinking boundaries (layer by layer) |

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
