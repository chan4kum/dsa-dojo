"""extra batch of Greedy problems - the problem bank for the "greedy" topic.

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
    # ---- Lemonade Change (LeetCode 860) ----
    dict(
        title="Lemonade Change",
        diff="E",
        lc=860,
        slug="lemonade-change",
        prompt=(
            "Each lemonade costs $5. Customers pay with $5, $10 or $20 in order. You start with no change. Can you "
            "give correct change to everyone?"
        ),
        sig="def lemonade_change(bills: List[int]) -> bool:",
        fn="lemonade_change",
        tests=[
            (([5, 5, 5, 10, 20],), True),
            (([5, 5, 10, 10, 20],), False),
            (([5, 10],), True),
            (([10],), False),
            (([],), True),
            (([5, 5, 10, 20, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10, 5, 5, 20, 5, 20, 5],), True),
        ],
        hints=[
            "You only ever hand out $5 and $10 bills. Track how many of each you hold.",
            "For $20 prefer giving one $10 + one $5 (keeps the more useful $5 bills).",
            "Greedy: change for 20 -> try (10 + 5) first, else three 5s; otherwise fail.",
        ],
        pattern="Greedy: spend the least flexible bill first",
        explain=(
            "$5 bills are the universal change; $10 bills are only useful for $20 customers. So use up the less "
            "flexible bill first."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(2^n) time - DFS over both change options",
        brute=r"""
# BRUTE FORCE: O(2^n) time - DFS over both change options
def lemonade_change(bills):
    def go(i, fives, tens):
        if i == len(bills):
            return True
        b = bills[i]
        if b == 5:
            return go(i + 1, fives + 1, tens)
        if b == 10:
            return fives >= 1 and go(i + 1, fives - 1, tens + 1)
        if tens >= 1 and fives >= 1 and go(i + 1, fives - 1, tens - 1):
            return True
        return fives >= 3 and go(i + 1, fives - 3, tens)

    return go(0, 0, 0)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Greedy: spend the least flexible bill first
def lemonade_change(bills):
    fives = tens = 0
    for b in bills:
        if b == 5:
            fives += 1
        elif b == 10:
            if not fives:
                return False
            fives -= 1
            tens += 1
        else:
            if tens and fives:
                tens -= 1
                fives -= 1
            elif fives >= 3:
                fives -= 3
            else:
                return False
    return True
""",
    ),
    # ---- Queue Reconstruction by Height (LeetCode 406) ----
    dict(
        title="Queue Reconstruction by Height",
        diff="M",
        lc=406,
        slug="queue-reconstruction-by-height",
        prompt=(
            "people[i] = [h, k]: a person of height h with exactly k people in FRONT of them who are at least as "
            "tall. Reconstruct the queue."
        ),
        sig="def reconstruct_queue(people: List[List[int]]) -> List[List[int]]:",
        fn="reconstruct_queue",
        tests=[
            (([[7, 0], [4, 4], [7, 1], [5, 0], [6, 1], [5, 2]],), [[5, 0], [7, 0], [5, 2], [6, 1], [4, 4], [7, 1]]),
            (([[6, 0], [5, 0], [4, 0], [3, 2], [2, 2], [1, 4]],), [[4, 0], [5, 0], [2, 2], [3, 2], [1, 4], [6, 0]]),
            (([],), []),
            (([[3, 0]],), [[3, 0]]),
        ],
        hints=[
            "The tallest people are unaffected by shorter ones - place them first.",
            "Sort by height descending (ties by k ascending).",
            (
                "Insert each person at index k in the result list; taller ones are already in place, so k is "
                "exactly right."
            ),
        ],
        pattern="Greedy insertion order (place the constraint-free ones first)",
        explain="A shorter person never changes a taller person's k. Process tall -> short and insert at position k.",
        cx="O(n^2) time (list insert), O(n) space",
        brute_cx="O(n!) time - try every permutation",
        brute=r"""
# BRUTE FORCE: O(n!) time - try every permutation
def reconstruct_queue(people):
    for perm in itertools.permutations(people):
        ok = True
        for i, (h, k) in enumerate(perm):
            if sum(1 for q in perm[:i] if q[0] >= h) != k:
                ok = False
                break
        if ok:
            return [list(p) for p in perm]
    return []
""",
        solution=r"""
# OPTIMISED: O(n^2) time (list insert), O(n) space
# Idea: Greedy insertion order (place the constraint-free ones first)
def reconstruct_queue(people):
    out = []
    for h, k in sorted(people, key=lambda p: (-p[0], p[1])):
        out.insert(k, [h, k])
    return out
""",
    ),
    # ---- Wiggle Subsequence (LeetCode 376) ----
    dict(
        title="Wiggle Subsequence",
        diff="M",
        lc=376,
        slug="wiggle-subsequence",
        prompt=(
            "A wiggle sequence alternates strictly between rising and falling differences. Return the length of the "
            "longest wiggle subsequence."
        ),
        sig="def wiggle_max_length(nums: List[int]) -> int:",
        fn="wiggle_max_length",
        tests=[
            (([1, 7, 4, 9, 2, 5],), 6),
            (([1, 17, 5, 10, 13, 15, 10, 5, 16, 8],), 7),
            (([1, 2, 3, 4, 5, 6, 7, 8, 9],), 2),
            (([5],), 1),
            (([3, 3, 3],), 1),
            (([],), 0),
        ],
        hints=[
            "Only the peaks and valleys matter; a long upward run contributes just its end.",
            "Count the number of direction changes in the sequence of differences (ignoring zeros).",
            "Track the last non-zero sign; whenever the sign flips, length += 1.",
        ],
        pattern="Greedy: count direction changes (peaks and valleys)",
        explain=(
            "Inside a monotone run you can always drop the middle elements without losing wiggle count; only "
            "turning points add length."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - DP over (last index, last direction)",
        brute=r"""
# BRUTE FORCE: O(n^2) time - DP over (last index, last direction)
def wiggle_max_length(nums):
    n = len(nums)
    if n == 0:
        return 0
    up = [1] * n
    down = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[i] > nums[j]:
                up[i] = max(up[i], down[j] + 1)
            elif nums[i] < nums[j]:
                down[i] = max(down[i], up[j] + 1)
    return max(max(up), max(down))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Greedy: count direction changes (peaks and valleys)
def wiggle_max_length(nums):
    if not nums:
        return 0
    length, prev = 1, 0
    for a, b in zip(nums, nums[1:]):
        d = b - a
        if d and (prev == 0 or (d > 0) != (prev > 0)):
            length += 1
            prev = d
    return length
""",
    ),
]
