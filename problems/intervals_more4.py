"""more Intervals problems (batch 5) - part of the problem bank for the "intervals" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Find Right Interval (LeetCode 436) ----
    dict(
        title="Find Right Interval",
        diff="M",
        lc=436,
        slug="find-right-interval",
        prompt=(
            "All interval start points are unique. The right interval of interval i is the interval j with the "
            "SMALLEST start such that start_j >= end_i. Return, for every interval, the index of its right "
            "interval, or -1 if none exists."
        ),
        sig="def find_right_interval(intervals: List[List[int]]) -> List[int]:",
        fn="find_right_interval",
        tests=[
            (([[1, 2]],), [-1]),
            (([[3, 4], [2, 3], [1, 2]],), [-1, 0, 1]),
            (([[1, 4], [2, 3], [3, 4]],), [-1, 2, -1]),
            (([[1, 1]],), [0]),
        ],
        hints=[
            "For one interval you want the smallest start that is >= its end.",
            "Sort the (start, index) pairs once so 'smallest start >= x' becomes a search in a sorted list.",
            (
                "Use bisect_left on the sorted starts with the end as the key; map the found position back to the "
                "original index."
            ),
        ],
        pattern="Sort once + binary search per query",
        explain=(
            "After sorting by start, the right interval is the first start not below the end, which bisect_left "
            "finds in O(log n). Keeping the original index next to each start lets us answer in the original order."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2) time - scan every interval for every interval",
        brute=r"""
# BRUTE FORCE: O(n^2) time - scan every interval for every interval
def find_right_interval(intervals):
    result = []
    for i, (_, end) in enumerate(intervals):
        best = -1
        for j, (start, _) in enumerate(intervals):
            if start >= end and (best == -1 or start < intervals[best][0]):
                best = j  # smaller qualifying start wins
        result.append(best)
    return result
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Sort once + binary search per query
def find_right_interval(intervals):
    order = sorted((start, i) for i, (start, _) in enumerate(intervals))
    starts = [s for s, _ in order]
    result = []
    for _, end in intervals:
        pos = bisect.bisect_left(starts, end)  # first start that is >= end
        result.append(order[pos][1] if pos < len(order) else -1)
    return result
""",
    ),
    # ---- Maximum Length of Pair Chain (LeetCode 646) ----
    dict(
        title="Maximum Length of Pair Chain",
        diff="M",
        lc=646,
        slug="maximum-length-of-pair-chain",
        prompt=(
            "A pair [c, d] follows [a, b] if b < c. Return the length of the longest chain you can build from the "
            "given pairs (any subset, any order)."
        ),
        sig="def find_longest_chain(pairs: List[List[int]]) -> int:",
        fn="find_longest_chain",
        tests=[
            (([[1, 2], [2, 3], [3, 4]],), 2),
            (([[1, 2], [7, 8], [4, 5]],), 3),
            (([[1, 2]],), 1),
            (([[1, 5], [2, 3], [4, 6]],), 2),
        ],
        hints=[
            "This is activity selection: pick as many non-overlapping pairs as possible.",
            "Which pair should you take first? The one that ENDS earliest - it leaves the most room.",
            "Sort by end; keep the end of the last chosen pair and take every pair whose start is strictly greater.",
        ],
        pattern="Greedy: sort by end, take the earliest finisher",
        explain=(
            "Exchange argument: swapping any chain's first pair for the earliest-ending pair never breaks the "
            "chain, so greedy is optimal."
        ),
        cx="O(n log n) time",
        brute_cx="O(n^2) time - DP over pairs sorted by start",
        brute=r"""
# BRUTE FORCE: O(n^2) time - DP over pairs sorted by start
def find_longest_chain(pairs):
    pairs = sorted(pairs)
    best = [1] * len(pairs)  # best[i]: longest chain ending with pairs[i]
    for i in range(len(pairs)):
        for j in range(i):
            if pairs[j][1] < pairs[i][0]:
                best[i] = max(best[i], best[j] + 1)
    return max(best)
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Greedy: sort by end, take the earliest finisher
def find_longest_chain(pairs):
    count, last_end = 0, float("-inf")
    for start, end in sorted(pairs, key=lambda p: p[1]):
        if start > last_end:  # fits after the previous pair
            count += 1
            last_end = end
    return count
""",
    ),
    # ---- Car Pooling (LeetCode 1094) ----
    dict(
        title="Car Pooling",
        diff="M",
        lc=1094,
        slug="car-pooling",
        prompt=(
            "A car has `capacity` empty seats and only drives east. Each trip is [passengers, from, to]; passengers "
            "get in at `from` and out at `to` (they leave BEFORE new passengers board at the same point). Return "
            "True if every trip can be done without ever exceeding capacity."
        ),
        sig="def car_pooling(trips: List[List[int]], capacity: int) -> bool:",
        fn="car_pooling",
        tests=[
            (([[2, 1, 5], [3, 3, 7]], 4), False),
            (([[2, 1, 5], [3, 3, 7]], 5), True),
            (([[3, 2, 7], [3, 7, 9], [8, 3, 9]], 11), True),
            (([[1, 0, 1]], 1), True),
        ],
        hints=[
            "The load only changes at pick-up and drop-off points.",
            "Add +passengers at `from` and -passengers at `to` in a difference array (or sorted events).",
            "Sweep the points in order, keeping a running total; if it ever exceeds capacity the answer is False.",
        ],
        pattern="Difference array / sweep line",
        explain=(
            "Recording only the changes and prefix-summing them gives the load at every point in one pass instead "
            "of re-adding each trip."
        ),
        cx="O(n + max_to) time",
        brute_cx="O(n * range) time - add each trip to every point it covers",
        brute=r"""
# BRUTE FORCE: O(n * range) time - add each trip to every point it covers
def car_pooling(trips, capacity):
    for point in range(max(t[2] for t in trips) + 1):
        load = sum(p for p, a, b in trips if a <= point < b)  # trip covers [from, to)
        if load > capacity:
            return False
    return True
""",
        solution=r"""
# OPTIMISED: O(n + max_to) time
# Idea: Difference array / sweep line
def car_pooling(trips, capacity):
    change = [0] * (max(t[2] for t in trips) + 1)
    for passengers, start, end in trips:
        change[start] += passengers
        change[end] -= passengers  # they leave before anyone boards at `end`
    load = 0
    for delta in change:
        load += delta
        if load > capacity:
            return False
    return True
""",
    ),
    # ---- Corporate Flight Bookings (LeetCode 1109) ----
    dict(
        title="Corporate Flight Bookings",
        diff="M",
        lc=1109,
        slug="corporate-flight-bookings",
        prompt=(
            "Flights are labelled 1..n. A booking [first, last, seats] reserves `seats` seats on every flight from "
            "first to last inclusive. Return an array with the total seats reserved on each flight."
        ),
        sig="def corp_flight_bookings(bookings: List[List[int]], n: int) -> List[int]:",
        fn="corp_flight_bookings",
        tests=[
            (([[1, 2, 10], [2, 3, 20], [2, 5, 25]], 5), [10, 55, 45, 25, 25]),
            (([[1, 2, 10], [2, 2, 15]], 2), [10, 25]),
            (([[1, 1, 5]], 1), [5]),
            (([[2, 3, 4]], 4), [0, 4, 4, 0]),
        ],
        hints=[
            "Adding seats to every flight of every booking is slow when ranges are long.",
            "Instead mark only the endpoints: +seats at first, -seats just after last.",
            "A prefix sum over those marks gives each flight's total.",
        ],
        pattern="Difference array",
        explain="A range update becomes two point updates; one prefix-sum pass then reconstructs every position.",
        cx="O(n + bookings) time",
        brute_cx="O(bookings * n) time - add seats flight by flight",
        brute=r"""
# BRUTE FORCE: O(bookings * n) time - add seats flight by flight
def corp_flight_bookings(bookings, n):
    seats = [0] * n
    for first, last, count in bookings:
        for flight in range(first, last + 1):
            seats[flight - 1] += count
    return seats
""",
        solution=r"""
# OPTIMISED: O(n + bookings) time
# Idea: Difference array
def corp_flight_bookings(bookings, n):
    diff = [0] * (n + 1)
    for first, last, count in bookings:
        diff[first - 1] += count
        diff[last] -= count  # just past the last booked flight
    result, running = [], 0
    for i in range(n):
        running += diff[i]
        result.append(running)
    return result
""",
    ),
    # ---- Meeting Scheduler (LeetCode 1229) ----
    dict(
        title="Meeting Scheduler",
        diff="M",
        lc=1229,
        slug="meeting-scheduler",
        prompt=(
            "Two people have lists of free time slots [start, end]; slots within one person never overlap. Return "
            "the EARLIEST time slot [start, start + duration] that fits inside a slot of each person, or [] if none "
            "exists."
        ),
        sig="def min_available_duration(slots1: List[List[int]], slots2: List[List[int]], duration: int) -> List[int]:",
        fn="min_available_duration",
        tests=[
            (([[10, 50], [60, 120], [140, 210]], [[0, 15], [60, 70]], 8), [60, 68]),
            (([[10, 50], [60, 120], [140, 210]], [[0, 15], [60, 70]], 12), []),
            (([[0, 5]], [[0, 5]], 5), [0, 5]),
            (([[0, 5]], [[6, 9]], 1), []),
        ],
        hints=[
            "Two slots can host the meeting if their overlap (max of starts to min of ends) is long enough.",
            "Sort both lists by start and walk them with two pointers.",
            (
                "At each step compute the overlap; if it fits, return it. Otherwise advance the pointer whose slot "
                "ENDS first."
            ),
        ],
        pattern="Two pointers over two sorted interval lists",
        explain=(
            "The slot that ends first can never overlap with anything later in the other list, so dropping it loses "
            "nothing - and the first fitting overlap found is the earliest."
        ),
        cx="O(n log n + m log m) time",
        brute_cx="O(n * m) time - test every pair of slots and keep the earliest",
        brute=r"""
# BRUTE FORCE: O(n * m) time - test every pair of slots and keep the earliest
def min_available_duration(slots1, slots2, duration):
    best = []
    for a_start, a_end in slots1:
        for b_start, b_end in slots2:
            start = max(a_start, b_start)
            if min(a_end, b_end) - start >= duration and (not best or start < best[0]):
                best = [start, start + duration]
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n + m log m) time
# Idea: Two pointers over two sorted interval lists
def min_available_duration(slots1, slots2, duration):
    slots1, slots2 = sorted(slots1), sorted(slots2)
    i = j = 0
    while i < len(slots1) and j < len(slots2):
        start = max(slots1[i][0], slots2[j][0])
        end = min(slots1[i][1], slots2[j][1])
        if end - start >= duration:
            return [start, start + duration]
        if slots1[i][1] < slots2[j][1]:  # the slot that finishes first is exhausted
            i += 1
        else:
            j += 1
    return []
""",
    ),
    # ---- Remove Interval (LeetCode 1272) ----
    dict(
        title="Remove Interval",
        diff="M",
        lc=1272,
        slug="remove-interval",
        prompt=(
            "intervals is a sorted list of disjoint half-open intervals [l, r). Remove every real number in [a, b) "
            "(to_be_removed) from them and return the remaining intervals, still sorted."
        ),
        sig="def remove_interval(intervals: List[List[int]], to_be_removed: List[int]) -> List[List[int]]:",
        fn="remove_interval",
        tests=[
            (([[0, 2], [3, 4], [5, 7]], [1, 6]), [[0, 1], [6, 7]]),
            (([[0, 5]], [2, 3]), [[0, 2], [3, 5]]),
            (([[-5, -4], [-3, -2], [1, 2], [3, 5], [8, 9]], [-1, 4]), [[-5, -4], [-3, -2], [4, 5], [8, 9]]),
            (([[0, 1]], [5, 6]), [[0, 1]]),
        ],
        hints=[
            "Handle each interval on its own - there are only three cases.",
            (
                "No overlap: keep it whole. Overlap: keep the part left of a and the part right of b (when they are "
                "non-empty)."
            ),
            "Two intervals overlap exactly when l < b and r > a.",
        ],
        pattern="Per-interval case analysis",
        explain=(
            "Intervals are disjoint, so what remains of each one is independent of the others: at most a left piece "
            "and a right piece."
        ),
        cx="O(n) time",
        brute_cx="O(total length) time - test every unit cell, then group runs",
        brute=r"""
# BRUTE FORCE: O(total length) time - test every unit cell, then group runs
def remove_interval(intervals, to_be_removed):
    a, b = to_be_removed
    result = []
    for left, right in intervals:
        run = None
        for x in range(left, right):  # unit cell [x, x + 1)
            if a <= x < b:
                run = None  # this cell is deleted
            elif run is None:
                run = [x, x + 1]
                result.append(run)
            else:
                run[1] = x + 1
    return result
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Per-interval case analysis
def remove_interval(intervals, to_be_removed):
    a, b = to_be_removed
    result = []
    for left, right in intervals:
        if right <= a or left >= b:  # no overlap
            result.append([left, right])
            continue
        if left < a:
            result.append([left, a])  # left remainder
        if right > b:
            result.append([b, right])  # right remainder
    return result
""",
    ),
    # ---- Meeting Rooms III (LeetCode 2402) ----
    dict(
        title="Meeting Rooms III",
        diff="H",
        lc=2402,
        slug="meeting-rooms-iii",
        prompt=(
            "There are n rooms numbered 0..n-1. Meetings [start, end) have unique start times. Each meeting takes "
            "the lowest-numbered FREE room at its start. If every room is busy it waits for the first room to free "
            "up (lowest number on ties) and keeps its duration. Earlier original start times get priority. Return "
            "the number of the room that hosts the most meetings (lowest number on ties)."
        ),
        sig="def most_booked(n: int, meetings: List[List[int]]) -> int:",
        fn="most_booked",
        tests=[
            ((2, [[0, 10], [1, 5], [2, 7], [3, 4]]), 0),
            ((3, [[1, 20], [2, 10], [3, 5], [4, 9], [6, 8]]), 1),
            ((1, [[0, 1], [1, 2]]), 0),
            ((2, [[0, 5], [1, 2]]), 0),
        ],
        hints=[
            "Process the meetings in order of start time, tracking when each room becomes free.",
            (
                "For each meeting: use the lowest-numbered room whose free time <= start; else the room with the "
                "smallest free time (lowest number on ties), starting at that time."
            ),
            "Make it fast with two heaps: free rooms by number, and busy rooms by (free time, number).",
        ],
        pattern="Simulation with two heaps",
        explain=(
            "One heap answers 'lowest free room' and the other answers 'which busy room frees first'; each meeting "
            "moves a room from one heap to the other, so each step costs O(log n)."
        ),
        cx="O(m log m + m log n) time",
        brute_cx="O(m * n) time - scan every room for every meeting",
        brute=r"""
# BRUTE FORCE: O(m * n) time - scan every room for every meeting
def most_booked(n, meetings):
    free_at = [0] * n
    held = [0] * n
    for start, end in sorted(meetings):
        duration = end - start
        free = [r for r in range(n) if free_at[r] <= start]
        if free:
            room = free[0]  # lowest-numbered free room
            free_at[room] = end
        else:
            room = min(range(n), key=lambda r: (free_at[r], r))  # earliest to free up
            free_at[room] += duration
        held[room] += 1
    return held.index(max(held))
""",
        solution=r"""
# OPTIMISED: O(m log m + m log n) time
# Idea: Simulation with two heaps
def most_booked(n, meetings):
    free_rooms = list(range(n))  # already a valid min-heap
    busy = []  # (time the room frees, room number)
    held = [0] * n
    for start, end in sorted(meetings):
        while busy and busy[0][0] <= start:  # release rooms that are done by now
            heapq.heappush(free_rooms, heapq.heappop(busy)[1])
        if free_rooms:
            room = heapq.heappop(free_rooms)
            heapq.heappush(busy, (end, room))
        else:
            free_time, room = heapq.heappop(busy)  # wait for the earliest room
            heapq.heappush(busy, (free_time + end - start, room))
        held[room] += 1
    return held.index(max(held))
""",
    ),
    # ---- Maximum Distance in Arrays (LeetCode 624) ----
    dict(
        title="Maximum Distance in Arrays",
        diff="M",
        lc=624,
        slug="maximum-distance-in-arrays",
        prompt=(
            "You get several non-empty arrays, each sorted ascending. Pick one number from each of two DIFFERENT "
            "arrays; their distance is the absolute difference. Return the maximum possible distance."
        ),
        sig="def max_distance(arrays: List[List[int]]) -> int:",
        fn="max_distance",
        tests=[
            (([[1, 2, 3], [4, 5], [1, 2, 3]],), 4),
            (([[1], [1]],), 0),
            (([[1, 4], [0, 5]],), 4),
            (([[1, 5], [3], [2, 4]],), 3),
        ],
        hints=[
            "Because each array is sorted, only its first (min) and last (max) element can be an extreme.",
            "The best pair is (some array's max, another array's min) or the reverse.",
            (
                "Scan once, keeping the smallest min and largest max of the arrays seen so far; compare each new "
                "array's ends against them BEFORE merging it in."
            ),
        ],
        pattern="Running min/max across a scan",
        explain=(
            "Checking the new array against earlier arrays only guarantees the two numbers come from different "
            "arrays, and the sorted order means ends are all that matter."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - compare the ends of every pair of arrays",
        brute=r"""
# BRUTE FORCE: O(n^2) time - compare the ends of every pair of arrays
def max_distance(arrays):
    best = 0
    for i in range(len(arrays)):
        for j in range(len(arrays)):
            if i != j:
                best = max(best, abs(arrays[i][-1] - arrays[j][0]))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Running min/max across a scan
def max_distance(arrays):
    low, high = arrays[0][0], arrays[0][-1]
    best = 0
    for arr in arrays[1:]:
        best = max(best, abs(arr[-1] - low), abs(high - arr[0]))
        low, high = min(low, arr[0]), max(high, arr[-1])
    return best
""",
    ),
]
