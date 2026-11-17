"""extra batch of Stack / Monotonic Stack problems - the problem bank for the "stack_monotonic" topic (batch 5).

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


def _parens_ok(args, got):
    """True if got is a valid parentheses string, a subsequence of s, with the minimum number of removals."""
    s = args[0]
    if not isinstance(got, str):
        return False
    it = iter(s)
    if not all(c in it for c in got):
        return False
    balance = 0
    for c in got:
        if c == "(":
            balance += 1
        elif c == ")":
            balance -= 1
            if balance < 0:
                return False
    if balance:
        return False
    opens = bad_close = 0
    for c in s:
        if c == "(":
            opens += 1
        elif c == ")":
            if opens:
                opens -= 1
            else:
                bad_close += 1
    return len(got) == len(s) - opens - bad_close


def _threshold_ok(args, got):
    """True if got is -1 and no valid length exists, or got is a length k with a window of k values all > t / k."""
    nums, threshold = args
    n = len(nums)

    def valid(k):
        return any(all(x * k > threshold for x in nums[i : i + k]) for i in range(n - k + 1))

    if got == -1:
        return not any(valid(k) for k in range(1, n + 1))
    return isinstance(got, int) and 1 <= got <= n and valid(got)


PROBLEMS = [
    # ---- Baseball Game (LeetCode 682) ----
    dict(
        title="Baseball Game",
        diff="E",
        lc=682,
        slug="baseball-game",
        prompt=(
            "operations is a list of strings describing a scoring record. An integer string records that score; '+' "
            "records the sum of the previous two scores; 'D' records double the previous score; 'C' invalidates "
            "(removes) the previous score. Return the sum of all scores after applying every operation."
        ),
        sig="def cal_points(operations: List[str]) -> int:",
        fn="cal_points",
        tests=[
            ((["5", "2", "C", "D", "+"],), 30),
            ((["5", "-2", "4", "C", "D", "9", "+", "+"],), 27),
            ((["1"],), 1),
            ((["3", "C"],), 0),
        ],
        hints=[
            "Every operation looks only at the most recent valid scores.",
            "That is a stack: push new scores, pop on 'C', read the top one or two for 'D' and '+'.",
            "At the end, the answer is the sum of the stack.",
        ],
        pattern="Stack of valid scores",
        explain=(
            "'C' removes the latest score, and '+' / 'D' read the latest one or two - always the top of a "
            "last-in-first-out structure. Pushing each new score and popping on 'C' keeps exactly the valid scores "
            "on the stack, so the answer is its sum. The brute force keeps the stack as a list of indices into an "
            "array of values."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n) time - a stack of indices into a values array",
        brute=r"""
# BRUTE FORCE: O(n) time - a stack of indices into a values array
def cal_points(operations):
    values = [0] * len(operations)
    alive = []

    for i, op in enumerate(operations):
        if op == "C":
            alive.pop()
            continue

        if op == "D":
            values[i] = 2 * values[alive[-1]]
        elif op == "+":
            values[i] = values[alive[-1]] + values[alive[-2]]
        else:
            values[i] = int(op)

        alive.append(i)

    return sum(values[i] for i in alive)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Stack of valid scores
def cal_points(operations):
    scores = []

    for op in operations:
        if op == "C":
            scores.pop()
        elif op == "D":
            scores.append(2 * scores[-1])
        elif op == "+":
            scores.append(scores[-1] + scores[-2])
        else:
            scores.append(int(op))

    return sum(scores)
""",
    ),
    # ---- Shortest Subarray with Sum at Least K (LeetCode 862) ----
    dict(
        title="Shortest Subarray with Sum at Least K",
        diff="H",
        lc=862,
        slug="shortest-subarray-with-sum-at-least-k",
        prompt=(
            "nums may contain negative numbers. Return the length of the shortest non-empty contiguous subarray "
            "whose sum is at least k, or -1 if there is none."
        ),
        sig="def shortest_subarray(nums: List[int], k: int) -> int:",
        fn="shortest_subarray",
        tests=[
            (([1], 1), 1),
            (([1, 2], 4), -1),
            (([2, -1, 2], 3), 3),
            (([84, -37, 32, 40, 95], 167), 3),
            (([-1, 5], 5), 1),
        ],
        hints=[
            (
                "With prefix sums P, a subarray (i, j] has sum P[j] - P[i]; you want the largest i < j with P[j] - "
                "P[i] >= k."
            ),
            "A sliding window fails because of negative numbers - extending the window can decrease the sum.",
            (
                "Keep a deque of indices with INCREASING prefix sums: pop from the front while P[j] - P[front] >= k "
                "(record the length), and pop from the back while P[back] >= P[j] (they can never beat j)."
            ),
        ],
        pattern="Prefix sums + monotonic deque",
        explain=(
            "An earlier index with a larger-or-equal prefix sum than a later one is useless: the later index gives "
            "a shorter subarray for any future end, so those are discarded from the back, keeping the prefix sums "
            "increasing. Once the front index satisfies the sum condition for the current end, no later end can use "
            "it to be shorter, so it is popped. Each index enters and leaves once."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - try every start with a running sum",
        brute=r"""
# BRUTE FORCE: O(n^2) time - try every start with a running sum
def shortest_subarray(nums, k):
    best = -1

    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total >= k:
                if best == -1 or j - i + 1 < best:
                    best = j - i + 1
                break

    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Prefix sums + monotonic deque
def shortest_subarray(nums, k):
    prefix = [0]

    for x in nums:
        prefix.append(prefix[-1] + x)

    window = deque()
    best = float("inf")

    for j, value in enumerate(prefix):
        while window and value - prefix[window[0]] >= k:
            best = min(best, j - window.popleft())
        while window and prefix[window[-1]] >= value:
            window.pop()
        window.append(j)

    return -1 if best == float("inf") else best
""",
    ),
    # ---- Minimum Cost Tree From Leaf Values (LeetCode 1130) ----
    dict(
        title="Minimum Cost Tree From Leaf Values",
        diff="M",
        lc=1130,
        slug="minimum-cost-tree-from-leaf-values",
        prompt=(
            "arr lists the leaf values of a binary tree in in-order, and every non-leaf node has exactly two "
            "children. The value of a non-leaf node is (largest leaf in its left subtree) * (largest leaf in its "
            "right subtree). Return the minimum possible sum of the non-leaf node values over all such trees."
        ),
        sig="def mct_from_leaf_values(arr: List[int]) -> int:",
        fn="mct_from_leaf_values",
        tests=[
            (([6, 2, 4],), 32),
            (([4, 11],), 44),
            (([1, 2, 3],), 8),
            (([7, 7, 7],), 98),
        ],
        hints=[
            (
                "Brute force: interval DP - dp[i][j] = min over split points k of dp[i][k] + dp[k+1][j] + max(i..k) "
                "* max(k+1..j)."
            ),
            (
                "Greedy view: whenever two leaves are merged, the smaller one disappears from further products - so "
                "merge the smallest leaves first, paired with their smaller neighbour."
            ),
            (
                "Scan with a decreasing stack: when the new value is at least the top, pop the top (the 'valley') "
                "and pay top * min(left neighbour, new value). Pay for what is left at the end."
            ),
        ],
        pattern="Monotonic decreasing stack (greedy removal of the smallest valley)",
        explain=(
            "Each non-leaf product removes the smaller of the two multiplied maxima from the game, so the cheapest "
            "plan removes the smallest element as early as possible, paired with its smaller neighbour (the "
            "cheapest partner it could ever have). A decreasing stack finds the smallest element whose neighbours "
            "are both larger, in amortised O(1). The interval DP considers every possible tree."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^3) time - interval DP over every split point",
        brute=r"""
# BRUTE FORCE: O(n^3) time - interval DP over every split point
def mct_from_leaf_values(arr):
    n = len(arr)
    best = [[0] * n for _ in range(n)]
    top = [[0] * n for _ in range(n)]

    for i in range(n):
        top[i][i] = arr[i]
        for j in range(i + 1, n):
            top[i][j] = max(top[i][j - 1], arr[j])

    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            best[i][j] = min(
                best[i][k] + best[k + 1][j] + top[i][k] * top[k + 1][j] for k in range(i, j)
            )

    return best[0][n - 1]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic decreasing stack (greedy removal of the smallest valley)
def mct_from_leaf_values(arr):
    stack = [float("inf")]
    total = 0

    for value in arr:
        while stack[-1] <= value:
            valley = stack.pop()
            total += valley * min(stack[-1], value)
        stack.append(value)

    while len(stack) > 2:
        total += stack.pop() * stack[-1]

    return total
""",
    ),
    # ---- Minimum Remove to Make Valid Parentheses (LeetCode 1249) ----
    dict(
        title="Minimum Remove to Make Valid Parentheses",
        diff="M",
        lc=1249,
        slug="minimum-remove-to-make-valid-parentheses",
        prompt=(
            "s contains letters and the brackets '(' and ')'. Remove the minimum number of brackets so that the "
            "result is a valid parentheses string (every '(' matched, no unmatched ')'). Return any valid result."
        ),
        sig="def min_remove_to_make_valid(s: str) -> str:",
        fn="min_remove_to_make_valid",
        check=_parens_ok,
        tests=[
            (("lee(t(c)o)de)",), "lee(t(c)o)de"),
            (("a)b(c)d",), "ab(c)d"),
            (("))((",), ""),
            (("abc",), "abc"),
        ],
        hints=[
            "A ')' with no '(' waiting for it must be removed; a '(' that never gets closed must be removed too.",
            (
                "Scan left to right with a stack of indices of unmatched '('. On ')' pop if possible, otherwise "
                "mark this ')' for removal."
            ),
            (
                "After the scan, whatever is left on the stack is an unmatched '(' - mark those too, and rebuild "
                "the string without the marked positions."
            ),
        ],
        pattern="Stack of unmatched bracket indices",
        explain=(
            "A bracket is removable exactly when it cannot be paired by the standard stack matching. Matching "
            "greedily is optimal, so the unmatched ')' (seen when the stack is empty) and the unmatched '(' (left "
            "on the stack) form a minimum removal set. The brute force tries removing 0, 1, 2, ... brackets in "
            "every possible way until the string becomes valid."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="exponential - try every set of removed brackets, smallest sets first",
        brute=r"""
# BRUTE FORCE: exponential - try every set of removed brackets, smallest sets first
def min_remove_to_make_valid(s):
    def valid(text):
        balance = 0

        for c in text:
            if c == "(":
                balance += 1
            elif c == ")":
                balance -= 1
                if balance < 0:
                    return False

        return balance == 0

    brackets = [i for i, c in enumerate(s) if c in "()"]

    for count in range(len(brackets) + 1):
        for removed in itertools.combinations(brackets, count):
            gone = set(removed)
            candidate = "".join(c for i, c in enumerate(s) if i not in gone)
            if valid(candidate):
                return candidate
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Stack of unmatched bracket indices
def min_remove_to_make_valid(s):
    chars = list(s)
    stack = []

    for i, c in enumerate(chars):
        if c == "(":
            stack.append(i)
        elif c == ")":
            if stack:
                stack.pop()
            else:
                chars[i] = ""

    for i in stack:
        chars[i] = ""

    return "".join(chars)
""",
    ),
    # ---- Sum of Subarray Ranges (LeetCode 2104) ----
    dict(
        title="Sum of Subarray Ranges",
        diff="M",
        lc=2104,
        slug="sum-of-subarray-ranges",
        prompt=(
            "The range of a subarray is its maximum minus its minimum. Return the sum of the ranges of all "
            "contiguous subarrays of nums."
        ),
        sig="def sub_array_ranges(nums: List[int]) -> int:",
        fn="sub_array_ranges",
        tests=[
            (([1, 2, 3],), 4),
            (([1, 3, 3],), 4),
            (([4, -2, -3, 4, 1],), 59),
            (([5],), 0),
        ],
        hints=[
            "Sum of (max - min) = sum of all subarray maximums minus sum of all subarray minimums.",
            (
                "For each element, count the subarrays in which it is the maximum: (distance to the previous "
                "greater-or-equal) * (distance to the next greater)."
            ),
            (
                "A monotonic stack finds those distances in O(n). Minimums follow by negating the array and reusing "
                "the same function."
            ),
        ],
        pattern="Monotonic stack contribution counting (max and min)",
        explain=(
            "Instead of looking at each subarray, ask how many subarrays each element is the max of. The element "
            "can extend left until a larger-or-equal element and right until a strictly larger one (the asymmetry "
            "breaks ties so each subarray has exactly one designated maximum). Product of the two extents times the "
            "value is its total contribution. The brute force extends every start while tracking max and min."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - track max and min while extending every start",
        brute=r"""
# BRUTE FORCE: O(n^2) time - track max and min while extending every start
def sub_array_ranges(nums):
    total = 0

    for i in range(len(nums)):
        high = low = nums[i]
        for j in range(i, len(nums)):
            high = max(high, nums[j])
            low = min(low, nums[j])
            total += high - low

    return total
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic stack contribution counting (max and min)
def sub_array_ranges(nums):
    def sum_of_maximums(arr):
        n = len(arr)
        left = [0] * n
        right = [0] * n
        stack = []

        for i in range(n):
            while stack and arr[stack[-1]] < arr[i]:
                stack.pop()
            left[i] = i - (stack[-1] if stack else -1)
            stack.append(i)

        stack = []

        for i in range(n - 1, -1, -1):
            while stack and arr[stack[-1]] <= arr[i]:
                stack.pop()
            right[i] = (stack[-1] if stack else n) - i
            stack.append(i)

        return sum(arr[i] * left[i] * right[i] for i in range(n))

    return sum_of_maximums(nums) + sum_of_maximums([-x for x in nums])
""",
    ),
    # ---- Replace Non-Coprime Numbers in Array (LeetCode 2197) ----
    dict(
        title="Replace Non-Coprime Numbers in Array",
        diff="H",
        lc=2197,
        slug="replace-non-coprime-numbers-in-array",
        prompt=(
            "While there are two ADJACENT numbers with gcd greater than 1, replace them by their least common "
            "multiple. Repeat until no such pair remains and return the resulting array. (The result does not "
            "depend on which pair you merge first.)"
        ),
        sig="def replace_non_coprimes(nums: List[int]) -> List[int]:",
        fn="replace_non_coprimes",
        tests=[
            (([6, 4, 3, 2, 7, 6, 2],), [12, 7, 6]),
            (([2, 2, 1, 1, 3, 3, 3],), [2, 1, 1, 3]),
            (([5],), [5]),
            (([4, 6, 9],), [36]),
        ],
        hints=[
            "A merge can create a new non-coprime pair with the left neighbour, so merges can cascade leftwards.",
            "Process left to right keeping the finished prefix on a stack.",
            (
                "For each new number, while it is not coprime with the stack top, pop the top and replace the "
                "number by lcm(top, number). Then push it."
            ),
        ],
        pattern="Stack with cascading merges",
        explain=(
            "The stack always holds a prefix in which no two neighbours are merge-able. Adding a number may make it "
            "merge with the top, and the merged value may merge with the next element down, and so on - the while "
            "loop handles the cascade. Each element is pushed once and popped at most once. The brute force rescans "
            "the whole array after every single merge."
        ),
        cx="O(n log M) time (gcd), O(n) space",
        brute_cx="O(n^2 log M) time - rescan for any non-coprime neighbours after every merge",
        brute=r"""
# BRUTE FORCE: O(n^2 log M) time - rescan for any non-coprime neighbours after every merge
def replace_non_coprimes(nums):
    arr = list(nums)
    changed = True

    while changed:
        changed = False
        for i in range(len(arr) - 1):
            g = math.gcd(arr[i], arr[i + 1])
            if g > 1:
                arr[i : i + 2] = [arr[i] // g * arr[i + 1]]
                changed = True
                break

    return arr
""",
        solution=r"""
# OPTIMISED: O(n log M) time (gcd), O(n) space
# Idea: Stack with cascading merges
def replace_non_coprimes(nums):
    stack = []
    for x in nums:
        while stack and math.gcd(stack[-1], x) > 1:
            g = math.gcd(stack[-1], x)
            x = stack.pop() // g * x
        stack.append(x)
    return stack
""",
    ),
    # ---- Steps to Make Array Non-decreasing (LeetCode 2289) ----
    dict(
        title="Steps to Make Array Non-decreasing",
        diff="M",
        lc=2289,
        slug="steps-to-make-array-non-decreasing",
        prompt=(
            "In one step, remove ALL elements nums[i] for which nums[i - 1] > nums[i] (decided simultaneously on "
            "the current array). Return the number of steps until the array is non-decreasing."
        ),
        sig="def total_steps(nums: List[int]) -> int:",
        fn="total_steps",
        tests=[
            (([5, 3, 4, 4, 7, 3, 6, 11, 8, 5, 11],), 3),
            (([4, 5, 7, 7, 13],), 0),
            (([3, 2, 1],), 1),
            (([10, 1, 2, 3, 4, 5, 6, 1, 2, 3],), 6),
        ],
        hints=[
            "Simulating step by step is O(n^2) in the worst case.",
            (
                "For each element, ask: after how many steps is it removed? An element is removed by the nearest "
                "larger element to its left, but only after everything between them has been removed."
            ),
            (
                "Keep a stack of (value, steps). For a new element pop all smaller-or-equal tops, taking the "
                "maximum of their steps; its own steps = that maximum + 1 (or 0 if no larger element remains on the "
                "stack)."
            ),
        ],
        pattern="Monotonic stack carrying a 'time of removal' per element",
        explain=(
            "An element dies once its nearest greater element on the left becomes adjacent to it, which happens "
            "after all the smaller elements between them have died - so its death time is one more than the latest "
            "death among them. The decreasing stack provides exactly those in-between elements as it pops. If "
            "nothing greater stands on the left the element never dies (time 0)."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - simulate every round",
        brute=r"""
# BRUTE FORCE: O(n^2) time - simulate every round
def total_steps(nums):
    arr = list(nums)
    steps = 0

    while True:
        keep = [arr[0]] + [arr[i] for i in range(1, len(arr)) if arr[i - 1] <= arr[i]]
        if len(keep) == len(arr):
            return steps
        arr = keep
        steps += 1
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic stack carrying a 'time of removal' per element
def total_steps(nums):
    stack = []
    best = 0

    for x in nums:
        steps = 0
        while stack and stack[-1][0] <= x:
            steps = max(steps, stack.pop()[1])
        steps = steps + 1 if stack else 0
        best = max(best, steps)
        stack.append((x, steps))

    return best
""",
    ),
    # ---- Subarray With Elements Greater Than Varying Threshold (LeetCode 2334) ----
    dict(
        title="Subarray With Elements Greater Than Varying Threshold",
        diff="H",
        lc=2334,
        slug="subarray-with-elements-greater-than-varying-threshold",
        prompt=(
            "Find a subarray of length k in which EVERY element is greater than threshold / k. Return the size k of "
            "any such subarray, or -1 if none exists."
        ),
        sig="def valid_subarray_size(nums: List[int], threshold: int) -> int:",
        fn="valid_subarray_size",
        check=_threshold_ok,
        tests=[
            (([1, 3, 4, 3, 1], 6), 3),
            (([6, 5, 6, 5, 8], 7), 1),
            (([1, 1], 5), -1),
            (([4], 3), 1),
        ],
        hints=[
            "All elements of the window exceed threshold / k iff the window's MINIMUM times k exceeds the threshold.",
            (
                "So for each element as the minimum, the widest window where it is still the minimum gives the best "
                "chance."
            ),
            (
                "Find, with a monotonic stack, the nearest smaller value on the left and right; the window length "
                "is right - left - 1; accept if nums[i] * length > threshold."
            ),
        ],
        pattern="Monotonic stack: widest window in which each element is the minimum",
        explain=(
            "If a window of length L with minimum m fails m * L > threshold, shorter windows containing m can only "
            "be worse for the condition at their own size, so it suffices to test the maximal window of every "
            "element - the largest span in which it is the smallest. Previous / next smaller elements give those "
            "spans in O(n). Brute force tries every length k and every window of that length."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^3) time - try every length and every window",
        brute=r"""
# BRUTE FORCE: O(n^3) time - try every length and every window
def valid_subarray_size(nums, threshold):
    n = len(nums)
    for k in range(1, n + 1):
        for i in range(n - k + 1):
            if all(x * k > threshold for x in nums[i : i + k]):
                return k
    return -1
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic stack: widest window in which each element is the minimum
def valid_subarray_size(nums, threshold):
    n = len(nums)
    left = [-1] * n
    right = [n] * n
    stack = []

    for i, x in enumerate(nums):
        while stack and nums[stack[-1]] >= x:
            right[stack.pop()] = i
        left[i] = stack[-1] if stack else -1
        stack.append(i)

    for i, x in enumerate(nums):
        length = right[i] - left[i] - 1
        if x * length > threshold:
            return length

    return -1
""",
    ),
    # ---- Construct Smallest Number From DI String (LeetCode 2375) ----
    dict(
        title="Construct Smallest Number From DI String",
        diff="M",
        lc=2375,
        slug="construct-smallest-number-from-di-string",
        prompt=(
            "pattern has length n and uses only 'I' (increasing) and 'D' (decreasing). Build the lexicographically "
            "smallest string num of n + 1 distinct digits from '1' to '9' such that num[i] < num[i + 1] when "
            "pattern[i] == 'I' and num[i] > num[i + 1] when pattern[i] == 'D'."
        ),
        sig="def smallest_number(pattern: str) -> str:",
        fn="smallest_number",
        tests=[
            (("IIIDIDDD",), "123549876"),
            (("DDD",), "4321"),
            (("I",), "12"),
            (("D",), "21"),
            (("DID",), "2143"),
        ],
        hints=[
            "Without any 'D' the answer is simply 1, 2, 3, ... in order.",
            "Each run of D's must be reversed: a run of k D's needs k + 1 numbers in decreasing order.",
            (
                "Push 1, 2, 3, ... on a stack one by one; whenever the next pattern character is 'I' (or the "
                "pattern ends), pop everything - that reverses each D-run."
            ),
        ],
        pattern="Stack reversal of runs",
        explain=(
            "The smallest digits go first, so we use 1, 2, 3, ... in order and only reverse the blocks that the "
            "'D's force. A block that ends at an 'I' (or the end) is emitted by popping the stack, which reverses "
            "it in O(1) amortised per digit. The brute force is a depth-first search that tries digits in "
            "increasing order and returns the first complete valid string."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="exponential - depth-first search trying digits in ascending order",
        brute=r"""
# BRUTE FORCE: exponential - depth-first search trying digits in ascending order
def smallest_number(pattern):
    n = len(pattern)
    chosen = []
    used = [False] * 10

    def dfs(i):
        if i == n + 1:
            return True

        for digit in range(1, 10):
            if used[digit]:
                continue

            if i > 0 and ((pattern[i - 1] == "I") != (chosen[-1] < digit)):
                continue

            used[digit] = True
            chosen.append(digit)

            if dfs(i + 1):
                return True

            chosen.pop()
            used[digit] = False

        return False

    dfs(0)

    return "".join(map(str, chosen))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Stack reversal of runs
def smallest_number(pattern):
    result = []
    stack = []

    for i in range(len(pattern) + 1):
        stack.append(str(i + 1))
        if i == len(pattern) or pattern[i] == "I":
            while stack:
                result.append(stack.pop())

    return "".join(result)
""",
    ),
    # ---- Next Greater Element IV (LeetCode 2454) ----
    dict(
        title="Next Greater Element IV",
        diff="H",
        lc=2454,
        slug="next-greater-element-iv",
        prompt=(
            "For each index i, the second greater element is nums[j] where j > i, nums[j] > nums[i], and there is "
            "exactly one index k with i < k < j and nums[k] > nums[i] (j is the second index to the right holding a "
            "larger value). Return an array of those values, with -1 where none exists."
        ),
        sig="def second_greater_element(nums: List[int]) -> List[int]:",
        fn="second_greater_element",
        tests=[
            (([2, 4, 0, 9, 6],), [9, 6, 6, -1, -1]),
            (([3, 3],), [-1, -1]),
            (([1, 2, 3],), [3, -1, -1]),
            (([5, 4, 3, 2, 1],), [-1, -1, -1, -1, -1]),
        ],
        hints=[
            "The ordinary next-greater problem uses one decreasing stack.",
            (
                "Use two stacks: s1 holds elements still waiting for their FIRST greater element, s2 those waiting "
                "for their SECOND."
            ),
            (
                "On a new value x: first resolve every s2 element smaller than x (x is their second greater). Then "
                "move every s1 element smaller than x to s2, keeping their relative order, and push the new index "
                "on s1."
            ),
        ],
        pattern="Two monotonic stacks (first-greater and second-greater queues)",
        explain=(
            "An element passes through two stages: waiting for a first larger value, then waiting for another "
            "larger value. Each stage is a decreasing stack, because a smaller waiting element is always resolved "
            "no later than a larger one. When an element is promoted from s1 to s2 the popped group is re-pushed in "
            "reverse so s2 stays decreasing. Every index moves at most twice."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - for each element scan right for the second larger value",
        brute=r"""
# BRUTE FORCE: O(n^2) time - for each element scan right for the second larger value
def second_greater_element(nums):
    result = []

    for i, x in enumerate(nums):
        seen = 0
        answer = -1

        for j in range(i + 1, len(nums)):
            if nums[j] > x:
                seen += 1
                if seen == 2:
                    answer = nums[j]
                    break

        result.append(answer)

    return result
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Two monotonic stacks (first-greater and second-greater queues)
def second_greater_element(nums):
    result = [-1] * len(nums)
    first = []
    second = []

    for i, x in enumerate(nums):
        while second and nums[second[-1]] < x:
            result[second.pop()] = x
        moved = []
        while first and nums[first[-1]] < x:
            moved.append(first.pop())
        second.extend(reversed(moved))
        first.append(i)

    return result
""",
    ),
    # ---- Robot Collisions (LeetCode 2751) ----
    dict(
        title="Robot Collisions",
        diff="H",
        lc=2751,
        slug="robot-collisions",
        prompt=(
            "Robots stand at distinct positions on a line, each with a health and a direction ('L' or 'R'); all "
            "move at the same speed. When a right-moving robot meets a left-moving one, the one with less health is "
            "removed and the other loses 1 health; equal health removes both. Return the healths of the surviving "
            "robots in the ORIGINAL input order."
        ),
        sig="def survived_robots_healths(positions: List[int], healths: List[int], directions: str) -> List[int]:",
        fn="survived_robots_healths",
        tests=[
            (([5, 4, 3, 2, 1], [2, 17, 9, 15, 10], "RRRRR"), [2, 17, 9, 15, 10]),
            (([3, 5, 2, 6], [10, 10, 15, 12], "RLRL"), [14]),
            (([1, 2, 5, 6], [10, 10, 11, 11], "RLRL"), []),
            (([1], [5], "L"), [5]),
        ],
        hints=[
            "Only a robot moving right that has a robot moving left somewhere to its right can ever collide.",
            "Sort the robots by position and sweep left to right keeping a stack of right-moving robots.",
            (
                "When a left-moving robot arrives, fight it against the stack top repeatedly until it dies or the "
                "stack empties; update healths as you go and report the survivors in the original order."
            ),
        ],
        pattern="Sort by position + stack of right-movers (asteroid-collision style)",
        explain=(
            "After sorting by position, robots that move away from each other never interact. A left-mover can only "
            "meet right-movers that came before it, always the nearest one first - a stack. Each fight removes at "
            "least one robot, so total work is linear after the sort. The brute force repeatedly finds the first "
            "adjacent right-then-left pair in the sorted list and resolves it."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2) time - repeatedly resolve the first adjacent collision",
        brute=r"""
# BRUTE FORCE: O(n^2) time - repeatedly resolve the first adjacent collision
def survived_robots_healths(positions, healths, directions):
    order = sorted(range(len(positions)), key=lambda i: positions[i])
    alive = [[i, healths[i]] for i in order]
    changed = True

    while changed:
        changed = False

        for k in range(len(alive) - 1):
            a, b = alive[k], alive[k + 1]

            if directions[a[0]] == "R" and directions[b[0]] == "L":
                if a[1] > b[1]:
                    a[1] -= 1
                    del alive[k + 1]
                elif a[1] < b[1]:
                    b[1] -= 1
                    del alive[k]
                else:
                    del alive[k : k + 2]

                changed = True
                break

    return [health for _, health in sorted(alive)]
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Sort by position + stack of right-movers (asteroid-collision style)
def survived_robots_healths(positions, healths, directions):
    health = list(healths)
    stack = []

    for i in sorted(range(len(positions)), key=lambda i: positions[i]):
        if directions[i] == "R":
            stack.append(i)
            continue

        while stack and health[i] > 0:
            j = stack[-1]

            if health[j] < health[i]:
                health[j] = 0
                stack.pop()
                health[i] -= 1
            elif health[j] > health[i]:
                health[j] -= 1
                health[i] = 0
            else:
                health[j] = health[i] = 0
                stack.pop()

    return [h for h in health if h > 0]
""",
    ),
    # ---- Beautiful Towers I (LeetCode 2865) ----
    dict(
        title="Beautiful Towers I",
        diff="M",
        lc=2865,
        slug="beautiful-towers-i",
        prompt=(
            "maxHeights[i] is the maximum allowed height of the tower at position i. Choose heights 1 <= h[i] <= "
            "maxHeights[i] forming a MOUNTAIN: for some peak index p, h is non-decreasing up to p and "
            "non-increasing after it. Return the maximum possible sum of the heights."
        ),
        sig="def maximum_sum_of_heights(max_heights: List[int]) -> int:",
        fn="maximum_sum_of_heights",
        tests=[
            (([5, 3, 4, 1, 1],), 13),
            (([6, 5, 3, 9, 2, 7],), 22),
            (([3, 2, 5, 5, 2, 3],), 18),
            (([4],), 4),
        ],
        hints=[
            (
                "Fix the peak p. Going left, each tower can be at most the minimum of maxHeights between it and p; "
                "the same going right."
            ),
            "Brute force: for every peak, expand outwards with a running minimum - O(n^2).",
            (
                "Precompute, with a monotonic stack, the best left-side sum ending at each index as a peak (reuse "
                "the sum of the previous smaller element), and the same from the right; combine as left[p] + "
                "right[p] - maxHeights[p]."
            ),
        ],
        pattern="Monotonic stack prefix sums (previous smaller element reuse)",
        explain=(
            "For peak p the heights to the left are the running minimum of maxHeights going outward. If the "
            "previous smaller element is at position q, then positions at or before q have exactly the same heights "
            "as when q is the peak, so left[p] = left[q] + maxHeights[p] * (p - q). A decreasing stack finds q. The "
            "same works from the right, and the best peak maximises the combined sum."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - for every peak expand both sides with a running minimum",
        brute=r"""
# BRUTE FORCE: O(n^2) time - for every peak expand both sides with a running minimum
def maximum_sum_of_heights(max_heights):
    n = len(max_heights)
    best = 0

    for peak in range(n):
        total = max_heights[peak]
        low = max_heights[peak]

        for i in range(peak - 1, -1, -1):
            low = min(low, max_heights[i])
            total += low

        low = max_heights[peak]

        for i in range(peak + 1, n):
            low = min(low, max_heights[i])
            total += low

        best = max(best, total)

    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic stack prefix sums (previous smaller element reuse)
def maximum_sum_of_heights(max_heights):
    n = len(max_heights)
    left = [0] * n
    stack = []

    for i in range(n):
        while stack and max_heights[stack[-1]] > max_heights[i]:
            stack.pop()
        if stack:
            left[i] = left[stack[-1]] + max_heights[i] * (i - stack[-1])
        else:
            left[i] = max_heights[i] * (i + 1)
        stack.append(i)

    right = [0] * n
    stack = []

    for i in range(n - 1, -1, -1):
        while stack and max_heights[stack[-1]] > max_heights[i]:
            stack.pop()
        if stack:
            right[i] = right[stack[-1]] + max_heights[i] * (stack[-1] - i)
        else:
            right[i] = max_heights[i] * (n - i)
        stack.append(i)

    return max(left[i] + right[i] - max_heights[i] for i in range(n))
""",
    ),
    # ---- Find the Number of Subarrays Where Boundary Elements Are Maximum (LeetCode 3113) ----
    dict(
        title="Find the Number of Subarrays Where Boundary Elements Are Maximum",
        diff="H",
        lc=3113,
        slug="find-the-number-of-subarrays-where-boundary-elements-are-maximum",
        prompt=(
            "Count the subarrays of nums in which the first and the last element are both equal to the maximum of "
            "that subarray (a single element counts)."
        ),
        sig="def number_of_subarrays(nums: List[int]) -> int:",
        fn="number_of_subarrays",
        tests=[
            (([1, 4, 3, 3, 2],), 6),
            (([3, 3, 3],), 6),
            (([1],), 1),
            (([1, 2, 3],), 3),
        ],
        hints=[
            "Fix the right end j. A valid left end i has nums[i] == nums[j] and nothing larger in between.",
            (
                "Keep a decreasing stack of values with how many times each value occurs in a row of 'still "
                "visible' positions."
            ),
            (
                "On x: pop smaller values, then increase the count if the top equals x (else push [x, 1]); the "
                "number of valid subarrays ending here is the top's count."
            ),
        ],
        pattern="Monotonic stack with run counts",
        explain=(
            "Elements smaller than a newer, larger element can never be the boundary of a valid subarray ending "
            "after it, so they are popped. Equal values stay visible to each other, so the stack stores (value, "
            "count). The subarrays ending at the new element that start at an equal visible element number exactly "
            "that count (including itself). Summing over all positions gives the answer."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - extend every start while tracking the maximum",
        brute=r"""
# BRUTE FORCE: O(n^2) time - extend every start while tracking the maximum
def number_of_subarrays(nums):
    count = 0

    for i in range(len(nums)):
        top = nums[i]
        for j in range(i, len(nums)):
            top = max(top, nums[j])
            if nums[i] == top and nums[j] == top:
                count += 1

    return count
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic stack with run counts
def number_of_subarrays(nums):
    stack = []
    total = 0

    for x in nums:
        while stack and stack[-1][0] < x:
            stack.pop()
        if stack and stack[-1][0] == x:
            stack[-1][1] += 1
        else:
            stack.append([x, 1])
        total += stack[-1][1]

    return total
""",
    ),
]
