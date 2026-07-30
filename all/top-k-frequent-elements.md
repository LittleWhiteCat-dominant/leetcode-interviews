# 347. Top K Frequent Elements

**Difficulty:** Medium
**Topics:** Array, Hash Table, Divide and Conquer, Sorting, Heap (Priority Queue), Bucket Sort, Counting, Quickselect
**Common companies:** All big tech
**Category (README):** 8. Heap / Priority Queue

## Problem Description

Given an integer array `nums` and an integer `k`, return *the* `k` *most frequent elements*. You may return the answer in **any order**.

 

**Example 1:**

**Input:** nums = [1,1,1,2,2,3], k = 2

**Output:** [1,2]

**Example 2:**

**Input:** nums = [1], k = 1

**Output:** [1]

**Example 3:**

**Input:** nums = [1,2,1,2,1,2,3,1,3,2], k = 2

**Output:** [1,2]

 

**Constraints:**

	
- `1 <= nums.length <= 105`

	
- `-104 <= nums[i] <= 104`

	
- `k` is in the range `[1, the number of unique elements in the array]`.

	
- It is **guaranteed** that the answer is **unique**.

 

**Follow up:** Your algorithm's time complexity must be better than `O(n log n)`, where n is the array's size.

## Key Idea

Hash-map counting + min-heap keeping the top K

## Approach

1. Identify the core pattern for this category: **8. Heap / Priority Queue**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n log k) — counting is O(n), and maintaining a heap of size `k` over the distinct elements beats the required O(n log n) bound.
**Space Complexity:** O(n) — the frequency map plus the heap.

## Reference Solution (Python)

```python
import heapq
from collections import Counter


def topKFrequent(nums: list[int], k: int) -> list[int]:
    counts = Counter(nums)
    return heapq.nlargest(k, counts.keys(), key=counts.get)
```

## Reference

- LeetCode: https://leetcode.com/problems/top-k-frequent-elements/
