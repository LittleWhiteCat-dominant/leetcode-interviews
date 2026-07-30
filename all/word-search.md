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

1. Identify the core pattern for this category: **9.1 DFS / BFS Fundamentals**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
