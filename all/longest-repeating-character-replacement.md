# 424. Longest Repeating Character Replacement

**Difficulty:** Medium
**Topics:** Hash Table, String, Sliding Window
**Common companies:** Google, Meta
**Category (README):** 1.2 Sliding Window

## Problem Description

You are given a string `s` and an integer `k`. You can choose any character of the string and change it to any other uppercase English character. You can perform this operation at most `k` times.

Return *the length of the longest substring containing the same letter you can get after performing the above operations*.

 

**Example 1:**

```

**Input:** s = "ABAB", k = 2
**Output:** 4
**Explanation:** Replace the two 'A's with two 'B's or vice versa.

```

**Example 2:**

```

**Input:** s = "AABABBA", k = 1
**Output:** 4
**Explanation:** Replace the one 'A' in the middle with 'B' and form "AABBBBA".
The substring "BBBB" has the longest repeating letters, which is 4.
There may exists other ways to achieve this answer too.
```

 

**Constraints:**

	
- `1 <= s.length <= 105`

	
- `s` consists of only uppercase English letters.

	
- `0 <= k <= s.length`

## Key Idea

Window allowing up to k replacements

## Approach

This is solved with **a sliding window that tracks the count of the most frequent character inside it**:

1. Expand the window by moving `right` forward, incrementing the count of `s[right]` and updating `max_count`, the highest frequency of any single character seen in the current window.
2. The window is valid as long as `(window length) - max_count <= k`, meaning at most `k` characters need to be replaced to make the whole window a single repeated letter.
3. If the window becomes invalid, shrink it from the left by incrementing `left` and decrementing the count of `s[left]` (note `max_count` is never decreased, since a smaller window can never beat a previously found valid length).
4. Track the maximum window size seen at any point as the answer.

**Time Complexity:** O(n) — the sliding window's left and right pointers each move forward at most n times.
**Space Complexity:** O(1) — the character counts table has a fixed size of 26.

## Reference Solution (Python)

```python
from collections import Counter


def characterReplacement(s: str, k: int) -> int:
    counts = Counter()
    left = 0
    max_count = 0
    result = 0

    for right, ch in enumerate(s):
        counts[ch] += 1
        max_count = max(max_count, counts[ch])

        while (right - left + 1) - max_count > k:
            counts[s[left]] -= 1
            left += 1

        result = max(result, right - left + 1)

    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/longest-repeating-character-replacement/
