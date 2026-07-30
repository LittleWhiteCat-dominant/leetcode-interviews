# 153. Find Minimum in Rotated Sorted Array

**Difficulty:** Medium
**Topics:** Array, Binary Search
**Common companies:** **Meta favorite**
**Category (README):** 1.4 Binary Search

## Problem Description

Suppose an array of length `n` sorted in ascending order is **rotated** between `1` and `n` times. For example, the array `nums = [0,1,2,4,5,6,7]` might become:

	
- `[4,5,6,7,0,1,2]` if it was rotated `4` times.

	
- `[0,1,2,4,5,6,7]` if it was rotated `7` times.

Notice that **rotating** an array `[a[0], a[1], a[2], ..., a[n-1]]` 1 time results in the array `[a[n-1], a[0], a[1], a[2], ..., a[n-2]]`.

Given the sorted rotated array `nums` of **unique** elements, return *the minimum element of this array*.

You must write an algorithm that runs in `O(log n) time`.

 

**Example 1:**

```

**Input:** nums = [3,4,5,1,2]
**Output:** 1
**Explanation:** The original array was [1,2,3,4,5] rotated 3 times.

```

**Example 2:**

```

**Input:** nums = [4,5,6,7,0,1,2]
**Output:** 0
**Explanation:** The original array was [0,1,2,4,5,6,7] and it was rotated 4 times.

```

**Example 3:**

```

**Input:** nums = [11,13,15,17]
**Output:** 11
**Explanation:** The original array was [11,13,15,17] and it was rotated 4 times. 

```

 

**Constraints:**

	
- `n == nums.length`

	
- `1 <= n <= 5000`

	
- `-5000 <= nums[i] <= 5000`

	
- All the integers of `nums` are **unique**.

	
- `nums` is sorted and rotated between `1` and `n` times.

## Key Idea

Compare with the right endpoint to shrink the interval

## Approach

1. Identify the core pattern for this category: **1.4 Binary Search**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
