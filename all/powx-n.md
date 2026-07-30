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

1. Identify the core pattern for this category: **14. Bit Manipulation & Math**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/powx-n/
