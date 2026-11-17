"""more Bits and Math problems (batch 5) - part of the problem bank for the "bits_math" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""


def _nozero_ok(args, got):
    """True if got is two positive integers without any digit 0 whose sum is n."""
    (n,) = args
    return (
        isinstance(got, list)
        and len(got) == 2
        and all(isinstance(x, int) and x > 0 and "0" not in str(x) for x in got)
        and sum(got) == n
    )


PROBLEMS = [
    # ---- UTF-8 Validation (LeetCode 393) ----
    dict(
        title="UTF-8 Validation",
        diff="M",
        lc=393,
        slug="utf-8-validation",
        prompt=(
            "data is a list of integers, each holding one byte (only the lowest 8 bits matter). A UTF-8 character "
            "uses 1 to 4 bytes: a 1-byte character starts with bit 0; an n-byte character (n = 2, 3, 4) starts with "
            "a first byte of n ones then a zero (110xxxxx, 1110xxxx, 11110xxx), followed by n - 1 bytes that start "
            "with the bits 10. Return true if data is a valid UTF-8 encoding."
        ),
        sig="def valid_utf8(data: List[int]) -> bool:",
        fn="valid_utf8",
        tests=[
            (([197, 130, 1],), True),
            (([235, 140, 4],), False),
            (([0],), True),
            (([145],), False),
        ],
        hints=[
            "Read the first byte of a character: its leading bits tell you how many bytes the character has.",
            (
                "Then the next n - 1 bytes must start with the bits 10. A byte that starts with 10 where a "
                "character should begin is invalid."
            ),
            (
                "Keep a counter of continuation bytes still expected. Check the top bits with shifts: x >> 7 == 0, "
                "x >> 5 == 0b110, x >> 4 == 0b1110, x >> 3 == 0b11110, x >> 6 == 0b10."
            ),
        ],
        pattern="Bit masks / shifts with a state counter",
        explain=(
            "The validity of a byte depends on whether we are at the start of a character or in the middle of one. "
            "Shifting right keeps only the top bits we care about, so each pattern check is one comparison. The "
            "counter of bytes still owed must be zero at the end. The brute force converts every byte to an "
            "8-character bit string and uses string prefixes instead of shifts."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time but with string building per byte",
        brute=r"""
# BRUTE FORCE: O(n) time but with string building per byte
def valid_utf8(data):
    bits = ["{:08b}".format(x & 255) for x in data]
    i = 0
    while i < len(bits):
        ones = len(bits[i]) - len(bits[i].lstrip("1"))
        if ones == 0:
            size = 1
        elif 2 <= ones <= 4:
            size = ones
        else:
            return False
        if i + size > len(bits):
            return False
        for k in range(1, size):
            if not bits[i + k].startswith("10"):
                return False
        i += size
    return True
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Bit masks / shifts with a state counter
def valid_utf8(data):
    owed = 0
    for x in data:
        x &= 255
        if owed == 0:
            if x >> 7 == 0:
                owed = 0
            elif x >> 5 == 0b110:
                owed = 1
            elif x >> 4 == 0b1110:
                owed = 2
            elif x >> 3 == 0b11110:
                owed = 3
            else:
                return False
        else:
            if x >> 6 != 0b10:
                return False
            owed -= 1
    return owed == 0
""",
    ),
    # ---- Poor Pigs (LeetCode 458) ----
    dict(
        title="Poor Pigs",
        diff="H",
        lc=458,
        slug="poor-pigs",
        prompt=(
            "There are `buckets` buckets of liquid and exactly ONE is poisonous. Pigs can be fed from any buckets "
            "simultaneously; a pig that drinks the poison dies after minutes_to_die minutes. You have "
            "minutes_to_test minutes in total and every test round takes minutes_to_die minutes (a pig that "
            "survives a round can be used again). Return the minimum number of pigs needed to find the poisonous "
            "bucket."
        ),
        sig="def poor_pigs(buckets: int, minutes_to_die: int, minutes_to_test: int) -> int:",
        fn="poor_pigs",
        tests=[
            ((4, 15, 15), 2),
            ((4, 15, 30), 2),
            ((1000, 15, 60), 5),
            ((1, 15, 15), 0),
        ],
        hints=[
            (
                "A pig gives information through WHEN it dies: in round 1, in round 2, ..., or never. With r rounds "
                "that is r + 1 possible outcomes per pig."
            ),
            "p pigs give (r + 1)^p different outcome combinations, and each combination can single out one bucket.",
            (
                "So you need the smallest p with (rounds + 1)^p >= buckets, where rounds = minutes_to_test // "
                "minutes_to_die."
            ),
        ],
        pattern="Information counting (base-(rounds+1) digits)",
        explain=(
            "Give each bucket a unique code with p digits in base (r + 1): digit j tells in which round pig j "
            "drinks from the bucket (or never). The pattern of deaths then identifies the bucket. More codes than "
            "buckets is enough, and fewer cannot distinguish them all. The brute force counts, with a recursion "
            "over pigs left and rounds left, how many buckets p pigs can separate: f(p, r) = sum over k pigs dying "
            "in the first round of C(p, k) * f(p - k, r - 1)."
        ),
        cx="O(log buckets) time, O(1) space",
        brute_cx="exponential - a recursion over pigs and rounds with no memory",
        brute=r"""
# BRUTE FORCE: exponential - a recursion over pigs and rounds with no memory
def poor_pigs(buckets, minutes_to_die, minutes_to_test):
    rounds = minutes_to_test // minutes_to_die

    def can_separate(pigs, left):
        if left == 0:
            return 1
        return sum(math.comb(pigs, k) * can_separate(pigs - k, left - 1) for k in range(pigs + 1))

    pigs = 0
    while can_separate(pigs, rounds) < buckets:
        pigs += 1
    return pigs
""",
        solution=r"""
# OPTIMISED: O(log buckets) time, O(1) space
# Idea: Information counting (base-(rounds+1) digits)
def poor_pigs(buckets, minutes_to_die, minutes_to_test):
    states = minutes_to_test // minutes_to_die + 1
    pigs = 0
    while states**pigs < buckets:
        pigs += 1
    return pigs
""",
    ),
    # ---- Total Hamming Distance (LeetCode 477) ----
    dict(
        title="Total Hamming Distance",
        diff="M",
        lc=477,
        slug="total-hamming-distance",
        prompt=(
            "The Hamming distance of two integers is the number of bit positions where they differ. Given an "
            "integer array nums, return the SUM of the Hamming distances between all pairs of numbers (each pair "
            "counted once)."
        ),
        sig="def total_hamming_distance(nums: List[int]) -> int:",
        fn="total_hamming_distance",
        tests=[
            (([4, 14, 2],), 6),
            (([4, 14, 4],), 4),
            (([1],), 0),
            (([0, 0],), 0),
        ],
        hints=[
            "Brute force: for every pair, XOR the numbers and count the 1 bits - O(n^2) pairs.",
            "Look at ONE bit position at a time. Two numbers differ there only when one has 1 and the other has 0.",
            "If c numbers have a 1 at that bit, then c * (n - c) pairs differ. Add this over all bit positions.",
        ],
        pattern="Count per bit instead of per pair",
        explain=(
            "The total distance is the sum over bit positions of the number of pairs that differ in that position. "
            "Pairs that differ at a bit are exactly (numbers with 1) x (numbers with 0), so we only need one count "
            "per bit. That replaces n^2 pair work by 32 passes over the array."
        ),
        cx="O(32 * n) time, O(1) space",
        brute_cx="O(n^2) time - XOR and popcount for every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - XOR and popcount for every pair
def total_hamming_distance(nums):
    total = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            total += bin(nums[i] ^ nums[j]).count("1")
    return total
""",
        solution=r"""
# OPTIMISED: O(32 * n) time, O(1) space
# Idea: Count per bit instead of per pair
def total_hamming_distance(nums):
    n = len(nums)
    total = 0
    for bit in range(32):
        ones = sum((x >> bit) & 1 for x in nums)
        total += ones * (n - ones)
    return total
""",
    ),
    # ---- Perfect Number (LeetCode 507) ----
    dict(
        title="Perfect Number",
        diff="E",
        lc=507,
        slug="perfect-number",
        prompt=(
            "A perfect number equals the sum of its POSITIVE divisors other than itself (6 = 1 + 2 + 3). Given an "
            "integer num, return true if it is a perfect number."
        ),
        sig="def check_perfect_number(num: int) -> bool:",
        fn="check_perfect_number",
        tests=[
            ((28,), True),
            ((7,), False),
            ((6,), True),
            ((1,), False),
        ],
        hints=[
            "Brute force: add up every i in 1 .. num - 1 that divides num.",
            "Divisors come in pairs (d, num / d). You only need to look for d up to the square root of num.",
            (
                "For each d <= sqrt(num) that divides num, add d and num // d (once if they are equal). Start with "
                "1 and never count num itself; for num = 1 the answer is false."
            ),
        ],
        pattern="Divisor pairs up to the square root",
        explain=(
            "Every divisor below sqrt(num) has a partner above it, so scanning to the square root finds all "
            "divisors in O(sqrt n). We must not count num itself, and 1 is a special case because it has no proper "
            "divisors."
        ),
        cx="O(sqrt n) time, O(1) space",
        brute_cx="O(n) time - test every smaller number",
        brute=r"""
# BRUTE FORCE: O(n) time - test every smaller number
def check_perfect_number(num):
    return num > 1 and sum(d for d in range(1, num) if num % d == 0) == num
""",
        solution=r"""
# OPTIMISED: O(sqrt n) time, O(1) space
# Idea: Divisor pairs up to the square root
def check_perfect_number(num):
    if num <= 1:
        return False
    total = 1
    d = 2
    while d * d <= num:
        if num % d == 0:
            total += d
            if d != num // d:
                total += num // d
        d += 1
    return total == num
""",
    ),
    # ---- Maximum Swap (LeetCode 670) ----
    dict(
        title="Maximum Swap",
        diff="M",
        lc=670,
        slug="maximum-swap",
        prompt=(
            "You may swap two digits of the non-negative integer num at most once. Return the maximum value you can "
            "get."
        ),
        sig="def maximum_swap(num: int) -> int:",
        fn="maximum_swap",
        tests=[
            ((2736,), 7236),
            ((9973,), 9973),
            ((98368,), 98863),
            ((1993,), 9913),
        ],
        hints=[
            "To make the number larger you want a bigger digit as far LEFT as possible.",
            (
                "Scan from the left: at the first position where some LATER digit is bigger, swap in the biggest "
                "later digit."
            ),
            (
                "If that biggest digit appears several times, take its LAST occurrence (it pushes the small digit "
                "furthest right). Record the last index of every digit first."
            ),
        ],
        pattern="Greedy with last-occurrence table",
        explain=(
            "The leftmost digit that has a larger digit somewhere to its right is where the gain is largest. "
            "Swapping with the largest such digit is best, and using its last occurrence leaves the swapped-out "
            "small digit in the lowest position. The brute force tries all pairs of positions."
        ),
        cx="O(d) time where d = number of digits, O(1) space",
        brute_cx="O(d^3) time - try every swap",
        brute=r"""
# BRUTE FORCE: O(d^3) time - try every swap
def maximum_swap(num):
    digits = str(num)
    best = num
    for i in range(len(digits)):
        for j in range(i + 1, len(digits)):
            chars = list(digits)
            chars[i], chars[j] = chars[j], chars[i]
            best = max(best, int("".join(chars)))
    return best
""",
        solution=r"""
# OPTIMISED: O(d) time where d = number of digits, O(1) space
# Idea: Greedy with last-occurrence table
def maximum_swap(num):
    digits = list(str(num))
    last = {int(c): i for i, c in enumerate(digits)}
    for i, c in enumerate(digits):
        for d in range(9, int(c), -1):
            if last.get(d, -1) > i:
                j = last[d]
                digits[i], digits[j] = digits[j], digits[i]
                return int("".join(digits))
    return num
""",
    ),
    # ---- Reordered Power of 2 (LeetCode 869) ----
    dict(
        title="Reordered Power of 2",
        diff="M",
        lc=869,
        slug="reordered-power-of-2",
        prompt=(
            "Reorder the digits of the integer n in any order (the leading digit must not be zero). Return true if "
            "the result can be a power of two."
        ),
        sig="def reordered_power_of2(n: int) -> bool:",
        fn="reordered_power_of2",
        tests=[
            ((1,), True),
            ((10,), False),
            ((46,), True),
            ((24,), False),
        ],
        hints=[
            (
                "Brute force: try every permutation of the digits, skip those with a leading zero, and test for a "
                "power of two."
            ),
            "A power of two with the same digits has exactly the same MULTISET of digits as n.",
            (
                "There are only about 30 powers of two below 10^9. Compare the sorted digits of n with the sorted "
                "digits of each."
            ),
        ],
        pattern="Canonical form (sorted digits) comparison",
        explain=(
            "Two numbers are digit rearrangements of each other exactly when their sorted digit strings are equal, "
            "and that also guarantees the same length, so no leading zero issue arises for the power of two itself. "
            "Checking the few powers of two replaces a factorial number of permutations. The brute force tries all "
            "permutations."
        ),
        cx="O(30 * d log d) time, O(d) space",
        brute_cx="O(d! * d) time - every permutation of the digits",
        brute=r"""
# BRUTE FORCE: O(d! * d) time - every permutation of the digits
def reordered_power_of2(n):
    for perm in set(itertools.permutations(str(n))):
        if perm[0] == "0":
            continue
        v = int("".join(perm))
        if v & (v - 1) == 0:
            return True
    return False
""",
        solution=r"""
# OPTIMISED: O(30 * d log d) time, O(d) space
# Idea: Canonical form (sorted digits) comparison
def reordered_power_of2(n):
    target = sorted(str(n))
    return any(sorted(str(1 << k)) == target for k in range(31))
""",
    ),
    # ---- Complement of Base 10 Integer (LeetCode 1009) ----
    dict(
        title="Complement of Base 10 Integer",
        diff="E",
        lc=1009,
        slug="complement-of-base-10-integer",
        prompt=(
            "The complement of an integer flips every bit of its binary representation (without leading zeros): 1 "
            "becomes 0 and 0 becomes 1. Given a non-negative integer n, return its complement."
        ),
        sig="def bitwise_complement(n: int) -> int:",
        fn="bitwise_complement",
        tests=[
            ((5,), 2),
            ((7,), 0),
            ((10,), 5),
            ((0,), 1),
        ],
        hints=[
            "5 is 101. Flipping gives 010 = 2, but only the bits up to the highest set bit are flipped.",
            "Build a mask of ones with the same length as n: 1, 11, 111, ... until it is at least n.",
            (
                "XOR n with the mask. Special case: n = 0 is written '0', so its complement is 1 (a mask of a "
                "single 1 handles it)."
            ),
        ],
        pattern="XOR with an all-ones mask",
        explain=(
            "XOR with 1 flips a bit and XOR with 0 keeps it, so XOR with a mask of ones that covers exactly the "
            "bits of n flips all of them. The mask 2^k - 1 is built by shifting left and adding 1. The brute force "
            "flips the characters of the binary string."
        ),
        cx="O(log n) time, O(1) space",
        brute_cx="O(log n) time with string building",
        brute=r"""
# BRUTE FORCE: O(log n) time with string building
def bitwise_complement(n):
    flipped = "".join("1" if c == "0" else "0" for c in bin(n)[2:])
    return int(flipped, 2)
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(1) space
# Idea: XOR with an all-ones mask
def bitwise_complement(n):
    mask = 1
    while mask < n:
        mask = (mask << 1) | 1
    return mask ^ n
""",
    ),
    # ---- Convert to Base -2 (LeetCode 1017) ----
    dict(
        title="Convert to Base -2",
        diff="M",
        lc=1017,
        slug="convert-to-base-2",
        prompt=(
            "Given an integer n, return its representation in base -2 as a string of 0s and 1s with no leading "
            "zeros (except for the number 0 itself, written '0'). Digit i has weight (-2)^i."
        ),
        sig="def base_neg2(n: int) -> str:",
        fn="base_neg2",
        tests=[
            ((2,), "110"),
            ((3,), "111"),
            ((4,), "100"),
            ((0,), "0"),
        ],
        hints=[
            "Do it like ordinary base conversion: the last digit is n mod 2 (0 or 1).",
            "After removing the digit r, the rest is (n - r) divided by the BASE, i.e. by -2.",
            "Repeat until n becomes 0, collecting the digits, then reverse them. n = 0 is a special case.",
        ],
        pattern="Repeated division by a negative base",
        explain=(
            "n = r + (-2) * q with r in {0, 1}; the remainder r is the lowest digit and the same process applies to "
            "q. Because the base is negative the signs alternate, but dividing exactly (n - r) by -2 keeps "
            "everything an integer. The brute force tries every binary string of increasing length and evaluates "
            "it, which is correct because the representation is unique."
        ),
        cx="O(log n) time, O(log n) space",
        brute_cx="O(2^L * L) time for L digits - try all digit strings",
        brute=r"""
# BRUTE FORCE: O(2^L * L) time for L digits - try all digit strings
def base_neg2(n):
    if n == 0:
        return "0"
    for length in range(1, 12):
        for digits in itertools.product("01", repeat=length):
            if digits[0] == "0":
                continue
            value = sum(int(d) * (-2) ** (length - 1 - i) for i, d in enumerate(digits))
            if value == n:
                return "".join(digits)
""",
        solution=r"""
# OPTIMISED: O(log n) time, O(log n) space
# Idea: Repeated division by a negative base
def base_neg2(n):
    if n == 0:
        return "0"
    digits = []
    while n:
        r = n & 1
        digits.append(str(r))
        n = -((n - r) // 2)
    return "".join(reversed(digits))
""",
    ),
    # ---- Adding Two Negabinary Numbers (LeetCode 1073) ----
    dict(
        title="Adding Two Negabinary Numbers",
        diff="M",
        lc=1073,
        slug="adding-two-negabinary-numbers",
        prompt=(
            "A negabinary number is written in base -2; arrays list its digits from the MOST significant one, with "
            "no leading zeros (except [0] itself). Given two such arrays arr1 and arr2, return their sum in the "
            "same format."
        ),
        sig="def add_negabinary(arr1: List[int], arr2: List[int]) -> List[int]:",
        fn="add_negabinary",
        tests=[
            (([1, 1, 1, 1, 1], [1, 0, 1]), [1, 0, 0, 0, 0]),
            (([0], [0]), [0]),
            (([0], [1]), [1]),
            (([1, 1], [1, 1]), [1, 0]),
        ],
        hints=[
            "Add digit by digit from the right, like school addition, keeping a carry.",
            (
                "In base -2 a carry has the opposite sign: if the digit total is t, write t & 1 and carry -(t >> 1) "
                "(an arithmetic shift)."
            ),
            (
                "Keep going while either array has digits left or the carry is non-zero, then remove leading zeros "
                "(but keep one 0 if the result is zero) and reverse."
            ),
        ],
        pattern="Digit-wise addition with a sign-flipping carry",
        explain=(
            "Writing t = d + (-2) * c with d in {0, 1} gives the output digit d and the carry c to the next "
            "position; for a negative base the carry c = -(t >> 1). The total at each position ranges from -1 to 3, "
            "which this rule handles. The brute force converts both numbers to ordinary integers, adds them and "
            "converts the sum back to base -2."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - convert to integers, add, and convert back",
        brute=r"""
# BRUTE FORCE: O(n^2) time - convert to integers, add, and convert back
def add_negabinary(arr1, arr2):
    def to_int(digits):
        value = 0
        for d in digits:
            value = value * -2 + d
        return value

    total = to_int(arr1) + to_int(arr2)
    if total == 0:
        return [0]
    out = []
    while total:
        r = total & 1
        out.append(r)
        total = -((total - r) // 2)
    return out[::-1]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Digit-wise addition with a sign-flipping carry
def add_negabinary(arr1, arr2):
    i, j = len(arr1) - 1, len(arr2) - 1
    carry = 0
    out = []
    while i >= 0 or j >= 0 or carry:
        total = carry
        if i >= 0:
            total += arr1[i]
            i -= 1
        if j >= 0:
            total += arr2[j]
            j -= 1
        out.append(total & 1)
        carry = -(total >> 1)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out[::-1]
""",
    ),
    # ---- Distribute Candies to People (LeetCode 1103) ----
    dict(
        title="Distribute Candies to People",
        diff="E",
        lc=1103,
        slug="distribute-candies-to-people",
        prompt=(
            "You have `candies` candies and num_people people standing in a row. Give 1 candy to the first person, "
            "2 to the second, ..., n to the last; then continue from the first person with n + 1, n + 2, ... (one "
            "more each time). When fewer candies remain than the next gift, give all of them to the current person "
            "and stop. Return the array with how many candies each person ends up with."
        ),
        sig="def distribute_candies(candies: int, num_people: int) -> List[int]:",
        fn="distribute_candies",
        tests=[
            ((7, 4), [1, 2, 3, 1]),
            ((10, 3), [5, 2, 3]),
            ((1, 1), [1]),
            ((3, 5), [1, 2, 0, 0, 0]),
        ],
        hints=[
            (
                "Simulation works: hand out gift 1, 2, 3, ... to people 0, 1, 2, ... (wrapping around) until the "
                "candies run out."
            ),
            (
                "Faster: gifts 1..k cost k(k+1)/2 candies in total. Find the largest k with k(k+1)/2 <= candies (a "
                "quadratic, so use a square root)."
            ),
            (
                "Person i gets gifts i + 1, i + 1 + n, ... - an arithmetic series you can sum with a formula. The "
                "few candies left over (fewer than k + 1) go to the next person in line."
            ),
        ],
        pattern="Arithmetic series instead of simulation",
        explain=(
            "The gifts form 1, 2, 3, ...; the full ones are exactly the first k natural numbers, with k from the "
            "quadratic k(k+1)/2 <= candies. Person i receives every n-th gift starting at i + 1, which is an "
            "arithmetic progression with a known count. The remainder is a partial gift for person k mod n. The "
            "brute force simulates candy by gift."
        ),
        cx="O(n) time, O(n) space (independent of the candy count)",
        brute_cx="O(sqrt(candies)) time - hand out one gift at a time",
        brute=r"""
# BRUTE FORCE: O(sqrt(candies)) time - hand out one gift at a time
def distribute_candies(candies, num_people):
    result = [0] * num_people
    gift = 1
    i = 0
    while candies > 0:
        take = min(gift, candies)
        result[i % num_people] += take
        candies -= take
        gift += 1
        i += 1
    return result
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space (independent of the candy count)
# Idea: Arithmetic series instead of simulation
def distribute_candies(candies, num_people):
    k = (math.isqrt(8 * candies + 1) - 1) // 2
    rounds, extra = divmod(k, num_people)
    result = []
    for i in range(num_people):
        count = rounds + (1 if i < extra else 0)
        result.append(count * (i + 1) + num_people * count * (count - 1) // 2)
    result[extra] += candies - k * (k + 1) // 2
    return result
""",
    ),
    # ---- Day of the Year (LeetCode 1154) ----
    dict(
        title="Day of the Year",
        diff="E",
        lc=1154,
        slug="day-of-the-year",
        prompt=(
            "Given a date string in the format 'YYYY-MM-DD' (Gregorian calendar), return its day number within the "
            "year (1 January is day 1)."
        ),
        sig="def day_of_year(date: str) -> int:",
        fn="day_of_year",
        tests=[
            (("2019-01-09",), 9),
            (("2019-02-10",), 41),
            (("2003-03-01",), 60),
            (("2004-03-01",), 61),
        ],
        hints=[
            "Add up the lengths of the months before the given month, then add the day.",
            (
                "A year is a leap year if it is divisible by 4, except years divisible by 100 that are not "
                "divisible by 400."
            ),
            "Only February changes: add 1 extra day when the month is after February and the year is a leap year.",
        ],
        pattern="Calendar arithmetic with the leap-year rule",
        explain=(
            "The day number is the sum of the previous months' lengths plus the day of the month, with February "
            "counted as 29 days in a leap year. The brute force starts at 1 January and steps forward one day at a "
            "time until it reaches the date."
        ),
        cx="O(1) time, O(1) space",
        brute_cx="O(365) time - walk forward one day at a time",
        brute=r"""
# BRUTE FORCE: O(365) time - walk forward one day at a time
def day_of_year(date):
    year, month, day = (int(x) for x in date.split("-"))
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    lengths = [31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    m, d, count = 1, 1, 1
    while (m, d) != (month, day):
        d += 1
        if d > lengths[m - 1]:
            d = 1
            m += 1
        count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(1) time, O(1) space
# Idea: Calendar arithmetic with the leap-year rule
def day_of_year(date):
    year, month, day = (int(x) for x in date.split("-"))
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    lengths = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    return sum(lengths[: month - 1]) + day + (1 if leap and month > 2 else 0)
""",
    ),
    # ---- Day of the Week (LeetCode 1185) ----
    dict(
        title="Day of the Week",
        diff="E",
        lc=1185,
        slug="day-of-the-week",
        prompt=(
            "Given a date as three integers day, month and year (Gregorian calendar, 1971 to 2100), return the name "
            "of the weekday ('Sunday', 'Monday', ..., 'Saturday')."
        ),
        sig="def day_of_the_week(day: int, month: int, year: int) -> str:",
        fn="day_of_the_week",
        tests=[
            ((31, 8, 2019), "Saturday"),
            ((18, 7, 1999), "Sunday"),
            ((15, 8, 1993), "Sunday"),
            ((1, 1, 1971), "Friday"),
        ],
        hints=[
            "A known reference date gives the answer by counting days: 1 January 1971 was a Friday.",
            (
                "Brute force: walk forward day by day from the reference date, rotating the weekday. Fine for 130 "
                "years but wasteful."
            ),
            (
                "Closed formula (Zeller's congruence): treat January and February as months 13 and 14 of the "
                "previous year, then h = (q + 13(m+1)/5 + K + K/4 + J/4 + 5J) mod 7 with K = year mod 100, J = year "
                "/ 100. h = 0 is Saturday, 1 is Sunday, ..."
            ),
        ],
        pattern="Zeller's congruence (calendar formula)",
        explain=(
            "Zeller's formula packs the leap-year and month-length rules into integer arithmetic, so the weekday is "
            "found in O(1). Shifting January/February to months 13/14 of the previous year moves the leap day to "
            "the end of the counted year, which is why the formula needs no leap-year test. The brute force counts "
            "days from 1 January 1971 with an explicit calendar."
        ),
        cx="O(1) time, O(1) space",
        brute_cx="O(days since 1971) time - step through every day",
        brute=r"""
# BRUTE FORCE: O(days since 1971) time - step through every day
def day_of_the_week(day, month, year):
    names = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]

    def leap(y):
        return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

    weekday = 5
    y, m, d = 1971, 1, 1
    while (y, m, d) != (year, month, day):
        lengths = [31, 29 if leap(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        d += 1
        if d > lengths[m - 1]:
            d = 1
            m += 1
            if m > 12:
                m = 1
                y += 1
        weekday = (weekday + 1) % 7
    return names[weekday]
""",
        solution=r"""
# OPTIMISED: O(1) time, O(1) space
# Idea: Zeller's congruence (calendar formula)
def day_of_the_week(day, month, year):
    names = ["Saturday", "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    if month < 3:
        month += 12
        year -= 1
    k, j = year % 100, year // 100
    h = (day + 13 * (month + 1) // 5 + k + k // 4 + j // 4 + 5 * j) % 7
    return names[h]
""",
    ),
    # ---- Minimum Cost to Move Chips to The Same Position (LeetCode 1217) ----
    dict(
        title="Minimum Cost to Move Chips to The Same Position",
        diff="E",
        lc=1217,
        slug="minimum-cost-to-move-chips-to-the-same-position",
        prompt=(
            "position[i] is the position of chip i. In one move a chip can go from x to x + 2 or x - 2 at NO cost, "
            "or to x + 1 or x - 1 at cost 1. Return the minimum total cost to bring all chips to the same position."
        ),
        sig="def min_cost_to_move_chips(position: List[int]) -> int:",
        fn="min_cost_to_move_chips",
        tests=[
            (([1, 2, 3],), 1),
            (([2, 2, 2, 3, 3],), 2),
            (([1, 1000000000],), 1),
            (([5],), 0),
        ],
        hints=[
            (
                "Moving by 2 is free, so all chips on odd positions can be gathered at one odd spot for free, and "
                "all chips on even positions at one even spot."
            ),
            "Only the PARITY of a position matters.",
            (
                "Finally one group has to be moved onto the other: each chip costs 1. Move the smaller group, so "
                "the answer is min(number of odd, number of even)."
            ),
        ],
        pattern="Parity classes",
        explain=(
            "A chip changes parity only through a cost-1 move, so chips of the same parity can be merged for free. "
            "Two piles remain (odd and even); moving one pile onto the other costs 1 per chip, so we move the "
            "smaller pile. The brute force tries every existing position as the target and sums the cost of each "
            "chip, which is 0 for an even distance and 1 for an odd distance."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - try every chip position as the target",
        brute=r"""
# BRUTE FORCE: O(n^2) time - try every chip position as the target
def min_cost_to_move_chips(position):
    return min(sum(abs(p - target) % 2 for p in position) for target in position)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Parity classes
def min_cost_to_move_chips(position):
    odd = sum(p % 2 for p in position)
    return min(odd, len(position) - odd)
""",
    ),
    # ---- Sequential Digits (LeetCode 1291) ----
    dict(
        title="Sequential Digits",
        diff="M",
        lc=1291,
        slug="sequential-digits",
        prompt=(
            "A number has SEQUENTIAL DIGITS if each digit is exactly one more than the previous digit (e.g. 123, "
            "4567). Return a sorted list of all numbers in the range [low, high] (inclusive) that have sequential "
            "digits."
        ),
        sig="def sequential_digits(low: int, high: int) -> List[int]:",
        fn="sequential_digits",
        tests=[
            ((100, 300), [123, 234]),
            ((1000, 13000), [1234, 2345, 3456, 4567, 5678, 6789, 12345]),
            ((10, 10), []),
            ((10, 12), [12]),
        ],
        hints=[
            "Brute force: check every number from low to high - far too slow when high is 10^9.",
            (
                "A sequential number is a window of the string '123456789': its start digit and length determine "
                "it. There are only 36 of them."
            ),
            (
                "Take every substring of '123456789' (by increasing length, then start), convert it to an integer, "
                "keep it if it lies in [low, high]. They are produced already in sorted order."
            ),
        ],
        pattern="Generate candidates instead of testing the range",
        explain=(
            "Only 36 numbers have sequential digits, and they are all substrings of 123456789. Enumerating by "
            "length first and start digit second yields increasing values, so no sort is needed. The brute force "
            "tests every number in the range."
        ),
        cx="O(1) time (36 candidates), O(1) space",
        brute_cx="O(high - low) time",
        brute=r"""
# BRUTE FORCE: O(high - low) time
def sequential_digits(low, high):
    result = []
    for x in range(low, high + 1):
        s = str(x)
        if all(int(s[i + 1]) - int(s[i]) == 1 for i in range(len(s) - 1)):
            result.append(x)
    return result
""",
        solution=r"""
# OPTIMISED: O(1) time (36 candidates), O(1) space
# Idea: Generate candidates instead of testing the range
def sequential_digits(low, high):
    digits = "123456789"
    result = []
    for length in range(len(str(low)), len(str(high)) + 1):
        for start in range(0, 10 - length):
            value = int(digits[start : start + length])
            if low <= value <= high:
                result.append(value)
    return result
""",
    ),
    # ---- Convert Integer to the Sum of Two No-Zero Integers (LeetCode 1317) ----
    dict(
        title="Convert Integer to the Sum of Two No-Zero Integers",
        diff="E",
        lc=1317,
        slug="convert-integer-to-the-sum-of-two-no-zero-integers",
        prompt=(
            "A NO-ZERO integer is a positive integer with no digit 0 in its decimal representation. Given n (n >= "
            "2), return ANY two no-zero integers [a, b] with a + b = n (a solution always exists)."
        ),
        sig="def get_no_zero_integers(n: int) -> List[int]:",
        fn="get_no_zero_integers",
        check=_nozero_ok,
        tests=[
            ((2,), [1, 1]),
            ((11,), [2, 9]),
            ((10000,), [1, 9999]),
            ((4,), [1, 3]),
        ],
        hints=[
            "You are free to pick any valid pair, so look for one that is easy to find.",
            "Try a = 1, 2, 3, ... and set b = n - a.",
            (
                "Stop at the first a where neither a nor b contains the character '0'. In practice this happens "
                "after a handful of tries."
            ),
        ],
        pattern="Search with an easy early exit",
        explain=(
            "Zeros are not that common, so scanning a upwards finds a pair almost at once. A checker verifies the "
            "answer, because many pairs are valid. The brute force tries every pair (a, b) with both ranging over 1 "
            ".. n - 1."
        ),
        cx="O(k log n) time, k = number of tries (small), O(1) space",
        brute_cx="O(n^2) time - every pair (a, b)",
        brute=r"""
# BRUTE FORCE: O(n^2) time - every pair (a, b)
def get_no_zero_integers(n):
    for a in range(1, n):
        for b in range(1, n):
            if a + b == n and "0" not in str(a) and "0" not in str(b):
                return [a, b]
""",
        solution=r"""
# OPTIMISED: O(k log n) time, k = number of tries (small), O(1) space
# Idea: Search with an easy early exit
def get_no_zero_integers(n):
    for a in range(1, n):
        b = n - a
        if "0" not in str(a) and "0" not in str(b):
            return [a, b]
""",
    ),
    # ---- Angle Between Hands of a Clock (LeetCode 1344) ----
    dict(
        title="Angle Between Hands of a Clock",
        diff="M",
        lc=1344,
        slug="angle-between-hands-of-a-clock",
        prompt=(
            "Given hour (1-12) and minutes (0-59), return the smaller angle in degrees between the hour hand and "
            "the minute hand of an analogue clock (answers within 1e-5 are accepted)."
        ),
        sig="def angle_clock(hour: int, minutes: int) -> float:",
        fn="angle_clock",
        compare="float",
        tests=[
            ((12, 30), 165.0),
            ((3, 30), 75.0),
            ((3, 15), 7.5),
            ((4, 50), 155.0),
        ],
        hints=[
            "The minute hand moves 360 / 60 = 6 degrees per minute.",
            (
                "The hour hand moves 30 degrees per hour AND 0.5 degrees per minute (it creeps while the minutes "
                "pass). Use hour % 12 so 12 counts as 0."
            ),
            "Take the absolute difference d of the two angles. The smaller angle is min(d, 360 - d).",
        ],
        pattern="Angle arithmetic (rates of the two hands)",
        explain=(
            "Each hand has an exact position that is a linear function of the time, so the angle between them is "
            "the difference of two linear expressions. Because angles wrap around, the answer is the smaller of the "
            "two arcs. The brute force works in half-degree ticks (720 per circle), counts the clockwise gap with "
            "integers and takes the shorter way round."
        ),
        cx="O(1) time, O(1) space",
        brute_cx="O(1) time, integer ticks of half a degree",
        brute=r"""
# BRUTE FORCE: O(1) time, integer ticks of half a degree
def angle_clock(hour, minutes):
    total = (hour % 12) * 60 + minutes
    hour_tick = total
    minute_tick = minutes * 12
    gap = (minute_tick - hour_tick) % 720
    return min(gap, 720 - gap) / 2
""",
        solution=r"""
# OPTIMISED: O(1) time, O(1) space
# Idea: Angle arithmetic (rates of the two hands)
def angle_clock(hour, minutes):
    hour_angle = (hour % 12) * 30 + minutes * 0.5
    minute_angle = minutes * 6
    diff = abs(hour_angle - minute_angle)
    return min(diff, 360 - diff)
""",
    ),
    # ---- Sort Integers by The Number of 1 Bits (LeetCode 1356) ----
    dict(
        title="Sort Integers by The Number of 1 Bits",
        diff="E",
        lc=1356,
        slug="sort-integers-by-the-number-of-1-bits",
        prompt=(
            "Sort the integer array arr by the number of 1 bits in their binary representation, in ascending order. "
            "If several integers have the same number of 1 bits, sort them in ascending numeric order. Return the "
            "sorted array."
        ),
        sig="def sort_by_bits(arr: List[int]) -> List[int]:",
        fn="sort_by_bits",
        tests=[
            (([0, 1, 2, 3, 4, 5, 6, 7, 8],), [0, 1, 2, 4, 8, 3, 5, 6, 7]),
            (([1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1],), [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024]),
            (([3, 1, 2],), [1, 2, 3]),
            (([7],), [7]),
        ],
        hints=[
            "You need a sort whose key is a PAIR: (number of 1 bits, value).",
            (
                "Count the 1 bits of x with bin(x).count('1') or with the loop x &= x - 1 (each step clears the "
                "lowest set bit)."
            ),
            (
                "sorted(arr, key=lambda x: (bits(x), x)). Tuples compare element by element, which gives the "
                "tie-break for free."
            ),
        ],
        pattern="Sort with a composite key",
        explain=(
            "A tuple key compares the bit count first and the value second, which is exactly the required order. "
            "Counting bits with x &= x - 1 takes as many steps as there are set bits. The brute force is an "
            "insertion sort that compares the same pair by hand."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2) time - insertion sort with a bit-counting comparison",
        brute=r"""
# BRUTE FORCE: O(n^2) time - insertion sort with a bit-counting comparison
def sort_by_bits(arr):
    def ones(x):
        count = 0
        while x:
            count += x & 1
            x >>= 1
        return count

    result = list(arr)
    for i in range(1, len(result)):
        item = result[i]
        j = i - 1
        while j >= 0 and (ones(result[j]), result[j]) > (ones(item), item):
            result[j + 1] = result[j]
            j -= 1
        result[j + 1] = item
    return result
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Sort with a composite key
def sort_by_bits(arr):
    return sorted(arr, key=lambda x: (bin(x).count("1"), x))
""",
    ),
    # ---- Number of Days Between Two Dates (LeetCode 1360) ----
    dict(
        title="Number of Days Between Two Dates",
        diff="E",
        lc=1360,
        slug="number-of-days-between-two-dates",
        prompt=(
            "Given two dates as strings 'YYYY-MM-DD' (years 1971 to 2100), return the number of days between them "
            "(the order of the dates does not matter, the result is never negative)."
        ),
        sig="def days_between_dates(date1: str, date2: str) -> int:",
        fn="days_between_dates",
        tests=[
            (("2019-06-29", "2019-06-30"), 1),
            (("2020-01-15", "2019-12-31"), 15),
            (("2020-03-01", "2020-02-28"), 2),
            (("2000-01-01", "2000-01-01"), 0),
        ],
        hints=[
            (
                "Convert each date to a single day number (days since some fixed starting point); then the answer "
                "is the absolute difference."
            ),
            "Day number = days in all earlier years + days in earlier months of this year + day. Leap years add 1 day.",
            (
                "Trick: treat March as the first month (move January and February to months 13 and 14 of the "
                "previous year). Then days = 365y + y/4 - y/100 + y/400 + (153(m - 3) + 2)/5 + d, with integer "
                "divisions."
            ),
        ],
        pattern="Convert to an absolute day count",
        explain=(
            "Subtracting two absolute day numbers gives the distance regardless of month lengths. Starting the year "
            "in March puts the variable-length February at the end of the year, so month offsets become the simple "
            "expression (153(m-3)+2)/5 and leap days are counted by y/4 - y/100 + y/400. The brute force steps one "
            "day at a time from the earlier to the later date."
        ),
        cx="O(1) time, O(1) space",
        brute_cx="O(days between) time - step day by day",
        brute=r"""
# BRUTE FORCE: O(days between) time - step day by day
def days_between_dates(date1, date2):
    def leap(y):
        return y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)

    a = tuple(int(x) for x in date1.split("-"))
    b = tuple(int(x) for x in date2.split("-"))
    if a > b:
        a, b = b, a
    y, m, d = a
    steps = 0
    while (y, m, d) != b:
        lengths = [31, 29 if leap(y) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
        d += 1
        if d > lengths[m - 1]:
            d = 1
            m += 1
            if m > 12:
                m = 1
                y += 1
        steps += 1
    return steps
""",
        solution=r"""
# OPTIMISED: O(1) time, O(1) space
# Idea: Convert to an absolute day count
def days_between_dates(date1, date2):
    def day_number(date):
        y, m, d = (int(x) for x in date.split("-"))
        if m < 3:
            y -= 1
            m += 12
        return 365 * y + y // 4 - y // 100 + y // 400 + (153 * (m - 3) + 2) // 5 + d

    return abs(day_number(date1) - day_number(date2))
""",
    ),
    # ---- Concatenation of Consecutive Binary Numbers (LeetCode 1680) ----
    dict(
        title="Concatenation of Consecutive Binary Numbers",
        diff="M",
        lc=1680,
        slug="concatenation-of-consecutive-binary-numbers",
        prompt=(
            "Write the binary representations of 1, 2, 3, ..., n one after another to form one long binary string "
            "(for n = 3 that is '1' + '10' + '11' = '11011'). Return the decimal value of this string modulo 10^9 + "
            "7."
        ),
        sig="def concatenated_binary(n: int) -> int:",
        fn="concatenated_binary",
        tests=[
            ((1,), 1),
            ((3,), 27),
            ((4,), 220),
            ((12,), 505379714),
        ],
        hints=[
            "Building the string and converting it creates a number with about n log n bits - too large for big n.",
            "Appending x to a binary string is: result = (result << (number of bits of x)) + x.",
            (
                "Keep result modulo 10^9 + 7 at every step. The bit length of x is x.bit_length() (it only changes "
                "when x is a power of two)."
            ),
        ],
        pattern="Shift-and-add with modular arithmetic",
        explain=(
            "Concatenating b bits to the right of a number multiplies it by 2^b and adds the new number. Applying % "
            "mod after each step keeps the numbers small without changing the final residue. The brute force builds "
            "the whole string, converts it to an integer and takes the remainder at the end."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2 log n) time - a huge integer is built before the modulo",
        brute=r"""
# BRUTE FORCE: O(n^2 log n) time - a huge integer is built before the modulo
def concatenated_binary(n):
    text = "".join(bin(x)[2:] for x in range(1, n + 1))
    return int(text, 2) % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Shift-and-add with modular arithmetic
def concatenated_binary(n):
    mod = 10**9 + 7
    result = 0
    for x in range(1, n + 1):
        result = ((result << x.bit_length()) + x) % mod
    return result
""",
    ),
    # ---- Count Square Sum Triples (LeetCode 1925) ----
    dict(
        title="Count Square Sum Triples",
        diff="E",
        lc=1925,
        slug="count-square-sum-triples",
        prompt=(
            "A square triple (a, b, c) is a set of positive integers with a^2 + b^2 = c^2. Given n, return the "
            "number of ordered triples with 1 <= a, b, c <= n (so (3, 4, 5) and (4, 3, 5) both count)."
        ),
        sig="def count_triples(n: int) -> int:",
        fn="count_triples",
        tests=[
            ((5,), 2),
            ((10,), 4),
            ((1,), 0),
            ((13,), 6),
        ],
        hints=[
            "Brute force: three nested loops over a, b, c - O(n^3).",
            "Once a and b are fixed, c is determined: c^2 = a^2 + b^2.",
            "Loop over a and b, compute s = a^2 + b^2 and c = isqrt(s). Count the pair if c * c == s and c <= n.",
        ],
        pattern="Remove a loop by computing the dependent value",
        explain=(
            "The third number is forced by the first two, so a perfect-square test replaces a whole loop. "
            "math.isqrt gives an exact integer square root without floating-point error. The brute force checks "
            "every possible c as well."
        ),
        cx="O(n^2) time, O(1) space",
        brute_cx="O(n^3) time - three nested loops",
        brute=r"""
# BRUTE FORCE: O(n^3) time - three nested loops
def count_triples(n):
    count = 0
    for a in range(1, n + 1):
        for b in range(1, n + 1):
            for c in range(1, n + 1):
                if a * a + b * b == c * c:
                    count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(1) space
# Idea: Remove a loop by computing the dependent value
def count_triples(n):
    count = 0
    for a in range(1, n + 1):
        for b in range(1, n + 1):
            s = a * a + b * b
            c = math.isqrt(s)
            if c <= n and c * c == s:
                count += 1
    return count
""",
    ),
]
