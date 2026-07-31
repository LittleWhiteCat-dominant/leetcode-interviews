# 286. Walls and Gates

**Difficulty:** Medium (LeetCode Premium — statement not publicly available)
**Topics:** Array, Breadth-First Search, Matrix
**Common companies:** **Meta, Google favorite**
**Category (README):** 9.1 DFS / BFS Fundamentals

## Problem Description

This is a Premium problem. View it on LeetCode: https://leetcode.com/problems/walls-and-gates/

## Key Idea

Multi-source BFS expanding from all gates simultaneously

## Approach

This is solved with **multi-source BFS starting simultaneously from every gate**:

1. Scan the grid once and enqueue the coordinates of every gate (cells with value `0`) as initial BFS sources.
2. Run a standard BFS: repeatedly pop a cell and examine its four neighbors.
3. If a neighbor is an empty room (still holding the sentinel `INF` value), it hasn't been reached yet, so set its distance to `current cell's distance + 1` and enqueue it.
4. Because all gates start in the queue at the same "layer", the first time any room is visited it is guaranteed to be via the nearest gate, so no revisiting or distance comparison is needed.
5. Continue until the queue is empty; every reachable room now holds its shortest distance to a gate.

**Time Complexity:** O(m * n) — every cell is enqueued and processed at most once during the multi-source BFS.
**Space Complexity:** O(m * n) — the BFS queue can hold up to all cells in the worst case.

## Reference Solution (Python)

```python
from collections import deque


def wallsAndGates(rooms: list[list[int]]) -> None:
    if not rooms or not rooms[0]:
        return

    rows, cols = len(rooms), len(rooms[0])
    EMPTY = 2147483647
    queue = deque()

    for r in range(rows):
        for c in range(cols):
            if rooms[r][c] == 0:
                queue.append((r, c))

    while queue:
        r, c = queue.popleft()
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and rooms[nr][nc] == EMPTY:
                rooms[nr][nc] = rooms[r][c] + 1
                queue.append((nr, nc))
```

## Reference

- LeetCode: https://leetcode.com/problems/walls-and-gates/
