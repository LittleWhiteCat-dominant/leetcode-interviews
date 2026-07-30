# 74. Search a 2D Matrix

**Difficulty:** Medium
**Topics:** Array, Binary Search, Matrix
**Common companies:** Amazon, Apple
**Category (README):** 1.4 Binary Search

## Problem Description

You are given an `m x n` integer matrix `matrix` with the following two properties:

	
- Each row is sorted in non-decreasing order.

	
- The first integer of each row is greater than the last integer of the previous row.

Given an integer `target`, return `true` *if* `target` *is in* `matrix` *or* `false` *otherwise*.

You must write a solution in `O(log(m * n))` time complexity.

 

**Example 1:**

```

**Input:** matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
**Output:** true

```

**Example 2:**

```

**Input:** matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
**Output:** false

```

 

**Constraints:**

	
- `m == matrix.length`

	
- `n == matrix[i].length`

	
- `1 <= m, n <= 100`

	
- `-104 <= matrix[i][j], target <= 104`

## Key Idea

Flatten to 1D binary search or start from a corner with two pointers

## Approach

1. Identify the core pattern for this category: **1.4 Binary Search**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/search-a-2d-matrix/
