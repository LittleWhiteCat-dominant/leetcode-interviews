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

This is solved with **backtracking over sorted candidates, skipping duplicate values at the same recursion level**:

1. Sort `candidates` first so equal values become adjacent and the remaining target can be pruned early.
2. Backtrack with a `start` index and `remaining` target; whenever `remaining == 0`, the current `path` is a valid combination, so record a copy of it.
3. In the loop over `candidates[start:]`, break immediately once `candidates[i] > remaining`, since all later candidates (sorted ascending) would only be larger.
4. Skip `candidates[i]` when `i > start and candidates[i] == candidates[i - 1]` — this ensures duplicate values are only used once per position in the tree, preventing duplicate combinations without needing a final dedup step.
5. Otherwise, add `candidates[i]` to `path`, recurse into `backtrack(i + 1, remaining - candidates[i])` (each candidate used at most once), then pop it before trying the next candidate.

**Time Complexity:** O(2^n) worst case — for exploring subsets of the candidates, though sorting and early pruning (breaking once the remaining target is exceeded, skipping duplicates) cut this down substantially in practice.
**Space Complexity:** O(n) — for the recursion depth and the current path, excluding the output.

## Reference Solution (Python)

```python
def combinationSum2(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()
    result = []
    path = []

    def backtrack(start: int, remaining: int) -> None:
        if remaining == 0:
            result.append(path[:])
            return

        for i in range(start, len(candidates)):
            if candidates[i] > remaining:
                break
            if i > start and candidates[i] == candidates[i - 1]:
                continue

            path.append(candidates[i])
            backtrack(i + 1, remaining - candidates[i])
            path.pop()

    backtrack(0, target)
    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/combination-sum-ii/
