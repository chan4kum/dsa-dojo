from core import *

PROBLEMS = [
    dict(
        title="Valid Parentheses", diff="E", lc=20, slug="valid-parentheses",
        prompt="A string contains only the brackets ()[]{}. Decide whether every bracket is closed by the "
               "right type, in the right order.",
        sig="def is_valid(s: str) -> bool:",
        fn="is_valid",
        tests=[(("()",), True), (("()[]{}",), True), (("(]",), False), (("([)]",), False), (("{[]}",), True),
               (("(",), False), (("]",), False), (("",), True)],
        hints=["The most recently opened bracket must be the first one closed. Which structure gives you 'most recent'?",
               "Use a stack: push every opener; on a closer, the top must be its matching opener.",
               "Fail on a mismatch or an empty stack when a closer arrives; succeed only if the stack is empty at the end."],
        pattern="Stack (LIFO matching of nested structure)",
        explain="""
        Nesting is last-opened-first-closed, exactly LIFO. A dict maps each closer to its opener. Three failure
        modes: wrong type on top, closer with an empty stack, openers left over at the end. O(n) time/space.""",
        solution=r'''
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
''',
    ),
    dict(
        title="Daily Temperatures", diff="M", lc=739, slug="daily-temperatures",
        prompt="For each day, output how many days you must wait for a strictly warmer temperature "
               "(0 if it never comes).",
        sig="def daily_temperatures(temperatures: List[int]) -> List[int]:",
        fn="daily_temperatures",
        tests=[(([73, 74, 75, 71, 69, 72, 76, 73],), [1, 1, 4, 2, 1, 1, 0, 0]), (([30, 40, 50, 60],), [1, 1, 1, 0]),
               (([30, 60, 90],), [1, 1, 0]), (([90, 80, 70],), [0, 0, 0]), (([50],), [0])],
        hints=["Brute force scans ahead from every day: O(n^2) in the worst case.",
               "Days still waiting for a warmer day form a decreasing run of temperatures. Keep their indices on a stack.",
               "For each new temperature, pop every earlier day that is colder - this day is their answer - then push today."],
        pattern="Monotonic (decreasing) stack: 'next greater element'",
        explain="""
        Unresolved days are kept in a stack whose temperatures are non-increasing from bottom to top. A warmer
        day resolves (pops) all colder days on top in one go. Each index is pushed once and popped once, so
        O(n) overall even though there is a while inside a for.""",
        solution=r'''
def daily_temperatures(temperatures):
    ans = [0] * len(temperatures)
    stack = []                                   # indices, temperatures decreasing
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans
''',
    ),
    dict(
        title="Largest Rectangle in Histogram", diff="H", lc=84, slug="largest-rectangle-in-histogram",
        prompt="Bars of width 1 have the given heights. Return the area of the largest axis-aligned rectangle "
               "that fits inside the histogram.",
        sig="def largest_rectangle_area(heights: List[int]) -> int:",
        fn="largest_rectangle_area",
        tests=[(([2, 1, 5, 6, 2, 3],), 10), (([2, 4],), 4), (([1],), 1), (([2, 2, 2],), 6), (([6, 5, 4, 3, 2, 1],), 12),
               (([],), 0)],
        hints=["For each bar as the limiting (shortest) bar, the rectangle extends left and right until a shorter bar.",
               "So you need, for every bar, the nearest shorter bar on each side. That is 'next smaller element' twice.",
               "One pass with an increasing stack: when a shorter bar arrives, pop taller bars and compute their rectangles; append a sentinel 0 at the end."],
        pattern="Monotonic (increasing) stack: nearest smaller element on both sides",
        explain="""
        A popped bar's right boundary is the current (shorter) index; its left boundary is the new stack top
        (the previous shorter bar). Width = right - left - 1. A trailing 0 sentinel forces everything to pop.
        O(n) time, O(n) space.""",
        solution=r'''
def largest_rectangle_area(heights):
    stack = []                                 # indices with increasing heights
    best = 0
    for i, h in enumerate(heights + [0]):      # sentinel flushes the stack
        while stack and heights[stack[-1]] >= h:
            height = heights[stack.pop()]
            left = stack[-1] if stack else -1
            best = max(best, height * (i - left - 1))
        stack.append(i)
    return best
''',
    ),
    dict(
        title="Sliding Window Maximum", diff="H", lc=239, slug="sliding-window-maximum",
        prompt="For every window of size k sliding over the array, output the maximum of that window.",
        sig="def max_sliding_window(nums: List[int], k: int) -> List[int]:",
        fn="max_sliding_window",
        tests=[(([1, 3, -1, -3, 5, 3, 6, 7], 3), [3, 3, 5, 5, 6, 7]), (([1], 1), [1]), (([9, 11], 2), [11]),
               (([4, 3, 2, 1], 2), [4, 3, 2]), (([1, -1], 1), [1, -1])],
        hints=["Recomputing max per window is O(n*k). A heap helps but needs lazy deletion.",
               "Keep a deque of indices whose values are decreasing; the front is always the current maximum.",
               "For each i: pop smaller values from the back, push i, drop the front if it left the window, then read the front."],
        pattern="Monotonic deque (decreasing) over a sliding window",
        explain="""
        An element that is smaller than a newer element can never be a window maximum again (the newer one
        stays in the window at least as long), so discard it. The deque therefore holds candidates in
        decreasing order; the front is the max. Each index enters and leaves once: O(n).""",
        solution=r'''
def max_sliding_window(nums, k):
    dq = deque()                       # indices; nums[dq] decreasing
    out = []
    for i, x in enumerate(nums):
        while dq and nums[dq[-1]] <= x:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:             # front slid out of the window
            dq.popleft()
        if i >= k - 1:
            out.append(nums[dq[0]])
    return out
''',
    ),
]
