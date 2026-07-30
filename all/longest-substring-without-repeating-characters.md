# 3. Longest Substring Without Repeating Characters

**Difficulty:** Medium
**Topics:** Hash Table, String, Sliding Window
**Common companies:** All big tech
**Category (README):** 1.2 Sliding Window

## Problem Description

Given a string `s`, find the length of the **longest** **substring** without duplicate characters.

 

**Example 1:**

```

**Input:** s = "abcabcbb"
**Output:** 3
**Explanation:** The answer is "abc", with the length of 3. Note that `"bca"` and `"cab"` are also correct answers.

```

**Example 2:**

```

**Input:** s = "bbbbb"
**Output:** 1
**Explanation:** The answer is "b", with the length of 1.

```

**Example 3:**

```

**Input:** s = "pwwkew"
**Output:** 3
**Explanation:** The answer is "wke", with the length of 3.
Notice that the answer must be a substring, "pwke" is a subsequence and not a substring.

```

 

**Constraints:**

	
- `0 <= s.length <= 105`

	
- `s` consists of English letters, digits, symbols and spaces.

## Key Idea

Hash map inside the window tracking last-seen index

## Approach

1. Identify the core pattern for this category: **1.2 Sliding Window**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — each character is visited once as the right pointer scans the string, with O(1) hash map operations.
**Space Complexity:** O(min(n, m)) — where m is the size of the character set, for the last-seen-index hash map.

## Reference Solution (Python)

```python
def lengthOfLongestSubstring(s: str) -> int:
    last_seen: dict[str, int] = {}
    left = 0
    longest = 0

    for right, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= left:
            left = last_seen[ch] + 1
        last_seen[ch] = right
        longest = max(longest, right - left + 1)

    return longest
```

## Reference

- LeetCode: https://leetcode.com/problems/longest-substring-without-repeating-characters/
