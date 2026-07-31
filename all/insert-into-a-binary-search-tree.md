# 701. Insert into a Binary Search Tree

**Difficulty:** Medium
**Topics:** Tree, Binary Search Tree, Binary Tree
**Common companies:** Amazon, Apple
**Category (README):** 7.2 Binary Search Tree (BST)

## Problem Description

You are given the `root` node of a binary search tree (BST) and a `value` to insert into the tree. Return *the root node of the BST after the insertion*. It is **guaranteed** that the new value does not exist in the original BST.

**Notice** that there may exist multiple valid ways for the insertion, as long as the tree remains a BST after insertion. You can return **any of them**.

 

**Example 1:**

```

**Input:** root = [4,2,7,1,3], val = 5
**Output:** [4,2,7,1,3,5]
**Explanation:** Another accepted tree is:

```

**Example 2:**

```

**Input:** root = [40,20,60,10,30,50,70], val = 25
**Output:** [40,20,60,10,30,50,70,null,null,25]

```

**Example 3:**

```

**Input:** root = [4,2,7,1,3,null,null,null,null,null,null], val = 5
**Output:** [4,2,7,1,3,5]

```

 

**Constraints:**

	
- The number of nodes in the tree will be in the range `[0, 104]`.

	
- `-108 <= Node.val <= 108`

	
- All the values `Node.val` are **unique**.

	
- `-108 <= val <= 108`

	
- It's **guaranteed** that `val` does not exist in the original BST.

## Key Idea

Recursive/iterative traversal using BST properties

## Approach

This is solved with **an iterative descent that follows BST ordering to find the correct empty spot**:

1. If the tree is empty, the new value becomes the root, so return a fresh `TreeNode(val)` immediately.
2. Otherwise, starting at the root, compare `val` to the current node's value at each step.
3. If `val` is smaller, move to the left child; if that child is missing, attach the new node there and stop.
4. Otherwise, move to the right child; if that child is missing, attach the new node there and stop.
5. Return the (unchanged) `root` reference once the new node has been attached.

**Time Complexity:** O(h) — where `h` is the height of the tree (O(log n) average, O(n) worst case for a skewed tree).
**Space Complexity:** O(h) — for the iterative approach's implicit call depth is O(1); using recursion would be O(h) for the call stack.

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def insertIntoBST(root: "TreeNode | None", val: int) -> "TreeNode | None":
    if root is None:
        return TreeNode(val)

    node = root
    while True:
        if val < node.val:
            if node.left is None:
                node.left = TreeNode(val)
                break
            node = node.left
        else:
            if node.right is None:
                node.right = TreeNode(val)
                break
            node = node.right

    return root
```

## Reference

- LeetCode: https://leetcode.com/problems/insert-into-a-binary-search-tree/
