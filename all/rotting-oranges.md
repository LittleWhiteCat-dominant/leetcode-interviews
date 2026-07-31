# 994. Rotting Oranges

**Difficulty:** Medium
**Topics:** Array, Breadth-First Search, Matrix
**Common companies:** Amazon, Apple
**Category (README):** 9.1 DFS / BFS Fundamentals

## Problem Description

You are given an `m x n` `grid` where each cell can have one of three values:

	
- `0` representing an empty cell,

	
- `1` representing a fresh orange, or

	
- `2` representing a rotten orange.

Every minute, any fresh orange that is **4-directionally adjacent** to a rotten orange becomes rotten.

Return *the minimum number of minutes that must elapse until no cell has a fresh orange*. If *this is impossible, return* `-1`.

 

**Example 1:**

```

**Input:** grid = [[2,1,1],[1,1,0],[0,1,1]]
**Output:** 4

```

**Example 2:**

```

**Input:** grid = [[2,1,1],[0,1,1],[1,0,1]]
**Output:** -1
**Explanation:** The orange in the bottom left corner (row 2, column 0) is never rotten, because rotting only happens 4-directionally.

```

**Example 3:**

```

**Input:** grid = [[0,2]]
**Output:** 0
**Explanation:** Since there are already no fresh oranges at minute 0, the answer is just 0.

```

 

**Constraints:**

	
- `m == grid.length`

	
- `n == grid[i].length`

	
- `1 <= m, n <= 10`

	
- `grid[i][j]` is `0`, `1`, or `2`.

## Key Idea

Multi-source BFS, expanding layer by layer to compute time

## Approach

This is solved with **multi-source BFS, expanding one minute (layer) at a time**:

1. Scan the grid once to seed a queue with the coordinates of every already-rotten orange, and count the total number of fresh oranges.
2. Run BFS in rounds: each round represents exactly one minute, so process all nodes currently in the queue before moving to the next minute.
3. For each rotten orange in the current round, rot any 4-directionally adjacent fresh orange, decrementing the fresh count and enqueueing it for the next round.
4. Stop once the queue is empty or there are no fresh oranges left, incrementing the minute counter after each full round that produced new rot.
5. If fresh oranges remain unrotted at the end, return `-1`; otherwise return the number of minutes elapsed.

**Time Complexity:** O(m * n) — every cell is enqueued and processed at most once.
**Space Complexity:** O(m * n) — the BFS queue can hold up to all cells.

## Reference Solution (Python)

```python
from collections import deque

def orangesRotting(grid: list[list[int]]) -> int:
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    minutes = 0
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while queue and fresh > 0:
        minutes += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))

    return minutes if fresh == 0 else -1
```

## Reference

- LeetCode: https://leetcode.com/problems/rotting-oranges/
