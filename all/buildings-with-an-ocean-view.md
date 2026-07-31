# 1762. Buildings With an Ocean View

**Difficulty:** Medium (LeetCode Premium — statement not publicly available)
**Topics:** Array, Stack, Monotonic Stack
**Common companies:** **Meta favorite**
**Category (README):** 6. Hash Table

## Problem Description

This is a Premium problem. View it on LeetCode: https://leetcode.com/problems/buildings-with-an-ocean-view/

## Key Idea

Right-to-left scan tracking the running maximum

## Approach

This is solved with **a single right-to-left scan tracking the tallest building seen so far**:

1. Observe that a building has an ocean view (to the right) exactly when it is strictly taller than every building to its right.
2. Scan `heights` from the last index down to the first, keeping a running `max_height_so_far` (initialized to `-inf`).
3. At each index, if the current height exceeds `max_height_so_far`, this building has a view, so record its index and update `max_height_so_far`.
4. Because the scan goes right to left, indices are collected in decreasing order.
5. Reverse the collected list before returning so indices come out in increasing order.

**Time Complexity:** O(n) — a single right-to-left pass through the heights array.
**Space Complexity:** O(1) extra space, beyond the output list.

## Reference Solution (Python)

```python
def findBuildings(heights: list[int]) -> list[int]:
    result = []
    max_height_so_far = float("-inf")

    for i in range(len(heights) - 1, -1, -1):
        if heights[i] > max_height_so_far:
            result.append(i)
            max_height_so_far = heights[i]

    result.reverse()
    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/buildings-with-an-ocean-view/
