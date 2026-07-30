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

1. Identify the core pattern for this category: **1.6 Matrix**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
