# 50. Pow(x, n)

**Difficulty:** Medium
**Topics:** Math, Recursion
**Common companies:** All big tech
**Category (README):** 14. Bit Manipulation & Math

## Problem Description

Implement pow(x, n), which calculates `x` raised to the power `n` (i.e., `xn`).

 

**Example 1:**

```

**Input:** x = 2.00000, n = 10
**Output:** 1024.00000

```

**Example 2:**

```

**Input:** x = 2.10000, n = 3
**Output:** 9.26100

```

**Example 3:**

```

**Input:** x = 2.00000, n = -2
**Output:** 0.25000
**Explanation:** 2-2 = 1/22 = 1/4 = 0.25

```

 

**Constraints:**

	
- `-100.0 < x < 100.0`

	
- `-231 <= n <= 231-1`

	
- `n` is an integer.

	
- Either `x` is not zero or `n > 0`.

	
- `-104 <= xn <= 104`

## Key Idea

Fast exponentiation, recursive or iterative binary splitting

## Approach

This is solved with **iterative fast exponentiation (binary exponentiation)**:

1. If `n` is negative, rewrite the problem as `(1/x)^(-n)` by inverting `x` and negating `n`, so the rest of the algorithm only handles non-negative exponents.
2. Maintain a `result` accumulator (starting at 1.0) and repeatedly examine `n` in binary, one bit at a time.
3. If the current lowest bit of `n` is 1, multiply `result` by the current value of `x` — this contributes `x` raised to that bit's place value.
4. Square `x` on every iteration (`x *= x`) and right-shift `n` by one bit (`n >>= 1`), so `x` always represents `x` raised to the power of the current bit's place value.
5. Repeat until `n` becomes 0; `result` then holds `x^n`, computed in O(log n) multiplications instead of O(n).

**Time Complexity:** O(log n) — the exponent is halved on each iteration of fast exponentiation.
**Space Complexity:** O(1) — computed iteratively with no extra recursion stack.

## Reference Solution (Python)

```python
def myPow(x: float, n: int) -> float:
    if n < 0:
        x = 1 / x
        n = -n

    result = 1.0
    while n:
        if n & 1:
            result *= x
        x *= x
        n >>= 1

    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/powx-n/
