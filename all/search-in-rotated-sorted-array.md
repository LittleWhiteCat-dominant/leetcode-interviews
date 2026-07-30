# 33. Search in Rotated Sorted Array

**Difficulty:** Medium
**Topics:** Array, Binary Search
**Common companies:** All big tech
**Category (README):** 1.4 Binary Search

## Problem Description

There is an integer array `nums` sorted in ascending order (with **distinct** values).

Prior to being passed to your function, `nums` is **possibly left rotated** at an unknown index `k` (`1 <= k < nums.length`) such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (**0-indexed**). For example, `[0,1,2,4,5,6,7]` might be left rotated by `3` indices and become `[4,5,6,7,0,1,2]`.

Given the array `nums` **after** the possible rotation and an integer `target`, return *the index of *`target`* if it is in *`nums`*, or *`-1`* if it is not in *`nums`.

You must write an algorithm with `O(log n)` runtime complexity.

 

**Example 1:**

```
**Input:** nums = [4,5,6,7,0,1,2], target = 0
**Output:** 4

```

**Example 2:**

```
**Input:** nums = [4,5,6,7,0,1,2], target = 3
**Output:** -1

```

**Example 3:**

```
**Input:** nums = [1], target = 0
**Output:** -1

```

 

**Constraints:**

	
- `1 <= nums.length <= 5000`

	
- `-104 <= nums[i] <= 104`

	
- All values of `nums` are **unique**.

	
- `nums` is an ascending array that is possibly rotated.

	
- `-104 <= target <= 104`

## Key Idea

Determine which half is sorted to decide the shrink direction

## Approach

1. Identify the core pattern for this category: **1.4 Binary Search**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/search-in-rotated-sorted-array/
