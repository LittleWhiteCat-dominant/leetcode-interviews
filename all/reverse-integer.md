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

1. Identify the core pattern for this category: **14. Bit Manipulation & Math**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/reverse-integer/
