"""more String problems (batch 4) - part of the problem bank for the "strings" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Length of Last Word (LeetCode 58) ----
    dict(
        title="Length of Last Word",
        diff="E",
        lc=58,
        slug="length-of-last-word",
        prompt=(
            "Return the length of the last word in s (words are separated by spaces; there may be leading or "
            "trailing spaces)."
        ),
        sig="def length_of_last_word(s: str) -> int:",
        fn="length_of_last_word",
        tests=[
            (("Hello World",), 5),
            (("   fly me   to   the moon  ",), 4),
            (("luffy is still joyboy",), 6),
            (("a",), 1),
        ],
        hints=[
            "Only the END of the string matters - there is no need to look at the front.",
            "Skip trailing spaces first.",
            "Then count characters until you hit a space or the start of the string.",
        ],
        pattern="Scan from the end",
        explain=(
            "Splitting the whole string allocates a list of every word just to read the last one. Walking back from "
            "the end touches only the characters you need."
        ),
        cx="O(length of the trailing part) time, O(1) space",
        brute_cx="O(n) time and O(n) space - split into words",
        brute=r"""
# BRUTE FORCE: O(n) time and O(n) space - split into words
def length_of_last_word(s):
    return len(s.split()[-1])
""",
        solution=r"""
# OPTIMISED: O(length of the trailing part) time, O(1) space
# Idea: Scan from the end
def length_of_last_word(s):
    i = len(s) - 1

    while s[i] == " ":  # skip trailing spaces
        i -= 1

    length = 0

    while i >= 0 and s[i] != " ":
        length += 1
        i -= 1

    return length
""",
    ),
    # ---- Compare Version Numbers (LeetCode 165) ----
    dict(
        title="Compare Version Numbers",
        diff="M",
        lc=165,
        slug="compare-version-numbers",
        prompt=(
            "Compare dotted version strings like '1.01.2'. Return -1 if version1 < version2, 1 if version1 > "
            "version2, otherwise 0. Leading zeros are ignored and missing parts count as 0."
        ),
        sig="def compare_version(version1: str, version2: str) -> int:",
        fn="compare_version",
        tests=[
            (("1.2", "1.10"), -1),
            (("1.01", "1.001"), 0),
            (("1.0", "1.0.0.0"), 0),
            (("0.1", "1.1"), -1),
            (("1.0.1", "1"), 1),
        ],
        hints=[
            "Compare part by part, as integers (so '01' equals '1').",
            "If one version has fewer parts, treat the missing parts as 0.",
            "Split by '.', then walk up to the longer length comparing int(part or 0).",
        ],
        pattern="Parse and compare component by component",
        explain=(
            "'1.0' and '1.0.0' are equal because absent components default to 0. Padding the shorter list (or using "
            "0 for missing indexes) handles that uniformly."
        ),
        cx="O(n + m) time",
        brute_cx="O(n + m) time - split, pad the shorter list, then compare",
        brute=r"""
# BRUTE FORCE: O(n + m) time - split, pad the shorter list, then compare
def compare_version(version1, version2):
    a = [int(x) for x in version1.split(".")]
    b = [int(x) for x in version2.split(".")]
    size = max(len(a), len(b))
    a += [0] * (size - len(a))  # pad with zeros so the lists line up
    b += [0] * (size - len(b))

    if a < b:
        return -1

    return 1 if a > b else 0
""",
        solution=r"""
# OPTIMISED: O(n + m) time
# Idea: Parse and compare component by component
def compare_version(version1, version2):
    i = j = 0

    while i < len(version1) or j < len(version2):
        num1 = num2 = 0

        while i < len(version1) and version1[i] != ".":  # read one component without splitting
            num1 = num1 * 10 + int(version1[i])
            i += 1

        while j < len(version2) and version2[j] != ".":
            num2 = num2 * 10 + int(version2[j])
            j += 1

        if num1 != num2:
            return -1 if num1 < num2 else 1

        i += 1  # skip the dot
        j += 1

    return 0
""",
    ),
    # ---- Number of Segments in a String (LeetCode 434) ----
    dict(
        title="Number of Segments in a String",
        diff="E",
        lc=434,
        slug="number-of-segments-in-a-string",
        prompt="A segment is a run of non-space characters. Return the number of segments in s.",
        sig="def count_segments(s: str) -> int:",
        fn="count_segments",
        tests=[
            (("Hello, my name is John",), 5),
            (("Hello",), 1),
            (("",), 0),
            (("    ",), 0),
            ((" a  b ",), 2),
        ],
        hints=[
            "A segment starts where a non-space character follows a space (or the string start).",
            "Count those start positions.",
            "Check s[i] != ' ' and (i == 0 or s[i - 1] == ' ').",
        ],
        pattern="Count boundaries instead of building pieces",
        explain="Counting the beginnings of runs needs no extra memory, unlike creating the list of words.",
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time and O(n) space - split and count",
        brute=r"""
# BRUTE FORCE: O(n) time and O(n) space - split and count
def count_segments(s):
    return len(s.split())
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Count boundaries instead of building pieces
def count_segments(s):
    return sum(1 for i, ch in enumerate(s) if ch != " " and (i == 0 or s[i - 1] == " "))
""",
    ),
    # ---- Reverse String II (LeetCode 541) ----
    dict(
        title="Reverse String II",
        diff="E",
        lc=541,
        slug="reverse-string-ii",
        prompt=(
            "For every block of 2k characters, reverse the first k. If fewer than k characters remain, reverse them "
            "all; if between k and 2k remain, reverse only the first k."
        ),
        sig="def reverse_str(s: str, k: int) -> str:",
        fn="reverse_str",
        tests=[
            (("abcdefg", 2), "bacdfeg"),
            (("abcd", 2), "bacd"),
            (("abcdefgh", 3), "cbadefhg"),
            (("a", 5), "a"),
        ],
        hints=[
            "Jump through the string in steps of 2k.",
            "At each start i, the chunk to reverse is s[i : i + k] (slicing past the end is safe in Python).",
            "Rebuild: reversed chunk + the untouched next k characters.",
        ],
        pattern="Stride through blocks and slice",
        explain=(
            "Python slicing clamps at the end of the string, which takes care of both 'fewer than k' cases without "
            "special code."
        ),
        cx="O(n) time",
        brute_cx="O(n) time - swap characters one by one in a list",
        brute=r"""
# BRUTE FORCE: O(n) time - swap characters one by one in a list
def reverse_str(s, k):
    chars = list(s)

    for start in range(0, len(chars), 2 * k):
        i, j = start, min(start + k, len(chars)) - 1
        while i < j:  # two-pointer swap inside the first k characters of the block
            chars[i], chars[j] = chars[j], chars[i]
            i += 1
            j -= 1

    return "".join(chars)
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Stride through blocks and slice
def reverse_str(s, k):
    pieces = []
    for start in range(0, len(s), 2 * k):
        pieces.append(s[start : start + k][::-1])  # reversed first k
        pieces.append(s[start + k : start + 2 * k])  # next k untouched
    return "".join(pieces)
""",
    ),
    # ---- Reverse Words in a String III (LeetCode 557) ----
    dict(
        title="Reverse Words in a String III",
        diff="E",
        lc=557,
        slug="reverse-words-in-a-string-iii",
        prompt=(
            "Reverse the characters of each word in s, keeping the words in their original order and the spaces as "
            "they are."
        ),
        sig="def reverse_words(s: str) -> str:",
        fn="reverse_words",
        tests=[
            (("Let's take LeetCode contest",), "s'teL ekat edoCteeL tsetnoc"),
            (("God Ding",), "doG gniD"),
            (("a",), "a"),
            (("ab cd",), "ba dc"),
        ],
        hints=[
            "Reverse each word separately.",
            "Split on ' ', reverse every piece, join with ' '.",
            "In-place version: find each word's [start, end] and swap characters with two pointers.",
        ],
        pattern="Per-word two-pointer reversal",
        explain=(
            "The word order never changes, so the task decomposes into independent reversals - each a classic "
            "two-pointer swap."
        ),
        cx="O(n) time",
        brute_cx="O(n) time - split, reverse each word with slicing, join",
        brute=r"""
# BRUTE FORCE: O(n) time - split, reverse each word with slicing, join
def reverse_words(s):
    return " ".join(word[::-1] for word in s.split(" "))
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Per-word two-pointer reversal
def reverse_words(s):
    chars, start = list(s), 0

    for i in range(len(chars) + 1):
        if i == len(chars) or chars[i] == " ":  # the word chars[start..i-1] ends here
            lo, hi = start, i - 1
            while lo < hi:
                chars[lo], chars[hi] = chars[hi], chars[lo]
                lo += 1
                hi -= 1
            start = i + 1

    return "".join(chars)
""",
    ),
    # ---- Merge Strings Alternately (LeetCode 1768) ----
    dict(
        title="Merge Strings Alternately",
        diff="E",
        lc=1768,
        slug="merge-strings-alternately",
        prompt=(
            "Merge two strings by taking letters alternately, starting with word1. When one string runs out, append "
            "the rest of the other."
        ),
        sig="def merge_alternately(word1: str, word2: str) -> str:",
        fn="merge_alternately",
        tests=[
            (("abc", "pqr"), "apbqcr"),
            (("ab", "pqrs"), "apbqrs"),
            (("abcd", "pq"), "apbqcd"),
            (("", "xy"), "xy"),
        ],
        hints=[
            "Walk both strings with the same index i.",
            "At each i append word1[i] if it exists, then word2[i] if it exists.",
            "Loop to the length of the LONGER string.",
        ],
        pattern="Parallel iteration with bounds checks",
        explain=(
            "A single loop up to max(len) with two guarded appends handles every length combination without extra "
            "branches for the leftovers."
        ),
        cx="O(n + m) time",
        brute_cx="O(n + m) time - merge the overlap, then append the remainder separately",
        brute=r"""
# BRUTE FORCE: O(n + m) time - merge the overlap, then append the remainder separately
def merge_alternately(word1, word2):
    out, i = [], 0
    while i < len(word1) and i < len(word2):  # the part where both strings still have letters
        out.append(word1[i])
        out.append(word2[i])
        i += 1
    return "".join(out) + word1[i:] + word2[i:]  # one of these two is empty
""",
        solution=r"""
# OPTIMISED: O(n + m) time
# Idea: Parallel iteration with bounds checks
def merge_alternately(word1, word2):
    out = []
    for i in range(max(len(word1), len(word2))):
        if i < len(word1):
            out.append(word1[i])
        if i < len(word2):
            out.append(word2[i])
    return "".join(out)
""",
    ),
    # ---- Shortest Palindrome (LeetCode 214) ----
    dict(
        title="Shortest Palindrome",
        diff="H",
        lc=214,
        slug="shortest-palindrome",
        prompt="You may add characters only at the FRONT of s. Return the shortest palindrome you can create.",
        sig="def shortest_palindrome(s: str) -> str:",
        fn="shortest_palindrome",
        tests=[
            (("aacecaaa",), "aaacecaaa"),
            (("abcd",), "dcbabcd"),
            (("",), ""),
            (("a",), "a"),
            (("aba",), "aba"),
        ],
        hints=[
            "Find the longest palindromic PREFIX of s. The rest of s, reversed, goes in front.",
            "Checking each prefix directly is O(n^2).",
            (
                "Build t = s + '#' + reverse(s) and compute the KMP failure array: its last value is the length of "
                "the longest prefix of s that is also a suffix of reverse(s) - i.e. the palindromic prefix."
            ),
        ],
        pattern="KMP failure function to find the longest palindromic prefix",
        explain=(
            "A prefix of s is a palindrome exactly when it equals the matching suffix of reverse(s). The separator "
            "'#' stops the match from running past s, and the KMP table finds the longest such overlap in linear "
            "time."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - test each prefix for being a palindrome",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test each prefix for being a palindrome
def shortest_palindrome(s):
    for end in range(len(s), 0, -1):  # longest prefix first
        prefix = s[:end]
        if prefix == prefix[::-1]:
            return s[end:][::-1] + s  # mirror the remaining tail onto the front
    return s
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: KMP failure function to find the longest palindromic prefix
def shortest_palindrome(s):
    t = s + "#" + s[::-1]
    fail = [0] * len(t)  # fail[i] = longest proper prefix of t[:i+1] that is also its suffix

    for i in range(1, len(t)):
        k = fail[i - 1]
        while k and t[i] != t[k]:
            k = fail[k - 1]
        if t[i] == t[k]:
            k += 1
        fail[i] = k

    longest_pal_prefix = fail[-1]

    return s[longest_pal_prefix:][::-1] + s
""",
    ),
]
