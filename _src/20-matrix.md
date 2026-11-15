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
{{solution:matrix/1}}

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
{{ladder}}

**More:** 59 Spiral Matrix II (M), 867 Transpose Matrix (E), 74 Search a 2D Matrix (M), 240 Search a 2D Matrix II (M), 498 Diagonal Traverse (M), 566 Reshape the Matrix (E), 1051 Height Checker (E).
