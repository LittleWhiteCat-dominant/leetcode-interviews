# 314. Binary Tree Vertical Order Traversal

**Difficulty:** Medium (LeetCode Premium — statement not publicly available)
**Topics:** Hash Table, Tree, Depth-First Search, Breadth-First Search, Sorting, Binary Tree
**Common companies:** **Meta favorite**
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

This is a Premium problem. View it on LeetCode: https://leetcode.com/problems/binary-tree-vertical-order-traversal/

## Key Idea

BFS tracking column index, then group and sort by column

## Approach

1. Identify the core pattern for this category: **7.1 Binary Tree Traversal & Recursion**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n log n) — O(n) for the BFS, plus sorting the up-to-n distinct column indices.
**Space Complexity:** O(n) — for the queue and the column-to-values map.

## Reference Solution (Python)

```python
from collections import defaultdict, deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def verticalOrder(root: TreeNode | None) -> list[list[int]]:
    if not root:
        return []

    columns = defaultdict(list)
    queue = deque([(root, 0)])

    while queue:
        node, col = queue.popleft()
        columns[col].append(node.val)
        if node.left:
            queue.append((node.left, col - 1))
        if node.right:
            queue.append((node.right, col + 1))

    return [columns[col] for col in sorted(columns)]
```

## Reference

- LeetCode: https://leetcode.com/problems/binary-tree-vertical-order-traversal/
