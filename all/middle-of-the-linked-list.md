# 876. Middle of the Linked List

**Difficulty:** Easy
**Topics:** Linked List, Two Pointers
**Common companies:** All big tech
**Category (README):** 3. Linked List

## Problem Description

Given the `head` of a singly linked list, return *the middle node of the linked list*.

If there are two middle nodes, return **the second middle** node.

 

**Example 1:**

```

**Input:** head = [1,2,3,4,5]
**Output:** [3,4,5]
**Explanation:** The middle node of the list is node 3.

```

**Example 2:**

```

**Input:** head = [1,2,3,4,5,6]
**Output:** [4,5,6]
**Explanation:** Since the list has two middle nodes with values 3 and 4, we return the second one.

```

 

**Constraints:**

	
- The number of nodes in the list is in the range `[1, 100]`.

	
- `1 <= Node.val <= 100`

## Key Idea

Fast/slow pointers, fast pointer moves at 2x speed

## Approach

This is solved with **the fast/slow pointer (tortoise and hare) technique**:

1. Start both `slow` and `fast` pointers at `head`.
2. On each step, advance `slow` by one node and `fast` by two nodes.
3. When `fast` reaches the end of the list (or `fast.next` is `None`), `slow` is exactly at the middle, since it has covered half the distance `fast` has.
4. Return `slow`; this naturally lands on the second middle node when the list has even length, since `fast` runs out one step sooner.

**Time Complexity:** O(n) — the fast pointer traverses the list once.
**Space Complexity:** O(1) — only two pointers are used.

## Reference Solution (Python)

```python
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def middleNode(head: ListNode | None) -> ListNode | None:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

## Reference

- LeetCode: https://leetcode.com/problems/middle-of-the-linked-list/
