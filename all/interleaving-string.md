# 97. Interleaving String

**Difficulty:** Medium
**Topics:** String, Dynamic Programming
**Common companies:** Google, Amazon
**Category (README):** 12.2 2D DP

## Problem Description

Given strings `s1`, `s2`, and `s3`, find whether `s3` is formed by an **interleaving** of `s1` and `s2`.

An **interleaving** of two strings `s` and `t` is a configuration where `s` and `t` are divided into `n` and `m` substrings respectively, such that:

	
- `s = s1 + s2 + ... + sn`

	
- `t = t1 + t2 + ... + tm`

	
- `|n - m| <= 1`

	
- The **interleaving** is `s1 + t1 + s2 + t2 + s3 + t3 + ...` or `t1 + s1 + t2 + s2 + t3 + s3 + ...`

**Note:** `a + b` is the concatenation of strings `a` and `b`.

 

**Example 1:**

```

**Input:** s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"
**Output:** true
**Explanation:** One way to obtain s3 is:
Split s1 into s1 = "aa" + "bc" + "c", and s2 into s2 = "dbbc" + "a".
Interleaving the two splits, we get "aa" + "dbbc" + "bc" + "a" + "c" = "aadbbcbcac".
Since s3 can be obtained by interleaving s1 and s2, we return true.

```

**Example 2:**

```

**Input:** s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"
**Output:** false
**Explanation:** Notice how it is impossible to interleave s2 with any other string to obtain s3.

```

**Example 3:**

```

**Input:** s1 = "", s2 = "", s3 = ""
**Output:** true

```

 

**Constraints:**

	
- `0 <= s1.length, s2.length <= 100`

	
- `0 <= s3.length <= 200`

	
- `s1`, `s2`, and `s3` consist of lowercase English letters.

 

**Follow up:** Could you solve it using only `O(s2.length)` additional memory space?

## Key Idea

2D DP checking whether two strings can interleave into a third

## Approach

This is solved with **2D dynamic programming compressed into a rolling 1D array**:

1. First check the necessary length condition: if `len(s1) + len(s2) != len(s3)`, return `False` immediately.
2. Define `dp[j]` as whether `s3`'s prefix of the current length can be formed by interleaving `s1`'s prefix up to row `i` with `s2`'s prefix up to column `j`.
3. Initialize row 0 using only `s2` against `s3`, since no characters from `s1` are used yet.
4. For each subsequent row `i` (one character of `s1` consumed), update `dp[0]` using only `s1`, then for each `j`, combine two possibilities: `from_s1` (extend using `s1[i-1]` if `dp[j]` was true and it matches `s3[i+j-1]`) or `from_s2` (extend using `s2[j-1]` if `dp[j-1]` was true and it matches `s3[i+j-1]`).
5. The final answer is `dp[n]` after processing all rows.

**Time Complexity:** O(m * n) — where `m = len(s1)` and `n = len(s2)`; every DP cell is computed once.
**Space Complexity:** O(n) — using a rolling 1D DP row instead of a full 2D table.

## Reference Solution (Python)

```python
def isInterleave(s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False

    dp = [False] * (n + 1)
    dp[0] = True

    for j in range(1, n + 1):
        dp[j] = dp[j - 1] and s2[j - 1] == s3[j - 1]

    for i in range(1, m + 1):
        dp[0] = dp[0] and s1[i - 1] == s3[i - 1]
        for j in range(1, n + 1):
            from_s1 = dp[j] and s1[i - 1] == s3[i + j - 1]
            from_s2 = dp[j - 1] and s2[j - 1] == s3[i + j - 1]
            dp[j] = from_s1 or from_s2

    return dp[n]
```

## Reference

- LeetCode: https://leetcode.com/problems/interleaving-string/
