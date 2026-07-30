# 647. Palindromic Substrings

**Difficulty:** Medium
**Topics:** Two Pointers, String, Dynamic Programming
**Common companies:** Amazon, Google
**Category (README):** 2. String

## Problem Description

Given a string `s`, return *the number of **palindromic substrings** in it*.

A string is a **palindrome** when it reads the same backward as forward.

A **substring** is a contiguous sequence of characters within the string.

 

**Example 1:**

```

**Input:** s = "abc"
**Output:** 3
**Explanation:** Three palindromic strings: "a", "b", "c".

```

**Example 2:**

```

**Input:** s = "aaa"
**Output:** 6
**Explanation:** Six palindromic strings: "a", "a", "a", "aa", "aa", "aaa".

```

 

**Constraints:**

	
- `1 <= s.length <= 1000`

	
- `s` consists of lowercase English letters.

## Key Idea

Expand around center, counting palindromes

## Approach

1. Identify the core pattern for this category: **2. String**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n^2) — expanding around each of the 2n - 1 centers takes up to O(n).
**Space Complexity:** O(1) — only a running counter and pointers are used.

## Reference Solution (Python)

```python
def countSubstrings(s: str) -> int:
    n = len(s)
    count = 0

    def expand(left: int, right: int) -> None:
        nonlocal count
        while left >= 0 and right < n and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1

    for center in range(n):
        expand(center, center)
        expand(center, center + 1)

    return count
```

## Reference

- LeetCode: https://leetcode.com/problems/palindromic-substrings/
