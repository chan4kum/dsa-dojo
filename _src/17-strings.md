# 17 - String algorithms (pattern matching, borders, hashing)

> **One idea:** when a match fails, do not forget what you already learned about the text - reuse it.

## 1. First principles
- Naive matching compares the pattern at every offset: O(n*m). Most of those comparisons repeat work.
- **Prefix function (KMP):** `pi[i]` = length of the longest *proper* prefix of `s[:i+1]` that is also its suffix (a *border*). On a mismatch you fall back to `pi[k-1]` rather than restarting - total O(n + m).
- **Z-function:** `z[i]` = length of the longest common prefix of `s` and `s[i:]`. Same family, different view.
- **Rolling hash (Rabin-Karp):** hash of a window updated in O(1) when it slides; compare hashes first, strings only on a match. Great for "duplicate substring", with binary search on the length.
- **Manacher:** longest palindromic substring in O(n). In interviews: *expand around centre* (O(n^2)) is usually enough.
- Many "string" problems are really: hashing (anagrams), sliding window (substrings), DP (LCS/edit), trie (prefixes), stack (parsing).

## 2. How to spot it
- "find the pattern in the text", "repeated substring", "longest prefix which is also a suffix", "shortest palindrome by adding chars in front".
- "duplicate substring of length L", "search many substrings quickly".

## 3. Paper recipe
1. Write the pattern and, under it, the prefix function row **by hand** (see the trace).
2. For each position write the fallback chain when the next char mismatches.
3. For matching: build `pattern + '#' + text`; every place where `pi == len(pattern)` is a match end.
4. Alternatively think "border": period of a string = `n - pi[-1]`; repeated-substring test = `pi[-1] > 0 and n % (n - pi[-1]) == 0`.

## 4. Hand trace
{{trace:prefix_fn}}

## 5. Template
{{solution:strings/1}}

## 6. Traps
- Forgetting the separator character (`#`) so borders cross from pattern into text.
- Off-by-one when converting the match end to a start index (`i - 2*m`).
- Empty needle/pattern.
- Building a string with `s = piece + s` / `s += piece` in a loop: each step may copy the whole string, so it can be O(n^2) (CPython sometimes optimises `s += x` in place, but that is an implementation detail, never a guarantee). Collect pieces in a list and `''.join` once - always O(n).
- Rolling hash collisions: use a large modulus (or two) and verify on a hash hit.

## 7. Self-check
1. Why is KMP O(n) even though there is a `while` inside the `for`?
2. How do you use the prefix function to test whether a string is built by repeating a substring?
3. What does `pi[-1]` of `"abcabcabc"` tell you?

## 8. Practice ladder
{{ladder}}

**More:** 459 Repeated Substring Pattern (E), 214 Shortest Palindrome (H), 187 Repeated DNA Sequences (M), 1044 Longest Duplicate Substring (H), 5 Longest Palindromic Substring (M), 647 Palindromic Substrings (M), 6 Zigzag Conversion (M), 8 String to Integer (atoi) (M), 38 Count and Say (M), 68 Text Justification (H).
