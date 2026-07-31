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

This is solved with **expand-around-center**:

1. Every palindrome has a center, which is either a single character (odd-length palindrome) or the gap between two characters (even-length palindrome), giving `2n - 1` possible centers.
2. For each center, expand outward with a `left`/`right` pointer pair as long as `s[left] == s[right]` and both indices stay in bounds.
3. Each successful expansion step confirms one more palindromic substring, so increment a running counter each time the condition holds.
4. Call the expansion helper twice per index `i`: once with `(i, i)` for odd-length palindromes centered on a character, and once with `(i, i + 1)` for even-length palindromes centered between characters.
5. Sum the counts across all centers to get the total number of palindromic substrings.

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
