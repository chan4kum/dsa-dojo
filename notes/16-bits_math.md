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
- Operator precedence: `a & b == c` parses as `a & (b == c)`; always parenthesise bit-ops.
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
| `bits_math/3` | Medium | Sum of Two Integers | [#371](https://leetcode.com/problems/sum-of-two-integers/) | Bit manipulation: XOR = sum without carry, (AND << 1) = carry |
| `bits_math/4` | Medium | Pow(x, n) | [#50](https://leetcode.com/problems/powx-n/) | Exponentiation by squaring (binary decomposition of the exponent) |
| `bits_math/8` | Medium | Reverse Integer | [#7](https://leetcode.com/problems/reverse-integer/) | Digit extraction with divmod |
| `bits_math/11` | Medium | Count Primes | [#204](https://leetcode.com/problems/count-primes/) | Sieve: eliminate multiples instead of testing each number |

Start one with `python dsa.py start bits_math/1`.

**More:** 191 Number of 1 Bits (E), 231 Power of Two (E), 268 Missing Number (E), 190 Reverse Bits (E), 137 Single Number II (M), 260 Single Number III (M), 201 Bitwise AND of Numbers Range (M), 421 Maximum XOR of Two Numbers (M), 1239 Maximum Length of a Concatenated String with Unique Characters (M), 204 Count Primes (M), 172 Factorial Trailing Zeroes (M), 1071 GCD of Strings (E), 149 Max Points on a Line (H).

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
