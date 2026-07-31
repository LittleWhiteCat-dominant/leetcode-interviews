# 1584. Min Cost to Connect All Points

**Difficulty:** Medium
**Topics:** Array, Union-Find, Graph Theory, Minimum Spanning Tree
**Common companies:** Amazon, Google
**Category (README):** 9.3 Advanced Graph Algorithms (Shortest Path / MST)

## Problem Description

You are given an array `points` representing integer coordinates of some points on a 2D-plane, where `points[i] = [xi, yi]`.

The cost of connecting two points `[xi, yi]` and `[xj, yj]` is the **manhattan distance** between them: `|xi - xj| + |yi - yj|`, where `|val|` denotes the absolute value of `val`.

Return *the minimum cost to make all points connected.* All points are connected if there is **exactly one** simple path between any two points.

 

**Example 1:**

```

**Input:** points = [[0,0],[2,2],[3,10],[5,2],[7,0]]
**Output:** 20
**Explanation:** 

We can connect the points as shown above to get the minimum cost of 20.
Notice that there is a unique path between every pair of points.

```

**Example 2:**

```

**Input:** points = [[3,12],[-2,5],[-4,1]]
**Output:** 18

```

 

**Constraints:**

	
- `1 <= points.length <= 1000`

	
- `-106 <= xi, yi <= 106`

	
- All pairs `(xi, yi)` are distinct.

## Key Idea

Kruskal's or Prim's minimum spanning tree

## Approach

This is solved with **Prim's minimum spanning tree algorithm using an array-based min search**:

1. Treat every pair of points as a potential edge weighted by their Manhattan distance, and build the MST greedily starting from an arbitrary point (point `0`).
2. Maintain `min_dist[v]`, the cheapest known distance connecting each unvisited point `v` to the growing tree, initialized to infinity except `min_dist[0] = 0`.
3. Repeat `n` times: pick the unvisited point `u` with the smallest `min_dist`, mark it as added to the tree, and add its cost to the running total.
4. After adding `u`, relax `min_dist[v]` for every unvisited `v` using the Manhattan distance between `u` and `v`.
5. Since the graph is dense (complete), this array-based selection avoids the overhead of a heap and stays efficient at O(n^2).

**Time Complexity:** O(n^2) — Prim's algorithm with an array-based minimum search, which is efficient on this dense (complete) graph.
**Space Complexity:** O(n) — for the `in_mst` and `min_dist` arrays.

## Reference Solution (Python)

```python
import math


def minCostConnectPoints(points: list[list[int]]) -> int:
    n = len(points)
    in_mst = [False] * n
    min_dist = [math.inf] * n
    min_dist[0] = 0
    total = 0

    for _ in range(n):
        u = min((i for i in range(n) if not in_mst[i]), key=lambda i: min_dist[i])
        in_mst[u] = True
        total += min_dist[u]

        for v in range(n):
            if not in_mst[v]:
                dist = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                if dist < min_dist[v]:
                    min_dist[v] = dist

    return total
```

## Reference

- LeetCode: https://leetcode.com/problems/min-cost-to-connect-all-points/
