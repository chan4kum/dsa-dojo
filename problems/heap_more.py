"""extra batch of Heap problems - the problem bank for the "heap" topic.

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

from core import Counter


def _reorg_ok(args, got):
    s = args[0]
    if max(Counter(s).values(), default=0) > (len(s) + 1) // 2:
        return got == ""
    return sorted(got) == sorted(s) and all(got[i] != got[i + 1] for i in range(len(got) - 1))


PROBLEMS = [
    # ---- Last Stone Weight (LeetCode 1046) ----
    dict(
        title="Last Stone Weight",
        diff="E",
        lc=1046,
        slug="last-stone-weight",
        prompt=(
            "Repeatedly smash the two heaviest stones: equal -> both vanish, otherwise the heavier loses the "
            "lighter's weight. Return the weight of the last stone (0 if none)."
        ),
        sig="def last_stone_weight(stones: List[int]) -> int:",
        fn="last_stone_weight",
        tests=[
            (([2, 7, 4, 1, 8, 1],), 1),
            (([1],), 1),
            (([2, 2],), 0),
            (([10, 4, 2, 10],), 2),
            (([],), 0),
        ],
        hints=[
            "Each round needs the two largest values. Sorting every round works but is wasteful.",
            "A max-heap returns the largest in O(log n).",
            "Python has a min-heap: store negatives. Pop two, push back the difference if non-zero.",
        ],
        pattern="Max-heap via negated values (repeated 'take the largest')",
        explain=(
            "Whenever a process repeatedly asks for the current maximum/minimum while inserting new items, a heap "
            "is the\n        tool: O(log n) per operation instead of O(n log n) for re-sorting."
        ),
        cx="O(n log n) time, O(n) space",
        brute_cx="O(n^2 log n) time - re-sort every round",
        brute=r"""
# BRUTE FORCE: O(n^2 log n) time - re-sort every round
def last_stone_weight(stones):
    s = sorted(stones)
    while len(s) > 1:
        a, b = s.pop(), s.pop()
        if a != b:
            s.append(a - b)
            s.sort()
    return s[0] if s else 0
""",
        solution=r"""
# OPTIMISED: O(n log n) time, O(n) space
# Idea: Max-heap via negated values (repeated 'take the largest')
def last_stone_weight(stones):
    h = [-x for x in stones]
    heapq.heapify(h)
    while len(h) > 1:
        a, b = -heapq.heappop(h), -heapq.heappop(h)
        if a != b:
            heapq.heappush(h, -(a - b))
    return -h[0] if h else 0
""",
    ),
    # ---- K Closest Points to Origin (LeetCode 973) ----
    dict(
        title="K Closest Points to Origin",
        diff="M",
        lc=973,
        slug="k-closest-points-to-origin",
        prompt=(
            "Return the k points closest to (0, 0) by Euclidean distance (any order; the tests avoid ties at the "
            "boundary)."
        ),
        sig="def k_closest(points: List[List[int]], k: int) -> List[List[int]]:",
        fn="k_closest",
        compare="unordered",
        tests=[
            (([[1, 3], [-2, 2]], 1), [[-2, 2]]),
            (([[3, 3], [5, -1], [-2, 4]], 2), [[3, 3], [-2, 4]]),
            (([[0, 1], [1, 0]], 2), [[0, 1], [1, 0]]),
            (([[1, 1], [2, 2], [3, 3], [0, 0]], 3), [[0, 0], [1, 1], [2, 2]]),
        ],
        hints=[
            "You do not need the points fully sorted, only the k smallest.",
            "Compare squared distances - no sqrt needed.",
            "Keep a max-heap of size k: push each point; if the heap exceeds k, pop the farthest. O(n log k).",
        ],
        pattern="Bounded heap of size k (top-k selection)",
        explain=(
            "A heap capped at k elements never grows large, so each push/pop is O(log k). Alternatives: "
            "heapq.nsmallest,\n        or quickselect for O(n) average."
        ),
        cx="O(n log k) time, O(k) space",
        brute_cx="O(n log n) time - sort all points by distance",
        brute=r"""
# BRUTE FORCE: O(n log n) time - sort all points by distance
def k_closest(points, k):
    return sorted(points, key=lambda p: p[0] ** 2 + p[1] ** 2)[:k]
""",
        solution=r"""
# OPTIMISED: O(n log k) time, O(k) space
# Idea: Bounded heap of size k (top-k selection)
def k_closest(points, k):
    heap = []  # max-heap through negated distance
    for x, y in points:
        heapq.heappush(heap, (-(x * x + y * y), x, y))
        if len(heap) > k:
            heapq.heappop(heap)
    return [[x, y] for _, x, y in heap]
""",
    ),
    # ---- Reorganize String (LeetCode 767) ----
    dict(
        title="Reorganize String",
        diff="M",
        lc=767,
        slug="reorganize-string",
        prompt=(
            "Rearrange the letters of s so that no two adjacent characters are equal. Return any valid arrangement, "
            "or '' if impossible."
        ),
        sig="def reorganize_string(s: str) -> str:",
        fn="reorganize_string",
        check=_reorg_ok,
        tests=[
            (("aab",), "aba"),
            (("aaab",), ""),
            (("vvvlo",), "vlvov"),
            (("a",), "a"),
            (("aabbcc",), "abcabc"),
            (("aaaabbbb",), "abababab"),
        ],
        hints=[
            "When is it impossible? Look at the most frequent letter.",
            (
                "If max_count > (n+1)//2 it is impossible. Otherwise always place the letter with the most "
                "remaining occurrences (that is not the previous one)."
            ),
            (
                "Max-heap of (count, char). Pop the top, append, hold it back one round, push it again after "
                "placing the next letter."
            ),
        ],
        pattern="Greedy with a max-heap (most frequent first, avoid the last used)",
        explain=(
            "Placing the currently most plentiful letter keeps the 'bottleneck' letter from piling up at the "
            "end.\n        Remembering the previously used letter prevents adjacency. Any valid answer is accepted "
            "(validator)."
        ),
        cx="O(n log 26) time",
        brute_cx="O(n!) time - try all permutations",
        brute=r"""
# BRUTE FORCE: O(n!) time - try all permutations
def reorganize_string(s):
    for p in itertools.permutations(s):
        if all(p[i] != p[i + 1] for i in range(len(p) - 1)):
            return "".join(p)
    return ""
""",
        solution=r"""
# OPTIMISED: O(n log 26) time
# Idea: Greedy with a max-heap (most frequent first, avoid the last used)
def reorganize_string(s):
    heap = [(-c, ch) for ch, c in Counter(s).items()]
    heapq.heapify(heap)
    out, prev = [], None  # prev = (neg_count, char) held back one step
    while heap or prev:
        if not heap:
            return ""  # only the previous letter is left -> would be adjacent
        c, ch = heapq.heappop(heap)
        out.append(ch)
        if prev:
            heapq.heappush(heap, prev)
            prev = None
        if c + 1 < 0:
            prev = (c + 1, ch)
    return "".join(out)
""",
    ),
    # ---- Top K Frequent Words (LeetCode 692) ----
    dict(
        title="Top K Frequent Words",
        diff="M",
        lc=692,
        slug="top-k-frequent-words",
        prompt="Return the k most frequent words, sorted by frequency descending; ties broken alphabetically.",
        sig="def top_k_frequent(words: List[str], k: int) -> List[str]:",
        fn="top_k_frequent",
        tests=[
            ((["i", "love", "leetcode", "i", "love", "coding"], 2), ["i", "love"]),
            (
                (["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4),
                ["the", "is", "sunny", "day"],
            ),
            ((["a"], 1), ["a"]),
            ((["b", "a"], 2), ["a", "b"]),
        ],
        hints=[
            "Count first. Then the ordering is (-count, word).",
            "Sorting all distinct words costs O(m log m). Do you need them all sorted?",
            "heapq.nsmallest(k, counts, key=lambda w: (-counts[w], w)) keeps only k candidates (O(m log k)).",
        ],
        pattern="Counter + top-k with a composite sort key",
        explain=(
            "The tie-break turns the key into a tuple. A bounded heap avoids sorting everything when k << distinct "
            "words."
        ),
        cx="O(m log k) time",
        brute_cx="O(m log m) time - sort all distinct words",
        brute=r"""
# BRUTE FORCE: O(m log m) time - sort all distinct words
def top_k_frequent(words, k):
    cnt = Counter(words)
    return sorted(cnt, key=lambda w: (-cnt[w], w))[:k]
""",
        solution=r"""
# OPTIMISED: O(m log k) time
# Idea: Counter + top-k with a composite sort key
def top_k_frequent(words, k):
    cnt = Counter(words)
    return heapq.nsmallest(k, cnt, key=lambda w: (-cnt[w], w))
""",
    ),
    # ---- Find K Pairs with Smallest Sums (LeetCode 373) ----
    dict(
        title="Find K Pairs with Smallest Sums",
        diff="M",
        lc=373,
        slug="find-k-pairs-with-smallest-sums",
        prompt=(
            "Two sorted arrays nums1, nums2. Return the k pairs (u, v), u from nums1 and v from nums2, with the "
            "smallest sums u+v (any order)."
        ),
        sig="def k_smallest_pairs(nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:",
        fn="k_smallest_pairs",
        compare="unordered",
        tests=[
            (([1, 7, 11], [2, 4, 6], 3), [[1, 2], [1, 4], [1, 6]]),
            (([1, 1, 2], [1, 2, 3], 2), [[1, 1], [1, 1]]),
            (([1, 2], [3], 3), [[1, 3], [2, 3]]),
            (([1, 2], [], 2), []),
        ],
        hints=[
            "All pairs is O(mn). Because both arrays are sorted, the smallest sum is always (0,0).",
            "After taking pair (i, j), the next candidates are (i, j+1) (and (i+1, 0) for the first column).",
            "Min-heap seeded with (nums1[i] + nums2[0], i, 0) for the first min(k, m) rows; pop, then push (i, j+1).",
        ],
        pattern="Best-first search with a heap over a sorted 2D implicit grid",
        explain=(
            "Think of the pair sums as a matrix sorted along rows and columns. Pop the smallest, expand its right "
            "neighbour.\n        Each pop adds at most one new candidate: O(k log k)."
        ),
        cx="O(k log k) time",
        brute_cx="O(m*n log(mn)) time - build all pairs and sort",
        brute=r"""
# BRUTE FORCE: O(m*n log(mn)) time - build all pairs and sort
def k_smallest_pairs(nums1, nums2, k):
    pairs = sorted(([a, b] for a in nums1 for b in nums2), key=lambda p: p[0] + p[1])
    return pairs[:k]
""",
        solution=r"""
# OPTIMISED: O(k log k) time
# Idea: Best-first search with a heap over a sorted 2D implicit grid
def k_smallest_pairs(nums1, nums2, k):
    if not nums1 or not nums2:
        return []
    heap = [(nums1[i] + nums2[0], i, 0) for i in range(min(k, len(nums1)))]
    heapq.heapify(heap)
    out = []
    while heap and len(out) < k:
        _, i, j = heapq.heappop(heap)
        out.append([nums1[i], nums2[j]])
        if j + 1 < len(nums2):
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
    return out
""",
    ),
]
