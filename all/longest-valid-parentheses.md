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

This is solved with **a stack that tracks indices of unmatched characters, seeded with a base index of -1**:

1. Initialize a stack with `-1` as a sentinel base for length calculations.
2. For each `'('`, push its index onto the stack.
3. For each `')'`, pop the stack; if the stack becomes empty, this `')'` is unmatched, so push its index as the new base.
4. If the stack is non-empty after popping, the current valid substring length is `i - stack[-1]`, so update the running maximum.
5. Repeat through the whole string and return the maximum valid length found.

**Time Complexity:** O(n) — each index is pushed and popped from the stack at most once.
**Space Complexity:** O(n) — for the stack of unmatched indices.

## Reference Solution (Python)

```python
def longestValidParentheses(s: str) -> int:
    stack = [-1]
    longest = 0

    for i, ch in enumerate(s):
        if ch == '(':
            stack.append(i)
        else:
            stack.pop()
            if not stack:
                stack.append(i)
            else:
                longest = max(longest, i - stack[-1])

    return longest
```

## Reference

- LeetCode: https://leetcode.com/problems/longest-valid-parentheses/
