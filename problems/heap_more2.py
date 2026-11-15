"""extra batch of Heap problems - the problem bank for the "heap" topic.

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

PROBLEMS = [
    # ---- Ugly Number II (LeetCode 264) ----
    dict(
        title="Ugly Number II",
        diff="M",
        lc=264,
        slug="ugly-number-ii",
        prompt=(
            "Ugly numbers have only prime factors 2, 3 and 5 (1 counts as ugly). Return the n-th ugly number "
            "(1-indexed)."
        ),
        sig="def nth_ugly_number(n: int) -> int:",
        fn="nth_ugly_number",
        tests=[
            ((10,), 12),
            ((1,), 1),
            ((7,), 8),
            ((15,), 24),
            ((20,), 36),
            ((2,), 2),
        ],
        hints=[
            "Every ugly number (except 1) is a smaller ugly number times 2, 3 or 5.",
            "Generate in increasing order with a min-heap and a seen set, OR with three pointers.",
            (
                "Three-pointer DP: ugly[i] = min(ugly[p2]*2, ugly[p3]*3, ugly[p5]*5); advance every pointer that "
                "produced the min."
            ),
        ],
        pattern="k-way merge of implicit sorted sequences (multiples of earlier results)",
        explain=(
            "The ugly numbers are the merge of three sorted lists (2x, 3x, 5x of the sequence itself). Pointers "
            "walk each list and skip duplicates."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n log n) time - heap + seen set",
        brute=r"""
# BRUTE FORCE: O(n log n) time - heap + seen set
def nth_ugly_number(n):
    h, seen, x = [1], {1}, 1
    for _ in range(n):
        x = heapq.heappop(h)
        for f in (2, 3, 5):
            if x * f not in seen:
                seen.add(x * f)
                heapq.heappush(h, x * f)
    return x
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: k-way merge of implicit sorted sequences (multiples of earlier results)
def nth_ugly_number(n):
    u = [1]
    i2 = i3 = i5 = 0
    while len(u) < n:
        nxt = min(u[i2] * 2, u[i3] * 3, u[i5] * 5)
        u.append(nxt)
        if nxt == u[i2] * 2:
            i2 += 1
        if nxt == u[i3] * 3:
            i3 += 1
        if nxt == u[i5] * 5:
            i5 += 1
    return u[n - 1]
""",
    ),
    # ---- Kth Smallest Element in a Sorted Matrix (LeetCode 378) ----
    dict(
        title="Kth Smallest Element in a Sorted Matrix",
        diff="M",
        lc=378,
        slug="kth-smallest-element-in-a-sorted-matrix",
        prompt=(
            "Rows and columns are both sorted ascending. Return the k-th smallest element (1-indexed) of the whole "
            "matrix."
        ),
        sig="def kth_smallest(matrix: List[List[int]], k: int) -> int:",
        fn="kth_smallest",
        tests=[
            (([[1, 5, 9], [10, 11, 13], [12, 13, 15]], 8), 13),
            (([[-5]], 1), -5),
            (([[1, 2], [1, 3]], 2), 1),
            (([[1, 3, 5], [6, 7, 12], [11, 14, 14]], 6), 11),
            (([[1, 2], [3, 4]], 4), 4),
        ],
        hints=[
            "Each row is a sorted list - you want the k-th item of the merge of rows.",
            "Min-heap seeded with each row's first element; pop k times, pushing the popped item's right neighbour.",
            "Alternative: binary search the VALUE and count elements <= mid with a staircase walk.",
        ],
        pattern="k-way merge with a heap (or binary search on value)",
        explain="You never need the whole sorted order - just pop the smallest k times, expanding only the frontier.",
        cx="O(k log n) time, O(n) space",
        brute_cx="O(n^2 log n) time - flatten and sort",
        brute=r"""
# BRUTE FORCE: O(n^2 log n) time - flatten and sort
def kth_smallest(matrix, k):
    return sorted(x for row in matrix for x in row)[k - 1]
""",
        solution=r"""
# OPTIMISED: O(k log n) time, O(n) space
# Idea: k-way merge with a heap (or binary search on value)
def kth_smallest(matrix, k):
    n = len(matrix)
    h = [(matrix[r][0], r, 0) for r in range(n)]
    heapq.heapify(h)
    for _ in range(k - 1):
        v, r, c = heapq.heappop(h)
        if c + 1 < len(matrix[r]):
            heapq.heappush(h, (matrix[r][c + 1], r, c + 1))
    return h[0][0]
""",
    ),
]
