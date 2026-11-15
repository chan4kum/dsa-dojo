"""more Heap problems (batch 4) - part of the problem bank for the "heap" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- IPO (LeetCode 502) ----
    dict(
        title="IPO",
        diff="H",
        lc=502,
        slug="ipo",
        prompt=(
            "You start with capital w and may finish at most k projects. Project i needs capital[i] to start and "
            "adds profits[i] to your capital. Return the maximum final capital."
        ),
        sig="def find_maximized_capital(k: int, w: int, profits: List[int], capital: List[int]) -> int:",
        fn="find_maximized_capital",
        tests=[
            ((2, 0, [1, 2, 3], [0, 1, 1]), 4),
            ((3, 0, [1, 2, 3], [0, 1, 2]), 6),
            ((1, 0, [1], [1]), 0),
            ((2, 5, [1, 2, 3], [4, 4, 9]), 8),
        ],
        hints=[
            "At each step you may pick any project you can afford; the best choice is the one with the largest profit.",
            "Sort projects by required capital. Move every newly affordable project into a max-heap by profit.",
            (
                "Repeat k times: pop the most profitable affordable project and add its profit to w (stop if none "
                "is affordable)."
            ),
        ],
        pattern="Two structures: sorted list for 'unlocking', max-heap for 'best now'",
        explain=(
            "Capital only grows, so a project once affordable stays affordable. A pointer over the sorted list "
            "unlocks projects once; the heap gives the best in O(log n)."
        ),
        cx="O(n log n + k log n) time",
        brute_cx="O(k * n) time - rescan all projects every round",
        brute=r"""
# BRUTE FORCE: O(k * n) time - rescan all projects every round
def find_maximized_capital(k, w, profits, capital):
    done = set()
    for _ in range(k):
        best = -1
        for i in range(len(profits)):
            if i not in done and capital[i] <= w and (best == -1 or profits[i] > profits[best]):
                best = i  # the most profitable project we can afford right now
        if best == -1:
            break
        done.add(best)
        w += profits[best]
    return w
""",
        solution=r"""
# OPTIMISED: O(n log n + k log n) time
# Idea: Two structures: sorted list for 'unlocking', max-heap for 'best now'
def find_maximized_capital(k, w, profits, capital):
    projects = sorted(zip(capital, profits))  # cheapest to start first
    heap, i = [], 0
    for _ in range(k):
        while i < len(projects) and projects[i][0] <= w:
            heapq.heappush(heap, -projects[i][1])  # negated: heapq is a min-heap
            i += 1
        if not heap:
            break
        w -= heapq.heappop(heap)  # take the best affordable profit
    return w
""",
    ),
]
