def max_increase_keeping_skyline(grid: list[list[int]]) -> int:
    # rol_max = [max(row) for row in grid]
    row_max = []
    for row in grid:
        row_max.append(max(row))

    col_max = []
    n = len(grid)
    for c in range(n):
        col_values = []
        for r in range(n):
            col_values.append(grid[r][c])
        col_max.append(max(col_values))
    # col_max = [max(grid[r][c]) for r in range(n) for c in range(n)]

    totalNum = 0

    for c in range(n): 
        for r in range(n):
            totalNum += min(row_max[r], col_max[c]) - grid[r][c]
    
    return totalNum