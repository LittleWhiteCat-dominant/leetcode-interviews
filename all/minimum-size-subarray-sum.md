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

1. Identify the core pattern for this category: **1.2 Sliding Window**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
