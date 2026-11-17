# 16 - Bit manipulation & math tricks

> **One idea:** numbers are arrays of bits. A handful of identities (XOR cancels, `n & (n-1)` clears the lowest set bit, shifting = multiply/divide by 2) solve a surprising number of problems in O(1) space.

## 1. First principles
- `a ^ a = 0`, `a ^ 0 = a`, XOR is commutative and associative -> **pairs cancel**.
- `n & (n - 1)` removes the lowest set bit (count bits, test power of two: `n > 0 and n & (n-1) == 0`).
- `n & -n` isolates the lowest set bit. `1 << k` is the k-th bit. `x >> 1` = floor(x / 2).
- Bitmask = a set of up to ~20-30 items as one integer: `mask | (1 << i)` add, `mask & (1 << i)` test, `mask ^ (1 << i)` toggle.
- Add without `+`: `sum = a ^ b` (no carry), `carry = (a & b) << 1`; repeat.
- **Exponentiation by squaring:** `x^n` from the binary digits of n -> O(log n). Same idea for modular power and matrix power.
- Number theory staples: `gcd(a, b)` by Euclid (`a, b = b, a % b`), sieve of Eratosthenes O(n log log n), `% MOD` after every multiplication.

## 2. How to spot it
- "without extra space", "every element appears twice except one", "single number".
- "power of two", "number of 1 bits", "subsets of a small set (n <= 20)".
- "XOR of ...", "maximum XOR" (binary trie).
- Huge exponents / modulo 10^9+7.

## 3. Paper recipe
1. Write the numbers in binary in columns. Many tricks become obvious in the picture.
2. For XOR problems write the running XOR column by column.
3. For masks: list what each bit means, then write the operation as bit-ops.
4. Python ints are unbounded: for 32-bit behaviour mask with `& 0xFFFFFFFF` and fix the sign.

## 4. Hand trace
**XOR cancels pairs** (`[4,1,2,1,2]`):

| next v | binary | running XOR (binary) | value |
|---|---|---|---|
| 4 | 100 | 100 | 4 |
| 1 | 001 | 101 | 5 |
| 2 | 010 | 111 | 7 |
| 1 | 001 | 110 | 6 |
| 2 | 010 | 100 | 4 |

**Counting bits** (`bits[i] = bits[i>>1] + (i & 1)`):

| i | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| binary | 0000 | 0001 | 0010 | 0011 | 0100 | 0101 | 0110 | 0111 | 1000 |
| bits[i>>1] + (i&1) | 0 | 1 | 1 | 2 | 1 | 2 | 2 | 3 | 1 |

## 5. Template
*Reference solution for **Pow(x, n)** (`bits_math/4`) - tested by `python dsa.py selftest`:*

```python
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
```

## 6. Traps
- Operator precedence differs by language: in **C/Java** `a & b == c` parses as `a & (b == c)`; in **Python** bitwise operators bind tighter than `==`, so it is `(a & b) == c`. Either way, parenthesise bit-ops - it removes the doubt.
- Negative numbers and `>>` (arithmetic shift) - Python never overflows, so mimic 32-bit explicitly.
- `1 << i` for i >= 31 in other languages needs a long.
- Floating-point `x ** n` for huge n; use the squaring loop with modulo.

## 7. Self-check
1. Why does `n & (n-1)` clear exactly one bit? Show it on 12 (`1100`).
2. Find two numbers that appear once while all others appear twice (hint: XOR splits them by a differing bit).
3. How many subsets does a 20-element mask enumerate, and what is the cost?

## 8. Practice ladder
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `bits_math/1` | Easy | Single Number | [#136](https://leetcode.com/problems/single-number/) | Bit manipulation: XOR cancellation |
| `bits_math/2` | Easy | Counting Bits | [#338](https://leetcode.com/problems/counting-bits/) | DP on bits (relate i to i >> 1) |
| `bits_math/5` | Easy | Number of 1 Bits | [#191](https://leetcode.com/problems/number-of-1-bits/) | Bit trick: n & (n-1) removes the lowest set bit |
| `bits_math/6` | Easy | Reverse Bits | [#190](https://leetcode.com/problems/reverse-bits/) | Bit-by-bit construction with shifts |
| `bits_math/7` | Easy | Power of Two | [#231](https://leetcode.com/problems/power-of-two/) | Bit trick: single set bit test |
| `bits_math/9` | Easy | Hamming Distance | [#461](https://leetcode.com/problems/hamming-distance/) | XOR = difference mask, then popcount |
| `bits_math/10` | Easy | Plus One | [#66](https://leetcode.com/problems/plus-one/) | Carry propagation from the least significant end |
| `bits_math/12` | Easy | Happy Number | [#202](https://leetcode.com/problems/happy-number/) | Cycle detection on an implicit sequence (set or Floyd) |
| `bits_math/17` | Easy | Palindrome Number | [#9](https://leetcode.com/problems/palindrome-number/) | Reverse only half the digits (no overflow, no string) |
| `bits_math/18` | Easy | Excel Sheet Column Title | [#168](https://leetcode.com/problems/excel-sheet-column-title/) | Bijective base-26 (subtract 1 each step) |
| `bits_math/19` | Easy | Excel Sheet Column Number | [#171](https://leetcode.com/problems/excel-sheet-column-number/) | Positional number system (Horner's rule in base 26) |
| `bits_math/20` | Easy | Power of Three | [#326](https://leetcode.com/problems/power-of-three/) | Divisibility of the largest power (3 is prime) |
| `bits_math/21` | Easy | Ugly Number | [#263](https://leetcode.com/problems/ugly-number/) | Strip the allowed prime factors, check what is left |
| `bits_math/23` | Easy | Power of Four | [#342](https://leetcode.com/problems/power-of-four/) | Bit tricks: single set bit + position mask |
| `bits_math/24` | Easy | Convert a Number to Hexadecimal | [#405](https://leetcode.com/problems/convert-a-number-to-hexadecimal/) | Bit masking and shifting, 4 bits per hex digit |
| `bits_math/25` | Easy | Number Complement | [#476](https://leetcode.com/problems/number-complement/) | XOR with an all-ones mask |
| `bits_math/26` | Easy | Binary Number with Alternating Bits | [#693](https://leetcode.com/problems/binary-number-with-alternating-bits/) | Shift-and-XOR to compare neighbouring bits |
| `bits_math/27` | Easy | Prime Number of Set Bits in Binary Representation | [#762](https://leetcode.com/problems/prime-number-of-set-bits-in-binary-representation/) | Popcount + tiny precomputed prime set |
| `bits_math/28` | Easy | Binary Gap | [#868](https://leetcode.com/problems/binary-gap/) | Single bit scan remembering the previous set bit |
| `bits_math/29` | Easy | Number of Steps to Reduce a Number to Zero | [#1342](https://leetcode.com/problems/number-of-steps-to-reduce-a-number-to-zero/) | Count bit operations instead of simulating |
| `bits_math/30` | Easy | Add to Array-Form of Integer | [#989](https://leetcode.com/problems/add-to-array-form-of-integer/) | Schoolbook addition with k doubling as the carry |
| `bits_math/31` | Easy | Base 7 | [#504](https://leetcode.com/problems/base-7/) | Repeated division to change base |
| `bits_math/32` | Easy | Add Digits | [#258](https://leetcode.com/problems/add-digits/) | Digital root via modulo 9 |
| `bits_math/33` | Easy | Minimum Bit Flips to Convert Number | [#2220](https://leetcode.com/problems/minimum-bit-flips-to-convert-number/) | XOR + popcount (Hamming distance) |
| `bits_math/35` | Easy | XOR Operation in an Array | [#1486](https://leetcode.com/problems/xor-operation-in-an-array/) | XOR prefix patterns (period 4) |
| `bits_math/39` | Easy | Perfect Number | [#507](https://leetcode.com/problems/perfect-number/) | Divisor pairs up to the square root |
| `bits_math/42` | Easy | Complement of Base 10 Integer | [#1009](https://leetcode.com/problems/complement-of-base-10-integer/) | XOR with an all-ones mask |
| `bits_math/45` | Easy | Distribute Candies to People | [#1103](https://leetcode.com/problems/distribute-candies-to-people/) | Arithmetic series instead of simulation |
| `bits_math/46` | Easy | Day of the Year | [#1154](https://leetcode.com/problems/day-of-the-year/) | Calendar arithmetic with the leap-year rule |
| `bits_math/47` | Easy | Day of the Week | [#1185](https://leetcode.com/problems/day-of-the-week/) | Zeller's congruence (calendar formula) |
| `bits_math/48` | Easy | Minimum Cost to Move Chips to The Same Position | [#1217](https://leetcode.com/problems/minimum-cost-to-move-chips-to-the-same-position/) | Parity classes |
| `bits_math/50` | Easy | Convert Integer to the Sum of Two No-Zero Integers | [#1317](https://leetcode.com/problems/convert-integer-to-the-sum-of-two-no-zero-integers/) | Search with an easy early exit |
| `bits_math/52` | Easy | Sort Integers by The Number of 1 Bits | [#1356](https://leetcode.com/problems/sort-integers-by-the-number-of-1-bits/) | Sort with a composite key |
| `bits_math/53` | Easy | Number of Days Between Two Dates | [#1360](https://leetcode.com/problems/number-of-days-between-two-dates/) | Convert to an absolute day count |
| `bits_math/55` | Easy | Count Square Sum Triples | [#1925](https://leetcode.com/problems/count-square-sum-triples/) | Remove a loop by computing the dependent value |
| `bits_math/3` | Medium | Sum of Two Integers | [#371](https://leetcode.com/problems/sum-of-two-integers/) | Bit manipulation: XOR = sum without carry, (AND << 1) = carry |
| `bits_math/4` | Medium | Pow(x, n) | [#50](https://leetcode.com/problems/powx-n/) | Exponentiation by squaring (binary decomposition of the exponent) |
| `bits_math/8` | Medium | Reverse Integer | [#7](https://leetcode.com/problems/reverse-integer/) | Digit extraction with divmod |
| `bits_math/11` | Medium | Count Primes | [#204](https://leetcode.com/problems/count-primes/) | Sieve: eliminate multiples instead of testing each number |
| `bits_math/13` | Medium | Single Number III | [#260](https://leetcode.com/problems/single-number-iii/) | XOR cancels pairs; split into two groups by a differing bit |
| `bits_math/14` | Medium | Single Number II | [#137](https://leetcode.com/problems/single-number-ii/) | Count each bit modulo 3 (two bit-masks as a base-3 counter) |
| `bits_math/15` | Medium | Bitwise AND of Numbers Range | [#201](https://leetcode.com/problems/bitwise-and-of-numbers-range/) | Common binary prefix of the two endpoints |
| `bits_math/16` | Medium | Factorial Trailing Zeroes | [#172](https://leetcode.com/problems/factorial-trailing-zeroes/) | Count prime factors (the scarcer prime, 5, decides) |
| `bits_math/22` | Medium | Integer to Roman | [#12](https://leetcode.com/problems/integer-to-roman/) | Greedy over a descending value table |
| `bits_math/34` | Medium | Divide Two Integers | [#29](https://leetcode.com/problems/divide-two-integers/) | Binary long division with shifts |
| `bits_math/36` | Medium | UTF-8 Validation | [#393](https://leetcode.com/problems/utf-8-validation/) | Bit masks / shifts with a state counter |
| `bits_math/38` | Medium | Total Hamming Distance | [#477](https://leetcode.com/problems/total-hamming-distance/) | Count per bit instead of per pair |
| `bits_math/40` | Medium | Maximum Swap | [#670](https://leetcode.com/problems/maximum-swap/) | Greedy with last-occurrence table |
| `bits_math/41` | Medium | Reordered Power of 2 | [#869](https://leetcode.com/problems/reordered-power-of-2/) | Canonical form (sorted digits) comparison |
| `bits_math/43` | Medium | Convert to Base -2 | [#1017](https://leetcode.com/problems/convert-to-base-2/) | Repeated division by a negative base |
| `bits_math/44` | Medium | Adding Two Negabinary Numbers | [#1073](https://leetcode.com/problems/adding-two-negabinary-numbers/) | Digit-wise addition with a sign-flipping carry |
| `bits_math/49` | Medium | Sequential Digits | [#1291](https://leetcode.com/problems/sequential-digits/) | Generate candidates instead of testing the range |
| `bits_math/51` | Medium | Angle Between Hands of a Clock | [#1344](https://leetcode.com/problems/angle-between-hands-of-a-clock/) | Angle arithmetic (rates of the two hands) |
| `bits_math/54` | Medium | Concatenation of Consecutive Binary Numbers | [#1680](https://leetcode.com/problems/concatenation-of-consecutive-binary-numbers/) | Shift-and-add with modular arithmetic |
| `bits_math/37` | Hard | Poor Pigs | [#458](https://leetcode.com/problems/poor-pigs/) | Information counting (base-(rounds+1) digits) |

Start one with `python dsa.py start bits_math/1`.

**More:** 191 Number of 1 Bits (E), 231 Power of Two (E), 268 Missing Number (E), 190 Reverse Bits (E), 137 Single Number II (M), 260 Single Number III (M), 201 Bitwise AND of Numbers Range (M), 421 Maximum XOR of Two Numbers in an Array (M), 1239 Maximum Length of a Concatenated String with Unique Characters (M), 204 Count Primes (M), 172 Factorial Trailing Zeroes (M), 1071 Greatest Common Divisor of Strings (E), 149 Max Points on a Line (H).

## 9. Make it stay - the teacher's anchors

**Picture it.** Light switches: each bit is a switch. XOR flips switches; two identical flips cancel out.

**The rule in one sentence.** n & (n-1) removes the lowest set bit; x ^ x = 0; x ^ 0 = x; n & -n isolates the lowest set bit; shifts multiply/divide by 2.

**Why it works.** Binary arithmetic acts on all bits in parallel, so a few instructions replace a loop over elements or bits.

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. Why does n & (n-1) clear the lowest set bit?
2. How does XOR find the single number?
3. Why is repeated squaring O(log n) for x**n?

**Mistakes students make most.**
- Forgetting Python ints are unbounded (mask with 0xFFFFFFFF for 32-bit tricks).
- Floor division with negatives.
- Overflow reasoning copied from C/Java (state it, then explain Python's difference).

**When NOT to use it.** A clear arithmetic or hash-based approach is just as fast and far more readable.

**The same idea in disguise.** Single number -> counting bits -> power of two -> sum without + (XOR + carry) -> reverse bits -> pow(x, n) (binary exponentiation) -> sieve (math).
