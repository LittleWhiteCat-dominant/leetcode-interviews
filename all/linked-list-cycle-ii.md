# 142. Linked List Cycle II

**Difficulty:** Medium
**Topics:** Hash Table, Linked List, Two Pointers
**Common companies:** All big tech
**Category (README):** 3. Linked List

## Problem Description

Given the `head` of a linked list, return *the node where the cycle begins. If there is no cycle, return *`null`.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointer. Internally, `pos` is used to denote the index of the node that tail's `next` pointer is connected to (**0-indexed**). It is `-1` if there is no cycle. **Note that** `pos` **is not passed as a parameter**.

**Do not modify** the linked list.

 

**Example 1:**

```

**Input:** head = [3,2,0,-4], pos = 1
**Output:** tail connects to node index 1
**Explanation:** There is a cycle in the linked list, where tail connects to the second node.

```

**Example 2:**

```

**Input:** head = [1,2], pos = 0
**Output:** tail connects to node index 0
**Explanation:** There is a cycle in the linked list, where tail connects to the first node.

```

**Example 3:**

```

**Input:** head = [1], pos = -1
**Output:** no cycle
**Explanation:** There is no cycle in the linked list.

```

 

**Constraints:**

	
- The number of the nodes in the list is in the range `[0, 104]`.

	
- `-105 <= Node.val <= 105`

	
- `pos` is `-1` or a **valid index** in the linked-list.

 

**Follow up:** Can you solve it using `O(1)` (i.e. constant) memory?

## Key Idea

Floyd's fast/slow pointer cycle detection

## Approach

This is solved with **Floyd's cycle detection followed by a second pointer phase to locate the cycle entrance**:

1. Move `slow` one step and `fast` two steps at a time until they meet inside a cycle (or `fast` hits the end, meaning no cycle).
2. Once `slow` and `fast` meet, reset a new pointer to `head` while leaving `slow` at the meeting point.
3. Advance both the new pointer and `slow` one step at a time; by the mathematical property of Floyd's algorithm, they meet exactly at the cycle's starting node.
4. Return that meeting node as the cycle start, or `None` if no cycle was ever detected.

**Time Complexity:** O(n) — the fast/slow pointers each traverse a bounded number of nodes proportional to the list length.
**Space Complexity:** O(1) — only a constant number of pointers are used.

## Reference Solution (Python)

```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def detectCycle(head: ListNode) -> ListNode:
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            pointer = head
            while pointer is not slow:
                pointer = pointer.next
                slow = slow.next
            return pointer

    return None
```

## Reference

- LeetCode: https://leetcode.com/problems/linked-list-cycle-ii/
