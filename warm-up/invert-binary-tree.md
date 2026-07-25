# 226. Invert Binary Tree

**Difficulty:** Easy
**Topics:** Tree, Depth-First Search, Breadth-First Search, Binary Tree, Recursion
**Category warm-up for:** Tree

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

**Iterative approach (BFS with a queue):**
1. Push the root onto a queue.
2. Repeatedly pop a node, swap its `left` and `right` children, and push each (now swapped) child onto the queue if it exists.
3. Continue until the queue is empty.

**Time Complexity:** O(n) — every node is visited exactly once.
**Space Complexity:** O(h) for the recursive call stack (h = tree height); O(n) worst case for the iterative queue on a very wide tree.

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

## Follow-up Questions Interviewers May Ask

- Can you also implement this iteratively? What are the trade-offs versus the recursive version (stack overflow risk on very deep trees)?
- How would you verify whether a tree is a mirror image of another tree without physically inverting it (see LC 101, Symmetric Tree)?
- How would this generalize to an N-ary tree, where each node can have more than two children?
