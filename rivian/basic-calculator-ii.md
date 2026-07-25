# 227. Basic Calculator II

**Difficulty:** Medium
**Topics:** Stack, String, Math
**Reported at Rivian:** Confirmed — reported as the actual coding problem in a Rivian onsite round.

## Problem Description

Given a string `s` which represents an expression, evaluate this expression and return its value.

The integer division should truncate toward zero.

You may assume that the given expression is always valid. All intermediate results will be in the range of `[-2^31, 2^31 - 1]`.

**Note:** You are not supposed to use any built-in function which evaluates strings as mathematical expressions, such as `eval()`.

## Example 1

```
Input: s = "3+2*2"
Output: 7
```

## Example 2

```
Input: s = " 3/2 "
Output: 1
```

## Example 3

```
Input: s = " 3+5 / 2 "
Output: 5
```

## Constraints

- `1 <= s.length <= 3 * 10^5`
- `s` consists of integers and operators `('+', '-', '*', '/')` separated by some number of spaces.
- `s` represents a **valid** expression.
- All the integers in the expression are non-negative integers in the range `[0, 2^31 - 1]`.
- The answer is guaranteed to fit in a **32-bit integer**.

## Approach

1. Parse the string left to right, extracting one number and one operator at a time (skipping spaces).
2. Use a stack to handle operator precedence: `*` and `/` bind tighter than `+` and `-`.
   - When you see a `+`, push the current number onto the stack.
   - When you see a `-`, push the negation of the current number onto the stack.
   - When you see a `*` or `/`, pop the last value from the stack, apply the operator with the current number, and push the result back.
3. At the end, the answer is the sum of everything on the stack.
4. Track the "previous operator" as you scan so you know how to combine the just-parsed number with what's already on the stack.

**Time Complexity:** O(n), single pass over the string.
**Space Complexity:** O(n) for the stack in the worst case (e.g., an expression that is all additions/subtractions).

## Reference Solution (Python)

```python
def calculate(s: str) -> int:
    stack: list[int] = []
    current_number = 0
    operator = "+"

    for i, char in enumerate(s):
        if char.isdigit():
            current_number = current_number * 10 + int(char)

        if char in "+-*/" or i == len(s) - 1:
            if operator == "+":
                stack.append(current_number)
            elif operator == "-":
                stack.append(-current_number)
            elif operator == "*":
                stack.append(stack.pop() * current_number)
            elif operator == "/":
                # Truncate toward zero, matching Python's int() behavior for
                # positive results and int(a / b) for negative results.
                prev = stack.pop()
                stack.append(int(prev / current_number))

            operator = char
            current_number = 0

    return sum(stack)
```

## Follow-up Questions Interviewers May Ask

- How would you extend this to support parentheses (see LC 224, Basic Calculator)?
- How would you support floating-point numbers?
- How would you validate that the input expression is well-formed instead of assuming it is valid?
