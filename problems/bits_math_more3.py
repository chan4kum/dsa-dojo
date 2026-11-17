"""more Bits and Math problems (batch 4) - part of the problem bank for the "bits_math" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Power of Four (LeetCode 342) ----
    dict(
        title="Power of Four",
        diff="E",
        lc=342,
        slug="power-of-four",
        prompt="Return True if n is a power of four (1, 4, 16, 64, ...).",
        sig="def is_power_of_four(n: int) -> bool:",
        fn="is_power_of_four",
        tests=[
            ((16,), True),
            ((5,), False),
            ((1,), True),
            ((64,), True),
            ((8,), False),
            ((-4,), False),
            ((0,), False),
        ],
        hints=[
            "Repeatedly dividing by 4 works: it must end exactly at 1.",
            "A power of four is a power of two (one set bit) - check n & (n - 1) == 0 and n > 0.",
            "The single bit must sit at an EVEN position: AND with 0x55555555 (bits 0, 2, 4, ...) must be non-zero.",
        ],
        pattern="Bit tricks: single set bit + position mask",
        explain=(
            "n & (n-1) clears the lowest set bit, so the result is 0 only when exactly one bit is set. The mask "
            "0x5555... keeps only even bit positions, separating 4^k from 2 * 4^k."
        ),
        cx="O(1) time and space",
        brute_cx="O(log n) time - divide by 4 repeatedly",
        brute=r"""
# BRUTE FORCE: O(log n) time - divide by 4 repeatedly
def is_power_of_four(n):
    if n < 1:
        return False
    while n % 4 == 0:
        n //= 4
    return n == 1
""",
        solution=r"""
# OPTIMISED: O(1) time and space
# Idea: Bit tricks: single set bit + position mask
def is_power_of_four(n):
    return n > 0 and n & (n - 1) == 0 and n & 0x55555555 != 0
""",
    ),
    # ---- Convert a Number to Hexadecimal (LeetCode 405) ----
    dict(
        title="Convert a Number to Hexadecimal",
        diff="E",
        lc=405,
        slug="convert-a-number-to-hexadecimal",
        prompt=(
            "Return the lowercase hexadecimal string of a 32-bit signed integer. Negative numbers use two's "
            "complement (so -1 is 'ffffffff'). No leading zeros except for 0 itself."
        ),
        sig="def to_hex(num: int) -> str:",
        fn="to_hex",
        tests=[
            ((26,), "1a"),
            ((-1,), "ffffffff"),
            ((0,), "0"),
            ((255,), "ff"),
            ((-2147483648,), "80000000"),
            ((16,), "10"),
        ],
        hints=[
            "Hex digit = 4 bits. Take the number 4 bits at a time with `& 15`.",
            "For a negative number add 2**32 first (or mask with 0xFFFFFFFF) to get its two's complement bits.",
            "Collect digits from the least significant end and reverse; stop when the value reaches 0.",
        ],
        pattern="Bit masking and shifting, 4 bits per hex digit",
        explain=(
            "Masking with 0xFFFFFFFF turns any signed 32-bit value into the unsigned number with the same bit pattern."
        ),
        cx="O(1) - at most 8 digits",
        brute_cx="O(1) - repeated divmod by 16 (arithmetic instead of bit operations)",
        brute=r"""
# BRUTE FORCE: O(1) - repeated divmod by 16 (arithmetic instead of bit operations)
def to_hex(num):
    if num == 0:
        return "0"

    if num < 0:
        num += 2**32  # two's complement

    digits = "0123456789abcdef"
    out = ""

    while num > 0:
        num, rem = divmod(num, 16)
        out = digits[rem] + out

    return out
""",
        solution=r"""
# OPTIMISED: O(1) - at most 8 digits
# Idea: Bit masking and shifting, 4 bits per hex digit
def to_hex(num):
    if num == 0:
        return "0"

    num &= 0xFFFFFFFF  # same bits as a 32-bit unsigned number
    digits, out = "0123456789abcdef", []

    while num:
        out.append(digits[num & 15])  # lowest 4 bits
        num >>= 4

    return "".join(reversed(out))
""",
    ),
    # ---- Number Complement (LeetCode 476) ----
    dict(
        title="Number Complement",
        diff="E",
        lc=476,
        slug="number-complement",
        prompt=(
            "Flip every bit of a positive integer's binary representation (no leading zeros) and return the "
            "resulting number."
        ),
        sig="def find_complement(num: int) -> int:",
        fn="find_complement",
        tests=[
            ((5,), 2),
            ((1,), 0),
            ((10,), 5),
            ((7,), 0),
            ((8,), 7),
        ],
        hints=[
            "Only the bits up to the highest set bit count - leading zeros stay out of it.",
            "XOR with 1 flips a bit.",
            "Build a mask of ones as long as the number (1 << bit_length) - 1 and XOR the number with it.",
        ],
        pattern="XOR with an all-ones mask",
        explain=(
            "XOR flips exactly the masked bits; the mask length equals the number's bit length so leading zeros are "
            "untouched."
        ),
        cx="O(1)",
        brute_cx="O(log n) - flip the characters of the binary string",
        brute=r"""
# BRUTE FORCE: O(log n) - flip the characters of the binary string
def find_complement(num):
    flipped = "".join("1" if ch == "0" else "0" for ch in bin(num)[2:])
    return int(flipped, 2)
""",
        solution=r"""
# OPTIMISED: O(1)
# Idea: XOR with an all-ones mask
def find_complement(num):
    mask = (1 << num.bit_length()) - 1  # ones over exactly the significant bits
    return num ^ mask
""",
    ),
    # ---- Binary Number with Alternating Bits (LeetCode 693) ----
    dict(
        title="Binary Number with Alternating Bits",
        diff="E",
        lc=693,
        slug="binary-number-with-alternating-bits",
        prompt=(
            "Return True if a positive integer's binary representation has adjacent bits that always differ (like "
            "101010)."
        ),
        sig="def has_alternating_bits(n: int) -> bool:",
        fn="has_alternating_bits",
        tests=[
            ((5,), True),
            ((7,), False),
            ((11,), False),
            ((10,), True),
            ((1,), True),
            ((2,), True),
        ],
        hints=[
            "Compare each bit with its neighbour, e.g. on the binary string.",
            "n ^ (n >> 1) compares every bit with the one above it.",
            "For an alternating number that XOR is all ones (like 0111), and x & (x + 1) == 0 tests 'all ones'.",
        ],
        pattern="Shift-and-XOR to compare neighbouring bits",
        explain=(
            "If all neighbours differ, n ^ (n >> 1) has ones everywhere below the top bit - a number of the form "
            "2^k - 1."
        ),
        cx="O(1)",
        brute_cx="O(log n) - scan the binary string",
        brute=r"""
# BRUTE FORCE: O(log n) - scan the binary string
def has_alternating_bits(n):
    bits = bin(n)[2:]
    return all(a != b for a, b in zip(bits, bits[1:]))
""",
        solution=r"""
# OPTIMISED: O(1)
# Idea: Shift-and-XOR to compare neighbouring bits
def has_alternating_bits(n):
    x = n ^ (n >> 1)  # ones wherever a bit differs from its upper neighbour
    return x & (x + 1) == 0  # x is of the form 111...1
""",
    ),
    # ---- Prime Number of Set Bits in Binary Representation (LeetCode 762) ----
    dict(
        title="Prime Number of Set Bits in Binary Representation",
        diff="E",
        lc=762,
        slug="prime-number-of-set-bits-in-binary-representation",
        prompt="Count the integers in [left, right] whose binary representation has a PRIME number of 1 bits.",
        sig="def count_prime_set_bits(left: int, right: int) -> int:",
        fn="count_prime_set_bits",
        tests=[
            ((6, 10), 4),
            ((10, 15), 5),
            ((1, 1), 0),
            ((3, 3), 1),
            ((1, 20), 14),
        ],
        hints=[
            "Count the 1 bits of each number (bin(x).count('1')).",
            "right <= 10^6 < 2^20 so the bit count never exceeds 19.",
            "Precompute the set of primes up to 19 once: {2, 3, 5, 7, 11, 13, 17, 19} and test membership.",
        ],
        pattern="Popcount + tiny precomputed prime set",
        explain="The popcount range is tiny, so a constant-size prime lookup replaces trial division for every number.",
        cx="O((right - left) * popcount)",
        brute_cx="O((right - left) * sqrt(bits)) - trial division per number",
        brute=r"""
# BRUTE FORCE: O((right - left) * sqrt(bits)) - trial division per number
def count_prime_set_bits(left, right):
    def is_prime(k):
        if k < 2:
            return False
        return all(k % d for d in range(2, int(k**0.5) + 1))

    return sum(1 for x in range(left, right + 1) if is_prime(bin(x).count("1")))
""",
        solution=r"""
# OPTIMISED: O((right - left) * popcount)
# Idea: Popcount + tiny precomputed prime set
def count_prime_set_bits(left, right):
    primes = {2, 3, 5, 7, 11, 13, 17, 19}  # popcount of numbers below 2**20 is at most 19
    return sum(1 for x in range(left, right + 1) if bin(x).count("1") in primes)
""",
    ),
    # ---- Binary Gap (LeetCode 868) ----
    dict(
        title="Binary Gap",
        diff="E",
        lc=868,
        slug="binary-gap",
        prompt=(
            "Return the longest distance between two ADJACENT 1 bits in the binary form of n (0 if there are fewer "
            "than two 1s)."
        ),
        sig="def binary_gap(n: int) -> int:",
        fn="binary_gap",
        tests=[
            ((22,), 2),
            ((8,), 0),
            ((5,), 2),
            ((6,), 1),
            ((1,), 0),
            ((13,), 2),
        ],
        hints=[
            "Record the position of every 1 bit.",
            "The answer is the largest difference between consecutive positions.",
            "No list needed: scan bits from the bottom, remembering the position of the last 1 seen.",
        ],
        pattern="Single bit scan remembering the previous set bit",
        explain="Adjacent ones are consecutive in scan order, so one variable for 'last position' is enough.",
        cx="O(log n) time, O(1) space",
        brute_cx="O(log n) time, O(log n) space - list of positions",
        brute=r"""
# BRUTE FORCE: O(log n) time, O(log n) space - list of positions
def binary_gap(n):
    positions = [i for i, ch in enumerate(bin(n)[2:]) if ch == "1"]
    return max((b - a for a, b in zip(positions, positions[1:])), default=0)
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: Single bit scan remembering the previous set bit
def binary_gap(n):
    best, last, pos = 0, -1, 0

    while n:
        if n & 1:
            if last != -1:
                best = max(best, pos - last)
            last = pos
        n >>= 1
        pos += 1

    return best
""",
    ),
    # ---- Number of Steps to Reduce a Number to Zero (LeetCode 1342) ----
    dict(
        title="Number of Steps to Reduce a Number to Zero",
        diff="E",
        lc=1342,
        slug="number-of-steps-to-reduce-a-number-to-zero",
        prompt="Each step: if num is even divide it by 2, otherwise subtract 1. Return the number of steps to reach 0.",
        sig="def number_of_steps(num: int) -> int:",
        fn="number_of_steps",
        tests=[
            ((14,), 6),
            ((8,), 4),
            ((123,), 12),
            ((0,), 0),
            ((1,), 1),
        ],
        hints=[
            "Simulating works in O(log n) steps - try it.",
            "Dividing by 2 is a right shift; subtracting 1 from an odd number clears its lowest bit.",
            (
                "Every bit costs one step to clear (the subtraction, for 1 bits) and each position except the top "
                "costs one halving: bit_length - 1 + popcount."
            ),
        ],
        pattern="Count bit operations instead of simulating",
        explain="A halving happens once per bit position below the top, and a subtraction once for every set bit.",
        cx="O(1) with bit_length and popcount",
        brute_cx="O(log n) - simulate the process",
        brute=r"""
# BRUTE FORCE: O(log n) - simulate the process
def number_of_steps(num):
    steps = 0
    while num:
        num = num // 2 if num % 2 == 0 else num - 1
        steps += 1
    return steps
""",
        solution=r"""
# OPTIMISED: O(1) with bit_length and popcount
# Idea: Count bit operations instead of simulating
def number_of_steps(num):
    if num == 0:
        return 0
    return num.bit_length() - 1 + bin(num).count("1")  # halvings + subtractions
""",
    ),
    # ---- Add to Array-Form of Integer (LeetCode 989) ----
    dict(
        title="Add to Array-Form of Integer",
        diff="E",
        lc=989,
        slug="add-to-array-form-of-integer",
        prompt=(
            "num is a non-negative integer written as a list of digits (most significant first). Return the digit "
            "list of num + k."
        ),
        sig="def add_to_array_form(num: List[int], k: int) -> List[int]:",
        fn="add_to_array_form",
        tests=[
            (([1, 2, 0, 0], 34), [1, 2, 3, 4]),
            (([2, 7, 4], 181), [4, 5, 5]),
            (([2, 1, 5], 806), [1, 0, 2, 1]),
            (([0], 23), [2, 3]),
            (([9, 9, 9], 1), [1, 0, 0, 0]),
        ],
        hints=[
            "Convert to an integer, add, convert back - fine in Python, but not in languages with 32-bit integers.",
            "Do schoolbook addition from the last digit, carrying 1s.",
            (
                "Treat k itself as the carry: digit = (num[i] + k) % 10, then k = (num[i] + k) // 10. Keep going "
                "while k > 0."
            ),
        ],
        pattern="Schoolbook addition with k doubling as the carry",
        explain=(
            "Adding k to the last digit and feeding the quotient back into k handles both the carry and the extra "
            "digits of k."
        ),
        cx="O(max(n, digits of k)) time",
        brute_cx="O(n) time - convert to a big integer (fails in fixed-width languages)",
        brute=r"""
# BRUTE FORCE: O(n) time - convert to a big integer (fails in fixed-width languages)
def add_to_array_form(num, k):
    total = int("".join(map(str, num))) + k
    return [int(ch) for ch in str(total)]
""",
        solution=r"""
# OPTIMISED: O(max(n, digits of k)) time
# Idea: Schoolbook addition with k doubling as the carry
def add_to_array_form(num, k):
    out = []
    i = len(num) - 1

    while i >= 0 or k:
        if i >= 0:
            k += num[i]  # k now holds digit + carry + remaining digits of k
            i -= 1
        k, digit = divmod(k, 10)
        out.append(digit)

    return out[::-1]
""",
    ),
    # ---- Base 7 (LeetCode 504) ----
    dict(
        title="Base 7",
        diff="E",
        lc=504,
        slug="base-7",
        prompt="Return the base-7 representation of an integer as a string (negative numbers get a leading minus).",
        sig="def convert_to_base7(num: int) -> str:",
        fn="convert_to_base7",
        tests=[
            ((100,), "202"),
            ((-7,), "-10"),
            ((0,), "0"),
            ((7,), "10"),
            ((-1,), "-1"),
            ((48,), "66"),
        ],
        hints=[
            "Same idea as binary: repeatedly take the remainder when dividing by the base.",
            "Remainders come out least significant first - reverse at the end.",
            "Handle the sign separately: work with abs(num), prefix '-' at the end; num == 0 gives '0'.",
        ],
        pattern="Repeated division to change base",
        explain="num % 7 is the lowest digit and num // 7 is what remains for the higher digits.",
        cx="O(log7 n)",
        brute_cx="O(log7 n) - greedy from the largest power of 7 downwards",
        brute=r"""
# BRUTE FORCE: O(log7 n) - greedy from the largest power of 7 downwards
def convert_to_base7(num):
    if num == 0:
        return "0"

    sign, n = ("-" if num < 0 else ""), abs(num)
    power = 1

    while power * 7 <= n:
        power *= 7  # largest power of 7 that fits

    digits = ""

    while power:
        digits += str(n // power)  # how many times this power fits
        n %= power
        power //= 7

    return sign + digits
""",
        solution=r"""
# OPTIMISED: O(log7 n)
# Idea: Repeated division to change base
def convert_to_base7(num):
    if num == 0:
        return "0"
    n, digits = abs(num), []
    while n:
        n, rem = divmod(n, 7)
        digits.append(str(rem))  # least significant digit first
    return ("-" if num < 0 else "") + "".join(reversed(digits))
""",
    ),
    # ---- Add Digits (LeetCode 258) ----
    dict(
        title="Add Digits",
        diff="E",
        lc=258,
        slug="add-digits",
        prompt="Repeatedly replace num by the sum of its digits until a single digit remains. Return it.",
        sig="def add_digits(num: int) -> int:",
        fn="add_digits",
        tests=[
            ((38,), 2),
            ((0,), 0),
            ((9,), 9),
            ((10,), 1),
            ((99,), 9),
            ((12345,), 6),
        ],
        hints=[
            "A loop that sums digits until num < 10 works.",
            "The digit sum of a number has the same remainder mod 9 as the number itself.",
            "So the answer is 0 for 0, else 1 + (num - 1) % 9 (the 'digital root').",
        ],
        pattern="Digital root via modulo 9",
        explain=(
            "10 ≡ 1 (mod 9), so every digit sum keeps the value mod 9; the digital root is that remainder, with 9 "
            "instead of 0 for non-zero multiples of 9."
        ),
        cx="O(1)",
        brute_cx="O(log n) per round - simulate the digit sums",
        brute=r"""
# BRUTE FORCE: O(log n) per round - simulate the digit sums
def add_digits(num):
    while num >= 10:
        num = sum(int(ch) for ch in str(num))
    return num
""",
        solution=r"""
# OPTIMISED: O(1)
# Idea: Digital root via modulo 9
def add_digits(num):
    return 0 if num == 0 else 1 + (num - 1) % 9
""",
    ),
    # ---- Minimum Bit Flips to Convert Number (LeetCode 2220) ----
    dict(
        title="Minimum Bit Flips to Convert Number",
        diff="E",
        lc=2220,
        slug="minimum-bit-flips-to-convert-number",
        prompt="Return the minimum number of single-bit flips needed to turn start into goal.",
        sig="def min_bit_flips(start: int, goal: int) -> int:",
        fn="min_bit_flips",
        tests=[
            ((10, 7), 3),
            ((3, 4), 3),
            ((0, 0), 0),
            ((5, 5), 0),
            ((8, 1), 2),
        ],
        hints=[
            "Each differing bit position needs exactly one flip.",
            "XOR has a 1 exactly where two numbers differ.",
            "The answer is the number of set bits of start ^ goal (Hamming distance).",
        ],
        pattern="XOR + popcount (Hamming distance)",
        explain="XOR marks every differing position; counting its ones counts the required flips.",
        cx="O(log max) time",
        brute_cx="O(log max) time - compare bit by bit",
        brute=r"""
# BRUTE FORCE: O(log max) time - compare bit by bit
def min_bit_flips(start, goal):
    flips = 0
    for i in range(32):
        if (start >> i) & 1 != (goal >> i) & 1:
            flips += 1
    return flips
""",
        solution=r"""
# OPTIMISED: O(log max) time
# Idea: XOR + popcount (Hamming distance)
def min_bit_flips(start, goal):
    diff, flips = start ^ goal, 0
    while diff:
        diff &= diff - 1  # Kernighan: drop the lowest set bit
        flips += 1
    return flips
""",
    ),
    # ---- Divide Two Integers (LeetCode 29) ----
    dict(
        title="Divide Two Integers",
        diff="M",
        lc=29,
        slug="divide-two-integers",
        prompt=(
            "Return dividend / divisor truncated toward zero WITHOUT using *, / or %. If the result is outside the "
            "signed 32-bit range, clamp it to [-2**31, 2**31 - 1]. The divisor is never 0."
        ),
        sig="def divide(dividend: int, divisor: int) -> int:",
        fn="divide",
        tests=[
            ((10, 3), 3),
            ((7, -3), -2),
            ((-7, 2), -3),
            ((0, 1), 0),
            ((1, 1), 1),
            ((-2147483648, -1), 2147483647),
        ],
        hints=[
            "Repeated subtraction counts the quotient but takes dividend / divisor steps - too slow for big inputs.",
            (
                "Double the divisor (shift left) until it would exceed the dividend; each doubling is a "
                "power-of-two multiple."
            ),
            "Subtract the largest such multiple, add its power of two to the answer, and repeat with the remainder.",
        ],
        pattern="Binary long division with shifts",
        explain=(
            "Every quotient is a sum of distinct powers of two. Greedily subtracting the biggest divisor << k finds "
            "them in O(log^2 n)."
        ),
        cx="O(log^2 n) time",
        brute_cx="O(dividend / divisor) time - repeated subtraction",
        brute=r"""
# BRUTE FORCE: O(dividend / divisor) time - repeated subtraction
def divide(dividend, divisor):
    negative = (dividend < 0) != (divisor < 0)
    a, b, count = abs(dividend), abs(divisor), 0
    while a >= b:  # one subtraction per unit of quotient
        a -= b
        count += 1
    result = -count if negative else count
    return max(-(2**31), min(2**31 - 1, result))
""",
        solution=r"""
# OPTIMISED: O(log^2 n) time
# Idea: Binary long division with shifts
def divide(dividend, divisor):
    negative = (dividend < 0) != (divisor < 0)
    a, b, quotient = abs(dividend), abs(divisor), 0

    for shift in range(31, -1, -1):  # try the biggest multiples first
        if (b << shift) <= a:
            a -= b << shift
            quotient += 1 << shift

    result = -quotient if negative else quotient

    return max(-(2**31), min(2**31 - 1, result))
""",
    ),
    # ---- XOR Operation in an Array (LeetCode 1486) ----
    dict(
        title="XOR Operation in an Array",
        diff="E",
        lc=1486,
        slug="xor-operation-in-an-array",
        prompt="Let nums[i] = start + 2 * i for 0 <= i < n. Return the XOR of all the elements of nums.",
        sig="def xor_operation(n: int, start: int) -> int:",
        fn="xor_operation",
        tests=[
            ((5, 0), 8),
            ((4, 3), 8),
            ((1, 7), 7),
            ((10, 5), 2),
        ],
        hints=[
            "Just build the array and XOR it - O(n).",
            "XOR of 0..m has a repeating pattern of period 4 (m, 1, m + 1, 0).",
            (
                "Factor out the lowest bit: all terms share start's lowest bit, and the rest forms a consecutive "
                "range - O(1) with the period-4 formula."
            ),
        ],
        pattern="XOR prefix patterns (period 4)",
        explain=(
            "Write each term as 2*(start//2 + i) + (start & 1). XOR of a consecutive range comes from the prefix "
            "formula, and the shared low bit survives only when n is odd."
        ),
        cx="O(1)",
        brute_cx="O(n) time - XOR the terms one by one",
        brute=r"""
# BRUTE FORCE: O(n) time - XOR the terms one by one
def xor_operation(n, start):
    result = 0
    for i in range(n):
        result ^= start + 2 * i
    return result
""",
        solution=r"""
# OPTIMISED: O(1)
# Idea: XOR prefix patterns (period 4)
def xor_operation(n, start):
    def xor_to(m):  # XOR of 0..m
        return [m, 1, m + 1, 0][m % 4]

    base, low = start >> 1, start & 1
    high = xor_to(base + n - 1) ^ xor_to(base - 1) if base > 0 else xor_to(base + n - 1)
    return (high << 1) | (low & n)  # low bit survives only when n is odd
""",
    ),
]
