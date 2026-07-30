# 338. Counting Bits

**Difficulty:** Easy
**Topics:** Dynamic Programming, Bit Manipulation
**Common companies:** All big tech
**Category (README):** 14. Bit Manipulation & Math

## Problem Description

Given an integer `n`, return *an array *`ans`* of length *`n + 1`* such that for each *`i`* *(`0 <= i <= n`)*, *`ans[i]`* is the **number of ***`1`***'s** in the binary representation of *`i`.

Do not solve it with built-in functions (i.e., like `__builtin_popcount` in C++).

 

**Example 1:**

```

**Input:** n = 2
**Output:** [0,1,1]
**Explanation:**
0 --> 0
1 --> 1
2 --> 10

```

**Example 2:**

```

**Input:** n = 5
**Output:** [0,1,1,2,1,2]
**Explanation:**
0 --> 0
1 --> 1
2 --> 10
3 --> 11
4 --> 100
5 --> 101

```

 

**Constraints:**

	
- `0 <= n <= 105`

 

**Follow up:**

	
- It is very easy to come up with a solution with a runtime of `O(n log n)`. Can you do it in linear time `O(n)` and possibly in a single pass?

## Key Idea

dp[i] = dp[i >> 1] + (i & 1)

## Approach

1. Identify the core pattern for this category: **14. Bit Manipulation & Math**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — one constant-time DP transition per value from 1 to n.
**Space Complexity:** O(n) — the output array itself (O(1) extra beyond it).

## Reference Solution (Python)

```python
def countBits(n: int) -> list[int]:
    ans = [0] * (n + 1)
    for i in range(1, n + 1):
        ans[i] = ans[i >> 1] + (i & 1)
    return ans
```

## Reference

- LeetCode: https://leetcode.com/problems/counting-bits/
