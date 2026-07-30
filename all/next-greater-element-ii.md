# 503. Next Greater Element II

**Difficulty:** Medium
**Topics:** Array, Stack, Monotonic Stack
**Common companies:** Amazon, Google
**Category (README):** 4.2 Monotonic Stack

## Problem Description

Given a circular integer array `nums` (i.e., the next element of `nums[nums.length - 1]` is `nums[0]`), return *the **next greater number** for every element in* `nums`.

The **next greater number** of a number `x` is the first greater number to its traversing-order next in the array, which means you could search circularly to find its next greater number. If it doesn't exist, return `-1` for this number.

 

**Example 1:**

```

**Input:** nums = [1,2,1]
**Output:** [2,-1,2]
Explanation: The first 1's next greater number is 2; 
The number 2 can't find next greater number. 
The second 1's next greater number needs to search circularly, which is also 2.

```

**Example 2:**

```

**Input:** nums = [1,2,3,4,3]
**Output:** [2,3,4,-1,4]

```

 

**Constraints:**

	
- `1 <= nums.length <= 104`

	
- `-109 <= nums[i] <= 109`

## Key Idea

Monotonic stack + hash map lookup

## Approach

1. Identify the core pattern for this category: **4.2 Monotonic Stack**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — each index is pushed and popped from the monotonic stack at most once across the two virtual passes.
**Space Complexity:** O(n) — for the stack and the result array.

## Reference Solution (Python)

```python
def nextGreaterElements(nums: list[int]) -> list[int]:
    n = len(nums)
    result = [-1] * n
    stack: list[int] = []

    for i in range(2 * n):
        idx = i % n
        while stack and nums[stack[-1]] < nums[idx]:
            result[stack.pop()] = nums[idx]
        if i < n:
            stack.append(idx)

    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/next-greater-element-ii/
