# 45. Jump Game II

**Difficulty:** Medium
**Topics:** Array, Greedy, Dynamic Programming
**Reported at Rivian:** Referenced in Rivian interview prep guides as a frequently tested topic area.

## Problem Description

You are given a **0-indexed** array of integers `nums` of length `n`. You are initially positioned at `nums[0]`.

Each element `nums[i]` represents the maximum length of a forward jump from index `i`. In other words, if you are at `nums[i]`, you can jump to any `nums[i + j]` where:

- `0 <= j <= nums[i]`
- `i + j < n`

Return *the minimum number of jumps to reach `nums[n - 1]`*. The test cases are generated such that you can reach `nums[n - 1]`.

## Example 1

```
Input: nums = [2,3,1,1,4]
Output: 2
Explanation: The minimum number of jumps to reach the last index is 2.
Jump 1 step from index 0 to 1, then 3 steps to the last index.
```

## Example 2

```
Input: nums = [2,3,0,1,4]
Output: 2
```

## Constraints

- `1 <= nums.length <= 10^4`
- `0 <= nums[i] <= 1000`
- It's guaranteed that you can reach `nums[n - 1]`.

## Approach

This is solved optimally with a **greedy, BFS-like "layered" approach**:

1. Think of it as a BFS over "layers", where each layer represents all positions reachable within the current jump count.
2. Maintain `current_end` (the farthest index reachable with the current number of jumps) and `farthest` (the farthest index reachable with one more jump, updated as you scan).
3. Iterate through the array. For each index `i` (up to but not including the last index), update `farthest = max(farthest, i + nums[i])`.
4. When `i` reaches `current_end`, it means we must take another jump: increment the jump count and set `current_end = farthest`.
5. Stop once `current_end >= n - 1`.

**Time Complexity:** O(n) — a single pass through the array.
**Space Complexity:** O(1) extra space.

## Reference Solution (Python)

```python
def jump(nums: list[int]) -> int:
    n = len(nums)
    jumps = 0
    current_end = 0
    farthest = 0

    for i in range(n - 1):
        farthest = max(farthest, i + nums[i])
        if i == current_end:
            jumps += 1
            current_end = farthest

    return jumps
```

## Follow-up Questions Interviewers May Ask

- How does this differ from Jump Game I (LC 55), which only asks whether the last index is reachable at all?
- Can you also reconstruct the actual sequence of jumps taken, not just the count?
- What if backward jumps were also allowed?
