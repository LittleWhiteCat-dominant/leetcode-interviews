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

This is solved with **slow/fast pointer split + in-place reversal + interleave merge**:

1. Use slow/fast pointers to find the middle of the list, so it can be split into a first half and a second half.
2. Reverse the second half in place using the standard iterative pointer-reversal pattern.
3. Merge the two halves by alternating nodes: take one node from the first half, then one from the reversed second half, repeating until the second half is exhausted.
4. Since the second half is never longer than the first, the loop is driven by the second half's remaining nodes, naturally leaving the interleave correctly terminated.

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
