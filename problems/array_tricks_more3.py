"""extra batch of Array Tricks problems - the problem bank for the "array_tricks" topic (batch 3).

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
    # ---- Shortest Unsorted Continuous Subarray (LeetCode 581) ----
    dict(
        title="Shortest Unsorted Continuous Subarray",
        diff="M",
        lc=581,
        slug="shortest-unsorted-continuous-subarray",
        prompt=(
            "Find the shortest contiguous subarray that, if sorted in ascending order, makes the whole array "
            "sorted. Return its length (0 if the array is already sorted)."
        ),
        sig="def find_unsorted_subarray(nums: List[int]) -> int:",
        fn="find_unsorted_subarray",
        tests=[
            (([2, 6, 4, 8, 10, 9, 15],), 5),
            (([1, 2, 3, 4],), 0),
            (([1],), 0),
            (([2, 1],), 2),
            (([1, 3, 2, 2, 2],), 4),
            (([1, 2, 3, 3, 3],), 0),
        ],
        hints=[
            "Everything before the subarray and after it is already in its final place.",
            "The right end is the last index that is smaller than the maximum seen before it.",
            (
                "The left end is the first index that is larger than the minimum seen after it - scan from the "
                "right tracking the minimum."
            ),
        ],
        pattern="Two scans: running max from the left, running min from the right",
        explain=(
            "An element is out of place on the right side exactly when some earlier element is larger, i.e. it is "
            "smaller than the running maximum; the last such index is the right boundary. Symmetrically, an element "
            "is out of place on the left when it is larger than the running minimum of the suffix; the first such "
            "index is the left boundary. Both boundaries come from single linear scans."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^3 log n) time - try every subarray, sort it, test the whole array",
        brute=r"""
# BRUTE FORCE: O(n^3 log n) time - try every subarray, sort it, test the whole array
def find_unsorted_subarray(nums):
    n = len(nums)
    if nums == sorted(nums):
        return 0
    best = n
    for i in range(n):
        for j in range(i, n):
            trial = nums[:i] + sorted(nums[i : j + 1]) + nums[j + 1 :]
            if trial == sorted(nums):
                best = min(best, j - i + 1)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two scans: running max from the left, running min from the right
def find_unsorted_subarray(nums):
    n = len(nums)
    biggest, smallest = nums[0], nums[-1]
    start = end = -1
    for i in range(n):
        biggest = max(biggest, nums[i])
        if nums[i] < biggest:
            end = i
        j = n - 1 - i
        smallest = min(smallest, nums[j])
        if nums[j] > smallest:
            start = j
    return end - start + 1 if end != -1 else 0
""",
    ),
    # ---- Longest Continuous Increasing Subsequence (LeetCode 674) ----
    dict(
        title="Longest Continuous Increasing Subsequence",
        diff="E",
        lc=674,
        slug="longest-continuous-increasing-subsequence",
        prompt="Return the length of the longest contiguous strictly increasing run in nums.",
        sig="def find_length_of_lcis(nums: List[int]) -> int:",
        fn="find_length_of_lcis",
        tests=[
            (([1, 3, 5, 4, 7],), 3),
            (([2, 2, 2, 2, 2],), 1),
            (([1],), 1),
            (([1, 2, 3],), 3),
            (([3, 2, 1],), 1),
        ],
        hints=[
            "A run ends exactly where nums[i] <= nums[i-1].",
            "Keep the length of the run that ends at the current index.",
            "Extend it when nums[i] > nums[i-1], otherwise reset it to 1; track the maximum.",
        ],
        pattern="Single pass with a running run length",
        explain=(
            "Runs are contiguous, so the run ending at i depends only on whether nums[i] continues the run ending "
            "at i-1. One counter that either grows or resets covers every run in a single pass."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - extend a run from every start index",
        brute=r"""
# BRUTE FORCE: O(n^2) time - extend a run from every start index
def find_length_of_lcis(nums):
    best = 1
    for i in range(len(nums)):
        j = i
        while j + 1 < len(nums) and nums[j + 1] > nums[j]:
            j += 1
        best = max(best, j - i + 1)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Single pass with a running run length
def find_length_of_lcis(nums):
    best = run = 1
    for i in range(1, len(nums)):
        run = run + 1 if nums[i] > nums[i - 1] else 1
        best = max(best, run)
    return best
""",
    ),
    # ---- Valid Mountain Array (LeetCode 941) ----
    dict(
        title="Valid Mountain Array",
        diff="E",
        lc=941,
        slug="valid-mountain-array",
        prompt=(
            "Return True if arr is a mountain: it strictly increases to a peak and then strictly decreases, and "
            "both the climb and the descent are non-empty."
        ),
        sig="def valid_mountain_array(arr: List[int]) -> bool:",
        fn="valid_mountain_array",
        tests=[
            (([2, 1],), False),
            (([3, 5, 5],), False),
            (([0, 3, 2, 1],), True),
            (([0, 1, 2, 3],), False),
            (([3, 2, 1],), False),
            (([1, 3, 2],), True),
        ],
        hints=[
            "Walk up while the next value is larger.",
            "The place where you stop is the peak - it must not be the first or the last index.",
            "From the peak walk down while the next value is smaller; you must reach the end.",
        ],
        pattern="Two phases with one pointer",
        explain=(
            "A mountain is exactly: strictly up, then strictly down, with at least one step each way. Climb with "
            "one pointer, reject if it never moved or reached the end, then descend; the array is a mountain "
            "precisely when the descent consumes the rest. Equal neighbours stop both walks, so plateaus are "
            "rejected."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - try every index as the peak and check both sides",
        brute=r"""
# BRUTE FORCE: O(n^2) time - try every index as the peak and check both sides
def valid_mountain_array(arr):
    n = len(arr)
    for peak in range(1, n - 1):
        up = all(arr[i] < arr[i + 1] for i in range(peak))
        down = all(arr[i] > arr[i + 1] for i in range(peak, n - 1))
        if up and down:
            return True
    return False
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Two phases with one pointer
def valid_mountain_array(arr):
    n = len(arr)
    i = 0
    while i + 1 < n and arr[i] < arr[i + 1]:
        i += 1
    if i == 0 or i == n - 1:
        return False
    while i + 1 < n and arr[i] > arr[i + 1]:
        i += 1
    return i == n - 1
""",
    ),
    # ---- Rotate Function (LeetCode 396) ----
    dict(
        title="Rotate Function",
        diff="M",
        lc=396,
        slug="rotate-function",
        prompt=(
            "Rotate nums clockwise by k positions to get arr_k, and define F(k) = sum of i * arr_k[i]. Return the "
            "maximum of F(0), F(1), ..., F(n-1)."
        ),
        sig="def max_rotate_function(nums: List[int]) -> int:",
        fn="max_rotate_function",
        tests=[
            (([4, 3, 2, 6],), 26),
            (([100],), 0),
            (([1, 2],), 2),
            (([1, 2, 3],), 8),
            (([-1, -2, -3],), -5),
        ],
        hints=[
            "Computing every F(k) from scratch is O(n^2). How does F(k) relate to F(k-1)?",
            (
                "Rotating by one moves every element's index up by one (adding the total sum), except the last "
                "element, which drops from index n-1 to 0."
            ),
            "F(k) = F(k-1) + sum(nums) - n * nums[n-k].",
        ],
        pattern="Recurrence between consecutive rotations",
        explain=(
            "One more clockwise rotation raises the index of n-1 elements by one (adding the total sum to F) and "
            "sends the previous last element from index n-1 to index 0 (losing n * that element relative to the "
            "shifted sum). So each F(k) follows from F(k-1) in O(1)."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - rebuild every rotation and recompute the weighted sum",
        brute=r"""
# BRUTE FORCE: O(n^2) time - rebuild every rotation and recompute the weighted sum
def max_rotate_function(nums):
    n = len(nums)
    best = None
    for k in range(n):
        rotated = nums[n - k :] + nums[: n - k]
        value = sum(i * x for i, x in enumerate(rotated))
        best = value if best is None else max(best, value)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Recurrence between consecutive rotations
def max_rotate_function(nums):
    n, total = len(nums), sum(nums)
    current = sum(i * x for i, x in enumerate(nums))
    best = current
    for k in range(1, n):
        current += total - n * nums[n - k]
        best = max(best, current)
    return best
""",
    ),
    # ---- Minimum Moves to Equal Array Elements (LeetCode 453) ----
    dict(
        title="Minimum Moves to Equal Array Elements",
        diff="M",
        lc=453,
        slug="minimum-moves-to-equal-array-elements",
        prompt=(
            "In one move you add 1 to n - 1 of the elements (all but one). Return the minimum number of moves to "
            "make all elements equal."
        ),
        sig="def min_moves(nums: List[int]) -> int:",
        fn="min_moves",
        tests=[
            (([1, 2, 3],), 3),
            (([1, 1, 1],), 0),
            (([1],), 0),
            (([1, 100],), 99),
            (([5, 6, 8, 8, 5],), 7),
        ],
        hints=[
            (
                "Raising n-1 elements by 1 changes only the DIFFERENCES between the elements in one way: it is "
                "equivalent to lowering one element by 1."
            ),
            "So the task becomes: lower elements by 1 per move until all equal - they will all meet at the minimum.",
            "Answer = sum(nums) - n * min(nums).",
        ],
        pattern="Change of viewpoint: relative differences",
        explain=(
            "Adding 1 to everything except x keeps all pairwise differences the same as subtracting 1 from x alone "
            "(then adding 1 to everyone changes nothing about equality). So each move is 'decrease one element by "
            "1', and the cheapest common value is the minimum, costing sum(nums) - n * min(nums)."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(sum - n * min) moves - literally simulate: add 1 to all but the current maximum",
        brute=r"""
# BRUTE FORCE: O(sum - n * min) moves - literally simulate: add 1 to all but the current maximum
def min_moves(nums):
    nums = list(nums)
    moves = 0
    while min(nums) != max(nums):
        top = nums.index(max(nums))
        nums = [x + 1 if i != top else x for i, x in enumerate(nums)]
        moves += 1
    return moves
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Change of viewpoint: relative differences
def min_moves(nums):
    return sum(nums) - len(nums) * min(nums)
""",
    ),
    # ---- Minimum Moves to Equal Array Elements II (LeetCode 462) ----
    dict(
        title="Minimum Moves to Equal Array Elements II",
        diff="M",
        lc=462,
        slug="minimum-moves-to-equal-array-elements-ii",
        prompt=(
            "In one move you add 1 to or subtract 1 from a single element. Return the minimum number of moves to "
            "make all elements equal."
        ),
        sig="def min_moves2(nums: List[int]) -> int:",
        fn="min_moves2",
        tests=[
            (([1, 2, 3],), 2),
            (([1, 10, 2, 9],), 16),
            (([1],), 0),
            (([1, 1, 1],), 0),
            (([-3, 4],), 7),
        ],
        hints=[
            "The meeting value minimises the sum of absolute distances.",
            "Moving the target up by 1 helps the elements below it and hurts the ones above it.",
            "The best target is the median; the cost is the sum of |x - median|.",
        ],
        pattern="Median minimises the sum of absolute deviations",
        explain=(
            "f(t) = sum |x - t| is convex and piecewise linear; its slope is (#elements <= t) - (#elements > t), "
            "which changes sign at the median. Any median (middle element after sorting) is optimal."
        ),
        cx="O(n log n) time, O(1) extra space",
        brute_cx="O(n * range) time - try every target between min and max",
        brute=r"""
# BRUTE FORCE: O(n * range) time - try every target between min and max
def min_moves2(nums):
    best = None
    for target in range(min(nums), max(nums) + 1):
        cost = sum(abs(x - target) for x in nums)
        best = cost if best is None else min(best, cost)
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(1) extra space
# Idea: Median minimises the sum of absolute deviations
def min_moves2(nums):
    ordered = sorted(nums)
    median = ordered[len(ordered) // 2]
    return sum(abs(x - median) for x in ordered)
""",
    ),
    # ---- Array Nesting (LeetCode 565) ----
    dict(
        title="Array Nesting",
        diff="M",
        lc=565,
        slug="array-nesting",
        prompt=(
            "nums is a permutation of 0..n-1. For each start index i build the set s(i) = {nums[i], nums[nums[i]], "
            "...} and stop just before a value repeats. Return the maximum size of any s(i)."
        ),
        sig="def array_nesting(nums: List[int]) -> int:",
        fn="array_nesting",
        tests=[
            (([5, 4, 0, 3, 1, 6, 2],), 4),
            (([0, 1, 2],), 1),
            (([1, 0],), 2),
            (([0],), 1),
            (([1, 2, 0],), 3),
        ],
        hints=[
            "Follow i -> nums[i] -> nums[nums[i]] ...: in a permutation every chain closes into a cycle.",
            "Every element belongs to exactly one cycle, and starting anywhere on a cycle gives the same set.",
            "Walk each cycle once, marking visited elements, and track the longest cycle.",
        ],
        pattern="Cycles of a permutation, visit each once",
        explain=(
            "A permutation splits into disjoint cycles. The set s(i) is the cycle containing i, so its size is the "
            "cycle length. Marking elements as visited ensures each cycle is walked once, giving O(n) total instead "
            "of re-walking a cycle from each of its elements."
        ),
        cx="O(n) time, O(n) space (or O(1) if the input may be modified)",
        brute_cx="O(n^2) time - walk the chain from every start without remembering visited elements",
        brute=r"""
# BRUTE FORCE: O(n^2) time - walk the chain from every start without remembering visited elements
def array_nesting(nums):
    best = 0
    for start in range(len(nums)):
        seen = set()
        i = start
        while nums[i] not in seen:
            seen.add(nums[i])
            i = nums[i]
        best = max(best, len(seen))
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space (or O(1) if the input may be modified)
# Idea: Cycles of a permutation, visit each once
def array_nesting(nums):
    visited = [False] * len(nums)
    best = 0
    for start in range(len(nums)):
        length, i = 0, start
        while not visited[i]:
            visited[i] = True
            i = nums[i]
            length += 1
        best = max(best, length)
    return best
""",
    ),
    # ---- Max Chunks To Make Sorted II (LeetCode 768) ----
    dict(
        title="Max Chunks To Make Sorted II",
        diff="H",
        lc=768,
        slug="max-chunks-to-make-sorted-ii",
        prompt=(
            "arr is any integer array (duplicates allowed). Split it into the most contiguous chunks such that "
            "sorting each chunk separately and concatenating gives the sorted array. Return the number of chunks."
        ),
        sig="def max_chunks_to_sorted_ii(arr: List[int]) -> int:",
        fn="max_chunks_to_sorted_ii",
        tests=[
            (([5, 4, 3, 2, 1],), 1),
            (([2, 1, 3, 4, 4],), 4),
            (([1],), 1),
            (([1, 1, 1],), 3),
            (([2, 2, 1],), 1),
            (([1, 0, 1, 3, 2],), 3),
        ],
        hints=[
            "A cut after index i is safe when every element on the left is <= every element on the right.",
            "That means max(prefix) <= min(suffix). Duplicates are fine because equal values may sit on both sides.",
            (
                "Precompute suffix minimums, sweep with a running prefix maximum, and count the cut points (plus "
                "the final chunk)."
            ),
        ],
        pattern="Prefix max vs suffix min",
        explain=(
            "After sorting, all of the left chunk's elements must be no larger than anything to its right, so a cut "
            "is valid exactly when max of the prefix <= min of the suffix. Every valid cut is independent of the "
            "others, so counting all of them (the end of the array always counts) gives the maximum number of "
            "chunks."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(2^n * n log n) time - try every set of cut positions",
        brute=r"""
# BRUTE FORCE: O(2^n * n log n) time - try every set of cut positions
def max_chunks_to_sorted_ii(arr):
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
# OPTIMISED: O(n) time, O(n) space
# Idea: Prefix max vs suffix min
def max_chunks_to_sorted_ii(arr):
    n = len(arr)
    suffix_min = [float("inf")] * (n + 1)
    for i in range(n - 1, -1, -1):
        suffix_min[i] = min(arr[i], suffix_min[i + 1])
    chunks, prefix_max = 0, float("-inf")
    for i in range(n):
        prefix_max = max(prefix_max, arr[i])
        if prefix_max <= suffix_min[i + 1]:
            chunks += 1
    return chunks
""",
    ),
    # ---- Partition Array into Disjoint Intervals (LeetCode 915) ----
    dict(
        title="Partition Array into Disjoint Intervals",
        diff="M",
        lc=915,
        slug="partition-array-into-disjoint-intervals",
        prompt=(
            "Split nums into a left part and a right part (both non-empty) so that every element of the left is <= "
            "every element of the right and the left is as short as possible. Return the left length."
        ),
        sig="def partition_disjoint(nums: List[int]) -> int:",
        fn="partition_disjoint",
        tests=[
            (([5, 0, 3, 8, 6],), 3),
            (([1, 1, 1, 0, 6, 12],), 4),
            (([1, 1],), 1),
            (([1, 2],), 1),
            (([3, 1, 2, 5],), 3),
        ],
        hints=[
            "A split at k is valid when max(nums[:k]) <= min(nums[k:]).",
            "Trying every k and recomputing max/min is O(n^2); precomputing prefix max and suffix min makes it O(n).",
            (
                "One pass: keep the max of the left part and the overall max; when you see a value smaller than the "
                "left max, the left part must grow to include it."
            ),
        ],
        pattern="Running maximum with a movable boundary",
        explain=(
            "Start with the left part = first element. Any later element smaller than the left part's max can't "
            "stay on the right, so the left must extend to that index (and the left max becomes the max seen so "
            "far). Elements >= the left max never force an extension. The final boundary is the shortest valid "
            "split."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n^2) time - try every split and recompute max/min",
        brute=r"""
# BRUTE FORCE: O(n^2) time - try every split and recompute max/min
def partition_disjoint(nums):
    for k in range(1, len(nums)):
        if max(nums[:k]) <= min(nums[k:]):
            return k
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Running maximum with a movable boundary
def partition_disjoint(nums):
    left_max = overall_max = nums[0]
    boundary = 1
    for i in range(1, len(nums)):
        overall_max = max(overall_max, nums[i])
        if nums[i] < left_max:
            left_max = overall_max
            boundary = i + 1
    return boundary
""",
    ),
    # ---- Degree of an Array (LeetCode 697) ----
    dict(
        title="Degree of an Array",
        diff="E",
        lc=697,
        slug="degree-of-an-array",
        prompt=(
            "The degree of an array is the highest frequency of any value. Return the length of the shortest "
            "contiguous subarray of nums that has the same degree as nums."
        ),
        sig="def find_shortest_sub_array(nums: List[int]) -> int:",
        fn="find_shortest_sub_array",
        tests=[
            (([1, 2, 2, 3, 1],), 2),
            (([1, 2, 2, 3, 1, 4, 2],), 6),
            (([1],), 1),
            (([1, 1, 2, 2],), 2),
            (([1, 2, 3],), 1),
        ],
        hints=[
            (
                "The subarray must contain all occurrences of some most-frequent value, so it is bounded by that "
                "value's first and last position."
            ),
            "Record count, first index and last index for each value.",
            "Among the values with maximum count, take the smallest last - first + 1.",
        ],
        pattern="Hash map of (count, first, last)",
        explain=(
            "A subarray with the full degree must hold at least `degree` copies of one value, hence it spans from "
            "that value's first to last occurrence. Using exactly that span is enough, so the answer is the minimum "
            "span over all values reaching the maximum frequency."
        ),
        cx="O(n) time, O(n) space",
        brute_cx="O(n^3) time - compute the degree of every subarray",
        brute=r"""
# BRUTE FORCE: O(n^3) time - compute the degree of every subarray
def find_shortest_sub_array(nums):
    degree = max(Counter(nums).values())
    best = len(nums)
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            if max(Counter(nums[i : j + 1]).values()) == degree:
                best = min(best, j - i + 1)
    return best
""",
        solution=r"""
# OPTIMISED: O(n) time, O(n) space
# Idea: Hash map of (count, first, last)
def find_shortest_sub_array(nums):
    first, last, count = {}, {}, Counter()
    for i, x in enumerate(nums):
        first.setdefault(x, i)
        last[x] = i
        count[x] += 1
    degree = max(count.values())
    return min(last[x] - first[x] + 1 for x in count if count[x] == degree)
""",
    ),
    # ---- 1-bit and 2-bit Characters (LeetCode 717) ----
    dict(
        title="1-bit and 2-bit Characters",
        diff="E",
        lc=717,
        slug="1-bit-and-2-bit-characters",
        prompt=(
            "Characters are encoded as '0' (one bit) or '10' / '11' (two bits). bits always ends with 0. Return "
            "True if the last character must be the one-bit character '0'."
        ),
        sig="def is_one_bit_character(bits: List[int]) -> bool:",
        fn="is_one_bit_character",
        tests=[
            (([1, 0, 0],), True),
            (([1, 1, 1, 0],), False),
            (([0],), True),
            (([1, 0],), False),
            (([0, 0],), True),
            (([1, 1, 0],), True),
        ],
        hints=[
            (
                "The decoding is unambiguous: a leading 1 always starts a 2-bit character, a leading 0 is a 1-bit "
                "character."
            ),
            "So you can simply walk the bits and jump 1 or 2 positions.",
            "If the walk lands exactly on the last index, the final 0 stands alone.",
        ],
        pattern="Deterministic left-to-right parsing",
        explain=(
            "Because a 1 always opens a 2-bit character and a 0 is complete by itself, there is exactly one way to "
            "split the stream. Walk it: advance 2 on a 1, 1 on a 0. The last bit is a 1-bit character exactly when "
            "the walk arrives on it (equivalently, the number of consecutive 1s right before it is even)."
        ),
        cx="O(n) time, O(1) space",
        brute_cx="O(n) time and space - dynamic programming over 'is this prefix a valid decoding?'",
        brute=r"""
# BRUTE FORCE: O(n) time and space - dynamic programming over 'is this prefix a valid decoding?'
def is_one_bit_character(bits):
    n = len(bits)
    valid = [False] * n
    valid[0] = True
    for i in range(1, n):
        one = bits[i - 1] == 0 and valid[i - 1]
        two = i >= 2 and bits[i - 2] == 1 and valid[i - 2]
        valid[i] = one or two
    return valid[n - 1]
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) space
# Idea: Deterministic left-to-right parsing
def is_one_bit_character(bits):
    i = 0
    while i < len(bits) - 1:
        i += bits[i] + 1
    return i == len(bits) - 1
""",
    ),
    # ---- Positions of Large Groups (LeetCode 830) ----
    dict(
        title="Positions of Large Groups",
        diff="E",
        lc=830,
        slug="positions-of-large-groups",
        prompt=(
            "A group is a maximal run of the same character in s. Return the [start, end] index pairs of all groups "
            "of length 3 or more, in increasing order of start."
        ),
        sig="def large_group_positions(s: str) -> List[List[int]]:",
        fn="large_group_positions",
        tests=[
            (("abbxxxxzzy",), [[3, 6]]),
            (("abc",), []),
            (("abcdddeeeeaabbbcd",), [[3, 5], [6, 9], [12, 14]]),
            (("aaa",), [[0, 2]]),
            (("a",), []),
        ],
        hints=[
            "Groups are consecutive runs - one left-to-right scan is enough.",
            "Keep the start of the current run; when the character changes (or the string ends) close the run.",
            "Record [start, i - 1] if the run length i - start is at least 3.",
        ],
        pattern="Run-length scan",
        explain=(
            "Each run ends exactly where the next character differs (or at the end of the string). Tracking the "
            "start of the current run gives its length when it closes, so every group is examined once."
        ),
        cx="O(n) time, O(1) extra space",
        brute_cx="O(n^3) time - test every substring for being a maximal run of one character",
        brute=r"""
# BRUTE FORCE: O(n^3) time - test every substring for being a maximal run of one character
def large_group_positions(s):
    n = len(s)
    out = []
    for i in range(n):
        for j in range(i + 2, n):
            same = all(s[k] == s[i] for k in range(i, j + 1))
            left_ok = i == 0 or s[i - 1] != s[i]
            right_ok = j == n - 1 or s[j + 1] != s[j]
            if same and left_ok and right_ok:
                out.append([i, j])
    return out
""",
        solution=r"""
# OPTIMISED: O(n) time, O(1) extra space
# Idea: Run-length scan
def large_group_positions(s):
    out = []
    start = 0
    for i in range(1, len(s) + 1):
        if i == len(s) or s[i] != s[start]:
            if i - start >= 3:
                out.append([start, i - 1])
            start = i
    return out
""",
    ),
]
