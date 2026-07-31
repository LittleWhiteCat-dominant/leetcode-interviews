# 103. Binary Tree Zigzag Level Order Traversal

**Difficulty:** Medium
**Topics:** Tree, Breadth-First Search, Binary Tree
**Common companies:** All big tech
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

Given the `root` of a binary tree, return *the zigzag level order traversal of its nodes' values*. (i.e., from left to right, then right to left for the next level and alternate between).

 

**Example 1:**

```

**Input:** root = [3,9,20,null,null,15,7]
**Output:** [[3],[20,9],[15,7]]

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

	
- `-100 <= Node.val <= 100`

## Key Idea

BFS + queue

## Approach

This is solved with **level-order BFS that alternates the append direction each level**:

1. Return an empty list immediately if `root` is `None`.
2. Run the usual BFS, snapshotting the queue length at the start of each level to know how many nodes belong to it.
3. Use a `deque` for the current level's values and a `left_to_right` flag; append to the right end when the flag is true, and to the left end (`appendleft`) when it's false.
4. Still enqueue children left-to-right regardless of the flag, since the zigzag only affects output order, not traversal order.
5. After finishing a level, add it to the result and flip `left_to_right` before moving to the next level.

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


def zigzagLevelOrder(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []

    result = []
    queue = deque([root])
    left_to_right = True

    while queue:
        level = deque()
        for _ in range(len(queue)):
            node = queue.popleft()
            if left_to_right:
                level.append(node.val)
            else:
                level.appendleft(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(list(level))
        left_to_right = not left_to_right

    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/binary-tree-zigzag-level-order-traversal/
