# 34. Find First and Last Position of Element in Sorted Array

**Difficulty:** Medium
**Topics:** Array, Binary Search
**Common companies:** Google, Amazon
**Category (README):** 1.4 Binary Search

## Problem Description

Given an array of integers `nums` sorted in non-decreasing order, find the starting and ending position of a given `target` value.

If `target` is not found in the array, return `[-1, -1]`.

You must write an algorithm with `O(log n)` runtime complexity.

 

**Example 1:**

```
**Input:** nums = [5,7,7,8,8,10], target = 8
**Output:** [3,4]

```

**Example 2:**

```
**Input:** nums = [5,7,7,8,8,10], target = 6
**Output:** [-1,-1]

```

**Example 3:**

```
**Input:** nums = [], target = 0
**Output:** [-1,-1]

```

 

**Constraints:**

	
- `0 <= nums.length <= 105`

	
- `-109 <= nums[i] <= 109`

	
- `nums` is a non-decreasing array.

	
- `-109 <= target <= 109`

## Key Idea

Two binary searches for left/right boundaries

## Approach

This is solved with **two targeted binary searches, one for each boundary**:

1. Run a binary search that keeps narrowing toward the left whenever the middle element equals the target, recording the leftmost matching index found so far.
2. If no match was found at all, the target is absent, so return `[-1, -1]` immediately.
3. Otherwise, run a second binary search that instead narrows toward the right on a match, recording the rightmost matching index.
4. Return `[left, right]` as the final answer.

**Time Complexity:** O(log n) — two independent binary searches over the array.
**Space Complexity:** O(1) — only a few pointer variables are used.

## Reference Solution (Python)

```python
def searchRange(nums: list[int], target: int) -> list[int]:
    def find_bound(is_lower: bool) -> int:
        lo, hi = 0, len(nums) - 1
        bound = -1
        while lo <= hi:
            mid = (lo + hi) // 2
            if nums[mid] == target:
                bound = mid
                if is_lower:
                    hi = mid - 1
                else:
                    lo = mid + 1
            elif nums[mid] < target:
                lo = mid + 1
            else:
                hi = mid - 1
        return bound

    left = find_bound(True)
    if left == -1:
        return [-1, -1]
    right = find_bound(False)
    return [left, right]
```

## Reference

- LeetCode: https://leetcode.com/problems/find-first-and-last-position-of-element-in-sorted-array/
