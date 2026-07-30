# 680. Valid Palindrome II

**Difficulty:** Easy
**Topics:** Two Pointers, String, Greedy
**Common companies:** **Meta favorite**
**Category (README):** 1.1 Two Pointers

## Problem Description

Given a string `s`, return `true` *if the *`s`* can be palindrome after deleting **at most one** character from it*.

 

**Example 1:**

```

**Input:** s = "aba"
**Output:** true

```

**Example 2:**

```

**Input:** s = "abca"
**Output:** true
**Explanation:** You could delete the character 'c'.

```

**Example 3:**

```

**Input:** s = "abc"
**Output:** false

```

 

**Constraints:**

	
- `1 <= s.length <= 105`

	
- `s` consists of lowercase English letters.

## Key Idea

Allow skipping one mismatched character then re-verify

## Approach

1. Identify the core pattern for this category: **1.1 Two Pointers**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — the two-pointer scan runs once, and at most one extra O(n) palindrome check is triggered on the first mismatch.
**Space Complexity:** O(1) — only pointer indices are used, no extra data structures.

## Reference Solution (Python)

```python
def validPalindrome(s: str) -> bool:
    def is_palindrome_range(i: int, j: int) -> bool:
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return is_palindrome_range(left + 1, right) or is_palindrome_range(left, right - 1)
        left += 1
        right -= 1

    return True
```

## Reference

- LeetCode: https://leetcode.com/problems/valid-palindrome-ii/
