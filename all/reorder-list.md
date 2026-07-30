# 143. Reorder List

**Difficulty:** Medium
**Topics:** Linked List, Two Pointers, Stack, Recursion
**Common companies:** **Meta favorite**
**Category (README):** 3. Linked List

## Problem Description

You are given the head of a singly linked-list. The list can be represented as:

```

L0 → L1 → … → Ln - 1 → Ln

```

*Reorder the list to be on the following form:*

```

L0 → Ln → L1 → Ln - 1 → L2 → Ln - 2 → …

```

You may not modify the values in the list's nodes. Only nodes themselves may be changed.

 

**Example 1:**

```

**Input:** head = [1,2,3,4]
**Output:** [1,4,2,3]

```

**Example 2:**

```

**Input:** head = [1,2,3,4,5]
**Output:** [1,5,2,4,3]

```

 

**Constraints:**

	
- The number of nodes in the list is in the range `[1, 5 * 104]`.

	
- `1 <= Node.val <= 1000`

## Key Idea

Find the midpoint + reverse the second half + interleave merge

## Approach

1. Identify the core pattern for this category: **3. Linked List**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — one pass to find the midpoint, one pass to reverse the second half, one pass to merge.
**Space Complexity:** O(1) — pointers only, no extra data structures.

## Reference Solution (Python)

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reorderList(head: ListNode) -> None:
    if not head or not head.next:
        return

    slow, fast = head, head
    while fast.next and fast.next.next:
        slow = slow.next
        fast = fast.next.next

    second = slow.next
    slow.next = None
    prev = None
    while second:
        second.next, prev, second = prev, second, second.next

    first, second = head, prev
    while second:
        first.next, first = second, first.next
        second.next, second = first, second.next
```

## Reference

- LeetCode: https://leetcode.com/problems/reorder-list/
