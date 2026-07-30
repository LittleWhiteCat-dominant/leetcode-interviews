# 746. Min Cost Climbing Stairs

**Difficulty:** Easy
**Topics:** Array, Dynamic Programming
**Common companies:** Amazon, Apple
**Category (README):** 12.1 1D DP

## Problem Description

You are given an integer array `cost` where `cost[i]` is the cost of `ith` step on a staircase. Once you pay the cost, you can either climb one or two steps.

You can either start from the step with index `0`, or the step with index `1`.

Return *the minimum cost to reach the top of the floor*.

 

**Example 1:**

```

**Input:** cost = [10,15,20]
**Output:** 15
**Explanation:** You will start at index 1.
- Pay 15 and climb two steps to reach the top.
The total cost is 15.

```

**Example 2:**

```

**Input:** cost = [1,100,1,1,1,100,1,1,100,1]
**Output:** 6
**Explanation:** You will start at index 0.
- Pay 1 and climb two steps to reach index 2.
- Pay 1 and climb two steps to reach index 4.
- Pay 1 and climb two steps to reach index 6.
- Pay 1 and climb one step to reach index 7.
- Pay 1 and climb two steps to reach index 9.
- Pay 1 and climb one step to reach the top.
The total cost is 6.

```

 

**Constraints:**

	
- `2 <= cost.length <= 1000`

	
- `0 <= cost[i] <= 999`

## Key Idea

Similar to #70, with weighted DP transitions

## Approach

1. Identify the core pattern for this category: **12.1 1D DP**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — one pass computing the DP transition for each step.
**Space Complexity:** O(1) — only the two previous DP values are kept.

## Reference Solution (Python)

```python
def minCostClimbingStairs(cost: list[int]) -> int:
    n = len(cost)
    dp0, dp1 = 0, 0

    for i in range(2, n + 1):
        dp0, dp1 = dp1, min(dp1 + cost[i - 1], dp0 + cost[i - 2])

    return dp1
```

## Reference

- LeetCode: https://leetcode.com/problems/min-cost-climbing-stairs/
