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

This is solved with **the `n & (n - 1)` lowest-set-bit-clearing trick**:

1. Recall that `n - 1` flips all bits after (and including) the lowest set bit of `n`, so `n & (n - 1)` clears exactly that lowest set bit while leaving all higher bits unchanged.
2. Initialize a counter to `0`.
3. Repeatedly apply `n &= n - 1` and increment the counter, each time removing one set bit from `n`.
4. Stop once `n` becomes `0` — the counter now equals the total number of set bits, and the loop runs exactly as many times as there are set bits rather than iterating over all 32 bit positions.

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
