# 155. Min Stack

**Difficulty:** Medium
**Topics:** Stack, Design
**Common companies:** Amazon, Apple
**Category (README):** 4.1 Basic Stack Applications

## Problem Description

Design a stack that supports push, pop, top, and retrieving the minimum element in constant time.

Implement the `MinStack` class:

	
- `MinStack()` initializes the stack object.

	
- `void push(int value)` pushes the element `value` onto the stack.

	
- `void pop()` removes the element on the top of the stack.

	
- `int top()` gets the top element of the stack.

	
- `int getMin()` retrieves the minimum element in the stack.

You must implement a solution with `O(1)` time complexity for each function.

 

**Example 1:**

```

**Input**
["MinStack","push","push","push","getMin","pop","top","getMin"]
[[],[-2],[0],[-3],[],[],[],[]]

**Output**
[null,null,null,null,-3,null,0,-2]

**Explanation**
MinStack minStack = new MinStack();
minStack.push(-2);
minStack.push(0);
minStack.push(-3);
minStack.getMin(); // return -3
minStack.pop();
minStack.top();    // return 0
minStack.getMin(); // return -2

```

 

**Constraints:**

	
- `-231 <= val <= 231 - 1`

	
- Methods `pop`, `top` and `getMin` operations will always be called on **non-empty** stacks.

	
- At most `3 * 104` calls will be made to `push`, `pop`, `top`, and `getMin`.

## Key Idea

An auxiliary stack tracking the running minimum

## Approach

This is solved with **a single stack of (value, running-minimum) pairs**:

1. Instead of a separate min-tracking stack, store each pushed value alongside the minimum seen so far, as a tuple.
2. On `push(val)`, compute the new running minimum as `min(val, current top's minimum)` (or just `val` if the stack is empty), and push `(val, running_min)`.
3. `pop()` simply removes the top tuple, automatically restoring the previous running minimum since it's baked into the tuple below.
4. `top()` and `getMin()` just read the value or minimum from the top tuple, both O(1).

**Time Complexity:** O(1) — every operation (`push`, `pop`, `top`, `getMin`) only touches the top of the stack.
**Space Complexity:** O(n) — each stack entry stores both the value and the running minimum.

## Reference Solution (Python)

```python
class MinStack:
    def __init__(self) -> None:
        self._stack: list[tuple[int, int]] = []

    def push(self, val: int) -> None:
        current_min = min(val, self._stack[-1][1]) if self._stack else val
        self._stack.append((val, current_min))

    def pop(self) -> None:
        self._stack.pop()

    def top(self) -> int:
        return self._stack[-1][0]

    def getMin(self) -> int:
        return self._stack[-1][1]
```

## Reference

- LeetCode: https://leetcode.com/problems/min-stack/
