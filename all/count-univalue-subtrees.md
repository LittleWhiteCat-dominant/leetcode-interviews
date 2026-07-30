# 250. Count Univalue Subtrees

**Difficulty:** Medium (LeetCode Premium — statement not publicly available)
**Topics:** Tree, Depth-First Search, Binary Tree
**Common companies:** Google, Amazon
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

This is a Premium problem. View it on LeetCode: https://leetcode.com/problems/count-univalue-subtrees/

## Key Idea

DFS + prefix sum/hash map

## Approach

1. Identify the core pattern for this category: **7.1 Binary Tree Traversal & Recursion**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — every node is visited exactly once during the post-order pass.
**Space Complexity:** O(h) — recursion stack proportional to the tree height.

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def countUnivalSubtrees(root: TreeNode | None) -> int:
    count = 0

    def is_unival(node: TreeNode | None) -> bool:
        nonlocal count
        if not node:
            return True

        left_unival = is_unival(node.left)
        right_unival = is_unival(node.right)

        if not left_unival or not right_unival:
            return False
        if node.left and node.left.val != node.val:
            return False
        if node.right and node.right.val != node.val:
            return False

        count += 1
        return True

    is_unival(root)
    return count
```

## Reference

- LeetCode: https://leetcode.com/problems/count-univalue-subtrees/
