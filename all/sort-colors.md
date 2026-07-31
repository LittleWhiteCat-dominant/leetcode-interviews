# 75. Sort Colors

**Difficulty:** Medium
**Topics:** Array, Two Pointers, Sorting
**Common companies:** Google, Meta
**Category (README):** 1.1 Two Pointers

## Problem Description

Given an array `nums` with `n` objects colored red, white, or blue, sort them **in-place **so that objects of the same color are adjacent, with the colors in the order red, white, and blue.

We will use the integers `0`, `1`, and `2` to represent the color red, white, and blue, respectively.

You must solve this problem without using the library's sort function.

 

**Example 1:**

```

**Input:** nums = [2,0,2,1,1,0]
**Output:** [0,0,1,1,2,2]

```

**Example 2:**

```

**Input:** nums = [2,0,1]
**Output:** [0,1,2]

```

 

**Constraints:**

	
- `n == nums.length`

	
- `1 <= n <= 300`

	
- `nums[i]` is either `0`, `1`, or `2`.

 

**Follow up:** Could you come up with a one-pass algorithm using only constant extra space?

## Key Idea

Three-pointer Dutch National Flag problem

## Approach

This is solved with **the Dutch National Flag three-pointer partition**:

1. Maintain three pointers: `low` (boundary for the next `0`), `mid` (current element being examined), and `high` (boundary for the next `2`).
2. While `mid <= high`, inspect `nums[mid]`.
3. If it's `0`, swap it with `nums[low]` and advance both `low` and `mid` (the swapped-in value at `mid` is already known to be `1` or has just been placed correctly).
4. If it's `1`, it's already in the correct region, so just advance `mid`.
5. If it's `2`, swap it with `nums[high]` and decrement `high`, but do not advance `mid` yet since the newly swapped-in value still needs to be classified.
6. The array ends up partitioned into `0`s, then `1`s, then `2`s once `mid` passes `high`.

**Time Complexity:** O(n) — a single pass with the Dutch National Flag three-pointer technique.
**Space Complexity:** O(1) — sorted in-place with swaps only.

## Reference Solution (Python)

```python
def sortColors(nums: list[int]) -> None:
    low, mid, high = 0, 0, len(nums) - 1

    while mid <= high:
        if nums[mid] == 0:
            nums[low], nums[mid] = nums[mid], nums[low]
            low += 1
            mid += 1
        elif nums[mid] == 1:
            mid += 1
        else:
            nums[mid], nums[high] = nums[high], nums[mid]
            high -= 1
```

## Reference

- LeetCode: https://leetcode.com/problems/sort-colors/
