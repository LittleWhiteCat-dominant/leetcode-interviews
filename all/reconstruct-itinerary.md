# 332. Reconstruct Itinerary

**Difficulty:** Hard
**Topics:** Array, String, Depth-First Search, Graph Theory, Sorting, Heap (Priority Queue), Eulerian Circuit
**Common companies:** Google, Amazon
**Category (README):** 9.3 Advanced Graph Algorithms (Shortest Path / MST)

## Problem Description

You are given a list of airline `tickets` where `tickets[i] = [fromi, toi]` represent the departure and the arrival airports of one flight. Reconstruct the itinerary in order and return it.

All of the tickets belong to a man who departs from `"JFK"`, thus, the itinerary must begin with `"JFK"`. If there are multiple valid itineraries, you should return the itinerary that has the smallest lexical order when read as a single string.

	
- For example, the itinerary `["JFK", "LGA"]` has a smaller lexical order than `["JFK", "LGB"]`.

You may assume all tickets form at least one valid itinerary. You must use all the tickets once and only once.

 

**Example 1:**

```

**Input:** tickets = [["MUC","LHR"],["JFK","MUC"],["SFO","SJC"],["LHR","SFO"]]
**Output:** ["JFK","MUC","LHR","SFO","SJC"]

```

**Example 2:**

```

**Input:** tickets = [["JFK","SFO"],["JFK","ATL"],["SFO","ATL"],["ATL","JFK"],["ATL","SFO"]]
**Output:** ["JFK","ATL","JFK","SFO","ATL","SFO"]
**Explanation:** Another possible reconstruction is ["JFK","SFO","ATL","JFK","ATL","SFO"] but it is larger in lexical order.

```

 

**Constraints:**

	
- `1 <= tickets.length <= 300`

	
- `tickets[i].length == 2`

	
- `fromi.length == 3`

	
- `toi.length == 3`

	
- `fromi` and `toi` consist of uppercase English letters.

	
- `fromi != toi`

## Key Idea

Eulerian path + greedy/backtracking

## Approach

1. Identify the core pattern for this category: **9.3 Advanced Graph Algorithms (Shortest Path / MST)**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(E log E) — dominated by sorting the tickets, where E is the number of tickets.
**Space Complexity:** O(E) — for the adjacency list and the recursion/route stack.

## Reference Solution (Python)

```python
from collections import defaultdict
from typing import List


def findItinerary(tickets: List[List[str]]) -> List[str]:
    graph = defaultdict(list)
    for src, dst in sorted(tickets, reverse=True):
        graph[src].append(dst)

    route = []

    def visit(airport: str) -> None:
        destinations = graph[airport]
        while destinations:
            visit(destinations.pop())
        route.append(airport)

    visit("JFK")
    return route[::-1]
```

## Reference

- LeetCode: https://leetcode.com/problems/reconstruct-itinerary/
