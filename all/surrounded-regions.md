# 130. Surrounded Regions

**Difficulty:** Medium
**Topics:** Array, Depth-First Search, Breadth-First Search, Union-Find, Matrix
**Common companies:** Amazon, Google
**Category (README):** 9.1 DFS / BFS Fundamentals

## Problem Description

You are given an `m x n` matrix `board` containing **letters** `'X'` and `'O'`, **capture regions** that are **surrounded**:

	
- **Connect**: A cell is connected to adjacent cells horizontally or vertically.

	
- **Region**: To form a region **connect every** `'O'` cell.

	
- **Surround**: A region is surrounded if none of the `'O'` cells in that region are on the edge of the board. Such regions are **completely enclosed **by `'X'` cells.

To capture a **surrounded region**, replace all `'O'`s with `'X'`s **in-place** within the original board. You do not need to return anything.

 

**Example 1:**

**Input:** board = [["X","X","X","X"],["X","O","O","X"],["X","X","O","X"],["X","O","X","X"]]

**Output:** [["X","X","X","X"],["X","X","X","X"],["X","X","X","X"],["X","O","X","X"]]

**Explanation:**

In the above diagram, the bottom region is not captured because it is on the edge of the board and cannot be surrounded.

**Example 2:**

**Input:** board = [["X"]]

**Output:** [["X"]]

 

**Constraints:**

	
- `m == board.length`

	
- `n == board[i].length`

	
- `1 <= m, n <= 200`

	
- `board[i][j]` is `'X'` or `'O'`.

## Key Idea

Reverse DFS starting from the border

## Approach

1. Identify the core pattern for this category: **9.1 DFS / BFS Fundamentals**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(m * n) — each cell is visited a constant number of times across the border DFS and final sweep.
**Space Complexity:** O(m * n) — worst-case DFS recursion stack when the board is mostly `'O'`.

## Reference Solution (Python)

```python
def solve(board: list[list[str]]) -> None:
    if not board or not board[0]:
        return

    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int) -> None:
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != "O":
            return
        board[r][c] = "#"
        dfs(r + 1, c)
        dfs(r - 1, c)
        dfs(r, c + 1)
        dfs(r, c - 1)

    for r in range(rows):
        dfs(r, 0)
        dfs(r, cols - 1)
    for c in range(cols):
        dfs(0, c)
        dfs(rows - 1, c)

    for r in range(rows):
        for c in range(cols):
            if board[r][c] == "O":
                board[r][c] = "X"
            elif board[r][c] == "#":
                board[r][c] = "O"
```

## Reference

- LeetCode: https://leetcode.com/problems/surrounded-regions/
