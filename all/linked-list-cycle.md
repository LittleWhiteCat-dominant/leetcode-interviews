# 141. Linked List Cycle

**Difficulty:** Easy
**Topics:** Hash Table, Linked List, Two Pointers
**Common companies:** All big tech
**Category (README):** 3. Linked List

## Problem Description

Given `head`, the head of a linked list, determine if the linked list has a cycle in it.

There is a cycle in a linked list if there is some node in the list that can be reached again by continuously following the `next` pointer. Internally, `pos` is used to denote the index of the node that tail's `next` pointer is connected to. **Note that `pos` is not passed as a parameter**.

Return `true`* if there is a cycle in the linked list*. Otherwise, return `false`.

 

**Example 1:**

```

**Input:** head = [3,2,0,-4], pos = 1
**Output:** true
**Explanation:** There is a cycle in the linked list, where the tail connects to the 1st node (0-indexed).

```

**Example 2:**

```

**Input:** head = [1,2], pos = 0
**Output:** true
**Explanation:** There is a cycle in the linked list, where the tail connects to the 0th node.

```

**Example 3:**

```

**Input:** head = [1], pos = -1
**Output:** false
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

1. Identify the core pattern for this category: **3. Linked List**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — the fast pointer visits at most 2n nodes before either reaching the end or meeting the slow pointer.
**Space Complexity:** O(1) — only two pointers are used regardless of list size.

## Reference Solution (Python)

```python
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def hasCycle(head: ListNode) -> bool:
    slow = fast = head

    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True

    return False
```

## Reference

- LeetCode: https://leetcode.com/problems/linked-list-cycle/
