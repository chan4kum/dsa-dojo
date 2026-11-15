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
{{trace:bits}}

## 5. Template
{{solution:bits_math/4}}

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
{{ladder}}

**More:** 191 Number of 1 Bits (E), 231 Power of Two (E), 268 Missing Number (E), 190 Reverse Bits (E), 137 Single Number II (M), 260 Single Number III (M), 201 Bitwise AND of Numbers Range (M), 421 Maximum XOR of Two Numbers in an Array (M), 1239 Maximum Length of a Concatenated String with Unique Characters (M), 204 Count Primes (M), 172 Factorial Trailing Zeroes (M), 1071 Greatest Common Divisor of Strings (E), 149 Max Points on a Line (H).
