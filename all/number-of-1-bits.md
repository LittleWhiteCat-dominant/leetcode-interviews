# 191. Number of 1 Bits

**Difficulty:** Easy
**Topics:** Divide and Conquer, Bit Manipulation
**Common companies:** All big tech
**Category (README):** 14. Bit Manipulation & Math

## Problem Description

Given a positive integer `n`, write a function that returns the number of set bits in its binary representation (also known as the Hamming weight).

 

**Example 1:**

**Input:** n = 11

**Output:** 3

**Explanation:**

The input binary string **1011** has a total of three set bits.

**Example 2:**

**Input:** n = 128

**Output:** 1

**Explanation:**

The input binary string **10000000** has a total of one set bit.

**Example 3:**

**Input:** n = 2147483645

**Output:** 30

**Explanation:**

The input binary string **1111111111111111111111111111101** has a total of thirty set bits.

 

**Constraints:**

	
- `1 <= n <= 231 - 1`

 

**Follow up:** If this function is called many times, how would you optimize it?

## Key Idea

n & (n-1) clears the lowest set bit

## Approach

1. Identify the core pattern for this category: **14. Bit Manipulation & Math**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(k) — where `k` is the number of set bits (at most 32); each iteration clears exactly one set bit.
**Space Complexity:** O(1) — only a counter is used.

## Reference Solution (Python)

```python
def hammingWeight(n: int) -> int:
    count = 0
    while n:
        n &= n - 1
        count += 1
    return count
```

## Reference

- LeetCode: https://leetcode.com/problems/number-of-1-bits/
