"""more String problems (batch 3) - part of the problem bank for the "strings" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Reverse Vowels of a String (LeetCode 345) ----
    dict(
        title="Reverse Vowels of a String",
        diff="E",
        lc=345,
        slug="reverse-vowels-of-a-string",
        prompt=(
            "Reverse only the vowels (a, e, i, o, u in either case) of the string; every other character stays "
            "where it is."
        ),
        sig="def reverse_vowels(s: str) -> str:",
        fn="reverse_vowels",
        tests=[
            (("hello",), "holle"),
            (("leetcode",), "leotcede"),
            (("aA",), "Aa"),
            (("xyz",), "xyz"),
            (("",), ""),
        ],
        hints=[
            "Vowels swap with each other; consonants never move.",
            "Put one pointer at each end of the string.",
            "Move each pointer inward until it sits on a vowel, swap the two, and continue until they meet.",
        ],
        pattern="Two pointers from both ends, skipping non-vowels",
        explain=(
            "It is 'Reverse String' with a filter. The pointers skip anything that is not a vowel, so only "
            "vowels\n        are ever swapped and the rest of the string is untouched."
        ),
        cx="O(n) time, O(n) space (strings are immutable, so we work on a list)",
        brute_cx="O(n) time, O(n) extra space - collect, reverse, refill",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) extra space - collect, reverse, refill
def reverse_vowels(s):
    vowels = "aeiouAEIOU"
    found = [ch for ch in s if ch in vowels]  # every vowel, in reading order
    found.reverse()  # the order they should appear in now
    result = []

    for ch in s:
        if ch in vowels:
            result.append(found.pop(0))  # next reversed vowel
        else:
            result.append(ch)

    return "".join(result)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space (strings are immutable, so we work on a list)
# Idea: Two pointers from both ends, skipping non-vowels
def reverse_vowels(s):
    vowels = set("aeiouAEIOU")
    chars = list(s)
    left, right = 0, len(chars) - 1

    while left < right:
        while left < right and chars[left] not in vowels:  # skip consonants on the left
            left += 1
        while left < right and chars[right] not in vowels:  # skip consonants on the right
            right -= 1
        chars[left], chars[right] = chars[right], chars[left]
        left += 1
        right -= 1

    return "".join(chars)
""",
    ),
    # ---- Repeated Substring Pattern (LeetCode 459) ----
    dict(
        title="Repeated Substring Pattern",
        diff="E",
        lc=459,
        slug="repeated-substring-pattern",
        prompt="Return True if the string can be built by repeating one of its substrings two or more times.",
        sig="def repeated_substring_pattern(s: str) -> bool:",
        fn="repeated_substring_pattern",
        tests=[
            (("abab",), True),
            (("aba",), False),
            (("abcabcabc",), True),
            (("a",), False),
            (("aa",), True),
        ],
        hints=[
            "The repeating unit must have a length that divides len(s) evenly.",
            "For each such length L, compare s with s[:L] repeated len(s) // L times.",
            (
                "Clever one-liner: s is made of repeats exactly when s appears inside (s + s) with the first and "
                "last character removed."
            ),
        ],
        pattern="String rotation trick: s is periodic iff s in (s + s)[1:-1]",
        explain=(
            "If s = u repeated k times, then s + s = u repeated 2k times, so s hides inside the doubled string at "
            "an\n        offset smaller than len(s). Trimming the first and last character forbids the two trivial "
            "matches."
        ),
        cx="O(n) time with a linear-time substring search",
        brute_cx="O(n * d(n)) time - try every divisor length",
        brute=r"""
# BRUTE FORCE: O(n * d(n)) time - try every divisor length
def repeated_substring_pattern(s):
    n = len(s)
    for length in range(1, n // 2 + 1):  # candidate unit size
        if (
            n % length == 0 and s[:length] * (n // length) == s
        ):  # does repeating the unit rebuild s?
            return True
    return False
""",
        solution=r"""
# OPTIMISED: O(n) time with a linear-time substring search
# Idea: String rotation trick: s is periodic iff s in (s + s)[1:-1]
def repeated_substring_pattern(s):
    # s + s contains s at positions 0 and len(s); a periodic s also contains it in between
    return s in (s + s)[1:-1]
""",
    ),
    # ---- Count Binary Substrings (LeetCode 696) ----
    dict(
        title="Count Binary Substrings",
        diff="E",
        lc=696,
        slug="count-binary-substrings",
        prompt=(
            "Count the non-empty substrings that have equally many 0s and 1s, with all the 0s grouped together and "
            "all the 1s grouped together."
        ),
        sig="def count_binary_substrings(s: str) -> int:",
        fn="count_binary_substrings",
        tests=[
            (("00110011",), 6),
            (("10101",), 4),
            (("0",), 0),
            ((("000111"),), 3),
            (("00100",), 2),
        ],
        hints=[
            "Write the string as runs of equal characters, e.g. 00110011 -> run lengths 2, 2, 2, 2.",
            "A valid substring straddles exactly one boundary between two neighbouring runs.",
            "Between runs of length a and b you can form min(a, b) valid substrings. Sum over all neighbouring pairs.",
        ],
        pattern="Run-length groups: add min(previous run, current run)",
        explain=(
            "Around one boundary you can grow outward symmetrically: 01, 0011, 000111 ... until the shorter run is "
            "used\n        up. That gives min(a, b) substrings, and different boundaries never double count."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - expand every starting point",
        brute=r"""
# BRUTE FORCE: O(n^2) time - expand every starting point
def count_binary_substrings(s):
    count = 0

    for i in range(len(s)):
        for j in range(i + 2, len(s) + 1, 2):  # only even lengths can be balanced
            half = (j - i) // 2
            other = "1" if s[i] == "0" else "0"
            if s[i:j] == s[i] * half + other * half:  # e.g. 000111
                count += 1

    return count
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Run-length groups: add min(previous run, current run)
def count_binary_substrings(s):
    prev_run, cur_run, total = 0, 1, 0

    for i in range(1, len(s)):
        if s[i] == s[i - 1]:
            cur_run += 1  # the current run keeps growing
        else:
            total += min(prev_run, cur_run)  # the finished run pairs with the one before it
            prev_run, cur_run = cur_run, 1

    return total + min(prev_run, cur_run)  # the last boundary
""",
    ),
    # ---- Count and Say (LeetCode 38) ----
    dict(
        title="Count and Say",
        diff="M",
        lc=38,
        slug="count-and-say",
        prompt=(
            "count_and_say(1) = '1'. Each next term describes the previous one by reading its runs aloud: '1' -> "
            "'one 1' -> '11' -> 'two 1s' -> '21' -> '1211' ... Return the n-th term."
        ),
        sig="def count_and_say(n: int) -> str:",
        fn="count_and_say",
        tests=[
            ((1,), "1"),
            ((2,), "11"),
            ((4,), "1211"),
            ((5,), "111221"),
            ((6,), "312211"),
        ],
        hints=[
            "Each term is produced from the previous term only.",
            "To say a term, split it into runs of the same digit: '1211' -> 1, 2, 11.",
            "For every run output str(run length) + digit. Repeat n - 1 times starting from '1'.",
        ],
        pattern="Run-length encoding, applied n - 1 times",
        explain=(
            "The sequence is run-length encoding fed back into itself. itertools.groupby splits a string into runs, "
            "so\n        each term is one join over its runs."
        ),
        cx="O(total length of all terms) time",
        brute_cx="same cost, but a hand-written run scanner and recursion",
        brute=r"""
# BRUTE FORCE: same cost, but a hand-written run scanner and recursion
def count_and_say(n):
    if n == 1:
        return "1"

    previous = count_and_say(n - 1)  # the term we have to read aloud
    result = ""
    i = 0

    while i < len(previous):
        j = i
        while j < len(previous) and previous[j] == previous[i]:  # find where this run ends
            j += 1
        result += str(j - i) + previous[i]  # "<how many><which digit>"
        i = j

    return result
""",
        solution=r"""
# OPTIMISED: O(total length of all terms) time
# Idea: Run-length encoding, applied n - 1 times
def count_and_say(n):
    term = "1"
    for _ in range(n - 1):
        # groupby yields (digit, run) for each block of equal digits
        term = "".join(str(len(list(run))) + digit for digit, run in itertools.groupby(term))
    return term
""",
    ),
    # ---- Zigzag Conversion (LeetCode 6) ----
    dict(
        title="Zigzag Conversion",
        diff="M",
        lc=6,
        slug="zigzag-conversion",
        prompt=(
            "Write the string in a zigzag down and up over num_rows rows, then read it row by row. "
            "('PAYPALISHIRING', 3) -> 'PAHNAPLSIIGYIR'."
        ),
        sig="def convert(s: str, num_rows: int) -> str:",
        fn="convert",
        tests=[
            (("PAYPALISHIRING", 3), "PAHNAPLSIIGYIR"),
            (("PAYPALISHIRING", 4), "PINALSIGYAHRPI"),
            (("A", 1), "A"),
            (("AB", 1), "AB"),
            (("ABC", 2), "ACB"),
        ],
        hints=[
            "You do not need a 2-D picture. Each character just lands in some row.",
            (
                "The row number goes 0, 1, ..., last, then back up ..., 1, 0, and repeats. Keep a direction that "
                "flips at the ends."
            ),
            "Append each character to its row's string, then join the rows. With one row (or rows >= length) return s.",
        ],
        pattern="Simulate a bouncing row index",
        explain=(
            "The picture is a distraction: only the ROW of each character matters, and the row index simply "
            "bounces\n        between 0 and num_rows - 1. One list of row-buffers is enough."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(rows * n) time and space - fill a real 2-D grid",
        brute=r"""
# BRUTE FORCE: O(rows * n) time and space - fill a real 2-D grid
def convert(s, num_rows):
    if num_rows == 1 or num_rows >= len(s):
        return s

    grid = [[""] * len(s) for _ in range(num_rows)]  # one column per character is always enough
    r = c = 0
    going_down = True

    for ch in s:
        grid[r][c] = ch

        if going_down:
            if r == num_rows - 1:  # bottom reached: turn and move diagonally up-right
                going_down = False
                r -= 1
                c += 1
            else:
                r += 1
        else:
            if r == 0:  # top reached: turn and go straight down
                going_down = True
                r += 1
            else:
                r -= 1
                c += 1

    return "".join(ch for row in grid for ch in row)  # read row by row
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Simulate a bouncing row index
def convert(s, num_rows):
    if num_rows == 1 or num_rows >= len(s):
        return s

    rows = [""] * num_rows
    row, step = 0, 1  # step = +1 going down, -1 going up

    for ch in s:
        rows[row] += ch
        if row == 0:
            step = 1  # at the top: head down
        elif row == num_rows - 1:
            step = -1  # at the bottom: head up
        row += step

    return "".join(rows)
""",
    ),
    # ---- Longest Palindrome (LeetCode 409) ----
    dict(
        title="Longest Palindrome",
        diff="E",
        lc=409,
        slug="longest-palindrome",
        prompt=(
            "Using the letters of s (case-sensitive), each at most as often as it appears, return the length of the "
            "longest palindrome you can build."
        ),
        sig="def longest_palindrome(s: str) -> int:",
        fn="longest_palindrome",
        tests=[
            (("abccccdd",), 7),
            (("a",), 1),
            (("aaaaaccc",), 7),
            (("Aa",), 1),
            (("bb",), 2),
            (("",), 0),
        ],
        hints=[
            "A palindrome is made of mirrored PAIRS of letters, plus at most one letter in the middle.",
            "Every letter with count c contributes c // 2 pairs (that is c - c % 2 letters).",
            "If any letter has an odd count there is a spare letter to put in the middle: add 1.",
        ],
        pattern="Count frequencies: use all pairs, allow one odd centre",
        explain=(
            "We are free to rearrange, so only counts matter. Pairs are always usable; the single centre can come "
            "from\n        any letter that has a leftover."
        ),
        cx="O(n) time, O(alphabet) space",
        brute_cx="O(n^2) time - repeatedly search for a matching partner",
        brute=r"""
# BRUTE FORCE: O(n^2) time - repeatedly search for a matching partner
def longest_palindrome(s):
    letters = list(s)
    pairs = leftover = 0

    while letters:
        ch = letters.pop()
        if ch in letters:  # found a partner: remove it and count one mirrored pair
            letters.remove(ch)
            pairs += 1
        else:
            leftover += 1  # an unmatched letter (could be the centre)

    return pairs * 2 + (1 if leftover else 0)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(alphabet) space
# Idea: Count frequencies: use all pairs, allow one odd centre
def longest_palindrome(s):
    length = 0
    odd_seen = False
    for count in Counter(s).values():
        length += count - count % 2  # all the pairs of this letter
        if count % 2:
            odd_seen = True  # a spare letter exists for the middle
    return length + (1 if odd_seen else 0)
""",
    ),
    # ---- Repeated DNA Sequences (LeetCode 187) ----
    dict(
        title="Repeated DNA Sequences",
        diff="M",
        lc=187,
        slug="repeated-dna-sequences",
        prompt=(
            "s consists of the letters A, C, G, T. Return every 10-letter substring that occurs more than once in s "
            "(any order)."
        ),
        sig="def find_repeated_dna_sequences(s: str) -> List[str]:",
        fn="find_repeated_dna_sequences",
        compare="unordered",
        tests=[
            (("AAAAACCCCCAAAAACCCCCCAAAAAGGGTTT",), ["AAAAACCCCC", "CCCCCAAAAA"]),
            (("AAAAAAAAAAAAA",), ["AAAAAAAAAA"]),
            (("",), []),
            (("ACGT",), []),
        ],
        hints=[
            "There are only len(s) - 9 windows of length 10.",
            "Remember every window you have already seen in a set.",
            "If a window is seen again, put it in the answer (use a second set so it is reported only once).",
        ],
        pattern="Sliding window of fixed length + hash set of seen windows",
        explain=(
            "Comparing every pair of windows is quadratic. A set remembers 'seen before?' in O(1), so each window "
            "is\n        handled exactly once."
        ),
        cx="O(n) windows, O(10n) time to hash them, O(n) space",
        brute_cx="O(n^2) time - compare every window with every later window",
        brute=r"""
# BRUTE FORCE: O(n^2) time - compare every window with every later window
def find_repeated_dna_sequences(s):
    found = []

    for i in range(len(s) - 9):
        window = s[i : i + 10]
        if window in found:
            continue  # already reported
        # does the same 10 letters start somewhere later?
        if any(s[j : j + 10] == window for j in range(i + 1, len(s) - 9)):
            found.append(window)

    return found
""",
        solution=r"""
# OPTIMISED: O(n) windows, O(10n) time to hash them, O(n) space
# Idea: Sliding window of fixed length + hash set of seen windows
def find_repeated_dna_sequences(s):
    seen, repeated = set(), set()
    for i in range(len(s) - 9):
        window = s[i : i + 10]  # the 10 letters starting at i
        if window in seen:
            repeated.add(window)  # second (or later) sighting
        seen.add(window)
    return list(repeated)
""",
    ),
]
