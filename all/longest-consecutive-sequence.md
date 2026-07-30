# 128. Longest Consecutive Sequence

**Difficulty:** Medium
**Topics:** Array, Hash Table, Union-Find
**Common companies:** **Google, Meta favorite**
**Category (README):** 6. Hash Table

## Problem Description

Given an unsorted array of integers `nums`, return *the length of the longest consecutive elements sequence.*

You must write an algorithm that runs in `O(n)` time.

 

**Example 1:**

```

**Input:** nums = [100,4,200,1,3,2]
**Output:** 4
**Explanation:** The longest consecutive elements sequence is `[1, 2, 3, 4]`. Therefore its length is 4.

```

**Example 2:**

```

**Input:** nums = [0,3,7,2,5,8,4,6,0,1]
**Output:** 9

```

**Example 3:**

```

**Input:** nums = [1,0,1,2]
**Output:** 3

```

 

**Constraints:**

	
- `0 <= nums.length <= 105`

	
- `-109 <= nums[i] <= 109`

## Key Idea

Hash set for O(1) lookup; only expand from sequence starting points

## Approach

1. Identify the core pattern for this category: **6. Hash Table**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — each number is visited a constant number of times because inner while-loops only run for true sequence starting points.
**Space Complexity:** O(n) — for the hash set holding all numbers.

## Reference Solution (Python)

```python
def longestConsecutive(nums: list[int]) -> int:
    num_set = set(nums)
    longest = 0

    for num in num_set:
        if num - 1 not in num_set:
            length = 1
            while num + length in num_set:
                length += 1
            longest = max(longest, length)

    return longest
```

## Reference

- LeetCode: https://leetcode.com/problems/longest-consecutive-sequence/
