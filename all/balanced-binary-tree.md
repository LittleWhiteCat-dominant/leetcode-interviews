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

1. Identify the core pattern for this category: **7.1 Binary Tree Traversal & Recursion**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/balanced-binary-tree/
