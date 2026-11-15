"""extra batch of Backtracking problems - the problem bank for the "backtracking" topic.

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
    # ---- Combination Sum III (LeetCode 216) ----
    dict(
        title="Combination Sum III",
        diff="M",
        lc=216,
        slug="combination-sum-iii",
        prompt=(
            "Use exactly k distinct numbers from 1..9, each at most once, that add up to n. Return all combinations."
        ),
        sig="def combination_sum3(k: int, n: int) -> List[List[int]]:",
        fn="combination_sum3",
        compare="nested_unordered",
        tests=[
            ((3, 7), [[1, 2, 4]]),
            ((3, 9), [[1, 2, 6], [1, 3, 5], [2, 3, 4]]),
            ((4, 1), []),
            ((2, 18), []),
            ((1, 5), [[5]]),
        ],
        hints=[
            "Choose numbers in increasing order so each set is generated once.",
            "State: (start, remaining count, remaining sum). Stop when count == 0.",
            "Prune: if the remaining sum goes negative, or numbers left are fewer than the count needed, return.",
        ],
        pattern="Backtracking with increasing start index and pruning",
        explain=(
            "Increasing order removes permutations of the same set. Pruning on the remaining sum cuts huge parts of "
            "the search tree."
        ),
        cx="O(C(9,k) * k) time",
        brute_cx="O(2^9 * 9) time - test every subset of 1..9",
        brute=r"""
# BRUTE FORCE: O(2^9 * 9) time - test every subset of 1..9
def combination_sum3(k, n):
    out = []
    for mask in range(1 << 9):
        s = [i + 1 for i in range(9) if mask >> i & 1]
        if len(s) == k and sum(s) == n:
            out.append(s)
    return out
""",
        solution=r"""
# OPTIMISED: O(C(9,k) * k) time
# Idea: Backtracking with increasing start index and pruning
def combination_sum3(k, n):
    out = []

    def go(start, left, path):
        if left == 0 and len(path) == k:
            out.append(path[:])
            return
        if len(path) == k or left <= 0:
            return
        for x in range(start, 10):
            if x > left:
                break
            path.append(x)
            go(x + 1, left - x, path)
            path.pop()

    go(1, n, [])
    return out
""",
    ),
    # ---- Letter Case Permutation (LeetCode 784) ----
    dict(
        title="Letter Case Permutation",
        diff="M",
        lc=784,
        slug="letter-case-permutation",
        prompt=(
            "Every letter of s may be lowercase or uppercase. Return all strings you can form (digits stay as they "
            "are)."
        ),
        sig="def letter_case_permutation(s: str) -> List[str]:",
        fn="letter_case_permutation",
        compare="unordered",
        tests=[
            (("a1b2",), ["a1b2", "a1B2", "A1b2", "A1B2"]),
            (("3z4",), ["3z4", "3Z4"]),
            (("12",), ["12"]),
            (("",), [""]),
            (("ab",), ["ab", "aB", "Ab", "AB"]),
        ],
        hints=[
            "Each letter is a binary choice; digits have exactly one option.",
            "At index i branch on lower/upper if s[i] is a letter; otherwise continue.",
            "Alternative: iteratively double the result list at each letter.",
        ],
        pattern="Binary decision per position (subset-style backtracking)",
        explain=(
            "The solution space is 2^(number of letters). BFS-style list doubling and DFS backtracking enumerate "
            "the same tree."
        ),
        cx="O(n * 2^L) time (L = number of letters)",
        brute_cx="O(n * 2^n) time - mask over ALL positions, skip masks that touch digits",
        brute=r"""
# BRUTE FORCE: O(n * 2^n) time - mask over ALL positions, skip masks that touch digits
def letter_case_permutation(s):
    n, seen = len(s), set()
    for mask in range(1 << n):
        t = []
        for i, c in enumerate(s):
            if mask >> i & 1:
                if not c.isalpha():
                    break
                t.append(c.upper())
            else:
                t.append(c.lower())
        else:
            seen.add("".join(t))
    return list(seen)
""",
        solution=r"""
# OPTIMISED: O(n * 2^L) time (L = number of letters)
# Idea: Binary decision per position (subset-style backtracking)
def letter_case_permutation(s):
    out = [""]
    for c in s:
        if c.isalpha():
            out = [p + x for p in out for x in (c.lower(), c.upper())]
        else:
            out = [p + c for p in out]
    return out
""",
    ),
    # ---- Beautiful Arrangement (LeetCode 526) ----
    dict(
        title="Beautiful Arrangement",
        diff="M",
        lc=526,
        slug="beautiful-arrangement",
        prompt=(
            "Count permutations of 1..n where, for every position i (1-indexed), perm[i] % i == 0 or i % perm[i] == 0."
        ),
        sig="def count_arrangement(n: int) -> int:",
        fn="count_arrangement",
        tests=[
            ((1,), 1),
            ((2,), 2),
            ((3,), 3),
            ((4,), 8),
            ((6,), 36),
            ((8,), 132),
        ],
        hints=[
            "Place numbers position by position and stop a branch as soon as it violates the rule.",
            "Track used numbers with a bitmask or boolean array.",
            "Fill positions from the BACK (n down to 1): strict positions have few candidates, so you prune early.",
        ],
        pattern="Backtracking with constraint pruning (permutation search)",
        explain=(
            "Checking the condition as soon as each element is placed prunes dead branches instead of testing n! "
            "complete permutations."
        ),
        cx="O(k) where k is the number of valid prefixes (far below n!)",
        brute_cx="O(n! * n) time - test every permutation",
        brute=r"""
# BRUTE FORCE: O(n! * n) time - test every permutation
def count_arrangement(n):
    c = 0
    for p in itertools.permutations(range(1, n + 1)):
        if all(p[i - 1] % i == 0 or i % p[i - 1] == 0 for i in range(1, n + 1)):
            c += 1
    return c
""",
        solution=r"""
# OPTIMISED: O(k) where k is the number of valid prefixes (far below n!)
# Idea: Backtracking with constraint pruning (permutation search)
def count_arrangement(n):
    used = [False] * (n + 1)

    def go(pos):
        if pos == 0:
            return 1
        total = 0
        for v in range(1, n + 1):
            if not used[v] and (v % pos == 0 or pos % v == 0):
                used[v] = True
                total += go(pos - 1)
                used[v] = False
        return total

    return go(n)
""",
    ),
    # ---- Partition to K Equal Sum Subsets (LeetCode 698) ----
    dict(
        title="Partition to K Equal Sum Subsets",
        diff="M",
        lc=698,
        slug="partition-to-k-equal-sum-subsets",
        prompt="Can the array be divided into k non-empty subsets with equal sums?",
        sig="def can_partition_k_subsets(nums: List[int], k: int) -> bool:",
        fn="can_partition_k_subsets",
        tests=[
            (([4, 3, 2, 3, 5, 2, 1], 4), True),
            (([1, 2, 3, 4], 3), False),
            (([2, 2, 2, 2, 3, 4, 5], 4), False),
            (([1], 1), True),
            (([1, 1, 1, 1], 2), True),
            (([10, 10, 10, 7, 7, 7, 7, 7, 7, 6, 6, 6], 3), True),
        ],
        hints=[
            "Each subset must sum to total/k; if total is not divisible by k the answer is False.",
            "Fill buckets one by one with a DFS over numbers, trying each number in each bucket.",
            (
                "Sort descending (fail fast), skip a bucket with the same current sum as one already tried, and "
                "prune when a bucket exceeds the target."
            ),
        ],
        pattern="Backtracking on bucket assignment with symmetry pruning",
        explain=(
            "Fail-fast ordering (largest first) and skipping equivalent buckets reduce the exponential search "
            "dramatically in practice."
        ),
        cx="O(k * 2^n) time with bitmask DP (or pruned DFS)",
        brute_cx="O(k^n) time - assign each number to any bucket",
        brute=r"""
# BRUTE FORCE: O(k^n) time - assign each number to any bucket
def can_partition_k_subsets(nums, k):
    total = sum(nums)
    if total % k:
        return False
    t = total // k
    buckets = [0] * k

    def go(i):
        if i == len(nums):
            return all(b == t for b in buckets)
        for b in range(k):
            buckets[b] += nums[i]
            if buckets[b] <= t and go(i + 1):
                return True
            buckets[b] -= nums[i]
        return False

    return go(0)
""",
        solution=r"""
# OPTIMISED: O(k * 2^n) time with bitmask DP (or pruned DFS)
# Idea: Backtracking on bucket assignment with symmetry pruning
def can_partition_k_subsets(nums, k):
    total = sum(nums)
    if total % k:
        return False
    t = total // k
    nums = sorted(nums, reverse=True)
    if nums[0] > t:
        return False
    buckets = [0] * k

    def go(i):
        if i == len(nums):
            return True
        seen = set()
        for b in range(k):
            if buckets[b] + nums[i] <= t and buckets[b] not in seen:
                seen.add(buckets[b])
                buckets[b] += nums[i]
                if go(i + 1):
                    return True
                buckets[b] -= nums[i]
        return False

    return go(0)
""",
    ),
]
