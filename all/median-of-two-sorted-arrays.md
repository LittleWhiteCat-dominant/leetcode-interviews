# 4. Median of Two Sorted Arrays

**Difficulty:** Hard
**Topics:** Array, Binary Search, Divide and Conquer
**Common companies:** Google (L5+ favorite)
**Category (README):** 1.4 Binary Search

## Problem Description

Given two sorted arrays `nums1` and `nums2` of size `m` and `n` respectively, return **the median** of the two sorted arrays.

The overall run time complexity should be `O(log (m+n))`.

 

**Example 1:**

```

**Input:** nums1 = [1,3], nums2 = [2]
**Output:** 2.00000
**Explanation:** merged array = [1,2,3] and median is 2.

```

**Example 2:**

```

**Input:** nums1 = [1,2], nums2 = [3,4]
**Output:** 2.50000
**Explanation:** merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.

```

 

**Constraints:**

	
- `nums1.length == m`

	
- `nums2.length == n`

	
- `0 <= m <= 1000`

	
- `0 <= n <= 1000`

	
- `1 <= m + n <= 2000`

	
- `-106 <= nums1[i], nums2[i] <= 106`

## Key Idea

Binary search for the k-th smallest element

## Approach

1. Identify the core pattern for this category: **1.4 Binary Search**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(log(min(m, n))) — binary search is performed only over the smaller array.
**Space Complexity:** O(1) — only a constant number of index and value variables are used.

## Reference Solution (Python)

```python
def findMedianSortedArrays(nums1: list[int], nums2: list[int]) -> float:
    if len(nums1) > len(nums2):
        nums1, nums2 = nums2, nums1

    m, n = len(nums1), len(nums2)
    total_left = (m + n + 1) // 2
    lo, hi = 0, m

    while lo <= hi:
        i = (lo + hi) // 2
        j = total_left - i

        left1 = nums1[i - 1] if i > 0 else float('-inf')
        right1 = nums1[i] if i < m else float('inf')
        left2 = nums2[j - 1] if j > 0 else float('-inf')
        right2 = nums2[j] if j < n else float('inf')

        if left1 <= right2 and left2 <= right1:
            if (m + n) % 2 == 1:
                return float(max(left1, left2))
            return (max(left1, left2) + min(right1, right2)) / 2.0
        elif left1 > right2:
            hi = i - 1
        else:
            lo = i + 1

    return 0.0
```

## Reference

- LeetCode: https://leetcode.com/problems/median-of-two-sorted-arrays/
