# 46. Permutations

**Difficulty:** Medium
**Topics:** Array, Backtracking
**Common companies:** All big tech
**Category (README):** 11. Backtracking

## Problem Description

Given an array `nums` of distinct integers, return all the possible permutations. You can return the answer in **any order**.

 

**Example 1:**

```
**Input:** nums = [1,2,3]
**Output:** [[1,2,3],[1,3,2],[2,1,3],[2,3,1],[3,1,2],[3,2,1]]

```

**Example 2:**

```
**Input:** nums = [0,1]
**Output:** [[0,1],[1,0]]

```

**Example 3:**

```
**Input:** nums = [1]
**Output:** [[1]]

```

 

**Constraints:**

	
- `1 <= nums.length <= 6`

	
- `-10 <= nums[i] <= 10`

	
- All the integers of `nums` are **unique**.

## Key Idea

Use a `visited` array, or swap in place to generate permutations

## Approach

1. Identify the core pattern for this category: **11. Backtracking**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n \* n!) — there are n! permutations, each taking O(n) to build.
**Space Complexity:** O(n) — recursion depth and the `used` array, excluding the output.

## Reference Solution (Python)

```python
from typing import List

def permute(nums: List[int]) -> List[List[int]]:
    result = []
    path = []
    used = [False] * len(nums)

    def backtrack() -> None:
        if len(path) == len(nums):
            result.append(path[:])
            return
        for i, num in enumerate(nums):
            if used[i]:
                continue
            used[i] = True
            path.append(num)
            backtrack()
            path.pop()
            used[i] = False

    backtrack()
    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/permutations/
