"""more Stack problems (batch 4) - part of the problem bank for the "stack_monotonic" topic.

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""

PROBLEMS = [
    # ---- Remove Outermost Parentheses (LeetCode 1021) ----
    dict(
        title="Remove Outermost Parentheses",
        diff="E",
        lc=1021,
        slug="remove-outermost-parentheses",
        prompt=(
            "s is a valid parentheses string. Split it into primitive pieces (non-empty valid strings that cannot "
            "be split further) and remove the outermost pair of each. Return the result."
        ),
        sig="def remove_outer_parentheses(s: str) -> str:",
        fn="remove_outer_parentheses",
        tests=[
            (("(()())(())",), "()()()"),
            (("(()())(())(()(()))",), "()()()()(())"),
            (("()()",), ""),
            (("((()))",), "(())"),
        ],
        hints=[
            "Track the depth: '(' increases it, ')' decreases it.",
            "An outermost '(' is one that brings the depth from 0 to 1; an outermost ')' brings it from 1 to 0.",
            (
                "Keep every character that is NOT outermost: for '(' keep if depth > 0 before it; for ')' keep if "
                "depth > 1 before it."
            ),
        ],
        pattern="Depth counter instead of a stack",
        explain=(
            "A stack of brackets is overkill when you only need nesting depth; a single integer does the same job "
            "in O(1) space."
        ),
        cx="O(n) time, O(1) extra space",
        brute_cx="O(n) time - explicitly cut the string into primitive pieces first",
        brute=r"""
# BRUTE FORCE: O(n) time - explicitly cut the string into primitive pieces first
def remove_outer_parentheses(s):
    pieces, start, depth = [], 0, 0
    for i, ch in enumerate(s):
        depth += 1 if ch == "(" else -1
        if depth == 0:  # a primitive piece s[start..i] just ended
            pieces.append(s[start : i + 1])
            start = i + 1
    return "".join(piece[1:-1] for piece in pieces)  # strip the outer pair of each piece
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) extra space
# Idea: Depth counter instead of a stack
def remove_outer_parentheses(s):
    out, depth = [], 0

    for ch in s:
        if ch == "(":
            if depth > 0:
                out.append(ch)  # not an outermost opener
            depth += 1
        else:
            depth -= 1
            if depth > 0:
                out.append(ch)  # not an outermost closer

    return "".join(out)
""",
    ),
    # ---- Minimum Add to Make Parentheses Valid (LeetCode 921) ----
    dict(
        title="Minimum Add to Make Parentheses Valid",
        diff="M",
        lc=921,
        slug="minimum-add-to-make-parentheses-valid",
        prompt=(
            "Return the minimum number of parentheses you must insert (anywhere) to make the string of '(' and ')' "
            "valid."
        ),
        sig="def min_add_to_make_valid(s: str) -> int:",
        fn="min_add_to_make_valid",
        tests=[
            (("())",), 1),
            (("(((",), 3),
            (("()",), 0),
            (("()))((",), 4),
            (("",), 0),
        ],
        hints=[
            "Valid Parentheses with a stack: unmatched characters are what is left over.",
            "You do not need the stack itself - only how many '(' are still waiting and how many ')' found no partner.",
            "Scan: '(' -> open += 1. ')' -> if open > 0 then open -= 1 else unmatched += 1. Answer = open + unmatched.",
        ],
        pattern="Balance counter (stack reduced to two integers)",
        explain=(
            "An unmatched ')' needs a '(' inserted before it, and every '(' still open at the end needs a ')' "
            "appended. Those two kinds of repairs never interfere."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - repeatedly delete adjacent '()' pairs until none remain",
        brute=r"""
# BRUTE FORCE: O(n^2) time - repeatedly delete adjacent '()' pairs until none remain
def min_add_to_make_valid(s):
    while "()" in s:
        s = s.replace(
            "()", ""
        )  # remove every matched pair; what is left needs one insertion per character
    return len(s)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Balance counter (stack reduced to two integers)
def min_add_to_make_valid(s):
    open_count = unmatched_close = 0

    for ch in s:
        if ch == "(":
            open_count += 1
        elif open_count:
            open_count -= 1  # matches an earlier '('
        else:
            unmatched_close += 1  # nothing to match: needs an inserted '('

    return open_count + unmatched_close
""",
    ),
    # ---- Sum of Subarray Minimums (LeetCode 907) ----
    dict(
        title="Sum of Subarray Minimums",
        diff="M",
        lc=907,
        slug="sum-of-subarray-minimums",
        prompt="Return the sum of min(subarray) over all contiguous subarrays of arr, modulo 1_000_000_007.",
        sig="def sum_subarray_mins(arr: List[int]) -> int:",
        fn="sum_subarray_mins",
        tests=[
            (([3, 1, 2, 4],), 17),
            (([11, 81, 94, 43, 3],), 444),
            (([1],), 1),
            (([2, 2, 2],), 12),
        ],
        hints=[
            "Count, for each element, in how many subarrays IT is the minimum.",
            (
                "If arr[i] is the min, the subarray stays within (previous smaller, next smaller-or-equal). Ties "
                "must be broken on ONE side so subarrays are not counted twice."
            ),
            "Monotonic stack gives both boundaries: contribution = arr[i] * (i - left) * (right - i).",
        ],
        pattern="Monotonic stack: contribution technique (each element's reach)",
        explain=(
            "Instead of enumerating subarrays, ask how many subarrays each element wins. The number of choices for "
            "the left end times the number for the right end gives that count."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - extend every start position keeping a running minimum",
        brute=r"""
# BRUTE FORCE: O(n^2) time - extend every start position keeping a running minimum
def sum_subarray_mins(arr):
    total = 0
    for i in range(len(arr)):
        low = arr[i]
        for j in range(i, len(arr)):
            low = min(low, arr[j])  # minimum of arr[i..j]
            total += low
    return total % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic stack: contribution technique (each element's reach)
def sum_subarray_mins(arr):
    n, total = len(arr), 0
    left = [0] * n  # distance to the previous element strictly smaller
    right = [0] * n  # distance to the next element smaller or equal
    stack = []

    for i in range(n):
        while stack and arr[stack[-1]] > arr[i]:
            j = stack.pop()
            right[j] = i - j  # i is the next smaller-or-equal for j... (strictly smaller pops here)
        left[i] = i - stack[-1] if stack else i + 1
        stack.append(i)

    for j in stack:
        right[j] = n - j  # nothing smaller on the right

    for i in range(n):
        total += arr[i] * left[i] * right[i]

    return total % (10**9 + 7)
""",
    ),
    # ---- Maximal Rectangle (LeetCode 85) ----
    dict(
        title="Maximal Rectangle",
        diff="H",
        lc=85,
        slug="maximal-rectangle",
        prompt="matrix holds '0' and '1' characters. Return the area of the largest rectangle containing only '1'.",
        sig="def maximal_rectangle(matrix: List[List[str]]) -> int:",
        fn="maximal_rectangle",
        tests=[
            (
                (
                    [
                        ["1", "0", "1", "0", "0"],
                        ["1", "0", "1", "1", "1"],
                        ["1", "1", "1", "1", "1"],
                        ["1", "0", "0", "1", "0"],
                    ],
                ),
                6,
            ),
            (([["0"]],), 0),
            (([["1"]],), 1),
            (([["0", "0"], ["0", "0"]],), 0),
            (([["1", "1"], ["1", "1"]],), 4),
        ],
        hints=[
            "Fix a row as the bottom edge. Each column has a 'height' = number of consecutive 1s ending at this row.",
            "The best rectangle with that bottom edge is the Largest Rectangle in Histogram of those heights.",
            (
                "Update heights row by row (height = height + 1 if '1' else 0) and run the monotonic-stack "
                "histogram routine each time."
            ),
        ],
        pattern="Reduce to Largest Rectangle in Histogram per row",
        explain=(
            "Every rectangle has a bottom row. Treating the consecutive-ones counts as bar heights turns each row "
            "into the histogram problem, solved in O(cols) with a monotonic stack."
        ),
        cx="O(rows * cols) time, O(cols) space",
        brute_cx="O(rows^2 * cols^2 * ...) time - test every rectangle with prefix sums",
        brute=r"""
# BRUTE FORCE: O(rows^2 * cols^2 * ...) time - test every rectangle with prefix sums
def maximal_rectangle(matrix):
    rows, cols = len(matrix), len(matrix[0])
    # prefix[r][c] = number of '1' in the rectangle from (0, 0) to (r - 1, c - 1)
    prefix = [[0] * (cols + 1) for _ in range(rows + 1)]

    for r in range(rows):
        for c in range(cols):
            prefix[r + 1][c + 1] = (
                prefix[r][c + 1] + prefix[r + 1][c] - prefix[r][c] + (matrix[r][c] == "1")
            )

    best = 0

    for r1 in range(rows):
        for r2 in range(r1, rows):
            for c1 in range(cols):
                for c2 in range(c1, cols):
                    area = (r2 - r1 + 1) * (c2 - c1 + 1)
                    ones = (
                        prefix[r2 + 1][c2 + 1]
                        - prefix[r1][c2 + 1]
                        - prefix[r2 + 1][c1]
                        + prefix[r1][c1]
                    )

                    if ones == area:  # all ones
                        best = max(best, area)

    return best
""",
        solution=r"""
# OPTIMISED: O(rows * cols) time, O(cols) space
# Idea: Reduce to Largest Rectangle in Histogram per row
def maximal_rectangle(matrix):
    cols = len(matrix[0])
    heights, best = [0] * cols, 0

    for row in matrix:
        for c in range(cols):
            heights[c] = (
                heights[c] + 1 if row[c] == "1" else 0
            )  # consecutive ones ending at this row

        stack = []  # indices of bars with increasing heights

        for i in range(cols + 1):
            h = heights[i] if i < cols else 0  # a sentinel bar of height 0 flushes the stack
            while stack and heights[stack[-1]] >= h:
                height = heights[stack.pop()]
                width = i if not stack else i - stack[-1] - 1
                best = max(best, height * width)
            stack.append(i)

    return best
""",
    ),
    # ---- Basic Calculator (LeetCode 224) ----
    dict(
        title="Basic Calculator",
        diff="H",
        lc=224,
        slug="basic-calculator",
        prompt=(
            "Evaluate an expression with non-negative integers, '+', '-', parentheses, spaces and unary minus (like "
            "'-(2+3)'). Do not use eval."
        ),
        sig="def calculate(s: str) -> int:",
        fn="calculate",
        tests=[
            (("1 + 1",), 2),
            ((" 2-1 + 2 ",), 3),
            (("(1+(4+5+2)-3)+(6+8)",), 23),
            (("-(2+3)",), -5),
            (("2-(5-6)",), 3),
        ],
        hints=[
            "Only + and - exist, so the only trouble is parentheses: a '-' before '(' flips every sign inside.",
            "Keep the current sign and a running result. When you meet '(', push the result and sign, and start fresh.",
            "On ')': result = popped_result + popped_sign * result_inside.",
        ],
        pattern="Stack of (result, sign) saved at each '('",
        explain=(
            "Parentheses are saved contexts. Pushing the outside result and its sign, then combining after the "
            "matching ')', evaluates nested groups without recursion or sign-flipping bookkeeping per number."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n) time - recursive-descent parser (one function call per nesting level)",
        brute=r"""
# BRUTE FORCE: O(n) time - recursive-descent parser (one function call per nesting level)
def calculate(s):
    text = s.replace(" ", "")
    pos = 0

    def expression():  # expression = term (('+' | '-') term)*
        nonlocal pos
        total = term()

        while pos < len(text) and text[pos] in "+-":
            op = text[pos]
            pos += 1
            value = term()
            total = total + value if op == "+" else total - value

        return total

    def term():  # term = number | '(' expression ')' | '-' term
        nonlocal pos

        if text[pos] == "-":
            pos += 1
            return -term()

        if text[pos] == "(":
            pos += 1
            value = expression()
            pos += 1  # skip ')'
            return value

        start = pos

        while pos < len(text) and text[pos].isdigit():
            pos += 1

        return int(text[start:pos])

    return expression()
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Stack of (result, sign) saved at each '('
def calculate(s):
    result, sign, number, stack = 0, 1, 0, []

    for ch in s:
        if ch.isdigit():
            number = number * 10 + int(ch)
        elif ch in "+-":
            result += sign * number  # finish the previous number
            number = 0
            sign = 1 if ch == "+" else -1
        elif ch == "(":
            stack.append(result)  # save the outside context
            stack.append(sign)
            result, sign = 0, 1
        elif ch == ")":
            result += sign * number
            number = 0
            result *= stack.pop()  # the sign in front of the parenthesis
            result += stack.pop()  # the result before the parenthesis

    return result + sign * number
""",
    ),
    # ---- Make The String Great (LeetCode 1544) ----
    dict(
        title="Make The String Great",
        diff="E",
        lc=1544,
        slug="make-the-string-great",
        prompt=(
            "Repeatedly delete two adjacent characters that are the same letter in different cases (like 'aA' or "
            "'Bb') until none remain. Return the final string."
        ),
        sig="def make_good(s: str) -> str:",
        fn="make_good",
        tests=[
            (("leEeetcode",), "leetcode"),
            (("abBAcC",), ""),
            (("s",), "s"),
            (("aAa",), "a"),
        ],
        hints=[
            "Deleting a pair can create a NEW adjacent bad pair from its former neighbours.",
            "You always compare the character you are about to add with the most recent kept character.",
            "Use a stack; two letters cancel when they differ only by case: abs(ord(a) - ord(b)) == 32.",
        ],
        pattern="Stack cancellation of adjacent pairs",
        explain=(
            "The stack always holds a string with no bad pair. Adding a character either cancels the top (pop) or "
            "is safe to append, so one pass suffices."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - repeatedly rescan and delete the first bad pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - repeatedly rescan and delete the first bad pair
def make_good(s):
    changed = True

    while changed:
        changed = False
        for i in range(len(s) - 1):
            if s[i] != s[i + 1] and s[i].lower() == s[i + 1].lower():
                s = s[:i] + s[i + 2 :]  # delete the bad pair and rescan
                changed = True
                break

    return s
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Stack cancellation of adjacent pairs
def make_good(s):
    stack = []
    for ch in s:
        if stack and abs(ord(stack[-1]) - ord(ch)) == 32:  # same letter, opposite case
            stack.pop()
        else:
            stack.append(ch)
    return "".join(stack)
""",
    ),
]
