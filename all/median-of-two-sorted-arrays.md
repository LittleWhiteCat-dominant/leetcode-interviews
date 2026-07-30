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

## Reference

- LeetCode: https://leetcode.com/problems/median-of-two-sorted-arrays/
