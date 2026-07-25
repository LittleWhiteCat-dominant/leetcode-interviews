# 200. Number of Islands

**Difficulty:** Medium
**Topics:** Array, Matrix, Depth-First Search, Breadth-First Search, Union Find
**Reported at Rivian:** Confirmed — appears in multiple onsite coding rounds (2025 candidate reports, US and Vancouver locations).

## Problem Description

Given an `m x n` 2D binary grid `grid` which represents a map of `'1'`s (land) and `'0'`s (water), return *the number of islands*.

An **island** is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. You may assume all four edges of the grid are surrounded by water.

## Example 1

```
Input: grid = [
  ["1","1","1","1","0"],
  ["1","1","0","1","0"],
  ["1","1","0","0","0"],
  ["0","0","0","0","0"]
]
Output: 1
```

## Example 2

```
Input: grid = [
  ["1","1","0","0","0"],
  ["1","1","0","0","0"],
  ["0","0","1","0","0"],
  ["0","0","0","1","1"]
]
Output: 3
```

## Constraints

- `m == grid.length`
- `n == grid[i].length`
- `1 <= m, n <= 300`
- `grid[i][j]` is `'0'` or `'1'`

## Approach

1. Scan every cell of the grid. Whenever an unvisited `'1'` is found, it marks the start of a new island — increment the island counter.
2. Run a DFS (or BFS) flood fill from that cell, marking every connected `'1'` cell as visited (e.g. by mutating it to `'0'` or using a separate `visited` matrix) so it is not counted again.
3. Continue scanning until the whole grid has been processed.
4. Alternative approach: Union-Find, unioning every land cell with its land neighbors, then counting the number of distinct roots. Useful as a follow-up if the interviewer asks for an "online" version where land can be added dynamically (see LeetCode 305, Number of Islands II).

**Time Complexity:** O(m · n) — every cell is visited a constant number of times.
**Space Complexity:** O(m · n) in the worst case for the DFS recursion stack / BFS queue (a grid that is entirely land).

## Reference Solution (Python)

```python
from collections import deque

def num_islands(grid: list[list[str]]) -> int:
    if not grid or not grid[0]:
        return 0

    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]
    islands = 0

    def bfs(start_r: int, start_c: int) -> None:
        queue = deque([(start_r, start_c)])
        visited[start_r][start_c] = True
        while queue:
            r, c = queue.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if (
                    0 <= nr < rows
                    and 0 <= nc < cols
                    and not visited[nr][nc]
                    and grid[nr][nc] == "1"
                ):
                    visited[nr][nc] = True
                    queue.append((nr, nc))

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "1" and not visited[r][c]:
                islands += 1
                bfs(r, c)

    return islands
```

## Follow-up Questions Interviewers May Ask

- What if the grid is too large to fit in memory (streamed row by row)?
- How would you support adding land cells one at a time and returning the island count after each addition (Union-Find, see LC 305)?
- How would you count islands in a grid with diagonal connectivity as well?
