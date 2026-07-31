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

This is solved with **Union-Find to check acyclicity and connectivity simultaneously**:

1. A valid tree on `n` nodes must have exactly `n - 1` edges; if the edge count differs, return `False` immediately.
2. Initialize a disjoint-set (Union-Find) structure with `n` singleton components, using path compression and union by rank.
3. For each edge `(a, b)`, attempt to union their components; if `a` and `b` are already in the same component, this edge would create a cycle, so return `False`.
4. If every edge unions successfully, exactly `n - 1` edges have merged `n` components into one connected, acyclic graph, so return `True`.

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
