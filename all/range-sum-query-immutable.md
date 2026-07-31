# 303. Range Sum Query - Immutable

**Difficulty:** Easy
**Topics:** Array, Design, Prefix Sum
**Common companies:** Google, Amazon
**Category (README):** 1.3 Prefix Sum

## Problem Description

Given an integer array `nums`, handle multiple queries of the following type:

	
- Calculate the **sum** of the elements of `nums` between indices `left` and `right` **inclusive** where `left <= right`.

Implement the `NumArray` class:

	
- `NumArray(int[] nums)` Initializes the object with the integer array `nums`.

	
- `int sumRange(int left, int right)` Returns the **sum** of the elements of `nums` between indices `left` and `right` **inclusive** (i.e. `nums[left] + nums[left + 1] + ... + nums[right]`).

 

**Example 1:**

```

**Input**
["NumArray", "sumRange", "sumRange", "sumRange"]
[[[-2, 0, 3, -5, 2, -1]], [0, 2], [2, 5], [0, 5]]
**Output**
[null, 1, -1, -3]

**Explanation**
NumArray numArray = new NumArray([-2, 0, 3, -5, 2, -1]);
numArray.sumRange(0, 2); // return (-2) + 0 + 3 = 1
numArray.sumRange(2, 5); // return 3 + (-5) + 2 + (-1) = -1
numArray.sumRange(0, 5); // return (-2) + 0 + 3 + (-5) + 2 + (-1) = -3

```

 

**Constraints:**

	
- `1 <= nums.length <= 104`

	
- `-105 <= nums[i] <= 105`

	
- `0 <= left <= right < nums.length`

	
- At most `104` calls will be made to `sumRange`.

## Key Idea

1D/2D prefix sum array

## Approach

This is solved with a **1D prefix-sum array**:

1. In the constructor, build a `prefix` array of length `n + 1` where `prefix[i]` is the sum of the first `i` elements of `nums`, with `prefix[0] = 0` as a sentinel.
2. Compute it incrementally: `prefix[i + 1] = prefix[i] + nums[i]`.
3. Since `sumRange(left, right)` needs `nums[left] + ... + nums[right]`, this equals `prefix[right + 1] - prefix[left]` — the cumulative sum up to `right` minus the cumulative sum up to (but not including) `left`.
4. Because `prefix` is precomputed once, each `sumRange` query is answered in O(1) with a single subtraction.

**Time Complexity:** O(n) to build the prefix sum, O(1) per `sumRange` query.
**Space Complexity:** O(n) — for the prefix sum array.

## Reference Solution (Python)

```python
from typing import List


class NumArray:
    def __init__(self, nums: List[int]):
        self.prefix = [0] * (len(nums) + 1)
        for i, num in enumerate(nums):
            self.prefix[i + 1] = self.prefix[i] + num

    def sumRange(self, left: int, right: int) -> int:
        return self.prefix[right + 1] - self.prefix[left]
```

## Reference

- LeetCode: https://leetcode.com/problems/range-sum-query-immutable/
