"""extra batch of Backtracking problems - the problem bank for the "backtracking" topic (batch 5).

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


def _gray_ok(args, got):
    """True if got is a valid n-bit Gray code: 2**n distinct values, start at 0, neighbours (cyclic) differ by 1 bit."""
    size = 1 << args[0]
    if not isinstance(got, list) or len(got) != size or len(set(got)) != size or got[0] != 0:
        return False
    if any(not 0 <= x < size for x in got):
        return False
    return all(bin(got[i] ^ got[(i + 1) % size]).count("1") == 1 for i in range(size))


def _unique_ok(args, got):
    """True if got is a binary string of length n that is not in nums."""
    nums = args[0]
    return isinstance(got, str) and len(got) == len(nums) and set(got) <= {"0", "1"} and got not in nums


def _fib_ok(num, parts):
    """True if parts is a valid Fibonacci-like split of the digit string num."""
    if len(parts) < 3 or "".join(map(str, parts)) != num:
        return False
    if any(p > 2**31 - 1 for p in parts):
        return False
    return all(parts[i] + parts[i + 1] == parts[i + 2] for i in range(len(parts) - 2))


def _fib_exists(num):
    """Exhaustive oracle: does ANY valid split exist?"""
    n = len(num)
    for mask in range(1 << (n - 1)):
        cuts = [0] + [i + 1 for i in range(n - 1) if (mask >> i) & 1] + [n]
        parts = [int(num[cuts[k] : cuts[k + 1]]) for k in range(len(cuts) - 1)]
        if _fib_ok(num, parts):
            return True
    return False


def _fib_check(args, got):
    num = args[0]
    if not got:
        return not _fib_exists(num)
    return _fib_ok(num, got)


PROBLEMS = [
    # ---- Gray Code (LeetCode 89) ----
    dict(
        title="Gray Code",
        diff="M",
        lc=89,
        slug="gray-code",
        prompt=(
            "An n-bit Gray code sequence has 2^n integers in [0, 2^n - 1], starts with 0, contains every value "
            "exactly once, and any two adjacent values (including the last and the first) differ in exactly one "
            "bit. Return any valid sequence."
        ),
        sig="def gray_code(n: int) -> List[int]:",
        fn="gray_code",
        check=_gray_ok,
        tests=[
            ((1,), [0, 1]),
            ((2,), [0, 1, 3, 2]),
            ((3,), [0, 1, 3, 2, 6, 7, 5, 4]),
        ],
        hints=[
            (
                "Think of the values as corners of a hypercube; you want a path through all corners that moves "
                "along one edge at a time and can return to the start."
            ),
            "Backtracking: from the current value try flipping each bit, skipping values already used.",
            "There is also a closed form: the i-th Gray code is i ^ (i >> 1).",
        ],
        pattern="Backtracking over a hypercube (or the reflected binary formula)",
        explain=(
            "Brute force walks the hypercube depth-first, flipping one bit at a time, and backtracks when stuck; "
            "the first full cycle is a valid answer. The reflected Gray code gets there directly: i ^ (i >> 1) "
            "changes exactly one bit between consecutive i, because incrementing i flips a trailing block of bits "
            "and the shifted copy flips the neighbour of that block's top bit, cancelling all but one change."
        ),
        cx="O(2^n) time, O(2^n) space",
        brute_cx="exponential - depth-first search for a Hamiltonian cycle on the hypercube",
        brute=r"""
# BRUTE FORCE: exponential - depth-first search for a Hamiltonian cycle on the hypercube
def gray_code(n):
    size = 1 << n
    path = [0]
    used = {0}

    def dfs():
        if len(path) == size:
            return bin(path[-1]).count("1") == 1 or size == 1
        for bit in range(n):
            nxt = path[-1] ^ (1 << bit)
            if nxt not in used:
                used.add(nxt)
                path.append(nxt)
                if dfs():
                    return True
                path.pop()
                used.remove(nxt)
        return False

    dfs()
    return path
""",
        solution=r"""
# OPTIMISED: O(2^n) time, O(2^n) space
# Idea: Backtracking over a hypercube (or the reflected binary formula)
def gray_code(n):
    return [i ^ (i >> 1) for i in range(1 << n)]
""",
    ),
    # ---- Additive Number (LeetCode 306) ----
    dict(
        title="Additive Number",
        diff="M",
        lc=306,
        slug="additive-number",
        prompt=(
            "A string of digits is an additive number if it can be split into at least three numbers (no leading "
            "zeros unless the number is exactly 0) such that each number from the third on is the sum of the "
            "previous two. Return True if num is additive."
        ),
        sig="def is_additive_number(num: str) -> bool:",
        fn="is_additive_number",
        tests=[
            (("112358",), True),
            (("199100199",), True),
            (("1023",), False),
            (("101",), True),
            (("11",), False),
            (("000",), True),
        ],
        hints=[
            "Once the first two numbers are chosen, the whole sequence is forced.",
            (
                "Choose the end of the first number and the end of the second number (two nested loops), skipping "
                "parts with leading zeros."
            ),
            (
                "Then keep generating x + y and check that the string continues with exactly those digits until it "
                "is used up."
            ),
        ],
        pattern="Choose the seed (first two parts), then verify deterministically",
        explain=(
            "The recurrence determines everything after the first two numbers, so trying all O(n^2) seeds and "
            "verifying each in O(n) decides the problem. Leading-zero parts are rejected immediately, and a "
            "mismatch in the generated digits abandons that seed early. Brute force instead tries every way to cut "
            "the string and tests the recurrence on all parts."
        ),
        cx="O(n^3) time, O(n) space",
        brute_cx="O(2^n * n) time - try every set of cut positions",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - try every set of cut positions
def is_additive_number(num):
    n = len(num)
    for mask in range(1 << (n - 1)):
        cuts = [0] + [i + 1 for i in range(n - 1) if (mask >> i) & 1] + [n]
        pieces = [num[cuts[k] : cuts[k + 1]] for k in range(len(cuts) - 1)]
        if len(pieces) < 3:
            continue
        if any(len(p) > 1 and p[0] == "0" for p in pieces):
            continue
        values = [int(p) for p in pieces]
        if all(values[i] == values[i - 1] + values[i - 2] for i in range(2, len(values))):
            return True
    return False
""",
        solution=r"""
# OPTIMISED: O(n^3) time, O(n) space
# Idea: Choose the seed (first two parts), then verify deterministically
def is_additive_number(num):
    n = len(num)
    for i in range(1, n):
        for j in range(i + 1, n):
            first, second = num[:i], num[i:j]
            if (len(first) > 1 and first[0] == "0") or (len(second) > 1 and second[0] == "0"):
                continue
            x, y = int(first), int(second)
            pos = j
            while pos < n:
                z = str(x + y)
                if not num.startswith(z, pos):
                    break
                pos += len(z)
                x, y = y, x + y
            else:
                return True
    return False
""",
    ),
    # ---- Reconstruct Itinerary (LeetCode 332) ----
    dict(
        title="Reconstruct Itinerary",
        diff="H",
        lc=332,
        slug="reconstruct-itinerary",
        prompt=(
            "tickets[i] = [from, to] are airline tickets. Rebuild the itinerary that starts at 'JFK' and uses every "
            "ticket exactly once. If several itineraries exist, return the one that is smallest in lexical order. "
            "(A valid itinerary is guaranteed to exist.)"
        ),
        sig="def find_itinerary(tickets: List[List[str]]) -> List[str]:",
        fn="find_itinerary",
        tests=[
            (
                ([["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]],),
                ["JFK", "MUC", "LHR", "SFO", "SJC"],
            ),
            (
                ([["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]],),
                ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"],
            ),
            (([["JFK", "A"]],), ["JFK", "A"]),
        ],
        hints=[
            (
                "Model airports as nodes and tickets as directed edges: you need a path that uses every edge once "
                "(an Eulerian path)."
            ),
            "A greedy 'always take the smallest destination' can strand you at a dead end before all tickets are used.",
            (
                "Hierholzer's algorithm: depth-first, always follow the smallest unused edge, and append an airport "
                "to the route only when it has no more outgoing tickets; reverse at the end."
            ),
        ],
        pattern="Eulerian path (Hierholzer) / backtracking over tickets",
        explain=(
            "Backtracking tries the smallest ticket first and undoes it if the walk gets stuck before using all "
            "tickets, which is correct but can retry a lot. Hierholzer's trick avoids the retries: a dead-end "
            "airport can only be the LAST stop, so it is written to the route first when the recursion unwinds; "
            "reversing the post-order gives the itinerary, and exploring edges in sorted order makes it the "
            "lexically smallest."
        ),
        cx="O(E log E) time, O(E) space",
        brute_cx="exponential in the worst case - depth-first search over tickets with backtracking",
        brute=r"""
# BRUTE FORCE: exponential in the worst case - depth-first search over tickets with backtracking
def find_itinerary(tickets):
    tickets = sorted(tickets)
    total = len(tickets)
    used = [False] * total
    path = ["JFK"]

    def dfs():
        if len(path) == total + 1:
            return True
        for i, (origin, target) in enumerate(tickets):
            if not used[i] and origin == path[-1]:
                used[i] = True
                path.append(target)
                if dfs():
                    return True
                path.pop()
                used[i] = False
        return False

    dfs()
    return path
""",
        solution=r"""
# OPTIMISED: O(E log E) time, O(E) space
# Idea: Eulerian path (Hierholzer) / backtracking over tickets
def find_itinerary(tickets):
    graph = defaultdict(list)
    for origin, target in sorted(tickets, reverse=True):
        graph[origin].append(target)
    route = []

    def visit(airport):
        while graph[airport]:
            visit(graph[airport].pop())
        route.append(airport)

    visit("JFK")
    return route[::-1]
""",
    ),
    # ---- Binary Watch (LeetCode 401) ----
    dict(
        title="Binary Watch",
        diff="E",
        lc=401,
        slug="binary-watch",
        prompt=(
            "A binary watch has 4 LEDs for the hour (0-11) and 6 LEDs for the minutes (0-59). Given the number of "
            "LEDs that are currently on, return all times the watch could show, formatted 'h:mm' (no leading zero "
            "on the hour, two digits for the minutes), in any order."
        ),
        sig="def read_binary_watch(turned_on: int) -> List[str]:",
        fn="read_binary_watch",
        compare="unordered",
        tests=[
            ((0,), ["0:00"]),
            (
                (1,),
                ["0:01", "0:02", "0:04", "0:08", "0:16", "0:32", "1:00", "2:00", "4:00", "8:00"],
            ),
            ((9,), []),
        ],
        hints=[
            "There are only 10 LEDs - and only 12 * 60 = 720 possible times.",
            (
                "Choose which turned_on LEDs of the 10 are lit (combinations), then read the first four as the hour "
                "bits and the rest as the minute bits."
            ),
            "Discard choices where the hour is 12 or more or the minute is 60 or more.",
        ],
        pattern="Choose k of n positions (combinations), then validate",
        explain=(
            "Selecting which LEDs are on is a combination problem over 10 positions. Each selection defines an hour "
            "and a minute by adding up the bit values; selections that decode to an impossible time are skipped. "
            "Enumerating all 720 times and counting set bits (the brute force) works too, since the state space is "
            "tiny."
        ),
        cx="O(C(10, k)) time, at most 252 selections",
        brute_cx="O(720) time - test every possible time",
        brute=r"""
# BRUTE FORCE: O(720) time - test every possible time
def read_binary_watch(turned_on):
    times = []
    for hour in range(12):
        for minute in range(60):
            if bin(hour).count("1") + bin(minute).count("1") == turned_on:
                times.append(f"{hour}:{minute:02d}")
    return times
""",
        solution=r"""
# OPTIMISED: O(C(10, k)) time, at most 252 selections
# Idea: Choose k of n positions (combinations), then validate
def read_binary_watch(turned_on):
    times = []
    for leds in itertools.combinations(range(10), turned_on):
        hour = minute = 0
        for led in leds:
            if led < 4:
                hour += 1 << led
            else:
                minute += 1 << (led - 4)
        if hour < 12 and minute < 60:
            times.append(f"{hour}:{minute:02d}")
    return times
""",
    ),
    # ---- 24 Game (LeetCode 679) ----
    dict(
        title="24 Game",
        diff="H",
        lc=679,
        slug="24-game",
        prompt=(
            "You are given four cards with values 1 to 9. Using each card exactly once, with the operators +, -, * "
            "and / (real division) and any parentheses, can you make 24? Unary minus is not allowed and the cards "
            "cannot be concatenated."
        ),
        sig="def judge_point24(cards: List[int]) -> bool:",
        fn="judge_point24",
        tests=[
            (([4, 1, 8, 7],), True),
            (([1, 2, 1, 2],), False),
            (([3, 3, 8, 8],), True),
            (([1, 1, 1, 1],), False),
            (([6, 6, 6, 6],), True),
        ],
        hints=[
            "Any expression combines two numbers at a time; after one combination you have a list one element shorter.",
            (
                "Recursively pick any two numbers, replace them with the result of each possible operation, and "
                "recurse on the shorter list."
            ),
            (
                "Division is not commutative, so try both a/b and b/a (skip zero divisors); compare with 24 using a "
                "small tolerance because of floating point."
            ),
        ],
        pattern="Backtracking over pairwise combinations",
        explain=(
            "Every way of parenthesising an expression is a sequence of 'merge two numbers' steps, so the search "
            "space is: choose a pair (6 ways for 4 numbers), choose an operation (up to 6 results counting reversed "
            "- and /), recurse on 3 numbers, then 2, then 1. That is at most 6 * 6 * 6 * 6 * 6 * 6 = 46,656 leaves. "
            "The brute force instead enumerates permutations of the cards and the five bracket shapes with every "
            "operator choice."
        ),
        cx="O(1) - at most 46,656 leaves for four cards",
        brute_cx="O(1) - 24 orders x 64 operator choices x 5 bracket shapes",
        brute=r"""
# BRUTE FORCE: O(1) - 24 orders x 64 operator choices x 5 bracket shapes
def judge_point24(cards):
    ops = [
        lambda x, y: x + y,
        lambda x, y: x - y,
        lambda x, y: x * y,
        lambda x, y: x / y,
    ]
    shapes = [
        lambda a, b, c, d, f, g, h: h(g(f(a, b), c), d),
        lambda a, b, c, d, f, g, h: h(f(a, b), g(c, d)),
        lambda a, b, c, d, f, g, h: h(g(a, f(b, c)), d),
        lambda a, b, c, d, f, g, h: h(a, g(f(b, c), d)),
        lambda a, b, c, d, f, g, h: h(a, g(b, f(c, d))),
    ]
    for a, b, c, d in itertools.permutations(cards):
        for f in ops:
            for g in ops:
                for h in ops:
                    for shape in shapes:
                        try:
                            value = shape(a, b, c, d, f, g, h)
                        except ZeroDivisionError:
                            continue
                        if abs(value - 24) < 1e-6:
                            return True
    return False
""",
        solution=r"""
# OPTIMISED: O(1) - at most 46,656 leaves for four cards
# Idea: Backtracking over pairwise combinations
def judge_point24(cards):
    def solve(nums):
        if len(nums) == 1:
            return abs(nums[0] - 24) < 1e-6
        for i in range(len(nums)):
            for j in range(i + 1, len(nums)):
                rest = [nums[k] for k in range(len(nums)) if k != i and k != j]
                a, b = nums[i], nums[j]
                options = [a + b, a - b, b - a, a * b]
                if abs(b) > 1e-9:
                    options.append(a / b)
                if abs(a) > 1e-9:
                    options.append(b / a)
                if any(solve(rest + [value]) for value in options):
                    return True
        return False

    return solve([float(c) for c in cards])
""",
    ),
    # ---- Pyramid Transition Matrix (LeetCode 756) ----
    dict(
        title="Pyramid Transition Matrix",
        diff="M",
        lc=756,
        slug="pyramid-transition-matrix",
        prompt=(
            "Build a pyramid from the bottom row. A block on a higher row sits on two adjacent blocks of the row "
            "below; allowed is a list of triples 'ABC' meaning a block C may sit on top of blocks A (left) and B "
            "(right). Return True if you can build the pyramid all the way to a single top block using only allowed "
            "triples."
        ),
        sig="def pyramid_transition(bottom: str, allowed: List[str]) -> bool:",
        fn="pyramid_transition",
        tests=[
            (("BCD", ["BCC", "CDE", "CEA", "FFF"]), True),
            (("AAAA", ["AAB", "AAC", "BCD", "BBE", "DEF"]), False),
            (("AB", ["ABC"]), True),
            (("AB", []), False),
        ],
        hints=[
            "Each pair of adjacent blocks offers a set of possible blocks for the row above.",
            "Generate every possible next row from the product of those option sets, then recurse on it.",
            "Many rows repeat across branches - memoise rows that have already been shown unbuildable.",
        ],
        pattern="Backtracking row by row (with memoisation)",
        explain=(
            "Choosing the next row is the only decision; everything above depends on it alone. Taking the cartesian "
            "product of the per-pair options enumerates all candidate rows, and recursing finds out whether any "
            "reaches height one. Memoising on the row string stops the search from re-exploring the same row "
            "reached through different choices."
        ),
        cx="exponential in the worst case, memoised per distinct row",
        brute_cx="exponential - expand level by level without early exit",
        brute=r"""
# BRUTE FORCE: exponential - expand level by level without early exit
def pyramid_transition(bottom, allowed):
    options = {}
    for triple in allowed:
        options.setdefault(triple[:2], []).append(triple[2])
    level = {bottom}
    for _ in range(len(bottom) - 1):
        following = set()
        for row in level:
            choices = [options.get(row[i : i + 2], []) for i in range(len(row) - 1)]
            if all(choices):
                for combo in itertools.product(*choices):
                    following.add("".join(combo))
        level = following
        if not level:
            return False
    return True
""",
        solution=r"""
# OPTIMISED: exponential in the worst case, memoised per distinct row
# Idea: Backtracking row by row (with memoisation)
def pyramid_transition(bottom, allowed):
    tops = defaultdict(list)
    for a, b, c in allowed:
        tops[(a, b)].append(c)

    @lru_cache(None)
    def can_build(row):
        if len(row) == 1:
            return True
        choices = [tops.get((row[i], row[i + 1]), []) for i in range(len(row) - 1)]
        if any(not option for option in choices):
            return False
        return any(can_build("".join(nxt)) for nxt in itertools.product(*choices))

    return can_build(bottom)
""",
    ),
    # ---- Split Array into Fibonacci Sequence (LeetCode 842) ----
    dict(
        title="Split Array into Fibonacci Sequence",
        diff="M",
        lc=842,
        slug="split-array-into-fibonacci-sequence",
        prompt=(
            "Split the digit string num into a Fibonacci-like sequence of at least 3 non-negative integers: no "
            "leading zeros (except the number 0 itself), every value fits in a signed 32-bit integer, and each "
            "value from the third is the sum of the previous two. Return any valid sequence, or [] if none exists."
        ),
        sig="def split_into_fibonacci(num: str) -> List[int]:",
        fn="split_into_fibonacci",
        check=_fib_check,
        tests=[
            (("123456579",), [123, 456, 579]),
            (("11235813",), [1, 1, 2, 3, 5, 8, 13]),
            (("112358130",), []),
            (("0123",), []),
            (("1101111",), [11, 0, 11, 11]),
            (("000",), [0, 0, 0]),
        ],
        hints=[
            "Pick the next number as a prefix of the remaining digits - at each step you have a few lengths to try.",
            "After two numbers are fixed, the next value is forced: it must equal their sum.",
            (
                "Prune hard: stop growing a candidate when it has a leading zero, exceeds 2^31 - 1, or is larger "
                "than the required sum."
            ),
        ],
        pattern="Backtracking with pruning (prefix choices + forced sums)",
        explain=(
            "Depth-first search builds the sequence number by number. Candidate numbers are prefixes of the rest of "
            "the string, and once two numbers exist the third is determined, so a candidate that is smaller than "
            "the target sum is skipped and a larger one ends the loop (longer prefixes only grow). The leading-zero "
            "and 32-bit rules cut the remaining branches. The brute force tries every cut set."
        ),
        cx="O(n^2) candidate prefixes per level in the worst case, far less with pruning",
        brute_cx="O(2^n * n) time - try every set of cut positions",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - try every set of cut positions
def split_into_fibonacci(num):
    n = len(num)
    limit = 2**31 - 1
    for mask in range(1 << (n - 1)):
        cuts = [0] + [i + 1 for i in range(n - 1) if (mask >> i) & 1] + [n]
        pieces = [num[cuts[k] : cuts[k + 1]] for k in range(len(cuts) - 1)]
        if len(pieces) < 3:
            continue
        if any(len(p) > 1 and p[0] == "0" for p in pieces):
            continue
        values = [int(p) for p in pieces]
        if any(v > limit for v in values):
            continue
        if all(values[i] + values[i + 1] == values[i + 2] for i in range(len(values) - 2)):
            return values
    return []
""",
        solution=r"""
# OPTIMISED: O(n^2) candidate prefixes per level in the worst case, far less with pruning
# Idea: Backtracking with pruning (prefix choices + forced sums)
def split_into_fibonacci(num):
    n = len(num)
    limit = 2**31 - 1
    result = []

    def dfs(pos):
        if pos == n:
            return len(result) >= 3
        for end in range(pos + 1, n + 1):
            if num[pos] == "0" and end > pos + 1:
                break
            value = int(num[pos:end])
            if value > limit:
                break
            if len(result) >= 2:
                target = result[-1] + result[-2]
                if value < target:
                    continue
                if value > target:
                    break
            result.append(value)
            if dfs(end):
                return True
            result.pop()
        return False

    return result if dfs(0) else []
""",
    ),
    # ---- Number of Squareful Arrays (LeetCode 996) ----
    dict(
        title="Number of Squareful Arrays",
        diff="H",
        lc=996,
        slug="number-of-squareful-arrays",
        prompt=(
            "An array is squareful if the sum of every pair of adjacent elements is a perfect square. Return the "
            "number of distinct permutations of nums that are squareful (two permutations are different if some "
            "index holds different values)."
        ),
        sig="def num_squareful_perms(nums: List[int]) -> int:",
        fn="num_squareful_perms",
        tests=[
            (([1, 17, 8],), 2),
            (([2, 2, 2],), 1),
            (([1],), 1),
            (([1, 3],), 2),
            (([1, 2],), 0),
        ],
        hints=[
            "Build the permutation left to right; each new element must make a perfect square with the previous one.",
            (
                "Duplicates would create repeated permutations - iterate over distinct VALUES with a count, not "
                "over positions."
            ),
            (
                "Backtrack with a Counter: choose a value with remaining count > 0 whose sum with the previous "
                "element is a square, recurse, restore."
            ),
        ],
        pattern="Backtracking over multiset permutations with a validity filter",
        explain=(
            "Pruning is the point: as soon as an adjacent sum is not a square, the whole subtree of permutations "
            "that start this way is discarded. Iterating over distinct values with remaining counts generates each "
            "distinct permutation exactly once. The brute force generates all n! permutations, deduplicates them "
            "with a set, and tests each."
        ),
        cx="O(n!) worst case, usually far less because of pruning",
        brute_cx="O(n! * n) time - test every permutation",
        brute=r"""
# BRUTE FORCE: O(n! * n) time - test every permutation
def num_squareful_perms(nums):
    def is_square(value):
        root = math.isqrt(value)
        return root * root == value

    count = 0
    for perm in set(itertools.permutations(nums)):
        if all(is_square(perm[i] + perm[i + 1]) for i in range(len(perm) - 1)):
            count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n!) worst case, usually far less because of pruning
# Idea: Backtracking over multiset permutations with a validity filter
def num_squareful_perms(nums):
    count = Counter(nums)
    values = list(count)

    def is_square(value):
        root = math.isqrt(value)
        return root * root == value

    def dfs(previous, remaining):
        if remaining == 0:
            return 1
        ways = 0
        for x in values:
            if count[x] == 0:
                continue
            if previous is not None and not is_square(previous + x):
                continue
            count[x] -= 1
            ways += dfs(x, remaining - 1)
            count[x] += 1
        return ways

    return dfs(None, len(nums))
""",
    ),
    # ---- Maximum Score Words Formed by Letters (LeetCode 1255) ----
    dict(
        title="Maximum Score Words Formed by Letters",
        diff="H",
        lc=1255,
        slug="maximum-score-words-formed-by-letters",
        prompt=(
            "words is a list of words, letters a multiset of available letters, and score[i] the value of the "
            "letter chr(97 + i). Each word may be used at most once, and a word can be formed only if enough "
            "letters remain (each letter is used at most as many times as it appears in letters). The score of a "
            "set of words is the sum of the scores of all their letters. Return the maximum score."
        ),
        sig="def max_score_words(words: List[str], letters: List[str], score: List[int]) -> int:",
        fn="max_score_words",
        tests=[
            (
                (
                    ["dog", "cat", "dad", "good"],
                    ["a", "a", "c", "d", "d", "d", "g", "o", "o"],
                    [1, 0, 9, 5, 0, 0, 3] + [0] * 7 + [2] + [0] * 11,
                ),
                23,
            ),
            (
                (
                    ["xxxz", "ax", "bx", "cx"],
                    ["z", "a", "b", "c", "x", "x", "x"],
                    [4, 4, 4] + [0] * 20 + [5, 0, 10],
                ),
                27,
            ),
            (
                (
                    ["leetcode"],
                    ["l", "e", "t", "c", "o", "d"],
                    [0, 0, 1, 1, 1] + [0] * 6 + [1, 0, 0, 1] + [0] * 4 + [1] + [0] * 6,
                ),
                0,
            ),
        ],
        hints=[
            "For each word there are only two choices: use it or skip it.",
            "Keep the letter counts that are still available while you recurse.",
            "To use a word, check that the counts allow it, subtract, recurse, then add the counts back (undo).",
        ],
        pattern="Include / exclude backtracking with a resource counter",
        explain=(
            "At most 14 words means at most 2^14 subsets. Recursion decides word by word: skipping costs nothing, "
            "taking is possible only if the remaining letter counts cover the word, and the counts are restored on "
            "return. A word's score depends only on its own letters, so the best score is the max over the two "
            "branches. The brute force tests every subset mask against the full letter multiset."
        ),
        cx="O(2^n * L) time, O(n + 26) space",
        brute_cx="O(2^n * n * L) time - total the letters of every subset",
        brute=r"""
# BRUTE FORCE: O(2^n * n * L) time - total the letters of every subset
def max_score_words(words, letters, score):
    have = Counter(letters)
    best = 0
    for mask in range(1 << len(words)):
        need = Counter()
        for i, word in enumerate(words):
            if (mask >> i) & 1:
                need.update(word)
        if all(have[c] >= v for c, v in need.items()):
            best = max(best, sum(score[ord(c) - 97] * v for c, v in need.items()))
    return best
""",
        solution=r"""
# OPTIMISED: O(2^n * L) time, O(n + 26) space
# Idea: Include / exclude backtracking with a resource counter
def max_score_words(words, letters, score):
    have = Counter(letters)

    def dfs(i):
        if i == len(words):
            return 0
        best = dfs(i + 1)
        word = words[i]
        need = Counter(word)
        if all(have[c] >= v for c, v in need.items()):
            for c, v in need.items():
                have[c] -= v
            best = max(best, sum(score[ord(c) - 97] for c in word) + dfs(i + 1))
            for c, v in need.items():
                have[c] += v
        return best

    return dfs(0)
""",
    ),
    # ---- Splitting a String Into Descending Consecutive Values (LeetCode 1849) ----
    dict(
        title="Splitting a String Into Descending Consecutive Values",
        diff="M",
        lc=1849,
        slug="splitting-a-string-into-descending-consecutive-values",
        prompt=(
            "Return True if the digit string s can be split into at least two non-empty substrings (leading zeros "
            "ARE allowed) whose numeric values are in strictly descending order and every pair of adjacent values "
            "differs by exactly 1."
        ),
        sig="def split_string(s: str) -> bool:",
        fn="split_string",
        tests=[
            (("1234",), False),
            (("050043",), True),
            (("9080701",), False),
            (("10009998",), True),
            (("21",), True),
            (("10",), True),
            (("00",), False),
        ],
        hints=[
            "Once the first piece is chosen, the next value must be exactly one less, and so on.",
            (
                "Try every first piece (not the whole string), then recurse: at each position find a prefix of the "
                "rest whose value is prev - 1."
            ),
            (
                "Stop extending a prefix once its value reaches prev - values only grow with length (zeros-padded "
                "values can repeat, so keep going while it is below prev)."
            ),
        ],
        pattern="Backtracking on prefix choices with a forced next value",
        explain=(
            "After the first number is fixed, each next number is forced to be previous - 1, so the search only "
            "branches over how many digits that next number spans (leading zeros allow several lengths with the "
            "same value). Values never shrink as a prefix gets longer, so once a prefix is at least the previous "
            "value there is nothing more to try at that position."
        ),
        cx="O(n^2) time with pruning, O(n) recursion depth",
        brute_cx="O(2^n * n) time - try every set of cut positions",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - try every set of cut positions
def split_string(s):
    n = len(s)
    for mask in range(1 << (n - 1)):
        cuts = [0] + [i + 1 for i in range(n - 1) if (mask >> i) & 1] + [n]
        values = [int(s[cuts[k] : cuts[k + 1]]) for k in range(len(cuts) - 1)]
        if len(values) >= 2 and all(values[i] - values[i + 1] == 1 for i in range(len(values) - 1)):
            return True
    return False
""",
        solution=r"""
# OPTIMISED: O(n^2) time with pruning, O(n) recursion depth
# Idea: Backtracking on prefix choices with a forced next value
def split_string(s):
    n = len(s)

    def dfs(pos, previous):
        if pos == n:
            return True
        for end in range(pos + 1, n + 1):
            value = int(s[pos:end])
            if value == previous - 1 and dfs(end, value):
                return True
            if value >= previous:
                break
        return False

    return any(dfs(end, int(s[:end])) for end in range(1, n))
""",
    ),
    # ---- Find Unique Binary String (LeetCode 1980) ----
    dict(
        title="Find Unique Binary String",
        diff="M",
        lc=1980,
        slug="find-unique-binary-string",
        prompt=(
            "nums contains n distinct binary strings, each of length n. Return ANY binary string of length n that "
            "does not appear in nums."
        ),
        sig="def find_different_binary_string(nums: List[str]) -> str:",
        fn="find_different_binary_string",
        check=_unique_ok,
        tests=[
            ((["01", "10"],), "11"),
            ((["00", "01"],), "10"),
            ((["111", "011", "001"],), "000"),
            ((["0"],), "1"),
        ],
        hints=[
            "There are 2^n strings of length n but only n in the list, so a missing one exists.",
            "Brute force: generate candidates (backtracking over each position's bit) until one is not in the set.",
            (
                "Cantor's diagonal: flip the i-th bit of the i-th string; the result differs from every string in "
                "at least one position."
            ),
        ],
        pattern="Backtracking/enumeration vs the diagonal argument",
        explain=(
            "Enumerating candidates and checking membership in a set works because at most n of the 2^n strings are "
            "taken, so one of the first n + 1 candidates is free. Cantor's diagonal gives the answer in O(n) with "
            "no search at all: the constructed string differs from nums[i] at position i, so it cannot equal any of "
            "them."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n * 2^n) worst case - enumerate candidates until one is missing from the list",
        brute=r"""
# BRUTE FORCE: O(n * 2^n) worst case - enumerate candidates until one is missing from the list
def find_different_binary_string(nums):
    taken = set(nums)
    n = len(nums)
    for value in range(2**n):
        candidate = format(value, f"0{n}b")
        if candidate not in taken:
            return candidate
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Backtracking/enumeration vs the diagonal argument
def find_different_binary_string(nums):
    return "".join("1" if nums[i][i] == "0" else "0" for i in range(len(nums)))
""",
    ),
    # ---- Count Number of Maximum Bitwise-OR Subsets (LeetCode 2044) ----
    dict(
        title="Count Number of Maximum Bitwise-OR Subsets",
        diff="M",
        lc=2044,
        slug="count-number-of-maximum-bitwise-or-subsets",
        prompt=(
            "The maximum possible bitwise OR of a subset of nums is the OR of all its elements. Return the number "
            "of different NON-EMPTY subsets (by index) whose OR equals that maximum."
        ),
        sig="def count_max_or_subsets(nums: List[int]) -> int:",
        fn="count_max_or_subsets",
        tests=[
            (([3, 1],), 2),
            (([2, 2, 2],), 7),
            (([3, 2, 1, 5],), 6),
            (([1],), 1),
        ],
        hints=[
            "OR can only add bits, so the maximum is the OR of every element.",
            "For each element decide: include it or not, carrying the OR so far.",
            (
                "Count the branches that finish with OR equal to the maximum (the empty subset never reaches it "
                "because nums has positive values)."
            ),
        ],
        pattern="Include / exclude backtracking carrying a running aggregate",
        explain=(
            "Each element is either in the subset or not, so recursion explores 2^n subsets, carrying the OR so "
            "far. Because OR is monotone, the target is simply the OR of the whole array. The brute force "
            "enumerates bitmask subsets and recomputes each OR."
        ),
        cx="O(2^n) time, O(n) recursion depth",
        brute_cx="O(2^n * n) time - recompute the OR of every subset mask",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - recompute the OR of every subset mask
def count_max_or_subsets(nums):
    n = len(nums)
    values = []
    for mask in range(1, 1 << n):
        total = 0
        for i in range(n):
            if (mask >> i) & 1:
                total |= nums[i]
        values.append(total)
    return values.count(max(values))
""",
        solution=r"""
# OPTIMISED: O(2^n) time, O(n) recursion depth
# Idea: Include / exclude backtracking carrying a running aggregate
def count_max_or_subsets(nums):
    target = 0
    for x in nums:
        target |= x

    def dfs(i, current):
        if i == len(nums):
            return 1 if current == target else 0
        return dfs(i + 1, current) + dfs(i + 1, current | nums[i])

    return dfs(0, 0)
""",
    ),
    # ---- Next Greater Numerically Balanced Number (LeetCode 2048) ----
    dict(
        title="Next Greater Numerically Balanced Number",
        diff="M",
        lc=2048,
        slug="next-greater-numerically-balanced-number",
        prompt=(
            "A number is numerically balanced if for every digit d in it, d occurs exactly d times (so 22 and 1333 "
            "are balanced, 1 is balanced, 0 never is). Return the smallest numerically balanced number that is "
            "strictly greater than n."
        ),
        sig="def next_beautiful_number(n: int) -> int:",
        fn="next_beautiful_number",
        tests=[
            ((1,), 22),
            ((1000,), 1333),
            ((3000,), 3133),
            ((0,), 1),
            ((22,), 122),
            ((122,), 212),
        ],
        hints=[
            (
                "A balanced number of length L uses digits d1 < d2 < ... with d1 + d2 + ... = L, so it has at most "
                "7 digits here."
            ),
            "Generate them all: choose the set of digits, then every arrangement of the resulting multiset.",
            "Sort the candidates and binary-search for the first one greater than n.",
        ],
        pattern="Enumerate all candidates (subset of digits + permutations), then binary search",
        explain=(
            "Because digit d needs exactly d copies, the possible multisets are few (subsets of 1..7 whose sum is "
            "at most 7), and their permutations number only in the thousands. Listing them all once and using "
            "bisect finds the successor of any n in a sorted list. Counting up from n + 1 and testing every number "
            "is the obvious brute force."
        ),
        cx="O(P log P) time, P < 10,000 candidate numbers",
        brute_cx="O(answer - n) time - test every number above n",
        brute=r"""
# BRUTE FORCE: O(answer - n) time - test every number above n
def next_beautiful_number(n):
    value = n + 1
    while True:
        counts = Counter(str(value))
        if all(int(digit) == count for digit, count in counts.items()):
            return value
        value += 1
""",
        solution=r"""
# OPTIMISED: O(P log P) time, P < 10,000 candidate numbers
# Idea: Enumerate all candidates (subset of digits + permutations), then binary search
def next_beautiful_number(n):
    candidates = []
    for mask in range(1, 1 << 7):
        digits = [d for d in range(1, 8) if (mask >> (d - 1)) & 1]
        if sum(digits) > 7:
            continue
        multiset = [d for d in digits for _ in range(d)]
        for perm in set(itertools.permutations(multiset)):
            candidates.append(int("".join(map(str, perm))))
    candidates.sort()
    return candidates[bisect.bisect_right(candidates, n)]
""",
    ),
    # ---- Maximum Good People Based on Statements (LeetCode 2151) ----
    dict(
        title="Maximum Good People Based on Statements",
        diff="H",
        lc=2151,
        slug="maximum-good-people-based-on-statements",
        prompt=(
            "n people each make statements about everyone: statements[i][j] is 0 (i says j is bad), 1 (i says j is "
            "good) or 2 (no statement; also statements[i][i] = 2). Good people ALWAYS tell the truth; bad people "
            "may say anything. Return the maximum number of good people consistent with the statements."
        ),
        sig="def maximum_good(statements: List[List[int]]) -> int:",
        fn="maximum_good",
        tests=[
            (([[2, 1, 2], [1, 2, 2], [2, 0, 2]],), 2),
            (([[2, 0], [0, 2]],), 1),
            (([[2]],), 1),
            (([[2, 1], [1, 2]],), 2),
        ],
        hints=[
            "Decide who is good and who is bad; only the good people's statements must be true.",
            "With n <= 15 you can try every assignment: a bitmask of good people.",
            (
                "An assignment is valid if every statement made by a good person matches the assignment. Take the "
                "valid assignment with the most good people."
            ),
        ],
        pattern="Subset enumeration / backtracking with consistency pruning",
        explain=(
            "Bad people impose no constraints, so only the statements of the people assumed good matter. "
            "Backtracking assigns good/bad person by person and checks the new person's statements against those "
            "already assigned (in both directions), pruning as soon as a contradiction appears or the remaining "
            "people cannot beat the best so far. The brute force tests every one of the 2^n assignments completely."
        ),
        cx="O(2^n * n) time worst case, usually much less with pruning",
        brute_cx="O(2^n * n^2) time - test every assignment fully",
        brute=r"""
# BRUTE FORCE: O(2^n * n^2) time - test every assignment fully
def maximum_good(statements):
    n = len(statements)
    best = 0
    for mask in range(1 << n):
        consistent = True
        for i in range(n):
            if not (mask >> i) & 1:
                continue
            for j in range(n):
                said = statements[i][j]
                if said != 2 and said != (mask >> j) & 1:
                    consistent = False
        if consistent:
            best = max(best, bin(mask).count("1"))
    return best
""",
        solution=r"""
# OPTIMISED: O(2^n * n) time worst case, usually much less with pruning
# Idea: Subset enumeration / backtracking with consistency pruning
def maximum_good(statements):
    n = len(statements)
    role = [0] * n
    best = 0

    def consistent(i):
        if role[i] == 1 and statements[i][i] not in (2, 1):
            return False
        for j in range(i):
            if role[i] == 1 and statements[i][j] != 2 and statements[i][j] != role[j]:
                return False
            if role[j] == 1 and statements[j][i] != 2 and statements[j][i] != role[i]:
                return False
        return True

    def dfs(i, good):
        nonlocal best
        if i == n:
            best = max(best, good)
            return
        if good + (n - i) <= best:
            return
        for r in (1, 0):
            role[i] = r
            if consistent(i):
                dfs(i + 1, good + r)

    dfs(0, 0)
    return best
""",
    ),
    # ---- Fair Distribution of Cookies (LeetCode 2305) ----
    dict(
        title="Fair Distribution of Cookies",
        diff="M",
        lc=2305,
        slug="fair-distribution-of-cookies",
        prompt=(
            "cookies[i] is the number of cookies in bag i. Distribute every bag (whole bags only) among k children. "
            "The unfairness of a distribution is the largest total any child receives. Return the minimum possible "
            "unfairness."
        ),
        sig="def distribute_cookies(cookies: List[int], k: int) -> int:",
        fn="distribute_cookies",
        tests=[
            (([8, 15, 10, 20, 8], 2), 31),
            (([6, 1, 3, 2, 2, 4, 1, 2], 3), 7),
            (([5], 1), 5),
            (([1, 2, 3], 3), 3),
        ],
        hints=[
            "Assign each bag to one of the k children - k^n possibilities in total.",
            "Keep the current load of each child; after all bags are assigned the unfairness is the maximum load.",
            (
                "Prune: skip a branch whose load already reaches the best answer found, and don't try two children "
                "with identical loads (they are interchangeable)."
            ),
        ],
        pattern="Backtracking assignment with pruning (symmetry + bound)",
        explain=(
            "Every bag goes to exactly one child, so recursion over bags with k choices each explores the whole "
            "space. Two prunings make it practical: a child whose load plus the new bag already is not below the "
            "best answer cannot lead to an improvement, and children with equal current loads are interchangeable "
            "so only one of them needs to be tried. The brute force enumerates all k^n assignments."
        ),
        cx="O(k^n) worst case, much smaller with pruning",
        brute_cx="O(k^n * n) time - evaluate every assignment",
        brute=r"""
# BRUTE FORCE: O(k^n * n) time - evaluate every assignment
def distribute_cookies(cookies, k):
    best = sum(cookies)
    for assignment in itertools.product(range(k), repeat=len(cookies)):
        loads = [0] * k
        for bag, child in zip(cookies, assignment):
            loads[child] += bag
        best = min(best, max(loads))
    return best
""",
        solution=r"""
# OPTIMISED: O(k^n) worst case, much smaller with pruning
# Idea: Backtracking assignment with pruning (symmetry + bound)
def distribute_cookies(cookies, k):
    bags = sorted(cookies, reverse=True)
    loads = [0] * k
    best = float("inf")

    def dfs(i):
        nonlocal best
        if i == len(bags):
            best = min(best, max(loads))
            return
        tried = set()
        for child in range(k):
            if loads[child] in tried or loads[child] + bags[i] >= best:
                continue
            tried.add(loads[child])
            loads[child] += bags[i]
            dfs(i + 1)
            loads[child] -= bags[i]

    dfs(0)
    return best
""",
    ),
    # ---- Maximum Rows Covered by Columns (LeetCode 2397) ----
    dict(
        title="Maximum Rows Covered by Columns",
        diff="M",
        lc=2397,
        slug="maximum-rows-covered-by-columns",
        prompt=(
            "matrix is an m x n binary matrix. Choose exactly num_select columns. A row is covered if every 1 in "
            "that row lies in one of the chosen columns (a row with no 1 is always covered). Return the maximum "
            "number of covered rows."
        ),
        sig="def maximum_rows(matrix: List[List[int]], num_select: int) -> int:",
        fn="maximum_rows",
        tests=[
            (([[0, 0, 0], [1, 0, 1], [0, 1, 1], [0, 0, 1]], 2), 3),
            (([[1], [0]], 1), 2),
            (([[1, 1], [0, 0]], 1), 1),
            (([[0]], 1), 1),
            (([[1, 1]], 2), 1),
        ],
        hints=[
            "n is small (at most 12), so you can try every way to choose the columns.",
            "Store each row as a bitmask of its 1-columns.",
            (
                "For a column mask, a row is covered iff row & ~mask == 0; count such rows and keep the best over "
                "masks with exactly num_select bits."
            ),
        ],
        pattern="Enumerate column subsets (bitmask) with a cheap subset test",
        explain=(
            "Choosing num_select columns out of n gives at most C(12, 6) = 924 selections. Representing each row as "
            "a bitmask turns 'all my 1's are chosen' into a single AND-NOT test, so each selection costs O(m). The "
            "brute force uses combinations of column indices and scans each row cell by cell."
        ),
        cx="O(C(n, k) * m) time, O(m) space",
        brute_cx="O(C(n, k) * m * n) time - check every cell of every row for each selection",
        brute=r"""
# BRUTE FORCE: O(C(n, k) * m * n) time - check every cell of every row for each selection
def maximum_rows(matrix, num_select):
    n = len(matrix[0])
    best = 0
    for cols in itertools.combinations(range(n), num_select):
        chosen = set(cols)
        covered = sum(1 for row in matrix if all(j in chosen for j, v in enumerate(row) if v))
        best = max(best, covered)
    return best
""",
        solution=r"""
# OPTIMISED: O(C(n, k) * m) time, O(m) space
# Idea: Enumerate column subsets (bitmask) with a cheap subset test
def maximum_rows(matrix, num_select):
    n = len(matrix[0])
    rows = [sum(v << j for j, v in enumerate(row)) for row in matrix]
    best = 0
    for mask in range(1 << n):
        if bin(mask).count("1") != num_select:
            continue
        best = max(best, sum(1 for row in rows if (row & ~mask) == 0))
    return best
""",
    ),
    # ---- Generate Binary Strings Without Adjacent Zeros (LeetCode 3211) ----
    dict(
        title="Generate Binary Strings Without Adjacent Zeros",
        diff="M",
        lc=3211,
        slug="generate-binary-strings-without-adjacent-zeros",
        prompt=(
            "Return all binary strings of length n in which every substring of length 2 contains at least one '1' "
            "(no two zeros are adjacent), in any order."
        ),
        sig="def valid_strings(n: int) -> List[str]:",
        fn="valid_strings",
        compare="unordered",
        tests=[
            ((1,), ["0", "1"]),
            ((2,), ["01", "10", "11"]),
            ((3,), ["010", "011", "101", "110", "111"]),
        ],
        hints=[
            "Build the string one character at a time.",
            "A '1' can always be appended; a '0' only if the string is empty or ends with '1'.",
            "Recurse until the length is n, then record the string - invalid prefixes are never extended.",
        ],
        pattern="Backtracking that prunes invalid prefixes",
        explain=(
            "The constraint only looks at the last character, so each prefix has either one or two allowed "
            "extensions. Generating directly with that rule produces only valid strings (their number grows like "
            "Fibonacci numbers), whereas the brute force builds all 2^n strings and filters afterwards."
        ),
        cx="O(n * F(n)) time and output size, F(n) ~ 1.6^n",
        brute_cx="O(n * 2^n) time - generate every string, then filter",
        brute=r"""
# BRUTE FORCE: O(n * 2^n) time - generate every string, then filter
def valid_strings(n):
    return [
        "".join(bits) for bits in itertools.product("01", repeat=n) if "00" not in "".join(bits)
    ]
""",
        solution=r"""
# OPTIMISED: O(n * F(n)) time and output size, F(n) ~ 1.6^n
# Idea: Backtracking that prunes invalid prefixes
def valid_strings(n):
    result = []

    def build(current):
        if len(current) == n:
            result.append(current)
            return
        build(current + "1")
        if not current or current[-1] == "1":
            build(current + "0")

    build("")
    return result
""",
    ),
]
