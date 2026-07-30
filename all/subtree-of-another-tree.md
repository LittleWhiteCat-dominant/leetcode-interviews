# 572. Subtree of Another Tree

**Difficulty:** Easy
**Topics:** Tree, Depth-First Search, String Matching, Binary Tree, Hash Function
**Common companies:** Amazon, Meta
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

Given the roots of two binary trees `root` and `subRoot`, return `true` if there is a subtree of `root` with the same structure and node values of` subRoot` and `false` otherwise.

A subtree of a binary tree `tree` is a tree that consists of a node in `tree` and all of this node's descendants. The tree `tree` could also be considered as a subtree of itself.

 

**Example 1:**

```

**Input:** root = [3,4,5,1,2], subRoot = [4,1,2]
**Output:** true

```

**Example 2:**

```

**Input:** root = [3,4,5,1,2,null,null,null,null,0], subRoot = [4,1,2]
**Output:** false

```

 

**Constraints:**

	
- The number of nodes in the `root` tree is in the range `[1, 2000]`.

	
- The number of nodes in the `subRoot` tree is in the range `[1, 1000]`.

	
- `-104 <= root.val <= 104`

	
- `-104 <= subRoot.val <= 104`

## Key Idea

Recursive node-by-node comparison

## Approach

1. Identify the core pattern for this category: **7.1 Binary Tree Traversal & Recursion**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(m * n) — in the worst case, `isSameTree` (O(n)) is invoked at each of the m nodes of `root`.
**Space Complexity:** O(m + n) — recursion stack depth from `isSubtree` plus `isSameTree`.

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def isSubtree(root: TreeNode, subRoot: TreeNode) -> bool:
    def isSameTree(p: TreeNode, q: TreeNode) -> bool:
        if not p and not q:
            return True
        if not p or not q or p.val != q.val:
            return False
        return isSameTree(p.left, q.left) and isSameTree(p.right, q.right)

    if not root:
        return subRoot is None
    if isSameTree(root, subRoot):
        return True
    return isSubtree(root.left, subRoot) or isSubtree(root.right, subRoot)
```

## Reference

- LeetCode: https://leetcode.com/problems/subtree-of-another-tree/
