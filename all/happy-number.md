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

## Reference

- LeetCode: https://leetcode.com/problems/happy-number/
