# 1448. Count Good Nodes in Binary Tree

**Difficulty:** Medium
**Topics:** Tree, Depth-First Search, Breadth-First Search, Binary Tree
**Common companies:** Amazon, Google
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

Given a binary tree `root`, a node *X* in the tree is named **good** if in the path from root to *X* there are no nodes with a value *greater than* X.



Return the number of **good** nodes in the binary tree.



 


**Example 1:**



****



```

**Input:** root = [3,1,4,3,null,1,5]
**Output:** 4
**Explanation:** Nodes in blue are **good**.
Root Node (3) is always a good node.
Node 4 -> (3,4) is the maximum value in the path starting from the root.
Node 5 -> (3,4,5) is the maximum value in the path
Node 3 -> (3,1,3) is the maximum value in the path.
```



**Example 2:**



****



```

**Input:** root = [3,3,null,4,2]
**Output:** 3
**Explanation:** Node 2 -> (3, 3, 2) is not good, because "3" is higher than it.
```



**Example 3:**



```

**Input:** root = [1]
**Output:** 1
**Explanation:** Root is considered as **good**.
```



 


**Constraints:**



	
- The number of nodes in the binary tree is in the range `[1, 10^5]`.

	
- Each node's value is between `[-10^4, 10^4]`.

## Key Idea

DFS carrying the max value seen along the path

## Approach

This is solved with **a top-down DFS that carries the maximum value seen so far on the path**:

1. Recurse with the current node and `max_so_far`, the largest value encountered from the root down to (but not including) this node.
2. A node counts as good if `node.val >= max_so_far`.
3. Update `max_so_far` to `max(max_so_far, node.val)` before descending into the children, so each child sees the correct running maximum for its own path.
4. Recurse into the left and right subtrees, summing their good-node counts along with the current node's contribution.
5. Kick off the recursion at the root with `max_so_far` initialized to `root.val`.

**Time Complexity:** O(n) — every node is visited exactly once.
**Space Complexity:** O(h) — recursion stack proportional to the tree height.

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def goodNodes(root: TreeNode) -> int:
    def dfs(node: TreeNode | None, max_so_far: int) -> int:
        if not node:
            return 0
        count = 1 if node.val >= max_so_far else 0
        max_so_far = max(max_so_far, node.val)
        count += dfs(node.left, max_so_far)
        count += dfs(node.right, max_so_far)
        return count

    return dfs(root, root.val)
```

## Reference

- LeetCode: https://leetcode.com/problems/count-good-nodes-in-binary-tree/
