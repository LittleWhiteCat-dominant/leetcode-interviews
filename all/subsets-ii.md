# 90. Subsets II

**Difficulty:** Medium
**Topics:** Array, Backtracking, Bit Manipulation
**Common companies:** Amazon, Meta
**Category (README):** 11. Backtracking

## Problem Description

Given an integer array `nums` that may contain duplicates, return *all possible* *subsets** (the power set)*.

The solution set **must not** contain duplicate subsets. Return the solution in **any order**.

 

**Example 1:**

```
**Input:** nums = [1,2,2]
**Output:** [[],[1],[1,2],[1,2,2],[2],[2,2]]

```

**Example 2:**

```
**Input:** nums = [0]
**Output:** [[],[0]]

```

 

**Constraints:**

	
- `1 <= nums.length <= 10`

	
- `-10 <= nums[i] <= 10`

## Key Idea

Sort first, then skip duplicate elements at the same recursion level

## Approach

1. Identify the core pattern for this category: **11. Backtracking**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/subsets-ii/
