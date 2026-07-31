# 15. 3Sum

**Difficulty:** Medium
**Topics:** Array, Two Pointers, Sorting
**Common companies:** All big tech
**Category (README):** 1.1 Two Pointers

## Problem Description

Given an integer array nums, return all the triplets `[nums[i], nums[j], nums[k]]` such that `i != j`, `i != k`, and `j != k`, and `nums[i] + nums[j] + nums[k] == 0`.

Notice that the solution set must not contain duplicate triplets.

 

**Example 1:**

```

**Input:** nums = [-1,0,1,2,-1,-4]
**Output:** [[-1,-1,2],[-1,0,1]]
**Explanation:** 
nums[0] + nums[1] + nums[2] = (-1) + 0 + 1 = 0.
nums[1] + nums[2] + nums[4] = 0 + 1 + (-1) = 0.
nums[0] + nums[3] + nums[4] = (-1) + 2 + (-1) = 0.
The distinct triplets are [-1,0,1] and [-1,-1,2].
Notice that the order of the output and the order of the triplets does not matter.

```

**Example 2:**

```

**Input:** nums = [0,1,1]
**Output:** []
**Explanation:** The only possible triplet does not sum up to 0.

```

**Example 3:**

```

**Input:** nums = [0,0,0]
**Output:** [[0,0,0]]
**Explanation:** The only possible triplet sums up to 0.

```

 

**Constraints:**

	
- `3 <= nums.length <= 3000`

	
- `-105 <= nums[i] <= 105`

## Key Idea

Sort + fix one number + two pointers with dedup

## Approach

This is solved with **sorting plus a fixed-pointer two-pointer sweep**:

1. Sort `nums` so duplicates are adjacent and the array can be scanned with two pointers.
2. Fix the smallest number of each triplet at index `i`, skipping `i` if it repeats the previous value (avoids duplicate triplets) and breaking early once `nums[i] > 0` (no negative pairing can bring the sum back to zero).
3. For the remainder of the array, use `left = i + 1` and `right = n - 1` pointers: move `left` right if the sum is too small, move `right` left if the sum is too large.
4. When `nums[i] + nums[left] + nums[right] == 0`, record the triplet, then advance both pointers past any duplicate values before continuing.

**Time Complexity:** O(n^2) — sorting takes O(n log n), then fixing one number and scanning with two pointers takes O(n) for each of the n numbers.
**Space Complexity:** O(1) extra space beyond the output (not counting the O(log n) to O(n) space used by the sort itself).

## Reference Solution (Python)

```python
def threeSum(nums: list[int]) -> list[list[int]]:
    nums.sort()
    n = len(nums)
    result = []

    for i in range(n - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        if nums[i] > 0:
            break

        left, right = i + 1, n - 1
        while left < right:
            total = nums[i] + nums[left] + nums[right]
            if total < 0:
                left += 1
            elif total > 0:
                right -= 1
            else:
                result.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1

    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/3sum/
