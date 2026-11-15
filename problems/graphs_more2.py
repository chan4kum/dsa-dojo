"""extra batch of Graphs problems - the problem bank for the "graphs" topic.

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


def _safe_sorted(x):
    return sorted(x)


PROBLEMS = [
    # ---- Island Perimeter (LeetCode 463) ----
    dict(
        title="Island Perimeter",
        diff="E",
        lc=463,
        slug="island-perimeter",
        prompt="grid has 1 = land, 0 = water, and exactly one island (no lakes). Return its perimeter.",
        sig="def island_perimeter(grid: List[List[int]]) -> int:",
        fn="island_perimeter",
        tests=[
            (([[0, 1, 0, 0], [1, 1, 1, 0], [0, 1, 0, 0], [1, 1, 0, 0]],), 16),
            (([[1]],), 4),
            (([[1, 0]],), 4),
            (([[1, 1], [1, 1]],), 8),
            (([[1, 1, 1]],), 8),
        ],
        hints=[
            "Perimeter counts edges between a land cell and water/outside.",
            "Each land cell contributes 4 edges, minus 2 for every shared edge with another land cell.",
            (
                "For each land cell add 4; if the cell above is land subtract 2; if the left is land subtract 2 "
                "(count each pair once)."
            ),
        ],
        pattern="Local counting on a grid (4 - 2*shared edges)",
        explain="You do not need BFS/DFS: perimeter is purely local. Each adjacent land pair hides two edges.",
        cx="O(R*C) time, O(1) space",
        brute_cx="O(R*C*4) - check all four neighbours of every land cell",
        brute=r"""
# BRUTE FORCE: O(R*C*4) - check all four neighbours of every land cell
def island_perimeter(grid):
    R, C, p = len(grid), len(grid[0]), 0
    for r in range(R):
        for c in range(C):
            if grid[r][c]:
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if not (0 <= nr < R and 0 <= nc < C) or not grid[nr][nc]:
                        p += 1
    return p
""",
        solution=r"""
# OPTIMISED: O(R*C) time, O(1) space
# Idea: Local counting on a grid (4 - 2*shared edges)
def island_perimeter(grid):
    p = 0
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v:
                p += 4
                if r and grid[r - 1][c]:
                    p -= 2
                if c and row[c - 1]:
                    p -= 2
    return p
""",
    ),
    # ---- Flood Fill (LeetCode 733) ----
    dict(
        title="Flood Fill",
        diff="E",
        lc=733,
        slug="flood-fill",
        prompt=(
            "Starting at (sr, sc), recolor the connected (4-direction) region that shares the start's color with "
            "`color`. Return the image."
        ),
        sig="def flood_fill(image: List[List[int]], sr: int, sc: int, color: int) -> List[List[int]]:",
        fn="flood_fill",
        tests=[
            (([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2), [[2, 2, 2], [2, 2, 0], [2, 0, 1]]),
            (([[0, 0, 0], [0, 0, 0]], 0, 0, 0), [[0, 0, 0], [0, 0, 0]]),
            (([[1]], 0, 0, 5), [[5]]),
            (([[1, 2], [2, 1]], 0, 0, 3), [[3, 2], [2, 1]]),
        ],
        hints=[
            "It is a connected-component traversal, like counting islands.",
            "If the new color equals the old color there is nothing to do (and a naive DFS would loop forever).",
            (
                "DFS/BFS from the start, only entering cells equal to the original color; overwrite as you visit "
                "(the overwrite doubles as the visited mark)."
            ),
        ],
        pattern="Grid DFS/BFS (connected region), mutate-as-visited",
        explain=(
            "Changing a cell's color to the new color means you never revisit it, which is why the equal-color "
            "guard is essential."
        ),
        cx="O(R*C) time",
        brute_cx="O(R*C) time - iterative BFS with an explicit visited set",
        brute=r"""
# BRUTE FORCE: O(R*C) time - iterative BFS with an explicit visited set
def flood_fill(image, sr, sc, color):
    img = [row[:] for row in image]
    old = img[sr][sc]
    seen, q = {(sr, sc)}, deque([(sr, sc)])
    while q:
        r, c = q.popleft()
        img[r][c] = color
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < len(img)
                and 0 <= nc < len(img[0])
                and (nr, nc) not in seen
                and image[nr][nc] == old
            ):
                seen.add((nr, nc))
                q.append((nr, nc))
    return img
""",
        solution=r"""
# OPTIMISED: O(R*C) time
# Idea: Grid DFS/BFS (connected region), mutate-as-visited
def flood_fill(image, sr, sc, color):
    old = image[sr][sc]
    if old == color:
        return image

    def dfs(r, c):
        if 0 <= r < len(image) and 0 <= c < len(image[0]) and image[r][c] == old:
            image[r][c] = color
            dfs(r + 1, c)
            dfs(r - 1, c)
            dfs(r, c + 1)
            dfs(r, c - 1)

    dfs(sr, sc)
    return image
""",
    ),
    # ---- Shortest Path in Binary Matrix (LeetCode 1091) ----
    dict(
        title="Shortest Path in Binary Matrix",
        diff="M",
        lc=1091,
        slug="shortest-path-in-binary-matrix",
        prompt=(
            "From the top-left to the bottom-right of an n x n binary grid, moving in 8 directions through 0-cells "
            "only. Return the length of the shortest path (number of cells), or -1."
        ),
        sig="def shortest_path_binary_matrix(grid: List[List[int]]) -> int:",
        fn="shortest_path_binary_matrix",
        tests=[
            (([[0, 1], [1, 0]],), 2),
            (([[0, 0, 0], [1, 1, 0], [1, 1, 0]],), 4),
            (([[1, 0, 0], [1, 1, 0], [1, 1, 0]],), -1),
            (([[0]],), 1),
            (([[0, 0], [0, 1]],), -1),
        ],
        hints=[
            "Unweighted shortest path = BFS.",
            "Neighbours are the 8 surrounding cells; mark cells visited when you ENQUEUE them.",
            "Start dist = 1 (cells counted). Return as soon as you dequeue the bottom-right cell.",
        ],
        pattern="BFS on a grid (unweighted shortest path)",
        explain=(
            "BFS explores in rings of equal distance, so the first time you reach the target is by the fewest steps."
        ),
        cx="O(n^2) time, O(n^2) space",
        brute_cx="exponential - DFS over all simple paths",
        brute=r"""
# BRUTE FORCE: exponential - DFS over all simple paths
def shortest_path_binary_matrix(grid):
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1
    best = [float("inf")]
    seen = [[False] * n for _ in range(n)]

    def go(r, c, d):
        if d >= best[0]:
            return
        if (r, c) == (n - 1, n - 1):
            best[0] = d
            return
        seen[r][c] = True
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if (
                    (dr or dc)
                    and 0 <= nr < n
                    and 0 <= nc < n
                    and not grid[nr][nc]
                    and not seen[nr][nc]
                ):
                    go(nr, nc, d + 1)
        seen[r][c] = False

    go(0, 0, 1)
    return -1 if best[0] == float("inf") else best[0]
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n^2) space
# Idea: BFS on a grid (unweighted shortest path)
def shortest_path_binary_matrix(grid):
    n = len(grid)
    if grid[0][0] or grid[n - 1][n - 1]:
        return -1
    q, seen = deque([(0, 0, 1)]), {(0, 0)}
    while q:
        r, c, d = q.popleft()
        if (r, c) == (n - 1, n - 1):
            return d
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and not grid[nr][nc] and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    q.append((nr, nc, d + 1))
    return -1
""",
    ),
    # ---- Find the Town Judge (LeetCode 997) ----
    dict(
        title="Find the Town Judge",
        diff="E",
        lc=997,
        slug="find-the-town-judge",
        prompt=(
            "Among n people, the judge trusts nobody and everybody else trusts the judge. trust[i] = [a, b] means a "
            "trusts b. Return the judge's label (1..n) or -1."
        ),
        sig="def find_judge(n: int, trust: List[List[int]]) -> int:",
        fn="find_judge",
        tests=[
            ((2, [[1, 2]]), 2),
            ((3, [[1, 3], [2, 3]]), 3),
            ((3, [[1, 3], [2, 3], [3, 1]]), -1),
            ((1, []), 1),
            ((3, [[1, 2], [2, 3]]), -1),
        ],
        hints=[
            "Think in terms of in-degree and out-degree of a directed graph.",
            "The judge has in-degree n-1 and out-degree 0.",
            "Keep one array: +1 for the person being trusted, -1 for the truster. The judge's score is exactly n-1.",
        ],
        pattern="Degree counting on a directed graph",
        explain=(
            "A single net score per node encodes both conditions: trusted by all others (+(n-1)) and trusting "
            "nobody (no -1 contributions)."
        ),
        cx="O(n + e) time, O(n) space",
        brute_cx="O(n * e) time - check each candidate against every edge",
        brute=r"""
# BRUTE FORCE: O(n * e) time - check each candidate against every edge
def find_judge(n, trust):
    for cand in range(1, n + 1):
        trusts_someone = any(a == cand for a, b in trust)
        trusted_by = {a for a, b in trust if b == cand}
        if not trusts_someone and len(trusted_by) == n - 1:
            return cand
    return -1
""",
        solution=r"""
# OPTIMISED: O(n + e) time, O(n) space
# Idea: Degree counting on a directed graph
def find_judge(n, trust):
    score = [0] * (n + 1)
    for a, b in trust:
        score[a] -= 1
        score[b] += 1
    for p in range(1, n + 1):
        if score[p] == n - 1:
            return p
    return -1
""",
    ),
    # ---- Min Cost to Connect All Points (LeetCode 1584) ----
    dict(
        title="Min Cost to Connect All Points",
        diff="M",
        lc=1584,
        slug="min-cost-to-connect-all-points",
        prompt=(
            "Points on a plane; the cost of connecting two is their Manhattan distance. Return the minimum total "
            "cost to connect all points (a minimum spanning tree)."
        ),
        sig="def min_cost_connect_points(points: List[List[int]]) -> int:",
        fn="min_cost_connect_points",
        tests=[
            (([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]],), 20),
            (([[3, 12], [-2, 5], [-4, 1]],), 18),
            (([[0, 0]],), 0),
            (([[0, 0], [1, 1]],), 2),
            (([[0, 0], [0, 1], [0, 2], [0, 3]],), 3),
        ],
        hints=[
            "This is a minimum spanning tree problem on a complete graph.",
            "Kruskal: sort all edges by weight, add an edge if it joins two different components (union-find).",
            (
                "Or Prim: grow the tree from point 0 with a heap of (dist, node); O(n^2 log n) with a heap or "
                "O(n^2) with an array."
            ),
        ],
        pattern="Minimum spanning tree (Kruskal + Union-Find / Prim)",
        explain=(
            "'Connect everything as cheaply as possible' = MST. Greedy edge selection is correct because the "
            "cheapest edge crossing any cut is in some MST."
        ),
        cx="O(n^2 log n) time (Kruskal on n^2 edges)",
        brute_cx="O(n^2 * n) time - Prim with a linear scan for the next vertex",
        brute=r"""
# BRUTE FORCE: O(n^2 * n) time - Prim with a linear scan for the next vertex
def min_cost_connect_points(points):
    n = len(points)
    INF = float("inf")
    dist = [INF] * n
    used = [False] * n
    dist[0] = 0
    total = 0
    for _ in range(n):
        u = min((i for i in range(n) if not used[i]), key=lambda i: dist[i])
        used[u] = True
        total += dist[u]
        for v in range(n):
            if not used[v]:
                d = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                dist[v] = min(dist[v], d)
    return total
""",
        solution=r"""
# OPTIMISED: O(n^2 log n) time (Kruskal on n^2 edges)
# Idea: Minimum spanning tree (Kruskal + Union-Find / Prim)
def min_cost_connect_points(points):
    n = len(points)
    edges = sorted(
        (abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1]), i, j)
        for i in range(n)
        for j in range(i + 1, n)
    )
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total = used = 0
    for w, a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            total += w
            used += 1
            if used == n - 1:
                break
    return total
""",
    ),
    # ---- Find Eventual Safe States (LeetCode 802) ----
    dict(
        title="Find Eventual Safe States",
        diff="M",
        lc=802,
        slug="find-eventual-safe-states",
        prompt=(
            "graph[i] lists the nodes reachable from i in a directed graph. A node is safe if every path from it "
            "ends at a terminal node (no cycles). Return all safe nodes in ascending order."
        ),
        sig="def eventual_safe_nodes(graph: List[List[int]]) -> List[int]:",
        fn="eventual_safe_nodes",
        tests=[
            (([[1, 2], [2, 3], [5], [0], [5], [], []],), [2, 4, 5, 6]),
            (([[1, 2, 3, 4], [1, 2], [3, 4], [0, 4], []],), [4]),
            (([[]],), [0]),
            (([[0]],), []),
            (([[1], [], [0]],), [0, 1, 2]),
        ],
        hints=[
            "A node is unsafe if it can reach a cycle.",
            (
                "Reverse the graph: terminal nodes are safe, then nodes whose all successors are safe become safe "
                "(Kahn on the reversed graph)."
            ),
            "Or DFS with 3 colors: unvisited / in-progress / safe. Reaching an in-progress node means a cycle.",
        ],
        pattern="Cycle detection with DFS colors / reverse topological order",
        explain=(
            "Safe = cannot reach a cycle. Peeling nodes whose out-neighbours are all safe is a topological sort run "
            "backwards."
        ),
        cx="O(V + E) time, O(V) space",
        brute_cx="O(V * (V + E)) time - DFS from every node looking for a cycle",
        brute=r"""
# BRUTE FORCE: O(V * (V + E)) time - DFS from every node looking for a cycle
def eventual_safe_nodes(graph):
    n = len(graph)

    def reaches_cycle(start):
        # a node is unsafe if some node reachable from it (including itself) lies on a cycle
        seen, stack = set(), [start]
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if v == u:
                    return True
                if v not in seen:
                    seen.add(v)
                    stack.append(v)
        reach = seen
        for u in reach | {start}:
            q, s2 = list(graph[u]), set()
            while q:
                x = q.pop()
                if x == u:
                    return True
                if x not in s2:
                    s2.add(x)
                    q.extend(graph[x])
        return False

    return [i for i in range(n) if not reaches_cycle(i)]
""",
        solution=r"""
# OPTIMISED: O(V + E) time, O(V) space
# Idea: Cycle detection with DFS colors / reverse topological order
def eventual_safe_nodes(graph):
    n = len(graph)
    color = [0] * n  # 0 unvisited, 1 in progress, 2 safe

    def safe(u):
        if color[u]:
            return color[u] == 2
        color[u] = 1
        for v in graph[u]:
            if not safe(v):
                return False
        color[u] = 2
        return True

    return [i for i in range(n) if safe(i)]
""",
    ),
]
