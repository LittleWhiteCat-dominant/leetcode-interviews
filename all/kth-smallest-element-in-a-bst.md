# 230. Kth Smallest Element in a BST

**Difficulty:** Medium
**Topics:** Tree, Depth-First Search, Binary Search Tree, Binary Tree
**Common companies:** All big tech
**Category (README):** 7.2 Binary Search Tree (BST)

## Problem Description

Given the `root` of a binary search tree, and an integer `k`, return *the* `kth` *smallest value (**1-indexed**) of all the values of the nodes in the tree*.

 

**Example 1:**

```

**Input:** root = [3,1,4,null,2], k = 1
**Output:** 1

```

**Example 2:**

```

**Input:** root = [5,3,6,2,4,null,null,1], k = 3
**Output:** 3

```

 

**Constraints:**

	
- The number of nodes in the tree is `n`.

	
- `1 <= k <= n <= 104`

	
- `0 <= Node.val <= 104`

 

**Follow up:** If the BST is modified often (i.e., we can do insert and delete operations) and you need to find the kth smallest frequently, how would you optimize?

## Key Idea

The k-th element of an in-order traversal is the answer

## Approach

This is solved with **an iterative in-order traversal using an explicit stack**:

1. Maintain a stack and a `node` pointer starting at the root.
2. Push all left children onto the stack until `node` becomes `None`, reaching the smallest unvisited value.
3. Pop the stack (this yields values in ascending order) and decrement `k`.
4. If `k` reaches `0`, the popped node's value is the answer.
5. Otherwise, move to the popped node's right child and repeat the left-spine push until the stack empties or `k` hits `0`.

**Time Complexity:** O(H + k) — where H is the tree height; we push at most H nodes at a time and pop k nodes before stopping.
**Space Complexity:** O(H) — the explicit stack holds at most one root-to-leaf path.

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def kthSmallest(root: TreeNode, k: int) -> int:
    stack = []
    node = root

    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right

    return -1
```

## Reference

- LeetCode: https://leetcode.com/problems/kth-smallest-element-in-a-bst/
