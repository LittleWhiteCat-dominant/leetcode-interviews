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

1. Identify the core pattern for this category: **7.1 Binary Tree Traversal & Recursion**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
