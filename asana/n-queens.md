# 51. N-Queens

**Difficulty:** Hard
**Topics:** Backtracking
**Reported at Asana:** Tracked in Asana's known coding question bank (InterviewSolver).

## Problem Description

The **n-queens** puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other.

Given an integer `n`, return *all distinct solutions to the **n-queens puzzle***. You may return the answer in **any order**.

Each solution contains a distinct board configuration of the n-queens' placement, where `'Q'` and `'.'` both indicate a queen and an empty space, respectively.

## Example 1

```
Input: n = 4
Output: [[".Q..","...Q","Q...","..Q."],["..Q.","Q...","...Q",".Q.."]]
Explanation: There exist two distinct solutions to the 4-queens puzzle as shown above.
```

## Example 2

```
Input: n = 1
Output: [["Q"]]
```

## Constraints

- `1 <= n <= 9`

## Approach

1. Since no two queens can share a row, place exactly one queen per row and recurse row by row.
2. Track which **columns**, **positive diagonals** (`row + col` is constant), and **negative diagonals** (`row - col` is constant) are already occupied, using three sets (or boolean arrays) for O(1) conflict checks.
3. At each row, try placing a queen in every column that doesn't conflict with an existing queen's column or either diagonal. Recurse into the next row; backtrack (remove the queen and unmark the sets) if the recursive call doesn't lead to a full solution, or after having explored that branch.
4. When a queen has been placed in every row (base case: `row == n`), record the current board configuration as a valid solution.

**Time Complexity:** O(n!) in the worst case (bounded further by pruning), since row placement branches are pruned by column/diagonal conflicts as the search proceeds.
**Space Complexity:** O(n) for the recursion depth and the tracking sets, plus O(n²) per solution stored in the output.

## Reference Solution (Python)

```python
def solve_n_queens(n: int) -> list[list[str]]:
    solutions: list[list[str]] = []
    col_used: set[int] = set()
    diag1_used: set[int] = set()  # row - col
    diag2_used: set[int] = set()  # row + col
    queen_cols = [-1] * n  # queen_cols[row] = column of the queen in that row

    def backtrack(row: int) -> None:
        if row == n:
            board = []
            for r in range(n):
                row_str = "." * queen_cols[r] + "Q" + "." * (n - queen_cols[r] - 1)
                board.append(row_str)
            solutions.append(board)
            return

        for col in range(n):
            if col in col_used or (row - col) in diag1_used or (row + col) in diag2_used:
                continue

            queen_cols[row] = col
            col_used.add(col)
            diag1_used.add(row - col)
            diag2_used.add(row + col)

            backtrack(row + 1)

            col_used.remove(col)
            diag1_used.remove(row - col)
            diag2_used.remove(row + col)

    backtrack(0)
    return solutions
```

## Follow-up Questions Interviewers May Ask

- How would you solve N-Queens II (LC 52), which only asks for the **count** of solutions rather than the solutions themselves?
- Can you optimize the conflict tracking with bitmasks instead of sets, for large `n`?
- How would you find just one valid solution efficiently, without generating all of them?
