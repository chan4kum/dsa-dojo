"""more String problems (batch 5) - part of the problem bank for the "strings" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Add Binary (LeetCode 67) ----
    dict(
        title="Add Binary",
        diff="E",
        lc=67,
        slug="add-binary",
        prompt="Given two binary strings, return their sum as a binary string.",
        sig="def add_binary(a: str, b: str) -> str:",
        fn="add_binary",
        tests=[
            (("11", "1"), "100"),
            (("1010", "1011"), "10101"),
            (("0", "0"), "0"),
            (("1", "1"), "10"),
            (("111", "111"), "1110"),
        ],
        hints=[
            "Python can convert with int(x, 2) and bin(), but the interesting version works digit by digit.",
            "Add from the right, like on paper: digit_a + digit_b + carry.",
            "Output (sum % 2), carry = sum // 2; after the loop append a leftover carry; reverse the result.",
        ],
        pattern="Schoolbook addition with a carry",
        explain=(
            "Each column's total is at most 1 + 1 + 1 = 3, so the digit is total % 2 and the carry total // 2. "
            "Digits are produced right to left, hence the final reverse."
        ),
        cx="O(max(m, n)) time",
        brute_cx="O(m + n) time - convert both to integers, add, convert back (relies on big integers)",
        brute=r"""
# BRUTE FORCE: O(m + n) time - convert both to integers, add, convert back (relies on big integers)
def add_binary(a, b):
    return bin(int(a, 2) + int(b, 2))[2:]
""",
        solution=r"""
# OPTIMISED: O(max(m, n)) time
# Idea: Schoolbook addition with a carry
def add_binary(a, b):
    out, carry = [], 0
    i, j = len(a) - 1, len(b) - 1
    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += int(a[i])
            i -= 1
        if j >= 0:
            total += int(b[j])
            j -= 1
        out.append(str(total % 2))
        carry = total // 2
    return "".join(reversed(out))
""",
    ),
    # ---- License Key Formatting (LeetCode 482) ----
    dict(
        title="License Key Formatting",
        diff="E",
        lc=482,
        slug="license-key-formatting",
        prompt=(
            "s contains letters, digits and dashes. Remove the dashes, uppercase the letters and regroup the "
            "characters into groups of k separated by dashes; only the FIRST group may be shorter (but not empty)."
        ),
        sig="def license_key_formatting(s: str, k: int) -> str:",
        fn="license_key_formatting",
        tests=[
            (("5F3Z-2e-9-w", 4), "5F3Z-2E9W"),
            (("2-5g-3-J", 2), "2-5G-3J"),
            (("---", 3), ""),
            (("a-a-a-a-", 1), "A-A-A-A"),
            (("abc", 5), "ABC"),
        ],
        hints=[
            "First clean the string: drop dashes and uppercase it.",
            "Working from the RIGHT makes every full group of k easy; the leftover goes to the front.",
            "Walk backwards, appending characters and a dash after every k of them; strip a trailing dash and reverse.",
        ],
        pattern="Build from the right so the short group lands in front",
        explain="Cutting groups from the end guarantees all groups but the first have exactly k characters.",
        cx="O(n) time",
        brute_cx="O(n) time - compute the first group's size from the length, then slice",
        brute=r"""
# BRUTE FORCE: O(n) time - compute the first group's size from the length, then slice
def license_key_formatting(s, k):
    chars = s.replace("-", "").upper()
    if not chars:
        return ""
    first = len(chars) % k or k  # size of the leading group
    groups = [chars[:first]] + [chars[i : i + k] for i in range(first, len(chars), k)]
    return "-".join(groups)
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Build from the right so the short group lands in front
def license_key_formatting(s, k):
    out, count = [], 0
    for ch in reversed(s):
        if ch == "-":
            continue
        if count == k:
            out.append("-")  # a full group of k has been written
            count = 0
        out.append(ch.upper())
        count += 1
    return "".join(reversed(out))
""",
    ),
    # ---- Detect Capital (LeetCode 520) ----
    dict(
        title="Detect Capital",
        diff="E",
        lc=520,
        slug="detect-capital",
        prompt=(
            "Return True if the word uses capitals correctly: all capitals, no capitals, or only the first letter "
            "capital."
        ),
        sig="def detect_capital_use(word: str) -> bool:",
        fn="detect_capital_use",
        tests=[
            (("USA",), True),
            (("FlaG",), False),
            (("leetcode",), True),
            (("Google",), True),
            (("gOogle",), False),
            (("A",), True),
        ],
        hints=[
            "There are exactly three allowed shapes.",
            "Count the uppercase letters.",
            "Valid when count == 0, count == len(word), or count == 1 and the first letter is the capital.",
        ],
        pattern="Count and compare against the allowed patterns",
        explain="Counting capitals once reduces the three shapes to three simple conditions.",
        cx="O(n) time",
        brute_cx="O(n) time - compare against the three transformed versions of the word",
        brute=r"""
# BRUTE FORCE: O(n) time - compare against the three transformed versions of the word
def detect_capital_use(word):
    return (
        word == word.upper() or word == word.lower() or word == word[0].upper() + word[1:].lower()
    )
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Count and compare against the allowed patterns
def detect_capital_use(word):
    caps = sum(1 for ch in word if ch.isupper())
    return caps == 0 or caps == len(word) or (caps == 1 and word[0].isupper())
""",
    ),
    # ---- Student Attendance Record I (LeetCode 551) ----
    dict(
        title="Student Attendance Record I",
        diff="E",
        lc=551,
        slug="student-attendance-record-i",
        prompt=(
            "s uses 'A' (absent), 'L' (late) and 'P' (present). A student is eligible for an award if they have "
            "fewer than 2 absences AND never 3 or more consecutive lates. Return whether the record qualifies."
        ),
        sig="def check_record(s: str) -> bool:",
        fn="check_record",
        tests=[
            (("PPALLP",), True),
            (("PPALLL",), False),
            (("AA",), False),
            (("LLL",), False),
            (("PLPLP",), True),
            (("LLPLL",), True),
        ],
        hints=[
            "Two independent rules: count A's, and detect a run of L's.",
            "A single pass can keep an absence counter and the length of the current L streak.",
            "Reset the streak whenever you see a non-L; fail as soon as absences reach 2 or the streak reaches 3.",
        ],
        pattern="Single pass with counters",
        explain="Both rules are decided by running counters, so no substring search or second pass is needed.",
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time - two separate scans / substring tests",
        brute=r"""
# BRUTE FORCE: O(n) time - two separate scans / substring tests
def check_record(s):
    absences = sum(1 for ch in s if ch == "A")
    for i in range(len(s) - 2):
        if s[i : i + 3] == "LLL":
            return False
    return absences < 2
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Single pass with counters
def check_record(s):
    absences = streak = 0
    for ch in s:
        if ch == "A":
            absences += 1
            if absences == 2:
                return False
        streak = streak + 1 if ch == "L" else 0
        if streak == 3:
            return False
    return True
""",
    ),
    # ---- Greatest Common Divisor of Strings (LeetCode 1071) ----
    dict(
        title="Greatest Common Divisor of Strings",
        diff="E",
        lc=1071,
        slug="greatest-common-divisor-of-strings",
        prompt=(
            "t divides s if s is t repeated one or more times. Return the longest string x that divides both str1 "
            "and str2 (or '' if none)."
        ),
        sig="def gcd_of_strings(str1: str, str2: str) -> str:",
        fn="gcd_of_strings",
        tests=[
            (("ABCABC", "ABC"), "ABC"),
            (("ABABAB", "ABAB"), "AB"),
            (("LEET", "CODE"), ""),
            (("AAAA", "AA"), "AA"),
            (("ABC", "ABC"), "ABC"),
        ],
        hints=[
            "A common divisor must be a prefix of both strings; try prefixes of the shorter string, longest first.",
            "A common divisor exists only if str1 + str2 == str2 + str1 (both are powers of the same base).",
            "Then the answer's length is gcd(len1, len2): take that prefix.",
        ],
        pattern="Number theory on string lengths (gcd) + commutativity check",
        explain=(
            "If the strings are powers of one base, they commute under concatenation, and the longest common base "
            "has length gcd of the two lengths."
        ),
        cx="O(m + n) time",
        brute_cx="O(min(m, n) * (m + n)) time - test every prefix length",
        brute=r"""
# BRUTE FORCE: O(min(m, n) * (m + n)) time - test every prefix length
def gcd_of_strings(str1, str2):
    for length in range(min(len(str1), len(str2)), 0, -1):
        base = str1[:length]
        if len(str1) % length == 0 and len(str2) % length == 0:
            if base * (len(str1) // length) == str1 and base * (len(str2) // length) == str2:
                return base
    return ""
""",
        solution=r"""
# OPTIMISED: O(m + n) time
# Idea: Number theory on string lengths (gcd) + commutativity check
def gcd_of_strings(str1, str2):
    if str1 + str2 != str2 + str1:
        return ""  # no common base string
    return str1[: math.gcd(len(str1), len(str2))]
""",
    ),
    # ---- Minimum Number of Steps to Make Two Strings Anagram (LeetCode 1347) ----
    dict(
        title="Minimum Number of Steps to Make Two Strings Anagram",
        diff="M",
        lc=1347,
        slug="minimum-number-of-steps-to-make-two-strings-anagram",
        prompt=(
            "s and t have equal length. One step replaces any character of t with any other character. Return the "
            "minimum steps to make t an anagram of s."
        ),
        sig="def min_steps(s: str, t: str) -> int:",
        fn="min_steps",
        tests=[
            (("bab", "aba"), 1),
            (("leetcode", "practice"), 5),
            (("anagram", "mangaar"), 0),
            (("xxyyzz", "xxyyzz"), 0),
            (("friend", "family"), 4),
        ],
        hints=[
            "Characters that already match (as counts) never need changing.",
            "Compare letter frequencies of s and t.",
            "Sum, over every letter, how many MORE copies s has than t - those are the letters t must gain.",
        ],
        pattern="Frequency counting",
        explain=(
            "Each replacement fixes one missing letter; the total missing count is the sum of positive differences "
            "(it equals the sum of surplus letters)."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - match each character of s against a list copy of t",
        brute=r"""
# BRUTE FORCE: O(n^2) time - match each character of s against a list copy of t
def min_steps(s, t):
    remaining = list(t)
    unmatched = 0
    for ch in s:
        if ch in remaining:
            remaining.remove(ch)  # linear search and shift
        else:
            unmatched += 1
    return unmatched
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Frequency counting
def min_steps(s, t):
    diff = Counter(s) - Counter(t)  # keeps only the letters s has more of
    return sum(diff.values())
""",
    ),
    # ---- Increasing Decreasing String (LeetCode 1370) ----
    dict(
        title="Increasing Decreasing String",
        diff="E",
        lc=1370,
        slug="increasing-decreasing-string",
        prompt=(
            "Repeat until every character is used: take the smallest remaining character, then repeatedly the "
            "smallest one strictly greater than the last taken, until none; then take the largest remaining, then "
            "repeatedly the largest strictly smaller than the last, until none. Return the resulting string."
        ),
        sig="def sort_string(s: str) -> str:",
        fn="sort_string",
        tests=[
            (("aaaabbbbcccc",), "abccbaabccba"),
            (("rat",), "art"),
            (("leetcode",), "cdelotee"),
            (("ggggggg",), "ggggggg"),
            (("abc",), "abc"),
        ],
        hints=[
            "Only the number of copies of each letter matters, not their positions.",
            "Keep 26 counters.",
            (
                "Alternate sweeping a..z and z..a, taking one copy of each letter that still has a count, until the "
                "output is long enough."
            ),
        ],
        pattern="Counting sort with alternating sweeps",
        explain=(
            "'Smallest strictly greater than the last' is exactly one forward sweep over distinct remaining "
            "letters; the backward sweep is the mirror."
        ),
        cx="O(26 * n) time",
        brute_cx="O(n^2) time - repeatedly search and remove from a sorted list",
        brute=r"""
# BRUTE FORCE: O(n^2) time - repeatedly search and remove from a sorted list
def sort_string(s):
    remaining = sorted(s)
    out = []
    while remaining:
        for ch in sorted(set(remaining)):  # ascending pass: one copy of each distinct letter
            out.append(ch)
            remaining.remove(ch)
        for ch in sorted(set(remaining), reverse=True):  # descending pass
            out.append(ch)
            remaining.remove(ch)
    return "".join(out)
""",
        solution=r"""
# OPTIMISED: O(26 * n) time
# Idea: Counting sort with alternating sweeps
def sort_string(s):
    counts = [0] * 26
    for ch in s:
        counts[ord(ch) - 97] += 1
    out = []
    while len(out) < len(s):
        for i in range(26):  # ascending sweep
            if counts[i]:
                out.append(chr(97 + i))
                counts[i] -= 1
        for i in range(25, -1, -1):  # descending sweep
            if counts[i]:
                out.append(chr(97 + i))
                counts[i] -= 1
    return "".join(out)
""",
    ),
    # ---- Consecutive Characters (LeetCode 1446) ----
    dict(
        title="Consecutive Characters",
        diff="E",
        lc=1446,
        slug="consecutive-characters",
        prompt=(
            "The power of a string is the length of the longest substring made of one repeated character. Return it."
        ),
        sig="def max_power(s: str) -> int:",
        fn="max_power",
        tests=[
            (("leetcode",), 2),
            (("abbcccddddeeeeedcba",), 5),
            (("a",), 1),
            (("tourist",), 1),
            (("cc",), 2),
        ],
        hints=[
            "Expanding from every start works but repeats comparisons.",
            "A run only grows while the next character equals the previous one.",
            "One pass: if s[i] == s[i-1] extend the current run, otherwise restart at 1; track the maximum.",
        ],
        pattern="Run-length scan",
        explain="Each position either extends the current run or starts a new one, so one pass suffices.",
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - expand from every start index",
        brute=r"""
# BRUTE FORCE: O(n^2) time - expand from every start index
def max_power(s):
    best = 1
    for i in range(len(s)):
        j = i
        while j + 1 < len(s) and s[j + 1] == s[i]:
            j += 1
        best = max(best, j - i + 1)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Run-length scan
def max_power(s):
    best = run = 1
    for i in range(1, len(s)):
        run = run + 1 if s[i] == s[i - 1] else 1
        best = max(best, run)
    return best
""",
    ),
    # ---- Largest Substring Between Two Equal Characters (LeetCode 1624) ----
    dict(
        title="Largest Substring Between Two Equal Characters",
        diff="E",
        lc=1624,
        slug="largest-substring-between-two-equal-characters",
        prompt=(
            "Return the length of the longest substring between two equal characters (not counting those two), or "
            "-1 if no character repeats."
        ),
        sig="def max_length_between_equal_characters(s: str) -> int:",
        fn="max_length_between_equal_characters",
        tests=[
            (("aa",), 0),
            (("abca",), 2),
            (("cbzxy",), -1),
            (("cabbac",), 4),
            (("a",), -1),
        ],
        hints=[
            "Checking every pair of equal characters is O(n^2).",
            "For a fixed letter the best pair is its FIRST and LAST occurrence.",
            "Store each letter's first index; at every later occurrence update the best with i - first - 1.",
        ],
        pattern="First-occurrence hash map",
        explain="Remembering where each letter first appeared turns the pair search into one pass.",
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - every pair of positions",
        brute=r"""
# BRUTE FORCE: O(n^2) time - every pair of positions
def max_length_between_equal_characters(s):
    best = -1
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            if s[i] == s[j]:
                best = max(best, j - i - 1)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: First-occurrence hash map
def max_length_between_equal_characters(s):
    first, best = {}, -1
    for i, ch in enumerate(s):
        if ch in first:
            best = max(best, i - first[ch] - 1)
        else:
            first[ch] = i
    return best
""",
    ),
    # ---- Determine if String Halves Are Alike (LeetCode 1704) ----
    dict(
        title="Determine if String Halves Are Alike",
        diff="E",
        lc=1704,
        slug="determine-if-string-halves-are-alike",
        prompt=(
            "s has even length. Split it into two equal halves. Return True if both halves contain the same number "
            "of vowels (aeiou, either case)."
        ),
        sig="def halves_are_alike(s: str) -> bool:",
        fn="halves_are_alike",
        tests=[
            (("book",), True),
            (("textbook",), False),
            (("MerryChristmas",), False),
            (("AbCdEfGh",), True),
            (("aa",), True),
        ],
        hints=[
            "Count the vowels in each half.",
            "You can avoid slicing by walking one index over both halves.",
            (
                "Keep one balance: +1 for a vowel in the first half, -1 for a vowel in the second; the answer is "
                "balance == 0."
            ),
        ],
        pattern="Single pass with a running balance",
        explain="Equal counts means the signed total cancels to 0, so no second counter is necessary.",
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time, O(n) space - slice both halves and count each",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - slice both halves and count each
def halves_are_alike(s):
    vowels = set("aeiouAEIOU")
    half = len(s) // 2
    return sum(ch in vowels for ch in s[:half]) == sum(ch in vowels for ch in s[half:])
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Single pass with a running balance
def halves_are_alike(s):
    vowels, half, balance = set("aeiouAEIOU"), len(s) // 2, 0
    for i, ch in enumerate(s):
        if ch in vowels:
            balance += 1 if i < half else -1
    return balance == 0
""",
    ),
    # ---- Count Number of Homogenous Substrings (LeetCode 1759) ----
    dict(
        title="Count Number of Homogenous Substrings",
        diff="M",
        lc=1759,
        slug="count-number-of-homogenous-substrings",
        prompt=(
            "A homogenous string uses one repeated character. Return the number of homogenous substrings of s "
            "(equal substrings at different positions count separately), modulo 1_000_000_007."
        ),
        sig="def count_homogenous(s: str) -> int:",
        fn="count_homogenous",
        tests=[
            (("abbcccaa",), 13),
            (("xy",), 2),
            (("zzzzz",), 15),
            (("a",), 1),
            (("aab",), 4),
        ],
        hints=[
            "A run of L equal characters contributes L * (L + 1) / 2 homogenous substrings.",
            "Equivalently, a character ending a run of length r adds r new substrings.",
            "One pass: run = run + 1 if s[i] == s[i-1] else 1; total += run.",
        ],
        pattern="Run-length counting (substrings ending here)",
        explain=(
            "Every homogenous substring ends at some index; at index i there are exactly `run` of them, one per "
            "start inside the current run."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) or worse - test every substring",
        brute=r"""
# BRUTE FORCE: O(n^2) or worse - test every substring
def count_homogenous(s):
    total = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            if len(set(s[i : j + 1])) == 1:
                total += 1
    return total % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Run-length counting (substrings ending here)
def count_homogenous(s):
    total = run = 0
    for i, ch in enumerate(s):
        run = run + 1 if i and ch == s[i - 1] else 1  # homogenous substrings ending at i
        total += run
    return total % (10**9 + 7)
""",
    ),
    # ---- Find the Difference (LeetCode 389) ----
    dict(
        title="Find the Difference",
        diff="E",
        lc=389,
        slug="find-the-difference",
        prompt="t is s shuffled with exactly one extra letter inserted. Return the extra letter.",
        sig="def find_the_difference(s: str, t: str) -> str:",
        fn="find_the_difference",
        tests=[
            (("abcd", "abcde"), "e"),
            (("", "y"), "y"),
            (("a", "aa"), "a"),
            (("ae", "aea"), "a"),
        ],
        hints=[
            "Compare letter counts: the letter whose count differs is the answer.",
            "Better: sum the character codes of t and subtract those of s.",
            "XOR of every character code in s and t also cancels the pairs and leaves the extra letter.",
        ],
        pattern="XOR / sum cancellation",
        explain=(
            "Pairs cancel under XOR (a ^ a = 0), so only the unpaired extra letter remains; it needs O(1) extra space."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n log n) time - sort both and find the first mismatch",
        brute=r"""
# BRUTE FORCE: O(n log n) time - sort both and find the first mismatch
def find_the_difference(s, t):
    a, b = sorted(s), sorted(t)
    for i, ch in enumerate(a):
        if ch != b[i]:
            return b[i]
    return b[-1]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: XOR / sum cancellation
def find_the_difference(s, t):
    code = 0
    for ch in s + t:
        code ^= ord(ch)  # equal letters cancel in pairs
    return chr(code)
""",
    ),
    # ---- Longest Uncommon Subsequence I (LeetCode 521) ----
    dict(
        title="Longest Uncommon Subsequence I",
        diff="E",
        lc=521,
        slug="longest-uncommon-subsequence-i",
        prompt=(
            "An uncommon subsequence is a subsequence of one string that is NOT a subsequence of the other. Return "
            "the length of the longest one, or -1 if none exists."
        ),
        sig="def find_lus_length(a: str, b: str) -> int:",
        fn="find_lus_length",
        tests=[
            (("aba", "cdc"), 3),
            (("aaa", "bbb"), 3),
            (("aaa", "aaa"), -1),
            (("a", "ab"), 2),
            (("ab", "a"), 2),
        ],
        hints=[
            "The whole string is its own longest subsequence.",
            "If a == b every subsequence of one is also one of the other: answer -1.",
            (
                "Otherwise the longer string cannot be a subsequence of the shorter, or (equal length, different) "
                "neither is: return max(len(a), len(b))."
            ),
        ],
        pattern="Reasoning shortcut (think before coding)",
        explain=(
            "The longest candidate is a whole string; it is uncommon unless the two strings are identical, so no "
            "enumeration is required."
        ),
        cx="O(n) time",
        brute_cx="O(2^n) time - enumerate all subsequences of both strings",
        brute=r"""
# BRUTE FORCE: O(2^n) time - enumerate all subsequences of both strings
def find_lus_length(a, b):
    def subsequences(s):
        result = {""}
        for ch in s:
            result |= {sub + ch for sub in result}
        return result

    sa, sb = subsequences(a), subsequences(b)
    uncommon = sa ^ sb  # in exactly one of them
    return max((len(x) for x in uncommon), default=-1)
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Reasoning shortcut (think before coding)
def find_lus_length(a, b):
    return -1 if a == b else max(len(a), len(b))
""",
    ),
    # ---- Find Common Characters (LeetCode 1002) ----
    dict(
        title="Find Common Characters",
        diff="E",
        lc=1002,
        slug="find-common-characters",
        prompt=(
            "Return every character (with multiplicity) that appears in ALL the words, in any order. If a letter "
            "appears 3 times in every word, include it 3 times."
        ),
        sig="def common_chars(words: List[str]) -> List[str]:",
        fn="common_chars",
        compare="unordered",
        tests=[
            ((["bella", "label", "roller"],), ["e", "l", "l"]),
            ((["cool", "lock", "cook"],), ["c", "o"]),
            ((["a"],), ["a"]),
            ((["abc", "def"],), []),
            ((["aab", "aabb"],), ["a", "a", "b"]),
        ],
        hints=[
            "For each letter you need the MINIMUM number of copies over all words.",
            "Count letters per word.",
            "Counter objects support intersection with &, which keeps the minimum count of every letter.",
        ],
        pattern="Multiset intersection (min of counts)",
        explain="A letter can appear in the answer as many times as the word with the fewest copies allows.",
        cx="O(total characters) time",
        brute_cx="O(total * letters) time - remove each letter of the first word from copies of the others",
        brute=r"""
# BRUTE FORCE: O(total * letters) time - remove each letter of the first word from copies of the others
def common_chars(words):
    others = [list(w) for w in words[1:]]
    result = []
    for ch in words[0]:
        if all(ch in w for w in others):
            for w in others:
                w.remove(ch)  # consume one copy from every other word
            result.append(ch)
    return result
""",
        solution=r"""
# OPTIMISED: O(total characters) time
# Idea: Multiset intersection (min of counts)
def common_chars(words):
    common = Counter(words[0])
    for word in words[1:]:
        common &= Counter(word)  # keep the minimum count per letter
    return list(common.elements())
""",
    ),
]
