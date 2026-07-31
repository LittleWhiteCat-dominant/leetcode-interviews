# 22. Generate Parentheses

**Difficulty:** Medium
**Topics:** String, Dynamic Programming, Backtracking
**Common companies:** Google, Meta
**Category (README):** 4.1 Basic Stack Applications

## Problem Description

Given `n` pairs of parentheses, write a function to *generate all combinations of well-formed parentheses*.

 

**Example 1:**

```
**Input:** n = 3
**Output:** ["((()))","(()())","(())()","()(())","()()()"]

```

**Example 2:**

```
**Input:** n = 1
**Output:** ["()"]

```

 

**Constraints:**

	
- `1 <= n <= 8`

## Key Idea

Backtracking + stack-style pruning (open count ≥ close count)

## Approach

This is solved with **backtracking, pruning any prefix that could never become balanced**:

1. Build strings character by character via DFS, tracking how many `(` and `)` have been placed so far.
2. Only add `(` if `open_count < n` (there's still room to open more pairs).
3. Only add `)` if `close_count < open_count` (never close more than currently open, which would make the prefix invalid).
4. When the current string reaches length `2 * n`, it is guaranteed to be a valid combination, so record it.
5. Backtrack by undoing the last character after each branch to explore the next possibility.

**Time Complexity:** O(4^n / sqrt(n)) — bounded by the nth Catalan number, the count of valid parentheses combinations.
**Space Complexity:** O(4^n / sqrt(n)) for the output, plus O(n) recursion depth for the call stack.

## Reference Solution (Python)

```python
def generateParenthesis(n: int) -> list[str]:
    result: list[str] = []

    def backtrack(current: list[str], open_count: int, close_count: int) -> None:
        if len(current) == 2 * n:
            result.append("".join(current))
            return
        if open_count < n:
            current.append("(")
            backtrack(current, open_count + 1, close_count)
            current.pop()
        if close_count < open_count:
            current.append(")")
            backtrack(current, open_count, close_count + 1)
            current.pop()

    backtrack([], 0, 0)
    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/generate-parentheses/
