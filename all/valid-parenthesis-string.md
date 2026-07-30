# 678. Valid Parenthesis String

**Difficulty:** Medium
**Topics:** String, Dynamic Programming, Stack, Greedy
**Common companies:** Google, Meta
**Category (README):** 13. Greedy

## Problem Description

Given a string `s` containing only three types of characters: `'('`, `')'` and `'*'`, return `true` *if* `s` *is **valid***.

The following rules define a **valid** string:

	
- Any left parenthesis `'('` must have a corresponding right parenthesis `')'`.

	
- Any right parenthesis `')'` must have a corresponding left parenthesis `'('`.

	
- Left parenthesis `'('` must go before the corresponding right parenthesis `')'`.

	
- `'*'` could be treated as a single right parenthesis `')'` or a single left parenthesis `'('` or an empty string `""`.

 

**Example 1:**

```
**Input:** s = "()"
**Output:** true

```

**Example 2:**

```
**Input:** s = "(*)"
**Output:** true

```

**Example 3:**

```
**Input:** s = "(*))"
**Output:** true

```

 

**Constraints:**

	
- `1 <= s.length <= 100`

	
- `s[i]` is `'('`, `')'` or `'*'`.

## Key Idea

Greedily maintain the possible range of open-bracket counts

## Approach

1. Identify the core pattern for this category: **13. Greedy**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/valid-parenthesis-string/
