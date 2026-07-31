# 743. Network Delay Time

**Difficulty:** Medium
**Topics:** Depth-First Search, Breadth-First Search, Graph Theory, Heap (Priority Queue), Shortest Path
**Common companies:** Amazon, Google
**Category (README):** 9.3 Advanced Graph Algorithms (Shortest Path / MST)

## Problem Description

You are given a network of `n` nodes, labeled from `1` to `n`. You are also given `times`, a list of travel times as directed edges `times[i] = (ui, vi, wi)`, where `ui` is the source node, `vi` is the target node, and `wi` is the time it takes for a signal to travel from source to target.

We will send a signal from a given node `k`. Return *the **minimum** time it takes for all the* `n` *nodes to receive the signal*. If it is impossible for all the `n` nodes to receive the signal, return `-1`.

 

**Example 1:**

```

**Input:** times = [[2,1,1],[2,3,1],[3,4,1]], n = 4, k = 2
**Output:** 2

```

**Example 2:**

```

**Input:** times = [[1,2,1]], n = 2, k = 1
**Output:** 1

```

**Example 3:**

```

**Input:** times = [[1,2,1]], n = 2, k = 2
**Output:** -1

```

 

**Constraints:**

	
- `1 <= k <= n <= 100`

	
- `1 <= times.length <= 6000`

	
- `times[i].length == 3`

	
- `1 <= ui, vi <= n`

	
- `ui != vi`

	
- `0 <= wi <= 100`

	
- All the pairs `(ui, vi)` are **unique**. (i.e., no multiple edges.)

## Key Idea

Dijkstra's single-source shortest path

## Approach

This is solved with **Dijkstra's algorithm using a min-heap**:

1. Build a directed adjacency list from `times`, mapping each source node to its `(destination, weight)` pairs.
2. Use a min-heap seeded with `(0, k)`, representing the source node `k` at distance `0`, and a `dist` map recording the shortest confirmed distance to each visited node.
3. Repeatedly pop the smallest-distance entry from the heap; if that node is already finalized in `dist`, skip it (a stale, superseded entry), otherwise record its distance and push all of its unvisited neighbors with their updated tentative distances.
4. This greedily finalizes nodes in increasing order of distance from `k`, which is the core Dijkstra invariant.
5. Once the heap is empty, if every node has an entry in `dist`, the signal reaches all `n` nodes, so return the maximum distance (the time for the last node to receive it); otherwise return `-1`.

**Time Complexity:** O(E log V) — Dijkstra's algorithm with a binary heap, where each edge relaxation is a heap push.
**Space Complexity:** O(V + E) — for the adjacency list, the distance map, and the heap.

## Reference Solution (Python)

```python
import heapq
from collections import defaultdict


def networkDelayTime(times: list[list[int]], n: int, k: int) -> int:
    graph = defaultdict(list)
    for u, v, w in times:
        graph[u].append((v, w))

    dist: dict[int, int] = {}
    heap = [(0, k)]

    while heap:
        d, node = heapq.heappop(heap)
        if node in dist:
            continue
        dist[node] = d
        for neighbor, weight in graph[node]:
            if neighbor not in dist:
                heapq.heappush(heap, (d + weight, neighbor))

    return max(dist.values()) if len(dist) == n else -1
```

## Reference

- LeetCode: https://leetcode.com/problems/network-delay-time/
