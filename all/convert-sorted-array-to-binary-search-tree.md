# 108. Convert Sorted Array to Binary Search Tree

**Difficulty:** Easy
**Topics:** Array, Divide and Conquer, Tree, Binary Search Tree, Binary Tree
**Common companies:** Google, Meta
**Category (README):** 7.2 Binary Search Tree (BST)

## Problem Description

Given an integer array `nums` where the elements are sorted in **ascending order**, convert *it to a ****height-balanced*** *binary search tree*.

 

**Example 1:**

```

**Input:** nums = [-10,-3,0,5,9]
**Output:** [0,-3,9,-10,null,5]
**Explanation:** [0,-10,5,null,-3,null,9] is also accepted:

```

**Example 2:**

```

**Input:** nums = [1,3]
**Output:** [3,1]
**Explanation:** [1,null,3] and [3,1] are both height-balanced BSTs.

```

 

**Constraints:**

	
- `1 <= nums.length <= 104`

	
- `-104 <= nums[i] <= 104`

	
- `nums` is sorted in a **strictly increasing** order.

## Key Idea

Recursively pick the midpoint as root

## Approach

This is solved with **recursive divide and conquer, always rooting at the midpoint**:

1. Given a subarray range `[lo, hi]`, pick the middle index `mid` as the root of that subtree, which keeps the two halves as balanced as possible.
2. Create a `TreeNode` with `nums[mid]`.
3. Recursively build the left subtree from `[lo, mid - 1]` and the right subtree from `[mid + 1, hi]`.
4. The base case is `lo > hi`, which returns `None` for an empty range.
5. Return the root produced by building the full range `[0, n - 1]`.

**Time Complexity:** O(n) — every element becomes exactly one tree node, visited once.
**Space Complexity:** O(log n) — recursion stack depth for a height-balanced tree (excluding the O(n) output tree itself).

## Reference Solution (Python)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


def sortedArrayToBST(nums: list[int]) -> TreeNode | None:
    def build(lo: int, hi: int) -> TreeNode | None:
        if lo > hi:
            return None
        mid = (lo + hi + 1) // 2
        root = TreeNode(nums[mid])
        root.left = build(lo, mid - 1)
        root.right = build(mid + 1, hi)
        return root

    return build(0, len(nums) - 1)
```

## Reference

- LeetCode: https://leetcode.com/problems/convert-sorted-array-to-binary-search-tree/
