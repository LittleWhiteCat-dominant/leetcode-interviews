# 704. Binary Search

**Difficulty:** Easy
**Topics:** Array, Binary Search
**Common companies:** All big tech
**Category (README):** 1.4 Binary Search

## Problem Description

Given an array of integers `nums` which is sorted in ascending order, and an integer `target`, write a function to search `target` in `nums`. If `target` exists, then return its index. Otherwise, return `-1`.

You must write an algorithm with `O(log n)` runtime complexity.

 

**Example 1:**

```

**Input:** nums = [-1,0,3,5,9,12], target = 9
**Output:** 4
**Explanation:** 9 exists in nums and its index is 4

```

**Example 2:**

```

**Input:** nums = [-1,0,3,5,9,12], target = 2
**Output:** -1
**Explanation:** 2 does not exist in nums so return -1

```

 

**Constraints:**

	
- `1 <= nums.length <= 104`

	
- `-104 < nums[i], target < 104`

	
- All the integers in `nums` are **unique**.

	
- `nums` is sorted in ascending order.

## Key Idea

Basic template

## Approach

This is solved with **the classic binary search template on a sorted array**:

1. Maintain `left` and `right` pointers spanning the whole array, `[0, len(nums) - 1]`.
2. While `left <= right`, compute `mid = (left + right) // 2` and compare `nums[mid]` to `target`.
3. If they are equal, `mid` is the answer, so return it immediately.
4. If `nums[mid] < target`, the target must be to the right, so move `left = mid + 1`; otherwise move `right = mid - 1`.
5. If the loop ends without finding a match, the target is not present, so return `-1`.

**Time Complexity:** O(log n) — the search space is halved on each iteration.
**Space Complexity:** O(1) — only a few pointers are used.

## Reference Solution (Python)

```python
def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1

    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return -1
```

## Reference

- LeetCode: https://leetcode.com/problems/binary-search/
