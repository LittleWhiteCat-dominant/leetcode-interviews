# 91. Decode Ways

**Difficulty:** Medium
**Topics:** String, Dynamic Programming
**Common companies:** All big tech
**Category (README):** 12.1 1D DP

## Problem Description

You have intercepted a secret message encoded as a string of numbers. The message is **decoded** via the following mapping:

`"1" -> 'A'

"2" -> 'B'

...

"25" -> 'Y'

"26" -> 'Z'`

However, while decoding the message, you realize that there are many different ways you can decode the message because some codes are contained in other codes (`"2"` and `"5"` vs `"25"`).

For example, `"11106"` can be decoded into:

	
- `"AAJF"` with the grouping `(1, 1, 10, 6)`

	
- `"KJF"` with the grouping `(11, 10, 6)`

	
- The grouping `(1, 11, 06)` is invalid because `"06"` is not a valid code (only `"6"` is valid).

Note: there may be strings that are impossible to decode.

Given a string s containing only digits, return the **number of ways** to **decode** it. If the entire string cannot be decoded in any valid way, return `0`.

The test cases are generated so that the answer fits in a **32-bit** integer.

 

**Example 1:**

**Input:** s = "12"

**Output:** 2

**Explanation:**

"12" could be decoded as "AB" (1 2) or "L" (12).

**Example 2:**

**Input:** s = "226"

**Output:** 3

**Explanation:**

"226" could be decoded as "BZ" (2 26), "VF" (22 6), or "BBF" (2 2 6).

**Example 3:**

**Input:** s = "06"

**Output:** 0

**Explanation:**

"06" cannot be mapped to "F" because of the leading zero ("6" is different from "06"). In this case, the string is not a valid encoding, so return 0.

 

**Constraints:**

	
- `1 <= s.length <= 100`

	
- `s` contains only digits and may contain leading zero(s).

## Key Idea

String DP; careful with "0" and valid two-digit ranges

## Approach

1. Identify the core pattern for this category: **12.1 1D DP**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — a single pass through the string with constant work per position.
**Space Complexity:** O(1) — only the previous two DP states are kept.

## Reference Solution (Python)

```python
def numDecodings(s: str) -> int:
    if not s or s[0] == '0':
        return 0

    n = len(s)
    prev2, prev1 = 1, 1  # dp[i - 2], dp[i - 1]

    for i in range(1, n):
        current = 0
        if s[i] != '0':
            current += prev1
        two_digit = int(s[i - 1:i + 1])
        if 10 <= two_digit <= 26:
            current += prev2
        prev2, prev1 = prev1, current

    return prev1
```

## Reference

- LeetCode: https://leetcode.com/problems/decode-ways/
