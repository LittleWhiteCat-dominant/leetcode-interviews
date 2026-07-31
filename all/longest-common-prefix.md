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

This is solved with **vertical scanning via `zip(*strs)` to compare characters column by column**:

1. Handle the empty-input edge case up front by returning `""`.
2. Use `zip(*strs)` to iterate over the strings column by column, where each `chars` tuple holds one character from every string at that position.
3. As soon as a column contains more than one distinct character (`len(set(chars)) > 1`), the common prefix ends there, so return `strs[0][:i]`.
4. If every column matches across all strings (loop completes without returning), the shortest string is itself the full common prefix, so return `min(strs, key=len)`.

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
