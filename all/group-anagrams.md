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

## Reference

- LeetCode: https://leetcode.com/problems/group-anagrams/
