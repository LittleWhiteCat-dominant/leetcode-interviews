# 100. Same Tree

**Difficulty:** Easy
**Topics:** Tree, Depth-First Search, Breadth-First Search, Binary Tree
**Common companies:** Amazon, Meta
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

Given the roots of two binary trees `p` and `q`, write a function to check if they are the same or not.

Two binary trees are considered the same if they are structurally identical, and the nodes have the same value.

 

**Example 1:**

```

**Input:** p = [1,2,3], q = [1,2,3]
**Output:** true

```

**Example 2:**

```

**Input:** p = [1,2], q = [1,null,2]
**Output:** false

```

**Example 3:**

```

**Input:** p = [1,2,1], q = [1,1,2]
**Output:** false

```

 

**Constraints:**

	
- The number of nodes in both trees is in the range `[0, 100]`.

	
- `-104 <= Node.val <= 104`

## Key Idea

Recursive node-by-node comparison

## Approach

1. Identify the core pattern for this category: **7.1 Binary Tree Traversal & Recursion**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/same-tree/
