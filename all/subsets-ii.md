# 90. Subsets II

**Difficulty:** Medium
**Topics:** Array, Backtracking, Bit Manipulation
**Common companies:** Amazon, Meta
**Category (README):** 11. Backtracking

## Problem Description

Given an integer array `nums` that may contain duplicates, return *all possible* *subsets** (the power set)*.

The solution set **must not** contain duplicate subsets. Return the solution in **any order**.

 

**Example 1:**

```
**Input:** nums = [1,2,2]
**Output:** [[],[1],[1,2],[1,2,2],[2],[2,2]]

```

**Example 2:**

```
**Input:** nums = [0]
**Output:** [[],[0]]

```

 

**Constraints:**

	
- `1 <= nums.length <= 10`

	
- `-10 <= nums[i] <= 10`

## Key Idea

Sort first, then skip duplicate elements at the same recursion level

## Approach

1. Identify the core pattern for this category: **11. Backtracking**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n * 2^n) — up to 2^n subsets, each taking O(n) to copy.
**Space Complexity:** O(n) — the recursion depth and the current path, excluding the output.

## Reference Solution (Python)

```python
def subsetsWithDup(nums: list[int]) -> list[list[int]]:
    nums.sort()
    result = []
    path = []

    def backtrack(start: int) -> None:
        result.append(path[:])
        for i in range(start, len(nums)):
            if i > start and nums[i] == nums[i - 1]:
                continue
            path.append(nums[i])
            backtrack(i + 1)
            path.pop()

    backtrack(0)
    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/subsets-ii/
