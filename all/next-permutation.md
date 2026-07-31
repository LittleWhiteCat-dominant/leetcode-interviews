# 31. Next Permutation

**Difficulty:** Medium
**Topics:** Array, Two Pointers
**Common companies:** Company list
**Category (README):** Company-Specific High-Frequency Lists

## Problem Description

A **permutation** of an array of integers is an arrangement of its members into a sequence or linear order.

	
- For example, for `arr = [1,2,3]`, the following are all the permutations of `arr`: `[1,2,3], [1,3,2], [2, 1, 3], [2, 3, 1], [3,1,2], [3,2,1]`.

The **next permutation** of an array of integers is the next lexicographically greater permutation of its integer. More formally, if all the permutations of the array are sorted in one container according to their lexicographical order, then the **next permutation** of that array is the permutation that follows it in the sorted container. If such arrangement is not possible, the array must be rearranged as the lowest possible order (i.e., sorted in ascending order).

	
- For example, the next permutation of `arr = [1,2,3]` is `[1,3,2]`.

	
- Similarly, the next permutation of `arr = [2,3,1]` is `[3,1,2]`.

	
- While the next permutation of `arr = [3,2,1]` is `[1,2,3]` because `[3,2,1]` does not have a lexicographical larger rearrangement.

Given an array of integers `nums`, *find the next permutation of* `nums`.

The replacement must be **in place** and use only constant extra memory.

 

**Example 1:**

```

**Input:** nums = [1,2,3]
**Output:** [1,3,2]

```

**Example 2:**

```

**Input:** nums = [3,2,1]
**Output:** [1,2,3]

```

**Example 3:**

```

**Input:** nums = [1,1,5]
**Output:** [1,5,1]

```

 

**Constraints:**

	
- `1 <= nums.length <= 100`

	
- `0 <= nums[i] <= 100`

## Key Idea

See company-specific high-frequency lists.

## Approach

This is solved with **a pivot scan followed by a swap and reversal**:

1. Scan from the right to find the first index `i` where `nums[i] < nums[i + 1]` — this is the "pivot", the rightmost position where the sequence can still be increased. If no such index exists, the array is fully descending (the last permutation), so skip straight to step 4.
2. Scan from the right again to find the rightmost index `j > i` where `nums[j] > nums[i]` — the smallest value that is still larger than `nums[i]`, guaranteed to exist since `nums[i + 1] > nums[i]`.
3. Swap `nums[i]` and `nums[j]`, which makes the prefix up to `i` the smallest possible increase.
4. Reverse the suffix after index `i` to put it in ascending order, which is the smallest possible arrangement for that suffix — this yields the very next lexicographic permutation (or, if no pivot was found in step 1, sorts the whole array ascending, wrapping around to the first permutation).

**Time Complexity:** O(n) — the pivot scan, the successor scan, and the final reversal are each linear.
**Space Complexity:** O(1) — the array is rearranged in place.

## Reference Solution (Python)

```python
def nextPermutation(nums: list[int]) -> None:
    n = len(nums)
    i = n - 2
    while i >= 0 and nums[i] >= nums[i + 1]:
        i -= 1

    if i >= 0:
        j = n - 1
        while nums[j] <= nums[i]:
            j -= 1
        nums[i], nums[j] = nums[j], nums[i]

    nums[i + 1:] = reversed(nums[i + 1:])
```

## Reference

- LeetCode: https://leetcode.com/problems/next-permutation/
