"""extra batch of Two Pointers problems - the problem bank for the "two_pointers" topic (batch 6).

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
    # ---- Swap Adjacent in LR String (LeetCode 777) ----
    dict(
        title="Swap Adjacent in LR String",
        diff="M",
        lc=777,
        slug="swap-adjacent-in-lr-string",
        prompt=(
            "A string uses only 'L', 'R' and 'X'. One move replaces 'XL' by 'LX' or 'RX' by 'XR'. Return True if "
            "start can be turned into end by a sequence of moves (both strings have the same length)."
        ),
        sig="def can_transform(start: str, end: str) -> bool:",
        fn="can_transform",
        tests=[
            (("RXXLRXRXL", "XRLXXRRLX"), True),
            (("X", "L"), False),
            (("LX", "XL"), False),
            (("XR", "RX"), False),
            (("XXXL", "LXXX"), True),
        ],
        hints=[
            "Moves never change the order of the 'L' and 'R' letters - only where the X's are.",
            "Compare the two strings with the X's skipped: they must list the same letters in the same order.",
            (
                "Walk both strings with two pointers over the non-X letters: an 'L' may only move left (its "
                "position in start must be >= its position in end) and an 'R' only right."
            ),
        ],
        pattern="Two pointers over the non-blank characters",
        explain=(
            "L and R can never pass each other, so the sequence of non-X letters is invariant. Matching the k-th "
            "letter of start with the k-th letter of end is therefore forced, and it is reachable exactly when the "
            "L has not been asked to move right or the R left. Skipping X's with two pointers checks this in one "
            "pass."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="exponential - explore every string reachable by moves",
        brute=r"""
# BRUTE FORCE: exponential - explore every string reachable by moves
def can_transform(start, end):
    seen = {start}
    stack = [start]

    while stack:
        current = stack.pop()

        if current == end:
            return True

        for i in range(len(current) - 1):
            pair = current[i : i + 2]

            if pair == "XL":
                nxt = current[:i] + "LX" + current[i + 2 :]
            elif pair == "RX":
                nxt = current[:i] + "XR" + current[i + 2 :]
            else:
                continue

            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)

    return False
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two pointers over the non-blank characters
def can_transform(start, end):
    n = len(start)
    j = 0

    for i in range(n):
        if start[i] == "X":
            continue

        while j < n and end[j] == "X":
            j += 1

        if j == n or start[i] != end[j]:
            return False

        if start[i] == "L" and i < j:
            return False

        if start[i] == "R" and i > j:
            return False

        j += 1

    while j < n and end[j] == "X":
        j += 1

    return j == n
""",
    ),
    # ---- Friends Of Appropriate Ages (LeetCode 825) ----
    dict(
        title="Friends Of Appropriate Ages",
        diff="M",
        lc=825,
        slug="friends-of-appropriate-ages",
        prompt=(
            "ages[i] is the age of person i. Person x sends a friend request to person y (y != x) unless age[y] <= "
            "0.5 * age[x] + 7, or age[y] > age[x], or age[y] > 100 and age[x] < 100. Return the total number of "
            "friend requests (a request x -> y and y -> x are counted separately)."
        ),
        sig="def num_friend_requests(ages: List[int]) -> int:",
        fn="num_friend_requests",
        tests=[
            (([16, 16],), 2),
            (([16, 17, 18],), 2),
            (([20, 30, 100, 110, 120],), 3),
            (([10, 10, 10],), 0),
            (([8],), 0),
        ],
        hints=[
            "The third rule never matters: if age[y] > 100 and age[x] < 100 then age[y] > age[x] already.",
            (
                "So x requests exactly those y with 0.5 * age[x] + 7 < age[y] <= age[x] - a contiguous range in "
                "sorted order."
            ),
            (
                "Sort the ages. For each x, keep two pointers: lo = first age above the lower bound, hi = first age "
                "above age[x]. The window size minus one (x itself) is its number of requests."
            ),
        ],
        pattern="Sort + two sliding bounds (window of valid values per element)",
        explain=(
            "After sorting, the people x may befriend form a window [lo, hi): everyone older than half of x plus "
            "seven and not older than x. As x grows both bounds only move right, so two pointers visit each person "
            "once. x itself lies inside its window whenever the window is non-empty, hence the minus one."
        ),
        cx="O(n log n) time, O(1) extra space",
        brute_cx="O(n^2) time - test every ordered pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every ordered pair
def num_friend_requests(ages):
    total = 0

    for i, x in enumerate(ages):
        for j, y in enumerate(ages):
            if i == j:
                continue
            if y <= 0.5 * x + 7 or y > x or (y > 100 and x < 100):
                continue
            total += 1

    return total
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space
# Idea: Sort + two sliding bounds (window of valid values per element)
def num_friend_requests(ages):
    ages = sorted(ages)
    n = len(ages)
    lo = hi = 0
    total = 0

    for x in ages:
        while lo < n and ages[lo] * 2 <= x + 14:
            lo += 1
        while hi < n and ages[hi] <= x:
            hi += 1
        if hi > lo:
            total += hi - lo - 1

    return total
""",
    ),
    # ---- 3Sum With Multiplicity (LeetCode 923) ----
    dict(
        title="3Sum With Multiplicity",
        diff="M",
        lc=923,
        slug="3sum-with-multiplicity",
        prompt=(
            "Count the triples i < j < k with arr[i] + arr[j] + arr[k] == target, modulo 1_000_000_007. Equal "
            "values at different indices count as different triples."
        ),
        sig="def three_sum_multi(arr: List[int], target: int) -> int:",
        fn="three_sum_multi",
        tests=[
            (([1, 1, 2, 2, 3, 3, 4, 4, 5, 5], 8), 20),
            (([1, 1, 2, 2, 2, 2], 5), 12),
            (([2, 1, 3], 6), 1),
            (([1, 1, 1], 3), 1),
            (([0, 0, 0, 0], 0), 4),
        ],
        hints=[
            "Sort the array - then the order of indices no longer matters, only the multiset of values.",
            "Fix the smallest element arr[i] and run the usual two-pointer search for the remaining sum.",
            (
                "When arr[lo] != arr[hi] hit the target, count how many equal values sit at each end and add left * "
                "right. When arr[lo] == arr[hi], every pair inside the block works: m * (m - 1) / 2."
            ),
        ],
        pattern="Sort + fix one + two pointers with run lengths",
        explain=(
            "Plain 3Sum skips duplicates because it wants distinct triples; here duplicates are the whole point. At "
            "a match with different end values the blocks of equal values multiply; when both ends share a value "
            "the whole remaining range is one block and any two of its m members complete the triple."
        ),
        cx="O(n^2) time, O(1) extra space",
        brute_cx="O(n^3) time - test every index triple",
        brute=r"""
# BRUTE FORCE: O(n^3) time - test every index triple
def three_sum_multi(arr, target):
    count = 0
    n = len(arr)

    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if arr[i] + arr[j] + arr[k] == target:
                    count += 1

    return count % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n^2) time, O(1) extra space
# Idea: Sort + fix one + two pointers with run lengths
def three_sum_multi(arr, target):
    arr = sorted(arr)
    n = len(arr)
    total = 0

    for i in range(n - 2):
        need = target - arr[i]
        lo, hi = i + 1, n - 1

        while lo < hi:
            s = arr[lo] + arr[hi]

            if s < need:
                lo += 1
            elif s > need:
                hi -= 1
            elif arr[lo] != arr[hi]:
                left = right = 1

                while lo + left < hi and arr[lo + left] == arr[lo]:
                    left += 1

                while hi - right > lo and arr[hi - right] == arr[hi]:
                    right += 1

                total += left * right
                lo += left
                hi -= right
            else:
                block = hi - lo + 1
                total += block * (block - 1) // 2
                break

    return total % (10**9 + 7)
""",
    ),
    # ---- Reverse Prefix of Word (LeetCode 2000) ----
    dict(
        title="Reverse Prefix of Word",
        diff="E",
        lc=2000,
        slug="reverse-prefix-of-word",
        prompt=(
            "Reverse the segment of word from index 0 up to and including the FIRST occurrence of ch. If ch does "
            "not occur, return word unchanged."
        ),
        sig="def reverse_prefix(word: str, ch: str) -> str:",
        fn="reverse_prefix",
        tests=[
            (("abcdefd", "d"), "dcbaefd"),
            (("xyxzxe", "z"), "zxyxxe"),
            (("abcd", "z"), "abcd"),
            (("ab", "b"), "ba"),
        ],
        hints=[
            "First find where the first occurrence of ch is.",
            "If there is none, nothing changes.",
            (
                "Otherwise swap characters from both ends of word[0..idx] moving inwards, or simply use "
                "word[idx::-1] + word[idx + 1:]."
            ),
        ],
        pattern="Two pointers swapping inwards (or a reversed slice)",
        explain=(
            "Only the segment up to the first ch is touched. Reversing a segment is the classic two-pointer swap: "
            "exchange the ends and walk towards the middle. Python's slice word[idx::-1] performs the same reversal "
            "in one expression."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n) time - build the reversed prefix by reading it backwards",
        brute=r"""
# BRUTE FORCE: O(n) time - build the reversed prefix by reading it backwards
def reverse_prefix(word, ch):
    idx = -1

    for i, c in enumerate(word):
        if c == ch:
            idx = i
            break

    if idx == -1:
        return word

    out = ""

    for i in range(idx, -1, -1):
        out += word[i]

    return out + word[idx + 1 :]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Two pointers swapping inwards (or a reversed slice)
def reverse_prefix(word, ch):
    idx = word.find(ch)

    if idx == -1:
        return word

    chars = list(word)
    i, j = 0, idx

    while i < j:
        chars[i], chars[j] = chars[j], chars[i]
        i += 1
        j -= 1

    return "".join(chars)
""",
    ),
    # ---- Watering Plants II (LeetCode 2105) ----
    dict(
        title="Watering Plants II",
        diff="M",
        lc=2105,
        slug="watering-plants-ii",
        prompt=(
            "Plants stand in a row with water needs plants[i]. Alice starts at the left with a can of capacity "
            "capacityA, Bob at the right with capacityB (both start full). They water at the same time, moving "
            "towards each other: each waters their next plant, refilling first if the can holds less than the plant "
            "needs (a plant is never watered in two parts). If they reach the same plant, whoever has more water "
            "left waters it (Alice on a tie), refilling if neither can. Return the total number of refills."
        ),
        sig="def minimum_refill(plants: List[int], capacity_a: int, capacity_b: int) -> int:",
        fn="minimum_refill",
        tests=[
            (([2, 2, 3, 3], 5, 5), 1),
            (([2, 2, 3, 3], 3, 4), 2),
            (([5], 10, 8), 0),
            (([1, 2, 4, 4, 5], 6, 5), 2),
        ],
        hints=[
            "Simulate it: Alice's pointer moves right, Bob's moves left, until they meet or cross.",
            (
                "Each person keeps the water currently in their can; refill (count it) when it is less than the "
                "plant's need."
            ),
            (
                "If the pointers land on the same plant, it is watered by the one with more water; refill only if "
                "even the larger amount is not enough."
            ),
        ],
        pattern="Two pointers moving inwards (simulation)",
        explain=(
            "Their routes are fixed in advance: Alice takes the left half, Bob the right half, and the middle plant "
            "of an odd-length row is contested. So the process is a direct two-pointer simulation with a running "
            "water level per person, finishing with a special case for the shared middle plant."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time - simulate Alice's half and Bob's half separately, then the middle plant",
        brute=r"""
# BRUTE FORCE: O(n) time - simulate Alice's half and Bob's half separately, then the middle plant
def minimum_refill(plants, capacity_a, capacity_b):
    n = len(plants)
    half = n // 2
    refills = 0
    water_a = capacity_a

    for i in range(half):
        if water_a < plants[i]:
            refills += 1
            water_a = capacity_a
        water_a -= plants[i]

    water_b = capacity_b

    for j in range(n - 1, n - 1 - half, -1):
        if water_b < plants[j]:
            refills += 1
            water_b = capacity_b
        water_b -= plants[j]

    if n % 2 and max(water_a, water_b) < plants[half]:
        refills += 1

    return refills
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two pointers moving inwards (simulation)
def minimum_refill(plants, capacity_a, capacity_b):
    water_a, water_b = capacity_a, capacity_b
    i, j = 0, len(plants) - 1
    refills = 0

    while i < j:
        if water_a < plants[i]:
            refills += 1
            water_a = capacity_a

        water_a -= plants[i]
        i += 1

        if water_b < plants[j]:
            refills += 1
            water_b = capacity_b

        water_b -= plants[j]
        j -= 1

    if i == j and max(water_a, water_b) < plants[i]:
        refills += 1

    return refills
""",
    ),
    # ---- Find All K-Distant Indices in an Array (LeetCode 2200) ----
    dict(
        title="Find All K-Distant Indices in an Array",
        diff="E",
        lc=2200,
        slug="find-all-k-distant-indices-in-an-array",
        prompt=(
            "Index i is k-distant if some index j with nums[j] == key has |i - j| <= k. Return all k-distant "
            "indices in increasing order."
        ),
        sig="def find_k_distant_indices(nums: List[int], key: int, k: int) -> List[int]:",
        fn="find_k_distant_indices",
        tests=[
            (([3, 4, 9, 1, 3, 9, 5], 9, 1), [1, 2, 3, 4, 5, 6]),
            (([2, 2, 2, 2, 2], 2, 2), [0, 1, 2, 3, 4]),
            (([1, 2], 3, 1), []),
            (([7], 7, 0), [0]),
            (([5, 1, 1, 1, 5], 5, 1), [0, 1, 3, 4]),
        ],
        hints=[
            "Each occurrence of key 'covers' the window [j - k, j + k].",
            "The answer is the union of those windows, clipped to the array.",
            (
                "Scan the key positions left to right and remember the next index not yet output, so overlapping "
                "windows add each index only once."
            ),
        ],
        pattern="Union of windows with a 'next unwritten index' pointer",
        explain=(
            "Windows around consecutive key positions may overlap. Keeping a pointer to the first index that has "
            "not been emitted yet lets each window contribute only its new part, so every index is appended at most "
            "once and in sorted order."
        ),
        cx="O(n) time, O(1) extra space",
        brute_cx="O(n^2) time - for each index look at every key position",
        brute=r"""
# BRUTE FORCE: O(n^2) time - for each index look at every key position
def find_k_distant_indices(nums, key, k):
    result = []
    for i in range(len(nums)):
        for j in range(len(nums)):
            if nums[j] == key and abs(i - j) <= k:
                result.append(i)
                break
    return result
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) extra space
# Idea: Union of windows with a 'next unwritten index' pointer
def find_k_distant_indices(nums, key, k):
    n = len(nums)
    result = []
    nxt = 0

    for j, value in enumerate(nums):
        if value == key:
            last = min(n - 1, j + k)
            for i in range(max(nxt, j - k), last + 1):
                result.append(i)
            nxt = last + 1

    return result
""",
    ),
    # ---- Move Pieces to Obtain a String (LeetCode 2337) ----
    dict(
        title="Move Pieces to Obtain a String",
        diff="M",
        lc=2337,
        slug="move-pieces-to-obtain-a-string",
        prompt=(
            "start and target use 'L', 'R' and '_' (blank). A piece 'L' may move one step left into a blank, an 'R' "
            "one step right into a blank; pieces never jump over each other. Return True if start can become target."
        ),
        sig="def can_change(start: str, target: str) -> bool:",
        fn="can_change",
        tests=[
            (("_L__R__R_", "L______RR"), True),
            (("R_L_", "__LR"), False),
            (("_R", "R_"), False),
            (("_L", "L_"), True),
            (("L_", "_L"), False),
        ],
        hints=[
            "Pieces cannot cross, so the order of the L/R pieces is fixed.",
            "Match the k-th piece of start with the k-th piece of target.",
            (
                "Matched pieces must be the same letter; an L's target index must be <= its start index, an R's "
                "target index >= its start index."
            ),
        ],
        pattern="Two pointers over the pieces, ignoring blanks",
        explain=(
            "Blanks are just room to move. Because L and R cannot pass each other, the pieces keep their relative "
            "order, so the question reduces to pairing the pieces in order and checking the direction each one "
            "needs to travel. Two pointers skip the blanks of each string independently."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="exponential - explore every arrangement reachable by single moves",
        brute=r"""
# BRUTE FORCE: exponential - explore every arrangement reachable by single moves
def can_change(start, target):
    seen = {start}
    stack = [start]

    while stack:
        current = stack.pop()

        if current == target:
            return True

        for i in range(len(current) - 1):
            pair = current[i : i + 2]

            if pair == "_L":
                nxt = current[:i] + "L_" + current[i + 2 :]
            elif pair == "R_":
                nxt = current[:i] + "_R" + current[i + 2 :]
            else:
                continue

            if nxt not in seen:
                seen.add(nxt)
                stack.append(nxt)

    return False
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two pointers over the pieces, ignoring blanks
def can_change(start, target):
    n = len(start)
    i = j = 0

    while True:
        while i < n and start[i] == "_":
            i += 1

        while j < n and target[j] == "_":
            j += 1

        if i == n or j == n:
            return i == n and j == n

        if start[i] != target[j]:
            return False

        if start[i] == "L" and i < j:
            return False

        if start[i] == "R" and i > j:
            return False

        i += 1
        j += 1
""",
    ),
    # ---- Maximum Matching of Players With Trainers (LeetCode 2410) ----
    dict(
        title="Maximum Matching of Players With Trainers",
        diff="M",
        lc=2410,
        slug="maximum-matching-of-players-with-trainers",
        prompt=(
            "players[i] is a player's ability, trainers[j] a trainer's training capacity. A player can be matched "
            "to a trainer if ability <= capacity; each player and each trainer is used at most once. Return the "
            "maximum number of matches."
        ),
        sig="def match_players_and_trainers(players: List[int], trainers: List[int]) -> int:",
        fn="match_players_and_trainers",
        tests=[
            (([4, 7, 9], [8, 2, 5, 8]), 2),
            (([1, 1, 1], [10]), 1),
            (([5], [3]), 0),
            (([1, 2, 3], [3, 2, 1]), 3),
        ],
        hints=[
            "Giving a strong trainer to a weak player wastes capacity.",
            "Sort both lists.",
            (
                "Walk through trainers in increasing order; whenever the current trainer can handle the weakest "
                "unmatched player, match them and advance the player pointer."
            ),
        ],
        pattern="Sort + greedy two pointers",
        explain=(
            "If the weakest unmatched player can be served by the weakest trainer that is strong enough, using it "
            "never hurts: any stronger trainer is at least as useful to everyone else. So scanning trainers upward "
            "and matching whenever possible is optimal (an exchange argument), and a single pass over two sorted "
            "arrays does it."
        ),
        cx="O(n log n + m log m) time, O(1) extra space",
        brute_cx="exponential - try every way to match or skip each player",
        brute=r"""
# BRUTE FORCE: exponential - try every way to match or skip each player
def match_players_and_trainers(players, trainers):
    def solve(i, used):
        if i == len(players):
            return 0
        best = solve(i + 1, used)
        for j, capacity in enumerate(trainers):
            if not (used >> j) & 1 and players[i] <= capacity:
                best = max(best, 1 + solve(i + 1, used | (1 << j)))
        return best

    return solve(0, 0)
""",
        solution=r"""
# OPTIMISED: O(n log n + m log m) time, O(1) extra space
# Idea: Sort + greedy two pointers
def match_players_and_trainers(players, trainers):
    players = sorted(players)
    trainers = sorted(trainers)
    i = 0
    for capacity in trainers:
        if i < len(players) and players[i] <= capacity:
            i += 1
    return i
""",
    ),
    # ---- Count the Number of Fair Pairs (LeetCode 2563) ----
    dict(
        title="Count the Number of Fair Pairs",
        diff="M",
        lc=2563,
        slug="count-the-number-of-fair-pairs",
        prompt="Count the pairs i < j with lower <= nums[i] + nums[j] <= upper.",
        sig="def count_fair_pairs(nums: List[int], lower: int, upper: int) -> int:",
        fn="count_fair_pairs",
        tests=[
            (([0, 1, 7, 4, 4, 5], 3, 6), 6),
            (([1, 7, 9, 2, 5], 11, 11), 1),
            (([1, 1], 1, 1), 0),
            (([1, 1], 2, 2), 1),
            (([-1, 1], 0, 0), 1),
        ],
        hints=[
            "Pairs are unordered, so sorting the array does not change the answer.",
            "Count pairs with sum <= x using two pointers on the sorted array, then subtract the count for lower - 1.",
            (
                "For at_most(x): with i at the left and j at the right, if arr[i] + arr[j] <= x then all of "
                "arr[i+1..j] pair with i (add j - i, move i); otherwise move j left."
            ),
        ],
        pattern="Sort + two pointers counting a prefix of pairs, then subtract",
        explain=(
            "Counting pairs with a sum in [lower, upper] equals counting sums <= upper minus sums <= lower - 1. On "
            "a sorted array a single two-pointer sweep counts all pairs with sum <= x: when the extremes fit, every "
            "partner between them fits too."
        ),
        cx="O(n log n) time, O(1) extra space",
        brute_cx="O(n^2) time - test every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every pair
def count_fair_pairs(nums, lower, upper):
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if lower <= nums[i] + nums[j] <= upper:
                count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space
# Idea: Sort + two pointers counting a prefix of pairs, then subtract
def count_fair_pairs(nums, lower, upper):
    arr = sorted(nums)

    def at_most(limit):
        total = 0
        i, j = 0, len(arr) - 1

        while i < j:
            if arr[i] + arr[j] <= limit:
                total += j - i
                i += 1
            else:
                j -= 1

        return total

    return at_most(upper) - at_most(lower - 1)
""",
    ),
    # ---- Make String a Subsequence Using Cyclic Increments (LeetCode 2825) ----
    dict(
        title="Make String a Subsequence Using Cyclic Increments",
        diff="M",
        lc=2825,
        slug="make-string-a-subsequence-using-cyclic-increments",
        prompt=(
            "In one operation you pick any set of indices of str1 and replace each chosen letter by the next letter "
            "cyclically ('a'->'b', ..., 'z'->'a'). Return True if, using at most one such operation, str2 can "
            "become a subsequence of str1."
        ),
        sig="def can_make_subsequence(str1: str, str2: str) -> bool:",
        fn="can_make_subsequence",
        tests=[
            (("abc", "ad"), True),
            (("zc", "ad"), True),
            (("ab", "d"), False),
            (("a", "a"), True),
            (("a", "b"), True),
            (("a", "c"), False),
        ],
        hints=[
            "Each index of str1 can end up as either its own letter or the next letter - you choose per index.",
            "Match str2 greedily from the left: take the earliest str1 position that can serve the next needed letter.",
            (
                "Two pointers: for each ch in str1, advance j in str2 if ch == str2[j] or next(ch) == str2[j]; the "
                "answer is j == len(str2). Remember 'z' wraps to 'a'."
            ),
        ],
        pattern="Greedy subsequence matching with two pointers (two allowed letters per position)",
        explain=(
            "Choosing the increments independently per index means each str1 position simply offers two letters. As "
            "in the plain subsequence check, matching each needed letter at the earliest position that offers it "
            "never blocks a later match, so a single pass with two pointers decides it."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(2^n * n) time - try every subset of indices to increment",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - try every subset of indices to increment
def can_make_subsequence(str1, str2):
    n = len(str1)

    for mask in range(1 << n):
        chars = []

        for i, ch in enumerate(str1):
            if (mask >> i) & 1:
                ch = chr((ord(ch) - 97 + 1) % 26 + 97)
            chars.append(ch)

        it = iter(chars)

        if all(c in it for c in str2):
            return True

    return False
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Greedy subsequence matching with two pointers (two allowed letters per position)
def can_make_subsequence(str1, str2):
    j = 0
    for ch in str1:
        if j < len(str2):
            bumped = chr((ord(ch) - 97 + 1) % 26 + 97)
            if str2[j] == ch or str2[j] == bumped:
                j += 1
    return j == len(str2)
""",
    ),
    # ---- Append Characters to String to Make Subsequence (LeetCode 2486) ----
    dict(
        title="Append Characters to String to Make Subsequence",
        diff="M",
        lc=2486,
        slug="append-characters-to-string-to-make-subsequence",
        prompt=(
            "Return the minimum number of characters that must be appended to the end of s so that t becomes a "
            "subsequence of s."
        ),
        sig="def append_characters(s: str, t: str) -> int:",
        fn="append_characters",
        tests=[
            (("coaching", "coding"), 4),
            (("abcde", "a"), 0),
            (("z", "abcde"), 5),
            (("abc", "abc"), 0),
        ],
        hints=[
            "Match t against s greedily from the left, as in the ordinary subsequence test.",
            "Characters of t that were matched need no help.",
            "Two pointers: advance j in t whenever s[i] == t[j]. The answer is len(t) - j.",
        ],
        pattern="Greedy subsequence matching with two pointers",
        explain=(
            "Matching the longest possible prefix of t inside s leaves exactly the suffix of t that cannot be found "
            "- and appending that suffix completes the subsequence. A shorter append would have to supply some of "
            "those unmatched characters anyway, so the count is optimal."
        ),
        cx="O(len(s)) time, O(1) space",
        brute_cx="O(len(t) * (len(s) + len(t))) time - try appending ever longer suffixes of t",
        brute=r"""
# BRUTE FORCE: O(len(t) * (len(s) + len(t))) time - try appending ever longer suffixes of t
def append_characters(s, t):
    for k in range(len(t) + 1):
        candidate = s + t[len(t) - k :]
        it = iter(candidate)
        if all(c in it for c in t):
            return k
""",
        solution=r"""
# OPTIMISED: O(len(s)) time, O(1) space
# Idea: Greedy subsequence matching with two pointers
def append_characters(s, t):
    j = 0
    for ch in s:
        if j < len(t) and ch == t[j]:
            j += 1
    return len(t) - j
""",
    ),
    # ---- The k Strongest Values in an Array (LeetCode 1471) ----
    dict(
        title="The k Strongest Values in an Array",
        diff="M",
        lc=1471,
        slug="the-k-strongest-values-in-an-array",
        prompt=(
            "Let m be the median of arr, defined as the element at index (n - 1) // 2 of the sorted array. A value "
            "a is stronger than b if |a - m| > |b - m|, or the distances are equal and a > b. Return the k "
            "strongest values in any order."
        ),
        sig="def get_strongest(arr: List[int], k: int) -> List[int]:",
        fn="get_strongest",
        compare="unordered",
        tests=[
            (([1, 2, 3, 4, 5], 2), [5, 1]),
            (([1, 1, 3, 5, 5], 2), [5, 5]),
            (([6, 7, 11, 7, 6, 8], 5), [11, 8, 6, 6, 7]),
            (([6, -3, 7, 2, 11], 3), [-3, 11, 2]),
            (([-7, 22, 17, 3], 2), [22, 17]),
        ],
        hints=[
            "Find the median first (after sorting).",
            "The strongest values are the ones farthest from the median - which in a sorted array sit at the two ENDS.",
            (
                "Use two pointers l and r on the sorted array: take whichever end is farther from m (the right end "
                "on a tie, since it is larger), k times."
            ),
        ],
        pattern="Sort + two pointers from both ends",
        explain=(
            "In sorted order the distance to the median grows towards both ends, so the strongest remaining value "
            "is always at the left end or the right end. Comparing the two ends with the tie rule (larger wins) and "
            "moving the winning pointer inwards yields the strongest values one by one."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n log n) time - sort every value by (strength) with a custom key",
        brute=r"""
# BRUTE FORCE: O(n log n) time - sort every value by (strength) with a custom key
def get_strongest(arr, k):
    ordered = sorted(arr)
    m = ordered[(len(arr) - 1) // 2]
    return sorted(arr, key=lambda x: (-abs(x - m), -x))[:k]
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Sort + two pointers from both ends
def get_strongest(arr, k):
    ordered = sorted(arr)
    m = ordered[(len(ordered) - 1) // 2]
    left, right = 0, len(ordered) - 1
    result = []

    while len(result) < k:
        if abs(ordered[left] - m) > abs(ordered[right] - m):
            result.append(ordered[left])
            left += 1
        else:
            result.append(ordered[right])
            right -= 1

    return result
""",
    ),
    # ---- Get the Maximum Score (LeetCode 1537) ----
    dict(
        title="Get the Maximum Score",
        diff="H",
        lc=1537,
        slug="get-the-maximum-score",
        prompt=(
            "nums1 and nums2 are sorted arrays of distinct values. A path starts at index 0 of either array and "
            "walks to the right; whenever the current value also appears in the other array you may switch to that "
            "array (continuing after that value). The score is the sum of the distinct values visited (a shared "
            "value counts once). Return the maximum score modulo 1_000_000_007."
        ),
        sig="def max_score(nums1: List[int], nums2: List[int]) -> int:",
        fn="max_score",
        tests=[
            (([2, 4, 5, 8, 10], [4, 6, 8, 9]), 30),
            (([1, 3, 5, 7, 9], [3, 5, 100]), 109),
            (([1, 2, 3, 4, 5], [6, 7, 8, 9, 10]), 40),
            (([1], [1]), 1),
            (([5], [7]), 7),
        ],
        hints=[
            "The shared values are the only places where the two paths can switch.",
            (
                "Between two consecutive shared values, the two arrays each have a segment; you will simply take "
                "the better one."
            ),
            (
                "Merge with two pointers keeping a running sum for each array; at a shared value set both sums to "
                "max(a, b) + value."
            ),
        ],
        pattern="Merge-style two pointers with running segment sums",
        explain=(
            "The paths can only change array at common values, which split both arrays into independent segments. "
            "For each pair of segments the best choice is the larger sum, independently of the other choices. A "
            "merge pass accumulates both running sums and resolves them to the maximum at each common value, so the "
            "whole thing is one linear sweep."
        ),
        cx="O(n + m) time, O(1) space",
        brute_cx="O(n + m) states with memoised recursion - best score from every (array, index)",
        brute=r"""
# BRUTE FORCE: O(n + m) states with memoised recursion - best score from every (array, index)
def max_score(nums1, nums2):
    arrays = (nums1, nums2)
    where = ({v: i for i, v in enumerate(nums1)}, {v: i for i, v in enumerate(nums2)})

    @lru_cache(None)
    def best(which, i):
        if i == len(arrays[which]):
            return 0

        v = arrays[which][i]
        stay = v + best(which, i + 1)
        other = 1 - which

        if v in where[other]:
            return max(stay, v + best(other, where[other][v] + 1))

        return stay

    return max(best(0, 0), best(1, 0)) % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(1) space
# Idea: Merge-style two pointers with running segment sums
def max_score(nums1, nums2):
    i = j = 0
    sum1 = sum2 = 0

    while i < len(nums1) or j < len(nums2):
        if i < len(nums1) and (j == len(nums2) or nums1[i] < nums2[j]):
            sum1 += nums1[i]
            i += 1
        elif j < len(nums2) and (i == len(nums1) or nums2[j] < nums1[i]):
            sum2 += nums2[j]
            j += 1
        else:
            sum1 = sum2 = max(sum1, sum2) + nums1[i]
            i += 1
            j += 1

    return max(sum1, sum2) % (10**9 + 7)
""",
    ),
    # ---- Maximum Score of a Good Subarray (LeetCode 1793) ----
    dict(
        title="Maximum Score of a Good Subarray",
        diff="H",
        lc=1793,
        slug="maximum-score-of-a-good-subarray",
        prompt=(
            "The score of a subarray nums[i..j] is min(nums[i..j]) * (j - i + 1). A subarray is good if i <= k <= "
            "j. Return the maximum score of a good subarray."
        ),
        sig="def maximum_score(nums: List[int], k: int) -> int:",
        fn="maximum_score",
        tests=[
            (([1, 4, 3, 7, 4, 5], 3), 15),
            (([5, 5, 4, 5, 4, 1, 1, 1], 0), 20),
            (([6], 0), 6),
            (([1, 2], 1), 2),
        ],
        hints=[
            "Every good subarray contains index k, so grow a window outwards from k.",
            (
                "Extending the window can only lower the minimum, so extend towards the larger neighbour to keep "
                "the minimum as high as possible."
            ),
            "Keep l and r (both starting at k), the running minimum, and record min * width after every step.",
        ],
        pattern="Greedy expanding two pointers from a centre",
        explain=(
            "For a given width the best window around k is the one with the highest minimum. Always stepping "
            "towards the larger of the two neighbouring values keeps the running minimum as large as possible at "
            "every width, so the best window of each width is visited. Recording min * width at each step gives the "
            "maximum."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - every good (left, right) pair with a running minimum",
        brute=r"""
# BRUTE FORCE: O(n^2) time - every good (left, right) pair with a running minimum
def maximum_score(nums, k):
    best = 0
    for left in range(k + 1):
        smallest = min(nums[left : k + 1])
        for right in range(k, len(nums)):
            smallest = min(smallest, nums[right])
            best = max(best, smallest * (right - left + 1))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Greedy expanding two pointers from a centre
def maximum_score(nums, k):
    n = len(nums)
    left = right = k
    smallest = nums[k]
    best = smallest

    while left > 0 or right < n - 1:
        if left == 0:
            right += 1
        elif right == n - 1:
            left -= 1
        elif nums[left - 1] > nums[right + 1]:
            left -= 1
        else:
            right += 1

        smallest = min(smallest, nums[left], nums[right])
        best = max(best, smallest * (right - left + 1))

    return best
""",
    ),
    # ---- Partition Array According to Given Pivot (LeetCode 2161) ----
    dict(
        title="Partition Array According to Given Pivot",
        diff="M",
        lc=2161,
        slug="partition-array-according-to-given-pivot",
        prompt=(
            "Rearrange nums so that all values smaller than pivot come first, then all values equal to pivot, then "
            "all larger values. Inside each group the original relative order must be kept. Return the rearranged "
            "array."
        ),
        sig="def pivot_array(nums: List[int], pivot: int) -> List[int]:",
        fn="pivot_array",
        tests=[
            (([9, 12, 5, 10, 14, 3, 10], 10), [9, 5, 3, 10, 10, 12, 14]),
            (([-3, 4, 3, 2], 2), [-3, 2, 4, 3]),
            (([1], 1), [1]),
            (([3, 1, 2], 5), [3, 1, 2]),
        ],
        hints=[
            "A stable three-way split: smaller, equal, larger.",
            "Pre-fill the result with the pivot; then only the smaller and larger values need placing.",
            (
                "Scan from the left writing smaller values forwards from index 0, and simultaneously from the right "
                "writing larger values backwards from the last index."
            ),
        ],
        pattern="Two pointers writing from both ends of the output",
        explain=(
            "Smaller values go to the front in scan order and larger values go to the back; scanning the input from "
            "the right end writes the larger values back-to-front, which keeps their original order. The positions "
            "in between are exactly the pivot copies, so a result array pre-filled with pivot is already right."
        ),
        cx="O(n) time, O(n) space (the output)",
        brute_cx="O(n log n) time - a stable sort with a three-valued key",
        brute=r"""
# BRUTE FORCE: O(n log n) time - a stable sort with a three-valued key
def pivot_array(nums, pivot):
    return sorted(nums, key=lambda x: 0 if x < pivot else 1 if x == pivot else 2)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space (the output)
# Idea: Two pointers writing from both ends of the output
def pivot_array(nums, pivot):
    n = len(nums)
    result = [pivot] * n
    low, high = 0, n - 1

    for i in range(n):
        j = n - 1 - i
        if nums[i] < pivot:
            result[low] = nums[i]
            low += 1
        if nums[j] > pivot:
            result[high] = nums[j]
            high -= 1

    return result
""",
    ),
    # ---- Rearrange Array Elements by Sign (LeetCode 2149) ----
    dict(
        title="Rearrange Array Elements by Sign",
        diff="M",
        lc=2149,
        slug="rearrange-array-elements-by-sign",
        prompt=(
            "nums has an equal number of positive and negative integers. Rearrange it so that the signs alternate "
            "starting with a positive value, and the positives (and the negatives) keep their original relative "
            "order. Return the new array."
        ),
        sig="def rearrange_array(nums: List[int]) -> List[int]:",
        fn="rearrange_array",
        tests=[
            (([3, 1, -2, -5, 2, -4],), [3, -2, 1, -5, 2, -4]),
            (([-1, 1],), [1, -1]),
            (([1, -1, 2, -2],), [1, -1, 2, -2]),
            (([-3, -2, 5, 4],), [5, -3, 4, -2]),
        ],
        hints=[
            "Positives must land on even indices and negatives on odd indices.",
            "Their relative order is preserved, so the k-th positive goes to index 2k and the k-th negative to 2k + 1.",
            (
                "Keep two write pointers (0 and 1), scan once and drop each element at its pointer, then advance "
                "that pointer by 2."
            ),
        ],
        pattern="Two write pointers stepping by 2",
        explain=(
            "Every positive ends at an even slot and every negative at an odd slot, in the order they were seen. "
            "Two independent write pointers that jump by two implement this directly with one pass and no separate "
            "positive/negative lists."
        ),
        cx="O(n) time, O(n) space (the output)",
        brute_cx="O(n) time - split into two lists and interleave them",
        brute=r"""
# BRUTE FORCE: O(n) time - split into two lists and interleave them
def rearrange_array(nums):
    positives = [x for x in nums if x > 0]
    negatives = [x for x in nums if x < 0]
    result = []
    for p, q in zip(positives, negatives):
        result.append(p)
        result.append(q)
    return result
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space (the output)
# Idea: Two write pointers stepping by 2
def rearrange_array(nums):
    result = [0] * len(nums)
    pos, neg = 0, 1

    for x in nums:
        if x > 0:
            result[pos] = x
            pos += 2
        else:
            result[neg] = x
            neg += 2

    return result
""",
    ),
    # ---- Remove Palindromic Subsequences (LeetCode 1332) ----
    dict(
        title="Remove Palindromic Subsequences",
        diff="E",
        lc=1332,
        slug="remove-palindromic-subsequences",
        prompt=(
            "s contains only the letters 'a' and 'b'. In one step you may delete any palindromic SUBSEQUENCE (not "
            "necessarily contiguous). Return the minimum number of steps to make s empty."
        ),
        sig="def remove_palindrome_sub(s: str) -> int:",
        fn="remove_palindrome_sub",
        tests=[
            (("ababa",), 1),
            (("abb",), 2),
            (("baabb",), 2),
            (("",), 0),
            (("a",), 1),
        ],
        hints=[
            "A subsequence made only of 'a's is a palindrome, and so is one made only of 'b's.",
            "So the answer is never more than 2.",
            (
                "It is 0 for an empty string, 1 if s itself is a palindrome (check with two pointers from both "
                "ends), otherwise 2."
            ),
        ],
        pattern="Observation (two letters => at most 2) + two-pointer palindrome check",
        explain=(
            "Delete all the a's in step one and all the b's in step two - each is a palindromic subsequence - so 2 "
            "always suffices. One step is enough exactly when s is already a palindrome, and an empty string needs "
            "none."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="exponential - try deleting every palindromic subsequence recursively",
        brute=r"""
# BRUTE FORCE: exponential - try deleting every palindromic subsequence recursively
def remove_palindrome_sub(s):
    @lru_cache(None)
    def solve(text):
        if not text:
            return 0

        n = len(text)
        best = n

        for mask in range(1, 1 << n):
            chosen = "".join(text[i] for i in range(n) if (mask >> i) & 1)
            if chosen == chosen[::-1]:
                rest = "".join(text[i] for i in range(n) if not (mask >> i) & 1)
                best = min(best, 1 + solve(rest))

        return best

    return solve(s)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Observation (two letters => at most 2) + two-pointer palindrome check
def remove_palindrome_sub(s):
    if not s:
        return 0

    i, j = 0, len(s) - 1

    while i < j:
        if s[i] != s[j]:
            return 2
        i += 1
        j -= 1

    return 1
""",
    ),
]
