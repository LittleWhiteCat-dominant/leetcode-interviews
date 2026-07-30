# 416. Partition Equal Subset Sum

**Difficulty:** Medium
**Topics:** Array, Dynamic Programming
**Common companies:** Amazon, Google
**Category (README):** 12.1 1D DP

## Problem Description

Given an integer array `nums`, return `true` *if you can partition the array into two subsets such that the sum of the elements in both subsets is equal or *`false`* otherwise*.

 

**Example 1:**

```

**Input:** nums = [1,5,11,5]
**Output:** true
**Explanation:** The array can be partitioned as [1, 5, 5] and [11].

```

**Example 2:**

```

**Input:** nums = [1,2,3,5]
**Output:** false
**Explanation:** The array cannot be partitioned into equal sum subsets.

```

 

**Constraints:**

	
- `1 <= nums.length <= 200`

	
- `1 <= nums[i] <= 100`

## Key Idea

0/1 knapsack; DP array marks reachable sums

## Approach

1. Identify the core pattern for this category: **12.1 1D DP**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n \* target) — where `target` is half the total sum, one pass per number over the DP array.
**Space Complexity:** O(target) — a 1D boolean DP array of reachable sums.

## Reference Solution (Python)

```python
from typing import List

def canPartition(nums: List[int]) -> bool:
    total = sum(nums)
    if total % 2 != 0:
        return False

    target = total // 2
    dp = [False] * (target + 1)
    dp[0] = True

    for num in nums:
        for s in range(target, num - 1, -1):
            if dp[s - num]:
                dp[s] = True

    return dp[target]
```

## Reference

- LeetCode: https://leetcode.com/problems/partition-equal-subset-sum/
