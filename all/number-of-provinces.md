# 547. Number of Provinces

**Difficulty:** Medium
**Topics:** Depth-First Search, Breadth-First Search, Union-Find, Graph Theory
**Common companies:** Google
**Category (README):** 10. Union Find

## Problem Description

There are `n` cities. Some of them are connected, while some are not. If city `a` is connected directly with city `b`, and city `b` is connected directly with city `c`, then city `a` is connected indirectly with city `c`.

A **province** is a group of directly or indirectly connected cities and no other cities outside of the group.

You are given an `n x n` matrix `isConnected` where `isConnected[i][j] = 1` if the `ith` city and the `jth` city are directly connected, and `isConnected[i][j] = 0` otherwise.

Return *the total number of **provinces***.

 

**Example 1:**

```

**Input:** isConnected = [[1,1,0],[1,1,0],[0,0,1]]
**Output:** 2

```

**Example 2:**

```

**Input:** isConnected = [[1,0,0],[0,1,0],[0,0,1]]
**Output:** 3

```

 

**Constraints:**

	
- `1 <= n <= 200`

	
- `n == isConnected.length`

	
- `n == isConnected[i].length`

	
- `isConnected[i][j]` is `1` or `0`.

	
- `isConnected[i][i] == 1`

	
- `isConnected[i][j] == isConnected[j][i]`

## Key Idea

Traverse the adjacency matrix, unioning cities

## Approach

1. Identify the core pattern for this category: **10. Union Find**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n^2) — dominated by scanning the upper triangle of the `n x n` adjacency matrix; union/find operations are near O(1) amortized.
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

    def union(self, a: int, b: int) -> None:
        root_a, root_b = self.find(a), self.find(b)
        if root_a != root_b:
            self.parent[root_a] = root_b
            self.count -= 1


def findCircleNum(isConnected: list[list[int]]) -> int:
    n = len(isConnected)
    uf = UnionFind(n)

    for i in range(n):
        for j in range(i + 1, n):
            if isConnected[i][j] == 1:
                uf.union(i, j)

    return uf.count
```

## Reference

- LeetCode: https://leetcode.com/problems/number-of-provinces/
