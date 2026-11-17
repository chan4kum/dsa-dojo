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
    # ---- Best Time to Buy and Sell Stock II (LeetCode 122) ----
    dict(
        title="Best Time to Buy and Sell Stock II",
        diff="M",
        lc=122,
        slug="best-time-to-buy-and-sell-stock-ii",
        prompt=(
            "You may buy and sell the stock many times (one share at a time, sell before buying again). Return the "
            "maximum total profit."
        ),
        sig="def max_profit(prices: List[int]) -> int:",
        fn="max_profit",
        tests=[
            (([7, 1, 5, 3, 6, 4],), 7),
            (([1, 2, 3, 4, 5],), 4),
            (([7, 6, 4, 3, 1],), 0),
            (([1],), 0),
            (([3, 2, 6, 5, 0, 3],), 7),
        ],
        hints=[
            "Unlimited transactions means you can profit from every rise.",
            "Any climb from a to c equals the sum of its daily steps.",
            "Add every positive day-to-day difference.",
        ],
        pattern="Greedy: capture every local gain",
        explain=(
            "A profit from buying at low a and selling at high c equals (b-a)+(c-b) for any day b in between, so "
            "summing\n        all positive adjacent differences captures every possible profit and never loses "
            "anything."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(2^n) time - try buy/sell/skip each day",
        brute=r"""
# BRUTE FORCE: O(2^n) time - try buy/sell/skip each day
def max_profit(prices):
    def go(i, holding):
        if i == len(prices):
            return 0
        skip = go(i + 1, holding)
        if holding:
            return max(skip, prices[i] + go(i + 1, False))
        return max(skip, -prices[i] + go(i + 1, True))

    return go(0, False)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Greedy: capture every local gain
def max_profit(prices):
    return sum(max(0, prices[i] - prices[i - 1]) for i in range(1, len(prices)))
""",
    ),
    # ---- Jump Game II (LeetCode 45) ----
    dict(
        title="Jump Game II",
        diff="M",
        lc=45,
        slug="jump-game-ii",
        prompt=(
            "nums[i] is the max jump length from i. You can always reach the last index. Return the minimum number "
            "of jumps to get there."
        ),
        sig="def jump(nums: List[int]) -> int:",
        fn="jump",
        tests=[
            (([2, 3, 1, 1, 4],), 2),
            (([2, 3, 0, 1, 4],), 2),
            (([1],), 0),
            (([1, 1, 1, 1],), 3),
            (([5, 1, 1, 1, 1, 1],), 1),
        ],
        hints=[
            "DP over 'min jumps to reach i' is O(n^2). Think in layers like BFS.",
            "Layer k = all indices reachable with k jumps; it is a contiguous range.",
            (
                "Track the end of the current layer and the farthest index reachable; when you pass the layer end, "
                "jumps++ and extend the layer."
            ),
        ],
        pattern="Greedy BFS over index ranges (implicit layers)",
        explain=(
            "The set of positions reachable in exactly k jumps is an interval, so BFS collapses to two numbers: "
            "current\n        layer end and farthest. O(n)."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - dp[i] = min jumps to reach i",
        brute=r"""
# BRUTE FORCE: O(n^2) time - dp[i] = min jumps to reach i
def jump(nums):
    n = len(nums)
    dp = [float("inf")] * n
    dp[0] = 0
    for i in range(n):
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            dp[j] = min(dp[j], dp[i] + 1)
    return dp[-1]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Greedy BFS over index ranges (implicit layers)
def jump(nums):
    jumps = end = far = 0
    for i in range(len(nums) - 1):
        far = max(far, i + nums[i])
        if i == end:
            jumps += 1
            end = far
    return jumps
""",
    ),
    # ---- Assign Cookies (LeetCode 455) ----
    dict(
        title="Assign Cookies",
        diff="E",
        lc=455,
        slug="assign-cookies",
        prompt=(
            "Child i is content with a cookie of size >= g[i]; cookie j has size s[j]. Each child gets at most one "
            "cookie. Return the max number of content children."
        ),
        sig="def find_content_children(g: List[int], s: List[int]) -> int:",
        fn="find_content_children",
        tests=[
            (([1, 2, 3], [1, 1]), 1),
            (([1, 2], [1, 2, 3]), 2),
            (([], [1]), 0),
            (([10, 9, 8, 7], [5, 6, 7, 8]), 2),
            (([1, 1], []), 0),
        ],
        hints=[
            "Which cookie should the least greedy child receive?",
            "The smallest cookie that satisfies them - bigger ones are more valuable to others.",
            (
                "Sort both; two pointers: if the cookie satisfies the child, count it and advance both; otherwise "
                "advance the cookie."
            ),
        ],
        pattern="Greedy matching after sorting (smallest sufficient)",
        explain=(
            "Exchange argument: giving a child anything larger than the smallest sufficient cookie can only hurt "
            "later\n        children. Sorting + two pointers executes that rule in O(n log n)."
        ),
        cx="O(n log n) time",
        brute_cx="O(n*m) time - for each child scan for the smallest unused sufficient cookie",
        brute=r"""
# BRUTE FORCE: O(n*m) time - for each child scan for the smallest unused sufficient cookie
def find_content_children(g, s):
    used = [False] * len(s)
    count = 0

    for need in sorted(g):
        best = -1
        for j, size in enumerate(s):
            if not used[j] and size >= need and (best == -1 or size < s[best]):
                best = j
        if best != -1:
            used[best] = True
            count += 1

    return count
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Greedy matching after sorting (smallest sufficient)
def find_content_children(g, s):
    g, s = sorted(g), sorted(s)
    i = 0
    for cookie in s:
        if i < len(g) and cookie >= g[i]:
            i += 1
    return i
""",
    ),
    # ---- Hand of Straights (LeetCode 846) ----
    dict(
        title="Hand of Straights",
        diff="M",
        lc=846,
        slug="hand-of-straights",
        prompt="Can the cards in `hand` be split into groups of exactly group_size consecutive values?",
        sig="def is_n_straight_hand(hand: List[int], group_size: int) -> bool:",
        fn="is_n_straight_hand",
        tests=[
            (([1, 2, 3, 6, 2, 3, 4, 7, 8], 3), True),
            (([1, 2, 3, 4, 5], 4), False),
            (([1, 2, 3], 1), True),
            (([1, 1, 2, 2, 3, 3], 3), True),
            (([1, 2, 4], 3), False),
        ],
        hints=[
            "The smallest card has to start a group - nothing smaller can be below it.",
            "So repeatedly take the smallest remaining value and build the run of group_size cards from it.",
            "Counter of cards; iterate sorted keys; for each key with count c > 0 consume c copies of key..key+size-1.",
        ],
        pattern="Greedy from the smallest + frequency map",
        explain=(
            "The minimum card is forced to be the start of a group, so there is no choice to make - the algorithm "
            "is just\n        bookkeeping. If any needed value is missing the answer is False."
        ),
        cx="O(n log n) time",
        brute_cx="O(n^2) time - repeatedly remove a run from a sorted list",
        brute=r"""
# BRUTE FORCE: O(n^2) time - repeatedly remove a run from a sorted list
def is_n_straight_hand(hand, group_size):
    if len(hand) % group_size:
        return False

    cards = sorted(hand)

    while cards:
        start = cards[0]
        for v in range(start, start + group_size):
            if v not in cards:
                return False
            cards.remove(v)

    return True
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Greedy from the smallest + frequency map
def is_n_straight_hand(hand, group_size):
    if len(hand) % group_size:
        return False

    cnt = Counter(hand)

    for x in sorted(cnt):
        c = cnt[x]
        if c:
            for v in range(x, x + group_size):
                if cnt[v] < c:
                    return False
                cnt[v] -= c

    return True
""",
    ),
    # ---- Valid Parenthesis String (LeetCode 678) ----
    dict(
        title="Valid Parenthesis String",
        diff="M",
        lc=678,
        slug="valid-parenthesis-string",
        prompt=(
            "s contains '(', ')' and '*'. '*' may act as '(', ')' or an empty string. Return True if s can be made "
            "a valid balanced string."
        ),
        sig="def check_valid_string(s: str) -> bool:",
        fn="check_valid_string",
        tests=[
            (("()",), True),
            (("(*)",), True),
            (("(*))",), True),
            (("(((*)",), False),
            ((")(",), False),
            (("*",), True),
            (("",), True),
            (("(*()",), True),
        ],
        hints=[
            "Trying every choice for each '*' is exponential. Track a RANGE of possible open counts instead.",
            "Keep lo = min possible open parens and hi = max possible.",
            (
                "'(' : lo++, hi++. ')': lo--, hi--. '*': lo--, hi++. Clamp lo at 0; if hi < 0 return False. At the "
                "end lo == 0 means valid."
            ),
        ],
        pattern="Greedy with a range of possible states",
        explain=(
            "The set of achievable 'open counts' after each character is a contiguous interval, so two integers "
            "represent\n        all 2^k possibilities. hi < 0 means too many ')' even if every * were '('. lo is "
            "clamped because an extra\n        ')' can always be avoided by treating the * as empty."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(3^k) time - try each * as '(', ')' or empty (k = number of stars)",
        brute=r"""
# BRUTE FORCE: O(3^k) time - try each * as '(', ')' or empty (k = number of stars)
def check_valid_string(s):
    def go(i, open_):
        if open_ < 0:
            return False

        if i == len(s):
            return open_ == 0

        c = s[i]

        if c == "(":
            return go(i + 1, open_ + 1)

        if c == ")":
            return go(i + 1, open_ - 1)

        return go(i + 1, open_ + 1) or go(i + 1, open_ - 1) or go(i + 1, open_)

    return go(0, 0)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Greedy with a range of possible states
def check_valid_string(s):
    lo = hi = 0

    for c in s:
        if c == "(":
            lo, hi = lo + 1, hi + 1
        elif c == ")":
            lo, hi = lo - 1, hi - 1
        else:
            lo, hi = lo - 1, hi + 1

        if hi < 0:
            return False

        lo = max(lo, 0)

    return lo == 0
""",
    ),
    # ---- Candy (LeetCode 135) ----
    dict(
        title="Candy",
        diff="H",
        lc=135,
        slug="candy",
        prompt=(
            "Children stand in a line with ratings. Each child gets at least 1 candy, and a child with a higher "
            "rating than a neighbour must get more candy than that neighbour. Return the minimum total candies."
        ),
        sig="def candy(ratings: List[int]) -> int:",
        fn="candy",
        tests=[
            (([1, 0, 2],), 5),
            (([1, 2, 2],), 4),
            (([1],), 1),
            (([1, 3, 2, 2, 1],), 7),
            (([5, 4, 3, 2, 1],), 15),
            (([],), 0),
        ],
        hints=[
            "The constraint has two directions (left neighbour and right neighbour). Handle them separately.",
            "Pass 1 left->right: if rating > left neighbour, candy = left + 1.",
            "Pass 2 right->left: if rating > right neighbour, candy = max(candy, right + 1). Sum.",
        ],
        pattern="Two-pass greedy (satisfy left constraints, then right constraints)",
        explain=(
            "Each pass enforces one side's rule with the minimum possible values; taking the max afterwards "
            "satisfies both\n        rules at once and is still minimal."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - keep fixing violations until stable",
        brute=r"""
# BRUTE FORCE: O(n^2) time - keep fixing violations until stable
def candy(ratings):
    n = len(ratings)
    c = [1] * n
    changed = True

    while changed:
        changed = False

        for i in range(n):
            if i and ratings[i] > ratings[i - 1] and c[i] <= c[i - 1]:
                c[i] = c[i - 1] + 1
                changed = True
            if i < n - 1 and ratings[i] > ratings[i + 1] and c[i] <= c[i + 1]:
                c[i] = c[i + 1] + 1
                changed = True

    return sum(c)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Two-pass greedy (satisfy left constraints, then right constraints)
def candy(ratings):
    n = len(ratings)
    c = [1] * n

    for i in range(1, n):
        if ratings[i] > ratings[i - 1]:
            c[i] = c[i - 1] + 1

    for i in range(n - 2, -1, -1):
        if ratings[i] > ratings[i + 1]:
            c[i] = max(c[i], c[i + 1] + 1)

    return sum(c)
""",
    ),
]
