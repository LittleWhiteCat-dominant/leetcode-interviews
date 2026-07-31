# 287. Find the Duplicate Number

**Difficulty:** Medium
**Topics:** Array, Two Pointers, Binary Search, Bit Manipulation
**Common companies:** All big tech
**Category (README):** 3. Linked List

## Problem Description

Given an array of integers `nums` containing `n + 1` integers where each integer is in the range `[1, n]` inclusive.

There is only **one repeated number** in `nums`, return *this repeated number*.

You must solve the problem **without** modifying the array `nums` and using only constant extra space.

 

**Example 1:**

```

**Input:** nums = [1,3,4,2,2]
**Output:** 2

```

**Example 2:**

```

**Input:** nums = [3,1,3,4,2]
**Output:** 3

```

**Example 3:**

```

**Input:** nums = [3,3,3,3,3]
**Output:** 3
```

 

**Constraints:**

	
- `1 <= n <= 105`

	
- `nums.length == n + 1`

	
- `1 <= nums[i] <= n`

	
- All the integers in `nums` appear only **once** except for **precisely one integer** which appears **two or more** times.

 

**Follow up:**

	
- How can we prove that at least one duplicate number must exist in `nums`?

	
- Can you solve the problem in linear runtime complexity?

## Key Idea

Treat the array as a linked list, apply Floyd's algorithm

## Approach

This is solved with **Floyd's cycle detection, treating array values as "next pointers"**:

1. View `nums` as a linked list where each index `i` points to index `nums[i]`; since a duplicate value exists, this implicit list must contain a cycle.
2. Move a slow pointer one step (`slow = nums[slow]`) and a fast pointer two steps (`fast = nums[nums[fast]]`) each iteration until they meet inside the cycle.
3. Reset `slow` to the start (`nums[0]`) while leaving `fast` at the meeting point.
4. Advance both pointers one step at a time; the index where they meet again is the entrance to the cycle, which is exactly the duplicate number.

**Time Complexity:** O(n) — Floyd's cycle detection makes a constant number of passes over the implicit linked list.
**Space Complexity:** O(1) — only two pointers are used, and the array is not modified.

## Reference Solution (Python)

```python
def findDuplicate(nums: list[int]) -> int:
    slow = fast = nums[0]

    while True:
        slow = nums[slow]
        fast = nums[nums[fast]]
        if slow == fast:
            break

    slow = nums[0]
    while slow != fast:
        slow = nums[slow]
        fast = nums[fast]

    return slow
```

## Reference

- LeetCode: https://leetcode.com/problems/find-the-duplicate-number/
