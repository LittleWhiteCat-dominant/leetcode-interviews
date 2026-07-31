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

This is solved with **backtracking using a `used` boolean array**:

1. Maintain a `path` list representing the permutation being built, and a `used` array marking which indices of `nums` are already placed in `path`.
2. At each recursive call, if `path` has the same length as `nums`, a complete permutation has been formed, so append a copy of `path` to the results.
3. Otherwise, iterate over every index `i` of `nums`; skip it if `used[i]` is already `true`.
4. Mark `used[i] = true`, append `nums[i]` to `path`, and recurse to place the next element.
5. After the recursive call returns, backtrack by popping the last element from `path` and resetting `used[i] = false`, so the index can be reused in a different position of another branch.

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
