# 131. Palindrome Partitioning

**Difficulty:** Medium
**Topics:** String, Dynamic Programming, Backtracking
**Common companies:** Amazon, Google
**Category (README):** 11. Backtracking

## Problem Description

Given a string `s`, partition `s` such that every substring of the partition is a **palindrome**. Return *all possible palindrome partitioning of *`s`.

 

**Example 1:**

```
**Input:** s = "aab"
**Output:** [["a","a","b"],["aa","b"]]

```

**Example 2:**

```
**Input:** s = "a"
**Output:** [["a"]]

```

 

**Constraints:**

	
- `1 <= s.length <= 16`

	
- `s` contains only lowercase English letters.

## Key Idea

Backtracking + palindrome check for pruning

## Approach

1. Identify the core pattern for this category: **11. Backtracking**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/palindrome-partitioning/
