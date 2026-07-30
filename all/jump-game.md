# 55. Jump Game

**Difficulty:** Medium
**Topics:** Array, Dynamic Programming, Greedy
**Common companies:** All big tech
**Category (README):** 13. Greedy

## Problem Description

You are given an integer array `nums`. You are initially positioned at the array's **first index**, and each element in the array represents your maximum jump length at that position.

Return `true`* if you can reach the last index, or *`false`* otherwise*.

 

**Example 1:**

```

**Input:** nums = [2,3,1,1,4]
**Output:** true
**Explanation:** Jump 1 step from index 0 to 1, then 3 steps to the last index.

```

**Example 2:**

```

**Input:** nums = [3,2,1,0,4]
**Output:** false
**Explanation:** You will always arrive at index 3 no matter what. Its maximum jump length is 0, which makes it impossible to reach the last index.

```

 

**Constraints:**

	
- `1 <= nums.length <= 104`

	
- `0 <= nums[i] <= 105`

## Key Idea

Track the farthest reachable position so far

## Approach

1. Identify the core pattern for this category: **13. Greedy**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — a single pass through the array.
**Space Complexity:** O(1) — only the running "farthest reachable" value is tracked.

## Reference Solution (Python)

```python
def canJump(nums: list[int]) -> bool:
    farthest = 0

    for i, num in enumerate(nums):
        if i > farthest:
            return False
        farthest = max(farthest, i + num)

    return True
```

## Reference

- LeetCode: https://leetcode.com/problems/jump-game/
