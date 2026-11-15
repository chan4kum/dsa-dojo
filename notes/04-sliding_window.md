# 04 - Sliding window

> **One idea:** keep a window `[l, r]` that always satisfies an invariant; extend `r` every step, move `l` only to repair the invariant.

## 1. First principles
- It is two pointers that move in the **same direction**, over a **contiguous** range.
- State per window is updated in O(1) (add the entering element, remove the leaving one), so the whole scan is O(n).
- **Fixed-size window:** size k never changes; slide by one.
- **Variable window - find longest:** expand always, shrink *while invalid*; record the best after repairing.
- **Variable window - find shortest:** expand until valid, then shrink *while still valid*, recording each time.
- Needs **monotonicity**: adding elements can only push the window toward invalid (or valid) in one direction. Negative numbers usually break it (use prefix sums).

## 2. How to spot it
- "longest / shortest / maximum / minimum **substring or subarray** such that ..."
- "contiguous", "at most k distinct", "no repeating", "contains all characters".
- Brute force enumerates all `(i, j)` and re-checks the window.

## 3. Paper recipe
1. Write the invariant in words ("window has no duplicates", "sum >= target", "covers all of t").
2. List what state you need to test it in O(1): a set, a counter, a running sum, a count of missing characters.
3. Decide: grow until valid then shrink (shortest) or grow then shrink until valid again (longest).
4. Write both update rules: **add `s[r]`**, **remove `s[l]`**.
5. Exactly-k trick: `exactly(k) = atMost(k) - atMost(k-1)`.

## 4. Hand trace
`s = "abcabcbb"`

| r | s[r] | what happened | l | window | best |
|---|---|---|---|---|---|
| 0 | a | - | 0 | 'a' | 1 |
| 1 | b | - | 0 | 'ab' | 2 |
| 2 | c | - | 0 | 'abc' | 3 |
| 3 | a | 'a' last seen at 0 (inside window) -> l = 1 | 1 | 'bca' | 3 |
| 4 | b | 'b' last seen at 1 (inside window) -> l = 2 | 2 | 'cab' | 3 |
| 5 | c | 'c' last seen at 2 (inside window) -> l = 3 | 3 | 'abc' | 3 |
| 6 | b | 'b' last seen at 4 (inside window) -> l = 5 | 5 | 'cb' | 3 |
| 7 | b | 'b' last seen at 6 (inside window) -> l = 7 | 7 | 'b' | 3 |

## 5. Template
*Reference solution for **Longest Substring Without Repeating Characters** (`sliding_window/2`) - tested by `python dsa.py selftest`:*

```python
# OPTIMISED: O(n) time, O(min(n, alphabet)) space
# Idea: Variable-size sliding window with a 'last seen' map (expand right, shrink left to
#       restore validity)
def length_of_longest_substring(s):
    last = {}
    left = best = 0
    for r, c in enumerate(s):
        if c in last and last[c] >= left:  # duplicate inside the window
            left = last[c] + 1
        last[c] = r
        best = max(best, r - left + 1)
    return best
```

## 6. Traps
- Using `l = last[c] + 1` without `max(l, ...)` (stale entries from before the window).
- Updating the answer before the window is repaired.
- Counter that goes negative on purpose (Minimum Window) - know *why*.
- Fixed window: off-by-one on the first window (`i >= k - 1`).

## 7. Self-check
1. Why does shrinking with `while` not make it O(n^2)?
2. Why can't you use a sliding window for "subarray sum equals k" with negatives?
3. How do you count subarrays with exactly K distinct integers using only "at most K"?

## 8. Practice ladder
| id | difficulty | problem | LeetCode | pattern it trains |
|---|---|---|---|---|
| `sliding_window/1` | Easy | Maximum Average Subarray I | [#643](https://leetcode.com/problems/maximum-average-subarray-i/) | Fixed-size sliding window (add the entering element, remove the leaving one) |
| `sliding_window/5` | Easy | Best Time to Buy and Sell Stock | [#121](https://leetcode.com/problems/best-time-to-buy-and-sell-stock/) | Running minimum (one-pass 'best so far' scan) |
| `sliding_window/25` | Easy | Minimum Recolors to Get K Consecutive Black Blocks | [#2379](https://leetcode.com/problems/minimum-recolors-to-get-k-consecutive-black-blocks/) | Fixed-size sliding window |
| `sliding_window/29` | Easy | Minimum Difference Between Highest and Lowest of K Scores | [#1984](https://leetcode.com/problems/minimum-difference-between-highest-and-lowest-of-k-scores/) | Sort + fixed-size window |
| `sliding_window/36` | Easy | Substrings of Size Three with Distinct Characters | [#1876](https://leetcode.com/problems/substrings-of-size-three-with-distinct-characters/) | Fixed-size sliding window with a letter counter |
| `sliding_window/45` | Easy | Maximum Length Substring With Two Occurrences | [#3090](https://leetcode.com/problems/maximum-length-substring-with-two-occurrences/) | Variable-size sliding window with per-character caps |
| `sliding_window/2` | Medium | Longest Substring Without Repeating Characters | [#3](https://leetcode.com/problems/longest-substring-without-repeating-characters/) | Variable-size sliding window with a 'last seen' map (expand right, shrink left to restore validity) |
| `sliding_window/3` | Medium | Minimum Size Subarray Sum | [#209](https://leetcode.com/problems/minimum-size-subarray-sum/) | Variable window that SHRINKS while the condition holds (needs non-negative values) |
| `sliding_window/6` | Medium | Longest Repeating Character Replacement | [#424](https://leetcode.com/problems/longest-repeating-character-replacement/) | Sliding window with a validity condition (length - max_freq <= k) |
| `sliding_window/7` | Medium | Permutation in String | [#567](https://leetcode.com/problems/permutation-in-string/) | Fixed-size sliding window + frequency map comparison |
| `sliding_window/8` | Medium | Find All Anagrams in a String | [#438](https://leetcode.com/problems/find-all-anagrams-in-a-string/) | Fixed-size sliding window + frequency map |
| `sliding_window/9` | Medium | Max Consecutive Ones III | [#1004](https://leetcode.com/problems/max-consecutive-ones-iii/) | Sliding window: 'at most k bad items' |
| `sliding_window/10` | Medium | Subarray Product Less Than K | [#713](https://leetcode.com/problems/subarray-product-less-than-k/) | Variable sliding window, counting subarrays ending at r |
| `sliding_window/11` | Medium | Fruit Into Baskets | [#904](https://leetcode.com/problems/fruit-into-baskets/) | Variable window with a count map (at most K distinct) |
| `sliding_window/12` | Medium | Longest Subarray of 1's After Deleting One Element | [#1493](https://leetcode.com/problems/longest-subarray-of-1s-after-deleting-one-element/) | Variable window with at most K = 1 violations |
| `sliding_window/13` | Medium | Maximum Number of Vowels in a Substring of Given Length | [#1456](https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/) | Fixed-size sliding window with a running count |
| `sliding_window/14` | Medium | Grumpy Bookstore Owner | [#1052](https://leetcode.com/problems/grumpy-bookstore-owner/) | Fixed-size sliding window maximising the extra gain |
| `sliding_window/15` | Medium | Binary Subarrays With Sum | [#930](https://leetcode.com/problems/binary-subarrays-with-sum/) | Prefix sum + hash map of counts |
| `sliding_window/17` | Medium | Get Equal Substrings Within Budget | [#1208](https://leetcode.com/problems/get-equal-substrings-within-budget/) | Variable-size sliding window (non-negative values) |
| `sliding_window/18` | Medium | Count Number of Nice Subarrays | [#1248](https://leetcode.com/problems/count-number-of-nice-subarrays/) | Exactly k = atMost(k) - atMost(k - 1) |
| `sliding_window/19` | Medium | Number of Substrings Containing All Three Characters | [#1358](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/) | Count by right endpoint using last-seen positions |
| `sliding_window/20` | Medium | Maximum Points You Can Obtain from Cards | [#1423](https://leetcode.com/problems/maximum-points-you-can-obtain-from-cards/) | Fixed-size window over a circular view of the ends |
| `sliding_window/21` | Medium | Longest Continuous Subarray With Absolute Diff Less Than or Equal to Limit | [#1438](https://leetcode.com/problems/longest-continuous-subarray-with-absolute-diff-less-than-or-equal-to-limit/) | Sliding window + monotonic deques for min and max |
| `sliding_window/22` | Medium | Maximum Erasure Value | [#1695](https://leetcode.com/problems/maximum-erasure-value/) | Sliding window with a set (unique elements) |
| `sliding_window/23` | Medium | Minimum Operations to Reduce X to Zero | [#1658](https://leetcode.com/problems/minimum-operations-to-reduce-x-to-zero/) | Complement trick: longest middle subarray with a target sum |
| `sliding_window/24` | Medium | Maximize the Confusion of an Exam | [#2024](https://leetcode.com/problems/maximize-the-confusion-of-an-exam/) | Longest window with at most k 'bad' elements (run for both targets) |
| `sliding_window/26` | Medium | Number of Sub-arrays of Size K and Average Greater than or Equal to Threshold | [#1343](https://leetcode.com/problems/number-of-sub-arrays-of-size-k-and-average-greater-than-or-equal-to-threshold/) | Fixed-size sliding window sum |
| `sliding_window/27` | Medium | Maximum Sum of Distinct Subarrays With Length K | [#2461](https://leetcode.com/problems/maximum-sum-of-distinct-subarrays-with-length-k/) | Fixed window + frequency map |
| `sliding_window/28` | Medium | Length of Longest Subarray With at Most K Frequency | [#2958](https://leetcode.com/problems/length-of-longest-subarray-with-at-most-k-frequency/) | Variable window with a frequency cap |
| `sliding_window/30` | Medium | Longest Turbulent Subarray | [#978](https://leetcode.com/problems/longest-turbulent-subarray/) | Sliding window over the sequence of comparison signs |
| `sliding_window/31` | Medium | Swap For Longest Repeated Character Substring | [#1156](https://leetcode.com/problems/swap-for-longest-repeated-character-substring/) | Run-length groups + cap by total letter count |
| `sliding_window/32` | Medium | Replace the Substring for Balanced String | [#1234](https://leetcode.com/problems/replace-the-substring-for-balanced-string/) | Shrinkable window where the condition is on what is OUTSIDE it |
| `sliding_window/33` | Medium | Maximum Number of Occurrences of a Substring | [#1297](https://leetcode.com/problems/maximum-number-of-occurrences-of-a-substring/) | Fixed-size sliding window + a hash counter of window contents |
| `sliding_window/34` | Medium | Frequency of the Most Frequent Element | [#1838](https://leetcode.com/problems/frequency-of-the-most-frequent-element/) | Sort + sliding window with a cost constraint |
| `sliding_window/35` | Medium | Longest Substring Of All Vowels in Order | [#1839](https://leetcode.com/problems/longest-substring-of-all-vowels-in-order/) | Window that resets whenever monotonicity breaks |
| `sliding_window/37` | Medium | Minimum Swaps to Group All 1's Together II | [#2134](https://leetcode.com/problems/minimum-swaps-to-group-all-1s-together-ii/) | Fixed-size circular sliding window |
| `sliding_window/38` | Medium | Longest Nice Subarray | [#2401](https://leetcode.com/problems/longest-nice-subarray/) | Sliding window with a bitmask of occupied bits |
| `sliding_window/39` | Medium | Take K of Each Character From Left and Right | [#2516](https://leetcode.com/problems/take-k-of-each-character-from-left-and-right/) | Maximise a window while the complement satisfies a constraint |
| `sliding_window/40` | Medium | Find the Longest Semi-Repetitive Substring | [#2730](https://leetcode.com/problems/find-the-longest-semi-repetitive-substring/) | Sliding window with a bounded 'violation' counter |
| `sliding_window/41` | Medium | Continuous Subarrays | [#2762](https://leetcode.com/problems/continuous-subarrays/) | Sliding window with monotonic deques for max and min |
| `sliding_window/42` | Medium | Count Complete Subarrays in an Array | [#2799](https://leetcode.com/problems/count-complete-subarrays-in-an-array/) | 'At least' sliding window: count all extensions of the minimal valid window |
| `sliding_window/43` | Medium | Maximum Sum of Almost Unique Subarray | [#2841](https://leetcode.com/problems/maximum-sum-of-almost-unique-subarray/) | Fixed-size sliding window with a sum and a distinct counter |
| `sliding_window/44` | Medium | Count Subarrays Where Max Element Appears at Least K Times | [#2962](https://leetcode.com/problems/count-subarrays-where-max-element-appears-at-least-k-times/) | 'At least k' window: count valid starts per right end |
| `sliding_window/46` | Medium | Find the Power of K-Size Subarrays I | [#3254](https://leetcode.com/problems/find-the-power-of-k-size-subarrays-i/) | Fixed window answered by a running 'streak length' |
| `sliding_window/4` | Hard | Minimum Window Substring | [#76](https://leetcode.com/problems/minimum-window-substring/) | Variable window: expand until valid, then shrink to the minimum while still valid |
| `sliding_window/16` | Hard | Subarrays with K Different Integers | [#992](https://leetcode.com/problems/subarrays-with-k-different-integers/) | Exactly K = atMost(K) - atMost(K - 1) |

Start one with `python dsa.py start sliding_window/1`.

**More:** 121 Best Time to Buy and Sell Stock (E), 424 Longest Repeating Character Replacement (M), 567 Permutation in String (M), 438 Find All Anagrams in a String (M), 904 Fruit Into Baskets (M), 1004 Max Consecutive Ones III (M), 713 Subarray Product Less Than K (M), 992 Subarrays with K Different Integers (H), 239 Sliding Window Maximum (H, see stack_monotonic).

## 9. Make it stay - the teacher's anchors

**Picture it.** A caterpillar: the head eats forward (extend right), and when the window is poisoned (invalid) the tail retreats until it is safe again.

**The rule in one sentence.** Contiguous subarray/substring + a validity condition that only gets worse as the window grows => expand right, shrink left while invalid.

**Why it works.** Every element enters once and leaves once, so the two pointers move at most 2n steps in total - amortised O(n) even though there is a loop inside the loop.

**Teach it back (say it aloud in under a minute - if you can't, you don't own it yet).**
1. What exact condition makes a window 'valid' in Longest Substring Without Repeating?
2. Fixed-size vs variable-size windows: when do you use which?
3. Why is the nested while loop still O(n)?

**Mistakes students make most.**
- Shrinking only once instead of `while invalid`.
- Updating the answer at the wrong moment (before/after shrinking).
- Using a window when negatives break monotonicity (use prefix sums + hash).

**When NOT to use it.** The validity condition is not monotone (a larger window can become valid again) or you need non-contiguous selections.

**The same idea in disguise.** Max average subarray (fixed) -> longest unique substring -> min size subarray sum -> min window substring -> longest repeating replacement -> permutation in string.
