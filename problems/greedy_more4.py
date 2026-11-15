"""extra batch of Greedy problems - the problem bank for the "greedy" topic (batch 4).

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
    # ---- Monotone Increasing Digits (LeetCode 738) ----
    dict(
        title="Monotone Increasing Digits",
        diff="M",
        lc=738,
        slug="monotone-increasing-digits",
        prompt=(
            "Return the largest integer <= n whose digits are in non-decreasing order from left to right (for "
            "example 1234 and 1999 qualify, 332 does not)."
        ),
        sig="def monotone_increasing_digits(n: int) -> int:",
        fn="monotone_increasing_digits",
        tests=[
            ((10,), 9),
            ((1234,), 1234),
            ((332,), 299),
            ((100,), 99),
            ((0,), 0),
            ((120,), 119),
            ((4321,), 3999),
        ],
        hints=[
            "Counting down from n and testing every number works but is hopelessly slow for n near 10^9.",
            (
                "If a digit is bigger than the digit after it, that digit must shrink by one and everything after "
                "it can become 9."
            ),
            (
                "Scan from the right so a decrease at an earlier digit is noticed after later fixes; remember the "
                "leftmost position where the 9s start."
            ),
        ],
        pattern="Greedy: lower the first bad digit, then maximise the suffix",
        explain=(
            "If digit d[i-1] > d[i] the prefix is too large, so d[i-1] must drop by 1 (the smallest change that "
            "fixes this pair). Once an earlier digit is lowered, every later digit can be 9 because the number is "
            "already smaller than n. Scanning right to left lets one fix cascade leftwards (332 -> 322 -> 299)."
        ),
        cx="O(d) time where d is the number of digits, O(d) space",
        brute_cx="O(n * d) time - test every number from n downwards",
        brute=r"""
# BRUTE FORCE: O(n * d) time - test every number from n downwards
def monotone_increasing_digits(n):
    def ok(x):
        s = str(x)
        return all(s[i] <= s[i + 1] for i in range(len(s) - 1))

    x = n
    while not ok(x):
        x -= 1
    return x
""",
        solution=r"""
# OPTIMISED: O(d) time where d is the number of digits, O(d) space
# Idea: Greedy: lower the first bad digit, then maximise the suffix
def monotone_increasing_digits(n):
    digits = list(str(n))
    mark = len(digits)
    for i in range(len(digits) - 1, 0, -1):
        if digits[i - 1] > digits[i]:
            digits[i - 1] = str(int(digits[i - 1]) - 1)
            mark = i
    for i in range(mark, len(digits)):
        digits[i] = "9"
    return int("".join(digits))
""",
    ),
    # ---- Max Chunks To Make Sorted (LeetCode 769) ----
    dict(
        title="Max Chunks To Make Sorted",
        diff="M",
        lc=769,
        slug="max-chunks-to-make-sorted",
        prompt=(
            "arr is a permutation of 0..n-1. Split it into the most contiguous chunks such that sorting each chunk "
            "on its own and concatenating gives the fully sorted array. Return the number of chunks."
        ),
        sig="def max_chunks_to_sorted(arr: List[int]) -> int:",
        fn="max_chunks_to_sorted",
        tests=[
            (([4, 3, 2, 1, 0],), 1),
            (([1, 0, 2, 3, 4],), 4),
            (([0],), 1),
            (([1, 2, 0],), 1),
            (([0, 1, 2],), 3),
            (([1, 0, 3, 2],), 2),
        ],
        hints=[
            "A cut after index i is allowed only if the first i+1 values are exactly the numbers 0..i in some order.",
            "Because arr is a permutation, that holds exactly when the maximum of the prefix equals i.",
            "Keep a running maximum and count the indices where it equals the index.",
        ],
        pattern="Greedy: cut as soon as the prefix is self-contained",
        explain=(
            "The sorted array holds value i at index i. A prefix of length i+1 can stand as its own chunk only if "
            "it contains precisely 0..i. In a permutation that is equivalent to max(prefix) == i, so every such "
            "index is a free cut and cutting early never hurts later chunks."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(2^n * n log n) time - try every set of cut positions",
        brute=r"""
# BRUTE FORCE: O(2^n * n log n) time - try every set of cut positions
def max_chunks_to_sorted(arr):
    n = len(arr)
    target = sorted(arr)
    best = 1
    for mask in range(1 << (n - 1)):
        pieces, start = [], 0
        for i in range(n - 1):
            if mask >> i & 1:
                pieces.append(arr[start : i + 1])
                start = i + 1
        pieces.append(arr[start:])
        merged = []
        for piece in pieces:
            merged += sorted(piece)
        if merged == target:
            best = max(best, len(pieces))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Greedy: cut as soon as the prefix is self-contained
def max_chunks_to_sorted(arr):
    chunks = biggest = 0
    for i, value in enumerate(arr):
        biggest = max(biggest, value)
        if biggest == i:
            chunks += 1
    return chunks
""",
    ),
    # ---- Minimum Deletions to Make Character Frequencies Unique (LeetCode 1647) ----
    dict(
        title="Minimum Deletions to Make Character Frequencies Unique",
        diff="M",
        lc=1647,
        slug="minimum-deletions-to-make-character-frequencies-unique",
        prompt=(
            "Delete the fewest characters from s so that no two different letters occur the same number of times (a "
            "frequency of 0 may repeat). Return the minimum number of deletions."
        ),
        sig="def min_deletions(s: str) -> int:",
        fn="min_deletions",
        tests=[
            (("aab",), 0),
            (("aaabbbcc",), 2),
            (("ceabaacb",), 2),
            (("a",), 0),
            (("abcabc",), 3),
            (("aaaa",), 0),
        ],
        hints=[
            "Only the multiset of frequencies matters, not which letters they belong to.",
            "Handle frequencies from largest to smallest; each one may stay or be lowered to the next free value.",
            (
                "Keep a cap = the highest frequency still allowed; keep min(freq, cap), delete the rest, then lower "
                "the cap by one (never below 0)."
            ),
        ],
        pattern="Greedy: sort frequencies, lower each to the highest unused value",
        explain=(
            "Process the biggest frequency first. It can keep its value, which blocks that value for everyone else, "
            "so the next frequency must be at most one lower. Lowering a frequency only as far as necessary wastes "
            "the fewest deletions, and a count of 0 is always allowed."
        ),
        cx="O(n + k log k) time for k distinct letters, O(k) space",
        brute_cx="exponential time - try every kept count for every letter",
        brute=r"""
# BRUTE FORCE: exponential time - try every kept count for every letter
def min_deletions(s):
    freqs = list(Counter(s).values())

    def go(i, used):
        if i == len(freqs):
            return 0
        best = float("inf")
        for keep in range(freqs[i] + 1):
            if keep == 0 or keep not in used:
                nxt = used | {keep} if keep else used
                best = min(best, freqs[i] - keep + go(i + 1, nxt))
        return best

    return go(0, frozenset())
""",
        solution=r"""
# OPTIMISED: O(n + k log k) time for k distinct letters, O(k) space
# Idea: Greedy: sort frequencies, lower each to the highest unused value
def min_deletions(s):
    freqs = sorted(Counter(s).values(), reverse=True)
    deletions, cap = 0, len(s)
    for freq in freqs:
        keep = min(freq, cap)
        deletions += freq - keep
        cap = max(keep - 1, 0)
    return deletions
""",
    ),
    # ---- Maximum Units on a Truck (LeetCode 1710) ----
    dict(
        title="Maximum Units on a Truck",
        diff="E",
        lc=1710,
        slug="maximum-units-on-a-truck",
        prompt=(
            "box_types[i] = [number_of_boxes, units_per_box]. The truck holds at most truck_size boxes. Return the "
            "maximum total number of units you can load."
        ),
        sig="def maximum_units(box_types: List[List[int]], truck_size: int) -> int:",
        fn="maximum_units",
        tests=[
            (([[1, 3], [2, 2], [3, 1]], 4), 8),
            (([[5, 10], [2, 5], [4, 7], [3, 9]], 10), 91),
            (([[1, 1]], 5), 1),
            (([[2, 5]], 1), 5),
            (([[3, 4], [3, 4]], 0), 0),
        ],
        hints=[
            "Every box takes one slot, so a slot is best spent on the box with the most units.",
            "Sort the box types by units per box, descending.",
            "Take as many boxes as fit from each type until the truck is full.",
        ],
        pattern="Greedy: fill the scarce resource with the best value per slot first",
        explain=(
            "All boxes occupy the same space, so the problem is a fractional-free knapsack with unit weights. "
            "Swapping a loaded low-unit box for an unloaded high-unit box never decreases the total, so loading the "
            "highest-unit boxes first is optimal (exchange argument)."
        ),
        cx="O(k log k) time for k box types, O(1) extra space",
        brute_cx="exponential time - try every count for every box type",
        brute=r"""
# BRUTE FORCE: exponential time - try every count for every box type
def maximum_units(box_types, truck_size):
    def go(i, room):
        if i == len(box_types):
            return 0
        count, units = box_types[i]
        best = 0
        for take in range(min(count, room) + 1):
            best = max(best, take * units + go(i + 1, room - take))
        return best

    return go(0, truck_size)
""",
        solution=r"""
# OPTIMISED: O(k log k) time for k box types, O(1) extra space
# Idea: Greedy: fill the scarce resource with the best value per slot first
def maximum_units(box_types, truck_size):
    total = 0
    for count, units in sorted(box_types, key=lambda box: -box[1]):
        take = min(count, truck_size)
        total += take * units
        truck_size -= take
        if truck_size == 0:
            break
    return total
""",
    ),
    # ---- Minimum Operations to Make the Array Increasing (LeetCode 1827) ----
    dict(
        title="Minimum Operations to Make the Array Increasing",
        diff="E",
        lc=1827,
        slug="minimum-operations-to-make-the-array-increasing",
        prompt=(
            "In one operation you may add 1 to any element. Return the minimum number of operations to make nums "
            "strictly increasing."
        ),
        sig="def min_operations(nums: List[int]) -> int:",
        fn="min_operations",
        tests=[
            (([1, 1, 1],), 3),
            (([1, 5, 2, 4, 1],), 14),
            (([8],), 0),
            (([1, 2, 3],), 0),
            (([5, 5],), 1),
        ],
        hints=[
            (
                "You can only raise values, so each element must be at least one more than its (already fixed) "
                "predecessor."
            ),
            "Process left to right and keep the value the previous element ended up with.",
            "If nums[i] <= previous, raise it to previous + 1 and pay the difference; otherwise keep it.",
        ],
        pattern="Greedy: raise each element by the minimum necessary, left to right",
        explain=(
            "Raising an element higher than needed only makes the next element's requirement bigger, so each "
            "element should end at exactly max(own value, previous + 1). Fixing the left side first never has to be "
            "undone."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="exponential time - try every final value for every element",
        brute=r"""
# BRUTE FORCE: exponential time - try every final value for every element
def min_operations(nums):
    top = max(nums) + len(nums)

    def go(i, prev):
        if i == len(nums):
            return 0
        best = float("inf")
        for value in range(max(nums[i], prev + 1), top + 1):
            best = min(best, value - nums[i] + go(i + 1, value))
        return best

    return go(0, float("-inf"))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Greedy: raise each element by the minimum necessary, left to right
def min_operations(nums):
    ops, prev = 0, float("-inf")
    for value in nums:
        if value <= prev:
            ops += prev + 1 - value
            prev += 1
        else:
            prev = value
    return ops
""",
    ),
    # ---- Minimum Time to Make Rope Colorful (LeetCode 1578) ----
    dict(
        title="Minimum Time to Make Rope Colorful",
        diff="M",
        lc=1578,
        slug="minimum-time-to-make-rope-colorful",
        prompt=(
            "colors[i] is the colour of balloon i and needed_time[i] the time to remove it. Remove balloons so no "
            "two neighbouring balloons share a colour. Return the minimum total removal time."
        ),
        sig="def min_cost(colors: str, needed_time: List[int]) -> int:",
        fn="min_cost",
        tests=[
            (("abaac", [1, 2, 3, 4, 5]), 3),
            (("abc", [1, 2, 3]), 0),
            (("aabaa", [1, 2, 3, 4, 1]), 2),
            (("aaaa", [1, 1, 1, 1]), 3),
            (("a", [5]), 0),
        ],
        hints=[
            "Only runs of equal colours cause trouble, and runs are independent.",
            "In a run of equal colours exactly one balloon has to stay.",
            "Keep the most expensive balloon of each run: the cost of a run is its sum minus its maximum.",
        ],
        pattern="Greedy: in each group keep the most expensive item",
        explain=(
            "Removing balloons from different runs never interacts, and within a run of length m we must remove at "
            "least m-1 of them. Keeping the one with the largest removal time leaves the smallest total to remove."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(2^n * n) time - try every subset of balloons to remove",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - try every subset of balloons to remove
def min_cost(colors, needed_time):
    n = len(colors)
    best = float("inf")
    for mask in range(1 << n):
        kept = [colors[i] for i in range(n) if not mask >> i & 1]
        if all(kept[i] != kept[i + 1] for i in range(len(kept) - 1)):
            best = min(best, sum(needed_time[i] for i in range(n) if mask >> i & 1))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Greedy: in each group keep the most expensive item
def min_cost(colors, needed_time):
    total = run_max = 0
    for i, cost in enumerate(needed_time):
        if i > 0 and colors[i] != colors[i - 1]:
            run_max = 0
        total += min(run_max, cost)
        run_max = max(run_max, cost)
    return total
""",
    ),
    # ---- Broken Calculator (LeetCode 991) ----
    dict(
        title="Broken Calculator",
        diff="M",
        lc=991,
        slug="broken-calculator",
        prompt=(
            "A calculator shows start_value. One operation either doubles the number or subtracts 1. Return the "
            "minimum number of operations to turn start_value into target."
        ),
        sig="def broken_calc(start_value: int, target: int) -> int:",
        fn="broken_calc",
        tests=[
            ((2, 3), 2),
            ((5, 8), 2),
            ((3, 10), 3),
            ((1, 1), 0),
            ((5, 5), 0),
            ((10, 1), 9),
        ],
        hints=[
            "Going forward has two choices at every step; going backwards from target is more forced.",
            "Reverse the operations: halve (only if even) or add 1.",
            "If target is even, halve it; if odd, add 1. Once target <= start, the rest is start - target additions.",
        ],
        pattern="Greedy on the reversed process",
        explain=(
            "Reversed, the moves are 'divide by 2' and 'add 1'. An odd target cannot be halved, so adding 1 is "
            "forced. For an even target halving is never worse than adding 2 steps of +1 then halving. When target "
            "drops to start or below, only +1 steps remain."
        ),
        cx="O(log target) time, O(1) space",
        brute_cx="O(target) time and space - breadth-first search over reachable values",
        brute=r"""
# BRUTE FORCE: O(target) time and space - breadth-first search over reachable values
def broken_calc(start_value, target):
    limit = 2 * max(start_value, target)
    seen = {start_value}
    queue = deque([(start_value, 0)])
    while queue:
        value, steps = queue.popleft()
        if value == target:
            return steps
        for nxt in (value * 2, value - 1):
            if 0 < nxt <= limit and nxt not in seen:
                seen.add(nxt)
                queue.append((nxt, steps + 1))
    return -1
""",
        solution=r"""
# OPTIMISED: O(log target) time, O(1) space
# Idea: Greedy on the reversed process
def broken_calc(start_value, target):
    steps = 0
    while target > start_value:
        target = target + 1 if target % 2 else target // 2
        steps += 1
    return steps + start_value - target
""",
    ),
    # ---- Maximum Number of Coins You Can Get (LeetCode 1561) ----
    dict(
        title="Maximum Number of Coins You Can Get",
        diff="M",
        lc=1561,
        slug="maximum-number-of-coins-you-can-get",
        prompt=(
            "There are 3n piles of coins. Repeatedly, you pick any 3 piles: Alice takes the largest, you take the "
            "second largest and Bob takes the smallest. Return the maximum coins you can collect."
        ),
        sig="def max_coins(piles: List[int]) -> int:",
        fn="max_coins",
        tests=[
            (([2, 4, 1, 2, 7, 8],), 9),
            (([2, 4, 5],), 4),
            (([9, 8, 7, 6, 5, 1, 2, 3, 4],), 18),
            (([1, 1, 1],), 1),
        ],
        hints=[
            "You never want Bob to take a big pile, so give Bob the smallest piles.",
            "Alice's pile is always lost; sacrifice the very largest ones to pair with good piles for you.",
            "Sort; ignore the n smallest (Bob's); then take every second pile starting from the next one.",
        ],
        pattern="Greedy after sorting: pair the best with the next best",
        explain=(
            "In every triple you get the middle pile. Give Bob the n smallest piles, and from the remaining 2n "
            "piles form pairs of two adjacent values (largest with second largest) so Alice's loss is as small as "
            "possible per pair you win; you collect every second pile of that suffix."
        ),
        cx="O(n log n) time, O(1) extra space",
        brute_cx="exponential time - try every way to group the piles into triples",
        brute=r"""
# BRUTE FORCE: exponential time - try every way to group the piles into triples
def max_coins(piles):
    def go(rest):
        if not rest:
            return 0
        first, others = rest[0], rest[1:]
        best = 0
        for i in range(len(others)):
            for j in range(i + 1, len(others)):
                triple = sorted([first, others[i], others[j]])
                remaining = [x for k, x in enumerate(others) if k not in (i, j)]
                best = max(best, triple[1] + go(remaining))
        return best

    return go(list(piles))
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space
# Idea: Greedy after sorting: pair the best with the next best
def max_coins(piles):
    piles = sorted(piles)
    return sum(piles[len(piles) // 3 :: 2])
""",
    ),
    # ---- Minimum Subsequence in Non-Increasing Order (LeetCode 1403) ----
    dict(
        title="Minimum Subsequence in Non-Increasing Order",
        diff="E",
        lc=1403,
        slug="minimum-subsequence-in-non-increasing-order",
        prompt=(
            "Return a subsequence of nums with the fewest elements whose sum is strictly greater than the sum of "
            "the elements left out (if several have the minimum size, take the one with the largest sum). Return it "
            "sorted in non-increasing order."
        ),
        sig="def min_subsequence(nums: List[int]) -> List[int]:",
        fn="min_subsequence",
        tests=[
            (([4, 3, 10, 9, 8],), [10, 9]),
            (([4, 4, 7, 6, 7],), [7, 7, 6]),
            (([6],), [6]),
            (([1, 1],), [1, 1]),
            (([3, 1, 2],), [3, 2]),
        ],
        hints=[
            "To beat the rest with few elements, take the biggest elements.",
            "Sort in descending order and keep taking until what you hold exceeds what is left.",
            "Compare 2 * taken with the total instead of recomputing the remainder.",
        ],
        pattern="Greedy: take the largest values first until the target is beaten",
        explain=(
            "Any subsequence of size k has sum at most the sum of the k largest values, so if some size-k choice "
            "wins then the k largest also win. Taking largest-first therefore finds the minimum size and, among "
            "those, the largest sum."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(2^n * n) time - try every subset",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - try every subset
def min_subsequence(nums):
    total = sum(nums)
    best = None
    for mask in range(1, 1 << len(nums)):
        chosen = [nums[i] for i in range(len(nums)) if mask >> i & 1]
        if 2 * sum(chosen) > total:
            key = (len(chosen), -sum(chosen))
            if best is None or key < best[0]:
                best = (key, sorted(chosen, reverse=True))
    return best[1]
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Greedy: take the largest values first until the target is beaten
def min_subsequence(nums):
    total, taken, out = sum(nums), 0, []
    for value in sorted(nums, reverse=True):
        out.append(value)
        taken += value
        if 2 * taken > total:
            break
    return out
""",
    ),
    # ---- Minimum Cost of Buying Candies With Discount (LeetCode 2144) ----
    dict(
        title="Minimum Cost of Buying Candies With Discount",
        diff="E",
        lc=2144,
        slug="minimum-cost-of-buying-candies-with-discount",
        prompt=(
            "In a shop, when you buy two candies you get a third one free, provided its cost is not more than the "
            "cheaper of the two you bought. Given the candy costs, return the minimum total cost to take all "
            "candies."
        ),
        sig="def minimum_cost(cost: List[int]) -> int:",
        fn="minimum_cost",
        tests=[
            (([1, 2, 3],), 5),
            (([6, 5, 7, 9, 2, 2],), 23),
            (([5, 5],), 10),
            (([7],), 7),
            (([1, 1, 1, 1],), 3),
        ],
        hints=[
            "The free candy is capped by the cheaper bought one, so you want the three costs to be close together.",
            "Sort in descending order and look at triples of neighbours.",
            "Pay for two, skip the third: ignore every third element (index 2, 5, 8, ...).",
        ],
        pattern="Greedy: group the most expensive items together",
        explain=(
            "To save as much as possible each free candy should be as expensive as allowed. In descending order, "
            "the two bought candies that sit right before a free one are the closest values that still allow it, so "
            "skipping every third element wastes nothing."
        ),
        cx="O(n log n) time, O(1) extra space",
        brute_cx="exponential time - try every way of choosing two bought candies and one free candy",
        brute=r"""
# BRUTE FORCE: exponential time - try every way of choosing two bought candies and one free candy
def minimum_cost(cost):
    def go(rest):
        if not rest:
            return 0
        best = rest[0] + go(rest[1:])
        n = len(rest)
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(n):
                    if k != i and k != j and rest[k] <= min(rest[i], rest[j]):
                        left = [x for t, x in enumerate(rest) if t not in (i, j, k)]
                        best = min(best, rest[i] + rest[j] + go(left))
        return best

    return go(list(cost))
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space
# Idea: Greedy: group the most expensive items together
def minimum_cost(cost):
    cost = sorted(cost, reverse=True)
    return sum(price for i, price in enumerate(cost) if i % 3 != 2)
""",
    ),
    # ---- Minimum Sum of Four Digit Number After Splitting Digits (LeetCode 2160) ----
    dict(
        title="Minimum Sum of Four Digit Number After Splitting Digits",
        diff="E",
        lc=2160,
        slug="minimum-sum-of-four-digit-number-after-splitting-digits",
        prompt=(
            "num is a 4-digit integer. Split its digits (all four must be used, leading zeros allowed) into two new "
            "integers new1 and new2. Return the minimum possible value of new1 + new2."
        ),
        sig="def minimum_sum(num: int) -> int:",
        fn="minimum_sum",
        tests=[
            ((2932,), 52),
            ((4009,), 13),
            ((1234,), 37),
            ((9999,), 198),
            ((1000,), 1),
        ],
        hints=[
            "A digit in the tens place is worth 10 times more than in the units place.",
            "Put the two smallest digits in the tens places.",
            "Sort the digits d0 <= d1 <= d2 <= d3; the answer is 10*(d0 + d1) + d2 + d3.",
        ],
        pattern="Greedy: smallest digits get the biggest place values",
        explain=(
            "Two two-digit numbers beat a 1+3 split because the hundreds digit would cost 100 per unit. With two "
            "tens places and two units places, the sum is 10*(tens digits) + (units digits), minimised by giving "
            "the two smallest digits the weight 10."
        ),
        cx="O(1) time and space (4 digits)",
        brute_cx="O(4! * 3) time - try every ordering and every split point",
        brute=r"""
# BRUTE FORCE: O(4! * 3) time - try every ordering and every split point
def minimum_sum(num):
    best = float("inf")
    for perm in itertools.permutations(str(num)):
        for cut in range(1, 4):
            first = int("".join(perm[:cut]))
            second = int("".join(perm[cut:]))
            best = min(best, first + second)
    return best
""",
        solution=r"""
# OPTIMISED: O(1) time and space (4 digits)
# Idea: Greedy: smallest digits get the biggest place values
def minimum_sum(num):
    d = sorted(int(ch) for ch in str(num))
    return 10 * (d[0] + d[1]) + d[2] + d[3]
""",
    ),
]
