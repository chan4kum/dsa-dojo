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

from core import Node, defaultdict, deque


def _topo_ok(args, got):
    n, pre = args
    indeg, adj = [0] * n, defaultdict(list)
    for a, b in pre:
        adj[b].append(a)
        indeg[a] += 1
    q, seen = deque(i for i in range(n) if indeg[i] == 0), 0
    while q:
        u = q.popleft()
        seen += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if seen < n:
        return got == []
    if sorted(got) != list(range(n)):
        return False
    pos = {c: i for i, c in enumerate(got)}
    return all(pos[b] < pos[a] for a, b in pre)


_ORIG = []


def _build_graph(adj):
    """Adjacency list (node i has value i+1) -> Node graph; remembers originals to detect fake 'copies'."""
    _ORIG.clear()
    if not adj:
        return (None,)
    nodes = [Node(i + 1) for i in range(len(adj))]
    for i, nb in enumerate(adj):
        nodes[i].neighbors = [nodes[j - 1] for j in nb]
    _ORIG.extend(nodes)
    return (nodes[0],)


def _graph_to_adj(start):
    if start is None:
        return []
    if any(start is o for o in _ORIG):
        return "returned the ORIGINAL node, not a copy"
    seen, order, stack = {id(start): start}, [], [start]
    while stack:
        u = stack.pop()
        order.append(u)
        for v in u.neighbors:
            if any(v is o for o in _ORIG):
                return "a neighbour is an ORIGINAL node, not a copy"
            if id(v) not in seen:
                seen[id(v)] = v
                stack.append(v)
    n = max(u.val for u in order)
    adj = [[] for _ in range(n)]
    for u in order:
        adj[u.val - 1] = sorted(v.val for v in u.neighbors)
    return adj


def _alien_ok(args, got):
    words = args[0]
    letters = {c for w in words for c in w}
    adj = {c: set() for c in letters}
    bad = False
    for a, b in zip(words, words[1:]):
        if len(a) > len(b) and a.startswith(b):
            bad = True
        for x, y in zip(a, b):
            if x != y:
                adj[x].add(y)
                break
    indeg = {c: 0 for c in letters}
    for u in adj:
        for v in adj[u]:
            indeg[v] += 1
    q, seen = deque(c for c in letters if indeg[c] == 0), 0
    while q:
        u = q.popleft()
        seen += 1
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    if bad or seen < len(letters):
        return got == ""
    if not isinstance(got, str) or sorted(got) != sorted(letters):
        return False
    pos = {c: i for i, c in enumerate(got)}
    return all(pos[u] < pos[v] for u in adj for v in adj[u])


PROBLEMS = [
    # ---- Number of Provinces (LeetCode 547) ----
    dict(
        title="Number of Provinces",
        diff="M",
        lc=547,
        slug="number-of-provinces",
        prompt=(
            "isConnected[i][j] = 1 means cities i and j are directly connected (connections are symmetric and "
            "transitive through other cities). A province is a group of connected cities. Return the number of "
            "provinces."
        ),
        sig="def find_circle_num(is_connected: List[List[int]]) -> int:",
        fn="find_circle_num",
        tests=[
            (([[1, 1, 0], [1, 1, 0], [0, 0, 1]],), 2),
            (([[1, 0, 0], [0, 1, 0], [0, 0, 1]],), 3),
            (([[1]],), 1),
            (([[1, 1, 1], [1, 1, 1], [1, 1, 1]],), 1),
        ],
        hints=[
            "Cities are nodes, 1s are edges. You are counting connected components.",
            "Start a traversal from every unvisited city and mark everything it can reach.",
            (
                "Each fresh start = one new province. DFS/BFS over the matrix row, or Union-Find (answer = n - "
                "successful unions)."
            ),
        ],
        pattern="Connected components (DFS/BFS or Union-Find)",
        explain=(
            "Components partition the nodes. Every traversal launched from an unvisited node discovers exactly one "
            "whole\n        component, so the number of launches is the component count."
        ),
        cx="O(n^2) time, O(n) space",
        brute_cx="O(n^3) time - repeatedly merge label sets until nothing changes",
        brute=r"""
# BRUTE FORCE: O(n^3) time - repeatedly merge label sets until nothing changes
def find_circle_num(is_connected):
    n = len(is_connected)
    label = list(range(n))
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(n):
                if is_connected[i][j] and label[i] != label[j]:
                    m = min(label[i], label[j])
                    label[i] = label[j] = m
                    changed = True
    return len(set(label))
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n) space
# Idea: Connected components (DFS/BFS or Union-Find)
def find_circle_num(is_connected):
    n, seen, count = len(is_connected), set(), 0

    def dfs(u):
        seen.add(u)
        for v in range(n):
            if is_connected[u][v] and v not in seen:
                dfs(v)

    for i in range(n):
        if i not in seen:
            count += 1
            dfs(i)
    return count
""",
    ),
    # ---- Max Area of Island (LeetCode 695) ----
    dict(
        title="Max Area of Island",
        diff="M",
        lc=695,
        slug="max-area-of-island",
        prompt=(
            "Grid of 0/1. An island is a group of 1s connected 4-directionally. Return the largest island's area (0 "
            "if none)."
        ),
        sig="def max_area_of_island(grid: List[List[int]]) -> int:",
        fn="max_area_of_island",
        tests=[
            (([[1, 1, 0, 0], [1, 0, 0, 1], [0, 0, 1, 1]],), 3),
            (([[0]],), 0),
            (([[1]],), 1),
            (([[1, 1, 1], [0, 1, 0], [1, 1, 1]],), 7),
            (([[0, 0], [0, 0]],), 0),
        ],
        hints=[
            "Same as 'Number of Islands', but you must measure each island.",
            "Let DFS return the size of the component it explores.",
            "dfs(r,c) = 1 + sum of dfs on the 4 neighbours, after marking (r,c) visited (set to 0).",
        ],
        pattern="Grid DFS returning component size (flood fill)",
        explain="Mark visited by overwriting the cell (or use a set) so each cell is counted once. Total work O(R*C).",
        cx="O(R*C) time",
        brute_cx="O((R*C)^2) time - flood fill each cell with a fresh visited set",
        brute=r"""
# BRUTE FORCE: O((R*C)^2) time - flood fill each cell with a fresh visited set
def max_area_of_island(grid):
    R, C = len(grid), len(grid[0])
    best = 0
    for r in range(R):
        for c in range(C):
            if grid[r][c] == 1:
                seen, stack = {(r, c)}, [(r, c)]
                while stack:
                    x, y = stack.pop()
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if (
                            0 <= nx < R
                            and 0 <= ny < C
                            and grid[nx][ny] == 1
                            and (nx, ny) not in seen
                        ):
                            seen.add((nx, ny))
                            stack.append((nx, ny))
                best = max(best, len(seen))
    return best
""",
        solution=r"""
# OPTIMISED: O(R*C) time
# Idea: Grid DFS returning component size (flood fill)
def max_area_of_island(grid):
    R, C = len(grid), len(grid[0])

    def dfs(r, c):
        if not (0 <= r < R and 0 <= c < C) or grid[r][c] != 1:
            return 0
        grid[r][c] = 0
        return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)

    return max(dfs(r, c) for r in range(R) for c in range(C))
""",
    ),
    # ---- Pacific Atlantic Water Flow (LeetCode 417) ----
    dict(
        title="Pacific Atlantic Water Flow",
        diff="M",
        lc=417,
        slug="pacific-atlantic-water-flow",
        prompt=(
            "heights[r][c] is a cell's height. Water flows to a neighbour of equal or lower height. The Pacific "
            "touches the top and left edges, the Atlantic the bottom and right. Return all cells from which water "
            "can reach BOTH oceans (any order)."
        ),
        sig="def pacific_atlantic(heights: List[List[int]]) -> List[List[int]]:",
        fn="pacific_atlantic",
        compare="unordered",
        tests=[
            (
                ([[1, 2, 2, 3, 5], [3, 2, 3, 4, 4], [2, 4, 5, 3, 1], [6, 7, 1, 4, 5], [5, 1, 1, 2, 4]],),
                [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]],
            ),
            (([[1]],), [[0, 0]]),
            (([[1, 1], [1, 1]],), [[0, 0], [0, 1], [1, 0], [1, 1]]),
        ],
        hints=[
            "Simulating water from every cell is O((RC)^2).",
            "Reverse the question: which cells can the ocean 'climb' into?",
            "BFS/DFS from all ocean-border cells going UPHILL (>=). Intersect the two reachable sets.",
        ],
        pattern="Reverse the direction + multi-source search from the borders",
        explain=(
            "'Can water get from X to the ocean' for all X is the same as 'what can be reached from the ocean going "
            "the\n        opposite way'. Two multi-source searches, one set intersection: O(R*C)."
        ),
        cx="O(R*C) time",
        brute_cx="O((R*C)^2) time - flood downhill from every cell",
        brute=r"""
# BRUTE FORCE: O((R*C)^2) time - flood downhill from every cell
def pacific_atlantic(heights):
    R, C = len(heights), len(heights[0])
    out = []
    for r in range(R):
        for c in range(C):
            seen, stack, pac, atl = {(r, c)}, [(r, c)], False, False
            while stack:
                x, y = stack.pop()
                if x == 0 or y == 0:
                    pac = True
                if x == R - 1 or y == C - 1:
                    atl = True
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if (
                        0 <= nx < R
                        and 0 <= ny < C
                        and (nx, ny) not in seen
                        and heights[nx][ny] <= heights[x][y]
                    ):
                        seen.add((nx, ny))
                        stack.append((nx, ny))
            if pac and atl:
                out.append([r, c])
    return out
""",
        solution=r"""
# OPTIMISED: O(R*C) time
# Idea: Reverse the direction + multi-source search from the borders
def pacific_atlantic(heights):
    R, C = len(heights), len(heights[0])

    def reach(starts):
        seen, q = set(starts), deque(starts)
        while q:
            r, c = q.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if (
                    0 <= nr < R
                    and 0 <= nc < C
                    and (nr, nc) not in seen
                    and heights[nr][nc] >= heights[r][c]
                ):
                    seen.add((nr, nc))
                    q.append((nr, nc))
        return seen

    pac = reach([(0, c) for c in range(C)] + [(r, 0) for r in range(1, R)])
    atl = reach([(R - 1, c) for c in range(C)] + [(r, C - 1) for r in range(R - 1)])
    return [list(p) for p in pac & atl]
""",
    ),
    # ---- Surrounded Regions (LeetCode 130) ----
    dict(
        title="Surrounded Regions",
        diff="M",
        lc=130,
        slug="surrounded-regions",
        prompt=(
            "Board of 'X' and 'O'. Capture every region of 'O's that is completely surrounded by 'X' (i.e. cannot "
            "reach the border): flip those O to X, in place."
        ),
        sig="def solve(board: List[List[str]]) -> None:",
        fn="solve",
        inplace=0,
        tests=[
            (
                ([["X", "X", "X", "X"], ["X", "O", "O", "X"], ["X", "X", "O", "X"], ["X", "O", "X", "X"]],),
                [["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "X", "X", "X"], ["X", "O", "X", "X"]],
            ),
            (([["X"]],), [["X"]]),
            (([["O", "O"], ["O", "O"]],), [["O", "O"], ["O", "O"]]),
            (
                ([["X", "O", "X"], ["X", "O", "X"], ["X", "X", "X"]],),
                [["X", "O", "X"], ["X", "O", "X"], ["X", "X", "X"]],
            ),
        ],
        hints=[
            "Deciding for each O whether it is enclosed means a search per cell - wasteful.",
            "Which O's are definitely SAFE?",
            (
                "Those connected to a border O. Mark them from the border (DFS), flip all remaining O to X, then "
                "restore the marks."
            ),
        ],
        pattern="Invert the question: mark what is safe from the border, then flip the rest",
        explain=(
            "Same trick as Pacific Atlantic: start from the known boundary condition. Three passes: mark safe cells "
            "('S'),\n        turn the other O's into X, turn 'S' back to O."
        ),
        cx="O(R*C) time",
        brute_cx="O((R*C)^2) time - for every O search whether it can reach the border",
        brute=r"""
# BRUTE FORCE: O((R*C)^2) time - for every O search whether it can reach the border
def solve(board):
    R, C = len(board), len(board[0])
    flip = []
    for r in range(R):
        for c in range(C):
            if board[r][c] == "O":
                seen, stack, escapes = {(r, c)}, [(r, c)], False
                while stack:
                    x, y = stack.pop()
                    if x in (0, R - 1) or y in (0, C - 1):
                        escapes = True
                    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                        nx, ny = x + dx, y + dy
                        if (
                            0 <= nx < R
                            and 0 <= ny < C
                            and board[nx][ny] == "O"
                            and (nx, ny) not in seen
                        ):
                            seen.add((nx, ny))
                            stack.append((nx, ny))
                if not escapes:
                    flip.append((r, c))
    for r, c in flip:
        board[r][c] = "X"
""",
        solution=r"""
# OPTIMISED: O(R*C) time
# Idea: Invert the question: mark what is safe from the border, then flip the rest
def solve(board):
    R, C = len(board), len(board[0])

    def mark(r, c):
        if 0 <= r < R and 0 <= c < C and board[r][c] == "O":
            board[r][c] = "S"
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                mark(r + dr, c + dc)

    for r in range(R):
        mark(r, 0)
        mark(r, C - 1)
    for c in range(C):
        mark(0, c)
        mark(R - 1, c)
    for r in range(R):
        for c in range(C):
            board[r][c] = "O" if board[r][c] == "S" else "X"
""",
    ),
    # ---- 01 Matrix (LeetCode 542) ----
    dict(
        title="01 Matrix",
        diff="M",
        lc=542,
        slug="01-matrix",
        prompt=(
            "For each cell of a 0/1 matrix return the distance to the nearest 0 (adjacent cells are distance 1; "
            "moves are 4-directional)."
        ),
        sig="def update_matrix(mat: List[List[int]]) -> List[List[int]]:",
        fn="update_matrix",
        tests=[
            (([[0, 0, 0], [0, 1, 0], [0, 0, 0]],), [[0, 0, 0], [0, 1, 0], [0, 0, 0]]),
            (([[0, 0, 0], [0, 1, 0], [1, 1, 1]],), [[0, 0, 0], [0, 1, 0], [1, 2, 1]]),
            (([[0]],), [[0]]),
            (([[0, 1, 1, 1]],), [[0, 1, 2, 3]]),
        ],
        hints=[
            "Running a BFS from every 1 is far too slow.",
            "Flip the viewpoint: start from ALL zeros at once.",
            (
                "Multi-source BFS: queue every 0 with distance 0; the first time a cell is reached is its shortest "
                "distance."
            ),
        ],
        pattern="Multi-source BFS (all sources start in the queue together)",
        explain=(
            "BFS explores in rings of increasing distance. Seeding it with every source simultaneously computes "
            "the\n        distance to the NEAREST source for every cell in one O(R*C) sweep."
        ),
        cx="O(R*C) time",
        brute_cx="O((R*C)^2) time - for each cell scan every 0 (Manhattan distance)",
        brute=r"""
# BRUTE FORCE: O((R*C)^2) time - for each cell scan every 0 (Manhattan distance)
def update_matrix(mat):
    R, C = len(mat), len(mat[0])
    zeros = [(r, c) for r in range(R) for c in range(C) if mat[r][c] == 0]
    return [
        [min(abs(r - zr) + abs(c - zc) for zr, zc in zeros) for c in range(C)] for r in range(R)
    ]
""",
        solution=r"""
# OPTIMISED: O(R*C) time
# Idea: Multi-source BFS (all sources start in the queue together)
def update_matrix(mat):
    R, C = len(mat), len(mat[0])
    dist = [[-1] * C for _ in range(R)]
    q = deque()
    for r in range(R):
        for c in range(C):
            if mat[r][c] == 0:
                dist[r][c] = 0
                q.append((r, c))
    while q:
        r, c = q.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and dist[nr][nc] == -1:
                dist[nr][nc] = dist[r][c] + 1
                q.append((nr, nc))
    return dist
""",
    ),
    # ---- Course Schedule II (LeetCode 210) ----
    dict(
        title="Course Schedule II",
        diff="M",
        lc=210,
        slug="course-schedule-ii",
        prompt=(
            "There are n courses (0..n-1); prerequisites [a, b] means take b before a. Return an order in which you "
            "can finish all courses, or [] if impossible (any valid order is accepted)."
        ),
        sig="def find_order(num_courses: int, prerequisites: List[List[int]]) -> List[int]:",
        fn="find_order",
        check=_topo_ok,
        tests=[
            ((2, [[1, 0]]), [0, 1]),
            ((4, [[1, 0], [2, 0], [3, 1], [3, 2]]), [0, 1, 2, 3]),
            ((1, []), [0]),
            ((2, [[1, 0], [0, 1]]), []),
            ((3, []), [0, 1, 2]),
        ],
        hints=[
            "This is Course Schedule I, but you must output the order, not just True/False.",
            "Which courses can be taken first? Those with no remaining prerequisites.",
            (
                "Kahn's algorithm: queue of in-degree-0 nodes; pop, append to order, decrement neighbours; if the "
                "order has fewer than n nodes there is a cycle."
            ),
        ],
        pattern="Topological sort (Kahn's BFS on in-degrees)",
        explain=(
            "Each popped node has all its prerequisites already placed, so the order built is valid. Leftover nodes "
            "all lie\n        on or behind a cycle - nothing could unlock them."
        ),
        cx="O(V+E) time",
        brute_cx="O(V^2 + V*E) time - repeatedly scan for a course whose prerequisites are all taken",
        brute=r"""
# BRUTE FORCE: O(V^2 + V*E) time - repeatedly scan for a course whose prerequisites are all taken
def find_order(num_courses, prerequisites):
    taken, order = set(), []
    while len(order) < num_courses:
        for c in range(num_courses):
            if c not in taken and all(b in taken for a, b in prerequisites if a == c):
                taken.add(c)
                order.append(c)
                break
        else:
            return []
    return order
""",
        solution=r"""
# OPTIMISED: O(V+E) time
# Idea: Topological sort (Kahn's BFS on in-degrees)
def find_order(num_courses, prerequisites):
    adj, indeg = defaultdict(list), [0] * num_courses
    for a, b in prerequisites:
        adj[b].append(a)
        indeg[a] += 1
    q = deque(i for i in range(num_courses) if indeg[i] == 0)
    order = []
    while q:
        u = q.popleft()
        order.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return order if len(order) == num_courses else []
""",
    ),
    # ---- Number of Connected Components in an Undirected Graph (LeetCode 323) ----
    dict(
        title="Number of Connected Components in an Undirected Graph",
        diff="M",
        lc=323,
        slug="number-of-connected-components-in-an-undirected-graph",
        prompt="n nodes labelled 0..n-1 and a list of undirected edges. Return the number of connected components.",
        sig="def count_components(n: int, edges: List[List[int]]) -> int:",
        fn="count_components",
        tests=[
            ((5, [[0, 1], [1, 2], [3, 4]]), 2),
            ((5, [[0, 1], [1, 2], [2, 3], [3, 4]]), 1),
            ((3, []), 3),
            ((1, []), 1),
            ((4, [[0, 1], [2, 3], [1, 2]]), 1),
        ],
        hints=[
            "Start with n components. What happens to the count when an edge joins two different components?",
            "It drops by one; an edge inside a component changes nothing.",
            "Union-Find: components = n - (number of successful unions).",
        ],
        pattern="Union-Find (disjoint set union) with path compression",
        explain=(
            "find(x) returns the representative of x's set; union merges two sets if their representatives "
            "differ.\n        Path compression + union by size make each operation almost O(1) (inverse Ackermann)."
        ),
        cx="O((V+E) alpha(V)) time",
        brute_cx="O(V*E) time - relabel components after every edge",
        brute=r"""
# BRUTE FORCE: O(V*E) time - relabel components after every edge
def count_components(n, edges):
    label = list(range(n))
    for a, b in edges:
        la, lb = label[a], label[b]
        if la != lb:
            label = [la if x == lb else x for x in label]
    return len(set(label))
""",
        solution=r"""
# OPTIMISED: O((V+E) alpha(V)) time
# Idea: Union-Find (disjoint set union) with path compression
def count_components(n, edges):
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]  # path compression (halving)
            x = parent[x]
        return x

    comps = n
    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            comps -= 1
    return comps
""",
    ),
    # ---- Graph Valid Tree (LeetCode 261) ----
    dict(
        title="Graph Valid Tree",
        diff="M",
        lc=261,
        slug="graph-valid-tree",
        prompt="Given n nodes and undirected edges, return True if the edges form a valid tree (connected, no cycles).",
        sig="def valid_tree(n: int, edges: List[List[int]]) -> bool:",
        fn="valid_tree",
        tests=[
            ((5, [[0, 1], [0, 2], [0, 3], [1, 4]]), True),
            ((5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]), False),
            ((1, []), True),
            ((4, [[0, 1], [2, 3]]), False),
            ((2, [[0, 1], [1, 0]]), False),
        ],
        hints=[
            "Characterise a tree: how many edges must it have?",
            "Exactly n - 1 edges. With n-1 edges, 'connected' and 'acyclic' are equivalent.",
            (
                "Check len(edges) == n-1, then verify connectivity (DFS from 0 reaches n nodes) or that no union "
                "fails in Union-Find."
            ),
        ],
        pattern="Tree = connected + (n-1) edges; Union-Find cycle detection",
        explain=(
            "A union that finds both endpoints already in the same set means a cycle. With exactly n-1 edges and no "
            "cycle the\n        graph is automatically connected."
        ),
        cx="O(n alpha(n)) time",
        brute_cx="O(n + E) time - DFS with parent tracking for cycles plus a connectivity count",
        brute=r"""
# BRUTE FORCE: O(n + E) time - DFS with parent tracking for cycles plus a connectivity count
def valid_tree(n, edges):
    adj = defaultdict(list)
    for a, b in edges:
        adj[a].append(b)
        adj[b].append(a)
    seen = set()

    def dfs(u, parent):
        seen.add(u)
        for v in adj[u]:
            if v == parent and adj[u].count(v) == 1:
                continue
            if v in seen or not dfs(v, u):
                return False
        return True

    return dfs(0, -1) and len(seen) == n
""",
        solution=r"""
# OPTIMISED: O(n alpha(n)) time
# Idea: Tree = connected + (n-1) edges; Union-Find cycle detection
def valid_tree(n, edges):
    if len(edges) != n - 1:
        return False
    parent = list(range(n))

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            return False
        parent[ra] = rb
    return True
""",
    ),
    # ---- Cheapest Flights Within K Stops (LeetCode 787) ----
    dict(
        title="Cheapest Flights Within K Stops",
        diff="M",
        lc=787,
        slug="cheapest-flights-within-k-stops",
        prompt=(
            "flights[i] = [from, to, price]. Return the cheapest price from src to dst with at most k stops (k+1 "
            "flights), or -1."
        ),
        sig="def find_cheapest_price(n: int, flights: List[List[int]], src: int, dst: int, k: int) -> int:",
        fn="find_cheapest_price",
        tests=[
            ((4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1), 700),
            ((3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1), 200),
            ((3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0), 500),
            ((2, [], 0, 1, 5), -1),
            ((3, [[0, 1, 5], [1, 2, 5]], 0, 2, 0), -1),
        ],
        hints=[
            "Dijkstra minimises cost but ignores the stop limit. What extra dimension does the state need?",
            "Cheapest path using at most j flights, for j = 1..k+1.",
            (
                "Bellman-Ford for k+1 rounds, relaxing from a COPY of the previous round's distances so each round "
                "adds exactly one flight."
            ),
        ],
        pattern="Bellman-Ford with a bounded number of edges (layered relaxation)",
        explain=(
            "After round j, dist[v] is the cheapest cost to v using at most j flights. Reading from the previous "
            "round's\n        snapshot prevents chaining two flights in one round."
        ),
        cx="O(k * E) time, O(V) space",
        brute_cx="exponential - DFS over every path with at most k+1 flights",
        brute=r"""
# BRUTE FORCE: exponential - DFS over every path with at most k+1 flights
def find_cheapest_price(n, flights, src, dst, k):
    adj = defaultdict(list)
    for a, b, p in flights:
        adj[a].append((b, p))
    best = [float("inf")]

    def go(u, flights_left, cost):
        if u == dst:
            best[0] = min(best[0], cost)
            return
        if flights_left == 0:
            return
        for v, p in adj[u]:
            go(v, flights_left - 1, cost + p)

    go(src, k + 1, 0)
    return -1 if best[0] == float("inf") else best[0]
""",
        solution=r"""
# OPTIMISED: O(k * E) time, O(V) space
# Idea: Bellman-Ford with a bounded number of edges (layered relaxation)
def find_cheapest_price(n, flights, src, dst, k):
    INF = float("inf")
    dist = [INF] * n
    dist[src] = 0
    for _ in range(k + 1):
        nxt = dist[:]
        for a, b, p in flights:
            if dist[a] + p < nxt[b]:
                nxt[b] = dist[a] + p
        dist = nxt
    return -1 if dist[dst] == INF else dist[dst]
""",
    ),
    # ---- Keys and Rooms (LeetCode 841) ----
    dict(
        title="Keys and Rooms",
        diff="M",
        lc=841,
        slug="keys-and-rooms",
        prompt=(
            "Room 0 is unlocked. rooms[i] lists the keys found in room i (key j opens room j). Return True if you "
            "can visit every room."
        ),
        sig="def can_visit_all_rooms(rooms: List[List[int]]) -> bool:",
        fn="can_visit_all_rooms",
        tests=[
            (([[1], [2], [3], []],), True),
            (([[1, 3], [3, 0, 1], [2], [0]],), False),
            (([[]],), True),
            (([[2], [], [1]],), True),
        ],
        hints=[
            "Rooms are nodes, keys are directed edges.",
            "Which rooms are reachable from room 0?",
            "DFS/BFS from 0; answer is len(visited) == n.",
        ],
        pattern="Reachability in a directed graph",
        explain=(
            "Pure graph traversal - the disguise is the story. Always ask: what are the nodes and what are the edges?"
        ),
        cx="O(V+E) time",
        brute_cx="O(V*E) time - keep collecting keys until nothing new opens",
        brute=r"""
# BRUTE FORCE: O(V*E) time - keep collecting keys until nothing new opens
def can_visit_all_rooms(rooms):
    opened = {0}
    changed = True
    while changed:
        changed = False
        for r in list(opened):
            for key in rooms[r]:
                if key not in opened:
                    opened.add(key)
                    changed = True
    return len(opened) == len(rooms)
""",
        solution=r"""
# OPTIMISED: O(V+E) time
# Idea: Reachability in a directed graph
def can_visit_all_rooms(rooms):
    seen, stack = {0}, [0]
    while stack:
        for key in rooms[stack.pop()]:
            if key not in seen:
                seen.add(key)
                stack.append(key)
    return len(seen) == len(rooms)
""",
    ),
    # ---- Clone Graph (LeetCode 133) ----
    dict(
        title="Clone Graph",
        diff="M",
        lc=133,
        slug="clone-graph",
        prompt=(
            "Return a deep copy (clone) of a connected undirected graph given by a reference to one node. Each Node "
            "has `val` and a list `neighbors`. (Tests describe the graph as an adjacency list where node i has "
            "value i+1.)"
        ),
        sig="def clone_graph(node: Optional[Node]) -> Optional[Node]:",
        fn="clone_graph",
        adapt_in=lambda a: _build_graph(a[0]),
        adapt_out=lambda n: _graph_to_adj(n),
        tests=[
            (([[2, 4], [1, 3], [2, 4], [1, 3]],), [[2, 4], [1, 3], [2, 4], [1, 3]]),
            (([[]],), [[]]),
            (([],), []),
            (([[2], [1]],), [[2], [1]]),
            (([[2, 3], [1, 3], [1, 2]],), [[2, 3], [1, 3], [1, 2]]),
        ],
        hints=[
            (
                "A deep copy must create NEW nodes and reproduce every edge, including cycles. What goes wrong if "
                "you recurse naively on a cycle?"
            ),
            "You would loop forever - you need to remember which nodes are already cloned.",
            (
                "dict old_node -> new_node. DFS/BFS: if the neighbour is not in the dict, clone and visit it; "
                "always append the clone of the neighbour to the clone's neighbour list."
            ),
        ],
        pattern="Graph traversal + memo dict (old -> new) to handle cycles",
        explain=(
            "The dict does double duty: it is the 'visited' set and the lookup that lets a cycle point back to "
            "an\n        already-created clone. Create the clone BEFORE recursing so the cycle can find it."
        ),
        cx="O(V+E) time and space",
        brute_cx="O(V+E) time - two passes: collect all nodes, create clones, then wire edges",
        brute="""
def clone_graph(node):
    if not node:
        return None
    nodes, stack = {node}, [node]
    while stack:
        u = stack.pop()
        for v in u.neighbors:
            if v not in nodes:
                nodes.add(v)
                stack.append(v)
    copy_of = {u: Node(u.val) for u in nodes}
    for u in nodes:
        copy_of[u].neighbors = [copy_of[v] for v in u.neighbors]
    return copy_of[node]
""",
        solution="""
def clone_graph(node):
    if not node:
        return None
    clones = {node: Node(node.val)}
    stack = [node]
    while stack:
        u = stack.pop()
        for v in u.neighbors:
            if v not in clones:
                clones[v] = Node(v.val)
                stack.append(v)
            clones[u].neighbors.append(clones[v])
    return clones[node]
""",
    ),
    # ---- Alien Dictionary (LeetCode 269) ----
    dict(
        title="Alien Dictionary",
        diff="H",
        lc=269,
        slug="alien-dictionary",
        prompt=(
            "Words are sorted lexicographically according to an unknown alphabet. Return a string with the letters "
            "in a valid order, or '' if the ordering is inconsistent (a cycle, or a longer word appearing before "
            "its own prefix). Any valid order is accepted."
        ),
        sig="def alien_order(words: List[str]) -> str:",
        fn="alien_order",
        check=_alien_ok,
        tests=[
            ((["wrt", "wrf", "er", "ett", "rftt"],), "wertf"),
            ((["z", "x"],), "zx"),
            ((["z", "x", "z"],), ""),
            ((["abc", "ab"],), ""),
            ((["z", "z"],), "z"),
            ((["ab", "adc"],), "abcd"),
        ],
        hints=[
            "Which pairs of letters give you ORDER information?",
            "Only the first differing letter of two adjacent words: that gives an edge a -> b.",
            (
                "Build the graph, then topologically sort (Kahn). If not all letters are output there is a cycle -> "
                "''. Also check the prefix case ('abc' before 'ab')."
            ),
        ],
        pattern="Derive a graph from the data, then topological sort",
        explain=(
            "The real difficulty is modelling: adjacent words only; first mismatch only; letters that never appear "
            "in an\n        edge still belong in the answer; the prefix trap. After that it is Course Schedule II."
        ),
        cx="O(total characters) time",
        brute_cx="O(k! * n * L) time - try every permutation of the letters",
        brute="""
def alien_order(words):
    letters = sorted({c for w in words for c in w})
    for perm in itertools.permutations(letters):
        rank = {c: i for i, c in enumerate(perm)}
        keys = [[rank[c] for c in w] for w in words]
        if keys == sorted(keys):
            return "".join(perm)
    return ""
""",
        solution="""
def alien_order(words):
    adj = {c: set() for w in words for c in w}
    for a, b in zip(words, words[1:]):
        if len(a) > len(b) and a.startswith(b):
            return ""
        for x, y in zip(a, b):
            if x != y:
                adj[x].add(y)
                break
    indeg = {c: 0 for c in adj}
    for u in adj:
        for v in adj[u]:
            indeg[v] += 1
    q = deque(c for c in adj if indeg[c] == 0)
    out = []
    while q:
        u = q.popleft()
        out.append(u)
        for v in adj[u]:
            indeg[v] -= 1
            if indeg[v] == 0:
                q.append(v)
    return "".join(out) if len(out) == len(adj) else ""
""",
    ),
    # ---- Word Search II (LeetCode 212) ----
    dict(
        title="Word Search II",
        diff="H",
        lc=212,
        slug="word-search-ii",
        prompt=(
            "Given a board of letters and a list of words, return all words that can be formed by paths of adjacent "
            "cells (each cell at most once per word)."
        ),
        sig="def find_words(board: List[List[str]], words: List[str]) -> List[str]:",
        fn="find_words",
        compare="unordered",
        tests=[
            (
                (
                    [["o", "a", "a", "n"], ["e", "t", "a", "e"], ["i", "h", "k", "r"], ["i", "f", "l", "v"]],
                    ["oath", "pea", "eat", "rain"],
                ),
                ["eat", "oath"],
            ),
            (([["a", "b"], ["c", "d"]], ["abcb"]), []),
            (([["a"]], ["a"]), ["a"]),
            (([["a", "a"]], ["aaa"]), []),
        ],
        hints=[
            "Running Word Search I once per word repeats the same board exploration many times.",
            "Search the board ONCE for all words at the same time. Which structure shares prefixes?",
            (
                "Build a trie of the words, DFS from every cell following trie edges; when a node marks a word, "
                "record it. Prune dead trie branches."
            ),
        ],
        pattern="Trie + grid DFS (search many words in one pass)",
        explain=(
            "A DFS path is a growing prefix; the trie tells you instantly whether ANY word starts with that prefix, "
            "so\n        hopeless paths are abandoned immediately and shared prefixes are explored once."
        ),
        cx="O(R*C*4^L) worst case, far less with pruning",
        brute_cx="O(W * R*C*4^L) - run Word Search I for every word",
        brute="""
def find_words(board, words):
    R, C = len(board), len(board[0])
    def exist(word):
        def go(r, c, i, path):
            if board[r][c] != word[i]:
                return False
            if i == len(word) - 1:
                return True
            path = path | {(r, c)}
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < R and 0 <= nc < C and (nr, nc) not in path and go(nr, nc, i + 1, path):
                    return True
            return False
        return any(go(r, c, 0, frozenset()) for r in range(R) for c in range(C))
    return [w for w in words if exist(w)]
""",
        solution="""
def find_words(board, words):
    root = {}
    for w in words:
        node = root
        for ch in w:
            node = node.setdefault(ch, {})
        node["$"] = w
    R, C = len(board), len(board[0])
    found = []
    def dfs(r, c, parent):
        ch = board[r][c]
        node = parent[ch]
        word = node.pop("$", None)
        if word:
            found.append(word)
        board[r][c] = "#"
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < R and 0 <= nc < C and board[nr][nc] in node:
                dfs(nr, nc, node)
        board[r][c] = ch
        if not node:                      # prune exhausted branch
            del parent[ch]
    for r in range(R):
        for c in range(C):
            if board[r][c] in root:
                dfs(r, c, root)
    return found
""",
    ),
]
