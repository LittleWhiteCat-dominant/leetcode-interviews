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

This is solved with **a two-pointer scan that branches once on the first mismatch**:

1. Move `left` and `right` inward from both ends while characters match.
2. As soon as a mismatch `s[left] != s[right]` is found, the answer depends on whether skipping exactly one of these two characters yields a palindrome.
3. Check both possibilities: is `s[left+1..right]` a palindrome, or is `s[left..right-1]` a palindrome?
4. Return `true` if either sub-range check succeeds.
5. If the two pointers cross without ever mismatching, `s` is already a palindrome, so return `true` directly.

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
