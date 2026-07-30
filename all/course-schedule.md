# 207. Course Schedule

**Difficulty:** Medium
**Topics:** Depth-First Search, Breadth-First Search, Graph Theory, Topological Sort
**Common companies:** All big tech
**Category (README):** 9.2 Topological Sort

## Problem Description

There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you **must** take course `bi` first if you want to take course `ai`.

	
- For example, the pair `[0, 1]`, indicates that to take course `0` you have to first take course `1`.

Return `true` if you can finish all courses. Otherwise, return `false`.

 

**Example 1:**

```

**Input:** numCourses = 2, prerequisites = [[1,0]]
**Output:** true
**Explanation:** There are a total of 2 courses to take. 
To take course 1 you should have finished course 0. So it is possible.

```

**Example 2:**

```

**Input:** numCourses = 2, prerequisites = [[1,0],[0,1]]
**Output:** false
**Explanation:** There are a total of 2 courses to take. 
To take course 1 you should have finished course 0, and to take course 0 you should also have finished course 1. So it is impossible.

```

 

**Constraints:**

	
- `1 <= numCourses <= 2000`

	
- `0 <= prerequisites.length <= 5000`

	
- `prerequisites[i].length == 2`

	
- `0 <= ai, bi < numCourses`

	
- All the pairs prerequisites[i] are **unique**.

## Key Idea

BFS in-degree table, or DFS three-color cycle detection

## Approach

1. Identify the core pattern for this category: **9.2 Topological Sort**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(V + E) — build the adjacency list once and process every vertex and edge exactly once during Kahn's BFS.
**Space Complexity:** O(V + E) — adjacency list, in-degree array, and the BFS queue.

## Reference Solution (Python)

```python
from collections import deque


def canFinish(numCourses: int, prerequisites: list[list[int]]) -> bool:
    graph: list[list[int]] = [[] for _ in range(numCourses)]
    indegree = [0] * numCourses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1

    queue = deque(c for c in range(numCourses) if indegree[c] == 0)
    visited = 0

    while queue:
        course = queue.popleft()
        visited += 1
        for nxt in graph[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return visited == numCourses
```

## Reference

- LeetCode: https://leetcode.com/problems/course-schedule/
