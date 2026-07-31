# 236. Lowest Common Ancestor of a Binary Tree

**Difficulty:** Medium
**Topics:** Tree, Depth-First Search, Binary Tree
**Common companies:** **Meta favorite**
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

Given a binary tree, find the lowest common ancestor (LCA) of two given nodes in the tree.

According to the definition of LCA on Wikipedia: “The lowest common ancestor is defined between two nodes `p` and `q` as the lowest node in `T` that has both `p` and `q` as descendants (where we allow **a node to be a descendant of itself**).”

 

**Example 1:**

```

**Input:** root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 1
**Output:** 3
**Explanation:** The LCA of nodes 5 and 1 is 3.

```

**Example 2:**

```

**Input:** root = [3,5,1,6,2,0,8,null,null,7,4], p = 5, q = 4
**Output:** 5
**Explanation:** The LCA of nodes 5 and 4 is 5, since a node can be a descendant of itself according to the LCA definition.

```

**Example 3:**

```

**Input:** root = [1,2], p = 1, q = 2
**Output:** 1

```

 

**Constraints:**

	
- The number of nodes in the tree is in the range `[2, 105]`.

	
- `-109 <= Node.val <= 109`

	
- All `Node.val` are **unique**.

	
- `p != q`

	
- `p` and `q` will exist in the tree.

## Key Idea

Recursively check whether left/right subtree contains p/q

## Approach

This is solved with **bottom-up recursion that reports whether each subtree contains `p`, `q`, or both**:

1. Base case: if the current node is `None`, or is itself `p` or `q`, return it directly — this signals "found" up the call stack.
2. Recurse into the left and right subtrees, collecting what each side reports.
3. If both the left and right recursive calls return a non-null result, `p` and `q` were found in different subtrees, so the current node is their LCA.
4. Otherwise, propagate whichever side returned a non-null result (or `None` if neither did) up to the parent call.

**Time Complexity:** O(n) — every node may be visited once in the worst case.
**Space Complexity:** O(H) — for the recursion stack, where H is the tree height.

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def lowestCommonAncestor(root: TreeNode, p: TreeNode, q: TreeNode) -> TreeNode:
    if root is None or root is p or root is q:
        return root

    left = lowestCommonAncestor(root.left, p, q)
    right = lowestCommonAncestor(root.right, p, q)

    if left and right:
        return root
    return left if left else right
```

## Reference

- LeetCode: https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-tree/
