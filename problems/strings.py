from core import *

PROBLEMS = [
    dict(
        title="Find the Index of the First Occurrence in a String", diff="E", lc=28,
        slug="find-the-index-of-the-first-occurrence-in-a-string",
        prompt="Return the index of the first occurrence of needle in haystack, or -1. (Empty needle -> 0.) "
               "Implement it yourself rather than with str.find; aim for O(n + m) using KMP.",
        sig="def str_str(haystack: str, needle: str) -> int:",
        fn="str_str",
        tests=[(("sadbutsad", "sad"), 0), (("leetcode", "leeto"), -1), (("hello", "ll"), 2), (("a", "a"), 0),
               (("mississippi", "issip"), 4), (("aaa", "aaaa"), -1), (("abc", ""), 0)],
        hints=["Naive matching restarts from the next index after a mismatch: O(n*m) worst case.",
               "After a partial match you already know some characters. The 'failure function' says how much of the needle's own prefix is still matched.",
               "pi[i] = length of the longest proper prefix of needle[:i+1] that is also its suffix. On a mismatch fall back to pi[k-1] instead of restarting."],
        pattern="KMP / prefix function (reuse knowledge from partial matches)",
        explain="""
        Build pi for needle + '#' + haystack; wherever pi equals len(needle) the needle ends there. The inner
        while-loop looks nested but k only ever decreases as much as it has increased, so total O(n + m)
        (amortised, like the monotonic stack).""",
        solution=r'''
def str_str(haystack, needle):
    if not needle:
        return 0
    m = len(needle)
    s = needle + "#" + haystack
    pi = [0] * len(s)
    for i in range(1, len(s)):
        k = pi[i - 1]
        while k and s[i] != s[k]:
            k = pi[k - 1]                # fall back, do not restart
        if s[i] == s[k]:
            k += 1
        pi[i] = k
        if k == m:
            return i - 2 * m             # match ends at i in s; start inside haystack
    return -1
''',
    ),
    dict(
        title="Longest Happy Prefix", diff="H", lc=1392, slug="longest-happy-prefix",
        prompt="A 'happy prefix' is a non-empty prefix that is also a suffix (but not the whole string). "
               "Return the longest one, or '' if none exists.",
        sig="def longest_prefix(s: str) -> str:",
        fn="longest_prefix",
        tests=[(("level",), "l"), (("ababab",), "abab"), (("abc",), ""), (("a",), ""), (("aaaa",), "aaa"), (("abcabcabc",), "abcabc")],
        hints=["Comparing every prefix with the matching suffix is O(n^2).",
               "This is exactly what the KMP prefix function stores.",
               "Compute pi for s; the answer is s[:pi[-1]]."],
        pattern="Prefix function (border of a string)",
        explain="""
        pi[i] is the length of the longest proper border (prefix = suffix) of s[:i+1]. The last entry is the
        border of the full string. O(n).""",
        solution=r'''
def longest_prefix(s):
    pi = [0] * len(s)
    for i in range(1, len(s)):
        k = pi[i - 1]
        while k and s[i] != s[k]:
            k = pi[k - 1]
        if s[i] == s[k]:
            k += 1
        pi[i] = k
    return s[: pi[-1]] if s else ""
''',
    ),
]
