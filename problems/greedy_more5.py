"""extra batch of Greedy problems - the problem bank for the "greedy" topic (batch 5).

Each entry in PROBLEMS is ONE problem, written so you can read it top to bottom:
  title / lc / slug  name and LeetCode number (the official statement lives on LeetCode)
  prompt             the task in plain words          sig / fn   the function signature students implement
  tests              (arguments, expected result)     hints      three nudges, smallest first
  pattern / explain  the idea, and WHY it works       cx         complexity of the optimised solution
  brute / brute_cx   a simple correct solution and its cost (may be slow - that is the point)
  solution           the optimised solution, tested by `python dsa.py selftest`
"""


def _advantage_ok(args, got):
    """True if got is a rearrangement of nums1 with the largest possible number of positions where got[i] > nums2[i]."""
    nums1, nums2 = args
    if not isinstance(got, list) or sorted(got) != sorted(nums1):
        return False
    small, other = sorted(nums1), sorted(nums2)
    best = j = 0
    for x in small:
        if x > other[j]:
            best += 1
            j += 1
    return sum(x > y for x, y in zip(got, nums2)) == best


def _aabb_ok(args, got):
    """True if got has exactly a letters 'a', b letters 'b' and neither 'aaa' nor 'bbb' inside."""
    a, b = args
    return (
        isinstance(got, str)
        and len(got) == a + b
        and got.count("a") == a
        and got.count("b") == b
        and "aaa" not in got
        and "bbb" not in got
    )


PROBLEMS = [
    # ---- Dota2 Senate (LeetCode 649) ----
    dict(
        title="Dota2 Senate",
        diff="M",
        lc=649,
        slug="dota2-senate",
        prompt=(
            "senate is a string of 'R' (Radiant) and 'D' (Dire) senators in voting order. Round by round, each "
            "senator still in the game, in order, may ban one senator of the OTHER party (who then loses all "
            "rights) or, if every remaining senator belongs to one party, announce victory for it. All senators "
            "play optimally. Return 'Radiant' or 'Dire', the party that wins."
        ),
        sig="def predict_party_victory(senate: str) -> str:",
        fn="predict_party_victory",
        tests=[
            (("RD",), "Radiant"),
            (("RDD",), "Dire"),
            (("DDRRR",), "Dire"),
            (("R",), "Radiant"),
        ],
        hints=[
            (
                "Optimal play means: ban the nearest opposing senator who has not yet voted this round - that is "
                "the one who would otherwise hurt you first."
            ),
            (
                "Keep two queues of voting positions, one per party. Compare the front of each: the smaller index "
                "votes first and bans the other."
            ),
            "The winner re-enters its queue for the NEXT round with position + n. Stop when one queue is empty.",
        ],
        pattern="Greedy with two queues (earliest voter bans)",
        explain=(
            "The senator who votes first among the two fronts can ban the opponent, and banning the opponent's "
            "earliest voter is always at least as good as any other ban. The winner survives into the next round so "
            "we add n to its index to keep the order circular. The brute force simulates the same rule directly on "
            "the string, scanning circularly for the next opponent."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - scan around the circle for every ban",
        brute=r"""
# BRUTE FORCE: O(n^2) time - scan around the circle for every ban
def predict_party_victory(senate):
    n = len(senate)
    alive = [True] * n

    while True:
        for i in range(n):
            if not alive[i]:
                continue

            target = None

            for step in range(1, n):
                j = (i + step) % n
                if alive[j] and senate[j] != senate[i]:
                    target = j
                    break

            if target is None:
                return "Radiant" if senate[i] == "R" else "Dire"

            alive[target] = False
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Greedy with two queues (earliest voter bans)
def predict_party_victory(senate):
    n = len(senate)
    radiant = deque(i for i, c in enumerate(senate) if c == "R")
    dire = deque(i for i, c in enumerate(senate) if c == "D")

    while radiant and dire:
        r, d = radiant.popleft(), dire.popleft()
        if r < d:
            radiant.append(r + n)
        else:
            dire.append(d + n)

    return "Radiant" if radiant else "Dire"
""",
    ),
    # ---- Advantage Shuffle (LeetCode 870) ----
    dict(
        title="Advantage Shuffle",
        diff="M",
        lc=870,
        slug="advantage-shuffle",
        prompt=(
            "nums1 and nums2 have the same length. The advantage of nums1 over nums2 is the number of indices i "
            "with nums1[i] > nums2[i]. Return ANY permutation of nums1 that maximises this advantage."
        ),
        sig="def advantage_count(nums1: List[int], nums2: List[int]) -> List[int]:",
        fn="advantage_count",
        check=_advantage_ok,
        tests=[
            (([2, 7, 11, 15], [1, 10, 4, 11]), [2, 11, 7, 15]),
            (([12, 24, 8, 32], [13, 25, 32, 11]), [24, 32, 8, 12]),
            (([1], [1]), [1]),
            (([5, 5], [1, 9]), [5, 5]),
        ],
        hints=[
            "Brute force: try every permutation of nums1 and keep the best. That is n! - far too slow.",
            (
                "Sort nums1. Walk it from smallest to largest and give each value to the smallest still-unbeaten "
                "element of nums2 that it can beat."
            ),
            (
                "A number that cannot beat the smallest remaining nums2 value cannot beat anything - sacrifice it "
                "against the largest nums2 values. Process nums2 by sorted index to know where each value goes."
            ),
        ],
        pattern="Sort both sides, match smallest winner to smallest target",
        explain=(
            "Using a large number to beat a small target wastes it. So take nums1 in increasing order: if it beats "
            "the smallest unmatched target it is used there, otherwise it can beat nothing and is parked to fill "
            "the leftover (losing) positions. This matches the maximum number of pairs, which the checker verifies "
            "independently. Many answers are valid, so the tests use a checker rather than one fixed output."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n! * n) time - try every ordering of nums1",
        brute=r"""
# BRUTE FORCE: O(n! * n) time - try every ordering of nums1
def advantage_count(nums1, nums2):
    best, best_score = None, -1
    for order in itertools.permutations(nums1):
        score = sum(x > y for x, y in zip(order, nums2))
        if score > best_score:
            best, best_score = list(order), score
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Sort both sides, match smallest winner to smallest target
def advantage_count(nums1, nums2):
    ordered = sorted(nums1)
    targets = sorted(range(len(nums2)), key=lambda i: nums2[i])
    answer = [None] * len(nums1)
    leftovers = []
    j = 0

    for x in ordered:
        if x > nums2[targets[j]]:
            answer[targets[j]] = x
            j += 1
        else:
            leftovers.append(x)

    for i in range(len(answer)):
        if answer[i] is None:
            answer[i] = leftovers.pop()

    return answer
""",
    ),
    # ---- Delete Columns to Make Sorted (LeetCode 944) ----
    dict(
        title="Delete Columns to Make Sorted",
        diff="E",
        lc=944,
        slug="delete-columns-to-make-sorted",
        prompt=(
            "strs holds n strings of equal length. Writing them one under another forms a grid. You may delete "
            "whole columns. Return the minimum number of columns to delete so that each REMAINING column is sorted "
            "top to bottom in non-decreasing order (columns are judged independently)."
        ),
        sig="def min_deletion_size(strs: List[str]) -> int:",
        fn="min_deletion_size",
        tests=[
            ((["cba", "daf", "ghi"],), 1),
            ((["a", "b"],), 0),
            ((["zyx", "wvu", "tsr"],), 3),
            ((["abc"],), 0),
        ],
        hints=[
            "Columns do not influence each other, so decide for each column on its own.",
            "A column must be deleted exactly when some letter is larger than the letter directly below it.",
            "Count the columns where strs[i][c] > strs[i + 1][c] for some row i.",
        ],
        pattern="Independent per-column check",
        explain=(
            "Sortedness of one column does not depend on any other column, so the answer is just the number of "
            "unsorted columns. A column is sorted iff every adjacent pair in it is in order, so comparing "
            "neighbours is enough. The brute force compares every pair of rows instead of only neighbours."
        ),
        cx="O(n * L) time, O(1) space",
        brute_cx="O(n^2 * L) time - compare every pair of rows in each column",
        brute=r"""
# BRUTE FORCE: O(n^2 * L) time - compare every pair of rows in each column
def min_deletion_size(strs):
    deleted = 0
    for c in range(len(strs[0])):
        if any(strs[i][c] > strs[j][c] for i in range(len(strs)) for j in range(i + 1, len(strs))):
            deleted += 1
    return deleted
""",
        solution=r"""
# OPTIMISED: O(n * L) time, O(1) space
# Idea: Independent per-column check
def min_deletion_size(strs):
    deleted = 0
    for c in range(len(strs[0])):
        for i in range(len(strs) - 1):
            if strs[i][c] > strs[i + 1][c]:
                deleted += 1
                break
    return deleted
""",
    ),
    # ---- String Without AAA or BBB (LeetCode 984) ----
    dict(
        title="String Without AAA or BBB",
        diff="M",
        lc=984,
        slug="string-without-aaa-or-bbb",
        prompt=(
            "Given a and b (a valid answer is guaranteed to exist), return ANY string of length a + b that contains "
            "exactly a letters 'a' and b letters 'b' and does not contain the substring 'aaa' or 'bbb'."
        ),
        sig="def str_without_3a3b(a: int, b: int) -> str:",
        fn="str_without_3a3b",
        check=_aabb_ok,
        tests=[
            ((1, 2), "abb"),
            ((4, 1), "aabaa"),
            ((1, 1), "ab"),
            ((2, 0), "aa"),
        ],
        hints=[
            (
                "You can never write three equal letters in a row, so after two equal letters the next one is "
                "forced to be the other."
            ),
            (
                "Otherwise, write the letter you have MORE of - running out of the majority letter is what makes a "
                "string impossible."
            ),
            (
                "Loop while letters remain: if the last two written are equal, write the other letter; else write "
                "the letter with the larger remaining count."
            ),
        ],
        pattern="Greedy: spend the majority letter, obey the run limit",
        explain=(
            "The only danger is being left with too many copies of one letter and nothing to separate them. Always "
            "using the more plentiful letter keeps the counts balanced, and the forced switch after two equal "
            "letters satisfies the rule. Many strings are valid, so a checker verifies the counts and the forbidden "
            "substrings. The brute force chooses the positions of the 'a's in every possible way until one string "
            "passes."
        ),
        cx="O(a + b) time, O(a + b) space",
        brute_cx="O(C(a+b, a) * (a+b)) time - try every placement of the 'a' letters",
        brute=r"""
# BRUTE FORCE: O(C(a+b, a) * (a+b)) time - try every placement of the 'a' letters
def str_without_3a3b(a, b):
    n = a + b

    for spots in itertools.combinations(range(n), a):
        chars = ["b"] * n
        for i in spots:
            chars[i] = "a"
        word = "".join(chars)
        if "aaa" not in word and "bbb" not in word:
            return word
""",
        solution=r"""
# OPTIMISED: O(a + b) time, O(a + b) space
# Idea: Greedy: spend the majority letter, obey the run limit
def str_without_3a3b(a, b):
    out = []

    while a or b:
        if len(out) >= 2 and out[-1] == out[-2]:
            letter = "b" if out[-1] == "a" else "a"
        else:
            letter = "a" if a >= b else "b"

        if letter == "a":
            a -= 1
        else:
            b -= 1

        out.append(letter)

    return "".join(out)
""",
    ),
    # ---- Previous Permutation With One Swap (LeetCode 1053) ----
    dict(
        title="Previous Permutation With One Swap",
        diff="M",
        lc=1053,
        slug="previous-permutation-with-one-swap",
        prompt=(
            "Given an array of positive integers, make exactly ONE swap of two elements so that the result is the "
            "lexicographically largest permutation that is still STRICTLY smaller than the original. If no such "
            "swap exists (the array is already the smallest arrangement), return the array unchanged."
        ),
        sig="def prev_perm_opt1(arr: List[int]) -> List[int]:",
        fn="prev_perm_opt1",
        tests=[
            (([3, 2, 1],), [3, 1, 2]),
            (([1, 1, 5],), [1, 1, 5]),
            (([1, 9, 4, 6, 7],), [1, 7, 4, 6, 9]),
            (([3, 1, 1, 3],), [1, 3, 1, 3]),
        ],
        hints=[
            (
                "To make the array smaller you need a larger value to move right and a smaller value to move left. "
                "The change should happen as far RIGHT as possible so little else is lost."
            ),
            (
                "Scan from the right for the first index i with arr[i] > arr[i + 1]. If there is none the array is "
                "already the smallest."
            ),
            (
                "Swap arr[i] with the largest value to its right that is still smaller than arr[i]; if that value "
                "repeats, take its LEFTMOST copy."
            ),
        ],
        pattern="Greedy swap at the rightmost descent",
        explain=(
            "Changing a later position changes the array less, so we pick the rightmost index i that has a smaller "
            "value somewhere after it (equivalent to the rightmost descent). Putting the biggest smaller value "
            "there keeps the array as large as possible, and the leftmost copy keeps the remaining suffix as large "
            "as possible. The brute force tries every pair swap and keeps the best result below the original."
        ),
        cx="O(n) time, O(n) space for the copy",
        brute_cx="O(n^3) time - try all swaps and compare whole arrays",
        brute=r"""
# BRUTE FORCE: O(n^3) time - try all swaps and compare whole arrays
def prev_perm_opt1(arr):
    n = len(arr)
    best = None

    for i in range(n):
        for j in range(i + 1, n):
            cand = list(arr)
            cand[i], cand[j] = cand[j], cand[i]
            if cand < arr and (best is None or cand > best):
                best = cand

    return best if best is not None else list(arr)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space for the copy
# Idea: Greedy swap at the rightmost descent
def prev_perm_opt1(arr):
    arr = list(arr)
    n = len(arr)

    for i in range(n - 2, -1, -1):
        if arr[i] > arr[i + 1]:
            best = i + 1
            for j in range(i + 1, n):
                if arr[j] < arr[i] and arr[j] > arr[best]:
                    best = j
            arr[i], arr[best] = arr[best], arr[i]
            break

    return arr
""",
    ),
    # ---- Break a Palindrome (LeetCode 1328) ----
    dict(
        title="Break a Palindrome",
        diff="M",
        lc=1328,
        slug="break-a-palindrome",
        prompt=(
            "palindrome is a string of lowercase letters that reads the same backwards. Replace EXACTLY ONE "
            "character so that the result is NOT a palindrome and is the lexicographically smallest possible. "
            "Return it, or an empty string if that is impossible."
        ),
        sig="def break_palindrome(palindrome: str) -> str:",
        fn="break_palindrome",
        tests=[
            (("abccba",), "aaccba"),
            (("a",), ""),
            (("aa",), "ab"),
            (("aba",), "abb"),
        ],
        hints=[
            "A single character cannot be made a non-palindrome, so the answer is '' when the length is 1.",
            (
                "Make the string as small as possible: change the first character that is not 'a' into 'a'. Only "
                "look at the first half - changing the middle of an odd string keeps it a palindrome."
            ),
            (
                "If the first half is all 'a', no letter can get smaller without a palindrome; change the LAST "
                "character to 'b' instead."
            ),
        ],
        pattern="Greedy: earliest improvement, else smallest damage at the end",
        explain=(
            "Lowering an early character helps the most, and 'a' is the smallest letter. We stop at the half-way "
            "point because the second half mirrors the first and the exact middle character (odd length) would "
            "leave the string a palindrome. If every character in the first half is already 'a', the whole string "
            "is 'a...a' (maybe with a middle letter) and the smallest legal change is raising the last 'a' to 'b'. "
            "The brute force tries every position and every letter."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(26 * n^2) time - try every replacement and test it",
        brute=r"""
# BRUTE FORCE: O(26 * n^2) time - try every replacement and test it
def break_palindrome(palindrome):
    best = None

    for i in range(len(palindrome)):
        for letter in "abcdefghijklmnopqrstuvwxyz":
            if letter == palindrome[i]:
                continue
            cand = palindrome[:i] + letter + palindrome[i + 1 :]
            if cand != cand[::-1] and (best is None or cand < best):
                best = cand

    return best if best is not None else ""
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Greedy: earliest improvement, else smallest damage at the end
def break_palindrome(palindrome):
    n = len(palindrome)
    if n == 1:
        return ""
    for i in range(n // 2):
        if palindrome[i] != "a":
            return palindrome[:i] + "a" + palindrome[i + 1 :]
    return palindrome[:-1] + "b"
""",
    ),
    # ---- Max Difference You Can Get From Changing an Integer (LeetCode 1432) ----
    dict(
        title="Max Difference You Can Get From Changing an Integer",
        diff="M",
        lc=1432,
        slug="max-difference-you-can-get-from-changing-an-integer",
        prompt=(
            "Take the integer num. Pick a digit x and a digit y (y may equal x) and replace EVERY occurrence of x "
            "in num with y. Do this twice independently to get a and b. Neither result may have a leading zero or "
            "be zero. Return the maximum possible value of a - b."
        ),
        sig="def max_diff(num: int) -> int:",
        fn="max_diff",
        tests=[
            ((555,), 888),
            ((9,), 8),
            ((123456,), 820000),
            ((10000,), 80000),
        ],
        hints=[
            "a and b can be chosen separately: make a as large as possible and b as small as possible.",
            "For the maximum, replace the first digit that is not 9 by 9 (everywhere it appears).",
            (
                "For the minimum: if the first digit is not 1, replace it by 1; otherwise replace the first later "
                "digit that is not 0 or 1 by 0. Leading digits must never become 0."
            ),
        ],
        pattern="Greedy on the most significant digit",
        explain=(
            "Digits to the left carry more weight, so the largest number comes from raising the leftmost non-9 "
            "digit to 9 and the smallest from lowering the leading digit to 1 (the smallest allowed leading digit). "
            "If it is already 1, we can only shrink a later digit towards 0, but skipping 0 and 1 because they "
            "cannot decrease. The brute force tries all 100 digit pairs, which is easy to trust."
        ),
        cx="O(d) time where d is the digit count, O(d) space",
        brute_cx="O(100 * d) time - try every (x, y) pair",
        brute=r"""
# BRUTE FORCE: O(100 * d) time - try every (x, y) pair
def max_diff(num):
    s = str(num)
    values = []

    for x in "0123456789":
        for y in "0123456789":
            t = s.replace(x, y)
            if t[0] != "0" and int(t) != 0:
                values.append(int(t))

    return max(values) - min(values)
""",
        solution=r"""
# OPTIMISED: O(d) time where d is the digit count, O(d) space
# Idea: Greedy on the most significant digit
def max_diff(num):
    s = str(num)
    high = s

    for ch in s:
        if ch != "9":
            high = s.replace(ch, "9")
            break

    low = s

    if s[0] != "1":
        low = s.replace(s[0], "1")
    else:
        for ch in s[1:]:
            if ch not in "01":
                low = s.replace(ch, "0")
                break

    return int(high) - int(low)
""",
    ),
    # ---- Least Number of Unique Integers after K Removals (LeetCode 1481) ----
    dict(
        title="Least Number of Unique Integers after K Removals",
        diff="M",
        lc=1481,
        slug="least-number-of-unique-integers-after-k-removals",
        prompt=(
            "Remove exactly k elements from arr (you choose which). Return the least possible number of DISTINCT "
            "values left in the array."
        ),
        sig="def find_least_num_of_unique_ints(arr: List[int], k: int) -> int:",
        fn="find_least_num_of_unique_ints",
        tests=[
            (([5, 5, 4], 1), 1),
            (([4, 3, 1, 1, 3, 3, 2], 3), 2),
            (([1], 1), 0),
            (([1, 2, 3], 0), 3),
        ],
        hints=[
            (
                "A value disappears only when ALL its copies are removed, so cheap values (few copies) are the best "
                "to wipe out."
            ),
            "Count the occurrences of each distinct value.",
            (
                "Sort the counts ascending and spend k on them in that order; each count you can pay in full "
                "removes one distinct value."
            ),
        ],
        pattern="Greedy on frequencies: remove rarest values first",
        explain=(
            "Each removed distinct value costs its frequency, and the benefit (one fewer distinct value) is the "
            "same for all values, so the cheapest ones first is optimal. Leftover budget that cannot finish another "
            "value is simply spent on partial removals. The brute force tries every subset of distinct values and "
            "keeps the largest set that fits in k."
        ),
        cx="O(n + u log u) time, O(u) space (u distinct values)",
        brute_cx="O(2^u * u) time - every subset of values",
        brute=r"""
# BRUTE FORCE: O(2^u * u) time - every subset of values
def find_least_num_of_unique_ints(arr, k):
    counts = list(Counter(arr).values())
    best = len(counts)
    for size in range(len(counts) + 1):
        for subset in itertools.combinations(counts, size):
            if sum(subset) <= k:
                best = min(best, len(counts) - size)
    return best
""",
        solution=r"""
# OPTIMISED: O(n + u log u) time, O(u) space (u distinct values)
# Idea: Greedy on frequencies: remove rarest values first
def find_least_num_of_unique_ints(arr, k):
    counts = sorted(Counter(arr).values())
    unique = len(counts)

    for c in counts:
        if k >= c:
            k -= c
            unique -= 1
        else:
            break

    return unique
""",
    ),
    # ---- Smallest String With A Given Numeric Value (LeetCode 1663) ----
    dict(
        title="Smallest String With A Given Numeric Value",
        diff="M",
        lc=1663,
        slug="smallest-string-with-a-given-numeric-value",
        prompt=(
            "The numeric value of a lowercase letter is its position in the alphabet ('a' = 1, ..., 'z' = 26) and "
            "the value of a string is the sum of its letters. Given n and k, return the lexicographically smallest "
            "string of length n whose value is k (a solution always exists)."
        ),
        sig="def get_smallest_string(n: int, k: int) -> str:",
        fn="get_smallest_string",
        tests=[
            ((3, 27), "aay"),
            ((5, 73), "aaszz"),
            ((1, 26), "z"),
            ((2, 3), "ab"),
        ],
        hints=[
            (
                "Smaller strings have 'a's at the front, so push as much of the value as possible towards the END "
                "of the string."
            ),
            "Start with n letters 'a' (value n); you still have k - n to distribute.",
            (
                "Walk from the last position backwards and raise each letter by min(25, what is left) - a letter "
                "can rise at most from 'a' to 'z'."
            ),
        ],
        pattern="Greedy: fill from the back",
        explain=(
            "Lexicographic order is decided by the earliest positions, so they should be as small as possible, i.e. "
            "'a'. That forces the value into the last positions, each taking up to 25 extra. The brute force builds "
            "the string left to right, trying letters in alphabetical order with only an impossibility prune, so "
            "the first complete string it finds is the smallest."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="exponential in the worst case - backtracking over letters with a feasibility prune",
        brute=r"""
# BRUTE FORCE: exponential in the worst case - backtracking over letters with a feasibility prune
def get_smallest_string(n, k):
    def build(pos, remaining):
        left = n - pos

        if remaining < left or remaining > 26 * left:
            return None

        if left == 0:
            return ""

        for value in range(1, 27):
            rest = build(pos + 1, remaining - value)
            if rest is not None:
                return chr(96 + value) + rest

        return None

    return build(0, k)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Greedy: fill from the back
def get_smallest_string(n, k):
    letters = ["a"] * n
    k -= n
    i = n - 1

    while k > 0:
        add = min(25, k)
        letters[i] = chr(97 + add)
        k -= add
        i -= 1

    return "".join(letters)
""",
    ),
    # ---- Partitioning Into Minimum Number Of Deci-Binary Numbers (LeetCode 1689) ----
    dict(
        title="Partitioning Into Minimum Number Of Deci-Binary Numbers",
        diff="M",
        lc=1689,
        slug="partitioning-into-minimum-number-of-deci-binary-numbers",
        prompt=(
            "A decimal number is DECI-BINARY if each digit is 0 or 1 and it has no leading zeros (e.g. 101, 1100). "
            "Given a positive integer n as a string, return the minimum number of positive deci-binary numbers that "
            "add up to n."
        ),
        sig="def min_partitions(n: str) -> int:",
        fn="min_partitions",
        tests=[
            (("32",), 3),
            (("82734",), 8),
            (("27346209830709182346",), 9),
            (("1",), 1),
        ],
        hints=[
            "Look at one digit position. Each deci-binary number contributes 0 or 1 there.",
            (
                "So a digit d needs at least d numbers - the whole sum needs at least as many numbers as the "
                "LARGEST digit."
            ),
            (
                "That many is also enough: use one number per unit of each digit, choosing the 1s where the digit "
                "still needs them. The answer is the maximum digit."
            ),
        ],
        pattern="Max digit (lower bound that is achievable)",
        explain=(
            "A digit d can only be built from d ones in that column, so the count of numbers is at least max digit. "
            "Taking m = max digit numbers, number j puts a 1 in every column whose digit is >= j; columns then add "
            "up to exactly their digits. The brute force peels off one deci-binary number at a time (1 in every "
            "non-zero column) and counts the rounds."
        ),
        cx="O(L) time, O(1) space",
        brute_cx="O(9 * L) time - subtract one deci-binary number per round",
        brute=r"""
# BRUTE FORCE: O(9 * L) time - subtract one deci-binary number per round
def min_partitions(n):
    digits = [int(c) for c in n]
    rounds = 0
    while any(digits):
        digits = [d - 1 if d > 0 else 0 for d in digits]
        rounds += 1
    return rounds
""",
        solution=r"""
# OPTIMISED: O(L) time, O(1) space
# Idea: Max digit (lower bound that is achievable)
def min_partitions(n):
    return int(max(n))
""",
    ),
    # ---- Maximum Element After Decreasing and Rearranging (LeetCode 1846) ----
    dict(
        title="Maximum Element After Decreasing and Rearranging",
        diff="M",
        lc=1846,
        slug="maximum-element-after-decreasing-and-rearranging",
        prompt=(
            "Given positive integers arr, you may decrease any element to a smaller positive integer and rearrange "
            "the elements in any order. The final array must start with 1 and every adjacent pair may differ by at "
            "most 1. Return the maximum possible value in the final array."
        ),
        sig="def maximum_element_after_decrementing_and_rearranging(arr: List[int]) -> int:",
        fn="maximum_element_after_decrementing_and_rearranging",
        tests=[
            (([2, 2, 1, 2, 1],), 2),
            (([100, 1, 1000],), 3),
            (([1, 2, 3, 4, 5],), 5),
            (([1],), 1),
        ],
        hints=[
            "Sort the array - rearranging is free, and a sorted order is the easiest to repair.",
            (
                "The first element must become 1. Every later element can be at most (previous element + 1), and no "
                "more than its own value."
            ),
            "Walk the sorted array setting arr[i] = min(arr[i], arr[i - 1] + 1). The last element is the answer.",
        ],
        pattern="Sort + greedy cap by the previous element",
        explain=(
            "In the sorted array each element is limited by two things: its own size (we can only decrease) and the "
            "chain rule (at most 1 above the previous one). Taking the minimum of both gives the largest valid "
            "value at each place, and the last one is the maximum overall. The brute force tests candidate answers "
            "m = n .. 1 and checks that 1, 2, ..., m can each be assigned to a distinct element that is at least as "
            "large."
        ),
        cx="O(n log n) time, O(1) extra space",
        brute_cx="O(n^2) time - test every candidate maximum",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every candidate maximum
def maximum_element_after_decrementing_and_rearranging(arr):
    ordered = sorted(arr)

    for m in range(len(ordered), 0, -1):
        pos = 0
        ok = True

        for need in range(1, m + 1):
            while pos < len(ordered) and ordered[pos] < need:
                pos += 1
            if pos == len(ordered):
                ok = False
                break
            pos += 1

        if ok:
            return m
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space
# Idea: Sort + greedy cap by the previous element
def maximum_element_after_decrementing_and_rearranging(arr):
    arr = sorted(arr)
    arr[0] = 1
    for i in range(1, len(arr)):
        arr[i] = min(arr[i], arr[i - 1] + 1)
    return arr[-1]
""",
    ),
    # ---- Merge Triplets to Form Target Triplet (LeetCode 1899) ----
    dict(
        title="Merge Triplets to Form Target Triplet",
        diff="M",
        lc=1899,
        slug="merge-triplets-to-form-target-triplet",
        prompt=(
            "Each triplet is [a, b, c]. You may pick two triplets and replace one by their element-wise maximum, "
            "any number of times. Return true if you can make some triplet equal to target = [x, y, z]."
        ),
        sig="def merge_triplets(triplets: List[List[int]], target: List[int]) -> bool:",
        fn="merge_triplets",
        tests=[
            (([[2, 5, 3], [1, 8, 4], [1, 7, 5]], [2, 7, 5]), True),
            (([[3, 4, 5], [4, 5, 6]], [3, 2, 5]), False),
            (([[2, 5, 3], [2, 3, 4], [1, 2, 5], [5, 2, 3]], [5, 5, 5]), True),
            (([[1, 1, 1]], [2, 2, 2]), False),
        ],
        hints=[
            "Taking a maximum can only ever raise values, never lower them.",
            "So a triplet with ANY coordinate bigger than the target can never be used.",
            (
                "Keep only the triplets that are <= target in all three coordinates, and check that the "
                "coordinate-wise maximum of those equals target."
            ),
        ],
        pattern="Filter unusable items, then check coverage",
        explain=(
            "A triplet that overshoots the target in one coordinate would poison the maximum, so it is useless. "
            "Among the safe ones, merging all of them gives the largest reachable triplet; each target coordinate "
            "must be supplied by at least one safe triplet. The brute force tries every subset of triplets, merges "
            "it and compares with the target."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(2^n * n) time - every subset of triplets",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - every subset of triplets
def merge_triplets(triplets, target):
    n = len(triplets)
    for size in range(1, n + 1):
        for chosen in itertools.combinations(triplets, size):
            merged = [max(t[i] for t in chosen) for i in range(3)]
            if merged == list(target):
                return True
    return False
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Filter unusable items, then check coverage
def merge_triplets(triplets, target):
    best = [0, 0, 0]
    for t in triplets:
        if t[0] <= target[0] and t[1] <= target[1] and t[2] <= target[2]:
            best = [max(best[i], t[i]) for i in range(3)]
    return best == list(target)
""",
    ),
    # ---- Maximum Number of Weeks for Which You Can Work (LeetCode 1953) ----
    dict(
        title="Maximum Number of Weeks for Which You Can Work",
        diff="M",
        lc=1953,
        slug="maximum-number-of-weeks-for-which-you-can-work",
        prompt=(
            "milestones[i] is the number of milestones in project i. Every week you complete exactly ONE milestone "
            "from ONE project, and you may NOT work on the same project in two consecutive weeks. You stop the "
            "first time you are forced to break that rule. Return the maximum number of weeks you can work."
        ),
        sig="def number_of_weeks(milestones: List[int]) -> int:",
        fn="number_of_weeks",
        tests=[
            (([1, 2, 3],), 6),
            (([5, 2, 1],), 7),
            (([1],), 1),
            (([4, 1],), 3),
        ],
        hints=[
            "If no project is huge, you can interleave everything and finish ALL milestones.",
            "The only trouble is the largest project: its milestones need other projects' milestones between them.",
            (
                "Let m be the largest count and rest = total - m. If m <= rest + 1 the answer is total, otherwise "
                "it is 2 * rest + 1 (the big project gets rest + 1 slots)."
            ),
        ],
        pattern="Largest pile vs everything else",
        explain=(
            "Separating k big-project milestones needs k - 1 milestones from other projects, so the big one can use "
            "at most rest + 1 weeks. If it has fewer than that, a careful interleaving finishes every milestone. "
            "The brute force explores every legal sequence of weeks with memoisation on (remaining counts, last "
            "project)."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="exponential - explore all legal week orders (memoised on the state)",
        brute=r"""
# BRUTE FORCE: exponential - explore all legal week orders (memoised on the state)
def number_of_weeks(milestones):
    @lru_cache(None)
    def best(state, last):
        result = 0
        for i, left in enumerate(state):
            if left and i != last:
                nxt = state[:i] + (left - 1,) + state[i + 1 :]
                result = max(result, 1 + best(nxt, i))
        return result

    return best(tuple(milestones), -1)
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Largest pile vs everything else
def number_of_weeks(milestones):
    total = sum(milestones)
    biggest = max(milestones)
    rest = total - biggest
    if biggest > rest + 1:
        return 2 * rest + 1
    return total
""",
    ),
    # ---- Minimum Number of Swaps to Make the String Balanced (LeetCode 1963) ----
    dict(
        title="Minimum Number of Swaps to Make the String Balanced",
        diff="M",
        lc=1963,
        slug="minimum-number-of-swaps-to-make-the-string-balanced",
        prompt=(
            "s has even length n with exactly n / 2 '[' and n / 2 ']'. It is balanced if it is empty, or is '[' + "
            "balanced + ']', or is two balanced strings joined together. You may swap any two characters any number "
            "of times. Return the minimum number of swaps needed to make s balanced."
        ),
        sig="def min_swaps(s: str) -> int:",
        fn="min_swaps",
        tests=[
            (("][][",), 1),
            (("]]][[[",), 2),
            (("[]",), 0),
            (("][",), 1),
        ],
        hints=[
            (
                "Scan left to right, matching each ']' with an earlier unmatched '['. A ']' with nothing to match "
                "is a problem."
            ),
            "Count those unmatched ']' (call it u). The unmatched '[' appear later and there are exactly u of them.",
            (
                "One swap fixes two problems at once (it moves one '[' to the front, replacing a stray ']'), so the "
                "answer is (u + 1) // 2."
            ),
        ],
        pattern="Count unmatched closers; one swap fixes two",
        explain=(
            "After cancelling matched pairs, the string reduces to u closers followed by u openers: ']]]...[[[...'. "
            "Swapping the outermost pair of that reduced string fixes two closers and two openers at once, so "
            "ceil(u / 2) swaps are needed and enough. The brute force runs a BFS over strings, one swap per step, "
            "until one is balanced."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(states * n^2) time - breadth-first search over swap sequences",
        brute=r"""
# BRUTE FORCE: O(states * n^2) time - breadth-first search over swap sequences
def min_swaps(s):
    def balanced(t):
        depth = 0
        for ch in t:
            depth += 1 if ch == "[" else -1
            if depth < 0:
                return False
        return True

    seen = {s}
    frontier = [s]
    steps = 0

    while frontier:
        if any(balanced(t) for t in frontier):
            return steps

        nxt = []

        for t in frontier:
            chars = list(t)

            for i in range(len(chars)):
                for j in range(i + 1, len(chars)):
                    if chars[i] != chars[j]:
                        chars[i], chars[j] = chars[j], chars[i]
                        u = "".join(chars)
                        chars[i], chars[j] = chars[j], chars[i]
                        if u not in seen:
                            seen.add(u)
                            nxt.append(u)

        frontier = nxt
        steps += 1
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Count unmatched closers; one swap fixes two
def min_swaps(s):
    open_count = 0
    stray = 0

    for ch in s:
        if ch == "[":
            open_count += 1
        elif open_count > 0:
            open_count -= 1
        else:
            stray += 1

    return (stray + 1) // 2
""",
    ),
    # ---- The Number of Weak Characters in the Game (LeetCode 1996) ----
    dict(
        title="The Number of Weak Characters in the Game",
        diff="M",
        lc=1996,
        slug="the-number-of-weak-characters-in-the-game",
        prompt=(
            "properties[i] = [attack, defense] of character i. Character i is WEAK if some other character has BOTH "
            "strictly greater attack and strictly greater defense. Return the number of weak characters."
        ),
        sig="def number_of_weak_characters(properties: List[List[int]]) -> int:",
        fn="number_of_weak_characters",
        tests=[
            (([[5, 5], [6, 3], [3, 6]],), 0),
            (([[2, 2], [3, 3]],), 1),
            (([[1, 5], [10, 4], [4, 3]],), 1),
            (([[1, 1], [1, 1]],), 0),
        ],
        hints=[
            "Brute force: for each character look through all others for one that beats it in both stats - O(n^2).",
            (
                "Sort by attack descending. Then everything seen so far has attack >= the current one, so only the "
                "defense must be compared with the best defense seen so far."
            ),
            (
                "Ties in attack must not count: sort equal attacks by defense ASCENDING so that a stronger-defense "
                "twin cannot be seen first."
            ),
        ],
        pattern="Sort one dimension, sweep the other",
        explain=(
            "After sorting attack descending, every earlier character has attack at least as large; making equal "
            "attacks appear with weaker defense first means a same-attack character is never mistaken for a "
            "dominator. A character is weak exactly when its defense is below the maximum defense seen before it. "
            "The brute force compares every ordered pair."
        ),
        cx="O(n log n) time, O(1) extra space",
        brute_cx="O(n^2) time - compare every pair",
        brute=r"""
# BRUTE FORCE: O(n^2) time - compare every pair
def number_of_weak_characters(properties):
    weak = 0
    for i, (a, d) in enumerate(properties):
        if any(a2 > a and d2 > d for j, (a2, d2) in enumerate(properties) if j != i):
            weak += 1
    return weak
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space
# Idea: Sort one dimension, sweep the other
def number_of_weak_characters(properties):
    ordered = sorted(properties, key=lambda p: (-p[0], p[1]))
    best_defense = 0
    weak = 0

    for _, defense in ordered:
        if defense < best_defense:
            weak += 1
        else:
            best_defense = defense

    return weak
""",
    ),
    # ---- Remove Colored Pieces if Both Neighbors are the Same Color (LeetCode 2038) ----
    dict(
        title="Remove Colored Pieces if Both Neighbors are the Same Color",
        diff="M",
        lc=2038,
        slug="remove-colored-pieces-if-both-neighbors-are-the-same-color",
        prompt=(
            "colors is a row of pieces, each 'A' or 'B'. Alice and Bob alternate, Alice first. Alice may remove an "
            "'A' whose two neighbours are BOTH 'A'; Bob may remove a 'B' whose two neighbours are both 'B'. Neither "
            "may touch the other colour. A player who cannot move loses. Return true if Alice wins with optimal "
            "play."
        ),
        sig="def winner_of_game(colors: str) -> bool:",
        fn="winner_of_game",
        tests=[
            (("AAABABB",), True),
            (("AA",), False),
            (("ABBBBBBBAAA",), False),
            (("AAA",), True),
        ],
        hints=[
            (
                "Removing an 'A' never creates or destroys a move for Bob, and vice versa - the two players do not "
                "interfere."
            ),
            (
                "In a run of k equal letters (k >= 3) exactly k - 2 removals are possible in total, whatever order "
                "they are done in."
            ),
            (
                "So count Alice's available moves (sum over 'A' runs of k - 2) and Bob's. Alice moves first, so she "
                "wins exactly when her count is strictly larger."
            ),
        ],
        pattern="Independent move counts decide a game",
        explain=(
            "Each removal shrinks one run by one and only changes that run, so the total number of moves per player "
            "is fixed from the start. Players alternate and the first one to run out loses; Alice needs strictly "
            "more moves than Bob because she goes first (equal counts mean Alice is stuck first). The brute force "
            "plays the actual game tree with memoisation."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="exponential - search the whole game tree (memoised on the string)",
        brute=r"""
# BRUTE FORCE: exponential - search the whole game tree (memoised on the string)
def winner_of_game(colors):
    @lru_cache(None)
    def wins(s, turn):
        for i in range(1, len(s) - 1):
            if s[i - 1] == s[i] == s[i + 1] == turn:
                other = "B" if turn == "A" else "A"
                if not wins(s[:i] + s[i + 1 :], other):
                    return True
        return False

    return wins(colors, "A")
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Independent move counts decide a game
def winner_of_game(colors):
    alice = bob = 0

    for i in range(1, len(colors) - 1):
        if colors[i - 1] == colors[i] == colors[i + 1]:
            if colors[i] == "A":
                alice += 1
            else:
                bob += 1

    return alice > bob
""",
    ),
    # ---- Destroying Asteroids (LeetCode 2126) ----
    dict(
        title="Destroying Asteroids",
        diff="M",
        lc=2126,
        slug="destroying-asteroids",
        prompt=(
            "A planet of mass `mass` collides with the asteroids in any order you like. If the planet's mass is at "
            "least the asteroid's mass, the asteroid is destroyed and its mass is ADDED to the planet; otherwise "
            "the planet is destroyed. Return true if all asteroids can be destroyed."
        ),
        sig="def asteroids_destroyed(mass: int, asteroids: List[int]) -> bool:",
        fn="asteroids_destroyed",
        tests=[
            ((10, [3, 9, 19, 5, 21]), True),
            ((5, [4, 9, 23, 4]), False),
            ((1, [1]), True),
            ((1, [2]), False),
        ],
        hints=[
            "Eating anything makes the planet bigger, so eat the safest asteroids first.",
            "Sort the asteroids from smallest to largest.",
            (
                "Go through them in that order: if mass < asteroid return false, otherwise add it to the mass. If "
                "you finish, return true."
            ),
        ],
        pattern="Sort ascending, grow as you go",
        explain=(
            "If any order works, then smallest-first works too: the smallest asteroid is the easiest and gives a "
            "snowball. An exchange argument shows that eating a larger asteroid before a smaller one can only hurt. "
            "The brute force tries every possible order of asteroids."
        ),
        cx="O(n log n) time, O(1) extra space",
        brute_cx="O(n! * n) time - try every order",
        brute=r"""
# BRUTE FORCE: O(n! * n) time - try every order
def asteroids_destroyed(mass, asteroids):
    for order in itertools.permutations(asteroids):
        current = mass
        for rock in order:
            if current < rock:
                break
            current += rock
        else:
            return True

    return False
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space
# Idea: Sort ascending, grow as you go
def asteroids_destroyed(mass, asteroids):
    for rock in sorted(asteroids):
        if mass < rock:
            return False
        mass += rock
    return True
""",
    ),
    # ---- Maximum Bags With Full Capacity of Rocks (LeetCode 2279) ----
    dict(
        title="Maximum Bags With Full Capacity of Rocks",
        diff="M",
        lc=2279,
        slug="maximum-bags-with-full-capacity-of-rocks",
        prompt=(
            "Bag i can hold capacity[i] rocks and currently holds rocks[i]. You have additionalRocks more rocks to "
            "distribute freely among the bags. Return the maximum number of bags that can be FULL."
        ),
        sig="def maximum_bags(capacity: List[int], rocks: List[int], additional_rocks: int) -> int:",
        fn="maximum_bags",
        tests=[
            (([2, 3, 4, 5], [1, 2, 4, 4], 2), 3),
            (([10, 2, 2], [2, 2, 0], 100), 3),
            (([1], [0], 0), 0),
            (([3, 3], [0, 1], 2), 1),
        ],
        hints=[
            "A bag needs capacity[i] - rocks[i] more rocks to be full. A bag that is already full needs 0.",
            "Each rock is worth the same, so you want to fill as MANY bags as possible, i.e. the cheapest ones.",
            "Sort these needs ascending and fill bags in that order while you still have enough rocks.",
        ],
        pattern="Sort costs, take the cheapest first",
        explain=(
            "This is the classic 'buy as many items as you can with a budget' problem: every full bag counts one, "
            "and its price is its need, so the cheapest bags first is optimal. Partially filling a bag gives "
            "nothing, so leftover rocks are simply unused. The brute force tries all subsets of bags by size, "
            "largest first, and returns the first size for which some subset of that many bags fits in the budget."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(2^n * n) time - every subset of bags",
        brute=r"""
# BRUTE FORCE: O(2^n * n) time - every subset of bags
def maximum_bags(capacity, rocks, additional_rocks):
    need = [c - r for c, r in zip(capacity, rocks)]
    for size in range(len(need), -1, -1):
        for combo in itertools.combinations(need, size):
            if sum(combo) <= additional_rocks:
                return size
    return 0
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Sort costs, take the cheapest first
def maximum_bags(capacity, rocks, additional_rocks):
    need = sorted(c - r for c, r in zip(capacity, rocks))
    full = 0

    for gap in need:
        if gap > additional_rocks:
            break
        additional_rocks -= gap
        full += 1

    return full
""",
    ),
    # ---- Partition Array Such That Maximum Difference Is K (LeetCode 2294) ----
    dict(
        title="Partition Array Such That Maximum Difference Is K",
        diff="M",
        lc=2294,
        slug="partition-array-such-that-maximum-difference-is-k",
        prompt=(
            "Split nums into the minimum number of SUBSEQUENCES (every element in exactly one) so that inside each "
            "subsequence the difference between its maximum and minimum element is at most k. Return that minimum "
            "number of subsequences."
        ),
        sig="def partition_array(nums: List[int], k: int) -> int:",
        fn="partition_array",
        tests=[
            (([3, 6, 1, 2, 5], 2), 2),
            (([1, 2, 3], 1), 2),
            (([2, 2, 4, 5], 0), 3),
            (([7], 3), 1),
        ],
        hints=[
            (
                "Subsequences do not need to be contiguous, so the ORDER of nums is irrelevant - only which values "
                "share a group."
            ),
            "Sort the array. Groups then become contiguous blocks of the sorted array.",
            (
                "Start a group at the smallest unused value and swallow every value up to start + k; the first "
                "value beyond that starts the next group."
            ),
        ],
        pattern="Sort + greedy interval cover",
        explain=(
            "This is the same as covering points on a line with the fewest intervals of length k. Starting an "
            "interval at the leftmost uncovered point is optimal because moving it to the right could only uncover "
            "that point. The brute force explores every way of putting each element into an existing group or a new "
            "one, pruning branches that already use too many groups."
        ),
        cx="O(n log n) time, O(1) extra space",
        brute_cx="exponential - try every assignment of elements to groups (Bell-number growth)",
        brute=r"""
# BRUTE FORCE: exponential - try every assignment of elements to groups (Bell-number growth)
def partition_array(nums, k):
    best = [len(nums)]
    groups = []

    def place(i):
        if len(groups) >= best[0]:
            return

        if i == len(nums):
            best[0] = len(groups)
            return

        x = nums[i]

        for g in groups:
            lo, hi = g
            if max(hi, x) - min(lo, x) <= k:
                g[0], g[1] = min(lo, x), max(hi, x)
                place(i + 1)
                g[0], g[1] = lo, hi

        groups.append([x, x])
        place(i + 1)
        groups.pop()

    place(0)

    return best[0]
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space
# Idea: Sort + greedy interval cover
def partition_array(nums, k):
    ordered = sorted(nums)
    groups = 1
    start = ordered[0]

    for x in ordered:
        if x - start > k:
            groups += 1
            start = x

    return groups
""",
    ),
    # ---- Optimal Partition of String (LeetCode 2405) ----
    dict(
        title="Optimal Partition of String",
        diff="M",
        lc=2405,
        slug="optimal-partition-of-string",
        prompt=(
            "Partition s into the fewest contiguous substrings such that NO letter appears twice inside the same "
            "substring. Return the minimum number of substrings."
        ),
        sig="def partition_string(s: str) -> int:",
        fn="partition_string",
        tests=[
            (("abacaba",), 4),
            (("ssssss",), 6),
            (("a",), 1),
            (("abc",), 1),
        ],
        hints=[
            "Extend the current substring as long as you can - ending it early never helps.",
            "Keep a set of the letters in the current substring.",
            (
                "When the next letter is already in the set, start a new substring (count + 1) with a fresh set "
                "containing that letter."
            ),
        ],
        pattern="Greedy: extend until a repeat forces a cut",
        explain=(
            "If a substring could still be extended without a repeat, cutting it there would leave the next piece "
            "starting earlier but never allow fewer pieces overall (the standard exchange argument for greedy "
            "partitioning). A cut is forced exactly at the first repeated letter. The brute force uses dynamic "
            "programming over every cut position and checks each candidate substring for repeats."
        ),
        cx="O(n) time, O(26) space",
        brute_cx="O(n^3) time - DP over all cut positions, each substring checked for repeats",
        brute=r"""
# BRUTE FORCE: O(n^3) time - DP over all cut positions, each substring checked for repeats
def partition_string(s):
    n = len(s)
    best = [0] + [n] * n

    for end in range(1, n + 1):
        for start in range(end):
            piece = s[start:end]
            if len(set(piece)) == len(piece):
                best[end] = min(best[end], best[start] + 1)

    return best[n]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(26) space
# Idea: Greedy: extend until a repeat forces a cut
def partition_string(s):
    count = 1
    seen = set()

    for ch in s:
        if ch in seen:
            count += 1
            seen = set()
        seen.add(ch)

    return count
""",
    ),
]
