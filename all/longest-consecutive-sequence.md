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

This is solved with **a hash set plus only expanding from true sequence starts to keep the algorithm O(n)**:

1. Put all numbers into a hash set for O(1) membership checks.
2. For each number, check whether `num - 1` is in the set; if it is, `num` is not the start of a sequence, so skip it.
3. If `num` is a sequence start (no predecessor in the set), repeatedly check `num + length` in the set, incrementing `length` until the chain breaks.
4. Track the maximum `length` found across all sequence starts and return it.

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
