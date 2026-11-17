"""Stack Monotonic problems - the problem bank for the "stack_monotonic" topic.

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
    # ---- Valid Parentheses (LeetCode 20) ----
    dict(
        title="Valid Parentheses",
        diff="E",
        lc=20,
        slug="valid-parentheses",
        prompt=(
            "A string contains only the brackets ()[]{}. Decide whether every bracket is closed by the right type, "
            "in the right order."
        ),
        sig="def is_valid(s: str) -> bool:",
        fn="is_valid",
        tests=[
            (("()",), True),
            (("()[]{}",), True),
            (("(]",), False),
            (("([)]",), False),
            (("{[]}",), True),
            (("(",), False),
            (("]",), False),
            (("",), True),
        ],
        hints=[
            "The most recently opened bracket must be the first one closed. Which structure gives you 'most recent'?",
            "Use a stack: push every opener; on a closer, the top must be its matching opener.",
            (
                "Fail on a mismatch or an empty stack when a closer arrives; succeed only if the stack is empty at "
                "the end."
            ),
        ],
        pattern="Stack (LIFO matching of nested structure)",
        explain=(
            "Nesting is last-opened-first-closed, exactly LIFO. A dict maps each closer to its opener. Three "
            "failure\n        modes: wrong type on top, closer with an empty stack, openers left over at the end. "
            "O(n) time/space."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) - repeatedly delete adjacent matched pairs",
        brute=r"""
# BRUTE FORCE: O(n^2) - repeatedly delete adjacent matched pairs
def is_valid(s):
    while "()" in s or "[]" in s or "{}" in s:
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Stack (LIFO matching of nested structure)
def is_valid(s):
    pair = {")": "(", "]": "[", "}": "{"}
    stack = []

    for ch in s:
        if ch in pair:
            if not stack or stack.pop() != pair[ch]:
                return False
        else:
            stack.append(ch)

    return not stack
""",
    ),
    # ---- Daily Temperatures (LeetCode 739) ----
    dict(
        title="Daily Temperatures",
        diff="M",
        lc=739,
        slug="daily-temperatures",
        prompt=(
            "For each day, output how many days you must wait for a strictly warmer temperature (0 if it never comes)."
        ),
        sig="def daily_temperatures(temperatures: List[int]) -> List[int]:",
        fn="daily_temperatures",
        tests=[
            (([73, 74, 75, 71, 69, 72, 76, 73],), [1, 1, 4, 2, 1, 1, 0, 0]),
            (([30, 40, 50, 60],), [1, 1, 1, 0]),
            (([30, 60, 90],), [1, 1, 0]),
            (([90, 80, 70],), [0, 0, 0]),
            (([50],), [0]),
        ],
        hints=[
            "Brute force scans ahead from every day: O(n^2) in the worst case.",
            "Days still waiting for a warmer day form a decreasing run of temperatures. Keep their indices on a stack.",
            (
                "For each new temperature, pop every earlier day that is colder - this day is their answer - then "
                "push today."
            ),
        ],
        pattern="Monotonic (decreasing) stack: 'next greater element'",
        explain=(
            "Unresolved days are kept in a stack whose temperatures are non-increasing from bottom to top. A "
            "warmer\n        day resolves (pops) all colder days on top in one go. Each index is pushed once and "
            "popped once, so\n        O(n) overall even though there is a while inside a for."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) - scan ahead from every day",
        brute=r"""
# BRUTE FORCE: O(n^2) - scan ahead from every day
def daily_temperatures(temperatures):
    out = []

    for i, t in enumerate(temperatures):
        d = 0
        for j in range(i + 1, len(temperatures)):
            if temperatures[j] > t:
                d = j - i
                break
        out.append(d)

    return out
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic (decreasing) stack: 'next greater element'
def daily_temperatures(temperatures):
    ans = [0] * len(temperatures)
    stack = []  # indices, temperatures decreasing

    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)

    return ans
""",
    ),
    # ---- Largest Rectangle in Histogram (LeetCode 84) ----
    dict(
        title="Largest Rectangle in Histogram",
        diff="H",
        lc=84,
        slug="largest-rectangle-in-histogram",
        prompt=(
            "Bars of width 1 have the given heights. Return the area of the largest axis-aligned rectangle that "
            "fits inside the histogram."
        ),
        sig="def largest_rectangle_area(heights: List[int]) -> int:",
        fn="largest_rectangle_area",
        tests=[
            (([2, 1, 5, 6, 2, 3],), 10),
            (([2, 4],), 4),
            (([1],), 1),
            (([2, 2, 2],), 6),
            (([6, 5, 4, 3, 2, 1],), 12),
            (([],), 0),
        ],
        hints=[
            "For each bar as the limiting (shortest) bar, the rectangle extends left and right until a shorter bar.",
            "So you need, for every bar, the nearest shorter bar on each side. That is 'next smaller element' twice.",
            (
                "One pass with an increasing stack: when a shorter bar arrives, pop taller bars and compute their "
                "rectangles; append a sentinel 0 at the end."
            ),
        ],
        pattern="Monotonic (increasing) stack: nearest smaller element on both sides",
        explain=(
            "A popped bar's right boundary is the current (shorter) index; its left boundary is the new stack "
            "top\n        (the previous shorter bar). Width = right - left - 1. A trailing 0 sentinel forces "
            "everything to pop.\n        O(n) time, O(n) space."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^3) - every range, take its minimum",
        brute=r"""
# BRUTE FORCE: O(n^3) - every range, take its minimum
def largest_rectangle_area(heights):
    best = 0
    for i in range(len(heights)):
        for j in range(i, len(heights)):
            best = max(best, min(heights[i : j + 1]) * (j - i + 1))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic (increasing) stack: nearest smaller element on both sides
def largest_rectangle_area(heights):
    stack = []  # indices with increasing heights
    best = 0

    for i, h in enumerate(heights + [0]):  # sentinel flushes the stack
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1
            best = max(best, height * (i - left - 1))
        stack.append(i)

    return best
""",
    ),
    # ---- Sliding Window Maximum (LeetCode 239) ----
    dict(
        title="Sliding Window Maximum",
        diff="H",
        lc=239,
        slug="sliding-window-maximum",
        prompt="For every window of size k sliding over the array, output the maximum of that window.",
        sig="def max_sliding_window(nums: List[int], k: int) -> List[int]:",
        fn="max_sliding_window",
        tests=[
            (([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7]),
            (([1], 1), [1]),
            (([9, 11], 2), [11]),
            (([4, 3, 2, 1], 2), [4, 3, 2]),
            (([1, -1], 1), [1, -1]),
        ],
        hints=[
            "Recomputing max per window is O(n*k). A heap helps but needs lazy deletion.",
            "Keep a deque of indices whose values are decreasing; the front is always the current maximum.",
            (
                "For each i: pop smaller values from the back, push i, drop the front if it left the window, then "
                "read the front."
            ),
        ],
        pattern="Monotonic deque (decreasing) over a sliding window",
        explain=(
            "An element that is smaller than a newer element can never be a window maximum again (the newer "
            "one\n        stays in the window at least as long), so discard it. The deque therefore holds "
            "candidates in\n        decreasing order; the front is the max. Each index enters and leaves once: O(n)."
        ),
        cx="O(n) time, O(k) space (monotonic deque)",
        brute_cx="O(n*k) - recompute the max of every window",
        brute=r"""
# BRUTE FORCE: O(n*k) - recompute the max of every window
def max_sliding_window(nums, k):
    return [max(nums[i : i + k]) for i in range(len(nums) - k + 1)]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(k) space (monotonic deque)
# Idea: Monotonic deque (decreasing) over a sliding window
def max_sliding_window(nums, k):
    dq = deque()  # indices; nums[dq] decreasing
    out = []

    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:  # front slid out of the window
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])

    return out
""",
    ),
]
