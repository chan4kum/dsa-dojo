# Brute-force (naive but correct) solutions for the base problems, keyed "<topic>/<n>".
# `selftest` runs each one against the same tests: it may be too SLOW on big inputs (reported as a timeout,
# which is exactly the point), but it must never be WRONG.
BRUTE = {
"hashing/1": (r'''
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []
''', "O(n^2) time, O(1) space - tries every pair"),
"hashing/2": (r'''
def group_anagrams(strs):
    groups = []
    for w in strs:
        for g in groups:
            if sorted(g[0]) == sorted(w):
                g.append(w)
                break
        else:
            groups.append([w])
    return groups
''', "O(n^2 * k log k) - compares each word with every existing group"),
"hashing/3": (r'''
def longest_consecutive(nums):
    best = 0
    for x in nums:
        y = x
        while y + 1 in nums:           # membership in a LIST is O(n)
            y += 1
        best = max(best, y - x + 1)
    return best
''', "O(n^3) worst case - expands from every element using list membership"),
"prefix_sums/1": (r'''
def pivot_index(nums):
    for i in range(len(nums)):
        if sum(nums[:i]) == sum(nums[i + 1:]):
            return i
    return -1
''', "O(n^2) - recomputes both sides for every index"),
"prefix_sums/2": (r'''
def product_except_self(nums):
    out = []
    for i in range(len(nums)):
        p = 1
        for j in range(len(nums)):
            if j != i:
                p *= nums[j]
        out.append(p)
    return out
''', "O(n^2) - multiplies everything else for each index"),
"prefix_sums/3": (r'''
def subarray_sum(nums, k):
    count = 0
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total == k:
                count += 1
    return count
''', "O(n^2) - every (start, end) pair with a running sum"),
"two_pointers/1": (r'''
def is_palindrome(s):
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]
''', "O(n) time, O(n) space - builds a cleaned reversed copy"),
"two_pointers/2": (r'''
def three_sum(nums):
    res = set()
    n = len(nums)
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                if nums[i] + nums[j] + nums[k] == 0:
                    res.add(tuple(sorted((nums[i], nums[j], nums[k]))))
    return [list(t) for t in res]
''', "O(n^3) - all triples, a set removes duplicates"),
"two_pointers/3": (r'''
def max_area(height):
    best = 0
    for i in range(len(height)):
        for j in range(i + 1, len(height)):
            best = max(best, (j - i) * min(height[i], height[j]))
    return best
''', "O(n^2) - every pair of lines"),
"two_pointers/4": (r'''
def trap(height):
    total = 0
    for i in range(len(height)):
        left = max(height[:i + 1])
        right = max(height[i:])
        total += min(left, right) - height[i]
    return total
''', "O(n^2) - recomputes the tallest wall on each side of every bar"),
"sliding_window/1": (r'''
def find_max_average(nums, k):
    return max(sum(nums[i:i + k]) for i in range(len(nums) - k + 1)) / k
''', "O(n*k) - re-sums every window"),
"sliding_window/2": (r'''
def length_of_longest_substring(s):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            if len(set(s[i:j + 1])) == j - i + 1:
                best = max(best, j - i + 1)
    return best
''', "O(n^3) - checks every substring for uniqueness"),
"sliding_window/3": (r'''
def min_subarray_len(target, nums):
    best = float("inf")
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            if total >= target:
                best = min(best, j - i + 1)
                break
    return 0 if best == float("inf") else best
''', "O(n^2) - every start, extend until the sum is reached"),
"sliding_window/4": (r'''
def min_window(s, t):
    need = Counter(t)
    best = ""
    for i in range(len(s)):
        for j in range(i + len(t), len(s) + 1):
            if not (need - Counter(s[i:j])) and (best == "" or j - i < len(best)):
                best = s[i:j]
    return best
''', "O(n^2 * m) - every substring checked against t"),
"array_tricks/1": (r'''
def max_subarray(nums):
    best = nums[0]
    for i in range(len(nums)):
        total = 0
        for j in range(i, len(nums)):
            total += nums[j]
            best = max(best, total)
    return best
''', "O(n^2) - all subarrays"),
"array_tricks/2": (r'''
def missing_number(nums):
    for i in range(len(nums) + 1):
        if i not in nums:
            return i
''', "O(n^2) - list membership for every candidate"),
"array_tricks/3": (r'''
def first_missing_positive(nums):
    seen = set(nums)
    i = 1
    while i in seen:
        i += 1
    return i
''', "O(n) time but O(n) extra space (the hard version asks for O(1))"),
"binary_search/1": (r'''
def search(nums, target):
    for i, x in enumerate(nums):
        if x == target:
            return i
    return -1
''', "O(n) - linear scan ignores the sorted order"),
"binary_search/2": (r'''
def search_rotated(nums, target):
    return nums.index(target) if target in nums else -1
''', "O(n) - linear scan"),
"binary_search/3": (r'''
def min_eating_speed(piles, h):
    k = 1
    while sum(-(-p // k) for p in piles) > h:
        k += 1
    return k
''', "O(max(piles) * n) - tries every speed in turn"),
"binary_search/4": (r'''
def split_array(nums, k):
    def parts(cap):
        c, cur = 1, 0
        for x in nums:
            if cur + x > cap:
                c, cur = c + 1, x
            else:
                cur += x
        return c
    cap = max(nums)
    while parts(cap) > k:
        cap += 1
    return cap
''', "O(sum * n) - tries every cap upward"),
"binary_search/5": (r'''
def find_median(a, b):
    m = sorted(a + b)
    n = len(m)
    return float(m[n // 2]) if n % 2 else (m[n // 2 - 1] + m[n // 2]) / 2
''', "O((m+n) log(m+n)) - merge and sort"),
"stack_monotonic/1": (r'''
def is_valid(s):
    while "()" in s or "[]" in s or "{}" in s:
        s = s.replace("()", "").replace("[]", "").replace("{}", "")
    return s == ""
''', "O(n^2) - repeatedly delete adjacent matched pairs"),
"stack_monotonic/2": (r'''
def daily_temperatures(temperatures):
    out = []
    for i, t in enumerate(temperatures):
        d = 0
        for j in range(i + 1, len(temperatures)):
            if temperatures[j] > t:
                d = j - i
                break
        out.append(d)
    return out
''', "O(n^2) - scan ahead from every day"),
"stack_monotonic/3": (r'''
def largest_rectangle_area(heights):
    best = 0
    for i in range(len(heights)):
        for j in range(i, len(heights)):
            best = max(best, min(heights[i:j + 1]) * (j - i + 1))
    return best
''', "O(n^3) - every range, take its minimum"),
"stack_monotonic/4": (r'''
def max_sliding_window(nums, k):
    return [max(nums[i:i + k]) for i in range(len(nums) - k + 1)]
''', "O(n*k) - recompute the max of every window"),
"linked_list/1": (r'''
def reverse_list(head):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    dummy = tail = ListNode()
    for v in reversed(vals):
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next
''', "O(n) time but O(n) extra space - copies values into a new list"),
"linked_list/2": (r'''
def middle_node(head):
    n, cur = 0, head
    while cur:
        n, cur = n + 1, cur.next
    for _ in range(n // 2):
        head = head.next
    return head
''', "two passes - count the length, then walk n/2"),
"linked_list/3": (r'''
def remove_nth_from_end(head, n):
    length, cur = 0, head
    while cur:
        length, cur = length + 1, cur.next
    dummy = ListNode(0, head)
    cur = dummy
    for _ in range(length - n):
        cur = cur.next
    cur.next = cur.next.next
    return dummy.next
''', "two passes - compute the length first"),
"linked_list/4": (r'''
def find_duplicate(nums):
    for i in range(len(nums)):
        if nums[i] in nums[i + 1:]:
            return nums[i]
''', "O(n^2) time (sorting would be O(n log n) but modifies the array)"),
"linked_list/5": (r'''
def reverse_k_group(head, k):
    vals = []
    while head:
        vals.append(head.val)
        head = head.next
    for i in range(0, len(vals) - k + 1, k):
        vals[i:i + k] = vals[i:i + k][::-1]
    dummy = tail = ListNode()
    for v in vals:
        tail.next = ListNode(v)
        tail = tail.next
    return dummy.next
''', "O(n) time, O(n) extra space - rebuild from a Python list"),
"intervals/1": (r'''
def merge(intervals):
    iv = [list(x) for x in intervals]
    changed = True
    while changed:
        changed = False
        for i in range(len(iv)):
            for j in range(i + 1, len(iv)):
                if iv[i][0] <= iv[j][1] and iv[j][0] <= iv[i][1]:
                    iv[i] = [min(iv[i][0], iv[j][0]), max(iv[i][1], iv[j][1])]
                    del iv[j]
                    changed = True
                    break
            if changed:
                break
    return sorted(iv)
''', "O(n^3) worst case - keep merging any overlapping pair"),
"intervals/2": (r'''
def insert(intervals, new_interval):
    iv = sorted([list(x) for x in intervals] + [list(new_interval)])
    out = []
    for s, e in iv:
        if out and s <= out[-1][1]:
            out[-1][1] = max(out[-1][1], e)
        else:
            out.append([s, e])
    return out
''', "O(n log n) - append, re-sort, re-merge (ignores that input is sorted)"),
"intervals/3": (r'''
def erase_overlap_intervals(intervals):
    iv = sorted(intervals)
    n = len(iv)
    dp = [1] * n                              # longest chain of non-overlapping intervals ending at i
    for i in range(n):
        for j in range(i):
            if iv[j][1] <= iv[i][0]:
                dp[i] = max(dp[i], dp[j] + 1)
    return n - max(dp, default=0)
''', "O(n^2) DP - longest non-overlapping chain"),
"greedy/1": (r'''
def can_jump(nums):
    def go(i):
        if i >= len(nums) - 1:
            return True
        return any(go(i + j) for j in range(1, nums[i] + 1))
    return go(0)
''', "exponential - tries every jump length from every index"),
"greedy/2": (r'''
def can_complete_circuit(gas, cost):
    n = len(gas)
    for s in range(n):
        tank = 0
        for k in range(n):
            i = (s + k) % n
            tank += gas[i] - cost[i]
            if tank < 0:
                break
        else:
            return s
    return -1
''', "O(n^2) - simulate the trip from every start"),
"greedy/3": (r'''
def partition_labels(s):
    sizes, start, end = [], 0, 0
    for i, c in enumerate(s):
        end = max(end, s.rfind(c))            # rfind scans the whole string: O(n)
        if i == end:
            sizes.append(end - start + 1)
            start = i + 1
    return sizes
''', "O(n^2) - last occurrence found by scanning every time"),
"heap/1": (r'''
def find_kth_largest(nums, k):
    return sorted(nums, reverse=True)[k - 1]
''', "O(n log n) - full sort"),
"heap/2": (r'''
def top_k_frequent(nums, k):
    count = Counter(nums)
    return [x for x, _ in sorted(count.items(), key=lambda t: -t[1])[:k]]
''', "O(n log n) - sort all distinct values by frequency"),
"heap/3": (r'''
def least_interval(tasks, n):
    remaining = Counter(tasks)
    cooldown = {}
    t = 0
    while remaining:
        t += 1
        ready = [c for c in remaining if cooldown.get(c, 0) < t]
        if ready:
            c = max(ready, key=lambda x: remaining[x])
            remaining[c] -= 1
            cooldown[c] = t + n
            if remaining[c] == 0:
                del remaining[c]
    return t
''', "simulation, one time unit at a time (O(T * distinct))"),
"trees/1": (r'''
def max_depth(root):
    if not root:
        return 0
    depth, level = 0, [root]
    while level:
        depth += 1
        level = [c for n in level for c in (n.left, n.right) if c]
    return depth
''', "O(n) - level by level (an alternative, not slower)"),
"trees/2": (r'''
def level_order(root):
    def height(n):
        return 0 if not n else 1 + max(height(n.left), height(n.right))
    def at_depth(n, d):
        if not n:
            return []
        return [n.val] if d == 0 else at_depth(n.left, d - 1) + at_depth(n.right, d - 1)
    return [at_depth(root, d) for d in range(height(root))]
''', "O(n * h) - re-walks the tree once per level"),
"trees/3": (r'''
def is_valid_bst(root):
    def values(n):
        return [] if not n else values(n.left) + [n.val] + values(n.right)
    def ok(n):
        if not n:
            return True
        return all(v < n.val for v in values(n.left)) and all(v > n.val for v in values(n.right)) and ok(n.left) and ok(n.right)
    return ok(root)
''', "O(n^2) - compares each node with every value in its subtrees"),
"trees/4": (r'''
def lowest_common_ancestor(root, p, q):
    def path(n, target):
        if not n:
            return None
        if n is target:
            return [n]
        for child in (n.left, n.right):
            r = path(child, target)
            if r:
                return [n] + r
        return None
    a, b = path(root, p), path(root, q)
    lca = None
    for x, y in zip(a, b):
        if x is y:
            lca = x
    return lca
''', "O(n) time, O(h) space - two root-to-node paths and compare"),
"trees/5": (r'''
def max_path_sum(root):
    def chain(n):
        return 0 if not n else n.val + max(0, chain(n.left), chain(n.right))
    best = float("-inf")
    stack = [root]
    while stack:
        n = stack.pop()
        if not n:
            continue
        best = max(best, n.val + max(0, chain(n.left)) + max(0, chain(n.right)))
        stack += [n.left, n.right]
    return best
''', "O(n^2) - recomputes the downward chains for every node"),
"backtracking/1": (r'''
def subsets(nums):
    n = len(nums)
    return [[nums[i] for i in range(n) if mask >> i & 1] for mask in range(1 << n)]
''', "O(n * 2^n) - one bitmask per subset"),
"backtracking/2": (r'''
def permute(nums):
    import itertools
    return [list(p) for p in itertools.permutations(nums)]
''', "O(n * n!) - library enumeration"),
"backtracking/3": (r'''
def combination_sum(candidates, target):
    res = []
    def go(i, remain, path):
        if remain == 0:
            res.append(path[:])
            return
        if i == len(candidates) or remain < 0:
            return
        c = candidates[i]
        for count in range(remain // c + 1):    # use candidate i exactly `count` times
            go(i + 1, remain - c * count, path + [c] * count)
    go(0, target, [])
    return res
''', "exponential - tries every multiplicity of every candidate, no sorting-based pruning"),
"backtracking/4": (r'''
def generate_parenthesis(n):
    import itertools
    def valid(s):
        bal = 0
        for ch in s:
            bal += 1 if ch == "(" else -1
            if bal < 0:
                return False
        return bal == 0
    return [s for s in ("".join(t) for t in itertools.product("()", repeat=2 * n)) if valid(s)]
''', "O(2^(2n) * n) - generate every string, then filter"),
"backtracking/5": (r'''
def solve_n_queens(n):
    import itertools
    res = []
    for cols in itertools.permutations(range(n)):
        if len({r + c for r, c in enumerate(cols)}) == n and len({r - c for r, c in enumerate(cols)}) == n:
            res.append(["." * c + "Q" + "." * (n - c - 1) for c in cols])
    return res
''', "O(n * n!) - every column permutation, check the diagonals at the end"),
"graphs/1": (r'''
def num_islands(grid):
    g = [row[:] for row in grid]
    R, C = len(g), len(g[0])
    def sink(r, c):
        if 0 <= r < R and 0 <= c < C and g[r][c] == "1":
            g[r][c] = "0"
            sink(r + 1, c); sink(r - 1, c); sink(r, c + 1); sink(r, c - 1)
    n = 0
    for r in range(R):
        for c in range(C):
            if g[r][c] == "1":
                n += 1
                sink(r, c)
    return n
''', "O(R*C) but recursive (deep recursion on big grids)"),
"graphs/2": (r'''
def oranges_rotting(grid):
    g = [row[:] for row in grid]
    R, C = len(g), len(g[0])
    minutes = 0
    while True:
        to_rot = [(r, c) for r in range(R) for c in range(C) if g[r][c] == 1 and
                  any(0 <= r + dr < R and 0 <= c + dc < C and g[r + dr][c + dc] == 2 for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)))]
        if not to_rot:
            break
        for r, c in to_rot:
            g[r][c] = 2
        minutes += 1
    return -1 if any(1 in row for row in g) else minutes
''', "O((R*C)^2) - rescans the whole grid every minute"),
"graphs/3": (r'''
def can_finish(num_courses, prerequisites):
    adj = [[] for _ in range(num_courses)]
    for a, b in prerequisites:
        adj[b].append(a)
    def reaches_itself(start):
        stack, seen = list(adj[start]), set()
        while stack:
            u = stack.pop()
            if u == start:
                return True
            if u not in seen:
                seen.add(u)
                stack.extend(adj[u])
        return False
    return not any(reaches_itself(i) for i in range(num_courses))
''', "O(V * (V+E)) - search for a cycle from every node"),
"graphs/4": (r'''
def find_redundant_connection(edges):
    adj = {}
    for u, v in edges:
        seen, stack = set(), [u]
        while stack:                              # is v already reachable from u?
            x = stack.pop()
            if x == v:
                return [u, v]
            if x not in seen:
                seen.add(x)
                stack.extend(adj.get(x, []))
        adj.setdefault(u, []).append(v)
        adj.setdefault(v, []).append(u)
    return []
''', "O(E * (V+E)) - one traversal per edge"),
"graphs/5": (r'''
def network_delay_time(times, n, k):
    dist = {i: float("inf") for i in range(1, n + 1)}
    dist[k] = 0
    for _ in range(n - 1):                        # Bellman-Ford relaxation rounds
        for u, v, w in times:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
    m = max(dist.values())
    return -1 if m == float("inf") else m
''', "O(V * E) - Bellman-Ford; Dijkstra's heap makes it O(E log V)"),
"graphs/6": (r'''
def ladder_length(begin_word, end_word, word_list):
    words = set(word_list)
    if end_word not in words:
        return 0
    def adjacent(a, b):
        return sum(x != y for x, y in zip(a, b)) == 1
    q, seen = deque([(begin_word, 1)]), {begin_word}
    while q:
        w, d = q.popleft()
        if w == end_word:
            return d
        for other in words:                       # compare with EVERY word
            if other not in seen and adjacent(w, other):
                seen.add(other)
                q.append((other, d + 1))
    return 0
''', "O(N^2 * L) - tests every word pair instead of generating neighbours"),
"dynamic_programming/1": (r'''
def climb_stairs(n):
    if n <= 2:
        return n
    return climb_stairs(n - 1) + climb_stairs(n - 2)
''', "O(2^n) - plain recursion recomputes the same subproblems"),
"dynamic_programming/2": (r'''
def rob(nums):
    def go(i):
        if i < 0:
            return 0
        return max(go(i - 1), go(i - 2) + nums[i])
    return go(len(nums) - 1)
''', "O(2^n) - recursion without memo"),
"dynamic_programming/3": (r'''
def coin_change(coins, amount):
    def go(a):
        if a == 0:
            return 0
        best = float("inf")
        for c in coins:
            if c <= a:
                best = min(best, go(a - c) + 1)
        return best
    r = go(amount)
    return -1 if r == float("inf") else r
''', "O(coins^amount) - exponential recursion"),
"dynamic_programming/4": (r'''
def length_of_lis(nums):
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp, default=0)
''', "O(n^2) DP; patience sorting gets O(n log n)"),
"dynamic_programming/5": (r'''
def longest_common_subsequence(text1, text2):
    def go(i, j):
        if i == len(text1) or j == len(text2):
            return 0
        if text1[i] == text2[j]:
            return 1 + go(i + 1, j + 1)
        return max(go(i + 1, j), go(i, j + 1))
    return go(0, 0)
''', "O(2^(m+n)) - recursion without memo"),
"dynamic_programming/6": (r'''
def min_distance(word1, word2):
    def go(i, j):
        if i == len(word1):
            return len(word2) - j
        if j == len(word2):
            return len(word1) - i
        if word1[i] == word2[j]:
            return go(i + 1, j + 1)
        return 1 + min(go(i + 1, j + 1), go(i + 1, j), go(i, j + 1))
    return go(0, 0)
''', "O(3^(m+n)) - recursion without memo"),
"dynamic_programming/7": (r'''
def can_partition(nums):
    total = sum(nums)
    if total % 2:
        return False
    def go(i, remain):
        if remain == 0:
            return True
        if i == len(nums) or remain < 0:
            return False
        return go(i + 1, remain - nums[i]) or go(i + 1, remain)
    return go(0, total // 2)
''', "O(2^n) - try every subset"),
"dynamic_programming/8": (r'''
def word_break(s, word_dict):
    words = set(word_dict)
    def go(i):
        if i == len(s):
            return True
        return any(s[i:j] in words and go(j) for j in range(i + 1, len(s) + 1))
    return go(0)
''', "O(2^n) - recursion without memo"),
"dynamic_programming/9": (r'''
def max_coins(nums):
    def go(arr):
        if not arr:
            return 0
        best = 0
        for i in range(len(arr)):
            left = arr[i - 1] if i else 1
            right = arr[i + 1] if i + 1 < len(arr) else 1
            best = max(best, left * arr[i] * right + go(arr[:i] + arr[i + 1:]))
        return best
    return go(nums)
''', "O(n!) - try every bursting order"),
"bits_math/1": (r'''
def single_number(nums):
    return [x for x, c in Counter(nums).items() if c == 1][0]
''', "O(n) time, O(n) space - count with a hash map"),
"bits_math/2": (r'''
def count_bits(n):
    return [bin(i).count("1") for i in range(n + 1)]
''', "O(n log n) - count each number's bits separately"),
"bits_math/3": (r'''
def get_sum(a, b):
    # brute force: walk the number line one step at a time (works for any signs)
    r = a
    step = 1 if b > 0 else -1
    for _ in range(abs(b)):
        r += step
    return r
''', "O(|b|) - increments/decrements a one at a time (still needs + 1, shows why bit tricks matter)"),
"bits_math/4": (r'''
def my_pow(x, n):
    r = 1.0
    for _ in range(abs(n)):
        r *= x
    return r if n >= 0 else 1 / r
''', "O(n) multiplications - too slow for n ~ 2^31"),
"strings/1": (r'''
def str_str(haystack, needle):
    for i in range(len(haystack) - len(needle) + 1):
        if haystack[i:i + len(needle)] == needle:
            return i
    return -1
''', "O(n*m) - compare at every offset"),
"strings/2": (r'''
def longest_prefix(s):
    for L in range(len(s) - 1, 0, -1):
        if s[:L] == s[-L:]:
            return s[:L]
    return ""
''', "O(n^2) - try every length from longest"),
"design/1": (r'''
class MinStack:
    def __init__(self):
        self.a = []
    def push(self, val):
        self.a.append(val)
    def pop(self):
        self.a.pop()
    def top(self):
        return self.a[-1]
    def get_min(self):
        return min(self.a)
''', "get_min is O(n) - scans the whole stack"),
"design/2": (r'''
class LRUCache:
    def __init__(self, capacity):
        self.cap = capacity
        self.items = []                       # [key, value], least recent first
    def get(self, key):
        for i, (k, v) in enumerate(self.items):
            if k == key:
                self.items.append(self.items.pop(i))
                return v
        return -1
    def put(self, key, value):
        for i, (k, v) in enumerate(self.items):
            if k == key:
                self.items.pop(i)
                break
        self.items.append([key, value])
        if len(self.items) > self.cap:
            self.items.pop(0)
''', "O(n) per operation - linear search in a list"),
"design/3": (r'''
class Trie:
    def __init__(self):
        self.words = set()
    def insert(self, word):
        self.words.add(word)
    def search(self, word):
        return word in self.words
    def starts_with(self, prefix):
        return any(w.startswith(prefix) for w in self.words)
''', "starts_with is O(total characters) - scans every stored word"),
"design/4": (r'''
class MedianFinder:
    def __init__(self):
        self.a = []
    def add_num(self, num):
        self.a.append(num)
    def find_median(self):
        s = sorted(self.a)
        n = len(s)
        return float(s[n // 2]) if n % 2 else (s[n // 2 - 1] + s[n // 2]) / 2
''', "find_median is O(n log n) - sorts on every query"),
"divide_conquer/1": (r'''
def sort_array(nums):
    a = list(nums)
    for i in range(1, len(a)):
        j = i
        while j and a[j - 1] > a[j]:
            a[j - 1], a[j] = a[j], a[j - 1]
            j -= 1
    return a
''', "O(n^2) - insertion sort"),
"divide_conquer/2": (r'''
def reverse_pairs(nums):
    return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] > 2 * nums[j])
''', "O(n^2) - check every pair"),
}
