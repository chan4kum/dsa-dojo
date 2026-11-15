from core import *

PROBLEMS = [
    dict(
        title="Sort an Array", diff="M", lc=912, slug="sort-an-array",
        prompt="Sort an integer array in ascending order WITHOUT calling sort(), in O(n log n) worst case. "
               "(Implement merge sort.)",
        sig="def sort_array(nums: List[int]) -> List[int]:",
        fn="sort_array",
        tests=[(([5, 2, 3, 1],), [1, 2, 3, 5]), (([5, 1, 1, 2, 0, 0],), [0, 0, 1, 1, 2, 5]), (([],), []), (([3],), [3]),
               (([-4, 0, 7, -4, 2],), [-4, -4, 0, 2, 7]), (([9, 8, 7, 6, 5, 4, 3, 2, 1],), [1, 2, 3, 4, 5, 6, 7, 8, 9])],
        hints=["Divide and conquer: if you could sort each half, how would you combine two sorted halves?",
               "Merging two sorted lists takes O(n) with two pointers.",
               "Recurse on halves until size <= 1, then merge. Use <= when comparing so equal elements keep their order (stable)."],
        pattern="Divide & conquer: split, solve halves, merge in O(n) -> O(n log n)",
        explain="""
        T(n) = 2T(n/2) + O(n) = O(n log n) by the recursion-tree (or master) theorem: log n levels, each doing
        O(n) merge work. Stable, needs O(n) extra space. The merge step is where problems like 'count inversions'
        hook in (see Reverse Pairs).""",
        solution=r'''
def sort_array(nums):
    if len(nums) <= 1:
        return nums
    mid = len(nums) // 2
    left, right = sort_array(nums[:mid]), sort_array(nums[mid:])
    out, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            out.append(left[i]); i += 1
        else:
            out.append(right[j]); j += 1
    out.extend(left[i:])
    out.extend(right[j:])
    return out
''',
    ),
    dict(
        title="Reverse Pairs", diff="H", lc=493, slug="reverse-pairs",
        prompt="Count pairs (i, j) with i < j and nums[i] > 2 * nums[j].",
        sig="def reverse_pairs(nums: List[int]) -> int:",
        fn="reverse_pairs",
        tests=[(([1, 3, 2, 3, 1],), 2), (([2, 4, 3, 5, 1],), 3), (([],), 0), (([5],), 0), (([2147483647, 2147483647, 2147483647],), 0),
               (([-5, -5],), 1)],
        hints=["Brute force over all pairs is O(n^2). Think merge sort: pairs split into 'both in left', 'both in right', 'one in each'.",
               "While merging, the two halves are already sorted. For each left element, count right elements with nums[j]*2 < nums[i] using a moving pointer.",
               "Count cross pairs BEFORE the merge step (pointer j only moves forward because left is sorted), then merge normally."],
        pattern="Divide & conquer with counting during merge sort (inversion-count family)",
        explain="""
        Within each recursion, count = pairs inside left + pairs inside right + cross pairs. Cross pairs are
        counted with a two-pointer sweep over the two sorted halves in O(n), so the whole thing stays
        O(n log n). Same idea solves Count of Smaller Numbers After Self and Count of Range Sum
        (alternatives: Fenwick tree / segment tree).""",
        solution=r'''
def reverse_pairs(nums):
    def sort(a):
        if len(a) <= 1:
            return a, 0
        mid = len(a) // 2
        left, x = sort(a[:mid])
        right, y = sort(a[mid:])
        count = x + y
        j = 0
        for v in left:                           # cross pairs: v > 2 * right[j]
            while j < len(right) and v > 2 * right[j]:
                j += 1
            count += j
        merged, i, j = [], 0, 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i]); i += 1
            else:
                merged.append(right[j]); j += 1
        merged += left[i:] + right[j:]
        return merged, count
    return sort(list(nums))[1]
''',
    ),
]
