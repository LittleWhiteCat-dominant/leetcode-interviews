# 238. Product of Array Except Self

**Difficulty:** Medium
**Topics:** Array, Prefix Sum
**Reported at Asana:** Confirmed — reported in multiple candidate interviews within the last 6 months, both as a coding-round and phone-screen question.

## Problem Description

Given an integer array `nums`, return *an array* `answer` *such that* `answer[i]` *is equal to the product of all the elements of* `nums` *except* `nums[i]`.

The product of any prefix or suffix of `nums` is **guaranteed** to fit in a **32-bit** integer.

You must write an algorithm that runs in `O(n)` time and without using the division operation.

## Example 1

```
Input: nums = [1,2,3,4]
Output: [24,12,8,6]
```

## Example 2

```
Input: nums = [-1,1,0,-3,3]
Output: [0,0,9,0,0]
```

## Constraints

- `2 <= nums.length <= 10^5`
- `-30 <= nums[i] <= 30`
- The input is generated such that `answer[i]` is guaranteed to fit in a 32-bit integer.

## Approach

1. `answer[i]` is the product of everything to the **left** of `i` multiplied by everything to the **right** of `i`.
2. Compute a `prefix` array where `prefix[i]` is the product of all elements before index `i`.
3. Compute a `suffix` value on the fly while scanning from the right, multiplying it into the result as you go, to avoid allocating a second full array (achieving O(1) extra space excluding the output).
4. Combine: `answer[i] = prefix[i] * suffix[i]`.

**Time Complexity:** O(n) — two passes over the array.
**Space Complexity:** O(1) extra space (excluding the output array), since the suffix product is tracked with a single running variable.

## Reference Solution (Python)

```python
def product_except_self(nums: list[int]) -> list[int]:
    n = len(nums)
    answer = [1] * n

    prefix = 1
    for i in range(n):
        answer[i] = prefix
        prefix *= nums[i]

    suffix = 1
    for i in range(n - 1, -1, -1):
        answer[i] *= suffix
        suffix *= nums[i]

    return answer
```

## Follow-up Questions Interviewers May Ask

- What would you do if division **were** allowed — how does the edge case of zeros in the array complicate that approach?
- Can you solve this with O(1) extra space (not counting the output array)? (The solution above already does.)
- How would you handle multiple zeros in the input array?
