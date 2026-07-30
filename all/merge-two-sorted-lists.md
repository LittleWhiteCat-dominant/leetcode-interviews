# 21. Merge Two Sorted Lists

**Difficulty:** Easy
**Topics:** Linked List, Recursion
**Common companies:** All big tech
**Category (README):** 3. Linked List

## Problem Description

You are given the heads of two sorted linked lists `list1` and `list2`.

Merge the two lists into one **sorted** list. The list should be made by splicing together the nodes of the first two lists.

Return *the head of the merged linked list*.

 

**Example 1:**

```

**Input:** list1 = [1,2,4], list2 = [1,3,4]
**Output:** [1,1,2,3,4,4]

```

**Example 2:**

```

**Input:** list1 = [], list2 = []
**Output:** []

```

**Example 3:**

```

**Input:** list1 = [], list2 = [0]
**Output:** [0]

```

 

**Constraints:**

	
- The number of nodes in both lists is in the range `[0, 50]`.

	
- `-100 <= Node.val <= 100`

	
- Both `list1` and `list2` are sorted in **non-decreasing** order.

## Key Idea

Two pointers + dummy head node

## Approach

1. Identify the core pattern for this category: **3. Linked List**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/merge-two-sorted-lists/
