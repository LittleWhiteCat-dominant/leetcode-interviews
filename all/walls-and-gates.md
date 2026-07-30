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

1. Identify the core pattern for this category: **9.1 DFS / BFS Fundamentals**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
