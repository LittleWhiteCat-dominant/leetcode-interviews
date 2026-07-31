# 778. Swim in Rising Water

**Difficulty:** Hard
**Topics:** Array, Binary Search, Depth-First Search, Breadth-First Search, Union-Find, Heap (Priority Queue), Matrix
**Common companies:** Google, Amazon
**Category (README):** 9.3 Advanced Graph Algorithms (Shortest Path / MST)

## Problem Description

You are given an `n x n` integer matrix `grid` where each value `grid[i][j]` represents the elevation at that point `(i, j)`.

It starts raining, and water gradually rises over time. At time `t`, the water level is `t`, meaning **any** cell with elevation less than equal to `t` is submerged or reachable.

You can swim from a square to another 4-directionally adjacent square if and only if the elevation of both squares individually are at most `t`. You can swim infinite distances in zero time. Of course, you must stay within the boundaries of the grid during your swim.

Return *the minimum time until you can reach the bottom right square *`(n - 1, n - 1)`* if you start at the top left square *`(0, 0)`.

 

**Example 1:**

```

**Input:** grid = [[0,2],[1,3]]
**Output:** 3
Explanation:
At time 0, you are in grid location (0, 0).
You cannot go anywhere else because 4-directionally adjacent neighbors have a higher elevation than t = 0.
You cannot reach point (1, 1) until time 3.
When the depth of water is 3, we can swim anywhere inside the grid.

```

**Example 2:**

```

**Input:** grid = [[0,1,2,3,4],[24,23,22,21,5],[12,13,14,15,16],[11,17,18,19,20],[10,9,8,7,6]]
**Output:** 16
**Explanation:** The final route is shown.
We need to wait until time 16 so that (0, 0) and (4, 4) are connected.

```

 

**Constraints:**

	
- `n == grid.length`

	
- `n == grid[i].length`

	
- `1 <= n <= 50`

	
- `0 <= grid[i][j] < n2`

	
- Each value `grid[i][j]` is **unique**.

## Key Idea

Dijkstra variant / binary search + BFS

## Approach

This is solved with **a Dijkstra-style min-heap that always expands the currently-lowest-elevation reachable cell**:

1. Push the starting cell `(0, 0)` onto a min-heap keyed by elevation, and mark it visited.
2. Repeatedly pop the cell with the smallest elevation from the heap; the running `result` (the minimum time needed so far) is the maximum elevation encountered along the path taken to reach it.
3. As soon as the popped cell is the bottom-right target `(n-1, n-1)`, return `result`, since a min-heap guarantees this is reached via the path minimizing the maximum elevation.
4. Otherwise, push each unvisited 4-directionally adjacent cell onto the heap (marking it visited immediately to avoid duplicate pushes), keyed by its own elevation.
5. Because the heap always expands the globally lowest-elevation frontier cell next, the first time the target is popped it's guaranteed to be via the optimal (minimax) route.

**Time Complexity:** O(n^2 log n) — each of the n^2 cells is pushed/popped from the min-heap at most once, at O(log n^2) cost each.
**Space Complexity:** O(n^2) — the visited grid and the heap.

## Reference Solution (Python)

```python
import heapq

def swimInWater(grid: list[list[int]]) -> int:
    n = len(grid)
    visited = [[False] * n for _ in range(n)]
    heap = [(grid[0][0], 0, 0)]
    visited[0][0] = True
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    result = 0
    while heap:
        elevation, r, c = heapq.heappop(heap)
        result = max(result, elevation)
        if r == n - 1 and c == n - 1:
            return result

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and not visited[nr][nc]:
                visited[nr][nc] = True
                heapq.heappush(heap, (grid[nr][nc], nr, nc))

    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/swim-in-rising-water/
