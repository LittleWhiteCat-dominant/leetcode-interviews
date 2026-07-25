# 25. Reverse Nodes in k-Group

**Difficulty:** Hard
**Topics:** Linked List, Recursion
**Reported at Asana:** Tracked in Asana's known coding question bank (InterviewSolver).

## Problem Description

Given the `head` of a linked list, reverse the nodes of the list `k` at a time, and return *the modified list*.

`k` is a positive integer and is less than or equal to the length of the linked list. If the number of nodes is not a multiple of `k` then left-out nodes, in the end, should remain as it is.

You may not alter the values in the list's nodes, only nodes themselves may be changed.

## Example 1

```
Input: head = [1,2,3,4,5], k = 2
Output: [2,1,4,3,5]
```

## Example 2

```
Input: head = [1,2,3,4,5], k = 3
Output: [3,2,1,4,5]
```

## Constraints

- The number of nodes in the list is `n`.
- `1 <= k <= n <= 5000`
- `0 <= Node.val <= 1000`

**Follow-up:** Can you solve the problem in `O(1)` extra memory space?

## Approach

1. **Check group length first**: before reversing a group, walk ahead `k` nodes to confirm there are at least `k` remaining nodes. If fewer than `k` nodes remain, leave that final partial group untouched.
2. **Reverse in place**: reverse the `k` nodes using the standard iterative three-pointer linked-list reversal technique (`prev`, `curr`, `next`).
3. **Reconnect**: after reversing a group, the group's original head becomes its tail (which must connect to the recursively/iteratively processed remainder of the list), and the group's original tail becomes its new head (which must connect to the previous group's tail).
4. This can be implemented either **recursively** (reverse a group, then recursively process the rest and attach it) or **iteratively** with a dummy head node and careful pointer bookkeeping (this achieves O(1) extra space, satisfying the follow-up).

**Time Complexity:** O(n) — every node is visited a constant number of times.
**Space Complexity:** O(1) for the iterative approach; O(n/k) recursion stack for the recursive approach.

## Reference Solution (Python, Iterative)

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def reverse_k_group(head: "ListNode | None", k: int) -> "ListNode | None":
    dummy = ListNode(0, head)
    group_prev = dummy

    while True:
        kth = group_prev
        for _ in range(k):
            kth = kth.next
            if not kth:
                return dummy.next

        group_next = kth.next
        prev, curr = group_next, group_prev.next

        while curr != group_next:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        new_group_head = kth
        old_group_head = group_prev.next
        group_prev.next = new_group_head
        group_prev = old_group_head
```

## Follow-up Questions Interviewers May Ask

- Can you implement this recursively? What's the trade-off compared to the iterative O(1)-space version?
- How would you reverse every **other** group of k nodes, leaving the rest untouched?
- How would you adapt this to a doubly linked list?
