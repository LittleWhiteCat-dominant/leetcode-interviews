# 22. Generate Parentheses

**Difficulty:** Medium
**Topics:** String, Dynamic Programming, Backtracking
**Common companies:** Google, Meta
**Category (README):** 4.1 Basic Stack Applications

## Problem Description

Given `n` pairs of parentheses, write a function to *generate all combinations of well-formed parentheses*.

 

**Example 1:**

```
**Input:** n = 3
**Output:** ["((()))","(()())","(())()","()(())","()()()"]

```

**Example 2:**

```
**Input:** n = 1
**Output:** ["()"]

```

 

**Constraints:**

	
- `1 <= n <= 8`

## Key Idea

Backtracking + stack-style pruning (open count ≥ close count)

## Approach

1. Identify the core pattern for this category: **4.1 Basic Stack Applications**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/generate-parentheses/
