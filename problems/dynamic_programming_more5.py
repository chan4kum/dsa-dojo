"""more Dynamic Programming problems (batch 6) - part of the problem bank for the "dynamic_programming" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Frog Jump (LeetCode 403) ----
    dict(
        title="Frog Jump",
        diff="H",
        lc=403,
        slug="frog-jump",
        prompt=(
            "stones holds the sorted positions of stones in a river (the first is position 0). A frog starts on the "
            "first stone and its first jump must be exactly 1 unit. If its last jump was k units, its next jump "
            "must be k - 1, k or k + 1 units, forwards, and must land on a stone. Return true if the frog can reach "
            "the last stone."
        ),
        sig="def can_cross(stones: List[int]) -> bool:",
        fn="can_cross",
        tests=[
            (([0, 1, 3, 5, 6, 8, 12, 17],), True),
            (([0, 1, 2, 3, 4, 8, 9, 11],), False),
            (([0, 1],), True),
            (([0, 2],), False),
        ],
        hints=[
            "The situation of the frog is (stone it stands on, size of the last jump).",
            (
                "Brute force: DFS over those situations. The same (stone, jump) pair is reached again and again - "
                "remember it."
            ),
            (
                "For every stone keep the SET of jump sizes with which it can be reached; from each such size k, "
                "try k - 1, k and k + 1 and record the jump on the stone you land on."
            ),
        ],
        pattern="DP over (position, last jump) as a set per stone",
        explain=(
            "What the frog may do next depends only on its stone and its last jump, so we store for each stone "
            "every jump size that can bring the frog there. Processing stones left to right guarantees a stone's "
            "set is complete before it is used. The last stone is reachable exactly when its set is non-empty. The "
            "brute force explores the same transitions by plain DFS without remembering anything."
        ),
        cx="O(n^2) time, O(n^2) space",
        brute_cx="exponential - DFS over jump choices with no memory",
        brute=r"""
# BRUTE FORCE: exponential - DFS over jump choices with no memory
def can_cross(stones):
    spots = set(stones)
    last = stones[-1]

    def go(pos, k):
        if pos == last:
            return True
        for step in (k - 1, k, k + 1):
            if step > 0 and pos + step in spots and go(pos + step, step):
                return True
        return False

    return go(stones[0], 0)
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n^2) space
# Idea: DP over (position, last jump) as a set per stone
def can_cross(stones):
    jumps = {s: set() for s in stones}
    jumps[stones[0]].add(0)
    for s in stones:
        for k in jumps[s]:
            for step in (k - 1, k, k + 1):
                if step > 0 and s + step in jumps:
                    jumps[s + step].add(step)
    return bool(jumps[stones[-1]])
""",
    ),
    # ---- Unique Substrings in Wraparound String (LeetCode 467) ----
    dict(
        title="Unique Substrings in Wraparound String",
        diff="M",
        lc=467,
        slug="unique-substrings-in-wraparound-string",
        prompt=(
            "Let base be the infinite string 'abcdefghijklmnopqrstuvwxyzabcdefghi...' (the alphabet repeated "
            "forever). Given a lowercase string s, return the number of DISTINCT non-empty substrings of s that "
            "also appear in base."
        ),
        sig="def find_substring_in_wrapround_string(s: str) -> int:",
        fn="find_substring_in_wrapround_string",
        tests=[
            (("a",), 1),
            (("cac",), 2),
            (("zab",), 6),
            (("abcabc",), 6),
        ],
        hints=[
            (
                "A substring is in base exactly when every letter is the successor of the previous one (z is "
                "followed by a)."
            ),
            (
                "Distinct substrings that END with letter c: if the longest valid run ending in c has length L, "
                "then there are exactly L of them (lengths 1..L), and shorter ones are included in longer ones."
            ),
            (
                "Track the current run length while scanning, keep for each letter the maximum run that ends in it, "
                "and sum those 26 maxima."
            ),
        ],
        pattern="DP: longest valid run ending at each letter",
        explain=(
            "Every valid substring is determined by its last letter and its length. If a run of length L ends at "
            "letter c, all its suffixes (lengths 1..L) are valid and distinct, so each letter contributes the "
            "longest run seen that ends there; duplicates across positions are automatically merged by the maximum. "
            "The brute force collects every valid substring in a set."
        ),
        cx="O(n) time, O(26) space",
        brute_cx="O(n^3) time - every substring checked and stored",
        brute=r"""
# BRUTE FORCE: O(n^3) time - every substring checked and stored
def find_substring_in_wrapround_string(s):
    found = set()
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            piece = s[i:j]
            if all((ord(piece[k + 1]) - ord(piece[k])) % 26 == 1 for k in range(len(piece) - 1)):
                found.add(piece)
    return len(found)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(26) space
# Idea: DP: longest valid run ending at each letter
def find_substring_in_wrapround_string(s):
    longest = defaultdict(int)
    run = 0
    for i, ch in enumerate(s):
        if i > 0 and (ord(ch) - ord(s[i - 1])) % 26 == 1:
            run += 1
        else:
            run = 1
        longest[ch] = max(longest[ch], run)
    return sum(longest.values())
""",
    ),
    # ---- Student Attendance Record II (LeetCode 552) ----
    dict(
        title="Student Attendance Record II",
        diff="H",
        lc=552,
        slug="student-attendance-record-ii",
        prompt=(
            "An attendance record is a string of 'P' (present), 'L' (late) and 'A' (absent). A student is awarded "
            "if the record has FEWER than 2 'A' in total and NEVER 3 or more consecutive 'L'. Given n, return the "
            "number of records of length n that earn the award, modulo 10^9 + 7."
        ),
        sig="def check_record(n: int) -> int:",
        fn="check_record",
        tests=[
            ((1,), 3),
            ((2,), 8),
            ((3,), 19),
            ((4,), 43),
        ],
        hints=[
            (
                "Checking all 3^n strings is far too slow for big n - but a record is described, for the future, by "
                "only two numbers."
            ),
            "How many 'A' so far (0 or 1) and how many 'L' in a row at the end (0, 1 or 2).",
            (
                "Keep a table dp[a][l] of counts. For each new day add 'P' (resets l to 0), 'L' (l + 1, only if l < "
                "2) or 'A' (only if a == 0)."
            ),
        ],
        pattern="Counting DP over a small state (absences, trailing lates)",
        explain=(
            "The award rules only look at the number of absences and the current streak of lates, so those six "
            "states are all we need to extend a record by one day. Starting from the empty record in state (0, 0) "
            "and applying the three transitions n times counts every valid record exactly once. The brute force "
            "builds all 3^n strings."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(3^n * n) time - generate and test every record",
        brute=r"""
# BRUTE FORCE: O(3^n * n) time - generate and test every record
def check_record(n):
    count = 0
    for record in itertools.product("PLA", repeat=n):
        word = "".join(record)
        if word.count("A") < 2 and "LLL" not in word:
            count += 1
    return count % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Counting DP over a small state (absences, trailing lates)
def check_record(n):
    mod = 10**9 + 7
    dp = [[0] * 3 for _ in range(2)]
    dp[0][0] = 1
    for _ in range(n):
        new = [[0] * 3 for _ in range(2)]
        for a in range(2):
            for late in range(3):
                v = dp[a][late]
                if not v:
                    continue
                new[a][0] += v
                if late < 2:
                    new[a][late + 1] += v
                if a == 0:
                    new[1][0] += v
        dp = [[x % mod for x in row] for row in new]
    return sum(sum(row) for row in dp) % mod
""",
    ),
    # ---- Non-negative Integers without Consecutive Ones (LeetCode 600) ----
    dict(
        title="Non-negative Integers without Consecutive Ones",
        diff="H",
        lc=600,
        slug="non-negative-integers-without-consecutive-ones",
        prompt=(
            "Given a positive integer n, return how many integers in the range [0, n] have NO two adjacent 1 bits "
            "in their binary representation."
        ),
        sig="def find_integers(n: int) -> int:",
        fn="find_integers",
        tests=[
            ((5,), 5),
            ((1,), 2),
            ((2,), 3),
            ((8,), 6),
        ],
        hints=[
            "Brute force: test every number from 0 to n. That is far too slow when n is 10^9.",
            (
                "Let f[i] = number of i-bit strings without '11'. Then f[i] = f[i-1] (first bit 0) + f[i-2] (first "
                "bits '10') - Fibonacci numbers."
            ),
            (
                "Walk the bits of n from the top. Each time n has a 1, count all numbers that put a 0 there and are "
                "free below (f[remaining]). If you meet '11' in n itself, stop; otherwise add 1 for n."
            ),
        ],
        pattern="Digit DP with Fibonacci counts",
        explain=(
            "Numbers <= n split by the first bit where they differ from n: at a position where n has 1, a smaller "
            "number has 0 and then any valid suffix, giving f[remaining bits] choices. Every such block is counted "
            "once, and the walk stops as soon as n itself contains '11' because every larger prefix is invalid too. "
            "If n never breaks the rule it counts itself (+1). The brute force checks each number's binary string."
        ),
        cx="O(log n) time, O(log n) space",
        brute_cx="O(n log n) time - test every number in the range",
        brute=r"""
# BRUTE FORCE: O(n log n) time - test every number in the range
def find_integers(n):
    return sum(1 for x in range(n + 1) if "11" not in bin(x))
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(log n) space
# Idea: Digit DP with Fibonacci counts
def find_integers(n):
    bits = bin(n)[2:]
    length = len(bits)
    f = [1, 2]
    for _ in range(length):
        f.append(f[-1] + f[-2])
    total = 0
    previous = "0"
    for i, bit in enumerate(bits):
        if bit == "1":
            total += f[length - i - 1]
            if previous == "1":
                return total
        previous = bit
    return total + 1
""",
    ),
    # ---- K Inverse Pairs Array (LeetCode 629) ----
    dict(
        title="K Inverse Pairs Array",
        diff="H",
        lc=629,
        slug="k-inverse-pairs-array",
        prompt=(
            "An inverse pair in an array is a pair of indices i < j with nums[i] > nums[j]. Return the number of "
            "different arrays that are permutations of 1..n and have EXACTLY k inverse pairs, modulo 10^9 + 7."
        ),
        sig="def k_inverse_pairs(n: int, k: int) -> int:",
        fn="k_inverse_pairs",
        tests=[
            ((3, 0), 1),
            ((3, 1), 2),
            ((1, 1), 0),
            ((4, 2), 5),
        ],
        hints=[
            (
                "Build permutations by inserting the number n into a permutation of 1..n-1. Where you insert it "
                "decides how many NEW inverse pairs appear."
            ),
            "Putting n at distance t from the right end creates exactly t new inversions, for t = 0 .. n - 1.",
            (
                "So dp[i][j] = dp[i-1][j] + dp[i-1][j-1] + ... + dp[i-1][j-(i-1)]. Keep a running window sum so "
                "each cell costs O(1)."
            ),
        ],
        pattern="DP with a sliding-window sum (insertion into permutations)",
        explain=(
            "Insert the largest value last: if it ends up with t numbers to its right, each of them forms an "
            "inversion with it, adding t inversions. Every permutation of i values is produced exactly once by one "
            "smaller permutation and one insertion slot. The sum over slots is a window of i consecutive values of "
            "the previous row, which we update incrementally. The brute force counts inversions in all n! "
            "permutations."
        ),
        cx="O(n * k) time, O(k) space",
        brute_cx="O(n! * n^2) time - enumerate every permutation",
        brute=r"""
# BRUTE FORCE: O(n! * n^2) time - enumerate every permutation
def k_inverse_pairs(n, k):
    count = 0
    for perm in itertools.permutations(range(n)):
        inversions = sum(1 for i in range(n) for j in range(i + 1, n) if perm[i] > perm[j])
        if inversions == k:
            count += 1
    return count % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n * k) time, O(k) space
# Idea: DP with a sliding-window sum (insertion into permutations)
def k_inverse_pairs(n, k):
    mod = 10**9 + 7
    dp = [1] + [0] * k
    for i in range(2, n + 1):
        new = [0] * (k + 1)
        window = 0
        for j in range(k + 1):
            window += dp[j]
            if j >= i:
                window -= dp[j - i]
            new[j] = window % mod
        dp = new
    return dp[k] % mod
""",
    ),
    # ---- 2 Keys Keyboard (LeetCode 650) ----
    dict(
        title="2 Keys Keyboard",
        diff="M",
        lc=650,
        slug="2-keys-keyboard",
        prompt=(
            "A notepad starts with one character 'A'. In each step you may either COPY ALL (copy everything "
            "currently on the notepad) or PASTE (append the copied text). Return the minimum number of steps to get "
            "exactly n characters 'A' on the notepad."
        ),
        sig="def min_steps(n: int) -> int:",
        fn="min_steps",
        tests=[
            ((3,), 3),
            ((1,), 0),
            ((9,), 6),
            ((12,), 7),
        ],
        hints=[
            "Brute force: BFS over the state (characters on screen, characters in clipboard).",
            "Copy-all followed by p pastes multiplies the length by p + 1 and costs p + 1 steps.",
            (
                "So reaching n means writing n as a product of factors and paying the SUM of the factors; the sum "
                "is smallest when you use the prime factors. Add up the prime factors of n."
            ),
        ],
        pattern="Prime factorisation as a cost",
        explain=(
            "Each 'copy then paste p times' block multiplies the text by f = p + 1 for f steps. Splitting a factor "
            "into smaller ones never costs more (a * b >= a + b for a, b >= 2), so the cheapest plan multiplies by "
            "the prime factors one at a time, and the cost is their sum. The brute force explores all (length, "
            "clipboard) states."
        ),
        cx="O(sqrt n) time, O(1) space",
        brute_cx="O(n^2) time - breadth-first search over (length, clipboard)",
        brute=r"""
# BRUTE FORCE: O(n^2) time - breadth-first search over (length, clipboard)
def min_steps(n):
    if n == 1:
        return 0
    seen = {(1, 0)}
    frontier = [(1, 0)]
    steps = 0
    while frontier:
        steps += 1
        nxt = []
        for length, clip in frontier:
            moves = [(length, length)]
            if clip:
                moves.append((length + clip, clip))
            for state in moves:
                if state[0] == n:
                    return steps
                if state[0] < n and state not in seen:
                    seen.add(state)
                    nxt.append(state)
        frontier = nxt
""",
        solution=r"""
# OPTIMISED: O(sqrt n) time, O(1) space
# Idea: Prime factorisation as a cost
def min_steps(n):
    total = 0
    d = 2
    while n > 1:
        while n % d == 0:
            total += d
            n //= d
        d += 1
    return total
""",
    ),
    # ---- Minimum ASCII Delete Sum for Two Strings (LeetCode 712) ----
    dict(
        title="Minimum ASCII Delete Sum for Two Strings",
        diff="M",
        lc=712,
        slug="minimum-ascii-delete-sum-for-two-strings",
        prompt=(
            "Delete characters from s1 and s2 until the two strings are EQUAL. Deleting a character costs its ASCII "
            "value. Return the minimum total cost."
        ),
        sig="def minimum_delete_sum(s1: str, s2: str) -> int:",
        fn="minimum_delete_sum",
        tests=[
            (("sea", "eat"), 231),
            (("delete", "leet"), 403),
            (("a", "a"), 0),
            (("a", "b"), 195),
        ],
        hints=[
            "What is left after deleting must be a string that is a subsequence of BOTH inputs (a common subsequence).",
            (
                "Cost = (total ASCII of s1 + total ASCII of s2) - 2 * (ASCII sum of the kept common subsequence), "
                "so keep the common subsequence with the LARGEST ASCII sum."
            ),
            "That is the longest-common-subsequence DP where a match adds the character's ASCII value instead of 1.",
        ],
        pattern="Weighted LCS",
        explain=(
            "The characters you keep are the same in both strings and form a common subsequence; every other "
            "character is deleted and paid for. Maximising the kept weight minimises the cost. The LCS recurrence "
            "works with weights: dp[i][j] = ascii(s1[i]) + dp[i+1][j+1] on a match, otherwise the better of "
            "skipping one character. The brute force tries every subsequence of s1 and keeps the heaviest one that "
            "is also a subsequence of s2."
        ),
        cx="O(n * m) time, O(n * m) space",
        brute_cx="O(2^n * (n + m)) time - every subsequence of s1",
        brute=r"""
# BRUTE FORCE: O(2^n * (n + m)) time - every subsequence of s1
def minimum_delete_sum(s1, s2):
    def is_subsequence(piece, text):
        it = iter(text)
        return all(c in it for c in piece)

    n = len(s1)
    best = 0
    for mask in range(1 << n):
        piece = "".join(s1[i] for i in range(n) if mask >> i & 1)
        if is_subsequence(piece, s2):
            best = max(best, sum(map(ord, piece)))
    return sum(map(ord, s1)) + sum(map(ord, s2)) - 2 * best
""",
        solution=r"""
# OPTIMISED: O(n * m) time, O(n * m) space
# Idea: Weighted LCS
def minimum_delete_sum(s1, s2):
    n, m = len(s1), len(s2)
    dp = [[0] * (m + 1) for _ in range(n + 1)]
    for i in range(n - 1, -1, -1):
        for j in range(m - 1, -1, -1):
            if s1[i] == s2[j]:
                dp[i][j] = ord(s1[i]) + dp[i + 1][j + 1]
            else:
                dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])
    return sum(map(ord, s1)) + sum(map(ord, s2)) - 2 * dp[0][0]
""",
    ),
    # ---- Champagne Tower (LeetCode 799) ----
    dict(
        title="Champagne Tower",
        diff="M",
        lc=799,
        slug="champagne-tower",
        prompt=(
            "Glasses are stacked in a pyramid: 1 glass in row 0, 2 in row 1, and so on. Each glass holds 1 cup. You "
            "pour `poured` cups into the top glass. When a glass overflows, the excess is split EQUALLY between the "
            "two glasses directly beneath it. Return how full the glass at (query_row, query_glass) is, as a number "
            "between 0 and 1 (both indices start at 0)."
        ),
        sig="def champagne_tower(poured: int, query_row: int, query_glass: int) -> float:",
        fn="champagne_tower",
        compare="float",
        tests=[
            ((1, 1, 1), 0.0),
            ((2, 1, 1), 0.5),
            ((4, 2, 1), 0.5),
            ((5, 2, 1), 1.0),
        ],
        hints=[
            "Simulate the pouring row by row - the water that reaches a glass is all that matters.",
            (
                "If x cups reach a glass, the overflow is max(0, x - 1), and each of the two glasses below gets "
                "half of it."
            ),
            (
                "Keep only the current row's amounts (not capped at 1), build the next row from it, and finally cap "
                "the queried glass at 1."
            ),
        ],
        pattern="Row-by-row simulation (overflow DP)",
        explain=(
            "The amount arriving at a glass is the sum of half-overflows from its two parents, so each row depends "
            "only on the row above. Storing the uncapped amount lets us compute overflow exactly. We stop at the "
            "queried row. The brute force defines the same quantity recursively without remembering any glass, so "
            "it is exponential in the row number."
        ),
        cx="O(r^2) time, O(r) space (r = query_row)",
        brute_cx="exponential - recompute each parent glass on every path",
        brute=r"""
# BRUTE FORCE: exponential - recompute each parent glass on every path
def champagne_tower(poured, query_row, query_glass):
    def reaching(r, c):
        if c < 0 or c > r:
            return 0.0
        if r == 0:
            return float(poured)
        left = max(0.0, reaching(r - 1, c - 1) - 1) / 2
        right = max(0.0, reaching(r - 1, c) - 1) / 2
        return left + right

    return min(1.0, reaching(query_row, query_glass))
""",
        solution=r"""
# OPTIMISED: O(r^2) time, O(r) space (r = query_row)
# Idea: Row-by-row simulation (overflow DP)
def champagne_tower(poured, query_row, query_glass):
    row = [float(poured)]
    for _ in range(query_row):
        nxt = [0.0] * (len(row) + 1)
        for i, amount in enumerate(row):
            extra = max(0.0, (amount - 1) / 2)
            nxt[i] += extra
            nxt[i + 1] += extra
        row = nxt
    return min(1.0, row[query_glass])
""",
    ),
    # ---- Minimum Swaps To Make Sequences Increasing (LeetCode 801) ----
    dict(
        title="Minimum Swaps To Make Sequences Increasing",
        diff="H",
        lc=801,
        slug="minimum-swaps-to-make-sequences-increasing",
        prompt=(
            "nums1 and nums2 have the same length. In one move you may swap nums1[i] with nums2[i] at the SAME "
            "index. Return the minimum number of moves needed to make BOTH arrays strictly increasing (an answer "
            "always exists)."
        ),
        sig="def min_swap(nums1: List[int], nums2: List[int]) -> int:",
        fn="min_swap",
        tests=[
            (([1, 3, 5, 4], [1, 2, 3, 7]), 1),
            (([0, 3, 5, 8, 9], [2, 1, 4, 6, 9]), 1),
            (([1], [1]), 0),
            (([3, 2], [1, 4]), 1),
        ],
        hints=[
            "At each index there are only two choices: keep the pair or swap it.",
            (
                "Whether index i is kept or swapped only constrains index i + 1 through the comparison with index "
                "i's final values."
            ),
            (
                "Let keep and swap be the minimum moves for the prefix ending at i with index i kept/swapped. "
                "Extend using which of the two comparisons (a[i] > a[i-1] and b[i] > b[i-1]) or the crossed one "
                "(a[i] > b[i-1] and b[i] > a[i-1]) hold."
            ),
        ],
        pattern="Two-state DP (keep / swap) per index",
        explain=(
            "If both 'same side' and 'crossed' comparisons are true, either choice is allowed; if only the "
            "same-side one holds, the decision must repeat the previous index's decision; if only the crossed one "
            "holds, it must be the opposite. That gives two O(1) transitions per index. The brute force tries every "
            "subset of indices to swap."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(2^n * n) time - try every subset of swaps",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - try every subset of swaps
def min_swap(nums1, nums2):
    n = len(nums1)
    best = None
    for choice in itertools.product((0, 1), repeat=n):
        a = [nums2[i] if choice[i] else nums1[i] for i in range(n)]
        b = [nums1[i] if choice[i] else nums2[i] for i in range(n)]
        if all(a[i] < a[i + 1] and b[i] < b[i + 1] for i in range(n - 1)):
            if best is None or sum(choice) < best:
                best = sum(choice)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two-state DP (keep / swap) per index
def min_swap(nums1, nums2):
    inf = float("inf")
    keep, swap = 0, 1
    for i in range(1, len(nums1)):
        new_keep = new_swap = inf
        if nums1[i] > nums1[i - 1] and nums2[i] > nums2[i - 1]:
            new_keep = keep
            new_swap = swap + 1
        if nums1[i] > nums2[i - 1] and nums2[i] > nums1[i - 1]:
            new_keep = min(new_keep, swap)
            new_swap = min(new_swap, keep + 1)
        keep, swap = new_keep, new_swap
    return min(keep, swap)
""",
    ),
    # ---- Soup Servings (LeetCode 808) ----
    dict(
        title="Soup Servings",
        diff="M",
        lc=808,
        slug="soup-servings",
        prompt=(
            "You have n ml of soup A and n ml of soup B. Each turn serve, with probability 1/4 each, one of: (100 "
            "A, 0 B), (75 A, 25 B), (50 A, 50 B), (25 A, 75 B). If there is not enough soup, serve what is left. "
            "Stop when one soup runs out. Return P(A empties first) + 0.5 * P(both empty at the same time). "
            "(Answers within 1e-5 are accepted.)"
        ),
        sig="def soup_servings(n: int) -> float:",
        fn="soup_servings",
        compare="float",
        tests=[
            ((50,), 0.625),
            ((100,), 0.71875),
            ((1,), 0.625),
            ((25,), 0.625),
        ],
        hints=[
            (
                "All amounts are multiples of 25, so work in units of 25 ml: m = ceil(n / 25). The four moves "
                "become (4,0), (3,1), (2,2), (1,3)."
            ),
            (
                "Let f(a, b) be the answer with a and b units left. If both are <= 0 it is 0.5, if only a <= 0 it "
                "is 1, if only b <= 0 it is 0; otherwise it is the average of the four next states."
            ),
            (
                "Memoise f. For very large n the answer is practically 1.0 (A is used up faster), so return 1.0 "
                "once n is about 4800 or more."
            ),
        ],
        pattern="Memoised probability DP, with a large-n shortcut",
        explain=(
            "Each move uses more A than B on average, so the probability tends to 1 for large n; the error at n = "
            "4800 is below 1e-5, which makes a cut-off legal. For smaller n the states are only (m + 1)^2 pairs of "
            "units. The brute force uses the same recursion without memoisation (and without the shortcut), which "
            "is only possible for small n."
        ),
        cx="O(min(n, 4800)^2 / 625) time and space - a few hundred states at most",
        brute_cx="exponential - the recursion has no memory (fine only for small n)",
        brute=r"""
# BRUTE FORCE: exponential - the recursion has no memory (fine only for small n)
def soup_servings(n):
    def f(a, b):
        if a <= 0 and b <= 0:
            return 0.5
        if a <= 0:
            return 1.0
        if b <= 0:
            return 0.0
        return 0.25 * (f(a - 4, b) + f(a - 3, b - 1) + f(a - 2, b - 2) + f(a - 1, b - 3))

    units = (n + 24) // 25
    return f(units, units)
""",
        solution=r"""
# OPTIMISED: O(min(n, 4800)^2 / 625) time and space - a few hundred states at most
# Idea: Memoised probability DP, with a large-n shortcut
def soup_servings(n):
    if n >= 4800:
        return 1.0
    units = (n + 24) // 25

    @lru_cache(None)
    def f(a, b):
        if a <= 0 and b <= 0:
            return 0.5
        if a <= 0:
            return 1.0
        if b <= 0:
            return 0.0
        return 0.25 * (f(a - 4, b) + f(a - 3, b - 1) + f(a - 2, b - 2) + f(a - 1, b - 3))

    return f(units, units)
""",
    ),
    # ---- Largest Sum of Averages (LeetCode 813) ----
    dict(
        title="Largest Sum of Averages",
        diff="M",
        lc=813,
        slug="largest-sum-of-averages",
        prompt=(
            "Split the array nums into AT MOST k non-empty contiguous groups. The score is the sum of the AVERAGES "
            "of the groups. Return the largest score (answers within 1e-6 are accepted)."
        ),
        sig="def largest_sum_of_averages(nums: List[int], k: int) -> float:",
        fn="largest_sum_of_averages",
        compare="float",
        tests=[
            (([9, 1, 2, 3, 9], 3), 20.0),
            (([1, 2, 3, 4, 5, 6, 7], 4), 20.5),
            (([5], 1), 5.0),
            (([1, 2], 5), 3.0),
        ],
        hints=[
            "Brute force: try all ways to place the cuts. That is exponential.",
            (
                "Let dp[i] = best score for the suffix starting at i using the current number of groups. With ONE "
                "group it is the average of nums[i:]."
            ),
            (
                "To allow one more group: dp[i] = max over j > i of average(i..j-1) + dp[j]. Prefix sums give each "
                "average in O(1). Repeat k - 1 times."
            ),
        ],
        pattern="Partition DP with prefix sums",
        explain=(
            "The best split of a suffix is: choose where its first group ends, take that group's average, and add "
            "the best split of the remainder with one group fewer. Allowing 'at most' k groups is the same as "
            "exactly min(k, n) groups because all numbers are positive and splitting never lowers the sum. The "
            "brute force tries every set of cut positions."
        ),
        cx="O(k * n^2) time, O(n) space",
        brute_cx="O(2^n * n) time - every placement of cuts",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - every placement of cuts
def largest_sum_of_averages(nums, k):
    n = len(nums)
    best = 0.0
    for groups in range(1, min(k, n) + 1):
        for cuts in itertools.combinations(range(1, n), groups - 1):
            bounds = [0, *cuts, n]
            total = sum(sum(nums[a:b]) / (b - a) for a, b in zip(bounds, bounds[1:]))
            best = max(best, total)
    return best
""",
        solution=r"""
# OPTIMISED: O(k * n^2) time, O(n) space
# Idea: Partition DP with prefix sums
def largest_sum_of_averages(nums, k):
    n = len(nums)
    prefix = [0]
    for x in nums:
        prefix.append(prefix[-1] + x)

    def average(i, j):
        return (prefix[j] - prefix[i]) / (j - i)

    dp = [average(i, n) for i in range(n)]
    for _ in range(k - 1):
        for i in range(n):
            for j in range(i + 1, n):
                dp[i] = max(dp[i], average(i, j) + dp[j])
    return dp[0]
""",
    ),
    # ---- Binary Trees With Factors (LeetCode 823) ----
    dict(
        title="Binary Trees With Factors",
        diff="M",
        lc=823,
        slug="binary-trees-with-factors",
        prompt=(
            "arr holds DISTINCT integers greater than 1. You may use each number any number of times to build "
            "binary trees in which every non-leaf node's value equals the PRODUCT of its two children's values. "
            "Return the number of such trees (a tree may have any root from arr), modulo 10^9 + 7."
        ),
        sig="def num_factored_binary_trees(arr: List[int]) -> int:",
        fn="num_factored_binary_trees",
        tests=[
            (([2, 4],), 3),
            (([2, 4, 5, 10],), 7),
            (([2],), 1),
            (([3, 5],), 2),
        ],
        hints=[
            (
                "Let count(v) be the number of trees with root v. A tree is a single node, or a root v with two "
                "subtrees whose roots multiply to v."
            ),
            (
                "count(v) = 1 + sum over pairs (a, b) in arr with a * b = v of count(a) * count(b). Left and right "
                "are different, so (a, b) and (b, a) both count."
            ),
            (
                "Process the values in increasing order and store count in a dictionary - factors are always "
                "smaller than v, so they are ready. The answer is the sum of all counts."
            ),
        ],
        pattern="DP over values in increasing order",
        explain=(
            "Every factor pair splits a value v into two smaller values, so counting trees by root value from small "
            "to large reuses already computed counts. The 1 stands for the one-node tree. The brute force evaluates "
            "the same recurrence recursively, recomputing shared sub-counts again and again."
        ),
        cx="O(n^2) time, O(n) space",
        brute_cx="exponential - recompute count(v) for shared factors",
        brute=r"""
# BRUTE FORCE: exponential - recompute count(v) for shared factors
def num_factored_binary_trees(arr):
    values = set(arr)

    def count(v):
        total = 1
        for a in values:
            if v % a == 0 and v // a in values:
                total += count(a) * count(v // a)
        return total

    return sum(count(v) for v in arr) % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n) space
# Idea: DP over values in increasing order
def num_factored_binary_trees(arr):
    mod = 10**9 + 7
    ways = {}
    for v in sorted(arr):
        total = 1
        for a, ways_a in ways.items():
            if v % a == 0 and v // a in ways:
                total += ways_a * ways[v // a]
        ways[v] = total % mod
    return sum(ways.values()) % mod
""",
    ),
    # ---- New 21 Game (LeetCode 837) ----
    dict(
        title="New 21 Game",
        diff="M",
        lc=837,
        slug="new-21-game",
        prompt=(
            "Alice starts with 0 points. While she has fewer than k points she draws a random integer from 1 to "
            "max_pts (all equally likely) and adds it. She stops as soon as she has k or more points. Return the "
            "probability that she ends with n points or fewer (answers within 1e-5 are accepted)."
        ),
        sig="def new21_game(n: int, k: int, max_pts: int) -> float:",
        fn="new21_game",
        compare="float",
        tests=[
            ((10, 1, 10), 1.0),
            ((6, 1, 10), 0.6),
            ((1, 1, 2), 0.5),
            ((1, 0, 1), 1.0),
        ],
        hints=[
            "Let dp[x] be the probability that Alice's score ever equals exactly x. dp[0] = 1.",
            (
                "dp[x] = (sum of dp[y] for y in [x - max_pts, x - 1], restricted to y < k) / max_pts - you can only "
                "draw from a score below k."
            ),
            (
                "Keep that sum as a sliding window. The answer is the sum of dp[x] for k <= x <= n. If k == 0 or n "
                "is already at least k + max_pts - 1, the answer is 1."
            ),
        ],
        pattern="Probability DP with a sliding-window sum",
        explain=(
            "A final score x >= k is reached from a score y < k that is within max_pts below x, each draw having "
            "probability 1/max_pts. The window sum of the last max_pts reachable dp values (only those still below "
            "k) makes each step O(1). The brute force writes the probability recursively over the score and "
            "averages max_pts children each time."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="exponential - recursion over scores with no memory",
        brute=r"""
# BRUTE FORCE: exponential - recursion over scores with no memory
def new21_game(n, k, max_pts):
    def f(points):
        if points >= k:
            return 1.0 if points <= n else 0.0
        return sum(f(points + draw) for draw in range(1, max_pts + 1)) / max_pts

    return f(0)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Probability DP with a sliding-window sum
def new21_game(n, k, max_pts):
    if k == 0 or n >= k + max_pts - 1:
        return 1.0
    dp = [0.0] * (n + 1)
    dp[0] = 1.0
    window = 1.0
    answer = 0.0
    for i in range(1, n + 1):
        dp[i] = window / max_pts
        if i < k:
            window += dp[i]
        else:
            answer += dp[i]
        if i - max_pts >= 0:
            window -= dp[i - max_pts]
    return answer
""",
    ),
    # ---- Flip String to Monotone Increasing (LeetCode 926) ----
    dict(
        title="Flip String to Monotone Increasing",
        diff="M",
        lc=926,
        slug="flip-string-to-monotone-increasing",
        prompt=(
            "A binary string is MONOTONE INCREASING if it is some 0s followed by some 1s (either part may be "
            "empty). In one move you can flip any single character. Return the minimum number of flips to make s "
            "monotone increasing."
        ),
        sig="def min_flips_mono_incr(s: str) -> int:",
        fn="min_flips_mono_incr",
        tests=[
            (("00110",), 1),
            (("010110",), 2),
            (("00011000",), 2),
            (("1",), 0),
        ],
        hints=[
            "A final string is determined by a split point: everything before it is 0, everything after it is 1.",
            (
                "For a split, flips = (number of 1s before it) + (number of 0s after it). Try every split (O(n^2)), "
                "then speed it up with prefix counts."
            ),
            (
                "One pass: count the 1s seen so far; on a '0' the best cost is min(flips + 1 (flip this 0 to 1), "
                "ones (flip all earlier 1s to 0))."
            ),
        ],
        pattern="Split-point DP in one pass",
        explain=(
            "flips[i] is the cheapest way to make the prefix ending at i monotone. A '1' never adds cost because it "
            "may stay as the start of the 1-block. A '0' either gets flipped to 1 (flips + 1, extending the "
            "previous solution) or all the earlier 1s are flipped to 0 (cost ones). The brute force evaluates each "
            "split point separately."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - count the cost of every split point",
        brute=r"""
# BRUTE FORCE: O(n^2) time - count the cost of every split point
def min_flips_mono_incr(s):
    n = len(s)
    return min(s[:split].count("1") + s[split:].count("0") for split in range(n + 1))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Split-point DP in one pass
def min_flips_mono_incr(s):
    ones = 0
    flips = 0
    for ch in s:
        if ch == "1":
            ones += 1
        else:
            flips = min(flips + 1, ones)
    return flips
""",
    ),
    # ---- Knight Dialer (LeetCode 935) ----
    dict(
        title="Knight Dialer",
        diff="M",
        lc=935,
        slug="knight-dialer",
        prompt=(
            "A chess knight is placed on a phone keypad (digits 0-9 in the usual 4x3 layout, with '*' and '#' "
            "unusable). It can stand on any digit first, then make n - 1 knight moves, and the digits it visits "
            "form a phone number of length n. Return how many distinct numbers of length n it can dial, modulo 10^9 "
            "+ 7."
        ),
        sig="def knight_dialer(n: int) -> int:",
        fn="knight_dialer",
        tests=[
            ((1,), 10),
            ((2,), 20),
            ((3,), 46),
            ((4,), 104),
        ],
        hints=[
            (
                "From each digit there is a fixed list of digits a knight can jump to (for example from 4: 0, 3, 9; "
                "from 5: none)."
            ),
            (
                "Let ways[d] = number of numbers of the current length that end at digit d. For length 1 every "
                "digit has 1."
            ),
            (
                "To go to the next length: new[to] += ways[from] for every knight move from -> to. Do this n - 1 "
                "times and sum."
            ),
        ],
        pattern="Graph-walk counting DP (rolling array)",
        explain=(
            "A number is a walk on the 'knight graph' of the keypad, and the count of walks of length n is obtained "
            "by pushing counts along the edges one step at a time. Only 10 counts are stored. The brute force "
            "follows every walk recursively, which has exponentially many branches."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="exponential - follow every walk",
        brute=r"""
# BRUTE FORCE: exponential - follow every walk
def knight_dialer(n):
    moves = {
        0: (4, 6),
        1: (6, 8),
        2: (7, 9),
        3: (4, 8),
        4: (0, 3, 9),
        5: (),
        6: (0, 1, 7),
        7: (2, 6),
        8: (1, 3),
        9: (2, 4),
    }

    def walks(digit, left):
        if left == 1:
            return 1
        return sum(walks(nxt, left - 1) for nxt in moves[digit])

    return sum(walks(d, n) for d in range(10)) % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Graph-walk counting DP (rolling array)
def knight_dialer(n):
    mod = 10**9 + 7
    moves = {
        0: (4, 6),
        1: (6, 8),
        2: (7, 9),
        3: (4, 8),
        4: (0, 3, 9),
        5: (),
        6: (0, 1, 7),
        7: (2, 6),
        8: (1, 3),
        9: (2, 4),
    }
    ways = [1] * 10
    for _ in range(n - 1):
        new = [0] * 10
        for digit, count in enumerate(ways):
            for nxt in moves[digit]:
                new[nxt] = (new[nxt] + count) % mod
        ways = new
    return sum(ways) % mod
""",
    ),
    # ---- Distinct Subsequences II (LeetCode 940) ----
    dict(
        title="Distinct Subsequences II",
        diff="H",
        lc=940,
        slug="distinct-subsequences-ii",
        prompt=(
            "Given a string s, return the number of DISTINCT non-empty subsequences of s, modulo 10^9 + 7. (A "
            "subsequence keeps the relative order of some characters; two subsequences are the same if they are "
            "equal as strings.)"
        ),
        sig="def distinct_subseq_ii(s: str) -> int:",
        fn="distinct_subseq_ii",
        tests=[
            (("abc",), 7),
            (("aba",), 6),
            (("aaa",), 3),
            (("a",), 1),
        ],
        hints=[
            "Brute force: put every subsequence in a set. That is 2^n subsets.",
            (
                "Let ends[c] = number of distinct subsequences that END with letter c. A new character c can be "
                "appended to every distinct subsequence so far, or stand alone."
            ),
            (
                "On reading c: ends[c] = (sum of all ends) + 1. This REPLACES the old ends[c] because the old ones "
                "are included in the new set. The answer is sum(ends)."
            ),
        ],
        pattern="DP: count distinct subsequences by last letter",
        explain=(
            "Appending c to every distinct subsequence so far (plus the single letter c) gives all distinct "
            "subsequences that end with c at this point. This set contains the earlier subsequences ending with c, "
            "so we overwrite rather than add, which is what removes duplicates. The brute force builds all "
            "subsequences and keeps them in a set."
        ),
        cx="O(26 n) time (O(n) with a running total), O(26) space",
        brute_cx="O(2^n * n) time - every subsequence stored in a set",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - every subsequence stored in a set
def distinct_subseq_ii(s):
    found = set()
    n = len(s)
    for mask in range(1, 1 << n):
        found.add("".join(s[i] for i in range(n) if mask >> i & 1))
    return len(found) % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(26 n) time (O(n) with a running total), O(26) space
# Idea: DP: count distinct subsequences by last letter
def distinct_subseq_ii(s):
    mod = 10**9 + 7
    ends = [0] * 26
    for ch in s:
        ends[ord(ch) - 97] = (sum(ends) + 1) % mod
    return sum(ends) % mod
""",
    ),
    # ---- Last Stone Weight II (LeetCode 1049) ----
    dict(
        title="Last Stone Weight II",
        diff="M",
        lc=1049,
        slug="last-stone-weight-ii",
        prompt=(
            "You have stones with given weights. Each turn pick any two stones x <= y and smash them: if x == y "
            "both vanish, otherwise the stone y - x remains. After all turns at most one stone is left. Return the "
            "smallest possible weight of the last stone (0 if none is left)."
        ),
        sig="def last_stone_weight_ii(stones: List[int]) -> int:",
        fn="last_stone_weight_ii",
        tests=[
            (([2, 7, 4, 1, 8, 1],), 1),
            (([31, 26, 33, 21, 40],), 5),
            (([1],), 1),
            (([1, 1],), 0),
        ],
        hints=[
            (
                "Whatever you do, the final stone equals a sum of stones with plus signs minus the sum of the "
                "others (each stone ends up with a + or a - sign)."
            ),
            (
                "So the task is to split the stones into two groups whose sums are as CLOSE as possible; the answer "
                "is the difference."
            ),
            (
                "That is subset sum: find the largest reachable subset sum not exceeding total / 2 using a boolean "
                "knapsack; answer = total - 2 * best."
            ),
        ],
        pattern="Subset-sum knapsack (partition into two near-equal halves)",
        explain=(
            "Smashing stones builds an expression of +/- signs over the weights, and every sign assignment is "
            "possible. The smallest absolute value is the smallest gap between two group sums. A boolean knapsack "
            "up to half the total finds the best achievable smaller group. The brute force tries every sign "
            "assignment."
        ),
        cx="O(n * total) time, O(total) space",
        brute_cx="O(2^n * n) time - every sign assignment",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - every sign assignment
def last_stone_weight_ii(stones):
    best = None
    for signs in itertools.product((1, -1), repeat=len(stones)):
        value = abs(sum(s * w for s, w in zip(signs, stones)))
        if best is None or value < best:
            best = value
    return best
""",
        solution=r"""
# OPTIMISED: O(n * total) time, O(total) space
# Idea: Subset-sum knapsack (partition into two near-equal halves)
def last_stone_weight_ii(stones):
    total = sum(stones)
    half = total // 2
    reachable = [False] * (half + 1)
    reachable[0] = True
    for w in stones:
        for t in range(half, w - 1, -1):
            if reachable[t - w]:
                reachable[t] = True
    best = max(t for t in range(half + 1) if reachable[t])
    return total - 2 * best
""",
    ),
    # ---- Filling Bookcase Shelves (LeetCode 1105) ----
    dict(
        title="Filling Bookcase Shelves",
        diff="M",
        lc=1105,
        slug="filling-bookcase-shelves",
        prompt=(
            "books[i] = [thickness, height]. Place the books IN ORDER on shelves of total width shelf_width: each "
            "shelf holds a consecutive group of books whose thicknesses add up to at most shelf_width, and a shelf "
            "is as tall as its tallest book. Return the minimum possible total height of all shelves."
        ),
        sig="def min_height_shelves(books: List[List[int]], shelf_width: int) -> int:",
        fn="min_height_shelves",
        tests=[
            (([[1, 1], [2, 3], [2, 3], [1, 1], [1, 1], [1, 1], [1, 2]], 4), 6),
            (([[1, 3], [2, 4], [3, 2]], 6), 4),
            (([[5, 5]], 5), 5),
            (([[1, 1], [1, 1]], 1), 2),
        ],
        hints=[
            (
                "Because the order is fixed, the problem is: where do the shelves end? A shelf is a consecutive "
                "block of books."
            ),
            "Let dp[i] = minimum height for the first i books. The LAST shelf holds books j..i for some j.",
            (
                "dp[i] = min over valid j of dp[j - 1] + (max height among books j..i). Extend j backwards while "
                "the width still fits, updating the max height as you go."
            ),
        ],
        pattern="Partition DP (where does the last shelf start?)",
        explain=(
            "The optimal arrangement of the first i books ends with some last shelf. Whatever is below it must "
            "itself be optimal for the remaining prefix, so dp[i] = min over feasible last shelves of dp[start - 1] "
            "+ shelf height. Scanning the start backwards keeps the thickness sum and tallest height incremental. "
            "The brute force tries every sequence of shelf endings recursively."
        ),
        cx="O(n * w) time, O(n) space (inner loop stops when the shelf is full)",
        brute_cx="exponential - every way of cutting the books into shelves",
        brute=r"""
# BRUTE FORCE: exponential - every way of cutting the books into shelves
def min_height_shelves(books, shelf_width):
    n = len(books)

    def best(i):
        if i == n:
            return 0
        result = float("inf")
        width = height = 0
        for j in range(i, n):
            width += books[j][0]
            if width > shelf_width:
                break
            height = max(height, books[j][1])
            result = min(result, height + best(j + 1))
        return result

    return best(0)
""",
        solution=r"""
# OPTIMISED: O(n * w) time, O(n) space (inner loop stops when the shelf is full)
# Idea: Partition DP (where does the last shelf start?)
def min_height_shelves(books, shelf_width):
    n = len(books)
    dp = [0] + [float("inf")] * n
    for i in range(1, n + 1):
        width = height = 0
        for j in range(i, 0, -1):
            width += books[j - 1][0]
            if width > shelf_width:
                break
            height = max(height, books[j - 1][1])
            dp[i] = min(dp[i], dp[j - 1] + height)
    return dp[n]
""",
    ),
    # ---- Count Vowels Permutation (LeetCode 1220) ----
    dict(
        title="Count Vowels Permutation",
        diff="H",
        lc=1220,
        slug="count-vowels-permutation",
        prompt=(
            "Count the strings of length n made only of the vowels a, e, i, o, u such that: 'a' may only be "
            "followed by 'e'; 'e' only by 'a' or 'i'; 'i' by anything EXCEPT 'i'; 'o' only by 'i' or 'u'; 'u' only "
            "by 'a'. Return the count modulo 10^9 + 7."
        ),
        sig="def count_vowel_permutation(n: int) -> int:",
        fn="count_vowel_permutation",
        tests=[
            ((1,), 5),
            ((2,), 10),
            ((3,), 19),
            ((5,), 68),
        ],
        hints=[
            "Only the last vowel matters for what can come next.",
            (
                "Let ways[v] = number of valid strings of the current length that end with vowel v. For length 1 "
                "each is 1."
            ),
            (
                "Appending a new vowel x is allowed after any y that may be followed by x. E.g. a is allowed after "
                "e, i, u. Update all five counts together for n - 1 steps."
            ),
        ],
        pattern="State-machine counting DP",
        explain=(
            "The rules form a small directed graph on the five vowels; a valid string is a walk in that graph. We "
            "keep one count per ending vowel and push it to the vowels allowed next, n - 1 times. The brute force "
            "extends strings letter by letter following the same follow-rules, so it enumerates every valid string."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(5 * 2^n)-ish time - enumerate every valid string",
        brute=r"""
# BRUTE FORCE: O(5 * 2^n)-ish time - enumerate every valid string
def count_vowel_permutation(n):
    follows = {"a": "e", "e": "ai", "i": "aeou", "o": "iu", "u": "a"}

    def extend(last, left):
        if left == 1:
            return 1
        return sum(extend(nxt, left - 1) for nxt in follows[last])

    return sum(extend(v, n) for v in "aeiou") % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: State-machine counting DP
def count_vowel_permutation(n):
    mod = 10**9 + 7
    a = e = i = o = u = 1
    for _ in range(n - 1):
        a, e, i, o, u = (e + i + u) % mod, (a + i) % mod, (e + o) % mod, i, (i + o) % mod
    return (a + e + i + o + u) % mod
""",
    ),
    # ---- Count Sorted Vowel Strings (LeetCode 1641) ----
    dict(
        title="Count Sorted Vowel Strings",
        diff="M",
        lc=1641,
        slug="count-sorted-vowel-strings",
        prompt=(
            "Return the number of strings of length n made of the vowels a, e, i, o, u that are LEXICOGRAPHICALLY "
            "SORTED (each letter is the same as or comes after the previous one, e.g. 'aeiou', 'aaee')."
        ),
        sig="def count_vowel_strings(n: int) -> int:",
        fn="count_vowel_strings",
        tests=[
            ((1,), 5),
            ((2,), 15),
            ((3,), 35),
            ((4,), 70),
        ],
        hints=[
            "A sorted string is fully described by HOW MANY of each vowel it contains.",
            (
                "Let ways[v] = number of sorted strings of the current length ending with vowel v. A string ending "
                "in v can be extended by any vowel >= v, i.e. ways[v] = sum of ways[u] for u <= v from the previous "
                "length."
            ),
            (
                "So each step is a prefix sum over the five counts. After n - 1 steps, sum the five counts. (It "
                "also equals C(n + 4, 4).)"
            ),
        ],
        pattern="Prefix-sum DP / stars and bars",
        explain=(
            "Sorted strings correspond to choosing how many times each of the five vowels appears, which counts as "
            "combinations with repetition. The DP gets there by pushing counts to vowels that are not smaller. The "
            "brute force enumerates all multisets of size n with itertools.combinations_with_replacement."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(C(n + 4, 4)) time - generate every sorted string",
        brute=r"""
# BRUTE FORCE: O(C(n + 4, 4)) time - generate every sorted string
def count_vowel_strings(n):
    return sum(1 for _ in itertools.combinations_with_replacement("aeiou", n))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Prefix-sum DP / stars and bars
def count_vowel_strings(n):
    counts = [1] * 5
    for _ in range(n - 1):
        for i in range(1, 5):
            counts[i] += counts[i - 1]
    return sum(counts)
""",
    ),
]
