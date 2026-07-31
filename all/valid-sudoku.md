# 36. Valid Sudoku

**Difficulty:** Medium
**Topics:** Array, Hash Table, Matrix
**Common companies:** Apple, Amazon
**Category (README):** 1.6 Matrix

## Problem Description

Determine if a `9 x 9` Sudoku board is valid. Only the filled cells need to be validated **according to the following rules**:

	
- Each row must contain the digits `1-9` without repetition.

	
- Each column must contain the digits `1-9` without repetition.

	
- Each of the nine `3 x 3` sub-boxes of the grid must contain the digits `1-9` without repetition.

**Note:**

	
- A Sudoku board (partially filled) could be valid but is not necessarily solvable.

	
- Only the filled cells need to be validated according to the mentioned rules.

 

**Example 1:**

```

**Input:** board = 
[["5","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
**Output:** true

```

**Example 2:**

```

**Input:** board = 
[["8","3",".",".","7",".",".",".","."]
,["6",".",".","1","9","5",".",".","."]
,[".","9","8",".",".",".",".","6","."]
,["8",".",".",".","6",".",".",".","3"]
,["4",".",".","8",".","3",".",".","1"]
,["7",".",".",".","2",".",".",".","6"]
,[".","6",".",".",".",".","2","8","."]
,[".",".",".","4","1","9",".",".","5"]
,[".",".",".",".","8",".",".","7","9"]]
**Output:** false
**Explanation:** Same as Example 1, except with the **5** in the top left corner being modified to **8**. Since there are two 8's in the top left 3x3 sub-box, it is invalid.

```

 

**Constraints:**

	
- `board.length == 9`

	
- `board[i].length == 9`

	
- `board[i][j]` is a digit `1-9` or `'.'`.

## Key Idea

Hash sets tracking rows/columns/sub-boxes

## Approach

This is solved with **hash sets tracking seen digits per row, column, and 3x3 box**:

1. Allocate 9 sets each for rows, columns, and sub-boxes to record which digits have already been seen.
2. Scan every cell of the board; skip empty cells (`'.'`).
3. Compute the sub-box index as `(r // 3) * 3 + c // 3` to map each cell to one of the nine boxes.
4. Before recording the digit, check if it already exists in the corresponding row set, column set, or box set — if so, the board is invalid, so return `false`.
5. Otherwise add the digit to all three sets and continue.
6. If the entire board is scanned without conflicts, return `true`.

**Time Complexity:** O(1) — the board is always a fixed 9x9 size, so the single pass over its 81 cells is constant time (equivalently O(n^2) for an n x n board).
**Space Complexity:** O(1) — the row/column/box sets are bounded by the fixed 9x9x9 board size.

## Reference Solution (Python)

```python
def isValidSudoku(board: list[list[str]]) -> bool:
    rows = [set() for _ in range(9)]
    cols = [set() for _ in range(9)]
    boxes = [set() for _ in range(9)]

    for r in range(9):
        for c in range(9):
            val = board[r][c]
            if val == '.':
                continue

            box_idx = (r // 3) * 3 + c // 3
            if val in rows[r] or val in cols[c] or val in boxes[box_idx]:
                return False

            rows[r].add(val)
            cols[c].add(val)
            boxes[box_idx].add(val)

    return True
```

## Reference

- LeetCode: https://leetcode.com/problems/valid-sudoku/
