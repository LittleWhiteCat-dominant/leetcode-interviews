# 199. Binary Tree Right Side View

**Difficulty:** Medium
**Topics:** Tree, Breadth-First Search, Depth-First Search, Binary Tree
**Reported at Asana:** Tracked in Asana's known coding question bank (InterviewSolver).

## Problem Description

Given the `root` of a binary tree, imagine yourself standing on the **right side** of it, return *the values of the nodes you can see ordered from top to bottom*.

## Example 1

```
Input: root = [1,2,3,null,5,null,4]
Output: [1,3,4]
```

## Example 2

```
Input: root = [1,null,3]
Output: [1,3]
```

## Example 3

```
Input: root = []
Output: []
```

## Constraints

- The number of nodes in the tree is in the range `[0, 100]`.
- `-100 <= Node.val <= 100`

## Approach

**Approach A — BFS (level order)**
1. Perform a standard level-order BFS traversal using a queue.
2. For each level, the **last** node processed is the one visible from the right side.
3. Collect that last node's value per level.

**Approach B — DFS (right-first)**
1. Traverse the right subtree before the left subtree at every node.
2. Track the current depth; the first time you reach a given depth (since right is visited first), record that node's value.

**Time Complexity:** O(n) — every node is visited exactly once.
**Space Complexity:** O(n) in the worst case (widest BFS level, or deepest DFS recursion stack for a skewed tree).

## Reference Solution (Python, BFS)

```python
from collections import deque


class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def right_side_view(root: "TreeNode | None") -> list[int]:
    if not root:
        return []

    result: list[int] = []
    queue = deque([root])

    while queue:
        level_size = len(queue)
        for i in range(level_size):
            node = queue.popleft()
            if i == level_size - 1:
                result.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)

    return result
```

## Follow-up Questions Interviewers May Ask

- How would you solve this with DFS instead of BFS, and what are the trade-offs?
- How would you return the **left** side view instead?
- How would you adapt this to an N-ary tree instead of a binary tree?
