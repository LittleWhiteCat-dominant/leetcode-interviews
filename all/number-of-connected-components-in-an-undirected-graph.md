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

This is solved with **Union-Find (Disjoint Set Union)**:

1. Initialize a `UnionFind` structure with `n` nodes, each its own parent, and a `count` of `n` components.
2. `find(x)` walks up the parent chain with path halving (`parent[x] = parent[parent[x]]`) to keep future lookups fast.
3. For each edge `(a, b)`, call `union(a, b)`: find both roots, and if they differ, merge them by pointing one root at the other and decrementing `count`, since two components just became one.
4. After processing every edge, `count` holds exactly the number of connected components, since components only merge and never split.

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
