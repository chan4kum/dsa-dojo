"""extra batch of Hashing problems - the problem bank for the "hashing" topic (batch 6).

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
    # ---- Bulls and Cows (LeetCode 299) ----
    dict(
        title="Bulls and Cows",
        diff="M",
        lc=299,
        slug="bulls-and-cows",
        prompt=(
            "secret and guess are digit strings of the same length. A BULL is a digit that is correct in value and "
            "position. A COW is a digit of guess that occurs in secret but at a different position and is not "
            "already used by a bull or another cow. Return the hint 'xAyB' where x is the number of bulls and y the "
            "number of cows."
        ),
        sig="def get_hint(secret: str, guess: str) -> str:",
        fn="get_hint",
        tests=[
            (("1807", "7810"), "1A3B"),
            (("1123", "0111"), "1A1B"),
            (("1", "0"), "0A0B"),
            (("1", "1"), "1A0B"),
            (("11", "10"), "1A0B"),
        ],
        hints=[
            "Bulls are easy: compare the two strings position by position.",
            "Matches of any kind (bulls + cows) for a digit d are min(count of d in secret, count of d in guess).",
            "So cows = (sum over digits of that minimum) - bulls.",
        ],
        pattern="Frequency counting: common elements = sum of minimum counts",
        explain=(
            "A bull uses up one digit of each string. Every remaining pairing of equal digits in different "
            "positions is a cow, and each digit can be paired at most as often as it occurs in BOTH strings. The "
            "total number of pairable digits (bulls included) is therefore the sum over digits of min(count in "
            "secret, count in guess) - exactly the size of the multiset intersection. Subtracting the bulls leaves "
            "the cows. The brute force marks used secret positions and hunts for a partner for every non-bull guess "
            "digit."
        ),
        cx="O(n) time, O(1) space (10 digits)",
        brute_cx="O(n^2) time - for each non-bull guess digit scan the secret for an unused partner",
        brute=r"""
# BRUTE FORCE: O(n^2) time - for each non-bull guess digit scan the secret for an unused partner
def get_hint(secret, guess):
    n = len(secret)
    used = [False] * n
    bulls = cows = 0
    for i in range(n):
        if secret[i] == guess[i]:
            bulls += 1
            used[i] = True
    for i in range(n):
        if secret[i] != guess[i]:
            for j in range(n):
                if not used[j] and secret[j] == guess[i]:
                    used[j] = True
                    cows += 1
                    break
    return "%dA%dB" % (bulls, cows)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space (10 digits)
# Idea: Frequency counting: common elements = sum of minimum counts
def get_hint(secret, guess):
    bulls = sum(a == b for a, b in zip(secret, guess))
    common = sum((Counter(secret) & Counter(guess)).values())
    return "%dA%dB" % (bulls, common - bulls)
""",
    ),
    # ---- Prison Cells After N Days (LeetCode 957) ----
    dict(
        title="Prison Cells After N Days",
        diff="M",
        lc=957,
        slug="prison-cells-after-n-days",
        prompt=(
            "Eight prison cells in a row are occupied (1) or vacant (0). Each day, a cell becomes occupied if its "
            "two neighbours were both occupied or both vacant the day before, otherwise it becomes vacant. The "
            "first and last cells have only one neighbour, so they are vacant after the first day. Return the state "
            "after n days."
        ),
        sig="def prison_after_n_days(cells: List[int], n: int) -> List[int]:",
        fn="prison_after_n_days",
        tests=[
            (([0, 1, 0, 1, 1, 0, 0, 1], 7), [0, 0, 1, 1, 0, 0, 0, 0]),
            (([1, 1, 1, 1, 1, 1, 1, 1], 1), [0, 1, 1, 1, 1, 1, 1, 0]),
            (([1, 0, 0, 1, 0, 0, 1, 0], 1), [0, 0, 0, 1, 0, 0, 1, 0]),
            (([1, 0, 0, 1, 0, 0, 1, 0], 15), [0, 0, 0, 1, 0, 0, 1, 0]),
        ],
        hints=[
            "There are only 2^8 = 256 possible states (really 64 after day 1), so the sequence of states MUST repeat.",
            (
                "Remember each state with the day you first saw it in a dictionary; a repeat means a cycle of "
                "length (day - firstDay)."
            ),
            "When a cycle is found, skip whole cycles: the remaining days only matter modulo the cycle length.",
        ],
        pattern="Cycle detection with a visited-state hash map",
        explain=(
            "The next day depends only on the current day, and the state space is tiny, so the simulation is "
            "eventually periodic. n can be 10^9, but we never need to simulate that long: record each state with "
            "its day number; the first time a state repeats we know the cycle length c, and the state after the "
            "remaining days equals the state after (remaining mod c) days. The brute force simulates all n days, "
            "fine for small n but hopeless for 10^9."
        ),
        cx="O(min(n, 256) * 8) time, O(256) space",
        brute_cx="O(n * 8) time - simulate every single day",
        brute=r"""
# BRUTE FORCE: O(n * 8) time - simulate every single day
def prison_after_n_days(cells, n):
    state = list(cells)
    size = len(state)
    for _ in range(n):
        state = [
            0 if i in (0, size - 1) else int(state[i - 1] == state[i + 1]) for i in range(size)
        ]
    return state
""",
        solution=r"""
# OPTIMISED: O(min(n, 256) * 8) time, O(256) space
# Idea: Cycle detection with a visited-state hash map
def prison_after_n_days(cells, n):
    size = len(cells)
    state = tuple(cells)
    seen = {}
    day = 0
    while day < n:
        if state in seen:
            cycle = day - seen[state]
            n = day + (n - day) % cycle
            seen = {}
            if day == n:
                break
        seen[state] = day
        state = tuple(
            0 if i in (0, size - 1) else int(state[i - 1] == state[i + 1]) for i in range(size)
        )
        day += 1
    return list(state)
""",
    ),
    # ---- Largest Values From Labels (LeetCode 1090) ----
    dict(
        title="Largest Values From Labels",
        diff="M",
        lc=1090,
        slug="largest-values-from-labels",
        prompt=(
            "Item i has value values[i] (>= 0) and label labels[i]. Choose a subset of at most num_wanted items "
            "such that at most use_limit items share any one label. Return the largest possible sum of the chosen "
            "values."
        ),
        sig=(
            "def largest_vals_from_labels(values: List[int], labels: List[int], num_wanted: int, use_limit: int) -> "
            "int:"
        ),
        fn="largest_vals_from_labels",
        tests=[
            (([5, 4, 3, 2, 1], [1, 1, 2, 2, 3], 3, 1), 9),
            (([5, 4, 3, 2, 1], [1, 3, 3, 3, 2], 3, 2), 12),
            (([9, 8, 8, 7, 6], [0, 0, 0, 1, 1], 3, 1), 16),
            (([5], [1], 1, 1), 5),
        ],
        hints=[
            "Values are non-negative, so taking one more allowed item never hurts.",
            "Consider items from the largest value to the smallest.",
            (
                "Take an item if fewer than num_wanted are chosen AND its label has been used fewer than use_limit "
                "times (count with a dict)."
            ),
        ],
        pattern="Greedy by value with a per-label counter",
        explain=(
            "If an item is the best remaining and its label still has capacity, taking it is never worse than any "
            "alternative (exchange argument: replacing it by a smaller item in an optimal answer cannot gain). So "
            "sort by value descending, keep a hash map of how often each label has been used, and take items while "
            "both limits allow. The brute force tries every subset of at most num_wanted items."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(2^n * n) time - try every subset of size <= num_wanted and check the label limit",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - try every subset of size <= num_wanted and check the label limit
def largest_vals_from_labels(values, labels, num_wanted, use_limit):
    n = len(values)
    best = 0
    for size in range(1, min(n, num_wanted) + 1):
        for combo in itertools.combinations(range(n), size):
            counts = Counter(labels[i] for i in combo)
            if max(counts.values()) <= use_limit:
                best = max(best, sum(values[i] for i in combo))
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Greedy by value with a per-label counter
def largest_vals_from_labels(values, labels, num_wanted, use_limit):
    used = Counter()
    total = taken = 0
    for v, lab in sorted(zip(values, labels), reverse=True):
        if taken == num_wanted:
            break
        if used[lab] < use_limit:
            used[lab] += 1
            total += v
            taken += 1
    return total
""",
    ),
    # ---- Unique Number of Occurrences (LeetCode 1207) ----
    dict(
        title="Unique Number of Occurrences",
        diff="E",
        lc=1207,
        slug="unique-number-of-occurrences",
        prompt="Return true if every distinct value of arr occurs a different number of times from every other value.",
        sig="def unique_occurrences(arr: List[int]) -> bool:",
        fn="unique_occurrences",
        tests=[
            (([1, 2, 2, 1, 1, 3],), True),
            (([1, 2],), False),
            (([-3, 0, 1, -3, 1, 1, 1, -3, 10, 0],), True),
            (([5],), True),
        ],
        hints=[
            "First count how often each value appears.",
            "The counts are 'all different' exactly when no two values share a count.",
            "Put the counts in a set: its size must equal the number of distinct values.",
        ],
        pattern="Count, then compare the number of distinct counts with the number of values",
        explain=(
            "A hash map gives value -> frequency. The frequencies are pairwise different iff turning them into a "
            "set does not lose any element, i.e. len(set(counts)) == len(counts). The brute force recounts each "
            "value with list.count and compares all pairs of distinct values."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - list.count for every value, then compare all pairs",
        brute=r"""
# BRUTE FORCE: O(n^2) time - list.count for every value, then compare all pairs
def unique_occurrences(arr):
    values = list(set(arr))
    counts = [arr.count(v) for v in values]
    for i in range(len(counts)):
        for j in range(i + 1, len(counts)):
            if counts[i] == counts[j]:
                return False
    return True
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Count, then compare the number of distinct counts with the number of values
def unique_occurrences(arr):
    counts = Counter(arr).values()
    return len(set(counts)) == len(counts)
""",
    ),
    # ---- How Many Numbers Are Smaller Than the Current Number (LeetCode 1365) ----
    dict(
        title="How Many Numbers Are Smaller Than the Current Number",
        diff="E",
        lc=1365,
        slug="how-many-numbers-are-smaller-than-the-current-number",
        prompt=(
            "For every nums[i], count how many numbers in the whole array are strictly smaller than nums[i] (the "
            "element itself does not count). Return the counts."
        ),
        sig="def smaller_numbers_than_current(nums: List[int]) -> List[int]:",
        fn="smaller_numbers_than_current",
        tests=[
            (([8, 1, 2, 2, 3],), [4, 0, 1, 1, 3]),
            (([6, 5, 4, 8],), [2, 1, 0, 3]),
            (([7, 7, 7, 7],), [0, 0, 0, 0]),
            (([1],), [0]),
        ],
        hints=[
            "For a sorted copy, the number of smaller elements of v is the index where v FIRST appears.",
            "Duplicates must all map to the first index - record it only the first time you meet the value.",
            "Sort once, build value -> first index, and answer each query with a dictionary lookup.",
        ],
        pattern="Sort once; first-occurrence index = count of smaller values",
        explain=(
            "In ascending order, everything before the first copy of v is strictly smaller than v and everything "
            "from there on is >= v. So the answer for v is the index of its first occurrence in the sorted array. A "
            "dictionary built with setdefault keeps only the first index of each value, making each query O(1). The "
            "brute force compares every pair."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2) time - count smaller elements separately for every position",
        brute=r"""
# BRUTE FORCE: O(n^2) time - count smaller elements separately for every position
def smaller_numbers_than_current(nums):
    return [sum(1 for other in nums if other < v) for v in nums]
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Sort once; first-occurrence index = count of smaller values
def smaller_numbers_than_current(nums):
    first = {}
    for i, v in enumerate(sorted(nums)):
        first.setdefault(v, i)
    return [first[v] for v in nums]
""",
    ),
    # ---- Check If Array Pairs Are Divisible by k (LeetCode 1497) ----
    dict(
        title="Check If Array Pairs Are Divisible by k",
        diff="M",
        lc=1497,
        slug="check-if-array-pairs-are-divisible-by-k",
        prompt=(
            "arr has an even length. Can you split it into pairs so that the sum of every pair is divisible by k? "
            "Every element must be used in exactly one pair."
        ),
        sig="def can_arrange(arr: List[int], k: int) -> bool:",
        fn="can_arrange",
        tests=[
            (([1, 2, 3, 4, 5, 10, 6, 7, 8, 9], 5), True),
            (([1, 2, 3, 4, 5, 6], 7), True),
            (([1, 2, 3, 4, 5, 6], 10), False),
            (([-10, 10], 2), True),
            (([-1, 1, -2, 2, -3, 3, -4, 4], 3), True),
        ],
        hints=[
            "Only the remainder x % k matters (Python's % is never negative, which handles negative numbers).",
            "A number with remainder r can only pair with a number with remainder k - r (or 0 with 0).",
            (
                "So count remainders: cnt[r] must equal cnt[k - r]; cnt[0] must be even; and if k is even, cnt[k / "
                "2] must be even."
            ),
        ],
        pattern="Remainder buckets that must be paired off",
        explain=(
            "(a + b) % k == 0 means the remainders add up to 0 or k. Therefore each element with remainder r > 0 "
            "needs a partner with remainder k - r, so the two buckets must have the same size. Remainder 0 pairs "
            "with itself, and for even k the remainder k/2 pairs with itself, so those two buckets need an even "
            "size. This is a pure counting argument - no search needed. The brute force tries every way to match "
            "the first element with a compatible partner and recurses."
        ),
        cx="O(n + k) time, O(k) space",
        brute_cx="O((n - 1)!!) time - recursively pair the first element with every compatible partner",
        brute=r"""
# BRUTE FORCE: O((n - 1)!!) time - recursively pair the first element with every compatible partner
def can_arrange(arr, k):
    def solve(items):
        if not items:
            return True
        first, rest = items[0], items[1:]
        for i, other in enumerate(rest):
            if (first + other) % k == 0 and solve(rest[:i] + rest[i + 1 :]):
                return True
        return False

    return solve(list(arr))
""",
        solution=r"""
# OPTIMISED: O(n + k) time, O(k) space
# Idea: Remainder buckets that must be paired off
def can_arrange(arr, k):
    cnt = Counter(x % k for x in arr)
    if cnt[0] % 2:
        return False
    for r in range(1, k):
        if r == k - r:
            if cnt[r] % 2:
                return False
        elif cnt[r] != cnt[k - r]:
            return False
    return True
""",
    ),
    # ---- Count Good Meals (LeetCode 1711) ----
    dict(
        title="Count Good Meals",
        diff="M",
        lc=1711,
        slug="count-good-meals",
        prompt=(
            "A good meal is a pair of items (different indices) whose deliciousness values sum to a power of two. "
            "Count the good meals in deliciousness (pairs of positions i < j), modulo 10^9 + 7."
        ),
        sig="def count_pairs(deliciousness: List[int]) -> int:",
        fn="count_pairs",
        tests=[
            (([1, 3, 5, 7, 9],), 4),
            (([1, 1, 1, 3, 3, 3, 7],), 15),
            (([1, 1],), 1),
            (([3],), 0),
            (([0, 1],), 1),
        ],
        hints=[
            "Values go up to 2^20, so the sum is at most 2^21: there are only about 22 powers of two to consider.",
            "For a fixed element x and a fixed power p, the partner must equal p - x.",
            (
                "Scan left to right with a counter of earlier values; for each x add counter[p - x] for each of the "
                "22 powers."
            ),
        ],
        pattern="Two-sum with a small fixed set of targets",
        explain=(
            "Two-sum asks for pairs adding up to one target; here the targets are the ~22 powers of two that are "
            "reachable, so we run 22 two-sum checks at once. Scanning left to right and counting earlier partners "
            "makes every pair (i < j) counted exactly once, and Counter returns 0 for unseen keys. Total work is 22 "
            "* n lookups. The brute force tests each pair's sum with the bit trick s & (s - 1) == 0."
        ),
        cx="O(22 * n) time, O(n) space",
        brute_cx="O(n^2) time - test every pair's sum for being a power of two",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every pair's sum for being a power of two
def count_pairs(deliciousness):
    total = 0
    n = len(deliciousness)
    for i in range(n):
        for j in range(i + 1, n):
            s = deliciousness[i] + deliciousness[j]
            if s > 0 and s & (s - 1) == 0:
                total += 1
    return total % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(22 * n) time, O(n) space
# Idea: Two-sum with a small fixed set of targets
def count_pairs(deliciousness):
    seen = Counter()
    total = 0
    for x in deliciousness:
        for k in range(22):
            total += seen[(1 << k) - x]
        seen[x] += 1
    return total % (10**9 + 7)
""",
    ),
    # ---- Tuple with Same Product (LeetCode 1726) ----
    dict(
        title="Tuple with Same Product",
        diff="M",
        lc=1726,
        slug="tuple-with-same-product",
        prompt=(
            "nums holds DISTINCT positive integers. Count the ordered tuples (a, b, c, d) of four different "
            "elements of nums (taken from four different positions) such that a * b == c * d."
        ),
        sig="def tuple_same_product(nums: List[int]) -> int:",
        fn="tuple_same_product",
        tests=[
            (([2, 3, 4, 6],), 8),
            (([1, 2, 4, 5, 10],), 16),
            (([1, 2, 3],), 0),
            (([2, 3],), 0),
            (([1, 2, 3, 6],), 8),
        ],
        hints=[
            "Group all unordered pairs {x, y} by their product x * y.",
            (
                "Two different pairs with the same product share no element (distinct numbers!), so any two of them "
                "form a tuple."
            ),
            (
                "A product with c pairs gives c * (c - 1) / 2 pair-of-pairs, and each pair-of-pairs yields 8 "
                "ordered tuples."
            ),
        ],
        pattern="Group by product; count combinations within each group",
        explain=(
            "Take two unordered pairs {a, b} and {c, d} with equal product. If they shared an element, say a = c, "
            "then b = d, so they would be the same pair; hence different pairs with equal product are automatically "
            "disjoint. Each such pair-of-pairs can be ordered in 2 * 2 * 2 = 8 ways (swap inside the first pair, "
            "inside the second, and swap which pair comes first). So the answer is 8 * sum over products of "
            "C(count, 2). The brute force loops over all ordered tuples."
        ),
        cx="O(n^2) time, O(n^2) space",
        brute_cx="O(n^4) time - test every ordered tuple of four different positions",
        brute=r"""
# BRUTE FORCE: O(n^4) time - test every ordered tuple of four different positions
def tuple_same_product(nums):
    n = len(nums)
    total = 0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    if len({a, b, c, d}) == 4 and nums[a] * nums[b] == nums[c] * nums[d]:
                        total += 1
    return total
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n^2) space
# Idea: Group by product; count combinations within each group
def tuple_same_product(nums):
    products = Counter()
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            products[nums[i] * nums[j]] += 1
    return sum(8 * c * (c - 1) // 2 for c in products.values())
""",
    ),
    # ---- Finding the Users Active Minutes (LeetCode 1817) ----
    dict(
        title="Finding the Users Active Minutes",
        diff="M",
        lc=1817,
        slug="finding-the-users-active-minutes",
        prompt=(
            "logs[i] = [user, minute] records an action. A user's active minutes (UAM) is the number of DISTINCT "
            "minutes in which they acted. Return a list answer of length k where answer[j] is the number of users "
            "whose UAM equals j + 1 (k is at least the largest UAM)."
        ),
        sig="def finding_users_active_minutes(logs: List[List[int]], k: int) -> List[int]:",
        fn="finding_users_active_minutes",
        tests=[
            (([[0, 5], [1, 2], [0, 2], [0, 5], [1, 3]], 5), [0, 2, 0, 0, 0]),
            (([[1, 1], [2, 2], [2, 3]], 4), [1, 1, 0, 0]),
            (([[1, 1]], 1), [1]),
            (([[1, 1], [2, 1], [3, 1]], 3), [3, 0, 0]),
        ],
        hints=[
            "Repeated actions in the same minute must count once - use a set per user.",
            "Build user -> set of minutes in one pass over the logs.",
            "Then every user contributes 1 to answer[len(set) - 1].",
        ],
        pattern="Map of sets, then a histogram of set sizes",
        explain=(
            "A dictionary from user to a set of minutes removes duplicate actions automatically. After one pass, "
            "the UAM of a user is the size of their set; a second pass over the users builds the histogram. The "
            "brute force rescans the whole log list for every user."
        ),
        cx="O(n + k) time, O(n) space",
        brute_cx="O(users * n) time - rescan all logs for every user",
        brute=r"""
# BRUTE FORCE: O(users * n) time - rescan all logs for every user
def finding_users_active_minutes(logs, k):
    answer = [0] * k
    for user in sorted({u for u, _ in logs}):
        minutes = {t for u, t in logs if u == user}
        answer[len(minutes) - 1] += 1
    return answer
""",
        solution=r"""
# OPTIMISED: O(n + k) time, O(n) space
# Idea: Map of sets, then a histogram of set sizes
def finding_users_active_minutes(logs, k):
    minutes = defaultdict(set)
    for user, t in logs:
        minutes[user].add(t)
    answer = [0] * k
    for s in minutes.values():
        answer[len(s) - 1] += 1
    return answer
""",
    ),
    # ---- Find Original Array From Doubled Array (LeetCode 2007) ----
    dict(
        title="Find Original Array From Doubled Array",
        diff="M",
        lc=2007,
        slug="find-original-array-from-doubled-array",
        prompt=(
            "changed was made by taking an array original, appending the double of every element, and shuffling. "
            "Return original (in any order), or an empty list if changed is not a doubled array."
        ),
        sig="def find_original_array(changed: List[int]) -> List[int]:",
        fn="find_original_array",
        compare="unordered",
        tests=[
            (([1, 3, 4, 2, 6, 8],), [1, 3, 4]),
            (([6, 3, 0, 1],), []),
            (([1],), []),
            (([0, 0],), [0]),
            (([2, 1],), [1]),
        ],
        hints=[
            "The smallest value can never be the double of anything remaining, so it must belong to original.",
            "Process values in increasing order: take x, and cancel one copy of 2 * x from the multiset.",
            (
                "Use a Counter; if the partner 2 * x is missing, the answer is []. Handle 0 carefully (0 doubles to "
                "itself)."
            ),
        ],
        pattern="Greedy smallest-first matching with a frequency map",
        explain=(
            "Consider the smallest remaining value x. It is not the double of any remaining value (that value would "
            "be smaller), so x belongs to original and its double 2x must still be present - consume one copy of "
            "each. Repeating this decides everything and also gives the unique original multiset. For x = 0 the "
            "partner is another 0, which is why we decrement before testing for the partner. Odd length is "
            "impossible. The brute force tries every subset of half the positions as the original."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(C(n, n/2) * n log n) time - try every choice of n/2 positions as the original",
        brute=r"""
# BRUTE FORCE: O(C(n, n/2) * n log n) time - try every choice of n/2 positions as the original
def find_original_array(changed):
    n = len(changed)
    if n % 2:
        return []
    target = sorted(changed)
    for combo in itertools.combinations(range(n), n // 2):
        original = [changed[i] for i in combo]
        if sorted(original + [2 * x for x in original]) == target:
            return original
    return []
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Greedy smallest-first matching with a frequency map
def find_original_array(changed):
    if len(changed) % 2:
        return []
    cnt = Counter(changed)
    original = []
    for x in sorted(cnt):
        while cnt[x] > 0:
            cnt[x] -= 1
            if cnt[2 * x] <= 0:
                return []
            cnt[2 * x] -= 1
            original.append(x)
    return original
""",
    ),
    # ---- Number of Pairs of Strings With Concatenation Equal to Target (LeetCode 2023) ----
    dict(
        title="Number of Pairs of Strings With Concatenation Equal to Target",
        diff="M",
        lc=2023,
        slug="number-of-pairs-of-strings-with-concatenation-equal-to-target",
        prompt=(
            "Count the ordered pairs of indices (i, j) with i != j such that nums[i] + nums[j] (string "
            "concatenation) equals target."
        ),
        sig="def num_of_pairs(nums: List[str], target: str) -> int:",
        fn="num_of_pairs",
        tests=[
            ((["777", "7", "77", "77"], "7777"), 4),
            ((["123", "4", "12", "34"], "1234"), 2),
            ((["1", "1", "1"], "11"), 6),
            ((["1"], "11"), 0),
        ],
        hints=[
            "If nums[i] + nums[j] == target, then nums[i] is a prefix of target and nums[j] is the remaining suffix.",
            "Try every cut of target into prefix | suffix and count how many strings equal each part.",
            (
                "Multiply the two counts; if prefix == suffix, the same string cannot be used twice, so use count * "
                "(count - 1)."
            ),
        ],
        pattern="Split the target and look up both halves in a frequency map",
        explain=(
            "A concatenation equal to target is determined by where target is cut. For each of the len(target) - 1 "
            "cuts, the number of ordered pairs is cnt[prefix] * cnt[suffix] - any copy of the prefix with any copy "
            "of the suffix. The only exception is prefix == suffix: the two strings must be different positions, "
            "giving cnt * (cnt - 1). The brute force concatenates all ordered pairs."
        ),
        cx="O(n + |target|^2) time, O(n) space",
        brute_cx="O(n^2 * |target|) time - concatenate every ordered pair and compare",
        brute=r"""
# BRUTE FORCE: O(n^2 * |target|) time - concatenate every ordered pair and compare
def num_of_pairs(nums, target):
    count = 0
    for i in range(len(nums)):
        for j in range(len(nums)):
            if i != j and nums[i] + nums[j] == target:
                count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n + |target|^2) time, O(n) space
# Idea: Split the target and look up both halves in a frequency map
def num_of_pairs(nums, target):
    cnt = Counter(nums)
    total = 0
    for cut in range(1, len(target)):
        p, s = target[:cut], target[cut:]
        if p == s:
            total += cnt[p] * (cnt[p] - 1)
        else:
            total += cnt[p] * cnt[s]
    return total
""",
    ),
    # ---- Find All Possible Recipes from Given Supplies (LeetCode 2115) ----
    dict(
        title="Find All Possible Recipes from Given Supplies",
        diff="M",
        lc=2115,
        slug="find-all-possible-recipes-from-given-supplies",
        prompt=(
            "recipes[i] can be made from the ingredients in ingredients[i]. An ingredient is either in supplies "
            "(unlimited) or is itself another recipe. Return all recipes that can be made, in any order."
        ),
        sig="def find_all_recipes(recipes: List[str], ingredients: List[List[str]], supplies: List[str]) -> List[str]:",
        fn="find_all_recipes",
        compare="unordered",
        tests=[
            ((["bread"], [["yeast", "flour"]], ["yeast", "flour", "corn"]), ["bread"]),
            (
                (["bread", "sandwich"], [["yeast", "flour"], ["bread", "meat"]], ["yeast", "flour", "meat"]),
                ["bread", "sandwich"],
            ),
            (
                (
                    ["bread", "sandwich", "burger"],
                    [["yeast", "flour"], ["bread", "meat"], ["sandwich", "meat", "bread"]],
                    ["yeast", "flour", "meat"],
                ),
                ["bread", "sandwich", "burger"],
            ),
            ((["bread"], [["yeast", "flour"]], ["yeast"]), []),
        ],
        hints=[
            "A recipe depends on its ingredients - draw an edge ingredient -> recipe; this is a dependency graph.",
            (
                "Start from what you have (supplies). A recipe becomes available once ALL its missing ingredients "
                "are available."
            ),
            (
                "Topological order (Kahn): keep for each recipe the count of ingredients not in supplies, and "
                "release it when that count hits 0."
            ),
        ],
        pattern="Topological sort over a dependency graph",
        explain=(
            "Each recipe has an in-degree equal to the number of its ingredients that are not already supplies. A "
            "recipe with in-degree 0 can be cooked now; cooking it satisfies every recipe that lists it, decreasing "
            "their in-degrees, and so on - exactly Kahn's algorithm. Recipes on a cycle (or depending on something "
            "unobtainable) never reach in-degree 0 and are correctly left out. The brute force repeatedly scans all "
            "recipes until a pass adds nothing."
        ),
        cx="O(R + E) time, O(R + E) space (R recipes, E ingredient mentions)",
        brute_cx="O(R * (R + E)) time - repeat full passes over all recipes until nothing new can be made",
        brute=r"""
# BRUTE FORCE: O(R * (R + E)) time - repeat full passes over all recipes until nothing new can be made
def find_all_recipes(recipes, ingredients, supplies):
    have = set(supplies)
    made = []
    changed = True
    while changed:
        changed = False
        for r, ing in zip(recipes, ingredients):
            if r not in have and all(x in have for x in ing):
                have.add(r)
                made.append(r)
                changed = True
    return made
""",
        solution=r"""
# OPTIMISED: O(R + E) time, O(R + E) space (R recipes, E ingredient mentions)
# Idea: Topological sort over a dependency graph
def find_all_recipes(recipes, ingredients, supplies):
    have = set(supplies)
    indegree = {}
    users = defaultdict(list)
    for r, ing in zip(recipes, ingredients):
        need = 0
        for x in ing:
            if x not in have:
                need += 1
                users[x].append(r)
        indegree[r] = need
    queue = deque(r for r in recipes if indegree[r] == 0)
    made = []
    while queue:
        r = queue.popleft()
        made.append(r)
        for nxt in users[r]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return made
""",
    ),
    # ---- Most Frequent Number Following Key In an Array (LeetCode 2190) ----
    dict(
        title="Most Frequent Number Following Key In an Array",
        diff="E",
        lc=2190,
        slug="most-frequent-number-following-key-in-an-array",
        prompt=(
            "Look at every index i with nums[i] == key and i + 1 < len(nums); the value nums[i + 1] 'follows' key. "
            "Return the value that follows key the most times (the answer is guaranteed to be unique)."
        ),
        sig="def most_frequent(nums: List[int], key: int) -> int:",
        fn="most_frequent",
        tests=[
            (([1, 100, 200, 1, 100], 1), 100),
            (([2, 2, 2, 2, 3], 2), 2),
            (([1, 2], 1), 2),
            (([5, 6, 7, 5, 6, 5, 7, 5, 6], 5), 6),
        ],
        hints=[
            "Only the pairs (nums[i], nums[i + 1]) with nums[i] == key matter.",
            "Count nums[i + 1] in a hash map during a single pass.",
            "Return the key of the map with the largest count.",
        ],
        pattern="Single pass with a frequency map",
        explain=(
            "Every candidate answer is a value that appears right after a key occurrence, so one scan over adjacent "
            "pairs with a Counter collects all frequencies; the maximum is the answer (unique by the statement). "
            "The brute force tests each distinct value separately by rescanning the whole array."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n * distinct) time - rescan the array once per candidate value",
        brute=r"""
# BRUTE FORCE: O(n * distinct) time - rescan the array once per candidate value
def most_frequent(nums, key):
    best, best_count = None, 0
    for cand in set(nums):
        c = sum(1 for i in range(len(nums) - 1) if nums[i] == key and nums[i + 1] == cand)
        if c > best_count:
            best, best_count = cand, c
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Single pass with a frequency map
def most_frequent(nums, key):
    counts = Counter(nums[i + 1] for i in range(len(nums) - 1) if nums[i] == key)
    return max(counts, key=counts.get)
""",
    ),
    # ---- Replace Elements in an Array (LeetCode 2295) ----
    dict(
        title="Replace Elements in an Array",
        diff="M",
        lc=2295,
        slug="replace-elements-in-an-array",
        prompt=(
            "nums holds distinct positive integers. Apply the operations in order: operation [a, b] replaces the "
            "number a (which is present) by b (which is NOT present at that moment). Return the final array."
        ),
        sig="def array_change(nums: List[int], operations: List[List[int]]) -> List[int]:",
        fn="array_change",
        tests=[
            (([1, 2, 4, 6], [[1, 3], [4, 7], [6, 1]]), [3, 2, 7, 1]),
            (([1, 2], [[1, 3], [2, 1], [3, 2]]), [2, 1]),
            (([5], []), [5]),
            (([5], [[5, 6]]), [6]),
        ],
        hints=[
            "Searching the array for a on every operation costs O(n) each - O(n * m) in total.",
            "Because all values are distinct, a value identifies exactly one index: keep value -> index in a dict.",
            "Operation [a, b]: i = pos.pop(a); nums[i] = b; pos[b] = i.",
        ],
        pattern="Value -> index hash map for O(1) updates",
        explain=(
            "Distinctness (guaranteed before every operation) means each value occurs at one index only, so a "
            "dictionary maps the current value to its slot. Replacing a by b moves the dictionary entry from a to b "
            "and overwrites the slot - O(1). The brute force calls list.index for every operation."
        ),
        cx="O(n + m) time, O(n) space",
        brute_cx="O(n * m) time - list.index to locate the value for every operation",
        brute=r"""
# BRUTE FORCE: O(n * m) time - list.index to locate the value for every operation
def array_change(nums, operations):
    out = list(nums)
    for a, b in operations:
        out[out.index(a)] = b
    return out
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(n) space
# Idea: Value -> index hash map for O(1) updates
def array_change(nums, operations):
    out = list(nums)
    pos = {v: i for i, v in enumerate(out)}
    for a, b in operations:
        i = pos.pop(a)
        out[i] = b
        pos[b] = i
    return out
""",
    ),
    # ---- Make Number of Distinct Characters Equal (LeetCode 2531) ----
    dict(
        title="Make Number of Distinct Characters Equal",
        diff="M",
        lc=2531,
        slug="make-number-of-distinct-characters-equal",
        prompt=(
            "You must make exactly ONE swap: pick an index i in word1 and an index j in word2 and exchange word1[i] "
            "with word2[j] (the two characters may be equal). Return true if the two words can end up with the same "
            "number of distinct characters."
        ),
        sig="def is_it_possible(word1: str, word2: str) -> bool:",
        fn="is_it_possible",
        tests=[
            (("ac", "b"), False),
            (("abcc", "aab"), True),
            (("abcde", "fghij"), True),
            (("a", "a"), True),
        ],
        hints=[
            "Which positions you swap does not matter - only WHICH letters (a from word1, b from word2) are exchanged.",
            "So there are at most 26 * 26 letter pairs to test, using frequency tables for both words.",
            (
                "Update the distinct counts in O(1): word1 loses a (if its count was 1) and gains b (if b was "
                "absent); symmetric for word2."
            ),
        ],
        pattern="Frequency tables; try all alphabet pairs instead of all index pairs",
        explain=(
            "The effect of a swap on the number of distinct letters depends only on the two letters involved and "
            "the frequency tables. Removing one 'a' from word1 reduces its distinct count only if a occurred once; "
            "adding 'b' increases it only if b was absent - and the mirror image for word2. If a == b nothing "
            "changes. Trying all present letter pairs is at most 26 * 26 checks, independent of the word lengths. "
            "The brute force really swaps every pair of positions and recomputes the sets."
        ),
        cx="O(|word1| + |word2| + 26^2) time, O(1) space",
        brute_cx="O(|w1| * |w2| * (|w1| + |w2|)) time - perform every swap and recount distinct characters",
        brute=r"""
# BRUTE FORCE: O(|w1| * |w2| * (|w1| + |w2|)) time - perform every swap and recount distinct characters
def is_it_possible(word1, word2):
    for i in range(len(word1)):
        for j in range(len(word2)):
            new1 = word1[:i] + word2[j] + word1[i + 1 :]
            new2 = word2[:j] + word1[i] + word2[j + 1 :]
            if len(set(new1)) == len(set(new2)):
                return True
    return False
""",
        solution=r"""
# OPTIMISED: O(|word1| + |word2| + 26^2) time, O(1) space
# Idea: Frequency tables; try all alphabet pairs instead of all index pairs
def is_it_possible(word1, word2):
    c1, c2 = Counter(word1), Counter(word2)
    for a in c1:
        for b in c2:
            if a == b:
                d1, d2 = len(c1), len(c2)
            else:
                d1 = len(c1) - (c1[a] == 1) + (b not in c1)
                d2 = len(c2) - (c2[b] == 1) + (a not in c2)
            if d1 == d2:
                return True
    return False
""",
    ),
    # ---- Sum of Distances (LeetCode 2615) ----
    dict(
        title="Sum of Distances",
        diff="M",
        lc=2615,
        slug="sum-of-distances",
        prompt=(
            "For every index i, return the sum of |i - j| over all other indices j with nums[j] == nums[i] (0 if "
            "there is none)."
        ),
        sig="def distance(nums: List[int]) -> List[int]:",
        fn="distance",
        tests=[
            (([1, 3, 1, 1, 2],), [5, 0, 3, 4, 0]),
            (([0, 5, 3],), [0, 0, 0]),
            (([1, 1],), [1, 1]),
            (([7, 7, 7],), [3, 2, 3]),
        ],
        hints=[
            "Group the indices by value; each group is independent and its indices are already increasing.",
            (
                "For the k-th index p in a group, indices before it are smaller: their total distance is k * p - "
                "(sum of those indices)."
            ),
            "Likewise the indices after it contribute (sum of those) - (count after) * p. Keep a running prefix sum.",
        ],
        pattern="Group by value + prefix sums of positions",
        explain=(
            "Inside a group with sorted positions p_0 < p_1 < ... , the distance from p_k to the earlier ones is "
            "sum(p_k - p_t) = k * p_k - prefix, and to the later ones sum(p_t - p_k) = (total - prefix - p_k) - (m "
            "- 1 - k) * p_k. With the prefix maintained as we walk the group, each index costs O(1), so the whole "
            "thing is linear. The brute force adds up the distances to every equal element directly."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - compare every pair of equal values",
        brute=r"""
# BRUTE FORCE: O(n^2) time - compare every pair of equal values
def distance(nums):
    n = len(nums)
    return [sum(abs(i - j) for j in range(n) if j != i and nums[j] == nums[i]) for i in range(n)]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Group by value + prefix sums of positions
def distance(nums):
    groups = defaultdict(list)
    for i, v in enumerate(nums):
        groups[v].append(i)
    out = [0] * len(nums)
    for pos in groups.values():
        total = sum(pos)
        m = len(pos)
        pre = 0
        for k, p in enumerate(pos):
            left = k * p - pre
            right = (total - pre - p) - (m - 1 - k) * p
            out[p] = left + right
            pre += p
    return out
""",
    ),
    # ---- Divide Players Into Teams of Equal Skill (LeetCode 2491) ----
    dict(
        title="Divide Players Into Teams of Equal Skill",
        diff="M",
        lc=2491,
        slug="divide-players-into-teams-of-equal-skill",
        prompt=(
            "skill has an even length. Split the players into pairs (teams of two) so that EVERY team has the same "
            "total skill. The chemistry of a team is the product of its two skills. Return the sum of the "
            "chemistries, or -1 if no such split exists."
        ),
        sig="def divide_players(skill: List[int]) -> int:",
        fn="divide_players",
        tests=[
            (([3, 2, 5, 1, 3, 4],), 22),
            (([3, 4],), 12),
            (([1, 1, 2, 3],), -1),
            (([1, 1],), 1),
        ],
        hints=[
            "If all pairs have the same sum S, then S * (n / 2) must equal the total skill - so S is forced.",
            "The smallest player must be matched with the player of skill S - smallest, i.e. the largest one.",
            (
                "Sort and pair the i-th smallest with the i-th largest; every pair must have sum S. A frequency map "
                "works without sorting."
            ),
        ],
        pattern="Forced pairing: smallest with largest (or a complement frequency map)",
        explain=(
            "The common pair sum is determined: S = total / (n / 2). For any valid split, the weakest player has to "
            "pair with someone of skill S - weakest, and by an exchange argument that someone is the strongest "
            "player. After sorting, matching the ends and moving inward either reproduces S for every pair or "
            "exposes a mismatch. The brute force tries all perfect matchings recursively and checks the sums."
        ),
        cx="O(n log n) time, O(1) extra space (O(n) with a frequency map)",
        brute_cx="O((n - 1)!!) time - try every perfect matching of the players",
        brute=r"""
# BRUTE FORCE: O((n - 1)!!) time - try every perfect matching of the players
def divide_players(skill):
    def matchings(items):
        if not items:
            yield []
            return
        first, rest = items[0], items[1:]
        for i, other in enumerate(rest):
            for tail in matchings(rest[:i] + rest[i + 1 :]):
                yield [(first, other)] + tail

    for pairs in matchings(list(skill)):
        if len({a + b for a, b in pairs}) == 1:
            return sum(a * b for a, b in pairs)
    return -1
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space (O(n) with a frequency map)
# Idea: Forced pairing: smallest with largest (or a complement frequency map)
def divide_players(skill):
    skill = sorted(skill)
    target = skill[0] + skill[-1]
    total = 0
    for i in range(len(skill) // 2):
        if skill[i] + skill[-1 - i] != target:
            return -1
        total += skill[i] * skill[-1 - i]
    return total
""",
    ),
    # ---- Odd String Difference (LeetCode 2451) ----
    dict(
        title="Odd String Difference",
        diff="E",
        lc=2451,
        slug="odd-string-difference",
        prompt=(
            "Every word has the same length n. Its difference array has n - 1 entries: the gap between consecutive "
            "letter positions (a = 0, b = 1, ...), e.g. 'acb' -> [2, -1]. All words but ONE share the same "
            "difference array; return the word that is different."
        ),
        sig="def odd_string(words: List[str]) -> str:",
        fn="odd_string",
        tests=[
            ((["adc", "wzy", "abc"],), "abc"),
            ((["aaa", "bob", "ccc", "ddd"],), "bob"),
            ((["abc", "bcd", "cde", "aaa"],), "aaa"),
            ((["ab", "ab", "ac"],), "ac"),
        ],
        hints=[
            "Turn each word into a canonical key: the tuple of differences between neighbouring letters.",
            "Words with equal keys are 'the same shape'; the odd word's key occurs exactly once.",
            "Count the keys in a hash map and return the word whose key has count 1.",
        ],
        pattern="Canonical key (shape signature) + frequency map",
        explain=(
            "Shifting a word by a constant changes every letter but none of the neighbour differences, so the "
            "difference array is a canonical form of the word's shape. With a Counter over those tuples, the unique "
            "shape (count 1) belongs to the answer. The brute force compares each word's key with every other "
            "word's."
        ),
        cx="O(n * L) time, O(n * L) space",
        brute_cx="O(n^2 * L) time - compare every word's difference array with all the others",
        brute=r"""
# BRUTE FORCE: O(n^2 * L) time - compare every word's difference array with all the others
def odd_string(words):
    keys = [[ord(w[i + 1]) - ord(w[i]) for i in range(len(w) - 1)] for w in words]
    for i, key in enumerate(keys):
        if sum(1 for other in keys if other == key) == 1:
            return words[i]
    return ""
""",
        solution=r"""
# OPTIMISED: O(n * L) time, O(n * L) space
# Idea: Canonical key (shape signature) + frequency map
def odd_string(words):
    keys = [tuple(ord(w[i + 1]) - ord(w[i]) for i in range(len(w) - 1)) for w in words]
    counts = Counter(keys)
    for w, key in zip(words, keys):
        if counts[key] == 1:
            return w
    return ""
""",
    ),
    # ---- Number of Beautiful Pairs (LeetCode 2748) ----
    dict(
        title="Number of Beautiful Pairs",
        diff="E",
        lc=2748,
        slug="number-of-beautiful-pairs",
        prompt=(
            "A pair of indices i < j is beautiful if the FIRST digit of nums[i] and the LAST digit of nums[j] are "
            "coprime (gcd = 1). No number ends in 0. Return the number of beautiful pairs."
        ),
        sig="def count_beautiful_pairs(nums: List[int]) -> int:",
        fn="count_beautiful_pairs",
        tests=[
            (([2, 5, 1, 4],), 5),
            (([11, 21, 12],), 2),
            (([1, 1],), 1),
            (([2, 4],), 0),
        ],
        hints=[
            "Only the first digit of nums[i] and the last digit of nums[j] matter - each is one of 1..9.",
            "Scan j from left to right and keep cnt[d] = how many earlier numbers have first digit d.",
            "For each j add cnt[d] for every digit d in 1..9 with gcd(d, last digit of nums[j]) == 1.",
        ],
        pattern="Count by a tiny key (a digit) instead of comparing pairs",
        explain=(
            "The condition depends on two single digits, so earlier numbers can be summarised by a 9-slot histogram "
            "of first digits. For every new number, the number of beautiful pairs ending at it is the total of the "
            "histogram slots whose digit is coprime with its last digit - at most 9 gcd checks. The brute force "
            "tests every pair."
        ),
        cx="O(9 * n) time, O(1) space",
        brute_cx="O(n^2) time - test every pair of indices",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every pair of indices
def count_beautiful_pairs(nums):
    total = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if math.gcd(int(str(nums[i])[0]), nums[j] % 10) == 1:
                total += 1
    return total
""",
        solution=r"""
# OPTIMISED: O(9 * n) time, O(1) space
# Idea: Count by a tiny key (a digit) instead of comparing pairs
def count_beautiful_pairs(nums):
    cnt = [0] * 10
    total = 0
    for x in nums:
        last = x % 10
        for d in range(1, 10):
            if cnt[d] and math.gcd(d, last) == 1:
                total += cnt[d]
        cnt[int(str(x)[0])] += 1
    return total
""",
    ),
    # ---- High-Access Employees (LeetCode 2933) ----
    dict(
        title="High-Access Employees",
        diff="M",
        lc=2933,
        slug="high-access-employees",
        prompt=(
            "access_times[i] = [name, time] where time is 'HHMM' on the same day. An employee is high-access if "
            "they have at least three accesses within a one-hour period; accesses exactly 60 minutes apart do NOT "
            "count as the same period. Return the names of the high-access employees, in any order."
        ),
        sig="def find_high_access_employees(access_times: List[List[str]]) -> List[str]:",
        fn="find_high_access_employees",
        compare="unordered",
        tests=[
            (([["a", "0549"], ["b", "0457"], ["a", "0532"], ["a", "0621"], ["b", "0540"]],), ["a"]),
            (
                (
                    [
                        ["d", "0002"],
                        ["c", "0808"],
                        ["c", "0829"],
                        ["e", "0215"],
                        ["d", "1508"],
                        ["d", "1444"],
                        ["d", "1410"],
                        ["c", "0809"],
                    ],
                ),
                ["c", "d"],
            ),
            (([["a", "0100"], ["a", "0130"], ["a", "0200"]],), []),
            (
                ([["cd", "1025"], ["ab", "1025"], ["cd", "1046"], ["cd", "1055"], ["ab", "1124"], ["ab", "1120"]],),
                ["ab", "cd"],
            ),
        ],
        hints=[
            "Convert 'HHMM' to minutes since midnight: int(HH) * 60 + int(MM).",
            "Group the times by employee, then sort each employee's times.",
            "In sorted order, three accesses fit in a one-hour window iff times[i + 2] - times[i] < 60 for some i.",
        ],
        pattern="Group by key, sort, sliding window of fixed size 3",
        explain=(
            "Per employee, sort the access minutes. Any three accesses inside a window of length < 60 can be taken "
            "as three CONSECUTIVE entries of the sorted list (replace them by the tightest cluster), so it is "
            "enough to test every triple of neighbours: the first and the third must be less than 60 minutes apart. "
            "The brute force checks every triple of accesses of the employee."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n + sum k^3) time - test every triple of accesses per employee",
        brute=r"""
# BRUTE FORCE: O(n + sum k^3) time - test every triple of accesses per employee
def find_high_access_employees(access_times):
    by_name = defaultdict(list)
    for name, t in access_times:
        by_name[name].append(int(t[:2]) * 60 + int(t[2:]))
    out = []
    for name, times in by_name.items():
        for trio in itertools.combinations(times, 3):
            if max(trio) - min(trio) < 60:
                out.append(name)
                break
    return out
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Group by key, sort, sliding window of fixed size 3
def find_high_access_employees(access_times):
    by_name = defaultdict(list)
    for name, t in access_times:
        by_name[name].append(int(t[:2]) * 60 + int(t[2:]))
    out = []
    for name, times in by_name.items():
        times.sort()
        if any(times[i + 2] - times[i] < 60 for i in range(len(times) - 2)):
            out.append(name)
    return out
""",
    ),
]
