# 437. Path Sum III

**Difficulty:** Medium
**Topics:** Tree, Depth-First Search, Binary Tree
**Common companies:** Google, Amazon
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

Given the `root` of a binary tree and an integer `targetSum`, return *the number of paths where the sum of the values along the path equals* `targetSum`.

The path does not need to start or end at the root or a leaf, but it must go downwards (i.e., traveling only from parent nodes to child nodes).

 

**Example 1:**

```

**Input:** root = [10,5,-3,3,2,null,11,3,-2,null,1], targetSum = 8
**Output:** 3
**Explanation:** The paths that sum to 8 are shown.

```

**Example 2:**

```

**Input:** root = [5,4,8,11,null,13,4,7,2,null,null,5,1], targetSum = 22
**Output:** 3

```

 

**Constraints:**

	
- The number of nodes in the tree is in the range `[0, 1000]`.

	
- `-109 <= Node.val <= 109`

	
- `-1000 <= targetSum <= 1000`

## Key Idea

DFS + prefix sum/hash map

## Approach

1. Identify the core pattern for this category: **7.1 Binary Tree Traversal & Recursion**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — each node is visited once, with O(1) amortized hash map operations.
**Space Complexity:** O(n) — for the prefix-sum hash map and the recursion stack.

## Reference Solution (Python)

```python
from collections import defaultdict
from typing import Optional


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def pathSum(root: Optional[TreeNode], targetSum: int) -> int:
    prefix_counts = defaultdict(int)
    prefix_counts[0] = 1

    def dfs(node: Optional[TreeNode], current_sum: int) -> int:
        if not node:
            return 0

        current_sum += node.val
        count = prefix_counts[current_sum - targetSum]

        prefix_counts[current_sum] += 1
        count += dfs(node.left, current_sum) + dfs(node.right, current_sum)
        prefix_counts[current_sum] -= 1

        return count

    return dfs(root, 0)
```

## Reference

- LeetCode: https://leetcode.com/problems/path-sum-iii/
