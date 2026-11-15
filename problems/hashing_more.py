from core import *

PROBLEMS = [
    dict(
        title="Contains Duplicate", diff="E", lc=217, slug="contains-duplicate",
        prompt="Return True if any value appears at least twice in the array.",
        sig="def contains_duplicate(nums: List[int]) -> bool:", fn="contains_duplicate",
        tests=[(([1, 2, 3, 1],), True), (([1, 2, 3, 4],), False), (([1, 1, 1, 3, 3, 4, 3, 2, 4, 2],), True), (([],), False), (([7],), False)],
        hints=["Brute force compares every pair. What do you really need to know about each value?",
               "'Have I seen this value before?' - a membership question.",
               "Walk once, keep a set; the first value already in the set is a duplicate. (Or compare len(set(nums)) with len(nums).)"],
        pattern="Hash set: O(1) 'seen before?'",
        explain="""
        A set answers membership in O(1) on average, so one pass suffices. Sorting first (O(n log n), O(1) extra
        space) is the in-place alternative: duplicates become neighbours.""",
        cx="O(n) time, O(n) space", brute_cx="O(n^2) time, O(1) space - compare every pair",
        brute=r'''
def contains_duplicate(nums):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                return True
    return False
''',
        solution=r'''
def contains_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False
''',
    ),
    dict(
        title="Valid Anagram", diff="E", lc=242, slug="valid-anagram",
        prompt="Return True if t is a rearrangement of the letters of s.",
        sig="def is_anagram(s: str, t: str) -> bool:", fn="is_anagram",
        tests=[(("anagram", "nagaram"), True), (("rat", "car"), False), (("a", "a"), True), (("ab", "a"), False), (("", ""), True)],
        hints=["Two strings are anagrams exactly when every letter occurs the same number of times in both.",
               "Either sort both and compare, or count letters.",
               "Counter(s) == Counter(t), or a 26-slot array: +1 for s, -1 for t, all zeros at the end."],
        pattern="Frequency counting (canonical form of a multiset)",
        explain="""
        An anagram class is identified by its letter counts. Counting is O(n); sorting is O(n log n) but needs no
        extra structure. The same canonical-key idea powers Group Anagrams.""",
        cx="O(n) time, O(1) space (alphabet is fixed)", brute_cx="O(n log n) time - sort both strings",
        brute=r'''
def is_anagram(s, t):
    return sorted(s) == sorted(t)
''',
        solution=r'''
def is_anagram(s, t):
    if len(s) != len(t):
        return False
    count = Counter(s)
    for ch in t:
        count[ch] -= 1
        if count[ch] < 0:
            return False
    return True
''',
    ),
    dict(
        title="Isomorphic Strings", diff="E", lc=205, slug="isomorphic-strings",
        prompt="Two strings are isomorphic if the characters of s can be replaced to get t, with a consistent one-to-one "
               "mapping (no two characters map to the same character). Decide if s and t are isomorphic.",
        sig="def is_isomorphic(s: str, t: str) -> bool:", fn="is_isomorphic",
        tests=[(("egg", "add"), True), (("foo", "bar"), False), (("paper", "title"), True), (("badc", "baba"), False), (("ab", "aa"), False)],
        hints=["Which consistency must hold in BOTH directions?",
               "Keep a map s->t and a map t->s. A conflict in either means False.",
               "Alternative: map each char to the index of its first occurrence; two strings are isomorphic iff those patterns are equal."],
        pattern="Bijection check with two hash maps (or normalised pattern)",
        explain="""
        One map only checks functions (same letter -> same letter). 'Two different letters never share a target'
        needs the reverse map too. Normalising both strings to 'first-occurrence index' patterns is a neat one-liner.""",
        cx="O(n) time, O(1)-O(n) space", brute_cx="O(n^2) time - compare every pair of positions",
        brute=r'''
def is_isomorphic(s, t):
    if len(s) != len(t):
        return False
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            if (s[i] == s[j]) != (t[i] == t[j]):
                return False
    return True
''',
        solution=r'''
def is_isomorphic(s, t):
    if len(s) != len(t):
        return False
    s2t, t2s = {}, {}
    for a, b in zip(s, t):
        if s2t.setdefault(a, b) != b or t2s.setdefault(b, a) != a:
            return False
    return True
''',
    ),
]
