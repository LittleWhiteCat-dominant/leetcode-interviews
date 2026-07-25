# 206. Reverse Linked List

**Difficulty:** Easy
**Topics:** Linked List, Recursion
**Category warm-up for:** Linked List

## Problem Description

Given the `head` of a singly linked list, reverse the list, and return *the reversed list*.

## Example 1

```
Input: head = [1,2,3,4,5]
Output: [5,4,3,2,1]
```

## Example 2

```
Input: head = [1,2]
Output: [2,1]
```

## Example 3

```
Input: head = []
Output: []
```

## Constraints

- The number of nodes in the list is the range `[0, 5000]`.
- `-5000 <= Node.val <= 5000`

**Follow-up:** A linked list can be reversed either iteratively or recursively. Could you implement both?

## Approach

**Iterative (three-pointer) — the standard, O(1)-space approach:**
1. Maintain `prev` (initially `None`) and `curr` (initially `head`).
2. At each step, save `curr.next` in a temporary variable, then point `curr.next` back to `prev`.
3. Advance `prev` to `curr`, and `curr` to the saved next node.
4. Repeat until `curr` is `None`; `prev` is now the new head of the reversed list.

**Recursive approach:**
1. Base case: if `head` is `None` or `head.next` is `None`, return `head` (it's already "reversed" on its own).
2. Recursively reverse the rest of the list starting at `head.next`, obtaining `new_head`.
3. Set `head.next.next = head` (point the next node back at the current node) and `head.next = None`.
4. Return `new_head`.

**Time Complexity:** O(n) for both approaches — every node is visited once.
**Space Complexity:** O(1) for the iterative approach; O(n) recursion stack for the recursive approach.

## Reference Solution (Python, Iterative)

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_list(head: "ListNode | None") -> "ListNode | None":
    prev = None
    curr = head

    while curr:
        next_node = curr.next
        curr.next = prev
        prev = curr
        curr = next_node

    return prev
```

## Reference Solution (Python, Recursive)

```python
def reverse_list_recursive(head: "ListNode | None") -> "ListNode | None":
    if head is None or head.next is None:
        return head

    new_head = reverse_list_recursive(head.next)
    head.next.next = head
    head.next = None
    return new_head
```

## Follow-up Questions Interviewers May Ask

- Can you reverse only a sub-range of the list, from position `left` to `right` (see LC 92, Reverse Linked List II)?
- Can you reverse the list in groups of `k` nodes at a time (see LC 25, Reverse Nodes in k-Group)?
- How would you reverse a doubly linked list instead?
