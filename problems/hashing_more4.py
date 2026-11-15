"""more Hashing problems (batch 5) - part of the problem bank for the "hashing" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
The core trick: a dict or set answers "have I seen this?" and "how many of these?" in O(1), replacing an inner loop.
"""

PROBLEMS = [
    # ---- X of a Kind in a Deck of Cards (LeetCode 914) ----
    dict(
        title="X of a Kind in a Deck of Cards",
        diff="E",
        lc=914,
        slug="x-of-a-kind-in-a-deck-of-cards",
        prompt=(
            "Can the deck be split into groups where every group has the same size X >= 2 and all cards in a group "
            "have the same value?"
        ),
        sig="def has_groups_size_x(deck: List[int]) -> bool:",
        fn="has_groups_size_x",
        tests=[
            (([1, 2, 3, 4, 4, 3, 2, 1],), True),
            (([1, 1, 1, 2, 2, 2, 3, 3],), False),
            (([1],), False),
            (([1, 1],), True),
            (([1, 1, 2, 2, 2, 2],), True),
        ],
        hints=[
            "Count how many cards each value has.",
            "A group size X works only if X divides EVERY count.",
            "So the best X is the greatest common divisor of all counts; the answer is gcd >= 2.",
        ],
        pattern="Frequency count + gcd",
        explain=(
            "X must divide every count, hence divide their gcd; the gcd itself is the largest candidate, so "
            "checking whether it is at least 2 settles everything."
        ),
        cx="O(n + k log n) time, k = distinct values",
        brute_cx="O(n^2) time - try every X and test every count",
        brute=r"""
# BRUTE FORCE: O(n^2) time - try every X and test every count
def has_groups_size_x(deck):
    counts = Counter(deck).values()
    return any(all(c % x == 0 for c in counts) for x in range(2, len(deck) + 1))
""",
        solution=r"""
# OPTIMISED: O(n + k log n) time, k = distinct values
# Idea: Frequency count + gcd
def has_groups_size_x(deck):
    g = 0
    for c in Counter(deck).values():
        g = math.gcd(g, c)  # gcd(0, c) == c, so this starts cleanly
    return g >= 2
""",
    ),
    # ---- N-Repeated Element in Size 2N Array (LeetCode 961) ----
    dict(
        title="N-Repeated Element in Size 2N Array",
        diff="E",
        lc=961,
        slug="n-repeated-element-in-size-2n-array",
        prompt=(
            "nums has length 2n and n + 1 distinct values; exactly one value appears n times and every other value "
            "appears once. Return the repeated value."
        ),
        sig="def repeated_n_times(nums: List[int]) -> int:",
        fn="repeated_n_times",
        tests=[
            (([1, 2, 3, 3],), 3),
            (([2, 1, 2, 5, 3, 2],), 2),
            (([5, 1, 5, 2, 5, 3, 5, 4],), 5),
        ],
        hints=[
            "Every value except one is unique.",
            "So the first value you see TWICE must be the repeated one.",
            "Scan with a set: return the first number already in the set.",
        ],
        pattern="First duplicate with a set",
        explain=(
            "Only the repeated value can ever appear twice, so detecting any duplicate is enough - no counting needed."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - count each value with list.count",
        brute=r"""
# BRUTE FORCE: O(n^2) time - count each value with list.count
def repeated_n_times(nums):
    n = len(nums) // 2
    for x in nums:
        if nums.count(x) == n:
            return x
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: First duplicate with a set
def repeated_n_times(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return x
        seen.add(x)
""",
    ),
    # ---- Pairs of Songs With Total Durations Divisible by 60 (LeetCode 1010) ----
    dict(
        title="Pairs of Songs With Total Durations Divisible by 60",
        diff="M",
        lc=1010,
        slug="pairs-of-songs-with-total-durations-divisible-by-60",
        prompt="Count pairs of songs (i < j) whose total duration time[i] + time[j] is divisible by 60.",
        sig="def num_pairs_divisible_by_60(time: List[int]) -> int:",
        fn="num_pairs_divisible_by_60",
        tests=[
            (([30, 20, 150, 100, 40],), 3),
            (([60, 60, 60],), 3),
            (([1],), 0),
            (([30, 30, 30],), 3),
        ],
        hints=[
            "Only each duration's remainder mod 60 matters.",
            "A song with remainder r needs a partner with remainder (60 - r) % 60.",
            (
                "Walk the list keeping counts of remainders seen so far; add the count of the needed partner "
                "remainder before recording the current one."
            ),
        ],
        pattern="Remainder counting (two-sum modulo)",
        explain=(
            "Looking up the complement's count replaces the inner loop; checking BEFORE inserting guarantees i < j."
        ),
        cx="O(n) time, O(60) space",
        brute_cx="O(n^2) time - test every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every pair
def num_pairs_divisible_by_60(time):
    return sum(
        1
        for i in range(len(time))
        for j in range(i + 1, len(time))
        if (time[i] + time[j]) % 60 == 0
    )
""",
        solution=r"""
# OPTIMISED: O(n) time, O(60) space
# Idea: Remainder counting (two-sum modulo)
def num_pairs_divisible_by_60(time):
    seen = [0] * 60  # seen[r]: how many earlier songs have remainder r
    pairs = 0
    for t in time:
        r = t % 60
        pairs += seen[(60 - r) % 60]
        seen[r] += 1
    return pairs
""",
    ),
    # ---- Number of Equivalent Domino Pairs (LeetCode 1128) ----
    dict(
        title="Number of Equivalent Domino Pairs",
        diff="E",
        lc=1128,
        slug="number-of-equivalent-domino-pairs",
        prompt=(
            "Dominoes [a, b] and [c, d] are equivalent if (a == c and b == d) or (a == d and b == c). Count the "
            "pairs (i < j) of equivalent dominoes."
        ),
        sig="def num_equiv_domino_pairs(dominoes: List[List[int]]) -> int:",
        fn="num_equiv_domino_pairs",
        tests=[
            (([[1, 2], [2, 1], [3, 4], [5, 6]],), 1),
            (([[1, 2], [1, 2], [1, 1], [1, 2], [2, 2]],), 3),
            (([[1, 1]],), 0),
            (([[1, 2], [2, 1], [1, 2], [2, 1]],), 6),
        ],
        hints=[
            "Make equivalent dominoes look identical: sort the two numbers.",
            "Count how many dominoes have each normalised form.",
            "A group of c equal dominoes contributes c * (c - 1) / 2 pairs.",
        ],
        pattern="Canonical form + counting pairs",
        explain="Normalising turns 'equivalent' into 'equal', and equal items in a group of c form c choose 2 pairs.",
        cx="O(n) time",
        brute_cx="O(n^2) time - compare every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - compare every pair
def num_equiv_domino_pairs(dominoes):
    return sum(
        1
        for i in range(len(dominoes))
        for j in range(i + 1, len(dominoes))
        if sorted(dominoes[i]) == sorted(dominoes[j])
    )
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Canonical form + counting pairs
def num_equiv_domino_pairs(dominoes):
    counts = Counter(tuple(sorted(d)) for d in dominoes)
    return sum(c * (c - 1) // 2 for c in counts.values())
""",
    ),
    # ---- Maximum Number of Balloons (LeetCode 1189) ----
    dict(
        title="Maximum Number of Balloons",
        diff="E",
        lc=1189,
        slug="maximum-number-of-balloons",
        prompt='Using each character of text at most once, how many copies of the word "balloon" can you form?',
        sig="def max_number_of_balloons(text: str) -> int:",
        fn="max_number_of_balloons",
        tests=[
            (("nlaebolko",), 1),
            (("loonbalxballpoon",), 2),
            (("leetcode",), 0),
            (("balloonballoon",), 2),
        ],
        hints=[
            "Count the letters of text.",
            "'balloon' needs b:1, a:1, l:2, o:2, n:1.",
            "The answer is the minimum over letters of (available count // needed count).",
        ],
        pattern="Frequency count, bottleneck letter",
        explain="The scarcest letter (relative to how much one word needs) limits the number of words you can build.",
        cx="O(n) time",
        brute_cx="O(n * L) time - build one word at a time until a letter runs out",
        brute=r"""
# BRUTE FORCE: O(n * L) time - build one word at a time until a letter runs out
def max_number_of_balloons(text):
    letters = list(text)
    words = 0
    while True:
        for ch in "balloon":
            if ch in letters:
                letters.remove(ch)
            else:
                return words
        words += 1
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Frequency count, bottleneck letter
def max_number_of_balloons(text):
    have, need = Counter(text), Counter("balloon")
    return min(have[ch] // k for ch, k in need.items())
""",
    ),
    # ---- Check If N and Its Double Exist (LeetCode 1346) ----
    dict(
        title="Check If N and Its Double Exist",
        diff="E",
        lc=1346,
        slug="check-if-n-and-its-double-exist",
        prompt="Return True if there are two DIFFERENT indices i and j with arr[i] == 2 * arr[j].",
        sig="def check_if_exist(arr: List[int]) -> bool:",
        fn="check_if_exist",
        tests=[
            (([10, 2, 5, 3],), True),
            (([3, 1, 7, 11],), False),
            (([0, 0],), True),
            (([0],), False),
            (([-2, 0, 10, -19, 4, 6, -8],), False),
        ],
        hints=[
            "For each number x you want to know if 2x or x / 2 appeared before.",
            "Keep a set of numbers seen so far.",
            (
                "Check x * 2 in seen, or (x is even and x // 2 in seen). Checking BEFORE inserting handles the "
                "'different indices' rule (and the lone 0)."
            ),
        ],
        pattern="Set of seen values (two-sum style)",
        explain="Whichever of the pair comes second finds the first in the set, so one pass in either order suffices.",
        cx="O(n) time",
        brute_cx="O(n^2) time - test every ordered pair of indices",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every ordered pair of indices
def check_if_exist(arr):
    return any(i != j and arr[i] == 2 * arr[j] for i in range(len(arr)) for j in range(len(arr)))
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Set of seen values (two-sum style)
def check_if_exist(arr):
    seen = set()
    for x in arr:
        if 2 * x in seen or (x % 2 == 0 and x // 2 in seen):
            return True
        seen.add(x)
    return False
""",
    ),
    # ---- Determine if Two Strings Are Close (LeetCode 1657) ----
    dict(
        title="Determine if Two Strings Are Close",
        diff="M",
        lc=1657,
        slug="determine-if-two-strings-are-close",
        prompt=(
            "Two operations are allowed on a string: (1) swap any two characters; (2) pick two letters that both "
            "appear and swap ALL occurrences of one with the other. Return True if word1 can be turned into word2."
        ),
        sig="def close_strings(word1: str, word2: str) -> bool:",
        fn="close_strings",
        tests=[
            (("abc", "bca"), True),
            (("a", "aa"), False),
            (("cabbba", "abbccc"), True),
            (("cabbba", "aabbss"), False),
        ],
        hints=[
            "Operation 1 lets you reorder freely, so positions do not matter.",
            "Operation 2 lets you shuffle which letter owns which frequency - but never introduces a new letter.",
            "So the words are close iff they use the same SET of letters and the same MULTISET of frequencies.",
        ],
        pattern="Compare letter sets and sorted frequency lists",
        explain=(
            "Op 1 equalises order; op 2 permutes frequencies among existing letters. Those are the only freedoms, "
            "so these two invariants are both necessary and sufficient."
        ),
        cx="O(n + k log k) time",
        brute_cx="O(reachable strings) time - BFS using both operations",
        brute=r"""
# BRUTE FORCE: O(reachable strings) time - BFS using both operations
def close_strings(word1, word2):
    if len(word1) != len(word2):
        return False
    seen, queue = {word1}, deque([word1])
    while queue:
        cur = queue.popleft()
        if cur == word2:
            return True
        nxt = []
        for i in range(len(cur)):  # operation 1: swap two positions
            for j in range(i + 1, len(cur)):
                chars = list(cur)
                chars[i], chars[j] = chars[j], chars[i]
                nxt.append("".join(chars))
        letters = sorted(set(cur))
        for a in range(len(letters)):  # operation 2: swap two existing letters everywhere
            for b in range(a + 1, len(letters)):
                nxt.append(
                    cur.translate({ord(letters[a]): letters[b], ord(letters[b]): letters[a]})
                )
        for s in nxt:
            if s not in seen:
                seen.add(s)
                queue.append(s)
    return False
""",
        solution=r"""
# OPTIMISED: O(n + k log k) time
# Idea: Compare letter sets and sorted frequency lists
def close_strings(word1, word2):
    if len(word1) != len(word2):
        return False
    c1, c2 = Counter(word1), Counter(word2)
    return set(c1) == set(c2) and sorted(c1.values()) == sorted(c2.values())
""",
    ),
    # ---- Max Number of K-Sum Pairs (LeetCode 1679) ----
    dict(
        title="Max Number of K-Sum Pairs",
        diff="M",
        lc=1679,
        slug="max-number-of-k-sum-pairs",
        prompt="One operation removes two numbers from nums whose sum is k. Return the maximum number of operations.",
        sig="def max_operations(nums: List[int], k: int) -> int:",
        fn="max_operations",
        tests=[
            (([1, 2, 3, 4], 5), 2),
            (([3, 1, 3, 4, 3], 6), 1),
            (([1, 1], 2), 1),
            (([1], 1), 0),
        ],
        hints=[
            "Each value x can only pair with the value k - x.",
            "Count occurrences of every value.",
            "For x < k - x add min(count[x], count[k - x]); when x == k - x add count[x] // 2.",
        ],
        pattern="Frequency count + complement matching",
        explain="Pairs (x, k - x) are independent of other pairs, so each contributes the smaller of the two counts.",
        cx="O(n) time",
        brute_cx="O(n^3) time - repeatedly find and remove any valid pair",
        brute=r"""
# BRUTE FORCE: O(n^3) time - repeatedly find and remove any valid pair
def max_operations(nums, k):
    nums = list(nums)
    ops = 0
    found = True
    while found:
        found = False
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                if nums[i] + nums[j] == k:
                    del nums[j], nums[i]  # remove the larger index first
                    ops += 1
                    found = True
                    break
            if found:
                break
    return ops
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Frequency count + complement matching
def max_operations(nums, k):
    counts = Counter(nums)
    ops = 0
    for x, c in counts.items():
        y = k - x
        if x < y:
            ops += min(c, counts.get(y, 0))
        elif x == y:
            ops += c // 2
    return ops
""",
    ),
    # ---- Find Players With Zero or One Losses (LeetCode 2225) ----
    dict(
        title="Find Players With Zero or One Losses",
        diff="M",
        lc=2225,
        slug="find-players-with-zero-or-one-losses",
        prompt=(
            "matches[i] = [winner, loser]. Return [players who never lost, players who lost exactly once], each "
            "list sorted ascending. Only players who played at least one match count."
        ),
        sig="def find_winners(matches: List[List[int]]) -> List[List[int]]:",
        fn="find_winners",
        tests=[
            (
                ([[1, 3], [2, 3], [3, 6], [5, 6], [5, 7], [4, 5], [4, 8], [4, 9], [10, 4], [10, 9]],),
                [[1, 2, 10], [4, 5, 7, 8]],
            ),
            (([[2, 3], [1, 3], [5, 4], [6, 4]],), [[1, 2, 5, 6], []]),
            (([[1, 2]],), [[1], [2]]),
        ],
        hints=[
            "You need each player's number of losses.",
            "Collect every player that appears, and count losses in a Counter.",
            "Players with 0 losses = appeared but not in the counter; exactly 1 loss = counter value 1. Sort both.",
        ],
        pattern="Counting with a hash map",
        explain="One pass records who played and how often each lost; then the two groups are read off the counts.",
        cx="O(n log n) time (sorting)",
        brute_cx="O(P * M) time - rescan all matches for every player",
        brute=r"""
# BRUTE FORCE: O(P * M) time - rescan all matches for every player
def find_winners(matches):
    players = {p for match in matches for p in match}
    never, once = [], []
    for p in sorted(players):
        losses = sum(1 for _, loser in matches if loser == p)
        if losses == 0:
            never.append(p)
        elif losses == 1:
            once.append(p)
    return [never, once]
""",
        solution=r"""
# OPTIMISED: O(n log n) time (sorting)
# Idea: Counting with a hash map
def find_winners(matches):
    players = set()
    losses = Counter()
    for winner, loser in matches:
        players.add(winner)
        players.add(loser)
        losses[loser] += 1
    return [
        sorted(p for p in players if losses[p] == 0),
        sorted(p for p in players if losses[p] == 1),
    ]
""",
    ),
    # ---- Max Sum of a Pair With Equal Sum of Digits (LeetCode 2342) ----
    dict(
        title="Max Sum of a Pair With Equal Sum of Digits",
        diff="M",
        lc=2342,
        slug="max-sum-of-a-pair-with-equal-sum-of-digits",
        prompt=(
            "Choose two different indices i, j such that nums[i] and nums[j] have the same digit sum. Return the "
            "maximum possible nums[i] + nums[j], or -1 if no such pair exists."
        ),
        sig="def maximum_sum(nums: List[int]) -> int:",
        fn="maximum_sum",
        tests=[
            (([18, 43, 36, 13, 7],), 54),
            (([10, 12, 19, 14],), -1),
            (([5, 5],), 10),
            (([1],), -1),
        ],
        hints=[
            "Group numbers by their digit sum.",
            "Within a group only the two LARGEST numbers matter.",
            (
                "Keep a dict digit_sum -> best number so far; when a new number arrives, combine it with the stored "
                "best, then update the best."
            ),
        ],
        pattern="Group by key, keep the running maximum",
        explain=(
            "For each digit sum we only ever need the biggest earlier partner, so one dict of maxima replaces "
            "comparing all pairs."
        ),
        cx="O(n log V) time",
        brute_cx="O(n^2 log V) time - compare every pair",
        brute=r"""
# BRUTE FORCE: O(n^2 log V) time - compare every pair
def maximum_sum(nums):
    def digit_sum(x):
        return sum(int(d) for d in str(x))

    best = -1
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if digit_sum(nums[i]) == digit_sum(nums[j]):
                best = max(best, nums[i] + nums[j])
    return best
""",
        solution=r"""
# OPTIMISED: O(n log V) time
# Idea: Group by key, keep the running maximum
def maximum_sum(nums):
    best_by_sum = {}
    answer = -1
    for x in nums:
        s = sum(int(d) for d in str(x))
        if s in best_by_sum:
            answer = max(answer, best_by_sum[s] + x)
        best_by_sum[s] = max(best_by_sum.get(s, 0), x)
    return answer
""",
    ),
    # ---- Equal Row and Column Pairs (LeetCode 2352) ----
    dict(
        title="Equal Row and Column Pairs",
        diff="M",
        lc=2352,
        slug="equal-row-and-column-pairs",
        prompt=(
            "Given an n x n grid, count pairs (r, c) such that row r and column c contain the same numbers in the "
            "same order."
        ),
        sig="def equal_pairs(grid: List[List[int]]) -> int:",
        fn="equal_pairs",
        tests=[
            (([[3, 2, 1], [1, 7, 6], [2, 7, 7]],), 1),
            (([[3, 1, 2, 2], [1, 4, 4, 5], [2, 4, 2, 2], [2, 4, 2, 2]],), 3),
            (([[1]],), 1),
            (([[1, 2], [3, 4]],), 0),
        ],
        hints=[
            "Comparing every row with every column element by element costs O(n^3).",
            "Rows and columns can be turned into tuples, which are hashable.",
            "Count each row tuple in a Counter, then for every column add the count of a matching row.",
        ],
        pattern="Hash whole rows (tuples) and match against columns",
        explain=(
            "Hashing replaces an O(n) comparison per (row, column) pair with an O(1) lookup after O(n) work per line."
        ),
        cx="O(n^2) time, O(n^2) space",
        brute_cx="O(n^3) time - compare every row with every column",
        brute=r"""
# BRUTE FORCE: O(n^3) time - compare every row with every column
def equal_pairs(grid):
    n = len(grid)
    return sum(
        1 for r in range(n) for c in range(n) if all(grid[r][k] == grid[k][c] for k in range(n))
    )
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n^2) space
# Idea: Hash whole rows (tuples) and match against columns
def equal_pairs(grid):
    rows = Counter(tuple(row) for row in grid)
    return sum(rows[tuple(col)] for col in zip(*grid))  # zip(*grid) yields the columns
""",
    ),
    # ---- Uncommon Words from Two Sentences (LeetCode 884) ----
    dict(
        title="Uncommon Words from Two Sentences",
        diff="E",
        lc=884,
        slug="uncommon-words-from-two-sentences",
        prompt=(
            "A word is uncommon if it appears exactly once in one sentence and does not appear in the other. Return "
            "all uncommon words (any order). Sentences are space-separated lowercase words."
        ),
        sig="def uncommon_from_sentences(s1: str, s2: str) -> List[str]:",
        fn="uncommon_from_sentences",
        compare="unordered",
        tests=[
            (("this apple is sweet", "this apple is sour"), ["sweet", "sour"]),
            (("apple apple", "banana"), ["banana"]),
            (("a b", "c d"), ["a", "b", "c", "d"]),
        ],
        hints=[
            "A word that is uncommon appears exactly once across BOTH sentences combined.",
            "Join the sentences and count every word.",
            "Return the words whose total count is 1.",
        ],
        pattern="Count words over the combined text",
        explain=(
            "Appearing once in one sentence and zero times in the other is the same as appearing once overall; "
            "appearing twice in one sentence disqualifies it automatically."
        ),
        cx="O(n) time",
        brute_cx="O(n^2) time - list.count for every word",
        brute=r"""
# BRUTE FORCE: O(n^2) time - list.count for every word
def uncommon_from_sentences(s1, s2):
    words = (s1 + " " + s2).split()
    return [w for w in words if words.count(w) == 1]
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Count words over the combined text
def uncommon_from_sentences(s1, s2):
    counts = Counter((s1 + " " + s2).split())
    return [w for w, c in counts.items() if c == 1]
""",
    ),
]
