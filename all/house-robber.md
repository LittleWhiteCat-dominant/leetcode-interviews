# 198. House Robber

**Difficulty:** Medium
**Topics:** Array, Dynamic Programming
**Common companies:** All big tech
**Category (README):** 12.1 1D DP

## Problem Description

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed, the only constraint stopping you from robbing each of them is that adjacent houses have security systems connected and **it will automatically contact the police if two adjacent houses were broken into on the same night**.

Given an integer array `nums` representing the amount of money of each house, return *the maximum amount of money you can rob tonight **without alerting the police***.

 

**Example 1:**

```

**Input:** nums = [1,2,3,1]
**Output:** 4
**Explanation:** Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.

```

**Example 2:**

```

**Input:** nums = [2,7,9,3,1]
**Output:** 12
**Explanation:** Rob house 1 (money = 2), rob house 3 (money = 9) and rob house 5 (money = 1).
Total amount you can rob = 2 + 9 + 1 = 12.

```

 

**Constraints:**

	
- `1 <= nums.length <= 100`

	
- `0 <= nums[i] <= 400`

## Key Idea

dp[i] = max(dp[i-1], dp[i-2] + nums[i]); split the circular array into two segments

## Approach

This is solved with **1D dynamic programming using two rolling variables**:

1. Define `dp[i]` as the maximum amount robbable using houses `0..i`; the recurrence is `dp[i] = max(dp[i-1], dp[i-2] + nums[i])` (either skip house `i` or rob it and add to the best result two houses back).
2. Since only the last two states are ever needed, replace the full DP array with two rolling variables `prev` and `curr`.
3. For each house's `money`, update simultaneously: `prev, curr = curr, max(curr, prev + money)`.
4. After processing all houses, `curr` holds the final answer.

**Time Complexity:** O(n) — a single linear pass through the houses.
**Space Complexity:** O(1) — only two running variables are kept instead of a full DP array.

## Reference Solution (Python)

```python
def rob(nums: list[int]) -> int:
    prev, curr = 0, 0
    for money in nums:
        prev, curr = curr, max(curr, prev + money)
    return curr
```

## Reference

- LeetCode: https://leetcode.com/problems/house-robber/
