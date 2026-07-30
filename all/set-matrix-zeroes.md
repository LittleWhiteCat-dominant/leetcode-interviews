# 73. Set Matrix Zeroes

**Difficulty:** Medium
**Topics:** Array, Hash Table, Matrix
**Common companies:** Amazon, Apple
**Category (README):** 1.6 Matrix

## Problem Description

Given an `m x n` integer matrix `matrix`, if an element is `0`, set its entire row and column to `0`'s.

You must do it in place.

 

**Example 1:**

```

**Input:** matrix = [[1,1,1],[1,0,1],[1,1,1]]
**Output:** [[1,0,1],[0,0,0],[1,0,1]]

```

**Example 2:**

```

**Input:** matrix = [[0,1,2,0],[3,4,5,2],[1,3,1,5]]
**Output:** [[0,0,0,0],[0,4,5,0],[0,3,1,0]]

```

 

**Constraints:**

	
- `m == matrix.length`

	
- `n == matrix[0].length`

	
- `1 <= m, n <= 200`

	
- `-231 <= matrix[i][j] <= 231 - 1`

 

**Follow up:**

	
- A straightforward solution using `O(mn)` space is probably a bad idea.

	
- A simple improvement uses `O(m + n)` space, but still not the best solution.

	
- Could you devise a constant space solution?

## Key Idea

Use the first row/column as markers for O(1) extra space

## Approach

1. Identify the core pattern for this category: **1.6 Matrix**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/set-matrix-zeroes/
