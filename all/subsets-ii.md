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

This is solved with **backtracking over sorted input, skipping duplicate choices at the same recursion level**:

1. Sort `nums` first so that any duplicate values become adjacent, which makes duplicate subsets easy to detect and prune.
2. Use backtracking with a `start` index and a running `path`: at every recursive call, immediately append a copy of `path` to the result, since every prefix of the chosen path is itself a valid subset.
3. Iterate candidates from `start` to the end of the array, choosing `nums[i]` and recursing with `start = i + 1`.
4. Before choosing `nums[i]`, skip it if `i > start` and `nums[i] == nums[i - 1]` — this means an identical value was already tried as the first choice at this recursion level, so trying it again would only produce duplicate subsets.
5. After recursing, pop the last element from `path` to backtrack and try the next candidate.

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
