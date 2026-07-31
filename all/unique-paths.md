# 62. Unique Paths

**Difficulty:** Medium
**Topics:** Math, Dynamic Programming, Combinatorics
**Common companies:** All big tech
**Category (README):** 12.2 2D DP

## Problem Description

There is a robot on an `m x n` grid. The robot is initially located at the **top-left corner** (i.e., `grid[0][0]`). The robot tries to move to the **bottom-right corner** (i.e., `grid[m - 1][n - 1]`). The robot can only move either down or right at any point in time.

Given the two integers `m` and `n`, return *the number of possible unique paths that the robot can take to reach the bottom-right corner*.

The test cases are generated so that the answer will be less than or equal to `2 * 109`.

 

**Example 1:**

```

**Input:** m = 3, n = 7
**Output:** 28

```

**Example 2:**

```

**Input:** m = 3, n = 2
**Output:** 3
**Explanation:** From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
1. Right -> Down -> Down
2. Down -> Down -> Right
3. Down -> Right -> Down

```

 

**Constraints:**

	
- `1 <= m, n <= 100`

## Key Idea

2D grid DP

## Approach

This is solved with **space-optimized 2D grid DP collapsed into a single rolling row**:

1. Observe that the number of ways to reach cell `(i, j)` equals the sum of the ways to reach the cell above it and the cell to its left.
2. Initialize a 1D array `row` of length `n` with all 1s, representing the first row (only one way to reach any cell by moving right along the top edge).
3. For each subsequent row, update `row[j] += row[j - 1]` for `j` from 1 to `n - 1`; `row[j]` before the update still holds the "came from above" value, and adding `row[j - 1]` (already updated for this row) adds the "came from the left" value.
4. After processing all `m - 1` remaining rows in place, `row[-1]` holds the total number of unique paths to the bottom-right corner.

**Time Complexity:** O(m * n) — every cell of the grid is visited once.
**Space Complexity:** O(n) — a single rolling row is reused instead of a full 2D table.

## Reference Solution (Python)

```python
def uniquePaths(m: int, n: int) -> int:
    row = [1] * n

    for _ in range(1, m):
        for j in range(1, n):
            row[j] += row[j - 1]

    return row[-1]
```

## Reference

- LeetCode: https://leetcode.com/problems/unique-paths/
