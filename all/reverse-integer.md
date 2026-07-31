# 7. Reverse Integer

**Difficulty:** Medium
**Topics:** Math
**Common companies:** All big tech
**Category (README):** 14. Bit Manipulation & Math

## Problem Description

Given a signed 32-bit integer `x`, return `x`* with its digits reversed*. If reversing `x` causes the value to go outside the signed 32-bit integer range `[-231, 231 - 1]`, then return `0`.

**Assume the environment does not allow you to store 64-bit integers (signed or unsigned).**

 

**Example 1:**

```

**Input:** x = 123
**Output:** 321

```

**Example 2:**

```

**Input:** x = -123
**Output:** -321

```

**Example 3:**

```

**Input:** x = 120
**Output:** 21

```

 

**Constraints:**

	
- `-231 <= x <= 231 - 1`

## Key Idea

Build digit by digit with modulo, watch for overflow

## Approach

This is solved with **digit-by-digit extraction via modulo/division, with an overflow guard**:

1. Record the sign of `x`, then work with its absolute value so the digit extraction logic stays sign-agnostic.
2. Repeatedly peel off the last digit with `x % 10` and shrink `x` with `x //= 10`.
3. Build up the reversed number by doing `result = result * 10 + digit` on each iteration.
4. After each multiplication, check whether `result` has already exceeded the 32-bit signed max; if so, return `0` immediately instead of continuing.
5. Once `x` is fully consumed, reapply the sign and do a final range check against `[INT_MIN, INT_MAX]` before returning.

**Time Complexity:** O(log₁₀|x|) — one iteration per digit of `x`.
**Space Complexity:** O(1) — only a handful of scalar variables.

## Reference Solution (Python)

```python
def reverse(x: int) -> int:
    INT_MIN, INT_MAX = -2**31, 2**31 - 1
    sign = -1 if x < 0 else 1
    x = abs(x)

    result = 0
    while x:
        digit = x % 10
        x //= 10
        result = result * 10 + digit
        if result > INT_MAX:
            return 0

    result *= sign
    return result if INT_MIN <= result <= INT_MAX else 0
```

## Reference

- LeetCode: https://leetcode.com/problems/reverse-integer/
