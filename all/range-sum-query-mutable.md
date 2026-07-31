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

This is solved with a **Binary Indexed Tree (Fenwick Tree)**, since a plain prefix-sum array would need O(n) to rebuild after every update:

1. Store a 1-indexed Fenwick tree array `tree` of size `n + 1`, alongside a shadow copy `nums` of the current values (needed to compute deltas on update).
2. `_update_tree(index, delta)` propagates a change at `index` upward through the tree by repeatedly jumping to `i += i & (-i)` (adding the lowest set bit), updating every ancestor node that covers this index — O(log n) nodes touched.
3. `_prefix_sum(index)` computes the sum of `nums[0..index]` by walking downward from `i = index + 1`, repeatedly jumping to `i -= i & (-i)` and accumulating `tree[i]` — again O(log n) steps.
4. `update(index, val)` computes `delta = val - nums[index]`, updates the shadow array, then calls `_update_tree` to propagate that delta.
5. `sumRange(left, right)` returns `_prefix_sum(right) - _prefix_sum(left - 1)`, the same prefix-sum-difference trick as the immutable version, but now each prefix sum is O(log n) instead of O(1), trading a bit of query speed for O(log n) updates.
6. The initial tree is built by calling `update` once per input element in the constructor.

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
