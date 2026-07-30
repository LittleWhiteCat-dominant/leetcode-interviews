# 11. Container With Most Water

**Difficulty:** Medium
**Topics:** Array, Two Pointers, Greedy
**Common companies:** All big tech
**Category (README):** 1.1 Two Pointers

## Problem Description

You are given an integer array `height` of length `n`. There are `n` vertical lines drawn such that the two endpoints of the `ith` line are `(i, 0)` and `(i, height[i])`.

Find two lines that together with the x-axis form a container, such that the container contains the most water.

Return *the maximum amount of water a container can store*.

**Notice** that you may not slant the container.

 

**Example 1:**

```

**Input:** height = [1,8,6,2,5,4,8,3,7]
**Output:** 49
**Explanation:** The above vertical lines are represented by array [1,8,6,2,5,4,8,3,7]. In this case, the max area of water (blue section) the container can contain is 49.

```

**Example 2:**

```

**Input:** height = [1,1]
**Output:** 1

```

 

**Constraints:**

	
- `n == height.length`

	
- `2 <= n <= 105`

	
- `0 <= height[i] <= 104`

## Key Idea

Move the shorter side inward

## Approach

1. Identify the core pattern for this category: **1.1 Two Pointers**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — each pointer moves inward at most n times total, so the array is scanned once.
**Space Complexity:** O(1) — only a few pointer/variable references are used.

## Reference Solution (Python)

```python
def maxArea(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    best = 0

    while left < right:
        area = (right - left) * min(height[left], height[right])
        best = max(best, area)
        if height[left] < height[right]:
            left += 1
        else:
            right -= 1

    return best
```

## Reference

- LeetCode: https://leetcode.com/problems/container-with-most-water/
