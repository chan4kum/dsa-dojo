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
    # ---- Next Greater Element I (LeetCode 496) ----
    dict(
        title="Next Greater Element I",
        diff="E",
        lc=496,
        slug="next-greater-element-i",
        prompt=(
            "For each value in nums1 (a subset of nums2, all distinct), find the first greater value to its right "
            "inside nums2, or -1."
        ),
        sig="def next_greater_element(nums1: List[int], nums2: List[int]) -> List[int]:",
        fn="next_greater_element",
        tests=[
            (([4, 1, 2], [1, 3, 4, 2]), [-1, 3, -1]),
            (([2, 4], [1, 2, 3, 4]), [3, -1]),
            (([1], [1]), [-1]),
            (([], [1, 2]), []),
            (([3, 1], [3, 2, 1, 4]), [4, 4]),
        ],
        hints=[
            "Computing 'next greater' for every element of nums2 once is enough.",
            "A decreasing stack: when a bigger value arrives, it is the answer for everything it pops.",
            "Fill a dict value -> next greater while scanning nums2, then look up each nums1 value.",
        ],
        pattern="Monotonic decreasing stack + lookup dict",
        explain=(
            "An element waits on the stack until something bigger shows up. That bigger element is exactly its "
            "'next greater'."
        ),
        cx="O(n + m) time, O(n) space",
        brute_cx="O(n*m) time",
        brute=r"""
# BRUTE FORCE: O(n*m) time
def next_greater_element(nums1, nums2):
    out = []
    for x in nums1:
        i = nums2.index(x)
        nxt = -1
        for y in nums2[i + 1 :]:
            if y > x:
                nxt = y
                break
        out.append(nxt)
    return out
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(n) space
# Idea: Monotonic decreasing stack + lookup dict
def next_greater_element(nums1, nums2):
    nxt, st = {}, []
    for y in nums2:
        while st and st[-1] < y:
            nxt[st.pop()] = y
        st.append(y)
    return [nxt.get(x, -1) for x in nums1]
""",
    ),
    # ---- Remove All Adjacent Duplicates In String (LeetCode 1047) ----
    dict(
        title="Remove All Adjacent Duplicates In String",
        diff="E",
        lc=1047,
        slug="remove-all-adjacent-duplicates-in-string",
        prompt="Repeatedly delete pairs of equal adjacent letters until none remain. Return the result.",
        sig="def remove_duplicates(s: str) -> str:",
        fn="remove_duplicates",
        tests=[
            (("abbaca",), "ca"),
            (("azxxzy",), "ay"),
            (("aaaa",), ""),
            (("",), ""),
            (("abc",), "abc"),
            (("aabccba",), "a"),
        ],
        hints=[
            "After deleting a pair, new neighbours may become equal.",
            "A stack naturally compares the new character with the latest survivor.",
            "If the top equals the current character pop it, otherwise push; join the stack.",
        ],
        pattern="Stack as a self-cancelling accumulator",
        explain="The stack always holds the already-reduced prefix, so cascading cancellations happen automatically.",
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time (rescan after each removal)",
        brute=r"""
# BRUTE FORCE: O(n^2) time (rescan after each removal)
def remove_duplicates(s):
    changed = True
    while changed:
        changed = False
        for i in range(len(s) - 1):
            if s[i] == s[i + 1]:
                s = s[:i] + s[i + 2 :]
                changed = True
                break
    return s
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Stack as a self-cancelling accumulator
def remove_duplicates(s):
    st = []
    for c in s:
        if st and st[-1] == c:
            st.pop()
        else:
            st.append(c)
    return "".join(st)
""",
    ),
    # ---- Validate Stack Sequences (LeetCode 946) ----
    dict(
        title="Validate Stack Sequences",
        diff="M",
        lc=946,
        slug="validate-stack-sequences",
        prompt=(
            "Given the push order and a claimed pop order of distinct values, is the pop order achievable on one stack?"
        ),
        sig="def validate_stack_sequences(pushed: List[int], popped: List[int]) -> bool:",
        fn="validate_stack_sequences",
        tests=[
            (([1, 2, 3, 4, 5], [4, 5, 3, 2, 1]), True),
            (([1, 2, 3, 4, 5], [4, 3, 5, 1, 2]), False),
            (([], []), True),
            (([1], [1]), True),
            (([2, 1, 0], [1, 2, 0]), True),
        ],
        hints=[
            "Simulate it: you push in order and pop as soon as the stack top equals the next required pop.",
            "Greedy popping is safe: if the top matches, popping now is never worse.",
            "Push each value; while stack top == popped[j]: pop, j += 1. At the end the stack must be empty.",
        ],
        pattern="Simulate with a stack (greedy pop whenever possible)",
        explain=(
            "Whenever the top equals the next demanded value, it must be popped now - any later pop would be "
            "blocked by items pushed on top."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time (try the next pop from the list of remaining stack items)",
        brute=r"""
# BRUTE FORCE: O(n^2) time (try the next pop from the list of remaining stack items)
def validate_stack_sequences(pushed, popped):
    st, i = [], 0
    for want in popped:
        while (not st or st[-1] != want) and i < len(pushed):
            st.append(pushed[i])
            i += 1
        if not st or st[-1] != want:
            return False
        st.pop()
    return True
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Simulate with a stack (greedy pop whenever possible)
def validate_stack_sequences(pushed, popped):
    st, j = [], 0
    for x in pushed:
        st.append(x)
        while st and j < len(popped) and st[-1] == popped[j]:
            st.pop()
            j += 1
    return not st
""",
    ),
    # ---- Simplify Path (LeetCode 71) ----
    dict(
        title="Simplify Path",
        diff="M",
        lc=71,
        slug="simplify-path",
        prompt=(
            "Convert a Unix absolute path to its canonical form ('.' = current dir, '..' = parent, collapse "
            "multiple slashes, no trailing slash except root)."
        ),
        sig="def simplify_path(path: str) -> str:",
        fn="simplify_path",
        tests=[
            (("/home/",), "/home"),
            (("/../",), "/"),
            (("/home//foo/",), "/home/foo"),
            (("/a/./b/../../c/",), "/c"),
            (("/a/../../b/../c//.//",), "/c"),
            (("/...",), "/..."),
        ],
        hints=[
            "Split by '/' and treat each token separately.",
            "'..' undoes the previous directory; '.' and '' are ignored.",
            "Stack of names: '..' pops if non-empty; otherwise push. Return '/' + '/'.join(stack).",
        ],
        pattern="Stack of path components",
        explain=(
            "A path is a walk; '..' is 'undo last step', exactly stack pop. Ignoring '.' and empty tokens handles "
            "redundant slashes."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time (repeatedly rewrite the string)",
        brute=r"""
# BRUTE FORCE: O(n^2) time (repeatedly rewrite the string)
def simplify_path(path):
    parts = [p for p in path.split("/") if p not in ("", ".")]
    i = 0
    while i < len(parts):
        if parts[i] == "..":
            if i > 0:
                del parts[i - 1 : i + 1]
                i -= 1
            else:
                del parts[i]
        else:
            i += 1
    return "/" + "/".join(parts)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Stack of path components
def simplify_path(path):
    st = []
    for tok in path.split("/"):
        if tok == "..":
            if st:
                st.pop()
        elif tok and tok != ".":
            st.append(tok)
    return "/" + "/".join(st)
""",
    ),
    # ---- Basic Calculator II (LeetCode 227) ----
    dict(
        title="Basic Calculator II",
        diff="M",
        lc=227,
        slug="basic-calculator-ii",
        prompt=(
            "Evaluate an expression with non-negative integers, + - * / (integer division truncating toward zero) "
            "and spaces. No parentheses."
        ),
        sig="def calculate(s: str) -> int:",
        fn="calculate",
        tests=[
            (("3+2*2",), 7),
            ((" 3/2 ",), 1),
            ((" 3+5 / 2 ",), 5),
            (("14-3/2",), 13),
            (("2*3*4",), 24),
            (("0",), 0),
            (("1-1+1",), 1),
        ],
        hints=[
            "* and / bind tighter than + and -. Postpone additions but apply multiplications at once.",
            (
                "Keep the last operator seen; when a number ends, apply it to a stack: + push n, - push -n, * / "
                "modify the stack top."
            ),
            "Answer = sum(stack). For division truncate toward zero: int(top / n).",
        ],
        pattern="Stack of terms (resolve * and / immediately, sum the rest)",
        explain=(
            "Precedence means a term is a product chain. Collect terms on a stack, collapsing * and / as you read "
            "them, then add everything."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time (re-scan and replace the first * or / each time)",
        brute=r"""
# BRUTE FORCE: O(n^2) time (re-scan and replace the first * or / each time)
def calculate(s):
    import re

    toks = re.findall(r"\d+|[-+*/]", s.replace(" ", ""))
    while "*" in toks or "/" in toks:
        i = next(k for k, t in enumerate(toks) if t in "*/")
        a, b = int(toks[i - 1]), int(toks[i + 1])
        toks[i - 1 : i + 2] = [str(a * b if toks[i] == "*" else int(a / b))]
    res = int(toks[0])
    for i in range(1, len(toks), 2):
        res += int(toks[i + 1]) if toks[i] == "+" else -int(toks[i + 1])
    return res
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Stack of terms (resolve * and / immediately, sum the rest)
def calculate(s):
    st, num, op = [], 0, "+"
    for ch in s + "+":
        if ch.isdigit():
            num = num * 10 + int(ch)
        elif ch != " ":
            if op == "+":
                st.append(num)
            elif op == "-":
                st.append(-num)
            elif op == "*":
                st.append(st.pop() * num)
            else:
                st.append(int(st.pop() / num))
            op, num = ch, 0
    return sum(st)
""",
    ),
    # ---- 132 Pattern (LeetCode 456) ----
    dict(
        title="132 Pattern",
        diff="M",
        lc=456,
        slug="132-pattern",
        prompt="Is there a subsequence i < j < k with nums[i] < nums[k] < nums[j]?",
        sig="def find132pattern(nums: List[int]) -> bool:",
        fn="find132pattern",
        tests=[
            (([1, 2, 3, 4],), False),
            (([3, 1, 4, 2],), True),
            (([-1, 3, 2, 0],), True),
            (([1, 0, 1, -4, -3],), False),
            (([],), False),
            (([3, 5, 0, 3, 4],), True),
        ],
        hints=[
            "Treat the middle value (the '3') as the anchor and the '2' as the best candidate to its right.",
            "Scan from the right with a decreasing stack; keep the largest popped value as the '2'.",
            "Maintain two = max popped value. If nums[i] < two you found the '1'.",
        ],
        pattern="Right-to-left monotonic stack keeping the best '2'",
        explain=(
            "Popped values are all smaller than the current '3'; the largest of them is the strongest '2'. Any "
            "element below it completes the pattern."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^3) time",
        brute=r"""
# BRUTE FORCE: O(n^3) time
def find132pattern(nums):
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] < nums[k] < nums[j]:
                    return True
    return False
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Right-to-left monotonic stack keeping the best '2'
def find132pattern(nums):
    st, two = [], float("-inf")
    for x in reversed(nums):
        if x < two:
            return True
        while st and st[-1] < x:
            two = st.pop()
        st.append(x)
    return False
""",
    ),
    # ---- Remove Duplicate Letters (LeetCode 316) ----
    dict(
        title="Remove Duplicate Letters",
        diff="M",
        lc=316,
        slug="remove-duplicate-letters",
        prompt=(
            "Remove duplicate letters so each appears once, and return the lexicographically smallest result (keep "
            "relative order of the kept letters)."
        ),
        sig="def remove_duplicate_letters(s: str) -> str:",
        fn="remove_duplicate_letters",
        tests=[
            (("bcabc",), "abc"),
            (("cbacdcbc",), "acdb"),
            (("a",), "a"),
            (("",), ""),
            (("abacb",), "abc"),
            (("ecbacba",), "eacb"),
        ],
        hints=[
            "A smaller letter earlier is always better - if you can still afford to drop the bigger one before it.",
            "Count remaining occurrences so you know if a letter appears again later.",
            "Stack: while top > c and top occurs later, pop it (and unmark). Push c unless already in the stack.",
        ],
        pattern="Monotonic stack with 'can I drop it' (last-occurrence) guard",
        explain=(
            "Greedy lexicographic minimisation: pop a bigger top only when a later copy exists, so no letter is lost."
        ),
        cx="O(n) time, O(1) space (26 letters)",
        brute_cx="O(2^n) time (try all subsequences with all letters)",
        brute=r"""
# BRUTE FORCE: O(2^n) time (try all subsequences with all letters)
def remove_duplicate_letters(s):
    need = set(s)
    best = None
    n = len(s)
    for mask in range(1 << n):
        sub = "".join(s[i] for i in range(n) if mask >> i & 1)
        if len(sub) == len(need) and set(sub) == need:
            if best is None or sub < best:
                best = sub
    return best if best is not None else ""
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space (26 letters)
# Idea: Monotonic stack with 'can I drop it' (last-occurrence) guard
def remove_duplicate_letters(s):
    last = {c: i for i, c in enumerate(s)}
    st, seen = [], set()
    for i, c in enumerate(s):
        if c in seen:
            continue
        while st and st[-1] > c and last[st[-1]] > i:
            seen.discard(st.pop())
        st.append(c)
        seen.add(c)
    return "".join(st)
""",
    ),
]
