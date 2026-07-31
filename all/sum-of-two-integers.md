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

This is solved with **bitwise addition simulation using XOR for sum and AND-shift for carry**:

1. Mask both `a` and `b` to 32 bits so Python's arbitrary-precision integers behave like fixed-width signed integers throughout the computation.
2. Loop while there is a nonzero carry: XOR gives the sum of `a` and `b` ignoring carries, while `(a & b) << 1` gives the carry bits that need to be added in next.
3. Set `a` to the XOR result and `b` to the masked carry, then repeat until `b` becomes `0`.
4. Once the loop ends, `a` holds the raw 32-bit unsigned result.
5. If that value's highest bit indicates it should be interpreted as negative (i.e., it exceeds the max positive 32-bit signed value), convert it back to a proper negative Python integer via two's-complement inversion before returning.

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
