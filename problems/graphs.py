from core import *

PROBLEMS = [
    dict(
        title="Number of Islands", diff="M", lc=200, slug="number-of-islands",
        prompt="A grid of '1' (land) and '0' (water). Count the islands: groups of land cells connected "
               "horizontally or vertically.",
        sig="def num_islands(grid: List[List[str]]) -> int:",
        fn="num_islands",
        tests=[(([["1", "1", "0"], ["1", "0", "0"], ["0", "0", "1"]],), 2), (([["1"]],), 1), (([["0"]],), 0),
               (([["1", "0", "1"], ["0", "1", "0"], ["1", "0", "1"]],), 5), (([["1", "1"], ["1", "1"]],), 1)],
        hints=["Think of each land cell as a graph node with up to 4 neighbours. Islands = connected components.",
               "Scan every cell; when you meet unvisited land, that is a NEW island - count it.",
               "Then flood-fill (DFS/BFS) from it, marking all connected land visited so it is not counted again."],
        pattern="Graph traversal on a grid: count connected components with DFS/BFS flood fill",
        explain="""
        Each flood fill consumes exactly one component, so the number of fills started equals the number of
        islands. Mark cells visited when pushing (not when popping) to avoid duplicates. Iterative stack here
        avoids recursion-depth limits on big grids. O(R*C).""",
        solution=r'''
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
''',
    ),
    dict(
        title="Rotting Oranges", diff="M", lc=994, slug="rotting-oranges",
        prompt="Grid cells: 0 empty, 1 fresh orange, 2 rotten orange. Every minute, fresh oranges adjacent "
               "(4-directionally) to a rotten one become rotten. Return the minutes until none are fresh, or -1 if impossible.",
        sig="def oranges_rotting(grid: List[List[int]]) -> int:",
        fn="oranges_rotting",
        tests=[(([[2, 1, 1], [1, 1, 0], [0, 1, 1]],), 4), (([[2, 1, 1], [0, 1, 1], [1, 0, 1]],), -1), (([[0, 2]],), 0),
               (([[0]],), 0), (([[1]],), -1), (([[2, 2], [1, 1], [0, 0], [2, 0]],), 1)],
        hints=["All rotten oranges spread at the same time - this is not a single-source search.",
               "Put ALL initially rotten oranges in the queue at once (multi-source BFS). Each BFS layer = one minute.",
               "Count fresh oranges; decrement as they rot. If any fresh remain when the queue empties, return -1."],
        pattern="Multi-source BFS (level = time)",
        explain="""
        BFS explores by distance from the source set; seeding with all rotten cells makes distance =
        'minutes until it rots'. Layer-by-layer processing gives the total minutes. O(R*C).""",
        solution=r'''
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
        for _ in range(len(q)):                      # one minute
            x, y = q.popleft()
            for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                if 0 <= nx < R and 0 <= ny < C and g[nx][ny] == 1:
                    g[nx][ny] = 2
                    fresh -= 1
                    q.append((nx, ny))
        minutes += 1
    return minutes if fresh == 0 else -1
''',
    ),
    dict(
        title="Course Schedule", diff="M", lc=207, slug="course-schedule",
        prompt="There are n courses (0..n-1). Each pair [a, b] means you must take b before a. "
               "Can you finish all courses? (i.e., the prerequisite graph has no cycle)",
        sig="def can_finish(num_courses: int, prerequisites: List[List[int]]) -> bool:",
        fn="can_finish",
        tests=[((2, [[1, 0]]), True), ((2, [[1, 0], [0, 1]]), False), ((1, []), True),
               ((4, [[1, 0], [2, 1], [3, 2]]), True), ((3, [[0, 1], [1, 2], [2, 0]]), False), ((3, []), True)],
        hints=["Model courses as nodes and 'b before a' as an edge b -> a. You need an order that respects every edge.",
               "A course with no remaining prerequisites (in-degree 0) can be taken now. Taking it frees its dependents.",
               "Kahn's algorithm: queue of in-degree-0 nodes; pop, decrement neighbours' in-degree; if you processed all n nodes there is no cycle."],
        pattern="Topological sort (Kahn's BFS) / cycle detection in a directed graph",
        explain="""
        Repeatedly remove nodes with no incoming edges. If the graph is a DAG you will remove all of them; a
        cycle leaves nodes whose in-degree never reaches 0. O(V + E). Record the pop order and you also have a
        valid course order (Course Schedule II).""",
        solution=r'''
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
''',
    ),
    dict(
        title="Redundant Connection", diff="M", lc=684, slug="redundant-connection",
        prompt="A tree with n nodes (1..n) had one extra edge added, creating exactly one cycle. Given the edge list, "
               "return an edge that can be removed to restore a tree (if several, the one appearing last in the input).",
        sig="def find_redundant_connection(edges: List[List[int]]) -> List[int]:",
        fn="find_redundant_connection",
        tests=[(([[1, 2], [1, 3], [2, 3]],), [2, 3]), (([[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]],), [1, 4]),
               (([[1, 2], [2, 3], [1, 3]],), [1, 3]), (([[1, 2], [1, 2]],), [1, 2])],
        hints=["The extra edge is the first one that connects two nodes that are ALREADY connected.",
               "You need 'are u and v in the same component?' and 'merge components' quickly.",
               "Union-Find (DSU): for each edge, if find(u) == find(v) return it; else union."],
        pattern="Union-Find (disjoint set union) for dynamic connectivity",
        explain="""
        DSU maintains components under unions with near-O(1) amortised find (path compression) and union (by
        size). Processing edges in order, the first edge whose endpoints already share a root closes a cycle.
        Use DSU when edges arrive incrementally and you only ask about connectivity.""",
        solution=r'''
def find_redundant_connection(edges):
    parent = list(range(len(edges) + 1))
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]        # path compression (halving)
            x = parent[x]
        return x
    for u, v in edges:
        ru, rv = find(u), find(v)
        if ru == rv:
            return [u, v]
        parent[ru] = rv
    return []
''',
    ),
    dict(
        title="Network Delay Time", diff="M", lc=743, slug="network-delay-time",
        prompt="Directed weighted edges [u, v, w] mean a signal takes w time from u to v. A signal starts at node k. "
               "Return the time until all n nodes (1..n) have received it, or -1 if some never do.",
        sig="def network_delay_time(times: List[List[int]], n: int, k: int) -> int:",
        fn="network_delay_time",
        tests=[(([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2), 2), (([[1, 2, 1]], 2, 1), 1), (([[1, 2, 1]], 2, 2), -1),
               (([[1, 2, 1], [2, 3, 2], [1, 3, 4]], 3, 1), 3), (([[1, 2, 1], [2, 1, 3]], 2, 1), 1)],
        hints=["You need the shortest time from k to EVERY node; the answer is the largest of those.",
               "Edges have non-negative weights - which classic shortest-path algorithm fits?",
               "Dijkstra with a min-heap of (dist, node); skip stale heap entries; if any node is unreached return -1."],
        pattern="Dijkstra's algorithm (single-source shortest paths, non-negative weights)",
        explain="""
        Greedy: the closest unsettled node's distance is final (no cheaper route can arrive via a farther
        node because weights are >= 0). A heap makes 'closest unsettled node' O(log V). Total O(E log V).
        Negative weights -> Bellman-Ford; unweighted -> plain BFS.""",
        solution=r'''
def network_delay_time(times, n, k):
    adj = defaultdict(list)
    for u, v, w in times:
        adj[u].append((v, w))
    dist = {}
    heap = [(0, k)]
    while heap:
        d, u = heapq.heappop(heap)
        if u in dist:
            continue                         # stale entry
        dist[u] = d
        for v, w in adj[u]:
            if v not in dist:
                heapq.heappush(heap, (d + w, v))
    return max(dist.values()) if len(dist) == n else -1
''',
    ),
    dict(
        title="Word Ladder", diff="H", lc=127, slug="word-ladder",
        prompt="Transform begin_word into end_word, changing one letter at a time, where every intermediate word "
               "must be in the word list. Return the number of words in the shortest sequence (including both ends), or 0.",
        sig="def ladder_length(begin_word: str, end_word: str, word_list: List[str]) -> int:",
        fn="ladder_length",
        tests=[(("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]), 5), (("hit", "cog", ["hot", "dot", "dog", "lot", "log"]), 0),
               (("a", "c", ["a", "b", "c"]), 2), (("hot", "dog", ["hot", "dog"]), 0), (("lost", "cost", ["most", "fist", "lost", "cost", "fish"]), 2)],
        hints=["Words are nodes; two words are adjacent if they differ by exactly one letter. You want a SHORTEST path.",
               "Edges are unweighted -> BFS.",
               "Generate neighbours by replacing each position with a-z and checking membership in a set (O(L*26) per word); mark visited."],
        pattern="BFS on an implicit graph (shortest path, unweighted)",
        explain="""
        The graph is never built explicitly: neighbours are generated on demand. BFS reaches the target in the
        minimum number of steps. Optimisation: bidirectional BFS, or wildcard-bucket adjacency ('h*t').
        Time O(N * L * 26).""",
        solution=r'''
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
                nw = w[:i] + ch + w[i + 1:]
                if nw in words and nw not in seen:
                    seen.add(nw)
                    q.append((nw, d + 1))
    return 0
''',
    ),
]
