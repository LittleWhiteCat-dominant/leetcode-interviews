# 300. Longest Increasing Subsequence

**Difficulty:** Medium
**Topics:** Array, Binary Search, Dynamic Programming
**Common companies:** Google
**Category (README):** 12.1 1D DP

## Problem Description

Given an integer array `nums`, return *the length of the longest **strictly increasing ******subsequence***.

 

**Example 1:**

```

**Input:** nums = [10,9,2,5,3,7,101,18]
**Output:** 4
**Explanation:** The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

```

**Example 2:**

```

**Input:** nums = [0,1,0,3,2,3]
**Output:** 4

```

**Example 3:**

```

**Input:** nums = [7,7,7,7,7,7,7]
**Output:** 1

```

 

**Constraints:**

	
- `1 <= nums.length <= 2500`

	
- `-104 <= nums[i] <= 104`

 

**Follow up:** Can you come up with an algorithm that runs in `O(n log(n))` time complexity?

## Key Idea

dp[i] = LIS ending at i, or a binary-search optimization

## Approach

1. Identify the core pattern for this category: **12.1 1D DP**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/longest-increasing-subsequence/
