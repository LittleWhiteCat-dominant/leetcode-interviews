# 827. Making A Large Island

**Difficulty:** Hard
**Topics:** Array, Matrix, Depth-First Search, Breadth-First Search, Union Find
**Reported at Asana:** Tracked in Asana's known coding question bank (InterviewSolver).

## Problem Description

You are given an `n x n` binary matrix `grid`. You are allowed to change **at most one** `0` to be `1`.

Return *the size of the largest island in* `grid` *after applying this operation*.

An **island** is a 4-directionally connected group of `1`s.

## Example 1

```
Input: grid = [[1,0],[0,1]]
Output: 3
Explanation: Change one 0 to 1 and connect two 1s, then we get an island with area = 3.
```

## Example 2

```
Input: grid = [[1,1],[1,0]]
Output: 4
Explanation: Change the 0 to 1 and make the island bigger, only one island with area = 4.
```

## Example 3

```
Input: grid = [[1,1],[1,1]]
Output: 4
Explanation: Can't change any 0 to 1, only one island with area = 4.
```

## Constraints

- `n == grid.length`
- `n == grid[i].length`
- `1 <= n <= 500`
- `grid[i][j]` is either `0` or `1`.

## Approach

1. **First pass — identify and label existing islands.** Run DFS/BFS on every unvisited land cell, assigning each island a unique id (starting from, say, `2`, so ids don't collide with the `0`/`1` values), and record each island's size in a hash map (`island_id -> size`).
2. **Second pass — evaluate every water cell as a candidate flip.** For every cell that is `0`, look at its (up to 4) neighbors, collect the **distinct** island ids adjacent to it, and sum their sizes plus 1 (for the flipped cell itself). Track the maximum such sum across all water cells.
3. **Edge case**: if the grid is entirely land (no `0` cells), the answer is simply the total number of cells (`n * n`), since no flip is possible/needed.

Using a **set** of neighbor island ids (rather than just summing all four neighbors) is critical — otherwise the same island reached from two different directions would be double-counted.

**Time Complexity:** O(n²) — each cell is visited a constant number of times across both passes.
**Space Complexity:** O(n²) for the labeled grid and the island-size map.

## Reference Solution (Python)

```python
def largest_island(grid: list[list[int]]) -> int:
    n = len(grid)
    island_size: dict[int, int] = {}
    island_id = 2  # start above 1 to avoid clashing with grid values

    def neighbors(r: int, c: int):
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n:
                yield nr, nc

    def flood_fill(r: int, c: int, label: int) -> int:
        stack = [(r, c)]
        grid[r][c] = label
        size = 0
        while stack:
            cr, cc = stack.pop()
            size += 1
            for nr, nc in neighbors(cr, cc):
                if grid[nr][nc] == 1:
                    grid[nr][nc] = label
                    stack.append((nr, nc))
        return size

    for r in range(n):
        for c in range(n):
            if grid[r][c] == 1:
                island_size[island_id] = flood_fill(r, c, island_id)
                island_id += 1

    if not island_size:
        return 1 if n > 0 else 0

    best = max(island_size.values())

    for r in range(n):
        for c in range(n):
            if grid[r][c] == 0:
                seen_ids = {grid[nr][nc] for nr, nc in neighbors(r, c) if grid[nr][nc] > 1}
                candidate = 1 + sum(island_size[i] for i in seen_ids)
                best = max(best, candidate)

    return best
```

## Follow-up Questions Interviewers May Ask

- How would you solve this if you were allowed to flip up to `k` zeros instead of just one?
- How would you extend this to support diagonal connectivity as well?
- Can you solve the island-labeling step with Union-Find instead of DFS/BFS?
