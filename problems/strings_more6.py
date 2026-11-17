"""extra batch of String problems - the problem bank for the "strings" topic (batch 6).

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

from collections import Counter
from itertools import groupby


def _freq_sort_ok(args, got):
    """True if got is a rearrangement of s in which each character forms ONE block and block sizes never grow."""
    (s,) = args
    if not isinstance(got, str) or sorted(got) != sorted(s):
        return False
    counts = Counter(s)
    blocks = [(ch, len(list(g))) for ch, g in groupby(got)]
    if len({ch for ch, _ in blocks}) != len(blocks):
        return False
    if any(counts[ch] != size for ch, size in blocks):
        return False
    sizes = [size for _, size in blocks]
    return sizes == sorted(sizes, reverse=True)


PROBLEMS = [
    # ---- Maximum Product of Word Lengths (LeetCode 318) ----
    dict(
        title="Maximum Product of Word Lengths",
        diff="M",
        lc=318,
        slug="maximum-product-of-word-lengths",
        prompt=(
            "words holds lowercase words. Return the largest value of len(words[i]) * len(words[j]) over pairs of "
            "words that share NO common letter. If no such pair exists, return 0."
        ),
        sig="def max_product(words: List[str]) -> int:",
        fn="max_product",
        tests=[
            ((["abcw", "baz", "foo", "bar", "xtfn", "abcdef"],), 16),
            ((["a", "ab", "abc", "d", "cd", "bcd", "abcd"],), 4),
            ((["a", "aa", "aaa", "aaaa"],), 0),
            ((["ab", "cd"],), 4),
        ],
        hints=[
            "Two words are compatible exactly when their SETS of letters are disjoint.",
            "A word's letter set fits in 26 bits: bit (ch - 'a') is on if the letter occurs.",
            "Two words are disjoint iff mask1 & mask2 == 0; keep only the longest word for each distinct mask.",
        ],
        pattern="Bitmask as a set of letters",
        explain=(
            "Comparing letters pairwise costs O(L) per pair. Encode each word as a 26-bit integer instead; then 'no "
            "shared letter' is a single AND being zero. Words with the same mask are interchangeable for this "
            "question, so only the longest one per mask matters, which also shrinks the number of pairs to try. Two "
            "words with equal masks share letters, so they never pair with each other."
        ),
        cx="O(total letters + M^2) time where M <= number of distinct masks, O(M) space",
        brute_cx="O(n^2 * L) time - build sets and intersect them for every pair",
        brute=r"""
# BRUTE FORCE: O(n^2 * L) time - build sets and intersect them for every pair
def max_product(words):
    best = 0
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            if not set(words[i]) & set(words[j]):
                best = max(best, len(words[i]) * len(words[j]))
    return best
""",
        solution=r"""
# OPTIMISED: O(total letters + M^2) time where M <= number of distinct masks, O(M) space
# Idea: Bitmask as a set of letters
def max_product(words):
    longest = {}
    for w in words:
        mask = 0
        for ch in w:
            mask |= 1 << (ord(ch) - 97)
        longest[mask] = max(longest.get(mask, 0), len(w))
    items = list(longest.items())
    best = 0
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i][0] & items[j][0] == 0:
                best = max(best, items[i][1] * items[j][1])
    return best
""",
    ),
    # ---- Palindrome Pairs (LeetCode 336) ----
    dict(
        title="Palindrome Pairs",
        diff="H",
        lc=336,
        slug="palindrome-pairs",
        prompt=(
            "words holds distinct strings (some may be empty). Return every pair of indices [i, j] with i != j such "
            "that words[i] + words[j] is a palindrome. The pairs may be returned in any order."
        ),
        sig="def palindrome_pairs(words: List[str]) -> List[List[int]]:",
        fn="palindrome_pairs",
        compare="unordered",
        tests=[
            ((["abcd", "dcba", "lls", "s", "sssll"],), [[0, 1], [1, 0], [3, 2], [2, 4]]),
            ((["bat", "tab", "cat"],), [[0, 1], [1, 0]]),
            ((["a", ""],), [[0, 1], [1, 0]]),
            ((["ab"],), []),
        ],
        hints=[
            (
                "Try every pair and test the concatenation - correct, but O(n^2 * L). How could a hash map avoid "
                "pairing everything?"
            ),
            (
                "If w + x is a palindrome and x is not longer than w, then w = (palindrome part) + reverse(x), or "
                "the mirror image."
            ),
            (
                "For each word w and each cut into left|right: if left is a palindrome, look up reverse(right) in a "
                "dict and put it BEFORE w; if right is a palindrome, look up reverse(left) and put it AFTER w."
            ),
        ],
        pattern="Split each word at every cut and look up the reversed half in a hash map",
        explain=(
            "Take a pair (a, b) with a + b a palindrome. Whichever word is shorter, the longer one splits into a "
            "palindromic piece plus the reverse of the shorter word. So for every word w and every cut position, if "
            "the left part is a palindrome then reverse(right) placed in FRONT of w completes a palindrome; if the "
            "right part is a palindrome then reverse(left) placed AFTER w does. Both cases are one dictionary "
            "lookup. To avoid reporting a pair twice, the 'right part palindrome' case skips the cut where the "
            "right part is empty (that case is already covered by the left-palindrome branch). The empty string is "
            "just another word: it pairs with every palindromic word in both orders."
        ),
        cx="O(n * L^2) time, O(n * L) space",
        brute_cx="O(n^2 * L) time - concatenate and test every ordered pair",
        brute=r"""
# BRUTE FORCE: O(n^2 * L) time - concatenate and test every ordered pair
def palindrome_pairs(words):
    out = []
    for i in range(len(words)):
        for j in range(len(words)):
            if i != j:
                s = words[i] + words[j]
                if s == s[::-1]:
                    out.append([i, j])
    return out
""",
        solution=r"""
# OPTIMISED: O(n * L^2) time, O(n * L) space
# Idea: Split each word at every cut and look up the reversed half in a hash map
def palindrome_pairs(words):
    index = {w: i for i, w in enumerate(words)}
    out = []
    for i, w in enumerate(words):
        for cut in range(len(w) + 1):
            left, right = w[:cut], w[cut:]
            if left == left[::-1]:
                j = index.get(right[::-1])
                if j is not None and j != i:
                    out.append([j, i])
            if cut != len(w) and right == right[::-1]:
                j = index.get(left[::-1])
                if j is not None and j != i:
                    out.append([i, j])
    return out
""",
    ),
    # ---- Sort Characters By Frequency (LeetCode 451) ----
    dict(
        title="Sort Characters By Frequency",
        diff="M",
        lc=451,
        slug="sort-characters-by-frequency",
        prompt=(
            "Rearrange the characters of s so that the most frequent characters come first, each distinct character "
            "forming one block. Characters with equal frequency may appear in any order. Any valid answer is "
            "accepted."
        ),
        sig="def frequency_sort(s: str) -> str:",
        fn="frequency_sort",
        check=_freq_sort_ok,
        tests=[
            (("tree",), "eert"),
            (("cccaaa",), "cccaaa"),
            (("Aabb",), "bbAa"),
            (("a",), "a"),
        ],
        hints=[
            "Count each character first; the output is built from blocks 'char repeated count times'.",
            "Sorting the blocks by count costs O(k log k); but counts are at most n, so a bucket per count works too.",
            (
                "Make n + 1 buckets: bucket[c] holds the blocks of characters that occur c times; read buckets from "
                "n down to 1."
            ),
        ],
        pattern="Counting + bucket sort by frequency",
        explain=(
            "Frequencies are integers between 1 and n, which is exactly the situation where bucket sort beats "
            "comparison sorting. After counting, drop each character's block (ch * count) into bucket[count]. "
            "Reading the buckets from the highest index down emits the blocks in decreasing frequency, and a block "
            "is never split, so each character stays together. The brute force just sorts every character by "
            "(-count, char)."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n log n) time - sort all n characters by (-frequency, character)",
        brute=r"""
# BRUTE FORCE: O(n log n) time - sort all n characters by (-frequency, character)
def frequency_sort(s):
    counts = Counter(s)
    return "".join(sorted(s, key=lambda ch: (-counts[ch], ch)))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Counting + bucket sort by frequency
def frequency_sort(s):
    counts = Counter(s)
    buckets = [[] for _ in range(len(s) + 1)]
    for ch, k in counts.items():
        buckets[k].append(ch * k)
    return "".join("".join(b) for b in reversed(buckets))
""",
    ),
    # ---- Validate IP Address (LeetCode 468) ----
    dict(
        title="Validate IP Address",
        diff="M",
        lc=468,
        slug="validate-ip-address",
        prompt=(
            "Return 'IPv4' if query_ip is a valid IPv4 address, 'IPv6' if it is a valid IPv6 address, else "
            "'Neither'. IPv4: four decimal numbers 0..255 separated by '.', with no leading zeros (so '01' is "
            "invalid). IPv6: eight groups of 1 to 4 hexadecimal digits (either case) separated by ':'; leading "
            "zeros are allowed and '::' compression is NOT allowed."
        ),
        sig="def valid_ip_address(query_ip: str) -> str:",
        fn="valid_ip_address",
        tests=[
            (("172.16.254.1",), "IPv4"),
            (("2001:0db8:85a3:0:0:8A2E:0370:7334",), "IPv6"),
            (("256.256.256.256",), "Neither"),
            (("1.1.1.01",), "Neither"),
            (("2001:0db8:85a3::8A2E:037j:7334",), "Neither"),
            (("02001:0db8:85a3:0000:0000:8a2e:0370:7334",), "Neither"),
        ],
        hints=[
            "The separator decides the format: exactly three '.' means try IPv4, exactly seven ':' means try IPv6.",
            "Validate every group on its own: IPv4 groups are 1-3 digits, no leading zero (except '0'), value <= 255.",
            "Check characters yourself ('0123456789' / hex digits) - int() would accept signs, spaces and underscores.",
        ],
        pattern="Split by separator, then validate each field with explicit rules",
        explain=(
            "Parsing problems are mostly about being strict. After deciding the family by counting separators, "
            "split and test every field. For IPv4 each field must be non-empty, only ASCII digits, at most 3 "
            "characters, no leading zero unless it is exactly '0', and numerically at most 255. For IPv6 each field "
            "must be 1 to 4 characters, all hexadecimal. Never rely on int(): it quietly accepts '+5', ' 5' and "
            "'1_0'. The brute force instead checks each IPv4 field by trying every legal value 0..255 and comparing "
            "its canonical text."
        ),
        cx="O(n) time, O(1) extra space",
        brute_cx="O(n + 4 * 256) time - compare each IPv4 field with the text of every value 0..255",
        brute=r"""
# BRUTE FORCE: O(n + 4 * 256) time - compare each IPv4 field with the text of every value 0..255
def valid_ip_address(query_ip):
    if query_ip.count(".") == 3:
        for part in query_ip.split("."):
            if not any(part == str(v) for v in range(256)):
                return "Neither"
        return "IPv4"
    if query_ip.count(":") == 7:
        for part in query_ip.split(":"):
            if not 1 <= len(part) <= 4:
                return "Neither"
            for ch in part:
                if ch not in "0123456789abcdefABCDEF":
                    return "Neither"
        return "IPv6"
    return "Neither"
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) extra space
# Idea: Split by separator, then validate each field with explicit rules
def valid_ip_address(query_ip):
    if query_ip.count(".") == 3:
        for part in query_ip.split("."):
            if not part or len(part) > 3:
                return "Neither"
            if any(ch not in "0123456789" for ch in part):
                return "Neither"
            if len(part) > 1 and part[0] == "0":
                return "Neither"
            if int(part) > 255:
                return "Neither"
        return "IPv4"
    if query_ip.count(":") == 7:
        for part in query_ip.split(":"):
            if not 1 <= len(part) <= 4:
                return "Neither"
            if any(ch not in "0123456789abcdefABCDEF" for ch in part):
                return "Neither"
        return "IPv6"
    return "Neither"
""",
    ),
    # ---- Find the Closest Palindrome (LeetCode 564) ----
    dict(
        title="Find the Closest Palindrome",
        diff="H",
        lc=564,
        slug="find-the-closest-palindrome",
        prompt=(
            "n is a positive integer given as a string. Return, as a string, the closest integer to n that is a "
            "palindrome and is NOT n itself. If two palindromes are equally close, return the smaller one."
        ),
        sig="def nearest_palindromic(n: str) -> str:",
        fn="nearest_palindromic",
        tests=[
            (("123",), "121"),
            (("1",), "0"),
            (("99",), "101"),
            (("10",), "9"),
            (("1213",), "1221"),
        ],
        hints=[
            (
                "Searching n-1, n+1, n-2, n+2, ... works for small n but can take about 10^(len/2) steps - far too "
                "slow for 18 digits."
            ),
            (
                "The closest palindrome keeps (almost) the same left half: mirror the left half, and also try left "
                "half - 1 and + 1."
            ),
            (
                "Also include the 'carry' cases 10^(L-1) - 1 (all nines, one digit shorter) and 10^L + 1; drop n "
                "itself and pick the smallest distance, breaking ties by the smaller number."
            ),
        ],
        pattern="Generate a handful of candidate palindromes from the prefix, then pick the best",
        explain=(
            "A palindrome is fixed by its left half, so the nearest one must come from a left half that differs "
            "from n's by at most 1 (a bigger change moves the number by at least 10^(L/2)). Mirror prefix-1, prefix "
            "and prefix+1 to get three candidates (take care of odd length by not repeating the middle digit). "
            "Changing the length gives two more: 99...9 with one digit fewer and 10...01 with one digit more. "
            "Remove n itself, then choose the minimum by (distance, value). The brute force walks outward one step "
            "at a time."
        ),
        cx="O(L) time and space for an L-digit number",
        brute_cx="O(distance to the nearest palindrome) steps, each O(L) - walk outward from n",
        brute=r"""
# BRUTE FORCE: O(distance to the nearest palindrome) steps, each O(L) - walk outward from n
def nearest_palindromic(n):
    num = int(n)
    d = 1
    while True:
        lo = num - d
        if lo >= 0 and str(lo) == str(lo)[::-1]:
            return str(lo)
        hi = num + d
        if str(hi) == str(hi)[::-1]:
            return str(hi)
        d += 1
""",
        solution=r"""
# OPTIMISED: O(L) time and space for an L-digit number
# Idea: Generate a handful of candidate palindromes from the prefix, then pick the best
def nearest_palindromic(n):
    length = len(n)
    num = int(n)
    cands = {10 ** (length - 1) - 1, 10**length + 1}
    prefix = int(n[: (length + 1) // 2])
    for p in (prefix - 1, prefix, prefix + 1):
        s = str(p)
        tail = s[:-1] if length % 2 else s
        cands.add(int(s + tail[::-1]))
    cands.discard(num)
    return str(min(cands, key=lambda x: (abs(x - num), x)))
""",
    ),
    # ---- Find Duplicate File in System (LeetCode 609) ----
    dict(
        title="Find Duplicate File in System",
        diff="M",
        lc=609,
        slug="find-duplicate-file-in-system",
        prompt=(
            "Each string in paths looks like 'dir file1.txt(content1) file2.txt(content2) ...'. Return the groups "
            "of full file paths ('dir/file') that have identical content; ignore contents held by only one file. "
            "The groups and the paths inside a group may be in any order."
        ),
        sig="def find_duplicate(paths: List[str]) -> List[List[str]]:",
        fn="find_duplicate",
        compare="nested_unordered",
        tests=[
            (
                (["root/a 1.txt(abcd) 2.txt(efgh)", "root/c 3.txt(abcd)", "root/c/d 4.txt(efgh)", "root 4.txt(efgh)"],),
                [["root/a/2.txt", "root/c/d/4.txt", "root/4.txt"], ["root/a/1.txt", "root/c/3.txt"]],
            ),
            (
                (["root/a 1.txt(abcd) 2.txt(efgh)", "root/c 3.txt(abcd)", "root/c/d 4.txt(efgh)"],),
                [["root/a/2.txt", "root/c/d/4.txt"], ["root/a/1.txt", "root/c/3.txt"]],
            ),
            ((["root 1.txt(a)"],), []),
            ((["r a.txt(x) b.txt(x)"],), [["r/a.txt", "r/b.txt"]]),
        ],
        hints=[
            "First parse every entry: split on spaces; the first token is the directory, the rest are name(content).",
            "Two files are duplicates exactly when their content strings are equal - so content is the natural key.",
            "Map content -> list of full paths in one pass, then return the lists that have at least two paths.",
        ],
        pattern="Group by key with a hash map",
        explain=(
            "Parsing gives (full path, content) pairs. Grouping equal contents is the textbook use of a dictionary "
            "from content to a list of paths; afterwards keep the groups whose size is at least 2. The brute force "
            "re-scans all files for every new content value, which is quadratic in the number of files. (In a real "
            "file system you would not compare whole contents but sizes first, then hashes - a good follow-up "
            "discussion.)"
        ),
        cx="O(total characters) time and space",
        brute_cx="O(F^2) comparisons for F files - rescan every file for each new content",
        brute=r"""
# BRUTE FORCE: O(F^2) comparisons for F files - rescan every file for each new content
def find_duplicate(paths):
    files = []
    for entry in paths:
        parts = entry.split(" ")
        for item in parts[1:]:
            name, content = item[:-1].split("(")
            files.append((content, parts[0] + "/" + name))
    out, done = [], set()
    for content, _ in files:
        if content in done:
            continue
        done.add(content)
        group = [p for c, p in files if c == content]
        if len(group) > 1:
            out.append(group)
    return out
""",
        solution=r"""
# OPTIMISED: O(total characters) time and space
# Idea: Group by key with a hash map
def find_duplicate(paths):
    groups = defaultdict(list)
    for entry in paths:
        parts = entry.split(" ")
        for item in parts[1:]:
            name, content = item[:-1].split("(")
            groups[content].append(parts[0] + "/" + name)
    return [g for g in groups.values() if len(g) > 1]
""",
    ),
    # ---- Repeated String Match (LeetCode 686) ----
    dict(
        title="Repeated String Match",
        diff="M",
        lc=686,
        slug="repeated-string-match",
        prompt=(
            "Return the minimum number of times a must be written one after another so that b is a substring of the "
            "result, or -1 if that is impossible."
        ),
        sig="def repeated_string_match(a: str, b: str) -> int:",
        fn="repeated_string_match",
        tests=[
            (("abcd", "cdabcdab"), 3),
            (("a", "aa"), 2),
            (("a", "a"), 1),
            (("abc", "wxyz"), -1),
        ],
        hints=[
            "You need at least ceil(len(b) / len(a)) copies just to be long enough to contain b.",
            "b may start in the middle of one copy, so one extra copy can be necessary - but never two more.",
            "Build a * q with q = ceil(len(b) / len(a)) and test b in it; if not found, test one more copy; else -1.",
        ],
        pattern="Length bound: only q and q + 1 repetitions need testing",
        explain=(
            "Writing a q = ceil(|b| / |a|) times gives the shortest string that could possibly hold b. If b begins "
            "inside a copy, its last characters spill into at most one extra copy, so q + 1 copies are the most "
            "that can ever be needed: any occurrence of b in a longer repetition also occurs within the first q + 1 "
            "copies shifted by whole periods. If neither q nor q + 1 copies contain b, no number will. The brute "
            "force simply tries 1, 2, 3, ... copies up to that bound."
        ),
        cx="O(|a| * q + |b|) time with a linear substring search, O(|a| * q) space",
        brute_cx="O(q^2 * |a|) time - rebuild and search every repetition count from 1 to q + 2",
        brute=r"""
# BRUTE FORCE: O(q^2 * |a|) time - rebuild and search every repetition count from 1 to q + 2
def repeated_string_match(a, b):
    q = -(-len(b) // len(a))
    for k in range(1, q + 3):
        if b in a * k:
            return k
    return -1
""",
        solution=r"""
# OPTIMISED: O(|a| * q + |b|) time with a linear substring search, O(|a| * q) space
# Idea: Length bound: only q and q + 1 repetitions need testing
def repeated_string_match(a, b):
    q = -(-len(b) // len(a))
    for k in (q, q + 1):
        if b in a * k:
            return k
    return -1
""",
    ),
    # ---- Most Common Word (LeetCode 819) ----
    dict(
        title="Most Common Word",
        diff="E",
        lc=819,
        slug="most-common-word",
        prompt=(
            "paragraph contains words separated by spaces and punctuation (!?',;.). Return the most frequent word "
            "that is not in banned, in lowercase. Words are case-insensitive and the answer is guaranteed to be "
            "unique."
        ),
        sig="def most_common_word(paragraph: str, banned: List[str]) -> str:",
        fn="most_common_word",
        tests=[
            (("Bob hit a ball, the hit BALL flew far after it was hit.", ["hit"]), "ball"),
            (("a.", []), "a"),
            (("a, a, a, a, b,b,b,c, c", ["a"]), "b"),
            (("Bob. hIt, baLl", ["bob", "hit"]), "ball"),
        ],
        hints=[
            "Normalise first: lowercase everything and turn every non-letter into a space, then split.",
            "Put the banned words in a set so each membership test is O(1).",
            "Count the remaining words with a hash map (Counter) and take the maximum by count.",
        ],
        pattern="Normalise, filter with a set, count with a hash map",
        explain=(
            "Most of the work is cleaning: replace anything that is not a letter by a space and lowercase the rest, "
            "so 'Ball,' and 'BALL' become the same token. Banned words go into a set. A Counter then gives "
            "frequencies and max(..., key=counts.get) picks the winner. The brute force recounts each word with "
            "list.count, which is quadratic in the number of words."
        ),
        cx="O(n + b) time, O(n + b) space (n characters, b banned words)",
        brute_cx="O(w^2) time for w words - list.count for every word",
        brute=r"""
# BRUTE FORCE: O(w^2) time for w words - list.count for every word
def most_common_word(paragraph, banned):
    cleaned = "".join(ch.lower() if ch.isalpha() else " " for ch in paragraph)
    words = [w for w in cleaned.split() if w not in banned]
    best, best_count = "", 0
    for w in words:
        c = words.count(w)
        if c > best_count:
            best, best_count = w, c
    return best
""",
        solution=r"""
# OPTIMISED: O(n + b) time, O(n + b) space (n characters, b banned words)
# Idea: Normalise, filter with a set, count with a hash map
def most_common_word(paragraph, banned):
    cleaned = "".join(ch.lower() if ch.isalpha() else " " for ch in paragraph)
    blocked = set(banned)
    counts = Counter(w for w in cleaned.split() if w not in blocked)
    return max(counts, key=counts.get)
""",
    ),
    # ---- Groups of Special-Equivalent Strings (LeetCode 893) ----
    dict(
        title="Groups of Special-Equivalent Strings",
        diff="M",
        lc=893,
        slug="groups-of-special-equivalent-strings",
        prompt=(
            "In one move you may swap any two characters of a word whose indices have the SAME parity (both even or "
            "both odd). Two words are special-equivalent if one can become the other with such moves. Return the "
            "number of groups of mutually special-equivalent words in words."
        ),
        sig="def num_special_equiv_groups(words: List[str]) -> int:",
        fn="num_special_equiv_groups",
        tests=[
            ((["abcd", "cdab", "cbad", "xyzz", "zzxy", "zzyx"],), 3),
            ((["abc", "acb", "bac", "bca", "cab", "cba"],), 3),
            ((["a"],), 1),
            ((["ab", "ba"],), 2),
        ],
        hints=[
            "Swaps never move a character between even and odd positions.",
            "So a word is described by two multisets: its even-position letters and its odd-position letters.",
            "Use (sorted evens, sorted odds) as a canonical signature and count the distinct signatures.",
        ],
        pattern="Canonical form (signature) for an equivalence class",
        explain=(
            "Equivalence classes are easiest to count by computing a canonical representative. Because the allowed "
            "swaps permute even positions among themselves and odd positions among themselves, any arrangement of "
            "the even letters and any arrangement of the odd letters is reachable. Hence two words are equivalent "
            "iff their even-letter multisets are equal and their odd-letter multisets are equal. Sorting each half "
            "gives a signature; the number of distinct signatures is the answer. The brute force compares each word "
            "with one representative per existing group."
        ),
        cx="O(n * L log L) time, O(n * L) space",
        brute_cx="O(n * groups * L log L) time - compare every word with each group's representative",
        brute=r"""
# BRUTE FORCE: O(n * groups * L log L) time - compare every word with each group's representative
def num_special_equiv_groups(words):
    reps = []
    for w in words:
        for r in reps:
            if sorted(w[::2]) == sorted(r[::2]) and sorted(w[1::2]) == sorted(r[1::2]):
                break
        else:
            reps.append(w)
    return len(reps)
""",
        solution=r"""
# OPTIMISED: O(n * L log L) time, O(n * L) space
# Idea: Canonical form (signature) for an equivalence class
def num_special_equiv_groups(words):
    return len({(tuple(sorted(w[::2])), tuple(sorted(w[1::2]))) for w in words})
""",
    ),
    # ---- Verifying an Alien Dictionary (LeetCode 953) ----
    dict(
        title="Verifying an Alien Dictionary",
        diff="E",
        lc=953,
        slug="verifying-an-alien-dictionary",
        prompt=(
            "An alien language uses the lowercase letters in a different alphabetical order, given by the string "
            "order. Return true if words are sorted lexicographically according to that order. (A prefix comes "
            "before any longer word that starts with it.)"
        ),
        sig="def is_alien_sorted(words: List[str], order: str) -> bool:",
        fn="is_alien_sorted",
        tests=[
            ((["hello", "leetcode"], "hlabcdefgijkmnopqrstuvwxyz"), True),
            ((["word", "world", "row"], "worldabcefghijkmnpqstuvxyz"), False),
            ((["apple", "app"], "abcdefghijklmnopqrstuvwxyz"), False),
            ((["app", "apple"], "abcdefghijklmnopqrstuvwxyz"), True),
        ],
        hints=[
            "Give every letter a rank: rank[order[i]] = i. Comparing words then means comparing lists of ranks.",
            "A list is sorted iff every ADJACENT pair is in order - you do not need to check all pairs.",
            (
                "For an adjacent pair, find the first differing position; if there is none, the shorter word must "
                "come first."
            ),
        ],
        pattern="Re-map the alphabet, then compare adjacent items",
        explain=(
            "Sortedness is transitive, so checking neighbours is enough: if words[i] <= words[i+1] for all i then "
            "the whole list is sorted. Replacing every letter with its position in order lets Python compare the "
            "lists of ranks lexicographically, which also handles the prefix rule correctly (a proper prefix is "
            "smaller). The brute force checks every pair i < j instead of only neighbours."
        ),
        cx="O(total characters) time, O(1) extra space (26 ranks)",
        brute_cx="O(n^2 * L) time - compare every pair of words, not just neighbours",
        brute=r"""
# BRUTE FORCE: O(n^2 * L) time - compare every pair of words, not just neighbours
def is_alien_sorted(words, order):
    rank = {ch: i for i, ch in enumerate(order)}
    keys = [[rank[ch] for ch in w] for w in words]
    for i in range(len(keys)):
        for j in range(i + 1, len(keys)):
            if keys[i] > keys[j]:
                return False
    return True
""",
        solution=r"""
# OPTIMISED: O(total characters) time, O(1) extra space (26 ranks)
# Idea: Re-map the alphabet, then compare adjacent items
def is_alien_sorted(words, order):
    rank = {ch: i for i, ch in enumerate(order)}
    keys = [[rank[ch] for ch in w] for w in words]
    return all(keys[i] <= keys[i + 1] for i in range(len(keys) - 1))
""",
    ),
    # ---- Check If Word Is Valid After Substitutions (LeetCode 1003) ----
    dict(
        title="Check If Word Is Valid After Substitutions",
        diff="M",
        lc=1003,
        slug="check-if-word-is-valid-after-substitutions",
        prompt=(
            "Start with the empty string and repeatedly insert the string 'abc' at any position. Return true if s "
            "can be produced this way."
        ),
        sig="def is_valid(s: str) -> bool:",
        fn="is_valid",
        tests=[
            (("aabcbc",), True),
            (("abcabcababcc",), True),
            (("abccba",), False),
            (("a",), False),
            (("abc",), True),
        ],
        hints=[
            (
                "Run the process backwards: a valid string must contain 'abc' somewhere, and deleting it leaves a "
                "valid string."
            ),
            "Repeatedly deleting 'abc' with replace() works but rescans the string each time.",
            (
                "Use a stack: push each character, and whenever the top three are 'a','b','c', pop them. Valid iff "
                "the stack ends empty."
            ),
        ],
        pattern="Stack reduction (undo the insertions as you scan)",
        explain=(
            "Every valid string ends with its last inserted 'abc' as an unbroken block, and removing that block "
            "leaves a valid string - so undoing insertions greedily is safe. A stack performs all removals in one "
            "left-to-right pass: after pushing a character, if the top three characters spell 'abc' they are a "
            "freshly closed block and can be removed. If the stack is empty at the end, every character was "
            "consumed by some 'abc'. Brute force: keep calling replace('abc', '') until nothing changes."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - rescan the whole string after each removal",
        brute=r"""
# BRUTE FORCE: O(n^2) time - rescan the whole string after each removal
def is_valid(s):
    while "abc" in s:
        s = s.replace("abc", "")
    return s == ""
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Stack reduction (undo the insertions as you scan)
def is_valid(s):
    stack = []
    for ch in s:
        stack.append(ch)
        if len(stack) >= 3 and stack[-3] == "a" and stack[-2] == "b" and stack[-1] == "c":
            del stack[-3:]
    return not stack
""",
    ),
    # ---- Camelcase Matching (LeetCode 1023) ----
    dict(
        title="Camelcase Matching",
        diff="M",
        lc=1023,
        slug="camelcase-matching",
        prompt=(
            "A query matches pattern if you can insert only LOWERCASE letters into the pattern (at any positions) "
            "to obtain the query. Return, for each query, whether it matches."
        ),
        sig="def camel_match(queries: List[str], pattern: str) -> List[bool]:",
        fn="camel_match",
        tests=[
            (
                (["FooBar", "FooBarTest", "FootBall", "FrameBuffer", "ForceFeedBack"], "FB"),
                [True, False, True, True, False],
            ),
            (
                (["FooBar", "FooBarTest", "FootBall", "FrameBuffer", "ForceFeedBack"], "FoBa"),
                [True, False, True, False, False],
            ),
            ((["a"], "a"), [True]),
            ((["aBc", "BB"], "B"), [True, False]),
        ],
        hints=[
            "Every uppercase letter of the query must be 'explained' by the pattern - it cannot be an inserted letter.",
            "Walk the query with a pointer i into the pattern: if the current letter equals pattern[i], advance i.",
            (
                "Otherwise the letter must be lowercase (an insertion); an uppercase mismatch means failure. At the "
                "end i must have consumed the whole pattern."
            ),
        ],
        pattern="Two pointers: greedy subsequence match with an uppercase constraint",
        explain=(
            "Matching is a subsequence test with one extra rule: letters of the query that are NOT matched to the "
            "pattern may only be lowercase. Scanning greedily, take a match whenever the query letter equals the "
            "next pattern letter (matching as early as possible never hurts); any other letter must be lowercase. "
            "The query matches iff the pattern is fully consumed and no unmatched uppercase letter appeared. The "
            "brute force explores both choices (match it / treat it as inserted) recursively."
        ),
        cx="O(total query length) time, O(1) extra space",
        brute_cx="O(2^L) time per query in the worst case - try 'match' and 'insert' at every lowercase letter",
        brute=r"""
# BRUTE FORCE: O(2^L) time per query in the worst case - try 'match' and 'insert' at every lowercase letter
def camel_match(queries, pattern):
    def ok(q, p):
        if not q:
            return not p
        if p and q[0] == p[0] and ok(q[1:], p[1:]):
            return True
        return q[0].islower() and ok(q[1:], p)

    return [ok(q, pattern) for q in queries]
""",
        solution=r"""
# OPTIMISED: O(total query length) time, O(1) extra space
# Idea: Two pointers: greedy subsequence match with an uppercase constraint
def camel_match(queries, pattern):
    out = []
    for q in queries:
        i = 0
        good = True
        for ch in q:
            if i < len(pattern) and ch == pattern[i]:
                i += 1
            elif ch.isupper():
                good = False
                break
        out.append(good and i == len(pattern))
    return out
""",
    ),
    # ---- Last Substring in Lexicographical Order (LeetCode 1163) ----
    dict(
        title="Last Substring in Lexicographical Order",
        diff="H",
        lc=1163,
        slug="last-substring-in-lexicographical-order",
        prompt="Return the lexicographically largest substring of s.",
        sig="def last_substring(s: str) -> str:",
        fn="last_substring",
        tests=[
            (("abab",), "bab"),
            (("leetcode",), "tcode"),
            (("a",), "a"),
            (("aaa",), "aaa"),
            (("cacacb",), "cb"),
        ],
        hints=[
            "The largest substring is always a SUFFIX: extending a substring to the right only makes it larger.",
            "So the task is: find the largest suffix. Comparing all n suffixes costs O(n^2).",
            (
                "Keep two candidate start indices i < j and a match length k; when s[i+k] and s[j+k] differ, the "
                "smaller one can never start the answer, so jump past it."
            ),
        ],
        pattern="Two-candidate scan (largest suffix, linear time)",
        explain=(
            "Any substring can be extended to the end of s without becoming smaller, so the answer is the maximum "
            "suffix. Maintain two candidates i < j and compare s[i..] with s[j..] character by character, k "
            "characters deep. If s[i+k] < s[j+k], then every start in i..i+k loses to the corresponding start in "
            "j..j+k, so skip i to i+k+1 (but not behind j). If s[i+k] > s[j+k], symmetrically skip j past j+k. Each "
            "skip advances a pointer by more than the work done, so the total work is linear. The brute force "
            "builds every suffix and takes max()."
        ),
        cx="O(n) time, O(1) extra space",
        brute_cx="O(n^2) time and space - build all suffixes and take the maximum",
        brute=r"""
# BRUTE FORCE: O(n^2) time and space - build all suffixes and take the maximum
def last_substring(s):
    return max(s[i:] for i in range(len(s)))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) extra space
# Idea: Two-candidate scan (largest suffix, linear time)
def last_substring(s):
    n = len(s)
    i, j, k = 0, 1, 0
    while j + k < n:
        if s[i + k] == s[j + k]:
            k += 1
        elif s[i + k] < s[j + k]:
            i = max(i + k + 1, j)
            j = i + 1
            k = 0
        else:
            j += k + 1
            k = 0
    return s[i:]
""",
    ),
    # ---- Count Substrings That Differ by One Character (LeetCode 1638) ----
    dict(
        title="Count Substrings That Differ by One Character",
        diff="M",
        lc=1638,
        slug="count-substrings-that-differ-by-one-character",
        prompt=(
            "Count the pairs (a substring of s, a substring of t) of equal length that differ in EXACTLY one "
            "position. Substrings at different positions count as different even if their text is equal."
        ),
        sig="def count_substrings(s: str, t: str) -> int:",
        fn="count_substrings",
        tests=[
            (("aba", "baba"), 6),
            (("ab", "bb"), 3),
            (("a", "a"), 0),
            (("abe", "bbc"), 10),
        ],
        hints=[
            "Fix the single mismatching pair of positions (i, j) with s[i] != t[j].",
            "The two substrings then extend that mismatch to the left and to the right using only EQUAL characters.",
            (
                "If L equal characters precede the mismatch (on both strings, diagonally) and R follow it, there "
                "are (L + 1) * (R + 1) pairs."
            ),
        ],
        pattern="Count by the unique mismatch; precompute equal-run lengths on diagonals",
        explain=(
            "Every valid pair has exactly one mismatching position; so classify pairs by that position (i, j). Left "
            "of it the two substrings agree for some number of characters (0..L), where L is the length of the "
            "equal run ending right before (i, j) along the diagonal; to the right they agree for 0..R characters. "
            "Choices on both sides are independent, giving (L + 1) * (R + 1). L and R come from two DP tables: "
            "left[i][j] = left[i-1][j-1] + 1 if the characters match else 0, and the mirrored table for the right "
            "side. The brute force tries every pair of starting positions and lengths and counts differences."
        ),
        cx="O(|s| * |t|) time and space",
        brute_cx="O(|s| * |t| * min(|s|, |t|)^2) time - enumerate pairs of substrings and count differences",
        brute=r"""
# BRUTE FORCE: O(|s| * |t| * min(|s|, |t|)^2) time - enumerate pairs of substrings and count differences
def count_substrings(s, t):
    total = 0
    for i in range(len(s)):
        for j in range(len(t)):
            diff = 0
            k = 0
            while i + k < len(s) and j + k < len(t):
                if s[i + k] != t[j + k]:
                    diff += 1
                if diff == 1:
                    total += 1
                elif diff > 1:
                    break
                k += 1
    return total
""",
        solution=r"""
# OPTIMISED: O(|s| * |t|) time and space
# Idea: Count by the unique mismatch; precompute equal-run lengths on diagonals
def count_substrings(s, t):
    m, n = len(s), len(t)
    left = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s[i - 1] == t[j - 1]:
                left[i][j] = left[i - 1][j - 1] + 1
    right = [[0] * (n + 2) for _ in range(m + 2)]
    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            if s[i] == t[j]:
                right[i][j] = right[i + 1][j + 1] + 1
    total = 0
    for i in range(m):
        for j in range(n):
            if s[i] != t[j]:
                total += (left[i][j] + 1) * (right[i + 1][j + 1] + 1)
    return total
""",
    ),
    # ---- Maximum Repeating Substring (LeetCode 1668) ----
    dict(
        title="Maximum Repeating Substring",
        diff="E",
        lc=1668,
        slug="maximum-repeating-substring",
        prompt=(
            "The k-repeating value of word is the largest k such that word repeated k times is a substring of "
            "sequence (0 if word itself is not a substring). Return it."
        ),
        sig="def max_repeating(sequence: str, word: str) -> int:",
        fn="max_repeating",
        tests=[
            (("ababc", "ab"), 2),
            (("ababc", "ba"), 1),
            (("ababc", "ac"), 0),
            (("aaaa", "a"), 4),
        ],
        hints=[
            "Brute force: keep increasing k while word * (k + 1) is still inside sequence.",
            "Define dp[i] = the number of consecutive copies of word that end exactly at position i of sequence.",
            "If sequence[i - w : i] == word then dp[i] = dp[i - w] + 1; the answer is the maximum dp value.",
        ],
        pattern="DP over end positions: chain consecutive matches",
        explain=(
            "A run of k copies of word ending at position i exists iff word ends at i and a run of k - 1 copies "
            "ends at i - len(word). That recurrence is dp[i] = dp[i - w] + 1 when the last w characters equal word, "
            "else 0. One left-to-right pass fills dp with a single O(w) comparison per index, and the maximum entry "
            "is the answer. The brute force rebuilds word * k and searches it for each k."
        ),
        cx="O(n * w) time, O(n) space",
        brute_cx="O(n^2) time-ish - keep growing word * k and re-searching sequence",
        brute=r"""
# BRUTE FORCE: O(n^2) time-ish - keep growing word * k and re-searching sequence
def max_repeating(sequence, word):
    k = 0
    while word * (k + 1) in sequence:
        k += 1
    return k
""",
        solution=r"""
# OPTIMISED: O(n * w) time, O(n) space
# Idea: DP over end positions: chain consecutive matches
def max_repeating(sequence, word):
    n, w = len(sequence), len(word)
    dp = [0] * (n + 1)
    best = 0
    for i in range(w, n + 1):
        if sequence[i - w : i] == word:
            dp[i] = dp[i - w] + 1
            best = max(best, dp[i])
    return best
""",
    ),
    # ---- Remove All Occurrences of a Substring (LeetCode 1910) ----
    dict(
        title="Remove All Occurrences of a Substring",
        diff="M",
        lc=1910,
        slug="remove-all-occurrences-of-a-substring",
        prompt=(
            "While part occurs in s, remove its LEFTMOST occurrence (the pieces on both sides join together). "
            "Return the final string."
        ),
        sig="def remove_occurrences(s: str, part: str) -> str:",
        fn="remove_occurrences",
        tests=[
            (("daabcbaabcbc", "abc"), "dab"),
            (("axxxxyyyyb", "xy"), "ab"),
            (("aaa", "a"), ""),
            (("abc", "abcd"), "abc"),
        ],
        hints=[
            "Removing an occurrence can create a NEW occurrence out of the characters on both sides of it.",
            "Simulating with find + slicing costs O(n) per removal. Can you remove while scanning once?",
            "Push characters on a stack; whenever the top len(part) characters spell part, pop them.",
        ],
        pattern="Stack that eagerly cancels a pattern",
        explain=(
            "Process the string left to right with a stack of surviving characters. After pushing a character, if "
            "the last len(part) stack entries equal part, that is exactly the leftmost occurrence in the current "
            "string, so pop it - any occurrence created by the join is detected at the next push because the "
            "characters before it are already on the stack. This reproduces the leftmost-first removal order in a "
            "single pass. The brute force literally finds and deletes the leftmost occurrence repeatedly."
        ),
        cx="O(n * |part|) time, O(n) space",
        brute_cx="O(n^2 / |part|) time - find and cut the leftmost occurrence, repeat",
        brute=r"""
# BRUTE FORCE: O(n^2 / |part|) time - find and cut the leftmost occurrence, repeat
def remove_occurrences(s, part):
    while part in s:
        i = s.index(part)
        s = s[:i] + s[i + len(part) :]
    return s
""",
        solution=r"""
# OPTIMISED: O(n * |part|) time, O(n) space
# Idea: Stack that eagerly cancels a pattern
def remove_occurrences(s, part):
    stack = []
    p = len(part)
    for ch in s:
        stack.append(ch)
        if len(stack) >= p and "".join(stack[-p:]) == part:
            del stack[-p:]
    return "".join(stack)
""",
    ),
    # ---- Count Vowel Substrings of a String (LeetCode 2062) ----
    dict(
        title="Count Vowel Substrings of a String",
        diff="E",
        lc=2062,
        slug="count-vowel-substrings-of-a-string",
        prompt=(
            "A vowel substring contains ONLY vowels (a, e, i, o, u) and has all five of them at least once. Return "
            "the number of vowel substrings of word."
        ),
        sig="def count_vowel_substrings(word: str) -> int:",
        fn="count_vowel_substrings",
        tests=[
            (("aeiouu",), 2),
            (("unicornarihan",), 0),
            (("cuaieuouac",), 7),
            (("aeiou",), 1),
        ],
        hints=[
            "A consonant breaks everything: a valid substring lives inside one maximal run of vowels.",
            "For a fixed right end i, the substring [start, i] is valid iff it contains all five vowels.",
            "Remember the last index of each vowel in the current run; valid starts are start..min(last positions).",
        ],
        pattern="Last-occurrence tracking per right end",
        explain=(
            "Fix the right end i inside a vowel run that began at index start. A start s is valid iff the window "
            "[s, i] holds all five vowels, i.e. s <= the earliest of the five most recent vowel positions. So the "
            "number of valid starts for this i is min(last) - start + 1 when all five were seen in the run, "
            "otherwise zero. A consonant resets the five positions and moves start forward. One pass, O(1) work per "
            "character. The brute force checks every substring."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^3) time - test every substring for the two conditions",
        brute=r"""
# BRUTE FORCE: O(n^3) time - test every substring for the two conditions
def count_vowel_substrings(word):
    vowels = set("aeiou")
    count = 0
    for i in range(len(word)):
        for j in range(i + 1, len(word) + 1):
            sub = set(word[i:j])
            if sub == vowels:
                count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Last-occurrence tracking per right end
def count_vowel_substrings(word):
    vowels = "aeiou"
    last = {v: -1 for v in vowels}
    start = 0
    total = 0
    for i, ch in enumerate(word):
        if ch not in vowels:
            last = {v: -1 for v in vowels}
            start = i + 1
            continue
        last[ch] = i
        low = min(last.values())
        if low >= start:
            total += low - start + 1
    return total
""",
    ),
    # ---- Check if a Parentheses String Can Be Valid (LeetCode 2116) ----
    dict(
        title="Check if a Parentheses String Can Be Valid",
        diff="M",
        lc=2116,
        slug="check-if-a-parentheses-string-can-be-valid",
        prompt=(
            "s consists of '(' and ')'. locked has the same length: if locked[i] is '1' the character s[i] is "
            "fixed, if it is '0' you may change s[i] to either bracket. Return true if some choice makes s a valid "
            "parentheses string."
        ),
        sig="def can_be_valid(s: str, locked: str) -> bool:",
        fn="can_be_valid",
        tests=[
            (("))()))", "010100"), True),
            (("()()", "0000"), True),
            ((")", "0"), False),
            (("()", "11"), True),
            (("(", "0"), False),
        ],
        hints=[
            "An odd length can never be balanced - return false at once.",
            "Scan left to right treating every unlocked position as '(' (the best case for staying non-negative).",
            (
                "Then scan right to left treating every unlocked position as ')' . If neither scan's balance ever "
                "goes negative, it works."
            ),
        ],
        pattern="Two greedy passes (best case from each side)",
        explain=(
            "A string is valid iff (a) its length is even and (b) every prefix has at least as many '(' as ')' AND "
            "every suffix has at least as many ')' as '('. Wildcards help the left-to-right check most when they "
            "act as '(' and the right-to-left check most when they act as ')'. If both optimistic scans survive, we "
            "can always complete the string: the wildcard count is exactly enough to fix the balance given the even "
            "length. If either scan fails, even the best case fails. The brute force tries all 2^f assignments of "
            "the f wildcards."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(2^f * n) time - try every way to fill the f changeable positions",
        brute=r"""
# BRUTE FORCE: O(2^f * n) time - try every way to fill the f changeable positions
def can_be_valid(s, locked):
    free = [i for i in range(len(s)) if locked[i] == "0"]
    for combo in itertools.product("()", repeat=len(free)):
        chars = list(s)
        for i, ch in zip(free, combo):
            chars[i] = ch
        bal = 0
        for ch in chars:
            bal += 1 if ch == "(" else -1
            if bal < 0:
                break
        else:
            if bal == 0:
                return True
    return False
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two greedy passes (best case from each side)
def can_be_valid(s, locked):
    n = len(s)
    if n % 2:
        return False
    bal = 0
    for i in range(n):
        bal += 1 if locked[i] == "0" or s[i] == "(" else -1
        if bal < 0:
            return False
    bal = 0
    for i in range(n - 1, -1, -1):
        bal += 1 if locked[i] == "0" or s[i] == ")" else -1
        if bal < 0:
            return False
    return True
""",
    ),
    # ---- Find Substring With Given Hash Value (LeetCode 2156) ----
    dict(
        title="Find Substring With Given Hash Value",
        diff="H",
        lc=2156,
        slug="find-substring-with-given-hash-value",
        prompt=(
            "The hash of a string t of length k is (val(t[0]) * p^0 + val(t[1]) * p^1 + ... + val(t[k-1]) * "
            "p^(k-1)) mod m, where val('a') = 1 ... val('z') = 26. Given s, power = p, modulo = m, k and "
            "hash_value, return the FIRST substring of s of length k whose hash equals hash_value (one is "
            "guaranteed to exist)."
        ),
        sig="def sub_str_hash(s: str, power: int, modulo: int, k: int, hash_value: int) -> str:",
        fn="sub_str_hash",
        tests=[
            (("leetcode", 7, 20, 2, 0), "ee"),
            (("fbxzaad", 31, 100, 3, 32), "fbx"),
            (("a", 1, 2, 1, 1), "a"),
            (("abc", 2, 10, 2, 5), "ab"),
        ],
        hints=[
            "Computing each window's hash from scratch costs O(k) per window - O(n * k) overall.",
            "Neighbouring windows share k - 1 characters: derive the hash of the window at i from the one at i + 1.",
            (
                "Scan from the RIGHT: h(i) = val(s[i]) + p * (h(i+1) - val(s[i+k]) * p^(k-1)); remember the "
                "smallest matching i."
            ),
        ],
        pattern="Rolling hash scanned right-to-left (the highest power leaves first)",
        explain=(
            "In this hash the FIRST character has the lowest power. Sliding the window one step to the LEFT "
            "therefore removes the last character (highest power p^(k-1)), multiplies the rest by p (shifting every "
            "power up by one) and adds the new first character with power 0: h(i) = val(s[i]) + p * (h(i+1) - "
            "val(s[i+k]) * p^(k-1)) mod m. Starting from the hash of the last window and moving left, each step is "
            "O(1); the last match we see is the leftmost. Python's % keeps the intermediate value non-negative. The "
            "brute force recomputes every window's hash from scratch."
        ),
        cx="O(n) time, O(1) extra space",
        brute_cx="O(n * k) time - compute every window's hash from scratch",
        brute=r"""
# BRUTE FORCE: O(n * k) time - compute every window's hash from scratch
def sub_str_hash(s, power, modulo, k, hash_value):
    for i in range(len(s) - k + 1):
        h = 0
        for j in range(k):
            h += (ord(s[i + j]) - 96) * pow(power, j, modulo)
        if h % modulo == hash_value:
            return s[i : i + k]
    return ""
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) extra space
# Idea: Rolling hash scanned right-to-left (the highest power leaves first)
def sub_str_hash(s, power, modulo, k, hash_value):
    n = len(s)
    top = pow(power, k - 1, modulo)
    h = 0
    for i in range(n - 1, n - k - 1, -1):
        h = (h * power + (ord(s[i]) - 96)) % modulo
    ans = n - k if h == hash_value else -1
    for i in range(n - k - 1, -1, -1):
        h = ((h - (ord(s[i + k]) - 96) * top) * power + (ord(s[i]) - 96)) % modulo
        if h == hash_value:
            ans = i
    return s[ans : ans + k]
""",
    ),
    # ---- Decode the Slanted Ciphertext (LeetCode 2075) ----
    dict(
        title="Decode the Slanted Ciphertext",
        diff="M",
        lc=2075,
        slug="decode-the-slanted-ciphertext",
        prompt=(
            "A text was written along diagonals (top-left to bottom-right, one diagonal after another) into a "
            "matrix with `rows` rows, padded with spaces to fill it, and then encoded_text was read off row by row. "
            "Recover the original text (it has no trailing spaces, but may have leading ones)."
        ),
        sig="def decode_ciphertext(encoded_text: str, rows: int) -> str:",
        fn="decode_ciphertext",
        tests=[
            (("ch   ie   pr", 3), "cipher"),
            (("iveo    eed   l te   olc", 4), "i love leetcode"),
            (("coding", 1), "coding"),
            (("a  b", 2), "ab"),
            (("   b", 2), " b"),
        ],
        hints=[
            "The matrix has cols = len(encoded_text) / rows columns; row r is encoded_text[r * cols : (r + 1) * cols].",
            "Diagonal number c starts at (0, c) and visits (1, c + 1), (2, c + 2), ... until it leaves the matrix.",
            "Read the diagonals for c = 0, 1, 2, ... in order, concatenate, and strip the trailing spaces.",
        ],
        pattern="Matrix reconstruction and diagonal traversal with index arithmetic",
        explain=(
            "Decoding just reverses the writing process: lay the string out row by row in a rows x cols grid, then "
            "walk the diagonals that start in the top row, from the leftmost column to the rightmost. The cell (r, "
            "c + r) lives at index r * cols + c + r of the encoded string, so no matrix is needed. Finally the "
            "padding spaces at the end are removed with rstrip (leading spaces belong to the text). The brute force "
            "builds the matrix explicitly."
        ),
        cx="O(n) time, O(n) output space",
        brute_cx="O(n) time and an extra rows x cols matrix - build the grid, then walk it",
        brute=r"""
# BRUTE FORCE: O(n) time and an extra rows x cols matrix - build the grid, then walk it
def decode_ciphertext(encoded_text, rows):
    cols = len(encoded_text) // rows
    grid = [encoded_text[r * cols : (r + 1) * cols] for r in range(rows)]
    out = []
    for c in range(cols):
        r = 0
        while r < rows and c + r < cols:
            out.append(grid[r][c + r])
            r += 1
    return "".join(out).rstrip()
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) output space
# Idea: Matrix reconstruction and diagonal traversal with index arithmetic
def decode_ciphertext(encoded_text, rows):
    cols = len(encoded_text) // rows
    out = []
    for c in range(cols):
        for r in range(min(rows, cols - c)):
            out.append(encoded_text[r * cols + c + r])
    return "".join(out).rstrip()
""",
    ),
]
