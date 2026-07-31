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

This is solved with **bottom-up 1D dynamic programming with rolling variables**:

1. Define `dp[i]` as the minimum cost to reach step `i` (where "reaching" step `n` means reaching the top of the floor, past the last step).
2. Since you can start for free at step `0` or step `1`, the base cases are `dp[0] = dp[1] = 0`.
3. For each step `i` from `2` to `n`, the cheapest way to arrive is `dp[i] = min(dp[i-1] + cost[i-1], dp[i-2] + cost[i-2])`, since you must pay to leave whichever of the two previous steps you climbed from.
4. Roll the last two DP values forward instead of storing a full array, since only `dp[i-1]` and `dp[i-2]` are ever needed.
5. Return `dp[n]`, the minimum cost to reach the top.

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
