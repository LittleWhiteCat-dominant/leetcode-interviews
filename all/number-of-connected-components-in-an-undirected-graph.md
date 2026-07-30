# 323. Number of Connected Components in an Undirected Graph

**Difficulty:** Medium (LeetCode Premium — statement not publicly available)
**Topics:** Depth-First Search, Breadth-First Search, Union-Find, Graph Theory
**Common companies:** Google, Meta (Premium)
**Category (README):** 9.2 Topological Sort

## Problem Description

This is a Premium problem. View it on LeetCode: https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/

## Key Idea

Union Find/DFS to count connected components

## Approach

1. Identify the core pattern for this category: **9.2 Topological Sort**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n + E) — with path compression, each union/find is close to O(1) amortized, over `n` nodes and `E` edges.
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


def countComponents(n: int, edges: list[list[int]]) -> int:
    uf = UnionFind(n)
    for a, b in edges:
        uf.union(a, b)
    return uf.count
```

## Reference

- LeetCode: https://leetcode.com/problems/number-of-connected-components-in-an-undirected-graph/
