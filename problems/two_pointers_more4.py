"""more Two Pointers problems (batch 5) - part of the problem bank for the "two_pointers" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Longest Word in Dictionary through Deleting (LeetCode 524) ----
    dict(
        title="Longest Word in Dictionary through Deleting",
        diff="M",
        lc=524,
        slug="longest-word-in-dictionary-through-deleting",
        prompt=(
            "Return the longest word in dictionary that can be formed by deleting some characters of s (a "
            "subsequence). On ties return the lexicographically smallest word; return '' if none fits."
        ),
        sig="def find_longest_word(s: str, dictionary: List[str]) -> str:",
        fn="find_longest_word",
        tests=[
            (("abpcplea", ["ale", "apple", "monkey", "plea"]), "apple"),
            (("abpcplea", ["a", "b", "c"]), "a"),
            (("abc", ["xyz"]), ""),
            (("bab", ["ba", "ab", "a", "b"]), "ab"),
        ],
        hints=[
            "A word fits if it is a subsequence of s - check it with two pointers.",
            "Sorting the dictionary by (-length, word) puts the preferred answers first.",
            "Then return the first word that is a subsequence; no need to test the rest.",
        ],
        pattern="Subsequence check with two pointers + smart ordering",
        explain=(
            "Sorting by the tie-breaking rule turns 'find the best' into 'find the first valid', so we stop at the "
            "first success."
        ),
        cx="O(D log D + D * |s|) time worst case",
        brute_cx="O(D * |s|) time - test every word and keep the best",
        brute=r"""
# BRUTE FORCE: O(D * |s|) time - test every word and keep the best
def find_longest_word(s, dictionary):
    def is_subsequence(word):
        i = 0
        for ch in s:
            if i < len(word) and word[i] == ch:
                i += 1
        return i == len(word)

    best = ""

    for word in dictionary:
        if is_subsequence(word) and (
            len(word) > len(best) or (len(word) == len(best) and word < best)
        ):
            best = word

    return best
""",
        solution=r"""
# OPTIMISED: O(D log D + D * |s|) time worst case
# Idea: Subsequence check with two pointers + smart ordering
def find_longest_word(s, dictionary):
    for word in sorted(dictionary, key=lambda w: (-len(w), w)):
        it = iter(s)
        if all(ch in it for ch in word):  # `in` on an iterator consumes it: a subsequence test
            return word
    return ""
""",
    ),
    # ---- Sum of Square Numbers (LeetCode 633) ----
    dict(
        title="Sum of Square Numbers",
        diff="M",
        lc=633,
        slug="sum-of-square-numbers",
        prompt="Return True if there are non-negative integers a and b with a*a + b*b == c.",
        sig="def judge_square_sum(c: int) -> bool:",
        fn="judge_square_sum",
        tests=[
            ((5,), True),
            ((3,), False),
            ((0,), True),
            ((1,), True),
            ((4,), True),
            ((2,), True),
            ((6,), False),
            ((25,), True),
        ],
        hints=[
            "a and b are at most sqrt(c).",
            "Trying every pair is O(c).",
            "Two pointers: lo = 0, hi = isqrt(c). If lo^2 + hi^2 is too small raise lo, if too big lower hi.",
        ],
        pattern="Two pointers on a sorted sequence of squares",
        explain=(
            "The squares 0, 1, 4, ... are sorted, so this is Two Sum on an implicit sorted array and each step "
            "discards one candidate."
        ),
        cx="O(sqrt(c)) time, O(1) space",
        brute_cx="O(c) time - try every pair (a, b)",
        brute=r"""
# BRUTE FORCE: O(c) time - try every pair (a, b)
def judge_square_sum(c):
    limit = math.isqrt(c)
    return any(a * a + b * b == c for a in range(limit + 1) for b in range(a, limit + 1))
""",
        solution=r"""
# OPTIMISED: O(sqrt(c)) time, O(1) space
# Idea: Two pointers on a sorted sequence of squares
def judge_square_sum(c):
    lo, hi = 0, math.isqrt(c)

    while lo <= hi:
        total = lo * lo + hi * hi
        if total == c:
            return True
        if total < c:
            lo += 1
        else:
            hi -= 1

    return False
""",
    ),
    # ---- Valid Triangle Number (LeetCode 611) ----
    dict(
        title="Valid Triangle Number",
        diff="M",
        lc=611,
        slug="valid-triangle-number",
        prompt=(
            "Return the number of triplets of array elements (by index) that can be the side lengths of a triangle "
            "(the two smaller sides must sum to MORE than the largest)."
        ),
        sig="def triangle_number(nums: List[int]) -> int:",
        fn="triangle_number",
        tests=[
            (([2, 2, 3, 4],), 3),
            (([4, 2, 3, 4],), 4),
            (([1, 1],), 0),
            (([0, 0, 0],), 0),
            (([3, 3, 3],), 1),
        ],
        hints=[
            "After sorting, a <= b <= c is a triangle iff a + b > c.",
            "Fix the largest side c at index k and look for pairs (i, j) below it.",
            (
                "Two pointers i = 0, j = k - 1: if nums[i] + nums[j] > nums[k] then EVERY index from i to j - 1 "
                "pairs with j: add j - i and move j down; otherwise move i up."
            ),
        ],
        pattern="Sort + fix the largest + two pointers (counting pairs in bulk)",
        explain=(
            "Once nums[i] + nums[j] > nums[k], any larger i also works with that j, so a whole range of pairs is "
            "counted in one step."
        ),
        cx="O(n^2) time",
        brute_cx="O(n^3) time - test every triplet",
        brute=r"""
# BRUTE FORCE: O(n^3) time - test every triplet
def triangle_number(nums):
    count = 0
    for a, b, c in itertools.combinations(nums, 3):
        x, y, z = sorted((a, b, c))
        if x + y > z:
            count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n^2) time
# Idea: Sort + fix the largest + two pointers (counting pairs in bulk)
def triangle_number(nums):
    nums = sorted(nums)
    count = 0

    for k in range(len(nums) - 1, 1, -1):  # nums[k] is the largest side
        i, j = 0, k - 1
        while i < j:
            if nums[i] + nums[j] > nums[k]:
                count += j - i  # every i' in [i, j) also works with this j
                j -= 1
            else:
                i += 1

    return count
""",
    ),
    # ---- Heaters (LeetCode 475) ----
    dict(
        title="Heaters",
        diff="M",
        lc=475,
        slug="heaters",
        prompt=(
            "Houses and heaters are points on a line. Every heater warms all positions within the same radius. "
            "Return the minimum radius so that every house is warmed."
        ),
        sig="def find_radius(houses: List[int], heaters: List[int]) -> int:",
        fn="find_radius",
        tests=[
            (([1, 2, 3], [2]), 1),
            (([1, 2, 3, 4], [1, 4]), 1),
            (([1, 5], [2]), 3),
            (([1], [1]), 0),
        ],
        hints=[
            "The radius is the largest distance from any house to its NEAREST heater.",
            "For one house, the nearest heater is one of the two heaters around it in sorted order.",
            (
                "Sort heaters and binary search (or two pointers over sorted houses) for each house; the answer is "
                "the maximum of those nearest distances."
            ),
        ],
        pattern="Nearest neighbour via sort + binary search / two pointers",
        explain=(
            "A max over houses of a min over heaters; sorting lets each inner minimum be found with one bisect "
            "instead of a scan."
        ),
        cx="O((n + m) log m) time",
        brute_cx="O(n * m) time - check every house against every heater",
        brute=r"""
# BRUTE FORCE: O(n * m) time - check every house against every heater
def find_radius(houses, heaters):
    return max(min(abs(h - w) for w in heaters) for h in houses)
""",
        solution=r"""
# OPTIMISED: O((n + m) log m) time
# Idea: Nearest neighbour via sort + binary search / two pointers
def find_radius(houses, heaters):
    heaters = sorted(heaters)
    radius = 0

    for h in houses:
        i = bisect.bisect_left(heaters, h)
        left = h - heaters[i - 1] if i > 0 else float("inf")
        right = heaters[i] - h if i < len(heaters) else float("inf")
        radius = max(radius, min(left, right))

    return radius
""",
    ),
    # ---- K-diff Pairs in an Array (LeetCode 532) ----
    dict(
        title="K-diff Pairs in an Array",
        diff="M",
        lc=532,
        slug="k-diff-pairs-in-an-array",
        prompt=(
            "Return the number of UNIQUE pairs (a, b) of values in nums (taken from different indices) with |a - b| "
            "== k."
        ),
        sig="def find_pairs(nums: List[int], k: int) -> int:",
        fn="find_pairs",
        tests=[
            (([3, 1, 4, 1, 5], 2), 2),
            (([1, 2, 3, 4, 5], 1), 4),
            (([1, 3, 1, 5, 4], 0), 1),
            (([1, 1], 0), 1),
            (([1], 1), 0),
        ],
        hints=[
            "Pairs are unique by VALUE, so duplicates should not be counted twice.",
            "Count occurrences of every distinct value.",
            (
                "For k > 0 count distinct x with x + k also present; for k == 0 count distinct x that occur at "
                "least twice."
            ),
        ],
        pattern="Frequency map (or sort + two pointers)",
        explain=(
            "Looking only upward (x + k) counts each pair once; k = 0 is special because a value needs a second copy."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - collect every qualifying pair into a set",
        brute=r"""
# BRUTE FORCE: O(n^2) time - collect every qualifying pair into a set
def find_pairs(nums, k):
    pairs = set()
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if abs(nums[i] - nums[j]) == k:
                pairs.add((min(nums[i], nums[j]), max(nums[i], nums[j])))
    return len(pairs)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Frequency map (or sort + two pointers)
def find_pairs(nums, k):
    counts = Counter(nums)
    if k == 0:
        return sum(1 for c in counts.values() if c > 1)
    return sum(1 for x in counts if x + k in counts)
""",
    ),
    # ---- Longest Mountain in Array (LeetCode 845) ----
    dict(
        title="Longest Mountain in Array",
        diff="M",
        lc=845,
        slug="longest-mountain-in-array",
        prompt=(
            "A mountain is a subarray of length >= 3 that strictly increases to a peak and then strictly decreases. "
            "Return the length of the longest mountain (0 if none)."
        ),
        sig="def longest_mountain(arr: List[int]) -> int:",
        fn="longest_mountain",
        tests=[
            (([2, 1, 4, 7, 3, 2, 5],), 5),
            (([2, 2, 2],), 0),
            (([1, 2, 3],), 0),
            (([0, 1, 0],), 3),
            (([2, 3, 3, 2],), 0),
        ],
        hints=[
            "Every mountain has exactly one peak: an index with a smaller left AND right neighbour.",
            "From a peak walk left while values decrease, and right while they decrease.",
            (
                "After handling a peak jump straight to the end of its right slope - mountains cannot overlap past "
                "the descent - to stay O(n)."
            ),
        ],
        pattern="Expand from peaks; skip what is already processed",
        explain=(
            "Each element is visited by at most a constant number of slope walks because after a peak we continue "
            "from where the descent ended."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - expand around every peak without skipping",
        brute=r"""
# BRUTE FORCE: O(n^2) time - expand around every peak without skipping
def longest_mountain(arr):
    best = 0

    for i in range(1, len(arr) - 1):
        if arr[i - 1] < arr[i] > arr[i + 1]:
            left = i - 1
            while left > 0 and arr[left - 1] < arr[left]:
                left -= 1
            right = i + 1
            while right < len(arr) - 1 and arr[right] > arr[right + 1]:
                right += 1
            best = max(best, right - left + 1)

    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Expand from peaks; skip what is already processed
def longest_mountain(arr):
    n, best, i = len(arr), 0, 1

    while i < n - 1:
        if arr[i - 1] < arr[i] > arr[i + 1]:  # a peak
            left = i - 1

            while left > 0 and arr[left - 1] < arr[left]:
                left -= 1

            right = i + 1

            while right < n - 1 and arr[right] > arr[right + 1]:
                right += 1

            best = max(best, right - left + 1)
            i = right  # nothing new can start before the end of this descent
        else:
            i += 1

    return best
""",
    ),
    # ---- Bag of Tokens (LeetCode 948) ----
    dict(
        title="Bag of Tokens",
        diff="M",
        lc=948,
        slug="bag-of-tokens",
        prompt=(
            "Start with `power` and score 0. Playing a token face UP costs tokens[i] power and gives 1 score; face "
            "DOWN (needs score >= 1) gives tokens[i] power and costs 1 score. Each token can be played at most "
            "once, in any order. Return the maximum score you can end with."
        ),
        sig="def bag_of_tokens_score(tokens: List[int], power: int) -> int:",
        fn="bag_of_tokens_score",
        tests=[
            (([100], 50), 0),
            (([200, 100], 150), 1),
            (([100, 200, 300, 400], 200), 2),
            (([], 5), 0),
            (([50], 50), 1),
        ],
        hints=[
            "Spend power on the CHEAPEST tokens and gain power from the MOST EXPENSIVE ones.",
            "Sort the tokens and use two pointers (cheapest at the left, priciest at the right).",
            (
                "If power >= tokens[left], play it up and score++. Else if score > 0, play tokens[right] down "
                "(power gain, score--). Else stop. Track the best score seen."
            ),
        ],
        pattern="Greedy + two pointers on sorted values",
        explain=(
            "Buying cheap points and selling one point for the biggest power boost is the best exchange rate, so "
            "the greedy two-ended walk is optimal."
        ),
        cx="O(n log n) time",
        brute_cx="O(n! * 2^n) time - try every order and every up/down choice",
        brute=r"""
# BRUTE FORCE: O(n! * 2^n) time - try every order and every up/down choice
def bag_of_tokens_score(tokens, power):
    best = 0

    def dfs(used, power, score):
        nonlocal best
        best = max(best, score)

        for i, t in enumerate(tokens):
            if not used >> i & 1:
                if power >= t:
                    dfs(used | 1 << i, power - t, score + 1)  # face up
                if score >= 1:
                    dfs(used | 1 << i, power + t, score - 1)  # face down

    dfs(0, power, 0)

    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Greedy + two pointers on sorted values
def bag_of_tokens_score(tokens, power):
    tokens = sorted(tokens)
    left, right, score, best = 0, len(tokens) - 1, 0, 0

    while left <= right:
        if power >= tokens[left]:
            power -= tokens[left]  # buy a point with the cheapest token
            left += 1
            score += 1
            best = max(best, score)
        elif score > 0:
            power += tokens[right]  # sell a point for the largest power gain
            right -= 1
            score -= 1
        else:
            break

    return best
""",
    ),
    # ---- Shortest Subarray to be Removed to Make Array Sorted (LeetCode 1574) ----
    dict(
        title="Shortest Subarray to be Removed to Make Array Sorted",
        diff="M",
        lc=1574,
        slug="shortest-subarray-to-be-removed-to-make-array-sorted",
        prompt=(
            "Remove one contiguous subarray (possibly empty) so that the remaining elements are non-decreasing. "
            "Return the minimum length you must remove."
        ),
        sig="def find_length_of_shortest_subarray(arr: List[int]) -> int:",
        fn="find_length_of_shortest_subarray",
        tests=[
            (([1, 2, 3, 10, 4, 2, 3, 5],), 3),
            (([5, 4, 3, 2, 1],), 4),
            (([1, 2, 3],), 0),
            (([1],), 0),
            (([2, 2, 2, 1, 1, 1],), 3),
        ],
        hints=[
            "What remains is a non-decreasing PREFIX plus a non-decreasing SUFFIX, glued together.",
            (
                "Find the longest sorted prefix and the longest sorted suffix. Removing everything outside just one "
                "of them is a baseline answer."
            ),
            (
                "For each prefix end i, advance a suffix pointer j while arr[j] < arr[i]; the removed length is j - "
                "i - 1. Both pointers only move forward."
            ),
        ],
        pattern="Sorted prefix + sorted suffix merged with two pointers",
        explain=(
            "For a fixed kept prefix, the best suffix start only moves right as the prefix grows (its last value "
            "grows), so one monotone sweep covers all combinations."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^3) time - try every removal length and position",
        brute=r"""
# BRUTE FORCE: O(n^3) time - try every removal length and position
def find_length_of_shortest_subarray(arr):
    n = len(arr)
    for length in range(n + 1):
        for start in range(n - length + 1):
            rest = arr[:start] + arr[start + length :]
            if all(rest[i] <= rest[i + 1] for i in range(len(rest) - 1)):
                return length
    return n
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Sorted prefix + sorted suffix merged with two pointers
def find_length_of_shortest_subarray(arr):
    n = len(arr)
    left = 0

    while left + 1 < n and arr[left] <= arr[left + 1]:
        left += 1

    if left == n - 1:
        return 0  # already sorted

    right = n - 1

    while right > 0 and arr[right - 1] <= arr[right]:
        right -= 1

    best = min(n - left - 1, right)  # keep only the prefix, or only the suffix
    j = right

    for i in range(left + 1):
        while j < n and arr[j] < arr[i]:
            j += 1
        best = min(best, j - i - 1)  # keep arr[:i + 1] and arr[j:]

    return best
""",
    ),
    # ---- Minimum Length of String After Deleting Similar Ends (LeetCode 1750) ----
    dict(
        title="Minimum Length of String After Deleting Similar Ends",
        diff="M",
        lc=1750,
        slug="minimum-length-of-string-after-deleting-similar-ends",
        prompt=(
            "s uses only 'a', 'b', 'c'. Repeatedly: pick a non-empty prefix and a non-empty suffix that do not "
            "overlap, whose characters are all the same letter, and delete both. Return the minimum possible length "
            "of s."
        ),
        sig="def minimum_length(s: str) -> int:",
        fn="minimum_length",
        tests=[
            (("ca",), 2),
            (("cabaabac",), 0),
            (("aabccabba",), 3),
            (("a",), 1),
            (("aa",), 0),
        ],
        hints=[
            "The two ends must be the SAME letter to do anything.",
            "Always delete the maximal run of that letter on both sides - taking less never helps.",
            (
                "Two pointers: while s[l] == s[r] and l < r, skip every equal letter from the left and from the "
                "right; the answer is r - l + 1."
            ),
        ],
        pattern="Two pointers closing in from both ends (greedy maximal strips)",
        explain=(
            "Stripping the whole run is never worse than a partial strip, because the leftovers would only be the "
            "same letter at the new ends and would be stripped next anyway."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="exponential in the worst case - search every prefix/suffix length with memoisation",
        brute=r"""
# BRUTE FORCE: exponential in the worst case - search every prefix/suffix length with memoisation
def minimum_length(s):
    @lru_cache(None)
    def best(left, r):  # the remaining string is s[l:r]
        result = r - left

        if r - left >= 2 and s[left] == s[r - 1]:
            c, p = s[left], 1

            while left + p <= r and s[left + p - 1] == c:  # prefix s[l:l+p] is all c
                q = 1
                while (
                    left + p <= r - q and s[r - q] == c
                ):  # suffix s[r-q:r] is all c, not overlapping
                    result = min(result, best(left + p, r - q))
                    q += 1
                p += 1

        return result

    return best(0, len(s))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two pointers closing in from both ends (greedy maximal strips)
def minimum_length(s):
    left, r = 0, len(s) - 1

    while left < r and s[left] == s[r]:
        c = s[left]
        while left <= r and s[left] == c:
            left += 1
        while left <= r and s[r] == c:
            r -= 1

    return r - left + 1
""",
    ),
    # ---- Find First Palindromic String in the Array (LeetCode 2108) ----
    dict(
        title="Find First Palindromic String in the Array",
        diff="E",
        lc=2108,
        slug="find-first-palindromic-string-in-the-array",
        prompt="Return the first string in words that is a palindrome, or '' if there is none.",
        sig="def first_palindrome(words: List[str]) -> str:",
        fn="first_palindrome",
        tests=[
            ((["abc", "car", "ada", "racecar", "cool"],), "ada"),
            ((["notapalindrome", "racecar"],), "racecar"),
            ((["def", "ghi"],), ""),
            ((["a"],), "a"),
        ],
        hints=[
            "A palindrome reads the same forwards and backwards.",
            "Reversing a copy works but allocates a new string per word.",
            "Compare characters from both ends moving inwards; stop at the first mismatch.",
        ],
        pattern="Two pointers palindrome check",
        explain="Comparing symmetric positions needs no extra memory and exits early on the first mismatch.",
        cx="O(total characters) time, O(1) extra space",
        brute_cx="O(total characters) time, O(longest word) extra space - build the reversed string",
        brute=r"""
# BRUTE FORCE: O(total characters) time, O(longest word) extra space - build the reversed string
def first_palindrome(words):
    for word in words:
        if word == word[::-1]:
            return word
    return ""
""",
        solution=r"""
# OPTIMISED: O(total characters) time, O(1) extra space
# Idea: Two pointers palindrome check
def first_palindrome(words):
    for word in words:
        i, j = 0, len(word) - 1
        while i < j and word[i] == word[j]:
            i += 1
            j -= 1
        if i >= j:  # all mirrored pairs matched
            return word

    return ""
""",
    ),
    # ---- Count Pairs Whose Sum is Less than Target (LeetCode 2824) ----
    dict(
        title="Count Pairs Whose Sum is Less than Target",
        diff="E",
        lc=2824,
        slug="count-pairs-whose-sum-is-less-than-target",
        prompt="Count pairs of indices i < j with nums[i] + nums[j] < target.",
        sig="def count_pairs(nums: List[int], target: int) -> int:",
        fn="count_pairs",
        tests=[
            (([-1, 1, 2, 3, 1], 2), 3),
            (([-6, 2, 5, -2, -7, -1, 3], -2), 10),
            (([1], 5), 0),
            (([1, 1], 2), 0),
        ],
        hints=[
            "Order does not matter for the sum, so you may sort the array first.",
            "In sorted order, if nums[lo] + nums[hi] < target then ALL of lo..hi-1 pair with hi.",
            "Two pointers: when the sum is small add hi - lo and move lo up; otherwise move hi down.",
        ],
        pattern="Sort + two pointers counting in bulk",
        explain=(
            "Sorting makes the 'sum below target' relation monotone, so one pointer move settles a whole block of "
            "pairs."
        ),
        cx="O(n log n) time",
        brute_cx="O(n^2) time - test every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every pair
def count_pairs(nums, target):
    return sum(1 for a, b in itertools.combinations(nums, 2) if a + b < target)
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Sort + two pointers counting in bulk
def count_pairs(nums, target):
    nums = sorted(nums)
    lo, hi, count = 0, len(nums) - 1, 0

    while lo < hi:
        if nums[lo] + nums[hi] < target:
            count += hi - lo  # nums[lo] works with every index in (lo, hi]
            lo += 1
        else:
            hi -= 1

    return count
""",
    ),
    # ---- Maximum Distance Between a Pair of Values (LeetCode 1855) ----
    dict(
        title="Maximum Distance Between a Pair of Values",
        diff="M",
        lc=1855,
        slug="maximum-distance-between-a-pair-of-values",
        prompt=(
            "nums1 and nums2 are both non-increasing. A pair (i, j) is valid if i <= j and nums1[i] <= nums2[j]; "
            "its distance is j - i. Return the maximum distance of a valid pair (0 if none)."
        ),
        sig="def max_distance(nums1: List[int], nums2: List[int]) -> int:",
        fn="max_distance",
        tests=[
            (([55, 30, 5, 4, 2], [100, 20, 10, 10, 5]), 2),
            (([2, 2, 2], [10, 10, 1]), 1),
            (([30, 29, 19, 5], [25, 25, 25, 25, 25]), 2),
            (([5], [1]), 0),
        ],
        hints=[
            "Checking every (i, j) is O(n * m).",
            "Both arrays are sorted, so for a fixed i the valid j's form a prefix of nums2.",
            (
                "Two pointers: advance j while nums2[j] >= nums1[i]; if j falls behind i advance i; record j - i "
                "after each extension."
            ),
        ],
        pattern="Two pointers on two sorted arrays",
        explain=(
            "As i increases, nums1[i] only decreases, so the farthest valid j never moves backwards - both pointers "
            "go forward once."
        ),
        cx="O(n + m) time",
        brute_cx="O(n * m) time - test every pair",
        brute=r"""
# BRUTE FORCE: O(n * m) time - test every pair
def max_distance(nums1, nums2):
    best = 0
    for i in range(len(nums1)):
        for j in range(i, len(nums2)):
            if nums1[i] <= nums2[j]:
                best = max(best, j - i)
    return best
""",
        solution=r"""
# OPTIMISED: O(n + m) time
# Idea: Two pointers on two sorted arrays
def max_distance(nums1, nums2):
    i = j = best = 0

    while i < len(nums1) and j < len(nums2):
        if nums1[i] <= nums2[j]:
            best = max(best, j - i)
            j += 1  # try to stretch the pair
        else:
            i += 1  # nums1[i] is too big for nums2[j]
            if j < i:
                j = i

    return best
""",
    ),
    # ---- Number of Subsequences That Satisfy the Given Sum Condition (LeetCode 1498) ----
    dict(
        title="Number of Subsequences That Satisfy the Given Sum Condition",
        diff="M",
        lc=1498,
        slug="number-of-subsequences-that-satisfy-the-given-sum-condition",
        prompt=(
            "Count the non-empty subsequences of nums whose minimum + maximum is <= target. Return the count modulo "
            "1_000_000_007."
        ),
        sig="def num_subseq(nums: List[int], target: int) -> int:",
        fn="num_subseq",
        tests=[
            (([3, 5, 6, 7], 9), 4),
            (([3, 3, 6, 8], 10), 6),
            (([2, 3, 3, 4, 6, 7], 12), 61),
            (([5], 10), 1),
            (([5], 9), 0),
        ],
        hints=[
            "Subsequence order does not matter for min and max, so sort the array.",
            (
                "Fix the minimum at index l and the maximum at index r: the elements strictly between can be chosen "
                "freely, giving 2^(r - l) subsequences."
            ),
            (
                "Two pointers: if nums[l] + nums[r] <= target add 2^(r-l) and move l up; else move r down. "
                "Precompute powers of two."
            ),
        ],
        pattern="Sort + two pointers + counting subsets by min/max",
        explain=(
            "Anchoring the smallest and largest chosen element makes everything between them optional, so each (l, "
            "r) contributes a power of two."
        ),
        cx="O(n log n) time",
        brute_cx="O(n * 2^n) time - enumerate every subsequence",
        brute=r"""
# BRUTE FORCE: O(n * 2^n) time - enumerate every subsequence
def num_subseq(nums, target):
    count = 0
    for mask in range(1, 1 << len(nums)):
        chosen = [nums[i] for i in range(len(nums)) if mask >> i & 1]
        if min(chosen) + max(chosen) <= target:
            count += 1
    return count % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Sort + two pointers + counting subsets by min/max
def num_subseq(nums, target):
    mod = 10**9 + 7
    nums = sorted(nums)
    n = len(nums)
    pow2 = [1] * n

    for i in range(1, n):
        pow2[i] = pow2[i - 1] * 2 % mod

    left, right, total = 0, n - 1, 0

    while left <= right:
        if nums[left] + nums[right] <= target:
            total = (
                total + pow2[right - left]
            ) % mod  # nums[l] is the min; anything between is optional
            left += 1
        else:
            right -= 1

    return total
""",
    ),
]
