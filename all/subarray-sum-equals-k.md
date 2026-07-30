# 560. Subarray Sum Equals K

**Difficulty:** Medium
**Topics:** Array, Hash Table, Prefix Sum
**Common companies:** **Meta favorite**
**Category (README):** 1.3 Prefix Sum

## Problem Description

Given an array of integers `nums` and an integer `k`, return *the total number of subarrays whose sum equals to* `k`.

A subarray is a contiguous **non-empty** sequence of elements within an array.

 

**Example 1:**

```
**Input:** nums = [1,1,1], k = 2
**Output:** 2

```

**Example 2:**

```
**Input:** nums = [1,2,3], k = 3
**Output:** 2

```

 

**Constraints:**

	
- `1 <= nums.length <= 2 * 104`

	
- `-1000 <= nums[i] <= 1000`

	
- `-107 <= k <= 107`

## Key Idea

Prefix sum + hash map counting occurrences

## Approach

1. Identify the core pattern for this category: **1.3 Prefix Sum**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — one pass while maintaining running prefix sums and a hash map.
**Space Complexity:** O(n) — the hash map can store up to n distinct prefix sums.

## Reference Solution (Python)

```python
from collections import defaultdict

def subarraySum(nums: list[int], k: int) -> int:
    count = 0
    prefix_sum = 0
    seen = defaultdict(int)
    seen[0] = 1

    for num in nums:
        prefix_sum += num
        count += seen[prefix_sum - k]
        seen[prefix_sum] += 1

    return count
```

## Reference

- LeetCode: https://leetcode.com/problems/subarray-sum-equals-k/
