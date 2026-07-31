# 695. Max Area of Island

**Difficulty:** Medium
**Topics:** Array, Depth-First Search, Breadth-First Search, Union-Find, Matrix
**Common companies:** Amazon, Google
**Category (README):** 9.1 DFS / BFS Fundamentals

## Problem Description

You are given an `m x n` binary matrix `grid`. An island is a group of `1`'s (representing land) connected **4-directionally** (horizontal or vertical.) You may assume all four edges of the grid are surrounded by water.

The **area** of an island is the number of cells with a value `1` in the island.

Return *the maximum **area** of an island in *`grid`. If there is no island, return `0`.

 

**Example 1:**

```

**Input:** grid = [[0,0,1,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,1,1,0,1,0,0,0,0,0,0,0,0],[0,1,0,0,1,1,0,0,1,0,1,0,0],[0,1,0,0,1,1,0,0,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,1,0,0],[0,0,0,0,0,0,0,1,1,1,0,0,0],[0,0,0,0,0,0,0,1,1,0,0,0,0]]
**Output:** 6
**Explanation:** The answer is not 11, because the island must be connected 4-directionally.

```

**Example 2:**

```

**Input:** grid = [[0,0,0,0,0,0,0,0]]
**Output:** 0

```

 

**Constraints:**

	
- `m == grid.length`

	
- `n == grid[i].length`

	
- `1 <= m, n <= 50`

	
- `grid[i][j]` is either `0` or `1`.

## Key Idea

DFS to compute the size of each connected component, take the max

## Approach

This is solved with **DFS flood-fill from each unvisited land cell, computing the area of its connected island**:

1. Iterate over every cell in the grid; when a `1` is found, launch a DFS from it to measure that island's area.
2. In `dfs(r, c)`, immediately return `0` if the cell is out of bounds or is water (`0`), otherwise mark it visited by setting `grid[r][c] = 0` in place (avoiding a separate visited set).
3. Return `1` (for the current cell) plus the sum of `dfs` recursing into all four neighboring directions.
4. Track the maximum area returned across all DFS calls started from land cells, defaulting to `0` if the grid has no land.

**Time Complexity:** O(m * n) — every cell is visited a constant number of times across all DFS calls.
**Space Complexity:** O(m * n) — for the recursion stack in the worst case of one giant island.

## Reference Solution (Python)

```python
def maxAreaOfIsland(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])

    def dfs(r: int, c: int) -> int:
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != 1:
            return 0
        grid[r][c] = 0
        return 1 + dfs(r + 1, c) + dfs(r - 1, c) + dfs(r, c + 1) + dfs(r, c - 1)

    return max(
        (dfs(r, c) for r in range(rows) for c in range(cols) if grid[r][c] == 1),
        default=0,
    )
```

## Reference

- LeetCode: https://leetcode.com/problems/max-area-of-island/
