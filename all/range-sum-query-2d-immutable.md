# 304. Range Sum Query 2D - Immutable

**Difficulty:** Medium
**Topics:** Array, Design, Matrix, Prefix Sum
**Common companies:** Google, Amazon
**Category (README):** 1.3 Prefix Sum

## Problem Description

Given a 2D matrix `matrix`, handle multiple queries of the following type:

	
- Calculate the **sum** of the elements of `matrix` inside the rectangle defined by its **upper left corner** `(row1, col1)` and **lower right corner** `(row2, col2)`.

Implement the `NumMatrix` class:

	
- `NumMatrix(int[][] matrix)` Initializes the object with the integer matrix `matrix`.

	
- `int sumRegion(int row1, int col1, int row2, int col2)` Returns the **sum** of the elements of `matrix` inside the rectangle defined by its **upper left corner** `(row1, col1)` and **lower right corner** `(row2, col2)`.

You must design an algorithm where `sumRegion` works on `O(1)` time complexity.

 

**Example 1:**

```

**Input**
["NumMatrix", "sumRegion", "sumRegion", "sumRegion"]
[[[[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]], [2, 1, 4, 3], [1, 1, 2, 2], [1, 2, 2, 4]]
**Output**
[null, 8, 11, 12]

**Explanation**
NumMatrix numMatrix = new NumMatrix([[3, 0, 1, 4, 2], [5, 6, 3, 2, 1], [1, 2, 0, 1, 5], [4, 1, 0, 1, 7], [1, 0, 3, 0, 5]]);
numMatrix.sumRegion(2, 1, 4, 3); // return 8 (i.e sum of the red rectangle)
numMatrix.sumRegion(1, 1, 2, 2); // return 11 (i.e sum of the green rectangle)
numMatrix.sumRegion(1, 2, 2, 4); // return 12 (i.e sum of the blue rectangle)

```

 

**Constraints:**

	
- `m == matrix.length`

	
- `n == matrix[i].length`

	
- `1 <= m, n <= 200`

	
- `-104 <= matrix[i][j] <= 104`

	
- `0 <= row1 <= row2 < m`

	
- `0 <= col1 <= col2 < n`

	
- At most `104` calls will be made to `sumRegion`.

## Key Idea

1D/2D prefix sum array

## Approach

This is solved with a **2D prefix-sum matrix**:

1. Precompute a `(m+1) x (n+1)` prefix matrix `prefix`, padded with an extra row and column of zeros so boundary lookups don't need special-casing.
2. Define `prefix[r+1][c+1]` as the sum of all cells `(0..r, 0..c)`, computed with inclusion-exclusion: `matrix[r][c] + prefix[r][c+1] + prefix[r+1][c] - prefix[r][c]` (the overlapping top-left region is subtracted once to avoid double-counting).
3. To answer `sumRegion(row1, col1, row2, col2)`, use the same inclusion-exclusion idea in reverse: take the sum of the full rectangle up to `(row2, col2)`, subtract the region above row1 and the region left of col1, then add back the top-left corner that was subtracted twice.
4. Because `prefix` is precomputed once in the constructor, each `sumRegion` query only does O(1) arithmetic on four lookups.

**Time Complexity:** O(m \* n) to build the 2D prefix sum, O(1) per `sumRegion` query.
**Space Complexity:** O(m \* n) — for the prefix sum matrix.

## Reference Solution (Python)

```python
from typing import List


class NumMatrix:
    def __init__(self, matrix: List[List[int]]):
        m, n = len(matrix), len(matrix[0])
        self.prefix = [[0] * (n + 1) for _ in range(m + 1)]
        for r in range(m):
            for c in range(n):
                self.prefix[r + 1][c + 1] = (
                    matrix[r][c]
                    + self.prefix[r][c + 1]
                    + self.prefix[r + 1][c]
                    - self.prefix[r][c]
                )

    def sumRegion(self, row1: int, col1: int, row2: int, col2: int) -> int:
        return (
            self.prefix[row2 + 1][col2 + 1]
            - self.prefix[row1][col2 + 1]
            - self.prefix[row2 + 1][col1]
            + self.prefix[row1][col1]
        )
```

## Reference

- LeetCode: https://leetcode.com/problems/range-sum-query-2d-immutable/
