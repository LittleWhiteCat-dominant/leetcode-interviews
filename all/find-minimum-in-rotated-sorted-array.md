# 153. Find Minimum in Rotated Sorted Array

**Difficulty:** Medium
**Topics:** Array, Binary Search
**Common companies:** **Meta favorite**
**Category (README):** 1.4 Binary Search

## Problem Description

Suppose an array of length `n` sorted in ascending order is **rotated** between `1` and `n` times. For example, the array `nums = [0,1,2,4,5,6,7]` might become:

	
- `[4,5,6,7,0,1,2]` if it was rotated `4` times.

	
- `[0,1,2,4,5,6,7]` if it was rotated `7` times.

Notice that **rotating** an array `[a[0], a[1], a[2], ..., a[n-1]]` 1 time results in the array `[a[n-1], a[0], a[1], a[2], ..., a[n-2]]`.

Given the sorted rotated array `nums` of **unique** elements, return *the minimum element of this array*.

You must write an algorithm that runs in `O(log n) time`.

 

**Example 1:**

```

**Input:** nums = [3,4,5,1,2]
**Output:** 1
**Explanation:** The original array was [1,2,3,4,5] rotated 3 times.

```

**Example 2:**

```

**Input:** nums = [4,5,6,7,0,1,2]
**Output:** 0
**Explanation:** The original array was [0,1,2,4,5,6,7] and it was rotated 4 times.

```

**Example 3:**

```

**Input:** nums = [11,13,15,17]
**Output:** 11
**Explanation:** The original array was [11,13,15,17] and it was rotated 4 times. 

```

 

**Constraints:**

	
- `n == nums.length`

	
- `1 <= n <= 5000`

	
- `-5000 <= nums[i] <= 5000`

	
- All the integers of `nums` are **unique**.

	
- `nums` is sorted and rotated between `1` and `n` times.

## Key Idea

Compare with the right endpoint to shrink the interval

## Approach

This is solved with **binary search that compares the middle element to the right endpoint**:

1. Maintain a search range `[lo, hi]` over the array.
2. At each step compute `mid` and compare `nums[mid]` to `nums[hi]`.
3. If `nums[mid] > nums[hi]`, the minimum must lie strictly to the right of `mid` (the rotation point is ahead), so set `lo = mid + 1`.
4. Otherwise, `nums[mid] <= nums[hi]` means the minimum is at `mid` or to its left, so set `hi = mid`.
5. Repeat until `lo == hi`; that index holds the minimum.

**Time Complexity:** O(log n) — binary search halves the search space each iteration.
**Space Complexity:** O(1) — only pointer variables are used.

## Reference Solution (Python)

```python
def findMin(nums: list[int]) -> int:
    lo, hi = 0, len(nums) - 1

    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid

    return nums[lo]
```

## Reference

- LeetCode: https://leetcode.com/problems/find-minimum-in-rotated-sorted-array/
