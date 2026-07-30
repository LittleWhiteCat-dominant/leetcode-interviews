# 41. First Missing Positive

**Difficulty:** Hard
**Topics:** Array, Hash Table
**Common companies:** All big tech
**Category (README):** 6. Hash Table

## Problem Description

Given an unsorted integer array `nums`. Return the *smallest positive integer* that is *not present* in `nums`.

You must implement an algorithm that runs in `O(n)` time and uses `O(1)` auxiliary space.

 

**Example 1:**

```

**Input:** nums = [1,2,0]
**Output:** 3
**Explanation:** The numbers in the range [1,2] are all in the array.

```

**Example 2:**

```

**Input:** nums = [3,4,-1,1]
**Output:** 2
**Explanation:** 1 is in the array but 2 is missing.

```

**Example 3:**

```

**Input:** nums = [7,8,9,11,12]
**Output:** 1
**Explanation:** The smallest positive integer 1 is missing.

```

 

**Constraints:**

	
- `1 <= nums.length <= 105`

	
- `-231 <= nums[i] <= 231 - 1`

## Key Idea

In-place hashing by placing each value at its target index

## Approach

1. Identify the core pattern for this category: **6. Hash Table**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — each element is swapped into place at most once, amortized across the single pass.
**Space Complexity:** O(1) — the input array is rearranged in place, no extra data structures.

## Reference Solution (Python)

```python
def firstMissingPositive(nums: list[int]) -> int:
    n = len(nums)

    for i in range(n):
        while 1 <= nums[i] <= n and nums[nums[i] - 1] != nums[i]:
            target = nums[i] - 1
            nums[i], nums[target] = nums[target], nums[i]

    for i in range(n):
        if nums[i] != i + 1:
            return i + 1

    return n + 1
```

## Reference

- LeetCode: https://leetcode.com/problems/first-missing-positive/
