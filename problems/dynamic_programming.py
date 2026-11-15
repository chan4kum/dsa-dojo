"""Dynamic Programming problems - the problem bank for the "dynamic_programming" topic.

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
    # ---- Climbing Stairs (LeetCode 70) ----
    dict(
        title="Climbing Stairs",
        diff="E",
        lc=70,
        slug="climbing-stairs",
        prompt="You can climb 1 or 2 steps at a time. How many distinct ways are there to climb n steps?",
        sig="def climb_stairs(n: int) -> int:",
        fn="climb_stairs",
        tests=[
            ((1,), 1),
            ((2,), 2),
            ((3,), 3),
            ((5,), 8),
            ((10,), 89),
            ((30,), 1346269),
        ],
        hints=[
            "Think about the LAST move you made. Where could you have been just before?",
            "ways(n) = ways(n-1) + ways(n-2): you arrived by a 1-step from n-1 or a 2-step from n-2.",
            "Naive recursion repeats work exponentially. Keep only the last two values and iterate.",
        ],
        pattern="1-D DP: state = position, transition from the previous 1-2 states (Fibonacci shape)",
        explain=(
            "DP recipe: (1) define the state, (2) write the recurrence by asking 'what was the last "
            "decision?',\n        (3) base cases, (4) order of evaluation, (5) shrink memory. Here the state is "
            "'ways to reach step i'.\n        Only two previous values are needed -> O(n) time, O(1) space."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(2^n) - plain recursion recomputes the same subproblems",
        brute=r"""
# BRUTE FORCE: O(2^n) - plain recursion recomputes the same subproblems
def climb_stairs(n):
    if n <= 2:
        return n
    return climb_stairs(n - 1) + climb_stairs(n - 2)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: 1-D DP: state = position, transition from the previous 1-2 states (Fibonacci shape)
def climb_stairs(n):
    a, b = 1, 1  # ways(0), ways(1)
    for _ in range(n - 1):
        a, b = b, a + b
    return b
""",
    ),
    # ---- House Robber (LeetCode 198) ----
    dict(
        title="House Robber",
        diff="M",
        lc=198,
        slug="house-robber",
        prompt=(
            "Houses in a row hold given amounts of money; robbing two adjacent houses triggers an alarm. Return the "
            "maximum you can rob."
        ),
        sig="def rob(nums: List[int]) -> int:",
        fn="rob",
        tests=[
            (([1, 2, 3, 1],), 4),
            (([2, 7, 9, 3, 1],), 12),
            (([5],), 5),
            (([2, 1, 1, 2],), 4),
            (([],), 0),
            (([10, 1, 1, 10],), 20),
        ],
        hints=[
            "For each house you have two choices: rob it or skip it.",
            "best(i) = max(best(i-1), best(i-2) + nums[i]).",
            "Only the previous two values matter: keep `take` and `skip` variables.",
        ],
        pattern="1-D DP with a take/skip decision at each element",
        explain=(
            "Skipping keeps the best of the first i-1 houses; robbing forces skipping house i-1, so it adds "
            "nums[i]\n        to the best of the first i-2. Two rolling variables give O(1) space."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(2^n) - recursion without memo",
        brute=r"""
# BRUTE FORCE: O(2^n) - recursion without memo
def rob(nums):
    def go(i):
        if i < 0:
            return 0
        return max(go(i - 1), go(i - 2) + nums[i])

    return go(len(nums) - 1)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: 1-D DP with a take/skip decision at each element
def rob(nums):
    prev2 = prev1 = 0  # best up to i-2, best up to i-1
    for x in nums:
        prev2, prev1 = prev1, max(prev1, prev2 + x)
    return prev1
""",
    ),
    # ---- Coin Change (LeetCode 322) ----
    dict(
        title="Coin Change",
        diff="M",
        lc=322,
        slug="coin-change",
        prompt=(
            "Given coin denominations (unlimited supply) and an amount, return the fewest coins that make exactly "
            "that amount, or -1 if impossible."
        ),
        sig="def coin_change(coins: List[int], amount: int) -> int:",
        fn="coin_change",
        tests=[
            (([1, 2, 5], 11), 3),
            (([2], 3), -1),
            (([1], 0), 0),
            (([186, 419, 83, 408], 6249), 20),
            (([2, 5, 10, 1], 27), 4),
            (([5], 5), 1),
        ],
        hints=[
            (
                "Greedy (take the biggest coin) fails, e.g. coins [1,3,4], amount 6 -> best is 3+3. You need to "
                "consider all choices."
            ),
            "dp[a] = fewest coins for amount a. What was the LAST coin used?",
            "dp[a] = 1 + min(dp[a - c]) over coins c <= a, with dp[0] = 0 and 'infinity' for unreachable.",
        ],
        pattern="Unbounded knapsack / DP over amount (min coins)",
        explain=(
            "Subproblems overlap heavily (amount 6 needs 5, 3, 2...). Bottom-up table dp[0..amount]. Each cell "
            "tries\n        every coin: O(amount * len(coins)). 'Min number of items to reach a total' = this "
            "pattern; 'count the\n        ways' is the same table with + instead of min (and loop order "
            "coins-outer)."
        ),
        cx="O(amount * coins) time, O(amount) space",
        brute_cx="O(coins^amount) - exponential recursion",
        brute=r"""
# BRUTE FORCE: O(coins^amount) - exponential recursion
def coin_change(coins, amount):
    def go(a):
        if a == 0:
            return 0
        best = float("inf")
        for c in coins:
            if c <= a:
                best = min(best, go(a - c) + 1)
        return best

    r = go(amount)
    return -1 if r == float("inf") else r
""",
        solution=r"""
# OPTIMISED: O(amount * coins) time, O(amount) space
# Idea: Unbounded knapsack / DP over amount (min coins)
def coin_change(coins, amount):
    INF = float("inf")
    dp = [0] + [INF] * amount
    for a in range(1, amount + 1):
        for c in coins:
            if c <= a and dp[a - c] + 1 < dp[a]:
                dp[a] = dp[a - c] + 1
    return -1 if dp[amount] == INF else dp[amount]
""",
    ),
    # ---- Longest Increasing Subsequence (LeetCode 300) ----
    dict(
        title="Longest Increasing Subsequence",
        diff="M",
        lc=300,
        slug="longest-increasing-subsequence",
        prompt="Return the length of the longest strictly increasing subsequence (elements need not be contiguous).",
        sig="def length_of_lis(nums: List[int]) -> int:",
        fn="length_of_lis",
        tests=[
            (([10, 9, 2, 5, 3, 7, 101, 18],), 4),
            (([0, 1, 0, 3, 2, 3],), 4),
            (([7, 7, 7, 7],), 1),
            (([],), 0),
            (([1, 3, 6, 7, 9, 4, 10, 5, 6],), 6),
        ],
        hints=[
            "O(n^2): dp[i] = 1 + max(dp[j]) over j < i with nums[j] < nums[i].",
            (
                "For O(n log n), keep tails[k] = the smallest possible last value of an increasing subsequence of "
                "length k+1."
            ),
            (
                "For each x, binary-search the first tail >= x (bisect_left) and overwrite it; append if x is "
                "larger than all tails."
            ),
        ],
        pattern="DP -> patience sorting with binary search (tails array)",
        explain=(
            "`tails` is always sorted. Replacing a tail with a smaller value keeps the same length but makes "
            "future\n        extension easier. `tails` is NOT itself the subsequence, only its length (len(tails)) "
            "is the answer.\n        bisect_left makes it strictly increasing (use bisect_right for "
            "non-decreasing). O(n log n)."
        ),
        cx="O(n log n) time (patience sorting) or O(n^2) DP",
        brute_cx="O(n^2) DP; patience sorting gets O(n log n)",
        brute=r"""
# BRUTE FORCE: O(n^2) DP; patience sorting gets O(n log n)
def length_of_lis(nums):
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp, default=0)
""",
        solution=r"""
# OPTIMISED: O(n log n) time (patience sorting) or O(n^2) DP
# Idea: DP -> patience sorting with binary search (tails array)
def length_of_lis(nums):
    tails = []
    for x in nums:
        i = bisect.bisect_left(tails, x)
        if i == len(tails):
            tails.append(x)
        else:
            tails[i] = x
    return len(tails)
""",
    ),
    # ---- Longest Common Subsequence (LeetCode 1143) ----
    dict(
        title="Longest Common Subsequence",
        diff="M",
        lc=1143,
        slug="longest-common-subsequence",
        prompt="Return the length of the longest subsequence common to two strings.",
        sig="def longest_common_subsequence(text1: str, text2: str) -> int:",
        fn="longest_common_subsequence",
        tests=[
            (("abcde", "ace"), 3),
            (("abc", "abc"), 3),
            (("abc", "def"), 0),
            (("", "abc"), 0),
            (("bsbininm", "jmjkbkjkv"), 1),
            (("oxcpqrsvwf", "shmtulqrypy"), 2),
        ],
        hints=[
            "Compare the LAST characters of both strings. What if they match? What if they do not?",
            "dp[i][j] = LCS of text1[:i], text2[:j]. Match -> 1 + dp[i-1][j-1]; else max(dp[i-1][j], dp[i][j-1]).",
            "Fill an (m+1) x (n+1) table with zeros on the border; the answer is dp[m][n].",
        ],
        pattern="2-D DP on two sequences (prefix pairs)",
        explain=(
            "A matching last pair can always be part of an optimal common subsequence, so we consume both. If "
            "they\n        differ at least one of them is not used, so drop one and take the better. O(m*n) "
            "time/space (O(n) space\n        with two rows). Edit Distance, Distinct Subsequences, Interleaving "
            "String share this skeleton."
        ),
        cx="O(m*n) time, O(min(m, n)) space",
        brute_cx="O(2^(m+n)) - recursion without memo",
        brute=r"""
# BRUTE FORCE: O(2^(m+n)) - recursion without memo
def longest_common_subsequence(text1, text2):
    def go(i, j):
        if i == len(text1) or j == len(text2):
            return 0
        if text1[i] == text2[j]:
            return 1 + go(i + 1, j + 1)
        return max(go(i + 1, j), go(i, j + 1))

    return go(0, 0)
""",
        solution=r"""
# OPTIMISED: O(m*n) time, O(min(m, n)) space
# Idea: 2-D DP on two sequences (prefix pairs)
def longest_common_subsequence(text1, text2):
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
""",
    ),
    # ---- Edit Distance (LeetCode 72) ----
    dict(
        title="Edit Distance",
        diff="M",
        lc=72,
        slug="edit-distance",
        prompt="Minimum number of single-character insertions, deletions or replacements to turn word1 into word2.",
        sig="def min_distance(word1: str, word2: str) -> int:",
        fn="min_distance",
        tests=[
            (("horse", "ros"), 3),
            (("intention", "execution"), 5),
            (("", ""), 0),
            (("", "abc"), 3),
            (("abc", ""), 3),
            (("kitten", "sitting"), 3),
        ],
        hints=[
            "Look at the last characters. If equal, they cost nothing - what remains to solve?",
            (
                "If different you have three options: replace, delete from word1, insert into word1. Each leaves a "
                "smaller subproblem."
            ),
            (
                "dp[i][j] = dp[i-1][j-1] if equal else 1 + min(dp[i-1][j-1], dp[i-1][j], dp[i][j-1]). Borders: "
                "dp[i][0]=i, dp[0][j]=j."
            ),
        ],
        pattern="2-D DP on two strings (edit operations as transitions)",
        explain=(
            "dp[i][j] = cost to convert the first i chars of word1 into the first j of word2. Replace = "
            "diagonal,\n        delete = up (consume a char of word1), insert = left (consume a char of word2). "
            "Borders are pure\n        deletions/insertions. O(m*n)."
        ),
        cx="O(m*n) time and space",
        brute_cx="O(3^(m+n)) - recursion without memo",
        brute=r"""
# BRUTE FORCE: O(3^(m+n)) - recursion without memo
def min_distance(word1, word2):
    def go(i, j):
        if i == len(word1):
            return len(word2) - j
        if j == len(word2):
            return len(word1) - i
        if word1[i] == word2[j]:
            return go(i + 1, j + 1)
        return 1 + min(go(i + 1, j + 1), go(i + 1, j), go(i, j + 1))

    return go(0, 0)
""",
        solution=r"""
# OPTIMISED: O(m*n) time and space
# Idea: 2-D DP on two strings (edit operations as transitions)
def min_distance(word1, word2):
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j - 1], dp[i - 1][j], dp[i][j - 1])
    return dp[m][n]
""",
    ),
    # ---- Partition Equal Subset Sum (LeetCode 416) ----
    dict(
        title="Partition Equal Subset Sum",
        diff="M",
        lc=416,
        slug="partition-equal-subset-sum",
        prompt="Can the array be split into two subsets with equal sums?",
        sig="def can_partition(nums: List[int]) -> bool:",
        fn="can_partition",
        tests=[
            (([1, 5, 11, 5],), True),
            (([1, 2, 3, 5],), False),
            (([2, 2],), True),
            (([1],), False),
            (([100, 100, 100, 100, 99, 1],), False),
        ],
        hints=[
            "Equal halves means one subset sums to total/2. If total is odd, stop.",
            "That is the subset-sum decision problem: reachable[s] = can some subset sum to s?",
            "0/1 knapsack boolean table: for each number x, update sums from high to low (so x is used at most once).",
        ],
        pattern="0/1 knapsack (subset sum) - iterate the capacity BACKWARDS",
        explain=(
            "reachable[s] |= reachable[s - x]. Going downward ensures each item is counted once (an upward "
            "loop\n        would let the same x be reused = unbounded knapsack, as in Coin Change). O(n * total/2) "
            "time, O(total)\n        space."
        ),
        cx="O(n * sum) time, O(sum) space (0/1 knapsack)",
        brute_cx="O(2^n) - try every subset",
        brute=r"""
# BRUTE FORCE: O(2^n) - try every subset
def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False

    def go(i, remain):
        if remain == 0:
            return True
        if i == len(nums) or remain < 0:
            return False
        return go(i + 1, remain - nums[i]) or go(i + 1, remain)

    return go(0, total // 2)
""",
        solution=r"""
# OPTIMISED: O(n * sum) time, O(sum) space (0/1 knapsack)
# Idea: 0/1 knapsack (subset sum) - iterate the capacity BACKWARDS
def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False
    target = total // 2
    reachable = [True] + [False] * target
    for x in nums:
        for s in range(target, x - 1, -1):  # backwards: each item used once
            if reachable[s - x]:
                reachable[s] = True
    return reachable[target]
""",
    ),
    # ---- Word Break (LeetCode 139) ----
    dict(
        title="Word Break",
        diff="M",
        lc=139,
        slug="word-break",
        prompt=(
            "Can the string s be segmented into a space-separated sequence of words from the dictionary (words may "
            "be reused)?"
        ),
        sig="def word_break(s: str, word_dict: List[str]) -> bool:",
        fn="word_break",
        tests=[
            (("leetcode", ["leet", "code"]), True),
            (("applepenapple", ["apple", "pen"]), True),
            (("catsandog", ["cats", "dog", "sand", "and", "cat"]), False),
            (("a", ["b"]), False),
            (("", ["a"]), True),
            (("aaaaaaa", ["aaaa", "aaa"]), True),
        ],
        hints=[
            "Brute-force splitting tries every cut point recursively - exponential.",
            "dp[i] = can the prefix s[:i] be segmented? dp[0] = True.",
            "dp[i] is True if some j < i has dp[j] True and s[j:i] is in the dictionary (use a set).",
        ],
        pattern="1-D DP over prefixes with a lookup inside (partition DP)",
        explain=(
            "A prefix is segmentable iff it ends with a dictionary word whose preceding prefix is "
            "segmentable.\n        O(n^2) substring checks (times word length for hashing); break at the first "
            "success per i."
        ),
        cx="O(n^2) time (memoised)",
        brute_cx="O(2^n) - recursion without memo",
        brute=r"""
# BRUTE FORCE: O(2^n) - recursion without memo
def word_break(s, word_dict):
    words = set(word_dict)

    def go(i):
        if i == len(s):
            return True
        return any(s[i:j] in words and go(j) for j in range(i + 1, len(s) + 1))

    return go(0)
""",
        solution=r"""
# OPTIMISED: O(n^2) time (memoised)
# Idea: 1-D DP over prefixes with a lookup inside (partition DP)
def word_break(s, word_dict):
    words = set(word_dict)
    dp = [True] + [False] * len(s)
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[len(s)]
""",
    ),
    # ---- Burst Balloons (LeetCode 312) ----
    dict(
        title="Burst Balloons",
        diff="H",
        lc=312,
        slug="burst-balloons",
        prompt=(
            "Balloons hold numbers. Bursting balloon i earns nums[i-1] * nums[i] * nums[i+1] (missing neighbours "
            "count as 1). Return the maximum coins from bursting all of them in the best order."
        ),
        sig="def max_coins(nums: List[int]) -> int:",
        fn="max_coins",
        tests=[
            (([3, 1, 5, 8],), 167),
            (([1, 5],), 10),
            (([7],), 7),
            (([],), 0),
            (([9, 76, 64, 21],), 116718),
        ],
        hints=[
            "Choosing which balloon to burst FIRST makes neighbours change - the subproblems are not independent.",
            "Flip it: choose which balloon is burst LAST in a range (l, r). Then its neighbours are exactly l and r.",
            "dp[l][r] = max over k in (l, r) of dp[l][k] + dp[k][r] + a[l]*a[k]*a[r], with 1s padded on both ends.",
        ],
        pattern="Interval DP: split an interval on the LAST action",
        explain=(
            "'Last' is the trick: after everything else inside (l, r) is gone, the last balloon k sees l and r "
            "as\n        neighbours, and the two sides (l,k) and (k,r) are independent. Fill by increasing interval "
            "length.\n        O(n^3) time, O(n^2) space."
        ),
        cx="O(n^3) time, O(n^2) space (interval DP)",
        brute_cx="O(n!) - try every bursting order",
        brute=r"""
# BRUTE FORCE: O(n!) - try every bursting order
def max_coins(nums):
    def go(arr):
        if not arr:
            return 0
        best = 0
        for i in range(len(arr)):
            left = arr[i - 1] if i else 1
            right = arr[i + 1] if i + 1 < len(arr) else 1
            best = max(best, left * arr[i] * right + go(arr[:i] + arr[i + 1 :]))
        return best

    return go(nums)
""",
        solution=r"""
# OPTIMISED: O(n^3) time, O(n^2) space (interval DP)
# Idea: Interval DP: split an interval on the LAST action
def max_coins(nums):
    a = [1] + nums + [1]
    n = len(a)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):  # window (l, r) exclusive of both ends
        for left in range(n - length):
            right = left + length
            for k in range(left + 1, right):  # k = balloon burst LAST in (l, r)
                dp[left][right] = max(
                    dp[left][right], dp[left][k] + dp[k][right] + a[left] * a[k] * a[right]
                )
    return dp[0][n - 1]
""",
    ),
]
