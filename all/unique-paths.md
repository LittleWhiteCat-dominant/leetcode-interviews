# 62. Unique Paths

**Difficulty:** Medium
**Topics:** Math, Dynamic Programming, Combinatorics
**Common companies:** All big tech
**Category (README):** 12.2 2D DP

## Problem Description

There is a robot on an `m x n` grid. The robot is initially located at the **top-left corner** (i.e., `grid[0][0]`). The robot tries to move to the **bottom-right corner** (i.e., `grid[m - 1][n - 1]`). The robot can only move either down or right at any point in time.

Given the two integers `m` and `n`, return *the number of possible unique paths that the robot can take to reach the bottom-right corner*.

The test cases are generated so that the answer will be less than or equal to `2 * 109`.

 

**Example 1:**

```

**Input:** m = 3, n = 7
**Output:** 28

```

**Example 2:**

```

**Input:** m = 3, n = 2
**Output:** 3
**Explanation:** From the top-left corner, there are a total of 3 ways to reach the bottom-right corner:
1. Right -> Down -> Down
2. Down -> Down -> Right
3. Down -> Right -> Down

```

 

**Constraints:**

	
- `1 <= m, n <= 100`

## Key Idea

2D grid DP

## Approach

1. Identify the core pattern for this category: **12.2 2D DP**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(m * n) — every cell of the grid is visited once.
**Space Complexity:** O(n) — a single rolling row is reused instead of a full 2D table.

## Reference Solution (Python)

```python
def uniquePaths(m: int, n: int) -> int:
    row = [1] * n

    for _ in range(1, m):
        for j in range(1, n):
            row[j] += row[j - 1]

    return row[-1]
```

## Reference

- LeetCode: https://leetcode.com/problems/unique-paths/
