# 269. Alien Dictionary

**Difficulty:** Hard (LeetCode Premium — statement not publicly available)
**Topics:** Array, String, Depth-First Search, Breadth-First Search, Graph Theory, Topological Sort
**Common companies:** **Meta, Google favorite (Premium)**
**Category (README):** 9.2 Topological Sort

## Problem Description

This is a Premium problem. View it on LeetCode: https://leetcode.com/problems/alien-dictionary/

## Key Idea

Build a graph, then topologically sort to determine letter order

## Approach

1. Identify the core pattern for this category: **9.2 Topological Sort**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(C) — where C is the total length of all words, to build the graph, plus O(V + E) for the topological sort (V is the alphabet size, at most 26).
**Space Complexity:** O(V + E) — for the adjacency structure and in-degree map.

## Reference Solution (Python)

```python
from collections import deque


def alienOrder(words: list[str]) -> str:
    adj = {c: set() for word in words for c in word}
    in_degree = {c: 0 for c in adj}

    for first, second in zip(words, words[1:]):
        min_len = min(len(first), len(second))
        for i in range(min_len):
            if first[i] != second[i]:
                if second[i] not in adj[first[i]]:
                    adj[first[i]].add(second[i])
                    in_degree[second[i]] += 1
                break
        else:
            if len(second) < len(first):
                return ""

    queue = deque([c for c in adj if in_degree[c] == 0])
    order = []

    while queue:
        c = queue.popleft()
        order.append(c)
        for neighbor in adj[c]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return "".join(order) if len(order) == len(adj) else ""
```

## Reference

- LeetCode: https://leetcode.com/problems/alien-dictionary/
