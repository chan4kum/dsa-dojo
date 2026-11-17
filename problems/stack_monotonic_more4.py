"""more Stack / Monotonic Stack problems (batch 5) - part of the problem bank for the "stack_monotonic" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Remove All Adjacent Duplicates in String II (LeetCode 1209) ----
    dict(
        title="Remove All Adjacent Duplicates in String II",
        diff="M",
        lc=1209,
        slug="remove-all-adjacent-duplicates-in-string-ii",
        prompt=(
            "Repeatedly delete k adjacent equal characters (the rest closes up) until no more can be deleted. "
            "Return the final string."
        ),
        sig="def remove_duplicates(s: str, k: int) -> str:",
        fn="remove_duplicates",
        tests=[
            (("abcd", 2), "abcd"),
            (("deeedbbcccbdaa", 3), "aa"),
            (("pbbcggttciiippooaais", 2), "ps"),
            (("aaa", 3), ""),
            (("aaaa", 3), "a"),
        ],
        hints=[
            "Deleting may create NEW adjacent groups, so one left-to-right scan with a simple counter is not enough.",
            "Keep a stack of [character, run length] for the string built so far.",
            (
                "For each character: if it equals the top, increment the run; when the run reaches k pop it. "
                "Otherwise push [char, 1]."
            ),
        ],
        pattern="Stack of (value, count)",
        explain=(
            "The stack always represents the fully reduced prefix, so a deletion only ever affects its top and the "
            "next character sees the right neighbour."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2 / k) time - rescan and delete until nothing changes",
        brute=r"""
# BRUTE FORCE: O(n^2 / k) time - rescan and delete until nothing changes
def remove_duplicates(s, k):
    changed = True

    while changed:
        changed = False
        i = 0

        while i + k <= len(s):
            if len(set(s[i : i + k])) == 1:  # k equal characters in a row
                s = s[:i] + s[i + k :]
                changed = True
                break
            i += 1

    return s
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Stack of (value, count)
def remove_duplicates(s, k):
    stack = []  # [character, run length]

    for ch in s:
        if stack and stack[-1][0] == ch:
            stack[-1][1] += 1
            if stack[-1][1] == k:
                stack.pop()  # a full group disappears
        else:
            stack.append([ch, 1])

    return "".join(ch * count for ch, count in stack)
""",
    ),
    # ---- Score of Parentheses (LeetCode 856) ----
    dict(
        title="Score of Parentheses",
        diff="M",
        lc=856,
        slug="score-of-parentheses",
        prompt=(
            "Score a balanced parentheses string: '()' = 1, 'AB' = score(A) + score(B), '(A)' = 2 * score(A). "
            "Return the score."
        ),
        sig="def score_of_parentheses(s: str) -> int:",
        fn="score_of_parentheses",
        tests=[
            (("()",), 1),
            (("(())",), 2),
            (("()()",), 2),
            (("(()(()))",), 6),
            (("()(())",), 3),
        ],
        hints=[
            "The rules are recursive: split into balanced pieces, double what is inside parentheses.",
            "Doubling happens once per nesting level, so a '()' at depth d is worth 2^d in the final sum.",
            "Track the depth; whenever you see '()' directly, add 1 << depth (the depth before opening it).",
        ],
        pattern="Depth counting instead of explicit recursion",
        explain=(
            "Every unit of score comes from an innermost '()' that is multiplied by 2 for each enclosing pair, so "
            "the answer is the sum of 2^depth over all innermost pairs."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - recursive splitting into balanced pieces",
        brute=r"""
# BRUTE FORCE: O(n^2) time - recursive splitting into balanced pieces
def score_of_parentheses(s):
    def score(left, right):  # s[left:right] is balanced
        total, i = 0, left

        while i < right:
            depth, j = 0, i

            while True:  # find the matching ')' of s[i]
                depth += 1 if s[j] == "(" else -1
                if depth == 0:
                    break
                j += 1

            inner = score(i + 1, j)
            total += 1 if j == i + 1 else 2 * inner
            i = j + 1

        return total

    return score(0, len(s))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Depth counting instead of explicit recursion
def score_of_parentheses(s):
    total = depth = 0

    for i, ch in enumerate(s):
        if ch == "(":
            depth += 1
        else:
            depth -= 1
            if s[i - 1] == "(":  # an innermost '()'
                total += 1 << depth

    return total
""",
    ),
    # ---- Reverse Substrings Between Each Pair of Parentheses (LeetCode 1190) ----
    dict(
        title="Reverse Substrings Between Each Pair of Parentheses",
        diff="M",
        lc=1190,
        slug="reverse-substrings-between-each-pair-of-parentheses",
        prompt=(
            "s has lowercase letters and balanced parentheses. Reverse the text inside every pair of parentheses, "
            "starting from the innermost pair, and return the result without any parentheses."
        ),
        sig="def reverse_parentheses(s: str) -> str:",
        fn="reverse_parentheses",
        tests=[
            (("(abcd)",), "dcba"),
            (("(u(love)i)",), "iloveu"),
            (("(ed(et(oc))el)",), "leetcode"),
            (("a(bcdefghijkl(mno)p)q",), "apmnolkjihgfedcbq"),
            (("abc",), "abc"),
        ],
        hints=[
            "Brute force: find the innermost pair, reverse it, repeat - O(n^2).",
            "First match every '(' with its ')' using a stack.",
            (
                "Walk the string; on a parenthesis JUMP to its partner and flip the walking direction. Letters met "
                "on the way are appended."
            ),
        ],
        pattern="Pair matching + 'teleport and reverse direction' walk",
        explain=(
            "Reversing nested substrings is equivalent to walking through the text and bouncing between matching "
            "parentheses, flipping direction each time: every character is visited once."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - repeatedly reverse the innermost pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - repeatedly reverse the innermost pair
def reverse_parentheses(s):
    while "(" in s:
        close = s.index(")")  # the first ')' closes an innermost pair
        open_ = s.rindex("(", 0, close)
        s = s[:open_] + s[open_ + 1 : close][::-1] + s[close + 1 :]
    return s
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Pair matching + 'teleport and reverse direction' walk
def reverse_parentheses(s):
    partner, stack = {}, []

    for i, ch in enumerate(s):
        if ch == "(":
            stack.append(i)
        elif ch == ")":
            j = stack.pop()
            partner[i], partner[j] = j, i  # remember both directions

    out, i, step = [], 0, 1

    while 0 <= i < len(s):
        if s[i] in "()":
            i = partner[i]  # jump to the matching parenthesis
            step = -step  # and walk the other way
        else:
            out.append(s[i])
        i += step

    return "".join(out)
""",
    ),
    # ---- Removing Stars From a String (LeetCode 2390) ----
    dict(
        title="Removing Stars From a String",
        diff="M",
        lc=2390,
        slug="removing-stars-from-a-string",
        prompt=(
            "In one operation a '*' removes itself and the closest non-star character to its left. Apply all "
            "operations and return the string."
        ),
        sig="def remove_stars(s: str) -> str:",
        fn="remove_stars",
        tests=[
            (("leet**cod*e",), "lecoe"),
            (("erase*****",), ""),
            (("abc",), "abc"),
            (("a*b*c",), "c"),
        ],
        hints=[
            "The 'closest character to the left' is the most recently kept one.",
            "That is exactly the top of a stack.",
            "Push letters; on '*' pop. The stack is the answer.",
        ],
        pattern="Stack as an undo buffer",
        explain=(
            "Each star cancels the latest surviving letter, which is the top of the stack; one pass processes "
            "everything."
        ),
        cx="O(n) time",
        brute_cx="O(n^2) time - repeatedly find the first star and delete it with its left neighbour",
        brute=r"""
# BRUTE FORCE: O(n^2) time - repeatedly find the first star and delete it with its left neighbour
def remove_stars(s):
    while "*" in s:
        i = s.index("*")
        s = s[: i - 1] + s[i + 1 :]  # drop the star and the letter before it
    return s
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Stack as an undo buffer
def remove_stars(s):
    stack = []
    for ch in s:
        if ch == "*":
            stack.pop()
        else:
            stack.append(ch)
    return "".join(stack)
""",
    ),
    # ---- Exclusive Time of Functions (LeetCode 636) ----
    dict(
        title="Exclusive Time of Functions",
        diff="M",
        lc=636,
        slug="exclusive-time-of-functions",
        prompt=(
            "A single-threaded CPU runs n functions (ids 0..n-1) that may call each other. logs are strings "
            "'id:start:t' or 'id:end:t' in the order the events happened; a function starts at the BEGINNING of "
            "time unit t and ends at the END of unit t. Return, for every function, its exclusive time (time units "
            "spent running it, not its callees)."
        ),
        sig="def exclusive_time(n: int, logs: List[str]) -> List[int]:",
        fn="exclusive_time",
        tests=[
            ((2, ["0:start:0", "1:start:2", "1:end:5", "0:end:6"]), [3, 4]),
            ((1, ["0:start:0", "0:start:2", "0:end:5", "0:start:6", "0:end:6", "0:end:7"]), [8]),
            ((2, ["0:start:0", "0:start:2", "0:end:5", "1:start:6", "1:end:6", "0:end:7"]), [7, 1]),
        ],
        hints=[
            "The function that is running is always the most recently started one that has not ended.",
            "Keep a stack of running function ids and the timestamp `prev` of the last event.",
            (
                "On a start: credit (t - prev) to the function on top, then push. On an end: credit (t - prev + 1) "
                "to the top, pop, and set prev = t + 1."
            ),
        ],
        pattern="Call-stack simulation with timestamps",
        explain=(
            "Time between two consecutive events belongs entirely to whichever function was on top, so each event "
            "only needs to settle the interval since the previous one."
        ),
        cx="O(L) time, O(depth) space",
        brute_cx="O(T) time - simulate every single time unit",
        brute=r"""
# BRUTE FORCE: O(T) time - simulate every single time unit
def exclusive_time(n, logs):
    events = []

    for log in logs:
        fid, kind, ts = log.split(":")
        events.append((int(ts), kind, int(fid)))

    result, stack, i = [0] * n, [], 0

    for now in range(events[-1][0] + 1):  # one iteration per time unit
        while i < len(events) and events[i][0] == now and events[i][1] == "start":
            stack.append(events[i][2])
            i += 1

        if stack:
            result[stack[-1]] += 1  # the top function ran during this unit

        while i < len(events) and events[i][0] == now and events[i][1] == "end":
            stack.pop()
            i += 1

    return result
""",
        solution=r"""
# OPTIMISED: O(L) time, O(depth) space
# Idea: Call-stack simulation with timestamps
def exclusive_time(n, logs):
    result, stack, prev = [0] * n, [], 0

    for log in logs:
        fid, kind, ts = log.split(":")
        fid, ts = int(fid), int(ts)

        if kind == "start":
            if stack:
                result[stack[-1]] += ts - prev  # the caller ran until now
            stack.append(fid)
            prev = ts
        else:
            result[stack.pop()] += ts - prev + 1  # end is inclusive
            prev = ts + 1

    return result
""",
    ),
    # ---- Longest Well-Performing Interval (LeetCode 1124) ----
    dict(
        title="Longest Well-Performing Interval",
        diff="M",
        lc=1124,
        slug="longest-well-performing-interval",
        prompt=(
            "hours[i] is the hours worked on day i. A day is tiring if hours > 8. An interval is well-performing if "
            "it has MORE tiring days than non-tiring days. Return the length of the longest well-performing "
            "interval."
        ),
        sig="def longest_wpi(hours: List[int]) -> int:",
        fn="longest_wpi",
        tests=[
            (([9, 9, 6, 0, 6, 6, 9],), 3),
            (([6, 6, 6],), 0),
            (([9],), 1),
            (([9, 6, 9],), 3),
            (([6, 9, 9, 6],), 3),
        ],
        hints=[
            "Score a tiring day +1 and any other day -1. A good interval has a positive sum.",
            "Use prefix sums: interval (j, i] is good when prefix[i] - prefix[j] > 0.",
            (
                "If prefix[i] > 0 the whole prefix works. Otherwise you need the EARLIEST j with prefix[j] = "
                "prefix[i] - 1 (store first occurrences; prefix values change by 1 so smaller ones appear first)."
            ),
        ],
        pattern="Prefix sums + first-occurrence map (+1/-1 walk)",
        explain=(
            "Because the prefix changes by exactly 1 each step, the earliest index with value prefix[i] - 1 is also "
            "the earliest index with any smaller value, so one dictionary lookup suffices."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - test every interval",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every interval
def longest_wpi(hours):
    best = 0

    for i in range(len(hours)):
        score = 0
        for j in range(i, len(hours)):
            score += 1 if hours[j] > 8 else -1
            if score > 0:
                best = max(best, j - i + 1)

    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Prefix sums + first-occurrence map (+1/-1 walk)
def longest_wpi(hours):
    score = best = 0
    first = {}  # prefix score -> first index where it appeared

    for i, h in enumerate(hours):
        score += 1 if h > 8 else -1
        if score > 0:
            best = i + 1  # the whole prefix is good
        else:
            first.setdefault(score, i)
            if score - 1 in first:
                best = max(best, i - first[score - 1])

    return best
""",
    ),
    # ---- Maximum Width Ramp (LeetCode 962) ----
    dict(
        title="Maximum Width Ramp",
        diff="M",
        lc=962,
        slug="maximum-width-ramp",
        prompt=(
            "A ramp is a pair (i, j) with i < j and nums[i] <= nums[j]; its width is j - i. Return the maximum "
            "width of a ramp (0 if there is none)."
        ),
        sig="def max_width_ramp(nums: List[int]) -> int:",
        fn="max_width_ramp",
        tests=[
            (([6, 0, 8, 2, 1, 5],), 4),
            (([9, 8, 1, 0, 1, 9, 4, 0, 4, 1],), 7),
            (([1, 1],), 1),
            (([3, 2, 1],), 0),
        ],
        hints=[
            "Checking every pair is O(n^2).",
            (
                "Only indices that are strict prefix MINIMA can be the left end of a best ramp (a smaller earlier "
                "value would be better)."
            ),
            (
                "Build a decreasing stack of those candidates, then scan j from the right; while nums[stack top] <= "
                "nums[j], pop and record j - i."
            ),
        ],
        pattern="Monotonic stack of candidates + right-to-left scan",
        explain=(
            "Candidates for the left end form a decreasing sequence; scanning j from the right, each candidate is "
            "popped the first (widest) time it can be matched."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - try every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - try every pair
def max_width_ramp(nums):
    best = 0
    for i in range(len(nums)):
        for j in range(len(nums) - 1, i, -1):
            if nums[i] <= nums[j]:
                best = max(best, j - i)
                break  # the first hit from the right is the widest for this i
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic stack of candidates + right-to-left scan
def max_width_ramp(nums):
    stack = []  # indices of strictly decreasing prefix minima

    for i, x in enumerate(nums):
        if not stack or x < nums[stack[-1]]:
            stack.append(i)

    best = 0

    for j in range(len(nums) - 1, -1, -1):
        while stack and nums[stack[-1]] <= nums[j]:
            best = max(
                best, j - stack.pop()
            )  # widest ramp ending at j (or further right) for this left end

    return best
""",
    ),
    # ---- Find the Most Competitive Subsequence (LeetCode 1673) ----
    dict(
        title="Find the Most Competitive Subsequence",
        diff="M",
        lc=1673,
        slug="find-the-most-competitive-subsequence",
        prompt=(
            "A sequence is more competitive than another of the same length if at the first differing position it "
            "has the smaller number. Return the most competitive subsequence of nums of length k."
        ),
        sig="def most_competitive(nums: List[int], k: int) -> List[int]:",
        fn="most_competitive",
        tests=[
            (([3, 5, 2, 6], 2), [2, 6]),
            (([2, 4, 3, 3, 5, 4, 9, 6], 4), [2, 3, 3, 4]),
            (([1], 1), [1]),
            (([5, 4, 3], 2), [4, 3]),
        ],
        hints=[
            "It is the lexicographically smallest subsequence of length k.",
            "Same idea as 'Remove K Digits': drop a larger earlier element when a smaller one arrives.",
            (
                "Monotonic stack: pop while stack top > x AND enough elements remain to still fill k; push x if the "
                "stack has fewer than k items."
            ),
        ],
        pattern="Monotonic stack with a length budget",
        explain=(
            "Replacing a larger earlier value by a smaller later one improves the prefix; the budget check "
            "(len(stack) - 1 + remaining >= k) keeps the final length reachable."
        ),
        cx="O(n) time, O(k) space",
        brute_cx="O(C(n, k) * k) time - compare every subsequence of length k",
        brute=r"""
# BRUTE FORCE: O(C(n, k) * k) time - compare every subsequence of length k
def most_competitive(nums, k):
    return list(min(itertools.combinations(nums, k)))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(k) space
# Idea: Monotonic stack with a length budget
def most_competitive(nums, k):
    stack, n = [], len(nums)
    for i, x in enumerate(nums):
        while stack and stack[-1] > x and len(stack) - 1 + (n - i) >= k:
            stack.pop()  # a smaller value can still complete the length
        if len(stack) < k:
            stack.append(x)
    return stack
""",
    ),
    # ---- Number of Visible People in a Queue (LeetCode 1944) ----
    dict(
        title="Number of Visible People in a Queue",
        diff="H",
        lc=1944,
        slug="number-of-visible-people-in-a-queue",
        prompt=(
            "People with DISTINCT heights stand in a queue facing right. Person i can see person j > i if everyone "
            "strictly between them is shorter than BOTH i and j. Return, for each person, how many people they can "
            "see."
        ),
        sig="def can_see_persons_count(heights: List[int]) -> List[int]:",
        fn="can_see_persons_count",
        tests=[
            (([10, 6, 8, 5, 11, 9],), [3, 1, 2, 1, 1, 0]),
            (([5, 1, 2, 3, 10],), [4, 1, 1, 1, 0]),
            (([1],), [0]),
            (([3, 2, 1],), [1, 1, 0]),
        ],
        hints=[
            (
                "Person i sees a chain of 'record-breaking' heights to the right, ending at the first person taller "
                "than i."
            ),
            "Process from the right with a stack of heights that are still visible from the left.",
            (
                "For height h: pop everyone shorter than h (each popped one is seen: count them); if the stack is "
                "still non-empty its top is seen too (+1); then push h."
            ),
        ],
        pattern="Monotonic stack processed right to left",
        explain=(
            "The stack holds exactly the people visible to anyone standing just to its left, in decreasing height. "
            "Popped people are hidden from everyone further left but were seen by the current person."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - scan to the right and track the tallest person in between",
        brute=r"""
# BRUTE FORCE: O(n^2) time - scan to the right and track the tallest person in between
def can_see_persons_count(heights):
    result = []

    for i in range(len(heights)):
        seen, between_max = 0, 0

        for j in range(i + 1, len(heights)):
            if between_max < min(heights[i], heights[j]):
                seen += 1  # nobody in between blocks the view
            between_max = max(between_max, heights[j])
            if between_max > heights[i]:
                break

        result.append(seen)

    return result
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic stack processed right to left
def can_see_persons_count(heights):
    result, stack = [0] * len(heights), []  # stack: heights visible to the left, decreasing

    for i in range(len(heights) - 1, -1, -1):
        seen = 0

        while stack and stack[-1] < heights[i]:
            stack.pop()  # shorter people: seen, but hidden behind us from everyone on the left
            seen += 1

        if stack:
            seen += 1  # the first taller person is also visible

        result[i] = seen
        stack.append(heights[i])

    return result
""",
    ),
    # ---- Final Prices With a Special Discount in a Shop (LeetCode 1475) ----
    dict(
        title="Final Prices With a Special Discount in a Shop",
        diff="E",
        lc=1475,
        slug="final-prices-with-a-special-discount-in-a-shop",
        prompt=(
            "For item i, the discount is prices[j] for the smallest j > i with prices[j] <= prices[i] (no discount "
            "if none). Return each item's final price."
        ),
        sig="def final_prices(prices: List[int]) -> List[int]:",
        fn="final_prices",
        tests=[
            (([8, 4, 6, 2, 3],), [4, 2, 4, 2, 3]),
            (([1, 2, 3, 4, 5],), [1, 2, 3, 4, 5]),
            (([10, 1, 1, 6],), [9, 0, 1, 6]),
            (([5],), [5]),
        ],
        hints=[
            "For each item you look for the NEXT smaller-or-equal price to its right.",
            "A scan per item is O(n^2).",
            (
                "Monotonic stack of indices still waiting for a discount: when price p arrives, pop every index "
                "with price >= p and subtract p from it."
            ),
        ],
        pattern="Next smaller element (monotonic stack)",
        explain=(
            "Each item waits on the stack until the first later price that is not larger, and is resolved exactly once."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - scan right for each item",
        brute=r"""
# BRUTE FORCE: O(n^2) time - scan right for each item
def final_prices(prices):
    result = list(prices)
    for i in range(len(prices)):
        for j in range(i + 1, len(prices)):
            if prices[j] <= prices[i]:
                result[i] -= prices[j]
                break
    return result
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Next smaller element (monotonic stack)
def final_prices(prices):
    result, stack = list(prices), []
    for i, p in enumerate(prices):
        while stack and prices[stack[-1]] >= p:
            result[stack.pop()] -= p  # p is the first smaller-or-equal price to the right
        stack.append(i)
    return result
""",
    ),
    # ---- Minimum String Length After Removing Substrings (LeetCode 2696) ----
    dict(
        title="Minimum String Length After Removing Substrings",
        diff="E",
        lc=2696,
        slug="minimum-string-length-after-removing-substrings",
        prompt=(
            "s has only uppercase letters. In one operation you may delete any substring equal to 'AB' or 'CD' (the "
            "rest closes up). Return the minimum possible length of s."
        ),
        sig="def min_length(s: str) -> int:",
        fn="min_length",
        tests=[
            (("ABFCACDB",), 2),
            (("ACBBD",), 5),
            (("A",), 1),
            (("ABCD",), 0),
            (("CABD",), 0),
        ],
        hints=[
            "Deleting a pair can bring two new letters together, forming another pair.",
            "Process left to right keeping the letters that survive so far (a stack).",
            (
                "If the stack top plus the current letter is 'AB' or 'CD', pop instead of push. The final stack "
                "size is the answer."
            ),
        ],
        pattern="Stack for cascading adjacent deletions",
        explain="The stack is always fully reduced, so a new letter can only form a pair with the top.",
        cx="O(n) time",
        brute_cx="O(n^2) time - repeatedly use str.replace until nothing changes",
        brute=r"""
# BRUTE FORCE: O(n^2) time - repeatedly use str.replace until nothing changes
def min_length(s):
    while "AB" in s or "CD" in s:
        s = s.replace("AB", "").replace("CD", "")
    return len(s)
""",
        solution=r"""
# OPTIMISED: O(n) time
# Idea: Stack for cascading adjacent deletions
def min_length(s):
    stack = []
    for ch in s:
        if stack and stack[-1] + ch in ("AB", "CD"):
            stack.pop()
        else:
            stack.append(ch)
    return len(stack)
""",
    ),
]
