# 297. Serialize and Deserialize Binary Tree

**Difficulty:** Hard
**Topics:** String, Tree, Depth-First Search, Breadth-First Search, Design, Binary Tree
**Common companies:** All big tech
**Category (README):** 7.1 Binary Tree Traversal & Recursion

## Problem Description

Serialization is the process of converting a data structure or object into a sequence of bits so that it can be stored in a file or memory buffer, or transmitted across a network connection link to be reconstructed later in the same or another computer environment.

Design an algorithm to serialize and deserialize a binary tree. There is no restriction on how your serialization/deserialization algorithm should work. You just need to ensure that a binary tree can be serialized to a string and this string can be deserialized to the original tree structure.

**Clarification:** The input/output format is the same as how LeetCode serializes a binary tree. You do not necessarily need to follow this format, so please be creative and come up with different approaches yourself.

 

**Example 1:**

```

**Input:** root = [1,2,3,null,null,4,5]
**Output:** [1,2,3,null,null,4,5]

```

**Example 2:**

```

**Input:** root = []
**Output:** []

```

 

**Constraints:**

	
- The number of nodes in the tree is in the range `[0, 104]`.

	
- `-1000 <= Node.val <= 1000`

## Key Idea

Pre-order traversal + null-node placeholders

## Approach

1. Identify the core pattern for this category: **7.1 Binary Tree Traversal & Recursion**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) for both `serialize` and `deserialize` — each node is visited exactly once.
**Space Complexity:** O(n) — the serialized string/list and the recursion stack both scale with the number of nodes.

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Codec:
    def serialize(self, root: TreeNode) -> str:
        values = []

        def dfs(node: TreeNode) -> None:
            if not node:
                values.append("N")
                return
            values.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(values)

    def deserialize(self, data: str) -> TreeNode:
        values = iter(data.split(","))

        def build() -> TreeNode:
            val = next(values)
            if val == "N":
                return None
            node = TreeNode(int(val))
            node.left = build()
            node.right = build()
            return node

        return build()
```

## Reference

- LeetCode: https://leetcode.com/problems/serialize-and-deserialize-binary-tree/
