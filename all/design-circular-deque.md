# 641. Design Circular Deque

**Difficulty:** Medium
**Topics:** Array, Linked List, Design, Queue
**Common companies:** Amazon
**Category (README):** 5. Queue / Monotonic Queue

## Problem Description

Design your implementation of the circular double-ended queue (deque).

Implement the `MyCircularDeque` class:

	
- `MyCircularDeque(int k)` Initializes the deque with a maximum size of `k`.

	
- `boolean insertFront()` Adds an item at the front of Deque. Returns `true` if the operation is successful, or `false` otherwise.

	
- `boolean insertLast()` Adds an item at the rear of Deque. Returns `true` if the operation is successful, or `false` otherwise.

	
- `boolean deleteFront()` Deletes an item from the front of Deque. Returns `true` if the operation is successful, or `false` otherwise.

	
- `boolean deleteLast()` Deletes an item from the rear of Deque. Returns `true` if the operation is successful, or `false` otherwise.

	
- `int getFront()` Returns the front item from the Deque. Returns `-1` if the deque is empty.

	
- `int getRear()` Returns the last item from Deque. Returns `-1` if the deque is empty.

	
- `boolean isEmpty()` Returns `true` if the deque is empty, or `false` otherwise.

	
- `boolean isFull()` Returns `true` if the deque is full, or `false` otherwise.

 

**Example 1:**

```

**Input**
["MyCircularDeque", "insertLast", "insertLast", "insertFront", "insertFront", "getRear", "isFull", "deleteLast", "insertFront", "getFront"]
[[3], [1], [2], [3], [4], [], [], [], [4], []]
**Output**
[null, true, true, true, false, 2, true, true, true, 4]

**Explanation**
MyCircularDeque myCircularDeque = new MyCircularDeque(3);
myCircularDeque.insertLast(1);  // return True
myCircularDeque.insertLast(2);  // return True
myCircularDeque.insertFront(3); // return True
myCircularDeque.insertFront(4); // return False, the queue is full.
myCircularDeque.getRear();      // return 2
myCircularDeque.isFull();       // return True
myCircularDeque.deleteLast();   // return True
myCircularDeque.insertFront(4); // return True
myCircularDeque.getFront();     // return 4

```

 

**Constraints:**

	
- `1 <= k <= 1000`

	
- `0 <= value <= 1000`

	
- At most `2000` calls will be made to `insertFront`, `insertLast`, `deleteFront`, `deleteLast`, `getFront`, `getRear`, `isEmpty`, `isFull`.

## Key Idea

Array simulating a circular queue

## Approach

1. Identify the core pattern for this category: **5. Queue / Monotonic Queue**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(1) per operation — index arithmetic only, no shifting of elements.
**Space Complexity:** O(k) — the fixed-size backing array.

## Reference Solution (Python)

```python
class MyCircularDeque:
    def __init__(self, k: int):
        self.capacity = k
        self.data = [0] * k
        self.front = 0
        self.size = 0

    def insertFront(self, value: int) -> bool:
        if self.isFull():
            return False
        self.front = (self.front - 1 + self.capacity) % self.capacity
        self.data[self.front] = value
        self.size += 1
        return True

    def insertLast(self, value: int) -> bool:
        if self.isFull():
            return False
        rear = (self.front + self.size) % self.capacity
        self.data[rear] = value
        self.size += 1
        return True

    def deleteFront(self) -> bool:
        if self.isEmpty():
            return False
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return True

    def deleteLast(self) -> bool:
        if self.isEmpty():
            return False
        self.size -= 1
        return True

    def getFront(self) -> int:
        if self.isEmpty():
            return -1
        return self.data[self.front]

    def getRear(self) -> int:
        if self.isEmpty():
            return -1
        rear = (self.front + self.size - 1) % self.capacity
        return self.data[rear]

    def isEmpty(self) -> bool:
        return self.size == 0

    def isFull(self) -> bool:
        return self.size == self.capacity
```

## Reference

- LeetCode: https://leetcode.com/problems/design-circular-deque/
