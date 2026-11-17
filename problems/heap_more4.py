"""more Heap / Priority Queue problems (batch 5) - part of the problem bank for the "heap" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- The K Weakest Rows in a Matrix (LeetCode 1337) ----
    dict(
        title="The K Weakest Rows in a Matrix",
        diff="E",
        lc=1337,
        slug="the-k-weakest-rows-in-a-matrix",
        prompt=(
            "Each row of mat is soldiers (1s) followed by civilians (0s). Row i is weaker than row j if it has "
            "fewer soldiers, or equally many and i < j. Return the indices of the k weakest rows, weakest first."
        ),
        sig="def k_weakest_rows(mat: List[List[int]], k: int) -> List[int]:",
        fn="k_weakest_rows",
        tests=[
            (([[1, 1, 0, 0, 0], [1, 1, 1, 1, 0], [1, 0, 0, 0, 0], [1, 1, 0, 0, 0], [1, 1, 1, 1, 1]], 3), [2, 0, 3]),
            (([[1, 0, 0, 0], [1, 1, 1, 1], [1, 0, 0, 0], [1, 0, 0, 0]], 2), [0, 2]),
            (([[1], [0]], 1), [1]),
            (([[1, 1], [1, 1]], 2), [0, 1]),
        ],
        hints=[
            "The 'strength' of a row is (number of soldiers, row index).",
            "Sorting all m rows by that key costs O(m log m).",
            (
                "You only need the k smallest keys: heapq.nsmallest(k, ...) keeps a heap of size k (O(m log k)). "
                "Soldiers can be counted by binary search because 1s come first."
            ),
        ],
        pattern="Top-k selection with a heap",
        explain=(
            "A bounded heap finds the k smallest keys without fully sorting; the tuple key breaks ties by index "
            "automatically."
        ),
        cx="O(m log n + m log k) time",
        brute_cx="O(m * n + m log m) time - count soldiers and sort every row",
        brute=r"""
# BRUTE FORCE: O(m * n + m log m) time - count soldiers and sort every row
def k_weakest_rows(mat, k):
    ranked = sorted(range(len(mat)), key=lambda i: (sum(mat[i]), i))
    return ranked[:k]
""",
        solution=r"""
# OPTIMISED: O(m log n + m log k) time
# Idea: Top-k selection with a heap
def k_weakest_rows(mat, k):
    def soldiers(row):  # 1s come first, so binary search for the first 0
        lo, hi = 0, len(row)

        while lo < hi:
            mid = (lo + hi) // 2
            if row[mid] == 1:
                lo = mid + 1
            else:
                hi = mid

        return lo

    return heapq.nsmallest(k, range(len(mat)), key=lambda i: (soldiers(mat[i]), i))
""",
    ),
    # ---- Furthest Building You Can Reach (LeetCode 1642) ----
    dict(
        title="Furthest Building You Can Reach",
        diff="M",
        lc=1642,
        slug="furthest-building-you-can-reach",
        prompt=(
            "You walk from building 0 to the right. Moving to a taller building needs either (height difference) "
            "bricks or ONE ladder; moving to an equal or lower building is free. With the given bricks and ladders, "
            "return the index of the furthest building you can reach."
        ),
        sig="def furthest_building(heights: List[int], bricks: int, ladders: int) -> int:",
        fn="furthest_building",
        tests=[
            (([4, 2, 7, 6, 9, 14, 12], 5, 1), 4),
            (([4, 12, 2, 7, 3, 18, 20, 3, 19], 10, 2), 7),
            (([14, 3, 19, 3], 17, 0), 3),
            (([1, 2], 0, 0), 0),
            (([1, 1, 1], 0, 0), 2),
        ],
        hints=[
            "Ladders are best spent on the LARGEST climbs, bricks on the smaller ones.",
            "But you do not know the future climbs yet - so decide lazily.",
            (
                "Use a min-heap of climbs so far. Whenever it holds more than `ladders` climbs, pay for the "
                "SMALLEST with bricks; if bricks go negative you are stuck."
            ),
        ],
        pattern="Greedy with a min-heap (regret / undo the cheapest ladder)",
        explain=(
            "Give every climb a ladder at first; when ladders run out, the smallest climb on the heap is the "
            "cheapest to convert into bricks. This always keeps the ladders on the biggest climbs seen so far."
        ),
        cx="O(n log L) time, O(L) space",
        brute_cx="O(n^2 log n) time - for each target, sort the climbs and test feasibility",
        brute=r"""
# BRUTE FORCE: O(n^2 log n) time - for each target, sort the climbs and test feasibility
def furthest_building(heights, bricks, ladders):
    furthest = 0

    for target in range(1, len(heights)):
        climbs = sorted(
            (heights[j + 1] - heights[j] for j in range(target) if heights[j + 1] > heights[j]),
            reverse=True,
        )
        needed = sum(climbs[ladders:])  # ladders cover the biggest climbs

        if needed <= bricks:
            furthest = target
        else:
            break

    return furthest
""",
        solution=r"""
# OPTIMISED: O(n log L) time, O(L) space
# Idea: Greedy with a min-heap (regret / undo the cheapest ladder)
def furthest_building(heights, bricks, ladders):
    heap = []  # climbs currently covered by ladders (min-heap)

    for i in range(len(heights) - 1):
        climb = heights[i + 1] - heights[i]

        if climb <= 0:
            continue

        heapq.heappush(heap, climb)

        if len(heap) > ladders:
            bricks -= heapq.heappop(heap)  # swap the smallest ladder climb for bricks
            if bricks < 0:
                return i

    return len(heights) - 1
""",
    ),
    # ---- Minimum Operations to Halve Array Sum (LeetCode 2208) ----
    dict(
        title="Minimum Operations to Halve Array Sum",
        diff="M",
        lc=2208,
        slug="minimum-operations-to-halve-array-sum",
        prompt=(
            "One operation replaces any element by half of it (the halved value may be a fraction). Return the "
            "minimum number of operations to reduce the array sum by at least half."
        ),
        sig="def halve_array(nums: List[int]) -> int:",
        fn="halve_array",
        tests=[
            (([5, 19, 8, 1],), 3),
            (([3, 8, 20],), 3),
            (([1],), 1),
            (([10, 10],), 2),
        ],
        hints=[
            "To lose as much sum as possible per operation, halve the LARGEST element.",
            "After halving it may still be the largest, so you need the maximum again and again.",
            (
                "Max-heap (store negatives in heapq): pop the max, push half of it, track the remaining sum until "
                "it is at most half of the original."
            ),
        ],
        pattern="Greedy with a max-heap",
        explain=(
            "Halving x removes x / 2 from the sum, so the biggest element removes the most. The heap returns the "
            "current maximum in O(log n)."
        ),
        cx="O(n log n) time",
        brute_cx="O(ops * n) time - scan for the maximum every operation",
        brute=r"""
# BRUTE FORCE: O(ops * n) time - scan for the maximum every operation
def halve_array(nums):
    values = [float(x) for x in nums]
    total, remaining, ops = sum(values), sum(values), 0

    while remaining * 2 > total:
        i = values.index(max(values))  # linear scan for the largest
        values[i] /= 2
        remaining -= values[i]  # the other half is what was removed
        ops += 1

    return ops
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Greedy with a max-heap
def halve_array(nums):
    heap = [-float(x) for x in nums]  # negatives turn heapq into a max-heap
    heapq.heapify(heap)
    total = remaining = float(sum(nums))
    ops = 0

    while remaining * 2 > total:
        biggest = -heapq.heappop(heap)
        remaining -= biggest / 2
        heapq.heappush(heap, -biggest / 2)
        ops += 1

    return ops
""",
    ),
    # ---- Maximal Score After Applying K Operations (LeetCode 2530) ----
    dict(
        title="Maximal Score After Applying K Operations",
        diff="M",
        lc=2530,
        slug="maximal-score-after-applying-k-operations",
        prompt=(
            "Exactly k times: pick an index i, add nums[i] to the score, then replace nums[i] by ceil(nums[i] / 3). "
            "Return the maximum score."
        ),
        sig="def max_kelements(nums: List[int], k: int) -> int:",
        fn="max_kelements",
        tests=[
            (([10, 10, 10, 10, 10], 5), 50),
            (([1, 10, 3, 3, 3], 3), 17),
            (([5], 2), 7),
            (([1, 1], 4), 4),
        ],
        hints=[
            "Taking the current maximum is always best: values only shrink after use.",
            "Re-finding the maximum with max() is O(n) per step.",
            "Use a max-heap: pop the biggest, add to the score, push back ceil(x / 3) = (x + 2) // 3.",
        ],
        pattern="Greedy with a max-heap",
        explain=(
            "An exchange argument shows picking the largest first can never be worse, and the heap keeps it "
            "available after every update."
        ),
        cx="O((n + k) log n) time",
        brute_cx="O(n * k) time - scan for the maximum every step",
        brute=r"""
# BRUTE FORCE: O(n * k) time - scan for the maximum every step
def max_kelements(nums, k):
    values, score = list(nums), 0
    for _ in range(k):
        i = values.index(max(values))
        score += values[i]
        values[i] = (values[i] + 2) // 3
    return score
""",
        solution=r"""
# OPTIMISED: O((n + k) log n) time
# Idea: Greedy with a max-heap
def max_kelements(nums, k):
    heap = [-x for x in nums]
    heapq.heapify(heap)
    score = 0

    for _ in range(k):
        biggest = -heapq.heappop(heap)
        score += biggest
        heapq.heappush(heap, -((biggest + 2) // 3))  # ceil(biggest / 3)

    return score
""",
    ),
    # ---- Remove Stones to Minimize the Total (LeetCode 1962) ----
    dict(
        title="Remove Stones to Minimize the Total",
        diff="M",
        lc=1962,
        slug="remove-stones-to-minimize-the-total",
        prompt=(
            "Exactly k times: choose a pile and remove floor(pile / 2) stones from it. Return the minimum possible "
            "total number of stones left."
        ),
        sig="def min_stone_sum(piles: List[int], k: int) -> int:",
        fn="min_stone_sum",
        tests=[
            (([5, 4, 9], 2), 12),
            (([4, 3, 6, 7], 3), 12),
            (([1], 5), 1),
            (([10], 1), 5),
        ],
        hints=[
            "Removing floor(p / 2) from a pile removes more the bigger the pile is.",
            "So always operate on the current largest pile.",
            "Max-heap: pop the largest p, push back p - p // 2 = ceil(p / 2); the answer is the sum of the heap.",
        ],
        pattern="Greedy with a max-heap",
        explain="The removal grows with the pile size, so the greedy choice is the largest pile at every step.",
        cx="O((n + k) log n) time",
        brute_cx="O(n * k) time - linear scan for the largest pile each time",
        brute=r"""
# BRUTE FORCE: O(n * k) time - linear scan for the largest pile each time
def min_stone_sum(piles, k):
    piles = list(piles)
    for _ in range(k):
        i = piles.index(max(piles))
        piles[i] -= piles[i] // 2
    return sum(piles)
""",
        solution=r"""
# OPTIMISED: O((n + k) log n) time
# Idea: Greedy with a max-heap
def min_stone_sum(piles, k):
    heap = [-p for p in piles]
    heapq.heapify(heap)
    for _ in range(k):
        biggest = -heapq.heappop(heap)
        heapq.heappush(heap, -(biggest - biggest // 2))  # keep ceil(biggest / 2)
    return -sum(heap)
""",
    ),
    # ---- Relative Ranks (LeetCode 506) ----
    dict(
        title="Relative Ranks",
        diff="E",
        lc=506,
        slug="relative-ranks",
        prompt=(
            "Athletes have distinct scores. Return each athlete's rank as text: 'Gold Medal', 'Silver Medal', "
            "'Bronze Medal' for places 1-3, then '4', '5', ... for the rest."
        ),
        sig="def find_relative_ranks(score: List[int]) -> List[str]:",
        fn="find_relative_ranks",
        tests=[
            (([5, 4, 3, 2, 1],), ["Gold Medal", "Silver Medal", "Bronze Medal", "4", "5"]),
            (([10, 3, 8, 9, 4],), ["Gold Medal", "5", "Bronze Medal", "Silver Medal", "4"]),
            (([1],), ["Gold Medal"]),
            (([2, 1],), ["Gold Medal", "Silver Medal"]),
        ],
        hints=[
            "The rank of a score is 1 + (the number of larger scores).",
            "Counting larger scores for every athlete is O(n^2).",
            "Sort the indices by score (or pop a max-heap of (score, index)); the position in that order is the rank.",
        ],
        pattern="Sort (or heap-pop) indices by score",
        explain="One sort produces all ranks together: the i-th largest score gets rank i + 1.",
        cx="O(n log n) time",
        brute_cx="O(n^2) time - count the larger scores for each athlete",
        brute=r"""
# BRUTE FORCE: O(n^2) time - count the larger scores for each athlete
def find_relative_ranks(score):
    medals = ["Gold Medal", "Silver Medal", "Bronze Medal"]
    out = []
    for s in score:
        rank = 1 + sum(1 for t in score if t > s)
        out.append(medals[rank - 1] if rank <= 3 else str(rank))
    return out
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Sort (or heap-pop) indices by score
def find_relative_ranks(score):
    medals = ["Gold Medal", "Silver Medal", "Bronze Medal"]
    result = [""] * len(score)
    for place, idx in enumerate(sorted(range(len(score)), key=lambda i: -score[i])):
        result[idx] = medals[place] if place < 3 else str(place + 1)
    return result
""",
    ),
    # ---- Maximum Product of Two Elements in an Array (LeetCode 1464) ----
    dict(
        title="Maximum Product of Two Elements in an Array",
        diff="E",
        lc=1464,
        slug="maximum-product-of-two-elements-in-an-array",
        prompt=(
            "Choose two different indices i and j and return the maximum value of (nums[i] - 1) * (nums[j] - 1). "
            "All numbers are at least 1."
        ),
        sig="def max_product(nums: List[int]) -> int:",
        fn="max_product",
        tests=[
            (([3, 4, 5, 2],), 12),
            (([1, 5, 4, 5],), 16),
            (([3, 7],), 12),
            (([2, 2],), 1),
        ],
        hints=[
            "Every (nums[k] - 1) is non-negative, so a bigger number can only help.",
            "Trying every pair is O(n^2).",
            "Only the two LARGEST values matter: find them in one pass (or heapq.nlargest(2, nums)).",
        ],
        pattern="Top-2 selection",
        explain=(
            "With non-negative factors the product is maximised by the two largest factors, which one pass can track."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - try every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - try every pair
def max_product(nums):
    return max((a - 1) * (b - 1) for a, b in itertools.combinations(nums, 2))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Top-2 selection
def max_product(nums):
    first = second = 0  # the two largest values seen so far
    for x in nums:
        if x > first:
            first, second = x, first
        elif x > second:
            second = x
    return (first - 1) * (second - 1)
""",
    ),
    # ---- Maximum Number of Events That Can Be Attended (LeetCode 1353) ----
    dict(
        title="Maximum Number of Events That Can Be Attended",
        diff="M",
        lc=1353,
        slug="maximum-number-of-events-that-can-be-attended",
        prompt=(
            "events[i] = [start, end]: event i can be attended on any single day d with start <= d <= end. You can "
            "attend at most one event per day. Return the maximum number of events you can attend."
        ),
        sig="def max_events(events: List[List[int]]) -> int:",
        fn="max_events",
        tests=[
            (([[1, 2], [2, 3], [3, 4]],), 3),
            (([[1, 2], [2, 3], [3, 4], [1, 2]],), 4),
            (([[1, 1], [1, 1], [1, 1]],), 1),
            (([[1, 100000]],), 1),
            (([[1, 5], [1, 5], [1, 5], [2, 3], [2, 3]],), 5),
        ],
        hints=[
            "Go through the days in order and decide what to attend each day.",
            "Among the events available today, the one that ENDS soonest is the most urgent.",
            (
                "Sort events by start; each day push the end times of newly available events on a min-heap, drop "
                "expired ones, and pop the earliest end to attend."
            ),
        ],
        pattern="Greedy by earliest deadline with a min-heap",
        explain=(
            "An exchange argument: attending the event with the earliest end never blocks a better schedule, since "
            "later events are still open tomorrow."
        ),
        cx="O(n log n + D) time",
        brute_cx="O(D * n) time - on every day scan all events for the most urgent available one",
        brute=r"""
# BRUTE FORCE: O(D * n) time - on every day scan all events for the most urgent available one
def max_events(events):
    last_day = max(end for _, end in events)
    done, attended = set(), 0

    for day in range(1, last_day + 1):
        best = None
        for i, (start, end) in enumerate(events):
            if i not in done and start <= day <= end and (best is None or end < events[best][1]):
                best = i  # the available event that ends soonest
        if best is not None:
            done.add(best)
            attended += 1

    return attended
""",
        solution=r"""
# OPTIMISED: O(n log n + D) time
# Idea: Greedy by earliest deadline with a min-heap
def max_events(events):
    events = sorted(events)
    heap, i, attended, day = [], 0, 0, 0

    while i < len(events) or heap:
        if not heap:
            day = max(day, events[i][0])  # jump over idle days

        while i < len(events) and events[i][0] <= day:
            heapq.heappush(heap, events[i][1])
            i += 1

        while heap and heap[0] < day:
            heapq.heappop(heap)  # expired

        if heap:
            heapq.heappop(heap)  # attend the event that ends soonest
            attended += 1

        day += 1

    return attended
""",
    ),
    # ---- Minimum Number of Refueling Stops (LeetCode 871) ----
    dict(
        title="Minimum Number of Refueling Stops",
        diff="H",
        lc=871,
        slug="minimum-number-of-refueling-stops",
        prompt=(
            "A car starts at position 0 with start_fuel units (1 unit = 1 mile). stations[i] = [position, fuel], "
            "sorted by position; stopping at a station gives you all of its fuel. Return the fewest stops to reach "
            "target, or -1."
        ),
        sig="def min_refuel_stops(target: int, start_fuel: int, stations: List[List[int]]) -> int:",
        fn="min_refuel_stops",
        tests=[
            ((1, 1, []), 0),
            ((100, 1, [[10, 100]]), -1),
            ((100, 10, [[10, 60], [20, 30], [30, 30], [60, 40]]), 2),
            ((100, 100, []), 0),
            ((50, 25, [[10, 15], [20, 20], [40, 30]]), 2),
        ],
        hints=[
            "DP: best[t] = furthest distance reachable with exactly t stops. O(n^2).",
            "Greedy: drive as far as possible, remembering fuel of stations you PASSED.",
            (
                "When you cannot go further, 'retroactively' stop at the passed station with the most fuel "
                "(max-heap). Count each such stop."
            ),
        ],
        pattern="Greedy with a max-heap of passed options",
        explain=(
            "Stopping late is never worse than stopping early, so postpone the decision until fuel actually runs "
            "out and then take the largest available refill."
        ),
        cx="O(n log n) time",
        brute_cx="O(n^2) time - DP over the number of stops",
        brute=r"""
# BRUTE FORCE: O(n^2) time - DP over the number of stops
def min_refuel_stops(target, start_fuel, stations):
    n = len(stations)
    reach = [start_fuel] + [0] * n  # reach[t] = furthest position with t stops

    for i, (pos, fuel) in enumerate(stations):
        for t in range(i, -1, -1):
            if reach[t] >= pos:
                reach[t + 1] = max(reach[t + 1], reach[t] + fuel)

    for t in range(n + 1):
        if reach[t] >= target:
            return t

    return -1
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Greedy with a max-heap of passed options
def min_refuel_stops(target, start_fuel, stations):
    heap, stops, reach, i = [], 0, start_fuel, 0  # heap: fuel of stations already passed (max-heap)

    while reach < target:
        while i < len(stations) and stations[i][0] <= reach:
            heapq.heappush(heap, -stations[i][1])
            i += 1
        if not heap:
            return -1  # stranded
        reach += -heapq.heappop(heap)  # refuel at the best passed station
        stops += 1

    return stops
""",
    ),
    # ---- Single-Threaded CPU (LeetCode 1834) ----
    dict(
        title="Single-Threaded CPU",
        diff="M",
        lc=1834,
        slug="single-threaded-cpu",
        prompt=(
            "tasks[i] = [enqueue_time, processing_time]. A single CPU runs one task at a time without interruption: "
            "when idle it takes, among tasks already enqueued, the one with the shortest processing time (smallest "
            "index on ties); if none is enqueued it waits for the next. Return the order in which tasks are "
            "processed (as indices)."
        ),
        sig="def get_order(tasks: List[List[int]]) -> List[int]:",
        fn="get_order",
        tests=[
            (([[1, 2], [2, 4], [3, 2], [4, 1]],), [0, 2, 3, 1]),
            (([[7, 10], [7, 12], [7, 5], [7, 4], [7, 2]],), [4, 3, 2, 0, 1]),
            (([[1, 1]],), [0]),
            (([[5, 2], [1, 3]],), [1, 0]),
        ],
        hints=[
            "Simulate time: keep the current time and the set of tasks that have been enqueued but not run.",
            "Choosing the shortest available job each time needs a priority queue ordered by (processing time, index).",
            (
                "Sort tasks by enqueue time; before each pick push all tasks with enqueue <= now; if the heap is "
                "empty jump `now` to the next enqueue time."
            ),
        ],
        pattern="Event simulation with a priority queue",
        explain=(
            "The heap holds exactly the tasks the CPU may choose from; sorting by enqueue time gives the arrival "
            "order cheaply."
        ),
        cx="O(n log n) time",
        brute_cx="O(n^2) time - scan all tasks for the best available one each time",
        brute=r"""
# BRUTE FORCE: O(n^2) time - scan all tasks for the best available one each time
def get_order(tasks):
    n, done, order, now = len(tasks), set(), [], 0

    while len(order) < n:
        ready = [(tasks[i][1], i) for i in range(n) if i not in done and tasks[i][0] <= now]

        if not ready:
            now = min(tasks[i][0] for i in range(n) if i not in done)  # idle until the next arrival
            continue

        _, i = min(ready)
        done.add(i)
        order.append(i)
        now += tasks[i][1]

    return order
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Event simulation with a priority queue
def get_order(tasks):
    arrivals = sorted(range(len(tasks)), key=lambda i: tasks[i][0])
    heap, order, now, k = [], [], 0, 0

    while k < len(arrivals) or heap:
        if not heap and now < tasks[arrivals[k]][0]:
            now = tasks[arrivals[k]][0]  # idle: jump to the next arrival

        while k < len(arrivals) and tasks[arrivals[k]][0] <= now:
            heapq.heappush(heap, (tasks[arrivals[k]][1], arrivals[k]))
            k += 1

        duration, i = heapq.heappop(heap)
        order.append(i)
        now += duration

    return order
""",
    ),
    # ---- Divide Intervals Into Minimum Number of Groups (LeetCode 2406) ----
    dict(
        title="Divide Intervals Into Minimum Number of Groups",
        diff="M",
        lc=2406,
        slug="divide-intervals-into-minimum-number-of-groups",
        prompt=(
            "Split the intervals [left, right] (inclusive) into groups so that no two intervals in the same group "
            "intersect (sharing an endpoint counts as intersecting). Return the minimum number of groups."
        ),
        sig="def min_groups(intervals: List[List[int]]) -> int:",
        fn="min_groups",
        tests=[
            (([[5, 10], [6, 8], [1, 5], [2, 3], [1, 10]],), 3),
            (([[1, 3], [5, 6], [8, 10], [11, 13]],), 1),
            (([[1, 1]],), 1),
            (([[1, 5], [5, 10]],), 2),
        ],
        hints=[
            "The answer equals the largest number of intervals covering a single point.",
            "Sort by start; keep a min-heap of the END times of the groups currently open.",
            (
                "For each interval: if the earliest-ending group ends BEFORE it starts, reuse that group (pop); "
                "then push the new end. The heap size at the end is the answer."
            ),
        ],
        pattern="Sort + min-heap of group end times (meeting-rooms pattern)",
        explain=(
            "The heap size is the number of simultaneously active groups; it only grows when no existing group is free."
        ),
        cx="O(n log n) time",
        brute_cx="O(n^2) time - for every interval's start count how many intervals cover that point",
        brute=r"""
# BRUTE FORCE: O(n^2) time - for every interval's start count how many intervals cover that point
def min_groups(intervals):
    best = 0
    for start, _ in intervals:  # the maximum overlap occurs at some interval's start
        covering = sum(1 for a, b in intervals if a <= start <= b)
        best = max(best, covering)
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Sort + min-heap of group end times (meeting-rooms pattern)
def min_groups(intervals):
    ends = []  # min-heap: end time of each open group
    for start, end in sorted(intervals):
        if ends and ends[0] < start:
            heapq.heapreplace(ends, end)  # reuse the group that is already finished
        else:
            heapq.heappush(ends, end)  # all groups still busy: open a new one
    return len(ends)
""",
    ),
    # ---- K-th Smallest Prime Fraction (LeetCode 786) ----
    dict(
        title="K-th Smallest Prime Fraction",
        diff="M",
        lc=786,
        slug="k-th-smallest-prime-fraction",
        prompt=(
            "arr is sorted ascending and contains 1 and distinct primes. For every i < j consider the fraction "
            "arr[i] / arr[j]. Return the k-th smallest fraction as [numerator, denominator] (k is 1-indexed)."
        ),
        sig="def kth_smallest_prime_fraction(arr: List[int], k: int) -> List[int]:",
        fn="kth_smallest_prime_fraction",
        tests=[
            (([1, 2, 3, 5], 3), [2, 5]),
            (([1, 7], 1), [1, 7]),
            (([1, 2, 3], 2), [1, 2]),
            (([1, 3, 5, 7], 4), [3, 7]),
        ],
        hints=[
            "There are n(n-1)/2 fractions - generating and sorting all of them is O(n^2 log n).",
            "For a fixed denominator arr[j], the fractions arr[0]/arr[j] < arr[1]/arr[j] < ... are already sorted.",
            (
                "Merge n - 1 sorted lists lazily: heap of (value, i, j); pop the smallest k times, each pop pushing "
                "(arr[i+1]/arr[j])."
            ),
        ],
        pattern="K-way merge of implicitly sorted lists",
        explain=(
            "Each denominator contributes a sorted sequence, so the k-th smallest overall is found after k pops of "
            "a heap with one entry per sequence."
        ),
        cx="O((n + k) log n) time",
        brute_cx="O(n^2 log n) time - build and sort every fraction",
        brute=r"""
# BRUTE FORCE: O(n^2 log n) time - build and sort every fraction
def kth_smallest_prime_fraction(arr, k):
    fractions = sorted(
        (arr[i] / arr[j], arr[i], arr[j]) for i in range(len(arr)) for j in range(i + 1, len(arr))
    )
    _, num, den = fractions[k - 1]
    return [num, den]
""",
        solution=r"""
# OPTIMISED: O((n + k) log n) time
# Idea: K-way merge of implicitly sorted lists
def kth_smallest_prime_fraction(arr, k):
    n = len(arr)
    heap = [(arr[0] / arr[j], 0, j) for j in range(1, n)]  # smallest fraction for each denominator
    heapq.heapify(heap)

    for _ in range(k - 1):
        _, i, j = heapq.heappop(heap)
        if i + 1 < j:  # the next numerator for the same denominator
            heapq.heappush(heap, (arr[i + 1] / arr[j], i + 1, j))

    _, i, j = heap[0]

    return [arr[i], arr[j]]
""",
    ),
]
