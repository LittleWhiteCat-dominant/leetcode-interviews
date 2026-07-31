# 92. Reverse Linked List II

**Difficulty:** Medium
**Topics:** Linked List
**Common companies:** Meta, Google
**Category (README):** 3. Linked List

## Problem Description

Given the `head` of a singly linked list and two integers `left` and `right` where `left <= right`, reverse the nodes of the list from position `left` to position `right`, and return *the reversed list*.

 

**Example 1:**

```

**Input:** head = [1,2,3,4,5], left = 2, right = 4
**Output:** [1,4,3,2,5]

```

**Example 2:**

```

**Input:** head = [5], left = 1, right = 1
**Output:** [5]

```

 

**Constraints:**

	
- The number of nodes in the list is `n`.

	
- `1 <= n <= 500`

	
- `-500 <= Node.val <= 500`

	
- `1 <= left <= right <= n`

 

**Follow up:** Could you do it in one pass?

## Key Idea

Locate the sub-range head/tail, then reverse locally

## Approach

This is solved with **a dummy head plus repeated head-insertion reversal on the sub-range**:

1. Add a dummy node before `head` so that reversing starting at position 1 doesn't require special-casing the list head.
2. Advance a `prev` pointer `left - 1` steps so it sits just before the sub-range to reverse.
3. Let `curr` be `prev.next` (the first node of the sub-range); it will end up as the tail of the reversed portion.
4. Repeat `right - left` times: detach the node right after `curr`, and re-insert it immediately after `prev`, effectively pushing each subsequent node to the front of the sub-range.
5. Return `dummy.next` as the new head of the list.

**Time Complexity:** O(n) — a single pass over the list.
**Space Complexity:** O(1) — in-place pointer manipulation with a dummy head.

## Reference Solution (Python)

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

def reverseBetween(head: ListNode, left: int, right: int) -> ListNode:
    dummy = ListNode(0, head)
    prev = dummy
    for _ in range(left - 1):
        prev = prev.next

    curr = prev.next
    for _ in range(right - left):
        nxt = curr.next
        curr.next = nxt.next
        nxt.next = prev.next
        prev.next = nxt

    return dummy.next
```

## Reference

- LeetCode: https://leetcode.com/problems/reverse-linked-list-ii/
