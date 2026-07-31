# 567. Permutation in String

**Difficulty:** Medium
**Topics:** Hash Table, Two Pointers, String, Sliding Window
**Common companies:** **Meta favorite**
**Category (README):** 1.2 Sliding Window

## Problem Description

Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`, or `false` otherwise.

In other words, return `true` if one of `s1`'s permutations is the substring of `s2`.

 

**Example 1:**

```

**Input:** s1 = "ab", s2 = "eidbaooo"
**Output:** true
**Explanation:** s2 contains one permutation of s1 ("ba").

```

**Example 2:**

```

**Input:** s1 = "ab", s2 = "eidboaoo"
**Output:** false

```

 

**Constraints:**

	
- `1 <= s1.length, s2.length <= 104`

	
- `s1` and `s2` consist of lowercase English letters.

## Key Idea

Fixed-size window + character frequency comparison

## Approach

This is solved with a **fixed-size sliding window and character frequency counters**:

1. A permutation of `s1` existing as a substring of `s2` is equivalent to some window of length `len(s1)` in `s2` having the exact same character counts as `s1`.
2. Build a frequency counter `need` for `s1`, and a counter `window` for the first `len(s1)` characters of `s2`.
3. If `window == need` already, return `true` immediately.
4. Slide the window one character at a time: increment the count of the character entering the window, decrement the count of the character leaving it (removing it from the counter entirely if its count drops to 0, so the comparison stays exact).
5. After each slide, compare `window == need`; if they match at any point, a permutation was found and we return `true`.
6. If the window slides through the whole string without a match, return `false`.

**Time Complexity:** O(n) — where n is the length of `s2`; the fixed-size window slides once across it.
**Space Complexity:** O(1) — the frequency counters are bounded by 26 lowercase letters.

## Reference Solution (Python)

```python
from collections import Counter

def checkInclusion(s1: str, s2: str) -> bool:
    n1, n2 = len(s1), len(s2)
    if n1 > n2:
        return False

    need = Counter(s1)
    window = Counter(s2[:n1])

    if window == need:
        return True

    for i in range(n1, n2):
        window[s2[i]] += 1
        left_char = s2[i - n1]
        window[left_char] -= 1
        if window[left_char] == 0:
            del window[left_char]
        if window == need:
            return True

    return False
```

## Reference

- LeetCode: https://leetcode.com/problems/permutation-in-string/
