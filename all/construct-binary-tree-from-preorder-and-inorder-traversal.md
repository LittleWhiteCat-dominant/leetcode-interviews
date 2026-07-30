# 105. Construct Binary Tree from Preorder and Inorder Traversal

**Difficulty:** Medium
**Topics:** Array, Hash Table, Divide and Conquer, Tree, Binary Tree
**Common companies:** All big tech
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

Given two integer arrays `preorder` and `inorder` where `preorder` is the preorder traversal of a binary tree and `inorder` is the inorder traversal of the same tree, construct and return *the binary tree*.

 

**Example 1:**

```

**Input:** preorder = [3,9,20,15,7], inorder = [9,3,15,20,7]
**Output:** [3,9,20,null,null,15,7]

```

**Example 2:**

```

**Input:** preorder = [-1], inorder = [-1]
**Output:** [-1]

```

 

**Constraints:**

	
- `1 <= preorder.length <= 3000`

	
- `inorder.length == preorder.length`

	
- `-3000 <= preorder[i], inorder[i] <= 3000`

	
- `preorder` and `inorder` consist of **unique** values.

	
- Each value of `inorder` also appears in `preorder`.

	
- `preorder` is **guaranteed** to be the preorder traversal of the tree.

	
- `inorder` is **guaranteed** to be the inorder traversal of the tree.

## Key Idea

Recursively split the array ranges

## Approach

1. Identify the core pattern for this category: **7.1 Binary Tree Traversal & Recursion**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — each node is created once, and the hash map gives O(1) lookups for the root's position in `inorder`.
**Space Complexity:** O(n) — for the index map and the recursion stack.

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def buildTree(preorder: list[int], inorder: list[int]) -> TreeNode | None:
    index_in_inorder = {val: i for i, val in enumerate(inorder)}
    pre_idx = 0

    def build(left: int, right: int) -> TreeNode | None:
        nonlocal pre_idx
        if left > right:
            return None

        root_val = preorder[pre_idx]
        pre_idx += 1
        root = TreeNode(root_val)

        mid = index_in_inorder[root_val]
        root.left = build(left, mid - 1)
        root.right = build(mid + 1, right)

        return root

    return build(0, len(inorder) - 1)
```

## Reference

- LeetCode: https://leetcode.com/problems/construct-binary-tree-from-preorder-and-inorder-traversal/
