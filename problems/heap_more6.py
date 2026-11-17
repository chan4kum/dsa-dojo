"""extra batch of Heap / Priority Queue problems - the problem bank for the "heap" topic (batch 6).

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Smallest Range Covering Elements from K Lists (LeetCode 632) ----
    dict(
        title="Smallest Range Covering Elements from K Lists",
        diff="H",
        lc=632,
        slug="smallest-range-covering-elements-from-k-lists",
        prompt=(
            "nums holds k lists of integers, each sorted in non-decreasing order. Find the SMALLEST range [a, b] "
            "that contains at least one number from each of the k lists. Range [a, b] is smaller than [c, d] if b - "
            "a < d - c, or if b - a == d - c and a < c. Return the range as [a, b]."
        ),
        sig="def smallest_range(nums: List[List[int]]) -> List[int]:",
        fn="smallest_range",
        tests=[
            (([[4, 10, 15, 24, 26], [0, 9, 12, 20], [5, 18, 22, 30]],), [20, 24]),
            (([[1, 2, 3], [1, 2, 3], [1, 2, 3]],), [1, 1]),
            (([[1]],), [1, 1]),
            (([[1, 5], [2, 3]],), [1, 2]),
        ],
        hints=[
            (
                "Brute force: the range starts and ends at some element of some list. Try all pairs of values and "
                "test every list."
            ),
            (
                "Take one element from each list - the range they span is [smallest, largest]. Moving the SMALLEST "
                "one to the next element in its list is the only move that can shrink the range."
            ),
            (
                "Keep the current smallest elements of all lists in a min-heap and track the current maximum. Pop "
                "the minimum, record the range if it is the best so far, push the next element of the same list. "
                "Stop when one list runs out."
            ),
        ],
        pattern="K-way merge with a min-heap and a running maximum",
        explain=(
            "At every moment we hold one element per list. The best range containing them is [min, max]. To find "
            "something better we must increase the minimum, and the only way is to advance the list the minimum "
            "came from; the heap gives the minimum quickly and we update the maximum with the new element. Once a "
            "list is exhausted no later range can cover it, so we stop. The brute force tries every pair of "
            "candidate endpoints."
        ),
        cx="O(N log k) time for N elements, O(k) space",
        brute_cx="O(N^2 * N) time - every pair of values checked against every list",
        brute=r"""
# BRUTE FORCE: O(N^2 * N) time - every pair of values checked against every list
def smallest_range(nums):
    values = sorted({x for lst in nums for x in lst})
    best = None
    for lo in values:
        for hi in values:
            if hi < lo:
                continue
            if all(any(lo <= x <= hi for x in lst) for lst in nums):
                cand = (hi - lo, lo)
                if best is None or cand < best:
                    best = cand
    return [best[1], best[1] + best[0]]
""",
        solution=r"""
# OPTIMISED: O(N log k) time for N elements, O(k) space
# Idea: K-way merge with a min-heap and a running maximum
def smallest_range(nums):
    heap = [(lst[0], i, 0) for i, lst in enumerate(nums)]
    heapq.heapify(heap)
    high = max(lst[0] for lst in nums)
    best = [heap[0][0], high]
    while True:
        low, i, j = heapq.heappop(heap)
        if high - low < best[1] - best[0]:
            best = [low, high]
        if j + 1 == len(nums[i]):
            return best
        nxt = nums[i][j + 1]
        high = max(high, nxt)
        heapq.heappush(heap, (nxt, i, j + 1))
""",
    ),
    # ---- Maximum Number of Eaten Apples (LeetCode 1705) ----
    dict(
        title="Maximum Number of Eaten Apples",
        diff="M",
        lc=1705,
        slug="maximum-number-of-eaten-apples",
        prompt=(
            "An apple tree grows apples[i] apples on day i that stay fresh for days[i] days (they can be eaten on "
            "days i .. i + days[i] - 1). On days with no apples growth, apples[i] = 0 and days[i] = 0. You may eat "
            "at most ONE apple per day and may keep eating after day n - 1 while fresh apples remain. Return the "
            "maximum number of apples you can eat."
        ),
        sig="def eaten_apples(apples: List[int], days: List[int]) -> int:",
        fn="eaten_apples",
        tests=[
            (([1, 2, 3, 5, 2], [3, 2, 1, 4, 2]), 7),
            (([3, 0, 0, 0, 0, 2], [3, 0, 0, 0, 0, 2]), 5),
            (([1], [1]), 1),
            (([0], [5]), 0),
        ],
        hints=[
            (
                "Each day, eat the fresh apple that will rot SOONEST - delaying an apple that is about to expire "
                "wastes it."
            ),
            (
                "Store batches as (expiry day, count) in a min-heap ordered by expiry. Add the new batch each day "
                "and discard batches that have already expired."
            ),
            (
                "Eat one apple from the top batch (decrement its count and drop the batch at zero). Keep looping "
                "after the last growth day while the heap is not empty."
            ),
        ],
        pattern="Greedy with a min-heap on expiry date",
        explain=(
            "Among the apples you can eat today, choosing the one that expires first never hurts (exchange "
            "argument), so the problem is simulating that rule fast. A heap of batches keyed by expiry day returns "
            "the earliest-expiring batch in O(log n). The brute force uses a dictionary and scans it for the "
            "smallest expiry each day."
        ),
        cx="O((n + total days) log n) time, O(n) space",
        brute_cx="O(days * batches) time - scan all batches for the soonest expiry each day",
        brute=r"""
# BRUTE FORCE: O(days * batches) time - scan all batches for the soonest expiry each day
def eaten_apples(apples, days):
    stock = {}
    eaten = 0
    day = 0
    while day < len(apples) or stock:
        if day < len(apples) and apples[day] > 0:
            expiry = day + days[day]
            stock[expiry] = stock.get(expiry, 0) + apples[day]
        for expiry in [e for e in stock if e <= day]:
            del stock[expiry]
        if stock:
            soonest = min(stock)
            stock[soonest] -= 1
            eaten += 1
            if stock[soonest] == 0:
                del stock[soonest]
        day += 1
    return eaten
""",
        solution=r"""
# OPTIMISED: O((n + total days) log n) time, O(n) space
# Idea: Greedy with a min-heap on expiry date
def eaten_apples(apples, days):
    heap = []
    eaten = 0
    day = 0
    while day < len(apples) or heap:
        if day < len(apples) and apples[day] > 0:
            heapq.heappush(heap, [day + days[day], apples[day]])
        while heap and heap[0][0] <= day:
            heapq.heappop(heap)
        if heap:
            heap[0][1] -= 1
            eaten += 1
            if heap[0][1] == 0:
                heapq.heappop(heap)
        day += 1
    return eaten
""",
    ),
    # ---- Maximum Score From Removing Stones (LeetCode 1753) ----
    dict(
        title="Maximum Score From Removing Stones",
        diff="M",
        lc=1753,
        slug="maximum-score-from-removing-stones",
        prompt=(
            "You have three piles with a, b and c stones. Each turn take one stone from each of two DIFFERENT "
            "non-empty piles and score 1 point. The game ends when fewer than two piles are non-empty. Return the "
            "maximum score."
        ),
        sig="def maximum_score(a: int, b: int, c: int) -> int:",
        fn="maximum_score",
        tests=[
            ((2, 4, 6), 6),
            ((4, 4, 6), 7),
            ((1, 8, 8), 8),
            ((1, 1, 1), 1),
        ],
        hints=[
            "Greedy: always take from the two LARGEST piles - emptying a pile early is what ends the game.",
            "Simulating that needs a heap (or sorting three numbers) each turn, which is O(total stones).",
            (
                "Closed form: if the largest pile is at least the sum of the other two, only the smaller two can be "
                "used up against it, so the score is a + b + c - max. Otherwise stones can be paired off almost "
                "perfectly: floor((a + b + c) / 2). So the answer is min((a + b + c) // 2, a + b + c - max)."
            ),
        ],
        pattern="Greedy simulation turned into a closed formula",
        explain=(
            "Every turn removes two stones, so the score is at most total // 2. Also every point uses at least one "
            "stone that is NOT in the largest pile, so it is at most total - max. Taking from the two largest piles "
            "reaches the smaller of these two bounds. The brute force simulates that greedy rule turn by turn."
        ),
        cx="O(1) time, O(1) space",
        brute_cx="O(a + b + c) time - simulate every turn",
        brute=r"""
# BRUTE FORCE: O(a + b + c) time - simulate every turn
def maximum_score(a, b, c):
    piles = [a, b, c]
    score = 0
    while True:
        piles.sort(reverse=True)
        if piles[1] == 0:
            return score
        piles[0] -= 1
        piles[1] -= 1
        score += 1
""",
        solution=r"""
# OPTIMISED: O(1) time, O(1) space
# Idea: Greedy simulation turned into a closed formula
def maximum_score(a, b, c):
    total = a + b + c
    return min(total // 2, total - max(a, b, c))
""",
    ),
    # ---- Process Tasks Using Servers (LeetCode 1882) ----
    dict(
        title="Process Tasks Using Servers",
        diff="M",
        lc=1882,
        slug="process-tasks-using-servers",
        prompt=(
            "servers[i] is the weight of server i and tasks[j] is the time task j takes. Task j arrives at second j "
            "and tasks are assigned in order. A task goes to the free server with the SMALLEST weight (ties: "
            "smallest index). If no server is free it waits in a queue and starts, in order, as soon as one becomes "
            "free (a server that starts a task at second t is free again at t + tasks[j]). Return ans where ans[j] "
            "is the server that runs task j."
        ),
        sig="def assign_tasks(servers: List[int], tasks: List[int]) -> List[int]:",
        fn="assign_tasks",
        tests=[
            (([3, 3, 2], [1, 2, 3, 2, 1, 2]), [2, 2, 0, 2, 1, 2]),
            (([5, 1, 4, 3, 2], [2, 1, 2, 4, 5, 2, 1]), [1, 4, 1, 4, 1, 3, 2]),
            (([1], [1]), [0]),
            (([2, 1], [1, 1, 1]), [1, 1, 1]),
        ],
        hints=[
            "Two groups of servers matter: the free ones and the busy ones.",
            (
                "Keep free servers in a min-heap ordered by (weight, index) and busy servers in a min-heap ordered "
                "by the time they become free."
            ),
            (
                "For task j: advance the clock to max(clock, j); if no server is free jump the clock to the "
                "earliest free time; move every busy server whose time has come back to the free heap; pop the best "
                "free server and push it onto the busy heap with its new finish time."
            ),
        ],
        pattern="Event simulation with two heaps (free and busy)",
        explain=(
            "A server's state changes only at its finish time, so we never need to advance second by second: the "
            "clock jumps to either the arrival time or the next release. The free heap answers 'which server is the "
            "best one' and the busy heap answers 'who is released next'. The brute force scans all servers for "
            "every task."
        ),
        cx="O((n + m) log n) time, O(n) space",
        brute_cx="O(n * m) time - scan every server for every task",
        brute=r"""
# BRUTE FORCE: O(n * m) time - scan every server for every task
def assign_tasks(servers, tasks):
    free_at = [0] * len(servers)
    clock = 0
    result = []
    for j, duration in enumerate(tasks):
        clock = max(clock, j)
        ready = [s for s in range(len(servers)) if free_at[s] <= clock]
        if not ready:
            clock = min(free_at)
            ready = [s for s in range(len(servers)) if free_at[s] <= clock]
        chosen = min(ready, key=lambda s: (servers[s], s))
        free_at[chosen] = clock + duration
        result.append(chosen)
    return result
""",
        solution=r"""
# OPTIMISED: O((n + m) log n) time, O(n) space
# Idea: Event simulation with two heaps (free and busy)
def assign_tasks(servers, tasks):
    free = [(w, i) for i, w in enumerate(servers)]
    heapq.heapify(free)
    busy = []
    result = []
    clock = 0
    for j, duration in enumerate(tasks):
        clock = max(clock, j)
        if not free:
            clock = max(clock, busy[0][0])
        while busy and busy[0][0] <= clock:
            _, w, i = heapq.heappop(busy)
            heapq.heappush(free, (w, i))
        w, i = heapq.heappop(free)
        result.append(i)
        heapq.heappush(busy, (clock + duration, w, i))
    return result
""",
    ),
    # ---- The Number of the Smallest Unoccupied Chair (LeetCode 1942) ----
    dict(
        title="The Number of the Smallest Unoccupied Chair",
        diff="M",
        lc=1942,
        slug="the-number-of-the-smallest-unoccupied-chair",
        prompt=(
            "n friends attend a party; times[i] = [arrival_i, leaving_i] (all arrival times are different). Chairs "
            "are numbered 0, 1, 2, ... An arriving friend sits on the smallest-numbered chair that is free; a "
            "friend who leaves at time t frees the chair at time t (so an arrival at the same time can take it). "
            "Return the chair number that friend target_friend sits on."
        ),
        sig="def smallest_chair(times: List[List[int]], target_friend: int) -> int:",
        fn="smallest_chair",
        tests=[
            (([[1, 4], [2, 3], [4, 6]], 1), 1),
            (([[3, 10], [1, 5], [2, 6]], 0), 2),
            (([[1, 2]], 0), 0),
            (([[1, 3], [2, 4], [3, 5]], 2), 0),
        ],
        hints=[
            "Process friends in order of arrival.",
            (
                "Keep a min-heap of free chair numbers (initially 0 .. n - 1) and a min-heap of occupied chairs "
                "ordered by leaving time."
            ),
            (
                "Before seating a friend, move every chair whose occupant has left (leave <= arrival) back to the "
                "free heap. Take the smallest free chair, return it if this is the target, otherwise record its "
                "leave time."
            ),
        ],
        pattern="Two heaps: free resources and release times",
        explain=(
            "The order of arrivals is the order of seating. A chair is available again exactly when its occupant's "
            "leaving time is not later than the new arrival, which the busy heap detects in O(log n). The free heap "
            "hands out the smallest chair number. The brute force keeps for each chair the time it becomes free and "
            "scans the chairs for the first one that is free."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2) time - scan the chairs for every arrival",
        brute=r"""
# BRUTE FORCE: O(n^2) time - scan the chairs for every arrival
def smallest_chair(times, target_friend):
    order = sorted(range(len(times)), key=lambda i: times[i][0])
    free_time = []
    for friend in order:
        arrive, leave = times[friend]
        for chair in range(len(free_time)):
            if free_time[chair] <= arrive:
                free_time[chair] = leave
                break
        else:
            free_time.append(leave)
            chair = len(free_time) - 1
        if friend == target_friend:
            return chair
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Two heaps: free resources and release times
def smallest_chair(times, target_friend):
    n = len(times)
    order = sorted(range(n), key=lambda i: times[i][0])
    free = list(range(n))
    heapq.heapify(free)
    busy = []
    for friend in order:
        arrive, leave = times[friend]
        while busy and busy[0][0] <= arrive:
            _, chair = heapq.heappop(busy)
            heapq.heappush(free, chair)
        chair = heapq.heappop(free)
        if friend == target_friend:
            return chair
        heapq.heappush(busy, (leave, chair))
""",
    ),
    # ---- K Highest Ranked Items Within a Price Range (LeetCode 2146) ----
    dict(
        title="K Highest Ranked Items Within a Price Range",
        diff="M",
        lc=2146,
        slug="k-highest-ranked-items-within-a-price-range",
        prompt=(
            "grid[r][c] is 0 for a wall, 1 for an empty cell, and any larger number for an item with that price. "
            "pricing = [low, high] and start = [row, col] (not a wall). Moving 4-directionally one step costs 1. "
            "Rank reachable items with price in [low, high]: shorter distance from start first, then lower price, "
            "then smaller row, then smaller column. Return the positions [row, col] of the k highest-ranked items "
            "(fewer if there are not enough)."
        ),
        sig=(
            "def highest_ranked_k_items(grid: List[List[int]], pricing: List[int], start: List[int], k: int) -> "
            "List[List[int]]:"
        ),
        fn="highest_ranked_k_items",
        tests=[
            (([[1, 2, 0, 1], [1, 3, 0, 1], [0, 2, 5, 1]], [2, 5], [0, 0], 3), [[0, 1], [1, 1], [2, 1]]),
            (([[1, 2, 0, 1], [1, 3, 3, 1], [0, 2, 5, 1]], [2, 3], [2, 3], 2), [[2, 1], [1, 2]]),
            (([[1, 1, 1], [0, 0, 1], [2, 3, 4]], [2, 3], [0, 0], 3), [[2, 1], [2, 0]]),
            (([[5]], [2, 10], [0, 0], 1), [[0, 0]]),
        ],
        hints=[
            (
                "The first ranking key is the shortest-path distance, and all steps cost 1 - that is a "
                "breadth-first search from the start."
            ),
            (
                "Collect (distance, price, row, col) for every reachable cell whose value is in [low, high] (low is "
                "at least 2, so empty cells never count)."
            ),
            (
                "Tuples compare in exactly the ranking order. Take the k smallest with heapq.nsmallest (or sort all "
                "and slice) and return their coordinates."
            ),
        ],
        pattern="BFS distances + top-k by a composite key",
        explain=(
            "BFS gives the shortest distance to every reachable cell. The four ranking rules become a tuple "
            "(distance, price, row, col), whose natural ordering matches the problem. heapq.nsmallest picks k of "
            "them in O(n log k). The brute force computes distances by repeatedly relaxing all neighbours until "
            "nothing changes, then sorts everything."
        ),
        cx="O(R * C * log k) time, O(R * C) space",
        brute_cx="O((R * C)^2) time - relax distances until stable, then sort all items",
        brute=r"""
# BRUTE FORCE: O((R * C)^2) time - relax distances until stable, then sort all items
def highest_ranked_k_items(grid, pricing, start, k):
    low, high = pricing
    rows, cols = len(grid), len(grid[0])
    inf = float("inf")
    dist = [[inf] * cols for _ in range(rows)]
    dist[start[0]][start[1]] = 0
    changed = True
    while changed:
        changed = False
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 0 or dist[r][c] == inf:
                    continue
                for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nr, nc = r + dr, c + dc
                    if (
                        0 <= nr < rows
                        and 0 <= nc < cols
                        and grid[nr][nc] != 0
                        and dist[nr][nc] > dist[r][c] + 1
                    ):
                        dist[nr][nc] = dist[r][c] + 1
                        changed = True
    items = sorted(
        (dist[r][c], grid[r][c], r, c)
        for r in range(rows)
        for c in range(cols)
        if dist[r][c] < inf and low <= grid[r][c] <= high
    )
    return [[r, c] for _, _, r, c in items[:k]]
""",
        solution=r"""
# OPTIMISED: O(R * C * log k) time, O(R * C) space
# Idea: BFS distances + top-k by a composite key
def highest_ranked_k_items(grid, pricing, start, k):
    low, high = pricing
    rows, cols = len(grid), len(grid[0])
    dist = {(start[0], start[1]): 0}
    queue = deque([(start[0], start[1])])
    found = []
    while queue:
        r, c = queue.popleft()
        if low <= grid[r][c] <= high:
            found.append((dist[(r, c)], grid[r][c], r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 0 and (nr, nc) not in dist:
                dist[(nr, nc)] = dist[(r, c)] + 1
                queue.append((nr, nc))
    return [[r, c] for _, _, r, c in heapq.nsmallest(k, found)]
""",
    ),
    # ---- Maximum Total Importance of Roads (LeetCode 2285) ----
    dict(
        title="Maximum Total Importance of Roads",
        diff="M",
        lc=2285,
        slug="maximum-total-importance-of-roads",
        prompt=(
            "n cities 0..n-1 and bidirectional roads. Assign each city a DISTINCT integer value from 1 to n. The "
            "importance of a road is the sum of the values of its two cities. Return the maximum possible total "
            "importance of all roads."
        ),
        sig="def maximum_importance(n: int, roads: List[List[int]]) -> int:",
        fn="maximum_importance",
        tests=[
            ((5, [[0, 1], [1, 2], [2, 3], [0, 2], [1, 3], [2, 4]]), 43),
            ((5, [[0, 3], [2, 4], [1, 3]]), 20),
            ((2, []), 0),
            ((3, [[0, 1]]), 5),
        ],
        hints=[
            "A city's value is counted once for EVERY road that touches it, so its contribution is value * degree.",
            (
                "To maximise sum(value * degree) give the biggest values to the cities with the biggest degrees "
                "(rearrangement inequality)."
            ),
            "Count degrees, sort them ascending and multiply by 1, 2, ..., n; add up.",
        ],
        pattern="Sort by degree, assign largest values to largest degrees",
        explain=(
            "Total importance equals the sum over cities of value x degree. Pairing the sorted values with the "
            "sorted degrees maximises such a sum, which is the rearrangement inequality. The brute force tries "
            "every assignment of the n values to the cities."
        ),
        cx="O(n log n + E) time, O(n) space",
        brute_cx="O(n! * E) time - every assignment of values",
        brute=r"""
# BRUTE FORCE: O(n! * E) time - every assignment of values
def maximum_importance(n, roads):
    best = 0
    for values in itertools.permutations(range(1, n + 1)):
        total = sum(values[a] + values[b] for a, b in roads)
        best = max(best, total)
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n + E) time, O(n) space
# Idea: Sort by degree, assign largest values to largest degrees
def maximum_importance(n, roads):
    degree = [0] * n
    for a, b in roads:
        degree[a] += 1
        degree[b] += 1
    return sum(d * v for v, d in enumerate(sorted(degree), 1))
""",
    ),
    # ---- Minimum Amount of Time to Fill Cups (LeetCode 2335) ----
    dict(
        title="Minimum Amount of Time to Fill Cups",
        diff="E",
        lc=2335,
        slug="minimum-amount-of-time-to-fill-cups",
        prompt=(
            "A water dispenser fills cold, warm and hot cups. Each second you may fill 2 cups of DIFFERENT types, "
            "or just 1 cup. amount = [cold, warm, hot] gives how many cups of each type you need. Return the "
            "minimum number of seconds."
        ),
        sig="def fill_cups(amount: List[int]) -> int:",
        fn="fill_cups",
        tests=[
            (([1, 4, 2],), 4),
            (([5, 4, 4],), 7),
            (([5, 0, 0],), 5),
            (([0, 0, 0],), 0),
        ],
        hints=[
            (
                "Greedy: each second fill one cup of each of the two types with the MOST cups still needed (a "
                "max-heap does this)."
            ),
            (
                "Two lower bounds exist: the biggest type needs one second per cup, and every second fills at most "
                "two cups."
            ),
            "So the answer is max(largest amount, ceil(total / 2)) - and the greedy achieves it.",
        ],
        pattern="Greedy on the two largest, closed-form bound",
        explain=(
            "Time can never be below the size of the biggest group (one cup of it per second) nor below half the "
            "total (two cups per second). Filling the two largest groups each second keeps the pile sizes balanced "
            "and reaches the larger bound. The brute force simulates that greedy rule second by second."
        ),
        cx="O(1) time, O(1) space",
        brute_cx="O(total) time - simulate each second",
        brute=r"""
# BRUTE FORCE: O(total) time - simulate each second
def fill_cups(amount):
    cups = list(amount)
    seconds = 0
    while any(cups):
        cups.sort(reverse=True)
        cups[0] -= 1
        if cups[1] > 0:
            cups[1] -= 1
        seconds += 1
    return seconds
""",
        solution=r"""
# OPTIMISED: O(1) time, O(1) space
# Idea: Greedy on the two largest, closed-form bound
def fill_cups(amount):
    return max(max(amount), (sum(amount) + 1) // 2)
""",
    ),
    # ---- Put Marbles in Bags (LeetCode 2551) ----
    dict(
        title="Put Marbles in Bags",
        diff="H",
        lc=2551,
        slug="put-marbles-in-bags",
        prompt=(
            "weights[i] is the weight of marble i. Split the marbles, in their ORIGINAL order, into k non-empty "
            "consecutive bags. The cost of a bag holding marbles i..j is weights[i] + weights[j]; the score is the "
            "sum of the bag costs. Return (maximum possible score) - (minimum possible score)."
        ),
        sig="def put_marbles(weights: List[int], k: int) -> int:",
        fn="put_marbles",
        tests=[
            (([1, 3, 5, 1], 2), 4),
            (([1, 3], 2), 0),
            (([5], 1), 0),
            (([1, 4, 2, 5, 2], 3), 3),
        ],
        hints=[
            (
                "The first and last marbles of the whole row are always counted. Everything else depends on where "
                "the k - 1 cuts are placed."
            ),
            "A cut between positions i and i + 1 adds exactly weights[i] + weights[i + 1] to the score.",
            (
                "Compute those adjacent pair sums, sort them, and the max score takes the k - 1 largest while the "
                "min score takes the k - 1 smallest. Subtract."
            ),
        ],
        pattern="Independent cut costs: top-k minus bottom-k",
        explain=(
            "Every score equals weights[0] + weights[n-1] plus the sum of pair-sums at the chosen cuts, and cuts do "
            "not affect each other. So the best and worst choices are the k - 1 largest and the k - 1 smallest "
            "pair-sums; the fixed part cancels in the difference. The brute force tries every set of cut positions."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(C(n - 1, k - 1) * n) time - every choice of cuts",
        brute=r"""
# BRUTE FORCE: O(C(n - 1, k - 1) * n) time - every choice of cuts
def put_marbles(weights, k):
    n = len(weights)
    scores = []
    for cuts in itertools.combinations(range(1, n), k - 1):
        bounds = [0, *cuts, n]
        scores.append(sum(weights[a] + weights[b - 1] for a, b in zip(bounds, bounds[1:])))
    return max(scores) - min(scores)
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Independent cut costs: top-k minus bottom-k
def put_marbles(weights, k):
    pairs = sorted(weights[i] + weights[i + 1] for i in range(len(weights) - 1))
    return sum(pairs[len(pairs) - k + 1 :]) - sum(pairs[: k - 1])
""",
    ),
    # ---- Take Gifts From the Richest Pile (LeetCode 2558) ----
    dict(
        title="Take Gifts From the Richest Pile",
        diff="E",
        lc=2558,
        slug="take-gifts-from-the-richest-pile",
        prompt=(
            "gifts[i] is the number of gifts in pile i. Every second, pick the pile with the MOST gifts (any one if "
            "tied) and leave behind floor(sqrt(gifts)) in it, taking the rest. Repeat for k seconds. Return the "
            "number of gifts remaining after k seconds."
        ),
        sig="def pick_gifts(gifts: List[int], k: int) -> int:",
        fn="pick_gifts",
        tests=[
            (([25, 64, 9, 4, 100], 4), 29),
            (([1, 1, 1, 1], 4), 4),
            (([4], 0), 4),
            (([100], 2), 3),
        ],
        hints=[
            "You repeatedly need the largest pile and then its value changes - a max-heap fits.",
            "Python's heapq is a min-heap: store the negated values.",
            (
                "k times: pop the largest, push floor(sqrt(value)) (use math.isqrt, exact for integers). At the end "
                "add up the heap."
            ),
        ],
        pattern="Max-heap simulation",
        explain=(
            "Each step reads and replaces the maximum, which is the textbook heap operation (O(log n)) compared "
            "with an O(n) scan for the maximum. math.isqrt avoids floating-point mistakes for large integers. The "
            "brute force scans the list for the largest pile each time."
        ),
        cx="O((n + k) log n) time, O(n) space",
        brute_cx="O(k * n) time - scan for the maximum every second",
        brute=r"""
# BRUTE FORCE: O(k * n) time - scan for the maximum every second
def pick_gifts(gifts, k):
    piles = list(gifts)
    for _ in range(k):
        i = piles.index(max(piles))
        piles[i] = math.isqrt(piles[i])
    return sum(piles)
""",
        solution=r"""
# OPTIMISED: O((n + k) log n) time, O(n) space
# Idea: Max-heap simulation
def pick_gifts(gifts, k):
    heap = [-g for g in gifts]
    heapq.heapify(heap)
    for _ in range(k):
        top = -heapq.heappop(heap)
        heapq.heappush(heap, -math.isqrt(top))
    return -sum(heap)
""",
    ),
    # ---- Maximum Elegance of a K-Length Subsequence (LeetCode 2813) ----
    dict(
        title="Maximum Elegance of a K-Length Subsequence",
        diff="H",
        lc=2813,
        slug="maximum-elegance-of-a-k-length-subsequence",
        prompt=(
            "items[i] = [profit, category]. Choose exactly k items (a subsequence). Its elegance is total_profit + "
            "distinct_categories^2. Return the maximum elegance."
        ),
        sig="def find_maximum_elegance(items: List[List[int]], k: int) -> int:",
        fn="find_maximum_elegance",
        tests=[
            (([[3, 2], [5, 1], [10, 1]], 2), 17),
            (([[3, 1], [3, 1], [2, 2], [5, 3]], 3), 19),
            (([[1, 1], [2, 1], [3, 1]], 3), 7),
            (([[4, 1]], 1), 5),
        ],
        hints=[
            "Start from the k items with the largest profit - that is the best total profit.",
            (
                "To gain more distinct categories you must drop an item and bring in one from a NEW category. Only "
                "items whose category is repeated inside the selection are worth dropping, and the cheapest of "
                "those first."
            ),
            (
                "Go through the remaining items in decreasing profit; whenever one has an unseen category and the "
                "selection has a removable duplicate, swap it for the smallest-profit duplicate and re-evaluate the "
                "elegance. Keep the best."
            ),
        ],
        pattern="Greedy swap with a stack of removable duplicates",
        explain=(
            "Starting from the top-k profits, a swap is only useful if it increases the category count, since the "
            "profit can only go down when we bring in a smaller-profit item. The cheapest removable item is the "
            "lowest-profit duplicate in the selection, which a stack supplies because items are visited in "
            "decreasing profit. Later candidates have even smaller profit, so there is no reason to use a larger "
            "loss. The brute force tries all k-subsets."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(C(n, k) * k) time - every k-subset",
        brute=r"""
# BRUTE FORCE: O(C(n, k) * k) time - every k-subset
def find_maximum_elegance(items, k):
    best = 0
    for chosen in itertools.combinations(items, k):
        profit = sum(p for p, _ in chosen)
        categories = len({c for _, c in chosen})
        best = max(best, profit + categories * categories)
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Greedy swap with a stack of removable duplicates
def find_maximum_elegance(items, k):
    ordered = sorted(items, reverse=True)
    seen = set()
    duplicates = []
    total = 0
    best = 0
    for i, (profit, category) in enumerate(ordered):
        if i < k:
            total += profit
            if category in seen:
                duplicates.append(profit)
            else:
                seen.add(category)
            if i == k - 1:
                best = total + len(seen) ** 2
        elif category not in seen and duplicates:
            total += profit - duplicates.pop()
            seen.add(category)
            best = max(best, total + len(seen) ** 2)
    return best
""",
    ),
    # ---- Minimum Operations to Exceed Threshold Value II (LeetCode 3066) ----
    dict(
        title="Minimum Operations to Exceed Threshold Value II",
        diff="M",
        lc=3066,
        slug="minimum-operations-to-exceed-threshold-value-ii",
        prompt=(
            "In one operation remove the two SMALLEST elements x <= y of nums and insert min(x, y) * 2 + max(x, y) "
            "= 2x + y. Return the minimum number of operations so that every element is at least k (an answer is "
            "guaranteed to exist)."
        ),
        sig="def min_operations(nums: List[int], k: int) -> int:",
        fn="min_operations",
        tests=[
            (([2, 11, 10, 1, 3], 10), 2),
            (([1, 1, 2, 4, 9], 20), 4),
            (([5, 6], 3), 0),
            (([1, 1, 2], 4), 2),
        ],
        hints=[
            "You always combine the two smallest values, so you want a structure that returns the minimum fast.",
            "Put all numbers in a min-heap.",
            (
                "While the smallest value is < k: pop two, push 2x + y, count one operation. Stop as soon as the "
                "smallest value is at least k."
            ),
        ],
        pattern="Min-heap simulation",
        explain=(
            "Every operation needs the two smallest elements, and the new element goes back into the collection - "
            "exactly what a min-heap supports in O(log n). Checking only the heap top is enough to know whether all "
            "elements reach k. The brute force sorts the whole list again after each operation."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2 log n) time - re-sort after every operation",
        brute=r"""
# BRUTE FORCE: O(n^2 log n) time - re-sort after every operation
def min_operations(nums, k):
    values = sorted(nums)
    ops = 0
    while values[0] < k:
        x, y = values[0], values[1]
        values = sorted(values[2:] + [2 * x + y])
        ops += 1
    return ops
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Min-heap simulation
def min_operations(nums, k):
    heap = list(nums)
    heapq.heapify(heap)
    ops = 0
    while heap[0] < k:
        x = heapq.heappop(heap)
        y = heapq.heappop(heap)
        heapq.heappush(heap, 2 * x + y)
        ops += 1
    return ops
""",
    ),
    # ---- Most Frequent IDs (LeetCode 3092) ----
    dict(
        title="Most Frequent IDs",
        diff="M",
        lc=3092,
        slug="most-frequent-ids",
        prompt=(
            "A collection of IDs changes over time: at step i, freq[i] copies of the ID nums[i] are added (if "
            "positive) or removed (if negative). After each step, report the count of the MOST FREQUENT ID, or 0 if "
            "the collection is empty. Counts never become negative."
        ),
        sig="def most_frequent_ids(nums: List[int], freq: List[int]) -> List[int]:",
        fn="most_frequent_ids",
        tests=[
            (([2, 3, 2, 1], [3, 2, -3, 1]), [3, 3, 2, 2]),
            (([5, 5, 3], [2, -2, 1]), [2, 0, 1]),
            (([1], [1]), [1]),
            (([1, 1], [2, -2]), [2, 0]),
        ],
        hints=[
            "Keep a dictionary id -> current count. After a step the maximum can both rise and fall.",
            (
                "A max-heap of (count, id) pairs gives the maximum, but a pair becomes OUTDATED when the id's count "
                "changes."
            ),
            (
                "Push the new pair after every update. When reading the answer, pop from the top while the pair's "
                "count differs from the dictionary's current count (lazy deletion)."
            ),
        ],
        pattern="Max-heap with lazy deletion",
        explain=(
            "Heaps cannot change or remove an arbitrary element, so we leave outdated entries inside and just "
            "ignore them when they reach the top. Each update adds one entry and each entry is discarded at most "
            "once, so the total work is O(n log n). The brute force recomputes the maximum over the whole "
            "dictionary after each step."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n * distinct ids) time - scan all counts every step",
        brute=r"""
# BRUTE FORCE: O(n * distinct ids) time - scan all counts every step
def most_frequent_ids(nums, freq):
    counts = {}
    result = []
    for x, f in zip(nums, freq):
        counts[x] = counts.get(x, 0) + f
        result.append(max(counts.values()))
    return result
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Max-heap with lazy deletion
def most_frequent_ids(nums, freq):
    counts = defaultdict(int)
    heap = []
    result = []
    for x, f in zip(nums, freq):
        counts[x] += f
        heapq.heappush(heap, (-counts[x], x))
        while counts[heap[0][1]] != -heap[0][0]:
            heapq.heappop(heap)
        result.append(-heap[0][0])
    return result
""",
    ),
    # ---- Final Array State After K Multiplication Operations I (LeetCode 3264) ----
    dict(
        title="Final Array State After K Multiplication Operations I",
        diff="E",
        lc=3264,
        slug="final-array-state-after-k-multiplication-operations-i",
        prompt=(
            "Perform k operations on nums: find the minimum value (the FIRST one if there are ties) and multiply it "
            "by `multiplier`. Return the array after all k operations."
        ),
        sig="def get_final_state(nums: List[int], k: int, multiplier: int) -> List[int]:",
        fn="get_final_state",
        tests=[
            (([2, 1, 3, 5, 6], 5, 2), [8, 4, 6, 5, 6]),
            (([1, 2], 3, 4), [16, 8]),
            (([5], 0, 3), [5]),
            (([3, 3], 2, 2), [6, 6]),
        ],
        hints=[
            (
                "Simulate: repeatedly find the smallest element (leftmost on a tie) and replace it with value * "
                "multiplier."
            ),
            (
                "Finding the minimum by scanning costs O(n) each time; a min-heap of (value, index) pairs does it "
                "in O(log n) and breaks ties by the smaller index automatically."
            ),
            (
                "Pop, multiply, push back with the same index, k times. Afterwards write each heap entry back to "
                "its index."
            ),
        ],
        pattern="Min-heap of (value, index)",
        explain=(
            "A tuple (value, index) is ordered by value first and by index second, which is the required tie rule. "
            "Popping the minimum and pushing the multiplied value back is one heap round trip, O(log n). The brute "
            "force scans the array each time."
        ),
        cx="O((n + k) log n) time, O(n) space",
        brute_cx="O(k * n) time - linear scan for the minimum",
        brute=r"""
# BRUTE FORCE: O(k * n) time - linear scan for the minimum
def get_final_state(nums, k, multiplier):
    values = list(nums)
    for _ in range(k):
        i = values.index(min(values))
        values[i] *= multiplier
    return values
""",
        solution=r"""
# OPTIMISED: O((n + k) log n) time, O(n) space
# Idea: Min-heap of (value, index)
def get_final_state(nums, k, multiplier):
    heap = [(v, i) for i, v in enumerate(nums)]
    heapq.heapify(heap)
    for _ in range(k):
        v, i = heapq.heappop(heap)
        heapq.heappush(heap, (v * multiplier, i))
    result = [0] * len(nums)
    for v, i in heap:
        result[i] = v
    return result
""",
    ),
    # ---- K-th Nearest Obstacle Queries (LeetCode 3275) ----
    dict(
        title="K-th Nearest Obstacle Queries",
        diff="M",
        lc=3275,
        slug="k-th-nearest-obstacle-queries",
        prompt=(
            "On an infinite plane, queries[i] = [x, y] places an obstacle at (x, y) (all positions are different). "
            "The distance of an obstacle is |x| + |y|. After each query return the distance of the k-th NEAREST "
            "obstacle placed so far, or -1 if fewer than k obstacles exist."
        ),
        sig="def results_array(queries: List[List[int]], k: int) -> List[int]:",
        fn="results_array",
        tests=[
            (([[1, 2], [3, 4], [2, 3], [-3, 0]], 2), [-1, 7, 5, 3]),
            (([[5, 5], [4, 4], [3, 3]], 1), [10, 8, 6]),
            (([[1, 1]], 2), [-1]),
            (([[1, 0], [0, 1]], 2), [-1, 1]),
        ],
        hints=[
            "After each insertion you need the k-th smallest distance in a growing collection.",
            "Keep only the k SMALLEST distances seen so far; the k-th smallest is the LARGEST among them.",
            (
                "Use a max-heap of size k (negated values in Python): push the new distance, pop the largest if the "
                "size exceeds k, and report the top when the heap holds exactly k items (else -1)."
            ),
        ],
        pattern="Bounded max-heap for the k-th smallest of a stream",
        explain=(
            "A larger distance than the k-th smallest can never become the k-th smallest again, because later "
            "insertions only push the k-th value down or leave it. So the heap keeps just k values and its top is "
            "the answer. The brute force keeps all distances and sorts after every query."
        ),
        cx="O(n log k) time, O(k) space",
        brute_cx="O(n^2 log n) time - sort all distances after every query",
        brute=r"""
# BRUTE FORCE: O(n^2 log n) time - sort all distances after every query
def results_array(queries, k):
    distances = []
    result = []
    for x, y in queries:
        distances.append(abs(x) + abs(y))
        distances.sort()
        result.append(distances[k - 1] if len(distances) >= k else -1)
    return result
""",
        solution=r"""
# OPTIMISED: O(n log k) time, O(k) space
# Idea: Bounded max-heap for the k-th smallest of a stream
def results_array(queries, k):
    heap = []
    result = []
    for x, y in queries:
        heapq.heappush(heap, -(abs(x) + abs(y)))
        if len(heap) > k:
            heapq.heappop(heap)
        result.append(-heap[0] if len(heap) == k else -1)
    return result
""",
    ),
    # ---- Choose K Elements With Maximum Sum (LeetCode 3478) ----
    dict(
        title="Choose K Elements With Maximum Sum",
        diff="M",
        lc=3478,
        slug="choose-k-elements-with-maximum-sum",
        prompt=(
            "nums1 and nums2 have length n. For every index i, look at all indices j with nums1[j] < nums1[i] "
            "(STRICTLY smaller) and choose at most k of them so that the sum of their nums2[j] values is as large "
            "as possible. Return answer[i] = that maximum sum (0 if no such j exists)."
        ),
        sig="def find_max_sum(nums1: List[int], nums2: List[int], k: int) -> List[int]:",
        fn="find_max_sum",
        tests=[
            (([4, 2, 1, 5, 3], [10, 20, 30, 40, 50], 2), [80, 30, 0, 80, 50]),
            (([2, 2, 2, 2], [3, 1, 2, 3], 1), [0, 0, 0, 0]),
            (([1], [5], 1), [0]),
            (([1, 2], [7, 3], 1), [0, 7]),
        ],
        hints=[
            (
                "Sort the indices by nums1. Everything strictly smaller than index i appears BEFORE the group of "
                "equal nums1 values."
            ),
            (
                "Keep a min-heap holding the k largest nums2 values among the processed indices, together with "
                "their running sum."
            ),
            (
                "Process indices in groups of equal nums1: first assign the current sum to every index of the "
                "group, THEN push the group's nums2 values (popping the smallest while the heap has more than k "
                "values)."
            ),
        ],
        pattern="Sort + sliding top-k with a min-heap (batch equal keys)",
        explain=(
            "When indices are visited in increasing nums1, the processed ones are exactly the candidates with a "
            "smaller or equal nums1, and handling a whole group of equals before adding any of them to the heap "
            "makes the comparison strict. A min-heap of size k keeps the k largest nums2 values; its running sum is "
            "the answer. The brute force filters and sorts all candidates for each index."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2 log n) time - filter and sort for every index",
        brute=r"""
# BRUTE FORCE: O(n^2 log n) time - filter and sort for every index
def find_max_sum(nums1, nums2, k):
    result = []
    for i in range(len(nums1)):
        candidates = sorted(
            (nums2[j] for j in range(len(nums1)) if nums1[j] < nums1[i]), reverse=True
        )
        result.append(sum(candidates[:k]))
    return result
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Sort + sliding top-k with a min-heap (batch equal keys)
def find_max_sum(nums1, nums2, k):
    n = len(nums1)
    order = sorted(range(n), key=lambda i: nums1[i])
    result = [0] * n
    heap = []
    total = 0
    i = 0
    while i < n:
        j = i
        while j < n and nums1[order[j]] == nums1[order[i]]:
            result[order[j]] = total
            j += 1
        for t in range(i, j):
            value = nums2[order[t]]
            heapq.heappush(heap, value)
            total += value
            if len(heap) > k:
                total -= heapq.heappop(heap)
        i = j
    return result
""",
    ),
    # ---- Maximum Spending After Buying Items (LeetCode 2931) ----
    dict(
        title="Maximum Spending After Buying Items",
        diff="H",
        lc=2931,
        slug="maximum-spending-after-buying-items",
        prompt=(
            "values is an m x n grid: row i lists the item values of shop i, sorted in NON-INCREASING order. On day "
            "d (d = 1, 2, ...) you pick a shop and buy its RIGHTMOST remaining item; paying value * d. You must buy "
            "all m * n items. Return the maximum total amount you can spend."
        ),
        sig="def max_spending(values: List[List[int]]) -> int:",
        fn="max_spending",
        tests=[
            (([[8, 5, 2], [6, 4, 1], [9, 7, 3]],), 285),
            (([[10, 8, 6, 4, 2], [9, 7, 5, 3, 2]],), 386),
            (([[5]],), 5),
            (([[3, 1]],), 7),
        ],
        hints=[
            "The multiplier d grows with the day, so you want the most expensive items to be bought LAST.",
            (
                "Because each shop is sorted non-increasing, its rightmost item is its cheapest - so every shop can "
                "be emptied from cheapest to dearest."
            ),
            (
                "That means any global order sorted ascending by value is reachable: flatten all values, sort them "
                "ascending, and sum value * (position + 1)."
            ),
        ],
        pattern="Rearrangement inequality: smallest first, largest last",
        explain=(
            "Pairing small values with small multipliers maximises the sum of products. The shop rows are sorted so "
            "that the item you can buy is always that shop's current minimum; buying the global minimum among the "
            "available ones is therefore the same as buying in globally sorted order. Ties do not matter. The brute "
            "force tries every sequence of shops (with the multiplier equal to the day number), i.e. all "
            "interleavings."
        ),
        cx="O(m n log(m n)) time, O(m n) space",
        brute_cx="exponential - every interleaving of the shops' purchases",
        brute=r"""
# BRUTE FORCE: exponential - every interleaving of the shops' purchases
def max_spending(values):
    shops = len(values)
    total_days = sum(len(row) for row in values)

    def best(left, day):
        if day > total_days:
            return 0
        result = 0
        for s in range(shops):
            if left[s] > 0:
                nxt = list(left)
                nxt[s] -= 1
                result = max(result, values[s][left[s] - 1] * day + best(tuple(nxt), day + 1))
        return result

    return best(tuple(len(row) for row in values), 1)
""",
        solution=r"""
# OPTIMISED: O(m n log(m n)) time, O(m n) space
# Idea: Rearrangement inequality: smallest first, largest last
def max_spending(values):
    ordered = sorted(v for row in values for v in row)
    return sum(v * day for day, v in enumerate(ordered, 1))
""",
    ),
    # ---- Construct String With Repeat Limit (LeetCode 2182) ----
    dict(
        title="Construct String With Repeat Limit",
        diff="M",
        lc=2182,
        slug="construct-string-with-repeat-limit",
        prompt=(
            "Build a new string from the letters of s (each letter used at most as many times as it appears in s) "
            "such that no letter appears more than repeat_limit times IN A ROW. Return the lexicographically "
            "LARGEST string you can build (a longer string beats its own prefix)."
        ),
        sig="def repeat_limited_string(s: str, repeat_limit: int) -> str:",
        fn="repeat_limited_string",
        tests=[
            (("cczazcc", 3), "zzcccac"),
            (("aababab", 2), "bbabaa"),
            (("a", 1), "a"),
            (("aaaa", 2), "aa"),
        ],
        hints=[
            "To be lexicographically largest, always write the LARGEST letter you are still allowed to write.",
            (
                "Write up to repeat_limit copies of the current largest letter. If copies remain, you must put ONE "
                "copy of the next-largest available letter between them."
            ),
            (
                "Then go back to the largest letter. If there is no other letter left to use as a separator, stop. "
                "Keep letter counts in an array or a max-heap."
            ),
        ],
        pattern="Greedy with letter counts (largest first, minimal separator)",
        explain=(
            "A larger letter early always beats anything later, so we spend the biggest letter at every chance. The "
            "rule limits runs, so when a run is cut we insert the smallest harm: exactly one copy of the "
            "next-largest letter, which keeps the string as large as possible. If no separator exists the remaining "
            "copies of the large letter are unusable. The brute force searches every legal string recursively and "
            "keeps the largest."
        ),
        cx="O(n + 26) time, O(26) space",
        brute_cx="exponential - search every legal string",
        brute=r"""
# BRUTE FORCE: exponential - search every legal string
def repeat_limited_string(s, repeat_limit):
    letters = sorted(set(s))

    def best(counts, last, run):
        result = ""
        for ch in letters:
            if counts[ch] == 0:
                continue
            new_run = run + 1 if ch == last else 1
            if new_run > repeat_limit:
                continue
            counts[ch] -= 1
            result = max(result, ch + best(counts, ch, new_run))
            counts[ch] += 1
        return result

    return best(Counter(s), "", 0)
""",
        solution=r"""
# OPTIMISED: O(n + 26) time, O(26) space
# Idea: Greedy with letter counts (largest first, minimal separator)
def repeat_limited_string(s, repeat_limit):
    counts = Counter(s)
    letters = sorted(counts, reverse=True)
    out = []
    i = 0
    while i < len(letters):
        c = letters[i]
        take = min(counts[c], repeat_limit)
        out.append(c * take)
        counts[c] -= take
        if counts[c] == 0:
            i += 1
            continue
        j = i + 1
        while j < len(letters) and counts[letters[j]] == 0:
            j += 1
        if j == len(letters):
            break
        out.append(letters[j])
        counts[letters[j]] -= 1
    return "".join(out)
""",
    ),
    # ---- Find the K-Sum of an Array (LeetCode 2386) ----
    dict(
        title="Find the K-Sum of an Array",
        diff="H",
        lc=2386,
        slug="find-the-k-sum-of-an-array",
        prompt=(
            "The K-Sum of an array is the k-th LARGEST value among the sums of all its subsequences (the empty "
            "subsequence has sum 0, and subsequences with equal sums are counted separately). Given nums and k, "
            "return the K-Sum."
        ),
        sig="def k_sum(nums: List[int], k: int) -> int:",
        fn="k_sum",
        tests=[
            (([2, 4, -2], 5), 2),
            (([1, -2, 3, 4, -10, 12], 16), 10),
            (([5], 1), 5),
            (([5], 2), 0),
        ],
        hints=[
            "The largest subsequence sum is the sum of all positive numbers.",
            (
                "Every other subsequence sum is that maximum MINUS something: drop a positive number or take a "
                "negative one - either way you lose its absolute value. So work with the absolute values sorted "
                "ascending and find the (k-1)-th SMALLEST total loss."
            ),
            (
                "Enumerate loss totals in increasing order with a min-heap over (loss, last index used). From (s, "
                "i) push (s + a[i+1], i+1) (add the next item) and (s - a[i] + a[i+1], i+1) (swap the last item for "
                "the next one). The (k-1)-th pop gives the answer total - loss."
            ),
        ],
        pattern="Heap enumeration of the k smallest subset sums",
        explain=(
            "With absolute values sorted ascending, each subset of 'lost' items is generated exactly once by two "
            "moves from its parent - extend with the next index, or shift the last index by one - and both children "
            "cost at least as much as the parent. A min-heap therefore pops losses in sorted order, so k - 1 pops "
            "suffice. The brute force builds all 2^n subset sums and sorts them."
        ),
        cx="O(n log n + k log k) time, O(n + k) space",
        brute_cx="O(2^n * n) time - every subsequence sum",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - every subsequence sum
def k_sum(nums, k):
    sums = []
    for mask in range(1 << len(nums)):
        sums.append(sum(nums[i] for i in range(len(nums)) if mask >> i & 1))
    sums.sort(reverse=True)
    return sums[k - 1]
""",
        solution=r"""
# OPTIMISED: O(n log n + k log k) time, O(n + k) space
# Idea: Heap enumeration of the k smallest subset sums
def k_sum(nums, k):
    total = sum(x for x in nums if x > 0)
    losses = sorted(abs(x) for x in nums)
    best = total
    heap = [(losses[0], 0)]
    for _ in range(k - 1):
        loss, i = heapq.heappop(heap)
        best = total - loss
        if i + 1 < len(losses):
            heapq.heappush(heap, (loss + losses[i + 1], i + 1))
            heapq.heappush(heap, (loss - losses[i] + losses[i + 1], i + 1))
    return best
""",
    ),
    # ---- Mark Elements on Array by Performing Queries (LeetCode 3080) ----
    dict(
        title="Mark Elements on Array by Performing Queries",
        diff="M",
        lc=3080,
        slug="mark-elements-on-array-by-performing-queries",
        prompt=(
            "All elements of nums start unmarked. Query [index, k] does: (1) mark nums[index] if it is unmarked; "
            "(2) mark the k unmarked elements with the SMALLEST values (smaller index first on ties), or all of "
            "them if fewer than k remain. After each query, report the sum of the values that are still unmarked."
        ),
        sig="def unmarked_sum_array(nums: List[int], queries: List[List[int]]) -> List[int]:",
        fn="unmarked_sum_array",
        tests=[
            (([1, 2, 2, 1, 2, 3, 1], [[1, 2], [3, 3], [4, 2]]), [8, 3, 0]),
            (([1, 4, 2, 3], [[0, 1]]), [7]),
            (([5], [[0, 1]]), [0]),
            (([3, 1, 2], [[2, 2]]), [0]),
        ],
        hints=[
            "Keep the running sum of unmarked values and subtract values as they get marked.",
            (
                "You repeatedly need 'the smallest unmarked (value, index)': a min-heap of (value, index) gives it "
                "in O(log n)."
            ),
            (
                "Per query: mark index (if unmarked, subtract it). Then pop from the heap, skipping entries that "
                "are already marked, until you have marked k more or the heap is empty. Record the sum."
            ),
        ],
        pattern="Min-heap with a 'marked' array (skip stale entries)",
        explain=(
            "Marking by index is random access while marking by value order is a priority-queue operation. The heap "
            "holds all elements once, an element that was marked by index is simply skipped when it reaches the "
            "top, so each element is popped at most once overall. The brute force sorts the unmarked elements again "
            "for every query."
        ),
        cx="O((n + q) log n) time, O(n) space",
        brute_cx="O(q * n log n) time - re-sort the unmarked elements per query",
        brute=r"""
# BRUTE FORCE: O(q * n log n) time - re-sort the unmarked elements per query
def unmarked_sum_array(nums, queries):
    marked = [False] * len(nums)
    result = []
    for index, k in queries:
        marked[index] = True
        order = sorted((v, i) for i, v in enumerate(nums) if not marked[i])
        for _, i in order[:k]:
            marked[i] = True
        result.append(sum(v for i, v in enumerate(nums) if not marked[i]))
    return result
""",
        solution=r"""
# OPTIMISED: O((n + q) log n) time, O(n) space
# Idea: Min-heap with a 'marked' array (skip stale entries)
def unmarked_sum_array(nums, queries):
    marked = [False] * len(nums)
    heap = [(v, i) for i, v in enumerate(nums)]
    heapq.heapify(heap)
    remaining = sum(nums)
    result = []
    for index, k in queries:
        if not marked[index]:
            marked[index] = True
            remaining -= nums[index]
        while k > 0 and heap:
            v, i = heapq.heappop(heap)
            if not marked[i]:
                marked[i] = True
                remaining -= v
                k -= 1
        result.append(remaining)
    return result
""",
    ),
]
