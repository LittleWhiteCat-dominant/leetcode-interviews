# 862. Shortest Subarray with Sum at Least K

**Difficulty:** Hard
**Topics:** Array, Binary Search, Queue, Sliding Window, Heap (Priority Queue), Prefix Sum, Monotonic Queue
**Common companies:** Google
**Category (README):** 5. Queue / Monotonic Queue

## Problem Description

Given an integer array `nums` and an integer `k`, return *the length of the shortest non-empty **subarray** of *`nums`* with a sum of at least *`k`. If there is no such **subarray**, return `-1`.

A **subarray** is a **contiguous** part of an array.

 

**Example 1:**

```
**Input:** nums = [1], k = 1
**Output:** 1

```

**Example 2:**

```
**Input:** nums = [1,2], k = 4
**Output:** -1

```

**Example 3:**

```
**Input:** nums = [2,-1,2], k = 3
**Output:** 3

```

 

**Constraints:**

	
- `1 <= nums.length <= 105`

	
- `-105 <= nums[i] <= 105`

	
- `1 <= k <= 109`

## Key Idea

Monotonic queue / prefix sum optimization

## Approach

This is solved with **prefix sums combined with a monotonic increasing deque of indices**:

1. Build a prefix-sum array `prefix` of length `n + 1`, where `prefix[i]` is the sum of the first `i` elements.
2. Maintain a deque of indices into `prefix` whose corresponding values are strictly increasing; any subarray sum can be read as `prefix[j] - prefix[i]` for `i < j`.
3. For each new index `i`, while the front of the deque gives a subarray sum `prefix[i] - prefix[front] >= k`, that candidate is optimal for `i` (and can only get worse as more elements are added), so pop it from the front and update the best (minimum) length found.
4. Before pushing index `i`, pop indices from the back of the deque whose prefix value is `>= prefix[i]`, since they can never produce a shorter valid subarray than `i` would (a smaller or equal prefix at a later index dominates).
5. After processing all indices, return the best length found, or `-1` if no valid subarray existed.

**Time Complexity:** O(n) — each prefix-sum index is pushed and popped from the deque at most once.
**Space Complexity:** O(n) — the prefix sum array and the monotonic deque.

## Reference Solution (Python)

```python
from collections import deque

def shortestSubarray(nums: list[int], k: int) -> int:
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(n):
        prefix[i + 1] = prefix[i] + nums[i]

    result = n + 1
    dq = deque()

    for i, p in enumerate(prefix):
        while dq and p - prefix[dq[0]] >= k:
            result = min(result, i - dq.popleft())
        while dq and prefix[dq[-1]] >= p:
            dq.pop()
        dq.append(i)

    return result if result <= n else -1
```

## Reference

- LeetCode: https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/
