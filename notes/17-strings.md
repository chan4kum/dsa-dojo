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
`s = "ababaca"`; pi[i] = length of the longest proper prefix of s[:i+1] that is also a suffix

| i | s[i] | fallback | pi[i] |
|---|---|---|---|
| 0 | a | - | 0 |
| 1 | b | - | 0 |
| 2 | a | - | 1 |
| 3 | b | - | 2 |
| 4 | a | - | 3 |
| 5 | c | fell back from 3 -> 1 | 0 |
| 6 | a | - | 1 |

## 5. Template
*Reference solution for **Find the Index of the First Occurrence in a String** (`strings/1`) - tested by `python dsa.py selftest`:*

```python
def str_str(haystack, needle):
    if not needle:
        return 0
    m = len(needle)
    s = needle + "#" + haystack
    pi = [0] * len(s)
    for i in range(1, len(s)):
        k = pi[i - 1]
        while k and s[i] != s[k]:
            k = pi[k - 1]                # fall back, do not restart
        if s[i] == s[k]:
            k += 1
        pi[i] = k
        if k == m:
            return i - 2 * m             # match ends at i in s; start inside haystack
    return -1
```

## 6. Traps
- Forgetting the separator character (`#`) so borders cross from pattern into text.
- Off-by-one when converting the match end to a start index (`i - 2*m`).
- Empty needle/pattern.
- Using `str` concatenation in a loop (O(n^2)); use a list and `''.join`.
- Rolling hash collisions: use a large modulus (or two) and verify on a hash hit.

## 7. Self-check
1. Why is KMP O(n) even though there is a `while` inside the `for`?
2. How do you use the prefix function to test whether a string is built by repeating a substring?
3. What does `pi[-1]` of `"abcabcabc"` tell you?

## 8. Practice ladder
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `strings/1` | Easy | Find the Index of the First Occurrence in a String | [#28](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) | KMP / prefix function (reuse knowledge from partial matches) |
| `strings/3` | Easy | Longest Common Prefix | [#14](https://leetcode.com/problems/longest-common-prefix/) | Vertical scanning (column by column) |
| `strings/6` | Easy | Roman to Integer | [#13](https://leetcode.com/problems/roman-to-integer/) | Single left-to-right pass with a lookahead rule |
| `strings/7` | Easy | Add Strings | [#415](https://leetcode.com/problems/add-strings/) | Digit-by-digit arithmetic with carry (two pointers from the right) |
| `strings/4` | Medium | Reverse Words in a String | [#151](https://leetcode.com/problems/reverse-words-in-a-string/) | Split, reverse, join (in-place version: reverse all then each word) |
| `strings/5` | Medium | String to Integer (atoi) | [#8](https://leetcode.com/problems/string-to-integer-atoi/) | Careful state-by-state parsing (finite automaton) |
| `strings/8` | Medium | Multiply Strings | [#43](https://leetcode.com/problems/multiply-strings/) | Schoolbook multiplication with a position array |
| `strings/9` | Medium | Encode and Decode Strings | [#271](https://leetcode.com/problems/encode-and-decode-strings/) | Length-prefixed framing (the idea behind most network protocols) |
| `strings/2` | Hard | Longest Happy Prefix | [#1392](https://leetcode.com/problems/longest-happy-prefix/) | Prefix function (border of a string) |

Start one with `python dsa.py start strings/1`.

**More:** 459 Repeated Substring Pattern (E), 214 Shortest Palindrome (H), 187 Repeated DNA Sequences (M), 1044 Longest Duplicate Substring (H), 5 Longest Palindromic Substring (M), 647 Palindromic Substrings (M), 6 Zigzag Conversion (M), 8 String to Integer (M), 38 Count and Say (M), 68 Text Justification (H).

## 9. Make it stay - the teacher's anchors

**Picture it.** KMP is a reader who remembers how much of the pattern they had already matched, so after a mismatch they never re-read text they have already seen.

**The rule in one sentence.** Compare by index, not by slicing; precompute what the pattern already tells you about itself (the prefix function).

**Why it works.** The prefix function stores, for each position, the longest proper prefix that is also a suffix - exactly the amount of progress that survives a mismatch.

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. Compute the prefix function of 'abab' by hand.
2. Why is KMP O(n+m) when it seems to 'go back'?
3. How do you choose between expand-around-centre, DP and Manacher for palindromes?

**Mistakes students make most.**
- Slicing in loops (hidden O(n) per slice).
- Off-by-one with inclusive/exclusive ends.
- Ignoring Unicode/case/whitespace requirements in the prompt.

**When NOT to use it.** Python's built-ins (`find`, `in`, `split`) are allowed and clear - say so, then offer the manual version if asked.

**The same idea in disguise.** strStr -> longest prefix-suffix -> repeated substring -> atoi (state machine) -> add/multiply strings (carry) -> decode string (stack).
