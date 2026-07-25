# 136. Single Number

**Difficulty:** Easy
**Topics:** Array, Bit Manipulation
**Category warm-up for:** Bit Manipulation & Math

## Problem Description

Given a **non-empty** array of integers `nums`, every element appears *twice* except for one. Find that single one.

You must implement a solution with a linear runtime complexity and use only constant extra space.

## Example 1

```
Input: nums = [2,2,1]
Output: 1
```

## Example 2

```
Input: nums = [4,1,2,1,2]
Output: 4
```

## Example 3

```
Input: nums = [1]
Output: 1
```

## Constraints

- `1 <= nums.length <= 3 * 10^4`
- `-3 * 10^4 <= nums[i] <= 3 * 10^4`
- Each element in the array appears twice except for one element which appears only once.

## Approach

1. **Key insight**: XOR (`^`) has two useful properties here: `a ^ a = 0` (a number XORed with itself cancels out), and XOR is commutative/associative, so order doesn't matter.
2. XOR every element in the array together. Every number that appears **twice** cancels itself out to `0`, leaving only the number that appears once.
3. This avoids the O(n) extra space that a hash-map-based counting approach would require, satisfying the "constant extra space" constraint.

**Time Complexity:** O(n) — a single pass through the array.
**Space Complexity:** O(1) extra space.

## Reference Solution (Python)

```python
from functools import reduce
from operator import xor


def single_number(nums: list[int]) -> int:
    return reduce(xor, nums, 0)
```

Equivalently, without `functools`:

```python
def single_number(nums: list[int]) -> int:
    result = 0
    for num in nums:
        result ^= num
    return result
```

## Follow-up Questions Interviewers May Ask

- How would you solve **Single Number II** (LC 137), where every element appears **three** times except one?
- How would you solve **Single Number III** (LC 260), where **two** elements each appear once and everything else appears twice?
- How would you explain why XOR works here to someone unfamiliar with bitwise operations?
