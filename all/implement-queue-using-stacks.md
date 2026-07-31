# 232. Implement Queue using Stacks

**Difficulty:** Easy
**Topics:** Stack, Design, Queue
**Common companies:** Amazon, Apple
**Category (README):** 5. Queue / Monotonic Queue

## Problem Description

Implement a first in first out (FIFO) queue using only two stacks. The implemented queue should support all the functions of a normal queue (`push`, `peek`, `pop`, and `empty`).

Implement the `MyQueue` class:

	
- `void push(int x)` Pushes element x to the back of the queue.

	
- `int pop()` Removes the element from the front of the queue and returns it.

	
- `int peek()` Returns the element at the front of the queue.

	
- `boolean empty()` Returns `true` if the queue is empty, `false` otherwise.

**Notes:**

	
- You must use **only** standard operations of a stack, which means only `push to top`, `peek/pop from top`, `size`, and `is empty` operations are valid.

	
- Depending on your language, the stack may not be supported natively. You may simulate a stack using a list or deque (double-ended queue) as long as you use only a stack's standard operations.

 

**Example 1:**

```

**Input**
["MyQueue", "push", "push", "peek", "pop", "empty"]
[[], [1], [2], [], [], []]
**Output**
[null, null, null, 1, 1, false]

**Explanation**
MyQueue myQueue = new MyQueue();
myQueue.push(1); // queue is: [1]
myQueue.push(2); // queue is: [1, 2] (leftmost is front of the queue)
myQueue.peek(); // return 1
myQueue.pop(); // return 1, queue is [2]
myQueue.empty(); // return false

```

 

**Constraints:**

	
- `1 <= x <= 9`

	
- At most `100` calls will be made to `push`, `pop`, `peek`, and `empty`.

	
- All the calls to `pop` and `peek` are valid.

 

**Follow-up:** Can you implement the queue such that each operation is **amortized** `O(1)` time complexity? In other words, performing `n` operations will take overall `O(n)` time even if one of those operations may take longer.

## Key Idea

Simulate one structure with the other

## Approach

This is solved with **two stacks: one for incoming pushes, one for outgoing pops, reversing order on transfer**:

1. Maintain an `in_stack` that simply receives every `push(x)` in arrival order.
2. Maintain an `out_stack` that serves `pop()`/`peek()`; when it's empty, pop everything from `in_stack` and push it onto `out_stack`, which reverses the order so the oldest pushed element ends up on top.
3. `pop()` and `peek()` first ensure `out_stack` is refilled (if empty), then operate on its top.
4. `empty()` returns true only when both stacks are empty. Each element is moved from `in_stack` to `out_stack` at most once, giving amortized O(1) operations.

**Time Complexity:** O(1) amortized for `push`, `pop`, `peek`, and `empty` — each element is moved between the two stacks at most once.
**Space Complexity:** O(n) — both stacks together hold all currently enqueued elements.

## Reference Solution (Python)

```python
class MyQueue:
    def __init__(self):
        self.in_stack: list[int] = []
        self.out_stack: list[int] = []

    def push(self, x: int) -> None:
        self.in_stack.append(x)

    def _transfer_if_needed(self) -> None:
        if not self.out_stack:
            while self.in_stack:
                self.out_stack.append(self.in_stack.pop())

    def pop(self) -> int:
        self._transfer_if_needed()
        return self.out_stack.pop()

    def peek(self) -> int:
        self._transfer_if_needed()
        return self.out_stack[-1]

    def empty(self) -> bool:
        return not self.in_stack and not self.out_stack
```

## Reference

- LeetCode: https://leetcode.com/problems/implement-queue-using-stacks/
