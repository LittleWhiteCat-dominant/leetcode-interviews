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

This is solved with **dynamic programming reusing previously computed bit counts**:

1. Initialize `ans[0] = 0`, since zero has no set bits.
2. For each `i` from 1 to `n`, note that `i >> 1` drops the lowest bit of `i`, so `ans[i >> 1]` already gives the popcount of everything above that lowest bit.
3. Add back `i & 1`, which is 1 if the lowest bit of `i` is set and 0 otherwise, giving the transition `ans[i] = ans[i >> 1] + (i & 1)`.
4. Fill the array left to right so that `ans[i >> 1]` is always already computed by the time it's needed.

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
