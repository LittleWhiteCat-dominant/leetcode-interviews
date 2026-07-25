# 807. Max Increase to Keep City Skyline

**Difficulty:** Medium
**Topics:** Array, Matrix, Greedy
**Reported at Rivian:** Tracked in Rivian's known coding question bank (CodeJeet).

## Problem Description

There is a city composed of `n x n` blocks, where each block contains a single building represented by a value `grid[r][c]`. We want to build a new skyscraper on every block so that the height of the buildings can be increased as much as possible, without changing the city's **skyline** from any of the four cardinal directions (north, south, east, or west).

The city's skyline is the outer contour formed by all the building heights when viewed from a distance. The skyline from each cardinal direction must remain the same after the increases.

Return *the maximum total sum* that the height of the buildings can be increased by, **without changing the city's skyline** from any of the four directions.

## Example 1

```
Input: grid = [[3,0,8,4],[2,4,5,7],[9,2,6,3],[0,3,1,0]]
Output: 35
Explanation:
The building heights are shown in the center of the block.
The skyline viewed from each direction is the same as the original grid.
The grid after increasing the height of buildings without affecting skylines is:
gridNew = [[8,4,8,7],[7,4,7,7],[9,4,8,7],[3,3,3,3]]
```

## Example 2

```
Input: grid = [[0,0,0],[0,0,0],[0,0,0]]
Output: 0
```

## Constraints

- `n == grid.length`
- `n == grid[r].length`
- `2 <= n <= 50`
- `0 <= grid[r][c] <= 100`

## Approach

1. Compute two arrays: `row_max[r]` (the maximum height in row `r`, which is the skyline constraint from the east/west view) and `col_max[c]` (the maximum height in column `c`, the skyline constraint from the north/south view).
2. For every cell `(r, c)`, the maximum height it can be increased to, without breaking either skyline, is `min(row_max[r], col_max[c])`.
3. Sum up `min(row_max[r], col_max[c]) - grid[r][c]` for every cell to get the total possible increase.

**Time Complexity:** O(n²) — one pass to compute row/column maxima, another pass to compute the total increase.
**Space Complexity:** O(n) for the `row_max` and `col_max` arrays.

## Reference Solution (Python)

```python
def max_increase_keeping_skyline(grid: list[list[int]]) -> int:
    n = len(grid)
    row_max = [max(row) for row in grid]
    col_max = [max(grid[r][c] for r in range(n)) for c in range(n)]

    total_increase = 0
    for r in range(n):
        for c in range(n):
            total_increase += min(row_max[r], col_max[c]) - grid[r][c]

    return total_increase
```

## Follow-up Questions Interviewers May Ask

- How would this change if the grid were rectangular (`m x n`) instead of square?
- How would you support updating a single cell's height and efficiently recomputing the answer (incremental updates)?
- Can you do it with O(1) extra space if in-place modification of derived row/col maxima is allowed?
