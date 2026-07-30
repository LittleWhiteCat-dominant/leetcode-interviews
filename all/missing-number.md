# 268. Missing Number

**Difficulty:** Easy
**Topics:** Array, Hash Table, Math, Binary Search, Bit Manipulation, Sorting
**Common companies:** All big tech
**Category (README):** 14. Bit Manipulation & Math

## Problem Description

Given an array `nums` containing `n` distinct numbers in the range `[0, n]`, return *the only number in the range that is missing from the array.*

 

**Example 1:**

**Input:** nums = [3,0,1]

**Output:** 2

**Explanation:**

`n = 3` since there are 3 numbers, so all numbers are in the range `[0,3]`. 2 is the missing number in the range since it does not appear in `nums`.

**Example 2:**

**Input:** nums = [0,1]

**Output:** 2

**Explanation:**

`n = 2` since there are 2 numbers, so all numbers are in the range `[0,2]`. 2 is the missing number in the range since it does not appear in `nums`.

**Example 3:**

**Input:** nums = [9,6,4,2,3,5,7,0,1]

**Output:** 8

**Explanation:**

`n = 9` since there are 9 numbers, so all numbers are in the range `[0,9]`. 8 is the missing number in the range since it does not appear in `nums`.

 

 

 

 

 

**Constraints:**

	
- `n == nums.length`

	
- `1 <= n <= 104`

	
- `0 <= nums[i] <= n`

	
- All the numbers of `nums` are **unique**.

 

**Follow up:** Could you implement a solution using only `O(1)` extra space complexity and `O(n)` runtime complexity?

## Key Idea

XOR trick, or the sum formula

## Approach

1. Identify the core pattern for this category: **14. Bit Manipulation & Math**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — a single pass XOR-ing every index and value.
**Space Complexity:** O(1) — only a running XOR accumulator is used.

## Reference Solution (Python)

```python
def missingNumber(nums: list[int]) -> int:
    missing = len(nums)
    for i, num in enumerate(nums):
        missing ^= i ^ num
    return missing
```

## Reference

- LeetCode: https://leetcode.com/problems/missing-number/
