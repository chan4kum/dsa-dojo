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
{{trace:mono_stack}}

## 5. Template
{{solution:stack_monotonic/2}}

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
{{ladder}}

**More:** 155 Min Stack (M), 150 Evaluate Reverse Polish Notation (M), 496 Next Greater Element I (E), 503 Next Greater Element II (M), 853 Car Fleet (M), 901 Online Stock Span (M), 402 Remove K Digits (M), 316 Remove Duplicate Letters (M), 394 Decode String (M), 224 Basic Calculator (H), 85 Maximal Rectangle (H), 42 Trapping Rain Water (H).
