"""more Sliding Window problems (batch 5) - part of the problem bank for the "sliding_window" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Get Equal Substrings Within Budget (LeetCode 1208) ----
    dict(
        title="Get Equal Substrings Within Budget",
        diff="M",
        lc=1208,
        slug="get-equal-substrings-within-budget",
        prompt=(
            "Changing s[i] into t[i] costs |s[i] - t[i]| (difference of their character codes). Return the maximum "
            "length of a substring of s that can be changed into the matching substring of t with total cost at "
            "most max_cost."
        ),
        sig="def equal_substring(s: str, t: str, max_cost: int) -> int:",
        fn="equal_substring",
        tests=[
            (("abcd", "bcdf", 3), 3),
            (("abcd", "cdef", 3), 1),
            (("abcd", "acde", 0), 1),
            (("a", "z", 5), 0),
        ],
        hints=[
            "Turn the strings into a cost array: cost[i] = |s[i] - t[i]|.",
            "Now: the longest subarray of cost[] with sum <= max_cost. All costs are non-negative.",
            "Sliding window: add cost[right]; while the sum exceeds max_cost remove cost[left] and advance left.",
        ],
        pattern="Variable-size sliding window (non-negative values)",
        explain=(
            "Because costs are non-negative, shrinking from the left can only reduce the sum, so the window is "
            "valid exactly when left is the smallest feasible start."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - sum every substring",
        brute=r"""
# BRUTE FORCE: O(n^2) time - sum every substring
def equal_substring(s, t, max_cost):
    best = 0
    for i in range(len(s)):
        cost = 0
        for j in range(i, len(s)):
            cost += abs(ord(s[j]) - ord(t[j]))
            if cost > max_cost:
                break
            best = max(best, j - i + 1)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Variable-size sliding window (non-negative values)
def equal_substring(s, t, max_cost):
    left = cost = best = 0
    for right in range(len(s)):
        cost += abs(ord(s[right]) - ord(t[right]))
        while cost > max_cost:  # shrink until the budget holds again
            cost -= abs(ord(s[left]) - ord(t[left]))
            left += 1
        best = max(best, right - left + 1)
    return best
""",
    ),
    # ---- Count Number of Nice Subarrays (LeetCode 1248) ----
    dict(
        title="Count Number of Nice Subarrays",
        diff="M",
        lc=1248,
        slug="count-number-of-nice-subarrays",
        prompt="A subarray is nice if it has exactly k odd numbers. Return the number of nice subarrays.",
        sig="def number_of_subarrays(nums: List[int], k: int) -> int:",
        fn="number_of_subarrays",
        tests=[
            (([1, 1, 2, 1, 1], 3), 2),
            (([2, 4, 6], 1), 0),
            (([2, 2, 2, 1, 2, 2, 1, 2, 2, 2], 2), 16),
            (([1], 1), 1),
            (([1, 2, 1], 1), 4),
        ],
        hints=[
            "Only the parity of each number matters.",
            "'Exactly k' is hard for a window, but 'at most k' is easy.",
            (
                "answer = atMost(k) - atMost(k - 1), where atMost(m) counts subarrays ending at each right end: "
                "right - left + 1."
            ),
        ],
        pattern="Exactly k = atMost(k) - atMost(k - 1)",
        explain=(
            "A window can count 'at most m odd numbers' because that property is monotone in the window size; "
            "subtracting two such counts isolates exactly k."
        ),
        cx="O(n) time",
        brute_cx="O(n^2) time - count odd numbers for every subarray",
        brute=r"""
# BRUTE FORCE: O(n^2) time - count odd numbers for every subarray
def number_of_subarrays(nums, k):
    count = 0
    for i in range(len(nums)):
        odd = 0
        for j in range(i, len(nums)):
            odd += nums[j] % 2
            if odd == k:
                count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Exactly k = atMost(k) - atMost(k - 1)
def number_of_subarrays(nums, k):
    def at_most(m):
        if m < 0:
            return 0
        left = odd = total = 0
        for right, x in enumerate(nums):
            odd += x & 1
            while odd > m:
                odd -= nums[left] & 1
                left += 1
            total += right - left + 1  # every start in [left, right] works
        return total

    return at_most(k) - at_most(k - 1)
""",
    ),
    # ---- Number of Substrings Containing All Three Characters (LeetCode 1358) ----
    dict(
        title="Number of Substrings Containing All Three Characters",
        diff="M",
        lc=1358,
        slug="number-of-substrings-containing-all-three-characters",
        prompt=(
            "s contains only 'a', 'b' and 'c'. Return the number of substrings that contain at least one of each "
            "letter."
        ),
        sig="def number_of_substrings(s: str) -> int:",
        fn="number_of_substrings",
        tests=[
            (("abcabc",), 10),
            (("aaacb",), 3),
            (("abc",), 1),
            (("ab",), 0),
            (("aaaa",), 0),
        ],
        hints=[
            "Fix the RIGHT end of the substring.",
            "The substring must start at or before the smallest of the last positions of a, b and c.",
            "Keep last[a], last[b], last[c]; for each right end, if all are seen add min(last) + 1.",
        ],
        pattern="Count by right endpoint using last-seen positions",
        explain=(
            "Any start up to the earliest 'most recent letter' still sees all three letters, so those starts are "
            "counted in one step."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - extend every start until all three letters appear",
        brute=r"""
# BRUTE FORCE: O(n^2) time - extend every start until all three letters appear
def number_of_substrings(s):
    count = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            if len(set(s[i : j + 1])) == 3:
                count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Count by right endpoint using last-seen positions
def number_of_substrings(s):
    last = {"a": -1, "b": -1, "c": -1}
    count = 0
    for i, ch in enumerate(s):
        last[ch] = i
        count += (
            min(last.values()) + 1
        )  # starts 0..min(last) contain all three (0 if one is unseen)
    return count
""",
    ),
    # ---- Maximum Points You Can Obtain from Cards (LeetCode 1423) ----
    dict(
        title="Maximum Points You Can Obtain from Cards",
        diff="M",
        lc=1423,
        slug="maximum-points-you-can-obtain-from-cards",
        prompt=(
            "From a row of cards you take exactly k cards, each time from either the left end or the right end. "
            "Return the maximum total points."
        ),
        sig="def max_score(card_points: List[int], k: int) -> int:",
        fn="max_score",
        tests=[
            (([1, 2, 3, 4, 5, 6, 1], 3), 12),
            (([2, 2, 2], 2), 4),
            (([9, 7, 7, 9, 7, 7, 9], 7), 55),
            (([1, 1000, 1], 1), 1),
        ],
        hints=[
            "Whatever you take is a prefix of length i plus a suffix of length k - i.",
            "Start with the first k cards, then trade them one by one for cards from the right end.",
            "Slide: total += card[-i] - card[k - i] for i = 1..k, tracking the maximum.",
        ],
        pattern="Fixed-size window over a circular view of the ends",
        explain=(
            "The k cards always form one contiguous block when the array is viewed as a circle; sliding it one step "
            "swaps exactly one card out and one in."
        ),
        cx="O(k) time, O(1) space",
        brute_cx="O(k^2) time - sum a prefix and a suffix for each split",
        brute=r"""
# BRUTE FORCE: O(k^2) time - sum a prefix and a suffix for each split
def max_score(card_points, k):
    n = len(card_points)
    return max(sum(card_points[:i]) + sum(card_points[n - (k - i) :]) for i in range(k + 1))
""",
        solution=r"""
# OPTIMISED: O(k) time, O(1) space
# Idea: Fixed-size window over a circular view of the ends
def max_score(card_points, k):
    total = sum(card_points[:k])  # all k from the left
    best = total
    for i in range(1, k + 1):
        total += card_points[-i] - card_points[k - i]  # swap one left card for one right card
        best = max(best, total)
    return best
""",
    ),
    # ---- Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit (LeetCode 1438) ----
    dict(
        title="Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit",
        diff="M",
        lc=1438,
        slug="longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit",
        prompt=(
            "Return the length of the longest subarray in which the absolute difference between any two elements is "
            "at most limit."
        ),
        sig="def longest_subarray(nums: List[int], limit: int) -> int:",
        fn="longest_subarray",
        tests=[
            (([8, 2, 4, 7], 4), 2),
            (([10, 1, 2, 4, 7, 2], 5), 4),
            (([4, 2, 2, 2, 4, 4, 2, 2], 0), 3),
            (([1], 5), 1),
        ],
        hints=[
            "Any two elements differ by at most limit exactly when max - min <= limit.",
            "A sliding window needs the max and min of the CURRENT window quickly.",
            (
                "Keep two monotonic deques of indices (one decreasing for the max, one increasing for the min); "
                "shrink from the left while max - min > limit."
            ),
        ],
        pattern="Sliding window + monotonic deques for min and max",
        explain=(
            "Each deque holds only candidates that could still become the extreme, so the window's max and min are "
            "always at the fronts in O(1)."
        ),
        cx="O(n) time",
        brute_cx="O(n^2) time - track min and max while extending each start",
        brute=r"""
# BRUTE FORCE: O(n^2) time - track min and max while extending each start
def longest_subarray(nums, limit):
    best = 0
    for i in range(len(nums)):
        lo = hi = nums[i]
        for j in range(i, len(nums)):
            lo, hi = min(lo, nums[j]), max(hi, nums[j])
            if hi - lo > limit:
                break
            best = max(best, j - i + 1)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Sliding window + monotonic deques for min and max
def longest_subarray(nums, limit):
    maxq, minq = deque(), deque()  # indices; values decreasing / increasing
    left = best = 0
    for right, x in enumerate(nums):
        while maxq and nums[maxq[-1]] <= x:
            maxq.pop()
        maxq.append(right)
        while minq and nums[minq[-1]] >= x:
            minq.pop()
        minq.append(right)
        while (
            nums[maxq[0]] - nums[minq[0]] > limit
        ):  # window too spread out: drop the oldest element
            left += 1
            if maxq[0] < left:
                maxq.popleft()
            if minq[0] < left:
                minq.popleft()
        best = max(best, right - left + 1)
    return best
""",
    ),
    # ---- Maximum Erasure Value (LeetCode 1695) ----
    dict(
        title="Maximum Erasure Value",
        diff="M",
        lc=1695,
        slug="maximum-erasure-value",
        prompt=(
            "Erase one subarray that contains only UNIQUE elements; your score is its sum. Return the maximum score."
        ),
        sig="def maximum_unique_subarray(nums: List[int]) -> int:",
        fn="maximum_unique_subarray",
        tests=[
            (([4, 2, 4, 5, 6],), 17),
            (([5, 2, 1, 2, 5, 2, 1, 2, 5],), 8),
            (([1],), 1),
            (([1, 1, 1],), 1),
        ],
        hints=[
            "A window is valid while it has no duplicate.",
            "Keep a set of the window's elements and its running sum.",
            (
                "When the new element is already in the set, remove elements from the left until it is gone; then "
                "add it and update the best sum."
            ),
        ],
        pattern="Sliding window with a set (unique elements)",
        explain=(
            "Each element enters and leaves the window at most once, so the total work is linear even though "
            "shrinking happens inside the loop."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - extend each start until a duplicate appears",
        brute=r"""
# BRUTE FORCE: O(n^2) time - extend each start until a duplicate appears
def maximum_unique_subarray(nums):
    best = 0
    for i in range(len(nums)):
        seen, total = set(), 0
        for j in range(i, len(nums)):
            if nums[j] in seen:
                break
            seen.add(nums[j])
            total += nums[j]
            best = max(best, total)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Sliding window with a set (unique elements)
def maximum_unique_subarray(nums):
    seen, left, total, best = set(), 0, 0, 0
    for x in nums:
        while x in seen:  # shrink until x is no longer a duplicate
            seen.remove(nums[left])
            total -= nums[left]
            left += 1
        seen.add(x)
        total += x
        best = max(best, total)
    return best
""",
    ),
    # ---- Minimum Operations to Reduce X to Zero (LeetCode 1658) ----
    dict(
        title="Minimum Operations to Reduce X to Zero",
        diff="M",
        lc=1658,
        slug="minimum-operations-to-reduce-x-to-zero",
        prompt=(
            "Each operation removes the leftmost or the rightmost element of nums and subtracts it from x. Return "
            "the minimum number of operations to make x exactly 0, or -1 if impossible."
        ),
        sig="def min_operations(nums: List[int], x: int) -> int:",
        fn="min_operations",
        tests=[
            (([1, 1, 4, 2, 3], 5), 2),
            (([5, 6, 7, 8, 9], 4), -1),
            (([3, 2, 20, 1, 1, 3], 10), 5),
            (([1], 1), 1),
            (([1, 1], 3), -1),
        ],
        hints=[
            "The removed elements are a prefix plus a suffix; what stays is a contiguous MIDDLE part.",
            "The middle part must sum to total - x, and to minimise removals you want it as LONG as possible.",
            "Longest subarray with sum == total - x (all numbers positive): classic sliding window.",
        ],
        pattern="Complement trick: longest middle subarray with a target sum",
        explain=(
            "Minimising what you take from the ends is the same as maximising what you keep in the middle, which a "
            "positive-number window finds in one pass."
        ),
        cx="O(n) time",
        brute_cx="O(n^3) time - try every (left count, right count) and sum them",
        brute=r"""
# BRUTE FORCE: O(n^3) time - try every (left count, right count) and sum them
def min_operations(nums, x):
    n, best = len(nums), float("inf")
    for i in range(n + 1):
        for j in range(n - i + 1):
            if sum(nums[:i]) + sum(nums[n - j :]) == x:
                best = min(best, i + j)
    return -1 if best == float("inf") else best
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Complement trick: longest middle subarray with a target sum
def min_operations(nums, x):
    target = sum(nums) - x
    if target < 0:
        return -1
    if target == 0:
        return len(nums)  # take everything
    left = cur = 0
    longest = -1
    for right, v in enumerate(nums):
        cur += v
        while cur > target:
            cur -= nums[left]
            left += 1
        if cur == target:
            longest = max(longest, right - left + 1)
    return -1 if longest == -1 else len(nums) - longest
""",
    ),
    # ---- Maximize the Confusion of an Exam (LeetCode 2024) ----
    dict(
        title="Maximize the Confusion of an Exam",
        diff="M",
        lc=2024,
        slug="maximize-the-confusion-of-an-exam",
        prompt=(
            "answer_key is a string of 'T' and 'F'. You may change at most k answers. Return the maximum number of "
            "consecutive equal answers you can obtain."
        ),
        sig="def max_consecutive_answers(answer_key: str, k: int) -> int:",
        fn="max_consecutive_answers",
        tests=[
            (("TTFF", 2), 4),
            (("TFFT", 1), 3),
            (("TTFTTFTT", 1), 5),
            (("T", 0), 1),
        ],
        hints=[
            "A final run of all-'T' (or all-'F') needs every other letter inside it flipped.",
            "So find the longest window containing at most k letters different from the target letter.",
            "Run a sliding window once for target 'T' and once for 'F'; the answer is the larger.",
        ],
        pattern="Longest window with at most k 'bad' elements (run for both targets)",
        explain=(
            "This is Longest Repeating Character Replacement specialised to two letters: the window may contain at "
            "most k flips."
        ),
        cx="O(n) time",
        brute_cx="O(n^2) time - expand from every start for both targets",
        brute=r"""
# BRUTE FORCE: O(n^2) time - expand from every start for both targets
def max_consecutive_answers(answer_key, k):
    best = 0
    for target in "TF":
        for i in range(len(answer_key)):
            flips = 0
            for j in range(i, len(answer_key)):
                if answer_key[j] != target:
                    flips += 1
                if flips > k:
                    break
                best = max(best, j - i + 1)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Longest window with at most k 'bad' elements (run for both targets)
def max_consecutive_answers(answer_key, k):
    def longest(target):
        left = flips = best = 0
        for right, ch in enumerate(answer_key):
            if ch != target:
                flips += 1
            while flips > k:
                if answer_key[left] != target:
                    flips -= 1
                left += 1
            best = max(best, right - left + 1)
        return best

    return max(longest("T"), longest("F"))
""",
    ),
    # ---- Minimum Recolors to Get K Consecutive Black Blocks (LeetCode 2379) ----
    dict(
        title="Minimum Recolors to Get K Consecutive Black Blocks",
        diff="E",
        lc=2379,
        slug="minimum-recolors-to-get-k-consecutive-black-blocks",
        prompt=(
            "blocks is a string of 'W' (white) and 'B' (black). One operation recolors a white block black. Return "
            "the minimum operations so that some k consecutive blocks are all black."
        ),
        sig="def minimum_recolors(blocks: str, k: int) -> int:",
        fn="minimum_recolors",
        tests=[
            (("WBBWWBBWBW", 7), 3),
            (("WBWBBBW", 2), 0),
            (("BBBB", 2), 0),
            (("W", 1), 1),
        ],
        hints=[
            "For a fixed window of size k the cost is its number of white blocks.",
            "You want the window with the FEWEST whites.",
            "Slide the window: add 1 when a 'W' enters, subtract 1 when a 'W' leaves; track the minimum.",
        ],
        pattern="Fixed-size sliding window",
        explain="Updating the count in O(1) per step avoids recounting each window from scratch.",
        cx="O(n) time",
        brute_cx="O(n * k) time - count the whites of every window",
        brute=r"""
# BRUTE FORCE: O(n * k) time - count the whites of every window
def minimum_recolors(blocks, k):
    return min(blocks[i : i + k].count("W") for i in range(len(blocks) - k + 1))
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Fixed-size sliding window
def minimum_recolors(blocks, k):
    whites = blocks[:k].count("W")
    best = whites
    for i in range(k, len(blocks)):
        whites += (blocks[i] == "W") - (blocks[i - k] == "W")  # one block enters, one leaves
        best = min(best, whites)
    return best
""",
    ),
    # ---- Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold (LeetCode 1343) ----
    dict(
        title="Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold",
        diff="M",
        lc=1343,
        slug="number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold",
        prompt="Count the subarrays of length k whose average is at least threshold.",
        sig="def num_of_subarrays(arr: List[int], k: int, threshold: int) -> int:",
        fn="num_of_subarrays",
        tests=[
            (([2, 2, 2, 2, 5, 5, 5, 8], 3, 4), 3),
            (([11, 13, 17, 23, 29, 31, 7, 5, 2, 3], 3, 5), 6),
            (([1], 1, 1), 1),
            (([1, 1], 2, 2), 0),
        ],
        hints=[
            "average >= threshold  <=>  sum >= k * threshold (no division).",
            "Computing each window's sum from scratch costs O(k).",
            "Keep a running window sum: add the new element and subtract the one that left.",
        ],
        pattern="Fixed-size sliding window sum",
        explain="Each shift changes the sum by two numbers, so every window costs O(1).",
        cx="O(n) time",
        brute_cx="O(n * k) time - re-sum every window",
        brute=r"""
# BRUTE FORCE: O(n * k) time - re-sum every window
def num_of_subarrays(arr, k, threshold):
    return sum(1 for i in range(len(arr) - k + 1) if sum(arr[i : i + k]) >= k * threshold)
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Fixed-size sliding window sum
def num_of_subarrays(arr, k, threshold):
    need = k * threshold
    window = sum(arr[:k])
    count = 1 if window >= need else 0
    for i in range(k, len(arr)):
        window += arr[i] - arr[i - k]
        if window >= need:
            count += 1
    return count
""",
    ),
    # ---- Maximum Sum of Distinct Subarrays With Length K (LeetCode 2461) ----
    dict(
        title="Maximum Sum of Distinct Subarrays With Length K",
        diff="M",
        lc=2461,
        slug="maximum-sum-of-distinct-subarrays-with-length-k",
        prompt=(
            "Return the maximum sum over all subarrays of length exactly k whose elements are all distinct (0 if "
            "there is no such subarray)."
        ),
        sig="def maximum_subarray_sum(nums: List[int], k: int) -> int:",
        fn="maximum_subarray_sum",
        tests=[
            (([1, 5, 4, 2, 9, 9, 9], 3), 15),
            (([4, 4, 4], 3), 0),
            (([1, 2], 2), 3),
            (([1, 1], 2), 0),
        ],
        hints=[
            "Window of fixed size k: it is valid when it holds k DIFFERENT values.",
            "Maintain a Counter of the window and its sum.",
            (
                "When an element leaves, decrement its count and delete it at 0; the window is distinct iff the "
                "Counter has exactly k keys."
            ),
        ],
        pattern="Fixed window + frequency map",
        explain=(
            "The number of keys in the counter equals the number of distinct values, so the distinctness test is O(1)."
        ),
        cx="O(n) time, O(k) space",
        brute_cx="O(n * k) time - build a set for every window",
        brute=r"""
# BRUTE FORCE: O(n * k) time - build a set for every window
def maximum_subarray_sum(nums, k):
    best = 0
    for i in range(len(nums) - k + 1):
        window = nums[i : i + k]
        if len(set(window)) == k:
            best = max(best, sum(window))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(k) space
# Idea: Fixed window + frequency map
def maximum_subarray_sum(nums, k):
    counts, total, best = Counter(), 0, 0
    for right, x in enumerate(nums):
        counts[x] += 1
        total += x
        if right >= k:  # the element k steps back leaves the window
            old = nums[right - k]
            counts[old] -= 1
            total -= old
            if counts[old] == 0:
                del counts[old]
        if right >= k - 1 and len(counts) == k:
            best = max(best, total)
    return best
""",
    ),
    # ---- Length of Longest Subarray With at Most K Frequency (LeetCode 2958) ----
    dict(
        title="Length of Longest Subarray With at Most K Frequency",
        diff="M",
        lc=2958,
        slug="length-of-longest-subarray-with-at-most-k-frequency",
        prompt=(
            "A subarray is good if every value appears at most k times in it. Return the length of the longest good "
            "subarray."
        ),
        sig="def max_subarray_length(nums: List[int], k: int) -> int:",
        fn="max_subarray_length",
        tests=[
            (([1, 2, 3, 1, 2, 3, 1, 2], 2), 6),
            (([1, 2, 1, 2, 1, 2, 1, 2], 1), 2),
            (([5, 5, 5, 5, 5, 5, 5], 4), 4),
            (([1], 1), 1),
        ],
        hints=[
            "Being good is monotone: removing elements from a good window keeps it good.",
            "Track counts in the window.",
            (
                "After adding nums[right], while its count exceeds k, remove elements from the left (decrementing "
                "counts) and move left."
            ),
        ],
        pattern="Variable window with a frequency cap",
        explain=(
            "Only the newly added value can break the rule, so shrinking until its count is back to k restores "
            "validity."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - extend each start until some value exceeds k copies",
        brute=r"""
# BRUTE FORCE: O(n^2) time - extend each start until some value exceeds k copies
def max_subarray_length(nums, k):
    best = 0
    for i in range(len(nums)):
        counts = Counter()
        for j in range(i, len(nums)):
            counts[nums[j]] += 1
            if counts[nums[j]] > k:
                break
            best = max(best, j - i + 1)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Variable window with a frequency cap
def max_subarray_length(nums, k):
    counts, left, best = Counter(), 0, 0
    for right, x in enumerate(nums):
        counts[x] += 1
        while counts[x] > k:  # x is over the cap: drop elements from the left
            counts[nums[left]] -= 1
            left += 1
        best = max(best, right - left + 1)
    return best
""",
    ),
    # ---- Minimum Difference Between Highest and Lowest of K Scores (LeetCode 1984) ----
    dict(
        title="Minimum Difference Between Highest and Lowest of K Scores",
        diff="E",
        lc=1984,
        slug="minimum-difference-between-highest-and-lowest-of-k-scores",
        prompt=(
            "Choose any k scores from nums. Return the minimum possible difference between the highest and the "
            "lowest of the chosen scores."
        ),
        sig="def minimum_difference(nums: List[int], k: int) -> int:",
        fn="minimum_difference",
        tests=[
            (([90], 1), 0),
            (([9, 4, 1, 7], 2), 2),
            (([87063, 61094, 44530, 21297, 95857, 93551, 9918], 6), 74560),
            (([1, 2, 3], 3), 2),
        ],
        hints=[
            "The chosen scores should be close to each other in VALUE.",
            "After sorting, the best k scores are always consecutive in sorted order.",
            "Slide a window of size k over the sorted array: minimise nums[i + k - 1] - nums[i].",
        ],
        pattern="Sort + fixed-size window",
        explain=(
            "If a chosen set skipped a middle value, adding it in place of an extreme would not widen the range, so "
            "optimal sets are contiguous in sorted order."
        ),
        cx="O(n log n) time",
        brute_cx="O(C(n, k) * k) time - try every subset of k scores",
        brute=r"""
# BRUTE FORCE: O(C(n, k) * k) time - try every subset of k scores
def minimum_difference(nums, k):
    return min(max(c) - min(c) for c in itertools.combinations(nums, k))
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Sort + fixed-size window
def minimum_difference(nums, k):
    nums = sorted(nums)
    return min(nums[i + k - 1] - nums[i] for i in range(len(nums) - k + 1))
""",
    ),
]
