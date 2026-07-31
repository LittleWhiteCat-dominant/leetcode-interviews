# 225. Implement Stack using Queues

**Difficulty:** Easy
**Topics:** Stack, Design, Queue
**Common companies:** Amazon, Apple
**Category (README):** 5. Queue / Monotonic Queue

## Problem Description

Implement a last-in-first-out (LIFO) stack using only two queues. The implemented stack should support all the functions of a normal stack (`push`, `top`, `pop`, and `empty`).

Implement the `MyStack` class:

	
- `void push(int x)` Pushes element x to the top of the stack.

	
- `int pop()` Removes the element on the top of the stack and returns it.

	
- `int top()` Returns the element on the top of the stack.

	
- `boolean empty()` Returns `true` if the stack is empty, `false` otherwise.

**Notes:**

	
- You must use **only** standard operations of a queue, which means that only `push to back`, `peek/pop from front`, `size` and `is empty` operations are valid.

	
- Depending on your language, the queue may not be supported natively. You may simulate a queue using a list or deque (double-ended queue) as long as you use only a queue's standard operations.

 

**Example 1:**

```

**Input**
["MyStack", "push", "push", "top", "pop", "empty"]
[[], [1], [2], [], [], []]
**Output**
[null, null, null, 2, 2, false]

**Explanation**
MyStack myStack = new MyStack();
myStack.push(1);
myStack.push(2);
myStack.top(); // return 2
myStack.pop(); // return 2
myStack.empty(); // return False

```

 

**Constraints:**

	
- `1 <= x <= 9`

	
- At most `100` calls will be made to `push`, `pop`, `top`, and `empty`.

	
- All the calls to `pop` and `top` are valid.

 

**Follow-up:** Can you implement the stack using only one queue?

## Key Idea

Simulate one structure with the other

## Approach

This is solved with **a single queue, rotated after every push so the newest element sits at the front**:

1. Keep all elements in one `deque` used strictly as a queue.
2. On `push(x)`, append `x` to the back, then rotate the queue by popping from the front and re-appending, repeated `len(queue) - 1` times, moving `x` all the way to the front.
3. This makes the front of the queue always hold the most recently pushed element, mimicking a stack's top.
4. `pop()` and `top()` then simply operate on the front of the queue, and `empty()` checks if the queue is empty.

**Time Complexity:** O(n) for `push` (rotating the queue so the new element is at the front), O(1) for `pop`, `top`, and `empty`.
**Space Complexity:** O(n) — a single queue holds all currently pushed elements.

## Reference Solution (Python)

```python
from collections import deque


class MyStack:
    def __init__(self):
        self.queue: deque[int] = deque()

    def push(self, x: int) -> None:
        self.queue.append(x)
        for _ in range(len(self.queue) - 1):
            self.queue.append(self.queue.popleft())

    def pop(self) -> int:
        return self.queue.popleft()

    def top(self) -> int:
        return self.queue[0]

    def empty(self) -> bool:
        return not self.queue
```

## Reference

- LeetCode: https://leetcode.com/problems/implement-stack-using-queues/
