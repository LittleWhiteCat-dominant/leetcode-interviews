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

1. Identify the core pattern for this category: **6. Hash Table**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
