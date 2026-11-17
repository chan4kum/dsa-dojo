"""extra batch of Strings problems - the problem bank for the "strings" topic.

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
    # ---- Longest Common Prefix (LeetCode 14) ----
    dict(
        title="Longest Common Prefix",
        diff="E",
        lc=14,
        slug="longest-common-prefix",
        prompt="Return the longest prefix shared by all strings in the list ('' if none).",
        sig="def longest_common_prefix(strs: List[str]) -> str:",
        fn="longest_common_prefix",
        tests=[
            ((["flower", "flow", "flight"],), "fl"),
            ((["dog", "racecar", "car"],), ""),
            ((["a"],), "a"),
            (([],), ""),
            ((["abc", "abc"],), "abc"),
            ((["ab", "a"],), "a"),
        ],
        hints=[
            "The common prefix cannot be longer than the shortest string.",
            "Compare column by column: the i-th character of every string.",
            (
                "Stop at the first column where a string ends or a character differs. (Or: the common prefix of "
                "min(strs) and max(strs).)"
            ),
        ],
        pattern="Vertical scanning (column by column)",
        explain=(
            "Lexicographically, only the smallest and largest strings need comparing: if they share a prefix, "
            "everything in\n        between does as well. That gives a neat O(n + L) alternative."
        ),
        cx="O(total characters)",
        brute_cx="O(n * L) - shrink a candidate prefix against every string",
        brute=r"""
# BRUTE FORCE: O(n * L) - shrink a candidate prefix against every string
def longest_common_prefix(strs):
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
    return prefix
""",
        solution=r"""
# OPTIMISED: O(total characters)
# Idea: Vertical scanning (column by column)
def longest_common_prefix(strs):
    if not strs:
        return ""
    for i, ch in enumerate(strs[0]):
        for s in strs[1:]:
            if i == len(s) or s[i] != ch:
                return strs[0][:i]
    return strs[0]
""",
    ),
    # ---- Reverse Words in a String (LeetCode 151) ----
    dict(
        title="Reverse Words in a String",
        diff="M",
        lc=151,
        slug="reverse-words-in-a-string",
        prompt=(
            "Reverse the order of the words in s. Words are separated by one or more spaces; the output has single "
            "spaces and no leading/trailing spaces."
        ),
        sig="def reverse_words(s: str) -> str:",
        fn="reverse_words",
        tests=[
            (("the sky is blue",), "blue is sky the"),
            (("  hello world  ",), "world hello"),
            (("a good   example",), "example good a"),
            (("x",), "x"),
            (("   ",), ""),
        ],
        hints=[
            "Splitting on whitespace handles extra spaces for you.",
            "split() with no argument drops empty pieces.",
            (
                "' '.join(reversed(s.split())). In C/Java the in-place version: reverse the whole string, then "
                "reverse each word."
            ),
        ],
        pattern="Split, reverse, join (in-place version: reverse all then each word)",
        explain=(
            "Know both the one-liner and the in-place 'double reversal' - the latter is the same trick as Rotate Array."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n) - manual scan collecting words",
        brute=r"""
# BRUTE FORCE: O(n) - manual scan collecting words
def reverse_words(s):
    words, cur = [], ""

    for ch in s:
        if ch == " ":
            if cur:
                words.append(cur)
                cur = ""
        else:
            cur += ch

    if cur:
        words.append(cur)

    out = ""

    for w in reversed(words):
        out = out + (" " if out else "") + w

    return out
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Split, reverse, join (in-place version: reverse all then each word)
def reverse_words(s):
    return " ".join(reversed(s.split()))
""",
    ),
    # ---- String to Integer (atoi) (LeetCode 8) ----
    dict(
        title="String to Integer (atoi)",
        diff="M",
        lc=8,
        slug="string-to-integer-atoi",
        prompt=(
            "Implement atoi: skip leading spaces, read an optional sign, read digits until a non-digit, clamp to "
            "the 32-bit signed range. Return 0 if no digits."
        ),
        sig="def my_atoi(s: str) -> int:",
        fn="my_atoi",
        tests=[
            (("42",), 42),
            (("   -42",), -42),
            (("4193 with words",), 4193),
            (("words and 987",), 0),
            (("-91283472332",), -2147483648),
            (("+1",), 1),
            (("",), 0),
            (("2147483648",), 2147483647),
            (("  +  1",), 0),
        ],
        hints=[
            "This is about carefully following a specification in order.",
            "Phase 1: skip spaces. Phase 2: one optional sign. Phase 3: digits. Stop at anything else.",
            "Accumulate res = res*10 + digit, apply the sign, then clamp to [-2^31, 2^31-1].",
        ],
        pattern="Careful state-by-state parsing (finite automaton)",
        explain=(
            "Interviewers test whether you enumerate edge cases: empty input, only spaces, sign without digits, "
            "double signs,\n        overflow. List them BEFORE coding."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) - regular expression",
        brute=r"""
# BRUTE FORCE: O(n) - regular expression
def my_atoi(s):
    import re

    m = re.match(r"^\s*([+-]?\d+)", s)
    if not m:
        return 0
    return max(-(2**31), min(2**31 - 1, int(m.group(1))))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Careful state-by-state parsing (finite automaton)
def my_atoi(s):
    i, n = 0, len(s)

    while i < n and s[i] == " ":
        i += 1

    sign = 1

    if i < n and s[i] in "+-":
        sign = -1 if s[i] == "-" else 1
        i += 1

    res = 0

    while i < n and s[i].isdigit():
        res = res * 10 + int(s[i])
        i += 1

    return max(-(2**31), min(2**31 - 1, sign * res))
""",
    ),
    # ---- Roman to Integer (LeetCode 13) ----
    dict(
        title="Roman to Integer",
        diff="E",
        lc=13,
        slug="roman-to-integer",
        prompt=(
            "Convert a Roman numeral (I=1, V=5, X=10, L=50, C=100, D=500, M=1000, with subtractive pairs like IV, "
            "IX, XL, XC, CD, CM) to an integer."
        ),
        sig="def roman_to_int(s: str) -> int:",
        fn="roman_to_int",
        tests=[
            (("III",), 3),
            (("LVIII",), 58),
            (("MCMXCIV",), 1994),
            (("IV",), 4),
            (("IX",), 9),
            (("MMMCMXCIX",), 3999),
        ],
        hints=[
            "Mostly add the values left to right. When does a symbol count as negative?",
            "When a smaller value appears BEFORE a larger one.",
            "For each char: if value < value of the next char, subtract it; else add it.",
        ],
        pattern="Single left-to-right pass with a lookahead rule",
        explain="The subtractive pairs are exactly the cases where a symbol is smaller than its right neighbour.",
        cx="O(n)",
        brute_cx="O(n) - greedily match two-letter tokens first",
        brute=r"""
# BRUTE FORCE: O(n) - greedily match two-letter tokens first
def roman_to_int(s):
    vals = {
        "M": 1000,
        "CM": 900,
        "D": 500,
        "CD": 400,
        "C": 100,
        "XC": 90,
        "L": 50,
        "XL": 40,
        "X": 10,
        "IX": 9,
        "V": 5,
        "IV": 4,
        "I": 1,
    }
    i, total = 0, 0

    while i < len(s):
        if s[i : i + 2] in vals:
            total += vals[s[i : i + 2]]
            i += 2
        else:
            total += vals[s[i]]
            i += 1

    return total
""",
        solution=r"""
# OPTIMISED: O(n)
# Idea: Single left-to-right pass with a lookahead rule
def roman_to_int(s):
    v = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}
    total = 0

    for i, ch in enumerate(s):
        if i + 1 < len(s) and v[ch] < v[s[i + 1]]:
            total -= v[ch]
        else:
            total += v[ch]

    return total
""",
    ),
    # ---- Add Strings (LeetCode 415) ----
    dict(
        title="Add Strings",
        diff="E",
        lc=415,
        slug="add-strings",
        prompt=(
            "Add two non-negative integers given as decimal strings without converting the whole strings to integers."
        ),
        sig="def add_strings(num1: str, num2: str) -> str:",
        fn="add_strings",
        tests=[
            (("11", "123"), "134"),
            (("456", "77"), "533"),
            (("0", "0"), "0"),
            (("999", "1"), "1000"),
            (("1", "9999"), "10000"),
        ],
        hints=[
            "Do it the way you add on paper: right to left with a carry.",
            "Two pointers from the ends; missing digits count as 0.",
            "digit = (a + b + carry) % 10; carry = (a + b + carry) // 10; reverse the collected digits at the end.",
        ],
        pattern="Digit-by-digit arithmetic with carry (two pointers from the right)",
        explain="Same carry loop as 'Add Two Numbers' on linked lists, and the building block for Multiply Strings.",
        cx="O(max(m, n))",
        brute_cx="O(m + n) - Python big ints (not allowed in an interview, but a good oracle)",
        brute=r"""
# BRUTE FORCE: O(m + n) - Python big ints (not allowed in an interview, but a good oracle)
def add_strings(num1, num2):
    return str(int(num1) + int(num2))
""",
        solution=r"""
# OPTIMISED: O(max(m, n))
# Idea: Digit-by-digit arithmetic with carry (two pointers from the right)
def add_strings(num1, num2):
    i, j, carry, out = len(num1) - 1, len(num2) - 1, 0, []

    while i >= 0 or j >= 0 or carry:
        a = int(num1[i]) if i >= 0 else 0
        b = int(num2[j]) if j >= 0 else 0
        carry, d = divmod(a + b + carry, 10)
        out.append(str(d))
        i, j = i - 1, j - 1

    return "".join(reversed(out))
""",
    ),
    # ---- Multiply Strings (LeetCode 43) ----
    dict(
        title="Multiply Strings",
        diff="M",
        lc=43,
        slug="multiply-strings",
        prompt=(
            "Multiply two non-negative integers given as strings and return the product as a string, without "
            "converting them to integers."
        ),
        sig="def multiply(num1: str, num2: str) -> str:",
        fn="multiply",
        tests=[
            (("2", "3"), "6"),
            (("123", "456"), "56088"),
            (("0", "123"), "0"),
            (("999", "999"), "998001"),
            (("9", "9"), "81"),
        ],
        hints=[
            "Digit i of num1 times digit j of num2 contributes to position i + j (and carries to i + j + 1).",
            "Use an array of length m + n for the result digits.",
            "Accumulate products into res[i+j+1], then normalise carries; strip leading zeros.",
        ],
        pattern="Schoolbook multiplication with a position array",
        explain=(
            "Visualise the long-multiplication grid: each digit product lands at a fixed position. Working from the "
            "right\n        and propagating carries mirrors what you do on paper."
        ),
        cx="O(m*n)",
        brute_cx="O(m*n) - repeated addition of shifted partial products using Add Strings",
        brute=r"""
# BRUTE FORCE: O(m*n) - repeated addition of shifted partial products using Add Strings
def multiply(num1, num2):
    if num1 == "0" or num2 == "0":
        return "0"

    def add(a, b):
        i, j, carry, out = len(a) - 1, len(b) - 1, 0, []

        while i >= 0 or j >= 0 or carry:
            x = int(a[i]) if i >= 0 else 0
            y = int(b[j]) if j >= 0 else 0
            carry, d = divmod(x + y + carry, 10)
            out.append(str(d))
            i, j = i - 1, j - 1

        return "".join(reversed(out))

    total = "0"

    for k, d in enumerate(reversed(num2)):
        partial = "0"
        for _ in range(int(d)):
            partial = add(partial, num1)
        total = add(total, partial + "0" * k)

    return total
""",
        solution=r"""
# OPTIMISED: O(m*n)
# Idea: Schoolbook multiplication with a position array
def multiply(num1, num2):
    if num1 == "0" or num2 == "0":
        return "0"

    m, n = len(num1), len(num2)
    res = [0] * (m + n)

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            total = res[i + j + 1] + int(num1[i]) * int(num2[j])
            res[i + j + 1] = total % 10
            res[i + j] += total // 10

    return "".join(map(str, res)).lstrip("0")
""",
    ),
    # ---- Encode and Decode Strings (LeetCode 271) ----
    dict(
        title="Encode and Decode Strings",
        diff="M",
        lc=271,
        slug="encode-and-decode-strings",
        prompt=(
            "Design encode(strs) -> str and decode(s) -> list so that decode(encode(strs)) == strs for ANY strings "
            "(they may contain any characters, including your separator). Define encode, decode and roundtrip(strs) "
            "= decode(encode(strs)) yourself (the tests call roundtrip)."
        ),
        sig=(
            "def encode(strs: List[str]) -> str:\n    pass\n\ndef decode(s: str) -> List[str]:\n    pass\n\ndef "
            "roundtrip(strs: List[str]) -> List[str]:\n    return decode(encode(strs))"
        ),
        fn="roundtrip",
        tests=[
            ((["lint", "code", "love", "you"],), ["lint", "code", "love", "you"]),
            ((["we", "say", ":", "yes"],), ["we", "say", ":", "yes"]),
            (([],), []),
            ((["", ""],), ["", ""]),
            ((["4#abcd", "#", "10#"],), ["4#abcd", "#", "10#"]),
            ((["a,b", "c"],), ["a,b", "c"]),
        ],
        hints=[
            "A separator character fails because the strings may contain it. What else can mark where a string ends?",
            "Escaping works, but is fiddly. What if you told the decoder HOW LONG each string is?",
            (
                "Length prefix: encode each string as f'{len(s)}#{s}'. To decode read digits up to '#', then take "
                "exactly that many characters. Content can never be confused with structure."
            ),
        ],
        pattern="Length-prefixed framing (the idea behind most network protocols)",
        explain=(
            "Delimiters are fragile because data can contain them; lengths are not. This is how HTTP bodies, "
            "protobuf and\n        TCP framing work - a good bridge to system design discussions."
        ),
        cx="O(total length)",
        brute_cx="O(total length) - escape the separator inside the strings",
        brute="""
def encode(strs):
    return "".join(s.replace("\\\\", "\\\\\\\\").replace(",", "\\\\,") + "," for s in strs)

def decode(s):
    out, cur, i = [], [], 0
    while i < len(s):
        ch = s[i]
        if ch == "\\\\":
            cur.append(s[i + 1])
            i += 2
            continue
        if ch == ",":
            out.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
        i += 1
    return out

def roundtrip(strs):
    return decode(encode(strs))
""",
        solution="""
def encode(strs):
    return "".join(f"{len(s)}#{s}" for s in strs)

def decode(s):
    out, i = [], 0
    while i < len(s):
        j = s.index("#", i)
        n = int(s[i:j])
        out.append(s[j + 1:j + 1 + n])
        i = j + 1 + n
    return out

def roundtrip(strs):
    return decode(encode(strs))
""",
    ),
]
