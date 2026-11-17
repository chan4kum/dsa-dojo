"""more Prefix Sums problems (batch 5) - part of the problem bank for the "prefix_sums" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
The core trick: precompute running totals once, then any range total is a subtraction: sum(l..r) = P[r+1] - P[l].
"""

PROBLEMS = [
    # ---- Maximum Sum of Two Non-Overlapping Subarrays (LeetCode 1031) ----
    dict(
        title="Maximum Sum of Two Non-Overlapping Subarrays",
        diff="M",
        lc=1031,
        slug="maximum-sum-of-two-non-overlapping-subarrays",
        prompt=(
            "Return the maximum total of two non-overlapping subarrays of lengths first_len and second_len. The "
            "first-length one may come before or after the second-length one."
        ),
        sig="def max_sum_two_no_overlap(nums: List[int], first_len: int, second_len: int) -> int:",
        fn="max_sum_two_no_overlap",
        tests=[
            (([0, 6, 5, 2, 2, 5, 1, 9, 4], 1, 2), 20),
            (([3, 8, 1, 3, 2, 1, 8, 9, 0], 3, 2), 29),
            (([2, 1, 5, 6, 0, 9, 5, 0, 3, 8], 4, 3), 31),
            (([1, 2], 1, 1), 3),
        ],
        hints=[
            "With prefix sums every subarray sum is O(1).",
            (
                "Sweep a right end i. The second block is the window of length B ending at i; the first block can "
                "be ANY window of length A that ends at or before i - B."
            ),
            (
                "Keep the best A-window seen so far (and symmetrically the best B-window before an A-window), and "
                "try both orders at every i."
            ),
        ],
        pattern="Prefix sums + best-so-far on one side",
        explain=(
            "Fixing one block as the window ending at i leaves a clean question for the other block: its best "
            "placement entirely to the left, which is a running maximum."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - try every pair of start positions",
        brute=r"""
# BRUTE FORCE: O(n^2) time - try every pair of start positions
def max_sum_two_no_overlap(nums, first_len, second_len):
    n, best = len(nums), 0
    for i in range(n - first_len + 1):
        for j in range(n - second_len + 1):
            if i + first_len <= j or j + second_len <= i:  # the two blocks do not overlap
                best = max(best, sum(nums[i : i + first_len]) + sum(nums[j : j + second_len]))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Prefix sums + best-so-far on one side
def max_sum_two_no_overlap(nums, first_len, second_len):
    prefix = [0]

    for x in nums:
        prefix.append(prefix[-1] + x)

    best_a = best_b = result = 0

    for i in range(first_len + second_len, len(prefix)):
        best_a = max(
            best_a, prefix[i - second_len] - prefix[i - second_len - first_len]
        )  # A ends before B's window
        best_b = max(
            best_b, prefix[i - first_len] - prefix[i - first_len - second_len]
        )  # B ends before A's window
        window_b = prefix[i] - prefix[i - second_len]
        window_a = prefix[i] - prefix[i - first_len]
        result = max(result, best_a + window_b, best_b + window_a)

    return result
""",
    ),
    # ---- Can Make Palindrome from Substring (LeetCode 1177) ----
    dict(
        title="Can Make Palindrome from Substring",
        diff="M",
        lc=1177,
        slug="can-make-palindrome-from-substring",
        prompt=(
            "For each query [left, right, k]: you may rearrange the letters of s[left..right] and then replace at "
            "most k letters with any letters. Can the substring become a palindrome? Return one boolean per query."
        ),
        sig="def can_make_pali_queries(s: str, queries: List[List[int]]) -> List[bool]:",
        fn="can_make_pali_queries",
        tests=[
            (("abcda", [[3, 3, 0], [1, 2, 0], [0, 3, 1], [0, 3, 2], [0, 4, 1]]), [True, False, False, True, True]),
            (("lyb", [[0, 1, 0], [2, 2, 1]]), [False, True]),
            (("aabb", [[0, 3, 0]]), [True]),
        ],
        hints=[
            (
                "After rearranging, only letters with an ODD count are a problem: every pair of equal letters is "
                "already fine."
            ),
            "With o letters of odd count you must change floor(o / 2) of them. So the answer is o // 2 <= k.",
            (
                "Store, for each prefix, a bitmask of which letters have odd count so far; the odd letters of a "
                "substring are prefix[r + 1] XOR prefix[l]."
            ),
        ],
        pattern="Prefix parity bitmask (XOR)",
        explain=(
            "XOR cancels the letters that appear an even number of times between two prefixes, leaving a mask of "
            "exactly the odd ones; counting its bits is O(1)."
        ),
        cx="O(n + q) time",
        brute_cx="O(q * n) time - count letters inside each substring",
        brute=r"""
# BRUTE FORCE: O(q * n) time - count letters inside each substring
def can_make_pali_queries(s, queries):
    answer = []
    for left, right, k in queries:
        counts = Counter(s[left : right + 1])
        odd = sum(1 for c in counts.values() if c % 2)
        answer.append(odd // 2 <= k)
    return answer
""",
        solution=r"""
# OPTIMISED: O(n + q) time
# Idea: Prefix parity bitmask (XOR)
def can_make_pali_queries(s, queries):
    prefix = [0]

    for ch in s:
        prefix.append(prefix[-1] ^ (1 << (ord(ch) - 97)))  # flip this letter's parity bit

    answer = []

    for left, right, k in queries:
        odd = bin(prefix[right + 1] ^ prefix[left]).count("1")
        answer.append(odd // 2 <= k)

    return answer
""",
    ),
    # ---- Matrix Block Sum (LeetCode 1314) ----
    dict(
        title="Matrix Block Sum",
        diff="M",
        lc=1314,
        slug="matrix-block-sum",
        prompt=(
            "For each cell (i, j) return the sum of all cells (r, c) with i - k <= r <= i + k and j - k <= c <= j + "
            "k that lie inside the matrix."
        ),
        sig="def matrix_block_sum(mat: List[List[int]], k: int) -> List[List[int]]:",
        fn="matrix_block_sum",
        tests=[
            (([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 1), [[12, 21, 16], [27, 45, 33], [24, 39, 28]]),
            (([[1, 2, 3], [4, 5, 6], [7, 8, 9]], 2), [[45, 45, 45], [45, 45, 45], [45, 45, 45]]),
            (([[5]], 1), [[5]]),
        ],
        hints=[
            "Each answer is the sum of a rectangle, clamped to the matrix borders.",
            "Build a 2D prefix table P where P[i][j] is the sum of the top-left i x j block.",
            (
                "Rectangle sum = P[r2][c2] - P[r1][c2] - P[r2][c1] + P[r1][c1] (inclusion-exclusion), with the "
                "corners clamped."
            ),
        ],
        pattern="2D prefix sums",
        explain=(
            "Inclusion-exclusion lets any rectangle be read from four precomputed corners, so every cell costs O(1) "
            "no matter how large k is."
        ),
        cx="O(m * n) time and space",
        brute_cx="O(m * n * k^2) time - add up each block cell by cell",
        brute=r"""
# BRUTE FORCE: O(m * n * k^2) time - add up each block cell by cell
def matrix_block_sum(mat, k):
    m, n = len(mat), len(mat[0])

    return [
        [
            sum(
                mat[r][c]
                for r in range(max(0, i - k), min(m, i + k + 1))
                for c in range(max(0, j - k), min(n, j + k + 1))
            )
            for j in range(n)
        ]
        for i in range(m)
    ]
""",
        solution=r"""
# OPTIMISED: O(m * n) time and space
# Idea: 2D prefix sums
def matrix_block_sum(mat, k):
    m, n = len(mat), len(mat[0])
    prefix = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m):
        for j in range(n):
            prefix[i + 1][j + 1] = mat[i][j] + prefix[i][j + 1] + prefix[i + 1][j] - prefix[i][j]

    result = [[0] * n for _ in range(m)]

    for i in range(m):
        for j in range(n):
            r1, c1 = max(0, i - k), max(0, j - k)
            r2, c2 = min(m, i + k + 1), min(n, j + k + 1)
            result[i][j] = prefix[r2][c2] - prefix[r1][c2] - prefix[r2][c1] + prefix[r1][c1]

    return result
""",
    ),
    # ---- Find the Longest Substring Containing Vowels in Even Counts (LeetCode 1371) ----
    dict(
        title="Find the Longest Substring Containing Vowels in Even Counts",
        diff="M",
        lc=1371,
        slug="find-the-longest-substring-containing-vowels-in-even-counts",
        prompt=(
            "Return the length of the longest substring of s in which each of the vowels a, e, i, o, u appears an "
            "even number of times (zero counts as even)."
        ),
        sig="def find_the_longest_substring(s: str) -> int:",
        fn="find_the_longest_substring",
        tests=[
            (("eleetminicoworoep",), 13),
            (("leetcodeisgreat",), 5),
            (("bcbcbc",), 6),
            (("a",), 0),
        ],
        hints=[
            "Only the PARITY of each vowel's count matters: five bits describe the state.",
            (
                "A substring has all-even vowels exactly when its two ends have the same parity mask in the prefix "
                "sequence."
            ),
            (
                "Store the FIRST index where each mask appeared; at every position the best substring ends here and "
                "starts after that first index."
            ),
        ],
        pattern="Prefix parity mask + first-occurrence map",
        explain=(
            "Equal masks at two positions mean every vowel's count changed by an even amount in between, and the "
            "earliest equal mask gives the longest span."
        ),
        cx="O(n) time, O(32) space",
        brute_cx="O(n^2) time - count vowels in every substring",
        brute=r"""
# BRUTE FORCE: O(n^2) time - count vowels in every substring
def find_the_longest_substring(s):
    best = 0

    for i in range(len(s)):
        counts = dict.fromkeys("aeiou", 0)
        for j in range(i, len(s)):
            if s[j] in counts:
                counts[s[j]] += 1
            if all(c % 2 == 0 for c in counts.values()):
                best = max(best, j - i + 1)

    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(32) space
# Idea: Prefix parity mask + first-occurrence map
def find_the_longest_substring(s):
    bit = {"a": 1, "e": 2, "i": 4, "o": 8, "u": 16}
    first = {0: -1}  # mask -> earliest index where it was seen (-1 = before the string)
    mask = best = 0

    for i, ch in enumerate(s):
        mask ^= bit.get(ch, 0)
        if mask in first:
            best = max(best, i - first[mask])
        else:
            first[mask] = i

    return best
""",
    ),
    # ---- Maximum Number of Non-Overlapping Subarrays With Sum Equals Target (LeetCode 1546) ----
    dict(
        title="Maximum Number of Non-Overlapping Subarrays With Sum Equals Target",
        diff="M",
        lc=1546,
        slug="maximum-number-of-non-overlapping-subarrays-with-sum-equals-target",
        prompt="Return the maximum number of non-empty, non-overlapping subarrays whose sum equals target.",
        sig="def max_non_overlapping(nums: List[int], target: int) -> int:",
        fn="max_non_overlapping",
        tests=[
            (([1, 1, 1, 1, 1], 2), 2),
            (([-1, 3, 5, 1, 4, 2, -9], 6), 2),
            (([0, 0, 0], 0), 3),
            (([1], 5), 0),
        ],
        hints=[
            "A subarray ending at i has sum target when prefix[i] - target equals an EARLIER prefix value.",
            "Greedy: the moment you can close a subarray, do it - ending earlier never hurts.",
            (
                "Keep a set of prefix sums since the last cut. When prefix - target is in the set, count one and "
                "reset the set to just {prefix}."
            ),
        ],
        pattern="Greedy + prefix-sum set with reset",
        explain=(
            "Taking the earliest possible end leaves the most room for later subarrays; resetting the set after "
            "each cut guarantees the next subarray starts after the previous one ended."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - DP over end positions",
        brute=r"""
# BRUTE FORCE: O(n^2) time - DP over end positions
def max_non_overlapping(nums, target):
    n = len(nums)
    best = [0] * (n + 1)  # best[i]: answer using only the first i numbers

    for i in range(1, n + 1):
        best[i] = best[i - 1]
        total = 0
        for j in range(i, 0, -1):  # subarray nums[j-1 .. i-1]
            total += nums[j - 1]
            if total == target:
                best[i] = max(best[i], best[j - 1] + 1)

    return best[n]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Greedy + prefix-sum set with reset
def max_non_overlapping(nums, target):
    seen, prefix, count = {0}, 0, 0

    for x in nums:
        prefix += x
        if prefix - target in seen:  # a subarray ending here sums to target
            count += 1
            seen = {0}  # cut here: nothing may start before this point
            prefix = 0
        else:
            seen.add(prefix)

    return count
""",
    ),
    # ---- Plates Between Candles (LeetCode 2055) ----
    dict(
        title="Plates Between Candles",
        diff="M",
        lc=2055,
        slug="plates-between-candles",
        prompt=(
            "s is made of '*' (plates) and '|' (candles). For each query [l, r], count the plates that lie between "
            "the FIRST and LAST candle inside s[l..r] (0 if the range has fewer than two candles)."
        ),
        sig="def plates_between_candles(s: str, queries: List[List[int]]) -> List[int]:",
        fn="plates_between_candles",
        tests=[
            (("**|**|***|", [[2, 5], [5, 9]]), [2, 3]),
            (("***|**|*****|**||**|*", [[1, 17], [4, 5], [14, 17], [5, 11], [15, 16]]), [9, 0, 0, 0, 0]),
            (("|*|", [[0, 2]]), [1]),
        ],
        hints=[
            "Plates between two positions = a prefix-sum subtraction.",
            "The first candle at or after l and the last candle at or before r define the counted range.",
            (
                "Precompute prefix plate counts, next_candle[i] (nearest candle at or to the right) and "
                "prev_candle[i] (nearest at or to the left)."
            ),
        ],
        pattern="Prefix sums + nearest-candle lookup tables",
        explain=(
            "Three O(n) tables turn every query into O(1): snap l right and r left to the nearest candles, then "
            "subtract plate prefixes."
        ),
        cx="O(n + q) time",
        brute_cx="O(q * n) time - slice and count for every query",
        brute=r"""
# BRUTE FORCE: O(q * n) time - slice and count for every query
def plates_between_candles(s, queries):
    answer = []

    for left, right in queries:
        part = s[left : right + 1]
        if part.count("|") < 2:
            answer.append(0)
        else:
            inner = part[part.index("|") : part.rindex("|") + 1]
            answer.append(inner.count("*"))

    return answer
""",
        solution=r"""
# OPTIMISED: O(n + q) time
# Idea: Prefix sums + nearest-candle lookup tables
def plates_between_candles(s, queries):
    n = len(s)
    plates = [0] * (n + 1)

    for i, ch in enumerate(s):
        plates[i + 1] = plates[i] + (ch == "*")

    next_candle, prev_candle = [n] * n, [-1] * n
    last = -1

    for i in range(n):
        if s[i] == "|":
            last = i
        prev_candle[i] = last

    nxt = n

    for i in range(n - 1, -1, -1):
        if s[i] == "|":
            nxt = i
        next_candle[i] = nxt

    answer = []

    for left, right in queries:
        a, b = next_candle[left], prev_candle[right]  # snap inwards to real candles
        answer.append(plates[b] - plates[a + 1] if a < b else 0)

    return answer
""",
    ),
    # ---- Number of Ways to Split Array (LeetCode 2270) ----
    dict(
        title="Number of Ways to Split Array",
        diff="M",
        lc=2270,
        slug="number-of-ways-to-split-array",
        prompt=(
            "A split index i (0 <= i < n - 1) is valid when the sum of the first i + 1 elements is at least the sum "
            "of the remaining elements. Return the number of valid splits."
        ),
        sig="def ways_to_split_array(nums: List[int]) -> int:",
        fn="ways_to_split_array",
        tests=[
            (([10, 4, -8, 7],), 2),
            (([2, 3, 1, 0],), 2),
            (([1, 1],), 1),
            (([-2, -1],), 0),
        ],
        hints=[
            "The right sum is just total - left sum.",
            "Compute the total once.",
            "Walk i from 0 to n - 2 keeping a running left sum and compare it with total - left.",
        ],
        pattern="Running prefix sum against the total",
        explain=(
            "Knowing the total, the right part never needs to be summed: it is the total minus what you have "
            "already accumulated."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - re-sum both sides at every split",
        brute=r"""
# BRUTE FORCE: O(n^2) time - re-sum both sides at every split
def ways_to_split_array(nums):
    return sum(1 for i in range(len(nums) - 1) if sum(nums[: i + 1]) >= sum(nums[i + 1 :]))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Running prefix sum against the total
def ways_to_split_array(nums):
    total, left, ways = sum(nums), 0, 0
    for x in nums[:-1]:  # the right part must keep at least one element
        left += x
        if left >= total - left:
            ways += 1
    return ways
""",
    ),
    # ---- Longest Subsequence With Limited Sum (LeetCode 2389) ----
    dict(
        title="Longest Subsequence With Limited Sum",
        diff="E",
        lc=2389,
        slug="longest-subsequence-with-limited-sum",
        prompt=(
            "For each query q, return the maximum length of a subsequence of nums whose sum is at most q (a "
            "subsequence keeps relative order, but only the chosen values matter for the sum)."
        ),
        sig="def answer_queries(nums: List[int], queries: List[int]) -> List[int]:",
        fn="answer_queries",
        tests=[
            (([4, 5, 2, 1], [3, 10, 21]), [2, 3, 4]),
            (([2, 3, 4, 5], [1]), [0]),
            (([1, 1, 1], [0, 2, 3]), [0, 2, 3]),
        ],
        hints=[
            "Since order does not affect the sum, to fit the MOST numbers you should pick the smallest ones.",
            "Sort nums and build prefix sums: prefix[k] is the cost of the k smallest numbers.",
            (
                "For a query q the answer is the largest k with prefix[k] <= q: bisect_right on the prefix list, "
                "minus one."
            ),
        ],
        pattern="Sort + prefix sums + binary search",
        explain="Sorted prefix sums are non-decreasing, so 'how many smallest numbers fit in q' is a single bisect.",
        cx="O((n + q) log n) time",
        brute_cx="O(q * n) time - greedily add the smallest numbers for each query",
        brute=r"""
# BRUTE FORCE: O(q * n) time - greedily add the smallest numbers for each query
def answer_queries(nums, queries):
    ordered = sorted(nums)
    answer = []

    for q in queries:
        total = count = 0
        for x in ordered:
            if total + x > q:
                break
            total += x
            count += 1
        answer.append(count)

    return answer
""",
        solution=r"""
# OPTIMISED: O((n + q) log n) time
# Idea: Sort + prefix sums + binary search
def answer_queries(nums, queries):
    prefix = list(itertools.accumulate(sorted(nums)))  # cost of the 1, 2, 3... smallest numbers
    return [bisect.bisect_right(prefix, q) for q in queries]
""",
    ),
    # ---- Count Vowel Strings in Ranges (LeetCode 2559) ----
    dict(
        title="Count Vowel Strings in Ranges",
        diff="M",
        lc=2559,
        slug="count-vowel-strings-in-ranges",
        prompt=(
            "For each query [l, r] return how many words in words[l..r] both START and END with a vowel (a, e, i, "
            "o, u)."
        ),
        sig="def vowel_strings(words: List[str], queries: List[List[int]]) -> List[int]:",
        fn="vowel_strings",
        tests=[
            ((["aba", "bcb", "ece", "aa", "e"], [[0, 2], [1, 4], [1, 1]]), [2, 3, 0]),
            ((["a", "e", "i"], [[0, 2], [0, 1], [2, 2]]), [3, 2, 1]),
            ((["bcd"], [[0, 0]]), [0]),
        ],
        hints=[
            "Turn each word into 1 (starts and ends with a vowel) or 0.",
            "Now every query is a range sum over a 0/1 array.",
            "Prefix sums: answer = prefix[r + 1] - prefix[l].",
        ],
        pattern="Prefix sums over a 0/1 indicator",
        explain="Pre-classifying each word once makes each query a subtraction instead of a rescan.",
        cx="O(n + q) time",
        brute_cx="O(q * n) time - check every word in every range",
        brute=r"""
# BRUTE FORCE: O(q * n) time - check every word in every range
def vowel_strings(words, queries):
    good = [w[0] in "aeiou" and w[-1] in "aeiou" for w in words]
    return [sum(good[left : right + 1]) for left, right in queries]
""",
        solution=r"""
# OPTIMISED: O(n + q) time
# Idea: Prefix sums over a 0/1 indicator
def vowel_strings(words, queries):
    prefix = [0]
    for w in words:
        prefix.append(prefix[-1] + (w[0] in "aeiou" and w[-1] in "aeiou"))
    return [prefix[right + 1] - prefix[left] for left, right in queries]
""",
    ),
    # ---- Find the Score of All Prefixes of an Array (LeetCode 2640) ----
    dict(
        title="Find the Score of All Prefixes of an Array",
        diff="M",
        lc=2640,
        slug="find-the-score-of-all-prefixes-of-an-array",
        prompt=(
            "The conversion array is conver[i] = nums[i] + max(nums[0..i]). The score of a prefix is the sum of "
            "conver over that prefix. Return the score of every prefix nums[0..i]."
        ),
        sig="def find_prefix_score(nums: List[int]) -> List[int]:",
        fn="find_prefix_score",
        tests=[
            (([2, 3, 7, 5, 10],), [4, 10, 24, 36, 56]),
            (([1, 1, 2, 4, 8, 16],), [2, 4, 8, 16, 32, 64]),
            (([5],), [10]),
        ],
        hints=[
            "conver[i] needs the maximum so far - keep it as a running value.",
            "score[i] = score[i - 1] + conver[i].",
            "One pass: update the running max, compute conver, add to the running score, append.",
        ],
        pattern="Running max + running prefix sum",
        explain="Both quantities are cumulative, so each element only extends the previous state.",
        cx="O(n) time",
        brute_cx="O(n^2) time - recompute the max and sum for each prefix",
        brute=r"""
# BRUTE FORCE: O(n^2) time - recompute the max and sum for each prefix
def find_prefix_score(nums):
    scores = []
    for i in range(len(nums)):
        scores.append(sum(nums[j] + max(nums[: j + 1]) for j in range(i + 1)))
    return scores
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Running max + running prefix sum
def find_prefix_score(nums):
    best = score = 0
    result = []
    for x in nums:
        best = max(best, x)
        score += x + best
        result.append(score)
    return result
""",
    ),
    # ---- Check if All the Integers in a Range Are Covered (LeetCode 1893) ----
    dict(
        title="Check if All the Integers in a Range Are Covered",
        diff="E",
        lc=1893,
        slug="check-if-all-the-integers-in-a-range-are-covered",
        prompt=(
            "ranges holds inclusive intervals [start, end]. Return True if every integer from left to right "
            "(inclusive) lies in at least one of the intervals."
        ),
        sig="def is_covered(ranges: List[List[int]], left: int, right: int) -> bool:",
        fn="is_covered",
        tests=[
            (([[1, 2], [3, 4], [5, 6]], 2, 5), True),
            (([[1, 10], [10, 20]], 21, 21), False),
            (([[1, 5]], 1, 5), True),
            (([[2, 3]], 1, 3), False),
        ],
        hints=[
            "Values are small (1..50), so you can mark them.",
            "Add +1 at each interval's start and -1 just after its end in a difference array.",
            "Prefix-sum it; every integer in [left, right] must have a count of at least 1.",
        ],
        pattern="Difference array coverage count",
        explain=(
            "The prefix sum of the difference array is the number of intervals covering each integer, so 'covered' "
            "means 'count > 0' on the whole range."
        ),
        cx="O(n + max) time",
        brute_cx="O(n * range) time - test each integer against every interval",
        brute=r"""
# BRUTE FORCE: O(n * range) time - test each integer against every interval
def is_covered(ranges, left, right):
    return all(any(a <= x <= b for a, b in ranges) for x in range(left, right + 1))
""",
        solution=r"""
# OPTIMISED: O(n + max) time
# Idea: Difference array coverage count
def is_covered(ranges, left, right):
    size = max(right, max(b for _, b in ranges)) + 2
    diff = [0] * size

    for a, b in ranges:
        diff[a] += 1
        diff[b + 1] -= 1

    cover = 0

    for x in range(right + 1):
        cover += diff[x]
        if x >= left and cover == 0:
            return False

    return True
""",
    ),
    # ---- Number of Submatrices That Sum to Target (LeetCode 1074) ----
    dict(
        title="Number of Submatrices That Sum to Target",
        diff="H",
        lc=1074,
        slug="number-of-submatrices-that-sum-to-target",
        prompt=(
            "Return the number of non-empty submatrices (contiguous rectangles) of the matrix whose elements sum to "
            "target."
        ),
        sig="def num_submatrix_sum_target(matrix: List[List[int]], target: int) -> int:",
        fn="num_submatrix_sum_target",
        tests=[
            (([[0, 1, 0], [1, 1, 1], [0, 1, 0]], 0), 4),
            (([[1, -1], [-1, 1]], 0), 5),
            (([[904]], 0), 0),
            (([[2]], 2), 1),
        ],
        hints=[
            "Fixing the top and bottom rows turns the rectangle into a 1D problem over columns.",
            "Squash those rows into one array of column sums; count subarrays with sum == target.",
            (
                "Subarray count with a target sum: prefix sums + a dictionary of how often each prefix value has "
                "appeared (like Subarray Sum Equals K)."
            ),
        ],
        pattern="Reduce 2D to 1D (row pairs) + prefix-sum hashmap",
        explain=(
            "Each pair of rows defines a strip; counting rectangles in the strip is exactly the classic 'subarrays "
            "summing to k' problem, solved in O(columns)."
        ),
        cx="O(m^2 * n) time, O(n) space",
        brute_cx="O(m^2 * n^2) time - check every rectangle with a 2D prefix table",
        brute=r"""
# BRUTE FORCE: O(m^2 * n^2) time - check every rectangle with a 2D prefix table
def num_submatrix_sum_target(matrix, target):
    m, n = len(matrix), len(matrix[0])
    prefix = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m):
        for j in range(n):
            prefix[i + 1][j + 1] = matrix[i][j] + prefix[i][j + 1] + prefix[i + 1][j] - prefix[i][j]

    count = 0

    for r1 in range(m):
        for r2 in range(r1, m):
            for c1 in range(n):
                for c2 in range(c1, n):
                    total = (
                        prefix[r2 + 1][c2 + 1]
                        - prefix[r1][c2 + 1]
                        - prefix[r2 + 1][c1]
                        + prefix[r1][c1]
                    )
                    count += total == target

    return count
""",
        solution=r"""
# OPTIMISED: O(m^2 * n) time, O(n) space
# Idea: Reduce 2D to 1D (row pairs) + prefix-sum hashmap
def num_submatrix_sum_target(matrix, target):
    m, n = len(matrix), len(matrix[0])
    count = 0

    for top in range(m):
        column_sums = [0] * n

        for bottom in range(top, m):
            for c in range(n):
                column_sums[c] += matrix[bottom][c]  # rows top..bottom squashed into one array

            seen = {0: 1}
            running = 0

            for value in column_sums:
                running += value
                count += seen.get(running - target, 0)
                seen[running] = seen.get(running, 0) + 1

    return count
""",
    ),
]
