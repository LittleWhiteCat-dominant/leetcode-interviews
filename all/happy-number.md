# 202. Happy Number

**Difficulty:** Easy
**Topics:** Hash Table, Math, Two Pointers
**Common companies:** Google, Apple
**Category (README):** 6. Hash Table

## Problem Description

Write an algorithm to determine if a number `n` is happy.

A **happy number** is a number defined by the following process:

	
- Starting with any positive integer, replace the number by the sum of the squares of its digits.

	
- Repeat the process until the number equals 1 (where it will stay), or it **loops endlessly in a cycle** which does not include 1.

	
- Those numbers for which this process **ends in 1** are happy.

Return `true` *if* `n` *is a happy number, and* `false` *if not*.

 

**Example 1:**

```

**Input:** n = 19
**Output:** true
**Explanation:**
12 + 92 = 82
82 + 22 = 68
62 + 82 = 100
12 + 02 + 02 = 1

```

**Example 2:**

```

**Input:** n = 2
**Output:** false

```

 

**Constraints:**

	
- `1 <= n <= 231 - 1`

## Key Idea

Hash set to detect cycles

## Approach

1. Identify the core pattern for this category: **6. Hash Table**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(log n) per digit-square-sum step, and the cycle detection terminates in a bounded number of steps for 32-bit integers.
**Space Complexity:** O(1) — using Floyd's cycle detection avoids the O(k) hash set of visited values.

## Reference Solution (Python)

```python
def isHappy(n: int) -> bool:
    def get_next(num: int) -> int:
        total = 0
        while num > 0:
            digit = num % 10
            num //= 10
            total += digit * digit
        return total

    slow, fast = n, get_next(n)
    while fast != 1 and slow != fast:
        slow = get_next(slow)
        fast = get_next(get_next(fast))

    return fast == 1
```

## Reference

- LeetCode: https://leetcode.com/problems/happy-number/
