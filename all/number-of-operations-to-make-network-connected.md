# 1319. Number of Operations to Make Network Connected

**Difficulty:** Medium
**Topics:** Depth-First Search, Breadth-First Search, Union-Find, Graph Theory
**Common companies:** Amazon
**Category (README):** 10. Union Find

## Problem Description

There are `n` computers numbered from `0` to `n - 1` connected by ethernet cables `connections` forming a network where `connections[i] = [ai, bi]` represents a connection between computers `ai` and `bi`. Any computer can reach any other computer directly or indirectly through the network.

You are given an initial computer network `connections`. You can extract certain cables between two directly connected computers, and place them between any pair of disconnected computers to make them directly connected.

Return *the minimum number of times you need to do this in order to make all the computers connected*. If it is not possible, return `-1`.

 

**Example 1:**

```

**Input:** n = 4, connections = [[0,1],[0,2],[1,2]]
**Output:** 1
**Explanation:** Remove cable between computer 1 and 2 and place between computers 1 and 3.

```

**Example 2:**

```

**Input:** n = 6, connections = [[0,1],[0,2],[0,3],[1,2],[1,3]]
**Output:** 2

```

**Example 3:**

```

**Input:** n = 6, connections = [[0,1],[0,2],[0,3],[1,2]]
**Output:** -1
**Explanation:** There are not enough cables.

```

 

**Constraints:**

	
- `1 <= n <= 105`

	
- `1 <= connections.length <= min(n * (n - 1) / 2, 105)`

	
- `connections[i].length == 2`

	
- `0 <= ai, bi < n`

	
- `ai != bi`

	
- There are no repeated connections.

	
- No two computers are connected by more than one cable.

## Key Idea

Determine the number of connected components; answer = components - 1

## Approach

1. Identify the core pattern for this category: **10. Union Find**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n + E) — with path compression, each union/find is close to O(1) amortized, over `n` computers and `E` connections.
**Space Complexity:** O(n) — for the parent array.

## Reference Solution (Python)

```python
class UnionFind:
    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.count = size

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False
        self.parent[root_a] = root_b
        self.count -= 1
        return True


def makeConnected(n: int, connections: list[list[int]]) -> int:
    if len(connections) < n - 1:
        return -1

    uf = UnionFind(n)
    for a, b in connections:
        uf.union(a, b)

    return uf.count - 1
```

## Reference

- LeetCode: https://leetcode.com/problems/number-of-operations-to-make-network-connected/
