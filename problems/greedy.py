from core import *

PROBLEMS = [
    dict(
        title="Jump Game", diff="M", lc=55, slug="jump-game",
        prompt="nums[i] is the maximum jump length from index i. Starting at index 0, can you reach the last index?",
        sig="def can_jump(nums: List[int]) -> bool:",
        fn="can_jump",
        tests=[(([2, 3, 1, 1, 4],), True), (([3, 2, 1, 0, 4],), False), (([0],), True), (([0, 1],), False),
               (([2, 0, 0],), True), (([1, 1, 1, 1],), True)],
        hints=["Backtracking / DP over all jump choices is exponential or O(n^2).",
               "You only care about the FARTHEST index reachable so far, not how you got there.",
               "Scan left to right: if i > farthest you are stuck (False); else farthest = max(farthest, i + nums[i])."],
        pattern="Greedy: maintain the farthest reachable frontier",
        explain="""
        Reachability is contiguous: if you can reach index j, you can reach everything before it too. So one
        number (the frontier) summarises all possibilities. If the scan index ever exceeds the frontier, the
        gap cannot be crossed. O(n) time, O(1) space.""",
        solution=r'''
def can_jump(nums):
    reach = 0
    for i, x in enumerate(nums):
        if i > reach:
            return False
        reach = max(reach, i + x)
    return True
''',
    ),
    dict(
        title="Gas Station", diff="M", lc=134, slug="gas-station",
        prompt="Stations on a circle have gas[i] fuel and the trip to the next station costs cost[i]. Return the "
               "start index from which you can complete the full circle once, or -1. The answer is unique if it exists.",
        sig="def can_complete_circuit(gas: List[int], cost: List[int]) -> int:",
        fn="can_complete_circuit",
        tests=[(([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]), 3), (([2, 3, 4], [3, 4, 3]), -1), (([5], [4]), 0),
               (([3, 1, 1], [1, 2, 2]), 0), (([2], [2]), 0)],
        hints=["If total gas < total cost, it is impossible - no start works.",
               "If you run out of fuel going from start s to station j, then NO station between s and j can be a valid start either. Why?",
               "Track the tank; when it goes negative at i, reset the start to i+1 and the tank to 0."],
        pattern="Greedy with a 'discard the failed prefix' argument",
        explain="""
        Any station k between s and the failure point j had a non-negative tank on arrival from s, so starting
        at k is strictly worse than starting at s. Hence the next candidate is j+1. If the global surplus is
        >= 0, the last surviving candidate works. One pass, O(n).""",
        solution=r'''
def can_complete_circuit(gas, cost):
    if sum(gas) < sum(cost):
        return -1
    tank = start = 0
    for i in range(len(gas)):
        tank += gas[i] - cost[i]
        if tank < 0:            # cannot get past i from `start`
            start = i + 1
            tank = 0
    return start
''',
    ),
    dict(
        title="Partition Labels", diff="M", lc=763, slug="partition-labels",
        prompt="Split a string into as many parts as possible so that each letter appears in at most one part. "
               "Return the sizes of the parts.",
        sig="def partition_labels(s: str) -> List[int]:",
        fn="partition_labels",
        tests=[(("ababcbacadefegdehijhklij",), [9, 7, 8]), (("eccbbbbdec",), [10]), (("a",), [1]), (("abc",), [1, 1, 1]),
               (("caedbdedda",), [1, 9])],
        hints=["If a letter appears at positions 3 and 20, any part containing position 3 must reach at least 20.",
               "Precompute the last index of each letter.",
               "Sweep: end = max(end, last[c]) for each char; when i == end the part is closed - record its size."],
        pattern="Greedy interval extension using last occurrences",
        explain="""
        Each letter defines an interval [first, last] that must stay in one part. Merging overlapping intervals
        on the fly (extending `end`) and cutting whenever the index reaches `end` yields the maximum number of
        parts. O(n).""",
        solution=r'''
def partition_labels(s):
    last = {c: i for i, c in enumerate(s)}
    sizes = []
    start = end = 0
    for i, c in enumerate(s):
        end = max(end, last[c])
        if i == end:                     # everything seen so far closes here
            sizes.append(end - start + 1)
            start = i + 1
    return sizes
''',
    ),
]
