# 21. Merge Two Sorted Lists

**Difficulty:** Easy
**Topics:** Linked List, Recursion
**Common companies:** All big tech
**Category (README):** 3. Linked List

## Problem Description

You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists into one **sorted** list. The list should be made by splicing together the nodes of the first two lists.

Return *the head of the merged linked list*.

 

**Example 1:**

```

**Input:** list1 = [1,2,4], list2 = [1,3,4]
**Output:** [1,1,2,3,4,4]

```

**Example 2:**

```

**Input:** list1 = [], list2 = []
**Output:** []

```

**Example 3:**

```

**Input:** list1 = [], list2 = [0]
**Output:** [0]

```

 

**Constraints:**

	
- The number of nodes in both lists is in the range `[0, 50]`.

	
- `-100 <= Node.val <= 100`

	
- Both `list1` and `list2` are sorted in **non-decreasing** order.

## Key Idea

Two pointers + dummy head node

## Approach

This is solved with **a dummy-head merge using two pointers**:

1. Create a dummy node to serve as an anchor before the merged list, and a `tail` pointer starting at the dummy.
2. While both `list1` and `list2` still have nodes, compare their current values and splice the smaller node onto `tail.next`, then advance that list's pointer and `tail`.
3. Once one list is exhausted, attach the remainder of the other list directly to `tail.next`, since it is already sorted.
4. Return `dummy.next` as the head of the merged list.

**Time Complexity:** O(m + n) — each node from both lists is visited exactly once.
**Space Complexity:** O(1) extra — nodes are relinked in place; only a dummy head and pointers are allocated.

## Reference Solution (Python)

```python
class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def mergeTwoLists(list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
    dummy = ListNode()
    tail = dummy

    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next

    tail.next = list1 if list1 else list2
    return dummy.next
```

## Reference

- LeetCode: https://leetcode.com/problems/merge-two-sorted-lists/
