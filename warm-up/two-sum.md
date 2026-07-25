# 1. Two Sum

**Difficulty:** Easy
**Topics:** Array, Hash Table
**Reported as a warm-up at:** Universal — used as an opening question at virtually every big-tech company (Google, Meta, Amazon, Apple, Netflix, and beyond).

## Problem Description

Given an array of integers `nums` and an integer `target`, return *indices of the two numbers such that they add up to* `target`.

You may assume that each input would have **exactly one solution**, and you may not use the *same* element twice.

You can return the answer in any order.

## Example 1

```
Input: nums = [2,7,11,15], target = 9
Output: [0,1]
Explanation: Because nums[0] + nums[1] == 9, we return [0, 1].
```

## Example 2

```
Input: nums = [3,2,4], target = 6
Output: [1,2]
```

## Example 3

```
Input: nums = [3,3], target = 6
Output: [0,1]
```

## Constraints

- `2 <= nums.length <= 10^4`
- `-10^9 <= nums[i] <= 10^9`
- `-10^9 <= target <= 10^9`
- **Only one valid answer exists.**

## Approach

1. **Brute force (state this first, then optimize):** try every pair `(i, j)` with `i < j` and check if `nums[i] + nums[j] == target`. This is O(n²) time, O(1) space.
2. **Optimal — one-pass hash map:** while iterating through `nums`, for each element `num` at index `i`, compute `complement = target - num`. Check whether `complement` is already in the hash map:
   - If it is, you've found your pair — return `[hash_map[complement], i]`.
   - If not, store `num -> i` in the hash map and continue.
3. This works in a single pass because by the time you reach the second half of a valid pair, the first half is guaranteed to already be in the map.

**Time Complexity:** O(n) — a single pass with O(1) average hash map lookups.
**Space Complexity:** O(n) for the hash map.

## Reference Solution (Python)

```python
def two_sum(nums: list[int], target: int) -> list[int]:
    seen: dict[int, int] = {}

    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i

    return []  # Unreachable given the problem's guarantee of exactly one solution.
```

## Follow-up Questions Interviewers May Ask

- What if the array is already sorted — can you solve it with two pointers in O(1) extra space instead (see LC 167, Two Sum II)?
- What if there could be **multiple** valid pairs and you need to return all of them, without duplicates?
- How would you solve **3Sum** (LC 15), which asks for triplets that sum to zero?
- What if `nums` is a massive stream that doesn't fit in memory — how would you find pairs summing to `target` online?
- How would you handle the case where **no** valid pair exists (relaxing the "exactly one solution" guarantee)?
