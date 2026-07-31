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

This is solved with **expand-around-center, trying every possible palindrome center**:

1. For each index `i`, there are two kinds of centers to check: odd-length palindromes centered at `i` (`expand(i, i)`) and even-length palindromes centered between `i` and `i + 1` (`expand(i, i + 1)`).
2. `expand(left, right)` grows outward while the characters at `left` and `right` match, then returns the bounds of the widest palindrome found for that center.
3. After each expansion, compare its length to the best palindrome recorded so far (`start`, `end`) and update if it's longer.
4. Repeat for every index, then return `s[start:end + 1]` as the longest palindromic substring.

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
