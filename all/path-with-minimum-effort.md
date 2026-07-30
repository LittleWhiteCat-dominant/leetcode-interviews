# 1631. Path With Minimum Effort

**Difficulty:** Medium
**Topics:** Array, Binary Search, Depth-First Search, Breadth-First Search, Union-Find, Heap (Priority Queue), Matrix
**Common companies:** Google, Amazon
**Category (README):** 9.3 Advanced Graph Algorithms (Shortest Path / MST)

## Problem Description

You are a hiker preparing for an upcoming hike. You are given `heights`, a 2D array of size `rows x columns`, where `heights[row][col]` represents the height of cell `(row, col)`. You are situated in the top-left cell, `(0, 0)`, and you hope to travel to the bottom-right cell, `(rows-1, columns-1)` (i.e., **0-indexed**). You can move **up**, **down**, **left**, or **right**, and you wish to find a route that requires the minimum **effort**.

A route's **effort** is the **maximum absolute difference**** **in heights between two consecutive cells of the route.

Return *the minimum **effort** required to travel from the top-left cell to the bottom-right cell.*

 

**Example 1:**

```

**Input:** heights = [[1,2,2],[3,8,2],[5,3,5]]
**Output:** 2
**Explanation:** The route of [1,3,5,3,5] has a maximum absolute difference of 2 in consecutive cells.
This is better than the route of [1,2,2,2,5], where the maximum absolute difference is 3.

```

**Example 2:**

```

**Input:** heights = [[1,2,3],[3,8,4],[5,3,5]]
**Output:** 1
**Explanation:** The route of [1,2,3,4,5] has a maximum absolute difference of 1 in consecutive cells, which is better than route [1,3,5,3,5].

```

**Example 3:**

```

**Input:** heights = [[1,2,1,1,1],[1,2,1,2,1],[1,2,1,2,1],[1,2,1,2,1],[1,1,1,2,1]]
**Output:** 0
**Explanation:** This route does not require any effort.

```

 

**Constraints:**

	
- `rows == heights.length`

	
- `columns == heights[i].length`

	
- `1 <= rows, columns <= 100`

	
- `1 <= heights[i][j] <= 106`

## Key Idea

Dijkstra variant, or binary search + BFS

## Approach

1. Identify the core pattern for this category: **9.3 Advanced Graph Algorithms (Shortest Path / MST)**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(m \* n \* log(m \* n)) — Dijkstra with a binary heap over all cells.
**Space Complexity:** O(m \* n) — for the effort grid and the priority queue.

## Reference Solution (Python)

```python
import heapq
from typing import List

def minimumEffortPath(heights: List[List[int]]) -> int:
    rows, cols = len(heights), len(heights[0])
    effort = [[float("inf")] * cols for _ in range(rows)]
    effort[0][0] = 0
    heap = [(0, 0, 0)]

    while heap:
        cur_effort, r, c = heapq.heappop(heap)
        if r == rows - 1 and c == cols - 1:
            return cur_effort
        if cur_effort > effort[r][c]:
            continue

        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                new_effort = max(cur_effort, abs(heights[nr][nc] - heights[r][c]))
                if new_effort < effort[nr][nc]:
                    effort[nr][nc] = new_effort
                    heapq.heappush(heap, (new_effort, nr, nc))

    return 0
```

## Reference

- LeetCode: https://leetcode.com/problems/path-with-minimum-effort/
