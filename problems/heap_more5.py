"""extra batch of Heap / Priority Queue problems - the problem bank for the "heap" topic (batch 5).

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

from functools import lru_cache


@lru_cache(None)
def _happy_len(counts, last, run):
    """Longest valid continuation: counts left per letter, last letter index and how many times in a row."""
    best = 0
    for i in range(3):
        if counts[i] == 0 or (i == last and run == 2):
            continue
        nxt = list(counts)
        nxt[i] -= 1
        best = max(best, 1 + _happy_len(tuple(nxt), i, run + 1 if i == last else 1))
    return best


def _happy_ok(args, got):
    """True if `got` uses only a, b, c within their limits, has no triple repeat and is as long as possible."""
    if not isinstance(got, str) or set(got) - set("abc"):
        return False
    if any(got.count(ch) > n for ch, n in zip("abc", args)) or any(ch * 3 in got for ch in "abc"):
        return False
    return len(got) == _happy_len(tuple(args), -1, 0)


def _top_k_ok(args, got):
    """True if `got` is a subsequence of nums of length k whose sum equals the sum of the k largest values."""
    nums, k = args
    if not isinstance(got, list) or len(got) != k or sum(got) != sum(sorted(nums)[-k:]):
        return False
    rest = iter(nums)
    return all(x in rest for x in got)


def _barcodes_ok(args, got):
    """True if `got` rearranges the barcodes so that no two neighbours are equal."""
    return (
        isinstance(got, list)
        and sorted(got) == sorted(args[0])
        and all(got[i] != got[i + 1] for i in range(len(got) - 1))
    )


PROBLEMS = [
    # ---- Longest Happy String (LeetCode 1405) ----
    dict(
        title="Longest Happy String",
        diff="M",
        lc=1405,
        slug="longest-happy-string",
        prompt=(
            "A string is happy if it uses only 'a', 'b', 'c' and has no 'aaa', 'bbb' or 'ccc'. Given a, b, c as the "
            "maximum number of times each letter may be used, return any longest happy string (empty if none)."
        ),
        sig="def longest_diverse_string(a: int, b: int, c: int) -> str:",
        fn="longest_diverse_string",
        check=_happy_ok,
        tests=[
            ((1, 1, 7), "ccaccbcc"),
            ((7, 1, 0), "aabaa"),
            ((0, 0, 0), ""),
            ((2, 2, 1), "aabbc"),
            ((1, 0, 0), "a"),
        ],
        hints=[
            "Greedy: always append the letter with the most copies left - unless that would make three in a row.",
            "Keep the letters in a max-heap keyed by remaining count.",
            (
                "If the top letter would be a third repeat, use the SECOND most frequent letter once instead (if "
                "none is left, stop), then put the top letter back."
            ),
        ],
        pattern="Greedy with a max-heap, falling back to the runner-up to break a triple",
        explain=(
            "Spending the most plentiful letter first keeps the other letters available as separators for as long "
            "as possible. When the leader would form a triple, a single copy of the runner-up breaks the run; if "
            "there is no runner-up the string cannot be extended and the result is already maximal. The heap "
            "returns the leader each step in O(log 3)."
        ),
        cx="O(a + b + c) time, O(1) extra space",
        brute_cx=(
            "exponential in the worst case - search every valid continuation (memoised on counts, last letter, run)"
        ),
        brute=r"""
# BRUTE FORCE: exponential in the worst case - search every valid continuation (memoised on counts, last letter, run)
def longest_diverse_string(a, b, c):
    @lru_cache(None)
    def best(counts, last, run):
        result = ""

        for i, ch in enumerate("abc"):
            if counts[i] == 0 or (i == last and run == 2):
                continue
            nxt = list(counts)
            nxt[i] -= 1
            candidate = ch + best(tuple(nxt), i, run + 1 if i == last else 1)
            if len(candidate) > len(result):
                result = candidate

        return result

    return best((a, b, c), -1, 0)
""",
        solution=r"""
# OPTIMISED: O(a + b + c) time, O(1) extra space
# Idea: Greedy with a max-heap, falling back to the runner-up to break a triple
def longest_diverse_string(a, b, c):
    heap = [(-count, ch) for count, ch in ((a, "a"), (b, "b"), (c, "c")) if count > 0]
    heapq.heapify(heap)
    out = []

    while heap:
        count, ch = heapq.heappop(heap)

        if len(out) >= 2 and out[-1] == out[-2] == ch:
            if not heap:
                break
            count2, ch2 = heapq.heappop(heap)
            out.append(ch2)
            if count2 + 1 < 0:
                heapq.heappush(heap, (count2 + 1, ch2))
            heapq.heappush(heap, (count, ch))
        else:
            out.append(ch)
            if count + 1 < 0:
                heapq.heappush(heap, (count + 1, ch))

    return "".join(out)
""",
    ),
    # ---- Jump Game VI (LeetCode 1696) ----
    dict(
        title="Jump Game VI",
        diff="M",
        lc=1696,
        slug="jump-game-vi",
        prompt=(
            "Start at index 0 of nums. From index i you may jump to any index in [i + 1, min(n - 1, i + k)]. Your "
            "score is the sum of nums at every index you visit (including 0 and n - 1). Return the maximum score "
            "when you reach the last index."
        ),
        sig="def max_result(nums: List[int], k: int) -> int:",
        fn="max_result",
        tests=[
            (([1, -1, -2, 4, -7, 3], 2), 7),
            (([10, -5, -2, 4, 0, 3], 3), 17),
            (([1, -5, -20, 4, -1, 3, -6, -3], 2), 0),
            (([5], 3), 5),
            (([-3, -2], 1), -5),
        ],
        hints=[
            "dp[i] = nums[i] + max(dp[j]) over the k indices j just before i.",
            "Scanning the window takes O(k) per index. You only need the MAXIMUM of a sliding window of dp values.",
            (
                "Keep a max-heap of (dp value, index); before reading it, pop tops whose index is older than i - k "
                "(lazy deletion)."
            ),
        ],
        pattern="DP + sliding-window maximum (heap with lazy deletion, or a monotonic deque)",
        explain=(
            "The best score reaching i comes from the best score among the k previous positions. A max-heap of (dp, "
            "index) exposes that maximum in O(1); stale entries (index < i - k) are discarded when they reach the "
            "top. Each index is pushed and popped at most once."
        ),
        cx="O(n log n) time, O(n) space (O(n) with a monotonic deque)",
        brute_cx="O(n * k) time - scan the previous k scores for every index",
        brute=r"""
# BRUTE FORCE: O(n * k) time - scan the previous k scores for every index
def max_result(nums, k):
    dp = [0] * len(nums)
    dp[0] = nums[0]
    for i in range(1, len(nums)):
        dp[i] = nums[i] + max(dp[max(0, i - k) : i])
    return dp[-1]
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space (O(n) with a monotonic deque)
# Idea: DP + sliding-window maximum (heap with lazy deletion, or a monotonic deque)
def max_result(nums, k):
    heap = [(-nums[0], 0)]
    score = nums[0]

    for i in range(1, len(nums)):
        while heap[0][1] < i - k:
            heapq.heappop(heap)
        score = nums[i] - heap[0][0]
        heapq.heappush(heap, (-score, i))

    return score
""",
    ),
    # ---- Maximum Average Pass Ratio (LeetCode 1792) ----
    dict(
        title="Maximum Average Pass Ratio",
        diff="M",
        lc=1792,
        slug="maximum-average-pass-ratio",
        prompt=(
            "classes[i] = [pass, total] is how many students pass out of how many are in class i. You may place "
            "extraStudents new students (who all pass) into any classes. Return the maximum possible average of the "
            "classes' pass ratios (answers within 1e-5 are accepted)."
        ),
        sig="def max_average_ratio(classes: List[List[int]], extraStudents: int) -> float:",
        fn="max_average_ratio",
        compare="float",
        tests=[
            (([[1, 2], [3, 5], [2, 2]], 2), 0.7833333333333333),
            (([[2, 4], [3, 9], [4, 5], [2, 10]], 4), 0.5348484848484849),
            (([[1, 1]], 3), 1.0),
            (([[1, 2]], 1), 0.6666666666666666),
        ],
        hints=[
            "Adding one passing student to a class with p/t raises its ratio by (p+1)/(t+1) - p/t.",
            (
                "That gain shrinks as a class grows (diminishing returns), so a student should go where the CURRENT "
                "gain is largest."
            ),
            (
                "Max-heap on the gain: pop the class with the biggest gain, add a student, recompute its gain, push "
                "it back; repeat extraStudents times."
            ),
        ],
        pattern="Greedy on marginal gain with a max-heap (diminishing returns)",
        explain=(
            "The gain from the next student in a class strictly decreases as the class grows, so the objective is a "
            "sum of concave pieces and assigning each student to the largest current marginal gain is optimal. A "
            "heap keyed by the negative gain finds that class in O(log n); only the chosen class's gain changes."
        ),
        cx="O((n + e) log n) time, O(n) space",
        brute_cx="exponential - try every way to split the extra students among the classes",
        brute=r"""
# BRUTE FORCE: exponential - try every way to split the extra students among the classes
def max_average_ratio(classes, extraStudents):
    def best(i, left):
        p, t = classes[i]
        if i == len(classes) - 1:
            return (p + left) / (t + left)
        return max((p + x) / (t + x) + best(i + 1, left - x) for x in range(left + 1))

    return best(0, extraStudents) / len(classes)
""",
        solution=r"""
# OPTIMISED: O((n + e) log n) time, O(n) space
# Idea: Greedy on marginal gain with a max-heap (diminishing returns)
def max_average_ratio(classes, extraStudents):
    def gain(p, t):
        return (p + 1) / (t + 1) - p / t

    heap = [(-gain(p, t), p, t) for p, t in classes]
    heapq.heapify(heap)

    for _ in range(extraStudents):
        _, p, t = heapq.heappop(heap)
        p, t = p + 1, t + 1
        heapq.heappush(heap, (-gain(p, t), p, t))

    return sum(p / t for _, p, t in heap) / len(classes)
""",
    ),
    # ---- Maximum Product After K Increments (LeetCode 2233) ----
    dict(
        title="Maximum Product After K Increments",
        diff="M",
        lc=2233,
        slug="maximum-product-after-k-increments",
        prompt=(
            "In one operation you add 1 to any element of nums. Do at most k operations and return the maximum "
            "possible product of all elements, modulo 1_000_000_007."
        ),
        sig="def maximum_product(nums: List[int], k: int) -> int:",
        fn="maximum_product",
        tests=[
            (([0, 4], 5), 20),
            (([6, 3, 3, 2], 2), 216),
            (([5], 3), 8),
            (([1, 1], 0), 1),
        ],
        hints=[
            "For a fixed sum, a product is largest when the factors are as equal as possible.",
            "So each increment should go to the current smallest element.",
            "Use a min-heap: pop the smallest, add 1, push it back, k times; then multiply everything mod 1e9+7.",
        ],
        pattern="Greedy on the minimum with a min-heap",
        explain=(
            "Increasing the smallest factor raises the product by the largest relative amount (x -> x+1 multiplies "
            "the product by (x+1)/x, which is biggest for small x). Repeating that k times keeps the multiset as "
            "level as possible, which maximises the product."
        ),
        cx="O((n + k) log n) time, O(n) space",
        brute_cx="exponential - try every way to place the k increments",
        brute=r"""
# BRUTE FORCE: exponential - try every way to place the k increments
def maximum_product(nums, k):
    def best(arr, left):
        if left == 0:
            product = 1
            for x in arr:
                product *= x
            return product
        return max(best(arr[:i] + [arr[i] + 1] + arr[i + 1 :], left - 1) for i in range(len(arr)))

    return best(list(nums), k) % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O((n + k) log n) time, O(n) space
# Idea: Greedy on the minimum with a min-heap
def maximum_product(nums, k):
    heap = list(nums)
    heapq.heapify(heap)

    for _ in range(k):
        heapq.heappush(heap, heapq.heappop(heap) + 1)

    product = 1

    for x in heap:
        product = product * x % (10**9 + 7)

    return product
""",
    ),
    # ---- Total Cost to Hire K Workers (LeetCode 2462) ----
    dict(
        title="Total Cost to Hire K Workers",
        diff="M",
        lc=2462,
        slug="total-cost-to-hire-k-workers",
        prompt=(
            "Hire k workers in k rounds. In each round look at the first `candidates` and the last `candidates` "
            "workers still unhired and hire the cheapest one (smallest index on ties). Return the total cost."
        ),
        sig="def total_cost(costs: List[int], k: int, candidates: int) -> int:",
        fn="total_cost",
        tests=[
            (([17, 12, 10, 2, 7, 2, 11, 20, 8], 3, 4), 11),
            (([1, 2, 4, 1], 3, 3), 4),
            (([5], 1, 1), 5),
            (([3, 3, 3, 3], 2, 1), 6),
        ],
        hints=[
            (
                "Only workers in the left window or the right window are eligible; the middle is untouched until "
                "the windows move."
            ),
            "Use two min-heaps: one for the left window, one for the right window.",
            (
                "Hire from the heap with the smaller top (left wins ties). Then refill that heap with the next "
                "unseen worker from its side, taking care that the windows never overlap."
            ),
        ],
        pattern="Two heaps for two sliding ends",
        explain=(
            "The eligible set is always 'the cheapest of the left window and the cheapest of the right window'. Two "
            "min-heaps expose both minima; after hiring, the next worker from the same side enters its heap. "
            "Initial windows are built so no worker sits in both heaps, and when the unseen middle runs out nothing "
            "more is pushed."
        ),
        cx="O((k + candidates) log candidates) time, O(candidates) space",
        brute_cx="O(k * n) time - rebuild the eligible set and scan it each round",
        brute=r"""
# BRUTE FORCE: O(k * n) time - rebuild the eligible set and scan it each round
def total_cost(costs, k, candidates):
    workers = list(costs)
    total = 0

    for _ in range(k):
        n = len(workers)
        eligible = set(range(min(candidates, n))) | set(range(max(0, n - candidates), n))
        pick = min(eligible, key=lambda i: (workers[i], i))
        total += workers.pop(pick)

    return total
""",
        solution=r"""
# OPTIMISED: O((k + candidates) log candidates) time, O(candidates) space
# Idea: Two heaps for two sliding ends
def total_cost(costs, k, candidates):
    n = len(costs)
    left = costs[:candidates]
    right = costs[max(candidates, n - candidates) :]
    heapq.heapify(left)
    heapq.heapify(right)
    i, j = candidates, max(candidates, n - candidates) - 1
    total = 0

    for _ in range(k):
        if not right or (left and left[0] <= right[0]):
            total += heapq.heappop(left)
            if i <= j:
                heapq.heappush(left, costs[i])
                i += 1
        else:
            total += heapq.heappop(right)
            if i <= j:
                heapq.heappush(right, costs[j])
                j -= 1

    return total
""",
    ),
    # ---- Maximum Subsequence Score (LeetCode 2542) ----
    dict(
        title="Maximum Subsequence Score",
        diff="M",
        lc=2542,
        slug="maximum-subsequence-score",
        prompt=(
            "Choose k indices. The score is (sum of nums1 at those indices) * (minimum of nums2 at those indices). "
            "Return the maximum score."
        ),
        sig="def max_score(nums1: List[int], nums2: List[int], k: int) -> int:",
        fn="max_score",
        tests=[
            (([1, 3, 3, 2], [2, 1, 3, 4], 3), 12),
            (([4, 2, 3, 1, 1], [7, 5, 10, 9, 6], 1), 30),
            (([5], [3], 1), 15),
            (([1, 1], [1, 1], 2), 2),
        ],
        hints=[
            "The minimum of nums2 is a hard-to-handle coupling. Fix it: suppose the minimum is nums2[i].",
            (
                "Sort indices by nums2 in DESCENDING order. When you reach i, every index processed so far has "
                "nums2 >= nums2[i], so nums2[i] is the minimum of any chosen set that includes i."
            ),
            (
                "Among those, maximise the sum of nums1: keep the k largest nums1 values seen so far in a min-heap "
                "and their running sum."
            ),
        ],
        pattern="Sort by one key, heap for the best k of the other",
        explain=(
            "After sorting by nums2 descending, the current nums2 value is automatically the minimum of any set "
            "drawn from the prefix. The best such set takes the k largest nums1 in the prefix. A size-k min-heap "
            "maintains that set and its sum as the prefix grows; the answer is the best (sum * current nums2) over "
            "positions where the heap holds k values."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(C(n, k) * k) time - evaluate every k-subset",
        brute=r"""
# BRUTE FORCE: O(C(n, k) * k) time - evaluate every k-subset
def max_score(nums1, nums2, k):
    best = 0
    for chosen in itertools.combinations(range(len(nums1)), k):
        best = max(best, sum(nums1[i] for i in chosen) * min(nums2[i] for i in chosen))
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Sort by one key, heap for the best k of the other
def max_score(nums1, nums2, k):
    heap = []
    total = best = 0

    for b, a in sorted(zip(nums2, nums1), reverse=True):
        heapq.heappush(heap, a)
        total += a
        if len(heap) > k:
            total -= heapq.heappop(heap)
        if len(heap) == k:
            best = max(best, total * b)

    return best
""",
    ),
    # ---- Maximum Performance of a Team (LeetCode 1383) ----
    dict(
        title="Maximum Performance of a Team",
        diff="H",
        lc=1383,
        slug="maximum-performance-of-a-team",
        prompt=(
            "Engineer i has speed[i] and efficiency[i]. Pick at most k engineers. The performance of a team is (sum "
            "of speeds) * (minimum efficiency). Return the maximum performance modulo 1_000_000_007."
        ),
        sig="def max_performance(n: int, speed: List[int], efficiency: List[int], k: int) -> int:",
        fn="max_performance",
        tests=[
            ((6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 2), 60),
            ((6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 3), 68),
            ((6, [2, 10, 3, 1, 5, 8], [5, 4, 3, 9, 7, 2], 4), 72),
            ((3, [2, 8, 2], [2, 7, 1], 2), 56),
            ((1, [5], [4], 1), 20),
        ],
        hints=[
            "Fix the minimum efficiency: process engineers in decreasing order of efficiency.",
            (
                "When engineer e is added, everyone already added is at least as efficient, so e's efficiency is "
                "the team minimum."
            ),
            (
                "Among the engineers seen so far keep the k fastest (min-heap of speeds + running sum); candidate "
                "performance = sum * current efficiency. Take the best candidate, reduce mod only at the end."
            ),
        ],
        pattern="Sort by efficiency desc + min-heap of the top-k speeds",
        explain=(
            "This is the same trick as Maximum Subsequence Score: sorting by the 'min' attribute makes the current "
            "value the minimum for any team built from the prefix, and the best team of size <= k from the prefix "
            "is its k fastest engineers. Taking the maximum over all prefixes covers every possible minimum. Do the "
            "maximisation with exact integers and apply the modulus once at the end."
        ),
        cx="O(n log n) time, O(k) space",
        brute_cx="O(2^n) time - evaluate every team of at most k engineers",
        brute=r"""
# BRUTE FORCE: O(2^n) time - evaluate every team of at most k engineers
def max_performance(n, speed, efficiency, k):
    best = 0
    for size in range(1, k + 1):
        for team in itertools.combinations(range(n), size):
            best = max(best, sum(speed[i] for i in team) * min(efficiency[i] for i in team))
    return best % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(k) space
# Idea: Sort by efficiency desc + min-heap of the top-k speeds
def max_performance(n, speed, efficiency, k):
    heap = []
    total = best = 0

    for eff, spd in sorted(zip(efficiency, speed), reverse=True):
        heapq.heappush(heap, spd)
        total += spd
        if len(heap) > k:
            total -= heapq.heappop(heap)
        best = max(best, total * eff)

    return best % (10**9 + 7)
""",
    ),
    # ---- Find Subsequence of Length K With the Largest Sum (LeetCode 2099) ----
    dict(
        title="Find Subsequence of Length K With the Largest Sum",
        diff="E",
        lc=2099,
        slug="find-subsequence-of-length-k-with-the-largest-sum",
        prompt=(
            "Return a subsequence of nums (elements in their original order) of length k that has the largest "
            "possible sum. Any such subsequence is accepted."
        ),
        sig="def max_subsequence(nums: List[int], k: int) -> List[int]:",
        fn="max_subsequence",
        check=_top_k_ok,
        tests=[
            (([2, 1, 3, 3], 2), [3, 3]),
            (([-1, -2, 3, 4], 3), [-1, 3, 4]),
            (([3, 4, 3, 3], 2), [3, 4]),
            (([5], 1), [5]),
        ],
        hints=[
            "The k elements with the largest values give the largest sum - order does not affect the sum.",
            "Find those k elements (a heap or a sort), but remember WHERE they were.",
            "Take the indices of the k largest values, sort the indices, and read the values back in index order.",
        ],
        pattern="Top-k selection by value, restore original order by index",
        explain=(
            "Any k-subset with the k largest values maximises the sum. Ties are harmless: any choice among equal "
            "values keeps the sum. Selecting by index (heap.nlargest or sorting indices by value) and then sorting "
            "the chosen indices restores the subsequence order."
        ),
        cx="O(n log k) time with a heap (O(n log n) with a full sort), O(k) space",
        brute_cx="O(C(n, k) * k) time - try every subsequence of length k",
        brute=r"""
# BRUTE FORCE: O(C(n, k) * k) time - try every subsequence of length k
def max_subsequence(nums, k):
    best, best_sum = None, None
    for chosen in itertools.combinations(range(len(nums)), k):
        total = sum(nums[i] for i in chosen)
        if best_sum is None or total > best_sum:
            best, best_sum = [nums[i] for i in chosen], total
    return best
""",
        solution=r"""
# OPTIMISED: O(n log k) time with a heap (O(n log n) with a full sort), O(k) space
# Idea: Top-k selection by value, restore original order by index
def max_subsequence(nums, k):
    top = heapq.nlargest(k, range(len(nums)), key=lambda i: nums[i])
    return [nums[i] for i in sorted(top)]
""",
    ),
    # ---- Super Ugly Number (LeetCode 313) ----
    dict(
        title="Super Ugly Number",
        diff="M",
        lc=313,
        slug="super-ugly-number",
        prompt=(
            "A super ugly number is a positive integer whose prime factors all belong to the given list primes (1 "
            "counts). Return the n-th super ugly number in increasing order."
        ),
        sig="def nth_super_ugly_number(n: int, primes: List[int]) -> int:",
        fn="nth_super_ugly_number",
        tests=[
            ((12, [2, 7, 13, 19]), 32),
            ((1, [2, 3, 5]), 1),
            ((10, [2, 3, 5]), 12),
            ((5, [3]), 81),
        ],
        hints=[
            "Every super ugly number other than 1 is a smaller super ugly number times one of the primes.",
            "Generate them in order with a min-heap seeded with 1: pop the smallest x, push x * p for each prime.",
            (
                "The same number can be reached by two routes (2*3 = 3*2); keep a set of what you have pushed so "
                "you do not count a value twice."
            ),
        ],
        pattern="Generate in order with a min-heap (k-way merge of multiples)",
        explain=(
            "Starting from 1 and repeatedly multiplying by the primes produces every super ugly number. A min-heap "
            "pops them in increasing order, and a 'seen' set removes duplicates reached by different factor orders. "
            "After n pops the last popped value is the answer."
        ),
        cx="O(n * m * log(n * m)) time with m = len(primes), O(n * m) space",
        brute_cx="O(answer * m) time - test every integer by dividing out the allowed primes",
        brute=r"""
# BRUTE FORCE: O(answer * m) time - test every integer by dividing out the allowed primes
def nth_super_ugly_number(n, primes):
    count, x = 0, 0

    while count < n:
        x += 1
        rest = x
        for p in primes:
            while rest % p == 0:
                rest //= p
        if rest == 1:
            count += 1

    return x
""",
        solution=r"""
# OPTIMISED: O(n * m * log(n * m)) time with m = len(primes), O(n * m) space
# Idea: Generate in order with a min-heap (k-way merge of multiples)
def nth_super_ugly_number(n, primes):
    heap = [1]
    seen = {1}
    value = 1

    for _ in range(n):
        value = heapq.heappop(heap)
        for p in primes:
            if value * p not in seen:
                seen.add(value * p)
                heapq.heappush(heap, value * p)

    return value
""",
    ),
    # ---- Range Sum of Sorted Subarray Sums (LeetCode 1508) ----
    dict(
        title="Range Sum of Sorted Subarray Sums",
        diff="M",
        lc=1508,
        slug="range-sum-of-sorted-subarray-sums",
        prompt=(
            "nums has n positive integers. List the sums of all n*(n+1)/2 non-empty contiguous subarrays and sort "
            "them. Return the sum of the numbers from position left to position right (1-indexed, inclusive) in "
            "that sorted list, modulo 1_000_000_007."
        ),
        sig="def range_sum(nums: List[int], n: int, left: int, right: int) -> int:",
        fn="range_sum",
        tests=[
            (([1, 2, 3, 4], 4, 1, 5), 13),
            (([1, 2, 3, 4], 4, 3, 4), 6),
            (([1, 2, 3, 4], 4, 1, 10), 50),
            (([5], 1, 1, 1), 5),
        ],
        hints=[
            "Materialising and sorting all O(n^2) sums works for small n but wastes memory.",
            "For each start index the subarray sums form an increasing sequence (all numbers are positive).",
            (
                "So this is a k-way merge of n sorted lists: heap of (current sum, end index), pop the smallest "
                "`right` times and extend that chain by one element."
            ),
        ],
        pattern="K-way merge of sorted chains with a min-heap",
        explain=(
            "For a fixed start, extending the subarray only increases the sum, so each start index produces a "
            "sorted stream. A min-heap holding one head per stream pops the sums in global sorted order; after "
            "popping a sum, push the next sum of the same stream. We only need to pop `right` values and add those "
            "at positions >= left."
        ),
        cx="O(right * log n) time, O(n) space",
        brute_cx="O(n^2 log n) time and O(n^2) space - compute and sort every subarray sum",
        brute=r"""
# BRUTE FORCE: O(n^2 log n) time and O(n^2) space - compute and sort every subarray sum
def range_sum(nums, n, left, right):
    sums = []

    for i in range(n):
        total = 0
        for j in range(i, n):
            total += nums[j]
            sums.append(total)

    sums.sort()

    return sum(sums[left - 1 : right]) % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(right * log n) time, O(n) space
# Idea: K-way merge of sorted chains with a min-heap
def range_sum(nums, n, left, right):
    heap = [(x, i) for i, x in enumerate(nums)]
    heapq.heapify(heap)
    total = 0

    for k in range(1, right + 1):
        value, end = heapq.heappop(heap)
        if k >= left:
            total += value
        if end + 1 < n:
            heapq.heappush(heap, (value + nums[end + 1], end + 1))

    return total % (10**9 + 7)
""",
    ),
    # ---- Number of Orders in the Backlog (LeetCode 1801) ----
    dict(
        title="Number of Orders in the Backlog",
        diff="M",
        lc=1801,
        slug="number-of-orders-in-the-backlog",
        prompt=(
            "orders[i] = [price, amount, type] arrive in order; type 0 is a buy, type 1 is a sell. A buy matches "
            "the cheapest sell with price <= its price; a sell matches the most expensive buy with price >= its "
            "price. Matching trades min(amounts) units, repeated while possible. Unmatched leftovers join the "
            "backlog. Return the total unit amount left in the backlog, modulo 1_000_000_007."
        ),
        sig="def get_number_of_backlog_orders(orders: List[List[int]]) -> int:",
        fn="get_number_of_backlog_orders",
        tests=[
            (([[10, 5, 0], [15, 2, 1], [25, 1, 1], [30, 4, 0]],), 6),
            (([[7, 1000000000, 1], [15, 3, 0], [5, 999999995, 0], [5, 1, 1]],), 999999984),
            (([[5, 3, 0], [5, 3, 1]],), 0),
            (([[5, 2, 1], [6, 2, 1]],), 4),
        ],
        hints=[
            "Keep two collections: the buy backlog and the sell backlog.",
            (
                "A buy needs the CHEAPEST sell, a sell needs the MOST EXPENSIVE buy - two heaps (a max-heap via "
                "negated prices)."
            ),
            (
                "While the incoming order has amount left and the best opposite order is acceptable in price, "
                "trade; pop that heap entry when it is used up. Push any remainder on the order's own heap."
            ),
        ],
        pattern="Order-book simulation with two priority queues",
        explain=(
            "This is exactly how a limit order book works: each side is a priority queue ordered by best price. An "
            "incoming order trades against the top of the opposite queue as long as prices cross; anything "
            "unmatched is stored on its own side. Only the tops are ever touched, so each order is pushed and "
            "popped once."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2) time - scan every resting order for the best match each time",
        brute=r"""
# BRUTE FORCE: O(n^2) time - scan every resting order for the best match each time
def get_number_of_backlog_orders(orders):
    buys, sells = [], []

    for price, amount, kind in orders:
        if kind == 0:
            while amount:
                options = [o for o in sells if o[1] > 0 and o[0] <= price]
                if not options:
                    break
                best = min(options, key=lambda o: o[0])
                take = min(amount, best[1])
                amount -= take
                best[1] -= take

            if amount:
                buys.append([price, amount])
        else:
            while amount:
                options = [o for o in buys if o[1] > 0 and o[0] >= price]
                if not options:
                    break
                best = max(options, key=lambda o: o[0])
                take = min(amount, best[1])
                amount -= take
                best[1] -= take

            if amount:
                sells.append([price, amount])

    return sum(o[1] for o in buys + sells) % (10**9 + 7)
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Order-book simulation with two priority queues
def get_number_of_backlog_orders(orders):
    buys, sells = [], []

    for price, amount, kind in orders:
        if kind == 0:
            while amount and sells and sells[0][0] <= price:
                take = min(amount, sells[0][1])
                amount -= take
                sells[0][1] -= take
                if sells[0][1] == 0:
                    heapq.heappop(sells)

            if amount:
                heapq.heappush(buys, [-price, amount])
        else:
            while amount and buys and -buys[0][0] >= price:
                take = min(amount, buys[0][1])
                amount -= take
                buys[0][1] -= take
                if buys[0][1] == 0:
                    heapq.heappop(buys)

            if amount:
                heapq.heappush(sells, [price, amount])

    return sum(o[1] for o in buys + sells) % (10**9 + 7)
""",
    ),
    # ---- Distant Barcodes (LeetCode 1054) ----
    dict(
        title="Distant Barcodes",
        diff="M",
        lc=1054,
        slug="distant-barcodes",
        prompt=(
            "Rearrange the barcodes so that no two adjacent barcodes are equal. An answer is guaranteed to exist; "
            "return any valid arrangement."
        ),
        sig="def rearrange_barcodes(barcodes: List[int]) -> List[int]:",
        fn="rearrange_barcodes",
        check=_barcodes_ok,
        tests=[
            (([1, 1, 1, 2, 2, 2],), [2, 1, 2, 1, 2, 1]),
            (([1, 1, 1, 1, 2, 2, 3, 3],), [1, 3, 1, 3, 2, 1, 2, 1]),
            (([7],), [7]),
            (([1, 2],), [1, 2]),
        ],
        hints=[
            "The most frequent value is the dangerous one - place it first and keep it spread out.",
            "Use a max-heap of (count, value). Each step take the top value, unless it equals the previous placement.",
            (
                "If the top equals the previous value, take the second-most frequent instead, then push both back "
                "with updated counts."
            ),
        ],
        pattern="Greedy with a max-heap, never repeat the last value (cf. Reorganize String)",
        explain=(
            "A valid arrangement exists exactly when no value occupies more than ceil(n/2) slots. Always placing "
            "the most frequent value that differs from the last one keeps the heavy values apart; the guarantee "
            "ensures a different value is always available when the top equals the previous."
        ),
        cx="O(n log k) time, O(k) space for k distinct values",
        brute_cx="O(n!) time - try permutations until one has no equal neighbours",
        brute=r"""
# BRUTE FORCE: O(n!) time - try permutations until one has no equal neighbours
def rearrange_barcodes(barcodes):
    for perm in itertools.permutations(barcodes):
        if all(perm[i] != perm[i + 1] for i in range(len(perm) - 1)):
            return list(perm)
""",
        solution=r"""
# OPTIMISED: O(n log k) time, O(k) space for k distinct values
# Idea: Greedy with a max-heap, never repeat the last value (cf. Reorganize String)
def rearrange_barcodes(barcodes):
    heap = [(-count, value) for value, count in Counter(barcodes).items()]
    heapq.heapify(heap)
    out = []

    while heap:
        count, value = heapq.heappop(heap)

        if out and out[-1] == value:
            count2, value2 = heapq.heappop(heap)
            out.append(value2)
            if count2 + 1 < 0:
                heapq.heappush(heap, (count2 + 1, value2))
            heapq.heappush(heap, (count, value))
        else:
            out.append(value)
            if count + 1 < 0:
                heapq.heappush(heap, (count + 1, value))

    return out
""",
    ),
    # ---- Minimum Cost to Hire K Workers (LeetCode 857) ----
    dict(
        title="Minimum Cost to Hire K Workers",
        diff="H",
        lc=857,
        slug="minimum-cost-to-hire-k-workers",
        prompt=(
            "Worker i has quality[i] and a minimum wage expectation wage[i]. Hire exactly k workers and pay them in "
            "proportion to their quality, every worker getting at least their minimum wage. Return the least total "
            "pay (answers within 1e-5 are accepted)."
        ),
        sig="def mincost_to_hire_workers(quality: List[int], wage: List[int], k: int) -> float:",
        fn="mincost_to_hire_workers",
        compare="float",
        tests=[
            (([10, 20, 5], [70, 50, 30], 2), 105.0),
            (([3, 1, 10, 10, 1], [4, 8, 2, 2, 7], 3), 30.666666666666664),
            (([5], [10], 1), 10.0),
            (([1, 1], [1, 3], 2), 6.0),
        ],
        hints=[
            (
                "Everyone in the group is paid at the same rate r per unit of quality. The rate must satisfy r >= "
                "wage[i] / quality[i] for every hired worker."
            ),
            "So a group's rate is the MAX ratio in the group and its cost is rate * (sum of qualities).",
            (
                "Sort by ratio ascending; when worker i is added, their ratio is the max of the group. Keep the k "
                "smallest qualities seen (max-heap) to minimise the quality sum, and evaluate ratio * sum."
            ),
        ],
        pattern="Sort by ratio, max-heap to keep the k smallest qualities",
        explain=(
            "If the group's pay rate is fixed at the largest wage/quality ratio r, the cost is r times the total "
            "quality, so within the prefix of workers whose ratio <= r we want the k with the smallest quality. "
            "Sorting by ratio makes each worker in turn the rate-setter, and a max-heap of qualities (evicting the "
            "largest) maintains the best k and their sum."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(C(n, k) * k) time - evaluate every group of k workers",
        brute=r"""
# BRUTE FORCE: O(C(n, k) * k) time - evaluate every group of k workers
def mincost_to_hire_workers(quality, wage, k):
    best = float("inf")
    for group in itertools.combinations(range(len(quality)), k):
        rate = max(wage[i] / quality[i] for i in group)
        best = min(best, rate * sum(quality[i] for i in group))
    return best
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Sort by ratio, max-heap to keep the k smallest qualities
def mincost_to_hire_workers(quality, wage, k):
    workers = sorted(zip(quality, wage), key=lambda w: w[1] / w[0])
    heap = []
    total = 0
    best = float("inf")

    for q, w in workers:
        heapq.heappush(heap, -q)
        total += q
        if len(heap) > k:
            total += heapq.heappop(heap)
        if len(heap) == k:
            best = min(best, total * w / q)

    return best
""",
    ),
    # ---- Minimize Deviation in Array (LeetCode 1675) ----
    dict(
        title="Minimize Deviation in Array",
        diff="H",
        lc=1675,
        slug="minimize-deviation-in-array",
        prompt=(
            "You may repeatedly: halve an even element, or double an odd element. The deviation of the array is max "
            "- min. Return the smallest deviation reachable."
        ),
        sig="def minimum_deviation(nums: List[int]) -> int:",
        fn="minimum_deviation",
        tests=[
            (([1, 2, 3, 4],), 1),
            (([4, 1, 5, 20, 3],), 3),
            (([2, 10, 8],), 3),
            (([3],), 0),
            (([1, 1],), 0),
        ],
        hints=[
            (
                "An odd number can only become 2x (and then back to x); an even number can be halved until it is "
                "odd. So every element has a small set of possible values."
            ),
            (
                "Doubling every odd number up front makes all numbers even, and from then on you only ever DECREASE "
                "values (halving), never increase."
            ),
            (
                "Repeatedly halve the current MAXIMUM (that is the only way to reduce the deviation). Track the "
                "minimum seen and the best max - min; stop when the maximum is odd."
            ),
        ],
        pattern="Normalise to the maximal form, then shrink the maximum with a max-heap",
        explain=(
            "Once odd numbers are doubled, each element's options form a chain of halvings. The maximum is the only "
            "value whose reduction can lower the deviation; halving anything else cannot help. A max-heap gives the "
            "maximum, the running minimum is updated with each halved value, and when the maximum is odd it cannot "
            "be halved any further so the process ends. The best max - min seen along the way is the answer."
        ),
        cx="O(n log n * log M) time, O(n) space",
        brute_cx="exponential in n - try every combination of reachable values, one per element",
        brute=r"""
# BRUTE FORCE: exponential in n - try every combination of reachable values, one per element
def minimum_deviation(nums):
    options = []

    for x in nums:
        if x % 2:
            options.append([x, 2 * x])
        else:
            values = [x]
            while x % 2 == 0:
                x //= 2
                values.append(x)
            options.append(values)

    best = float("inf")

    for choice in itertools.product(*options):
        best = min(best, max(choice) - min(choice))

    return best
""",
        solution=r"""
# OPTIMISED: O(n log n * log M) time, O(n) space
# Idea: Normalise to the maximal form, then shrink the maximum with a max-heap
def minimum_deviation(nums):
    heap = [-(x * 2 if x % 2 else x) for x in nums]
    heapq.heapify(heap)
    low = -max(heap)
    best = float("inf")

    while True:
        top = -heap[0]
        best = min(best, top - low)
        if top % 2:
            break
        top //= 2
        low = min(low, top)
        heapq.heapreplace(heap, -top)

    return best
""",
    ),
    # ---- Split Array into Consecutive Subsequences (LeetCode 659) ----
    dict(
        title="Split Array into Consecutive Subsequences",
        diff="M",
        lc=659,
        slug="split-array-into-consecutive-subsequences",
        prompt=(
            "nums is sorted in non-decreasing order. Return True if it can be split into one or more subsequences, "
            "each consisting of consecutive increasing integers and having length at least 3."
        ),
        sig="def is_possible(nums: List[int]) -> bool:",
        fn="is_possible",
        tests=[
            (([1, 2, 3, 3, 4, 5],), True),
            (([1, 2, 3, 3, 4, 4, 5, 5],), True),
            (([1, 2, 3, 4, 4, 5],), False),
            (([1, 2],), False),
            (([1, 1, 2, 2, 3, 3],), True),
        ],
        hints=[
            "Process the numbers in order. Each number either extends an existing chain or starts a new one.",
            "Extending is always at least as good as starting - but WHICH chain to extend? A chain ending at x - 1.",
            (
                "Extend the SHORTEST chain ending at x - 1 (it is the one most in need of length). Keep, per end "
                "value, a min-heap of chain lengths. At the end every chain must have length >= 3."
            ),
        ],
        pattern="Greedy chain extension with per-end min-heaps",
        explain=(
            "Short chains are the ones at risk of ending below length 3, so a new element should lengthen the "
            "shortest chain that ends right before it. Maintaining, for each end value, a min-heap of chain lengths "
            "implements this: pop the shortest chain ending at x - 1, push its length + 1 under x (or start a "
            "length-1 chain if none exists). Finally every remaining chain length must be >= 3."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="exponential - try to attach each number to every possible chain (backtracking)",
        brute=r"""
# BRUTE FORCE: exponential - try to attach each number to every possible chain (backtracking)
def is_possible(nums):
    def place(i, chains):
        if i == len(nums):
            return all(length >= 3 for _, length in chains)

        x = nums[i]
        tried = set()

        for idx, (end, length) in enumerate(chains):
            if end == x - 1 and (end, length) not in tried:
                tried.add((end, length))
                extended = chains[:idx] + [(x, length + 1)] + chains[idx + 1 :]
                if place(i + 1, extended):
                    return True

        return place(i + 1, chains + [(x, 1)])

    return place(0, [])
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Greedy chain extension with per-end min-heaps
def is_possible(nums):
    ends = defaultdict(list)

    for x in nums:
        if ends[x - 1]:
            length = heapq.heappop(ends[x - 1])
            heapq.heappush(ends[x], length + 1)
        else:
            heapq.heappush(ends[x], 1)

    return all(length >= 3 for lengths in ends.values() for length in lengths)
""",
    ),
    # ---- Trapping Rain Water II (LeetCode 407) ----
    dict(
        title="Trapping Rain Water II",
        diff="H",
        lc=407,
        slug="trapping-rain-water-ii",
        prompt=(
            "heightMap is an m x n grid of cell heights. Rain falls and water can only escape over the border of "
            "the grid. Return the total volume of trapped water."
        ),
        sig="def trap_rain_water(heightMap: List[List[int]]) -> int:",
        fn="trap_rain_water",
        tests=[
            (([[1, 4, 3, 1, 3, 2], [3, 2, 1, 3, 2, 4], [2, 3, 3, 2, 3, 1]],), 4),
            (([[3, 3, 3, 3, 3], [3, 2, 2, 2, 3], [3, 2, 1, 2, 3], [3, 2, 2, 2, 3], [3, 3, 3, 3, 3]],), 10),
            (([[5]],), 0),
            (([[1, 1, 1], [1, 0, 1], [1, 1, 1]],), 1),
            (([[3, 3, 3], [3, 0, 3], [3, 1, 3], [3, 3, 3]],), 5),
        ],
        hints=[
            (
                "A cell holds water up to the height of the LOWEST point on the 'wall' around it - the wall is the "
                "cheapest way out to the border."
            ),
            (
                "Think Dijkstra from the border: always expand the lowest wall cell, because water inside cannot "
                "rise above it."
            ),
            (
                "Seed a min-heap with all border cells. Pop the lowest (h); for each unvisited neighbour, add "
                "max(0, h - height) water and push the neighbour with level max(h, its height)."
            ),
        ],
        pattern="Dijkstra-style flood from the border with a min-heap",
        explain=(
            "The water level at a cell equals the minimum over all paths to the border of the maximum height along "
            "the path - the 'bottleneck' height. Expanding cells from the border in increasing order of their "
            "current wall level (a min-heap) finalises each cell's level the first time it is reached, so the water "
            "above it is that level minus its own height (never negative)."
        ),
        cx="O(m * n * log(m * n)) time, O(m * n) space",
        brute_cx="O((m * n)^2) time worst case - relax water levels repeatedly until nothing changes",
        brute=r"""
# BRUTE FORCE: O((m * n)^2) time worst case - relax water levels repeatedly until nothing changes
def trap_rain_water(heightMap):
    m, n = len(heightMap), len(heightMap[0])
    inf = float("inf")
    level = [
        [heightMap[i][j] if i in (0, m - 1) or j in (0, n - 1) else inf for j in range(n)]
        for i in range(m)
    ]
    changed = True

    while changed:
        changed = False

        for i in range(1, m - 1):
            for j in range(1, n - 1):
                lowest_neighbour = min(
                    level[i - 1][j], level[i + 1][j], level[i][j - 1], level[i][j + 1]
                )
                new = max(heightMap[i][j], lowest_neighbour)
                if new < level[i][j]:
                    level[i][j] = new
                    changed = True

    return sum(level[i][j] - heightMap[i][j] for i in range(1, m - 1) for j in range(1, n - 1))
""",
        solution=r"""
# OPTIMISED: O(m * n * log(m * n)) time, O(m * n) space
# Idea: Dijkstra-style flood from the border with a min-heap
def trap_rain_water(heightMap):
    m, n = len(heightMap), len(heightMap[0])

    if m < 3 or n < 3:
        return 0

    seen = [[False] * n for _ in range(m)]
    heap = []

    for i in range(m):
        for j in range(n):
            if i in (0, m - 1) or j in (0, n - 1):
                heapq.heappush(heap, (heightMap[i][j], i, j))
                seen[i][j] = True

    water = 0

    while heap:
        level, i, j = heapq.heappop(heap)
        for a, b in ((i + 1, j), (i - 1, j), (i, j + 1), (i, j - 1)):
            if 0 <= a < m and 0 <= b < n and not seen[a][b]:
                seen[a][b] = True
                water += max(0, level - heightMap[a][b])
                heapq.heappush(heap, (max(level, heightMap[a][b]), a, b))

    return water
""",
    ),
]
