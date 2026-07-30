# 307. Range Sum Query - Mutable

**Difficulty:** Medium
**Topics:** Array, Divide and Conquer, Design, Binary Indexed Tree, Segment Tree
**Common companies:** Google
**Category (README):** 7.4 Segment Tree / Binary Indexed Tree

## Problem Description

Given an integer array `nums`, handle multiple queries of the following types:

	
- **Update** the value of an element in `nums`.

	
- Calculate the **sum** of the elements of `nums` between indices `left` and `right` **inclusive** where `left <= right`.

Implement the `NumArray` class:

	
- `NumArray(int[] nums)` Initializes the object with the integer array `nums`.

	
- `void update(int index, int val)` **Updates** the value of `nums[index]` to be `val`.

	
- `int sumRange(int left, int right)` Returns the **sum** of the elements of `nums` between indices `left` and `right` **inclusive** (i.e. `nums[left] + nums[left + 1] + ... + nums[right]`).

 

**Example 1:**

```

**Input**
["NumArray", "sumRange", "update", "sumRange"]
[[[1, 3, 5]], [0, 2], [1, 2], [0, 2]]
**Output**
[null, 9, null, 8]

**Explanation**
NumArray numArray = new NumArray([1, 3, 5]);
numArray.sumRange(0, 2); // return 1 + 3 + 5 = 9
numArray.update(1, 2);   // nums = [1, 2, 5]
numArray.sumRange(0, 2); // return 1 + 2 + 5 = 8

```

 

**Constraints:**

	
- `1 <= nums.length <= 3 * 104`

	
- `-100 <= nums[i] <= 100`

	
- `0 <= index < nums.length`

	
- `-100 <= val <= 100`

	
- `0 <= left <= right < nums.length`

	
- At most `3 * 104` calls will be made to `update` and `sumRange`.

## Key Idea

Segment tree or Binary Indexed Tree (Fenwick Tree)

## Approach

1. Identify the core pattern for this category: **7.4 Segment Tree / Binary Indexed Tree**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(log n) per `update` or `sumRange` call using a Binary Indexed Tree; O(n log n) to build.
**Space Complexity:** O(n) — for the Fenwick tree and the shadow copy of `nums`.

## Reference Solution (Python)

```python
from typing import List


class NumArray:
    def __init__(self, nums: List[int]):
        self.n = len(nums)
        self.nums = [0] * self.n
        self.tree = [0] * (self.n + 1)
        for i, num in enumerate(nums):
            self.update(i, num)

    def _update_tree(self, index: int, delta: int) -> None:
        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def _prefix_sum(self, index: int) -> int:
        total = 0
        i = index + 1
        while i > 0:
            total += self.tree[i]
            i -= i & (-i)
        return total

    def update(self, index: int, val: int) -> None:
        delta = val - self.nums[index]
        self.nums[index] = val
        self._update_tree(index, delta)

    def sumRange(self, left: int, right: int) -> int:
        return self._prefix_sum(right) - self._prefix_sum(left - 1)
```

## Reference

- LeetCode: https://leetcode.com/problems/range-sum-query-mutable/
