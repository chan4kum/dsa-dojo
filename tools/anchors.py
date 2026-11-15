"""Teacher's anchors appended to every topic note: an image, a one-line rule, the 'why', teach-back prompts,
the mistakes students make most, when NOT to use the idea, and how the same idea reappears in disguise.
Writing is deliberate: concepts stick when they have an image, a reason, and a contrast."""

A = {}

A["hashing"] = dict(
    picture=(
        "A coat check. Instead of searching every rack for your coat (O(n)), you hand over a ticket (the hash) and "
        "the attendant walks straight to the hook."
    ),
    rule="If your inner loop only asks 'does something equal F(x) exist?', replace the loop with a dictionary lookup.",
    why=(
        "A hash maps a key to an array slot, and array access by index is O(1). You pay O(n) memory once to turn "
        "every future 'seen it?' from a scan into a jump."
    ),
    teach=[
        "Why must Two Sum look up the complement BEFORE inserting the current number?",
        "What makes two words anagrams, and how does that become a dictionary key?",
        "Why is Longest Consecutive Sequence O(n) although it has a while inside a for?",
    ],
    mistakes=[
        "Using a list for membership tests (`x in list` is O(n), silently making the solution O(n^2)).",
        "Using a mutable key (list) - convert to a tuple.",
        "Forgetting duplicates: a set loses counts, a Counter keeps them.",
    ],
    not_when=(
        "The data is already sorted and memory is tight - two pointers gives O(1) space. Or the question is about "
        "ORDER/RANGES (use sorting/heap/tree), because hashes destroy order."
    ),
    disguises=(
        "Two Sum -> Subarray Sum Equals K (store prefix sums) -> Contiguous Array (store first index of a balance) "
        "-> Longest Substring Without Repeating (store last index). Same lookup, different 'key'."
    ),
)
A["prefix_sums"] = dict(
    picture=(
        "Mile markers on a highway. The distance between markers 12 and 47 is marker(47) - marker(12): you never "
        "re-drive the road."
    ),
    rule="A range sum is a difference of two prefix sums: sum(l..r) = P[r+1] - P[l].",
    why=(
        "Every prefix already contains everything before it, so subtracting the shorter prefix cancels the shared "
        "part and leaves exactly the range."
    ),
    teach=[
        "Write sum(i..j) using P. What is P[0] and why do we need it?",
        "How does 'subarray sum = k' become a Two Sum problem on prefixes?",
        "What do you store in the dictionary and why do we insert P[0] = 0 first?",
    ],
    mistakes=[
        "Off-by-one between P of length n+1 and the array of length n.",
        "Forgetting the empty prefix (misses subarrays that start at index 0).",
        "Using a sliding window when negatives exist (windows need non-negative numbers; prefix + hash does not).",
    ],
    not_when=(
        "You only need ONE range query (just loop), or updates are interleaved with queries (use a Fenwick tree / "
        "segment tree, see Range Sum Query - Mutable)."
    ),
    disguises=(
        "Range sum -> pivot index -> product except self (prefix AND suffix products) -> subarray sum divisible by "
        "k (prefix mod k) -> path sum on a tree (prefix sums down the path)."
    ),
)
A["two_pointers"] = dict(
    picture=(
        "Two people squeezing a sorted bookshelf from both ends: if the sum of the two books is too heavy, the "
        "heavier book can never be part of the answer - drop it."
    ),
    rule="Sorted (or monotone) data + a pair condition => start at both ends and discard one end every step.",
    why=(
        "Each move eliminates a candidate that can no longer succeed, so you do at most n moves instead of n^2 "
        "pairs. The elimination argument IS the proof."
    ),
    teach=[
        "In Two Sum II, why is it safe to move `right` left when the sum is too big?",
        "Why does Container With Most Water move the SHORTER wall?",
        "How does read/write pointers (Move Zeroes) differ from converging pointers?",
    ],
    mistakes=[
        "Applying converging pointers to unsorted data.",
        "Moving the wrong pointer in Container With Most Water.",
        "Duplicates in 3Sum: skip equal values AFTER recording a triple.",
    ],
    not_when=(
        "The condition is not monotone in either pointer, or you need indices of the ORIGINAL order after sorting "
        "(hash map instead)."
    ),
    disguises=(
        "Two Sum II -> 3Sum -> Container -> Trapping Rain Water -> Sort Colors (three-way partition) -> Merge "
        "Sorted Array (from the back)."
    ),
)
A["sliding_window"] = dict(
    picture=(
        "A caterpillar: the head eats forward (extend right), and when the window is poisoned (invalid) the tail "
        "retreats until it is safe again."
    ),
    rule=(
        "Contiguous subarray/substring + a validity condition that only gets worse as the window grows => expand "
        "right, shrink left while invalid."
    ),
    why=(
        "Every element enters once and leaves once, so the two pointers move at most 2n steps in total - amortised "
        "O(n) even though there is a loop inside the loop."
    ),
    teach=[
        "What exact condition makes a window 'valid' in Longest Substring Without Repeating?",
        "Fixed-size vs variable-size windows: when do you use which?",
        "Why is the nested while loop still O(n)?",
    ],
    mistakes=[
        "Shrinking only once instead of `while invalid`.",
        "Updating the answer at the wrong moment (before/after shrinking).",
        "Using a window when negatives break monotonicity (use prefix sums + hash).",
    ],
    not_when=(
        "The validity condition is not monotone (a larger window can become valid again) or you need non-contiguous "
        "selections."
    ),
    disguises=(
        "Max average subarray (fixed) -> longest unique substring -> min size subarray sum -> min window substring "
        "-> longest repeating replacement -> permutation in string."
    ),
)
A["array_tricks"] = dict(
    picture=(
        "Kadane: walking along a road with a running balance. If your balance goes negative, you would be better "
        "off starting fresh from the next town."
    ),
    rule="Ask 'what is the best answer ENDING at index i?' - often it depends only on the best ending at i-1.",
    why=(
        "An optimal subarray never needs a negative-sum prefix (cut it and you do better), so a running total that "
        "goes below zero can be discarded."
    ),
    teach=[
        "Explain Kadane in one sentence without code.",
        "Why must Maximum Product Subarray track a minimum too?",
        "How can the input array itself act as a hash table when values lie in [1, n]?",
    ],
    mistakes=[
        "Initialising the best to 0 (breaks all-negative arrays).",
        "Forgetting that a negative flips max and min.",
        "Cyclic sort: advancing i after a swap instead of re-checking the swapped-in value.",
    ],
    not_when="The best subarray must have a fixed length or a constraint on sum - use a window/prefix sums instead.",
    disguises=(
        "Max subarray -> max product -> best time to buy/sell (running min) -> circular subarray -> house robber "
        "(best ending at i with a skip)."
    ),
)
A["binary_search"] = dict(
    picture=(
        "The number-guessing game: 'higher or lower?' halves the range every time - 1,000,000 possibilities in 20 "
        "questions."
    ),
    rule=(
        "If a yes/no predicate flips from False to True exactly once over an ordered range, binary search finds the "
        "flip in O(log n) - on an array OR on the answer itself."
    ),
    why=(
        "Each probe at mid rules out half the range because monotonicity guarantees what lies on each side. Always "
        "ask: 'what is my predicate, and is it monotone?'"
    ),
    teach=[
        "Write the predicate for 'first index >= target'.",
        "Why is `lo < hi` with `hi = mid` safe and `lo <= hi` with `hi = mid` an infinite loop?",
        "How do you recognise 'binary search on the answer'?",
    ],
    mistakes=[
        "Infinite loops from wrong mid rounding (use upper mid when lo = mid).",
        "Off-by-one on bounds (half-open [lo, hi) is the most reliable).",
        "Binary searching a non-monotone predicate.",
    ],
    not_when="You cannot define a monotone predicate, or n is tiny and a linear scan is clearer.",
    disguises=(
        "Search -> first/last position -> rotated array -> peak -> Koko/ship packages/split array (search the "
        "answer) -> median of two sorted arrays (search the partition)."
    ),
)
A["stack_monotonic"] = dict(
    picture=(
        "A line of people waiting to see a doctor; a taller newcomer makes everyone shorter in front of them "
        "irrelevant (they will never be 'the next taller person' for anyone)."
    ),
    rule=(
        "'Next greater/smaller element' or 'matching pairs/nesting' => keep a stack of unresolved items; resolve "
        "them when the answer arrives."
    ),
    why=(
        "An element leaves the stack exactly when its question is answered, so every element is pushed and popped "
        "once: O(n)."
    ),
    teach=[
        "What does the stack hold at any moment in Daily Temperatures?",
        "Why decreasing vs increasing stack - what decides it?",
        "How does the same stack solve Largest Rectangle in Histogram?",
    ],
    mistakes=[
        "Storing values when you need indices (distances, widths).",
        "Forgetting to flush the remaining stack at the end.",
        "Using strict vs non-strict comparisons incorrectly with equal values.",
    ],
    not_when="You need ANY greater element (not the nearest), or the order of arrival is irrelevant.",
    disguises=(
        "Valid parentheses -> daily temperatures -> next greater (circular) -> remove K digits -> asteroid "
        "collision -> largest rectangle -> sliding window maximum (monotonic DEQUE)."
    ),
)
A["linked_list"] = dict(
    picture=(
        "A treasure hunt: each clue only tells you where the next one is. If you lose the clue, you lose the rest "
        "of the hunt - so save `next` BEFORE you overwrite a pointer."
    ),
    rule=(
        "Draw boxes and arrows. Every pointer change = one arrow redrawn; do them in an order that never orphans nodes."
    ),
    why=(
        "A singly linked list has no random access, so every technique is about moving pointers cleverly: dummy "
        "head (no special cases), fast/slow (find middle/cycle), reverse (read backwards)."
    ),
    teach=[
        "Why does a dummy head remove edge cases?",
        "Prove that fast and slow must meet in a cycle.",
        "Where does the cycle start - derive a = L - b?",
    ],
    mistakes=[
        "Losing the rest of the list by overwriting `next` first.",
        "Not handling empty/one-node lists.",
        "Off-by-one in 'n-th from end' (the gap must be n, with a dummy).",
    ],
    not_when=(
        "You need random access or length-dependent logic repeatedly - convert to an array first (and say so; "
        "interviewers like the trade-off discussion)."
    ),
    disguises=(
        "Reverse -> middle -> palindrome -> reorder list -> reverse k-group; Floyd: cycle -> cycle start -> find "
        "the duplicate number -> happy number."
    ),
)
A["intervals"] = dict(
    picture=(
        "A calendar: sort meetings by start time and the whole picture falls out; overlaps can only happen between "
        "neighbours."
    ),
    rule="Sort first (by start to merge, by END to pick the maximum non-overlapping set), then sweep once.",
    why=(
        "After sorting by start, if interval i overlaps some later interval j, it already overlaps i+1. Sorting by "
        "end makes the earliest finisher the safest greedy pick (exchange argument)."
    ),
    teach=[
        "Which sort key for merging, which for scheduling - and why?",
        "How does a min-heap give the number of rooms needed?",
        "What does 'touching' intervals mean for <= vs <?",
    ],
    mistakes=[
        "Choosing the wrong sort key.",
        "Mutating the input intervals unexpectedly.",
        "Treating [1,2] and [2,3] as overlapping when the problem says they are not (or vice versa).",
    ],
    not_when="Intervals arrive online with deletions (use a balanced tree/sorted container).",
    disguises=(
        "Merge -> insert -> non-overlapping -> meeting rooms I/II -> arrows to burst balloons -> interval "
        "intersections -> employee free time."
    ),
)
A["greedy"] = dict(
    picture=(
        "Always picking the cheapest checkout lane: great when your choice cannot hurt later choices, disastrous "
        "when it can (coin change with 1, 3, 4)."
    ),
    rule=(
        "Make the locally best choice ONLY IF you can prove it never hurts the future (exchange argument / "
        "stays-ahead)."
    ),
    why="The proof is the algorithm: take any optimal solution, swap in the greedy choice, show it is no worse.",
    teach=[
        "Give a counter-example where greedy fails (coin change).",
        "State the exchange argument for 'sort by end time'.",
        "What state do you carry in Jump Game?",
    ],
    mistakes=[
        "Believing the samples instead of attacking the idea with adversarial input.",
        "Sorting by the wrong key.",
        "Skipping the global feasibility check (Gas Station).",
    ],
    not_when=(
        "Choices interact (knapsack-like) - use DP. If you cannot say why greedy is safe in one sentence, it "
        "probably is not."
    ),
    disguises=(
        "Jump game -> gas station -> partition labels -> candy (two passes) -> task scheduler (heap + greedy) -> "
        "valid parenthesis string (range of states)."
    ),
)
A["heap"] = dict(
    picture=(
        "A tournament bracket kept in a tree: the champion is always on top, and replacing it only requires "
        "replaying one root-to-leaf path."
    ),
    rule=(
        "Repeatedly need the current min/max while things keep arriving? Use a heap: O(log n) per operation instead "
        "of O(n log n) re-sorting."
    ),
    why=(
        "A heap keeps only PARTIAL order (parent <= children), which is all you need for 'the best one', and that "
        "is why it is cheaper than a sorted list."
    ),
    teach=[
        "Why a MIN-heap of size k for the k LARGEST?",
        "Heap vs sort vs quickselect: when each?",
        "Why does Python store negatives for a max-heap?",
    ],
    mistakes=[
        "Comparing unorderable payloads on ties (add an index tie-breaker).",
        "Using a max-heap when a bounded min-heap is cheaper.",
        "Forgetting `heapify` is O(n).",
    ],
    not_when=(
        "You need the whole sorted order, or arbitrary-element deletion (use a sorted container or lazy deletion)."
    ),
    disguises=(
        "Kth largest -> top K frequent -> merge K lists -> meeting rooms II -> task scheduler -> median of a stream "
        "(two heaps) -> smallest range."
    ),
)
A["trees"] = dict(
    picture=(
        "A company org chart: each manager only needs a report from direct reports. Information flows UP as return "
        "values, and instructions flow DOWN as parameters."
    ),
    rule=(
        "Decide what each node must (1) receive from its parent and (2) return to its parent - then recursion "
        "writes itself."
    ),
    why=(
        "A tree is recursive by definition (a node + two trees), so a correct answer for the subtrees plus a "
        "combine step at the root is a proof by induction."
    ),
    teach=[
        "Which problems pass state DOWN (good nodes) and which return state UP (balanced tree)?",
        "Why does a BST inorder give sorted order?",
        "What is the difference between the value a node RETURNS and the candidate answer it RECORDS (diameter)?",
    ],
    mistakes=[
        "Forgetting the None base case.",
        "Validating a BST by comparing only with the parent (must carry a (low, high) range).",
        "Recomputing heights top-down (O(n^2)) instead of bottom-up.",
    ],
    not_when=(
        "The structure has cycles (it is a graph - add a visited set) or very deep chains risk recursion limits "
        "(use an explicit stack)."
    ),
    disguises=(
        "Depth -> balanced -> diameter -> max path sum (return one-sided chain, record two-sided) -> LCA -> path "
        "sum III (prefix sums on a path) -> serialize (preorder + nulls)."
    ),
)
A["backtracking"] = dict(
    picture=(
        "Walking a maze with chalk: choose a corridor, mark it, explore; if it dead-ends, rub out the mark and go "
        "back to the last junction."
    ),
    rule="choose -> explore -> UN-choose. The recursion tree is the search space; prune branches that cannot succeed.",
    why=(
        "Undoing the choice restores the exact previous state, so siblings do not see each other's decisions. "
        "Pruning cuts whole subtrees before you explore them."
    ),
    teach=[
        "Draw the recursion tree for subsets of [1,2,3].",
        "How do you avoid duplicates when the input has repeats?",
        "Why do we copy `path` when we record a result?",
    ],
    mistakes=[
        "Appending `path` itself instead of `path[:]`.",
        "Forgetting to undo the choice.",
        "No pruning/sorting so duplicates explode.",
    ],
    not_when="Overlapping subproblems exist (the same state is reached many ways) - memoise it and you are doing DP.",
    disguises=(
        "Subsets -> permutations -> combination sum -> parentheses -> word search -> N-Queens -> palindrome "
        "partitioning -> restore IP addresses."
    ),
)
A["graphs"] = dict(
    picture=(
        "A city map: BFS is a ripple spreading outward (shortest in hops); DFS is a hiker following one road to its "
        "end before backing up."
    ),
    rule=(
        "Name the nodes and the edges first. Then pick BFS (shortest unweighted), DFS "
        "(reachability/components/cycle), Kahn (ordering), Dijkstra (weighted), Union-Find (merging groups)."
    ),
    why=(
        "Marking nodes visited when they ENTER the queue/stack guarantees each node and edge is processed once: O(V+E)."
    ),
    teach=[
        "What are the nodes and edges in Word Ladder?",
        "Why does BFS give shortest paths only when edges have equal weight?",
        "How does Kahn's algorithm detect a cycle?",
    ],
    mistakes=[
        "Marking visited too late (duplicates in the queue).",
        "Using DFS recursion on huge grids (stack overflow) without noting it.",
        "Treating a grid as a graph but forgetting bounds checks.",
    ],
    not_when=(
        "Negative edge weights (Dijkstra fails - Bellman-Ford) or when the structure is actually a tree (simpler "
        "recursion)."
    ),
    disguises=(
        "Islands -> rotting oranges (multi-source BFS) -> 01 matrix -> course schedule (topological) -> redundant "
        "connection (union-find) -> network delay (Dijkstra) -> word ladder -> alien dictionary (graph built from "
        "data)."
    ),
)
A["dynamic_programming"] = dict(
    picture=(
        "A staircase of answers: you do not climb the whole tower from scratch each time - you write the answer for "
        "each step on the wall and read it back."
    ),
    rule=(
        "Define the STATE in one sentence ('dp[i] = best answer for the first i items'), write the TRANSITION from "
        "smaller states, set the BASE cases, then pick the evaluation order."
    ),
    why=(
        "DP = recursion + memory. If the same sub-question is asked many times, answering it once and caching it "
        "turns exponential into polynomial."
    ),
    teach=[
        "State the dp meaning for LIS, LCS, Edit Distance, Coin Change - each in one sentence.",
        "How do you turn a top-down memo into a bottom-up table, and then shrink the table?",
        "Combinations vs permutations: which loop goes outside?",
    ],
    mistakes=[
        "A vague state definition ('dp[i] is the answer') - write exactly what i means.",
        "Wrong base cases / indexing offsets.",
        "Reaching for DP when greedy is provable (or vice versa).",
    ],
    not_when="Subproblems do not overlap (plain divide and conquer) or a simple greedy proof exists.",
    disguises=(
        "Climbing stairs -> robber -> coin change -> LIS -> knapsack (partition, target sum) -> grid paths -> "
        "LCS/edit distance -> intervals (burst balloons) -> state machines (stocks with cooldown) -> regex."
    ),
)
A["bits_math"] = dict(
    picture="Light switches: each bit is a switch. XOR flips switches; two identical flips cancel out.",
    rule=(
        "n & (n-1) removes the lowest set bit; x ^ x = 0; x ^ 0 = x; n & -n isolates the lowest set bit; shifts "
        "multiply/divide by 2."
    ),
    why="Binary arithmetic acts on all bits in parallel, so a few instructions replace a loop over elements or bits.",
    teach=[
        "Why does n & (n-1) clear the lowest set bit?",
        "How does XOR find the single number?",
        "Why is repeated squaring O(log n) for x**n?",
    ],
    mistakes=[
        "Forgetting Python ints are unbounded (mask with 0xFFFFFFFF for 32-bit tricks).",
        "Floor division with negatives.",
        "Overflow reasoning copied from C/Java (state it, then explain Python's difference).",
    ],
    not_when="A clear arithmetic or hash-based approach is just as fast and far more readable.",
    disguises=(
        "Single number -> counting bits -> power of two -> sum without + (XOR + carry) -> reverse bits -> pow(x, n) "
        "(binary exponentiation) -> sieve (math)."
    ),
)
A["strings"] = dict(
    picture=(
        "KMP is a reader who remembers how much of the pattern they had already matched, so after a mismatch they "
        "never re-read text they have already seen."
    ),
    rule=(
        "Compare by index, not by slicing; precompute what the pattern already tells you about itself (the prefix "
        "function)."
    ),
    why=(
        "The prefix function stores, for each position, the longest proper prefix that is also a suffix - exactly "
        "the amount of progress that survives a mismatch."
    ),
    teach=[
        "Compute the prefix function of 'abab' by hand.",
        "Why is KMP O(n+m) when it seems to 'go back'?",
        "How do you choose between expand-around-centre, DP and Manacher for palindromes?",
    ],
    mistakes=[
        "Slicing in loops (hidden O(n) per slice).",
        "Off-by-one with inclusive/exclusive ends.",
        "Ignoring Unicode/case/whitespace requirements in the prompt.",
    ],
    not_when=(
        "Python's built-ins (`find`, `in`, `split`) are allowed and clear - say so, then offer the manual version "
        "if asked."
    ),
    disguises=(
        "strStr -> longest prefix-suffix -> repeated substring -> atoi (state machine) -> add/multiply strings "
        "(carry) -> decode string (stack)."
    ),
)
A["design"] = dict(
    picture=(
        "A restaurant kitchen: the menu (interface) stays the same, but the layout behind it (hash map + linked "
        "list, heaps, tries) decides how fast every dish arrives."
    ),
    rule=(
        "List the operations and their required complexities FIRST; then choose the structure(s) that give each "
        "operation its cost, usually by combining two structures."
    ),
    why=(
        "One structure rarely gives O(1) for everything, but two that cover for each other's weaknesses do (map = "
        "lookup, list = order; two heaps = median)."
    ),
    teach=[
        "What does each of the two structures in LRU Cache do?",
        "Why does a trie beat a hash set for prefix queries?",
        "How do two heaps give the median in O(log n) per insert?",
    ],
    mistakes=[
        "Choosing the structure before listing the operations.",
        "Forgetting to keep the two structures in sync after delete/evict.",
        "Ignoring capacity and edge cases (empty, duplicates).",
    ],
    not_when="Simple data + few operations - a plain list or dict is enough; do not over-engineer.",
    disguises=(
        "Min stack -> LRU -> trie -> median finder -> kth largest stream -> time-based key-value store -> Fenwick "
        "tree -> browser history."
    ),
)
A["divide_conquer"] = dict(
    picture=(
        "Sorting a library: split the shelves between helpers, each sorts their part, then you merge two sorted "
        "shelves - merging is easy, splitting is free."
    ),
    rule=(
        "Split into independent halves, solve each recursively, combine cheaply. Cost: T(n) = 2T(n/2) + O(n) => O(n "
        "log n)."
    ),
    why="Halving gives log n levels, and each level does O(n) total work in the combine step.",
    teach=[
        "Write the recurrence for merge sort and solve it by drawing the tree.",
        "How does merge sort count inversions (Reverse Pairs) for free?",
        "When does divide and conquer differ from DP?",
    ],
    mistakes=[
        "Combine step slower than O(n) (e.g. repeated slicing).",
        "Forgetting base cases (size 0/1).",
        "Assuming subproblems are independent when they overlap (use DP).",
    ],
    not_when="Subproblems overlap - memoise instead. Or a simple scan already solves it.",
    disguises=(
        "Merge sort -> count inversions / reverse pairs -> quickselect -> closest pair -> build tree from "
        "traversals -> median of two sorted arrays."
    ),
)
A["matrix"] = dict(
    picture=(
        "A rubber-stamp: rotating a picture 90 degrees equals flipping it along a diagonal and then mirroring it - "
        "two easy moves instead of one confusing one."
    ),
    rule=(
        "Treat a matrix as coordinates (r, c). Compose simple transforms (transpose, reverse rows), shrink "
        "boundaries (spiral), or reuse the matrix as its own scratch space (first row/column markers)."
    ),
    why=(
        "Most matrix problems are index arithmetic in disguise; once you write where (r, c) ends up, the code is "
        "mechanical."
    ),
    teach=[
        "Where does cell (r, c) go in a clockwise rotation?",
        "Why do the guards `top <= bottom` and `left <= right` appear in Spiral Matrix?",
        "Why can't Game of Life update cells in place without encoding?",
    ],
    mistakes=[
        "Updating cells in an order that corrupts values you still need.",
        "Row/column swapped (r, c vs x, y).",
        "Forgetting the single row / single column case.",
    ],
    not_when="You need path-finding or connectivity - that is a graph on a grid (BFS/DFS), see the graphs topic.",
    disguises=(
        "Rotate -> spiral -> set zeroes -> game of life -> valid sudoku -> search a 2D matrix (binary search on a "
        "virtual 1-D index)."
    ),
)


def render(topic):
    a = A.get(topic)
    if not a:
        return ""
    teach = "\n".join(f"{i}. {q}" for i, q in enumerate(a["teach"], 1))
    mist = "\n".join(f"- {m}" for m in a["mistakes"])
    return f"""
## 9. Make it stay - the teacher's anchors

**Picture it.** {a["picture"]}

**The rule in one sentence.** {a["rule"]}

**Why it works.** {a["why"]}

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
{teach}

**Mistakes students make most.**
{mist}

**When NOT to use it.** {a["not_when"]}

**The same idea in disguise.** {a["disguises"]}
"""
