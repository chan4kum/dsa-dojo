# 14 - Graphs (BFS, DFS, topological sort, union-find, shortest paths)

> **One idea:** model the problem as nodes + edges, then pick the traversal that matches the question.

## 1. First principles
- Representation: adjacency list `adj[u] = [v, ...]` (sparse, usual) or a grid where the neighbours are the 4 (or 8) surrounding cells. Implicit graphs (words differing by one letter, game states) are never built - neighbours are generated on demand.
- Always keep a **visited** set; mark visited **when you push**, not when you pop.
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

`.` empty, `1` fresh, `2` rotten - each row of the grid shown side by side

```text
minute 0:   211  11.  .11   fresh=6
minute 1:   221  21.  .11   fresh=4
minute 2:   222  22.  .11   fresh=2
minute 3:   222  22.  .21   fresh=1
minute 4:   222  22.  .22   fresh=0
```

Answer: **4** minutes.

Topological sort (Kahn):

Edges (b -> a): 0->1, 0->2, 1->3, 2->3

| step | order so far | in-degree [0..3] | queue |
|---|---|---|---|
| start | - | [0, 1, 1, 2] | [0] |
| pop 0 | [0] | [0, 0, 0, 2] | [1, 2] |
| pop 1 | [0, 1] | [0, 0, 0, 1] | [2] |
| pop 2 | [0, 1, 2] | [0, 0, 0, 0] | [3] |
| pop 3 | [0, 1, 2, 3] | [0, 0, 0, 0] | [] |

All 4 nodes processed -> no cycle; a valid order is `[0, 1, 2, 3]`.

Union-Find:

Nodes 1..5 start as their own parent.

| edge | roots | result | parent[1..5] |
|---|---|---|---|
| [1, 2] | find(1)=1, find(2)=2 | union: parent[1] = 2 | [2, 2, 3, 4, 5] |
| [2, 3] | find(2)=2, find(3)=3 | union: parent[2] = 3 | [2, 3, 3, 4, 5] |
| [4, 5] | find(4)=4, find(5)=5 | union: parent[4] = 5 | [2, 3, 3, 5, 5] |
| [3, 1] | find(3)=3 == find(1)=3 | SAME component -> this edge closes a cycle | [3, 3, 3, 5, 5] |

Dijkstra:

Edges: 1->2 (1), 1->3 (4), 2->3 (2), 2->4 (6), 3->4 (3); source 1

| heap pop (dist, node) | action | pushed |
|---|---|---|
| (0, 1) | settle 1 at 0 | (1, 2), (4, 3) |
| (1, 2) | settle 2 at 1 | (3, 3), (7, 4) |
| (3, 3) | settle 3 at 3 | (6, 4) |
| (4, 3) | stale -> skip | - |
| (6, 4) | settle 4 at 6 | - |
| (7, 4) | stale -> skip | - |

Final distances: `{1: 0, 2: 1, 3: 3, 4: 6}`

## 5. Templates
*Reference solution for **Network Delay Time** (`graphs/5`) - tested by `python dsa.py selftest`:*

```python
# OPTIMISED: O(E log V) time (Dijkstra with a heap)
# Idea: Dijkstra's algorithm (single-source shortest paths, non-negative weights)
def network_delay_time(times, n, k):
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))
    dist = {}
    heap = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in dist:
            continue  # stale entry
        dist[u] = d
        for v, w in adj[u]:
            if v not in dist:
                heapq.heappush(heap, (d + w, v))
    return max(dist.values()) if len(dist) == n else -1
```

The other skeletons: `graphs/1` iterative DFS flood fill, `graphs/2` BFS with a level loop, `graphs/3` Kahn's topological sort, `graphs/4` union-find, `graphs/6` BFS on an implicit graph.

## 6. Traps
- Marking visited on pop -> the same node enters the queue many times.
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
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `graphs/20` | Easy | Island Perimeter | [#463](https://leetcode.com/problems/island-perimeter/) | Local counting on a grid (4 - 2*shared edges) |
| `graphs/21` | Easy | Flood Fill | [#733](https://leetcode.com/problems/flood-fill/) | Grid DFS/BFS (connected region), mutate-as-visited |
| `graphs/23` | Easy | Find the Town Judge | [#997](https://leetcode.com/problems/find-the-town-judge/) | Degree counting on a directed graph |
| `graphs/26` | Easy | Find if Path Exists in Graph | [#1971](https://leetcode.com/problems/find-if-path-exists-in-graph/) | Connectivity: BFS/DFS or Union-Find |
| `graphs/1` | Medium | Number of Islands | [#200](https://leetcode.com/problems/number-of-islands/) | Graph traversal on a grid: count connected components with DFS/BFS flood fill |
| `graphs/2` | Medium | Rotting Oranges | [#994](https://leetcode.com/problems/rotting-oranges/) | Multi-source BFS (level = time) |
| `graphs/3` | Medium | Course Schedule | [#207](https://leetcode.com/problems/course-schedule/) | Topological sort (Kahn's BFS) / cycle detection in a directed graph |
| `graphs/4` | Medium | Redundant Connection | [#684](https://leetcode.com/problems/redundant-connection/) | Union-Find (disjoint set union) for dynamic connectivity |
| `graphs/5` | Medium | Network Delay Time | [#743](https://leetcode.com/problems/network-delay-time/) | Dijkstra's algorithm (single-source shortest paths, non-negative weights) |
| `graphs/7` | Medium | Number of Provinces | [#547](https://leetcode.com/problems/number-of-provinces/) | Connected components (DFS/BFS or Union-Find) |
| `graphs/8` | Medium | Max Area of Island | [#695](https://leetcode.com/problems/max-area-of-island/) | Grid DFS returning component size (flood fill) |
| `graphs/9` | Medium | Pacific Atlantic Water Flow | [#417](https://leetcode.com/problems/pacific-atlantic-water-flow/) | Reverse the direction + multi-source search from the borders |
| `graphs/10` | Medium | Surrounded Regions | [#130](https://leetcode.com/problems/surrounded-regions/) | Invert the question: mark what is safe from the border, then flip the rest |
| `graphs/11` | Medium | 01 Matrix | [#542](https://leetcode.com/problems/01-matrix/) | Multi-source BFS (all sources start in the queue together) |
| `graphs/12` | Medium | Course Schedule II | [#210](https://leetcode.com/problems/course-schedule-ii/) | Topological sort (Kahn's BFS on in-degrees) |
| `graphs/13` | Medium | Number of Connected Components in an Undirected Graph | [#323](https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/) | Union-Find (disjoint set union) with path compression |
| `graphs/14` | Medium | Graph Valid Tree | [#261](https://leetcode.com/problems/graph-valid-tree/) | Tree = connected + (n-1) edges; Union-Find cycle detection |
| `graphs/15` | Medium | Cheapest Flights Within K Stops | [#787](https://leetcode.com/problems/cheapest-flights-within-k-stops/) | Bellman-Ford with a bounded number of edges (layered relaxation) |
| `graphs/16` | Medium | Keys and Rooms | [#841](https://leetcode.com/problems/keys-and-rooms/) | Reachability in a directed graph |
| `graphs/17` | Medium | Clone Graph | [#133](https://leetcode.com/problems/clone-graph/) | Graph traversal + memo dict (old -> new) to handle cycles |
| `graphs/22` | Medium | Shortest Path in Binary Matrix | [#1091](https://leetcode.com/problems/shortest-path-in-binary-matrix/) | BFS on a grid (unweighted shortest path) |
| `graphs/24` | Medium | Min Cost to Connect All Points | [#1584](https://leetcode.com/problems/min-cost-to-connect-all-points/) | Minimum spanning tree (Kruskal + Union-Find / Prim) |
| `graphs/25` | Medium | Find Eventual Safe States | [#802](https://leetcode.com/problems/find-eventual-safe-states/) | Cycle detection with DFS colors / reverse topological order |
| `graphs/27` | Medium | All Paths From Source to Target | [#797](https://leetcode.com/problems/all-paths-from-source-to-target/) | DFS backtracking on a DAG |
| `graphs/28` | Medium | Is Graph Bipartite? | [#785](https://leetcode.com/problems/is-graph-bipartite/) | Graph 2-colouring with BFS (an odd cycle makes it impossible) |
| `graphs/29` | Medium | Evaluate Division | [#399](https://leetcode.com/problems/evaluate-division/) | Weighted graph / weighted Union-Find |
| `graphs/30` | Medium | Most Stones Removed with Same Row or Column | [#947](https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/) | Union-Find where rows and columns are the nodes |
| `graphs/31` | Medium | Satisfiability of Equality Equations | [#990](https://leetcode.com/problems/satisfiability-of-equality-equations/) | Union-Find: merge equalities first, then verify inequalities |
| `graphs/32` | Medium | Path With Minimum Effort | [#1631](https://leetcode.com/problems/path-with-minimum-effort/) | Dijkstra with a minimax cost (max instead of sum) |
| `graphs/33` | Medium | Find the City With the Smallest Number of Neighbors at a Threshold Distance | [#1334](https://leetcode.com/problems/find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance/) | All-pairs shortest paths (Floyd-Warshall) |
| `graphs/34` | Medium | Path with Maximum Probability | [#1514](https://leetcode.com/problems/path-with-maximum-probability/) | Dijkstra with a max-heap on products |
| `graphs/35` | Medium | Minimum Height Trees | [#310](https://leetcode.com/problems/minimum-height-trees/) | Topological-style leaf trimming to find the tree centre |
| `graphs/36` | Medium | Shortest Bridge | [#934](https://leetcode.com/problems/shortest-bridge/) | Flood fill one island, then multi-source BFS to the other |
| `graphs/37` | Medium | Smallest String With Swaps | [#1202](https://leetcode.com/problems/smallest-string-with-swaps/) | Union-Find groups + sort within each group |
| `graphs/38` | Medium | Number of Operations to Make Network Connected | [#1319](https://leetcode.com/problems/number-of-operations-to-make-network-connected/) | Count components; cable count is the feasibility test |
| `graphs/39` | Medium | Possible Bipartition | [#886](https://leetcode.com/problems/possible-bipartition/) | Graph 2-colouring (bipartite check) |
| `graphs/40` | Medium | Course Schedule IV | [#1462](https://leetcode.com/problems/course-schedule-iv/) | Transitive closure (Floyd-Warshall on booleans) |
| `graphs/41` | Medium | Time Needed to Inform All Employees | [#1376](https://leetcode.com/problems/time-needed-to-inform-all-employees/) | Longest root-to-node path sum in a tree |
| `graphs/42` | Medium | Reorder Routes to Make All Paths Lead to the City Zero | [#1466](https://leetcode.com/problems/reorder-routes-to-make-all-paths-lead-to-the-city-zero/) | Traverse an undirected tree, remembering the original direction |
| `graphs/43` | Medium | Number of Enclaves | [#1020](https://leetcode.com/problems/number-of-enclaves/) | Flood fill from the boundary inwards |
| `graphs/6` | Hard | Word Ladder | [#127](https://leetcode.com/problems/word-ladder/) | BFS on an implicit graph (shortest path, unweighted) |
| `graphs/18` | Hard | Alien Dictionary | [#269](https://leetcode.com/problems/alien-dictionary/) | Derive a graph from the data, then topological sort |
| `graphs/19` | Hard | Word Search II | [#212](https://leetcode.com/problems/word-search-ii/) | Trie + grid DFS (search many words in one pass) |

Start one with `python dsa.py start graphs/1`.

**More:** 733 Flood Fill (E), 695 Max Area of Island (M), 133 Clone Graph (M), 417 Pacific Atlantic Water Flow (M), 130 Surrounded Regions (M), 542 01 Matrix (M), 785 Is Graph Bipartite? (M), 210 Course Schedule II (M), 547 Number of Provinces (M), 721 Accounts Merge (M), 787 Cheapest Flights Within K Stops (M), 1631 Path With Minimum Effort (M), 1584 Min Cost to Connect All Points (M), 310 Minimum Height Trees (M), 269 Alien Dictionary (H), 332 Reconstruct Itinerary (H), 1192 Critical Connections in a Network (H).

## 9. Make it stay - the teacher's anchors

**Picture it.** A city map: BFS is a ripple spreading outward (shortest in hops); DFS is a hiker following one road to its end before backing up.

**The rule in one sentence.** Name the nodes and the edges first. Then pick BFS (shortest unweighted), DFS (reachability/components/cycle), Kahn (ordering), Dijkstra (weighted), Union-Find (merging groups).

**Why it works.** Marking nodes visited when they ENTER the queue/stack guarantees each node and edge is processed once: O(V+E).

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. What are the nodes and edges in Word Ladder?
2. Why does BFS give shortest paths only when edges have equal weight?
3. How does Kahn's algorithm detect a cycle?

**Mistakes students make most.**
- Marking visited too late (duplicates in the queue).
- Using DFS recursion on huge grids (stack overflow) without noting it.
- Treating a grid as a graph but forgetting bounds checks.

**When NOT to use it.** Negative edge weights (Dijkstra fails - Bellman-Ford) or when the structure is actually a tree (simpler recursion).

**The same idea in disguise.** Islands -> rotting oranges (multi-source BFS) -> 01 matrix -> course schedule (topological) -> redundant connection (union-find) -> network delay (Dijkstra) -> word ladder -> alien dictionary (graph built from data).
