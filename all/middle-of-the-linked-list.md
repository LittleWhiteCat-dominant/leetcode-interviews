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

1. Identify the core pattern for this category: **3. Linked List**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
