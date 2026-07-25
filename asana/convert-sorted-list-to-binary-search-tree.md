# 109. Convert Sorted List to Binary Search Tree

**Difficulty:** Medium
**Topics:** Linked List, Tree, Binary Search Tree, Depth-First Search, Binary Tree, Divide and Conquer
**Reported at Asana:** Tracked in Asana's known coding question bank (InterviewSolver).

## Problem Description

Given the `head` of a singly linked list where elements are **sorted in ascending order**, convert *it to a **height-balanced** binary search tree*.

## Example 1

```
Input: head = [-10,-3,0,5,9]
Output: [0,-3,9,-10,null,5]
Explanation: One possible answer is [0,-3,9,-10,null,5], which represents the shown height balanced BST.
```

## Example 2

```
Input: head = []
Output: []
```

## Constraints

- The number of nodes in `head` is in the range `[0, 2 * 10^4]`.
- `-10^5 <= Node.val <= 10^5`

## Approach

**Approach A — Convert to array first (simplest)**
1. Traverse the linked list once, copying values into an array.
2. Recursively build a balanced BST from the sorted array by always choosing the middle element as the root (same technique as LC 108, Convert Sorted Array to BST).

**Approach B — Fast/slow pointer (O(1) extra space beyond recursion, avoids the array copy)**
1. Use the classic fast/slow pointer technique to find the middle node of the current sublist in O(n) time — this becomes the root of the (sub)tree.
2. Split the list at the middle node, recursively build the left subtree from the left half and the right subtree from the right half.
3. This avoids the O(n) auxiliary array, though it does re-scan sublists in each recursive call, leading to O(n log n) total time rather than O(n).

**Time Complexity:** O(n) with the array-conversion approach; O(n log n) with the pure linked-list fast/slow pointer approach (due to repeated list traversals).
**Space Complexity:** O(n) for the array approach (plus O(log n) recursion), O(log n) recursion stack for the pure linked-list approach.

## Reference Solution (Python, Array Conversion)

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def sorted_list_to_bst(head: "ListNode | None") -> "TreeNode | None":
    values: list[int] = []
    node = head
    while node:
        values.append(node.val)
        node = node.next

    def build(left: int, right: int) -> "TreeNode | None":
        if left > right:
            return None
        mid = (left + right) // 2
        root = TreeNode(values[mid])
        root.left = build(left, mid - 1)
        root.right = build(mid + 1, right)
        return root

    return build(0, len(values) - 1)
```

## Follow-up Questions Interviewers May Ask

- Can you solve this with O(1) extra space beyond the recursion stack (no array copy)?
- How would you verify that the resulting tree is height-balanced?
- How would this change if the input were a doubly linked list instead of singly linked?
