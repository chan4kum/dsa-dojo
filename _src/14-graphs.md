# 14 - Graphs (BFS, DFS, topological sort, union-find, shortest paths)

> **One idea:** model the problem as nodes + edges, then pick the traversal that matches the question.

## 1. First principles
- Representation: adjacency list `adj[u] = [v, ...]` (sparse, usual) or a grid where the neighbours are the 4 (or 8) surrounding cells. Implicit graphs (words differing by one letter, game states) are never built - neighbours are generated on demand.
- Always keep a **visited** set. For BFS (and DFS), mark a node visited **when you push it**, not when you pop it. **Dijkstra is the exception:** a node's distance is final only when it is *popped* (a cheaper path may still be queued), so skip stale pops instead.
- **Which tool?**
  | Question | Tool | Cost |
  |---|---|---|
  | connected components, flood fill, reachability | DFS or BFS | O(V+E) |
  | shortest path, **unweighted** (fewest steps) | **BFS** (level = distance); multi-source BFS starts with many sources | O(V+E) |
  | shortest path, **non-negative weights** | **Dijkstra** (min-heap) | O((V+E) log V) |
  | shortest path with negative edges / at most k edges | Bellman-Ford | O(VE) |
  | ordering with dependencies, detect a cycle in a directed graph | **Topological sort** (Kahn: in-degrees) | O(V+E) |
  | "are these connected?" while edges arrive, count components, cycle in an undirected graph | **Union-Find (DSU)** | ~O(alpha(n)) per op |
  | cheapest way to connect everything | MST (Kruskal with DSU / Prim with heap) | O(E log E) |
  | two-colouring, odd cycle | BFS/DFS colouring (bipartite check) | O(V+E) |

## 2. How to spot it
- Grid with islands/regions/rooms/oranges/mazes.
- "prerequisites", "dependencies", "order of tasks", "alien dictionary".
- "network", "cities and roads", "friends", "word transformations", "connected".
- State-space puzzles (locks, sliding puzzle): nodes = states, edges = moves.

## 3. Paper recipe
1. Say what the **nodes** are and what an **edge** is. (If you cannot, you do not have a graph problem.)
2. Directed or undirected? Weighted? Cyclic? Connected? Sparse?
3. Decide the question type with the table above -> pick the algorithm.
4. Write the visited rule (when is a node "done"?).
5. For grids: write `dirs = [(1,0),(-1,0),(0,1),(0,-1)]` and the bounds check.
6. Hand-run it on a 4-5 node graph and write the queue/stack/heap contents at each step (see the traces).

## 4. Hand traces
Multi-source BFS (time = BFS level):

{{trace:bfs_grid}}

Topological sort (Kahn):

{{trace:kahn}}

Union-Find:

{{trace:dsu}}

Dijkstra:

{{trace:dijkstra}}

## 5. Templates
{{solution:graphs/5}}

The other skeletons: `graphs/1` iterative DFS flood fill, `graphs/2` BFS with a level loop, `graphs/3` Kahn's topological sort, `graphs/4` union-find, `graphs/6` BFS on an implicit graph.

## 6. Traps
- Marking visited on pop in BFS -> the same node enters the queue many times (for Dijkstra, finalising on pop is correct, but it fails with negative edges: use Bellman-Ford).
- Using DFS to find a shortest path in an unweighted graph (use BFS).
- Dijkstra with negative edges (wrong), or without skipping stale heap entries (slow).
- Forgetting disconnected components: loop over **all** start nodes.
- Recursion depth on big grids -> prefer an explicit stack/queue.
- Directed vs undirected edges when building `adj`.

## 7. Self-check
1. Why does BFS give shortest paths in unweighted graphs, but not in weighted ones?
2. How does Kahn's algorithm detect a cycle?
3. What does *path compression* do to the cost of `find`?
4. Which algorithm for "cheapest flight with at most k stops", and why not plain Dijkstra?

## 8. Practice ladder
{{ladder}}

**More:** 733 Flood Fill (E), 695 Max Area of Island (M), 133 Clone Graph (M), 417 Pacific Atlantic Water Flow (M), 130 Surrounded Regions (M), 542 01 Matrix (M), 785 Is Graph Bipartite? (M), 210 Course Schedule II (M), 547 Number of Provinces (M), 721 Accounts Merge (M), 787 Cheapest Flights Within K Stops (M), 1631 Path With Minimum Effort (M), 1584 Min Cost to Connect All Points (M), 310 Minimum Height Trees (M), 269 Alien Dictionary (H), 332 Reconstruct Itinerary (H), 1192 Critical Connections in a Network (H).
