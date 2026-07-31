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

This is solved by **building a letter-ordering graph and running Kahn's topological sort**:

1. Initialize an adjacency set and in-degree counter for every distinct character that appears in `words`.
2. Compare each pair of adjacent words: find the first position where their characters differ and add an edge from the earlier letter to the later letter (this is the only ordering constraint that pair provides), then stop comparing that pair.
3. If no differing character is found but the second word is shorter than the first, the ordering is invalid, so return `""`.
4. Seed a BFS queue with all letters that have in-degree `0`, then repeatedly pop a letter, append it to the result, and decrement the in-degree of its neighbors, enqueueing any that drop to `0`.
5. If the resulting order includes every letter, return it joined as a string; otherwise a cycle exists, so return `""`.

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
