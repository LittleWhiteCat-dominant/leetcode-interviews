# 567. Permutation in String

**Difficulty:** Medium
**Topics:** Hash Table, Two Pointers, String, Sliding Window
**Common companies:** **Meta favorite**
**Category (README):** 1.2 Sliding Window

## Problem Description

Given two strings `s1` and `s2`, return `true` if `s2` contains a permutation of `s1`, or `false` otherwise.

In other words, return `true` if one of `s1`'s permutations is the substring of `s2`.

 

**Example 1:**

```

**Input:** s1 = "ab", s2 = "eidbaooo"
**Output:** true
**Explanation:** s2 contains one permutation of s1 ("ba").

```

**Example 2:**

```

**Input:** s1 = "ab", s2 = "eidboaoo"
**Output:** false

```

 

**Constraints:**

	
- `1 <= s1.length, s2.length <= 104`

	
- `s1` and `s2` consist of lowercase English letters.

## Key Idea

Fixed-size window + character frequency comparison

## Approach

1. Identify the core pattern for this category: **1.2 Sliding Window**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/permutation-in-string/
