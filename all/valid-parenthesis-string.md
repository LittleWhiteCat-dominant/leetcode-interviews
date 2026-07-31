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

This is solved with **a greedy range-tracking scan over possible open-bracket counts**:

1. Instead of trying every interpretation of `'*'`, track the range `[low, high]` of possible counts of unmatched open parentheses after processing each character.
2. For `'('`, both `low` and `high` increase by 1 (it's always an open bracket).
3. For `')'`, both `low` and `high` decrease by 1 (it's always a close bracket).
4. For `'*'`, treat it optimistically as widening the range: `low` decreases by 1 (as if it were `')'`) and `high` increases by 1 (as if it were `'('`).
5. If `high` ever drops below 0, too many close brackets are forced no matter how `'*'` is interpreted, so return `false` immediately; clamp `low` at 0 since it can't represent a negative count of real open brackets.
6. After the scan, the string is valid if `low` can reach exactly 0, meaning `0` is a strictly feasible value in the final range.

**Time Complexity:** O(n) — a single pass tracking the feasible range of open-bracket counts.
**Space Complexity:** O(1) — only two running bounds (`low`, `high`) are kept.

## Reference Solution (Python)

```python
def checkValidString(s: str) -> bool:
    low, high = 0, 0

    for ch in s:
        if ch == '(':
            low += 1
            high += 1
        elif ch == ')':
            low -= 1
            high -= 1
        else:
            low -= 1
            high += 1

        if high < 0:
            return False
        low = max(low, 0)

    return low == 0
```

## Reference

- LeetCode: https://leetcode.com/problems/valid-parenthesis-string/
