# 283. Move Zeroes

**Difficulty:** Easy
**Topics:** Array, Two Pointers
**Common companies:** Amazon, Apple
**Category (README):** 1.1 Two Pointers

## Problem Description

Given an integer array `nums`, move all `0`'s to the end of it while maintaining the relative order of the non-zero elements.

**Note** that you must do this in-place without making a copy of the array.

 

**Example 1:**

```
**Input:** nums = [0,1,0,3,12]
**Output:** [1,3,12,0,0]

```

**Example 2:**

```
**Input:** nums = [0]
**Output:** [0]

```

 

**Constraints:**

	
- `1 <= nums.length <= 104`

	
- `-231 <= nums[i] <= 231 - 1`

 

**Follow up:** Could you minimize the total number of operations done?

## Key Idea

Fast/slow pointers overwriting in place

## Approach

1. Identify the core pattern for this category: **1.1 Two Pointers**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — a single pass to compact non-zero elements, plus a final pass to zero the tail.
**Space Complexity:** O(1) — the array is rearranged in place.

## Reference Solution (Python)

```python
def moveZeroes(nums: list[int]) -> None:
    insert_pos = 0
    for num in nums:
        if num != 0:
            nums[insert_pos] = num
            insert_pos += 1

    for i in range(insert_pos, len(nums)):
        nums[i] = 0
```

## Reference

- LeetCode: https://leetcode.com/problems/move-zeroes/
