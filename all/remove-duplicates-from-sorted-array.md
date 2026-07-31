# 26. Remove Duplicates from Sorted Array

**Difficulty:** Easy
**Topics:** Array, Two Pointers
**Common companies:** Amazon, Apple
**Category (README):** 1.1 Two Pointers

## Problem Description

Given an integer array `nums` sorted in **non-decreasing order**, remove the duplicates **in-place** such that each unique element appears only **once**. The **relative order** of the elements should be kept the **same**.

Consider the number of *unique elements* in `nums` to be `k**​​​​​​​**`​​​​​​​. After removing duplicates, return the number of unique elements `k`.

The first `k` elements of `nums` should contain the unique numbers in **sorted order**. The remaining elements beyond index `k - 1` can be ignored.

**Custom Judge:**

The judge will test your solution with the following code:

```

int[] nums = [...]; // Input array
int[] expectedNums = [...]; // The expected answer with correct length

int k = removeDuplicates(nums); // Calls your implementation

assert k == expectedNums.length;
for (int i = 0; i < k; i++) {
    assert nums[i] == expectedNums[i];
}

```

If all assertions pass, then your solution will be **accepted**.

 

**Example 1:**

```

**Input:** nums = [1,1,2]
**Output:** 2, nums = [1,2,_]
**Explanation:** Your function should return k = 2, with the first two elements of nums being 1 and 2 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).

```

**Example 2:**

```

**Input:** nums = [0,0,1,1,1,2,2,3,3,4]
**Output:** 5, nums = [0,1,2,3,4,_,_,_,_,_]
**Explanation:** Your function should return k = 5, with the first five elements of nums being 0, 1, 2, 3, and 4 respectively.
It does not matter what you leave beyond the returned k (hence they are underscores).

```

 

**Constraints:**

	
- `1 <= nums.length <= 3 * 104`

	
- `-100 <= nums[i] <= 100`

	
- `nums` is sorted in **non-decreasing** order.

## Key Idea

Fast/slow pointers overwriting in place

## Approach

This is solved with **fast/slow pointers overwriting duplicates in place**:

1. Since `nums` is sorted, all duplicates of a value are adjacent, so `slow` can track the end of the unique-elements-so-far region.
2. `slow` starts at index 0 (the first element is trivially unique); `fast` scans ahead from index 1.
3. Whenever `nums[fast] != nums[slow]`, a new unique value has been found: advance `slow` by one and copy `nums[fast]` into `nums[slow]`.
4. If `nums[fast] == nums[slow]`, it's a duplicate, so just advance `fast` without touching `slow`.
5. After `fast` finishes scanning the array, `slow + 1` is the count of unique elements, and `nums[0..slow]` holds them in sorted order.

**Time Complexity:** O(n) — a single pass with the fast pointer.
**Space Complexity:** O(1) — overwrites `nums` in place.

## Reference Solution (Python)

```python
from typing import List


def removeDuplicates(nums: List[int]) -> int:
    if not nums:
        return 0

    slow = 0
    for fast in range(1, len(nums)):
        if nums[fast] != nums[slow]:
            slow += 1
            nums[slow] = nums[fast]

    return slow + 1
```

## Reference

- LeetCode: https://leetcode.com/problems/remove-duplicates-from-sorted-array/
