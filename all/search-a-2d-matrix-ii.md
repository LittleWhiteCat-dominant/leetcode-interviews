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

This is solved with **a staircase search starting from the top-right corner**:

1. Start at the top-right corner of the matrix, where moving left decreases the value and moving down increases it.
2. Compare the current cell to `target`: if it matches, return `True` immediately.
3. If the current value is greater than `target`, the entire column below is too big, so move one column left.
4. If the current value is less than `target`, the entire row to the left is too small, so move one row down.
5. If the pointer walks off the matrix (row out of bounds or column negative) without a match, `target` is not present, so return `False`.

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
