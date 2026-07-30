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

1. Identify the core pattern for this category: **4.1 Basic Stack Applications**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
