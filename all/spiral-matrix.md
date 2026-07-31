# 54. Spiral Matrix

**Difficulty:** Medium
**Topics:** Array, Matrix, Simulation
**Common companies:** All big tech
**Category (README):** 1.6 Matrix

## Problem Description

Given an `m x n` `matrix`, return *all elements of the* `matrix` *in spiral order*.

 

**Example 1:**

```

**Input:** matrix = [[1,2,3],[4,5,6],[7,8,9]]
**Output:** [1,2,3,6,9,8,7,4,5]

```

**Example 2:**

```

**Input:** matrix = [[1,2,3,4],[5,6,7,8],[9,10,11,12]]
**Output:** [1,2,3,4,8,12,11,10,9,5,6,7]

```

 

**Constraints:**

	
- `m == matrix.length`

	
- `n == matrix[i].length`

	
- `1 <= m, n <= 10`

	
- `-100 <= matrix[i][j] <= 100`

## Key Idea

Maintain top/bottom/left/right boundaries, shrinking layer by layer

## Approach

This is solved with **shrinking boundary pointers traced in a repeating four-direction cycle**:

1. Track four boundaries: `top`, `bottom`, `left`, `right`, initialized to the matrix's outer edges.
2. Traverse the top row from `left` to `right`, then move `top` down by one.
3. Traverse the right column from `top` to `bottom`, then move `right` left by one.
4. If `top <= bottom` still holds, traverse the bottom row from `right` to `left`, then move `bottom` up by one.
5. If `left <= right` still holds, traverse the left column from `bottom` to `top`, then move `left` right by one.
6. Repeat this four-step cycle while `top <= bottom and left <= right`, appending each visited value to the result list.

**Time Complexity:** O(m * n) — every cell is visited exactly once.
**Space Complexity:** O(1) extra space — only four boundary pointers, excluding the output list.

## Reference Solution (Python)

```python
def spiralOrder(matrix: list[list[int]]) -> list[int]:
    result = []
    top, bottom = 0, len(matrix) - 1
    left, right = 0, len(matrix[0]) - 1

    while top <= bottom and left <= right:
        for c in range(left, right + 1):
            result.append(matrix[top][c])
        top += 1

        for r in range(top, bottom + 1):
            result.append(matrix[r][right])
        right -= 1

        if top <= bottom:
            for c in range(right, left - 1, -1):
                result.append(matrix[bottom][c])
            bottom -= 1

        if left <= right:
            for r in range(bottom, top - 1, -1):
                result.append(matrix[r][left])
            left += 1

    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/spiral-matrix/
