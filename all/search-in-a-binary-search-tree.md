# 700. Search in a Binary Search Tree

**Difficulty:** Easy
**Topics:** Tree, Binary Search Tree, Binary Tree
**Common companies:** Amazon, Apple
**Category (README):** 7.2 Binary Search Tree (BST)

## Problem Description

You are given the `root` of a binary search tree (BST) and an integer `val`.

Find the node in the BST that the node's value equals `val` and return the subtree rooted with that node. If such a node does not exist, return `null`.

 

**Example 1:**

```

**Input:** root = [4,2,7,1,3], val = 2
**Output:** [2,1,3]

```

**Example 2:**

```

**Input:** root = [4,2,7,1,3], val = 5
**Output:** []

```

 

**Constraints:**

	
- The number of nodes in the tree is in the range `[1, 5000]`.

	
- `1 <= Node.val <= 107`

	
- `root` is a binary search tree.

	
- `1 <= val <= 107`

## Key Idea

Recursive/iterative traversal using BST properties

## Approach

This is solved with **an iterative descent that exploits the BST ordering property**:

1. Start at `root` and loop while the current node exists and its value doesn't equal `val`.
2. At each step, use the BST invariant to decide direction: if `val` is smaller than the current node's value, move to the left child; otherwise move to the right child.
3. The loop naturally terminates either when a node with value `val` is found, or when it falls off the tree (`root` becomes `None`), which is also the correct "not found" result.

**Time Complexity:** O(h) — each step follows the BST invariant down a single path.
**Space Complexity:** O(1) — iterative traversal with no recursion stack.

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def searchBST(root: TreeNode, val: int) -> TreeNode:
    while root and root.val != val:
        root = root.left if val < root.val else root.right
    return root
```

## Reference

- LeetCode: https://leetcode.com/problems/search-in-a-binary-search-tree/
