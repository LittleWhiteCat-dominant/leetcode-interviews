# 210. Course Schedule II

**Difficulty:** Medium
**Topics:** Depth-First Search, Breadth-First Search, Graph Theory, Topological Sort
**Common companies:** All big tech
**Category (README):** 9.2 Topological Sort

## Problem Description

There are a total of `numCourses` courses you have to take, labeled from `0` to `numCourses - 1`. You are given an array `prerequisites` where `prerequisites[i] = [ai, bi]` indicates that you **must** take course `bi` first if you want to take course `ai`.

	
- For example, the pair `[0, 1]`, indicates that to take course `0` you have to first take course `1`.

Return *the ordering of courses you should take to finish all courses*. If there are many valid answers, return **any** of them. If it is impossible to finish all courses, return **an empty array**.

 

**Example 1:**

```

**Input:** numCourses = 2, prerequisites = [[1,0]]
**Output:** [0,1]
**Explanation:** There are a total of 2 courses to take. To take course 1 you should have finished course 0. So the correct course order is [0,1].

```

**Example 2:**

```

**Input:** numCourses = 4, prerequisites = [[1,0],[2,0],[3,1],[3,2]]
**Output:** [0,2,1,3]
**Explanation:** There are a total of 4 courses to take. To take course 3 you should have finished both courses 1 and 2. Both courses 1 and 2 should be taken after you finished course 0.
So one correct course order is [0,1,2,3]. Another correct ordering is [0,2,1,3].

```

**Example 3:**

```

**Input:** numCourses = 1, prerequisites = []
**Output:** [0]

```

 

**Constraints:**

	
- `1 <= numCourses <= 2000`

	
- `0 <= prerequisites.length <= numCourses * (numCourses - 1)`

	
- `prerequisites[i].length == 2`

	
- `0 <= ai, bi < numCourses`

	
- `ai != bi`

	
- All the pairs `[ai, bi]` are **distinct**.

## Key Idea

Same as 207, but output the topological order

## Approach

This is solved with **Kahn's algorithm (BFS topological sort), recording the visit order**:

1. Build an adjacency list `graph[prereq] -> [courses that depend on it]` and an `indegree` array counting prerequisites per course.
2. Seed a queue with every course whose `indegree` is 0, since those have no unmet prerequisites and can be taken first.
3. Repeatedly pop a course from the queue, append it to the output `order`, and decrement the indegree of each course it unlocks; enqueue any neighbor whose indegree drops to 0.
4. This naturally produces one valid topological ordering, since a course is only added once all of its prerequisites have already been placed in `order`.
5. If `len(order) == numCourses` at the end, return `order`; otherwise a cycle blocked some courses, so return an empty array.

**Time Complexity:** O(V + E) — build the adjacency list once and process every vertex and edge exactly once during Kahn's BFS.
**Space Complexity:** O(V + E) — adjacency list, in-degree array, and the BFS queue.

## Reference Solution (Python)

```python
from collections import deque


def findOrder(numCourses: int, prerequisites: list[list[int]]) -> list[int]:
    graph: list[list[int]] = [[] for _ in range(numCourses)]
    indegree = [0] * numCourses

    for course, prereq in prerequisites:
        graph[prereq].append(course)
        indegree[course] += 1

    queue = deque(c for c in range(numCourses) if indegree[c] == 0)
    order: list[int] = []

    while queue:
        course = queue.popleft()
        order.append(course)
        for nxt in graph[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    return order if len(order) == numCourses else []
```

## Reference

- LeetCode: https://leetcode.com/problems/course-schedule-ii/
