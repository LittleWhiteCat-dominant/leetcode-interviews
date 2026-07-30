# 124. Binary Tree Maximum Path Sum

**Difficulty:** Hard
**Topics:** Dynamic Programming, Tree, Depth-First Search, Binary Tree
**Common companies:** All big tech (Meta favorite)
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

A **path** in a binary tree is a sequence of nodes where each pair of adjacent nodes in the sequence has an edge connecting them. A node can only appear in the sequence **at most once**. Note that the path does not need to pass through the root.

The **path sum** of a path is the sum of the node's values in the path.

Given the `root` of a binary tree, return *the maximum **path sum** of any **non-empty** path*.

 

**Example 1:**

```

**Input:** root = [1,2,3]
**Output:** 6
**Explanation:** The optimal path is 2 -> 1 -> 3 with a path sum of 2 + 1 + 3 = 6.

```

**Example 2:**

```

**Input:** root = [-10,9,20,null,null,15,7]
**Output:** 42
**Explanation:** The optimal path is 15 -> 20 -> 7 with a path sum of 15 + 20 + 7 = 42.

```

 

**Constraints:**

	
- The number of nodes in the tree is in the range `[1, 3 * 104]`.

	
- `-1000 <= Node.val <= 1000`

## Key Idea

Post-order recursion returning single-side max, global variable tracks the answer

## Approach

1. Identify the core pattern for this category: **7.1 Binary Tree Traversal & Recursion**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — each node is visited exactly once in the post-order recursion.
**Space Complexity:** O(h) — recursion stack, where h is the tree height.

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def maxPathSum(root: TreeNode | None) -> int:
    best = float("-inf")

    def single_side_max(node: TreeNode | None) -> int:
        nonlocal best
        if node is None:
            return 0

        left_gain = max(single_side_max(node.left), 0)
        right_gain = max(single_side_max(node.right), 0)

        best = max(best, node.val + left_gain + right_gain)

        return node.val + max(left_gain, right_gain)

    single_side_max(root)
    return best
```

## Reference

- LeetCode: https://leetcode.com/problems/binary-tree-maximum-path-sum/
