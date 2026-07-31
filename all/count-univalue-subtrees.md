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

This is solved with **post-order DFS that reports whether each subtree is univalue**:

1. Define a helper `is_unival(node)` that returns whether the subtree rooted at `node` has all equal values, using an empty subtree (`None`) as trivially univalue.
2. Recurse into the left and right children first (post-order), since a subtree can only be univalue if both of its children's subtrees are.
3. If either child recursion returns `False`, or a present child's value differs from the current node's value, the current subtree is not univalue.
4. Otherwise, increment the global `count` and return `True` for this subtree.
5. Run the helper from `root` and return the accumulated `count`.

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
