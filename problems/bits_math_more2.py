"""more Bits & Math problems (batch 3) - part of the problem bank for the "bits_math" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Single Number III (LeetCode 260) ----
    dict(
        title="Single Number III",
        diff="M",
        lc=260,
        slug="single-number-iii",
        prompt=(
            "Every number in the array appears exactly twice except two numbers that appear once. Return those two "
            "numbers (any order) using O(1) extra space."
        ),
        sig="def single_number(nums: List[int]) -> List[int]:",
        fn="single_number",
        compare="unordered",
        tests=[
            (([1, 2, 1, 3, 2, 5],), [3, 5]),
            (([-1, 0],), [-1, 0]),
            (([0, 1],), [0, 1]),
            (([2, 1, 2, 3, 4, 1],), [3, 4]),
        ],
        hints=[
            "XOR of everything cancels the pairs and leaves a ^ b (the two unique numbers combined).",
            "a != b, so a ^ b has at least one set bit - a bit where a and b DIFFER. Isolate one with x & -x.",
            "Split all numbers into two groups by that bit. Each group holds one unique number; XOR each group.",
        ],
        pattern="XOR cancels pairs; split into two groups by a differing bit",
        explain=(
            "Single Number works because x ^ x = 0. With two uniques the total XOR is a ^ b, which is not enough "
            "on\n        its own, so we use any bit where a and b differ to separate them into two independent "
            "Single Number problems."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - count each number",
        brute=r"""
# BRUTE FORCE: O(n^2) time - count each number
def single_number(nums):
    # a number is unique when it appears exactly once in the whole array
    return [x for x in nums if nums.count(x) == 1]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: XOR cancels pairs; split into two groups by a differing bit
def single_number(nums):
    both = 0

    for x in nums:
        both ^= x  # pairs cancel, leaving a ^ b

    low_bit = both & -both  # lowest set bit of a ^ b: a bit where a and b differ
    a = 0

    for x in nums:
        if x & low_bit:  # only numbers having that bit: a (or b) plus cancelling pairs
            a ^= x

    return [a, both ^ a]
""",
    ),
    # ---- Single Number II (LeetCode 137) ----
    dict(
        title="Single Number II",
        diff="M",
        lc=137,
        slug="single-number-ii",
        prompt=(
            "Every number appears exactly three times except one that appears once. Return the number that appears "
            "once."
        ),
        sig="def single_number(nums: List[int]) -> int:",
        fn="single_number",
        tests=[
            (([2, 2, 3, 2],), 3),
            (([0, 1, 0, 1, 0, 1, 99],), 99),
            (([-2, -2, 1, 1, 4, 1, 4, 4, -4, -2],), -4),
            (([7],), 7),
        ],
        hints=[
            "Look at ONE bit position: add that bit over all numbers. The triples contribute multiples of 3.",
            "So (sum of that bit) % 3 is exactly that bit of the unique number.",
            "Do it for all bits at once with two variables 'ones' and 'twos' that count each bit mod 3.",
        ],
        pattern="Count each bit modulo 3 (two bit-masks as a base-3 counter)",
        explain=(
            "XOR is 'count mod 2'. We need 'count mod 3', which needs two bits per position: ones holds bits seen "
            "once\n        (mod 3), twos holds bits seen twice. A bit seen a third time is cleared from both."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - count each number",
        brute=r"""
# BRUTE FORCE: O(n^2) time - count each number
def single_number(nums):
    for x in nums:
        if nums.count(x) == 1:  # appears exactly once
            return x
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Count each bit modulo 3 (two bit-masks as a base-3 counter)
def single_number(nums):
    ones = twos = 0  # ones: bits seen 1 time (mod 3); twos: bits seen 2 times (mod 3)
    for x in nums:
        ones = (ones ^ x) & ~twos  # add x to ones unless that bit is already in twos
        twos = (twos ^ x) & ~ones  # add x to twos unless that bit just landed in ones
    return ones
""",
    ),
    # ---- Bitwise AND of Numbers Range (LeetCode 201) ----
    dict(
        title="Bitwise AND of Numbers Range",
        diff="M",
        lc=201,
        slug="bitwise-and-of-numbers-range",
        prompt="Return the bitwise AND of every integer in the inclusive range [left, right].",
        sig="def range_bitwise_and(left: int, right: int) -> int:",
        fn="range_bitwise_and",
        tests=[
            ((5, 7), 4),
            ((0, 0), 0),
            ((1, 2147483647), 0),
            ((6, 7), 6),
            ((12, 15), 12),
        ],
        hints=[
            "Write left and right in binary. As you count from left to right the low bits flip back and forth.",
            "Any bit that changes anywhere in the range becomes 0 in the AND. Only the common leading prefix survives.",
            "Shift both numbers right until they are equal (count the shifts), then shift the prefix back left.",
        ],
        pattern="Common binary prefix of the two endpoints",
        explain=(
            "If left and right differ, somewhere in the range the lowest differing bit passes through both 0 and 1, "
            "so\n        it and every bit below it is 0 in the result. What remains is the shared prefix."
        ),
        cx="O(log n) time, O(1) space",
        brute_cx="O(right - left) time - AND every number",
        brute=r"""
# BRUTE FORCE: O(right - left) time - AND every number
def range_bitwise_and(left, right):
    result = left
    for x in range(left + 1, right + 1):  # AND the numbers one by one
        result &= x
    return result
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Common binary prefix of the two endpoints
def range_bitwise_and(left, right):
    shifts = 0
    while left != right:  # drop the low bits until only the common prefix is left
        left >>= 1
        right >>= 1
        shifts += 1
    return left << shifts  # put the prefix back; the dropped bits become zeros
""",
    ),
    # ---- Factorial Trailing Zeroes (LeetCode 172) ----
    dict(
        title="Factorial Trailing Zeroes",
        diff="M",
        lc=172,
        slug="factorial-trailing-zeroes",
        prompt="Return the number of trailing zeroes in n! (n factorial).",
        sig="def trailing_zeroes(n: int) -> int:",
        fn="trailing_zeroes",
        tests=[
            ((3,), 0),
            ((5,), 1),
            ((0,), 0),
            ((25,), 6),
            ((100,), 24),
        ],
        hints=[
            "A trailing zero comes from a factor 10 = 2 x 5.",
            "There are always more factors of 2 than of 5 in n!, so just count the factors of 5.",
            (
                "Multiples of 5 give one, multiples of 25 give an extra one, multiples of 125 another... sum n//5 + "
                "n//25 + n//125 + ..."
            ),
        ],
        pattern="Count prime factors (the scarcer prime, 5, decides)",
        explain=(
            "Never compute n! - it is huge. Zeros are decided by the prime factorisation: each 10 needs a 2 and a "
            "5, and\n        5s are rarer. Numbers like 25 contain TWO fives, hence the repeated division."
        ),
        cx="O(log n) time, O(1) space",
        brute_cx="O(n) multiplications on huge numbers - build n! and count zeros",
        brute=r"""
# BRUTE FORCE: O(n) multiplications on huge numbers - build n! and count zeros
def trailing_zeroes(n):
    factorial = 1
    for i in range(2, n + 1):  # build the full factorial
        factorial *= i
    digits = str(factorial)
    return len(digits) - len(digits.rstrip("0"))  # count the zeros at the end
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Count prime factors (the scarcer prime, 5, decides)
def trailing_zeroes(n):
    zeros = 0
    while n:
        n //= 5  # how many multiples of 5, then 25, then 125 ... are <= n
        zeros += n
    return zeros
""",
    ),
    # ---- Palindrome Number (LeetCode 9) ----
    dict(
        title="Palindrome Number",
        diff="E",
        lc=9,
        slug="palindrome-number",
        prompt=(
            "Return True if the integer x reads the same forwards and backwards. Try it without converting to a string."
        ),
        sig="def is_palindrome(x: int) -> bool:",
        fn="is_palindrome",
        tests=[
            ((121,), True),
            ((-121,), False),
            ((10,), False),
            ((0,), True),
            ((12321,), True),
            ((1221,), True),
        ],
        hints=[
            "Negative numbers are never palindromes (the minus sign). A number ending in 0 can only be 0 itself.",
            "You do not need the whole number reversed - only the second half.",
            (
                "Peel digits off the end of x into 'half' until half >= x. Then x == half (even length) or x == "
                "half // 10 (odd length)."
            ),
        ],
        pattern="Reverse only half the digits (no overflow, no string)",
        explain=(
            "Reversing just half avoids both the extra string and any overflow worries. When the halves meet, "
            "the\n        remaining front half must equal the reversed back half; for odd length the middle digit "
            "is ignored."
        ),
        cx="O(log10 n) time, O(1) space",
        brute_cx="O(log10 n) time, O(log10 n) space - convert to string",
        brute=r"""
# BRUTE FORCE: O(log10 n) time, O(log10 n) space - convert to string
def is_palindrome(x):
    text = str(x)  # '-121' reversed is '121-', so negatives fail automatically
    return text == text[::-1]
""",
        solution=r"""
# OPTIMISED: O(log10 n) time, O(1) space
# Idea: Reverse only half the digits (no overflow, no string)
def is_palindrome(x):
    if x < 0 or (x % 10 == 0 and x != 0):  # '-1' or a trailing zero can never be mirrored
        return False
    half = 0  # the back half of x, built in reverse
    while x > half:
        half = half * 10 + x % 10  # move the last digit of x onto half
        x //= 10
    return x == half or x == half // 10  # even length | odd length (drop the middle digit)
""",
    ),
    # ---- Excel Sheet Column Title (LeetCode 168) ----
    dict(
        title="Excel Sheet Column Title",
        diff="E",
        lc=168,
        slug="excel-sheet-column-title",
        prompt="Columns go A..Z, then AA, AB, ... Given the column number (1-indexed) return its title.",
        sig="def convert_to_title(column_number: int) -> str:",
        fn="convert_to_title",
        tests=[
            ((1,), "A"),
            ((28,), "AB"),
            ((701,), "ZY"),
            ((26,), "Z"),
            ((52,), "AZ"),
            ((703,), "AAA"),
        ],
        hints=[
            "It is base 26, but with digits 1..26 instead of 0..25 (there is no zero digit).",
            "The trick: subtract 1 before every step, so A..Z becomes 0..25.",
            "Repeat: n -= 1; letter = chr(65 + n % 26); n //= 26. Build the letters from the right, then reverse.",
        ],
        pattern="Bijective base-26 (subtract 1 each step)",
        explain=(
            "Ordinary base conversion needs a digit for zero. Here Z (26) plays the role of 'zero carries over', "
            "which\n        is why n -= 1 first: it shifts the digit range to 0..25 and the usual divmod works."
        ),
        cx="O(log26 n) time, O(1) space",
        brute_cx="O(n * L) time - count up from 'A' one title at a time",
        brute=r"""
# BRUTE FORCE: O(n * L) time - count up from 'A' one title at a time
def convert_to_title(column_number):
    title = "A"

    for _ in range(column_number - 1):  # step to the next column title column_number - 1 times
        letters = list(title)
        i = len(letters) - 1

        while i >= 0 and letters[i] == "Z":  # Z rolls over to A and carries left
            letters[i] = "A"
            i -= 1

        if i < 0:
            letters.insert(0, "A")  # AZZ -> AAAA style growth
        else:
            letters[i] = chr(ord(letters[i]) + 1)

        title = "".join(letters)

    return title
""",
        solution=r"""
# OPTIMISED: O(log26 n) time, O(1) space
# Idea: Bijective base-26 (subtract 1 each step)
def convert_to_title(column_number):
    letters = []
    n = column_number
    while n > 0:
        n -= 1  # shift 1..26 to 0..25 so the usual base conversion works
        letters.append(chr(ord("A") + n % 26))  # the last letter
        n //= 26
    return "".join(reversed(letters))
""",
    ),
    # ---- Excel Sheet Column Number (LeetCode 171) ----
    dict(
        title="Excel Sheet Column Number",
        diff="E",
        lc=171,
        slug="excel-sheet-column-number",
        prompt="Given a column title like 'AB', return its column number (A = 1, Z = 26, AA = 27, ...).",
        sig="def title_to_number(column_title: str) -> int:",
        fn="title_to_number",
        tests=[
            (("A",), 1),
            (("AB",), 28),
            (("ZY",), 701),
            (("Z",), 26),
            (("AAA",), 703),
        ],
        hints=[
            "This is reading a number in base 26 where A = 1 ... Z = 26.",
            "Scan left to right. Each new letter shifts everything so far one place: total = total * 26 + value.",
            "value of a letter = ord(letter) - ord('A') + 1.",
        ],
        pattern="Positional number system (Horner's rule in base 26)",
        explain=(
            "'AB' means 1 * 26 + 2. Multiplying the running total by the base before adding the next digit "
            "processes the\n        number in a single pass - exactly how you parse '123' as ((1)*10 + 2)*10 + 3."
        ),
        cx="O(L) time, O(1) space",
        brute_cx="O(answer * L) time - count titles upward until it matches",
        brute=r"""
# BRUTE FORCE: O(answer * L) time - count titles upward until it matches
def title_to_number(column_title):
    title, number = "A", 1

    while title != column_title:  # walk through A, B, ..., Z, AA, AB, ... until we reach the target
        letters = list(title)
        i = len(letters) - 1

        while i >= 0 and letters[i] == "Z":
            letters[i] = "A"
            i -= 1

        if i < 0:
            letters.insert(0, "A")
        else:
            letters[i] = chr(ord(letters[i]) + 1)

        title = "".join(letters)
        number += 1

    return number
""",
        solution=r"""
# OPTIMISED: O(L) time, O(1) space
# Idea: Positional number system (Horner's rule in base 26)
def title_to_number(column_title):
    total = 0
    for ch in column_title:
        total = total * 26 + (ord(ch) - ord("A") + 1)  # shift the old digits, add the new one
    return total
""",
    ),
    # ---- Power of Three (LeetCode 326) ----
    dict(
        title="Power of Three",
        diff="E",
        lc=326,
        slug="power-of-three",
        prompt="Return True if n is a power of three (1, 3, 9, 27, ...).",
        sig="def is_power_of_three(n: int) -> bool:",
        fn="is_power_of_three",
        tests=[
            ((27,), True),
            ((0,), False),
            ((-1,), False),
            ((9,), True),
            ((45,), False),
            ((1,), True),
        ],
        hints=[
            "Negative numbers and 0 are never powers of three.",
            "Loop: while n is divisible by 3, divide by 3. A power of three ends at exactly 1.",
            (
                "Loop-free trick: 3^19 = 1162261467 is the biggest power of three that fits in 32 bits, and only "
                "powers of three divide it."
            ),
        ],
        pattern="Divisibility of the largest power (3 is prime)",
        explain=(
            "Because 3 is prime, the only divisors of 3^19 are 3^0, 3^1, ..., 3^19. So n divides 3^19 exactly when "
            "n is a\n        power of three - one modulo operation, no loop."
        ),
        cx="O(1) time, O(1) space",
        brute_cx="O(log3 n) time - build powers of three until we pass n",
        brute=r"""
# BRUTE FORCE: O(log3 n) time - build powers of three until we pass n
def is_power_of_three(n):
    if n < 1:
        return False
    power = 1
    while power < n:  # 1, 3, 9, 27, ... until we reach or pass n
        power *= 3
    return power == n
""",
        solution=r"""
# OPTIMISED: O(1) time, O(1) space
# Idea: Divisibility of the largest power (3 is prime)
def is_power_of_three(n):
    # 3**19 is the largest power of three below 2**31; its only divisors are smaller powers of three
    return n > 0 and 3**19 % n == 0
""",
    ),
    # ---- Ugly Number (LeetCode 263) ----
    dict(
        title="Ugly Number",
        diff="E",
        lc=263,
        slug="ugly-number",
        prompt=(
            "An ugly number is a positive integer whose only prime factors are 2, 3 and 5. Return True if n is ugly."
        ),
        sig="def is_ugly(n: int) -> bool:",
        fn="is_ugly",
        tests=[
            ((6,), True),
            ((1,), True),
            ((14,), False),
            ((0,), False),
            ((-6,), False),
            ((30,), True),
        ],
        hints=[
            "Zero and negatives are not ugly. One is ugly (no prime factors at all).",
            "Divide out every factor of 2, then 3, then 5.",
            "If what is left is 1, nothing but 2, 3, 5 divided it. Anything else left over is another prime factor.",
        ],
        pattern="Strip the allowed prime factors, check what is left",
        explain=(
            "Instead of listing all prime factors, remove the 'allowed' ones and see whether anything survives. "
            "A\n        leftover bigger than 1 must itself contain a forbidden prime."
        ),
        cx="O(log n) time, O(1) space",
        brute_cx="O(sqrt n) time - full trial-division factorisation",
        brute=r"""
# BRUTE FORCE: O(sqrt n) time - full trial-division factorisation
def is_ugly(n):
    if n < 1:
        return False

    factors, d = set(), 2

    while d * d <= n:  # trial division collects every prime factor
        while n % d == 0:
            factors.add(d)
            n //= d
        d += 1

    if n > 1:
        factors.add(n)  # what remains is itself a prime

    return factors <= {2, 3, 5}
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Strip the allowed prime factors, check what is left
def is_ugly(n):
    if n < 1:
        return False
    for p in (2, 3, 5):
        while n % p == 0:  # remove every allowed prime factor
            n //= p
    return n == 1  # anything left is a forbidden prime
""",
    ),
    # ---- Integer to Roman (LeetCode 12) ----
    dict(
        title="Integer to Roman",
        diff="M",
        lc=12,
        slug="integer-to-roman",
        prompt=(
            "Convert an integer from 1 to 3999 into a Roman numeral (use subtractive forms like IV, IX, XL, XC, CD, "
            "CM)."
        ),
        sig="def int_to_roman(num: int) -> str:",
        fn="int_to_roman",
        tests=[
            ((3749,), "MMMDCCXLIX"),
            ((58,), "LVIII"),
            ((1994,), "MCMXCIV"),
            ((4,), "IV"),
            ((9,), "IX"),
            ((3999,), "MMMCMXCIX"),
        ],
        hints=[
            "Roman numerals add up symbols from big to small: M=1000, D=500, C=100, L=50, X=10, V=5, I=1.",
            "Treat the six subtractive pairs (CM, CD, XC, XL, IX, IV) as extra 'symbols' so no special cases remain.",
            (
                "Walk the 13 values from largest to smallest: while num >= value, append the symbol and subtract "
                "the value."
            ),
        ],
        pattern="Greedy over a descending value table",
        explain=(
            "The table (1000, 900, 500, 400, ..., 4, 1) makes greedy correct: taking the largest value that still "
            "fits\n        always yields the canonical numeral, because each subtractive pair is itself in the "
            "table."
        ),
        cx="O(1) time (at most 13 table rows, bounded output)",
        brute_cx="O(num) time - write the additive form, then fix the 4s and 9s",
        brute=r"""
# BRUTE FORCE: O(num) time - write the additive form, then fix the 4s and 9s
def int_to_roman(num):
    # step 1: the simple additive numeral using only I V X L C D M (so 4 is 'IIII')
    result = ""

    for value, symbol in (
        (1000, "M"),
        (500, "D"),
        (100, "C"),
        (50, "L"),
        (10, "X"),
        (5, "V"),
        (1, "I"),
    ):
        while num >= value:
            result += symbol
            num -= value

    # step 2: rewrite the long forms into the subtractive ones
    for long_form, short_form in (
        ("DCCCC", "CM"),
        ("CCCC", "CD"),
        ("LXXXX", "XC"),
        ("XXXX", "XL"),
        ("VIIII", "IX"),
        ("IIII", "IV"),
    ):
        result = result.replace(long_form, short_form)

    return result
""",
        solution=r"""
# OPTIMISED: O(1) time (at most 13 table rows, bounded output)
# Idea: Greedy over a descending value table
def int_to_roman(num):
    table = [
        (1000, "M"),
        (900, "CM"),
        (500, "D"),
        (400, "CD"),
        (100, "C"),
        (90, "XC"),
        (50, "L"),
        (40, "XL"),
        (10, "X"),
        (9, "IX"),
        (5, "V"),
        (4, "IV"),
        (1, "I"),
    ]
    out = []

    for value, symbol in table:
        while num >= value:  # take the biggest value that still fits
            out.append(symbol)
            num -= value

    return "".join(out)
""",
    ),
]
