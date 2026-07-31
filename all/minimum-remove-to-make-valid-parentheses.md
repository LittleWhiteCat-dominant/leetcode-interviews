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

This is solved with **a stack that records indices of unmatched parentheses**:

1. Scan the string left to right; push the index of each `(` onto a stack.
2. For each `)`, if the stack is non-empty, pop it (the `)` is matched); otherwise this `)` is unmatched, so add its index to a `to_remove` set.
3. After the scan, any indices still left on the stack are unmatched `(` characters, so add them to `to_remove` too.
4. Build the result by keeping only the characters whose index is not in `to_remove`.

**Time Complexity:** O(n) — one pass to find indices to remove, one pass to build the result.
**Space Complexity:** O(n) — for the stack and the set of indices to remove.

## Reference Solution (Python)

```python
def minRemoveToMakeValid(s: str) -> str:
    to_remove = set()
    stack: list[int] = []

    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        elif ch == ')':
            if stack:
                stack.pop()
            else:
                to_remove.add(i)

    to_remove.update(stack)
    return ''.join(ch for i, ch in enumerate(s) if i not in to_remove)
```

## Reference

- LeetCode: https://leetcode.com/problems/minimum-remove-to-make-valid-parentheses/
