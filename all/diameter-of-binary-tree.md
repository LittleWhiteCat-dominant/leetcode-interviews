# 543. Diameter of Binary Tree

**Difficulty:** Easy
**Topics:** Tree, Depth-First Search, Binary Tree
**Common companies:** All big tech
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

Given the `root` of a binary tree, return *the length of the **diameter** of the tree*.

The **diameter** of a binary tree is the **length** of the longest path between any two nodes in a tree. This path may or may not pass through the `root`.

The **length** of a path between two nodes is represented by the number of edges between them.

 

**Example 1:**

```

**Input:** root = [1,2,3,4,5]
**Output:** 3
**Explanation:** 3 is the length of the path [4,2,1,3] or [5,2,1,3].

```

**Example 2:**

```

**Input:** root = [1,2]
**Output:** 1

```

 

**Constraints:**

	
- The number of nodes in the tree is in the range `[1, 104]`.

	
- `-100 <= Node.val <= 100`

## Key Idea

Post-order recursion; diameter = sum of left/right subtree depths

## Approach

1. Identify the core pattern for this category: **7.1 Binary Tree Traversal & Recursion**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — every node is visited exactly once.
**Space Complexity:** O(h) — recursion stack proportional to the tree height.

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def diameterOfBinaryTree(root: TreeNode | None) -> int:
    diameter = 0

    def depth(node: TreeNode | None) -> int:
        nonlocal diameter
        if not node:
            return 0
        left_depth = depth(node.left)
        right_depth = depth(node.right)
        diameter = max(diameter, left_depth + right_depth)
        return 1 + max(left_depth, right_depth)

    depth(root)
    return diameter
```

## Reference

- LeetCode: https://leetcode.com/problems/diameter-of-binary-tree/
