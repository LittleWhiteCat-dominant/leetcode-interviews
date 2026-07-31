# 98. Validate Binary Search Tree

**Difficulty:** Medium
**Topics:** Tree, Depth-First Search, Binary Search Tree, Binary Tree
**Common companies:** All big tech
**Category (README):** 7.2 Binary Search Tree (BST)

## Problem Description

Given the `root` of a binary tree, *determine if it is a valid binary search tree (BST)*.

A **valid BST** is defined as follows:

	
- The left subtree of a node contains only nodes with keys **strictly less than** the node's key.

	
- The right subtree of a node contains only nodes with keys **strictly greater than** the node's key.

	
- Both the left and right subtrees must also be binary search trees.

 

**Example 1:**

```

**Input:** root = [2,1,3]
**Output:** true

```

**Example 2:**

```

**Input:** root = [5,1,4,null,null,3,6]
**Output:** false
**Explanation:** The root node's value is 5 but its right child's value is 4.

```

 

**Constraints:**

	
- The number of nodes in the tree is in the range `[1, 104]`.

	
- `-231 <= Node.val <= 231 - 1`

## Key Idea

Recursively pass down lower/upper bounds

## Approach

This is solved with **recursive validation using a shrinking valid-value range**:

1. Recurse with each node carrying a `(lower, upper)` bound that its value must strictly fall within, starting with `(-infinity, +infinity)` at the root.
2. A `None` node is trivially valid (base case) and returns `true`.
3. If the current node's value doesn't satisfy `lower < node.val < upper`, the BST property is violated, so return `false`.
4. Recurse into the left subtree with the same `lower` bound but `upper` tightened to `node.val` (everything in the left subtree must stay below this node).
5. Recurse into the right subtree with the same `upper` bound but `lower` tightened to `node.val`.
6. The tree is a valid BST only if both recursive calls return `true`.

**Time Complexity:** O(n) — every node is visited exactly once.
**Space Complexity:** O(h) — recursion stack depth equals the tree height (`h`); O(n) worst case for a skewed tree.

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def isValidBST(root: TreeNode | None) -> bool:
    def validate(node: TreeNode | None, lower: float, upper: float) -> bool:
        if node is None:
            return True
        if not (lower < node.val < upper):
            return False
        return validate(node.left, lower, node.val) and validate(node.right, node.val, upper)

    return validate(root, float('-inf'), float('inf'))
```

## Reference

- LeetCode: https://leetcode.com/problems/validate-binary-search-tree/
