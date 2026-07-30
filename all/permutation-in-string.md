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

1. Identify the core pattern for this category: **1.2 Sliding Window**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
