"""more Graph problems (batch 4) - part of the problem bank for the "graphs" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""


def _round_all(values):
    """Round a list of floats so tiny float noise does not fail a test."""
    return [round(v, 5) for v in values]


PROBLEMS = [
    # ---- Find if Path Exists in Graph (LeetCode 1971) ----
    dict(
        title="Find if Path Exists in Graph",
        diff="E",
        lc=1971,
        slug="find-if-path-exists-in-graph",
        prompt=(
            "Nodes 0..n-1 are connected by undirected edges. Return True if there is a path from source to destination."
        ),
        sig="def valid_path(n: int, edges: List[List[int]], source: int, destination: int) -> bool:",
        fn="valid_path",
        tests=[
            ((3, [[0, 1], [1, 2], [2, 0]], 0, 2), True),
            ((6, [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]], 0, 5), False),
            ((1, [], 0, 0), True),
            ((2, [], 0, 1), False),
        ],
        hints=[
            "Build an adjacency list, then ask 'can I walk from source to destination?'.",
            "A DFS or BFS from source answers it in O(n + E).",
            (
                "If you only need connectivity and do not need the path, Union-Find works too: union every edge, "
                "then compare roots."
            ),
        ],
        pattern="Connectivity: BFS/DFS or Union-Find",
        explain=(
            "Two nodes are connected exactly when they lie in the same component. Union-Find builds the components "
            "once and answers any number of\n        queries in near O(1) each; a traversal re-explores the graph "
            "for every query."
        ),
        cx="O((n + E) * alpha(n)) time, O(n) space",
        brute_cx="O(n + E) time per query - DFS from the source",
        brute=r"""
# BRUTE FORCE: O(n + E) time per query - DFS from the source
def valid_path(n, edges, source, destination):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)
    seen, stack = {source}, [source]
    while stack:  # explore everything reachable from the source
        node = stack.pop()
        if node == destination:
            return True
        for nxt in adj[node]:
            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)
    return False
""",
        solution=r"""
# OPTIMISED: O((n + E) * alpha(n)) time, O(n) space
# Idea: Connectivity: BFS/DFS or Union-Find
def valid_path(n, edges, source, destination):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path halving keeps trees flat
            x = parent[x]
        return x

    for u, v in edges:
        parent[find(u)] = find(v)  # merge the two components
    return find(source) == find(destination)
""",
    ),
    # ---- All Paths From Source to Target (LeetCode 797) ----
    dict(
        title="All Paths From Source to Target",
        diff="M",
        lc=797,
        slug="all-paths-from-source-to-target",
        prompt=(
            "graph[i] lists the nodes you can go to from node i (a DAG). Return every path from node 0 to node n-1 "
            "(any order)."
        ),
        sig="def all_paths_source_target(graph: List[List[int]]) -> List[List[int]]:",
        fn="all_paths_source_target",
        compare="unordered",
        tests=[
            (([[1, 2], [3], [3], []],), [[0, 1, 3], [0, 2, 3]]),
            (([[4, 3, 1], [3, 2, 4], [3], [4], []],), [[0, 4], [0, 3, 4], [0, 1, 3, 4], [0, 1, 2, 3, 4], [0, 1, 4]]),
            (([[1], []],), [[0, 1]]),
            (([[1, 2], [2], []],), [[0, 1, 2], [0, 2]]),
        ],
        hints=[
            "A DAG has no cycles, so you never need a visited set - paths cannot loop.",
            "Walk from 0, extending the current path; when you reach n-1 save a copy.",
            "Use DFS backtracking: append the node, recurse into neighbours, pop the node.",
        ],
        pattern="DFS backtracking on a DAG",
        explain=(
            "Because there are no cycles, every walk ends. The number of paths can be exponential, so output size "
            "dominates the cost: O(2^n * n) in the worst case."
        ),
        cx="O(paths * n) time",
        brute_cx="O(paths * n) time - BFS over partial paths (copies a list at every step)",
        brute=r"""
# BRUTE FORCE: O(paths * n) time - BFS over partial paths (copies a list at every step)
def all_paths_source_target(graph):
    target = len(graph) - 1
    done, queue = [], deque([[0]])  # a queue of partial paths
    while queue:
        path = queue.popleft()
        if path[-1] == target:
            done.append(path)
            continue
        for nxt in graph[path[-1]]:
            queue.append(path + [nxt])  # a brand-new list for each extension
    return done
""",
        solution=r"""
# OPTIMISED: O(paths * n) time
# Idea: DFS backtracking on a DAG
def all_paths_source_target(graph):
    target, result, path = len(graph) - 1, [], [0]

    def dfs(node):
        if node == target:
            result.append(list(path))  # copy: `path` is reused
            return
        for nxt in graph[node]:
            path.append(nxt)
            dfs(nxt)
            path.pop()  # backtrack

    dfs(0)
    return result
""",
    ),
    # ---- Is Graph Bipartite? (LeetCode 785) ----
    dict(
        title="Is Graph Bipartite?",
        diff="M",
        lc=785,
        slug="is-graph-bipartite",
        prompt=(
            "graph[i] lists the neighbours of node i (undirected). Return True if the nodes can be split into two "
            "groups so that every edge joins different groups."
        ),
        sig="def is_bipartite(graph: List[List[int]]) -> bool:",
        fn="is_bipartite",
        tests=[
            (([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]],), False),
            (([[1, 3], [0, 2], [1, 3], [0, 2]],), True),
            (([[]],), True),
            (([[1], [0], [3], [2]],), True),
            (([[1, 2], [0, 2], [0, 1]],), False),
        ],
        hints=[
            "Two groups = two colours. Neighbours must get opposite colours.",
            (
                "Colour a start node 0, then give each neighbour the opposite colour. A neighbour already holding "
                "YOUR colour is a conflict."
            ),
            "The graph may be disconnected: start a new BFS from every uncoloured node.",
        ],
        pattern="Graph 2-colouring with BFS (an odd cycle makes it impossible)",
        explain=(
            "A graph is bipartite exactly when it has no odd-length cycle. BFS colouring finds a conflict the "
            "moment two adjacent nodes share a colour."
        ),
        cx="O(V + E) time, O(V) space",
        brute_cx="O(2^V * E) time - try every assignment of two groups",
        brute=r"""
# BRUTE FORCE: O(2^V * E) time - try every assignment of two groups
def is_bipartite(graph):
    n = len(graph)
    for mask in range(1 << n):  # every way to put each node in group 0 or group 1
        if all(((mask >> u) & 1) != ((mask >> v) & 1) for u in range(n) for v in graph[u]):
            return True
    return False
""",
        solution=r"""
# OPTIMISED: O(V + E) time, O(V) space
# Idea: Graph 2-colouring with BFS (an odd cycle makes it impossible)
def is_bipartite(graph):
    colour = {}
    for start in range(len(graph)):  # the graph may be disconnected
        if start in colour:
            continue
        colour[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nxt in graph[node]:
                if nxt not in colour:
                    colour[nxt] = 1 - colour[node]  # opposite group
                    queue.append(nxt)
                elif colour[nxt] == colour[node]:
                    return False  # an edge inside one group
    return True
""",
    ),
    # ---- Evaluate Division (LeetCode 399) ----
    dict(
        title="Evaluate Division",
        diff="M",
        lc=399,
        slug="evaluate-division",
        prompt=(
            "equations[i] = [A, B] with values[i] = A / B. For each query [C, D] return C / D, or -1.0 if it cannot "
            "be determined."
        ),
        sig=(
            "def calc_equation(equations: List[List[str]], values: List[float], queries: List[List[str]]) -> "
            "List[float]:"
        ),
        fn="calc_equation",
        adapt_out=_round_all,
        tests=[
            (
                ([["a", "b"], ["b", "c"]], [2.0, 3.0], [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]),
                [6.0, 0.5, -1.0, 1.0, -1.0],
            ),
            (
                (
                    [["a", "b"], ["b", "c"], ["bc", "cd"]],
                    [1.5, 2.5, 5.0],
                    [["a", "c"], ["c", "b"], ["bc", "cd"], ["cd", "bc"]],
                ),
                [3.75, 0.4, 5.0, 0.2],
            ),
            (([["a", "b"]], [0.5], [["a", "b"], ["b", "a"], ["a", "c"], ["x", "y"]]), [0.5, 2.0, -1.0, -1.0]),
        ],
        hints=[
            "Variables are nodes; A / B = v is an edge A -> B with weight v and an edge B -> A with weight 1/v.",
            "C / D is the PRODUCT of the weights along any path from C to D.",
            (
                "Per query: DFS multiplying weights. Faster: weighted Union-Find that stores each node's ratio to "
                "its root."
            ),
        ],
        pattern="Weighted graph / weighted Union-Find",
        explain=(
            "Every variable in a component is a fixed multiple of one root variable. Store that multiple, and any "
            "ratio inside the component is a division of\n        two stored numbers - no path search per query."
        ),
        cx="O((E + Q) * alpha) time",
        brute_cx="O(Q * (V + E)) time - one DFS per query",
        brute=r"""
# BRUTE FORCE: O(Q * (V + E)) time - one DFS per query
def calc_equation(equations, values, queries):
    graph = defaultdict(dict)
    for (a, b), v in zip(equations, values):
        graph[a][b] = v
        graph[b][a] = 1 / v

    def search(src, dst):
        if src not in graph or dst not in graph:
            return -1.0
        seen, stack = {src}, [(src, 1.0)]
        while stack:  # DFS, carrying the product of weights so far
            node, product = stack.pop()
            if node == dst:
                return product
            for nxt, w in graph[node].items():
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append((nxt, product * w))
        return -1.0

    return [search(c, d) for c, d in queries]
""",
        solution=r"""
# OPTIMISED: O((E + Q) * alpha) time
# Idea: Weighted graph / weighted Union-Find
def calc_equation(equations, values, queries):
    parent, ratio = {}, {}  # ratio[x] = x / parent[x]

    def find(x):
        if parent[x] != x:
            root = find(parent[x])
            ratio[x] *= ratio[parent[x]]  # now x / root
            parent[x] = root
        return parent[x]

    for (a, b), v in zip(equations, values):
        for name in (a, b):
            if name not in parent:
                parent[name], ratio[name] = name, 1.0
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb  # ra / rb = (a / ratio[a]) / (b / ratio[b]) with a / b = v
            ratio[ra] = v * ratio[b] / ratio[a]

    result = []
    for c, d in queries:
        if c in parent and d in parent and find(c) == find(d):
            result.append(ratio[c] / ratio[d])  # (c / root) / (d / root)
        else:
            result.append(-1.0)
    return result
""",
    ),
    # ---- Most Stones Removed with Same Row or Column (LeetCode 947) ----
    dict(
        title="Most Stones Removed with Same Row or Column",
        diff="M",
        lc=947,
        slug="most-stones-removed-with-same-row-or-column",
        prompt=(
            "Stones sit at distinct grid points. You may remove a stone if another stone remains in its row or "
            "column. Return the maximum number of stones you can remove."
        ),
        sig="def remove_stones(stones: List[List[int]]) -> int:",
        fn="remove_stones",
        tests=[
            (([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]],), 5),
            (([[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]],), 3),
            (([[0, 0]],), 0),
            (([[0, 0], [1, 1]],), 0),
        ],
        hints=[
            "Stones that share a row or column are linked; think of connected groups.",
            "Within a group of k connected stones you can always remove k - 1 of them.",
            (
                "Answer = number of stones - number of groups. Union rows with columns (offset the columns) so each "
                "stone is an edge."
            ),
        ],
        pattern="Union-Find where rows and columns are the nodes",
        explain=(
            "Treat each stone as an edge between its row node and its column node. A component with k stones can be "
            "peeled down to one stone, so the answer is stones - components."
        ),
        cx="O(n * alpha(n)) time",
        brute_cx="O(n^2) time - link stones that share a line and DFS over the stones",
        brute=r"""
# BRUTE FORCE: O(n^2) time - link stones that share a line and DFS over the stones
def remove_stones(stones):
    n, seen, groups = len(stones), set(), 0
    for i in range(n):
        if i in seen:
            continue
        groups += 1  # a new connected group of stones
        seen.add(i)
        stack = [i]
        while stack:
            a = stack.pop()
            for b in range(n):  # compare with EVERY stone (O(n^2) overall)
                if b not in seen and (stones[a][0] == stones[b][0] or stones[a][1] == stones[b][1]):
                    seen.add(b)
                    stack.append(b)
    return n - groups
""",
        solution=r"""
# OPTIMISED: O(n * alpha(n)) time
# Idea: Union-Find where rows and columns are the nodes
def remove_stones(stones):
    parent = {}

    def find(x):
        parent.setdefault(x, x)
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for row, col in stones:
        # a column node is tagged ("c", col) so it never collides with a row number
        parent[find(row)] = find(("c", col))
    components = len({find(row) for row, _ in stones})
    return len(stones) - components
""",
    ),
    # ---- Satisfiability of Equality Equations (LeetCode 990) ----
    dict(
        title="Satisfiability of Equality Equations",
        diff="M",
        lc=990,
        slug="satisfiability-of-equality-equations",
        prompt=(
            "Each equation is a string like 'a==b' or 'a!=b' over lowercase letters. Return True if the variables "
            "can be given integer values satisfying all of them."
        ),
        sig="def equations_possible(equations: List[str]) -> bool:",
        fn="equations_possible",
        tests=[
            ((["a==b", "b!=a"],), False),
            ((["b==a", "a==b"],), True),
            ((["a==b", "b==c", "a==c"],), True),
            ((["a==b", "b!=c", "c==a"],), False),
            ((["c==c", "b==d", "x!=z"],), True),
            ((["a!=a"],), False),
        ],
        hints=[
            "'==' relations are transitive: they build groups of equal variables.",
            "'!=' is a CHECK against those groups, so apply all '==' first.",
            "Union-Find: union every '==' pair, then fail if any '!=' pair shares a root.",
        ],
        pattern="Union-Find: merge equalities first, then verify inequalities",
        explain=(
            "Equalities create equivalence classes. An inequality is only violated when both sides are inside the "
            "same class, so one pass of unions and one pass of checks decides it."
        ),
        cx="O(n * alpha) time",
        brute_cx="O(n * (V + E)) time - a graph search for every '!=' equation",
        brute=r"""
# BRUTE FORCE: O(n * (V + E)) time - a graph search for every '!=' equation
def equations_possible(equations):
    same = defaultdict(set)  # graph of '==' links
    for eq in equations:
        if eq[1] == "=":
            same[eq[0]].add(eq[3])
            same[eq[3]].add(eq[0])
    for eq in equations:
        if eq[1] == "!":
            a, b = eq[0], eq[3]
            seen, stack = {a}, [a]
            while stack:  # can we get from a to b using only '==' links?
                x = stack.pop()
                for y in same[x]:
                    if y not in seen:
                        seen.add(y)
                        stack.append(y)
            if b in seen:  # a and b must be equal but the equation says they differ
                return False
    return True
""",
        solution=r"""
# OPTIMISED: O(n * alpha) time
# Idea: Union-Find: merge equalities first, then verify inequalities
def equations_possible(equations):
    parent = {c: c for c in "abcdefghijklmnopqrstuvwxyz"}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for eq in equations:
        if eq[1] == "=":
            parent[find(eq[0])] = find(eq[3])  # equal variables share a root
    return all(find(eq[0]) != find(eq[3]) for eq in equations if eq[1] == "!")
""",
    ),
    # ---- Path With Minimum Effort (LeetCode 1631) ----
    dict(
        title="Path With Minimum Effort",
        diff="M",
        lc=1631,
        slug="path-with-minimum-effort",
        prompt=(
            "Walk from the top-left to the bottom-right of a height grid (4 directions). The effort of a path is "
            "the largest height difference between two consecutive cells. Return the minimum possible effort."
        ),
        sig="def minimum_effort_path(heights: List[List[int]]) -> int:",
        fn="minimum_effort_path",
        tests=[
            (([[1, 2, 2], [3, 8, 2], [5, 3, 5]],), 2),
            (([[1, 2, 3], [3, 8, 4], [5, 3, 5]],), 1),
            (([[1, 2, 1, 1, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 2, 1, 2, 1], [1, 1, 1, 2, 1]],), 0),
            (([[1]],), 0),
        ],
        hints=[
            "The cost of a path is its WORST step, not the sum - so ordinary BFS levels do not apply.",
            "Dijkstra still works if the 'distance' to a cell is the smallest possible worst-step to reach it.",
            "When moving to a neighbour, new_cost = max(cost so far, |height difference|); push it into a min-heap.",
        ],
        pattern="Dijkstra with a minimax cost (max instead of sum)",
        explain=(
            "Dijkstra needs a cost that never decreases along a path; max(...) satisfies that. The heap always "
            "expands the cell reachable with the smallest worst-step."
        ),
        cx="O(R*C log(R*C)) time",
        brute_cx=(
            "O(R*C * K) time - for each candidate effort K (in increasing order) run a BFS limited to that step size"
        ),
        brute=r"""
# BRUTE FORCE: O(R*C * K) time - for each candidate effort K (in increasing order) run a BFS limited to that step size
def minimum_effort_path(heights):
    rows, cols = len(heights), len(heights[0])
    if rows == cols == 1:
        return 0
    steps = set()  # every distinct neighbour difference is a candidate answer
    for r in range(rows):
        for c in range(cols):
            if r + 1 < rows:
                steps.add(abs(heights[r][c] - heights[r + 1][c]))
            if c + 1 < cols:
                steps.add(abs(heights[r][c] - heights[r][c + 1]))
    for limit in sorted(steps):  # smallest allowed step first
        seen, queue = {(0, 0)}, deque([(0, 0)])
        while queue:
            r, c = queue.popleft()
            if (r, c) == (rows - 1, cols - 1):
                return limit
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in seen:
                    if abs(heights[nr][nc] - heights[r][c]) <= limit:
                        seen.add((nr, nc))
                        queue.append((nr, nc))
    return 0
""",
        solution=r"""
# OPTIMISED: O(R*C log(R*C)) time
# Idea: Dijkstra with a minimax cost (max instead of sum)
def minimum_effort_path(heights):
    rows, cols = len(heights), len(heights[0])
    best = [[float("inf")] * cols for _ in range(rows)]
    best[0][0] = 0
    heap = [(0, 0, 0)]  # (worst step so far, row, col)
    while heap:
        effort, r, c = heapq.heappop(heap)
        if (r, c) == (rows - 1, cols - 1):
            return effort
        if effort > best[r][c]:
            continue  # a stale heap entry
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_effort = max(effort, abs(heights[nr][nc] - heights[r][c]))
                if new_effort < best[nr][nc]:
                    best[nr][nc] = new_effort
                    heapq.heappush(heap, (new_effort, nr, nc))
    return 0
""",
    ),
    # ---- Find the City With the Smallest Number of Neighbors at a Threshold Distance (LeetCode 1334) ----
    dict(
        title="Find the City With the Smallest Number of Neighbors at a Threshold Distance",
        diff="M",
        lc=1334,
        slug="find-the-city-with-the-smallest-number-of-neighbors-at-a-threshold-distance",
        prompt=(
            "Cities 0..n-1 with weighted undirected edges [u, v, w]. For each city count the cities reachable "
            "within distance_threshold. Return the city with the fewest; on ties, the largest index."
        ),
        sig="def find_the_city(n: int, edges: List[List[int]], distance_threshold: int) -> int:",
        fn="find_the_city",
        tests=[
            ((4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4), 3),
            ((5, [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]], 2), 0),
            ((2, [], 1), 1),
            ((3, [[0, 1, 1], [1, 2, 1]], 1), 2),
        ],
        hints=[
            "You need the shortest distance between EVERY pair of cities (all-pairs).",
            (
                "n is small, so O(n^3) is fine. Floyd-Warshall: for each middle city k, try dist[i][j] = dist[i][k] "
                "+ dist[k][j]."
            ),
            (
                "Then count, for each city, the others with dist <= threshold, and pick the minimum (the later "
                "index wins ties)."
            ),
        ],
        pattern="All-pairs shortest paths (Floyd-Warshall)",
        explain=(
            "Floyd-Warshall allows intermediate cities one at a time, so after processing city k every pair uses "
            "the best path through cities 0..k. For small, dense graphs the triple loop is simpler than n Dijkstras."
        ),
        cx="O(n^3) time, O(n^2) space",
        brute_cx="O(n * n * E) time - Bellman-Ford from every city",
        brute=r"""
# BRUTE FORCE: O(n * n * E) time - Bellman-Ford from every city
def find_the_city(n, edges, distance_threshold):
    best_city, best_count = -1, n + 1
    for src in range(n):
        dist = [float("inf")] * n
        dist[src] = 0
        for _ in range(n - 1):  # Bellman-Ford: relax every edge n - 1 times
            for u, v, w in edges:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                if dist[v] + w < dist[u]:
                    dist[u] = dist[v] + w
        count = sum(1 for city in range(n) if city != src and dist[city] <= distance_threshold)
        if count <= best_count:  # <= so that a later index wins ties
            best_city, best_count = src, count
    return best_city
""",
        solution=r"""
# OPTIMISED: O(n^3) time, O(n^2) space
# Idea: All-pairs shortest paths (Floyd-Warshall)
def find_the_city(n, edges, distance_threshold):
    inf = float("inf")
    dist = [[0 if i == j else inf for j in range(n)] for i in range(n)]
    for u, v, w in edges:
        dist[u][v] = dist[v][u] = min(dist[u][v], w)
    for k in range(n):  # allow city k as an intermediate stop
        for i in range(n):
            for j in range(n):
                if dist[i][k] + dist[k][j] < dist[i][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    best_city, best_count = -1, n + 1
    for i in range(n):
        count = sum(1 for j in range(n) if i != j and dist[i][j] <= distance_threshold)
        if count <= best_count:
            best_city, best_count = i, count
    return best_city
""",
    ),
    # ---- Path with Maximum Probability (LeetCode 1514) ----
    dict(
        title="Path with Maximum Probability",
        diff="M",
        lc=1514,
        slug="path-with-maximum-probability",
        prompt=(
            "An undirected graph has edge success probabilities. Return the largest probability of getting from "
            "start to end (the product along a path), or 0 if unreachable."
        ),
        sig=(
            "def max_probability(n: int, edges: List[List[int]], succ_prob: List[float], start: int, end: int) -> "
            "float:"
        ),
        fn="max_probability",
        compare="float",
        tests=[
            ((3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.2], 0, 2), 0.25),
            ((3, [[0, 1], [1, 2], [0, 2]], [0.5, 0.5, 0.3], 0, 2), 0.3),
            ((3, [[0, 1]], [0.5], 0, 2), 0.0),
            ((2, [[0, 1]], [1.0], 0, 1), 1.0),
        ],
        hints=[
            (
                "Multiplying probabilities (each <= 1) never increases the value, just as adding positive weights "
                "never decreases a distance."
            ),
            "So Dijkstra applies - but you want the MAXIMUM product.",
            "Use a max-heap (push negated probabilities in Python's min-heap) and relax with prob * edge_probability.",
        ],
        pattern="Dijkstra with a max-heap on products",
        explain=(
            "Dijkstra works for any 'cost' that is monotone along a path. Here the best-so-far value is a product "
            "<= 1 that can only shrink, so the first time the heap pops `end` it is optimal."
        ),
        cx="O((V + E) log V) time",
        brute_cx="O(V!) time - DFS over every simple path",
        brute=r"""
# BRUTE FORCE: O(V!) time - DFS over every simple path
def max_probability(n, edges, succ_prob, start, end):
    adj = [[] for _ in range(n)]
    for (u, v), p in zip(edges, succ_prob):
        adj[u].append((v, p))
        adj[v].append((u, p))
    best = 0.0

    def dfs(node, prob, seen):  # try every simple path
        nonlocal best
        if node == end:
            best = max(best, prob)
            return
        for nxt, p in adj[node]:
            if nxt not in seen:
                dfs(nxt, prob * p, seen | {nxt})

    dfs(start, 1.0, {start})
    return best
""",
        solution=r"""
# OPTIMISED: O((V + E) log V) time
# Idea: Dijkstra with a max-heap on products
def max_probability(n, edges, succ_prob, start, end):
    adj = [[] for _ in range(n)]
    for (u, v), p in zip(edges, succ_prob):
        adj[u].append((v, p))
        adj[v].append((u, p))
    best = [0.0] * n
    best[start] = 1.0
    heap = [(-1.0, start)]  # negated: heapq is a min-heap
    while heap:
        neg_prob, node = heapq.heappop(heap)
        if node == end:
            return -neg_prob
        if -neg_prob < best[node]:
            continue  # stale entry
        for nxt, p in adj[node]:
            cand = -neg_prob * p
            if cand > best[nxt]:
                best[nxt] = cand
                heapq.heappush(heap, (-cand, nxt))
    return 0.0
""",
    ),
    # ---- Minimum Height Trees (LeetCode 310) ----
    dict(
        title="Minimum Height Trees",
        diff="M",
        lc=310,
        slug="minimum-height-trees",
        prompt=(
            "A tree has n nodes (0..n-1). Choosing any node as the root gives a rooted tree; return every root that "
            "gives the minimum possible height (any order)."
        ),
        sig="def find_min_height_trees(n: int, edges: List[List[int]]) -> List[int]:",
        fn="find_min_height_trees",
        compare="unordered",
        tests=[
            ((4, [[1, 0], [1, 2], [1, 3]]), [1]),
            ((6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]]), [3, 4]),
            ((1, []), [0]),
            ((2, [[0, 1]]), [0, 1]),
        ],
        hints=[
            "The best roots are the 'centre' of the tree - there are always one or two of them.",
            "Peel the tree like an onion: repeatedly remove all current leaves.",
            "Stop when 2 or fewer nodes remain; those are the answer. Track degrees and queue the nodes of degree 1.",
        ],
        pattern="Topological-style leaf trimming to find the tree centre",
        explain=(
            "Leaves are never good roots, so peel them layer by layer (like BFS from the outside in). The last one "
            "or two nodes left are the middle of the longest path."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - BFS from every node to measure its height",
        brute=r"""
# BRUTE FORCE: O(n^2) time - BFS from every node to measure its height
def find_min_height_trees(n, edges):
    adj = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v)
        adj[v].append(u)

    def height(root):  # BFS depth when `root` is the root
        seen, level, h = {root}, [root], 0
        while level:
            nxt = [y for x in level for y in adj[x] if y not in seen]
            seen.update(nxt)
            if nxt:
                h += 1
            level = nxt
        return h

    heights = [height(r) for r in range(n)]
    return [r for r in range(n) if heights[r] == min(heights)]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Topological-style leaf trimming to find the tree centre
def find_min_height_trees(n, edges):
    if n <= 2:
        return list(range(n))
    adj = [set() for _ in range(n)]
    for u, v in edges:
        adj[u].add(v)
        adj[v].add(u)
    leaves = [i for i in range(n) if len(adj[i]) == 1]
    remaining = n
    while remaining > 2:
        remaining -= len(leaves)  # strip off the current outer layer
        next_leaves = []
        for leaf in leaves:
            (neighbour,) = adj[leaf]  # a leaf has exactly one neighbour
            adj[neighbour].remove(leaf)
            if len(adj[neighbour]) == 1:  # it just became a leaf
                next_leaves.append(neighbour)
        leaves = next_leaves
    return leaves
""",
    ),
]
