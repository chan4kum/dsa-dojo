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
# OPTIMISED: O(n + m) time (KMP)
# Idea: KMP / prefix function (reuse knowledge from partial matches)
def str_str(haystack, needle):
    if not needle:
        return 0
    m = len(needle)
    s = needle + "#" + haystack
    pi = [0] * len(s)
    for i in range(1, len(s)):
        k = pi[i - 1]
        while k and s[i] != s[k]:
            k = pi[k - 1]  # fall back, do not restart
        if s[i] == s[k]:
            k += 1
        pi[i] = k
        if k == m:
            return i - 2 * m  # match ends at i in s; start inside haystack
    return -1
```

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
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `strings/1` | Easy | Find the Index of the First Occurrence in a String | [#28](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/) | KMP / prefix function (reuse knowledge from partial matches) |
| `strings/3` | Easy | Longest Common Prefix | [#14](https://leetcode.com/problems/longest-common-prefix/) | Vertical scanning (column by column) |
| `strings/6` | Easy | Roman to Integer | [#13](https://leetcode.com/problems/roman-to-integer/) | Single left-to-right pass with a lookahead rule |
| `strings/7` | Easy | Add Strings | [#415](https://leetcode.com/problems/add-strings/) | Digit-by-digit arithmetic with carry (two pointers from the right) |
| `strings/10` | Easy | Reverse Vowels of a String | [#345](https://leetcode.com/problems/reverse-vowels-of-a-string/) | Two pointers from both ends, skipping non-vowels |
| `strings/11` | Easy | Repeated Substring Pattern | [#459](https://leetcode.com/problems/repeated-substring-pattern/) | String rotation trick: s is periodic iff s in (s + s)[1:-1] |
| `strings/12` | Easy | Count Binary Substrings | [#696](https://leetcode.com/problems/count-binary-substrings/) | Run-length groups: add min(previous run, current run) |
| `strings/15` | Easy | Longest Palindrome | [#409](https://leetcode.com/problems/longest-palindrome/) | Count frequencies: use all pairs, allow one odd centre |
| `strings/17` | Easy | Length of Last Word | [#58](https://leetcode.com/problems/length-of-last-word/) | Scan from the end |
| `strings/19` | Easy | Number of Segments in a String | [#434](https://leetcode.com/problems/number-of-segments-in-a-string/) | Count boundaries instead of building pieces |
| `strings/20` | Easy | Reverse String II | [#541](https://leetcode.com/problems/reverse-string-ii/) | Stride through blocks and slice |
| `strings/21` | Easy | Reverse Words in a String III | [#557](https://leetcode.com/problems/reverse-words-in-a-string-iii/) | Per-word two-pointer reversal |
| `strings/22` | Easy | Merge Strings Alternately | [#1768](https://leetcode.com/problems/merge-strings-alternately/) | Parallel iteration with bounds checks |
| `strings/24` | Easy | Add Binary | [#67](https://leetcode.com/problems/add-binary/) | Schoolbook addition with a carry |
| `strings/25` | Easy | License Key Formatting | [#482](https://leetcode.com/problems/license-key-formatting/) | Build from the right so the short group lands in front |
| `strings/26` | Easy | Detect Capital | [#520](https://leetcode.com/problems/detect-capital/) | Count and compare against the allowed patterns |
| `strings/27` | Easy | Student Attendance Record I | [#551](https://leetcode.com/problems/student-attendance-record-i/) | Single pass with counters |
| `strings/28` | Easy | Greatest Common Divisor of Strings | [#1071](https://leetcode.com/problems/greatest-common-divisor-of-strings/) | Number theory on string lengths (gcd) + commutativity check |
| `strings/30` | Easy | Increasing Decreasing String | [#1370](https://leetcode.com/problems/increasing-decreasing-string/) | Counting sort with alternating sweeps |
| `strings/31` | Easy | Consecutive Characters | [#1446](https://leetcode.com/problems/consecutive-characters/) | Run-length scan |
| `strings/32` | Easy | Largest Substring Between Two Equal Characters | [#1624](https://leetcode.com/problems/largest-substring-between-two-equal-characters/) | First-occurrence hash map |
| `strings/33` | Easy | Determine if String Halves Are Alike | [#1704](https://leetcode.com/problems/determine-if-string-halves-are-alike/) | Single pass with a running balance |
| `strings/35` | Easy | Find the Difference | [#389](https://leetcode.com/problems/find-the-difference/) | XOR / sum cancellation |
| `strings/36` | Easy | Longest Uncommon Subsequence I | [#521](https://leetcode.com/problems/longest-uncommon-subsequence-i/) | Reasoning shortcut (think before coding) |
| `strings/37` | Easy | Find Common Characters | [#1002](https://leetcode.com/problems/find-common-characters/) | Multiset intersection (min of counts) |
| `strings/50` | Easy | Buddy Strings | [#859](https://leetcode.com/problems/buddy-strings/) | Compare mismatch positions (+ duplicate-letter special case) |
| `strings/53` | Easy | Remove Letter To Equalize Frequency | [#2423](https://leetcode.com/problems/remove-letter-to-equalize-frequency/) | Frequency map + simulate each possible removal |
| `strings/4` | Medium | Reverse Words in a String | [#151](https://leetcode.com/problems/reverse-words-in-a-string/) | Split, reverse, join (in-place version: reverse all then each word) |
| `strings/5` | Medium | String to Integer (atoi) | [#8](https://leetcode.com/problems/string-to-integer-atoi/) | Careful state-by-state parsing (finite automaton) |
| `strings/8` | Medium | Multiply Strings | [#43](https://leetcode.com/problems/multiply-strings/) | Schoolbook multiplication with a position array |
| `strings/9` | Medium | Encode and Decode Strings | [#271](https://leetcode.com/problems/encode-and-decode-strings/) | Length-prefixed framing (the idea behind most network protocols) |
| `strings/13` | Medium | Count and Say | [#38](https://leetcode.com/problems/count-and-say/) | Run-length encoding, applied n - 1 times |
| `strings/14` | Medium | Zigzag Conversion | [#6](https://leetcode.com/problems/zigzag-conversion/) | Simulate a bouncing row index |
| `strings/16` | Medium | Repeated DNA Sequences | [#187](https://leetcode.com/problems/repeated-dna-sequences/) | Sliding window of fixed length + hash set of seen windows |
| `strings/18` | Medium | Compare Version Numbers | [#165](https://leetcode.com/problems/compare-version-numbers/) | Parse and compare component by component |
| `strings/29` | Medium | Minimum Number of Steps to Make Two Strings Anagram | [#1347](https://leetcode.com/problems/minimum-number-of-steps-to-make-two-strings-anagram/) | Frequency counting |
| `strings/34` | Medium | Count Number of Homogenous Substrings | [#1759](https://leetcode.com/problems/count-number-of-homogenous-substrings/) | Run-length counting (substrings ending here) |
| `strings/39` | Medium | Fraction to Recurring Decimal | [#166](https://leetcode.com/problems/fraction-to-recurring-decimal/) | Long division with a hash map of seen remainders |
| `strings/40` | Medium | Largest Number | [#179](https://leetcode.com/problems/largest-number/) | Custom comparator sort (order two items by the concatenations) |
| `strings/42` | Medium | Reconstruct Original Digits from English | [#423](https://leetcode.com/problems/reconstruct-original-digits-from-english/) | Count letters and peel off digits by unique letters |
| `strings/43` | Medium | Longest Uncommon Subsequence II | [#522](https://leetcode.com/problems/longest-uncommon-subsequence-ii/) | Candidate = the strings themselves; subsequence test with two pointers |
| `strings/44` | Medium | Optimal Division | [#553](https://leetcode.com/problems/optimal-division/) | Observation / closed form (maximise numerator, minimise denominator) |
| `strings/45` | Medium | Fraction Addition and Subtraction | [#592](https://leetcode.com/problems/fraction-addition-and-subtraction/) | Parsing + exact fraction arithmetic with gcd reduction |
| `strings/46` | Medium | Remove Comments | [#722](https://leetcode.com/problems/remove-comments/) | Character state machine (in / out of block comment) |
| `strings/47` | Medium | Rotated Digits | [#788](https://leetcode.com/problems/rotated-digits/) | Digit counting (inclusion / exclusion on digit sets) |
| `strings/48` | Medium | Custom Sort String | [#791](https://leetcode.com/problems/custom-sort-string/) | Counting sort by a custom alphabet |
| `strings/49` | Medium | Find And Replace in String | [#833](https://leetcode.com/problems/find-and-replace-in-string/) | Process edits in sorted order (build left to right) |
| `strings/51` | Medium | Decoded String at Index | [#880](https://leetcode.com/problems/decoded-string-at-index/) | Reverse traversal with modular reduction of the index |
| `strings/52` | Medium | Reorder Data in Log Files | [#937](https://leetcode.com/problems/reorder-data-in-log-files/) | Sort with a composite key (stable sort keeps digit-logs in order) |
| `strings/54` | Medium | Using a Robot to Print the Lexicographically Smallest String | [#2434](https://leetcode.com/problems/using-a-robot-to-print-the-lexicographically-smallest-string/) | Greedy stack + suffix minimum |
| `strings/57` | Medium | Compare Strings by Frequency of the Smallest Character | [#1170](https://leetcode.com/problems/compare-strings-by-frequency-of-the-smallest-character/) | Precompute a value per item, then sorted array + binary search |
| `strings/2` | Hard | Longest Happy Prefix | [#1392](https://leetcode.com/problems/longest-happy-prefix/) | Prefix function (border of a string) |
| `strings/23` | Hard | Shortest Palindrome | [#214](https://leetcode.com/problems/shortest-palindrome/) | KMP failure function to find the longest palindromic prefix |
| `strings/38` | Hard | Text Justification | [#68](https://leetcode.com/problems/text-justification/) | Greedy line packing + arithmetic space distribution |
| `strings/41` | Hard | Integer to English Words | [#273](https://leetcode.com/problems/integer-to-english-words/) | Chunking into 3-digit groups with lookup tables |
| `strings/55` | Hard | Match Substring After Replacement | [#2301](https://leetcode.com/problems/match-substring-after-replacement/) | Sliding comparison with a set of allowed substitutions |
| `strings/56` | Hard | Three Equal Parts | [#927](https://leetcode.com/problems/three-equal-parts/) | Count the ones, then compare three aligned slices |

Start one with `python dsa.py start strings/1`.

**More:** 459 Repeated Substring Pattern (E), 214 Shortest Palindrome (H), 187 Repeated DNA Sequences (M), 1044 Longest Duplicate Substring (H), 5 Longest Palindromic Substring (M), 647 Palindromic Substrings (M), 6 Zigzag Conversion (M), 8 String to Integer (atoi) (M), 38 Count and Say (M), 68 Text Justification (H).

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
