# 684. Redundant Connection

**Difficulty:** Medium
**Topics:** Depth-First Search, Breadth-First Search, Union-Find, Graph Theory
**Common companies:** **Google, Meta favorite**
**Category (README):** 10. Union Find

## Problem Description

In this problem, a tree is an **undirected graph** that is connected and has no cycles.

You are given a graph that started as a tree with `n` nodes labeled from `1` to `n`, with one additional edge added. The added edge has two **different** vertices chosen from `1` to `n`, and was not an edge that already existed. The graph is represented as an array `edges` of length `n` where `edges[i] = [ai, bi]` indicates that there is an edge between nodes `ai` and `bi` in the graph.

Return *an edge that can be removed so that the resulting graph is a tree of *`n`* nodes*. If there are multiple answers, return the answer that occurs last in the input.

 

**Example 1:**

```

**Input:** edges = [[1,2],[1,3],[2,3]]
**Output:** [2,3]

```

**Example 2:**

```

**Input:** edges = [[1,2],[2,3],[3,4],[1,4],[1,5]]
**Output:** [1,4]

```

 

**Constraints:**

	
- `n == edges.length`

	
- `3 <= n <= 1000`

	
- `edges[i].length == 2`

	
- `1 <= ai < bi <= edges.length`

	
- `ai != bi`

	
- There are no repeated edges.

	
- The given graph is connected.

## Key Idea

Detect a cycle while unioning

## Approach

This is solved with **Union-Find (disjoint set union)** to detect the first edge that closes a cycle:

1. Initialize a `parent` array where each node is its own parent (each node starts in its own component).
2. Process edges `[u, v]` in the given order, and for each one find the root of `u` and the root of `v` using path-compressed `find`.
3. If `u` and `v` already share the same root, adding this edge would create a cycle — since a valid tree with `n` nodes has exactly `n - 1` edges, this edge is provably redundant, so return it immediately.
4. Otherwise, union the two components by attaching one root under the other, and continue to the next edge.
5. Because edges are processed in input order and the first cycle-closing edge is returned immediately, this naturally finds the redundant edge that "occurs last" among candidates, matching the problem's tie-breaking rule.

**Time Complexity:** O(n \* alpha(n)) — near-linear thanks to Union-Find with path compression.
**Space Complexity:** O(n) — for the parent array.

## Reference Solution (Python)

```python
from typing import List


def findRedundantConnection(edges: List[List[int]]) -> List[int]:
    n = len(edges)
    parent = list(range(n + 1))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for u, v in edges:
        root_u, root_v = find(u), find(v)
        if root_u == root_v:
            return [u, v]
        parent[root_u] = root_v

    return []
```

## Reference

- LeetCode: https://leetcode.com/problems/redundant-connection/
