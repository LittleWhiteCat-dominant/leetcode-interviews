# 300. Longest Increasing Subsequence

**Difficulty:** Medium
**Topics:** Array, Binary Search, Dynamic Programming
**Common companies:** Google
**Category (README):** 12.1 1D DP

## Problem Description

Given an integer array `nums`, return *the length of the longest **strictly increasing ******subsequence***.

 

**Example 1:**

```

**Input:** nums = [10,9,2,5,3,7,101,18]
**Output:** 4
**Explanation:** The longest increasing subsequence is [2,3,7,101], therefore the length is 4.

```

**Example 2:**

```

**Input:** nums = [0,1,0,3,2,3]
**Output:** 4

```

**Example 3:**

```

**Input:** nums = [7,7,7,7,7,7,7]
**Output:** 1

```

 

**Constraints:**

	
- `1 <= nums.length <= 2500`

	
- `-104 <= nums[i] <= 104`

 

**Follow up:** Can you come up with an algorithm that runs in `O(n log(n))` time complexity?

## Key Idea

dp[i] = LIS ending at i, or a binary-search optimization

## Approach

This is solved with **the patience-sorting / binary-search optimization achieving O(n log n)**:

1. Maintain a `tails` array where `tails[k]` is the smallest possible tail value of any increasing subsequence of length `k + 1`.
2. For each number, use binary search (`bisect_left`) to find its insertion position in `tails`.
3. If the number is larger than every element in `tails`, append it, extending the longest subsequence found so far by one.
4. Otherwise, overwrite `tails[idx]` with the number, since it gives a smaller possible tail for subsequences of that length (improving future extensibility) without changing `tails`' length.
5. The final length of `tails` is the length of the longest increasing subsequence.

**Time Complexity:** O(n log n) — each element performs one binary search over the `tails` array.
**Space Complexity:** O(n) — for the `tails` array tracking the smallest tail of increasing subsequences of each length.

## Reference Solution (Python)

```python
from bisect import bisect_left


def lengthOfLIS(nums: list[int]) -> int:
    tails: list[int] = []

    for num in nums:
        idx = bisect_left(tails, num)
        if idx == len(tails):
            tails.append(num)
        else:
            tails[idx] = num

    return len(tails)
```

## Reference

- LeetCode: https://leetcode.com/problems/longest-increasing-subsequence/
