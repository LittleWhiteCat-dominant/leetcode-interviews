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

1. Identify the core pattern for this category: **7.2 Binary Search Tree (BST)**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/validate-binary-search-tree/
