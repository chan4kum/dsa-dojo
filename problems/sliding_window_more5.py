"""extra batch of Sliding Window problems - the problem bank for the "sliding_window" topic (batch 5).

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

PROBLEMS = [
    # ---- Longest Turbulent Subarray (LeetCode 978) ----
    dict(
        title="Longest Turbulent Subarray",
        diff="M",
        lc=978,
        slug="longest-turbulent-subarray",
        prompt=(
            "A subarray is turbulent if the comparison sign between neighbours strictly alternates (up, down, up, "
            "... or down, up, down, ...). Equal neighbours break it. Return the length of the longest turbulent "
            "subarray (a single element counts as turbulent)."
        ),
        sig="def max_turbulence_size(arr: List[int]) -> int:",
        fn="max_turbulence_size",
        tests=[
            (([9, 4, 2, 10, 7, 8, 8, 1, 9],), 5),
            (([4, 8, 12, 16],), 2),
            (([100],), 1),
            (([9, 9],), 1),
            (([1, 2, 1, 2, 1],), 5),
        ],
        hints=[
            "Look at the sign of each adjacent comparison: +1, -1 or 0.",
            "A window is turbulent as long as consecutive signs are opposite and non-zero.",
            (
                "Walk once; when the alternation breaks (signs equal or zero) restart the window at the last "
                "element (or the current one after a 0)."
            ),
        ],
        pattern="Sliding window over the sequence of comparison signs",
        explain=(
            "Turbulence is a property of consecutive comparisons, not of the values. While the next comparison is "
            "the opposite sign of the previous one, the window keeps growing; the moment it repeats a sign (the "
            "last element is shared by the old and the new window) or is equal, the window restarts. One pass is "
            "enough because the best window ends at the break."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - check every subarray",
        brute=r"""
# BRUTE FORCE: O(n^2) time - check every subarray
def max_turbulence_size(arr):
    n = len(arr)
    best = 1
    for i in range(n):
        for j in range(i + 1, n):
            ok = all(arr[k] != arr[k + 1] for k in range(i, j))
            ok = ok and all(
                (arr[k] - arr[k + 1]) * (arr[k + 1] - arr[k + 2]) < 0 for k in range(i, j - 1)
            )
            if ok:
                best = max(best, j - i + 1)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Sliding window over the sequence of comparison signs
def max_turbulence_size(arr):
    n = len(arr)
    best = 1
    left = 0
    for i in range(1, n):
        cmp = (arr[i - 1] > arr[i]) - (arr[i - 1] < arr[i])
        if cmp == 0:
            left = i
        elif i == n - 1 or cmp * ((arr[i] > arr[i + 1]) - (arr[i] < arr[i + 1])) != -1:
            best = max(best, i - left + 1)
            left = i
    return best
""",
    ),
    # ---- Swap For Longest Repeated Character Substring (LeetCode 1156) ----
    dict(
        title="Swap For Longest Repeated Character Substring",
        diff="M",
        lc=1156,
        slug="swap-for-longest-repeated-character-substring",
        prompt=(
            "You may swap two characters of text (or do nothing). Return the length of the longest substring made "
            "of one repeated character that you can obtain."
        ),
        sig="def max_rep_opt1(text: str) -> int:",
        fn="max_rep_opt1",
        tests=[
            (("ababa",), 3),
            (("aaabaaa",), 6),
            (("aaabbaaa",), 4),
            (("aaaaa",), 5),
            (("abcdef",), 1),
        ],
        hints=[
            "Group the string into runs of equal letters.",
            (
                "A swap can extend a run by one letter pulled from elsewhere in the string - if that letter exists "
                "elsewhere."
            ),
            (
                "It can also glue two runs of the same letter separated by a single different letter. In every case "
                "the result is capped by the total count of that letter."
            ),
        ],
        pattern="Run-length groups + cap by total letter count",
        explain=(
            "A good swap either brings one more copy of the run's letter from another place (length run + 1, but "
            "never more than the total number of that letter) or fills a one-letter gap between two runs of the "
            "same letter, joining them (run1 + run2, plus one more copy if some letter is left over). Checking "
            "those two cases on the run list covers every beneficial swap."
        ),
        cx="O(n) time, O(1) space for a fixed alphabet",
        brute_cx="O(n^3) time - try every swap and measure the longest run",
        brute=r"""
# BRUTE FORCE: O(n^3) time - try every swap and measure the longest run
def max_rep_opt1(text):
    def longest(chars):
        best = run = 1
        for i in range(1, len(chars)):
            run = run + 1 if chars[i] == chars[i - 1] else 1
            best = max(best, run)
        return best

    best = longest(text)
    for i in range(len(text)):
        for j in range(i + 1, len(text)):
            chars = list(text)
            chars[i], chars[j] = chars[j], chars[i]
            best = max(best, longest(chars))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space for a fixed alphabet
# Idea: Run-length groups + cap by total letter count
def max_rep_opt1(text):
    runs = []
    for ch in text:
        if runs and runs[-1][0] == ch:
            runs[-1][1] += 1
        else:
            runs.append([ch, 1])
    total = Counter(text)
    best = 0
    for i, (ch, length) in enumerate(runs):
        best = max(best, min(length + 1, total[ch]))
        if i + 2 < len(runs) and runs[i + 1][1] == 1 and runs[i + 2][0] == ch:
            best = max(best, min(length + runs[i + 2][1] + 1, total[ch]))
    return best
""",
    ),
    # ---- Replace the Substring for Balanced String (LeetCode 1234) ----
    dict(
        title="Replace the Substring for Balanced String",
        diff="M",
        lc=1234,
        slug="replace-the-substring-for-balanced-string",
        prompt=(
            "s has length n (a multiple of 4) and only the letters 'Q', 'W', 'E', 'R'. It is balanced if each "
            "letter occurs exactly n / 4 times. You may replace ONE substring by any string of the same length. "
            "Return the minimum length of the substring to replace (0 if s is already balanced)."
        ),
        sig="def balanced_string(s: str) -> int:",
        fn="balanced_string",
        tests=[
            (("QWER",), 0),
            (("QQWE",), 1),
            (("QQQW",), 2),
            (("QQQQ",), 3),
        ],
        hints=[
            (
                "After replacing a window, anything can be placed inside it - so only the letters OUTSIDE the "
                "window matter."
            ),
            (
                "The outside is fine iff no letter occurs more than n / 4 times there (the window can fill up the "
                "shortfall)."
            ),
            (
                "Slide a window: expand right (remove that letter from the outside counts), and while the outside "
                "is valid, record the length and shrink from the left."
            ),
        ],
        pattern="Shrinkable window where the condition is on what is OUTSIDE it",
        explain=(
            "The replacement can supply any letters, so the requirement reduces to: every letter appears at most n "
            "/ 4 times outside the window. Keeping counts of the outside, a two-pointer sweep finds the shortest "
            "window satisfying this - once valid, moving the left edge right can only add letters back to the "
            "outside."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^3) time - for each window length and start, recount the outside",
        brute=r"""
# BRUTE FORCE: O(n^3) time - for each window length and start, recount the outside
def balanced_string(s):
    n = len(s)
    need = n // 4
    for length in range(n + 1):
        for start in range(n - length + 1):
            outside = Counter(s[:start] + s[start + length :])
            if all(outside[c] <= need for c in "QWER"):
                return length
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Shrinkable window where the condition is on what is OUTSIDE it
def balanced_string(s):
    n = len(s)
    need = n // 4
    count = Counter(s)
    if all(count[c] <= need for c in "QWER"):
        return 0
    best = n
    left = 0
    for right, ch in enumerate(s):
        count[ch] -= 1
        while left <= right and all(count[c] <= need for c in "QWER"):
            best = min(best, right - left + 1)
            count[s[left]] += 1
            left += 1
    return best
""",
    ),
    # ---- Maximum Number of Occurrences of a Substring (LeetCode 1297) ----
    dict(
        title="Maximum Number of Occurrences of a Substring",
        diff="M",
        lc=1297,
        slug="maximum-number-of-occurrences-of-a-substring",
        prompt=(
            "Return the maximum number of occurrences (overlaps allowed) of any substring of s that has at most "
            "max_letters distinct letters and a length between min_size and max_size inclusive."
        ),
        sig="def max_freq(s: str, max_letters: int, min_size: int, max_size: int) -> int:",
        fn="max_freq",
        tests=[
            (("aababcaab", 2, 3, 4), 2),
            (("aaaa", 1, 3, 3), 2),
            (("aabcabcab", 2, 2, 3), 3),
            (("abcde", 2, 3, 3), 0),
        ],
        hints=[
            "If a longer substring occurs k times, its prefix of length min_size occurs at least k times as well.",
            "So only substrings of length exactly min_size need to be considered; max_size is a red herring.",
            (
                "Slide a window of width min_size, track its distinct letters, and count each valid substring in a "
                "Counter."
            ),
        ],
        pattern="Fixed-size sliding window + a hash counter of window contents",
        explain=(
            "Every occurrence of a longer valid substring contains an occurrence of its shorter prefix, which has "
            "no more distinct letters. The shortest length therefore always does at least as well, so the problem "
            "collapses to a single fixed window size. A letter-count dictionary maintains the number of distinct "
            "letters as the window slides."
        ),
        cx="O(n * min_size) time, O(n) space",
        brute_cx="O(n * (max_size - min_size + 1) * max_size) time - count every allowed length",
        brute=r"""
# BRUTE FORCE: O(n * (max_size - min_size + 1) * max_size) time - count every allowed length
def max_freq(s, max_letters, min_size, max_size):
    count = Counter()
    for size in range(min_size, max_size + 1):
        for i in range(len(s) - size + 1):
            piece = s[i : i + size]
            if len(set(piece)) <= max_letters:
                count[piece] += 1
    return max(count.values(), default=0)
""",
        solution=r"""
# OPTIMISED: O(n * min_size) time, O(n) space
# Idea: Fixed-size sliding window + a hash counter of window contents
def max_freq(s, max_letters, min_size, max_size):
    count = Counter()
    window = Counter()
    for i, ch in enumerate(s):
        window[ch] += 1
        if i >= min_size:
            old = s[i - min_size]
            window[old] -= 1
            if window[old] == 0:
                del window[old]
        if i >= min_size - 1 and len(window) <= max_letters:
            count[s[i - min_size + 1 : i + 1]] += 1
    return max(count.values(), default=0)
""",
    ),
    # ---- Frequency of the Most Frequent Element (LeetCode 1838) ----
    dict(
        title="Frequency of the Most Frequent Element",
        diff="M",
        lc=1838,
        slug="frequency-of-the-most-frequent-element",
        prompt=(
            "In one operation you may add 1 to any element. Using at most k operations, return the maximum possible "
            "frequency of a single value in nums."
        ),
        sig="def max_frequency(nums: List[int], k: int) -> int:",
        fn="max_frequency",
        tests=[
            (([1, 2, 4], 5), 3),
            (([1, 4, 8, 13], 5), 2),
            (([3, 9, 6], 2), 1),
            (([5], 0), 1),
        ],
        hints=[
            (
                "You can only increase numbers, so the final common value equals some element of the array - the "
                "largest in its group."
            ),
            (
                "Sort the array; the best group for a target nums[right] is a block of the closest smaller values "
                "ending at it."
            ),
            (
                "Cost of raising a window [left..right] to nums[right] is nums[right] * width - window_sum. Shrink "
                "from the left while that cost exceeds k."
            ),
        ],
        pattern="Sort + sliding window with a cost constraint",
        explain=(
            "After sorting, raising a block of consecutive elements to the block's maximum costs max * width - sum. "
            "Choosing the elements closest to the target is always cheapest, so the optimal group is a contiguous "
            "window ending at the target. The cost only grows when the right end advances and shrinks when the left "
            "end advances, which is exactly the monotone behaviour a two-pointer window needs."
        ),
        cx="O(n log n) time, O(1) extra space",
        brute_cx="O(n^2 log n) time - for every target, add the cheapest elements one by one",
        brute=r"""
# BRUTE FORCE: O(n^2 log n) time - for every target, add the cheapest elements one by one
def max_frequency(nums, k):
    best = 1
    for target in set(nums):
        costs = sorted(target - x for x in nums if x <= target)
        spent = 0
        used = 0
        for cost in costs:
            if spent + cost > k:
                break
            spent += cost
            used += 1
        best = max(best, used)
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space
# Idea: Sort + sliding window with a cost constraint
def max_frequency(nums, k):
    nums = sorted(nums)
    left = 0
    total = 0
    best = 1
    for right, x in enumerate(nums):
        total += x
        while x * (right - left + 1) - total > k:
            total -= nums[left]
            left += 1
        best = max(best, right - left + 1)
    return best
""",
    ),
    # ---- Longest Substring Of All Vowels in Order (LeetCode 1839) ----
    dict(
        title="Longest Substring Of All Vowels in Order",
        diff="M",
        lc=1839,
        slug="longest-substring-of-all-vowels-in-order",
        prompt=(
            "word contains only the vowels a, e, i, o, u. A substring is beautiful if it contains all five vowels "
            "and its letters are in alphabetical (non-decreasing) order. Return the length of the longest beautiful "
            "substring, or 0 if there is none."
        ),
        sig="def longest_beautiful_substring(word: str) -> int:",
        fn="longest_beautiful_substring",
        tests=[
            (("aeiaaioaaaaeiiiiouuuooaauuaeiu",), 13),
            (("aeeeiiiioooauuuaeiou",), 5),
            (("a",), 0),
            (("aeiou",), 5),
        ],
        hints=[
            "Maximal non-decreasing runs cannot overlap - the string splits into them at every drop.",
            (
                "Inside a run, count the number of distinct letters seen (a new one appears each time the letter "
                "increases)."
            ),
            "A run is beautiful exactly when it has 5 distinct letters; keep the longest.",
        ],
        pattern="Window that resets whenever monotonicity breaks",
        explain=(
            "Because only vowels occur, a non-decreasing run with five distinct letters must contain all of a, e, "
            "i, o, u in order. Whenever a letter is smaller than the previous one the window can no longer extend "
            "any earlier window, so it restarts at that position. Counting letter increases gives the number of "
            "distinct letters in O(1)."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^3) time - test every substring",
        brute=r"""
# BRUTE FORCE: O(n^3) time - test every substring
def longest_beautiful_substring(word):
    best = 0
    n = len(word)
    for i in range(n):
        for j in range(i + 1, n + 1):
            piece = word[i:j]
            if len(set(piece)) == 5 and list(piece) == sorted(piece):
                best = max(best, j - i)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Window that resets whenever monotonicity breaks
def longest_beautiful_substring(word):
    best = 0
    start = 0
    distinct = 1
    for i in range(1, len(word) + 1):
        if i == len(word) or word[i] < word[i - 1]:
            if distinct == 5:
                best = max(best, i - start)
            start = i
            distinct = 1
        elif word[i] > word[i - 1]:
            distinct += 1
    return best
""",
    ),
    # ---- Substrings of Size Three with Distinct Characters (LeetCode 1876) ----
    dict(
        title="Substrings of Size Three with Distinct Characters",
        diff="E",
        lc=1876,
        slug="substrings-of-size-three-with-distinct-characters",
        prompt=(
            "A string is good if it has no repeated characters. Return the number of good substrings of length 3 in "
            "s (count each occurrence, even if the same substring appears several times)."
        ),
        sig="def count_good_substrings(s: str) -> int:",
        fn="count_good_substrings",
        tests=[
            (("xyzzaz",), 1),
            (("aababcabc",), 4),
            (("aaa",), 0),
            (("ab",), 0),
        ],
        hints=[
            "The window size is fixed at 3.",
            "Slide it along the string, maintaining counts of the three letters inside.",
            "The window is good when the number of distinct letters in it is 3.",
        ],
        pattern="Fixed-size sliding window with a letter counter",
        explain=(
            "A fixed window of width 3 visits each substring once. Updating the counter on entry and exit keeps the "
            "work per step constant; the window is good exactly when the counter has three keys."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time - build a set for every substring of length 3",
        brute=r"""
# BRUTE FORCE: O(n) time - build a set for every substring of length 3
def count_good_substrings(s):
    return sum(1 for i in range(len(s) - 2) if len(set(s[i : i + 3])) == 3)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Fixed-size sliding window with a letter counter
def count_good_substrings(s):
    window = Counter()
    good = 0
    for i, ch in enumerate(s):
        window[ch] += 1
        if i >= 3:
            old = s[i - 3]
            window[old] -= 1
            if window[old] == 0:
                del window[old]
        if i >= 2 and len(window) == 3:
            good += 1
    return good
""",
    ),
    # ---- Minimum Swaps to Group All 1's Together II (LeetCode 2134) ----
    dict(
        title="Minimum Swaps to Group All 1's Together II",
        diff="M",
        lc=2134,
        slug="minimum-swaps-to-group-all-1s-together-ii",
        prompt=(
            "nums is a CIRCULAR binary array (the last element is adjacent to the first). A swap exchanges the "
            "values at any two positions. Return the minimum number of swaps needed to make all the 1's contiguous "
            "(somewhere in the circle)."
        ),
        sig="def min_swaps(nums: List[int]) -> int:",
        fn="min_swaps",
        tests=[
            (([0, 1, 0, 1, 1, 0, 0],), 1),
            (([0, 1, 1, 1, 0, 0, 1, 1, 0],), 2),
            (([1, 1, 0, 0, 1],), 0),
            (([0, 0, 0],), 0),
            (([1, 1, 1],), 0),
        ],
        hints=[
            "Let k be the number of 1's: in the end they fill a window of exactly k consecutive positions.",
            "Each swap fixes one 0 inside that window, so the cost for a window is the number of 0's in it.",
            (
                "Slide a window of size k around the circle (index modulo n) and take the one with the fewest 0's "
                "(equivalently the most 1's)."
            ),
        ],
        pattern="Fixed-size circular sliding window",
        explain=(
            "The final block of 1's is a window of size k, and each zero inside it must be swapped with a one "
            "outside it - one swap per zero. Minimising the swaps therefore means finding the window of size k "
            "containing the most ones. Using indices modulo n handles the wrap-around without copying the array."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n * k) time - recount the zeros of every circular window",
        brute=r"""
# BRUTE FORCE: O(n * k) time - recount the zeros of every circular window
def min_swaps(nums):
    n = len(nums)
    k = sum(nums)
    if k == 0:
        return 0
    best = k
    for start in range(n):
        zeros = sum(1 for t in range(k) if nums[(start + t) % n] == 0)
        best = min(best, zeros)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Fixed-size circular sliding window
def min_swaps(nums):
    n = len(nums)
    k = sum(nums)
    if k in (0, n):
        return 0
    ones = sum(nums[:k])
    best = ones
    for i in range(1, n):
        ones += nums[(i + k - 1) % n] - nums[i - 1]
        best = max(best, ones)
    return k - best
""",
    ),
    # ---- Longest Nice Subarray (LeetCode 2401) ----
    dict(
        title="Longest Nice Subarray",
        diff="M",
        lc=2401,
        slug="longest-nice-subarray",
        prompt=(
            "A subarray is nice if the bitwise AND of every pair of elements at different positions is 0. Return "
            "the length of the longest nice subarray (a subarray of length 1 is always nice)."
        ),
        sig="def longest_nice_subarray(nums: List[int]) -> int:",
        fn="longest_nice_subarray",
        tests=[
            (([1, 3, 8, 48, 10],), 3),
            (([3, 1, 5, 11, 13],), 1),
            (([7],), 1),
            (([1, 2, 4, 8],), 4),
        ],
        hints=[
            "Pairwise AND == 0 means no bit is set in two different elements.",
            "Keep the OR of the window: a new element x can join only if (mask & x) == 0.",
            (
                "If it collides, drop elements from the left (XOR them out of the mask - safe because their bits "
                "were disjoint) until it fits."
            ),
        ],
        pattern="Sliding window with a bitmask of occupied bits",
        explain=(
            "Elements of a nice window use pairwise disjoint sets of bits, so the window's OR equals its XOR and "
            "removing an element is just XORing it out. The window can always be shrunk until the incoming element "
            "fits, which makes the left pointer monotone and the whole scan linear."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^4) time - check every pair inside every subarray",
        brute=r"""
# BRUTE FORCE: O(n^4) time - check every pair inside every subarray
def longest_nice_subarray(nums):
    best = 0
    n = len(nums)
    for i in range(n):
        for j in range(i, n):
            window = nums[i : j + 1]
            nice = all(
                window[a] & window[b] == 0
                for a in range(len(window))
                for b in range(a + 1, len(window))
            )
            if nice:
                best = max(best, j - i + 1)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Sliding window with a bitmask of occupied bits
def longest_nice_subarray(nums):
    mask = 0
    left = 0
    best = 0
    for right, x in enumerate(nums):
        while mask & x:
            mask ^= nums[left]
            left += 1
        mask |= x
        best = max(best, right - left + 1)
    return best
""",
    ),
    # ---- Take K of Each Character From Left and Right (LeetCode 2516) ----
    dict(
        title="Take K of Each Character From Left and Right",
        diff="M",
        lc=2516,
        slug="take-k-of-each-character-from-left-and-right",
        prompt=(
            "s contains only 'a', 'b' and 'c'. Each minute you take one character from either the leftmost or the "
            "rightmost end of s. Return the minimum number of minutes to take at least k of each letter, or -1 if "
            "that is impossible."
        ),
        sig="def take_characters(s: str, k: int) -> int:",
        fn="take_characters",
        tests=[
            (("aabaaaacaabc", 2), 8),
            (("a", 1), -1),
            (("abc", 0), 0),
            (("abc", 1), 3),
        ],
        hints=[
            "What you take is always a prefix plus a suffix; what remains untouched is a contiguous middle window.",
            "So maximise the length of the window you KEEP, subject to the outside holding at least k of every letter.",
            (
                "Slide a window: add letters (removing them from the outside count) and shrink from the left while "
                "some letter drops below k outside."
            ),
        ],
        pattern="Maximise a window while the complement satisfies a constraint",
        explain=(
            "Taking from both ends leaves a contiguous middle block untouched. Minimising minutes is the same as "
            "maximising that block, which is a standard longest-window sweep - except the constraint is on the "
            "counts outside the window (total minus inside). If the whole string lacks k of some letter, the answer "
            "is -1."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^3) time - try every prefix length and suffix length",
        brute=r"""
# BRUTE FORCE: O(n^3) time - try every prefix length and suffix length
def take_characters(s, k):
    n = len(s)
    best = None
    for left in range(n + 1):
        for right in range(n - left + 1):
            taken = Counter(s[:left]) + Counter(s[n - right :])
            if all(taken[c] >= k for c in "abc"):
                if best is None or left + right < best:
                    best = left + right
    return -1 if best is None else best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Maximise a window while the complement satisfies a constraint
def take_characters(s, k):
    count = Counter(s)
    if any(count[c] < k for c in "abc"):
        return -1
    left = 0
    keep = 0
    for right, ch in enumerate(s):
        count[ch] -= 1
        while count[ch] < k:
            count[s[left]] += 1
            left += 1
        keep = max(keep, right - left + 1)
    return len(s) - keep
""",
    ),
    # ---- Find the Longest Semi-Repetitive Substring (LeetCode 2730) ----
    dict(
        title="Find the Longest Semi-Repetitive Substring",
        diff="M",
        lc=2730,
        slug="find-the-longest-semi-repetitive-substring",
        prompt=(
            "A string of digits is semi-repetitive if it has at most one pair of equal ADJACENT digits. Return the "
            "length of the longest semi-repetitive substring of s."
        ),
        sig="def longest_semi_repetitive_substring(s: str) -> int:",
        fn="longest_semi_repetitive_substring",
        tests=[
            (("52233",), 4),
            (("5494",), 4),
            (("1111111",), 2),
            (("1",), 1),
            (("1212",), 4),
        ],
        hints=[
            "Count adjacent equal pairs inside the current window.",
            "Extend the right end; if the count exceeds 1, advance the left end.",
            "When the left end passes over a pair (s[left] == s[left + 1]), decrement the count.",
        ],
        pattern="Sliding window with a bounded 'violation' counter",
        explain=(
            "The window may contain at most one equal-neighbour pair. Adding a character on the right can create a "
            "new pair; removing from the left removes a pair only if the leftmost two characters were equal. Both "
            "updates are O(1), giving a linear sweep."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^3) time - count the pairs of every substring",
        brute=r"""
# BRUTE FORCE: O(n^3) time - count the pairs of every substring
def longest_semi_repetitive_substring(s):
    n = len(s)
    best = 1
    for i in range(n):
        for j in range(i + 1, n + 1):
            piece = s[i:j]
            pairs = sum(1 for k in range(len(piece) - 1) if piece[k] == piece[k + 1])
            if pairs <= 1:
                best = max(best, j - i)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Sliding window with a bounded 'violation' counter
def longest_semi_repetitive_substring(s):
    best = 1
    left = 0
    pairs = 0
    for right in range(1, len(s)):
        if s[right] == s[right - 1]:
            pairs += 1
        while pairs > 1:
            if s[left] == s[left + 1]:
                pairs -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
""",
    ),
    # ---- Continuous Subarrays (LeetCode 2762) ----
    dict(
        title="Continuous Subarrays",
        diff="M",
        lc=2762,
        slug="continuous-subarrays",
        prompt=(
            "A subarray is continuous if for every pair of its elements |a - b| <= 2 (equivalently max - min <= 2). "
            "Return the number of continuous subarrays."
        ),
        sig="def continuous_subarrays(nums: List[int]) -> int:",
        fn="continuous_subarrays",
        tests=[
            (([5, 4, 2, 4],), 8),
            (([1, 2, 3],), 6),
            (([1],), 1),
            (([1, 10],), 2),
        ],
        hints=[
            "The condition is just max - min <= 2 over the subarray.",
            (
                "If [l..r] is continuous so is every subarray inside it, so for each r the valid l's start at some "
                "minimum left."
            ),
            (
                "Keep the window's max and min with two monotonic deques; while max - min > 2 advance left. Add r - "
                "left + 1 for each r."
            ),
        ],
        pattern="Sliding window with monotonic deques for max and min",
        explain=(
            "Validity is monotone under shrinking, so for each right end there is a smallest left end and every "
            "left in between works; counting them contributes right - left + 1. Two monotonic deques report the "
            "window's maximum and minimum in O(1) amortised, which is what makes the sweep linear."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - extend every start while tracking max and min",
        brute=r"""
# BRUTE FORCE: O(n^2) time - extend every start while tracking max and min
def continuous_subarrays(nums):
    count = 0
    for i in range(len(nums)):
        hi = lo = nums[i]
        for j in range(i, len(nums)):
            hi = max(hi, nums[j])
            lo = min(lo, nums[j])
            if hi - lo > 2:
                break
            count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Sliding window with monotonic deques for max and min
def continuous_subarrays(nums):
    high = deque()
    low = deque()
    left = 0
    total = 0
    for right, x in enumerate(nums):
        while high and nums[high[-1]] <= x:
            high.pop()
        high.append(right)
        while low and nums[low[-1]] >= x:
            low.pop()
        low.append(right)
        while nums[high[0]] - nums[low[0]] > 2:
            left += 1
            if high[0] < left:
                high.popleft()
            if low[0] < left:
                low.popleft()
        total += right - left + 1
    return total
""",
    ),
    # ---- Count Complete Subarrays in an Array (LeetCode 2799) ----
    dict(
        title="Count Complete Subarrays in an Array",
        diff="M",
        lc=2799,
        slug="count-complete-subarrays-in-an-array",
        prompt=(
            "A subarray is complete if it contains as many distinct values as the whole array. Return the number of "
            "complete subarrays."
        ),
        sig="def count_complete_subarrays(nums: List[int]) -> int:",
        fn="count_complete_subarrays",
        tests=[
            (([1, 3, 1, 2, 2],), 4),
            (([5, 5, 5, 5],), 10),
            (([1, 2, 3],), 1),
            (([1, 2, 1],), 3),
        ],
        hints=[
            "Let D be the number of distinct values in the whole array.",
            "If [l..r] has D distinct values then so does every [l..r'] with r' > r.",
            (
                "For each left, find the smallest right that makes the window complete; it contributes n - right "
                "subarrays. Slide left forward and keep the right pointer where it is."
            ),
        ],
        pattern="'At least' sliding window: count all extensions of the minimal valid window",
        explain=(
            "Completeness is preserved when a window grows, so for each left there is a threshold right end and "
            "every later right end also works. Counting n - right for the first valid window, then advancing left, "
            "counts every complete subarray once. The distinct counter changes by one per move."
        ),
        cx="O(n) time, O(D) space",
        brute_cx="O(n^2) time - extend every start and track the distinct set",
        brute=r"""
# BRUTE FORCE: O(n^2) time - extend every start and track the distinct set
def count_complete_subarrays(nums):
    total_distinct = len(set(nums))
    count = 0
    for i in range(len(nums)):
        seen = set()
        for j in range(i, len(nums)):
            seen.add(nums[j])
            if len(seen) == total_distinct:
                count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n) time, O(D) space
# Idea: 'At least' sliding window: count all extensions of the minimal valid window
def count_complete_subarrays(nums):
    total_distinct = len(set(nums))
    window = Counter()
    left = 0
    count = 0
    for right, x in enumerate(nums):
        window[x] += 1
        while len(window) == total_distinct:
            count += len(nums) - right
            window[nums[left]] -= 1
            if window[nums[left]] == 0:
                del window[nums[left]]
            left += 1
    return count
""",
    ),
    # ---- Maximum Sum of Almost Unique Subarray (LeetCode 2841) ----
    dict(
        title="Maximum Sum of Almost Unique Subarray",
        diff="M",
        lc=2841,
        slug="maximum-sum-of-almost-unique-subarray",
        prompt=(
            "A subarray of length k is almost unique if it has at least m distinct elements. Return the maximum sum "
            "of an almost unique subarray of length exactly k, or 0 if there is none."
        ),
        sig="def max_sum(nums: List[int], m: int, k: int) -> int:",
        fn="max_sum",
        tests=[
            (([2, 6, 7, 3, 1, 7], 3, 4), 18),
            (([5, 9, 9, 2, 4, 5, 4], 1, 3), 23),
            (([1, 2, 1, 2, 1, 2, 1], 3, 3), 0),
            (([4], 1, 1), 4),
        ],
        hints=[
            "The window length is fixed at k.",
            "Maintain the window sum and a Counter of its elements as it slides.",
            "After each step, if the Counter has at least m keys, consider the window sum for the maximum.",
        ],
        pattern="Fixed-size sliding window with a sum and a distinct counter",
        explain=(
            "Each slide adds one element and removes one, so both the sum and the element counts update in O(1); "
            "the number of distinct values is the number of keys in the counter (delete keys that reach zero)."
        ),
        cx="O(n) time, O(k) space",
        brute_cx="O(n * k) time - recompute the sum and distinct count of every window",
        brute=r"""
# BRUTE FORCE: O(n * k) time - recompute the sum and distinct count of every window
def max_sum(nums, m, k):
    best = 0
    for i in range(len(nums) - k + 1):
        window = nums[i : i + k]
        if len(set(window)) >= m:
            best = max(best, sum(window))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(k) space
# Idea: Fixed-size sliding window with a sum and a distinct counter
def max_sum(nums, m, k):
    window = Counter()
    total = 0
    best = 0
    for i, x in enumerate(nums):
        window[x] += 1
        total += x
        if i >= k:
            old = nums[i - k]
            window[old] -= 1
            total -= old
            if window[old] == 0:
                del window[old]
        if i >= k - 1 and len(window) >= m:
            best = max(best, total)
    return best
""",
    ),
    # ---- Count Subarrays Where Max Element Appears at Least K Times (LeetCode 2962) ----
    dict(
        title="Count Subarrays Where Max Element Appears at Least K Times",
        diff="M",
        lc=2962,
        slug="count-subarrays-where-max-element-appears-at-least-k-times",
        prompt=(
            "Let M be the maximum value of nums. Return the number of subarrays in which M appears at least k times "
            "(k >= 1)."
        ),
        sig="def count_subarrays(nums: List[int], k: int) -> int:",
        fn="count_subarrays",
        tests=[
            (([1, 3, 2, 3, 3], 2), 6),
            (([1, 4, 2, 1], 3), 0),
            (([5], 1), 1),
            (([2, 2, 2], 2), 3),
        ],
        hints=[
            "Only the maximum of the WHOLE array matters, not each subarray's maximum.",
            "If [l..r] has at least k copies of M, so does [l'..r] for every l' <= l.",
            (
                "Sweep r, counting copies of M. While the window has >= k of them, move left forward; after the "
                "loop the number of valid starts for this r is exactly 'left'."
            ),
        ],
        pattern="'At least k' window: count valid starts per right end",
        explain=(
            "Once a window has k copies of the maximum, extending it to the left keeps it valid, so every start "
            "before the shrunk left pointer is valid for this right end. Shrinking until the count drops below k "
            "leaves left equal to the number of valid starts, and summing it over all right ends counts every "
            "subarray once."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - extend every start while counting the maximum",
        brute=r"""
# BRUTE FORCE: O(n^2) time - extend every start while counting the maximum
def count_subarrays(nums, k):
    top = max(nums)
    total = 0
    for i in range(len(nums)):
        seen = 0
        for j in range(i, len(nums)):
            if nums[j] == top:
                seen += 1
            if seen >= k:
                total += 1
    return total
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: 'At least k' window: count valid starts per right end
def count_subarrays(nums, k):
    top = max(nums)
    seen = 0
    left = 0
    total = 0
    for x in nums:
        if x == top:
            seen += 1
        while seen >= k:
            if nums[left] == top:
                seen -= 1
            left += 1
        total += left
    return total
""",
    ),
    # ---- Maximum Length Substring With Two Occurrences (LeetCode 3090) ----
    dict(
        title="Maximum Length Substring With Two Occurrences",
        diff="E",
        lc=3090,
        slug="maximum-length-substring-with-two-occurrences",
        prompt="Return the maximum length of a substring of s in which every character occurs at most twice.",
        sig="def maximum_length_substring(s: str) -> int:",
        fn="maximum_length_substring",
        tests=[
            (("bcbbbcba",), 4),
            (("aaaa",), 2),
            (("abc",), 3),
            (("aabbaabb",), 4),
        ],
        hints=[
            "Keep a count per character inside the window.",
            "Expand the right end; if the new character now appears 3 times, shrink from the left.",
            "Shrink only until that character's count drops back to 2.",
        ],
        pattern="Variable-size sliding window with per-character caps",
        explain=(
            "Only the character that was just added can violate the limit, so shrinking just until that one "
            "character is back to two occurrences restores validity. Each index enters and leaves the window once."
        ),
        cx="O(n) time, O(alphabet) space",
        brute_cx="O(n^3) time - check every substring",
        brute=r"""
# BRUTE FORCE: O(n^3) time - check every substring
def maximum_length_substring(s):
    best = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            if max(Counter(s[i:j]).values()) <= 2:
                best = max(best, j - i)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(alphabet) space
# Idea: Variable-size sliding window with per-character caps
def maximum_length_substring(s):
    count = Counter()
    left = 0
    best = 0
    for right, ch in enumerate(s):
        count[ch] += 1
        while count[ch] > 2:
            count[s[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
""",
    ),
    # ---- Find the Power of K-Size Subarrays I (LeetCode 3254) ----
    dict(
        title="Find the Power of K-Size Subarrays I",
        diff="M",
        lc=3254,
        slug="find-the-power-of-k-size-subarrays-i",
        prompt=(
            "The power of an array is its maximum element if its elements are consecutive integers in ascending "
            "order (x, x+1, x+2, ...), otherwise -1. Return an array where result[i] is the power of the subarray "
            "nums[i..i+k-1]."
        ),
        sig="def results_array(nums: List[int], k: int) -> List[int]:",
        fn="results_array",
        tests=[
            (([1, 2, 3, 4, 3, 2, 5], 3), [3, 4, -1, -1, -1]),
            (([2, 2, 2, 2, 2], 4), [-1, -1]),
            (([3, 2, 3, 2, 3, 2], 2), [-1, 3, -1, 3, -1]),
            (([5, 6], 1), [5, 6]),
        ],
        hints=[
            "A window is valid iff every adjacent pair inside it increases by exactly 1.",
            "Track the length of the current run of '+1 steps' ending at each index.",
            "A window ending at i is valid iff that run length is at least k; its power is nums[i].",
        ],
        pattern="Fixed window answered by a running 'streak length'",
        explain=(
            "Instead of re-checking every window, keep the length of the current streak of consecutive ascending "
            "values. A window of size k ending at i is valid exactly when the streak reaches back at least k "
            "elements, and then the maximum is simply nums[i]."
        ),
        cx="O(n) time, O(1) extra space",
        brute_cx="O(n * k) time - check every window",
        brute=r"""
# BRUTE FORCE: O(n * k) time - check every window
def results_array(nums, k):
    result = []
    for i in range(len(nums) - k + 1):
        window = nums[i : i + k]
        if all(window[t + 1] == window[t] + 1 for t in range(k - 1)):
            result.append(window[-1])
        else:
            result.append(-1)
    return result
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) extra space
# Idea: Fixed window answered by a running 'streak length'
def results_array(nums, k):
    result = [-1] * (len(nums) - k + 1)
    streak = 0
    for i, x in enumerate(nums):
        streak = streak + 1 if i > 0 and x == nums[i - 1] + 1 else 1
        if i >= k - 1 and streak >= k:
            result[i - k + 1] = x
    return result
""",
    ),
]
