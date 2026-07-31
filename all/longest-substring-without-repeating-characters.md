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

This is solved with **a sliding window tracking the last-seen index of each character**:

1. Maintain a hash map `last_seen` mapping each character to the most recent index at which it appeared, and a `left` pointer marking the start of the current window.
2. As `right` scans through the string, if the current character was seen before at or after `left`, jump `left` to `last_seen[ch] + 1` to exclude the earlier duplicate from the window.
3. Update `last_seen[ch]` to the current index `right`.
4. After each step, update the running maximum with the current window length `right - left + 1`.

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
