# 417. Pacific Atlantic Water Flow

**Difficulty:** Medium
**Topics:** Array, Depth-First Search, Breadth-First Search, Matrix
**Common companies:** Google, Amazon
**Category (README):** 9.1 DFS / BFS Fundamentals

## Problem Description

There is an `m x n` rectangular island that borders both the **Pacific Ocean** and **Atlantic Ocean**. The **Pacific Ocean** touches the island's left and top edges, and the **Atlantic Ocean** touches the island's right and bottom edges.

The island is partitioned into a grid of square cells. You are given an `m x n` integer matrix `heights` where `heights[r][c]` represents the **height above sea level** of the cell at coordinate `(r, c)`.

The island receives a lot of rain, and the rain water can flow to neighboring cells directly north, south, east, and west if the neighboring cell's height is **less than or equal to** the current cell's height. Water can flow from any cell adjacent to an ocean into the ocean.

Return *a **2D list** of grid coordinates *`result`* where *`result[i] = [ri, ci]`* denotes that rain water can flow from cell *`(ri, ci)`* to **both** the Pacific and Atlantic oceans*.

 

**Example 1:**

```

**Input:** heights = [[1,2,2,3,5],[3,2,3,4,4],[2,4,5,3,1],[6,7,1,4,5],[5,1,1,2,4]]
**Output:** [[0,4],[1,3],[1,4],[2,2],[3,0],[3,1],[4,0]]
**Explanation:** The following cells can flow to the Pacific and Atlantic oceans, as shown below:
[0,4]: [0,4] -> Pacific Ocean 
       [0,4] -> Atlantic Ocean
[1,3]: [1,3] -> [0,3] -> Pacific Ocean 
       [1,3] -> [1,4] -> Atlantic Ocean
[1,4]: [1,4] -> [1,3] -> [0,3] -> Pacific Ocean 
       [1,4] -> Atlantic Ocean
[2,2]: [2,2] -> [1,2] -> [0,2] -> Pacific Ocean 
       [2,2] -> [2,3] -> [2,4] -> Atlantic Ocean
[3,0]: [3,0] -> Pacific Ocean 
       [3,0] -> [4,0] -> Atlantic Ocean
[3,1]: [3,1] -> [3,0] -> Pacific Ocean 
       [3,1] -> [4,1] -> Atlantic Ocean
[4,0]: [4,0] -> Pacific Ocean 
       [4,0] -> Atlantic Ocean
Note that there are other possible paths for these cells to flow to the Pacific and Atlantic oceans.

```

**Example 2:**

```

**Input:** heights = [[1]]
**Output:** [[0,0]]
**Explanation:** The water can flow from the only cell to the Pacific and Atlantic oceans.

```

 

**Constraints:**

	
- `m == heights.length`

	
- `n == heights[r].length`

	
- `1 <= m, n <= 200`

	
- `0 <= heights[r][c] <= 105`

## Key Idea

Reverse DFS from both ocean borders, take the intersection

## Approach

1. Identify the core pattern for this category: **9.1 DFS / BFS Fundamentals**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(m \* n) — each cell is visited at most once per ocean during the reverse DFS.
**Space Complexity:** O(m \* n) — for the visited sets and recursion stack.

## Reference Solution (Python)

```python
from typing import List

def pacificAtlantic(heights: List[List[int]]) -> List[List[int]]:
    if not heights or not heights[0]:
        return []

    m, n = len(heights), len(heights[0])
    pacific = set()
    atlantic = set()

    def dfs(r: int, c: int, visited: set) -> None:
        visited.add((r, c))
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if (
                0 <= nr < m
                and 0 <= nc < n
                and (nr, nc) not in visited
                and heights[nr][nc] >= heights[r][c]
            ):
                dfs(nr, nc, visited)

    for c in range(n):
        dfs(0, c, pacific)
        dfs(m - 1, c, atlantic)
    for r in range(m):
        dfs(r, 0, pacific)
        dfs(r, n - 1, atlantic)

    return [[r, c] for r, c in pacific & atlantic]
```

## Reference

- LeetCode: https://leetcode.com/problems/pacific-atlantic-water-flow/
