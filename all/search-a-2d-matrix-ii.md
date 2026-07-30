# 240. Search a 2D Matrix II

**Difficulty:** Medium
**Topics:** Array, Binary Search, Divide and Conquer, Matrix
**Common companies:** Amazon, Apple
**Category (README):** 1.4 Binary Search

## Problem Description

Write an efficient algorithm that searches for a value `target` in an `m x n` integer matrix `matrix`. This matrix has the following properties:

	
- Integers in each row are sorted in ascending from left to right.

	
- Integers in each column are sorted in ascending from top to bottom.

 

**Example 1:**

```

**Input:** matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 5
**Output:** true

```

**Example 2:**

```

**Input:** matrix = [[1,4,7,11,15],[2,5,8,12,19],[3,6,9,16,22],[10,13,14,17,24],[18,21,23,26,30]], target = 20
**Output:** false

```

 

**Constraints:**

	
- `m == matrix.length`

	
- `n == matrix[i].length`

	
- `1 <= n, m <= 300`

	
- `-109 <= matrix[i][j] <= 109`

	
- All the integers in each row are **sorted** in ascending order.

	
- All the integers in each column are **sorted** in ascending order.

	
- `-109 <= target <= 109`

## Key Idea

Flatten to 1D binary search or start from a corner with two pointers

## Approach

1. Identify the core pattern for this category: **1.4 Binary Search**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(m + n) — the search pointer moves at most `m` times down and `n` times left.
**Space Complexity:** O(1) — only two index pointers are used.

## Reference Solution (Python)

```python
def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    rows, cols = len(matrix), len(matrix[0])
    row, col = 0, cols - 1

    while row < rows and col >= 0:
        if matrix[row][col] == target:
            return True
        if matrix[row][col] > target:
            col -= 1
        else:
            row += 1

    return False
```

## Reference

- LeetCode: https://leetcode.com/problems/search-a-2d-matrix-ii/
