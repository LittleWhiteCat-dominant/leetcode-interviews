# 40. Combination Sum II

**Difficulty:** Medium
**Topics:** Array, Backtracking
**Common companies:** Amazon, Google
**Category (README):** 11. Backtracking

## Problem Description

Given a collection of candidate numbers (`candidates`) and a target number (`target`), find all unique combinations in `candidates` where the candidate numbers sum to `target`.

Each number in `candidates` may only be used **once** in the combination.

**Note:** The solution set must not contain duplicate combinations.

 

**Example 1:**

```

**Input:** candidates = [10,1,2,7,6,1,5], target = 8
**Output:** 
[
[1,1,6],
[1,2,5],
[1,7],
[2,6]
]

```

**Example 2:**

```

**Input:** candidates = [2,5,2,1,2], target = 5
**Output:** 
[
[1,2,2],
[5]
]

```

 

**Constraints:**

	
- `1 <= candidates.length <= 100`

	
- `1 <= candidates[i] <= 50`

	
- `1 <= target <= 30`

## Key Idea

Sort first, skip duplicates at the same level, elements used once each

## Approach

1. Identify the core pattern for this category: **11. Backtracking**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/combination-sum-ii/
