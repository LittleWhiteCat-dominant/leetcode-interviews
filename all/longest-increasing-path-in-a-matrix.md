# 329. Longest Increasing Path in a Matrix

**Difficulty:** Hard
**Topics:** Array, Dynamic Programming, Depth-First Search, Breadth-First Search, Graph Theory, Topological Sort, Memoization, Matrix
**Common companies:** Google, Amazon
**Category (README):** 12.2 2D DP

## Problem Description

Given an `m x n` integers `matrix`, return *the length of the longest increasing path in *`matrix`.

From each cell, you can either move in four directions: left, right, up, or down. You **may not** move **diagonally** or move **outside the boundary** (i.e., wrap-around is not allowed).

 

**Example 1:**

```

**Input:** matrix = [[9,9,4],[6,6,8],[2,1,1]]
**Output:** 4
**Explanation:** The longest increasing path is `[1, 2, 6, 9]`.

```

**Example 2:**

```

**Input:** matrix = [[3,4,5],[3,2,6],[2,2,1]]
**Output:** 4
**Explanation: **The longest increasing path is `[3, 4, 5, 6]`. Moving diagonally is not allowed.

```

**Example 3:**

```

**Input:** matrix = [[1]]
**Output:** 1

```

 

**Constraints:**

	
- `m == matrix.length`

	
- `n == matrix[i].length`

	
- `1 <= m, n <= 200`

	
- `0 <= matrix[i][j] <= 231 - 1`

## Key Idea

DFS + memoization

## Approach

1. Identify the core pattern for this category: **12.2 2D DP**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(m * n) — memoization ensures each cell's longest increasing path is computed exactly once.
**Space Complexity:** O(m * n) — for the memoization cache and the recursion stack.

## Reference Solution (Python)

```python
from functools import lru_cache


def longestIncreasingPath(matrix: list[list[int]]) -> int:
    if not matrix or not matrix[0]:
        return 0

    rows, cols = len(matrix), len(matrix[0])

    @lru_cache(maxsize=None)
    def dfs(r: int, c: int) -> int:
        best = 1
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                best = max(best, 1 + dfs(nr, nc))
        return best

    return max(dfs(r, c) for r in range(rows) for c in range(cols))
```

## Reference

- LeetCode: https://leetcode.com/problems/longest-increasing-path-in-a-matrix/
