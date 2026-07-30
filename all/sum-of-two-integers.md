# 371. Sum of Two Integers

**Difficulty:** Medium
**Topics:** Math, Bit Manipulation
**Common companies:** Apple, Amazon
**Category (README):** 14. Bit Manipulation & Math

## Problem Description

Given two integers `a` and `b`, return *the sum of the two integers without using the operators* `+` *and* `-`.

 

**Example 1:**

```
**Input:** a = 1, b = 2
**Output:** 3

```

**Example 2:**

```
**Input:** a = 2, b = 3
**Output:** 5

```

 

**Constraints:**

	
- `-1000 <= a, b <= 1000`

## Key Idea

Simulate addition with bit operations (XOR + carry)

## Approach

1. Identify the core pattern for this category: **14. Bit Manipulation & Math**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(1) — bounded by the fixed 32-bit width, so the carry loop runs at most 32 times.
**Space Complexity:** O(1) — only a fixed number of integer variables.

## Reference Solution (Python)

```python
def getSum(a: int, b: int) -> int:
    mask = 0xFFFFFFFF
    a &= mask
    b &= mask

    while b:
        carry = (a & b) << 1 & mask
        a = a ^ b
        b = carry

    if a > 0x7FFFFFFF:
        a = ~(a ^ mask)

    return a
```

## Reference

- LeetCode: https://leetcode.com/problems/sum-of-two-integers/
