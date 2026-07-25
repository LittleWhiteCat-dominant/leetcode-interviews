# 20. Valid Parentheses

**Difficulty:** Easy
**Topics:** String, Stack
**Category warm-up for:** Stack

## Problem Description

Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is **valid**.

An input string is valid if:

1. Open brackets must be closed by the same type of brackets.
2. Open brackets must be closed in the correct order.
3. Every close bracket has a corresponding open bracket of the same type.

## Example 1

```
Input: s = "()"
Output: true
```

## Example 2

```
Input: s = "()[]{}"
Output: true
```

## Example 3

```
Input: s = "(]"
Output: false
```

## Example 4

```
Input: s = "([])"
Output: true
```

## Constraints

- `1 <= s.length <= 10^4`
- `s` consists of parentheses only `'()[]{}'`.

## Approach

1. Use a **stack** to track open brackets that haven't been closed yet.
2. Iterate through the string character by character:
   - If the character is an **opening** bracket, push it onto the stack.
   - If the character is a **closing** bracket, check whether the stack is non-empty and its top element is the matching opening bracket. If so, pop it; if not (empty stack, or mismatched type), the string is invalid.
3. At the end, the string is valid if and only if the stack is completely empty (every opening bracket found its match).

This works because a stack naturally enforces "closed in the correct order" — the most recently opened bracket must be the next one closed (LIFO).

**Time Complexity:** O(n) — a single pass through the string.
**Space Complexity:** O(n) for the stack in the worst case (e.g., a string of all opening brackets).

## Reference Solution (Python)

```python
def is_valid(s: str) -> bool:
    stack: list[str] = []
    pairs = {")": "(", "]": "[", "}": "{"}

    for char in s:
        if char in "([{":
            stack.append(char)
        else:
            if not stack or stack.pop() != pairs[char]:
                return False

    return not stack
```

## Follow-up Questions Interviewers May Ask

- How would you find the **minimum number of insertions** needed to make an invalid string valid?
- How would you generate all valid combinations of `n` pairs of parentheses instead of just validating one (see LC 22, Generate Parentheses)?
- How would you handle a string that also contains other characters mixed in with the brackets, which should be ignored?
