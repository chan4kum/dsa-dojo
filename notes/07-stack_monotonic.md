# 07 - Stacks, monotonic stacks & monotonic deques

> **One idea:** a stack remembers *unfinished business*. A monotonic stack keeps only the candidates that could still matter.

## 1. First principles
- **Plain stack (LIFO):** the most recent open thing is the first to close -> brackets, nested expressions, undo, DFS, parsing.
- **Monotonic stack:** keep the stack sorted (increasing or decreasing). When a new element breaks the order, pop - each popped element has just found *its answer* (its next greater / next smaller).
- **Monotonic deque:** same idea but you may also drop from the **front** when an element leaves a sliding window.
- Each element is pushed once and popped once -> **O(n)** even though there is a `while` inside the `for`.

## 2. How to spot it
- "next greater / smaller element", "how many days until ...", "previous smaller", "span".
- "largest rectangle", "trapping water", "remove k digits to make smallest number".
- Nested structure: brackets, `3[a2[c]]`, calculators.
- Window maximum/minimum of every window.

## 3. Paper recipe
1. Decide what the stack stores: **indices** (so you can compute distances/widths) - almost always indices.
2. Decide the order: *decreasing* stack answers "next greater"; *increasing* stack answers "next smaller".
3. Loop: `while stack and breaks_order(stack[-1], x): pop and resolve`; then push `i`.
4. Draw the stack after every step (see the trace).
5. Flush the stack at the end (sentinel value or a final loop).

## 4. Hand trace
`temperatures = [73, 74, 75, 71, 69, 72, 76, 73]`

| i | temp | resolved (popped) | stack (index:temp) |
|---|---|---|---|
| 0 | 73 | - | ['0:73'] |
| 1 | 74 | day 0 waited 1 | ['1:74'] |
| 2 | 75 | day 1 waited 1 | ['2:75'] |
| 3 | 71 | - | ['2:75', '3:71'] |
| 4 | 69 | - | ['2:75', '3:71', '4:69'] |
| 5 | 72 | day 4 waited 1, day 3 waited 2 | ['2:75', '5:72'] |
| 6 | 76 | day 5 waited 1, day 2 waited 4 | ['6:76'] |
| 7 | 73 | - | ['6:76', '7:73'] |

Answer: `[1, 1, 4, 2, 1, 1, 0, 0]` (days left on the stack never see a warmer day -> 0).

## 5. Template
*Reference solution for **Daily Temperatures** (`stack_monotonic/2`) - tested by `python dsa.py selftest`:*

```python
# OPTIMISED: O(n) time, O(n) space
# Idea: Monotonic (decreasing) stack: 'next greater element'
def daily_temperatures(temperatures):
    ans = [0] * len(temperatures)
    stack = []  # indices, temperatures decreasing
    for i, t in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < t:
            j = stack.pop()
            ans[j] = i - j
        stack.append(i)
    return ans
```

Monotonic **deque** (window maximum) is `stack_monotonic/4`; the largest-rectangle version with a sentinel is `stack_monotonic/3`.

Plain-stack skeleton (brackets): push openers, on a closer compare with `stack.pop()`, answer is `not stack`.

## 6. Traps
- Storing values instead of indices (cannot compute distance or width).
- Strict vs non-strict comparison (`<` vs `<=`) changes how **equal** values behave - test with duplicates.
- Forgetting the final flush (largest rectangle needs a trailing `0`).
- Popping from an empty stack.

## 7. Self-check
1. Why is Daily Temperatures O(n), not O(n^2)?
2. In Largest Rectangle, what are the left and right boundaries of a popped bar?
3. How does Sliding Window Maximum differ from a monotonic stack (what does the deque's front do)?

## 8. Practice ladder
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `stack_monotonic/1` | Easy | Valid Parentheses | [#20](https://leetcode.com/problems/valid-parentheses/) | Stack (LIFO matching of nested structure) |
| `stack_monotonic/11` | Easy | Next Greater Element I | [#496](https://leetcode.com/problems/next-greater-element-i/) | Monotonic decreasing stack + lookup dict |
| `stack_monotonic/12` | Easy | Remove All Adjacent Duplicates In String | [#1047](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/) | Stack as a self-cancelling accumulator |
| `stack_monotonic/18` | Easy | Remove Outermost Parentheses | [#1021](https://leetcode.com/problems/remove-outermost-parentheses/) | Depth counter instead of a stack |
| `stack_monotonic/23` | Easy | Make The String Great | [#1544](https://leetcode.com/problems/make-the-string-great/) | Stack cancellation of adjacent pairs |
| `stack_monotonic/33` | Easy | Final Prices With a Special Discount in a Shop | [#1475](https://leetcode.com/problems/final-prices-with-a-special-discount-in-a-shop/) | Next smaller element (monotonic stack) |
| `stack_monotonic/34` | Easy | Minimum String Length After Removing Substrings | [#2696](https://leetcode.com/problems/minimum-string-length-after-removing-substrings/) | Stack for cascading adjacent deletions |
| `stack_monotonic/2` | Medium | Daily Temperatures | [#739](https://leetcode.com/problems/daily-temperatures/) | Monotonic (decreasing) stack: 'next greater element' |
| `stack_monotonic/5` | Medium | Evaluate Reverse Polish Notation | [#150](https://leetcode.com/problems/evaluate-reverse-polish-notation/) | Stack evaluation (operands wait for their operator) |
| `stack_monotonic/6` | Medium | Decode String | [#394](https://leetcode.com/problems/decode-string/) | Stack of contexts for nested structures |
| `stack_monotonic/7` | Medium | Car Fleet | [#853](https://leetcode.com/problems/car-fleet/) | Sort + monotonic 'slowest ahead' (merge into the blocking fleet) |
| `stack_monotonic/8` | Medium | Asteroid Collision | [#735](https://leetcode.com/problems/asteroid-collision/) | Stack simulation (chain reactions) |
| `stack_monotonic/9` | Medium | Remove K Digits | [#402](https://leetcode.com/problems/remove-k-digits/) | Monotonic (increasing) stack - greedy removal |
| `stack_monotonic/10` | Medium | Next Greater Element II | [#503](https://leetcode.com/problems/next-greater-element-ii/) | Monotonic stack + doubled traversal for circular arrays |
| `stack_monotonic/13` | Medium | Validate Stack Sequences | [#946](https://leetcode.com/problems/validate-stack-sequences/) | Simulate with a stack (greedy pop whenever possible) |
| `stack_monotonic/14` | Medium | Simplify Path | [#71](https://leetcode.com/problems/simplify-path/) | Stack of path components |
| `stack_monotonic/15` | Medium | Basic Calculator II | [#227](https://leetcode.com/problems/basic-calculator-ii/) | Stack of terms (resolve * and / immediately, sum the rest) |
| `stack_monotonic/16` | Medium | 132 Pattern | [#456](https://leetcode.com/problems/132-pattern/) | Right-to-left monotonic stack keeping the best '2' |
| `stack_monotonic/17` | Medium | Remove Duplicate Letters | [#316](https://leetcode.com/problems/remove-duplicate-letters/) | Monotonic stack with 'can I drop it' (last-occurrence) guard |
| `stack_monotonic/19` | Medium | Minimum Add to Make Parentheses Valid | [#921](https://leetcode.com/problems/minimum-add-to-make-parentheses-valid/) | Balance counter (stack reduced to two integers) |
| `stack_monotonic/20` | Medium | Sum of Subarray Minimums | [#907](https://leetcode.com/problems/sum-of-subarray-minimums/) | Monotonic stack: contribution technique (each element's reach) |
| `stack_monotonic/24` | Medium | Remove All Adjacent Duplicates in String II | [#1209](https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string-ii/) | Stack of (value, count) |
| `stack_monotonic/25` | Medium | Score of Parentheses | [#856](https://leetcode.com/problems/score-of-parentheses/) | Depth counting instead of explicit recursion |
| `stack_monotonic/26` | Medium | Reverse Substrings Between Each Pair of Parentheses | [#1190](https://leetcode.com/problems/reverse-substrings-between-each-pair-of-parentheses/) | Pair matching + 'teleport and reverse direction' walk |
| `stack_monotonic/27` | Medium | Removing Stars From a String | [#2390](https://leetcode.com/problems/removing-stars-from-a-string/) | Stack as an undo buffer |
| `stack_monotonic/28` | Medium | Exclusive Time of Functions | [#636](https://leetcode.com/problems/exclusive-time-of-functions/) | Call-stack simulation with timestamps |
| `stack_monotonic/29` | Medium | Longest Well-Performing Interval | [#1124](https://leetcode.com/problems/longest-well-performing-interval/) | Prefix sums + first-occurrence map (+1/-1 walk) |
| `stack_monotonic/30` | Medium | Maximum Width Ramp | [#962](https://leetcode.com/problems/maximum-width-ramp/) | Monotonic stack of candidates + right-to-left scan |
| `stack_monotonic/31` | Medium | Find the Most Competitive Subsequence | [#1673](https://leetcode.com/problems/find-the-most-competitive-subsequence/) | Monotonic stack with a length budget |
| `stack_monotonic/3` | Hard | Largest Rectangle in Histogram | [#84](https://leetcode.com/problems/largest-rectangle-in-histogram/) | Monotonic (increasing) stack: nearest smaller element on both sides |
| `stack_monotonic/4` | Hard | Sliding Window Maximum | [#239](https://leetcode.com/problems/sliding-window-maximum/) | Monotonic deque (decreasing) over a sliding window |
| `stack_monotonic/21` | Hard | Maximal Rectangle | [#85](https://leetcode.com/problems/maximal-rectangle/) | Reduce to Largest Rectangle in Histogram per row |
| `stack_monotonic/22` | Hard | Basic Calculator | [#224](https://leetcode.com/problems/basic-calculator/) | Stack of (result, sign) saved at each '(' |
| `stack_monotonic/32` | Hard | Number of Visible People in a Queue | [#1944](https://leetcode.com/problems/number-of-visible-people-in-a-queue/) | Monotonic stack processed right to left |

Start one with `python dsa.py start stack_monotonic/1`.

**More:** 155 Min Stack (M), 150 Evaluate Reverse Polish Notation (M), 496 Next Greater Element I (E), 503 Next Greater Element II (M), 853 Car Fleet (M), 901 Online Stock Span (M), 402 Remove K Digits (M), 316 Remove Duplicate Letters (M), 394 Decode String (M), 224 Basic Calculator (H), 85 Maximal Rectangle (H), 42 Trapping Rain Water (H).

## 9. Make it stay - the teacher's anchors

**Picture it.** A line of people waiting to see a doctor; a taller newcomer makes everyone shorter in front of them irrelevant (they will never be 'the next taller person' for anyone).

**The rule in one sentence.** 'Next greater/smaller element' or 'matching pairs/nesting' => keep a stack of unresolved items; resolve them when the answer arrives.

**Why it works.** An element leaves the stack exactly when its question is answered, so every element is pushed and popped once: O(n).

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. What does the stack hold at any moment in Daily Temperatures?
2. Why decreasing vs increasing stack - what decides it?
3. How does the same stack solve Largest Rectangle in Histogram?

**Mistakes students make most.**
- Storing values when you need indices (distances, widths).
- Forgetting to flush the remaining stack at the end.
- Using strict vs non-strict comparisons incorrectly with equal values.

**When NOT to use it.** You need ANY greater element (not the nearest), or the order of arrival is irrelevant.

**The same idea in disguise.** Valid parentheses -> daily temperatures -> next greater (circular) -> remove K digits -> asteroid collision -> largest rectangle -> sliding window maximum (monotonic DEQUE).
