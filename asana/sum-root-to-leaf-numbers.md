# 129. Sum Root to Leaf Numbers

**Difficulty:** Medium
**Topics:** Tree, Depth-First Search, Binary Tree
**Reported at Asana:** Tracked in Asana's known coding question bank (InterviewSolver).

## Problem Description

You are given the `root` of a binary tree containing digits from `0` to `9` only.

Each root-to-leaf path in the tree represents a number.

- For example, the root-to-leaf path `1 -> 2 -> 3` represents the number `123`.

Return *the total sum of all root-to-leaf numbers*. Test cases are generated so that the answer will fit in a **32-bit** integer.

A **leaf** node is a node with no children.

## Example 1

```
Input: root = [1,2,3]
Output: 25
Explanation:
The root-to-leaf path 1->2 represents the number 12.
The root-to-leaf path 1->3 represents the number 13.
Therefore, sum = 12 + 13 = 25.
```

## Example 2

```
Input: root = [4,9,0,5,1]
Output: 1026
Explanation:
The root-to-leaf path 4->9->5 represents the number 495.
The root-to-leaf path 4->9->1 represents the number 491.
The root-to-leaf path 4->0 represents the number 40.
Therefore, sum = 495 + 491 + 40 = 1026.
```

## Constraints

- The number of nodes in the tree is in the range `[1, 1000]`.
- `0 <= Node.val <= 9`
- The depth of the tree will not exceed `10`.

## Approach

1. Perform a DFS from the root, carrying along the number formed so far (`current_number = current_number * 10 + node.val` as you descend).
2. When you reach a **leaf** node (no left and no right child), add `current_number` to the running total.
3. Recurse into both children, passing down the updated `current_number`; sum the contributions from the left and right subtrees.

**Time Complexity:** O(n) — every node is visited once.
**Space Complexity:** O(h) for the recursion stack, where h is the tree height (O(log n) balanced, O(n) worst case skewed).

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def sum_numbers(root: "TreeNode | None") -> int:
    def dfs(node: "TreeNode | None", current_number: int) -> int:
        if node is None:
            return 0

        current_number = current_number * 10 + node.val

        if node.left is None and node.right is None:
            return current_number

        return dfs(node.left, current_number) + dfs(node.right, current_number)

    return dfs(root, 0)
```

## Follow-up Questions Interviewers May Ask

- How would you solve this iteratively with an explicit stack instead of recursion?
- How would you handle a tree with digits that aren't restricted to `0`-`9` (e.g. multi-digit node values)?
- Can you also return the actual list of root-to-leaf numbers, not just their sum?
