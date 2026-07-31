# 19. Remove Nth Node From End of List

**Difficulty:** Medium
**Topics:** Linked List, Two Pointers
**Common companies:** Amazon, Google
**Category (README):** 3. Linked List

## Problem Description

Given the `head` of a linked list, remove the `nth` node from the end of the list and return its head.

 

**Example 1:**

```

**Input:** head = [1,2,3,4,5], n = 2
**Output:** [1,2,3,5]

```

**Example 2:**

```

**Input:** head = [1], n = 1
**Output:** []

```

**Example 3:**

```

**Input:** head = [1,2], n = 1
**Output:** [1]

```

 

**Constraints:**

	
- The number of nodes in the list is `sz`.

	
- `1 <= sz <= 30`

	
- `0 <= Node.val <= 100`

	
- `1 <= n <= sz`

 

**Follow up:** Could you do this in one pass?

## Key Idea

Fast pointer advances N steps first, then move both in sync

## Approach

This is solved with a **two-pointer gap technique in a single pass**:

1. Add a `dummy` node pointing to `head` so that removing the actual head node (when `n` equals the list length) doesn't need special-casing.
2. Start both `fast` and `slow` at `dummy`, and advance `fast` alone by `n` steps first, creating a fixed gap of `n` nodes between `fast` and `slow`.
3. Then advance `fast` and `slow` together, one step at a time, until `fast` reaches the last node (`fast.next is None`).
4. At that point, because of the `n`-node gap, `slow` is sitting exactly one node before the node that needs removal.
5. Unlink the target node with `slow.next = slow.next.next`, and return `dummy.next` as the new head.

**Time Complexity:** O(n) — a single pass with the two-pointer technique.
**Space Complexity:** O(1) — only a dummy node and two pointers are used.

## Reference Solution (Python)

```python
from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def removeNthFromEnd(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    dummy = ListNode(0, head)
    fast = slow = dummy

    for _ in range(n):
        fast = fast.next

    while fast.next:
        fast = fast.next
        slow = slow.next

    slow.next = slow.next.next
    return dummy.next
```

## Reference

- LeetCode: https://leetcode.com/problems/remove-nth-node-from-end-of-list/
