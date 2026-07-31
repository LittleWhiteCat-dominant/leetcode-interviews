# 79. Word Search

**Difficulty:** Medium
**Topics:** Array, String, Backtracking, Depth-First Search, Matrix
**Common companies:** All big tech
**Category (README):** 9.1 DFS / BFS Fundamentals

## Problem Description

Given an `m x n` grid of characters `board` and a string `word`, return `true` *if* `word` *exists in the grid*.

The word can be constructed from letters of sequentially adjacent cells, where adjacent cells are horizontally or vertically neighboring. The same letter cell may not be used more than once.

 

**Example 1:**

```

**Input:** board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCCED"
**Output:** true

```

**Example 2:**

```

**Input:** board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "SEE"
**Output:** true

```

**Example 3:**

```

**Input:** board = [["A","B","C","E"],["S","F","C","S"],["A","D","E","E"]], word = "ABCB"
**Output:** false

```

 

**Constraints:**

	
- `m == board.length`

	
- `n = board[i].length`

	
- `1 <= m, n <= 6`

	
- `1 <= word.length <= 15`

	
- `board` and `word` consists of only lowercase and uppercase English letters.

 

**Follow up:** Could you use search pruning to make your solution faster with a larger `board`?

## Key Idea

Backtracking DFS on the matrix, with pruning + visited marking

## Approach

This is solved with **backtracking DFS from every cell, marking visited cells in place**:

1. Try starting the search from every cell `(r, c)` on the board, since the word can begin anywhere.
2. Define `dfs(r, c, idx)`: if `idx` reaches `len(word)`, every character has matched, so return `true`.
3. Return `false` if `(r, c)` is out of bounds or `board[r][c]` doesn't match `word[idx]`.
4. Otherwise, temporarily overwrite `board[r][c]` (e.g. with `'#'`) to mark it visited for this path, preventing the same cell from being reused.
5. Recurse into all four neighboring directions looking for `word[idx + 1]`; short-circuit as soon as any direction succeeds.
6. Restore the original character at `(r, c)` before returning (backtrack), so other starting points can still use this cell.

**Time Complexity:** O(m * n * 4^L) — worst case, DFS/backtracking may explore up to 4 directions at each of the `L` characters of `word`, starting from each of the `m * n` cells.
**Space Complexity:** O(L) — recursion stack depth equals the length of `word` (the board is mutated in place instead of using a separate visited set).

## Reference Solution (Python)

```python
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])

    def dfs(r: int, c: int, idx: int) -> bool:
        if idx == len(word):
            return True
        if r < 0 or r >= rows or c < 0 or c >= cols or board[r][c] != word[idx]:
            return False

        temp = board[r][c]
        board[r][c] = "#"
        found = (
            dfs(r + 1, c, idx + 1)
            or dfs(r - 1, c, idx + 1)
            or dfs(r, c + 1, idx + 1)
            or dfs(r, c - 1, idx + 1)
        )
        board[r][c] = temp
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True

    return False
```

## Reference

- LeetCode: https://leetcode.com/problems/word-search/
