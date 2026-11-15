from core import *

PROBLEMS = [
    dict(
        title="Kth Largest Element in an Array", diff="M", lc=215, slug="kth-largest-element-in-an-array",
        prompt="Return the k-th largest element of an unsorted array (the k-th in sorted descending order, "
               "duplicates counted).",
        sig="def find_kth_largest(nums: List[int], k: int) -> int:",
        fn="find_kth_largest",
        tests=[(([3, 2, 1, 5, 6, 4], 2), 5), (([3, 2, 3, 1, 2, 4, 5, 5, 6], 4), 4), (([1], 1), 1), (([2, 1], 2), 1),
               (([7, 7, 7], 2), 7)],
        hints=["Sorting is O(n log n). You only need the top k, not a full order.",
               "Keep the k largest seen so far in a MIN-heap: its root is the smallest of those k.",
               "Push each number; if the heap exceeds size k, pop the root. At the end the root is the k-th largest."],
        pattern="Top-K with a size-k min-heap",
        explain="""
        The min-heap of size k always holds the k biggest elements so far; its root is the weakest member and
        gets evicted when something stronger arrives. O(n log k) time, O(k) space - much better than sorting
        when k is small. (Quickselect gives O(n) average.)""",
        solution=r'''
def find_kth_largest(nums, k):
    heap = []
    for x in nums:
        heapq.heappush(heap, x)
        if len(heap) > k:
            heapq.heappop(heap)       # evict the smallest of the k+1
    return heap[0]
''',
    ),
    dict(
        title="Top K Frequent Elements", diff="M", lc=347, slug="top-k-frequent-elements",
        prompt="Return the k most frequent values of the array (any order). Better than O(n log n) is expected.",
        sig="def top_k_frequent(nums: List[int], k: int) -> List[int]:",
        fn="top_k_frequent", compare="unordered",
        tests=[(([1, 1, 1, 2, 2, 3], 2), [1, 2]), (([1], 1), [1]), (([4, 4, 4, 5, 5, 6], 1), [4]),
               (([-1, -1, 2, 2, 3], 2), [-1, 2])],
        hints=["First count frequencies with a hash map.",
               "Then it is a Top-K problem over (count, value) pairs: heap of size k, or...",
               "Bucket sort: frequency can only be 1..n, so index buckets by count and read from the highest bucket down."],
        pattern="Frequency map + heap (O(n log k)) or bucket sort (O(n))",
        explain="""
        Count with Counter. Then either heapq.nlargest(k, counts, key=counts.get) - O(n log k) - or place each
        value into buckets[count] and collect from the end - O(n) because counts are bounded by n.""",
        solution=r'''
def top_k_frequent(nums, k):
    count = Counter(nums)
    buckets = [[] for _ in range(len(nums) + 1)]       # index = frequency
    for x, c in count.items():
        buckets[c].append(x)
    out = []
    for c in range(len(nums), 0, -1):
        for x in buckets[c]:
            out.append(x)
            if len(out) == k:
                return out
    return out
''',
    ),
    dict(
        title="Task Scheduler", diff="M", lc=621, slug="task-scheduler",
        prompt="Tasks are labelled by letters; each takes one time unit. The same letter must be separated by at "
               "least n idle-or-other units. Return the minimum total time to finish all tasks.",
        sig="def least_interval(tasks: List[str], n: int) -> int:",
        fn="least_interval",
        tests=[((["A", "A", "A", "B", "B", "B"], 2), 8), ((["A", "A", "A", "B", "B", "B"], 0), 6),
               ((["A", "A", "A", "A", "A", "A", "B", "C", "D", "E", "F", "G"], 2), 16), ((["A"], 5), 1),
               ((["A", "B", "C"], 3), 3)],
        hints=["The most frequent task forces the structure of the schedule.",
               "If the top task appears f times, you need f-1 'gaps' of length n+1, plus a final slot for it (and for any ties).",
               "Answer = max(len(tasks), (f-1)*(n+1) + number_of_tasks_with_frequency_f)."],
        pattern="Greedy / counting argument on the most frequent task (a heap simulation also works)",
        explain="""
        Lay out the most frequent task A as A _ _ A _ _ A (gap n). Other tasks fill the blanks; if there are
        more tasks than blanks no idling is needed and the answer is just len(tasks). Ties for the max
        frequency each add one extra final slot. O(n).""",
        solution=r'''
def least_interval(tasks, n):
    counts = Counter(tasks)
    f = max(counts.values())
    tied = sum(1 for c in counts.values() if c == f)
    return max(len(tasks), (f - 1) * (n + 1) + tied)
''',
    ),
]
