"""more Graph problems (batch 6) - part of the problem bank for the "graphs" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Swim in Rising Water (LeetCode 778) ----
    dict(
        title="Swim in Rising Water",
        diff="H",
        lc=778,
        slug="swim-in-rising-water",
        prompt=(
            "grid is n x n and holds each value 0..n*n-1 exactly once: grid[i][j] is the elevation of the cell. At "
            "time t the water depth is t everywhere, and you can swim between two 4-adjacent cells only if BOTH "
            "have elevation <= t (you can swim any distance instantly). Starting at the top-left cell at time 0, "
            "return the least time at which you can reach the bottom-right cell."
        ),
        sig="def swim_in_water(grid: List[List[int]]) -> int:",
        fn="swim_in_water",
        tests=[
            (([[0, 2], [1, 3]],), 3),
            (
                ([[0, 1, 2, 3, 4], [24, 23, 22, 21, 5], [12, 13, 14, 15, 16], [11, 17, 18, 19, 20], [10, 9, 8, 7, 6]],),
                16,
            ),
            (([[0]],), 0),
            (([[0, 1], [2, 3]],), 3),
        ],
        hints=[
            "The answer is the smallest possible 'highest cell on the path' over all paths from corner to corner.",
            (
                "Brute force: try t = 0, 1, 2, ... and check with a flood fill whether the target is reachable "
                "using cells <= t."
            ),
            (
                "Better: run Dijkstra, but a path's cost is the MAXIMUM elevation seen instead of the sum - always "
                "expand the cheapest frontier cell from a min-heap."
            ),
        ],
        pattern="Minimax path: Dijkstra with max instead of sum",
        explain=(
            "We want the path whose worst (highest) cell is as low as possible. Dijkstra's greedy argument still "
            "works when the path cost is max(cost so far, next cell): the cheapest frontier cell can never be "
            "improved later. The first time the bottom-right cell is popped from the heap its cost is the answer. "
            "The brute force raises t one by one and flood-fills."
        ),
        cx="O(n^2 log n) time, O(n^2) space",
        brute_cx="O(n^4) time - a flood fill for every possible water level",
        brute=r"""
# BRUTE FORCE: O(n^4) time - a flood fill for every possible water level
def swim_in_water(grid):
    n = len(grid)
    for t in range(n * n):
        if grid[0][0] > t:
            continue
        seen = {(0, 0)}
        stack = [(0, 0)]
        while stack:
            r, c = stack.pop()
            if (r, c) == (n - 1, n - 1):
                return t
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen and grid[nr][nc] <= t:
                    seen.add((nr, nc))
                    stack.append((nr, nc))
""",
        solution=r"""
# OPTIMISED: O(n^2 log n) time, O(n^2) space
# Idea: Minimax path: Dijkstra with max instead of sum
def swim_in_water(grid):
    n = len(grid)
    heap = [(grid[0][0], 0, 0)]
    seen = {(0, 0)}
    while heap:
        t, r, c = heapq.heappop(heap)
        if (r, c) == (n - 1, n - 1):
            return t
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
                seen.add((nr, nc))
                heapq.heappush(heap, (max(t, grid[nr][nc]), nr, nc))
""",
    ),
    # ---- Regions Cut By Slashes (LeetCode 959) ----
    dict(
        title="Regions Cut By Slashes",
        diff="M",
        lc=959,
        slug="regions-cut-by-slashes",
        prompt=(
            "An n x n grid is made of 1 x 1 squares; each square contains '/', '\\' or a space (so a slash splits "
            "it into two triangles). The strings in grid are the rows. Return the number of regions the slashes cut "
            "the grid into."
        ),
        sig="def regions_by_slashes(grid: List[str]) -> int:",
        fn="regions_by_slashes",
        tests=[
            (([" /", "/ "],), 2),
            (([" /", "  "],), 1),
            ((["/\\", "\\/"],), 5),
            (([" "],), 1),
        ],
        hints=[
            "Think of each square as four triangles: top, right, bottom, left.",
            (
                "A '/' joins top with left and right with bottom; a '\\' joins top with right and left with bottom; "
                "a space joins all four. Neighbouring squares share a side, so join those triangles too."
            ),
            (
                "The answer is the number of connected groups of triangles - use union-find (or flood fill on a 3x "
                "upscaled picture)."
            ),
        ],
        pattern="Union-find on sub-cell pieces",
        explain=(
            "Cutting a square with a slash only matters inside that square, so each square is modelled by its four "
            "triangles and the slash decides which triangles are already one piece. Adjacent squares connect "
            "through the touching triangles. Counting the groups gives the regions. The brute force draws the "
            "picture on a 3x larger grid (each slash becomes a diagonal wall) and flood-fills the empty cells."
        ),
        cx="O(n^2 α) time, O(n^2) space",
        brute_cx="O(n^2) time - flood fill on a grid 3 times larger",
        brute=r"""
# BRUTE FORCE: O(n^2) time - flood fill on a grid 3 times larger
def regions_by_slashes(grid):
    n = len(grid)
    size = 3 * n
    wall = [[False] * size for _ in range(size)]
    for i in range(n):
        for j in range(n):
            ch = grid[i][j]
            for k in range(3):
                if ch == "/":
                    wall[3 * i + k][3 * j + 2 - k] = True
                elif ch == "\\":
                    wall[3 * i + k][3 * j + k] = True
    seen = [[False] * size for _ in range(size)]
    regions = 0
    for r in range(size):
        for c in range(size):
            if wall[r][c] or seen[r][c]:
                continue
            regions += 1
            seen[r][c] = True
            stack = [(r, c)]
            while stack:
                x, y = stack.pop()
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < size and 0 <= ny < size and not wall[nx][ny] and not seen[nx][ny]:
                        seen[nx][ny] = True
                        stack.append((nx, ny))
    return regions
""",
        solution=r"""
# OPTIMISED: O(n^2 α) time, O(n^2) space
# Idea: Union-find on sub-cell pieces
def regions_by_slashes(grid):
    n = len(grid)
    parent = list(range(4 * n * n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        parent[find(a)] = find(b)

    for i in range(n):
        for j in range(n):
            base = 4 * (i * n + j)
            ch = grid[i][j]
            if ch == "/":
                union(base, base + 3)
                union(base + 1, base + 2)
            elif ch == "\\":
                union(base, base + 1)
                union(base + 2, base + 3)
            else:
                union(base, base + 1)
                union(base + 1, base + 2)
                union(base + 2, base + 3)
            if i + 1 < n:
                union(base + 2, 4 * ((i + 1) * n + j))
            if j + 1 < n:
                union(base + 1, 4 * (i * n + j + 1) + 3)
    return len({find(x) for x in range(4 * n * n)})
""",
    ),
    # ---- Shortest Path with Alternating Colors (LeetCode 1129) ----
    dict(
        title="Shortest Path with Alternating Colors",
        diff="M",
        lc=1129,
        slug="shortest-path-with-alternating-colors",
        prompt=(
            "A directed graph on nodes 0..n-1 has red edges and blue edges (self-loops and parallel edges are "
            "allowed). For every node, return the length of the shortest path from node 0 whose edge colours "
            "ALTERNATE (red, blue, red, ... or blue, red, ...), or -1 if there is none."
        ),
        sig=(
            "def shortest_alternating_paths(n: int, red_edges: List[List[int]], blue_edges: List[List[int]]) -> "
            "List[int]:"
        ),
        fn="shortest_alternating_paths",
        tests=[
            ((3, [[0, 1], [1, 2]], []), [0, 1, -1]),
            ((3, [[0, 1]], [[2, 1]]), [0, 1, -1]),
            ((3, [[0, 1]], [[1, 2]]), [0, 1, 2]),
            ((2, [], []), [0, -1]),
        ],
        hints=[
            (
                "Reaching node v after a red edge is a different situation from reaching it after a blue edge - the "
                "next edge you may use differs."
            ),
            (
                "So make the state (node, colour of the last edge) and run BFS over states; the start state may "
                "continue with either colour."
            ),
            "The answer for a node is the smaller BFS distance of its two states (or -1 if neither was reached).",
        ],
        pattern="BFS on an expanded state graph (node, last colour)",
        explain=(
            "The rule 'colours alternate' is a constraint on the previous edge, so it is hidden state. Putting the "
            "last colour into the node turns it into an ordinary unweighted shortest-path problem on 2n states, "
            "which BFS solves. The brute force relaxes edges Bellman-Ford style until no distance improves."
        ),
        cx="O(n + E) time, O(n + E) space",
        brute_cx="O(n * E) time - repeat edge relaxations until nothing changes",
        brute=r"""
# BRUTE FORCE: O(n * E) time - repeat edge relaxations until nothing changes
def shortest_alternating_paths(n, red_edges, blue_edges):
    inf = float("inf")
    dist = [[inf, inf] for _ in range(n)]
    dist[0] = [0, 0]
    changed = True
    while changed:
        changed = False
        for u, v in red_edges:
            if dist[u][1] + 1 < dist[v][0]:
                dist[v][0] = dist[u][1] + 1
                changed = True
        for u, v in blue_edges:
            if dist[u][0] + 1 < dist[v][1]:
                dist[v][1] = dist[u][0] + 1
                changed = True
    return [min(d) if min(d) < inf else -1 for d in dist]
""",
        solution=r"""
# OPTIMISED: O(n + E) time, O(n + E) space
# Idea: BFS on an expanded state graph (node, last colour)
def shortest_alternating_paths(n, red_edges, blue_edges):
    graph = [defaultdict(list), defaultdict(list)]
    for u, v in red_edges:
        graph[0][u].append(v)
    for u, v in blue_edges:
        graph[1][u].append(v)
    answer = [-1] * n
    seen = {(0, 0), (0, 1)}
    queue = deque([(0, 0, 0), (0, 1, 0)])
    while queue:
        node, color, dist = queue.popleft()
        if answer[node] == -1:
            answer[node] = dist
        nxt = 1 - color
        for v in graph[nxt][node]:
            if (v, nxt) not in seen:
                seen.add((v, nxt))
                queue.append((v, nxt, dist + 1))
    return answer
""",
    ),
    # ---- Minimum Number of Vertices to Reach All Nodes (LeetCode 1557) ----
    dict(
        title="Minimum Number of Vertices to Reach All Nodes",
        diff="M",
        lc=1557,
        slug="minimum-number-of-vertices-to-reach-all-nodes",
        prompt=(
            "A directed ACYCLIC graph has n nodes (0..n-1) and the given directed edges. Return the smallest set of "
            "nodes from which every node is reachable (the answer set is unique; any order is accepted)."
        ),
        sig="def find_smallest_set_of_vertices(n: int, edges: List[List[int]]) -> List[int]:",
        fn="find_smallest_set_of_vertices",
        compare="unordered",
        tests=[
            ((6, [[0, 1], [0, 2], [2, 5], [3, 4], [4, 2]]), [0, 3]),
            ((5, [[0, 1], [2, 1], [3, 1], [1, 4], [2, 4]]), [0, 2, 3]),
            ((1, []), [0]),
            ((3, [[0, 1], [1, 2]]), [0]),
        ],
        hints=[
            "A node with an incoming edge can be reached from another node.",
            "A node with NO incoming edge cannot be reached from anywhere else, so it must be in the set.",
            (
                "In a DAG those source nodes are enough: every other node is reachable from some source. Return the "
                "nodes with in-degree 0."
            ),
        ],
        pattern="In-degree zero = sources of a DAG",
        explain=(
            "Every node with in-degree 0 has to be chosen itself because nobody can reach it. Conversely, follow "
            "incoming edges backwards from any node: since there are no cycles the walk must end, and it can only "
            "end at a node with in-degree 0, so all nodes are covered by the sources. The brute force checks, for "
            "each node, whether any other node can reach it with a DFS."
        ),
        cx="O(n + E) time, O(n) space",
        brute_cx="O(n * (n + E)) time - a DFS from every node for every node",
        brute=r"""
# BRUTE FORCE: O(n * (n + E)) time - a DFS from every node for every node
def find_smallest_set_of_vertices(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)

    def reaches(start, target):
        seen = {start}
        stack = [start]
        while stack:
            node = stack.pop()
            for nxt in graph[node]:
                if nxt == target:
                    return True
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        return False

    return [v for v in range(n) if not any(reaches(u, v) for u in range(n) if u != v)]
""",
        solution=r"""
# OPTIMISED: O(n + E) time, O(n) space
# Idea: In-degree zero = sources of a DAG
def find_smallest_set_of_vertices(n, edges):
    has_incoming = [False] * n
    for _, v in edges:
        has_incoming[v] = True
    return [v for v in range(n) if not has_incoming[v]]
""",
    ),
    # ---- Number of Restricted Paths From First to Last Node (LeetCode 1786) ----
    dict(
        title="Number of Restricted Paths From First to Last Node",
        diff="M",
        lc=1786,
        slug="number-of-restricted-paths-from-first-to-last-node",
        prompt=(
            "A connected undirected weighted graph has nodes 1..n; edges[i] = [u, v, w]. Let dist(x) be the "
            "shortest distance from x to node n. A restricted path from node 1 to node n is a path z0 = 1, z1, ..., "
            "zk = n of edges in which dist(z_i) > dist(z_{i+1}) for every i. Return the number of restricted paths "
            "modulo 10^9 + 7."
        ),
        sig="def count_restricted_paths(n: int, edges: List[List[int]]) -> int:",
        fn="count_restricted_paths",
        tests=[
            ((5, [[1, 2, 3], [1, 3, 3], [2, 3, 1], [1, 4, 2], [5, 2, 2], [3, 5, 1], [5, 4, 10]]), 3),
            ((7, [[1, 3, 1], [4, 1, 2], [7, 3, 4], [2, 5, 3], [5, 6, 1], [6, 7, 2], [7, 5, 3], [2, 6, 4]]), 1),
            ((2, [[1, 2, 5]]), 1),
            ((3, [[1, 2, 1], [2, 3, 1], [1, 3, 2]]), 2),
        ],
        hints=[
            "First get dist(x) for every x with Dijkstra started from node n.",
            (
                "A restricted path only ever steps to a node with a strictly smaller dist, so there are no cycles "
                "to worry about."
            ),
            (
                "Let ways(u) = number of restricted paths from u to n. Process nodes in increasing dist order: "
                "ways(n) = 1 and ways(u) = sum of ways(v) over neighbours v with dist(v) < dist(u)."
            ),
        ],
        pattern="Dijkstra distances + DP in increasing distance order",
        explain=(
            "Strictly decreasing distance means every step goes 'downhill' towards n, so the graph of allowed steps "
            "is a DAG ordered by dist. Counting paths in a DAG is a DP over that order: each node adds up the "
            "counts of its downhill neighbours. The brute force computes all distances with Floyd-Warshall and "
            "counts paths with a plain recursion that has no memoisation."
        ),
        cx="O(E log n) time, O(n + E) space",
        brute_cx="exponential in the worst case - Floyd-Warshall plus an unmemoised path count",
        brute=r"""
# BRUTE FORCE: exponential in the worst case - Floyd-Warshall plus an unmemoised path count
def count_restricted_paths(n, edges):
    inf = float("inf")
    d = [[inf] * (n + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        d[i][i] = 0
    graph = defaultdict(list)
    for u, v, w in edges:
        d[u][v] = d[v][u] = min(d[u][v], w)
        graph[u].append(v)
        graph[v].append(u)
    for k in range(1, n + 1):
        for i in range(1, n + 1):
            for j in range(1, n + 1):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]

    def count(u):
        if u == n:
            return 1
        return sum(count(v) for v in graph[u] if d[v][n] < d[u][n])

    return count(1) % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(E log n) time, O(n + E) space
# Idea: Dijkstra distances + DP in increasing distance order
def count_restricted_paths(n, edges):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    dist = [float("inf")] * (n + 1)
    dist[n] = 0
    heap = [(0, n)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                heapq.heappush(heap, (dist[v], v))
    ways = [0] * (n + 1)
    ways[n] = 1
    for u in sorted(range(1, n + 1), key=lambda x: dist[x]):
        for v, _ in graph[u]:
            if dist[v] < dist[u]:
                ways[u] += ways[v]
    return ways[1] % (10**9 + 7)
""",
    ),
    # ---- Find All People With Secret (LeetCode 2092) ----
    dict(
        title="Find All People With Secret",
        diff="H",
        lc=2092,
        slug="find-all-people-with-secret",
        prompt=(
            "People 0..n-1. Person 0 knows a secret and shares it with firstPerson at time 0. meetings[i] = [x, y, "
            "time] means x and y meet at that time; whoever knows the secret at that moment tells the other, and "
            "the secret spreads instantly among everyone connected through meetings at the SAME time. Return every "
            "person who knows the secret at the end (any order)."
        ),
        sig="def find_all_people(n: int, meetings: List[List[int]], first_person: int) -> List[int]:",
        fn="find_all_people",
        compare="unordered",
        tests=[
            ((6, [[1, 2, 5], [2, 3, 8], [1, 5, 10]], 1), [0, 1, 2, 3, 5]),
            ((4, [[3, 1, 3], [1, 2, 2], [0, 3, 3]], 3), [0, 1, 3]),
            ((5, [[3, 4, 2], [1, 2, 1], [2, 3, 1]], 1), [0, 1, 2, 3, 4]),
            ((3, [], 2), [0, 2]),
        ],
        hints=[
            "Process the meetings in order of time, one time-group at a time.",
            (
                "Within one time, the secret spreads freely between everyone connected by that time's meetings - a "
                "connectivity problem (union-find or BFS)."
            ),
            (
                "After a group, people who still did not get the secret must be 'forgotten' as connected - unlink "
                "them, because a meeting at an earlier time cannot help at a later time."
            ),
        ],
        pattern="Time-ordered union-find with rollback of useless unions",
        explain=(
            "Meetings at the same time form groups in which the secret spreads to everyone if any member knows it, "
            "so union-find answers 'is this person connected to the knowers'. A union made at time t is only valid "
            "for time t, so people who did not end up connected to a knower have their link reset before the next "
            "time. The brute force simulates each time slice by repeatedly passing the secret along that slice's "
            "meetings until nothing changes."
        ),
        cx="O(M log M) time (sorting meetings), O(n + M) space",
        brute_cx="O(M * (M + n)) time - repeat passes within each time slice",
        brute=r"""
# BRUTE FORCE: O(M * (M + n)) time - repeat passes within each time slice
def find_all_people(n, meetings, first_person):
    knows = {0, first_person}
    by_time = defaultdict(list)
    for x, y, t in meetings:
        by_time[t].append((x, y))
    for t in sorted(by_time):
        changed = True
        while changed:
            changed = False
            for x, y in by_time[t]:
                if (x in knows) != (y in knows):
                    knows.add(x)
                    knows.add(y)
                    changed = True
    return sorted(knows)
""",
        solution=r"""
# OPTIMISED: O(M log M) time (sorting meetings), O(n + M) space
# Idea: Time-ordered union-find with rollback of useless unions
def find_all_people(n, meetings, first_person):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    parent[find(first_person)] = find(0)
    ordered = sorted(meetings, key=lambda m: m[2])
    i = 0
    while i < len(ordered):
        j = i
        while j < len(ordered) and ordered[j][2] == ordered[i][2]:
            j += 1
        group = ordered[i:j]
        for x, y, _ in group:
            parent[find(x)] = find(y)
        for x, y, _ in group:
            if find(x) != find(0):
                parent[x] = x
            if find(y) != find(0):
                parent[y] = y
        i = j
    return [p for p in range(n) if find(p) == find(0)]
""",
    ),
    # ---- Detonate the Maximum Bombs (LeetCode 2101) ----
    dict(
        title="Detonate the Maximum Bombs",
        diff="M",
        lc=2101,
        slug="detonate-the-maximum-bombs",
        prompt=(
            "bombs[i] = [x, y, r]: a bomb at (x, y) with blast radius r. When a bomb explodes it detonates every "
            "bomb whose centre is inside or on its circle, and those explode too (chain reaction). You choose ONE "
            "bomb to detonate first; return the maximum number of bombs that can explode."
        ),
        sig="def maximum_detonation(bombs: List[List[int]]) -> int:",
        fn="maximum_detonation",
        tests=[
            (([[2, 1, 3], [6, 1, 4]],), 2),
            (([[1, 1, 5], [10, 10, 5]],), 1),
            (([[1, 2, 3], [2, 3, 1], [3, 4, 2], [4, 5, 3], [5, 6, 4]],), 5),
            (([[5, 5, 1]],), 1),
        ],
        hints=[
            (
                "Make a directed graph: an edge i -> j if bomb j is inside bomb i's circle (dx^2 + dy^2 <= r_i^2). "
                "It is NOT symmetric."
            ),
            "Detonating bomb s sets off exactly the bombs reachable from s.",
            (
                "Run a DFS/BFS from every bomb and keep the largest reachable count. Compare squared distances so "
                "you only use integers."
            ),
        ],
        pattern="Reachability in an implicit directed graph",
        explain=(
            "The chain reaction is reachability: if A sets off B and B sets off C, then A sets off C. Since the "
            "edges go one way only (a big bomb can reach a small one but not necessarily the other way round) we "
            "must search from every start separately. The brute force grows the exploded set until it stops "
            "growing, re-checking all pairs each time."
        ),
        cx="O(n^3) time worst case (n searches, each over up to n^2 edges), O(n^2) space",
        brute_cx="O(n^4) time - regrow the exploded set by re-checking every pair",
        brute=r"""
# BRUTE FORCE: O(n^4) time - regrow the exploded set by re-checking every pair
def maximum_detonation(bombs):
    n = len(bombs)
    best = 0
    for start in range(n):
        exploded = {start}
        changed = True
        while changed:
            changed = False
            for i in list(exploded):
                xi, yi, ri = bombs[i]
                for j in range(n):
                    if j not in exploded:
                        dx, dy = xi - bombs[j][0], yi - bombs[j][1]
                        if dx * dx + dy * dy <= ri * ri:
                            exploded.add(j)
                            changed = True
        best = max(best, len(exploded))
    return best
""",
        solution=r"""
# OPTIMISED: O(n^3) time worst case (n searches, each over up to n^2 edges), O(n^2) space
# Idea: Reachability in an implicit directed graph
def maximum_detonation(bombs):
    n = len(bombs)
    graph = [[] for _ in range(n)]
    for i in range(n):
        xi, yi, ri = bombs[i]
        for j in range(n):
            if i != j:
                dx, dy = xi - bombs[j][0], yi - bombs[j][1]
                if dx * dx + dy * dy <= ri * ri:
                    graph[i].append(j)
    best = 0
    for start in range(n):
        seen = {start}
        stack = [start]
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        best = max(best, len(seen))
    return best
""",
    ),
    # ---- Count Unreachable Pairs of Nodes in an Undirected Graph (LeetCode 2316) ----
    dict(
        title="Count Unreachable Pairs of Nodes in an Undirected Graph",
        diff="M",
        lc=2316,
        slug="count-unreachable-pairs-of-nodes-in-an-undirected-graph",
        prompt=(
            "An undirected graph has n nodes (0..n-1) and the given edges. Return the number of pairs of different "
            "nodes that are NOT connected by any path."
        ),
        sig="def count_pairs_unreachable(n: int, edges: List[List[int]]) -> int:",
        fn="count_pairs_unreachable",
        tests=[
            ((3, [[0, 1], [0, 2], [1, 2]]), 0),
            ((7, [[0, 2], [0, 5], [2, 4], [1, 6], [5, 4]]), 14),
            ((2, []), 1),
            ((4, []), 6),
        ],
        hints=[
            "Two nodes are connected exactly when they belong to the same connected component.",
            "So an unreachable pair is a pair of nodes from different components.",
            (
                "Find the component sizes (union-find or DFS). Then, going through the sizes s, add s * (nodes not "
                "yet counted) - every pair is counted once."
            ),
        ],
        pattern="Connected components + counting pairs across them",
        explain=(
            "Pairs inside a component are connected, so the answer is the total number of pairs minus the connected "
            "ones - or equivalently, the pairs that choose their two endpoints from different components. Taking "
            "the components one at a time and multiplying by the number of nodes that are left counts each "
            "cross-pair exactly once. The brute force tests every pair with its own DFS."
        ),
        cx="O(n + E) time, O(n + E) space",
        brute_cx="O(n^2 * (n + E)) time - a fresh DFS for every pair of nodes",
        brute=r"""
# BRUTE FORCE: O(n^2 * (n + E)) time - a fresh DFS for every pair of nodes
def count_pairs_unreachable(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    def connected(a, b):
        seen = {a}
        stack = [a]
        while stack:
            u = stack.pop()
            if u == b:
                return True
            for v in graph[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        return False

    return sum(1 for a in range(n) for b in range(a + 1, n) if not connected(a, b))
""",
        solution=r"""
# OPTIMISED: O(n + E) time, O(n + E) space
# Idea: Connected components + counting pairs across them
def count_pairs_unreachable(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        parent[find(u)] = find(v)
    sizes = Counter(find(x) for x in range(n))
    remaining = n
    total = 0
    for size in sizes.values():
        remaining -= size
        total += size * remaining
    return total
""",
    ),
    # ---- Number of Good Paths (LeetCode 2421) ----
    dict(
        title="Number of Good Paths",
        diff="H",
        lc=2421,
        slug="number-of-good-paths",
        prompt=(
            "A tree has n nodes with values vals[i] and the given edges. A GOOD path starts and ends at nodes with "
            "the same value, and every node on it has a value no larger than that value. A single node is a good "
            "path. Paths are counted once regardless of direction. Return the number of good paths."
        ),
        sig="def number_of_good_paths(vals: List[int], edges: List[List[int]]) -> int:",
        fn="number_of_good_paths",
        tests=[
            (([1, 3, 2, 1, 3], [[0, 1], [0, 2], [2, 3], [2, 4]]), 6),
            (([1, 1, 2, 2, 3], [[0, 1], [1, 2], [2, 3], [2, 4]]), 7),
            (([1], []), 1),
            (([2, 1, 2], [[0, 1], [1, 2]]), 4),
        ],
        hints=[
            (
                "Brute force: from each node, walk only through nodes whose value is at most its own, and count the "
                "other nodes with an equal value you can reach."
            ),
            (
                "Add nodes to the structure in increasing order of value: when all nodes of value <= v are "
                "connected, the paths with maximum v live inside those components."
            ),
            (
                "Sort the edges by the larger endpoint value; union the endpoints, and when two components have the "
                "same maximum value m with a and b nodes of value m, add a * b good paths, then merge the counts."
            ),
        ],
        pattern="Offline union-find by increasing threshold (Kruskal-style)",
        explain=(
            "A good path with end value v can only use nodes of value <= v, so process edges from low to high by "
            "their larger endpoint. When an edge joins two components whose maxima are equal, every node of that "
            "maximum on one side pairs with every one on the other side, adding a * b new good paths; otherwise the "
            "component with the smaller maximum is absorbed. The brute force starts a search from every node "
            "limited to values <= its own."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2) time - a restricted search from every node",
        brute=r"""
# BRUTE FORCE: O(n^2) time - a restricted search from every node
def number_of_good_paths(vals, edges):
    n = len(vals)
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    total = 0
    for start in range(n):
        seen = {start}
        stack = [start]
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if v not in seen and vals[v] <= vals[start]:
                    seen.add(v)
                    stack.append(v)
        total += 1 + sum(1 for u in seen if u > start and vals[u] == vals[start])
    return total
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Offline union-find by increasing threshold (Kruskal-style)
def number_of_good_paths(vals, edges):
    n = len(vals)
    parent = list(range(n))
    top = list(vals)
    count = [1] * n

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = n
    for u, v in sorted(edges, key=lambda e: max(vals[e[0]], vals[e[1]])):
        ru, rv = find(u), find(v)
        if ru == rv:
            continue
        if top[ru] == top[rv]:
            total += count[ru] * count[rv]
            count[ru] += count[rv]
            parent[rv] = ru
        elif top[ru] < top[rv]:
            parent[ru] = rv
        else:
            parent[rv] = ru
    return total
""",
    ),
    # ---- Minimum Score of a Path Between Two Cities (LeetCode 2492) ----
    dict(
        title="Minimum Score of a Path Between Two Cities",
        diff="M",
        lc=2492,
        slug="minimum-score-of-a-path-between-two-cities",
        prompt=(
            "Cities 1..n and bidirectional roads [a, b, distance]. The score of a path is the MINIMUM road distance "
            "on it. A path from city 1 to city n is guaranteed to exist; a path may reuse roads and cities. Return "
            "the minimum possible score of a path from 1 to n."
        ),
        sig="def min_score(n: int, roads: List[List[int]]) -> int:",
        fn="min_score",
        tests=[
            ((4, [[1, 2, 9], [2, 3, 6], [2, 4, 5], [1, 4, 7]]), 5),
            ((4, [[1, 2, 2], [1, 3, 4], [3, 4, 7]]), 2),
            ((2, [[1, 2, 3]]), 3),
            ((5, [[1, 2, 8], [2, 5, 4], [3, 4, 1]]), 4),
        ],
        hints=[
            "Paths may repeat roads, so once you can reach a road you can walk to it, use it, and come back.",
            "Therefore every road in the connected component of city 1 can be part of some 1-to-n path.",
            (
                "Find the component of city 1 (DFS/BFS or union-find) and return the smallest road distance among "
                "its roads."
            ),
        ],
        pattern="Connected component + minimum edge",
        explain=(
            "Because walks may revisit nodes and edges, the smallest edge anywhere in the component containing city "
            "1 (which also contains city n) can always be included, and no path can use a road outside the "
            "component. So the answer is just that component's minimum edge. The brute force grows the set of "
            "reachable cities by scanning all roads repeatedly, then takes the minimum."
        ),
        cx="O(n + E) time, O(n + E) space",
        brute_cx="O(n * E) time - rescan every road until the reachable set stops growing",
        brute=r"""
# BRUTE FORCE: O(n * E) time - rescan every road until the reachable set stops growing
def min_score(n, roads):
    reach = {1}
    changed = True
    while changed:
        changed = False
        for a, b, _ in roads:
            if (a in reach) != (b in reach):
                reach.add(a)
                reach.add(b)
                changed = True
    return min(d for a, b, d in roads if a in reach)
""",
        solution=r"""
# OPTIMISED: O(n + E) time, O(n + E) space
# Idea: Connected component + minimum edge
def min_score(n, roads):
    graph = defaultdict(list)
    for a, b, d in roads:
        graph[a].append((b, d))
        graph[b].append((a, d))
    best = float("inf")
    seen = {1}
    stack = [1]
    while stack:
        u = stack.pop()
        for v, d in graph[u]:
            best = min(best, d)
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return best
""",
    ),
    # ---- Minimum Fuel Cost to Report to the Capital (LeetCode 2477) ----
    dict(
        title="Minimum Fuel Cost to Report to the Capital",
        diff="M",
        lc=2477,
        slug="minimum-fuel-cost-to-report-to-the-capital",
        prompt=(
            "The roads form a tree on cities 0..n-1 (n = len(roads) + 1) with the capital at city 0; each city has "
            "one representative who must travel to the capital. Every city has one car with `seats` seats "
            "(including the driver); representatives may share cars and swap cars at cities. Each road a car drives "
            "along costs 1 litre. Return the minimum litres of fuel."
        ),
        sig="def minimum_fuel_cost(roads: List[List[int]], seats: int) -> int:",
        fn="minimum_fuel_cost",
        tests=[
            (([[0, 1], [0, 2], [0, 3]], 5), 3),
            (([[3, 1], [3, 2], [1, 0], [0, 4], [0, 5], [4, 6]], 2), 7),
            (([], 1), 0),
            (([[0, 1], [1, 2]], 2), 2),
        ],
        hints=[
            "Look at one road at a time. Every representative below that road must cross it.",
            (
                "If s people are below a road, they need ceil(s / seats) cars to cross it, and that many litres are "
                "burnt on that road."
            ),
            (
                "So the answer is the sum over all non-root nodes of ceil(subtree_size / seats). Compute subtree "
                "sizes with one DFS from the capital."
            ),
        ],
        pattern="Tree: per-edge cost from subtree sizes",
        explain=(
            "Each road is crossed by all the representatives in the subtree below it, and packing them into full "
            "cars as early as possible costs ceil(size / seats) car-trips on that road; carpooling at the child's "
            "node can always be arranged, so the per-road costs add up independently. The brute force recomputes "
            "the subtree size from scratch for every non-root node."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - recount the subtree below every road",
        brute=r"""
# BRUTE FORCE: O(n^2) time - recount the subtree below every road
def minimum_fuel_cost(roads, seats):
    n = len(roads) + 1
    graph = defaultdict(list)
    for a, b in roads:
        graph[a].append(b)
        graph[b].append(a)
    parent = {0: None}
    order = [0]
    for u in order:
        for v in graph[u]:
            if v not in parent:
                parent[v] = u
                order.append(v)
    fuel = 0
    for node in range(1, n):
        size = 0
        stack = [node]
        while stack:
            u = stack.pop()
            size += 1
            for v in graph[u]:
                if v != parent[u]:
                    stack.append(v)
        fuel += -(-size // seats)
    return fuel
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Tree: per-edge cost from subtree sizes
def minimum_fuel_cost(roads, seats):
    n = len(roads) + 1
    graph = defaultdict(list)
    for a, b in roads:
        graph[a].append(b)
        graph[b].append(a)
    parent = {0: None}
    order = [0]
    for u in order:
        for v in graph[u]:
            if v not in parent:
                parent[v] = u
                order.append(v)
    size = [1] * n
    fuel = 0
    for u in reversed(order[1:]):
        fuel += -(-size[u] // seats)
        size[parent[u]] += size[u]
    return fuel
""",
    ),
    # ---- Maximum Star Sum of a Graph (LeetCode 2497) ----
    dict(
        title="Maximum Star Sum of a Graph",
        diff="M",
        lc=2497,
        slug="maximum-star-sum-of-a-graph",
        prompt=(
            "vals[i] is the value of node i of an undirected graph. A STAR is a centre node plus at most k of its "
            "neighbours (the edges to them); its sum is the centre value plus the chosen neighbours' values. Return "
            "the maximum star sum (a star may have only the centre)."
        ),
        sig="def max_star_sum(vals: List[int], edges: List[List[int]], k: int) -> int:",
        fn="max_star_sum",
        tests=[
            (([1, 2, 3, 4, 10, -10, -20], [[0, 1], [1, 2], [1, 3], [3, 4], [3, 5], [3, 6]], 2), 16),
            (([-5], [], 0), -5),
            (([1, -2, 3], [[0, 1], [1, 2]], 1), 3),
            (([5, 4, 3], [[0, 1], [0, 2]], 5), 12),
        ],
        hints=[
            "Try every node as the centre and decide which neighbours to take.",
            "A neighbour is worth taking only if its value is positive, and you want the largest ones.",
            (
                "For each centre: sort its neighbours' values descending, keep the positive ones among the first k, "
                "add them to the centre. The answer is the best over all centres."
            ),
        ],
        pattern="Per-node greedy: top-k positive neighbours",
        explain=(
            "Neighbour choices are independent for a given centre, so the best star takes the k largest neighbour "
            "values but never a non-positive one. Evaluating each centre costs a sort of its neighbours, so the "
            "whole thing is O(E log E). The brute force tries every subset of at most k neighbours of every centre."
        ),
        cx="O(n + E log E) time, O(n + E) space",
        brute_cx="exponential - every subset of at most k neighbours for every centre",
        brute=r"""
# BRUTE FORCE: exponential - every subset of at most k neighbours for every centre
def max_star_sum(vals, edges, k):
    neighbours = [[] for _ in vals]
    for a, b in edges:
        neighbours[a].append(vals[b])
        neighbours[b].append(vals[a])
    best = None
    for centre, around in enumerate(neighbours):
        for size in range(min(k, len(around)) + 1):
            for chosen in itertools.combinations(around, size):
                total = vals[centre] + sum(chosen)
                if best is None or total > best:
                    best = total
    return best
""",
        solution=r"""
# OPTIMISED: O(n + E log E) time, O(n + E) space
# Idea: Per-node greedy: top-k positive neighbours
def max_star_sum(vals, edges, k):
    neighbours = [[] for _ in vals]
    for a, b in edges:
        neighbours[a].append(vals[b])
        neighbours[b].append(vals[a])
    best = float("-inf")
    for centre, around in enumerate(neighbours):
        good = sorted((v for v in around if v > 0), reverse=True)[:k]
        best = max(best, vals[centre] + sum(good))
    return best
""",
    ),
    # ---- Reachable Nodes With Restrictions (LeetCode 2368) ----
    dict(
        title="Reachable Nodes With Restrictions",
        diff="M",
        lc=2368,
        slug="reachable-nodes-with-restrictions",
        prompt=(
            "An undirected tree has n nodes (0..n-1). Some nodes are restricted and may not be visited. Starting "
            "from node 0 (which is never restricted), return the maximum number of nodes you can reach, counting "
            "node 0."
        ),
        sig="def reachable_nodes(n: int, edges: List[List[int]], restricted: List[int]) -> int:",
        fn="reachable_nodes",
        tests=[
            ((7, [[0, 1], [1, 2], [3, 1], [4, 0], [0, 5], [5, 6]], [4, 5]), 4),
            ((7, [[0, 1], [0, 2], [0, 5], [0, 4], [3, 2], [6, 5]], [4, 2, 1]), 3),
            ((2, [[0, 1]], [1]), 1),
            ((3, [[0, 1], [1, 2]], []), 3),
        ],
        hints=[
            "Treat a restricted node as a wall: you may not step on it.",
            "Walk the tree from node 0 with DFS or BFS and skip restricted neighbours and nodes already seen.",
            "Put the restricted nodes in a set for O(1) checks; the answer is the number of nodes visited.",
        ],
        pattern="Graph traversal that avoids forbidden nodes",
        explain=(
            "Reachability with blocked nodes is just a normal traversal in which blocked nodes are pre-marked as "
            "seen (or skipped). Everything reached from 0 is counted. The brute force sweeps over all edges again "
            "and again, adding a node whenever one endpoint is reached and the other is allowed, until nothing "
            "changes."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n * E) time - rescan every edge until the reached set stops growing",
        brute=r"""
# BRUTE FORCE: O(n * E) time - rescan every edge until the reached set stops growing
def reachable_nodes(n, edges, restricted):
    blocked = set(restricted)
    reached = {0}
    changed = True
    while changed:
        changed = False
        for a, b in edges:
            if a in reached and b not in reached and b not in blocked:
                reached.add(b)
                changed = True
            if b in reached and a not in reached and a not in blocked:
                reached.add(a)
                changed = True
    return len(reached)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Graph traversal that avoids forbidden nodes
def reachable_nodes(n, edges, restricted):
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    seen = set(restricted)
    seen.add(0)
    stack = [0]
    count = 0
    while stack:
        u = stack.pop()
        count += 1
        for v in graph[u]:
            if v not in seen:
                seen.add(v)
                stack.append(v)
    return count
""",
    ),
    # ---- Count the Number of Complete Components (LeetCode 2685) ----
    dict(
        title="Count the Number of Complete Components",
        diff="M",
        lc=2685,
        slug="count-the-number-of-complete-components",
        prompt=(
            "An undirected graph has n nodes (0..n-1) and no repeated edges. A connected component is COMPLETE if "
            "every pair of its nodes is joined by an edge. Return the number of complete connected components."
        ),
        sig="def count_complete_components(n: int, edges: List[List[int]]) -> int:",
        fn="count_complete_components",
        tests=[
            ((6, [[0, 1], [0, 2], [1, 2], [3, 4]]), 3),
            ((6, [[0, 1], [0, 2], [1, 2], [3, 4], [3, 5]]), 1),
            ((1, []), 1),
            ((3, [[0, 1]]), 2),
        ],
        hints=[
            "Find the connected components first (union-find or DFS).",
            "A component with v nodes is complete exactly when it has v * (v - 1) / 2 edges.",
            "Count the nodes and the edges of each component and compare - no need to check pairs one by one.",
        ],
        pattern="Components + edge-count test for cliques",
        explain=(
            "A clique on v nodes has exactly v(v-1)/2 edges, and a connected component can never have more edges "
            "than that (no repeated edges), so equality means every pair is connected. Counting v and the edges per "
            "component is enough. The brute force finds each component and checks all of its node pairs in an "
            "adjacency set."
        ),
        cx="O(n + E) time, O(n + E) space",
        brute_cx="O(n^2) time - check every node pair of every component",
        brute=r"""
# BRUTE FORCE: O(n^2) time - check every node pair of every component
def count_complete_components(n, edges):
    adjacent = [set() for _ in range(n)]
    for a, b in edges:
        adjacent[a].add(b)
        adjacent[b].add(a)
    seen = set()
    total = 0
    for start in range(n):
        if start in seen:
            continue
        component = []
        stack = [start]
        seen.add(start)
        while stack:
            u = stack.pop()
            component.append(u)
            for v in adjacent[u]:
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        if all(b in adjacent[a] for a in component for b in component if a != b):
            total += 1
    return total
""",
        solution=r"""
# OPTIMISED: O(n + E) time, O(n + E) space
# Idea: Components + edge-count test for cliques
def count_complete_components(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        parent[find(a)] = find(b)
    nodes = Counter(find(x) for x in range(n))
    links = Counter(find(a) for a, _ in edges)
    return sum(1 for root, v in nodes.items() if links[root] == v * (v - 1) // 2)
""",
    ),
    # ---- Minimum Time to Visit Disappearing Nodes (LeetCode 3112) ----
    dict(
        title="Minimum Time to Visit Disappearing Nodes",
        diff="M",
        lc=3112,
        slug="minimum-time-to-visit-disappearing-nodes",
        prompt=(
            "An undirected graph has n nodes and edges [u, v, length]. Node i disappears at time disappear[i]: you "
            "can only be at a node at a time STRICTLY smaller than its disappearance time. Starting at node 0 at "
            "time 0, return for every node the minimum time to reach it, or -1 if it cannot be reached before it "
            "disappears."
        ),
        sig="def minimum_time(n: int, edges: List[List[int]], disappear: List[int]) -> List[int]:",
        fn="minimum_time",
        tests=[
            ((3, [[0, 1, 2], [1, 2, 1], [0, 2, 4]], [1, 1, 5]), [0, -1, 4]),
            ((3, [[0, 1, 2], [1, 2, 1], [0, 2, 4]], [1, 3, 5]), [0, 2, 3]),
            ((2, [[0, 1, 1]], [1, 1]), [0, -1]),
            ((1, [], [1]), [0]),
        ],
        hints=[
            "Without disappearing nodes this is a plain shortest-path problem: Dijkstra from node 0.",
            "Arriving at node v at time t is only possible if t < disappear[v].",
            (
                "In Dijkstra, when relaxing an edge to v, accept the new time only if it is smaller than the "
                "current best AND smaller than disappear[v]. Nodes never accepted stay at -1."
            ),
        ],
        pattern="Dijkstra with a deadline per node",
        explain=(
            "Waiting never helps, so the earliest arrival at each node is what matters, and a node that is reached "
            "late enough to have disappeared is simply not a usable node. Dijkstra's argument still holds because "
            "the rule 'arrival < deadline' is checked on the earliest candidate: a later arrival would fail too. "
            "The brute force relaxes all edges repeatedly (Bellman-Ford) with the same deadline check."
        ),
        cx="O((n + E) log n) time, O(n + E) space",
        brute_cx="O(n * E) time - Bellman-Ford rounds",
        brute=r"""
# BRUTE FORCE: O(n * E) time - Bellman-Ford rounds
def minimum_time(n, edges, disappear):
    inf = float("inf")
    dist = [inf] * n
    dist[0] = 0
    for _ in range(n):
        for u, v, w in edges:
            for a, b in ((u, v), (v, u)):
                if dist[a] < inf and dist[a] + w < disappear[b] and dist[a] + w < dist[b]:
                    dist[b] = dist[a] + w
    return [d if d < inf else -1 for d in dist]
""",
        solution=r"""
# OPTIMISED: O((n + E) log n) time, O(n + E) space
# Idea: Dijkstra with a deadline per node
def minimum_time(n, edges, disappear):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    dist = [float("inf")] * n
    dist[0] = 0
    heap = [(0, 0)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            nd = d + w
            if nd < dist[v] and nd < disappear[v]:
                dist[v] = nd
                heapq.heappush(heap, (nd, v))
    return [d if d < float("inf") else -1 for d in dist]
""",
    ),
    # ---- Shortest Distance After Road Addition Queries I (LeetCode 3243) ----
    dict(
        title="Shortest Distance After Road Addition Queries I",
        diff="M",
        lc=3243,
        slug="shortest-distance-after-road-addition-queries-i",
        prompt=(
            "n cities 0..n-1 with a one-way road i -> i + 1 for every i < n - 1. Each query [u, v] ADDS a one-way "
            "road u -> v (u < v - 1, and it stays for later queries). After each query, return the length of the "
            "shortest path from city 0 to city n - 1."
        ),
        sig="def shortest_distance_after_queries(n: int, queries: List[List[int]]) -> List[int]:",
        fn="shortest_distance_after_queries",
        tests=[
            ((5, [[2, 4], [0, 2], [0, 4]]), [3, 2, 1]),
            ((4, [[0, 3], [0, 2]]), [1, 1]),
            ((3, [[0, 2]]), [1]),
            ((6, [[1, 4], [0, 1]]), [3, 3]),
        ],
        hints=[
            "After each added road you need a fresh shortest path in an unweighted directed graph.",
            "Edges are unweighted, so breadth-first search from city 0 finds the answer.",
            (
                "Keep an adjacency list, append the new road for every query, then run BFS and record the distance "
                "to n - 1."
            ),
        ],
        pattern="BFS repeated after each graph update",
        explain=(
            "With unit road lengths BFS gives the shortest distance in O(n + roads). The graph only grows, and n is "
            "small in this version, so re-running BFS after each query is enough. The brute force recomputes "
            "all-pairs distances with Floyd-Warshall from scratch after every query."
        ),
        cx="O(q * (n + q)) time, O(n + q) space",
        brute_cx="O(q * n^3) time - Floyd-Warshall after every query",
        brute=r"""
# BRUTE FORCE: O(q * n^3) time - Floyd-Warshall after every query
def shortest_distance_after_queries(n, queries):
    inf = float("inf")
    roads = [(i, i + 1) for i in range(n - 1)]
    answer = []
    for u, v in queries:
        roads.append((u, v))
        d = [[inf] * n for _ in range(n)]
        for i in range(n):
            d[i][i] = 0
        for a, b in roads:
            d[a][b] = 1
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if d[i][k] + d[k][j] < d[i][j]:
                        d[i][j] = d[i][k] + d[k][j]
        answer.append(d[0][n - 1])
    return answer
""",
        solution=r"""
# OPTIMISED: O(q * (n + q)) time, O(n + q) space
# Idea: BFS repeated after each graph update
def shortest_distance_after_queries(n, queries):
    graph = [[i + 1] for i in range(n - 1)] + [[]]
    answer = []
    for u, v in queries:
        graph[u].append(v)
        dist = [-1] * n
        dist[0] = 0
        queue = deque([0])
        while queue:
            x = queue.popleft()
            for y in graph[x]:
                if dist[y] == -1:
                    dist[y] = dist[x] + 1
                    queue.append(y)
        answer.append(dist[n - 1])
    return answer
""",
    ),
    # ---- Minimum Time to Collect All Apples in a Tree (LeetCode 1443) ----
    dict(
        title="Minimum Time to Collect All Apples in a Tree",
        diff="M",
        lc=1443,
        slug="minimum-time-to-collect-all-apples-in-a-tree",
        prompt=(
            "An undirected tree has n nodes (0..n-1). hasApple[i] tells whether node i holds an apple. Starting at "
            "node 0, collect every apple and come back to node 0; walking along one edge takes 1 second. Return the "
            "minimum number of seconds."
        ),
        sig="def min_time_collect_apples(n: int, edges: List[List[int]], has_apple: List[bool]) -> int:",
        fn="min_time_collect_apples",
        tests=[
            ((7, [[0, 1], [0, 2], [1, 4], [1, 5], [2, 3], [2, 6]], [False, False, True, False, True, True, False]), 8),
            ((7, [[0, 1], [0, 2], [1, 4], [1, 5], [2, 3], [2, 6]], [False, False, True, False, False, True, False]), 6),
            ((7, [[0, 1], [0, 2], [1, 4], [1, 5], [2, 3], [2, 6]], [False] * 7), 0),
            ((2, [[0, 1]], [False, True]), 2),
        ],
        hints=[
            "An edge needs to be walked (twice - down and back) exactly when the subtree below it contains an apple.",
            "So you are looking for the nodes whose subtree contains at least one apple.",
            (
                "DFS from node 0: a node's subtree has an apple if the node itself or any child's subtree has one; "
                "each non-root such node adds 2 seconds."
            ),
        ],
        pattern="Tree DP: 'does my subtree contain a target?'",
        explain=(
            "The cheapest route visits only the edges that lead to apples, and each such edge is used once downward "
            "and once upward, costing 2. An edge leads to an apple iff the child's subtree contains one, which one "
            "postorder pass computes for all nodes. The brute force recounts the subtree below every edge on its "
            "own."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - search the subtree below every node separately",
        brute=r"""
# BRUTE FORCE: O(n^2) time - search the subtree below every node separately
def min_time_collect_apples(n, edges, has_apple):
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    parent = {0: None}
    order = [0]
    for u in order:
        for v in graph[u]:
            if v not in parent:
                parent[v] = u
                order.append(v)
    seconds = 0
    for node in range(1, n):
        found = False
        stack = [node]
        while stack and not found:
            u = stack.pop()
            if has_apple[u]:
                found = True
            for v in graph[u]:
                if v != parent[u]:
                    stack.append(v)
        if found:
            seconds += 2
    return seconds
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Tree DP: 'does my subtree contain a target?'
def min_time_collect_apples(n, edges, has_apple):
    graph = defaultdict(list)
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
    parent = {0: None}
    order = [0]
    for u in order:
        for v in graph[u]:
            if v not in parent:
                parent[v] = u
                order.append(v)
    has = list(has_apple)
    seconds = 0
    for u in reversed(order[1:]):
        if has[u]:
            seconds += 2
            has[parent[u]] = True
    return seconds
""",
    ),
    # ---- Number of Ways to Arrive at Destination (LeetCode 1976) ----
    dict(
        title="Number of Ways to Arrive at Destination",
        diff="M",
        lc=1976,
        slug="number-of-ways-to-arrive-at-destination",
        prompt=(
            "Intersections 0..n-1 joined by two-way roads [u, v, time] (positive times, at most one road per pair). "
            "Return the number of different ways to travel from 0 to n - 1 in the SHORTEST possible time, modulo "
            "10^9 + 7."
        ),
        sig="def count_paths(n: int, roads: List[List[int]]) -> int:",
        fn="count_paths",
        tests=[
            (
                (
                    7,
                    [
                        [0, 6, 7],
                        [0, 1, 2],
                        [1, 2, 3],
                        [1, 3, 3],
                        [6, 3, 3],
                        [3, 5, 1],
                        [6, 5, 1],
                        [2, 5, 1],
                        [0, 4, 5],
                        [4, 6, 2],
                    ],
                ),
                4,
            ),
            ((2, [[1, 0, 10]]), 1),
            ((3, [[0, 1, 1], [1, 2, 1], [0, 2, 2]]), 2),
            ((1, []), 1),
        ],
        hints=[
            "Dijkstra finds the shortest distance to every node; now we also need to COUNT the shortest routes.",
            (
                "Keep ways[v] = number of shortest routes to v. When you find a strictly shorter route to v, reset "
                "ways[v] to ways[u]; when you find an equally short one, add ways[u]."
            ),
            (
                "Because all times are positive, nodes are finalised in distance order, so ways[u] is complete when "
                "u is popped. Answer ways[n - 1] modulo 10^9 + 7."
            ),
        ],
        pattern="Dijkstra that also counts shortest paths",
        explain=(
            "A shortest route to v is a shortest route to some neighbour u plus the edge (u, v), so ways[v] is the "
            "sum of ways[u] over the neighbours u that realise dist[v]. Dijkstra's order guarantees that by the "
            "time u is finalised all its routes are counted. The brute force gets all distances from Floyd-Warshall "
            "and then walks every shortest path with an unmemoised recursion."
        ),
        cx="O(E log n) time, O(n + E) space",
        brute_cx="exponential in the worst case - Floyd-Warshall plus enumerating every shortest path",
        brute=r"""
# BRUTE FORCE: exponential in the worst case - Floyd-Warshall plus enumerating every shortest path
def count_paths(n, roads):
    inf = float("inf")
    d = [[inf] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    graph = defaultdict(list)
    for u, v, w in roads:
        d[u][v] = d[v][u] = min(d[u][v], w)
        graph[u].append((v, w))
        graph[v].append((u, w))
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][k] + d[k][j] < d[i][j]:
                    d[i][j] = d[i][k] + d[k][j]
    target = n - 1

    def ways(u):
        if u == target:
            return 1
        return sum(
            ways(v)
            for v, w in graph[u]
            if d[0][u] + w == d[0][v] and d[0][v] + d[v][target] == d[0][target]
        )

    return ways(0) % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(E log n) time, O(n + E) space
# Idea: Dijkstra that also counts shortest paths
def count_paths(n, roads):
    graph = defaultdict(list)
    for u, v, w in roads:
        graph[u].append((v, w))
        graph[v].append((u, w))
    dist = [float("inf")] * n
    ways = [0] * n
    dist[0], ways[0] = 0, 1
    heap = [(0, 0)]
    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue
        for v, w in graph[u]:
            if d + w < dist[v]:
                dist[v] = d + w
                ways[v] = ways[u]
                heapq.heappush(heap, (dist[v], v))
            elif d + w == dist[v]:
                ways[v] += ways[u]
    return ways[n - 1] % (10**9 + 7)
""",
    ),
    # ---- Find the Safest Path in a Grid (LeetCode 2812) ----
    dict(
        title="Find the Safest Path in a Grid",
        diff="M",
        lc=2812,
        slug="find-the-safest-path-in-a-grid",
        prompt=(
            "grid[r][c] is 1 if the cell holds a thief and 0 otherwise (there is at least one thief). The safeness "
            "of a cell is its Manhattan distance to the nearest thief. The safeness of a PATH is the smallest "
            "safeness of any cell on it. Moving 4-directionally from the top-left to the bottom-right cell, return "
            "the maximum safeness a path can have."
        ),
        sig="def maximum_safeness_factor(grid: List[List[int]]) -> int:",
        fn="maximum_safeness_factor",
        tests=[
            (([[1, 0, 0], [0, 0, 0], [0, 0, 1]],), 0),
            (([[0, 0, 1], [0, 0, 0], [0, 0, 0]],), 2),
            (([[0, 0, 0, 1], [0, 0, 0, 0], [0, 0, 0, 0], [1, 0, 0, 0]],), 2),
            (([[1]],), 0),
        ],
        hints=[
            (
                "First compute every cell's distance to the nearest thief. Doing a BFS from ALL thieves at once "
                "gives all of them in one pass."
            ),
            (
                "Now you want the path whose WORST cell is as large as possible - the same 'maximise the minimum' "
                "idea as a widest path."
            ),
            (
                "Run Dijkstra with a max-heap where the cost of a path is the minimum safeness along it; or binary "
                "search the answer t and test with a flood fill that only uses cells of safeness >= t."
            ),
        ],
        pattern="Multi-source BFS + maximin path (Dijkstra / binary search)",
        explain=(
            "Multi-source BFS spreads from every thief at once so each cell gets its nearest-thief distance exactly "
            "once. The best path then maximises its minimum cell, which Dijkstra handles by always expanding the "
            "safest reachable frontier cell. The brute force measures the distance to each thief by scanning them "
            "all, then tries the safeness levels from the highest down with a flood fill."
        ),
        cx="O(n^2 log n) time, O(n^2) space",
        brute_cx="O(n^4) time - scan all thieves per cell, then a flood fill per level",
        brute=r"""
# BRUTE FORCE: O(n^4) time - scan all thieves per cell, then a flood fill per level
def maximum_safeness_factor(grid):
    n = len(grid)
    thieves = [(r, c) for r in range(n) for c in range(n) if grid[r][c] == 1]
    dist = [
        [min(abs(r - tr) + abs(c - tc) for tr, tc in thieves) for c in range(n)] for r in range(n)
    ]
    for level in range(2 * n, -1, -1):
        if dist[0][0] < level:
            continue
        seen = {(0, 0)}
        stack = [(0, 0)]
        while stack:
            r, c = stack.pop()
            if (r, c) == (n - 1, n - 1):
                return level
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen and dist[nr][nc] >= level:
                    seen.add((nr, nc))
                    stack.append((nr, nc))
""",
        solution=r"""
# OPTIMISED: O(n^2 log n) time, O(n^2) space
# Idea: Multi-source BFS + maximin path (Dijkstra / binary search)
def maximum_safeness_factor(grid):
    n = len(grid)
    dist = [[-1] * n for _ in range(n)]
    queue = deque()
    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                dist[r][c] = 0
                queue.append((r, c))
    while queue:
        r, c = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                queue.append((nr, nc))
    heap = [(-dist[0][0], 0, 0)]
    seen = {(0, 0)}
    while heap:
        neg, r, c = heapq.heappop(heap)
        safe = -neg
        if (r, c) == (n - 1, n - 1):
            return safe
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
                seen.add((nr, nc))
                heapq.heappush(heap, (-min(safe, dist[nr][nc]), nr, nc))
""",
    ),
    # ---- Shortest Cycle in a Graph (LeetCode 2608) ----
    dict(
        title="Shortest Cycle in a Graph",
        diff="H",
        lc=2608,
        slug="shortest-cycle-in-a-graph",
        prompt=(
            "A bidirectional graph has n vertices (0..n-1) and the given edges (no self-loops, at most one edge per "
            "pair). Return the length (number of edges) of its shortest cycle, or -1 if it has no cycle."
        ),
        sig="def find_shortest_cycle(n: int, edges: List[List[int]]) -> int:",
        fn="find_shortest_cycle",
        tests=[
            ((7, [[0, 1], [1, 2], [2, 0], [3, 4], [4, 5], [5, 6], [6, 3]]), 3),
            ((4, [[0, 1], [0, 2]]), -1),
            ((4, [[0, 1], [1, 2], [2, 3], [3, 0]]), 4),
            ((5, [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0], [0, 2]]), 3),
        ],
        hints=[
            (
                "Brute force: a shortest cycle through an edge (a, b) is that edge plus the shortest a-b path that "
                "avoids the edge. Try every edge."
            ),
            (
                "Better: BFS from each vertex s. If you meet an already-seen vertex v from u (and v is not u's BFS "
                "parent), then s -> u, u - v, v -> s closes a cycle of length dist[u] + dist[v] + 1."
            ),
            (
                "That length is an upper bound for any BFS and exact when s lies on the shortest cycle, so the "
                "minimum over all start vertices is the answer."
            ),
        ],
        pattern="BFS from every vertex, detect non-tree edges",
        explain=(
            "A non-tree edge found by a BFS closes a cycle through the BFS source (possibly a closed walk, never "
            "shorter than a real cycle's length bound), and when the source is on a shortest cycle the BFS meets "
            "that cycle's closing edge with exactly its length. Taking the minimum over all sources therefore gives "
            "the girth. The brute force removes each edge in turn and finds the shortest path between its endpoints."
        ),
        cx="O(n * (n + E)) time, O(n + E) space",
        brute_cx="O(E * (n + E)) time - remove each edge and run a BFS between its endpoints",
        brute=r"""
# BRUTE FORCE: O(E * (n + E)) time - remove each edge and run a BFS between its endpoints
def find_shortest_cycle(n, edges):
    best = float("inf")
    for skip, (a, b) in enumerate(edges):
        graph = defaultdict(list)
        for i, (u, v) in enumerate(edges):
            if i != skip:
                graph[u].append(v)
                graph[v].append(u)
        dist = {a: 0}
        queue = deque([a])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    queue.append(v)
        if b in dist:
            best = min(best, dist[b] + 1)
    return -1 if best == float("inf") else best
""",
        solution=r"""
# OPTIMISED: O(n * (n + E)) time, O(n + E) space
# Idea: BFS from every vertex, detect non-tree edges
def find_shortest_cycle(n, edges):
    graph = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    best = float("inf")
    for source in range(n):
        dist = {source: 0}
        parent = {source: -1}
        queue = deque([source])
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if v not in dist:
                    dist[v] = dist[u] + 1
                    parent[v] = u
                    queue.append(v)
                elif parent[u] != v:
                    best = min(best, dist[u] + dist[v] + 1)
    return -1 if best == float("inf") else best
""",
    ),
]
