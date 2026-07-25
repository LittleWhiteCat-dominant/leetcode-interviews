# 1668. Maximum Repeating Substring

**Difficulty:** Easy
**Topics:** String, Array, String Matching, Sliding Window, Dynamic Programming
**Reported at Asana:** Confirmed — reported as a coding-round question in a candidate interview report.

## Problem Description

For a string `sequence`, a string `word` is `k`-repeating if `word` concatenated `k` times is a substring of `sequence`. The `word`'s **maximum** `k`-repeating value is the highest value `k` where `word` is `k`-repeating in `sequence`. If `word` is not a substring of `sequence`, `word`'s maximum `k`-repeating value is `0`.

Given strings `sequence` and `word`, return *the **maximum** `k`-repeating value of `word` in `sequence`*.

## Example 1

```
Input: sequence = "ababc", word = "ab"
Output: 2
Explanation: "abab" is a substring in "ababc".
```

## Example 2

```
Input: sequence = "ababc", word = "ba"
Output: 1
Explanation: "ba" is a substring in "ababc". "baba" is not a substring in "ababc".
```

## Example 3

```
Input: sequence = "ababc", word = "ac"
Output: 0
Explanation: "ac" is not a substring in "ababc".
```

## Constraints

- `1 <= sequence.length <= 100`
- `1 <= word.length <= 100`
- `sequence` and `word` contain only lowercase English letters.

## Approach

1. Since the constraints are small (`length <= 100`), the simplest approach is to build `word * k` incrementally and check whether it is a substring of `sequence`, increasing `k` until the check fails.
2. Start `k = 1`. While `word * (k + 1)` is a substring of `sequence`, increment `k`. Once it stops being a substring, return the current `k` (or `0` if `word` itself is never found).
3. For larger inputs, this could be optimized using KMP-based substring search or by directly counting the longest run of consecutive `word` occurrences.

**Time Complexity:** O(n²) in the worst case for the naive substring check (small enough given `n <= 100`); can be reduced to O(n · m) or better with more careful string matching.
**Space Complexity:** O(n) for the repeated string construction.

## Reference Solution (Python)

```python
def max_repeating(sequence: str, word: str) -> int:
    k = 0
    repeated = word
    while repeated in sequence:
        k += 1
        repeated += word
    return k
```

## Follow-up Questions Interviewers May Ask

- How would this scale if `sequence` and `word` could each be up to `10^6` characters long?
- Can you solve it using the KMP algorithm to avoid rebuilding the repeated string each time?
- How would you find the maximum repeating value for **every** possible `word` substring of `sequence` simultaneously?
