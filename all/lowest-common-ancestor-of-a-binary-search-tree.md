# 235. Lowest Common Ancestor of a Binary Search Tree

**Difficulty:** Medium
**Topics:** Tree, Depth-First Search, Binary Search Tree, Binary Tree
**Common companies:** Amazon, Google
**Category (README):** 7.2 Binary Search Tree (BST)

## Problem Description

Given a binary search tree (BST), find the lowest common ancestor (LCA) node of two given nodes in the BST.

According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants (where we allow **a node to be a descendant of itself**).”

 

**Example 1:**

```

**Input:** root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 8
**Output:** 6
**Explanation:** The LCA of nodes 2 and 8 is 6.

```

**Example 2:**

```

**Input:** root = [6,2,8,0,4,7,9,null,null,3,5], p = 2, q = 4
**Output:** 2
**Explanation:** The LCA of nodes 2 and 4 is 2, since a node can be a descendant of itself according to the LCA definition.

```

**Example 3:**

```

**Input:** root = [2,1], p = 2, q = 1
**Output:** 2

```

 

**Constraints:**

	
- The number of nodes in the tree is in the range `[2, 105]`.

	
- `-109 <= Node.val <= 109`

	
- All `Node.val` are **unique**.

	
- `p != q`

	
- `p` and `q` will exist in the BST.

## Key Idea

Use value comparisons to directly decide the search direction

## Approach

This is solved with **iterative BST navigation, exploiting the ordering property to avoid searching both subtrees**:

1. Start at the root and compare both `p.val` and `q.val` against the current node's value.
2. If both are smaller than the current node, the LCA must be in the left subtree, so move `node = node.left`.
3. If both are larger, the LCA must be in the right subtree, so move `node = node.right`.
4. Otherwise, `p` and `q` are on different sides (or one equals the current node), meaning the current node is the split point and thus the LCA — return it immediately.

**Time Complexity:** O(H) — where H is the tree height, since we walk a single root-to-node path using BST ordering.
**Space Complexity:** O(1) — the iterative approach uses no extra space beyond a single pointer.

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    node = root

    while node:
        if p.val < node.val and q.val < node.val:
            node = node.left
        elif p.val > node.val and q.val > node.val:
            node = node.right
        else:
            return node

    return None
```

## Reference

- LeetCode: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/
