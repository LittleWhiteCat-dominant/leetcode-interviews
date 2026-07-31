# 42. Trapping Rain Water

**Difficulty:** Hard
**Topics:** Array, Two Pointers, Dynamic Programming, Stack, Monotonic Stack
**Common companies:** Amazon, Google
**Category (README):** 1.1 Two Pointers

## Problem Description

Given `n` non-negative integers representing an elevation map where the width of each bar is `1`, compute how much water it can trap after raining.

 

**Example 1:**

```

**Input:** height = [0,1,0,2,1,0,1,3,2,1,2,1]
**Output:** 6
**Explanation:** The above elevation map (black section) is represented by array [0,1,0,2,1,0,1,3,2,1,2,1]. In this case, 6 units of rain water (blue section) are being trapped.

```

**Example 2:**

```

**Input:** height = [4,2,0,3,2,5]
**Output:** 9

```

 

**Constraints:**

	
- `n == height.length`

	
- `1 <= n <= 2 * 104`

	
- `0 <= height[i] <= 105`

## Key Idea

Two pointers tracking left/right max height, or monotonic stack

## Approach

This is solved with **two pointers converging from both ends while tracking running max heights**:

1. Place `left` at index 0 and `right` at the last index, and track `left_max`/`right_max` as the tallest bar seen so far from each side.
2. At each step, advance the pointer on the side with the smaller current height, since the water level there is bounded by the smaller of the two maxima.
3. If `height[left] <= height[right]`, update `left_max` and add `left_max - height[left]` (the trapped water at that column) to the total, then move `left` inward.
4. Otherwise do the symmetric update on the right side with `right_max` and move `right` inward.
5. Continue until the pointers meet, at which point every column's trapped water has been accounted for.

**Time Complexity:** O(n) — a single pass with two pointers moving inward.
**Space Complexity:** O(1) — only a constant number of running max/pointer variables are kept.

## Reference Solution (Python)

```python
def trap(height: list[int]) -> int:
    left, right = 0, len(height) - 1
    left_max, right_max = 0, 0
    water = 0

    while left < right:
        if height[left] <= height[right]:
            left_max = max(left_max, height[left])
            water += left_max - height[left]
            left += 1
        else:
            right_max = max(right_max, height[right])
            water += right_max - height[right]
            right -= 1

    return water
```

## Reference

- LeetCode: https://leetcode.com/problems/trapping-rain-water/
