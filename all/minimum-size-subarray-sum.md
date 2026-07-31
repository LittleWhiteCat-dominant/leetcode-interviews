# 209. Minimum Size Subarray Sum

**Difficulty:** Medium
**Topics:** Array, Binary Search, Sliding Window, Prefix Sum
**Common companies:** Amazon
**Category (README):** 1.2 Sliding Window

## Problem Description

Given an array of positive integers `nums` and a positive integer `target`, return *the **minimal length** of a **subarray** whose sum is greater than or equal to* `target`. If there is no such subarray, return `0` instead.

 

**Example 1:**

```

**Input:** target = 7, nums = [2,3,1,2,4,3]
**Output:** 2
**Explanation:** The subarray [4,3] has the minimal length under the problem constraint.

```

**Example 2:**

```

**Input:** target = 4, nums = [1,4,4]
**Output:** 1

```

**Example 3:**

```

**Input:** target = 11, nums = [1,1,1,1,1,1,1,1]
**Output:** 0

```

 

**Constraints:**

	
- `1 <= target <= 109`

	
- `1 <= nums.length <= 105`

	
- `1 <= nums[i] <= 104`

 

**Follow up:** If you have figured out the `O(n)` solution, try coding another solution of which the time complexity is `O(n log(n))`.

## Key Idea

Shrink the left pointer once the window sum exceeds target

## Approach

This is solved with **a variable-size sliding window**:

1. Expand the window by moving `right` forward, adding `nums[right]` to a running `window_sum`.
2. Whenever `window_sum >= target`, the current window is a valid candidate, so record its length if it's the smallest seen so far.
3. Then shrink the window from the left, subtracting `nums[left]` and advancing `left`, as long as the sum still meets or exceeds `target` — this finds the minimal valid window ending at the current `right`.
4. Since all numbers are positive, both pointers only move forward, giving a linear-time scan.
5. Return the best length found, or `0` if the window sum never reached `target`.

**Time Complexity:** O(n) — the left and right pointers each traverse the array at most once.
**Space Complexity:** O(1) — only a running sum and a couple of indices are tracked.

## Reference Solution (Python)

```python
def minSubArrayLen(target: int, nums: list[int]) -> int:
    left = 0
    window_sum = 0
    best = len(nums) + 1

    for right, num in enumerate(nums):
        window_sum += num
        while window_sum >= target:
            best = min(best, right - left + 1)
            window_sum -= nums[left]
            left += 1

    return best if best <= len(nums) else 0
```

## Reference

- LeetCode: https://leetcode.com/problems/minimum-size-subarray-sum/
