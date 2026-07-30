# 5. Longest Palindromic Substring

**Difficulty:** Medium
**Topics:** Two Pointers, String, Dynamic Programming
**Common companies:** All big tech
**Category (README):** 2. String

## Problem Description

Given a string `s`, return *the longest* *palindromic* *substring* in `s`.

 

**Example 1:**

```

**Input:** s = "babad"
**Output:** "bab"
**Explanation:** "aba" is also a valid answer.

```

**Example 2:**

```

**Input:** s = "cbbd"
**Output:** "bb"

```

 

**Constraints:**

	
- `1 <= s.length <= 1000`

	
- `s` consist of only digits and English letters.

## Key Idea

Expand around center, or interval DP

## Approach

1. Identify the core pattern for this category: **2. String**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n^2) — expanding around each of the 2n - 1 centers takes O(n) in the worst case.
**Space Complexity:** O(1) — only a few index variables are kept, excluding the output substring.

## Reference Solution (Python)

```python
def longestPalindrome(s: str) -> str:
    if not s:
        return ""

    start, end = 0, 0

    def expand(left: int, right: int) -> tuple[int, int]:
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return left + 1, right - 1

    for i in range(len(s)):
        l1, r1 = expand(i, i)
        if r1 - l1 > end - start:
            start, end = l1, r1
        l2, r2 = expand(i, i + 1)
        if r2 - l2 > end - start:
            start, end = l2, r2

    return s[start:end + 1]
```

## Reference

- LeetCode: https://leetcode.com/problems/longest-palindromic-substring/
