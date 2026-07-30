# 2. Add Two Numbers

**Difficulty:** Medium
**Topics:** Linked List, Math, Recursion
**Common companies:** Meta, Amazon
**Category (README):** 3. Linked List

## Problem Description

You are given two **non-empty** linked lists representing two non-negative integers. The digits are stored in **reverse order**, and each of their nodes contains a single digit. Add the two numbers and return the sum as a linked list.

You may assume the two numbers do not contain any leading zero, except the number 0 itself.

 

**Example 1:**

```

**Input:** l1 = [2,4,3], l2 = [5,6,4]
**Output:** [7,0,8]
**Explanation:** 342 + 465 = 807.

```

**Example 2:**

```

**Input:** l1 = [0], l2 = [0]
**Output:** [0]

```

**Example 3:**

```

**Input:** l1 = [9,9,9,9,9,9,9], l2 = [9,9,9,9]
**Output:** [8,9,9,9,0,0,0,1]

```

 

**Constraints:**

	
- The number of nodes in each linked list is in the range `[1, 100]`.

	
- `0 <= Node.val <= 9`

	
- It is guaranteed that the list represents a number that does not have leading zeros.

## Key Idea

Simulate addition with carry, dummy head node

## Approach

1. Identify the core pattern for this category: **3. Linked List**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(max(m, n)) — one pass through the longer of the two lists, where m and n are their lengths.
**Space Complexity:** O(max(m, n)) — for the newly created result list (excluding the inputs).

## Reference Solution (Python)

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def addTwoNumbers(l1: ListNode, l2: ListNode) -> ListNode:
    dummy = ListNode()
    current = dummy
    carry = 0

    while l1 or l2 or carry:
        val1 = l1.val if l1 else 0
        val2 = l2.val if l2 else 0
        total = val1 + val2 + carry
        carry, digit = divmod(total, 10)
        current.next = ListNode(digit)
        current = current.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None

    return dummy.next
```

## Reference

- LeetCode: https://leetcode.com/problems/add-two-numbers/
