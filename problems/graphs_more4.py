"""more Graph problems (batch 5) - part of the problem bank for the "graphs" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Shortest Bridge (LeetCode 934) ----
    dict(
        title="Shortest Bridge",
        diff="M",
        lc=934,
        slug="shortest-bridge",
        prompt=(
            "grid contains exactly two islands (4-connected groups of 1). You may flip 0s to 1s. Return the minimum "
            "number of 0s to flip so the two islands become one."
        ),
        sig="def shortest_bridge(grid: List[List[int]]) -> int:",
        fn="shortest_bridge",
        tests=[
            (([[0, 1], [1, 0]],), 1),
            (([[0, 1, 0], [0, 0, 0], [0, 0, 1]],), 2),
            (([[1, 1, 1, 1, 1], [1, 0, 0, 0, 1], [1, 0, 1, 0, 1], [1, 0, 0, 0, 1], [1, 1, 1, 1, 1]],), 1),
            (([[1, 0, 1]],), 1),
        ],
        hints=[
            "First find ONE island (DFS/BFS from any 1) so you can tell the two islands apart.",
            (
                "Then grow that island outwards one ring at a time - a BFS that starts from all its cells at once "
                "(multi-source BFS)."
            ),
            "The number of rings you expand before touching a cell of the other island is the number of 0s to flip.",
        ],
        pattern="Flood fill one island, then multi-source BFS to the other",
        explain=(
            "BFS explores by distance, so the first time the frontier reaches the second island, the ring count is "
            "the shortest water crossing. Starting the BFS from every cell of the first island is the same as "
            "adding one super-source."
        ),
        cx="O(R*C) time and space",
        brute_cx="O(|A| * |B|) time - Manhattan distance between every pair of cells from the two islands",
        brute=r"""
# BRUTE FORCE: O(|A| * |B|) time - Manhattan distance between every pair of cells from the two islands
def shortest_bridge(grid):
    rows, cols = len(grid), len(grid[0])
    seen, islands = set(), []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in seen:
                island, stack = [], [(r, c)]
                seen.add((r, c))

                while stack:  # collect one whole island
                    cr, cc = stack.pop()
                    island.append((cr, cc))

                    for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                        if (
                            0 <= nr < rows
                            and 0 <= nc < cols
                            and grid[nr][nc] == 1
                            and (nr, nc) not in seen
                        ):
                            seen.add((nr, nc))
                            stack.append((nr, nc))

                islands.append(island)

    first, second = islands

    # only water and the two islands exist, so a shortest path is a Manhattan path; flips = distance - 1
    return min(abs(a - c) + abs(b - d) for a, b in first for c, d in second) - 1
""",
        solution=r"""
# OPTIMISED: O(R*C) time and space
# Idea: Flood fill one island, then multi-source BFS to the other
def shortest_bridge(grid):
    rows, cols = len(grid), len(grid[0])
    grid = [row[:] for row in grid]
    frontier = []

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not frontier:  # flood the first island found and mark it 2
                stack = [(r, c)]
                grid[r][c] = 2

                while stack:
                    cr, cc = stack.pop()
                    frontier.append((cr, cc))
                    for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                            grid[nr][nc] = 2
                            stack.append((nr, nc))

    flips = 0

    while frontier:  # grow the island one ring of water at a time
        nxt = []

        for cr, cc in frontier:
            for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                if 0 <= nr < rows and 0 <= nc < cols:
                    if grid[nr][nc] == 1:
                        return flips  # reached the other island
                    if grid[nr][nc] == 0:
                        grid[nr][nc] = 2
                        nxt.append((nr, nc))

        frontier = nxt
        flips += 1

    return flips
""",
    ),
    # ---- Smallest String With Swaps (LeetCode 1202) ----
    dict(
        title="Smallest String With Swaps",
        diff="M",
        lc=1202,
        slug="smallest-string-with-swaps",
        prompt=(
            "You may swap the characters at the two indices of any pair in pairs, any number of times. Return the "
            "lexicographically smallest string you can get."
        ),
        sig="def smallest_string_with_swaps(s: str, pairs: List[List[int]]) -> str:",
        fn="smallest_string_with_swaps",
        tests=[
            (("dcab", [[0, 3], [1, 2]]), "bacd"),
            (("dcab", [[0, 3], [1, 2], [0, 2]]), "abcd"),
            (("cba", [[0, 1], [1, 2]]), "abc"),
            (("abc", []), "abc"),
        ],
        hints=[
            "If index i can swap with j and j with k, then i, j, k can be arranged in ANY order.",
            (
                "So indices form connected components (Union-Find), and inside a component the characters can be "
                "freely sorted."
            ),
            "Group indices by root; sort each group's characters; write them back to the sorted indices.",
        ],
        pattern="Union-Find groups + sort within each group",
        explain=(
            "A chain of swaps lets any character travel anywhere in its component, so the best arrangement is the "
            "sorted one, placed on the component's indices in increasing order."
        ),
        cx="O(n log n + P * alpha) time",
        brute_cx="O(n! * P) time - BFS over every string reachable by swaps",
        brute=r"""
# BRUTE FORCE: O(n! * P) time - BFS over every string reachable by swaps
def smallest_string_with_swaps(s, pairs):
    best, seen, queue = s, {s}, deque([s])

    while queue:  # explore every string reachable through the allowed swaps
        cur = queue.popleft()
        best = min(best, cur)

        for a, b in pairs:
            chars = list(cur)
            chars[a], chars[b] = chars[b], chars[a]
            nxt = "".join(chars)
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)

    return best
""",
        solution=r"""
# OPTIMISED: O(n log n + P * alpha) time
# Idea: Union-Find groups + sort within each group
def smallest_string_with_swaps(s, pairs):
    parent = list(range(len(s)))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in pairs:
        parent[find(a)] = find(b)

    groups = defaultdict(list)

    for i in range(len(s)):
        groups[find(i)].append(i)  # indices are appended in increasing order

    result = list(s)

    for indices in groups.values():
        letters = sorted(s[i] for i in indices)
        for i, ch in zip(indices, letters):
            result[i] = ch  # smallest letter to the smallest index

    return "".join(result)
""",
    ),
    # ---- Number of Operations to Make Network Connected (LeetCode 1319) ----
    dict(
        title="Number of Operations to Make Network Connected",
        diff="M",
        lc=1319,
        slug="number-of-operations-to-make-network-connected",
        prompt=(
            "n computers (0..n-1) with undirected cables. One operation moves a cable to join two other computers. "
            "Return the minimum operations to connect all computers, or -1 if impossible."
        ),
        sig="def make_connected(n: int, connections: List[List[int]]) -> int:",
        fn="make_connected",
        tests=[
            ((4, [[0, 1], [0, 2], [1, 2]]), 1),
            ((6, [[0, 1], [0, 2], [0, 3], [1, 2], [1, 3]]), 2),
            ((6, [[0, 1], [0, 2], [0, 3], [1, 2]]), -1),
            ((5, [[0, 1], [0, 2], [3, 4], [2, 3]]), 0),
        ],
        hints=[
            "To connect c components you need c - 1 cables.",
            "You need at least n - 1 cables in total, otherwise return -1.",
            "Count the components (Union-Find or DFS); the answer is components - 1 once enough cables exist.",
        ],
        pattern="Count components; cable count is the feasibility test",
        explain=(
            "Spare cables are those that close a cycle. If len(connections) >= n - 1 there are always enough spares "
            "somewhere, so only the number of components matters."
        ),
        cx="O((n + E) * alpha) time",
        brute_cx="O(n + E) time - DFS to count components",
        brute=r"""
# BRUTE FORCE: O(n + E) time - DFS to count components
def make_connected(n, connections):
    if len(connections) < n - 1:
        return -1

    adj = [[] for _ in range(n)]

    for a, b in connections:
        adj[a].append(b)
        adj[b].append(a)

    seen, components = set(), 0

    for start in range(n):
        if start in seen:
            continue

        components += 1  # a new component: explore all of it
        seen.add(start)
        stack = [start]

        while stack:
            node = stack.pop()
            for nxt in adj[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)

    return components - 1
""",
        solution=r"""
# OPTIMISED: O((n + E) * alpha) time
# Idea: Count components; cable count is the feasibility test
def make_connected(n, connections):
    if len(connections) < n - 1:
        return -1

    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    components = n

    for a, b in connections:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            components -= 1  # two components merged

    return components - 1
""",
    ),
    # ---- Possible Bipartition (LeetCode 886) ----
    dict(
        title="Possible Bipartition",
        diff="M",
        lc=886,
        slug="possible-bipartition",
        prompt=(
            "People are labelled 1..n. dislikes[i] = [a, b] means a and b must not be in the same group. Return "
            "True if everyone can be split into two groups."
        ),
        sig="def possible_bipartition(n: int, dislikes: List[List[int]]) -> bool:",
        fn="possible_bipartition",
        tests=[
            ((4, [[1, 2], [1, 3], [2, 4]]), True),
            ((3, [[1, 2], [1, 3], [2, 3]]), False),
            ((5, [[1, 2], [2, 3], [3, 4], [4, 5], [1, 5]]), False),
            ((1, []), True),
        ],
        hints=[
            "People are nodes and dislikes are edges: 'different groups' means opposite colours.",
            "This is exactly Is Graph Bipartite?",
            "Colour each component with BFS; an edge joining two equal colours means impossible.",
        ],
        pattern="Graph 2-colouring (bipartite check)",
        explain="Same algorithm as Is Graph Bipartite; only the input format (1-indexed edge list) differs.",
        cx="O(n + E) time",
        brute_cx="O(2^n * E) time - try every assignment of people to two groups",
        brute=r"""
# BRUTE FORCE: O(2^n * E) time - try every assignment of people to two groups
def possible_bipartition(n, dislikes):
    for mask in range(1 << n):  # bit i says which group person i + 1 joins
        if all(((mask >> (a - 1)) & 1) != ((mask >> (b - 1)) & 1) for a, b in dislikes):
            return True
    return False
""",
        solution=r"""
# OPTIMISED: O(n + E) time
# Idea: Graph 2-colouring (bipartite check)
def possible_bipartition(n, dislikes):
    adj = defaultdict(list)

    for a, b in dislikes:
        adj[a].append(b)
        adj[b].append(a)

    colour = {}

    for start in range(1, n + 1):
        if start in colour:
            continue

        colour[start] = 0
        queue = deque([start])

        while queue:
            node = queue.popleft()
            for nxt in adj[node]:
                if nxt not in colour:
                    colour[nxt] = 1 - colour[node]
                    queue.append(nxt)
                elif colour[nxt] == colour[node]:
                    return False

    return True
""",
    ),
    # ---- Course Schedule IV (LeetCode 1462) ----
    dict(
        title="Course Schedule IV",
        diff="M",
        lc=1462,
        slug="course-schedule-iv",
        prompt=(
            "prerequisites[i] = [a, b] means course a must be taken before b (prerequisites are transitive). For "
            "each query [u, v] return whether u is a prerequisite of v."
        ),
        sig=(
            "def check_if_prerequisite(num_courses: int, prerequisites: List[List[int]], queries: List[List[int]]) "
            "-> List[bool]:"
        ),
        fn="check_if_prerequisite",
        tests=[
            ((2, [[1, 0]], [[0, 1], [1, 0]]), [False, True]),
            ((2, [], [[1, 0], [0, 1]]), [False, False]),
            ((3, [[1, 2], [1, 0], [2, 0]], [[1, 0], [1, 2]]), [True, True]),
            ((3, [[0, 1], [1, 2]], [[0, 2], [2, 0]]), [True, False]),
        ],
        hints=[
            "A query asks about REACHABILITY in a directed graph.",
            "One DFS per query works; with many queries it is wasteful.",
            "Precompute reachability for all pairs with Floyd-Warshall (reach[i][j] |= reach[i][k] and reach[k][j]).",
        ],
        pattern="Transitive closure (Floyd-Warshall on booleans)",
        explain=(
            "Answering Q queries from a precomputed n x n table costs O(1) each, at the price of O(n^3) preprocessing."
        ),
        cx="O(n^3 + Q) time, O(n^2) space",
        brute_cx="O(Q * (n + E)) time - a DFS for every query",
        brute=r"""
# BRUTE FORCE: O(Q * (n + E)) time - a DFS for every query
def check_if_prerequisite(num_courses, prerequisites, queries):
    adj = defaultdict(list)

    for a, b in prerequisites:
        adj[a].append(b)

    def reaches(src, dst):
        seen, stack = {src}, [src]

        while stack:
            node = stack.pop()

            if node == dst and node != src:
                return True

            for nxt in adj[node]:
                if nxt == dst:
                    return True
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)

        return False

    return [reaches(u, v) for u, v in queries]
""",
        solution=r"""
# OPTIMISED: O(n^3 + Q) time, O(n^2) space
# Idea: Transitive closure (Floyd-Warshall on booleans)
def check_if_prerequisite(num_courses, prerequisites, queries):
    n = num_courses
    reach = [[False] * n for _ in range(n)]

    for a, b in prerequisites:
        reach[a][b] = True

    for k in range(n):  # allow k as an intermediate course
        for i in range(n):
            if reach[i][k]:
                for j in range(n):
                    if reach[k][j]:
                        reach[i][j] = True

    return [reach[u][v] for u, v in queries]
""",
    ),
    # ---- Time Needed to Inform All Employees (LeetCode 1376) ----
    dict(
        title="Time Needed to Inform All Employees",
        diff="M",
        lc=1376,
        slug="time-needed-to-inform-all-employees",
        prompt=(
            "A company is a tree: manager[i] is the direct manager of employee i (the head has -1). When employee i "
            "learns the news they need inform_time[i] minutes to tell all direct reports at once. Return the "
            "minutes until everyone knows, starting from head_id."
        ),
        sig="def num_of_minutes(n: int, head_id: int, manager: List[int], inform_time: List[int]) -> int:",
        fn="num_of_minutes",
        tests=[
            ((1, 0, [-1], [0]), 0),
            ((6, 2, [2, 2, -1, 2, 2, 2], [0, 0, 1, 0, 0, 0]), 1),
            ((7, 6, [1, 2, 3, 4, 5, 6, -1], [0, 6, 5, 4, 3, 2, 1]), 21),
            ((3, 0, [-1, 0, 0], [5, 0, 0]), 5),
        ],
        hints=[
            "The time an employee learns the news = sum of inform_time of all managers above them.",
            "The answer is the largest such sum over all employees.",
            "DFS/BFS down from the head carrying the accumulated time; or walk up from each employee (and memoise).",
        ],
        pattern="Longest root-to-node path sum in a tree",
        explain=(
            "Information flows along tree edges, and siblings are told simultaneously, so the total time is the "
            "maximum over root-to-leaf path sums."
        ),
        cx="O(n) time",
        brute_cx="O(n * depth) time - climb to the head from every employee",
        brute=r"""
# BRUTE FORCE: O(n * depth) time - climb to the head from every employee
def num_of_minutes(n, head_id, manager, inform_time):
    best = 0

    for employee in range(n):
        total, boss = 0, manager[employee]
        while boss != -1:  # add up every manager above this employee
            total += inform_time[boss]
            boss = manager[boss]
        best = max(best, total)

    return best
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Longest root-to-node path sum in a tree
def num_of_minutes(n, head_id, manager, inform_time):
    reports = defaultdict(list)

    for employee, boss in enumerate(manager):
        if boss != -1:
            reports[boss].append(employee)

    best, stack = 0, [(head_id, 0)]  # (employee, time at which they learn the news)

    while stack:
        employee, t = stack.pop()
        best = max(best, t)
        for report in reports[employee]:
            stack.append((report, t + inform_time[employee]))

    return best
""",
    ),
    # ---- Reorder Routes to Make All Paths Lead to the City Zero (LeetCode 1466) ----
    dict(
        title="Reorder Routes to Make All Paths Lead to the City Zero",
        diff="M",
        lc=1466,
        slug="reorder-routes-to-make-all-paths-lead-to-the-city-zero",
        prompt=(
            "n cities form a tree connected by n - 1 ONE-WAY roads connections[i] = [a, b] (from a to b). Return "
            "the minimum number of roads you must reverse so every city can reach city 0."
        ),
        sig="def min_reorder(n: int, connections: List[List[int]]) -> int:",
        fn="min_reorder",
        tests=[
            ((6, [[0, 1], [1, 3], [2, 3], [4, 0], [4, 5]]), 3),
            ((5, [[1, 0], [1, 2], [3, 2], [3, 4]]), 2),
            ((3, [[1, 0], [2, 0]]), 0),
            ((2, [[0, 1]]), 1),
        ],
        hints=[
            "Ignore directions to see the tree, then walk outwards from city 0.",
            "A road traversed from the parent to the child must point TOWARDS the parent to be correct.",
            (
                "So during the traversal, every original edge that points away from 0 (parent -> child) needs "
                "reversing: count them."
            ),
        ],
        pattern="Traverse an undirected tree, remembering the original direction",
        explain=(
            "Store each edge in both directions with a flag; when the traversal goes along an original edge (away "
            "from 0), that edge points the wrong way."
        ),
        cx="O(n) time",
        brute_cx="O(n) time - build parents with BFS, then compare every edge with its parent link",
        brute=r"""
# BRUTE FORCE: O(n) time - build parents with BFS, then compare every edge with its parent link
def min_reorder(n, connections):
    neighbours = defaultdict(list)

    for a, b in connections:
        neighbours[a].append(b)
        neighbours[b].append(a)

    parent, queue = {0: None}, deque([0])

    while queue:  # BFS records the parent of every city
        node = queue.popleft()
        for nxt in neighbours[node]:
            if nxt not in parent:
                parent[nxt] = node
                queue.append(nxt)

    # an edge a -> b is correct if b is the parent of a; otherwise it must be reversed
    return sum(1 for a, b in connections if parent[b] == a)
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Traverse an undirected tree, remembering the original direction
def min_reorder(n, connections):
    adj = defaultdict(list)

    for a, b in connections:
        adj[a].append(
            (b, 1)
        )  # travelling a -> b follows the road: it points away from 0, so it needs reversing
        adj[b].append((a, 0))

    seen, stack, flips = {0}, [0], 0

    while stack:
        node = stack.pop()
        for nxt, wrong_way in adj[node]:
            if nxt not in seen:
                seen.add(nxt)
                flips += wrong_way
                stack.append(nxt)

    return flips
""",
    ),
    # ---- Number of Enclaves (LeetCode 1020) ----
    dict(
        title="Number of Enclaves",
        diff="M",
        lc=1020,
        slug="number-of-enclaves",
        prompt=(
            "grid has 1 = land and 0 = sea. A move steps to a 4-adjacent land cell. Return the number of land cells "
            "from which you can NOT walk off the grid boundary."
        ),
        sig="def num_enclaves(grid: List[List[int]]) -> int:",
        fn="num_enclaves",
        tests=[
            (([[0, 0, 0, 0], [1, 0, 1, 0], [0, 1, 1, 0], [0, 0, 0, 0]],), 3),
            (([[0, 1, 1, 0], [0, 0, 1, 0], [0, 0, 1, 0], [0, 0, 0, 0]],), 0),
            (([[1]],), 0),
            (([[0, 0, 0], [0, 1, 0], [0, 0, 0]],), 1),
        ],
        hints=[
            "Land that touches the border can escape, and so can any land connected to it.",
            "Flood fill from every border land cell, marking what can escape.",
            "The answer is the number of land cells never reached.",
        ],
        pattern="Flood fill from the boundary inwards",
        explain=(
            "Starting from the edge avoids testing every land cell separately; one sweep marks everything that can "
            "escape."
        ),
        cx="O(R*C) time",
        brute_cx="O((R*C)^2) time - a separate search from every land cell",
        brute=r"""
# BRUTE FORCE: O((R*C)^2) time - a separate search from every land cell
def num_enclaves(grid):
    rows, cols = len(grid), len(grid[0])

    def can_escape(r, c):
        seen, stack = {(r, c)}, [(r, c)]

        while stack:
            cr, cc = stack.pop()
            if cr in (0, rows - 1) or cc in (0, cols - 1):
                return True
            for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
                if grid[nr][nc] == 1 and (nr, nc) not in seen:
                    seen.add((nr, nc))
                    stack.append((nr, nc))

        return False

    return sum(
        1 for r in range(rows) for c in range(cols) if grid[r][c] == 1 and not can_escape(r, c)
    )
""",
        solution=r"""
# OPTIMISED: O(R*C) time
# Idea: Flood fill from the boundary inwards
def num_enclaves(grid):
    rows, cols = len(grid), len(grid[0])
    grid = [row[:] for row in grid]
    stack = [
        (r, c)
        for r in range(rows)
        for c in range(cols)
        if (r in (0, rows - 1) or c in (0, cols - 1)) and grid[r][c]
    ]

    for r, c in stack:
        grid[r][c] = 0  # land that can escape

    while stack:
        cr, cc = stack.pop()
        for nr, nc in ((cr + 1, cc), (cr - 1, cc), (cr, cc + 1), (cr, cc - 1)):
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                grid[nr][nc] = 0
                stack.append((nr, nc))

    return sum(map(sum, grid))  # whatever land remains is enclosed
""",
    ),
]
