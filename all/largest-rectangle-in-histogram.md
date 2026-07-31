# 84. Largest Rectangle in Histogram

**Difficulty:** Hard
**Topics:** Array, Stack, Monotonic Stack
**Common companies:** Google, Amazon
**Category (README):** 4.2 Monotonic Stack

## Problem Description

Given an array of integers `heights` representing the histogram's bar height where the width of each bar is `1`, return *the area of the largest rectangle in the histogram*.

 

**Example 1:**

```

**Input:** heights = [2,1,5,6,2,3]
**Output:** 10
**Explanation:** The above is a histogram where width of each bar is 1.
The largest rectangle is shown in the red area, which has an area = 10 units.

```

**Example 2:**

```

**Input:** heights = [2,4]
**Output:** 4

```

 

**Constraints:**

	
- `1 <= heights.length <= 105`

	
- `0 <= heights[i] <= 104`

## Key Idea

Monotonically increasing stack; compute area on pop

## Approach

This is solved with **a monotonically increasing stack of bar indices**:

1. Scan bars left to right, pushing a sentinel height of `0` after the last real bar to force any remaining bars to be resolved.
2. Keep a stack of indices whose heights are non-decreasing; before pushing the current bar, pop while the top of the stack has a height `>=` the current height.
3. Each time a bar is popped, it is the shortest bar in a rectangle whose height is `heights[popped]`; its width spans from the new stack top (exclusive) to the current index (exclusive).
4. Update the running maximum area with `height * width` for every popped bar.
5. Push the current index onto the stack and continue until all bars (including the sentinel) are processed.

**Time Complexity:** O(n) — each index is pushed onto and popped from the stack at most once.
**Space Complexity:** O(n) — for the monotonic stack of indices.

## Reference Solution (Python)

```python
def largestRectangleArea(heights: list[int]) -> int:
    n = len(heights)
    stack: list[int] = []
    max_area = 0

    for i in range(n + 1):
        cur_height = heights[i] if i < n else 0
        while stack and heights[stack[-1]] >= cur_height:
            height = heights[stack.pop()]
            width = i if not stack else i - stack[-1] - 1
            max_area = max(max_area, height * width)
        stack.append(i)

    return max_area
```

## Reference

- LeetCode: https://leetcode.com/problems/largest-rectangle-in-histogram/
