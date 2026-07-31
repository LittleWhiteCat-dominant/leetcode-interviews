# 110. Balanced Binary Tree

**Difficulty:** Easy
**Topics:** Tree, Depth-First Search, Binary Tree
**Common companies:** Amazon, Apple
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

Given a binary tree, determine if it is **height-balanced**.

 

**Example 1:**

```

**Input:** root = [3,9,20,null,null,15,7]
**Output:** true

```

**Example 2:**

```

**Input:** root = [1,2,2,3,3,null,null,4,4]
**Output:** false

```

**Example 3:**

```

**Input:** root = []
**Output:** true

```

 

**Constraints:**

	
- The number of nodes in the tree is in the range `[0, 5000]`.

	
- `-104 <= Node.val <= 104`

## Key Idea

Post-order recursion returning both height and balance status

## Approach

This is solved with **a single post-order DFS that returns height and detects imbalance in one pass**:

1. Define a recursive `height` function that returns `0` for a `None` node (base case).
2. Recurse into the left and right subtrees first; if either returns `-1`, propagate `-1` immediately as a signal that an imbalance was already found further down.
3. Otherwise compare `abs(left_height - right_height)`; if it exceeds `1`, this node is unbalanced, so return `-1`.
4. If balanced so far, return `max(left_height, right_height) + 1` as this node's true height.
5. The tree is balanced overall if and only if the top-level call does not return `-1`.

**Time Complexity:** O(n) — each node is visited exactly once.
**Space Complexity:** O(h) — recursion stack, where h is the tree height (O(n) worst case, O(log n) if balanced).

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def isBalanced(root: TreeNode | None) -> bool:
    def height(node: TreeNode | None) -> int:
        if node is None:
            return 0
        left_height = height(node.left)
        if left_height == -1:
            return -1
        right_height = height(node.right)
        if right_height == -1:
            return -1
        if abs(left_height - right_height) > 1:
            return -1
        return max(left_height, right_height) + 1

    return height(root) != -1
```

## Reference

- LeetCode: https://leetcode.com/problems/balanced-binary-tree/
