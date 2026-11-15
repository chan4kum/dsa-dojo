"""extra batch of Backtracking problems - the problem bank for the "backtracking" topic (batch 4).

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
    # ---- Word Break II (LeetCode 140) ----
    dict(
        title="Word Break II",
        diff="H",
        lc=140,
        slug="word-break-ii",
        prompt=(
            "Given a string s and a dictionary of words, insert spaces into s to build every sentence in which all "
            "words are in the dictionary. Return all such sentences in any order."
        ),
        sig="def word_break(s: str, word_dict: List[str]) -> List[str]:",
        fn="word_break",
        compare="unordered",
        tests=[
            (("catsanddog", ["cat", "cats", "and", "sand", "dog"]), ["cats and dog", "cat sand dog"]),
            (
                ("pineapplepenapple", ["apple", "pen", "applepen", "pine", "pineapple"]),
                ["pine apple pen apple", "pineapple pen apple", "pine applepen apple"],
            ),
            (("catsandog", ["cats", "dog", "sand", "and", "cat"]), []),
            (("a", ["a"]), ["a"]),
            (("aaa", ["a", "aa"]), ["a a a", "a aa", "aa a"]),
        ],
        hints=[
            "Try every cut: choose the first word, then solve the same problem for the rest of the string.",
            (
                "The same suffix is solved again and again from different prefixes - remember the sentences for "
                "each start index."
            ),
            (
                "build(start) returns all sentences for s[start:]; combine each dictionary word s[start:end] with "
                "every sentence of build(end)."
            ),
        ],
        pattern="Backtracking over cut points + memoisation of suffix results",
        explain=(
            "Every sentence starts with some dictionary word s[start:end], followed by a sentence for the remaining "
            "suffix. Many prefixes lead to the same suffix, so caching build(start) avoids recomputing it. Dead "
            "ends cache as empty lists, which prunes whole branches."
        ),
        cx="output-sensitive: O(n^2 + total size of all sentences) with memoisation",
        brute_cx="O(2^n * n) time - try every set of cut positions and test every piece",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - try every set of cut positions and test every piece
def word_break(s, word_dict):
    words = set(word_dict)
    n = len(s)
    out = []
    for mask in range(1 << (n - 1)):
        pieces, start = [], 0
        for i in range(n - 1):
            if mask >> i & 1:
                pieces.append(s[start : i + 1])
                start = i + 1
        pieces.append(s[start:])
        if all(piece in words for piece in pieces):
            out.append(" ".join(pieces))
    return out
""",
        solution=r"""
# OPTIMISED: output-sensitive: O(n^2 + total size of all sentences) with memoisation
# Idea: Backtracking over cut points + memoisation of suffix results
def word_break(s, word_dict):
    words = set(word_dict)

    @lru_cache(None)
    def build(start):
        if start == len(s):
            return [""]
        sentences = []
        for end in range(start + 1, len(s) + 1):
            word = s[start:end]
            if word in words:
                for rest in build(end):
                    sentences.append(word + (" " + rest if rest else ""))
        return sentences

    return list(build(0))
""",
    ),
    # ---- Expression Add Operators (LeetCode 282) ----
    dict(
        title="Expression Add Operators",
        diff="H",
        lc=282,
        slug="expression-add-operators",
        prompt=(
            "num is a string of digits. Insert the operators +, - or * between digits (or nothing, to glue digits "
            "into a bigger number, but no number may have a leading zero) so the expression equals target. Return "
            "all such expressions in any order."
        ),
        sig="def add_operators(num: str, target: int) -> List[str]:",
        fn="add_operators",
        compare="unordered",
        tests=[
            (("123", 6), ["1+2+3", "1*2*3"]),
            (("232", 8), ["2*3+2", "2+3*2"]),
            (("105", 5), ["1*0+5", "10-5"]),
            (("00", 0), ["0+0", "0-0", "0*0"]),
            (("12", 3), ["1+2"]),
            (("12", -1), ["1-2"]),
            (("1", 1), ["1"]),
        ],
        hints=[
            "At each gap you choose: glue the next digit, or place +, - or *.",
            "Evaluating at the end is possible but wasteful; carry the running value as you go.",
            (
                "For * the new term replaces the previous one: value - last + last * cur. Remember last (signed) "
                "for the next step."
            ),
        ],
        pattern="Backtracking with a running value and the last term (to handle * precedence)",
        explain=(
            "Multiplication binds tighter than + and -, so when you multiply the current number into the previous "
            "term you must undo that term's contribution (value - last) and add last * cur instead. Carrying value "
            "and last makes each candidate O(1) to extend, and a leading zero is rejected by not extending a number "
            "that starts with 0."
        ),
        cx="O(4^n) time in the worst case, O(n) recursion depth",
        brute_cx="O(4^n * n) time - build every expression, then evaluate it from scratch",
        brute=r"""
# BRUTE FORCE: O(4^n * n) time - build every expression, then evaluate it from scratch
def add_operators(num, target):
    def value_of(numbers, ops):
        terms, signs = [numbers[0]], [1]
        for op, x in zip(ops, numbers[1:]):
            if op == "*":
                terms[-1] *= x
            else:
                terms.append(x)
                signs.append(1 if op == "+" else -1)
        return sum(sign * term for sign, term in zip(signs, terms))

    out = []
    for choice in itertools.product("+-*.", repeat=len(num) - 1):
        numbers, ops, current = [], [], num[0]
        for gap, digit in zip(choice, num[1:]):
            if gap == ".":
                current += digit
            else:
                numbers.append(current)
                ops.append(gap)
                current = digit
        numbers.append(current)
        if any(len(x) > 1 and x[0] == "0" for x in numbers):
            continue
        if value_of([int(x) for x in numbers], ops) == target:
            expr = numbers[0]
            for op, x in zip(ops, numbers[1:]):
                expr += op + x
            out.append(expr)
    return out
""",
        solution=r"""
# OPTIMISED: O(4^n) time in the worst case, O(n) recursion depth
# Idea: Backtracking with a running value and the last term (to handle * precedence)
def add_operators(num, target):
    out = []

    def go(i, expr, value, last):
        if i == len(num):
            if value == target:
                out.append(expr)
            return
        for j in range(i + 1, len(num) + 1):
            if j > i + 1 and num[i] == "0":
                break
            text = num[i:j]
            cur = int(text)
            if i == 0:
                go(j, text, cur, cur)
            else:
                go(j, expr + "+" + text, value + cur, cur)
                go(j, expr + "-" + text, value - cur, -cur)
                go(j, expr + "*" + text, value - last + last * cur, last * cur)

    go(0, "", 0, 0)
    return out
""",
    ),
    # ---- Remove Invalid Parentheses (LeetCode 301) ----
    dict(
        title="Remove Invalid Parentheses",
        diff="H",
        lc=301,
        slug="remove-invalid-parentheses",
        prompt=(
            "s contains letters and parentheses. Remove the minimum number of parentheses so the string becomes "
            "valid. Return all distinct valid strings you can get with that minimum, in any order."
        ),
        sig="def remove_invalid_parentheses(s: str) -> List[str]:",
        fn="remove_invalid_parentheses",
        compare="unordered",
        tests=[
            (("()())()",), ["(())()", "()()()"]),
            (("(a)())()",), ["(a())()", "(a)()()"]),
            ((")(",), [""]),
            (("n",), ["n"]),
            (("()",), ["()"]),
            (("((",), [""]),
            (("a)b(c)d",), ["ab(c)d"]),
        ],
        hints=[
            "First find how many '(' and how many ')' must be removed - one left-to-right scan with a counter does it.",
            (
                "Then try removing exactly that many of each, branching only on parentheses; abandon a branch when "
                "it can no longer be valid."
            ),
            (
                "Use a set to drop duplicates (removing either of two adjacent identical parentheses gives the same "
                "string)."
            ),
        ],
        pattern="Backtracking with a precomputed removal budget and pruning",
        explain=(
            "A left-to-right balance scan tells exactly how many '(' (left) and ')' (right) are surplus: an "
            "unmatched ')' is counted when the balance is already 0, whatever is left at the end is surplus '('. "
            "The DFS then decides per character 'remove it (if the budget allows)' or 'keep it (if the balance "
            "stays >= 0)', so only strings with the minimum removals are ever produced."
        ),
        cx="O(2^n) worst case, but pruned by the removal budget; O(n) depth",
        brute_cx="O(2^n * n) time - try every subset of characters to keep",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - try every subset of characters to keep
def remove_invalid_parentheses(s):
    def valid(text):
        balance = 0
        for ch in text:
            if ch == "(":
                balance += 1
            elif ch == ")":
                balance -= 1
                if balance < 0:
                    return False
        return balance == 0

    n = len(s)
    best, found = -1, set()
    for mask in range(1 << n):
        text = "".join(s[i] for i in range(n) if mask >> i & 1)
        if len(text) >= best and valid(text):
            if len(text) > best:
                best, found = len(text), set()
            found.add(text)
    return list(found)
""",
        solution=r"""
# OPTIMISED: O(2^n) worst case, but pruned by the removal budget; O(n) depth
# Idea: Backtracking with a precomputed removal budget and pruning
def remove_invalid_parentheses(s):
    left = right = 0
    for ch in s:
        if ch == "(":
            left += 1
        elif ch == ")":
            if left:
                left -= 1
            else:
                right += 1

    out = set()
    path = []

    def go(i, left_left, right_left, balance):
        if i == len(s):
            if left_left == 0 and right_left == 0 and balance == 0:
                out.add("".join(path))
            return
        ch = s[i]
        if ch == "(" and left_left > 0:
            go(i + 1, left_left - 1, right_left, balance)
        elif ch == ")" and right_left > 0:
            go(i + 1, left_left, right_left - 1, balance)
        path.append(ch)
        if ch == "(":
            go(i + 1, left_left, right_left, balance + 1)
        elif ch == ")":
            if balance > 0:
                go(i + 1, left_left, right_left, balance - 1)
        else:
            go(i + 1, left_left, right_left, balance)
        path.pop()

    go(0, left, right, 0)
    return list(out)
""",
    ),
    # ---- Matchsticks to Square (LeetCode 473) ----
    dict(
        title="Matchsticks to Square",
        diff="M",
        lc=473,
        slug="matchsticks-to-square",
        prompt=(
            "matchsticks[i] is a stick length. Use every stick exactly once (no breaking) to form a square. Return "
            "True if that is possible."
        ),
        sig="def makesquare(matchsticks: List[int]) -> bool:",
        fn="makesquare",
        tests=[
            (([1, 1, 2, 2, 2],), True),
            (([3, 3, 3, 3, 4],), False),
            (([1],), False),
            (([2, 2, 2, 2],), True),
            (([1, 1, 1, 1, 1, 1, 1, 1],), True),
            (([1, 2, 3],), False),
        ],
        hints=[
            "The total must be divisible by 4, and no single stick may exceed the side length.",
            "Place sticks one by one into one of four sides, never letting a side exceed the target.",
            (
                "Sort sticks descending (fail fast) and skip a side whose current length you have already tried for "
                "this stick."
            ),
        ],
        pattern="Backtracking: assign each item to a bucket with pruning",
        explain=(
            "It is a 4-way partition of the sticks into equal sums. Placing the longest sticks first fails early; "
            "trying two sides with identical current length is redundant (they are interchangeable), so each "
            "distinct length is tried once per stick. A full placement automatically gives four sides equal to "
            "total/4."
        ),
        cx="O(4^n) worst case, heavily pruned; O(n) depth",
        brute_cx="O(4^n * n) time - try every assignment of sticks to sides",
        brute=r"""
# BRUTE FORCE: O(4^n * n) time - try every assignment of sticks to sides
def makesquare(matchsticks):
    for assignment in itertools.product(range(4), repeat=len(matchsticks)):
        sides = [0, 0, 0, 0]
        for stick, side in zip(matchsticks, assignment):
            sides[side] += stick
        if len(set(sides)) == 1:
            return True
    return False
""",
        solution=r"""
# OPTIMISED: O(4^n) worst case, heavily pruned; O(n) depth
# Idea: Backtracking: assign each item to a bucket with pruning
def makesquare(matchsticks):
    total = sum(matchsticks)
    if len(matchsticks) < 4 or total % 4:
        return False
    side = total // 4
    sticks = sorted(matchsticks, reverse=True)
    if sticks[0] > side:
        return False
    sides = [0, 0, 0, 0]

    def place(i):
        if i == len(sticks):
            return True
        tried = set()
        for k in range(4):
            if sides[k] + sticks[i] <= side and sides[k] not in tried:
                tried.add(sides[k])
                sides[k] += sticks[i]
                if place(i + 1):
                    return True
                sides[k] -= sticks[i]
        return False

    return place(0)
""",
    ),
    # ---- Numbers With Same Consecutive Differences (LeetCode 967) ----
    dict(
        title="Numbers With Same Consecutive Differences",
        diff="M",
        lc=967,
        slug="numbers-with-same-consecutive-differences",
        prompt=(
            "Return all integers with exactly n digits (no leading zeros) in which the absolute difference between "
            "every two consecutive digits is k. Any order."
        ),
        sig="def nums_same_consec_diff(n: int, k: int) -> List[int]:",
        fn="nums_same_consec_diff",
        compare="unordered",
        tests=[
            ((3, 7), [181, 292, 707, 818, 929]),
            ((2, 1), [10, 12, 21, 23, 32, 34, 43, 45, 54, 56, 65, 67, 76, 78, 87, 89, 98]),
            ((2, 0), [11, 22, 33, 44, 55, 66, 77, 88, 99]),
            ((3, 9), [909]),
        ],
        hints=[
            (
                "Counting from 10^(n-1) to 10^n - 1 and checking digits works, but it visits numbers that fail at "
                "the second digit."
            ),
            "Build the number digit by digit; the next digit can only be last - k or last + k.",
            (
                "Start from the first digits 1..9 and extend until n digits; when k = 0 the two options coincide, "
                "so avoid duplicates."
            ),
        ],
        pattern="Backtracking: extend only with the digits that keep the constraint true",
        explain=(
            "The constraint couples only neighbouring digits, so a partial number is valid exactly when its last "
            "digit is. Each extension has at most two choices, so the search visits only valid prefixes instead of "
            "all 10^n numbers. A set of {last - k, last + k} removes the duplicate when k == 0."
        ),
        cx="O(9 * 2^(n-1)) time (the output size is the same order)",
        brute_cx="O(9 * 10^(n-1) * n) time - test every n-digit number",
        brute=r"""
# BRUTE FORCE: O(9 * 10^(n-1) * n) time - test every n-digit number
def nums_same_consec_diff(n, k):
    out = []
    for x in range(10 ** (n - 1), 10**n):
        digits = [int(ch) for ch in str(x)]
        if all(abs(digits[i] - digits[i + 1]) == k for i in range(n - 1)):
            out.append(x)
    return out
""",
        solution=r"""
# OPTIMISED: O(9 * 2^(n-1)) time (the output size is the same order)
# Idea: Backtracking: extend only with the digits that keep the constraint true
def nums_same_consec_diff(n, k):
    out = []

    def build(value, digits_left):
        if digits_left == 0:
            out.append(value)
            return
        last = value % 10
        for nxt in {last - k, last + k}:
            if 0 <= nxt <= 9:
                build(value * 10 + nxt, digits_left - 1)

    for first in range(1, 10):
        build(first, n - 1)
    return out
""",
    ),
    # ---- Path with Maximum Gold (LeetCode 1219) ----
    dict(
        title="Path with Maximum Gold",
        diff="M",
        lc=1219,
        slug="path-with-maximum-gold",
        prompt=(
            "grid[r][c] is the gold in a cell (0 = empty). Start from any non-empty cell, move up/down/left/right "
            "to non-empty cells, never visit a cell twice, and collect gold as you go. Return the maximum gold you "
            "can collect."
        ),
        sig="def get_maximum_gold(grid: List[List[int]]) -> int:",
        fn="get_maximum_gold",
        tests=[
            (([[0, 6, 0], [5, 8, 7], [0, 9, 0]],), 24),
            (([[1, 0, 7], [2, 0, 6], [3, 4, 5], [0, 3, 0], [9, 0, 20]],), 28),
            (([[0]],), 0),
            (([[5]],), 5),
            (([[1, 1], [1, 1]],), 4),
        ],
        hints=[
            "Try every non-empty cell as the starting point.",
            (
                "From a cell, explore the four neighbours depth-first, never stepping on a cell already on the "
                "current path."
            ),
            (
                "Mark the cell as used (for example set it to 0) before exploring and restore it afterwards - that "
                "is the 'undo' of backtracking."
            ),
        ],
        pattern="Grid backtracking: mark, explore, un-mark",
        explain=(
            "A path may not revisit cells, but different paths may share cells, so the 'visited' mark must be "
            "undone when the DFS returns. Trying every start and every simple path is exponential in general, but "
            "the problem guarantees at most 25 non-empty cells, which is fine."
        ),
        cx="O(cells * 3^cells) worst case; O(cells) depth",
        brute_cx="same search, but each step copies the path list and tests membership in O(length)",
        brute=r"""
# BRUTE FORCE: same search, but each step copies the path list and tests membership in O(length)
def get_maximum_gold(grid):
    rows, cols = len(grid), len(grid[0])
    best = 0

    def walk(r, c, path, total):
        nonlocal best
        best = max(best, total)
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != 0 and (nr, nc) not in path:
                walk(nr, nc, path + [(nr, nc)], total + grid[nr][nc])

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0:
                walk(r, c, [(r, c)], grid[r][c])
    return best
""",
        solution=r"""
# OPTIMISED: O(cells * 3^cells) worst case; O(cells) depth
# Idea: Grid backtracking: mark, explore, un-mark
def get_maximum_gold(grid):
    rows, cols = len(grid), len(grid[0])

    def dfs(r, c):
        gold = grid[r][c]
        grid[r][c] = 0
        best = 0
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] > 0:
                best = max(best, dfs(nr, nc))
        grid[r][c] = gold
        return gold + best

    return max((dfs(r, c) for r in range(rows) for c in range(cols) if grid[r][c] > 0), default=0)
""",
    ),
    # ---- The k-th Lexicographical String of All Happy Strings of Length n (LeetCode 1415) ----
    dict(
        title="The k-th Lexicographical String of All Happy Strings of Length n",
        diff="M",
        lc=1415,
        slug="the-k-th-lexicographical-string-of-all-happy-strings-of-length-n",
        prompt=(
            "A happy string uses only the letters a, b, c and has no two equal neighbouring letters. List all happy "
            "strings of length n in lexicographic order and return the k-th one, or '' if there are fewer than k."
        ),
        sig="def get_happy_string(n: int, k: int) -> str:",
        fn="get_happy_string",
        tests=[
            ((1, 3), "c"),
            ((1, 4), ""),
            ((3, 9), "cab"),
            ((2, 7), ""),
            ((3, 1), "aba"),
            ((2, 6), "cb"),
            ((10, 100), "abacbabacb"),
        ],
        hints=[
            "Generating all strings in order and indexing works - how many are there?",
            "There are 3 * 2^(n-1): 3 choices for the first letter, 2 for each later one.",
            (
                "Skip whole blocks: the first letter is chosen by k // 2^(n-1), then each later letter by the "
                "remaining k divided by the block size among the two allowed letters."
            ),
        ],
        pattern="Counting subtrees to skip branches (backtracking without enumerating)",
        explain=(
            "The decision tree is regular: after fixing a prefix, every continuation of the remaining length has "
            "the same number of leaves (2^remaining). So instead of enumerating, divide k by the leaf count of each "
            "branch to pick the right child, then continue inside it with the remainder."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(3 * 2^n * n) time - generate every happy string in order",
        brute=r"""
# BRUTE FORCE: O(3 * 2^n * n) time - generate every happy string in order
def get_happy_string(n, k):
    found = []

    def build(prefix):
        if len(prefix) == n:
            found.append(prefix)
            return
        for ch in "abc":
            if not prefix or prefix[-1] != ch:
                build(prefix + ch)

    build("")
    return found[k - 1] if k <= len(found) else ""
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Counting subtrees to skip branches (backtracking without enumerating)
def get_happy_string(n, k):
    total = 3 * 2 ** (n - 1)
    if k > total:
        return ""
    k -= 1
    block = 2 ** (n - 1)
    out = ["abc"[k // block]]
    k %= block
    for _ in range(1, n):
        block //= 2
        choices = [ch for ch in "abc" if ch != out[-1]]
        out.append(choices[k // block])
        k %= block
    return "".join(out)
""",
    ),
    # ---- Maximum Length of a Concatenated String with Unique Characters (LeetCode 1239) ----
    dict(
        title="Maximum Length of a Concatenated String with Unique Characters",
        diff="M",
        lc=1239,
        slug="maximum-length-of-a-concatenated-string-with-unique-characters",
        prompt=(
            "arr is a list of lowercase strings. Choose a subsequence of arr and concatenate it so the result has "
            "no repeated letter. Return the maximum possible length of such a result."
        ),
        sig="def max_length(arr: List[str]) -> int:",
        fn="max_length",
        tests=[
            ((["un", "iq", "ue"],), 4),
            ((["cha", "r", "act", "ers"],), 6),
            ((["abcdefghijklmnopqrstuvwxyz"],), 26),
            ((["aa", "bb"],), 0),
            ((["a", "b", "c"],), 3),
            ((["ab", "ba"],), 2),
        ],
        hints=[
            "Strings that repeat a letter by themselves can never be used - discard them first.",
            (
                "Represent each usable string by a bitmask of its letters; two strings fit together iff their masks "
                "do not overlap."
            ),
            "Keep the set of all masks reachable so far; for each new string combine it with every compatible mask.",
        ],
        pattern="Subset search with bitmask conflict checks",
        explain=(
            "Only the set of letters matters, not their order, and at most 26 distinct letters can ever be used, so "
            "the set of reachable masks is small. A new string extends exactly those masks that do not share a "
            "letter with it; the answer is the largest popcount of any reachable mask."
        ),
        cx="O(n * 2^min(n, 26)) worst case, usually far smaller; O(reachable masks) space",
        brute_cx="O(2^n * L) time - build and test every subset",
        brute=r"""
# BRUTE FORCE: O(2^n * L) time - build and test every subset
def max_length(arr):
    best = 0
    for mask in range(1 << len(arr)):
        joined = "".join(arr[i] for i in range(len(arr)) if mask >> i & 1)
        if len(set(joined)) == len(joined):
            best = max(best, len(joined))
    return best
""",
        solution=r"""
# OPTIMISED: O(n * 2^min(n, 26)) worst case, usually far smaller; O(reachable masks) space
# Idea: Subset search with bitmask conflict checks
def max_length(arr):
    masks = {0}
    best = 0
    for word in arr:
        word_mask = 0
        for ch in word:
            bit = 1 << (ord(ch) - 97)
            if word_mask & bit:
                word_mask = -1
                break
            word_mask |= bit
        if word_mask < 0:
            continue
        for existing in list(masks):
            if existing & word_mask == 0:
                merged = existing | word_mask
                masks.add(merged)
                best = max(best, bin(merged).count("1"))
    return best
""",
    ),
    # ---- Unique Paths III (LeetCode 980) ----
    dict(
        title="Unique Paths III",
        diff="H",
        lc=980,
        slug="unique-paths-iii",
        prompt=(
            "grid has 1 = start, 2 = end, 0 = empty square, -1 = obstacle. Count the 4-directional walks from the "
            "start to the end that step on every non-obstacle square exactly once."
        ),
        sig="def unique_paths_iii(grid: List[List[int]]) -> int:",
        fn="unique_paths_iii",
        tests=[
            (([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 2, -1]],), 2),
            (([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 2]],), 4),
            (([[0, 1], [2, 0]],), 0),
            (([[1, 2]],), 1),
        ],
        hints=[
            "Count how many squares must be visited so you know when a walk is complete.",
            "Depth-first search from the start, marking squares as visited and restoring them on the way back.",
            "Reaching the end only counts when no walkable square is left to visit (remaining == 0).",
        ],
        pattern="Hamiltonian-style path counting by backtracking",
        explain=(
            "A valid walk must cover every walkable square exactly once, so it is a Hamiltonian path from start to "
            "end. DFS with mark/un-mark explores all simple paths; the walk counts only if it reaches the end with "
            "zero squares left, which prunes every early arrival at the end."
        ),
        cx="O(3^cells) worst case; O(cells) depth",
        brute_cx="O(3^cells * cells) time - every simple path, copying the path list at each step",
        brute=r"""
# BRUTE FORCE: O(3^cells * cells) time - every simple path, copying the path list at each step
def unique_paths_iii(grid):
    rows, cols = len(grid), len(grid[0])
    walkable = sum(cell != -1 for row in grid for cell in row)
    start = next((r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1)
    count = 0

    def walk(r, c, path):
        nonlocal count
        if grid[r][c] == 2:
            if len(path) == walkable:
                count += 1
            return
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != -1 and (nr, nc) not in path:
                walk(nr, nc, path + [(nr, nc)])

    walk(start[0], start[1], [start])
    return count
""",
        solution=r"""
# OPTIMISED: O(3^cells) worst case; O(cells) depth
# Idea: Hamiltonian-style path counting by backtracking
def unique_paths_iii(grid):
    rows, cols = len(grid), len(grid[0])
    remaining = 1
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                start = (r, c)
            elif grid[r][c] == 0:
                remaining += 1

    def dfs(r, c, left):
        if grid[r][c] == 2:
            return 1 if left == 0 else 0
        saved, grid[r][c] = grid[r][c], -1
        total = 0
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] != -1:
                total += dfs(nr, nc, left - 1)
        grid[r][c] = saved
        return total

    return dfs(start[0], start[1], remaining)
""",
    ),
    # ---- Split a String Into the Max Number of Unique Substrings (LeetCode 1593) ----
    dict(
        title="Split a String Into the Max Number of Unique Substrings",
        diff="M",
        lc=1593,
        slug="split-a-string-into-the-max-number-of-unique-substrings",
        prompt=(
            "Split s into non-empty substrings (concatenating them gives s) so that all substrings are different. "
            "Return the maximum number of substrings you can get."
        ),
        sig="def max_unique_split(s: str) -> int:",
        fn="max_unique_split",
        tests=[
            (("ababccc",), 5),
            (("aba",), 2),
            (("aa",), 1),
            (("a",), 1),
            (("abc",), 3),
        ],
        hints=[
            "At each position choose where the next piece ends, remembering which pieces you already used.",
            "Use a set of used pieces; add before recursing and remove after (undo).",
            "Prune: if pieces so far + characters left cannot beat the best answer, stop.",
        ],
        pattern="Backtracking over cut points with a 'used' set and a bound",
        explain=(
            "The state is the start position plus the set of pieces used so far, so memoisation does not apply, but "
            "a simple bound works: even if every remaining character became its own piece, count + remaining "
            "characters must exceed the best known answer or the branch is useless."
        ),
        cx="O(2^n) worst case (n <= 16), pruned in practice; O(n) depth",
        brute_cx="O(2^n * n) time - try every set of cut positions and check uniqueness",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - try every set of cut positions and check uniqueness
def max_unique_split(s):
    n = len(s)
    best = 1
    for mask in range(1 << (n - 1)):
        pieces, start = [], 0
        for i in range(n - 1):
            if mask >> i & 1:
                pieces.append(s[start : i + 1])
                start = i + 1
        pieces.append(s[start:])
        if len(set(pieces)) == len(pieces):
            best = max(best, len(pieces))
    return best
""",
        solution=r"""
# OPTIMISED: O(2^n) worst case (n <= 16), pruned in practice; O(n) depth
# Idea: Backtracking over cut points with a 'used' set and a bound
def max_unique_split(s):
    best = 0
    used = set()

    def go(start, count):
        nonlocal best
        if count + (len(s) - start) <= best:
            return
        if start == len(s):
            best = count
            return
        for end in range(start + 1, len(s) + 1):
            piece = s[start:end]
            if piece not in used:
                used.add(piece)
                go(end, count + 1)
                used.remove(piece)

    go(0, 0)
    return best
""",
    ),
]
