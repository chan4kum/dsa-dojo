"""more Hashing problems (batch 4) - part of the problem bank for the "hashing" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Intersection of Two Arrays (LeetCode 349) ----
    dict(
        title="Intersection of Two Arrays",
        diff="E",
        lc=349,
        slug="intersection-of-two-arrays",
        prompt="Return the distinct values that appear in both arrays (any order).",
        sig="def intersection(nums1: List[int], nums2: List[int]) -> List[int]:",
        fn="intersection",
        compare="unordered",
        tests=[
            (([1, 2, 2, 1], [2, 2]), [2]),
            (([4, 9, 5], [9, 4, 9, 8, 4]), [4, 9]),
            (([1], [2]), []),
            (([], [1]), []),
        ],
        hints=[
            "Checking every pair is O(n * m).",
            "A hash set answers 'is x in the other array?' in O(1).",
            "Put one array in a set and keep the values of the other that it contains - or just use set intersection.",
        ],
        pattern="Hash set membership",
        explain=(
            "Sets remove duplicates automatically and give O(1) lookups, turning a quadratic comparison into one "
            "linear pass."
        ),
        cx="O(n + m) time, O(n) space",
        brute_cx="O(n * m) time - compare every pair",
        brute=r"""
# BRUTE FORCE: O(n * m) time - compare every pair
def intersection(nums1, nums2):
    result = []
    for a in nums1:
        for b in nums2:
            if a == b and a not in result:
                result.append(a)
    return result
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(n) space
# Idea: Hash set membership
def intersection(nums1, nums2):
    return list(set(nums1) & set(nums2))
""",
    ),
    # ---- Intersection of Two Arrays II (LeetCode 350) ----
    dict(
        title="Intersection of Two Arrays II",
        diff="E",
        lc=350,
        slug="intersection-of-two-arrays-ii",
        prompt=(
            "Return the intersection of two arrays as a multiset: each value appears as many times as it appears in "
            "BOTH arrays (any order)."
        ),
        sig="def intersect(nums1: List[int], nums2: List[int]) -> List[int]:",
        fn="intersect",
        compare="unordered",
        tests=[
            (([1, 2, 2, 1], [2, 2]), [2, 2]),
            (([4, 9, 5], [9, 4, 9, 8, 4]), [4, 9]),
            (([1], [2]), []),
            (([1, 1], [1]), [1]),
        ],
        hints=[
            "Duplicates now matter: a value should appear min(count in nums1, count in nums2) times.",
            "Count one array with a Counter.",
            "Walk the other array; if the counter still has the value, output it and decrement the counter.",
        ],
        pattern="Frequency counter consumed as you match",
        explain=(
            "Decrementing the counter on every match makes sure a value is never matched more times than it occurs "
            "in the first array."
        ),
        cx="O(n + m) time, O(min(n, m)) space",
        brute_cx="O(n * m) time - find and remove each match from a copy",
        brute=r"""
# BRUTE FORCE: O(n * m) time - find and remove each match from a copy
def intersect(nums1, nums2):
    remaining, result = list(nums2), []
    for x in nums1:
        if x in remaining:
            remaining.remove(x)  # use this occurrence up
            result.append(x)
    return result
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(min(n, m)) space
# Idea: Frequency counter consumed as you match
def intersect(nums1, nums2):
    counts, result = Counter(nums1), []
    for x in nums2:
        if counts[x] > 0:
            counts[x] -= 1
            result.append(x)
    return result
""",
    ),
    # ---- First Unique Character in a String (LeetCode 387) ----
    dict(
        title="First Unique Character in a String",
        diff="E",
        lc=387,
        slug="first-unique-character-in-a-string",
        prompt="Return the index of the first character that appears exactly once in s, or -1 if there is none.",
        sig="def first_uniq_char(s: str) -> int:",
        fn="first_uniq_char",
        tests=[
            (("leetcode",), 0),
            (("loveleetcode",), 2),
            (("aabb",), -1),
            (("z",), 0),
        ],
        hints=[
            "You need to know the TOTAL count of each character before deciding.",
            "First pass: count every character.",
            "Second pass: return the first index whose character has count 1.",
        ],
        pattern="Two passes: count, then find",
        explain=(
            "Counting first turns 'is it unique anywhere?' into a lookup, so each character is examined a constant "
            "number of times."
        ),
        cx="O(n) time, O(1) space (26 letters)",
        brute_cx="O(n^2) time - count each character with a scan",
        brute=r"""
# BRUTE FORCE: O(n^2) time - count each character with a scan
def first_uniq_char(s):
    for i, ch in enumerate(s):
        if s.count(ch) == 1:  # a full scan for every character
            return i
    return -1
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space (26 letters)
# Idea: Two passes: count, then find
def first_uniq_char(s):
    counts = Counter(s)
    for i, ch in enumerate(s):
        if counts[ch] == 1:
            return i
    return -1
""",
    ),
    # ---- Isomorphic Strings (LeetCode 205) ----
    dict(
        title="Isomorphic Strings",
        diff="E",
        lc=205,
        slug="isomorphic-strings",
        prompt=(
            "Two strings are isomorphic if the characters of s can be replaced one-to-one to get t (the order is "
            "preserved; no two characters may map to the same one). Return whether s and t are isomorphic."
        ),
        sig="def is_isomorphic(s: str, t: str) -> bool:",
        fn="is_isomorphic",
        tests=[
            (("egg", "add"), True),
            (("foo", "bar"), False),
            (("paper", "title"), True),
            (("badc", "baba"), False),
        ],
        hints=[
            "A mapping from s to t must never send one s-character to two different t-characters.",
            "It must also be injective: two different s-characters cannot share a t-character.",
            "Keep two dictionaries (s -> t and t -> s) and check both directions at every position.",
        ],
        pattern="Bijection check with two hash maps",
        explain=(
            "Checking only one direction would accept 'badc' -> 'baba' (a and c both map to a). The reverse map "
            "catches that."
        ),
        cx="O(n) time, O(1) space for a fixed alphabet",
        brute_cx="O(n^2) time - compare the first-occurrence index patterns",
        brute=r"""
# BRUTE FORCE: O(n^2) time - compare the first-occurrence index patterns
def is_isomorphic(s, t):
    if len(s) != len(t):
        return False
    # "pattern" of a string: where each character first appeared (O(n) per index() call)
    return [s.index(c) for c in s] == [t.index(c) for c in t]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space for a fixed alphabet
# Idea: Bijection check with two hash maps
def is_isomorphic(s, t):
    if len(s) != len(t):
        return False
    s_to_t, t_to_s = {}, {}
    for a, b in zip(s, t):
        if s_to_t.setdefault(a, b) != b or t_to_s.setdefault(b, a) != a:
            return False  # a conflict in either direction
    return True
""",
    ),
    # ---- Word Pattern (LeetCode 290) ----
    dict(
        title="Word Pattern",
        diff="E",
        lc=290,
        slug="word-pattern",
        prompt=(
            "Return True if the words of s follow the same pattern as the letters of pattern: a bijection between "
            "pattern letters and words."
        ),
        sig="def word_pattern(pattern: str, s: str) -> bool:",
        fn="word_pattern",
        tests=[
            (("abba", "dog cat cat dog"), True),
            (("abba", "dog cat cat fish"), False),
            (("aaaa", "dog cat cat dog"), False),
            (("abba", "dog dog dog dog"), False),
        ],
        hints=[
            "This is Isomorphic Strings, but the right-hand side is a list of words.",
            "Split s into words; the counts must match.",
            "Maintain two maps (letter -> word and word -> letter) and reject any conflict.",
        ],
        pattern="Bijection check with two hash maps",
        explain="Same two-way mapping idea; the second map prevents two different letters from sharing one word.",
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - compare first-occurrence index patterns",
        brute=r"""
# BRUTE FORCE: O(n^2) time - compare first-occurrence index patterns
def word_pattern(pattern, s):
    words = s.split()
    if len(words) != len(pattern):
        return False
    return [pattern.index(c) for c in pattern] == [words.index(w) for w in words]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Bijection check with two hash maps
def word_pattern(pattern, s):
    words = s.split()
    if len(words) != len(pattern):
        return False
    letter_to_word, word_to_letter = {}, {}
    for letter, word in zip(pattern, words):
        if (
            letter_to_word.setdefault(letter, word) != word
            or word_to_letter.setdefault(word, letter) != letter
        ):
            return False
    return True
""",
    ),
]
