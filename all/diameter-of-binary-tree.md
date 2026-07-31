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

This is solved with **post-order DFS that computes depth while tracking the best diameter seen**:

1. Define `depth(node)`, which returns the height of the subtree rooted at `node` (0 for `None`).
2. Recursively compute `left_depth = depth(node.left)` and `right_depth = depth(node.right)` before combining them, since the diameter through a node depends on both subtree heights.
3. At each node, the longest path passing through it is `left_depth + right_depth`; update the running `diameter` with `max(diameter, left_depth + right_depth)`.
4. Return `1 + max(left_depth, right_depth)` as this node's own height, so the parent call can use it correctly.
5. After the full traversal from `root`, `diameter` holds the answer, since every possible "peak" node was considered.

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
