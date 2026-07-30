# 43. Multiply Strings

**Difficulty:** Medium
**Topics:** Math, String, Simulation
**Common companies:** Google, Meta
**Category (README):** 2. String

## Problem Description

Given two non-negative integers `num1` and `num2` represented as strings, return the product of `num1` and `num2`, also represented as a string.

**Note:** You must not use any built-in BigInteger library or convert the inputs to integer directly.

 

**Example 1:**

```
**Input:** num1 = "2", num2 = "3"
**Output:** "6"

```

**Example 2:**

```
**Input:** num1 = "123", num2 = "456"
**Output:** "56088"

```

 

**Constraints:**

	
- `1 <= num1.length, num2.length <= 200`

	
- `num1` and `num2` consist of digits only.

	
- Both `num1` and `num2` do not contain any leading zero, except the number `0` itself.

## Key Idea

Simulate long multiplication

## Approach

1. Identify the core pattern for this category: **2. String**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(m * n) — every pair of digits from `num1` and `num2` is multiplied once.
**Space Complexity:** O(m + n) — for the intermediate digit-product buffer.

## Reference Solution (Python)

```python
def multiply(num1: str, num2: str) -> str:
    if num1 == "0" or num2 == "0":
        return "0"

    m, n = len(num1), len(num2)
    result = [0] * (m + n)

    for i in range(m - 1, -1, -1):
        for j in range(n - 1, -1, -1):
            mul = int(num1[i]) * int(num2[j])
            p1, p2 = i + j, i + j + 1
            total = mul + result[p2]
            result[p2] = total % 10
            result[p1] += total // 10

    start = 0
    while start < len(result) - 1 and result[start] == 0:
        start += 1

    return ''.join(map(str, result[start:]))
```

## Reference

- LeetCode: https://leetcode.com/problems/multiply-strings/
