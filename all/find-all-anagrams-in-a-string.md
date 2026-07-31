# 438. Find All Anagrams in a String

**Difficulty:** Medium
**Topics:** Hash Table, String, Sliding Window
**Common companies:** Google, Meta
**Category (README):** 1.2 Sliding Window

## Problem Description

Given two strings `s` and `p`, return an array of all the start indices of `p`'s anagrams in `s`. You may return the answer in **any order**.

 

**Example 1:**

```

**Input:** s = "cbaebabacd", p = "abc"
**Output:** [0,6]
**Explanation:**
The substring with start index = 0 is "cba", which is an anagram of "abc".
The substring with start index = 6 is "bac", which is an anagram of "abc".

```

**Example 2:**

```

**Input:** s = "abab", p = "ab"
**Output:** [0,1,2]
**Explanation:**
The substring with start index = 0 is "ab", which is an anagram of "ab".
The substring with start index = 1 is "ba", which is an anagram of "ab".
The substring with start index = 2 is "ab", which is an anagram of "ab".

```

 

**Constraints:**

	
- `1 <= s.length, p.length <= 3 * 104`

	
- `s` and `p` consist of lowercase English letters.

## Key Idea

Fixed-size window + character frequency comparison

## Approach

This is solved with **a fixed-size sliding window compared against a target frequency count**:

1. If `s` is shorter than `p`, no anagram can exist, so return an empty list immediately.
2. Build a 26-length count array `p_count` for the letters of `p`.
3. Slide a window of size `len(p)` across `s`, maintaining a running 26-length count array `s_count` for the current window: add the incoming character and remove the outgoing character once the window exceeds size `m`.
4. Whenever the window has reached full size, compare `s_count` to `p_count`; if they match, the current window start index is an anagram start.
5. Return all recorded start indices.

**Time Complexity:** O(n + m) — where `n = len(s)` and `m = len(p)`; each of the 26 letter counts is compared in O(1) as the window slides.
**Space Complexity:** O(1) — fixed-size arrays of 26 counters regardless of input size.

## Reference Solution (Python)

```python
def findAnagrams(s: str, p: str) -> list[int]:
    n, m = len(s), len(p)
    if n < m:
        return []

    p_count = [0] * 26
    s_count = [0] * 26

    for ch in p:
        p_count[ord(ch) - ord('a')] += 1

    result = []
    for i in range(n):
        s_count[ord(s[i]) - ord('a')] += 1
        if i >= m:
            s_count[ord(s[i - m]) - ord('a')] -= 1
        if i >= m - 1 and s_count == p_count:
            result.append(i - m + 1)

    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/find-all-anagrams-in-a-string/
