# 938. Range Sum of BST

**Difficulty:** Easy
**Topics:** Tree, Depth-First Search, Binary Search Tree, Binary Tree
**Common companies:** **Meta favorite**
**Category (README):** 7.2 Binary Search Tree (BST)

## Problem Description

Given the `root` node of a binary search tree and two integers `low` and `high`, return *the sum of values of all nodes with a value in the **inclusive** range *`[low, high]`.

 

**Example 1:**

```

**Input:** root = [10,5,15,3,7,null,18], low = 7, high = 15
**Output:** 32
**Explanation:** Nodes 7, 10, and 15 are in the range [7, 15]. 7 + 10 + 15 = 32.

```

**Example 2:**

```

**Input:** root = [10,5,15,3,7,13,18,1,null,6], low = 6, high = 10
**Output:** 23
**Explanation:** Nodes 6, 7, and 10 are in the range [6, 10]. 6 + 7 + 10 = 23.

```

 

**Constraints:**

	
- The number of nodes in the tree is in the range `[1, 2 * 104]`.

	
- `1 <= Node.val <= 105`

	
- `1 <= low <= high <= 105`

	
- All `Node.val` are **unique**.

## Key Idea

Prune the recursion using BST ordering properties

## Approach

This is solved with **DFS that prunes branches using BST ordering**:

1. At the base case, if the current node is `None`, its contribution to the sum is 0.
2. If the current node's value is less than `low`, every value in its left subtree is even smaller (BST property), so skip the left subtree entirely and only recurse right.
3. If the current node's value is greater than `high`, every value in its right subtree is even larger, so skip the right subtree entirely and only recurse left.
4. Otherwise the node's value is within `[low, high]`, so include it in the sum and recurse into both children to collect any additional in-range values.
5. This pruning avoids visiting subtrees that provably cannot contain any value in range.

**Time Complexity:** O(n) worst case — pruned using BST ordering, closer to O(log n + k) on balanced trees where k nodes are in range.
**Space Complexity:** O(h) — recursion stack proportional to the tree height.

## Reference Solution (Python)

```python
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def rangeSumBST(root: Optional[TreeNode], low: int, high: int) -> int:
    if not root:
        return 0

    if root.val < low:
        return rangeSumBST(root.right, low, high)
    if root.val > high:
        return rangeSumBST(root.left, low, high)

    return (
        root.val
        + rangeSumBST(root.left, low, high)
        + rangeSumBST(root.right, low, high)
    )
```

## Reference

- LeetCode: https://leetcode.com/problems/range-sum-of-bst/
