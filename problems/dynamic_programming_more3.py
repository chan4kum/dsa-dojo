"""more Dynamic Programming problems (batch 4) - part of the problem bank for the "dynamic_programming" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Integer Break (LeetCode 343) ----
    dict(
        title="Integer Break",
        diff="M",
        lc=343,
        slug="integer-break",
        prompt=(
            "Split n (n >= 2) into at least two positive integers so that their product is as large as possible. "
            "Return that product."
        ),
        sig="def integer_break(n: int) -> int:",
        fn="integer_break",
        tests=[
            ((2,), 1),
            ((3,), 2),
            ((4,), 4),
            ((10,), 36),
            ((8,), 18),
            ((12,), 81),
        ],
        hints=[
            "Try small n by hand: 4 -> 2*2, 5 -> 2*3, 6 -> 3*3, 7 -> 3*4, 8 -> 3*3*2.",
            (
                "DP view: best(n) = max over i of i * max(n - i, best(n - i)) - either keep the rest whole or split "
                "it further."
            ),
            (
                "Pattern: use as many 3s as possible, never a 1, and a leftover of 4 stays as 2*2 (remainder 1 -> "
                "turn 3+1 into 2+2)."
            ),
        ],
        pattern="DP first, then spot the math pattern (split into 3s)",
        explain=(
            "A 3 gives the best 'product per unit of sum' (3^(1/3) beats 2^(1/2) and 4^(1/4) ties with 2s). So "
            "greedily peel 3s; when the remainder is 1, borrow one 3 and make 2*2 instead of 3*1; when it is 2, "
            "multiply by 2."
        ),
        cx="O(n) time (the 3s loop) or O(log n) with fast power, O(1) space",
        brute_cx="O(2^n) time - plain recursion over every first piece",
        brute=r"""
# BRUTE FORCE: O(2^n) time - plain recursion over every first piece
def integer_break(n):
    def best(
        m,
    ):  # best product when splitting m into one or more pieces (m itself is allowed as a piece)
        result = m
        for i in range(1, m):
            result = max(result, i * best(m - i))
        return result

    return max(
        i * best(n - i) for i in range(1, n)
    )  # at least two pieces: a first piece i, the rest anything
""",
        solution=r"""
# OPTIMISED: O(n) time (the 3s loop) or O(log n) with fast power, O(1) space
# Idea: DP first, then spot the math pattern (split into 3s)
def integer_break(n):
    if n <= 3:
        return n - 1  # 2 -> 1*1, 3 -> 1*2

    threes, rest = divmod(n, 3)

    if rest == 0:
        return 3**threes

    if rest == 1:
        return 3 ** (threes - 1) * 4  # replace 3 + 1 by 2 + 2

    return 3**threes * 2
""",
    ),
    # ---- Arithmetic Slices (LeetCode 413) ----
    dict(
        title="Arithmetic Slices",
        diff="M",
        lc=413,
        slug="arithmetic-slices",
        prompt="Count the contiguous subarrays of length >= 3 whose consecutive differences are all equal.",
        sig="def number_of_arithmetic_slices(nums: List[int]) -> int:",
        fn="number_of_arithmetic_slices",
        tests=[
            (([1, 2, 3, 4],), 3),
            (([1],), 0),
            (([1, 2, 3, 8, 9, 10],), 2),
            (([1, 3, 5, 7, 9],), 6),
            (([1, 2],), 0),
        ],
        hints=[
            "Let cur = number of arithmetic slices that END at index i.",
            (
                "If nums[i] - nums[i-1] == nums[i-1] - nums[i-2], every slice ending at i-1 extends by one, plus "
                "one brand-new slice of length 3: cur = cur + 1."
            ),
            "Otherwise cur = 0. Add cur to a running total at every step.",
        ],
        pattern="Count subarrays by the number ending at each index (1-D DP)",
        explain=(
            "A run of m equally-spaced numbers hides 1 + 2 + ... + (m-2) slices. Counting slices ending at each "
            "index builds exactly that sum without looking at any subarray twice."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^3) time - test every subarray",
        brute=r"""
# BRUTE FORCE: O(n^3) time - test every subarray
def number_of_arithmetic_slices(nums):
    count = 0
    for i in range(len(nums)):
        for j in range(i + 2, len(nums)):  # nums[i..j] has length >= 3
            diffs = {nums[k + 1] - nums[k] for k in range(i, j)}
            if len(diffs) == 1:
                count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Count subarrays by the number ending at each index (1-D DP)
def number_of_arithmetic_slices(nums):
    total = ending_here = 0

    for i in range(2, len(nums)):
        if nums[i] - nums[i - 1] == nums[i - 1] - nums[i - 2]:
            ending_here += 1  # extend every slice ending at i-1, plus one new 3-slice
            total += ending_here
        else:
            ending_here = 0

    return total
""",
    ),
    # ---- Predict the Winner (LeetCode 486) ----
    dict(
        title="Predict the Winner",
        diff="M",
        lc=486,
        slug="predict-the-winner",
        prompt=(
            "Two players alternately take a number from either END of nums; both play optimally. Return True if "
            "player 1 ends with a score >= player 2's."
        ),
        sig="def predict_the_winner(nums: List[int]) -> bool:",
        fn="predict_the_winner",
        tests=[
            (([1, 5, 2],), False),
            (([1, 5, 233, 7],), True),
            (([1],), True),
            (([2, 4, 55, 6, 8],), False),
        ],
        hints=[
            "Track the DIFFERENCE (my score - opponent score) instead of two scores.",
            "dp[i][j] = the best difference the player to move can get from nums[i..j].",
            "dp[i][j] = max(nums[i] - dp[i+1][j], nums[j] - dp[i][j-1]). Player 1 wins if dp[0][n-1] >= 0.",
        ],
        pattern="Interval DP on a score difference (minimax)",
        explain=(
            "Whatever the opponent gains from the remaining numbers is lost by me, so my best value from taking an "
            "end is that number minus the opponent's best difference on what is left. This collapses minimax to a "
            "single table."
        ),
        cx="O(n^2) time, O(n^2) space",
        brute_cx="O(2^n) time - plain minimax recursion",
        brute=r"""
# BRUTE FORCE: O(2^n) time - plain minimax recursion
def predict_the_winner(nums):
    def diff(i, j):  # best (mover - opponent) score from nums[i..j]
        if i == j:
            return nums[i]
        return max(nums[i] - diff(i + 1, j), nums[j] - diff(i, j - 1))

    return diff(0, len(nums) - 1) >= 0
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n^2) space
# Idea: Interval DP on a score difference (minimax)
def predict_the_winner(nums):
    n = len(nums)
    dp = [[0] * n for _ in range(n)]

    for i in range(n):
        dp[i][i] = nums[i]

    for length in range(2, n + 1):  # shorter intervals first
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(nums[i] - dp[i + 1][j], nums[j] - dp[i][j - 1])

    return dp[0][n - 1] >= 0
""",
    ),
    # ---- Delete Operation for Two Strings (LeetCode 583) ----
    dict(
        title="Delete Operation for Two Strings",
        diff="M",
        lc=583,
        slug="delete-operation-for-two-strings",
        prompt=(
            "Return the minimum number of single-character deletions (from either string) needed to make word1 and "
            "word2 equal."
        ),
        sig="def min_distance(word1: str, word2: str) -> int:",
        fn="min_distance",
        tests=[
            (("sea", "eat"), 2),
            (("leetcode", "etco"), 4),
            (("a", "a"), 0),
            (("abc", ""), 3),
            (("", ""), 0),
        ],
        hints=[
            "What is left after deleting must be a common subsequence of both strings.",
            "To delete as little as possible, keep the LONGEST common subsequence.",
            "Answer = len(word1) + len(word2) - 2 * LCS.",
        ],
        pattern="Reduce to Longest Common Subsequence",
        explain=(
            "Every deletion removes a character that is not in the common subsequence we keep. Maximising the kept "
            "characters (the LCS) minimises the deletions."
        ),
        cx="O(m*n) time, O(n) space",
        brute_cx="O(2^(m+n)) time - recursion on the first characters",
        brute=r"""
# BRUTE FORCE: O(2^(m+n)) time - recursion on the first characters
def min_distance(word1, word2):
    def solve(i, j):  # deletions needed for word1[i:] and word2[j:]
        if i == len(word1):
            return len(word2) - j
        if j == len(word2):
            return len(word1) - i
        if word1[i] == word2[j]:
            return solve(i + 1, j + 1)  # keep the matching pair
        return 1 + min(solve(i + 1, j), solve(i, j + 1))  # delete from one side

    return solve(0, 0)
""",
        solution=r"""
# OPTIMISED: O(m*n) time, O(n) space
# Idea: Reduce to Longest Common Subsequence
def min_distance(word1, word2):
    n = len(word2)
    prev = [0] * (n + 1)  # LCS lengths for the previous row

    for ch in word1:
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if ch == word2[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur

    return len(word1) + len(word2) - 2 * prev[n]
""",
    ),
    # ---- Maximum Length of Repeated Subarray (LeetCode 718) ----
    dict(
        title="Maximum Length of Repeated Subarray",
        diff="M",
        lc=718,
        slug="maximum-length-of-repeated-subarray",
        prompt="Return the length of the longest CONTIGUOUS subarray that appears in both nums1 and nums2.",
        sig="def find_length(nums1: List[int], nums2: List[int]) -> int:",
        fn="find_length",
        tests=[
            (([1, 2, 3, 2, 1], [3, 2, 1, 4, 7]), 3),
            (([0, 0, 0, 0, 0], [0, 0, 0, 0, 0]), 5),
            (([1], [2]), 0),
            (([1, 2], [2, 1]), 1),
        ],
        hints=[
            "This is the longest common SUBSTRING, not subsequence - matches must be contiguous.",
            "Let dp[i][j] = length of the common run ending at nums1[i-1] and nums2[j-1].",
            "If the two numbers match dp[i][j] = dp[i-1][j-1] + 1, otherwise 0. The answer is the maximum cell.",
        ],
        pattern="2-D DP where a mismatch resets to 0 (longest common substring)",
        explain=(
            "Unlike LCS, a mismatch ends the run, so there is no max(left, up) - just 0. Only the previous row is "
            "needed, so space can be O(n)."
        ),
        cx="O(m*n) time, O(n) space",
        brute_cx="O(m*n*min(m, n)) time - extend every pair of start positions",
        brute=r"""
# BRUTE FORCE: O(m*n*min(m, n)) time - extend every pair of start positions
def find_length(nums1, nums2):
    best = 0

    for i in range(len(nums1)):
        for j in range(len(nums2)):
            k = 0
            while i + k < len(nums1) and j + k < len(nums2) and nums1[i + k] == nums2[j + k]:
                k += 1  # extend the match as far as it goes
            best = max(best, k)

    return best
""",
        solution=r"""
# OPTIMISED: O(m*n) time, O(n) space
# Idea: 2-D DP where a mismatch resets to 0 (longest common substring)
def find_length(nums1, nums2):
    best, n = 0, len(nums2)
    prev = [0] * (n + 1)

    for a in nums1:
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if a == nums2[j - 1]:
                cur[j] = prev[j - 1] + 1  # extend the run on the diagonal
                best = max(best, cur[j])
        prev = cur

    return best
""",
    ),
    # ---- Stone Game (LeetCode 877) ----
    dict(
        title="Stone Game",
        diff="M",
        lc=877,
        slug="stone-game",
        prompt=(
            "piles has an EVEN length and an ODD total. Alice and Bob alternately take a pile from either end "
            "(Alice first), both optimally. Return True if Alice wins."
        ),
        sig="def stone_game(piles: List[int]) -> bool:",
        fn="stone_game",
        tests=[
            (([5, 3, 4, 5],), True),
            (([3, 7, 2, 3],), True),
            (([1, 2],), True),
            (([2, 1, 9, 6],), True),
        ],
        hints=[
            "First solve it honestly with interval DP on the score difference (like Predict the Winner).",
            (
                "Colour the piles by position: even indices and odd indices. Alice can choose to take ALL the "
                "even-indexed piles or ALL the odd-indexed ones."
            ),
            (
                "Because the total is odd, one colour has strictly more stones - so Alice, who picks the colour, "
                "always wins."
            ),
        ],
        pattern="Interval DP, then a parity / strategy-stealing insight",
        explain=(
            "Taking an end pile first lets Alice decide whether Bob will be forced onto the even or odd positions "
            "for the whole game. She picks the richer parity, so the answer is always True."
        ),
        cx="O(1) time",
        brute_cx="O(n^2) time - interval DP on the score difference",
        brute=r"""
# BRUTE FORCE: O(n^2) time - interval DP on the score difference
def stone_game(piles):
    n = len(piles)
    dp = [[0] * n for _ in range(n)]  # dp[i][j] = best (mover - opponent) from piles[i..j]

    for i in range(n):
        dp[i][i] = piles[i]

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = max(piles[i] - dp[i + 1][j], piles[j] - dp[i][j - 1])

    return dp[0][n - 1] > 0
""",
        solution=r"""
# OPTIMISED: O(1) time
# Idea: Interval DP, then a parity / strategy-stealing insight
def stone_game(piles):
    return True  # Alice can always claim the richer of the even- or odd-indexed piles
""",
    ),
    # ---- Is Subsequence (LeetCode 392) ----
    dict(
        title="Is Subsequence",
        diff="E",
        lc=392,
        slug="is-subsequence",
        prompt=(
            "Return True if s is a subsequence of t (s can be obtained by deleting some characters of t without "
            "reordering)."
        ),
        sig="def is_subsequence(s: str, t: str) -> bool:",
        fn="is_subsequence",
        tests=[
            (("abc", "ahbgdc"), True),
            (("axc", "ahbgdc"), False),
            (("", "ahbgdc"), True),
            (("a", ""), False),
        ],
        hints=[
            "Walk through t once; you only need to remember how many characters of s you have matched.",
            "Keep a pointer i into s. When t[j] == s[i], advance i.",
            "s is a subsequence exactly when i reaches len(s).",
        ],
        pattern="Two pointers (greedy matching)",
        explain=(
            "Matching each character of s at its earliest possible position in t can never hurt later matches, so "
            "the greedy scan is correct."
        ),
        cx="O(len(t)) time, O(1) space",
        brute_cx="O(2^len(t)) time - recursion that tries to keep or skip each character of t",
        brute=r"""
# BRUTE FORCE: O(2^len(t)) time - recursion that tries to keep or skip each character of t
def is_subsequence(s, t):
    def solve(i, j):  # can s[i:] be found inside t[j:]?
        if i == len(s):
            return True
        if j == len(t):
            return False
        if s[i] == t[j] and solve(i + 1, j + 1):
            return True
        return solve(i, j + 1)  # skip t[j]

    return solve(0, 0)
""",
        solution=r"""
# OPTIMISED: O(len(t)) time, O(1) space
# Idea: Two pointers (greedy matching)
def is_subsequence(s, t):
    i = 0
    for ch in t:
        if i < len(s) and ch == s[i]:
            i += 1  # matched one more character of s
    return i == len(s)
""",
    ),
    # ---- Uncrossed Lines (LeetCode 1035) ----
    dict(
        title="Uncrossed Lines",
        diff="M",
        lc=1035,
        slug="uncrossed-lines",
        prompt=(
            "Write nums1 and nums2 on two rows. Draw lines between equal numbers so that no two lines cross and "
            "each number is used at most once. Return the maximum number of lines."
        ),
        sig="def max_uncrossed_lines(nums1: List[int], nums2: List[int]) -> int:",
        fn="max_uncrossed_lines",
        tests=[
            (([1, 4, 2], [1, 2, 4]), 2),
            (([2, 5, 1, 2, 5], [10, 5, 2, 1, 5, 2]), 3),
            (([1, 3, 7, 1, 7, 5], [1, 9, 2, 5, 1]), 2),
            (([1], [2]), 0),
        ],
        hints=[
            "Non-crossing means the matched positions keep the same order in both rows.",
            "That is exactly a common subsequence.",
            (
                "Compute the Longest Common Subsequence with the 2-D table: equal -> diagonal + 1, otherwise "
                "max(up, left)."
            ),
        ],
        pattern="Disguised Longest Common Subsequence",
        explain=(
            "Lines that never cross pair elements in increasing order on both rows - the definition of a common "
            "subsequence. The picture is just LCS in a costume."
        ),
        cx="O(m*n) time, O(n) space",
        brute_cx="O(2^(m+n)) time - recursion on the first elements",
        brute=r"""
# BRUTE FORCE: O(2^(m+n)) time - recursion on the first elements
def max_uncrossed_lines(nums1, nums2):
    def solve(i, j):
        if i == len(nums1) or j == len(nums2):
            return 0
        if nums1[i] == nums2[j]:
            return 1 + solve(i + 1, j + 1)  # draw the line
        return max(solve(i + 1, j), solve(i, j + 1))  # skip one number

    return solve(0, 0)
""",
        solution=r"""
# OPTIMISED: O(m*n) time, O(n) space
# Idea: Disguised Longest Common Subsequence
def max_uncrossed_lines(nums1, nums2):
    n = len(nums2)
    prev = [0] * (n + 1)

    for a in nums1:
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if a == nums2[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur

    return prev[n]
""",
    ),
    # ---- Minimum Insertion Steps to Make a String Palindrome (LeetCode 1312) ----
    dict(
        title="Minimum Insertion Steps to Make a String Palindrome",
        diff="H",
        lc=1312,
        slug="minimum-insertion-steps-to-make-a-string-palindrome",
        prompt=(
            "You may insert any character at any position of s. Return the minimum number of insertions that makes "
            "s a palindrome."
        ),
        sig="def min_insertions(s: str) -> int:",
        fn="min_insertions",
        tests=[
            (("zzazz",), 0),
            (("mbadm",), 2),
            (("leetcode",), 5),
            (("a",), 0),
            (("ab",), 1),
        ],
        hints=[
            "Characters that already sit in a palindromic subsequence need no partner.",
            "Every other character needs ONE inserted mirror image.",
            "Answer = len(s) - (longest palindromic subsequence). The LPS equals LCS(s, reversed s).",
        ],
        pattern="Longest Palindromic Subsequence via LCS with the reverse",
        explain=(
            "If the longest palindromic subsequence has length p, the other n - p characters each need one "
            "insertion to be mirrored; fewer is impossible because then a longer palindromic subsequence would "
            "exist."
        ),
        cx="O(n^2) time, O(n) space",
        brute_cx="O(2^n) time - recursion that compares the two ends",
        brute=r"""
# BRUTE FORCE: O(2^n) time - recursion that compares the two ends
def min_insertions(s):
    def solve(i, j):  # insertions to make s[i..j] a palindrome
        if i >= j:
            return 0
        if s[i] == s[j]:
            return solve(i + 1, j - 1)
        return 1 + min(solve(i + 1, j), solve(i, j - 1))  # mirror one of the two ends

    return solve(0, len(s) - 1)
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n) space
# Idea: Longest Palindromic Subsequence via LCS with the reverse
def min_insertions(s):
    t, n = s[::-1], len(s)
    prev = [0] * (n + 1)

    for ch in s:  # LCS(s, reverse(s)) = longest palindromic subsequence
        cur = [0] * (n + 1)
        for j in range(1, n + 1):
            if ch == t[j - 1]:
                cur[j] = prev[j - 1] + 1
            else:
                cur[j] = max(prev[j], cur[j - 1])
        prev = cur

    return n - prev[n]
""",
    ),
    # ---- Number of Dice Rolls With Target Sum (LeetCode 1155) ----
    dict(
        title="Number of Dice Rolls With Target Sum",
        diff="M",
        lc=1155,
        slug="number-of-dice-rolls-with-target-sum",
        prompt=(
            "Roll n dice, each with faces 1..k. Return the number of ways the faces add up to target, modulo "
            "1_000_000_007."
        ),
        sig="def num_rolls_to_target(n: int, k: int, target: int) -> int:",
        fn="num_rolls_to_target",
        tests=[
            ((1, 6, 3), 1),
            ((2, 6, 7), 6),
            ((30, 30, 500), 222616187),
            ((1, 2, 3), 0),
            ((3, 3, 3), 1),
        ],
        hints=[
            "Define ways(dice_left, remaining_sum).",
            "The next die shows face f in 1..k, so ways(d, t) = sum over f of ways(d - 1, t - f).",
            "Memoise (or fill a table dice by dice); take the modulus at every addition.",
        ],
        pattern="Counting DP over (items used, sum reached)",
        explain=(
            "The state (dice left, sum left) has at most n * target values, and each needs k additions, so the "
            "table is polynomial while the raw recursion branches k^n ways."
        ),
        cx="O(n * target * k) time, O(target) space",
        brute_cx="O(k^n) time - recursion without memoisation",
        brute=r"""
# BRUTE FORCE: O(k^n) time - recursion without memoisation
def num_rolls_to_target(n, k, target):
    mod = 10**9 + 7

    def ways(dice, remaining):
        if dice == 0:
            return 1 if remaining == 0 else 0
        return (
            sum(ways(dice - 1, remaining - f) for f in range(1, k + 1) if remaining - f >= 0) % mod
        )

    return ways(n, target)
""",
        solution=r"""
# OPTIMISED: O(n * target * k) time, O(target) space
# Idea: Counting DP over (items used, sum reached)
def num_rolls_to_target(n, k, target):
    mod = 10**9 + 7
    ways = [0] * (target + 1)  # ways[s] = number of ways to reach sum s with the dice so far
    ways[0] = 1

    for _ in range(n):
        nxt = [0] * (target + 1)
        for s in range(target + 1):
            if ways[s]:
                for face in range(1, k + 1):
                    if s + face <= target:
                        nxt[s + face] = (nxt[s + face] + ways[s]) % mod
        ways = nxt

    return ways[target]
""",
    ),
    # ---- Dungeon Game (LeetCode 174) ----
    dict(
        title="Dungeon Game",
        diff="H",
        lc=174,
        slug="dungeon-game",
        prompt=(
            "A knight starts at the top-left of a grid and must reach the bottom-right moving only right or down. "
            "Each cell adds or subtracts health, and health must stay >= 1 at all times. Return the minimum initial "
            "health."
        ),
        sig="def calculate_minimum_hp(dungeon: List[List[int]]) -> int:",
        fn="calculate_minimum_hp",
        tests=[
            (([[-2, -3, 3], [-5, -10, 1], [10, 30, -5]],), 7),
            (([[0]],), 1),
            (([[100]],), 1),
            (([[-3, 5]],), 4),
        ],
        hints=[
            "A forward DP (best sum so far) does not work: a path with a high total can still dip below 1 early.",
            "Work BACKWARDS: need[i][j] = the minimum health required when ENTERING cell (i, j).",
            (
                "need[i][j] = max(1, min(need[i+1][j], need[i][j+1]) - dungeon[i][j]); the last cell uses 1 as the "
                "'next' value."
            ),
        ],
        pattern="Backward DP (compute requirements from the goal)",
        explain=(
            "Going forward you would need to know both the running sum and the lowest point so far. Going backward "
            "removes that: the requirement at a cell depends only on the cheaper of its two successors."
        ),
        cx="O(m*n) time, O(n) space",
        brute_cx="O(2^(m+n)) time - enumerate every path and simulate it",
        brute=r"""
# BRUTE FORCE: O(2^(m+n)) time - enumerate every path and simulate it
def calculate_minimum_hp(dungeon):
    rows, cols = len(dungeon), len(dungeon[0])
    best = float("inf")

    def walk(r, c, total, lowest):  # total = health change so far, lowest = lowest total seen
        nonlocal best
        total += dungeon[r][c]
        lowest = min(lowest, total)

        if r == rows - 1 and c == cols - 1:
            best = min(best, max(1, 1 - lowest))  # start so that the lowest point is still 1
            return

        if r + 1 < rows:
            walk(r + 1, c, total, lowest)

        if c + 1 < cols:
            walk(r, c + 1, total, lowest)

    walk(0, 0, 0, 0)

    return best
""",
        solution=r"""
# OPTIMISED: O(m*n) time, O(n) space
# Idea: Backward DP (compute requirements from the goal)
def calculate_minimum_hp(dungeon):
    rows, cols = len(dungeon), len(dungeon[0])
    need = [float("inf")] * (
        cols + 1
    )  # need[c] = health needed to enter the cell in column c of this row
    need[cols - 1] = 1  # standing past the exit we need 1

    for r in range(rows - 1, -1, -1):
        for c in range(cols - 1, -1, -1):
            cheapest_next = min(need[c], need[c + 1])  # go down (need[c]) or right (need[c + 1])
            need[c] = max(1, cheapest_next - dungeon[r][c])
        need[cols] = float("inf")

    return need[0]
""",
    ),
    # ---- Longest Valid Parentheses (LeetCode 32) ----
    dict(
        title="Longest Valid Parentheses",
        diff="H",
        lc=32,
        slug="longest-valid-parentheses",
        prompt=(
            "Given a string of '(' and ')', return the length of the longest substring that is a valid "
            "(well-formed) parentheses string."
        ),
        sig="def longest_valid_parentheses(s: str) -> int:",
        fn="longest_valid_parentheses",
        tests=[
            (("(()",), 2),
            ((")()())",), 4),
            (("",), 0),
            (("()(())",), 6),
            (("))((",), 0),
        ],
        hints=[
            "Valid Parentheses uses a stack of brackets. Here you need LENGTHS, so store indices.",
            "Keep a stack of indices; start with -1 as a base. For '(' push i.",
            (
                "For ')' pop. If the stack is now empty push i (a new base); otherwise the valid run ends at i, so "
                "length = i - stack[-1]."
            ),
        ],
        pattern="Stack of indices as 'last unmatched position' markers",
        explain=(
            "The element under the stack top is always the index just before the current valid run. Every time a "
            "')' is matched, i - stack[-1] is the length of the run that ends here."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^3) time - check every substring with a counter",
        brute=r"""
# BRUTE FORCE: O(n^3) time - check every substring with a counter
def longest_valid_parentheses(s):
    def valid(sub):
        depth = 0
        for ch in sub:
            depth += 1 if ch == "(" else -1
            if depth < 0:
                return False
        return depth == 0

    best = 0

    for i in range(len(s)):
        for j in range(i + 2, len(s) + 1, 2):  # valid strings have even length
            if valid(s[i:j]):
                best = max(best, j - i)

    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Stack of indices as 'last unmatched position' markers
def longest_valid_parentheses(s):
    stack, best = [-1], 0  # -1 is the base: the index before the first character

    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)  # unmatched ')': it becomes the new base
            else:
                best = max(best, i - stack[-1])

    return best
""",
    ),
    # ---- Wildcard Matching (LeetCode 44) ----
    dict(
        title="Wildcard Matching",
        diff="H",
        lc=44,
        slug="wildcard-matching",
        prompt=(
            "Implement matching where '?' matches any single character and '*' matches any sequence (including "
            "empty). The whole string s must match pattern p."
        ),
        sig="def is_match(s: str, p: str) -> bool:",
        fn="is_match",
        tests=[
            (("aa", "a"), False),
            (("aa", "*"), True),
            (("cb", "?a"), False),
            (("adceb", "*a*b"), True),
            (("acdcb", "a*c?b"), False),
            (("", "*"), True),
        ],
        hints=[
            "State: dp[i][j] = does s[:i] match p[:j]?",
            "If p[j-1] is '*': it matches nothing (dp[i][j-1]) or one more character (dp[i-1][j]).",
            (
                "If it is '?' or an equal letter: dp[i][j] = dp[i-1][j-1]. dp[0][0] = True, and leading '*'s keep "
                "dp[0][j] True."
            ),
        ],
        pattern="2-D string-matching DP (the simpler cousin of Regular Expression Matching)",
        explain=(
            "A star can absorb any number of characters, which is just two moves in the table: stay on the star and "
            "consume a character of s, or skip the star entirely."
        ),
        cx="O(m*n) time, O(n) space",
        brute_cx="O(2^(m+n)) time - recursion that tries every way for '*' to match",
        brute=r"""
# BRUTE FORCE: O(2^(m+n)) time - recursion that tries every way for '*' to match
def is_match(s, p):
    def solve(i, j):
        if j == len(p):
            return i == len(s)

        if p[j] == "*":
            # the star matches nothing, or it swallows s[i] and stays active
            return solve(i, j + 1) or (i < len(s) and solve(i + 1, j))

        if i < len(s) and (p[j] == "?" or p[j] == s[i]):
            return solve(i + 1, j + 1)

        return False

    return solve(0, 0)
""",
        solution=r"""
# OPTIMISED: O(m*n) time, O(n) space
# Idea: 2-D string-matching DP (the simpler cousin of Regular Expression Matching)
def is_match(s, p):
    m, n = len(s), len(p)
    prev = [False] * (
        n + 1
    )  # dp row for i = 0: only patterns of leading stars match the empty string
    prev[0] = True

    for j in range(1, n + 1):
        prev[j] = prev[j - 1] and p[j - 1] == "*"

    for i in range(1, m + 1):
        cur = [False] * (n + 1)
        for j in range(1, n + 1):
            if p[j - 1] == "*":
                cur[j] = cur[j - 1] or prev[j]  # star matches empty, or swallows s[i-1]
            elif p[j - 1] == "?" or p[j - 1] == s[i - 1]:
                cur[j] = prev[j - 1]
        prev = cur

    return prev[n]
""",
    ),
    # ---- Best Time to Buy and Sell Stock III (LeetCode 123) ----
    dict(
        title="Best Time to Buy and Sell Stock III",
        diff="H",
        lc=123,
        slug="best-time-to-buy-and-sell-stock-iii",
        prompt=(
            "prices[i] is a stock's price on day i. You may complete at most TWO transactions (one at a time; sell "
            "before buying again). Return the maximum profit."
        ),
        sig="def max_profit_two(prices: List[int]) -> int:",
        fn="max_profit_two",
        tests=[
            (([3, 3, 5, 0, 0, 3, 1, 4],), 6),
            (([1, 2, 3, 4, 5],), 4),
            (([7, 6, 4, 3, 1],), 0),
            (([1],), 0),
            (([1, 2, 4, 2, 5, 7, 2, 4, 9, 0],), 13),
        ],
        hints=[
            "Brute force: pick a split day; best single trade before it + best single trade after it.",
            "Instead track four running values: after the 1st buy, 1st sell, 2nd buy, 2nd sell.",
            (
                "buy1 = max(buy1, -p); sell1 = max(sell1, buy1 + p); buy2 = max(buy2, sell1 - p); sell2 = "
                "max(sell2, buy2 + p)."
            ),
        ],
        pattern="State-machine DP (one variable per stage of the process)",
        explain=(
            "Each variable holds the best cash position when the process has reached that stage. Every day we "
            "choose between staying in the stage or moving to it from the previous one. The same idea generalises "
            "to k transactions."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - for each split day compute the best single trade on each side",
        brute=r"""
# BRUTE FORCE: O(n^2) time - for each split day compute the best single trade on each side
def max_profit_two(prices):
    def one_trade(segment):  # best profit from at most one buy/sell inside the segment
        best, low = 0, float("inf")
        for p in segment:
            low = min(low, p)
            best = max(best, p - low)
        return best

    n = len(prices)

    return max(one_trade(prices[:i]) + one_trade(prices[i:]) for i in range(n + 1))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: State-machine DP (one variable per stage of the process)
def max_profit_two(prices):
    buy1 = buy2 = float("-inf")  # best balance while holding a share (after buying)
    sell1 = sell2 = 0  # best balance after selling

    for p in prices:
        buy1 = max(buy1, -p)  # first purchase
        sell1 = max(sell1, buy1 + p)  # first sale
        buy2 = max(buy2, sell1 - p)  # second purchase uses the profit of the first trade
        sell2 = max(sell2, buy2 + p)  # second sale

    return sell2
""",
    ),
]
