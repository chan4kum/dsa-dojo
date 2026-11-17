"""Strings problems - the problem bank for the "strings" topic.

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
    # ---- Find the Index of the First Occurrence in a String (LeetCode 28) ----
    dict(
        title="Find the Index of the First Occurrence in a String",
        diff="E",
        lc=28,
        slug="find-the-index-of-the-first-occurrence-in-a-string",
        prompt=(
            "Return the index of the first occurrence of needle in haystack, or -1. (Empty needle -> 0.) Implement "
            "it yourself rather than with str.find; aim for O(n + m) using KMP."
        ),
        sig="def str_str(haystack: str, needle: str) -> int:",
        fn="str_str",
        tests=[
            (("sadbutsad", "sad"), 0),
            (("leetcode", "leeto"), -1),
            (("hello", "ll"), 2),
            (("a", "a"), 0),
            (("mississippi", "issip"), 4),
            (("aaa", "aaaa"), -1),
            (("abc", ""), 0),
        ],
        hints=[
            "Naive matching restarts from the next index after a mismatch: O(n*m) worst case.",
            (
                "After a partial match you already know some characters. The 'failure function' says how much of "
                "the needle's own prefix is still matched."
            ),
            (
                "pi[i] = length of the longest proper prefix of needle[:i+1] that is also its suffix. On a mismatch "
                "fall back to pi[k-1] instead of restarting."
            ),
        ],
        pattern="KMP / prefix function (reuse knowledge from partial matches)",
        explain=(
            "Build pi for needle + '#' + haystack; wherever pi equals len(needle) the needle ends there. The "
            "inner\n        while-loop looks nested but k only ever decreases as much as it has increased, so total "
            "O(n + m)\n        (amortised, like the monotonic stack)."
        ),
        cx="O(n + m) time (KMP)",
        brute_cx="O(n*m) - compare at every offset",
        brute=r"""
# BRUTE FORCE: O(n*m) - compare at every offset
def str_str(haystack, needle):
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i : i + len(needle)] == needle:
            return i
    return -1
""",
        solution=r"""
# OPTIMISED: O(n + m) time (KMP)
# Idea: KMP / prefix function (reuse knowledge from partial matches)
def str_str(haystack, needle):
    if not needle:
        return 0

    m = len(needle)
    s = needle + "#" + haystack
    pi = [0] * len(s)

    for i in range(1, len(s)):
        k = pi[i - 1]

        while k and s[i] != s[k]:
            k = pi[k - 1]  # fall back, do not restart

        if s[i] == s[k]:
            k += 1

        pi[i] = k

        if k == m:
            return i - 2 * m  # match ends at i in s; start inside haystack

    return -1
""",
    ),
    # ---- Longest Happy Prefix (LeetCode 1392) ----
    dict(
        title="Longest Happy Prefix",
        diff="H",
        lc=1392,
        slug="longest-happy-prefix",
        prompt=(
            "A 'happy prefix' is a non-empty prefix that is also a suffix (but not the whole string). Return the "
            "longest one, or '' if none exists."
        ),
        sig="def longest_prefix(s: str) -> str:",
        fn="longest_prefix",
        tests=[
            (("level",), "l"),
            (("ababab",), "abab"),
            (("abc",), ""),
            (("a",), ""),
            (("aaaa",), "aaa"),
            (("abcabcabc",), "abcabc"),
        ],
        hints=[
            "Comparing every prefix with the matching suffix is O(n^2).",
            "This is exactly what the KMP prefix function stores.",
            "Compute pi for s; the answer is s[:pi[-1]].",
        ],
        pattern="Prefix function (border of a string)",
        explain=(
            "pi[i] is the length of the longest proper border (prefix = suffix) of s[:i+1]. The last entry is "
            "the\n        border of the full string. O(n)."
        ),
        cx="O(n) time, O(n) space (prefix function)",
        brute_cx="O(n^2) - try every length from longest",
        brute=r"""
# BRUTE FORCE: O(n^2) - try every length from longest
def longest_prefix(s):
    for L in range(len(s) - 1, 0, -1):
        if s[:L] == s[-L:]:
            return s[:L]
    return ""
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space (prefix function)
# Idea: Prefix function (border of a string)
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
""",
    ),
]
