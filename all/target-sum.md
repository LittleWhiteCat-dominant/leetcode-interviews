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

This is solved by reframing symbol assignment as **a subset-sum 0/1 knapsack**:

1. Split `nums` into a "positive" subset `P` and "negative" subset `N` such that `sum(P) - sum(N) == target`.
2. Since `sum(P) + sum(N) == total`, this means `sum(P) == (total + target) / 2`; if that value is negative, not an integer, or exceeds `total`, return 0 immediately.
3. The problem now reduces to: how many subsets of `nums` sum to `subset_sum = (total + target) // 2`.
4. Run a 1D knapsack DP: `dp[s]` counts the number of ways to form sum `s`, initialized with `dp[0] = 1`.
5. For each number, iterate `s` from `subset_sum` down to that number and add `dp[s - num]` into `dp[s]` (reverse iteration keeps each number used at most once).
6. Return `dp[subset_sum]`.

**Time Complexity:** O(n * sum(nums)) — the DP fills a table of size `subset_sum + 1` once for each of the `n` numbers.
**Space Complexity:** O(sum(nums)) — a 1D DP array sized to the target subset sum.

## Reference Solution (Python)

```python
def findTargetSumWays(nums: list[int], target: int) -> int:
    total = sum(nums)
    if abs(target) > total or (total + target) % 2 != 0:
        return 0

    subset_sum = (total + target) // 2
    dp = [0] * (subset_sum + 1)
    dp[0] = 1

    for num in nums:
        for s in range(subset_sum, num - 1, -1):
            dp[s] += dp[s - num]

    return dp[subset_sum]
```

## Reference

- LeetCode: https://leetcode.com/problems/target-sum/
