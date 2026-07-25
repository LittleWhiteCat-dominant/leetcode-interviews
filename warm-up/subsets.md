# 78. Subsets

**Difficulty:** Medium
**Topics:** Array, Backtracking, Bit Manipulation
**Category warm-up for:** Backtracking

## Problem Description

Given an integer array `nums` of **unique** elements, return *all possible subsets (the power set)*.

The solution set **must not** contain duplicate subsets. Return the solution in **any order**.

## Example 1

```
Input: nums = [1,2,3]
Output: [[],[1],[2],[1,2],[3],[1,3],[2,3],[1,2,3]]
```

## Example 2

```
Input: nums = [0]
Output: [[],[0]]
```

## Constraints

- `1 <= nums.length <= 10`
- `-10 <= nums[i] <= 10`
- All the numbers of `nums` are **unique**.

## Approach

**Backtracking (include/exclude at each element):**
1. Process elements one at a time. At each element, branch into two choices: **include** it in the current subset, or **exclude** it.
2. Recurse into the next element for both branches; when you've processed all elements, the current partial subset is complete — add a copy of it to the results.
3. Backtrack (remove the element you just added) after returning from the "include" branch, before trying "exclude".

**Iterative (build up the power set):**
1. Start with `result = [[]]` (the empty subset).
2. For each number in `nums`, take every existing subset already in `result` and create a new subset by appending the current number to it; add all these new subsets to `result`.

**Bitmask approach:**
1. Since there are `2^n` subsets for `n` elements, iterate `mask` from `0` to `2^n - 1`. For each `mask`, include `nums[i]` in the current subset if bit `i` of `mask` is set.

**Time Complexity:** O(n · 2^n) — there are `2^n` subsets, and each takes up to O(n) to build/copy.
**Space Complexity:** O(n) for the recursion depth (excluding the output), or O(n · 2^n) if counting the total output size.

## Reference Solution (Python, Backtracking)

```python
def subsets(nums: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    current: list[int] = []

    def backtrack(index: int) -> None:
        if index == len(nums):
            result.append(current.copy())
            return

        # Exclude nums[index].
        backtrack(index + 1)

        # Include nums[index].
        current.append(nums[index])
        backtrack(index + 1)
        current.pop()

    backtrack(0)
    return result
```

## Follow-up Questions Interviewers May Ask

- How would you solve **Subsets II** (LC 90), where the input may contain duplicate numbers and the output subsets must still be unique?
- How would you generate subsets iteratively instead of recursively?
- How would you generate only subsets of a specific target size `k`, without generating and then filtering the full power set?
