# 450. Delete Node in a BST

**Difficulty:** Medium
**Topics:** Tree, Binary Search Tree, Binary Tree
**Common companies:** Amazon, Apple
**Category (README):** 7.2 Binary Search Tree (BST)

## Problem Description

Given a root node reference of a BST and a key, delete the node with the given key in the BST. Return *the **root node reference** (possibly updated) of the BST*.

Basically, the deletion can be divided into two stages:

	
- Search for a node to remove.

	
- If the node is found, delete the node.

 

**Example 1:**

```

**Input:** root = [5,3,6,2,4,null,7], key = 3
**Output:** [5,4,6,2,null,null,7]
**Explanation:** Given key to delete is 3. So we find the node with value 3 and delete it.
One valid answer is [5,4,6,2,null,null,7], shown in the above BST.
Please notice that another valid answer is [5,2,6,null,4,null,7] and it's also accepted.

```

**Example 2:**

```

**Input:** root = [5,3,6,2,4,null,7], key = 0
**Output:** [5,3,6,2,4,null,7]
**Explanation:** The tree does not contain a node with value = 0.

```

**Example 3:**

```

**Input:** root = [], key = 0
**Output:** []

```

 

**Constraints:**

	
- The number of nodes in the tree is in the range `[0, 104]`.

	
- `-105 <= Node.val <= 105`

	
- Each node has a **unique** value.

	
- `root` is a valid binary search tree.

	
- `-105 <= key <= 105`

 

**Follow up:** Could you solve it with time complexity `O(height of tree)`?

## Key Idea

Recursive/iterative traversal using BST properties

## Approach

This is solved with **BST-guided recursive search followed by successor replacement**:

1. Use the BST property to navigate to the target: recurse left if `key < root.val`, recurse right if `key > root.val`, reassigning `root.left`/`root.right` to the recursive result so the tree gets patched up on the way back.
2. Once `root.val == key`, handle the easy cases first: if the node has no left child, its right child replaces it; if it has no right child, its left child replaces it.
3. If the node has both children, find its in-order successor: the leftmost node in its right subtree (the smallest value greater than `root.val`).
4. Copy the successor's value into `root.val`, then recursively delete that successor value from the right subtree, since a value can't be duplicated in the tree.
5. Return `root` (unchanged or updated) at every level so the tree stays correctly linked as the recursion unwinds.

**Time Complexity:** O(h) — where h is the tree height, since we descend once to find the node and once more (in the right subtree) to find its successor.
**Space Complexity:** O(h) — recursion stack depth.

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def deleteNode(root: TreeNode | None, key: int) -> TreeNode | None:
    if not root:
        return None

    if key < root.val:
        root.left = deleteNode(root.left, key)
    elif key > root.val:
        root.right = deleteNode(root.right, key)
    else:
        if not root.left:
            return root.right
        if not root.right:
            return root.left

        successor = root.right
        while successor.left:
            successor = successor.left
        root.val = successor.val
        root.right = deleteNode(root.right, successor.val)

    return root
```

## Reference

- LeetCode: https://leetcode.com/problems/delete-node-in-a-bst/
