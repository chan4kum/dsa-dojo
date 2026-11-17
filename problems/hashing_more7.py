"""extra batch of Hashing problems - the problem bank for the "hashing" topic (batch 7).

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
    # ---- Distribute Candies (LeetCode 575) ----
    dict(
        title="Distribute Candies",
        diff="E",
        lc=575,
        slug="distribute-candies",
        prompt=(
            "candy_type has an even length n; candy_type[i] is the type of candy i. Alice may eat only n / 2 "
            "candies. Return the maximum number of DIFFERENT types she can eat."
        ),
        sig="def distribute_candies(candy_type: List[int]) -> int:",
        fn="distribute_candies",
        tests=[
            (([1, 1, 2, 2, 3, 3],), 3),
            (([1, 1, 2, 3],), 2),
            (([6, 6, 6, 6],), 1),
            (([1, 2, 3, 4],), 2),
        ],
        hints=[
            "She can never eat more distinct types than there are types in total.",
            "She also cannot eat more than n / 2 candies, so she cannot taste more than n / 2 types.",
            "Answer = min(number of distinct types, n // 2) - a set gives the first number.",
        ],
        pattern="Upper bound from two limits; a set counts distinct values",
        explain=(
            "Two independent caps apply: the number of distinct types (you cannot eat a type that does not exist) "
            "and the number of candies she may eat (each new type costs at least one candy). The minimum of the two "
            "is always achievable: if there are at least n/2 types she picks n/2 different ones, otherwise she "
            "tastes every type and fills the rest with repeats. The brute force tries every choice of n/2 candies."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(C(n, n/2) * n) time - try every choice of n / 2 candies",
        brute=r"""
# BRUTE FORCE: O(C(n, n/2) * n) time - try every choice of n / 2 candies
def distribute_candies(candy_type):
    n = len(candy_type)
    best = 0
    for combo in itertools.combinations(range(n), n // 2):
        best = max(best, len({candy_type[i] for i in combo}))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Upper bound from two limits; a set counts distinct values
def distribute_candies(candy_type):
    return min(len(set(candy_type)), len(candy_type) // 2)
""",
    ),
    # ---- Minimum Index Sum of Two Lists (LeetCode 599) ----
    dict(
        title="Minimum Index Sum of Two Lists",
        diff="E",
        lc=599,
        slug="minimum-index-sum-of-two-lists",
        prompt=(
            "list1 and list2 each hold distinct strings. A common string has index sum i + j where i, j are its "
            "positions in the two lists. Return all common strings with the SMALLEST index sum, in any order (at "
            "least one common string exists)."
        ),
        sig="def find_restaurant(list1: List[str], list2: List[str]) -> List[str]:",
        fn="find_restaurant",
        compare="unordered",
        tests=[
            (
                (
                    ["Shogun", "Tapioca Express", "Burger King", "KFC"],
                    ["Piatti", "The Grill at Torrey Pines", "Hungry Hunter Steakhouse", "Shogun"],
                ),
                ["Shogun"],
            ),
            ((["Shogun", "Tapioca Express", "Burger King", "KFC"], ["KFC", "Shogun", "Burger King"]), ["Shogun"]),
            ((["happy", "sad", "good"], ["sad", "happy", "good"]), ["sad", "happy"]),
            ((["a", "b"], ["b", "a"]), ["a", "b"]),
        ],
        hints=[
            "Comparing every string of list1 with every string of list2 costs O(n * m).",
            "Store the index of each list1 string in a dictionary.",
            (
                "Walk list2; for a common string add the two indices, track the minimum and collect the strings "
                "that reach it."
            ),
        ],
        pattern="Hash map of positions + running minimum",
        explain=(
            "A dictionary string -> index turns the 'is it in list1 and where' question into an O(1) lookup. While "
            "scanning list2 we maintain the best (smallest) index sum so far and the list of strings achieving it: "
            "a strictly smaller sum resets the list, an equal sum appends. The brute force compares every pair of "
            "strings."
        ),
        cx="O(n + m) time, O(n) space",
        brute_cx="O(n * m) time - compare every pair of strings",
        brute=r"""
# BRUTE FORCE: O(n * m) time - compare every pair of strings
def find_restaurant(list1, list2):
    best, out = None, []

    for i, a in enumerate(list1):
        for j, b in enumerate(list2):
            if a == b:
                if best is None or i + j < best:
                    best, out = i + j, [a]
                elif i + j == best:
                    out.append(a)

    return out
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(n) space
# Idea: Hash map of positions + running minimum
def find_restaurant(list1, list2):
    index = {s: i for i, s in enumerate(list1)}
    best, out = None, []

    for j, s in enumerate(list2):
        if s in index:
            total = index[s] + j
            if best is None or total < best:
                best, out = total, [s]
            elif total == best:
                out.append(s)

    return out
""",
    ),
    # ---- Number of Good Pairs (LeetCode 1512) ----
    dict(
        title="Number of Good Pairs",
        diff="E",
        lc=1512,
        slug="number-of-good-pairs",
        prompt="A pair (i, j) is good if nums[i] == nums[j] and i < j. Return the number of good pairs.",
        sig="def num_identical_pairs(nums: List[int]) -> int:",
        fn="num_identical_pairs",
        tests=[
            (([1, 2, 3, 1, 1, 3],), 4),
            (([1, 1, 1, 1],), 6),
            (([1, 2, 3],), 0),
            (([5],), 0),
        ],
        hints=[
            "Equal values form groups; a good pair lives inside one group.",
            "A group of size c contains c * (c - 1) / 2 pairs.",
            (
                "Count the groups with a hash map and add up the formula - or add the running count of earlier "
                "equal values."
            ),
        ],
        pattern="Count equal values; pairs = c * (c - 1) / 2",
        explain=(
            "Pairs never cross groups of different values, so the answer is the sum over values of C(c, 2). "
            "Equivalently, scanning left to right, each element forms a good pair with every EARLIER equal element, "
            "so add seen[x] before incrementing it. The brute force tests all pairs."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - test every pair i < j",
        brute=r"""
# BRUTE FORCE: O(n^2) time - test every pair i < j
def num_identical_pairs(nums):
    count = 0
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] == nums[j]:
                count += 1
    return count
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Count equal values; pairs = c * (c - 1) / 2
def num_identical_pairs(nums):
    seen = Counter()
    total = 0
    for x in nums:
        total += seen[x]
        seen[x] += 1
    return total
""",
    ),
    # ---- Check if All Characters Have Equal Number of Occurrences (LeetCode 1941) ----
    dict(
        title="Check if All Characters Have Equal Number of Occurrences",
        diff="E",
        lc=1941,
        slug="check-if-all-characters-have-equal-number-of-occurrences",
        prompt="Return true if every character that appears in s appears exactly the same number of times.",
        sig="def are_occurrences_equal(s: str) -> bool:",
        fn="are_occurrences_equal",
        tests=[
            (("abacbc",), True),
            (("aaabb",), False),
            (("a",), True),
            (("aabbc",), False),
        ],
        hints=[
            "Count the occurrences of every character.",
            "All counts are equal exactly when there is only ONE distinct count.",
            "len(set(counts.values())) == 1.",
        ],
        pattern="Count, then test that the set of counts has size one",
        explain=(
            "A frequency table maps each character to its count. If all counts coincide, collapsing them into a set "
            "leaves a single element. The brute force recounts each character with str.count and compares with the "
            "first count."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n * distinct) time - s.count for every distinct character",
        brute=r"""
# BRUTE FORCE: O(n * distinct) time - s.count for every distinct character
def are_occurrences_equal(s):
    first = s.count(s[0])
    return all(s.count(ch) == first for ch in set(s))
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Count, then test that the set of counts has size one
def are_occurrences_equal(s):
    return len(set(Counter(s).values())) == 1
""",
    ),
    # ---- Kth Distinct String in an Array (LeetCode 2053) ----
    dict(
        title="Kth Distinct String in an Array",
        diff="E",
        lc=2053,
        slug="kth-distinct-string-in-an-array",
        prompt=(
            "A string is distinct if it appears exactly once in arr. Return the k-th distinct string in the order "
            "of arr, or an empty string if there are fewer than k distinct strings."
        ),
        sig="def kth_distinct(arr: List[str], k: int) -> str:",
        fn="kth_distinct",
        tests=[
            ((["d", "b", "c", "b", "c", "a"], 2), "a"),
            ((["aaa", "aa", "a"], 1), "aaa"),
            ((["a", "b", "a"], 3), ""),
            ((["x"], 1), "x"),
        ],
        hints=[
            "First find out how many times each string occurs.",
            "'Distinct' means count == 1; the ORDER is the order of first appearance in arr.",
            "Scan arr once more, skipping strings with count > 1, and return the k-th survivor.",
        ],
        pattern="Frequency map, then an ordered second pass",
        explain=(
            "A Counter answers 'is this string unique' in O(1). Because the result must respect the original order, "
            "we cannot just iterate over the counter (well, a dict keeps insertion order, but a second pass over "
            "arr is the clearest). The brute force recounts each element with list.count."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - list.count for every element",
        brute=r"""
# BRUTE FORCE: O(n^2) time - list.count for every element
def kth_distinct(arr, k):
    for s in arr:
        if arr.count(s) == 1:
            k -= 1
            if k == 0:
                return s
    return ""
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Frequency map, then an ordered second pass
def kth_distinct(arr, k):
    counts = Counter(arr)
    for s in arr:
        if counts[s] == 1:
            k -= 1
            if k == 0:
                return s
    return ""
""",
    ),
    # ---- Count Common Words With One Occurrence (LeetCode 2085) ----
    dict(
        title="Count Common Words With One Occurrence",
        diff="E",
        lc=2085,
        slug="count-common-words-with-one-occurrence",
        prompt="Return the number of strings that appear exactly once in words1 AND exactly once in words2.",
        sig="def count_words(words1: List[str], words2: List[str]) -> int:",
        fn="count_words",
        tests=[
            ((["leetcode", "is", "amazing", "as", "is"], ["amazing", "leetcode", "is"]), 2),
            ((["b", "bb", "bbb"], ["a", "aa", "aaa"]), 0),
            ((["a", "ab"], ["a", "a", "a", "ab"]), 1),
            ((["x"], ["x"]), 1),
        ],
        hints=[
            "Count the words of each list separately.",
            "A word qualifies if it has count 1 in the first list and count 1 in the second.",
            "Iterate over one counter and look the word up in the other.",
        ],
        pattern="Two frequency maps and an intersection test",
        explain=(
            "One Counter per list gives O(1) occurrence queries. A qualifying word must be in both maps with count "
            "exactly 1, so it is enough to iterate over the words of the first list. The brute force counts "
            "occurrences with list.count for every distinct word."
        ),
        cx="O(n + m) time, O(n + m) space",
        brute_cx="O(n * (n + m)) time - list.count in both lists for every distinct word",
        brute=r"""
# BRUTE FORCE: O(n * (n + m)) time - list.count in both lists for every distinct word
def count_words(words1, words2):
    return sum(1 for w in set(words1) if words1.count(w) == 1 and words2.count(w) == 1)
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(n + m) space
# Idea: Two frequency maps and an intersection test
def count_words(words1, words2):
    c1, c2 = Counter(words1), Counter(words2)
    return sum(1 for w, k in c1.items() if k == 1 and c2[w] == 1)
""",
    ),
    # ---- Intersection of Multiple Arrays (LeetCode 2248) ----
    dict(
        title="Intersection of Multiple Arrays",
        diff="E",
        lc=2248,
        slug="intersection-of-multiple-arrays",
        prompt=(
            "nums is a list of arrays of distinct positive integers. Return, in ascending order, the integers that "
            "appear in EVERY array."
        ),
        sig="def intersection(nums: List[List[int]]) -> List[int]:",
        fn="intersection",
        tests=[
            (([[3, 1, 2, 4, 5], [1, 2, 3, 4], [3, 4, 5, 6]],), [3, 4]),
            (([[1, 2, 3], [4, 5, 6]],), []),
            (([[7]],), [7]),
            (([[1, 2], [2, 1], [1, 2]],), [1, 2]),
        ],
        hints=[
            "Values inside one array are distinct, so a value's total count equals the number of arrays containing it.",
            "Count every value across all arrays with a hash map.",
            "Keep the values whose count equals len(nums) and sort them.",
        ],
        pattern="Count occurrences across arrays; keep those present in all",
        explain=(
            "Because each array has distinct values, a value appears in an array at most once, so its global count "
            "is the number of arrays that contain it. A value is in the intersection iff that count is len(nums). "
            "The brute force checks each value of the first array against every other array with list membership."
        ),
        cx="O(N + k log k) time for N numbers, k results",
        brute_cx="O(N * total) time - list membership test of every first-array value in each other array",
        brute=r"""
# BRUTE FORCE: O(N * total) time - list membership test of every first-array value in each other array
def intersection(nums):
    out = []
    for v in nums[0]:
        if all(v in arr for arr in nums[1:]):
            out.append(v)
    return sorted(out)
""",
        solution=r"""
# OPTIMISED: O(N + k log k) time for N numbers, k results
# Idea: Count occurrences across arrays; keep those present in all
def intersection(nums):
    counts = Counter(v for arr in nums for v in arr)
    return sorted(v for v, c in counts.items() if c == len(nums))
""",
    ),
    # ---- Most Frequent Even Element (LeetCode 2404) ----
    dict(
        title="Most Frequent Even Element",
        diff="E",
        lc=2404,
        slug="most-frequent-even-element",
        prompt=(
            "Return the even element that occurs most often in nums. If several are tied, return the smallest of "
            "them. If there is no even element, return -1."
        ),
        sig="def most_frequent_even(nums: List[int]) -> int:",
        fn="most_frequent_even",
        tests=[
            (([0, 1, 2, 2, 4, 4, 1],), 2),
            (([4, 4, 4, 9, 2, 4],), 4),
            (([29, 47, 21, 41, 13, 37, 25, 7],), -1),
            (([2, 4],), 2),
        ],
        hints=[
            "Ignore odd numbers completely.",
            "Count the even numbers in a hash map.",
            "Choose the key with the largest count, breaking ties by the smaller value: minimise (-count, value).",
        ],
        pattern="Filtered frequency map with a composite tie-break key",
        explain=(
            "After filtering the evens, the best element is the one with the maximum count; for equal counts we "
            "want the minimum value. Sorting or taking min() on the key (-count, value) expresses both rules at "
            "once. The brute force recounts each distinct even value with list.count."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n * distinct) time - list.count for every distinct even value",
        brute=r"""
# BRUTE FORCE: O(n * distinct) time - list.count for every distinct even value
def most_frequent_even(nums):
    best, best_count = -1, 0
    for v in sorted({x for x in nums if x % 2 == 0}):
        c = nums.count(v)
        if c > best_count:
            best, best_count = v, c
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Filtered frequency map with a composite tie-break key
def most_frequent_even(nums):
    counts = Counter(x for x in nums if x % 2 == 0)
    if not counts:
        return -1
    return min(counts, key=lambda v: (-counts[v], v))
""",
    ),
    # ---- Largest Positive Integer That Exists With Its Negative (LeetCode 2441) ----
    dict(
        title="Largest Positive Integer That Exists With Its Negative",
        diff="E",
        lc=2441,
        slug="largest-positive-integer-that-exists-with-its-negative",
        prompt="Return the largest positive integer k such that -k is also in nums, or -1 if there is none.",
        sig="def find_max_k(nums: List[int]) -> int:",
        fn="find_max_k",
        tests=[
            (([-1, 2, -3, 3],), 3),
            (([-1, 10, 6, 7, -7, 1],), 7),
            (([-10, 8, 6, 7, -2, -3],), -1),
            (([1, -1],), 1),
        ],
        hints=[
            "For each positive x you only need to know whether -x exists somewhere in the array.",
            "A set answers membership in O(1).",
            "Take the maximum x > 0 with -x in the set, default -1.",
        ],
        pattern="Set membership instead of a nested scan",
        explain=(
            "Putting all numbers into a set means each 'does -x exist' query is O(1), so a single pass finds the "
            "largest valid x. The brute force scans the whole array for -x for every positive x."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - scan the array for -x for every positive x",
        brute=r"""
# BRUTE FORCE: O(n^2) time - scan the array for -x for every positive x
def find_max_k(nums):
    best = -1
    for x in nums:
        if x > 0 and -x in nums:
            best = max(best, x)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Set membership instead of a nested scan
def find_max_k(nums):
    seen = set(nums)
    return max((x for x in seen if x > 0 and -x in seen), default=-1)
""",
    ),
    # ---- Merge Two 2D Arrays by Summing Values (LeetCode 2570) ----
    dict(
        title="Merge Two 2D Arrays by Summing Values",
        diff="E",
        lc=2570,
        slug="merge-two-2d-arrays-by-summing-values",
        prompt=(
            "nums1 and nums2 hold [id, value] pairs, each sorted by id with unique ids inside one array. Return one "
            "array sorted by id that contains every id that appears in either input; its value is the SUM of the "
            "values it has in the inputs (a missing side counts as 0)."
        ),
        sig="def merge_arrays(nums1: List[List[int]], nums2: List[List[int]]) -> List[List[int]]:",
        fn="merge_arrays",
        tests=[
            (([[1, 2], [2, 3], [4, 5]], [[1, 4], [3, 2], [4, 1]]), [[1, 6], [2, 3], [3, 2], [4, 6]]),
            (([[2, 4], [3, 6], [5, 5]], [[1, 3], [4, 3]]), [[1, 3], [2, 4], [3, 6], [4, 3], [5, 5]]),
            (([[1, 1]], [[1, 1]]), [[1, 2]]),
            (([[1, 1]], [[2, 2]]), [[1, 1], [2, 2]]),
        ],
        hints=[
            "A dictionary id -> total value merges both arrays easily; sorting the keys finishes the job.",
            "Because both inputs are already sorted by id, you do not need a sort: merge them like in merge sort.",
            "Two pointers: take the smaller id, or add the values when the ids are equal.",
        ],
        pattern="Two-pointer merge of sorted lists (or hash map + sort)",
        explain=(
            "Hashing gives a simple O((n + m) log(n + m)) solution: accumulate sums per id, then sort the ids. But "
            "the inputs are sorted, so a two-pointer merge produces the answer already in order in O(n + m): "
            "advance the pointer with the smaller id, and when ids tie, emit their sum and advance both."
        ),
        cx="O(n + m) time, O(1) extra space",
        brute_cx="O((n + m) log(n + m)) time - accumulate in a dictionary, then sort the ids",
        brute=r"""
# BRUTE FORCE: O((n + m) log(n + m)) time - accumulate in a dictionary, then sort the ids
def merge_arrays(nums1, nums2):
    total = {}
    for i, v in nums1 + nums2:
        total[i] = total.get(i, 0) + v
    return [[i, total[i]] for i in sorted(total)]
""",
        solution=r"""
# OPTIMISED: O(n + m) time, O(1) extra space
# Idea: Two-pointer merge of sorted lists (or hash map + sort)
def merge_arrays(nums1, nums2):
    out = []
    i = j = 0

    while i < len(nums1) and j < len(nums2):
        if nums1[i][0] < nums2[j][0]:
            out.append(list(nums1[i]))
            i += 1
        elif nums1[i][0] > nums2[j][0]:
            out.append(list(nums2[j]))
            j += 1
        else:
            out.append([nums1[i][0], nums1[i][1] + nums2[j][1]])
            i += 1
            j += 1

    out.extend(list(p) for p in nums1[i:])
    out.extend(list(p) for p in nums2[j:])

    return out
""",
    ),
    # ---- Find the Distinct Difference Array (LeetCode 2670) ----
    dict(
        title="Find the Distinct Difference Array",
        diff="E",
        lc=2670,
        slug="find-the-distinct-difference-array",
        prompt=(
            "For every index i, diff[i] = (number of distinct values in nums[0..i]) - (number of distinct values in "
            "nums[i+1..n-1]). Return diff."
        ),
        sig="def distinct_difference_array(nums: List[int]) -> List[int]:",
        fn="distinct_difference_array",
        tests=[
            (([1, 2, 3, 4, 5],), [-3, -1, 1, 3, 5]),
            (([3, 2, 3, 4, 2],), [-2, -1, 0, 2, 3]),
            (([1],), [1]),
            (([1, 1],), [0, 1]),
        ],
        hints=[
            "Rebuilding both sets for every index is O(n^2).",
            (
                "The number of distinct values in a prefix only changes when a NEW value appears - a running set "
                "gives all prefix counts in one pass."
            ),
            "Do the same from the right for the suffix counts, then subtract.",
        ],
        pattern="Prefix and suffix distinct counts with running sets",
        explain=(
            "prefix[i] is the size of a growing set after reading nums[0..i]; suffix[i] is the size of a growing "
            "set built from the right after reading nums[i+1..]. Both arrays are computed in one pass each, and "
            "diff[i] = prefix[i] - suffix[i]. The brute force builds two fresh sets for every index."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^2) time - build the prefix set and the suffix set from scratch for every index",
        brute=r"""
# BRUTE FORCE: O(n^2) time - build the prefix set and the suffix set from scratch for every index
def distinct_difference_array(nums):
    return [len(set(nums[: i + 1])) - len(set(nums[i + 1 :])) for i in range(len(nums))]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Prefix and suffix distinct counts with running sets
def distinct_difference_array(nums):
    n = len(nums)
    suffix = [0] * (n + 1)
    seen = set()

    for i in range(n - 1, -1, -1):
        seen.add(nums[i])
        suffix[i] = len(seen)

    out = []
    seen = set()

    for i in range(n):
        seen.add(nums[i])
        out.append(len(seen) - suffix[i + 1])

    return out
""",
    ),
    # ---- Sort Array by Increasing Frequency (LeetCode 1636) ----
    dict(
        title="Sort Array by Increasing Frequency",
        diff="E",
        lc=1636,
        slug="sort-array-by-increasing-frequency",
        prompt=(
            "Sort nums by increasing frequency of the values. Values with the same frequency are sorted in "
            "DECREASING order. Return the sorted array."
        ),
        sig="def frequency_sort(nums: List[int]) -> List[int]:",
        fn="frequency_sort",
        tests=[
            (([1, 1, 2, 2, 2, 3],), [3, 1, 1, 2, 2, 2]),
            (([2, 3, 1, 3, 2],), [1, 3, 3, 2, 2]),
            (([-1, 1, -6, 4, 5, -6, 1, 4, 1],), [5, -1, 4, 4, -6, -6, 1, 1, 1]),
            (([7],), [7]),
        ],
        hints=[
            "You need each value's frequency before you can sort.",
            (
                "Python can sort by a tuple key: first criterion frequency ascending, second criterion the value "
                "descending."
            ),
            "key = (count[v], -v).",
        ],
        pattern="Frequency map + sort with a composite key",
        explain=(
            "A Counter provides the frequency in O(1); sorting the original list with key (frequency, -value) "
            "orders by frequency first and, for ties, by value descending because the negated value sorts "
            "ascending. The brute force recomputes frequencies with list.count inside the sort key."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2) time - list.count inside the sort key for every element",
        brute=r"""
# BRUTE FORCE: O(n^2) time - list.count inside the sort key for every element
def frequency_sort(nums):
    return sorted(nums, key=lambda v: (nums.count(v), -v))
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Frequency map + sort with a composite key
def frequency_sort(nums):
    counts = Counter(nums)
    return sorted(nums, key=lambda v: (counts[v], -v))
""",
    ),
]
