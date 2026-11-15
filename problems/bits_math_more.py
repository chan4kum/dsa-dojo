from core import *

PROBLEMS = [
    dict(
        title="Number of 1 Bits", diff="E", lc=191, slug="number-of-1-bits",
        prompt="Return the number of set bits (1s) in the binary representation of a non-negative integer.",
        sig="def hamming_weight(n: int) -> int:", fn="hamming_weight",
        tests=[((11,), 3), ((128,), 1), ((2147483645,), 30), ((0,), 0), ((255,), 8)],
        hints=["You can test the lowest bit with n & 1 and shift right. How many iterations?",
               "As many as the number's length. Can you iterate only over the 1s?",
               "n & (n - 1) clears the lowest set bit. Count how many times until n is 0 (Brian Kernighan)."],
        pattern="Bit trick: n & (n-1) removes the lowest set bit",
        explain="""
        Subtracting 1 flips the lowest 1 and every 0 below it, so AND-ing with n wipes exactly that bit. The loop runs
        once per set bit. The same trick tests powers of two (n & (n-1) == 0).""",
        cx="O(number of set bits)", brute_cx="O(bit length) - shift and test every bit",
        brute=r'''
def hamming_weight(n):
    c = 0
    while n:
        c += n & 1
        n >>= 1
    return c
''',
        solution=r'''
def hamming_weight(n):
    c = 0
    while n:
        n &= n - 1
        c += 1
    return c
''',
    ),
    dict(
        title="Reverse Bits", diff="E", lc=190, slug="reverse-bits",
        prompt="Reverse the bits of a 32-bit unsigned integer and return the result as an unsigned integer.",
        sig="def reverse_bits(n: int) -> int:", fn="reverse_bits",
        tests=[((43261596,), 964176192), ((4294967293,), 3221225471), ((0,), 0), ((1,), 2147483648)],
        hints=["Build the answer one bit at a time.",
               "Take the lowest bit of n, push it into the result from the other end.",
               "result = (result << 1) | (n & 1); n >>= 1 - repeat exactly 32 times."],
        pattern="Bit-by-bit construction with shifts",
        explain="""
        The loop pops from the right of n and pushes onto the right of result, which reverses the order. Always loop
        exactly 32 times, even when n becomes 0, so leading zeros are accounted for.""",
        cx="O(32) = O(1)", brute_cx="O(32) - via a binary string",
        brute=r'''
def reverse_bits(n):
    return int(format(n, "032b")[::-1], 2)
''',
        solution=r'''
def reverse_bits(n):
    res = 0
    for _ in range(32):
        res = (res << 1) | (n & 1)
        n >>= 1
    return res
''',
    ),
    dict(
        title="Power of Two", diff="E", lc=231, slug="power-of-two",
        prompt="Return True if n is a power of two (1, 2, 4, 8, ...).",
        sig="def is_power_of_two(n: int) -> bool:", fn="is_power_of_two",
        tests=[((1,), True), ((16,), True), ((3,), False), ((0,), False), ((-16,), False), ((1024,), True), ((218,), False)],
        hints=["A power of two has exactly one set bit in binary.",
               "What does n & (n-1) do to a number with one set bit?",
               "n > 0 and n & (n - 1) == 0."],
        pattern="Bit trick: single set bit test",
        explain="""
        Same primitive as Number of 1 Bits: removing the lowest set bit leaves 0 only if there was just one.""",
        cx="O(1)", brute_cx="O(log n) - divide by 2 while even",
        brute=r'''
def is_power_of_two(n):
    if n <= 0:
        return False
    while n % 2 == 0:
        n //= 2
    return n == 1
''',
        solution=r'''
def is_power_of_two(n):
    return n > 0 and n & (n - 1) == 0
''',
    ),
    dict(
        title="Reverse Integer", diff="M", lc=7, slug="reverse-integer",
        prompt="Reverse the decimal digits of a signed 32-bit integer. If the result leaves the range [-2^31, 2^31 - 1], return 0.",
        sig="def reverse(x: int) -> int:", fn="reverse",
        tests=[((123,), 321), ((-123,), -321), ((120,), 21), ((0,), 0), ((1534236469,), 0), ((-2147483648,), 0)],
        hints=["Peel off the last digit with % 10 and push it onto the result with * 10 + digit.",
               "Handle the sign separately (Python's % and // floor for negatives).",
               "After building, compare with the 32-bit limits and return 0 if out of range."],
        pattern="Digit extraction with divmod",
        explain="""
        Python has unbounded ints, so overflow is checked after the fact. In C/Java you must check BEFORE multiplying
        (res > INT_MAX/10) - mention this in an interview.""",
        cx="O(log x)", brute_cx="O(log x) - via string reversal",
        brute=r'''
def reverse(x):
    r = int(str(abs(x))[::-1]) * (1 if x >= 0 else -1)
    return r if -2 ** 31 <= r <= 2 ** 31 - 1 else 0
''',
        solution=r'''
def reverse(x):
    sign = -1 if x < 0 else 1
    x, res = abs(x), 0
    while x:
        x, d = divmod(x, 10)
        res = res * 10 + d
    res *= sign
    return res if -2 ** 31 <= res <= 2 ** 31 - 1 else 0
''',
    ),
    dict(
        title="Hamming Distance", diff="E", lc=461, slug="hamming-distance",
        prompt="Return the number of bit positions where the binary forms of x and y differ.",
        sig="def hamming_distance(x: int, y: int) -> int:", fn="hamming_distance",
        tests=[((1, 4), 2), ((3, 1), 1), ((0, 0), 0), ((7, 0), 3), ((93, 73), 2)],
        hints=["Which operation is 1 exactly where two bits differ?",
               "XOR.",
               "Count the set bits of x ^ y (Kernighan's loop)."],
        pattern="XOR = difference mask, then popcount",
        explain="""
        Two small tools combined: XOR finds differences, n & (n-1) counts them.""",
        cx="O(set bits)", brute_cx="O(bits) - compare bit by bit",
        brute=r'''
def hamming_distance(x, y):
    d = 0
    for i in range(32):
        if (x >> i & 1) != (y >> i & 1):
            d += 1
    return d
''',
        solution=r'''
def hamming_distance(x, y):
    z, d = x ^ y, 0
    while z:
        z &= z - 1
        d += 1
    return d
''',
    ),
    dict(
        title="Plus One", diff="E", lc=66, slug="plus-one",
        prompt="A non-negative integer is stored as a list of its decimal digits (most significant first). Add one and return the digits.",
        sig="def plus_one(digits: List[int]) -> List[int]:", fn="plus_one",
        tests=[(([1, 2, 3],), [1, 2, 4]), (([4, 3, 2, 1],), [4, 3, 2, 2]), (([9],), [1, 0]), (([9, 9],), [1, 0, 0]), (([1, 9],), [2, 0]), (([0],), [1])],
        hints=["Think of adding on paper: start from the last digit.",
               "A 9 becomes 0 and carries; anything else just increments and you are done.",
               "Scan from the right; if all digits were 9, the result is [1] + zeros."],
        pattern="Carry propagation from the least significant end",
        explain="""
        The loop ends early at the first non-9 digit, so most inputs take O(1); the all-9s case allocates one more digit.""",
        cx="O(n) time", brute_cx="O(n) - convert to int, add, convert back (cheating but a good oracle)",
        brute='''
def plus_one(digits):
    return [int(c) for c in str(int("".join(map(str, digits))) + 1)]
''',
        solution='''
def plus_one(digits):
    for i in range(len(digits) - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0
    return [1] + digits
''',
    ),
    dict(
        title="Count Primes", diff="M", lc=204, slug="count-primes",
        prompt="Return the number of primes strictly less than n.",
        sig="def count_primes(n: int) -> int:", fn="count_primes",
        tests=[((10,), 4), ((0,), 0), ((1,), 0), ((2,), 0), ((3,), 1), ((100,), 25), ((20000,), 2262)],
        hints=["Testing each number by trial division is O(n sqrt n).",
               "Instead of asking 'is k prime?' for every k, cross out the multiples of each prime.",
               "Sieve of Eratosthenes: start crossing out at p*p (smaller multiples were already removed by smaller primes). O(n log log n)."],
        pattern="Sieve: eliminate multiples instead of testing each number",
        explain="""
        Work is shared: composite numbers are crossed out once per prime factor, not tested independently. The
        classic example of 'reverse the direction of the loop'.""",
        cx="O(n log log n) time, O(n) space", brute_cx="O(n sqrt n) time - trial division",
        brute='''
def count_primes(n):
    def is_prime(k):
        if k < 2:
            return False
        i = 2
        while i * i <= k:
            if k % i == 0:
                return False
            i += 1
        return True
    return sum(1 for k in range(n) if is_prime(k))
''',
        solution='''
def count_primes(n):
    if n < 3:
        return 0
    sieve = bytearray([1]) * n
    sieve[0] = sieve[1] = 0
    for p in range(2, int(n ** 0.5) + 1):
        if sieve[p]:
            sieve[p * p::p] = bytearray(len(range(p * p, n, p)))
    return sum(sieve)
''',
    ),
    dict(
        title="Happy Number", diff="E", lc=202, slug="happy-number",
        prompt="Repeatedly replace n by the sum of the squares of its digits. Return True if this reaches 1, False if it loops forever.",
        sig="def is_happy(n: int) -> bool:", fn="is_happy",
        tests=[((19,), True), ((2,), False), ((1,), True), ((7,), True), ((4,), False), ((116,), False)],
        hints=["The process either hits 1 or repeats a value. What do you do to detect repeats?",
               "A set of seen values, or...",
               "treat next(n) as a 'next pointer': Floyd's fast/slow cycle detection works with O(1) space."],
        pattern="Cycle detection on an implicit sequence (set or Floyd)",
        explain="""
        Any 'apply f repeatedly' process is a linked list in disguise: the sequence either terminates or enters a
        cycle. That is the same reasoning as Linked List Cycle and Find the Duplicate Number.""",
        cx="O(log n) per step, O(1) space (Floyd)", brute_cx="O(log n) per step, O(k) space - set of seen values",
        brute='''
def is_happy(n):
    seen = set()
    while n != 1 and n not in seen:
        seen.add(n)
        n = sum(int(d) ** 2 for d in str(n))
    return n == 1
''',
        solution='''
def is_happy(n):
    def step(x):
        total = 0
        while x:
            x, d = divmod(x, 10)
            total += d * d
        return total
    slow, fast = n, step(n)
    while fast != 1 and slow != fast:
        slow, fast = step(slow), step(step(fast))
    return fast == 1
''',
    ),
]
