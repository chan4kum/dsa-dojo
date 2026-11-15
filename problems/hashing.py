"""Hashing problems - the problem bank for the "hashing" topic.

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
    # ---- Two Sum (LeetCode 1) ----
    dict(
        title="Two Sum",
        diff="E",
        lc=1,
        slug="two-sum",
        prompt=(
            "Given a list of integers and a target, return the indices of the two different elements that add up to "
            "the target. Exactly one such pair exists."
        ),
        sig="def two_sum(nums: List[int], target: int) -> List[int]:",
        fn="two_sum",
        compare="unordered",
        tests=[
            (([2, 7, 11, 15], 9), [0, 1]),
            (([3, 2, 4], 6), [1, 2]),
            (([3, 3], 6), [0, 1]),
            (([-1, -2, -3, -4, -5], -8), [2, 4]),
        ],
        hints=[
            "Brute force checks every pair: O(n^2). What are you really searching for, for each x?",
            "For each x you need the value (target - x). Can you answer 'have I seen this value?' in O(1)?",
            (
                "One pass: keep a dict value -> index of everything seen so far; look up the complement BEFORE "
                "inserting x."
            ),
        ],
        pattern="Hash map: trade memory for O(1) 'have I seen the complement?' lookups",
        explain=(
            "Brute force tries all pairs (O(n^2)). For a fixed x, the partner is forced: target - x.\n        So "
            "the question becomes 'is target - x somewhere earlier?' - a membership query, which a dict\n        "
            "answers in O(1). Scan left to right; before storing x, look up its complement. Checking "
            "before\n        inserting also guarantees we never pair an element with itself.\n        Time O(n), "
            "space O(n)."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time, O(1) space - tries every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time, O(1) space - tries every pair
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Hash map: trade memory for O(1) 'have I seen the complement?' lookups
def two_sum(nums, target):
    seen = {}  # value -> index
    for i, x in enumerate(nums):
        if target - x in seen:  # complement already seen?
            return [seen[target - x], i]
        seen[x] = i
    return []
""",
    ),
    # ---- Group Anagrams (LeetCode 49) ----
    dict(
        title="Group Anagrams",
        diff="M",
        lc=49,
        slug="group-anagrams",
        prompt=(
            "Group the given words so that words that are rearrangements of each other end up together. Return the "
            "groups in any order."
        ),
        sig="def group_anagrams(strs: List[str]) -> List[List[str]]:",
        fn="group_anagrams",
        compare="nested_unordered",
        tests=[
            ((["eat", "tea", "tan", "ate", "nat", "bat"],), [["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]),
            (([""],), [[""]]),
            ((["a"],), [["a"]]),
            ((["abc", "bca", "cab", "xyz"],), [["abc", "bca", "cab"], ["xyz"]]),
        ],
        hints=[
            "Two words are anagrams exactly when some canonical form of them is equal. What could that form be?",
            "Sorting the letters gives a canonical key; a counter of the 26 letters is another.",
            "dict: key = tuple(sorted(word)) -> list of words. Return the dict's values.",
        ],
        pattern="Hash map with a canonical-form key (group by signature)",
        explain=(
            "'Same multiset of letters' is an equivalence relation, so we need a key that is identical for\n        "
            "every member of a class. sorted(word) works (O(k log k) per word). A 26-length count tuple "
            "works\n        in O(k). Group with defaultdict(list).\n        Time O(n * k log k), space O(n * k)."
        ),
        cx="O(n*k) time, O(n*k) space (k = word length, count-signature key)",
        brute_cx="O(n^2 * k log k) - compares each word with every existing group",
        brute=r"""
# BRUTE FORCE: O(n^2 * k log k) - compares each word with every existing group
def group_anagrams(strs):
    groups = []
    for w in strs:
        for g in groups:
            if sorted(g[0]) == sorted(w):
                g.append(w)
                break
        else:
            groups.append([w])
    return groups
""",
        solution=r"""
# OPTIMISED: O(n*k) time, O(n*k) space (k = word length, count-signature key)
# Idea: Hash map with a canonical-form key (group by signature)
def group_anagrams(strs):
    groups = defaultdict(list)
    for w in strs:
        groups[tuple(sorted(w))].append(w)  # canonical signature
    return list(groups.values())
""",
    ),
    # ---- Longest Consecutive Sequence (LeetCode 128) ----
    dict(
        title="Longest Consecutive Sequence",
        diff="M",
        lc=128,
        slug="longest-consecutive-sequence",
        prompt=(
            "Given an unsorted list of integers, find the length of the longest run of consecutive integers (like "
            "4,5,6,7) that can be formed from its values. Must run in O(n)."
        ),
        sig="def longest_consecutive(nums: List[int]) -> int:",
        fn="longest_consecutive",
        tests=[
            (([100, 4, 200, 1, 3, 2],), 4),
            (([0, 3, 7, 2, 5, 8, 4, 6, 0, 1],), 9),
            (([],), 0),
            (([1, 2, 0, 1],), 3),
            (([5],), 1),
        ],
        hints=[
            "Sorting is O(n log n). The O(n) requirement hints at a hash set.",
            "Only start counting from a number x where x-1 is NOT in the set - that is the start of a run.",
            "From each start, walk x+1, x+2, ... while in the set. Every number is walked at most once overall.",
        ],
        pattern="Hash set + 'only expand from the start of a sequence' (amortised O(n))",
        explain=(
            "If you expand from every element you redo work (1,2,3,4 then 2,3,4 ...) = O(n^2). Fix: only expand "
            "from\n        run starts (x-1 absent). Each element is then visited once by the while-loop of its own "
            "run, so the\n        total is O(n) even though there is a nested loop.\n        Time O(n), space O(n)."
        ),
        cx="O(n) time, O(n) space (only start from run beginnings)",
        brute_cx="O(n^3) worst case - expands from every element using list membership",
        brute=r"""
# BRUTE FORCE: O(n^3) worst case - expands from every element using list membership
def longest_consecutive(nums):
    best = 0
    for x in nums:
        y = x
        while y + 1 in nums:  # membership in a LIST is O(n)
            y += 1
        best = max(best, y - x + 1)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space (only start from run beginnings)
# Idea: Hash set + 'only expand from the start of a sequence' (amortised O(n))
def longest_consecutive(nums):
    s = set(nums)
    best = 0
    for x in s:
        if x - 1 not in s:  # x starts a run
            y = x
            while y + 1 in s:
                y += 1
            best = max(best, y - x + 1)
    return best
""",
    ),
]
