# 49. Group Anagrams

**Difficulty:** Medium
**Topics:** Array, Hash Table, String, Sorting
**Common companies:** Google, Amazon
**Category (README):** 2. String

## Problem Description

Given an array of strings `strs`, group the anagrams together. You can return the answer in **any order**.

 

**Example 1:**

**Input:** strs = ["eat","tea","tan","ate","nat","bat"]

**Output:** [["bat"],["nat","tan"],["ate","eat","tea"]]

**Explanation:**

	
- There is no string in strs that can be rearranged to form `"bat"`.

	
- The strings `"nat"` and `"tan"` are anagrams as they can be rearranged to form each other.

	
- The strings `"ate"`, `"eat"`, and `"tea"` are anagrams as they can be rearranged to form each other.

**Example 2:**

**Input:** strs = [""]

**Output:** [[""]]

**Example 3:**

**Input:** strs = ["a"]

**Output:** [["a"]]

 

**Constraints:**

	
- `1 <= strs.length <= 104`

	
- `0 <= strs[i].length <= 100`

	
- `strs[i]` consists of lowercase English letters.

## Key Idea

Sorted string / character count as the hash key

## Approach

1. Identify the core pattern for this category: **2. String**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n * k) — where `n` is the number of strings and `k` is the max string length; using a 26-count tuple as the key avoids the O(k log k) sort per string.
**Space Complexity:** O(n * k) — to store all strings grouped in the hash map.

## Reference Solution (Python)

```python
from collections import defaultdict


def groupAnagrams(strs: list[str]) -> list[list[str]]:
    groups: dict[tuple[int, ...], list[str]] = defaultdict(list)

    for s in strs:
        count = [0] * 26
        for ch in s:
            count[ord(ch) - ord('a')] += 1
        groups[tuple(count)].append(s)

    return list(groups.values())
```

## Reference

- LeetCode: https://leetcode.com/problems/group-anagrams/
