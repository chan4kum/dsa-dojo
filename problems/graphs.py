"""Graphs problems - the problem bank for the "graphs" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
Optional keys: compare (how to compare answers), adapt_in/adapt_out (convert lists <-> linked lists / trees),
check (validate any correct answer), inplace (which argument is mutated).
"""

PROBLEMS = [
    # ---- Number of Islands (LeetCode 200) ----
    dict(
        title="Number of Islands",
        diff="M",
        lc=200,
        slug="number-of-islands",
        prompt=(
            "A grid of '1' (land) and '0' (water). Count the islands: groups of land cells connected horizontally "
            "or vertically."
        ),
        sig="def num_islands(grid: List[List[str]]) -> int:",
        fn="num_islands",
        tests=[
            (([["1", "1", "0"], ["1", "0", "0"], ["0", "0", "1"]],), 2),
            (([["1"]],), 1),
            (([["0"]],), 0),
            (([["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]],), 5),
            (([["1", "1"], ["1", "1"]],), 1),
        ],
        hints=[
            "Think of each land cell as a graph node with up to 4 neighbours. Islands = connected components.",
            "Scan every cell; when you meet unvisited land, that is a NEW island - count it.",
            "Then flood-fill (DFS/BFS) from it, marking all connected land visited so it is not counted again.",
        ],
        pattern="Graph traversal on a grid: count connected components with DFS/BFS flood fill",
        explain=(
            "Each flood fill consumes exactly one component, so the number of fills started equals the number "
            "of\n        islands. Mark cells visited when pushing (not when popping) to avoid duplicates. Iterative "
            "stack here\n        avoids recursion-depth limits on big grids. O(R*C)."
        ),
        cx="O(R*C) time",
        brute_cx="O(R*C) but recursive (deep recursion on big grids)",
        brute=r"""
# BRUTE FORCE: O(R*C) but recursive (deep recursion on big grids)
def num_islands(grid):
    g = [row[:] for row in grid]
    R, C = len(g), len(g[0])

    def sink(r, c):
        if 0 <= r < R and 0 <= c < C and g[r][c] == "1":
            g[r][c] = "0"
            sink(r + 1, c)
            sink(r - 1, c)
            sink(r, c + 1)
            sink(r, c - 1)

    n = 0

    for r in range(R):
        for c in range(C):
            if g[r][c] == "1":
                n += 1
                sink(r, c)

    return n
""",
        solution=r"""
# OPTIMISED: O(R*C) time
# Idea: Graph traversal on a grid: count connected components with DFS/BFS flood fill
def num_islands(grid):
    R, C = len(grid), len(grid[0])
    seen = [[False] * C for _ in range(R)]
    count = 0

    for r in range(R):
        for c in range(C):
            if grid[r][c] == "1" and not seen[r][c]:
                count += 1
                seen[r][c] = True
                stack = [(r, c)]

                while stack:
                    x, y = stack.pop()
                    for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                        if 0 <= nx < R and 0 <= ny < C and grid[nx][ny] == "1" and not seen[nx][ny]:
                            seen[nx][ny] = True
                            stack.append((nx, ny))

    return count
""",
    ),
    # ---- Rotting Oranges (LeetCode 994) ----
    dict(
        title="Rotting Oranges",
        diff="M",
        lc=994,
        slug="rotting-oranges",
        prompt=(
            "Grid cells: 0 empty, 1 fresh orange, 2 rotten orange. Every minute, fresh oranges adjacent "
            "(4-directionally) to a rotten one become rotten. Return the minutes until none are fresh, or -1 if "
            "impossible."
        ),
        sig="def oranges_rotting(grid: List[List[int]]) -> int:",
        fn="oranges_rotting",
        tests=[
            (([[2, 1, 1], [1, 1, 0], [0, 1, 1]],), 4),
            (([[2, 1, 1], [0, 1, 1], [1, 0, 1]],), -1),
            (([[0, 2]],), 0),
            (([[0]],), 0),
            (([[1]],), -1),
            (([[2, 2], [1, 1], [0, 0], [2, 0]],), 1),
        ],
        hints=[
            "All rotten oranges spread at the same time - this is not a single-source search.",
            "Put ALL initially rotten oranges in the queue at once (multi-source BFS). Each BFS layer = one minute.",
            "Count fresh oranges; decrement as they rot. If any fresh remain when the queue empties, return -1.",
        ],
        pattern="Multi-source BFS (level = time)",
        explain=(
            "BFS explores by distance from the source set; seeding with all rotten cells makes distance =\n        "
            "'minutes until it rots'. Layer-by-layer processing gives the total minutes. O(R*C)."
        ),
        cx="O(R*C) time (multi-source BFS)",
        brute_cx="O((R*C)^2) - rescans the whole grid every minute",
        brute=r"""
# BRUTE FORCE: O((R*C)^2) - rescans the whole grid every minute
def oranges_rotting(grid):
    g = [row[:] for row in grid]
    R, C = len(g), len(g[0])
    minutes = 0

    while True:
        to_rot = [
            (r, c)
            for r in range(R)
            for c in range(C)
            if g[r][c] == 1
            and any(
                0 <= r + dr < R and 0 <= c + dc < C and g[r + dr][c + dc] == 2
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
            )
        ]

        if not to_rot:
            break

        for r, c in to_rot:
            g[r][c] = 2

        minutes += 1

    return -1 if any(1 in row for row in g) else minutes
""",
        solution=r"""
# OPTIMISED: O(R*C) time (multi-source BFS)
# Idea: Multi-source BFS (level = time)
def oranges_rotting(grid):
    R, C = len(grid), len(grid[0])
    g = [row[:] for row in grid]
    q, fresh = deque(), 0

    for r in range(R):
        for c in range(C):
            if g[r][c] == 2:
                q.append((r, c))
            elif g[r][c] == 1:
                fresh += 1

    minutes = 0

    while q and fresh:
        for _ in range(len(q)):  # one minute
            x, y = q.popleft()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < R and 0 <= ny < C and g[nx][ny] == 1:
                    g[nx][ny] = 2
                    fresh -= 1
                    q.append((nx, ny))

        minutes += 1

    return minutes if fresh == 0 else -1
""",
    ),
    # ---- Course Schedule (LeetCode 207) ----
    dict(
        title="Course Schedule",
        diff="M",
        lc=207,
        slug="course-schedule",
        prompt=(
            "There are n courses (0..n-1). Each pair [a, b] means you must take b before a. Can you finish all "
            "courses? (i.e., the prerequisite graph has no cycle)"
        ),
        sig="def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:",
        fn="can_finish",
        tests=[
            ((2, [[1, 0]]), True),
            ((2, [[1, 0], [0, 1]]), False),
            ((1, []), True),
            ((4, [[1, 0], [2, 1], [3, 2]]), True),
            ((3, [[0, 1], [1, 2], [2, 0]]), False),
            ((3, []), True),
        ],
        hints=[
            "Model courses as nodes and 'b before a' as an edge b -> a. You need an order that respects every edge.",
            "A course with no remaining prerequisites (in-degree 0) can be taken now. Taking it frees its dependents.",
            (
                "Kahn's algorithm: queue of in-degree-0 nodes; pop, decrement neighbours' in-degree; if you "
                "processed all n nodes there is no cycle."
            ),
        ],
        pattern="Topological sort (Kahn's BFS) / cycle detection in a directed graph",
        explain=(
            "Repeatedly remove nodes with no incoming edges. If the graph is a DAG you will remove all of them; "
            "a\n        cycle leaves nodes whose in-degree never reaches 0. O(V + E). Record the pop order and you "
            "also have a\n        valid course order (Course Schedule II)."
        ),
        cx="O(V + E) time (Kahn / DFS colours)",
        brute_cx="O(V * (V+E)) - search for a cycle from every node",
        brute=r"""
# BRUTE FORCE: O(V * (V+E)) - search for a cycle from every node
def can_finish(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]

    for a, b in prerequisites:
        adj[b].append(a)

    def reaches_itself(start):
        stack, seen = list(adj[start]), set()

        while stack:
            u = stack.pop()
            if u == start:
                return True
            if u not in seen:
                seen.add(u)
                stack.extend(adj[u])

        return False

    return not any(reaches_itself(i) for i in range(num_courses))
""",
        solution=r"""
# OPTIMISED: O(V + E) time (Kahn / DFS colours)
# Idea: Topological sort (Kahn's BFS) / cycle detection in a directed graph
def can_finish(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    indeg = [0] * num_courses

    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1

    q = deque(i for i in range(num_courses) if indeg[i] == 0)
    done = 0

    while q:
        u = q.popleft()
        done += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)

    return done == num_courses
""",
    ),
    # ---- Redundant Connection (LeetCode 684) ----
    dict(
        title="Redundant Connection",
        diff="M",
        lc=684,
        slug="redundant-connection",
        prompt=(
            "A tree with n nodes (1..n) had one extra edge added, creating exactly one cycle. Given the edge list, "
            "return an edge that can be removed to restore a tree (if several, the one appearing last in the input)."
        ),
        sig="def find_redundant_connection(edges: List[List[int]]) -> List[int]:",
        fn="find_redundant_connection",
        tests=[
            (([[1, 2], [1, 3], [2, 3]],), [2, 3]),
            (([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],), [1, 4]),
            (([[1, 2], [2, 3], [1, 3]],), [1, 3]),
            (([[1, 2], [1, 2]],), [1, 2]),
        ],
        hints=[
            "The extra edge is the first one that connects two nodes that are ALREADY connected.",
            "You need 'are u and v in the same component?' and 'merge components' quickly.",
            "Union-Find (DSU): for each edge, if find(u) == find(v) return it; else union.",
        ],
        pattern="Union-Find (disjoint set union) for dynamic connectivity",
        explain=(
            "DSU maintains components under unions with near-O(1) amortised find (path compression) and union "
            "(by\n        size). Processing edges in order, the first edge whose endpoints already share a root "
            "closes a cycle.\n        Use DSU when edges arrive incrementally and you only ask about connectivity."
        ),
        cx="O(E * alpha(V)) time (union-find)",
        brute_cx="O(E * (V+E)) - one traversal per edge",
        brute=r"""
# BRUTE FORCE: O(E * (V+E)) - one traversal per edge
def find_redundant_connection(edges):
    adj = {}

    for u, v in edges:
        seen, stack = set(), [u]

        while stack:  # is v already reachable from u?
            x = stack.pop()
            if x == v:
                return [u, v]
            if x not in seen:
                seen.add(x)
                stack.extend(adj.get(x, []))

        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)

    return []
""",
        solution=r"""
# OPTIMISED: O(E * alpha(V)) time (union-find)
# Idea: Union-Find (disjoint set union) for dynamic connectivity
def find_redundant_connection(edges):
    parent = list(range(len(edges) + 1))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path compression (halving)
            x = parent[x]
        return x

    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return [u, v]
        parent[ru] = rv

    return []
""",
    ),
    # ---- Network Delay Time (LeetCode 743) ----
    dict(
        title="Network Delay Time",
        diff="M",
        lc=743,
        slug="network-delay-time",
        prompt=(
            "Directed weighted edges [u, v, w] mean a signal takes w time from u to v. A signal starts at node k. "
            "Return the time until all n nodes (1..n) have received it, or -1 if some never do."
        ),
        sig="def network_delay_time(times: List[List[int]], n: int, k: int) -> int:",
        fn="network_delay_time",
        tests=[
            (([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2), 2),
            (([[1, 2, 1]], 2, 1), 1),
            (([[1, 2, 1]], 2, 2), -1),
            (([[1, 2, 1], [2, 3, 2], [1, 3, 4]], 3, 1), 3),
            (([[1, 2, 1], [2, 1, 3]], 2, 1), 1),
        ],
        hints=[
            "You need the shortest time from k to EVERY node; the answer is the largest of those.",
            "Edges have non-negative weights - which classic shortest-path algorithm fits?",
            "Dijkstra with a min-heap of (dist, node); skip stale heap entries; if any node is unreached return -1.",
        ],
        pattern="Dijkstra's algorithm (single-source shortest paths, non-negative weights)",
        explain=(
            "Greedy: the closest unsettled node's distance is final (no cheaper route can arrive via a "
            "farther\n        node because weights are >= 0). A heap makes 'closest unsettled node' O(log V). Total "
            "O(E log V).\n        Negative weights -> Bellman-Ford; unweighted -> plain BFS."
        ),
        cx="O(E log V) time (Dijkstra with a heap)",
        brute_cx="O(V * E) - Bellman-Ford; Dijkstra's heap makes it O(E log V)",
        brute=r"""
# BRUTE FORCE: O(V * E) - Bellman-Ford; Dijkstra's heap makes it O(E log V)
def network_delay_time(times, n, k):
    dist = {i: float("inf") for i in range(1, n + 1)}
    dist[k] = 0

    for _ in range(n - 1):  # Bellman-Ford relaxation rounds
        for u, v, w in times:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    m = max(dist.values())

    return -1 if m == float("inf") else m
""",
        solution=r"""
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
""",
    ),
    # ---- Word Ladder (LeetCode 127) ----
    dict(
        title="Word Ladder",
        diff="H",
        lc=127,
        slug="word-ladder",
        prompt=(
            "Transform begin_word into end_word, changing one letter at a time, where every intermediate word must "
            "be in the word list. Return the number of words in the shortest sequence (including both ends), or 0."
        ),
        sig="def ladder_length(begin_word: str, end_word: str, word_list: List[str]) -> int:",
        fn="ladder_length",
        tests=[
            (("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]), 5),
            (("hit", "cog", ["hot", "dot", "dog", "lot", "log"]), 0),
            (("a", "c", ["a", "b", "c"]), 2),
            (("hot", "dog", ["hot", "dog"]), 0),
            (("lost", "cost", ["most", "fist", "lost", "cost", "fish"]), 2),
        ],
        hints=[
            "Words are nodes; two words are adjacent if they differ by exactly one letter. You want a SHORTEST path.",
            "Edges are unweighted -> BFS.",
            (
                "Generate neighbours by replacing each position with a-z and checking membership in a set (O(L*26) "
                "per word); mark visited."
            ),
        ],
        pattern="BFS on an implicit graph (shortest path, unweighted)",
        explain=(
            "The graph is never built explicitly: neighbours are generated on demand. BFS reaches the target in "
            "the\n        minimum number of steps. Optimisation: bidirectional BFS, or wildcard-bucket adjacency "
            "('h*t').\n        Time O(N * L * 26)."
        ),
        cx="O(N * L^2) time (generate neighbours by wildcard patterns)",
        brute_cx="O(N^2 * L) - tests every word pair instead of generating neighbours",
        brute=r"""
# BRUTE FORCE: O(N^2 * L) - tests every word pair instead of generating neighbours
def ladder_length(begin_word, end_word, word_list):
    words = set(word_list)

    if end_word not in words:
        return 0

    def adjacent(a, b):
        return sum(x != y for x, y in zip(a, b)) == 1

    q, seen = deque([(begin_word, 1)]), {begin_word}

    while q:
        w, d = q.popleft()
        if w == end_word:
            return d
        for other in words:  # compare with EVERY word
            if other not in seen and adjacent(w, other):
                seen.add(other)
                q.append((other, d + 1))

    return 0
""",
        solution=r"""
# OPTIMISED: O(N * L^2) time (generate neighbours by wildcard patterns)
# Idea: BFS on an implicit graph (shortest path, unweighted)
def ladder_length(begin_word, end_word, word_list):
    words = set(word_list)

    if end_word not in words:
        return 0

    q = deque([(begin_word, 1)])
    seen = {begin_word}

    while q:
        w, d = q.popleft()

        if w == end_word:
            return d

        for i in range(len(w)):
            for ch in "abcdefghijklmnopqrstuvwxyz":
                nw = w[:i] + ch + w[i + 1 :]
                if nw in words and nw not in seen:
                    seen.add(nw)
                    q.append((nw, d + 1))

    return 0
""",
    ),
]
