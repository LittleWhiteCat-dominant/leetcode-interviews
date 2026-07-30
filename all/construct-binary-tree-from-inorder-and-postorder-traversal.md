# 106. Construct Binary Tree from Inorder and Postorder Traversal

**Difficulty:** Medium
**Topics:** Array, Hash Table, Divide and Conquer, Tree, Binary Tree
**Common companies:** All big tech
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

Given two integer arrays `inorder` and `postorder` where `inorder` is the inorder traversal of a binary tree and `postorder` is the postorder traversal of the same tree, construct and return *the binary tree*.

 

**Example 1:**

```

**Input:** inorder = [9,3,15,20,7], postorder = [9,15,7,20,3]
**Output:** [3,9,20,null,null,15,7]

```

**Example 2:**

```

**Input:** inorder = [-1], postorder = [-1]
**Output:** [-1]

```

 

**Constraints:**

	
- `1 <= inorder.length <= 3000`

	
- `postorder.length == inorder.length`

	
- `-3000 <= inorder[i], postorder[i] <= 3000`

	
- `inorder` and `postorder` consist of **unique** values.

	
- Each value of `postorder` also appears in `inorder`.

	
- `inorder` is **guaranteed** to be the inorder traversal of the tree.

	
- `postorder` is **guaranteed** to be the postorder traversal of the tree.

## Key Idea

Recursively split the array ranges

## Approach

1. Identify the core pattern for this category: **7.1 Binary Tree Traversal & Recursion**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/construct-binary-tree-from-inorder-and-postorder-traversal/
