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

1. Identify the core pattern for this category: **7.2 Binary Search Tree (BST)**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/search-in-a-binary-search-tree/
