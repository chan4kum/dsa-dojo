"""extra batch of Intervals problems - the problem bank for the "intervals" topic (batch 5).

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
Optional keys: compare (how to compare answers), adapt_in/adapt_out (convert lists <-> linked lists / trees),
check (validate any correct answer), inplace (which argument is mutated), kind="design" + cls (class problems).
"""

PROBLEMS = [
    # ---- My Calendar I (LeetCode 729) ----
    dict(
        title="My Calendar I",
        diff="M",
        lc=729,
        slug="my-calendar-i",
        prompt=(
            "Implement a calendar. book(start, end) tries to add the half-open event [start, end) and returns True "
            "only if it does not overlap any event already booked (otherwise it adds nothing and returns False)."
        ),
        sig=(
            "class MyCalendar:\n    def __init__(self):\n        pass\n    def book(self, startTime: int, endTime: "
            "int) -> bool:\n        pass"
        ),
        kind="design",
        cls="MyCalendar",
        tests=[
            (
                (),
                [
                    ("book", [10, 20], True),
                    ("book", [15, 25], False),
                    ("book", [20, 30], True),
                    ("book", [5, 10], True),
                    ("book", [0, 6], False),
                    ("book", [0, 5], True),
                ],
            ),
            ((), [("book", [1, 2], True), ("book", [1, 2], False), ("book", [2, 3], True)]),
            ((), [("book", [0, 100], True), ("book", [50, 51], False), ("book", [100, 101], True)]),
        ],
        hints=[
            "Two half-open events [a, b) and [c, d) overlap exactly when a < d and c < b.",
            "Checking every booked event is O(n) per call - fine to start with.",
            (
                "Keep the booked events sorted by start: only the event just before and the event just after the "
                "new one can overlap it. Find the spot with bisect."
            ),
        ],
        pattern="Sorted list + binary search: only the two neighbours can overlap",
        explain=(
            "Booked events never overlap each other, so when they are sorted by start they are also sorted by end. "
            "A new event can only collide with the event that starts just before it (if that one ends after the new "
            "start) or the event that starts just after it (if that one starts before the new end). bisect finds "
            "the insertion point, and two comparisons decide the answer."
        ),
        cx="book: O(log n) to search, O(n) to insert into the list",
        brute_cx="book: O(n) - compare with every booked event",
        brute=r"""
# BRUTE FORCE: book: O(n) - compare with every booked event
class MyCalendar:
    def __init__(self):
        self.events = []

    def book(self, startTime, endTime):
        for s, e in self.events:
            if startTime < e and s < endTime:
                return False
        self.events.append((startTime, endTime))
        return True
""",
        solution=r"""
# OPTIMISED: book: O(log n) to search, O(n) to insert into the list
# Idea: Sorted list + binary search: only the two neighbours can overlap
class MyCalendar:
    def __init__(self):
        self.events = []

    def book(self, startTime, endTime):
        i = bisect.bisect_left(self.events, (startTime, endTime))
        if i > 0 and self.events[i - 1][1] > startTime:
            return False
        if i < len(self.events) and self.events[i][0] < endTime:
            return False
        self.events.insert(i, (startTime, endTime))
        return True
""",
    ),
    # ---- My Calendar II (LeetCode 731) ----
    dict(
        title="My Calendar II",
        diff="M",
        lc=731,
        slug="my-calendar-ii",
        prompt=(
            "Like My Calendar I, but double bookings are allowed. book(start, end) adds the half-open event [start, "
            "end) and returns True unless that would create a TRIPLE booking (some instant covered by three "
            "events), in which case nothing is added and it returns False."
        ),
        sig=(
            "class MyCalendarTwo:\n    def __init__(self):\n        pass\n    def book(self, startTime: int, "
            "endTime: int) -> bool:\n        pass"
        ),
        kind="design",
        cls="MyCalendarTwo",
        tests=[
            (
                (),
                [
                    ("book", [10, 20], True),
                    ("book", [50, 60], True),
                    ("book", [10, 40], True),
                    ("book", [5, 15], False),
                    ("book", [5, 10], True),
                    ("book", [25, 55], True),
                ],
            ),
            ((), [("book", [1, 5], True), ("book", [1, 5], True), ("book", [1, 5], False), ("book", [5, 6], True)]),
            ((), [("book", [0, 10], True), ("book", [2, 4], True), ("book", [3, 5], False), ("book", [4, 6], True)]),
        ],
        hints=[
            "A triple booking exists exactly when the new event overlaps a region that is already double booked.",
            "Keep two lists: all booked events, and the regions that are already double booked.",
            (
                "On book: if [start, end) overlaps any double-booked region, reject. Otherwise add its overlaps "
                "with the single events to the double list, then add the event."
            ),
        ],
        pattern="Maintain the single-booked and double-booked regions",
        explain=(
            "If the new event touches any region that is already covered twice, some instant would be covered three "
            "times, so reject. Otherwise accept, and every overlap between the new event and an earlier event "
            "becomes a newly double-booked region. Rejected events must not change either list."
        ),
        cx="book: O(n) time, O(n) space",
        brute_cx="book: O(n) per call with a larger constant - recount coverage at every start point",
        brute=r"""
# BRUTE FORCE: book: O(n) per call with a larger constant - recount coverage at every start point
class MyCalendarTwo:
    def __init__(self):
        self.events = []

    def book(self, startTime, endTime):
        trial = self.events + [(startTime, endTime)]
        for point, _ in trial:
            if sum(1 for s, e in trial if s <= point < e) >= 3:
                return False
        self.events.append((startTime, endTime))
        return True
""",
        solution=r"""
# OPTIMISED: book: O(n) time, O(n) space
# Idea: Maintain the single-booked and double-booked regions
class MyCalendarTwo:
    def __init__(self):
        self.booked = []
        self.doubles = []

    def book(self, startTime, endTime):
        for s, e in self.doubles:
            if startTime < e and s < endTime:
                return False

        for s, e in self.booked:
            lo, hi = max(s, startTime), min(e, endTime)
            if lo < hi:
                self.doubles.append((lo, hi))

        self.booked.append((startTime, endTime))

        return True
""",
    ),
    # ---- My Calendar III (LeetCode 732) ----
    dict(
        title="My Calendar III",
        diff="H",
        lc=732,
        slug="my-calendar-iii",
        prompt=(
            "A k-booking is an instant covered by k events. book(start, end) adds the half-open event [start, end) "
            "and returns the largest k reached by any instant so far."
        ),
        sig=(
            "class MyCalendarThree:\n    def __init__(self):\n        pass\n    def book(self, startTime: int, "
            "endTime: int) -> int:\n        pass"
        ),
        kind="design",
        cls="MyCalendarThree",
        tests=[
            (
                (),
                [
                    ("book", [10, 20], 1),
                    ("book", [50, 60], 1),
                    ("book", [10, 40], 2),
                    ("book", [5, 15], 3),
                    ("book", [5, 10], 3),
                    ("book", [25, 55], 3),
                ],
            ),
            ((), [("book", [1, 2], 1), ("book", [2, 3], 1), ("book", [1, 3], 2)]),
            ((), [("book", [0, 10], 1), ("book", [0, 10], 2), ("book", [0, 10], 3), ("book", [10, 20], 3)]),
        ],
        hints=[
            (
                "The maximum overlap changes only at event boundaries: +1 at start, -1 at end, and you want the "
                "biggest running total."
            ),
            (
                "Re-sorting all boundaries on every call is O(n log n) per book. You need 'add 1 to a range, query "
                "the global maximum'."
            ),
            (
                "Use a dynamic segment tree over [0, 10^9] with range-add and a stored subtree maximum; only the "
                "nodes you touch are created."
            ),
        ],
        pattern="Dynamic segment tree: range add, global max (no push-down needed)",
        explain=(
            "Each node stores the maximum count in its range and an add-tag for the whole range. Adding an event "
            "bumps the tag of every node fully inside [start, end - 1]; partially covered nodes are recomputed as "
            "tag + max(children). The maximum for the whole timeline is the root value. Only O(log C) nodes are "
            "created per call, so the huge coordinate range costs nothing."
        ),
        cx="book: O(log C) time with C = 10^9 coordinates, O(n log C) space",
        brute_cx="book: O(n log n) - sort all boundaries and sweep",
        brute=r"""
# BRUTE FORCE: book: O(n log n) - sort all boundaries and sweep
class MyCalendarThree:
    def __init__(self):
        self.events = []

    def book(self, startTime, endTime):
        self.events.append((startTime, endTime))
        points = sorted([(s, 1) for s, _ in self.events] + [(e, -1) for _, e in self.events])
        best = running = 0
        for _, delta in points:
            running += delta
            best = max(best, running)
        return best
""",
        solution=r"""
# OPTIMISED: book: O(log C) time with C = 10^9 coordinates, O(n log C) space
# Idea: Dynamic segment tree: range add, global max (no push-down needed)
class MyCalendarThree:
    def __init__(self):
        self.best = defaultdict(int)
        self.tag = defaultdict(int)

    def _add(self, start, end, lo, hi, node):
        if start > hi or end < lo:
            return

        if start <= lo and hi <= end:
            self.best[node] += 1
            self.tag[node] += 1
            return

        mid = (lo + hi) // 2
        self._add(start, end, lo, mid, 2 * node)
        self._add(start, end, mid + 1, hi, 2 * node + 1)
        self.best[node] = self.tag[node] + max(self.best[2 * node], self.best[2 * node + 1])

    def book(self, startTime, endTime):
        self._add(startTime, endTime - 1, 0, 10**9, 1)
        return self.best[1]
""",
    ),
    # ---- Set Intersection Size At Least Two (LeetCode 757) ----
    dict(
        title="Set Intersection Size At Least Two",
        diff="H",
        lc=757,
        slug="set-intersection-size-at-least-two",
        prompt=(
            "intervals[i] = [start, end] (inclusive integers, start < end). Find the smallest set of integers that "
            "has at least two elements inside every interval and return its size."
        ),
        sig="def intersection_size_two(intervals: List[List[int]]) -> int:",
        fn="intersection_size_two",
        tests=[
            (([[1, 3], [3, 7], [8, 9]],), 5),
            (([[1, 3], [1, 4], [2, 5], [3, 5]],), 3),
            (([[1, 2], [2, 3], [2, 4], [4, 5]],), 5),
            (([[1, 2]],), 2),
            (([[1, 5], [2, 3]],), 2),
        ],
        hints=[
            (
                "Picking numbers as far right as possible inside an interval is never worse - they help later "
                "intervals more."
            ),
            "Sort by end ascending (and by start descending on ties) and keep the two largest chosen numbers.",
            (
                "For the next interval: if neither chosen number is inside, add end-1 and end; if only the larger "
                "one is inside, add end; if both are inside, add nothing."
            ),
        ],
        pattern="Greedy: sort by right end, keep the two rightmost chosen points",
        explain=(
            "Process intervals by increasing end. The two largest chosen values a < b tell how much of the next "
            "interval is already served: if start > b it has 0 chosen points, so take its last two values; if a < "
            "start <= b it has one, so take its end. Choosing the rightmost values keeps the most options for the "
            "intervals that follow, which is the exchange argument behind the greedy. Ties on end are processed by "
            "larger start first so a tighter interval is satisfied before a looser one."
        ),
        cx="O(n log n) time, O(1) extra space",
        brute_cx=(
            "exponential - try every subset of the integers between the smallest start and the largest end, by "
            "increasing size"
        ),
        brute=r"""
# BRUTE FORCE: exponential - try every subset of the integers in range, by increasing size
def intersection_size_two(intervals):
    low = min(s for s, _ in intervals)
    high = max(e for _, e in intervals)
    universe = range(low, high + 1)
    for size in range(2, len(universe) + 1):
        for chosen in itertools.combinations(universe, size):
            if all(sum(1 for x in chosen if s <= x <= e) >= 2 for s, e in intervals):
                return size
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space
# Idea: Greedy: sort by right end, keep the two rightmost chosen points
def intersection_size_two(intervals):
    intervals = sorted(intervals, key=lambda iv: (iv[1], -iv[0]))
    a = b = -1
    total = 0

    for start, end in intervals:
        if start > b:
            total += 2
            a, b = end - 1, end
        elif start > a:
            total += 1
            a, b = (b, end) if end != b else (end - 1, end)

    return total
""",
    ),
    # ---- Rectangle Area II (LeetCode 850) ----
    dict(
        title="Rectangle Area II",
        diff="H",
        lc=850,
        slug="rectangle-area-ii",
        prompt=(
            "rectangles[i] = [x1, y1, x2, y2] is an axis-aligned rectangle (bottom-left and top-right corners). "
            "Return the total area covered by the union of all rectangles, modulo 1_000_000_007."
        ),
        sig="def rectangle_area(rectangles: List[List[int]]) -> int:",
        fn="rectangle_area",
        tests=[
            (([[0, 0, 2, 2], [1, 0, 2, 3], [1, 0, 3, 1]],), 6),
            (([[0, 0, 1000000000, 1000000000]],), 49),
            (([[0, 0, 1, 1], [2, 2, 3, 3]],), 2),
            (([[0, 0, 2, 2], [1, 1, 3, 3]],), 7),
            (([[0, 0, 2, 2], [0, 0, 2, 2]],), 4),
        ],
        hints=[
            (
                "Adding the areas double counts overlaps. Cut the plane into vertical slabs between consecutive "
                "x-coordinates where nothing changes."
            ),
            (
                "Inside one slab the covered height is the length of the union of the y-ranges of the rectangles "
                "that span the slab."
            ),
            (
                "Sweep x left to right: add a rectangle's y-range at x1, remove it at x2; before each change add "
                "(covered y-length) * (width since the last event)."
            ),
        ],
        pattern="Sweep line over x; union length of the active y-intervals",
        explain=(
            "Between two consecutive event x-coordinates the set of rectangles that cross the slab is fixed, so the "
            "covered area of the slab is width * (length of the union of their y-intervals). The union length is "
            "the classic merge-sorted-intervals computation. Summing over slabs counts every covered unit exactly "
            "once."
        ),
        cx="O(n^2 log n) time (re-merge the active set per event); O(n log n) with a segment tree",
        brute_cx="O(n^3) time - compress both axes and mark every grid cell covered by any rectangle",
        brute=r"""
# BRUTE FORCE: O(n^3) time - compress both axes and mark every grid cell covered by any rectangle
def rectangle_area(rectangles):
    xs = sorted({x for r in rectangles for x in (r[0], r[2])})
    ys = sorted({y for r in rectangles for y in (r[1], r[3])})
    area = 0

    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            if any(
                r[0] <= xs[i] and xs[i + 1] <= r[2] and r[1] <= ys[j] and ys[j + 1] <= r[3]
                for r in rectangles
            ):
                area += (xs[i + 1] - xs[i]) * (ys[j + 1] - ys[j])

    return area % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n^2 log n) time (re-merge the active set per event); O(n log n) with a segment tree
# Idea: Sweep line over x; union length of the active y-intervals
def rectangle_area(rectangles):
    events = []

    for x1, y1, x2, y2 in rectangles:
        events.append((x1, 1, y1, y2))
        events.append((x2, -1, y1, y2))

    events.sort()
    active = []
    area = 0
    prev_x = events[0][0]

    for x, kind, y1, y2 in events:
        covered, reach = 0, float("-inf")

        for lo, hi in sorted(active):
            lo = max(lo, reach)
            if hi > lo:
                covered += hi - lo
                reach = hi

        area += covered * (x - prev_x)
        prev_x = x

        if kind == 1:
            active.append((y1, y2))
        else:
            active.remove((y1, y2))

    return area % (10**9 + 7)
""",
    ),
    # ---- Minimum Interval to Include Each Query (LeetCode 1851) ----
    dict(
        title="Minimum Interval to Include Each Query",
        diff="H",
        lc=1851,
        slug="minimum-interval-to-include-each-query",
        prompt=(
            "intervals[i] = [left, right] (inclusive) has size right - left + 1. For each query q return the size "
            "of the smallest interval with left <= q <= right, or -1 if none contains it."
        ),
        sig="def min_interval(intervals: List[List[int]], queries: List[int]) -> List[int]:",
        fn="min_interval",
        tests=[
            (([[1, 4], [2, 4], [3, 6], [4, 4]], [2, 3, 4, 5]), [3, 3, 1, 4]),
            (([[2, 3], [2, 5], [1, 8], [20, 25]], [2, 19, 5, 22]), [2, -1, 4, 6]),
            (([[1, 1]], [1, 2]), [1, -1]),
            (([[1, 10], [3, 4]], [3, 3, 11]), [2, 2, -1]),
        ],
        hints=[
            "Per query, scanning every interval is O(n * q). Answer the queries in increasing order instead.",
            (
                "Sort intervals by left. As the query value grows, push every interval with left <= q into a "
                "min-heap keyed by size."
            ),
            (
                "Before answering, pop heap tops whose right < q (they can never contain this or a later query). "
                "The top is the answer."
            ),
        ],
        pattern="Offline queries sorted + min-heap with lazy deletion",
        explain=(
            "Sorting the queries makes the set of 'started' intervals only grow. A heap ordered by size gives the "
            "smallest candidate; any interval that already ended before q can never help a later (larger) query, so "
            "it is discarded lazily when it surfaces at the top. Answers are written back at the queries' original "
            "positions."
        ),
        cx="O((n + q) log n) time, O(n + q) space",
        brute_cx="O(n * q) time - scan every interval for every query",
        brute=r"""
# BRUTE FORCE: O(n * q) time - scan every interval for every query
def min_interval(intervals, queries):
    answers = []
    for q in queries:
        sizes = [right - left + 1 for left, right in intervals if left <= q <= right]
        answers.append(min(sizes) if sizes else -1)
    return answers
""",
        solution=r"""
# OPTIMISED: O((n + q) log n) time, O(n + q) space
# Idea: Offline queries sorted + min-heap with lazy deletion
def min_interval(intervals, queries):
    intervals = sorted(intervals)
    answers = {}
    heap = []
    i = 0

    for q in sorted(set(queries)):
        while i < len(intervals) and intervals[i][0] <= q:
            left, right = intervals[i]
            heapq.heappush(heap, (right - left + 1, right))
            i += 1
        while heap and heap[0][1] < q:
            heapq.heappop(heap)
        answers[q] = heap[0][0] if heap else -1

    return [answers[q] for q in queries]
""",
    ),
    # ---- Count Ways to Group Overlapping Ranges (LeetCode 2580) ----
    dict(
        title="Count Ways to Group Overlapping Ranges",
        diff="M",
        lc=2580,
        slug="count-ways-to-group-overlapping-ranges",
        prompt=(
            "ranges[i] = [start, end] (inclusive). Split the ranges into two groups (either may be empty) so that "
            "any two ranges sharing at least one integer are in the same group. Return the number of ways, modulo "
            "1_000_000_007."
        ),
        sig="def count_ways(ranges: List[List[int]]) -> int:",
        fn="count_ways",
        tests=[
            (([[6, 10], [5, 15]],), 2),
            (([[1, 3], [10, 20], [2, 5], [4, 8]],), 4),
            (([[1, 1]],), 2),
            (([[1, 2], [3, 4], [5, 6]],), 8),
            (([[1, 5], [2, 3], [4, 6]],), 2),
        ],
        hints=[
            "Overlap is transitive through chains: if A overlaps B and B overlaps C, all three must share a group.",
            "So the ranges fall into connected blocks; each whole block goes to group 1 or group 2.",
            "Sort by start and merge overlapping ranges to count the blocks c; the answer is 2^c.",
        ],
        pattern="Merge intervals, count components, power of two",
        explain=(
            "Ranges that overlap (directly or through a chain) must all share a group, so each merged block makes "
            "one independent binary choice. Counting blocks is the standard sort-and-merge pass, and the answer is "
            "2^blocks modulo 1e9+7. Touching only at a shared integer counts as overlap, because ranges are "
            "inclusive."
        ),
        cx="O(n log n) time",
        brute_cx="O(2^n * n^2) time - try every assignment of ranges to the two groups",
        brute=r"""
# BRUTE FORCE: O(2^n * n^2) time - try every assignment of ranges to the two groups
def count_ways(ranges):
    n = len(ranges)
    total = 0

    for mask in range(1 << n):
        ok = True
        for i in range(n):
            for j in range(i + 1, n):
                overlap = ranges[i][0] <= ranges[j][1] and ranges[j][0] <= ranges[i][1]
                if overlap and (mask >> i & 1) != (mask >> j & 1):
                    ok = False
        total += ok

    return total % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Merge intervals, count components, power of two
def count_ways(ranges):
    blocks = 0
    reach = -1
    for start, end in sorted(ranges):
        if start > reach:
            blocks += 1
        reach = max(reach, end)
    return pow(2, blocks, 10**9 + 7)
""",
    ),
    # ---- Points That Intersect With Cars (LeetCode 2848) ----
    dict(
        title="Points That Intersect With Cars",
        diff="E",
        lc=2848,
        slug="points-that-intersect-with-cars",
        prompt=(
            "nums[i] = [start, end] is the inclusive range of integer points car i covers on a number line. Return "
            "how many integer points are covered by at least one car."
        ),
        sig="def number_of_points(nums: List[List[int]]) -> int:",
        fn="number_of_points",
        tests=[
            (([[3, 6], [1, 5], [4, 7]],), 7),
            (([[1, 3], [5, 8]],), 7),
            (([[1, 1]],), 1),
            (([[1, 5], [2, 3]],), 5),
            (([[1, 2], [3, 4]],), 4),
        ],
        hints=[
            "Marking every point of every car works, but it costs the sum of the lengths.",
            "Sort the cars by start and keep how far you have already counted.",
            "For each car add only the part to the right of the furthest point seen: end - max(start - 1, reach).",
        ],
        pattern="Sort and count the new part of each interval",
        explain=(
            "After sorting by start, everything up to `reach` is already counted. A car contributes only the points "
            "beyond reach, namely end - max(start - 1, reach) when positive. Because points are integers and ranges "
            "inclusive, the 'start - 1' keeps adjacent ranges like [1,2] and [3,4] from being merged into a "
            "non-existent overlap."
        ),
        cx="O(n log n) time, O(1) extra space",
        brute_cx="O(total length) time - add every covered point to a set",
        brute=r"""
# BRUTE FORCE: O(total length) time - add every covered point to a set
def number_of_points(nums):
    covered = set()
    for start, end in nums:
        covered.update(range(start, end + 1))
    return len(covered)
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space
# Idea: Sort and count the new part of each interval
def number_of_points(nums):
    total = 0
    reach = 0

    for start, end in sorted(nums):
        new_from = max(start - 1, reach)
        if end > new_from:
            total += end - new_from
            reach = end

    return total
""",
    ),
    # ---- Number of Flowers in Full Bloom (LeetCode 2251) ----
    dict(
        title="Number of Flowers in Full Bloom",
        diff="H",
        lc=2251,
        slug="number-of-flowers-in-full-bloom",
        prompt=(
            "flowers[i] = [start, end] is the inclusive time range during which flower i is in bloom. For each time "
            "in people, return how many flowers are in bloom at that time."
        ),
        sig="def full_bloom_flowers(flowers: List[List[int]], people: List[int]) -> List[int]:",
        fn="full_bloom_flowers",
        tests=[
            (([[1, 6], [3, 7], [9, 12], [4, 13]], [2, 3, 7, 11]), [1, 2, 2, 2]),
            (([[1, 10], [3, 3]], [3, 3, 2]), [2, 2, 1]),
            (([[5, 5]], [4, 5, 6]), [0, 1, 0]),
            (([[1, 2], [2, 3]], [2]), [2]),
        ],
        hints=[
            "Per person, scanning all flowers is O(n * m).",
            "Flowers in bloom at t = flowers that have started by t minus flowers that have ended before t.",
            (
                "Sort all starts and all ends once; then bisect_right(starts, t) - bisect_left(ends, t) answers "
                "each person in O(log n)."
            ),
        ],
        pattern="Counting with two sorted arrays and binary search",
        explain=(
            "A flower blooms at time t iff start <= t and end >= t. The number of flowers that already started is "
            "the count of starts <= t; those that ended strictly before t are the count of ends < t (every flower "
            "that ended before t also started before t, so subtracting is exact). Two sorted arrays and two bisects "
            "give each answer."
        ),
        cx="O((n + m) log n) time, O(n) space",
        brute_cx="O(n * m) time - test every flower for every person",
        brute=r"""
# BRUTE FORCE: O(n * m) time - test every flower for every person
def full_bloom_flowers(flowers, people):
    return [sum(1 for s, e in flowers if s <= t <= e) for t in people]
""",
        solution=r"""
# OPTIMISED: O((n + m) log n) time, O(n) space
# Idea: Counting with two sorted arrays and binary search
def full_bloom_flowers(flowers, people):
    starts = sorted(s for s, _ in flowers)
    ends = sorted(e for _, e in flowers)
    return [bisect.bisect_right(starts, t) - bisect.bisect_left(ends, t) for t in people]
""",
    ),
    # ---- Maximum Profit in Job Scheduling (LeetCode 1235) ----
    dict(
        title="Maximum Profit in Job Scheduling",
        diff="H",
        lc=1235,
        slug="maximum-profit-in-job-scheduling",
        prompt=(
            "Job i runs from startTime[i] to endTime[i] and earns profit[i]. You can do jobs one after another, but "
            "a job that starts exactly when another ends is allowed. Return the maximum total profit of "
            "non-overlapping jobs."
        ),
        sig="def job_scheduling(startTime: List[int], endTime: List[int], profit: List[int]) -> int:",
        fn="job_scheduling",
        tests=[
            (([1, 2, 3, 3], [3, 4, 5, 6], [50, 10, 40, 70]), 120),
            (([1, 2, 3, 4, 6], [3, 5, 10, 6, 9], [20, 20, 100, 70, 60]), 150),
            (([1, 1, 1], [2, 3, 4], [5, 6, 4]), 6),
            (([1], [2], [7]), 7),
        ],
        hints=[
            (
                "For each job there are two choices: skip it, or take it and then continue with jobs that start "
                "after it ends."
            ),
            "Sort jobs by end time; let best[i] be the best profit using the first i jobs.",
            (
                "best[i] = max(best[i-1], profit[i] + best[j]) where j is the number of jobs that end <= start[i] - "
                "find j with bisect_right on the sorted end times."
            ),
        ],
        pattern="Weighted interval scheduling: DP over jobs sorted by end + binary search",
        explain=(
            "Sorted by end time, the optimum for the first i jobs either skips job i (best[i-1]) or takes it, in "
            "which case the compatible earlier jobs are exactly those ending no later than its start - a prefix of "
            "the sorted order found by binary search. Taking the maximum of the two options is optimal because the "
            "sub-problems are independent."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(2^n) time - for each job try skipping it and taking it",
        brute=r"""
# BRUTE FORCE: O(2^n) time - for each job try skipping it and taking it
def job_scheduling(startTime, endTime, profit):
    jobs = sorted(zip(startTime, endTime, profit))

    def best(i, free_at):
        if i == len(jobs):
            return 0
        start, end, gain = jobs[i]
        skip = best(i + 1, free_at)
        if start >= free_at:
            return max(skip, gain + best(i + 1, end))
        return skip

    return best(0, 0)
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Weighted interval scheduling: DP over jobs sorted by end + binary search
def job_scheduling(startTime, endTime, profit):
    jobs = sorted(zip(endTime, startTime, profit))
    ends = [e for e, _, _ in jobs]
    best = [0] * (len(jobs) + 1)
    for i, (_, start, gain) in enumerate(jobs, 1):
        j = bisect.bisect_right(ends, start, 0, i - 1)
        best[i] = max(best[i - 1], best[j] + gain)
    return best[-1]
""",
    ),
    # ---- Video Stitching (LeetCode 1024) ----
    dict(
        title="Video Stitching",
        diff="M",
        lc=1024,
        slug="video-stitching",
        prompt=(
            "clips[i] = [start, end] covers the time range [start, end] of an event. Using the fewest clips (they "
            "may overlap and be trimmed), cover the whole range [0, time]. Return that number, or -1 if impossible."
        ),
        sig="def video_stitching(clips: List[List[int]], time: int) -> int:",
        fn="video_stitching",
        tests=[
            (([[0, 2], [4, 6], [8, 10], [1, 9], [1, 5], [5, 9]], 10), 3),
            (([[0, 1], [1, 2]], 5), -1),
            (
                (
                    [
                        [0, 1],
                        [6, 8],
                        [0, 2],
                        [5, 6],
                        [0, 4],
                        [0, 3],
                        [6, 7],
                        [1, 3],
                        [4, 7],
                        [1, 4],
                        [2, 5],
                        [2, 6],
                        [3, 4],
                        [4, 5],
                        [5, 7],
                        [6, 9],
                    ],
                    9,
                ),
                3,
            ),
            (([[0, 5]], 3), 1),
            (([[1, 5]], 3), -1),
        ],
        hints=[
            "You need clips whose union covers [0, time] without gaps.",
            "dp[t] = fewest clips to cover [0, t]; a clip [a, b] improves dp[t] for t in (a, b] using dp[a].",
            (
                "Greedy alternative (like Jump Game II): among clips starting at or before the current reach, "
                "always extend to the furthest end."
            ),
        ],
        pattern="Interval covering: greedy furthest reach (or DP over time)",
        explain=(
            "Standing at `reach`, any clip that starts at or before reach keeps the coverage gap-free, and picking "
            "the one that ends furthest is never worse than another choice (exchange argument). Repeating until "
            "reach >= time counts the minimum clips; if no clip extends reach, there is a gap and the answer is -1."
        ),
        cx="O(n log n) time (sort), O(1) extra space",
        brute_cx="O(time * n) time - DP over every time point and every clip",
        brute=r"""
# BRUTE FORCE: O(time * n) time - DP over every time point and every clip
def video_stitching(clips, time):
    inf = float("inf")
    dp = [inf] * (time + 1)
    dp[0] = 0

    for t in range(1, time + 1):
        for a, b in clips:
            if a < t <= b:
                dp[t] = min(dp[t], dp[a] + 1)

    return dp[time] if dp[time] != inf else -1
""",
        solution=r"""
# OPTIMISED: O(n log n) time (sort), O(1) extra space
# Idea: Interval covering: greedy furthest reach (or DP over time)
def video_stitching(clips, time):
    clips = sorted(clips)
    count = reach = furthest = 0
    i = 0

    while reach < time:
        while i < len(clips) and clips[i][0] <= reach:
            furthest = max(furthest, clips[i][1])
            i += 1
        if furthest <= reach:
            return -1
        reach = furthest
        count += 1

    return count
""",
    ),
    # ---- Minimum Number of Taps to Open to Water a Garden (LeetCode 1326) ----
    dict(
        title="Minimum Number of Taps to Open to Water a Garden",
        diff="H",
        lc=1326,
        slug="minimum-number-of-taps-to-open-to-water-a-garden",
        prompt=(
            "A garden is the segment [0, n]. There are n + 1 taps at positions 0..n; tap i, when opened, waters [i "
            "- ranges[i], i + ranges[i]]. Return the fewest taps that water the whole garden, or -1."
        ),
        sig="def min_taps(n: int, ranges: List[int]) -> int:",
        fn="min_taps",
        tests=[
            ((5, [3, 4, 1, 1, 0, 0]), 1),
            ((3, [0, 0, 0, 0]), -1),
            ((7, [1, 2, 1, 0, 2, 1, 0, 1]), 3),
            ((8, [4, 0, 0, 0, 0, 0, 0, 0, 4]), 2),
            ((8, [4, 0, 0, 0, 4, 0, 0, 0, 4]), 1),
        ],
        hints=[
            "Each tap is an interval [i - r, i + r] - this is interval covering of [0, n].",
            "For every left endpoint remember the furthest right end any tap starting there reaches.",
            (
                "Then run the greedy jump: keep the current reach and the furthest reach seen so far; when you pass "
                "the current reach, open one more tap."
            ),
        ],
        pattern="Interval covering reduced to Jump Game II",
        explain=(
            "Let reach_from[l] be the furthest right end of any tap whose interval starts at l (clamped to 0). Then "
            "covering [0, n] is exactly a jump game where from position l you can jump to reach_from[l]. The greedy "
            "that extends to the furthest right whenever the current tap runs out is optimal, and a position that "
            "cannot be passed means -1."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(2^n) time - try every subset of taps and test whether it covers [0, n]",
        brute=r"""
# BRUTE FORCE: O(2^n) time - try every subset of taps and test whether it covers [0, n]
def min_taps(n, ranges):
    best = None

    for mask in range(1 << (n + 1)):
        spans = sorted((max(0, i - r), i + r) for i, r in enumerate(ranges) if mask >> i & 1)
        reach = 0

        for left, right in spans:
            if left <= reach:
                reach = max(reach, right)

        if reach >= n:
            count = bin(mask).count("1")
            best = count if best is None else min(best, count)

    return -1 if best is None else best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Interval covering reduced to Jump Game II
def min_taps(n, ranges):
    reach_from = [0] * (n + 1)

    for i, r in enumerate(ranges):
        left = max(0, i - r)
        reach_from[left] = max(reach_from[left], min(n, i + r))

    taps = cur_end = furthest = 0

    for i in range(n):
        furthest = max(furthest, reach_from[i])
        if i == cur_end:
            if furthest <= i:
                return -1
            taps += 1
            cur_end = furthest

    return taps
""",
    ),
    # ---- Two Best Non-Overlapping Events (LeetCode 2054) ----
    dict(
        title="Two Best Non-Overlapping Events",
        diff="M",
        lc=2054,
        slug="two-best-non-overlapping-events",
        prompt=(
            "events[i] = [start, end, value] (times inclusive). Attend at most two events that do not overlap (the "
            "second must start strictly after the first ends). Return the maximum total value."
        ),
        sig="def max_two_events(events: List[List[int]]) -> int:",
        fn="max_two_events",
        tests=[
            (([[1, 3, 2], [4, 5, 2], [2, 4, 3]],), 4),
            (([[1, 3, 2], [4, 5, 2], [1, 5, 5]],), 5),
            (([[1, 5, 3], [1, 5, 1], [6, 6, 5]],), 8),
            (([[1, 2, 7]],), 7),
            (([[1, 3, 4], [3, 5, 6]],), 6),
        ],
        hints=[
            "Pairs: O(n^2) works for small n. For large n, fix the second event and ask for the best first event.",
            "Sort events by end time and keep a running prefix maximum of values.",
            (
                "For each event, bisect for the last event that ends before it starts and add that prefix maximum; "
                "also consider the event alone."
            ),
        ],
        pattern="Sort by end, prefix maximum + binary search",
        explain=(
            "If the events are sorted by end time, all events that finish before a given event begins form a prefix "
            "of the order, found by binary search. The best single value inside that prefix is a running maximum, "
            "so each event pays O(log n) for its best partner. Taking a single event alone is covered by also "
            "comparing with the event value itself."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2) time - test every pair of events",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every pair of events
def max_two_events(events):
    best = max(v for _, _, v in events)
    for i, (_, e1, v1) in enumerate(events):
        for j, (s2, _, v2) in enumerate(events):
            if i != j and e1 < s2:
                best = max(best, v1 + v2)
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Sort by end, prefix maximum + binary search
def max_two_events(events):
    events = sorted(events, key=lambda ev: ev[1])
    ends = [e for _, e, _ in events]
    prefix_best = []
    top = 0

    for _, _, value in events:
        top = max(top, value)
        prefix_best.append(top)

    best = 0

    for start, _, value in events:
        j = bisect.bisect_left(ends, start) - 1
        best = max(best, value + (prefix_best[j] if j >= 0 else 0))

    return best
""",
    ),
    # ---- Shifting Letters II (LeetCode 2381) ----
    dict(
        title="Shifting Letters II",
        diff="M",
        lc=2381,
        slug="shifting-letters-ii",
        prompt=(
            "s is a lowercase string. shifts[i] = [start, end, direction]: shift every letter in s[start..end] "
            "forward (direction 1) or backward (direction 0) by one in the alphabet, wrapping z -> a and a -> z. "
            "Apply all shifts and return the resulting string."
        ),
        sig="def shifting_letters(s: str, shifts: List[List[int]]) -> str:",
        fn="shifting_letters",
        tests=[
            (("abc", [[0, 1, 0], [1, 2, 1], [0, 2, 1]]), "ace"),
            (("dztz", [[0, 0, 0], [1, 1, 1]]), "catz"),
            (("a", [[0, 0, 0]]), "z"),
            (("z", [[0, 0, 1], [0, 0, 1]]), "b"),
            (("abc", []), "abc"),
        ],
        hints=[
            "Applying each shift letter by letter is O(n * m).",
            "Only the NET number of shifts per position matters (mod 26).",
            (
                "Use a difference array: add +1/-1 at start, the opposite at end + 1; a prefix sum gives each "
                "position's net shift."
            ),
        ],
        pattern="Difference array (range add) + prefix sum",
        explain=(
            "Each shift is a +1 or -1 on a contiguous range. Recording only the range boundaries in a difference "
            "array and taking one running sum yields the net shift of every position in O(n + m). The result is "
            "reduced mod 26, and Python's % keeps negative shifts in range."
        ),
        cx="O(n + m) time, O(n) space",
        brute_cx="O(n * m) time - apply every shift to every letter in its range",
        brute=r"""
# BRUTE FORCE: O(n * m) time - apply every shift to every letter in its range
def shifting_letters(s, shifts):
    letters = [ord(ch) - 97 for ch in s]
    for start, end, direction in shifts:
        for i in range(start, end + 1):
            letters[i] = (letters[i] + (1 if direction else -1)) % 26
    return "".join(chr(97 + x) for x in letters)
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(n) space
# Idea: Difference array (range add) + prefix sum
def shifting_letters(s, shifts):
    diff = [0] * (len(s) + 1)

    for start, end, direction in shifts:
        step = 1 if direction else -1
        diff[start] += step
        diff[end + 1] -= step

    out = []
    running = 0

    for i, ch in enumerate(s):
        running += diff[i]
        out.append(chr((ord(ch) - 97 + running) % 26 + 97))

    return "".join(out)
""",
    ),
]
