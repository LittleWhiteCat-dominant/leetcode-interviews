# 621. Task Scheduler

**Difficulty:** Medium
**Topics:** Array, Hash Table, Greedy, Sorting, Heap (Priority Queue), Counting
**Common companies:** All big tech
**Category (README):** 8. Heap / Priority Queue

## Problem Description

You are given an array of CPU `tasks`, each labeled with a letter from A to Z, and a number `n`. Each CPU interval can be idle or allow the completion of one task. Tasks can be completed in any order, but there's a constraint: there has to be a gap of **at least** `n` intervals between two tasks with the same label.

Return the **minimum** number of CPU intervals required to complete all tasks.

 

**Example 1:**

**Input:** tasks = ["A","A","A","B","B","B"], n = 2

**Output:** 8

**Explanation:** A possible sequence is: A -> B -> idle -> A -> B -> idle -> A -> B.

After completing task A, you must wait two intervals before doing A again. The same applies to task B. In the 3rd interval, neither A nor B can be done, so you idle. By the 4th interval, you can do A again as 2 intervals have passed.

**Example 2:**

**Input:** tasks = ["A","C","A","B","D","B"], n = 1

**Output:** 6

**Explanation:** A possible sequence is: A -> B -> C -> D -> A -> B.

With a cooling interval of 1, you can repeat a task after just one other task.

**Example 3:**

**Input:** tasks = ["A","A","A", "B","B","B"], n = 3

**Output:** 10

**Explanation:** A possible sequence is: A -> B -> idle -> idle -> A -> B -> idle -> idle -> A -> B.

There are only two types of tasks, A and B, which need to be separated by 3 intervals. This leads to idling twice between repetitions of these tasks.

 

**Constraints:**

	
- `1 <= tasks.length <= 104`

	
- `tasks[i]` is an uppercase English letter.

	
- `0 <= n <= 100`

## Key Idea

Max-heap by frequency with greedy scheduling + a cooldown queue

## Approach

This is solved with **a max-heap of task frequencies plus a cooldown queue**:

1. Count the frequency of each task label and push the negated counts onto a max-heap so the most frequent task is always scheduled first.
2. Simulate time tick by tick: on each tick, pop the most frequent remaining task from the heap and run it.
3. If that task still has remaining occurrences after running, place it in a cooldown queue tagged with the time (`current time + n`) when it becomes eligible again.
4. At the front of each tick, check whether the task at the head of the cooldown queue has become eligible; if so, push it back onto the heap.
5. Continue until both the heap and cooldown queue are empty; idle ticks happen implicitly whenever the heap is empty but the cooldown queue is not.
6. Return the total elapsed time.

**Time Complexity:** O(m log k) — `m` is the number of tasks and `k` (at most 26) is the number of distinct labels; each task triggers at most one heap push/pop.
**Space Complexity:** O(k) — the heap and cooldown queue each hold at most one entry per distinct task label.

## Reference Solution (Python)

```python
from collections import Counter, deque
import heapq


def leastInterval(tasks: list[str], n: int) -> int:
    counts = Counter(tasks)
    max_heap = [-count for count in counts.values()]
    heapq.heapify(max_heap)
    cooldown = deque()  # (available_time, remaining_count)
    time = 0

    while max_heap or cooldown:
        time += 1
        if max_heap:
            remaining = 1 + heapq.heappop(max_heap)
            if remaining:
                cooldown.append((time + n, remaining))
        if cooldown and cooldown[0][0] == time:
            heapq.heappush(max_heap, cooldown.popleft()[1])

    return time
```

## Reference

- LeetCode: https://leetcode.com/problems/task-scheduler/
