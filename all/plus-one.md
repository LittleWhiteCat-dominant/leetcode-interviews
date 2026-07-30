# 66. Plus One

**Difficulty:** Easy
**Topics:** Array, Math
**Common companies:** Google, Apple
**Category (README):** 14. Bit Manipulation & Math

## Problem Description

You are given a **large integer** represented as an integer array `digits`, where each `digits[i]` is the `ith` digit of the integer. The digits are ordered from most significant to least significant in left-to-right order. The large integer does not contain any leading `0`'s.

Increment the large integer by one and return *the resulting array of digits*.

 

**Example 1:**

```

**Input:** digits = [1,2,3]
**Output:** [1,2,4]
**Explanation:** The array represents the integer 123.
Incrementing by one gives 123 + 1 = 124.
Thus, the result should be [1,2,4].

```

**Example 2:**

```

**Input:** digits = [4,3,2,1]
**Output:** [4,3,2,2]
**Explanation:** The array represents the integer 4321.
Incrementing by one gives 4321 + 1 = 4322.
Thus, the result should be [4,3,2,2].

```

**Example 3:**

```

**Input:** digits = [9]
**Output:** [1,0]
**Explanation:** The array represents the integer 9.
Incrementing by one gives 9 + 1 = 10.
Thus, the result should be [1,0].

```

 

**Constraints:**

	
- `1 <= digits.length <= 100`

	
- `0 <= digits[i] <= 9`

	
- `digits` does not contain any leading `0`'s.

## Key Idea

Simulate digit-wise addition with carry on an array

## Approach

1. Identify the core pattern for this category: **14. Bit Manipulation & Math**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — at most one pass through the digits.
**Space Complexity:** O(1) extra — modifies `digits` in place (a new array is only allocated on overflow).

## Reference Solution (Python)

```python
from typing import List

def plusOne(digits: List[int]) -> List[int]:
    n = len(digits)
    for i in range(n - 1, -1, -1):
        if digits[i] < 9:
            digits[i] += 1
            return digits
        digits[i] = 0

    return [1] + digits
```

## Reference

- LeetCode: https://leetcode.com/problems/plus-one/
