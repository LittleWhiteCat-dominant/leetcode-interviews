# 48. Rotate Image

**Difficulty:** Medium
**Topics:** Array, Math, Matrix
**Common companies:** All big tech
**Category (README):** 1.6 Matrix

## Problem Description

You are given an `n x n` 2D `matrix` representing an image, rotate the image by **90** degrees (clockwise).

You have to rotate the image **in-place**, which means you have to modify the input 2D matrix directly. **DO NOT** allocate another 2D matrix and do the rotation.

 

**Example 1:**

```

**Input:** matrix = [[1,2,3],[4,5,6],[7,8,9]]
**Output:** [[7,4,1],[8,5,2],[9,6,3]]

```

**Example 2:**

```

**Input:** matrix = [[5,1,9,11],[2,4,8,10],[13,3,6,7],[15,14,12,16]]
**Output:** [[15,13,2,5],[14,3,4,1],[12,6,8,9],[16,7,10,11]]

```

 

**Constraints:**

	
- `n == matrix.length == matrix[i].length`

	
- `1 <= n <= 20`

	
- `-1000 <= matrix[i][j] <= 1000`

## Key Idea

Transpose then reverse each row

## Approach

This is solved with **transpose followed by a horizontal flip**:

1. Transpose the matrix in place by swapping `matrix[i][j]` with `matrix[j][i]` for every pair with `j > i`.
2. After transposing, rows and columns are swapped, so a 90-degree clockwise rotation is completed by reversing each row.
3. Both steps operate directly on the input matrix, so no auxiliary matrix is ever allocated.

**Time Complexity:** O(n^2) — every cell is visited a constant number of times.
**Space Complexity:** O(1) — rotation is done in-place.

## Reference Solution (Python)

```python
def rotate(matrix: list[list[int]]) -> None:
    n = len(matrix)

    for i in range(n):
        for j in range(i + 1, n):
            matrix[i][j], matrix[j][i] = matrix[j][i], matrix[i][j]

    for row in matrix:
        row.reverse()
```

## Reference

- LeetCode: https://leetcode.com/problems/rotate-image/
