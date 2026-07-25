# 152. Maximum Product Subarray

**Difficulty:** Medium
**Topics:** Array, Dynamic Programming
**Reported at Asana:** Tracked in Asana's known coding question bank (InterviewSolver).

## Problem Description

Given an integer array `nums`, find a subarray that has the largest product, and return *the product*.

The test cases are generated so that the answer will fit in a **32-bit** integer.

## Example 1

```
Input: nums = [2,3,-2,4]
Output: 6
Explanation: [2,3] has the largest product 6.
```

## Example 2

```
Input: nums = [-2,0,-1]
Output: 0
Explanation: The result cannot be 2, because [-2,-1] is not a subarray.
```

## Constraints

- `1 <= nums.length <= 2 * 10^4`
- `-10 <= nums[i] <= 10`
- The product of any subarray of `nums` is **guaranteed** to fit in a 32-bit integer.

## Approach

The key challenge versus Maximum Subarray (LC 53) is that a **negative number can flip** the sign of the running product — a very negative running minimum, multiplied by another negative number, can become the new maximum.

1. Track two running values at each index: `max_so_far` (the maximum product of a subarray ending here) and `min_so_far` (the minimum product of a subarray ending here, which matters because a negative number could turn it into the new max).
2. At each element `num`:
   - If `num` is negative, swap `max_so_far` and `min_so_far` before updating (since multiplying by a negative flips which one is more extreme).
   - Update `max_so_far = max(num, max_so_far * num)` and `min_so_far = min(num, min_so_far * num)`.
3. Track the overall answer as the running maximum of `max_so_far` across all indices.

**Time Complexity:** O(n) — a single pass through the array.
**Space Complexity:** O(1) extra space.

## Reference Solution (Python)

```python
def max_product(nums: list[int]) -> int:
    result = nums[0]
    max_so_far = nums[0]
    min_so_far = nums[0]

    for num in nums[1:]:
        if num < 0:
            max_so_far, min_so_far = min_so_far, max_so_far

        max_so_far = max(num, max_so_far * num)
        min_so_far = min(num, min_so_far * num)

        result = max(result, max_so_far)

    return result
```

## Follow-up Questions Interviewers May Ask

- How would you also return the actual subarray (start/end indices), not just the product?
- How does the presence of zeros in the array affect your approach?
- Can you adapt this idea to find the maximum product of a **subsequence** (not necessarily contiguous) instead?
