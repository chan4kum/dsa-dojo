"""Greedy problems - the problem bank for the "greedy" topic.

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
    # ---- Jump Game (LeetCode 55) ----
    dict(
        title="Jump Game",
        diff="M",
        lc=55,
        slug="jump-game",
        prompt="nums[i] is the maximum jump length from index i. Starting at index 0, can you reach the last index?",
        sig="def can_jump(nums: List[int]) -> bool:",
        fn="can_jump",
        tests=[
            (([2, 3, 1, 1, 4],), True),
            (([3, 2, 1, 0, 4],), False),
            (([0],), True),
            (([0, 1],), False),
            (([2, 0, 0],), True),
            (([1, 1, 1, 1],), True),
        ],
        hints=[
            "Backtracking / DP over all jump choices is exponential or O(n^2).",
            "You only care about the FARTHEST index reachable so far, not how you got there.",
            "Scan left to right: if i > farthest you are stuck (False); else farthest = max(farthest, i + nums[i]).",
        ],
        pattern="Greedy: maintain the farthest reachable frontier",
        explain=(
            "Reachability is contiguous: if you can reach index j, you can reach everything before it too. So "
            "one\n        number (the frontier) summarises all possibilities. If the scan index ever exceeds the "
            "frontier, the\n        gap cannot be crossed. O(n) time, O(1) space."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="exponential - tries every jump length from every index",
        brute=r"""
# BRUTE FORCE: exponential - tries every jump length from every index
def can_jump(nums):
    def go(i):
        if i >= len(nums) - 1:
            return True
        return any(go(i + j) for j in range(1, nums[i] + 1))

    return go(0)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Greedy: maintain the farthest reachable frontier
def can_jump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
    return True
""",
    ),
    # ---- Gas Station (LeetCode 134) ----
    dict(
        title="Gas Station",
        diff="M",
        lc=134,
        slug="gas-station",
        prompt=(
            "Stations on a circle have gas[i] fuel and the trip to the next station costs cost[i]. Return the start "
            "index from which you can complete the full circle once, or -1. The answer is unique if it exists."
        ),
        sig="def can_complete_circuit(gas: List[int], cost: List[int]) -> int:",
        fn="can_complete_circuit",
        tests=[
            (([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]), 3),
            (([2, 3, 4], [3, 4, 3]), -1),
            (([5], [4]), 0),
            (([3, 1, 1], [1, 2, 2]), 0),
            (([2], [2]), 0),
        ],
        hints=[
            "If total gas < total cost, it is impossible - no start works.",
            (
                "If you run out of fuel going from start s to station j, then NO station between s and j can be a "
                "valid start either. Why?"
            ),
            "Track the tank; when it goes negative at i, reset the start to i+1 and the tank to 0.",
        ],
        pattern="Greedy with a 'discard the failed prefix' argument",
        explain=(
            "Any station k between s and the failure point j had a non-negative tank on arrival from s, so "
            "starting\n        at k is strictly worse than starting at s. Hence the next candidate is j+1. If the "
            "global surplus is\n        >= 0, the last surviving candidate works. One pass, O(n)."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) - simulate the trip from every start",
        brute=r"""
# BRUTE FORCE: O(n^2) - simulate the trip from every start
def can_complete_circuit(gas, cost):
    n = len(gas)

    for s in range(n):
        tank = 0

        for k in range(n):
            i = (s + k) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                break
        else:
            return s

    return -1
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Greedy with a 'discard the failed prefix' argument
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1

    tank = start = 0

    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:  # cannot get past i from `start`
            start = i + 1
            tank = 0

    return start
""",
    ),
    # ---- Partition Labels (LeetCode 763) ----
    dict(
        title="Partition Labels",
        diff="M",
        lc=763,
        slug="partition-labels",
        prompt=(
            "Split a string into as many parts as possible so that each letter appears in at most one part. Return "
            "the sizes of the parts."
        ),
        sig="def partition_labels(s: str) -> List[int]:",
        fn="partition_labels",
        tests=[
            (("ababcbacadefegdehijhklij",), [9, 7, 8]),
            (("eccbbbbdec",), [10]),
            (("a",), [1]),
            (("abc",), [1, 1, 1]),
            (("caedbdedda",), [1, 9]),
        ],
        hints=[
            "If a letter appears at positions 3 and 20, any part containing position 3 must reach at least 20.",
            "Precompute the last index of each letter.",
            "Sweep: end = max(end, last[c]) for each char; when i == end the part is closed - record its size.",
        ],
        pattern="Greedy interval extension using last occurrences",
        explain=(
            "Each letter defines an interval [first, last] that must stay in one part. Merging overlapping "
            "intervals\n        on the fly (extending `end`) and cutting whenever the index reaches `end` yields "
            "the maximum number of\n        parts. O(n)."
        ),
        cx="O(n) time, O(1) space (26 letters)",
        brute_cx="O(n^2) - last occurrence found by scanning every time",
        brute=r"""
# BRUTE FORCE: O(n^2) - last occurrence found by scanning every time
def partition_labels(s):
    sizes, start, end = [], 0, 0
    for i, c in enumerate(s):
        end = max(end, s.rfind(c))  # rfind scans the whole string: O(n)
        if i == end:
            sizes.append(end - start + 1)
            start = i + 1
    return sizes
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space (26 letters)
# Idea: Greedy interval extension using last occurrences
def partition_labels(s):
    last = {c: i for i, c in enumerate(s)}
    sizes = []
    start = end = 0

    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:  # everything seen so far closes here
            sizes.append(end - start + 1)
            start = i + 1

    return sizes
""",
    ),
]
