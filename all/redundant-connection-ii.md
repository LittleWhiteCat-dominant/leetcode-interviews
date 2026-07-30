# 685. Redundant Connection II

**Difficulty:** Hard
**Topics:** Depth-First Search, Breadth-First Search, Union-Find, Graph Theory
**Common companies:** **Google, Meta favorite**
**Category (README):** 10. Union Find

## Problem Description

In this problem, a rooted tree is a **directed** graph such that, there is exactly one node (the root) for which all other nodes are descendants of this node, plus every node has exactly one parent, except for the root node which has no parents.

The given input is a directed graph that started as a rooted tree with `n` nodes (with distinct values from `1` to `n`), with one additional directed edge added. The added edge has two different vertices chosen from `1` to `n`, and was not an edge that already existed.

The resulting graph is given as a 2D-array of `edges`. Each element of `edges` is a pair `[ui, vi]` that represents a **directed** edge connecting nodes `ui` and `vi`, where `ui` is a parent of child `vi`.

Return *an edge that can be removed so that the resulting graph is a rooted tree of* `n` *nodes*. If there are multiple answers, return the answer that occurs last in the given 2D-array.

 

**Example 1:**

```

**Input:** edges = [[1,2],[1,3],[2,3]]
**Output:** [2,3]

```

**Example 2:**

```

**Input:** edges = [[1,2],[2,3],[3,4],[4,1],[1,5]]
**Output:** [4,1]

```

 

**Constraints:**

	
- `n == edges.length`

	
- `3 <= n <= 1000`

	
- `edges[i].length == 2`

	
- `1 <= ui, vi <= n`

	
- `ui != vi`

## Key Idea

Detect a cycle while unioning

## Approach

1. Identify the core pattern for this category: **10. Union Find**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n \* alpha(n)) — near-linear thanks to Union-Find with path compression.
**Space Complexity:** O(n) — for the parent array and Union-Find structure.

## Reference Solution (Python)

```python
from typing import List


class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n + 1))

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x: int, y: int) -> bool:
        root_x, root_y = self.find(x), self.find(y)
        if root_x == root_y:
            return False
        self.parent[root_x] = root_y
        return True


def findRedundantDirectedConnection(edges: List[List[int]]) -> List[int]:
    n = len(edges)
    parent = [0] * (n + 1)
    candidate1 = candidate2 = None

    # Detect a node with two parents; candidate1 is the earlier edge into it,
    # candidate2 is the later edge that created the second parent.
    for u, v in edges:
        if parent[v] != 0:
            candidate1 = [parent[v], v]
            candidate2 = [u, v]
        else:
            parent[v] = u

    uf = UnionFind(n)

    for u, v in edges:
        if candidate2 and [u, v] == candidate2:
            continue
        if not uf.union(u, v):
            # A cycle formed without involving the two-parent node.
            if not candidate1:
                return [u, v]
            return candidate1

    return candidate2
```

## Reference

- LeetCode: https://leetcode.com/problems/redundant-connection-ii/
