# 1249. Minimum Remove to Make Valid Parentheses

**Difficulty:** Medium
**Topics:** String, Stack
**Common companies:** **Meta favorite**
**Category (README):** 2. String

## Problem Description

Given a string s of `'('` , `')'` and lowercase English characters.

Your task is to remove the minimum number of parentheses ( `'('` or `')'`, in any positions ) so that the resulting *parentheses string* is valid and return **any** valid string.

Formally, a *parentheses string* is valid if and only if:

	
- It is the empty string, contains only lowercase characters, or

	
- It can be written as `AB` (`A` concatenated with `B`), where `A` and `B` are valid strings, or

	
- It can be written as `(A)`, where `A` is a valid string.

 

**Example 1:**

```

**Input:** s = "lee(t(c)o)de)"
**Output:** "lee(t(c)o)de"
**Explanation:** "lee(t(co)de)" , "lee(t(c)ode)" would also be accepted.

```

**Example 2:**

```

**Input:** s = "a)b(c)d"
**Output:** "ab(c)d"

```

**Example 3:**

```

**Input:** s = "))(("
**Output:** ""
**Explanation:** An empty string is also valid.

```

 

**Constraints:**

	
- `1 <= s.length <= 105`

	
- `s[i]` is either `'('` , `')'`, or lowercase English letter.

## Key Idea

Stack tracking indices to delete

## Approach

1. Identify the core pattern for this category: **2. String**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/
