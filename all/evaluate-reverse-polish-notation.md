# 150. Evaluate Reverse Polish Notation

**Difficulty:** Medium
**Topics:** Array, Math, Stack
**Common companies:** Amazon, Meta
**Category (README):** 4.1 Basic Stack Applications

## Problem Description

You are given an array of strings `tokens` that represents an arithmetic expression in a Reverse Polish Notation.

Evaluate the expression. Return *an integer that represents the value of the expression*.

**Note** that:

	
- The valid operators are `'+'`, `'-'`, `'*'`, and `'/'`.

	
- Each operand may be an integer or another expression.

	
- The division between two integers always **truncates toward zero**.

	
- There will not be any division by zero.

	
- The input represents a valid arithmetic expression in a reverse polish notation.

	
- The answer and all the intermediate calculations can be represented in a **32-bit** integer.

 

**Example 1:**

```

**Input:** tokens = ["2","1","+","3","*"]
**Output:** 9
**Explanation:** ((2 + 1) * 3) = 9

```

**Example 2:**

```

**Input:** tokens = ["4","13","5","/","+"]
**Output:** 6
**Explanation:** (4 + (13 / 5)) = 6

```

**Example 3:**

```

**Input:** tokens = ["10","6","9","3","+","-11","*","/","*","17","+","5","+"]
**Output:** 22
**Explanation:** ((10 * (6 / ((9 + 3) * -11))) + 17) + 5
= ((10 * (6 / (12 * -11))) + 17) + 5
= ((10 * (6 / -132)) + 17) + 5
= ((10 * 0) + 17) + 5
= (0 + 17) + 5
= 17 + 5
= 22

```

 

**Constraints:**

	
- `1 <= tokens.length <= 104`

	
- `tokens[i]` is either an operator: `"+"`, `"-"`, `"*"`, or `"/"`, or an integer in the range `[-200, 200]`.

## Key Idea

Stack holding operands

## Approach

1. Identify the core pattern for this category: **4.1 Basic Stack Applications**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — each token is processed once with O(1) stack operations.
**Space Complexity:** O(n) — the stack can hold up to n operands in the worst case.

## Reference Solution (Python)

```python
def evalRPN(tokens: list[str]) -> int:
    stack: list[int] = []
    operators = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: int(a / b),
    }

    for token in tokens:
        if token in operators:
            b = stack.pop()
            a = stack.pop()
            stack.append(operators[token](a, b))
        else:
            stack.append(int(token))

    return stack[0]
```

## Reference

- LeetCode: https://leetcode.com/problems/evaluate-reverse-polish-notation/
