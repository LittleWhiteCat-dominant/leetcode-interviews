from collections import deque

def num_islands(grid: list[list[str]]) -> int:

    if not grid or not grid[0]:
        return 0
    
    row, col = len(grid), len(grid[0])

    isVisited = [[False] * col for _ in range(row)]

    num_islands = 0

    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    def bfs(start_row, start_col):
        queue = deque([(start_row, start_col)])
        isVisited[start_row][start_col] = True

        while queue:
            cr, cc = queue.popleft()

            for dr, dc in directions:
                nr, nc = cr + dr, cc + dc

                if 0 <= nr < row and 0<= nc < col and isVisited[nr][nc] == False and grid[nr][nc] == '1':
                    isVisited[nr][nc] = True
                    queue.append((nr, nc))

    for r in range(row):
        for c in range(col):
            if grid[r][c] == '1' and isVisited[r][c] == False:
                num_islands += 1
                bfs(r, c)
    
    return num_islands