# 10 - Greedy

> **One idea:** make the locally best choice, and *prove* it never hurts the final answer.

## 1. First principles
- Greedy is DP where you can throw away all but one option at each step.
- It works when the problem has the **greedy-choice property** (some optimal solution contains the local best choice) and **optimal substructure**.
- Proof tools you can do in your head:
  - **Exchange argument:** take any optimal solution, swap in the greedy choice, show it is no worse.
  - **"Stays ahead":** show the greedy partial solution is always at least as good as any other at every step.
  - **Frontier/summary argument:** one number (farthest reach, current tank) captures all possibilities.
- If you can find a counter-example in 2 minutes with a tiny input, it is **not** greedy - use DP.

## 2. How to spot it
- "minimum number of ...", "maximum number of ... that fit", "is it possible to reach / complete".
- Sorting + one sweep solves it; or a running frontier (`farthest`, `tank`, `end`).
- Choices are *independent* once you pick an order.

## 3. Paper recipe
1. Try 3 small inputs by hand and guess a rule ("always take the earliest-finishing").
2. Attack the rule with an adversarial input (equal values, big then small, zeros).
3. Write the one-sentence proof (exchange / stays-ahead). No proof -> suspect DP.
4. Decide the sort key (if any) and the state variable(s) you carry.
5. Code the single pass; test empty / single / all-equal.

## 4. Hand trace
{{trace:jump_game}}

## 5. Template
{{solution:greedy/1}}

## 6. Traps
- Assuming greedy works because it passes the samples (Coin Change with [1,3,4] and amount 6).
- Sorting by the wrong key.
- Missing the global feasibility check (Gas Station: total gas >= total cost).
- Ties: decide what to do when two choices look equal.

## 7. Self-check
1. Give a counter-example showing greedy fails for Coin Change with coins [1,3,4].
2. State the exchange argument for "sort intervals by end".
3. Which pattern in this repo is greedy + a heap? (Task Scheduler, Reorganize String, Meeting Rooms II.)

## 8. Practice ladder
{{ladder}}

**More:** 455 Assign Cookies (E), 860 Lemonade Change (E), 45 Jump Game II (M), 1029 Two City Scheduling (M), 406 Queue Reconstruction by Height (M), 621 Task Scheduler (M), 135 Candy (H), 330 Patching Array (H), 767 Reorganize String (M), 402 Remove K Digits (M).
