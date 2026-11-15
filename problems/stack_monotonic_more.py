"""extra batch of Stack Monotonic problems - the problem bank for the "stack_monotonic" topic.

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
    # ---- Evaluate Reverse Polish Notation (LeetCode 150) ----
    dict(
        title="Evaluate Reverse Polish Notation",
        diff="M",
        lc=150,
        slug="evaluate-reverse-polish-notation",
        prompt=(
            "Evaluate an arithmetic expression in Reverse Polish Notation. Operators: + - * /. Division truncates "
            "toward zero."
        ),
        sig="def eval_rpn(tokens: List[str]) -> int:",
        fn="eval_rpn",
        tests=[
            ((["2", "1", "+", "3", "*"],), 9),
            ((["4", "13", "5", "/", "+"],), 6),
            ((["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"],), 22),
            ((["3", "-4", "/"],), 0),
            ((["18"],), 18),
            ((["7", "-2", "/"],), -3),
        ],
        hints=[
            (
                "In RPN the operator comes AFTER its two operands. What structure holds 'operands waiting for an "
                "operator'?"
            ),
            "A stack: push numbers; on an operator pop two, apply, push the result.",
            "Order matters for - and /: the first pop is the RIGHT operand. Use int(a / b) to truncate toward zero.",
        ],
        pattern="Stack evaluation (operands wait for their operator)",
        explain=(
            "Each operator consumes the two most recent un-consumed values - exactly stack behaviour. Python's // "
            "floors,\n        so for truncation toward zero use int(a / b) (fine for these magnitudes)."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - repeatedly find the first operator, reduce in place",
        brute=r"""
# BRUTE FORCE: O(n^2) time - repeatedly find the first operator, reduce in place
def eval_rpn(tokens):
    t = list(tokens)
    ops = {"+", "-", "*", "/"}
    while len(t) > 1:
        i = next(k for k, v in enumerate(t) if v in ops)
        a, b = int(t[i - 2]), int(t[i - 1])
        op = t[i]
        r = a + b if op == "+" else a - b if op == "-" else a * b if op == "*" else int(a / b)
        t[i - 2 : i + 1] = [str(r)]
    return int(t[0])
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Stack evaluation (operands wait for their operator)
def eval_rpn(tokens):
    st = []
    for tok in tokens:
        if tok in "+-*/" and len(tok) == 1:
            b, a = st.pop(), st.pop()
            if tok == "+":
                st.append(a + b)
            elif tok == "-":
                st.append(a - b)
            elif tok == "*":
                st.append(a * b)
            else:
                st.append(int(a / b))
        else:
            st.append(int(tok))
    return st[0]
""",
    ),
    # ---- Decode String (LeetCode 394) ----
    dict(
        title="Decode String",
        diff="M",
        lc=394,
        slug="decode-string",
        prompt=(
            "Decode strings of the form k[encoded] meaning encoded repeated k times; encodings may be nested. "
            "Example: 3[a2[c]] -> accaccacc."
        ),
        sig="def decode_string(s: str) -> str:",
        fn="decode_string",
        tests=[
            (("3[a]2[bc]",), "aaabcbc"),
            (("3[a2[c]]",), "accaccacc"),
            (("2[abc]3[cd]ef",), "abcabccdcdcdef"),
            (("abc",), "abc"),
            (("10[a]",), "a" * 10),
            (("",), ""),
        ],
        hints=[
            "Nesting means: when you meet ']', the innermost group is complete.",
            "On '[' remember (text so far, the repeat count) and start fresh.",
            "Stack of (previous_string, k). On ']' pop and set current = previous + current * k.",
        ],
        pattern="Stack of contexts for nested structures",
        explain=(
            "Each '[' opens a new context. Save what you had plus the multiplier, start collecting the inner text, "
            "and\n        on ']' glue everything back together. Multi-digit counts are accumulated digit by digit."
        ),
        cx="O(output length) time",
        brute_cx="O(n * output) time - repeatedly expand the innermost k[x] with a regex",
        brute=r"""
# BRUTE FORCE: O(n * output) time - repeatedly expand the innermost k[x] with a regex
def decode_string(s):
    import re

    pat = re.compile(r"(\d+)\[([a-z]*)\]")
    while True:
        m = pat.search(s)
        if not m:
            return s
        s = s[: m.start()] + m.group(2) * int(m.group(1)) + s[m.end() :]
""",
        solution=r"""
# OPTIMISED: O(output length) time
# Idea: Stack of contexts for nested structures
def decode_string(s):
    stack, cur, k = [], "", 0
    for ch in s:
        if ch.isdigit():
            k = k * 10 + int(ch)
        elif ch == "[":
            stack.append((cur, k))
            cur, k = "", 0
        elif ch == "]":
            prev, times = stack.pop()
            cur = prev + cur * times
        else:
            cur += ch
    return cur
""",
    ),
    # ---- Car Fleet (LeetCode 853) ----
    dict(
        title="Car Fleet",
        diff="M",
        lc=853,
        slug="car-fleet",
        prompt=(
            "Cars drive toward `target` on a one-lane road, never passing (a faster car catches up and then drives "
            "at the slower one's speed). position[i], speed[i] are given. Return the number of car fleets arriving."
        ),
        sig="def car_fleet(target: int, position: List[int], speed: List[int]) -> int:",
        fn="car_fleet",
        tests=[
            ((12, [10, 8, 0, 5, 3], [2, 4, 1, 1, 3]), 3),
            ((10, [3], [3]), 1),
            ((100, [0, 2, 4], [4, 2, 1]), 1),
            ((10, [6, 8], [3, 2]), 2),
            ((10, [], []), 0),
        ],
        hints=[
            "Compute each car's time to reach the target if it were alone.",
            (
                "Process cars from the closest to the target backwards. A car behind with a time <= the car ahead "
                "joins its fleet."
            ),
            "Sort by position descending; keep the 'current fleet time'; a car with time > current starts a new fleet.",
        ],
        pattern="Sort + monotonic 'slowest ahead' (merge into the blocking fleet)",
        explain=(
            "A car can never arrive earlier than the car ahead of it. If its solo time is <= the car ahead's, it "
            "gets stuck\n        behind and shares that arrival time. Only a strictly longer time forms a new fleet."
        ),
        cx="O(n log n) time",
        brute_cx="O(n^2) time - for each car compare with every car ahead",
        brute=r"""
# BRUTE FORCE: O(n^2) time - for each car compare with every car ahead
def car_fleet(target, position, speed):
    cars = [(p, (target - p) / s) for p, s in zip(position, speed)]
    fleets = 0
    for p, t in cars:
        if all(
            t > t2 for p2, t2 in cars if p2 > p
        ):  # nobody ahead is slower-or-equal -> leads its own fleet
            fleets += 1
    return fleets
""",
        solution=r"""
# OPTIMISED: O(n log n) time
# Idea: Sort + monotonic 'slowest ahead' (merge into the blocking fleet)
def car_fleet(target, position, speed):
    fleets, slowest = 0, 0.0
    for p, s in sorted(zip(position, speed), reverse=True):
        t = (target - p) / s
        if t > slowest:
            fleets += 1
            slowest = t
    return fleets
""",
    ),
    # ---- Asteroid Collision (LeetCode 735) ----
    dict(
        title="Asteroid Collision",
        diff="M",
        lc=735,
        slug="asteroid-collision",
        prompt=(
            "Asteroids move along a line: sign = direction (positive right, negative left), size = |value|. Same "
            "speed. When two meet, the smaller explodes (equal -> both). Return the survivors after all collisions."
        ),
        sig="def asteroid_collision(asteroids: List[int]) -> List[int]:",
        fn="asteroid_collision",
        tests=[
            (([5, 10, -5],), [5, 10]),
            (([8, -8],), []),
            (([10, 2, -5],), [10]),
            (([-2, -1, 1, 2],), [-2, -1, 1, 2]),
            (([1, -2, -2, -2],), [-2, -2, -2]),
            (([],), []),
        ],
        hints=[
            "A collision happens only when a right-mover is immediately followed by a left-mover.",
            "Keep a stack of survivors. The new asteroid may fight several stack tops in a row.",
            (
                "While new is negative and the top is positive: compare sizes; pop the smaller (or both if equal); "
                "if new dies, stop."
            ),
        ],
        pattern="Stack simulation (chain reactions)",
        explain=(
            "Only the stack top can collide with the incoming asteroid. A big left-mover can destroy many "
            "right-movers one\n        after another, hence the inner while-loop. Each asteroid is pushed/popped at "
            "most once: O(n)."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - rescan for the first colliding neighbours until none remain",
        brute=r"""
# BRUTE FORCE: O(n^2) time - rescan for the first colliding neighbours until none remain
def asteroid_collision(asteroids):
    a = list(asteroids)
    changed = True
    while changed:
        changed = False
        for i in range(len(a) - 1):
            if a[i] > 0 > a[i + 1]:
                if abs(a[i]) > abs(a[i + 1]):
                    del a[i + 1]
                elif abs(a[i]) < abs(a[i + 1]):
                    del a[i]
                else:
                    del a[i : i + 2]
                changed = True
                break
    return a
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Stack simulation (chain reactions)
def asteroid_collision(asteroids):
    st = []
    for x in asteroids:
        alive = True
        while alive and x < 0 and st and st[-1] > 0:
            if st[-1] < -x:
                st.pop()
            elif st[-1] == -x:
                st.pop()
                alive = False
            else:
                alive = False
        if alive:
            st.append(x)
    return st
""",
    ),
    # ---- Remove K Digits (LeetCode 402) ----
    dict(
        title="Remove K Digits",
        diff="M",
        lc=402,
        slug="remove-k-digits",
        prompt=(
            "Given a non-negative integer as a string, remove exactly k digits so the remaining number is as small "
            "as possible. Return it without leading zeros ('0' if empty)."
        ),
        sig="def remove_k_digits(num: str, k: int) -> str:",
        fn="remove_k_digits",
        tests=[
            (("1432219", 3), "1219"),
            (("10200", 1), "200"),
            (("10", 2), "0"),
            (("112", 1), "11"),
            (("9", 1), "0"),
            (("12345", 2), "123"),
            (("100", 1), "0"),
        ],
        hints=[
            "Which digit is best to delete? Compare adjacent digits.",
            (
                "The first digit that is larger than its right neighbour should go (that makes the number smaller "
                "most significantly)."
            ),
            (
                "Monotonic increasing stack: while k > 0 and top > digit: pop, k--. Push digit. Finally drop k more "
                "from the end and strip leading zeros."
            ),
        ],
        pattern="Monotonic (increasing) stack - greedy removal",
        explain=(
            "To minimise the number, earlier digits matter most. If a digit is greater than the next one, removing "
            "it\n        improves the number. The stack maintains non-decreasing digits; each pop is one deletion. "
            "Leftover k means the\n        digits are already increasing - remove from the end."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n*k) time - k times delete the first digit larger than its right neighbour",
        brute=r"""
# BRUTE FORCE: O(n*k) time - k times delete the first digit larger than its right neighbour
def remove_k_digits(num, k):
    s = num
    for _ in range(k):
        for i in range(len(s)):
            if i == len(s) - 1 or s[i] > s[i + 1]:
                s = s[:i] + s[i + 1 :]
                break
    return s.lstrip("0") or "0"
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic (increasing) stack - greedy removal
def remove_k_digits(num, k):
    st = []
    for d in num:
        while k and st and st[-1] > d:
            st.pop()
            k -= 1
        st.append(d)
    if k:
        st = st[:-k]
    return "".join(st).lstrip("0") or "0"
""",
    ),
    # ---- Next Greater Element II (LeetCode 503) ----
    dict(
        title="Next Greater Element II",
        diff="M",
        lc=503,
        slug="next-greater-element-ii",
        prompt=(
            "Circular array: for each element, find the next greater element scanning forward (wrapping around). "
            "Use -1 if none exists."
        ),
        sig="def next_greater_elements(nums: List[int]) -> List[int]:",
        fn="next_greater_elements",
        tests=[
            (([1, 2, 1],), [2, -1, 2]),
            (([1, 2, 3, 4, 3],), [2, 3, 4, -1, 4]),
            (([5],), [-1]),
            (([5, 4, 3],), [-1, 5, 5]),
            (([],), []),
        ],
        hints=[
            "The non-circular version uses a monotonic stack. How do you simulate wrapping?",
            "Iterate over indices 0 .. 2n-1 and use i % n.",
            (
                "Stack of indices with decreasing values; when nums[i % n] exceeds the top's value, that top's "
                "answer is found. Only push in the first lap."
            ),
        ],
        pattern="Monotonic stack + doubled traversal for circular arrays",
        explain=(
            "Walking the array twice lets every element 'see' the ones before it. The stack holds indices still "
            "waiting for\n        a greater element; each is resolved at most once."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - scan up to n-1 positions ahead for each element",
        brute=r"""
# BRUTE FORCE: O(n^2) time - scan up to n-1 positions ahead for each element
def next_greater_elements(nums):
    n = len(nums)
    out = []
    for i in range(n):
        ans = -1
        for step in range(1, n):
            if nums[(i + step) % n] > nums[i]:
                ans = nums[(i + step) % n]
                break
        out.append(ans)
    return out
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic stack + doubled traversal for circular arrays
def next_greater_elements(nums):
    n = len(nums)
    res = [-1] * n
    st = []
    for i in range(2 * n):
        x = nums[i % n]
        while st and nums[st[-1]] < x:
            res[st.pop()] = x
        if i < n:
            st.append(i)
    return res
""",
    ),
]
