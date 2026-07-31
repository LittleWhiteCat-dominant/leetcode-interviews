# 33. Search in Rotated Sorted Array

**Difficulty:** Medium
**Topics:** Array, Binary Search
**Common companies:** All big tech
**Category (README):** 1.4 Binary Search

## Problem Description

There is an integer array `nums` sorted in ascending order (with **distinct** values).

Prior to being passed to your function, `nums` is **possibly left rotated** at an unknown index `k` (`1 <= k < nums.length`) such that the resulting array is `[nums[k], nums[k+1], ..., nums[n-1], nums[0], nums[1], ..., nums[k-1]]` (**0-indexed**). For example, `[0,1,2,4,5,6,7]` might be left rotated by `3` indices and become `[4,5,6,7,0,1,2]`.

Given the array `nums` **after** the possible rotation and an integer `target`, return *the index of *`target`* if it is in *`nums`*, or *`-1`* if it is not in *`nums`.

You must write an algorithm with `O(log n)` runtime complexity.

 

**Example 1:**

```
**Input:** nums = [4,5,6,7,0,1,2], target = 0
**Output:** 4

```

**Example 2:**

```
**Input:** nums = [4,5,6,7,0,1,2], target = 3
**Output:** -1

```

**Example 3:**

```
**Input:** nums = [1], target = 0
**Output:** -1

```

 

**Constraints:**

	
- `1 <= nums.length <= 5000`

	
- `-104 <= nums[i] <= 104`

	
- All values of `nums` are **unique**.

	
- `nums` is an ascending array that is possibly rotated.

	
- `-104 <= target <= 104`

## Key Idea

Determine which half is sorted to decide the shrink direction

## Approach

This is solved with **modified binary search that identifies which half is sorted**:

1. Maintain `lo`/`hi` pointers and compute `mid` as usual; if `nums[mid] == target`, return `mid` immediately.
2. Determine which half of `[lo, mid]` / `[mid, hi]` is contiguously sorted by comparing `nums[lo]` to `nums[mid]`.
3. If the left half (`nums[lo..mid]`) is sorted, check whether `target` falls within that range; if so, search left (`hi = mid - 1`), otherwise search right (`lo = mid + 1`).
4. Otherwise the right half must be sorted, so check whether `target` falls within `nums[mid..hi]`; if so, search right, otherwise search left.
5. Repeat until the range is empty, returning `-1` if `target` was never found.

**Time Complexity:** O(log n) — standard binary search with one extra comparison per iteration to determine the sorted half.
**Space Complexity:** O(1) — only a few index variables.

## Reference Solution (Python)

```python
def search(nums: list[int], target: int) -> int:
    lo, hi = 0, len(nums) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] == target:
            return mid

        if nums[lo] <= nums[mid]:
            if nums[lo] <= target < nums[mid]:
                hi = mid - 1
            else:
                lo = mid + 1
        else:
            if nums[mid] < target <= nums[hi]:
                lo = mid + 1
            else:
                hi = mid - 1

    return -1
```

## Reference

- LeetCode: https://leetcode.com/problems/search-in-rotated-sorted-array/
