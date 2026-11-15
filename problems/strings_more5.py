"""extra batch of String problems - the problem bank for the "strings" topic (batch 5).

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


def _custom_ok(args, got):
    """True if got is a permutation of s in which the letters that occur in order respect that order."""
    order, s = args
    if not isinstance(got, str) or sorted(got) != sorted(s):
        return False
    rank = {c: i for i, c in enumerate(order)}
    ranks = [rank[c] for c in got if c in rank]
    return ranks == sorted(ranks)


def _equal_parts(arr, i, j):
    first, second, third = arr[: i + 1], arr[i + 1 : j], arr[j:]
    if not first or not second or not third:
        return False
    return int("".join(map(str, first)), 2) == int("".join(map(str, second)), 2) == int("".join(map(str, third)), 2)


def _three_ok(args, got):
    """True if got = [i, j] is a valid split, or [-1, -1] and no valid split exists."""
    arr = args[0]
    n = len(arr)
    if list(got) == [-1, -1]:
        return not any(_equal_parts(arr, i, j) for i in range(n) for j in range(i + 2, n))
    return isinstance(got, list) and len(got) == 2 and _equal_parts(arr, got[0], got[1])


PROBLEMS = [
    # ---- Text Justification (LeetCode 68) ----
    dict(
        title="Text Justification",
        diff="H",
        lc=68,
        slug="text-justification",
        prompt=(
            "Format words into lines of exactly max_width characters, packing as many words per line as fit with at "
            "least one space between words. Extra spaces are spread as evenly as possible between words; if they do "
            "not divide evenly the left gaps get more. A line with a single word, and the LAST line, are "
            "left-justified (single spaces between words, padded with spaces on the right). Return the lines."
        ),
        sig="def full_justify(words: List[str], max_width: int) -> List[str]:",
        fn="full_justify",
        tests=[
            (
                (["This", "is", "an", "example", "of", "text", "justification."], 16),
                ["This    is    an", "example  of text", "justification.  "],
            ),
            (
                (["What", "must", "be", "acknowledgment", "shall", "be"], 16),
                ["What   must   be", "acknowledgment  ", "shall be        "],
            ),
            (
                (
                    [
                        "Science",
                        "is",
                        "what",
                        "we",
                        "understand",
                        "well",
                        "enough",
                        "to",
                        "explain",
                        "to",
                        "a",
                        "computer.",
                        "Art",
                        "is",
                        "everything",
                        "else",
                        "we",
                        "do",
                    ],
                    20,
                ),
                [
                    "Science  is  what we",
                    "understand      well",
                    "enough to explain to",
                    "a  computer.  Art is",
                    "everything  else  we",
                    "do                  ",
                ],
            ),
            ((["a"], 3), ["a  "]),
        ],
        hints=[
            (
                "First decide which words go on which line: keep adding words while the line (words plus one space "
                "between each) still fits."
            ),
            (
                "For a normal line, total spaces = max_width - sum of word lengths; divide them over the gaps with "
                "divmod - the first `remainder` gaps get one extra."
            ),
            (
                "Remember the two special cases: a line with one word and the last line are left-justified and "
                "padded on the right."
            ),
        ],
        pattern="Greedy line packing + arithmetic space distribution",
        explain=(
            "Greedy packing is optimal here because the problem fixes the rule: put as many words as fit on each "
            "line. Once a line's words are known, the number of spaces is determined, and divmod(spaces, gaps) "
            "gives every gap a base width plus one extra for the leftmost `remainder` gaps. The brute force does "
            "the same packing but hands out the extra spaces one at a time, round-robin from the left."
        ),
        cx="O(total characters) time, O(total characters) space",
        brute_cx="O(total characters * gaps) time - spaces are handed out one at a time",
        brute=r"""
# BRUTE FORCE: O(total characters * gaps) time - spaces are handed out one at a time
def full_justify(words, max_width):
    lines = []
    current = []
    length = 0
    for word in words:
        if current and length + len(current) + len(word) > max_width:
            lines.append(current)
            current, length = [], 0
        current.append(word)
        length += len(word)
    if current:
        lines.append(current)
    result = []
    for index, line in enumerate(lines):
        gaps = len(line) - 1
        if index == len(lines) - 1 or gaps == 0:
            text = " ".join(line)
            result.append(text + " " * (max_width - len(text)))
            continue
        spaces = [1] * gaps
        extra = max_width - (sum(len(w) for w in line) + gaps)
        for step in range(extra):
            spaces[step % gaps] += 1
        text = ""
        for position, word in enumerate(line[:-1]):
            text += word + " " * spaces[position]
        result.append(text + line[-1])
    return result
""",
        solution=r"""
# OPTIMISED: O(total characters) time, O(total characters) space
# Idea: Greedy line packing + arithmetic space distribution
def full_justify(words, max_width):
    lines = []
    i, n = 0, len(words)
    while i < n:
        j = i
        length = len(words[i])
        while j + 1 < n and length + 1 + len(words[j + 1]) <= max_width:
            j += 1
            length += 1 + len(words[j])
        group = words[i : j + 1]
        if j == n - 1 or len(group) == 1:
            line = " ".join(group)
            line += " " * (max_width - len(line))
        else:
            spaces = max_width - sum(len(w) for w in group)
            base, extra = divmod(spaces, len(group) - 1)
            line = ""
            for k, word in enumerate(group[:-1]):
                line += word + " " * (base + (1 if k < extra else 0))
            line += group[-1]
        lines.append(line)
        i = j + 1
    return lines
""",
    ),
    # ---- Fraction to Recurring Decimal (LeetCode 166) ----
    dict(
        title="Fraction to Recurring Decimal",
        diff="M",
        lc=166,
        slug="fraction-to-recurring-decimal",
        prompt=(
            "Return numerator / denominator as a string. If the fractional part repeats, enclose the repeating "
            "digits in parentheses. The denominator is never 0."
        ),
        sig="def fraction_to_decimal(numerator: int, denominator: int) -> str:",
        fn="fraction_to_decimal",
        tests=[
            ((1, 2), "0.5"),
            ((2, 1), "2"),
            ((4, 333), "0.(012)"),
            ((1, 6), "0.1(6)"),
            ((-50, 8), "-6.25"),
            ((0, -5), "0"),
            ((-1, -2), "0.5"),
            ((22, 7), "3.(142857)"),
        ],
        hints=[
            "Handle the sign separately and work with absolute values; split off the integer part with divmod.",
            "Do long division by hand: remainder * 10, the next digit is (remainder * 10) // denominator.",
            (
                "The digits start repeating exactly when a remainder repeats - store each remainder with the "
                "position where it first appeared, and insert '(' there."
            ),
        ],
        pattern="Long division with a hash map of seen remainders",
        explain=(
            "The decimal expansion is determined by the remainders: the same remainder always produces the same "
            "next digits. Remembering where each remainder first appeared tells us exactly where the repeating "
            "block begins. There are fewer than `denominator` distinct remainders, so the loop is bounded. The "
            "brute force uses number theory: after removing the factors 2 and 5 from the reduced denominator, the "
            "leftover m decides the period (the order of 10 mod m)."
        ),
        cx="O(denominator) time and space",
        brute_cx="O(denominator) time - find the period as the multiplicative order of 10",
        brute=r"""
# BRUTE FORCE: O(denominator) time - find the period as the multiplicative order of 10
def fraction_to_decimal(numerator, denominator):
    if numerator == 0:
        return "0"
    sign = "-" if (numerator < 0) != (denominator < 0) else ""
    whole, rem = divmod(abs(numerator), abs(denominator))
    if rem == 0:
        return sign + str(whole)
    d = abs(denominator)
    g = math.gcd(rem, d)
    rem //= g
    d //= g
    twos = fives = 0
    m = d
    while m % 2 == 0:
        m //= 2
        twos += 1
    while m % 5 == 0:
        m //= 5
        fives += 1
    pre = max(twos, fives)
    if m == 1:
        return f"{sign}{whole}." + str(rem * 10**pre // d).zfill(pre)
    period = 1
    while pow(10, period, m) != 1:
        period += 1
    digits = str(rem * 10 ** (pre + period) // d).zfill(pre + period)
    return f"{sign}{whole}.{digits[:pre]}({digits[pre:]})"
""",
        solution=r"""
# OPTIMISED: O(denominator) time and space
# Idea: Long division with a hash map of seen remainders
def fraction_to_decimal(numerator, denominator):
    if numerator == 0:
        return "0"
    sign = "-" if (numerator < 0) != (denominator < 0) else ""
    n, d = abs(numerator), abs(denominator)
    whole, rem = divmod(n, d)
    out = [sign + str(whole)]
    if rem == 0:
        return out[0]
    out.append(".")
    seen = {}
    while rem and rem not in seen:
        seen[rem] = len(out)
        rem *= 10
        out.append(str(rem // d))
        rem %= d
    if rem:
        out.insert(seen[rem], "(")
        out.append(")")
    return "".join(out)
""",
    ),
    # ---- Largest Number (LeetCode 179) ----
    dict(
        title="Largest Number",
        diff="M",
        lc=179,
        slug="largest-number",
        prompt=(
            "Arrange the non-negative integers in nums so that their concatenation is the largest possible number. "
            "Return it as a string (the result may be huge)."
        ),
        sig="def largest_number(nums: List[int]) -> str:",
        fn="largest_number",
        tests=[
            (([10, 2],), "210"),
            (([3, 30, 34, 5, 9],), "9534330"),
            (([0, 0],), "0"),
            (([1],), "1"),
            (([824, 8247],), "8248247"),
        ],
        hints=[
            (
                "Comparing numbers by value fails: 3 should come before 30 even though 3 < 30 only matters in how "
                "the digits glue together."
            ),
            "For two numbers a and b, put a first if the string a+b is larger than b+a.",
            (
                "Sort with that comparison (functools.cmp_to_key). If the largest element is '0', the answer is '0' "
                "(avoid '000')."
            ),
        ],
        pattern="Custom comparator sort (order two items by the concatenations)",
        explain=(
            "The comparator 'a before b iff a+b > b+a' is a consistent total preorder, so sorting with it produces "
            "the order that maximises the concatenation (an exchange argument: swapping two adjacent items that "
            "violate it can only increase the result). Brute force tries every permutation and keeps the maximum "
            "string."
        ),
        cx="O(n log n * L) time",
        brute_cx="O(n! * n * L) time - build every permutation's concatenation",
        brute=r"""
# BRUTE FORCE: O(n! * n * L) time - build every permutation's concatenation
def largest_number(nums):
    best = max("".join(map(str, perm)) for perm in itertools.permutations(nums))
    return "0" if best.startswith("0") else best
""",
        solution=r"""
# OPTIMISED: O(n log n * L) time
# Idea: Custom comparator sort (order two items by the concatenations)
def largest_number(nums):
    def compare(a, b):
        return (a + b < b + a) - (a + b > b + a)

    parts = sorted(map(str, nums), key=functools.cmp_to_key(compare))
    return "0" if parts[0] == "0" else "".join(parts)
""",
    ),
    # ---- Integer to English Words (LeetCode 273) ----
    dict(
        title="Integer to English Words",
        diff="H",
        lc=273,
        slug="integer-to-english-words",
        prompt=(
            "Convert a non-negative integer (up to 2^31 - 1) to its English words, e.g. 123 -> 'One Hundred Twenty "
            "Three'. Capitalise every word, use no 'and', and separate words with single spaces."
        ),
        sig="def number_to_words(num: int) -> str:",
        fn="number_to_words",
        tests=[
            ((123,), "One Hundred Twenty Three"),
            ((12345,), "Twelve Thousand Three Hundred Forty Five"),
            ((1234567,), "One Million Two Hundred Thirty Four Thousand Five Hundred Sixty Seven"),
            ((0,), "Zero"),
            ((1000,), "One Thousand"),
            ((1000010,), "One Million Ten"),
            ((20,), "Twenty"),
        ],
        hints=[
            "English reads numbers in groups of three digits: ones, thousands, millions, billions.",
            (
                "Write a helper that spells a number below 1000: hundreds, then tens (with a special list for "
                "1-19), then ones."
            ),
            (
                "Split the number into groups from the right; for every non-zero group, append its words and the "
                "scale word, going from the largest group down."
            ),
        ],
        pattern="Chunking into 3-digit groups with lookup tables",
        explain=(
            "Every group of three digits is spelled the same way, followed by the scale word of its position. "
            "Skipping zero groups avoids 'One Million Thousand'. The brute force expresses the same grammar as a "
            "single recursion that peels off the biggest unit (billion, million, thousand, hundred, tens) that fits."
        ),
        cx="O(digits) time",
        brute_cx="O(digits) time - recursion over the largest unit that fits",
        brute=r"""
# BRUTE FORCE: O(digits) time - recursion over the largest unit that fits
def number_to_words(num):
    small = [
        "Zero",
        "One",
        "Two",
        "Three",
        "Four",
        "Five",
        "Six",
        "Seven",
        "Eight",
        "Nine",
        "Ten",
        "Eleven",
        "Twelve",
        "Thirteen",
        "Fourteen",
        "Fifteen",
        "Sixteen",
        "Seventeen",
        "Eighteen",
        "Nineteen",
    ]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]

    def words(n):
        if n < 20:
            return [small[n]] if n else []
        if n < 100:
            return [tens[n // 10]] + words(n % 10)
        if n < 1000:
            return [small[n // 100], "Hundred"] + words(n % 100)
        for size, name in ((10**9, "Billion"), (10**6, "Million"), (10**3, "Thousand")):
            if n >= size:
                return words(n // size) + [name] + words(n % size)

    return "Zero" if num == 0 else " ".join(words(num))
""",
        solution=r"""
# OPTIMISED: O(digits) time
# Idea: Chunking into 3-digit groups with lookup tables
def number_to_words(num):
    if num == 0:
        return "Zero"
    ones = [
        "",
        "One",
        "Two",
        "Three",
        "Four",
        "Five",
        "Six",
        "Seven",
        "Eight",
        "Nine",
        "Ten",
        "Eleven",
        "Twelve",
        "Thirteen",
        "Fourteen",
        "Fifteen",
        "Sixteen",
        "Seventeen",
        "Eighteen",
        "Nineteen",
    ]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    scales = ["", "Thousand", "Million", "Billion"]

    def below_thousand(n):
        parts = []
        if n >= 100:
            parts += [ones[n // 100], "Hundred"]
            n %= 100
        if n >= 20:
            parts.append(tens[n // 10])
            n %= 10
        if n:
            parts.append(ones[n])
        return parts

    groups = []
    while num:
        groups.append(num % 1000)
        num //= 1000
    words = []
    for index in range(len(groups) - 1, -1, -1):
        if groups[index]:
            words += below_thousand(groups[index])
            if index:
                words.append(scales[index])
    return " ".join(words)
""",
    ),
    # ---- Reconstruct Original Digits from English (LeetCode 423) ----
    dict(
        title="Reconstruct Original Digits from English",
        diff="M",
        lc=423,
        slug="reconstruct-original-digits-from-english",
        prompt=(
            "s is a scrambled concatenation of the English words for digits ('zero', 'one', ..., 'nine'), each "
            "digit possibly appearing several times. Return the digits in ascending order as a string (s is "
            "guaranteed to be valid)."
        ),
        sig="def original_digits(s: str) -> str:",
        fn="original_digits",
        tests=[
            (("owoztneoer",), "012"),
            (("fviefuro",), "45"),
            (("zero",), "0"),
            (("nine",), "9"),
        ],
        hints=[
            "Some digits own a letter no other digit word uses: z (zero), w (two), u (four), x (six), g (eight).",
            (
                "Once those are counted, other letters become unique after subtracting: h (three, minus eight), f "
                "(five, minus four), s (seven, minus six)."
            ),
            "Then o (one, minus zero, two, four) and finally i (nine, minus five, six, eight).",
        ],
        pattern="Count letters and peel off digits by unique letters",
        explain=(
            "The digit words overlap heavily, but they can be resolved in a fixed order in which every digit has a "
            "letter that only it (or already-counted digits) still contributes. That turns the puzzle into ten "
            "subtractions on a Counter. The brute force instead searches over how many copies of each digit to use, "
            "backtracking until every letter is consumed."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="exponential in the worst case - backtrack over the count of each digit",
        brute=r"""
# BRUTE FORCE: exponential in the worst case - backtrack over the count of each digit
def original_digits(s):
    names = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]

    def solve(digit, remaining):
        if digit == 10:
            return "" if sum(remaining.values()) == 0 else None
        need = Counter(names[digit])
        most = min(remaining[c] // v for c, v in need.items())
        for copies in range(most, -1, -1):
            rest = remaining.copy()
            for c, v in need.items():
                rest[c] -= copies * v
            tail = solve(digit + 1, rest)
            if tail is not None:
                return str(digit) * copies + tail
        return None

    return solve(0, Counter(s))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Count letters and peel off digits by unique letters
def original_digits(s):
    count = Counter(s)
    digits = [0] * 10
    digits[0] = count["z"]
    digits[2] = count["w"]
    digits[4] = count["u"]
    digits[6] = count["x"]
    digits[8] = count["g"]
    digits[3] = count["h"] - digits[8]
    digits[5] = count["f"] - digits[4]
    digits[7] = count["s"] - digits[6]
    digits[1] = count["o"] - digits[0] - digits[2] - digits[4]
    digits[9] = count["i"] - digits[5] - digits[6] - digits[8]
    return "".join(str(d) * digits[d] for d in range(10))
""",
    ),
    # ---- Longest Uncommon Subsequence II (LeetCode 522) ----
    dict(
        title="Longest Uncommon Subsequence II",
        diff="M",
        lc=522,
        slug="longest-uncommon-subsequence-ii",
        prompt=(
            "Given a list of strings, return the length of the longest string that is a subsequence of exactly ONE "
            "of them (an 'uncommon subsequence'), or -1 if there is none."
        ),
        sig="def find_lus_length(strs: List[str]) -> int:",
        fn="find_lus_length",
        tests=[
            ((["aba", "cdc", "eae"],), 3),
            ((["aaa", "aaa", "aa"],), -1),
            ((["a", "b"],), 1),
            ((["abc", "ab"],), 3),
            ((["ab", "ab"],), -1),
        ],
        hints=[
            "If a longest uncommon subsequence exists, you can take it to be one of the input strings itself.",
            "So test each string s: is it a subsequence of any OTHER string in the list?",
            (
                "Check strings from longest to shortest and return the first that is not a subsequence of any other "
                "string; return -1 if none qualifies."
            ),
        ],
        pattern="Candidate = the strings themselves; subsequence test with two pointers",
        explain=(
            "If a proper subsequence of some string were uncommon, the whole string would be uncommon too and "
            "longer (any other string containing the whole string would also contain the subsequence). So only full "
            "strings need testing, each against the others with a linear two-pointer subsequence check. The brute "
            "force enumerates every subsequence of every string and counts how many strings contain it."
        ),
        cx="O(n^2 * L) time, O(1) space",
        brute_cx="O(n * 2^L * n * L) time - enumerate every subsequence of every string",
        brute=r"""
# BRUTE FORCE: O(n * 2^L * n * L) time - enumerate every subsequence of every string
def find_lus_length(strs):
    def is_subsequence(small, big):
        it = iter(big)
        return all(c in it for c in small)

    best = -1
    for i, s in enumerate(strs):
        for size in range(1, len(s) + 1):
            for chosen in itertools.combinations(range(len(s)), size):
                sub = "".join(s[k] for k in chosen)
                if not any(is_subsequence(sub, t) for j, t in enumerate(strs) if j != i):
                    best = max(best, size)
    return best
""",
        solution=r"""
# OPTIMISED: O(n^2 * L) time, O(1) space
# Idea: Candidate = the strings themselves; subsequence test with two pointers
def find_lus_length(strs):
    def is_subsequence(small, big):
        it = iter(big)
        return all(c in it for c in small)

    for i, s in sorted(enumerate(strs), key=lambda item: -len(item[1])):
        if not any(is_subsequence(s, t) for j, t in enumerate(strs) if j != i):
            return len(s)
    return -1
""",
    ),
    # ---- Optimal Division (LeetCode 553) ----
    dict(
        title="Optimal Division",
        diff="M",
        lc=553,
        slug="optimal-division",
        prompt=(
            "The expression nums[0] / nums[1] / ... / nums[n-1] is evaluated left to right, but you may add "
            "parentheses anywhere to change the evaluation order. Return the expression string (with no redundant "
            "parentheses) that has the maximum value. (Every number is at least 2, so the optimal division is "
            "unique.)"
        ),
        sig="def optimal_division(nums: List[int]) -> str:",
        fn="optimal_division",
        tests=[
            (([1000, 100, 10, 2],), "1000/(100/10/2)"),
            (([2, 3, 4],), "2/(3/4)"),
            (([2],), "2"),
            (([2, 3],), "2/3"),
        ],
        hints=[
            "To make a / (...) large, make the denominator as small as possible.",
            (
                "The denominator should be nums[1] / nums[2] / ... / nums[n-1] evaluated left to right (all "
                "dividing), which is the smallest value it can take."
            ),
            (
                "So the answer is nums[0]/(nums[1]/nums[2]/.../nums[n-1]) - with special cases for one and two "
                "numbers, where no parentheses are needed."
            ),
        ],
        pattern="Observation / closed form (maximise numerator, minimise denominator)",
        explain=(
            "Only the first number can stay in the numerator; every other number ends up in the numerator or the "
            "denominator depending on parentheses. Putting parentheses around nums[1..] flips the second number's "
            "neighbours so that all of nums[2..] multiply the result instead of dividing it. Because every value is "
            "at least 2 this beats every other tree. The brute force enumerates all parenthesisations (Catalan "
            "many) with exact fractions."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(Catalan(n) * n) time - evaluate every parenthesisation exactly",
        brute=r"""
# BRUTE FORCE: O(Catalan(n) * n) time - evaluate every parenthesisation exactly
def optimal_division(nums):
    from fractions import Fraction

    def trees(lo, hi):
        if lo == hi:
            return [(Fraction(nums[lo]), str(nums[lo]))]
        options = []
        for mid in range(lo, hi):
            for left_value, left_text in trees(lo, mid):
                for right_value, right_text in trees(mid + 1, hi):
                    text = left_text + "/" + (f"({right_text})" if mid + 1 < hi else right_text)
                    options.append((left_value / right_value, text))
        return options

    return max(trees(0, len(nums) - 1), key=lambda item: item[0])[1]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Observation / closed form (maximise numerator, minimise denominator)
def optimal_division(nums):
    if len(nums) == 1:
        return str(nums[0])
    if len(nums) == 2:
        return f"{nums[0]}/{nums[1]}"
    return f"{nums[0]}/(" + "/".join(map(str, nums[1:])) + ")"
""",
    ),
    # ---- Fraction Addition and Subtraction (LeetCode 592) ----
    dict(
        title="Fraction Addition and Subtraction",
        diff="M",
        lc=592,
        slug="fraction-addition-and-subtraction",
        prompt=(
            "expression is a sum of fractions such as '-1/2+1/3-3/4' (each fraction is numerator/denominator, the "
            "first term may have a sign). Return the result as an irreducible fraction 'a/b'; an integer result is "
            "written with denominator 1 (e.g. '2/1', '0/1')."
        ),
        sig="def fraction_addition(expression: str) -> str:",
        fn="fraction_addition",
        tests=[
            (("-1/2+1/2",), "0/1"),
            (("-1/2+1/2+1/3",), "1/3"),
            (("1/3-1/2",), "-1/6"),
            (("5/3+1/3",), "2/1"),
            (("1/2",), "1/2"),
        ],
        hints=[
            "Keep the running total as one numerator and one denominator.",
            (
                "Adding a/b to n/d gives (n*b + a*d) / (d*b) - reduce by the gcd after each term so the numbers "
                "stay small."
            ),
            "Parse left to right: an optional sign, digits up to '/', digits after it.",
        ],
        pattern="Parsing + exact fraction arithmetic with gcd reduction",
        explain=(
            "Exact integer arithmetic avoids floating-point error. Each term is parsed into sign, numerator and "
            "denominator, the running fraction is combined with the cross-multiplication rule and reduced "
            "immediately. The brute force splits the string on signs and sums with the standard library's Fraction "
            "type."
        ),
        cx="O(length * log M) time",
        brute_cx="O(length) time - split on signs and sum with Fraction",
        brute=r"""
# BRUTE FORCE: O(length) time - split on signs and sum with Fraction
def fraction_addition(expression):
    from fractions import Fraction

    total = Fraction(0)
    for token in expression.replace("-", "+-").split("+"):
        if token:
            total += Fraction(token)
    return f"{total.numerator}/{total.denominator}"
""",
        solution=r"""
# OPTIMISED: O(length * log M) time
# Idea: Parsing + exact fraction arithmetic with gcd reduction
def fraction_addition(expression):
    num, den = 0, 1
    i, n = 0, len(expression)
    while i < n:
        sign = 1
        if expression[i] in "+-":
            sign = -1 if expression[i] == "-" else 1
            i += 1
        j = i
        while expression[j].isdigit():
            j += 1
        a = int(expression[i:j])
        i = j + 1
        j = i
        while j < n and expression[j].isdigit():
            j += 1
        b = int(expression[i:j])
        i = j
        num = num * b + sign * a * den
        den *= b
        g = math.gcd(abs(num), den)
        num //= g
        den //= g
    return f"{num}/{den}"
""",
    ),
    # ---- Remove Comments (LeetCode 722) ----
    dict(
        title="Remove Comments",
        diff="M",
        lc=722,
        slug="remove-comments",
        prompt=(
            "source is a C++ program, one string per line. '//' starts a line comment (the rest of that line is "
            "removed); '/*' starts a block comment that ends at the first following '*/' (it can span lines, and "
            "'/*/' does not close itself). Comment markers inside comments are ignored. Return the source with "
            "comments removed: when a block comment spans lines the text before it and after it join into one line, "
            "and lines that become empty are dropped."
        ),
        sig="def remove_comments(source: List[str]) -> List[str]:",
        fn="remove_comments",
        tests=[
            (
                (
                    [
                        "/*Test program */",
                        "int main()",
                        "{ ",
                        "  // variable declaration ",
                        "int a, b, c;",
                        "/* This is a test",
                        "   multiline  ",
                        "   comment for ",
                        "   testing */",
                        "a = b + c;",
                        "}",
                    ],
                ),
                ["int main()", "{ ", "  ", "int a, b, c;", "a = b + c;", "}"],
            ),
            ((["a/*comment", "line", "more_comment*/b"],), ["ab"]),
            ((["a//b", "c"],), ["a", "c"]),
            ((["/*/ x */y"],), ["y"]),
        ],
        hints=[
            "Scan characters left to right keeping one boolean: are we inside a block comment?",
            "Outside a block: '//' discards the rest of the line, '/*' enters a block, anything else is copied.",
            (
                "Keep the buffer across lines while inside a block comment, and emit it only when a line ends "
                "outside a block and the buffer is non-empty."
            ),
        ],
        pattern="Character state machine (in / out of block comment)",
        explain=(
            "Comments never nest, so a single flag captures the whole state. A block comment swallows newlines, "
            "which is why text before '/*' and after '*/' on different lines end up on the same output line - the "
            "buffer simply persists until the block closes. The brute force joins the lines with newlines, scans "
            "the one long string with find() and splits it again."
        ),
        cx="O(total characters) time",
        brute_cx="O(total characters) time - one long string, jump over comments with find()",
        brute=r"""
# BRUTE FORCE: O(total characters) time - one long string, jump over comments with find()
def remove_comments(source):
    text = "\n".join(source)
    out = ""
    i = 0
    while i < len(text):
        if text.startswith("//", i):
            j = text.find("\n", i)
            i = len(text) if j == -1 else j
        elif text.startswith("/*", i):
            j = text.find("*/", i + 2)
            i = len(text) if j == -1 else j + 2
        else:
            out += text[i]
            i += 1
    return [line for line in out.split("\n") if line]
""",
        solution=r"""
# OPTIMISED: O(total characters) time
# Idea: Character state machine (in / out of block comment)
def remove_comments(source):
    result = []
    in_block = False
    buffer = []
    for line in source:
        i = 0
        if not in_block:
            buffer = []
        while i < len(line):
            if in_block:
                if line[i : i + 2] == "*/":
                    in_block = False
                    i += 2
                else:
                    i += 1
            elif line[i : i + 2] == "/*":
                in_block = True
                i += 2
            elif line[i : i + 2] == "//":
                break
            else:
                buffer.append(line[i])
                i += 1
        if not in_block and buffer:
            result.append("".join(buffer))
    return result
""",
    ),
    # ---- Rotated Digits (LeetCode 788) ----
    dict(
        title="Rotated Digits",
        diff="M",
        lc=788,
        slug="rotated-digits",
        prompt=(
            "Rotating a digit by 180 degrees maps 0,1,8 to themselves, 2<->5 and 6<->9, and 3, 4, 7 to nothing "
            "(invalid). A number is good if every digit rotates to a valid digit and the rotated number is "
            "DIFFERENT from the original. Return how many good numbers are in [1, n]."
        ),
        sig="def rotated_digits(n: int) -> int:",
        fn="rotated_digits",
        tests=[
            ((10,), 4),
            ((1,), 0),
            ((2,), 1),
            ((100,), 40),
            ((857,), 247),
        ],
        hints=[
            (
                "Check one number: no 3/4/7 allowed, and at least one of 2, 5, 6, 9 (otherwise the number rotates "
                "to itself)."
            ),
            (
                "Count in bulk instead: numbers <= n using only digits {0,1,2,5,6,8,9}, minus numbers <= n using "
                "only {0,1,8}."
            ),
            (
                "To count numbers <= n with digits from an allowed set, walk the digits of n: at each position add "
                "(allowed digits smaller than this digit) * |allowed|^(remaining positions), stop if the digit "
                "itself is not allowed."
            ),
        ],
        pattern="Digit counting (inclusion / exclusion on digit sets)",
        explain=(
            "Valid-digit numbers that are not good are exactly those made only of 0, 1 and 8 (they rotate to "
            "themselves). So good = (numbers over the valid digit set) - (numbers over {0,1,8}), and both counts "
            "come from a standard 'numbers <= n over an allowed alphabet' walk along the digits of n. Zero is "
            "counted in both sets and cancels. The brute force tests every number from 1 to n."
        ),
        cx="O(digits) time",
        brute_cx="O(n * digits) time - test every number",
        brute=r"""
# BRUTE FORCE: O(n * digits) time - test every number
def rotated_digits(n):
    count = 0
    for value in range(1, n + 1):
        digits = str(value)
        if any(d in "347" for d in digits):
            continue
        if any(d in "2569" for d in digits):
            count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(digits) time
# Idea: Digit counting (inclusion / exclusion on digit sets)
def rotated_digits(n):
    def count_allowed(limit, allowed):
        text = str(limit)
        total = 0
        for i, ch in enumerate(text):
            digit = int(ch)
            total += sum(1 for a in allowed if a < digit) * len(allowed) ** (len(text) - i - 1)
            if digit not in allowed:
                return total
        return total + 1

    return count_allowed(n, {0, 1, 2, 5, 6, 8, 9}) - count_allowed(n, {0, 1, 8})
""",
    ),
    # ---- Custom Sort String (LeetCode 791) ----
    dict(
        title="Custom Sort String",
        diff="M",
        lc=791,
        slug="custom-sort-string",
        prompt=(
            "order contains distinct lowercase letters. Permute the letters of s so that whenever x occurs before y "
            "in order, x also occurs before y in the result. Letters of s that do not occur in order may be placed "
            "anywhere. Return any valid permutation."
        ),
        sig="def custom_sort_string(order: str, s: str) -> str:",
        fn="custom_sort_string",
        check=_custom_ok,
        tests=[
            (("cba", "abcd"), "cbad"),
            (("bcafg", "abcd"), "bcad"),
            (("a", "bbb"), "bbb"),
            (("xy", "yyxx"), "xxyy"),
        ],
        hints=[
            "Letters not in order are unconstrained - you can append them at the end.",
            "Count how often each letter occurs in s.",
            "Walk through order: emit each letter as many times as it occurs, then emit the remaining letters.",
        ],
        pattern="Counting sort by a custom alphabet",
        explain=(
            "The order string defines a rank for each letter, so the problem is a sort with a custom alphabet. "
            "Counting the letters of s and emitting them in the order of `order` is a counting sort - linear "
            "instead of n log n. The brute force is the general sort with a key (letters missing from order get the "
            "largest rank)."
        ),
        cx="O(len(order) + len(s)) time",
        brute_cx="O(n log n) time - sort s with a rank key",
        brute=r"""
# BRUTE FORCE: O(n log n) time - sort s with a rank key
def custom_sort_string(order, s):
    rank = {c: i for i, c in enumerate(order)}
    return "".join(sorted(s, key=lambda c: rank.get(c, len(order))))
""",
        solution=r"""
# OPTIMISED: O(len(order) + len(s)) time
# Idea: Counting sort by a custom alphabet
def custom_sort_string(order, s):
    count = Counter(s)
    out = []
    for c in order:
        out.append(c * count.pop(c, 0))
    for c, k in count.items():
        out.append(c * k)
    return "".join(out)
""",
    ),
    # ---- Find And Replace in String (LeetCode 833) ----
    dict(
        title="Find And Replace in String",
        diff="M",
        lc=833,
        slug="find-and-replace-in-string",
        prompt=(
            "You have k replacement operations (indices[i], sources[i], targets[i]), all applied to the ORIGINAL "
            "string s at the same time. An operation fires only if sources[i] occurs in s starting at indices[i]; "
            "then that occurrence is replaced by targets[i]. The replaced ranges never overlap. Return the "
            "resulting string."
        ),
        sig="def find_replace_string(s: str, indices: List[int], sources: List[str], targets: List[str]) -> str:",
        fn="find_replace_string",
        tests=[
            (("abcd", [0, 2], ["a", "cd"], ["eee", "ffff"]), "eeebffff"),
            (("abcd", [0, 2], ["ab", "ec"], ["eee", "ffff"]), "eeecd"),
            (("abc", [], [], []), "abc"),
            (("abcde", [3, 0], ["de", "ab"], ["X", "YY"]), "YYcX"),
        ],
        hints=[
            (
                "All operations refer to positions in the ORIGINAL string, so applying them left to right would "
                "shift later positions."
            ),
            (
                "Either sort the operations by index and build a new string left to right, copying the untouched "
                "stretches between them..."
            ),
            "...or apply them from the rightmost index to the leftmost, so earlier indices stay valid.",
        ],
        pattern="Process edits in sorted order (build left to right)",
        explain=(
            "Because the replaced ranges are disjoint, sorting the operations by index lets one pass build the "
            "output: copy the gap before the operation, then either the target (if the source matches) or nothing "
            "special (the original text is copied later). The brute force applies the matching operations right to "
            "left directly on the string, where edits cannot disturb the positions of operations that are still "
            "pending."
        ),
        cx="O(n + k log k) time",
        brute_cx="O(k * n) time - slice-and-rebuild the string for every operation",
        brute=r"""
# BRUTE FORCE: O(k * n) time - slice-and-rebuild the string for every operation
def find_replace_string(s, indices, sources, targets):
    for index, source, target in sorted(zip(indices, sources, targets), reverse=True):
        if s.startswith(source, index):
            s = s[:index] + target + s[index + len(source) :]
    return s
""",
        solution=r"""
# OPTIMISED: O(n + k log k) time
# Idea: Process edits in sorted order (build left to right)
def find_replace_string(s, indices, sources, targets):
    out = []
    pos = 0
    for index, source, target in sorted(zip(indices, sources, targets)):
        if s.startswith(source, index):
            out.append(s[pos:index])
            out.append(target)
            pos = index + len(source)
    out.append(s[pos:])
    return "".join(out)
""",
    ),
    # ---- Buddy Strings (LeetCode 859) ----
    dict(
        title="Buddy Strings",
        diff="E",
        lc=859,
        slug="buddy-strings",
        prompt=(
            "Return True if you can swap exactly two letters of s (at two different positions) so that the result "
            "equals goal."
        ),
        sig="def buddy_strings(s: str, goal: str) -> bool:",
        fn="buddy_strings",
        tests=[
            (("ab", "ba"), True),
            (("ab", "ab"), False),
            (("aa", "aa"), True),
            (("aaaaaaabc", "aaaaaaacb"), True),
            (("", "aa"), False),
        ],
        hints=[
            "The lengths must match.",
            "If s == goal you must still swap: possible only if some letter occurs twice (swap the two equal letters).",
            (
                "Otherwise collect the positions where s and goal differ: there must be exactly two, and swapping "
                "them must fix both."
            ),
        ],
        pattern="Compare mismatch positions (+ duplicate-letter special case)",
        explain=(
            "A single swap changes at most two positions, so s and goal may differ in exactly two places (which "
            "must cross-match), or in none - in which case the swap must be a no-op, available only when two equal "
            "letters exist. The brute force simply tries all pairs of positions."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^3) time - try every swap and compare",
        brute=r"""
# BRUTE FORCE: O(n^3) time - try every swap and compare
def buddy_strings(s, goal):
    if len(s) != len(goal):
        return False
    chars = list(s)
    for i in range(len(chars)):
        for j in range(i + 1, len(chars)):
            chars[i], chars[j] = chars[j], chars[i]
            if "".join(chars) == goal:
                return True
            chars[i], chars[j] = chars[j], chars[i]
    return False
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Compare mismatch positions (+ duplicate-letter special case)
def buddy_strings(s, goal):
    if len(s) != len(goal):
        return False
    if s == goal:
        return len(set(s)) < len(s)
    diff = [i for i in range(len(s)) if s[i] != goal[i]]
    return len(diff) == 2 and s[diff[0]] == goal[diff[1]] and s[diff[1]] == goal[diff[0]]
""",
    ),
    # ---- Decoded String at Index (LeetCode 880) ----
    dict(
        title="Decoded String at Index",
        diff="M",
        lc=880,
        slug="decoded-string-at-index",
        prompt=(
            "An encoded string s (lowercase letters and digits 2-9, starting with a letter) is decoded by reading "
            "left to right with a tape: a letter is written to the tape; a digit d repeats the whole current tape d "
            "times in total. Return the k-th letter (1-indexed) of the final decoded string without building it (it "
            "can be astronomically long)."
        ),
        sig="def decode_at_index(s: str, k: int) -> str:",
        fn="decode_at_index",
        tests=[
            (("leet2code3", 10), "o"),
            (("ha22", 5), "h"),
            (("a2345678999999999999999", 1), "a"),
            (("abc", 2), "b"),
        ],
        hints=[
            "First compute only the LENGTH of the decoded string: a letter adds 1, a digit multiplies by d.",
            (
                "Then walk the string backwards. A digit d means the tape was repeated d times, so position k is "
                "the same as k % (size / d)."
            ),
            (
                "A letter at the end of the tape: if k % size == 0 it is the answer, otherwise drop that letter "
                "(size -= 1)."
            ),
        ],
        pattern="Reverse traversal with modular reduction of the index",
        explain=(
            "Repeating the tape makes the decoded string periodic: position k inside the final tape equals position "
            "k mod (previous size). Undoing the operations from the end - dividing the size for digits, subtracting "
            "one for letters - maps k back to an earlier, shorter tape until k lands exactly on a letter. The brute "
            "force really builds the tape, stopping as soon as it has k characters."
        ),
        cx="O(len(s)) time, O(1) space",
        brute_cx="O(k + len(s)) time - build the decoded tape until it reaches k characters",
        brute=r"""
# BRUTE FORCE: O(k + len(s)) time - build the decoded tape until it reaches k characters
def decode_at_index(s, k):
    tape = ""
    for ch in s:
        if ch.isdigit():
            tape *= int(ch)
        else:
            tape += ch
        if len(tape) >= k:
            break
    return tape[k - 1]
""",
        solution=r"""
# OPTIMISED: O(len(s)) time, O(1) space
# Idea: Reverse traversal with modular reduction of the index
def decode_at_index(s, k):
    size = 0
    for ch in s:
        size = size * int(ch) if ch.isdigit() else size + 1
    for ch in reversed(s):
        k %= size
        if k == 0 and ch.isalpha():
            return ch
        if ch.isdigit():
            size //= int(ch)
        else:
            size -= 1
""",
    ),
    # ---- Reorder Data in Log Files (LeetCode 937) ----
    dict(
        title="Reorder Data in Log Files",
        diff="M",
        lc=937,
        slug="reorder-data-in-log-files",
        prompt=(
            "Each log is 'identifier rest'. A digit-log has only digits in rest; a letter-log has only lowercase "
            "letters (and spaces) in rest. Reorder the logs so that all letter-logs come before all digit-logs; "
            "letter-logs are sorted lexicographically by rest, ties broken by identifier; digit-logs keep their "
            "original relative order."
        ),
        sig="def reorder_log_files(logs: List[str]) -> List[str]:",
        fn="reorder_log_files",
        tests=[
            (
                (["dig1 8 1 5 1", "let1 art can", "dig2 3 6", "let2 own kit dig", "let3 art zero"],),
                ["let1 art can", "let3 art zero", "let2 own kit dig", "dig1 8 1 5 1", "dig2 3 6"],
            ),
            (
                (["a1 9 2 3 1", "g1 act car", "zo4 4 7", "ab1 off key dog", "a8 act zoo"],),
                ["g1 act car", "a8 act zoo", "ab1 off key dog", "a1 9 2 3 1", "zo4 4 7"],
            ),
            ((["a1 1"],), ["a1 1"]),
        ],
        hints=[
            "Split each log at the first space into identifier and rest; check whether rest[0] is a digit.",
            "Give every log a sort key: letter-logs (0, rest, identifier), digit-logs (1,).",
            "Python's sort is stable, so equal keys of digit-logs keep their original order.",
        ],
        pattern="Sort with a composite key (stable sort keeps digit-logs in order)",
        explain=(
            "A tuple key encodes all the rules at once: the first component pushes digit-logs after letter-logs, "
            "letter-logs compare by content then identifier, and digit-logs all share the same key, so a stable "
            "sort leaves them in their input order. The brute force separates the two kinds and insertion-sorts the "
            "letter-logs by hand."
        ),
        cx="O(n log n * L) time",
        brute_cx="O(n^2 * L) time - insertion sort of the letter-logs",
        brute=r"""
# BRUTE FORCE: O(n^2 * L) time - insertion sort of the letter-logs
def reorder_log_files(logs):
    letters, digits = [], []
    for log in logs:
        identifier, rest = log.split(" ", 1)
        if rest[0].isdigit():
            digits.append(log)
        else:
            letters.append((rest, identifier, log))
    ordered = []
    for item in letters:
        position = len(ordered)
        while position > 0 and (item[0], item[1]) < (
            ordered[position - 1][0],
            ordered[position - 1][1],
        ):
            position -= 1
        ordered.insert(position, item)
    return [item[2] for item in ordered] + digits
""",
        solution=r"""
# OPTIMISED: O(n log n * L) time
# Idea: Sort with a composite key (stable sort keeps digit-logs in order)
def reorder_log_files(logs):
    def key(log):
        identifier, rest = log.split(" ", 1)
        if rest[0].isdigit():
            return (1,)
        return (0, rest, identifier)

    return sorted(logs, key=key)
""",
    ),
    # ---- Remove Letter To Equalize Frequency (LeetCode 2423) ----
    dict(
        title="Remove Letter To Equalize Frequency",
        diff="E",
        lc=2423,
        slug="remove-letter-to-equalize-frequency",
        prompt=(
            "Remove exactly one letter from word (word has at least 2 letters). Return True if the remaining "
            "letters all occur the same number of times."
        ),
        sig="def equal_frequency(word: str) -> bool:",
        fn="equal_frequency",
        tests=[
            (("abcc",), True),
            (("aazz",), False),
            (("abbcc",), True),
            (("ab",), True),
            (("aabb",), False),
            (("abc",), True),
        ],
        hints=[
            "Removing a letter lowers one letter's count by 1 (and deletes the letter if its count was 1).",
            "There are at most 26 distinct letters, so you can try decrementing each letter's count.",
            "After the decrement, drop zero counts and check that all remaining counts are equal.",
        ],
        pattern="Frequency map + simulate each possible removal",
        explain=(
            "Which individual occurrence is removed does not matter, only which letter. With at most 26 letters, "
            "trying each letter on the frequency table and checking that the remaining non-zero counts form a "
            "single value costs O(26 * 26). The brute force removes each index and recounts."
        ),
        cx="O(n + 26^2) time",
        brute_cx="O(n^2) time - remove every index and recount",
        brute=r"""
# BRUTE FORCE: O(n^2) time - remove every index and recount
def equal_frequency(word):
    for i in range(len(word)):
        rest = word[:i] + word[i + 1 :]
        if len(set(Counter(rest).values())) <= 1:
            return True
    return False
""",
        solution=r"""
# OPTIMISED: O(n + 26^2) time
# Idea: Frequency map + simulate each possible removal
def equal_frequency(word):
    count = Counter(word)
    for letter in list(count):
        count[letter] -= 1
        remaining = {v for v in count.values() if v > 0}
        count[letter] += 1
        if len(remaining) <= 1:
            return True
    return False
""",
    ),
    # ---- Using a Robot to Print the Lexicographically Smallest String (LeetCode 2434) ----
    dict(
        title="Using a Robot to Print the Lexicographically Smallest String",
        diff="M",
        lc=2434,
        slug="using-a-robot-to-print-the-lexicographically-smallest-string",
        prompt=(
            "A robot holds a string t (initially empty). Operation 1 moves the first character of s to the end of "
            "t. Operation 2 removes the last character of t and writes it on paper. Repeat until both s and t are "
            "empty. Return the lexicographically smallest string that can end up on the paper."
        ),
        sig="def robot_with_string(s: str) -> str:",
        fn="robot_with_string",
        tests=[
            (("zza",), "azz"),
            (("bac",), "abc"),
            (("bdda",), "addb"),
            (("a",), "a"),
        ],
        hints=[
            "t behaves like a stack: you can write the top character at any time.",
            (
                "Write the top of the stack only when it is no larger than every character still in s (otherwise a "
                "smaller letter is still coming)."
            ),
            (
                "Precompute, for each position, the smallest character in the remaining suffix; after pushing s[i], "
                "keep popping while the top <= that suffix minimum. Pop everything at the end."
            ),
        ],
        pattern="Greedy stack + suffix minimum",
        explain=(
            "The paper gets the stack's top characters in pop order, so we want to pop a letter as soon as nothing "
            "smaller can still arrive. A letter c on top is safe to write exactly when every unread character is >= "
            "c (ties are fine: equal letters are interchangeable). Tracking the suffix minimum gives that test in "
            "O(1). The brute force tries every interleaving of pushes and pops."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(2^n) time - explore every sequence of push / pop operations",
        brute=r"""
# BRUTE FORCE: O(2^n) time - explore every sequence of push / pop operations
def robot_with_string(s):
    best = None

    def go(i, stack, out):
        nonlocal best
        if i == len(s) and not stack:
            if best is None or out < best:
                best = out
            return
        if i < len(s):
            go(i + 1, stack + s[i], out)
        if stack:
            go(i, stack[:-1], out + stack[-1])

    go(0, "", "")
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Greedy stack + suffix minimum
def robot_with_string(s):
    n = len(s)
    smallest = ["{"] * (n + 1)
    for i in range(n - 1, -1, -1):
        smallest[i] = min(s[i], smallest[i + 1])
    stack = []
    out = []
    for i, ch in enumerate(s):
        stack.append(ch)
        while stack and stack[-1] <= smallest[i + 1]:
            out.append(stack.pop())
    while stack:
        out.append(stack.pop())
    return "".join(out)
""",
    ),
    # ---- Match Substring After Replacement (LeetCode 2301) ----
    dict(
        title="Match Substring After Replacement",
        diff="H",
        lc=2301,
        slug="match-substring-after-replacement",
        prompt=(
            "mappings[i] = [old, new] means a character old in sub may be replaced by new. Each character of sub "
            "can be replaced at most once (replacements are not chained). Return True if some sequence of "
            "replacements turns sub into a substring of s."
        ),
        sig="def match_replacement(s: str, sub: str, mappings: List[List[str]]) -> bool:",
        fn="match_replacement",
        tests=[
            (("fool3e7bar", "leet", [["e", "3"], ["t", "7"], ["t", "8"]]), True),
            (("fooleetbar", "f00l", [["o", "0"]]), False),
            (("Fool33tbaR", "leetd", [["e", "3"], ["t", "7"], ["t", "8"], ["d", "b"], ["p", "b"]]), True),
            (("a", "a", []), True),
            (("a", "b", [["b", "a"]]), True),
            (("a", "b", [["a", "b"]]), False),
        ],
        hints=[
            (
                "A character of sub matches a character of s if they are equal OR (sub char, s char) is one of the "
                "allowed mappings."
            ),
            "Store the mappings as a set of pairs for O(1) lookup.",
            "Try every starting position in s and compare sub character by character; stop at the first mismatch.",
        ],
        pattern="Sliding comparison with a set of allowed substitutions",
        explain=(
            "Replacements are independent per position and never chained, so a window of s matches sub exactly when "
            "every aligned pair is equal or allowed. That is an O(n * m) window scan with O(1) lookups. The brute "
            "force expands all variants of sub obtainable by replacements and tests each as a substring of s."
        ),
        cx="O(len(s) * len(sub)) time, O(mappings) space",
        brute_cx="O(options^len(sub) * len(s)) time - build every possible variant of sub",
        brute=r"""
# BRUTE FORCE: O(options^len(sub) * len(s)) time - build every possible variant of sub
def match_replacement(s, sub, mappings):
    options = []
    for c in sub:
        choices = {c}
        for old, new in mappings:
            if old == c:
                choices.add(new)
        options.append(sorted(choices))
    for variant in itertools.product(*options):
        if "".join(variant) in s:
            return True
    return False
""",
        solution=r"""
# OPTIMISED: O(len(s) * len(sub)) time, O(mappings) space
# Idea: Sliding comparison with a set of allowed substitutions
def match_replacement(s, sub, mappings):
    allowed = {(old, new) for old, new in mappings}
    m = len(sub)
    for start in range(len(s) - m + 1):
        if all(sub[k] == s[start + k] or (sub[k], s[start + k]) in allowed for k in range(m)):
            return True
    return False
""",
    ),
    # ---- Three Equal Parts (LeetCode 927) ----
    dict(
        title="Three Equal Parts",
        diff="H",
        lc=927,
        slug="three-equal-parts",
        prompt=(
            "arr is a binary array (length >= 3). Find indices i < j - 1 such that arr[0..i], arr[i+1..j-1] and "
            "arr[j..n-1] each represent the SAME binary value (leading zeros are allowed). Return [i, j], or [-1, "
            "-1] if it is impossible; any valid answer is accepted."
        ),
        sig="def three_equal_parts(arr: List[int]) -> List[int]:",
        fn="three_equal_parts",
        check=_three_ok,
        tests=[
            (([1, 0, 1, 0, 1],), [0, 3]),
            (([1, 1, 0, 1, 1],), [-1, -1]),
            (([1, 1, 0, 0, 1],), [0, 2]),
            (([0, 0, 0],), [0, 2]),
            (([1, 0, 0, 1, 0, 0, 1],), [2, 5]),
        ],
        hints=[
            (
                "All three parts have the same value, so they contain the same number of ones: total ones must be "
                "divisible by 3 (and zero ones is a special easy case)."
            ),
            (
                "Find the first one of each third (the k-th, (k+1)-th... ones with k = total / 3). The last part is "
                "fixed: from its first one to the end - leading zeros do not matter, but trailing zeros do."
            ),
            (
                "Compare that pattern with the same-length slices starting at the first one of the other two parts; "
                "the leftover zeros between parts are the leading zeros."
            ),
        ],
        pattern="Count the ones, then compare three aligned slices",
        explain=(
            "Equal values with leading zeros allowed means the parts have identical bit patterns from their first "
            "one onward, so each holds total/3 ones. The third part ends at the array's end, so its pattern (from "
            "its first one) fixes how long the other patterns must be - trailing zeros included. Checking that the "
            "other two slices match, and that they do not overlap, decides it. The brute force tries every pair of "
            "cut positions."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^3) time - try every pair of cuts and compare the values",
        brute=r"""
# BRUTE FORCE: O(n^3) time - try every pair of cuts and compare the values
def three_equal_parts(arr):
    n = len(arr)

    def value(segment):
        return int("".join(map(str, segment)), 2)

    for i in range(n - 2):
        for j in range(i + 2, n):
            if value(arr[: i + 1]) == value(arr[i + 1 : j]) == value(arr[j:]):
                return [i, j]
    return [-1, -1]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Count the ones, then compare three aligned slices
def three_equal_parts(arr):
    n = len(arr)
    total = sum(arr)
    if total == 0:
        return [0, n - 1]
    if total % 3:
        return [-1, -1]
    k = total // 3
    ones = [i for i, v in enumerate(arr) if v]
    a, b, c = ones[0], ones[k], ones[2 * k]
    length = n - c
    if a + length > b or b + length > c:
        return [-1, -1]
    if arr[a : a + length] == arr[b : b + length] == arr[c:]:
        return [a + length - 1, b + length]
    return [-1, -1]
""",
    ),
    # ---- Compare Strings by Frequency of the Smallest Character (LeetCode 1170) ----
    dict(
        title="Compare Strings by Frequency of the Smallest Character",
        diff="M",
        lc=1170,
        slug="compare-strings-by-frequency-of-the-smallest-character",
        prompt=(
            "Let f(s) be the number of occurrences of the smallest letter of s (f('dcce') = 2). For each query, "
            "count the words w with f(query) < f(w). Return the counts in query order."
        ),
        sig="def num_smaller_by_frequency(queries: List[str], words: List[str]) -> List[int]:",
        fn="num_smaller_by_frequency",
        tests=[
            ((["cbd"], ["zaaaz"]), [1]),
            ((["bbb", "cc"], ["a", "aa", "aaa", "aaaa"]), [1, 2]),
            ((["a"], ["a"]), [0]),
            (([], ["a"]), []),
        ],
        hints=[
            "Compute f for every word once.",
            (
                "Comparing every query to every word is O(q * w); instead sort the word frequencies (or count them "
                "in a table)."
            ),
            "For each query, binary-search the number of word frequencies strictly greater than f(query).",
        ],
        pattern="Precompute a value per item, then sorted array + binary search",
        explain=(
            "f(word) depends only on the word, so computing it once and sorting those numbers turns each query into "
            "'how many values are strictly larger than x' - a bisect_right on the sorted list. The brute force "
            "recomputes the comparison for every (query, word) pair."
        ),
        cx="O((q + w) log w) time",
        brute_cx="O(q * w) time - compare every query with every word",
        brute=r"""
# BRUTE FORCE: O(q * w) time - compare every query with every word
def num_smaller_by_frequency(queries, words):
    def f(text):
        return text.count(min(text))

    return [sum(1 for word in words if f(query) < f(word)) for query in queries]
""",
        solution=r"""
# OPTIMISED: O((q + w) log w) time
# Idea: Precompute a value per item, then sorted array + binary search
def num_smaller_by_frequency(queries, words):
    def f(text):
        return text.count(min(text))

    freqs = sorted(f(word) for word in words)
    return [len(freqs) - bisect.bisect_right(freqs, f(query)) for query in queries]
""",
    ),
]
