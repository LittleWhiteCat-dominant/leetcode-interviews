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

1. Identify the core pattern for this category: **3. Linked List**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
