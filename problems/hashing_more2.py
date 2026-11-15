"""extra batch of Hashing problems - the problem bank for the "hashing" topic.

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
    # ---- First Unique Character in a String (LeetCode 387) ----
    dict(
        title="First Unique Character in a String",
        diff="E",
        lc=387,
        slug="first-unique-character-in-a-string",
        prompt="Return the index of the first character that appears exactly once in s, or -1.",
        sig="def first_uniq_char(s: str) -> int:",
        fn="first_uniq_char",
        tests=[
            (("leetcode",), 0),
            (("loveleetcode",), 2),
            (("aabb",), -1),
            (("z",), 0),
            (("",), -1),
        ],
        hints=[
            "Which characters repeat? You need counts before you can decide.",
            "Pass 1: count every character. Pass 2: scan left to right and return the first with count 1.",
            "Counter(s) then a single loop - O(n) instead of re-scanning for each character.",
        ],
        pattern="Frequency map, two passes (count first, decide second)",
        explain=(
            "Whenever a decision about an element depends on the WHOLE input (is it unique?), count first, then "
            "scan. Two O(n) passes beat O(n^2) re-scanning."
        ),
        cx="O(n) time, O(1) space (26 letters)",
        brute_cx="O(n^2) time",
        brute=r"""
# BRUTE FORCE: O(n^2) time
def first_uniq_char(s):
    for i, c in enumerate(s):
        if s.count(c) == 1:
            return i
    return -1
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space (26 letters)
# Idea: Frequency map, two passes (count first, decide second)
def first_uniq_char(s):
    cnt = Counter(s)
    for i, c in enumerate(s):
        if cnt[c] == 1:
            return i
    return -1
""",
    ),
    # ---- Ransom Note (LeetCode 383) ----
    dict(
        title="Ransom Note",
        diff="E",
        lc=383,
        slug="ransom-note",
        prompt="Can ransom_note be built from the letters of magazine, using each magazine letter at most once?",
        sig="def can_construct(ransom_note: str, magazine: str) -> bool:",
        fn="can_construct",
        tests=[
            (("a", "b"), False),
            (("aa", "ab"), False),
            (("aa", "aab"), True),
            (("", "x"), True),
            (("abc", "cba"), True),
        ],
        hints=[
            "Think of letters as a stock you consume.",
            "Count the magazine's letters. For each note letter, spend one from the stock.",
            "Counter(note) - Counter(magazine) is empty exactly when the note is constructible.",
        ],
        pattern="Frequency map as a budget (inventory)",
        explain=(
            "A Counter is an inventory: build the inventory once, then withdraw. If any withdrawal fails, the "
            "answer is False."
        ),
        cx="O(n + m) time, O(1) space",
        brute_cx="O(n*m) time - delete a matching letter from a list each time",
        brute=r"""
# BRUTE FORCE: O(n*m) time - delete a matching letter from a list each time
def can_construct(ransom_note, magazine):
    pool = list(magazine)
    for c in ransom_note:
        if c in pool:
            pool.remove(c)
        else:
            return False
    return True
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(1) space
# Idea: Frequency map as a budget (inventory)
def can_construct(ransom_note, magazine):
    stock = Counter(magazine)
    for c in ransom_note:
        if stock[c] == 0:
            return False
        stock[c] -= 1
    return True
""",
    ),
    # ---- Contains Duplicate II (LeetCode 219) ----
    dict(
        title="Contains Duplicate II",
        diff="E",
        lc=219,
        slug="contains-duplicate-ii",
        prompt="Are there two equal values nums[i] == nums[j] with i != j and |i - j| <= k?",
        sig="def contains_nearby_duplicate(nums: List[int], k: int) -> bool:",
        fn="contains_nearby_duplicate",
        tests=[
            (([1, 2, 3, 1], 3), True),
            (([1, 0, 1, 1], 1), True),
            (([1, 2, 3, 1, 2, 3], 2), False),
            (([], 1), False),
            (([5, 5], 0), False),
        ],
        hints=[
            "Only the most recent occurrence of a value can be the closest one.",
            "Remember the last index where each value was seen.",
            "dict value -> last index. If i - last[x] <= k return True; always overwrite last[x] = i.",
        ],
        pattern="Hash map of last-seen index (closest previous occurrence)",
        explain="'Nearest equal earlier element' needs only the last index per value. Store it, compare, overwrite.",
        cx="O(n) time, O(n) space",
        brute_cx="O(n*k) time",
        brute=r"""
# BRUTE FORCE: O(n*k) time
def contains_nearby_duplicate(nums, k):
    for i in range(len(nums)):
        for j in range(i + 1, min(len(nums), i + k + 1)):
            if nums[i] == nums[j]:
                return True
    return False
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Hash map of last-seen index (closest previous occurrence)
def contains_nearby_duplicate(nums, k):
    last = {}
    for i, x in enumerate(nums):
        if x in last and i - last[x] <= k:
            return True
        last[x] = i
    return False
""",
    ),
    # ---- 4Sum II (LeetCode 454) ----
    dict(
        title="4Sum II",
        diff="M",
        lc=454,
        slug="4sum-ii",
        prompt="Given four arrays of equal length n, count tuples (i, j, k, l) with a[i] + b[j] + c[k] + d[l] == 0.",
        sig="def four_sum_count(a: List[int], b: List[int], c: List[int], d: List[int]) -> int:",
        fn="four_sum_count",
        tests=[
            (([1, 2], [-2, -1], [-1, 2], [0, 2]), 2),
            (([0], [0], [0], [0]), 1),
            (([1], [1], [1], [1]), 0),
            (([-1, -1], [-1, 1], [-1, 1], [1, -1]), 6),
        ],
        hints=[
            "Four nested loops is n^4. Can you split the problem in two halves?",
            "Pairs (a,b) and pairs (c,d): you need sum(a,b) = -sum(c,d).",
            "Count all a+b sums in a dict, then for each c+d add count[-(c+d)]. O(n^2).",
        ],
        pattern="Meet in the middle with a hash map of pair sums",
        explain=(
            "Splitting a 4-way search into two 2-way halves turns n^4 into 2*n^2. The dictionary is the 'meeting "
            "point'."
        ),
        cx="O(n^2) time, O(n^2) space",
        brute_cx="O(n^4) time",
        brute=r"""
# BRUTE FORCE: O(n^4) time
def four_sum_count(a, b, c, d):
    return sum(1 for x in a for y in b for z in c for w in d if x + y + z + w == 0)
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(n^2) space
# Idea: Meet in the middle with a hash map of pair sums
def four_sum_count(a, b, c, d):
    ab = Counter(x + y for x in a for y in b)
    return sum(ab[-(z + w)] for z in c for w in d)
""",
    ),
    # ---- Word Pattern (LeetCode 290) ----
    dict(
        title="Word Pattern",
        diff="E",
        lc=290,
        slug="word-pattern",
        prompt=(
            "Does the string s follow the pattern? A full bijection between pattern letters and the words of s "
            "(space separated)."
        ),
        sig="def word_pattern(pattern: str, s: str) -> bool:",
        fn="word_pattern",
        tests=[
            (("abba", "dog cat cat dog"), True),
            (("abba", "dog cat cat fish"), False),
            (("aaaa", "dog cat cat dog"), False),
            (("abba", "dog dog dog dog"), False),
            (("a", "x y"), False),
        ],
        hints=[
            "It is the same idea as isomorphic strings, with words instead of characters.",
            "You need the mapping in BOTH directions or two different letters could share a word.",
            (
                "Two dicts (letter->word, word->letter), or compare the 'first-occurrence index' signature of both "
                "sequences."
            ),
        ],
        pattern="Bijection check with two maps",
        explain=(
            "A one-way map only proves 'same letter -> same word'. The reverse map proves 'different letters -> "
            "different words'."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - compare every pair of positions",
        brute=r"""
# BRUTE FORCE: O(n^2) time - compare every pair of positions
def word_pattern(pattern, s):
    w = s.split()
    if len(w) != len(pattern):
        return False
    for i in range(len(w)):
        for j in range(i + 1, len(w)):
            if (pattern[i] == pattern[j]) != (w[i] == w[j]):
                return False
    return True
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Bijection check with two maps
def word_pattern(pattern, s):
    w = s.split()
    if len(w) != len(pattern):
        return False
    fwd, back = {}, {}
    for ch, word in zip(pattern, w):
        if fwd.setdefault(ch, word) != word or back.setdefault(word, ch) != ch:
            return False
    return True
""",
    ),
]
