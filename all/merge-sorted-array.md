# 88. Merge Sorted Array

**Difficulty:** Easy
**Topics:** Array, Two Pointers, Sorting
**Common companies:** Amazon, Meta
**Category (README):** 1.1 Two Pointers

## Problem Description

You are given two integer arrays `nums1` and `nums2`, sorted in **non-decreasing order**, and two integers `m` and `n`, representing the number of elements in `nums1` and `nums2` respectively.

**Merge** `nums1` and `nums2` into a single array sorted in **non-decreasing order**.

The final sorted array should not be returned by the function, but instead be *stored inside the array *`nums1`. To accommodate this, `nums1` has a length of `m + n`, where the first `m` elements denote the elements that should be merged, and the last `n` elements are set to `0` and should be ignored. `nums2` has a length of `n`.

 

**Example 1:**

```

**Input:** nums1 = [1,2,3,0,0,0], m = 3, nums2 = [2,5,6], n = 3
**Output:** [1,2,2,3,5,6]
**Explanation:** The arrays we are merging are [1,2,3] and [2,5,6].
The result of the merge is [1,2,2,3,5,6] with the underlined elements coming from nums1.

```

**Example 2:**

```

**Input:** nums1 = [1], m = 1, nums2 = [], n = 0
**Output:** [1]
**Explanation:** The arrays we are merging are [1] and [].
The result of the merge is [1].

```

**Example 3:**

```

**Input:** nums1 = [0], m = 0, nums2 = [1], n = 1
**Output:** [1]
**Explanation:** The arrays we are merging are [] and [1].
The result of the merge is [1].
Note that because m = 0, there are no elements in nums1. The 0 is only there to ensure the merge result can fit in nums1.

```

 

**Constraints:**

	
- `nums1.length == m + n`

	
- `nums2.length == n`

	
- `0 <= m, n <= 200`

	
- `1 <= m + n <= 200`

	
- `-109 <= nums1[i], nums2[j] <= 109`

 

**Follow up: **Can you come up with an algorithm that runs in `O(m + n)` time?

## Key Idea

Merge back-to-front with two pointers to avoid overwrites

## Approach

This is solved with **a reverse two-pointer merge**:

1. Set up three pointers: `i` at the last valid element of `nums1` (index `m - 1`), `j` at the last element of `nums2` (index `n - 1`), and `k` at the last slot of the combined array (index `m + n - 1`).
2. Repeatedly compare `nums1[i]` and `nums2[j]`, placing the larger of the two at `nums1[k]`, then decrement the pointer of whichever element was placed and decrement `k`.
3. Continue until all of `nums2` has been placed (`j < 0`); any remaining elements in `nums1` are already in their correct positions and need no further work.
4. Writing from the back guarantees we never overwrite an unread element of `nums1`.

**Time Complexity:** O(m + n) — each element of both arrays is visited exactly once.
**Space Complexity:** O(1) — merging is done in place within `nums1`, using only pointer variables.

## Reference Solution (Python)

```python
def merge(nums1: list[int], m: int, nums2: list[int], n: int) -> None:
    i, j, k = m - 1, n - 1, m + n - 1
    while j >= 0:
        if i >= 0 and nums1[i] > nums2[j]:
            nums1[k] = nums1[i]
            i -= 1
        else:
            nums1[k] = nums2[j]
            j -= 1
        k -= 1
```

## Reference

- LeetCode: https://leetcode.com/problems/merge-sorted-array/
