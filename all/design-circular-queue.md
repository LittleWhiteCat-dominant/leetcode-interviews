# 622. Design Circular Queue

**Difficulty:** Medium
**Topics:** Array, Linked List, Design, Queue
**Common companies:** Amazon
**Category (README):** 5. Queue / Monotonic Queue

## Problem Description

Design your implementation of the circular queue. The circular queue is a linear data structure in which the operations are performed based on FIFO (First In First Out) principle, and the last position is connected back to the first position to make a circle. It is also called "Ring Buffer".

One of the benefits of the circular queue is that we can make use of the spaces in front of the queue. In a normal queue, once the queue becomes full, we cannot insert the next element even if there is a space in front of the queue. But using the circular queue, we can use the space to store new values.

Implement the `MyCircularQueue` class:

	
- `MyCircularQueue(k)` Initializes the object with the size of the queue to be `k`.

	
- `int Front()` Gets the front item from the queue. If the queue is empty, return `-1`.

	
- `int Rear()` Gets the last item from the queue. If the queue is empty, return `-1`.

	
- `boolean enQueue(int value)` Inserts an element into the circular queue. Return `true` if the operation is successful.

	
- `boolean deQueue()` Deletes an element from the circular queue. Return `true` if the operation is successful.

	
- `boolean isEmpty()` Checks whether the circular queue is empty or not.

	
- `boolean isFull()` Checks whether the circular queue is full or not.

You must solve the problem without using the built-in queue data structure in your programming language. 

 

**Example 1:**

```

**Input**
["MyCircularQueue", "enQueue", "enQueue", "enQueue", "enQueue", "Rear", "isFull", "deQueue", "enQueue", "Rear"]
[[3], [1], [2], [3], [4], [], [], [], [4], []]
**Output**
[null, true, true, true, false, 3, true, true, true, 4]

**Explanation**
MyCircularQueue myCircularQueue = new MyCircularQueue(3);
myCircularQueue.enQueue(1); // return True
myCircularQueue.enQueue(2); // return True
myCircularQueue.enQueue(3); // return True
myCircularQueue.enQueue(4); // return False
myCircularQueue.Rear();     // return 3
myCircularQueue.isFull();   // return True
myCircularQueue.deQueue();  // return True
myCircularQueue.enQueue(4); // return True
myCircularQueue.Rear();     // return 4

```

 

**Constraints:**

	
- `1 <= k <= 1000`

	
- `0 <= value <= 1000`

	
- At most `3000` calls will be made to `enQueue`, `deQueue`, `Front`, `Rear`, `isEmpty`, and `isFull`.

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
class MyCircularQueue:
    def __init__(self, k: int):
        self.capacity = k
        self.data = [0] * k
        self.front = 0
        self.size = 0

    def enQueue(self, value: int) -> bool:
        if self.isFull():
            return False
        rear = (self.front + self.size) % self.capacity
        self.data[rear] = value
        self.size += 1
        return True

    def deQueue(self) -> bool:
        if self.isEmpty():
            return False
        self.front = (self.front + 1) % self.capacity
        self.size -= 1
        return True

    def Front(self) -> int:
        if self.isEmpty():
            return -1
        return self.data[self.front]

    def Rear(self) -> int:
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

- LeetCode: https://leetcode.com/problems/design-circular-queue/
