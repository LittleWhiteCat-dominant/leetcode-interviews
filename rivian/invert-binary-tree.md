# 226. Invert Binary Tree

**Difficulty:** Easy
**Topics:** Tree, Depth-First Search, Breadth-First Search, Binary Tree, Recursion, Iteration
**Reported at Rivian:** Confirmed — reported as a coding challenge question for the Software Engineer II (RIV-4) role.

## Problem Description

Given the `root` of a binary tree, invert the tree, and return its root.

Inverting a binary tree means swapping every node's left and right children throughout the entire tree.

## Example 1

```
Input: root = [4,2,7,1,3,6,9]
Output: [4,7,2,9,6,3,1]
```

## Example 2

```
Input: root = [2,1,3]
Output: [2,3,1]
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

**Recursive approach:**
1. Base case: if the node is `None`, return `None`.
2. Recursively invert the left subtree and the right subtree.
3. Swap the node's `left` and `right` pointers.
4. Return the node.

**Iterative approach (BFS with a queue, or DFS with a stack):**
1. Use a queue (or stack) to process nodes one at a time.
2. For each node popped, swap its `left` and `right` children.
3. Push the (now swapped) children onto the queue/stack if they exist.
4. Continue until the queue/stack is empty.

**Time Complexity:** O(n) — every node is visited exactly once.
**Space Complexity:** O(h) for the recursive call stack (h = tree height), or O(n) in the worst case for the iterative queue/stack (a very wide tree).

## Reference Solution (Python, Recursive)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def invert_tree(root: "TreeNode | None") -> "TreeNode | None":
    if root is None:
        return None

    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
```

## Reference Solution (Python, Iterative BFS)

```python
from collections import deque


def invert_tree_iterative(root: "TreeNode | None") -> "TreeNode | None":
    if root is None:
        return None

    queue = deque([root])
    while queue:
        node = queue.popleft()
        node.left, node.right = node.right, node.left
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)

    return root
```

## Follow-up Questions Interviewers May Ask

- Can you solve it iteratively as well as recursively? What are the trade-offs (stack overflow risk on deep trees)?
- How would you verify whether a tree is a mirror of another tree without actually inverting it (LC 101, Symmetric Tree)?
- How would this change for an N-ary tree, where each node can have more than two children?
