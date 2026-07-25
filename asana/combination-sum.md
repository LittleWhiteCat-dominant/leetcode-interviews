# 39. Combination Sum

**Difficulty:** Medium
**Topics:** Array, Backtracking
**Reported at Asana:** Reported in candidate interview experience summaries as part of Asana's coding rounds.

## Problem Description

Given an array of **distinct** integers `candidates` and a target integer `target`, return *a list of all **unique combinations** of* `candidates` *where the chosen numbers sum to* `target`*.* You may return the combinations in **any order**.

The **same** number may be chosen from `candidates` an **unlimited number of times**. Two combinations are unique if the frequency of at least one of the chosen numbers is different.

The test cases are generated such that the number of unique combinations that sum up to `target` is less than `150` combinations for the given input.

## Example 1

```
Input: candidates = [2,3,6,7], target = 7
Output: [[2,2,3],[7]]
Explanation:
2 and 3 are candidates, and 2 + 2 + 3 = 7. Note that 2 can be used multiple times.
7 is a candidate, and 7 = 7.
These are the only two combinations.
```

## Example 2

```
Input: candidates = [2,3,5], target = 8
Output: [[2,2,2,2],[2,3,3],[3,5]]
```

## Example 3

```
Input: candidates = [2], target = 1
Output: []
```

## Constraints

- `1 <= candidates.length <= 30`
- `2 <= candidates[i] <= 40`
- All elements of `candidates` are **distinct**.
- `1 <= target <= 40`

## Approach

1. Sort `candidates` first — this enables early pruning (once a candidate exceeds the remaining target, all later, larger candidates can be skipped too).
2. Use **backtracking**: maintain a running combination and a `remaining` target value.
3. At each recursive step, iterate over candidates **starting from the current index** (not from 0) to avoid generating duplicate combinations in different orders (e.g. `[2,3]` and `[3,2]` should only be counted once).
4. Because a candidate can be reused, when recursing after choosing `candidates[i]`, pass `i` again (not `i + 1`) as the starting index for the next recursive call.
5. Base cases: if `remaining == 0`, record the current combination as a valid result; if `remaining < 0` or you've run out of candidates, backtrack.

**Time Complexity:** O(2^target) in the worst case (bounded by the branching factor of choices at each step), though pruning via sorting significantly reduces the practical runtime.
**Space Complexity:** O(target / min(candidates)) for the recursion depth in the worst case.

## Reference Solution (Python)

```python
def combination_sum(candidates: list[int], target: int) -> list[list[int]]:
    candidates.sort()
    result: list[list[int]] = []

    def backtrack(start: int, remaining: int, current: list[int]) -> None:
        if remaining == 0:
            result.append(current.copy())
            return

        for i in range(start, len(candidates)):
            candidate = candidates[i]
            if candidate > remaining:
                break  # candidates are sorted, so no later candidate can work either

            current.append(candidate)
            backtrack(i, remaining - candidate, current)  # reuse allowed: pass i, not i + 1
            current.pop()

    backtrack(0, target, [])
    return result
```

## Follow-up Questions Interviewers May Ask

- How does this differ from Combination Sum II (LC 40), where each candidate can only be used once and the input may contain duplicates?
- How would you count the number of combinations without generating them all explicitly (this becomes closer to a coin-change-style DP problem)?
- How would you bound or limit the total number of combinations returned if `target` were very large?
