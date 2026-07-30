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

1. Identify the core pattern for this category: **5. Queue / Monotonic Queue**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/
