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

This is solved with **running prefix sums combined with a hash map of prefix-sum frequencies**:

1. Maintain a running `prefix_sum` as you scan `nums` left to right, and a hash map `seen` counting how many times each prefix-sum value has occurred so far (initialized with `seen[0] = 1` to account for subarrays starting at index 0).
2. A subarray ending at the current index sums to `k` exactly when there was an earlier prefix sum equal to `prefix_sum - k`.
3. At each step, look up `seen[prefix_sum - k]` and add that count to the running total — this counts every valid subarray ending here in O(1).
4. Then record the current `prefix_sum` in `seen` by incrementing its count, so future indices can match against it.
5. Return the accumulated total after processing the whole array.

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
