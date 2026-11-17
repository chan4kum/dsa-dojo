"""Bits Math problems - the problem bank for the "bits_math" topic.

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
    # ---- Single Number (LeetCode 136) ----
    dict(
        title="Single Number",
        diff="E",
        lc=136,
        slug="single-number",
        prompt=(
            "Every number in the array appears twice except one. Find the one that appears once, in O(n) time and "
            "O(1) extra space."
        ),
        sig="def single_number(nums: List[int]) -> int:",
        fn="single_number",
        tests=[
            (([2, 2, 1],), 1),
            (([4, 1, 2, 1, 2],), 4),
            (([1],), 1),
            (([-1, -1, -2],), -2),
        ],
        hints=[
            "A hash set uses O(n) space. Is there an operation where equal things cancel?",
            "x XOR x = 0 and x XOR 0 = x; XOR is commutative and associative.",
            "XOR everything together: pairs vanish, the single number remains.",
        ],
        pattern="Bit manipulation: XOR cancellation",
        explain=(
            "Because XOR is order-independent, the result is XOR of all values, and every duplicated pair "
            "cancels\n        to 0. O(n) time, O(1) space."
        ),
        cx="O(n) time, O(1) space (XOR)",
        brute_cx="O(n) time, O(n) space - count with a hash map",
        brute=r"""
# BRUTE FORCE: O(n) time, O(n) space - count with a hash map
def single_number(nums):
    return [x for x, c in Counter(nums).items() if c == 1][0]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space (XOR)
# Idea: Bit manipulation: XOR cancellation
def single_number(nums):
    res = 0
    for x in nums:
        res ^= x
    return res
""",
    ),
    # ---- Counting Bits (LeetCode 338) ----
    dict(
        title="Counting Bits",
        diff="E",
        lc=338,
        slug="counting-bits",
        prompt="For every i from 0 to n, return the number of 1 bits in its binary form, as an array.",
        sig="def count_bits(n: int) -> List[int]:",
        fn="count_bits",
        tests=[
            ((2,), [0, 1, 1]),
            ((5,), [0, 1, 1, 2, 1, 2]),
            ((0,), [0]),
            ((8,), [0, 1, 1, 2, 1, 2, 2, 3, 1]),
        ],
        hints=[
            "Counting bits of each number separately is O(n log n). Can you reuse earlier answers?",
            "i >> 1 is i with the last bit removed - a smaller number whose answer you already have.",
            "bits[i] = bits[i >> 1] + (i & 1).",
        ],
        pattern="DP on bits (relate i to i >> 1)",
        explain=(
            "Shifting right drops the lowest bit, so popcount(i) = popcount(i>>1) + (i & 1). That is a one-line "
            "DP\n        in O(n)."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n log n) - count each number's bits separately",
        brute=r"""
# BRUTE FORCE: O(n log n) - count each number's bits separately
def count_bits(n):
    return [bin(i).count("1") for i in range(n + 1)]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: DP on bits (relate i to i >> 1)
def count_bits(n):
    bits = [0] * (n + 1)
    for i in range(1, n + 1):
        bits[i] = bits[i >> 1] + (i & 1)
    return bits
""",
    ),
    # ---- Sum of Two Integers (LeetCode 371) ----
    dict(
        title="Sum of Two Integers",
        diff="M",
        lc=371,
        slug="sum-of-two-integers",
        prompt="Add two integers without using + or -. (Treat them as 32-bit signed integers.)",
        sig="def get_sum(a: int, b: int) -> int:",
        fn="get_sum",
        tests=[
            ((1, 2), 3),
            ((2, 3), 5),
            ((-1, 1), 0),
            ((-5, -7), -12),
            ((0, 0), 0),
            ((1000, -999), 1),
        ],
        hints=[
            "Binary addition by hand: XOR gives the sum ignoring carries.",
            "AND shifted left by one gives the carries. Add the two parts - which is the same problem again.",
            "Repeat until the carry is 0. In Python mask to 32 bits and convert back to negative if bit 31 is set.",
        ],
        pattern="Bit manipulation: XOR = sum without carry, (AND << 1) = carry",
        explain=(
            "Loop: a, b = (a ^ b), (a & b) << 1 until b == 0. Python ints are unbounded, so simulate "
            "32-bit\n        two's complement with a mask and fix the sign at the end."
        ),
        cx="O(1) (32 iterations) using XOR and carry",
        brute_cx="O(|b|) - increments/decrements a one at a time (still needs + 1, shows why bit tricks matter)",
        brute=r"""
# BRUTE FORCE: O(|b|) - increments/decrements a one at a time (still needs + 1, shows why bit tricks matter)
def get_sum(a, b):
    # brute force: walk the number line one step at a time (works for any signs)
    r = a
    step = 1 if b > 0 else -1
    for _ in range(abs(b)):
        r += step
    return r
""",
        solution=r"""
# OPTIMISED: O(1) (32 iterations) using XOR and carry
# Idea: Bit manipulation: XOR = sum without carry, (AND << 1) = carry
def get_sum(a, b):
    MASK = 0xFFFFFFFF
    while b:
        a, b = (a ^ b) & MASK, ((a & b) << 1) & MASK
    return a if a <= 0x7FFFFFFF else ~(a ^ MASK)
""",
    ),
    # ---- Pow(x, n) (LeetCode 50) ----
    dict(
        title="Pow(x, n)",
        diff="M",
        lc=50,
        slug="powx-n",
        prompt="Compute x raised to the integer power n (n may be negative) faster than n multiplications.",
        sig="def my_pow(x: float, n: int) -> float:",
        fn="my_pow",
        compare="float",
        tests=[
            ((2.0, 10), 1024.0),
            ((2.0, -2), 0.25),
            ((3.0, 0), 1.0),
            ((2.0, 31), 2147483648.0),
            ((0.5, 3), 0.125),
        ],
        hints=[
            "x^n = (x^(n/2))^2 when n is even. How many levels is that?",
            (
                "Iteratively: look at the bits of n. For each set bit multiply the result by the current power of "
                "x; square x every step."
            ),
            "For negative n compute x^|n| and take the reciprocal (or invert x first).",
        ],
        pattern="Exponentiation by squaring (binary decomposition of the exponent)",
        explain=(
            "n = sum of powers of two, so x^n is a product of x^(2^k) for the set bits. Squaring x each step "
            "builds\n        x^(2^k). O(log n) multiplications. The same trick underlies modular exponentiation and "
            "matrix power\n        (fast Fibonacci)."
        ),
        cx="O(log n) time (binary exponentiation)",
        brute_cx="O(n) multiplications - too slow for n ~ 2^31",
        brute=r"""
# BRUTE FORCE: O(n) multiplications - too slow for n ~ 2^31
def my_pow(x, n):
    r = 1.0
    for _ in range(abs(n)):
        r *= x
    return r if n >= 0 else 1 / r
""",
        solution=r"""
# OPTIMISED: O(log n) time (binary exponentiation)
# Idea: Exponentiation by squaring (binary decomposition of the exponent)
def my_pow(x, n):
    if n < 0:
        x, n = 1 / x, -n

    result = 1.0

    while n:
        if n & 1:
            result *= x
        x *= x
        n >>= 1

    return result
""",
    ),
]
