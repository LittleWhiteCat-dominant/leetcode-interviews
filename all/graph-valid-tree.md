# 261. Graph Valid Tree

**Difficulty:** Medium (LeetCode Premium — statement not publicly available)
**Topics:** Depth-First Search, Breadth-First Search, Union-Find, Graph Theory
**Common companies:** Google, Meta (Premium)
**Category (README):** 9.2 Topological Sort

## Problem Description

This is a Premium problem. View it on LeetCode: https://leetcode.com/problems/graph-valid-tree/

## Key Idea

Union Find/DFS to check the graph is acyclic and connected

## Approach

1. Identify the core pattern for this category: **9.2 Topological Sort**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n * alpha(n)) — near-constant amortized time per union/find operation with path compression and union by rank, for `n` nodes and `n - 1` edges.
**Space Complexity:** O(n) — for the parent and rank arrays.

## Reference Solution (Python)

```python
def validTree(n: int, edges: list[list[int]]) -> bool:
    if len(edges) != n - 1:
        return False

    parent = list(range(n))
    rank = [0] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> bool:
        root_x, root_y = find(x), find(y)
        if root_x == root_y:
            return False
        if rank[root_x] < rank[root_y]:
            root_x, root_y = root_y, root_x
        parent[root_y] = root_x
        if rank[root_x] == rank[root_y]:
            rank[root_x] += 1
        return True

    for a, b in edges:
        if not union(a, b):
            return False

    return True
```

## Reference

- LeetCode: https://leetcode.com/problems/graph-valid-tree/
