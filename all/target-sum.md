# 494. Target Sum

**Difficulty:** Medium
**Topics:** Array, Dynamic Programming, Backtracking
**Common companies:** Google, Meta
**Category (README):** 12.2 2D DP

## Problem Description

You are given an integer array `nums` and an integer `target`.

You want to build an **expression** out of nums by adding one of the symbols `'+'` and `'-'` before each integer in nums and then concatenate all the integers.

	
- For example, if `nums = [2, 1]`, you can add a `'+'` before `2` and a `'-'` before `1` and concatenate them to build the expression `"+2-1"`.

Return the number of different **expressions** that you can build, which evaluates to `target`.

 

**Example 1:**

```

**Input:** nums = [1,1,1,1,1], target = 3
**Output:** 5
**Explanation:** There are 5 ways to assign symbols to make the sum of nums be target 3.
-1 + 1 + 1 + 1 + 1 = 3
+1 - 1 + 1 + 1 + 1 = 3
+1 + 1 - 1 + 1 + 1 = 3
+1 + 1 + 1 - 1 + 1 = 3
+1 + 1 + 1 + 1 - 1 = 3

```

**Example 2:**

```

**Input:** nums = [1], target = 1
**Output:** 1

```

 

**Constraints:**

	
- `1 <= nums.length <= 20`

	
- `0 <= nums[i] <= 1000`

	
- `0 <= sum(nums[i]) <= 1000`

	
- `-1000 <= target <= 1000`

## Key Idea

Reformulate as a 0/1 knapsack subset-sum problem

## Approach

1. Identify the core pattern for this category: **12.2 2D DP**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/target-sum/
