# 102. Binary Tree Level Order Traversal

**Difficulty:** Medium
**Topics:** Tree, Breadth-First Search, Binary Tree
**Common companies:** All big tech
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

Given the `root` of a binary tree, return *the level order traversal of its nodes' values*. (i.e., from left to right, level by level).

 

**Example 1:**

```

**Input:** root = [3,9,20,null,null,15,7]
**Output:** [[3],[9,20],[15,7]]

```

**Example 2:**

```

**Input:** root = [1]
**Output:** [[1]]

```

**Example 3:**

```

**Input:** root = []
**Output:** []

```

 

**Constraints:**

	
- The number of nodes in the tree is in the range `[0, 2000]`.

	
- `-1000 <= Node.val <= 1000`

## Key Idea

BFS + queue

## Approach

This is solved with **breadth-first search, processing one full level at a time**:

1. Return an empty list immediately if `root` is `None`.
2. Initialize a queue with just the root node.
3. While the queue is non-empty, snapshot its current length — that count is exactly the number of nodes in this level.
4. Pop that many nodes, record their values into a `level` list, and enqueue any of their children.
5. Append the completed `level` to the result, and repeat until the queue is empty.

**Time Complexity:** O(n) — every node is enqueued and dequeued exactly once.
**Space Complexity:** O(n) — for the queue and the output, up to O(n) nodes at the widest level.

## Reference Solution (Python)

```python
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def levelOrder(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []

    result = []
    queue = deque([root])

    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)

    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/binary-tree-level-order-traversal/
