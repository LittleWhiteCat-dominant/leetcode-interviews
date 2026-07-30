# 14. Longest Common Prefix

**Difficulty:** Easy
**Topics:** Array, String, Trie
**Common companies:** Google, Amazon
**Category (README):** 2. String

## Problem Description

Write a function to find the longest common prefix string amongst an array of strings.

If there is no common prefix, return an empty string `""`.

 

**Example 1:**

```

**Input:** strs = ["flower","flow","flight"]
**Output:** "fl"

```

**Example 2:**

```

**Input:** strs = ["dog","racecar","car"]
**Output:** ""
**Explanation:** There is no common prefix among the input strings.

```

 

**Constraints:**

	
- `1 <= strs.length <= 200`

	
- `0 <= strs[i].length <= 200`

	
- `strs[i]` consists of only lowercase English letters if it is non-empty.

## Key Idea

Vertical/horizontal scanning, or a Trie

## Approach

1. Identify the core pattern for this category: **2. String**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(S) — where S is the total number of characters across all strings, since each character is examined at most once.
**Space Complexity:** O(1) — excluding the output string, only a constant amount of extra space is used.

## Reference Solution (Python)

```python
def longestCommonPrefix(strs: list[str]) -> str:
    if not strs:
        return ""

    for i, chars in enumerate(zip(*strs)):
        if len(set(chars)) > 1:
            return strs[0][:i]

    return min(strs, key=len)
```

## Reference

- LeetCode: https://leetcode.com/problems/longest-common-prefix/
