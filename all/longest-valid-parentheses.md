# 32. Longest Valid Parentheses

**Difficulty:** Hard
**Topics:** String, Dynamic Programming, Stack
**Common companies:** All big tech
**Category (README):** 12.2 2D DP

## Problem Description

Given a string containing just the characters `'('` and `')'`, return *the length of the longest valid (well-formed) parentheses **substring*.

 

**Example 1:**

```

**Input:** s = "(()"
**Output:** 2
**Explanation:** The longest valid parentheses substring is "()".

```

**Example 2:**

```

**Input:** s = ")()())"
**Output:** 4
**Explanation:** The longest valid parentheses substring is "()()".

```

**Example 3:**

```

**Input:** s = ""
**Output:** 0

```

 

**Constraints:**

	
- `0 <= s.length <= 3 * 104`

	
- `s[i]` is `'('`, or `')'`.

## Key Idea

DP, or a stack tracking unmatched open-bracket positions

## Approach

1. Identify the core pattern for this category: **12.2 2D DP**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/longest-valid-parentheses/
