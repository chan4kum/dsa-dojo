from core import *

PROBLEMS = [
    dict(
        title="Maximum Average Subarray I", diff="E", lc=643, slug="maximum-average-subarray-i",
        prompt="Find the contiguous subarray of exactly length k with the largest average and return that average.",
        sig="def find_max_average(nums: List[int], k: int) -> float:",
        fn="find_max_average", compare="float",
        tests=[(([1, 12, -5, -6, 50, 3], 4), 12.75), (([5], 1), 5.0), (([0, 4, 0, 3, 2], 1), 4.0), (([-1, -2, -3], 2), -1.5)],
        hints=["Summing each window from scratch costs O(n*k).",
               "Consecutive windows share k-1 elements. What changes when the window slides by one?",
               "window_sum += nums[i] - nums[i-k]; track the max sum, divide by k at the end."],
        pattern="Fixed-size sliding window (add the entering element, remove the leaving one)",
        explain="""
        Maintain the window's sum incrementally: when the right edge enters index i, the element at i-k leaves.
        Each element is added once and removed once: O(n) time, O(1) space.""",
        solution=r'''
def find_max_average(nums, k):
    window = sum(nums[:k])
    best = window
    for i in range(k, len(nums)):
        window += nums[i] - nums[i - k]
        best = max(best, window)
    return best / k
''',
    ),
    dict(
        title="Longest Substring Without Repeating Characters", diff="M", lc=3,
        slug="longest-substring-without-repeating-characters",
        prompt="Return the length of the longest substring of s in which no character appears twice.",
        sig="def length_of_longest_substring(s: str) -> int:",
        fn="length_of_longest_substring",
        tests=[(("abcabcbb",), 3), (("bbbbb",), 1), (("pwwkew",), 3), (("",), 0), (("abba",), 2), (("dvdf",), 3)],
        hints=["Checking every substring is O(n^2) or worse. The window [l, r] should always be 'valid' (all unique).",
               "Expand r each step. If s[r] is already inside the window, move l forward until it is not.",
               "Store each char's last index: on a repeat, jump l to max(l, last[c]+1) in O(1)."],
        pattern="Variable-size sliding window with a 'last seen' map (expand right, shrink left to restore validity)",
        explain="""
        Invariant: s[l..r] has no duplicates. When s[r] already occurs inside the window at index j, the
        window must start after j, so l = max(l, j+1). The max() matters ('abba': the old 'a' is already
        outside the window). Each index is visited once: O(n) time, O(alphabet) space.""",
        solution=r'''
def length_of_longest_substring(s):
    last = {}
    l = best = 0
    for r, c in enumerate(s):
        if c in last and last[c] >= l:     # duplicate inside the window
            l = last[c] + 1
        last[c] = r
        best = max(best, r - l + 1)
    return best
''',
    ),
    dict(
        title="Minimum Size Subarray Sum", diff="M", lc=209, slug="minimum-size-subarray-sum",
        prompt="Given positive integers and a target, return the length of the shortest contiguous subarray "
               "whose sum is at least target, or 0 if there is none.",
        sig="def min_subarray_len(target: int, nums: List[int]) -> int:",
        fn="min_subarray_len",
        tests=[((7, [2, 3, 1, 2, 4, 3]), 2), ((4, [1, 4, 4]), 1), ((11, [1, 1, 1, 1, 1, 1, 1, 1]), 0),
               ((15, [1, 2, 3, 4, 5]), 5), ((3, [1, 1]), 0)],
        hints=["All numbers are positive - what does that say about extending or shrinking a window?",
               "Growing the window can only increase the sum; shrinking can only decrease it. That monotonicity is the key.",
               "Add nums[r]; while sum >= target, record the length and drop nums[l]."],
        pattern="Variable window that SHRINKS while the condition holds (needs non-negative values)",
        explain="""
        Because values are positive, the sum is monotonic in window size, so for each right end the smallest
        valid left end only moves right. Two pointers each go through the array once: O(n).
        (With negatives this breaks - use prefix sums + a deque/ordered structure instead.)""",
        solution=r'''
def min_subarray_len(target, nums):
    l = total = 0
    best = float("inf")
    for r, x in enumerate(nums):
        total += x
        while total >= target:             # shrink while still valid
            best = min(best, r - l + 1)
            total -= nums[l]
            l += 1
    return 0 if best == float("inf") else best
''',
    ),
    dict(
        title="Minimum Window Substring", diff="H", lc=76, slug="minimum-window-substring",
        prompt="Return the shortest substring of s that contains every character of t (with multiplicity). "
               "Return '' if there is none.",
        sig="def min_window(s: str, t: str) -> str:",
        fn="min_window",
        tests=[(("ADOBECODEBANC", "ABC"), "BANC"), (("a", "a"), "a"), (("a", "aa"), ""), (("aa", "aa"), "aa"),
               (("abc", "b"), "b")],
        hints=["Track how many required characters are still missing from the window.",
               "Expand r until nothing is missing; then shrink l as far as the window stays valid, recording the best.",
               "Counter need[c] (may go negative = surplus) plus an integer `missing`; window is valid when missing == 0."],
        pattern="Variable window: expand until valid, then shrink to the minimum while still valid",
        explain="""
        need[c] = how many more of c the window needs (negative = surplus). `missing` counts unmet characters,
        so validity is an O(1) check. After becoming valid, shrink from the left while the leftmost char is
        surplus (need < 0); that is the smallest window ending at r. Record it, then drop one needed char to
        continue. Time O(|s| + |t|).""",
        solution=r'''
def min_window(s, t):
    need = Counter(t)
    missing = len(t)
    l = 0
    best = (float("inf"), 0, 0)
    for r, c in enumerate(s):
        if need[c] > 0:
            missing -= 1
        need[c] -= 1
        if missing == 0:                       # window s[l..r] covers t
            while need[s[l]] < 0:              # drop surplus chars on the left
                need[s[l]] += 1
                l += 1
            if r - l + 1 < best[0]:
                best = (r - l + 1, l, r + 1)
            need[s[l]] += 1                    # give up one needed char -> invalid again
            missing += 1
            l += 1
    return "" if best[0] == float("inf") else s[best[1]:best[2]]
''',
    ),
]
