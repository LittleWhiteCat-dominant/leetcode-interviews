# 72. Edit Distance

**Difficulty:** Medium
**Topics:** String, Dynamic Programming
**Common companies:** **Google, Meta favorite**
**Category (README):** 12.2 2D DP

## Problem Description

Given two strings `word1` and `word2`, return *the minimum number of operations required to convert `word1` to `word2`*.

You have the following three operations permitted on a word:

	
- Insert a character

	
- Delete a character

	
- Replace a character

 

**Example 1:**

```

**Input:** word1 = "horse", word2 = "ros"
**Output:** 3
**Explanation:** 
horse -> rorse (replace 'h' with 'r')
rorse -> rose (remove 'r')
rose -> ros (remove 'e')

```

**Example 2:**

```

**Input:** word1 = "intention", word2 = "execution"
**Output:** 5
**Explanation:** 
intention -> inention (remove 't')
inention -> enention (replace 'i' with 'e')
enention -> exention (replace 'n' with 'x')
exention -> exection (replace 'n' with 'c')
exection -> execution (insert 'u')

```

 

**Constraints:**

	
- `0 <= word1.length, word2.length <= 500`

	
- `word1` and `word2` consist of lowercase English letters.

## Key Idea

Three transitions: insert/delete/replace

## Approach

1. Identify the core pattern for this category: **12.2 2D DP**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(m * n) — where m = len(word1), n = len(word2), one DP transition per cell.
**Space Complexity:** O(n) — a single 1D DP row, updated in place with a rolling `prev` value for the diagonal term.

## Reference Solution (Python)

```python
def minDistance(word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = list(range(n + 1))

    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(prev, dp[j], dp[j - 1])
            prev = temp

    return dp[n]
```

## Reference

- LeetCode: https://leetcode.com/problems/edit-distance/
