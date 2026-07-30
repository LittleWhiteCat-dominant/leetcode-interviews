# 115. Distinct Subsequences

**Difficulty:** Hard
**Topics:** String, Dynamic Programming
**Common companies:** Google, Amazon
**Category (README):** 12.2 2D DP

## Problem Description

Given two strings s and t, return *the number of distinct* ***subsequences**** of *s* which equals *t.

The test cases are generated so that the answer fits on a 32-bit signed integer.

 

**Example 1:**

```

**Input:** s = "rabbbit", t = "rabbit"
**Output:** 3
**Explanation:**
As shown below, there are 3 ways you can generate "rabbit" from s.
`**rabb**b**it**`
`**ra**b**bbit**`
`**rab**b**bit**`

```

**Example 2:**

```

**Input:** s = "babgbag", t = "bag"
**Output:** 5
**Explanation:**
As shown below, there are 5 ways you can generate "bag" from s.
`**ba**b**g**bag`
`**ba**bgba**g**`
`**b**abgb**ag**`
`ba**b**gb**ag**`
`babg**bag**`
```

 

**Constraints:**

	
- `1 <= s.length, t.length <= 1000`

	
- `s` and `t` consist of English letters.

## Key Idea

2D DP counting

## Approach

1. Identify the core pattern for this category: **12.2 2D DP**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(m * n) — where m = len(s), n = len(t), one DP transition per cell.
**Space Complexity:** O(n) — a single 1D DP row, updated in place from right to left.

## Reference Solution (Python)

```python
def numDistinct(s: str, t: str) -> int:
    m, n = len(s), len(t)
    dp = [0] * (n + 1)
    dp[0] = 1

    for i in range(1, m + 1):
        for j in range(n, 0, -1):
            if s[i - 1] == t[j - 1]:
                dp[j] += dp[j - 1]

    return dp[n]
```

## Reference

- LeetCode: https://leetcode.com/problems/distinct-subsequences/
