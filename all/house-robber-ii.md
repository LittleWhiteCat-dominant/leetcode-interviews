# 213. House Robber II

**Difficulty:** Medium
**Topics:** Array, Dynamic Programming
**Common companies:** All big tech
**Category (README):** 12.1 1D DP

## Problem Description

You are a professional robber planning to rob houses along a street. Each house has a certain amount of money stashed. All houses at this place are **arranged in a circle.** That means the first house is the neighbor of the last one. Meanwhile, adjacent houses have a security system connected, and **it will automatically contact the police if two adjacent houses were broken into on the same night**.

Given an integer array `nums` representing the amount of money of each house, return *the maximum amount of money you can rob tonight **without alerting the police***.

 

**Example 1:**

```

**Input:** nums = [2,3,2]
**Output:** 3
**Explanation:** You cannot rob house 1 (money = 2) and then rob house 3 (money = 2), because they are adjacent houses.

```

**Example 2:**

```

**Input:** nums = [1,2,3,1]
**Output:** 4
**Explanation:** Rob house 1 (money = 1) and then rob house 3 (money = 3).
Total amount you can rob = 1 + 3 = 4.

```

**Example 3:**

```

**Input:** nums = [1,2,3]
**Output:** 3

```

 

**Constraints:**

	
- `1 <= nums.length <= 100`

	
- `0 <= nums[i] <= 1000`

## Key Idea

dp[i] = max(dp[i-1], dp[i-2] + nums[i]); split the circular array into two segments

## Approach

This is solved by **reducing the circular problem to two linear House Robber subproblems**:

1. Handle the trivial case first: if there's only one house, return its value directly.
2. Because the houses form a circle, the first and last house can never both be robbed, so the optimal answer must exclude at least one of them.
3. Run the standard linear House Robber DP (`prev, curr = curr, max(curr, prev + money)`) once on all houses except the last, and once on all houses except the first.
4. Return the maximum of the two results.

**Time Complexity:** O(n) — two linear passes over the array (excluding first house, excluding last house).
**Space Complexity:** O(1) — only a constant number of running variables per pass.

## Reference Solution (Python)

```python
def rob(nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]

    def rob_linear(houses: list[int]) -> int:
        prev, curr = 0, 0
        for money in houses:
            prev, curr = curr, max(curr, prev + money)
        return curr

    return max(rob_linear(nums[1:]), rob_linear(nums[:-1]))
```

## Reference

- LeetCode: https://leetcode.com/problems/house-robber-ii/
