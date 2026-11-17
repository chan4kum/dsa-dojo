"""extra batch of Sliding Window problems - the problem bank for the "sliding_window" topic.

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
    # ---- Best Time to Buy and Sell Stock (LeetCode 121) ----
    dict(
        title="Best Time to Buy and Sell Stock",
        diff="E",
        lc=121,
        slug="best-time-to-buy-and-sell-stock",
        prompt=(
            "prices[i] is the price on day i. Buy once, then sell on a later day. Return the maximum profit (0 if "
            "none is possible)."
        ),
        sig="def max_profit(prices: List[int]) -> int:",
        fn="max_profit",
        tests=[
            (([7, 1, 5, 3, 6, 4],), 5),
            (([7, 6, 4, 3, 1],), 0),
            (([1, 2],), 1),
            (([2, 4, 1],), 2),
            (([3],), 0),
        ],
        hints=[
            "For a fixed selling day, which buying day is best?",
            "The cheapest price seen BEFORE it.",
            "Scan once: track min_price so far; profit candidate = price - min_price.",
        ],
        pattern="Running minimum (one-pass 'best so far' scan)",
        explain=(
            "For each day treat it as the sell day: the best buy is the minimum of all earlier days, which can be "
            "kept\n        up to date in O(1). The answer is the max over days of (price - running min)."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - every buy/sell pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - every buy/sell pair
def max_profit(prices):
    best = 0
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            best = max(best, prices[j] - prices[i])
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Running minimum (one-pass 'best so far' scan)
def max_profit(prices):
    best, low = 0, float("inf")
    for p in prices:
        low = min(low, p)
        best = max(best, p - low)
    return best
""",
    ),
    # ---- Longest Repeating Character Replacement (LeetCode 424) ----
    dict(
        title="Longest Repeating Character Replacement",
        diff="M",
        lc=424,
        slug="longest-repeating-character-replacement",
        prompt=(
            "You may replace at most k characters of the uppercase string s with any letter. Return the length of "
            "the longest substring consisting of a single repeated letter you can obtain."
        ),
        sig="def character_replacement(s: str, k: int) -> int:",
        fn="character_replacement",
        tests=[
            (("ABAB", 2), 4),
            (("AABABBA", 1), 4),
            (("AAAA", 0), 4),
            (("ABCDE", 1), 2),
            (("", 3), 0),
        ],
        hints=[
            "A window is valid if (window length - count of its most common letter) <= k.",
            "Use a sliding window with a counter of letters in it.",
            (
                "Expand right always; while the window is invalid, shrink left. You never need to shrink the max "
                "count downward - the best answer can only grow when max_count grows."
            ),
        ],
        pattern="Sliding window with a validity condition (length - max_freq <= k)",
        explain=(
            "Letters outside the dominant one are the ones that must be replaced. So the window is feasible "
            "iff\n        len - maxfreq <= k. Because we only care about the LARGEST window, a stale (too high) "
            "maxfreq just keeps the\n        window from shrinking below the best size already found - the classic "
            "accepted trick."
        ),
        cx="O(n) time, O(26) space",
        brute_cx="O(n^2 * 26) time - check every substring",
        brute=r"""
# BRUTE FORCE: O(n^2 * 26) time - check every substring
def character_replacement(s, k):
    best = 0

    for i in range(len(s)):
        cnt = Counter()
        for j in range(i, len(s)):
            cnt[s[j]] += 1
            if (j - i + 1) - max(cnt.values()) <= k:
                best = max(best, j - i + 1)

    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(26) space
# Idea: Sliding window with a validity condition (length - max_freq <= k)
def character_replacement(s, k):
    count = Counter()
    left = best = max_f = 0

    for right, ch in enumerate(s):
        count[ch] += 1
        max_f = max(max_f, count[ch])
        while (right - left + 1) - max_f > k:
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)

    return best
""",
    ),
    # ---- Permutation in String (LeetCode 567) ----
    dict(
        title="Permutation in String",
        diff="M",
        lc=567,
        slug="permutation-in-string",
        prompt="Return True if s2 contains a substring that is a permutation of s1.",
        sig="def check_inclusion(s1: str, s2: str) -> bool:",
        fn="check_inclusion",
        tests=[
            (("ab", "eidbaooo"), True),
            (("ab", "eidboaoo"), False),
            (("a", "a"), True),
            (("abc", "ab"), False),
            (("adc", "dcda"), True),
        ],
        hints=[
            "A permutation of s1 has exactly the letter counts of s1 and length len(s1).",
            "So look at every window of length len(s1) in s2.",
            (
                "Slide a fixed-size window, updating its Counter by one add and one remove per step; compare with "
                "Counter(s1) (26 letters = O(1))."
            ),
        ],
        pattern="Fixed-size sliding window + frequency map comparison",
        explain=(
            "Window size is fixed to len(s1). Moving it one step changes only two counts, so maintaining the "
            "counter is\n        O(1). Comparing two counters costs O(alphabet). Total O(n)."
        ),
        cx="O(n) time, O(26) space",
        brute_cx="O(n * m log m) time - sort every window",
        brute=r"""
# BRUTE FORCE: O(n * m log m) time - sort every window
def check_inclusion(s1, s2):
    m = len(s1)
    target = sorted(s1)
    return any(sorted(s2[i : i + m]) == target for i in range(len(s2) - m + 1))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(26) space
# Idea: Fixed-size sliding window + frequency map comparison
def check_inclusion(s1, s2):
    m = len(s1)

    if m > len(s2):
        return False

    need, win = Counter(s1), Counter(s2[:m])

    if win == need:
        return True

    for i in range(m, len(s2)):
        win[s2[i]] += 1
        out = s2[i - m]
        win[out] -= 1
        if win[out] == 0:
            del win[out]
        if win == need:
            return True

    return False
""",
    ),
    # ---- Find All Anagrams in a String (LeetCode 438) ----
    dict(
        title="Find All Anagrams in a String",
        diff="M",
        lc=438,
        slug="find-all-anagrams-in-a-string",
        prompt="Return the start indices of every substring of s that is an anagram of p.",
        sig="def find_anagrams(s: str, p: str) -> List[int]:",
        fn="find_anagrams",
        tests=[
            (("cbaebabacd", "abc"), [0, 6]),
            (("abab", "ab"), [0, 1, 2]),
            (("a", "ab"), []),
            (("aaaa", "aa"), [0, 1, 2]),
        ],
        hints=[
            "Same idea as 'Permutation in String', but collect every match.",
            "Fixed window of length len(p); update counts incrementally.",
            "Append the left index of the window whenever its Counter equals Counter(p).",
        ],
        pattern="Fixed-size sliding window + frequency map",
        explain=(
            "Identical machinery to Permutation in String; instead of returning at the first hit, record every start."
        ),
        cx="O(n) time, O(26) space",
        brute_cx="O(n * m log m) time - sort each window",
        brute=r"""
# BRUTE FORCE: O(n * m log m) time - sort each window
def find_anagrams(s, p):
    m, target = len(p), sorted(p)
    return [i for i in range(len(s) - m + 1) if sorted(s[i : i + m]) == target]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(26) space
# Idea: Fixed-size sliding window + frequency map
def find_anagrams(s, p):
    m, out = len(p), []

    if m > len(s):
        return out

    need, win = Counter(p), Counter(s[:m])

    if win == need:
        out.append(0)

    for i in range(m, len(s)):
        win[s[i]] += 1
        left = s[i - m]
        win[left] -= 1
        if win[left] == 0:
            del win[left]
        if win == need:
            out.append(i - m + 1)

    return out
""",
    ),
    # ---- Max Consecutive Ones III (LeetCode 1004) ----
    dict(
        title="Max Consecutive Ones III",
        diff="M",
        lc=1004,
        slug="max-consecutive-ones-iii",
        prompt="Binary array nums. You may flip at most k zeros to 1. Return the longest run of 1s possible.",
        sig="def longest_ones(nums: List[int], k: int) -> int:",
        fn="longest_ones",
        tests=[
            (([1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0], 2), 6),
            (([0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1], 3), 10),
            (([0, 0, 0], 0), 0),
            (([1, 1], 0), 2),
        ],
        hints=[
            "Rephrase: longest subarray containing at most k zeros.",
            "Sliding window, count zeros inside.",
            "Expand right; if zeros > k, move left until zeros <= k. Track the max length.",
        ],
        pattern="Sliding window: 'at most k bad items'",
        explain=(
            "Flipping zeros is a disguise: you are choosing the longest window that has no more than k zeros. This "
            "'at most\n        k violations' window template solves dozens of problems."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - every start, extend until k+1 zeros",
        brute=r"""
# BRUTE FORCE: O(n^2) time - every start, extend until k+1 zeros
def longest_ones(nums, k):
    best = 0

    for i in range(len(nums)):
        zeros = 0
        for j in range(i, len(nums)):
            zeros += nums[j] == 0
            if zeros > k:
                break
            best = max(best, j - i + 1)

    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Sliding window: 'at most k bad items'
def longest_ones(nums, k):
    left = zeros = best = 0

    for right, x in enumerate(nums):
        zeros += x == 0
        while zeros > k:
            zeros -= nums[left] == 0
            left += 1
        best = max(best, right - left + 1)

    return best
""",
    ),
]
