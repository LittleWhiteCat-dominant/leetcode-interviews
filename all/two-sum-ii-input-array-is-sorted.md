# 167. Two Sum II - Input Array Is Sorted

**Difficulty:** Medium
**Topics:** Array, Two Pointers, Binary Search
**Common companies:** Amazon, Google
**Category (README):** 1.1 Two Pointers

## Problem Description

Given a **1-indexed** array of integers `numbers` that is already ***sorted in non-decreasing order***, find two numbers such that they add up to a specific `target` number. Let these two numbers be `numbers[index1]` and `numbers[index2]` where `1 <= index1 < index2 <= numbers.length`.

Return* the indices of the two numbers *`index1`* and *`index2`*, **each incremented by one,** as an integer array *`[index1, index2]`* of length 2.*

The tests are generated such that there is **exactly one solution**. You **may not** use the same element twice.

Your solution must use only constant extra space.

 

**Example 1:**

```

**Input:** numbers = [2,7,11,15], target = 9
**Output:** [1,2]
**Explanation:** The sum of 2 and 7 is 9. Therefore, index1 = 1, index2 = 2. We return [1, 2].

```

**Example 2:**

```

**Input:** numbers = [2,3,4], target = 6
**Output:** [1,3]
**Explanation:** The sum of 2 and 4 is 6. Therefore index1 = 1, index2 = 3. We return [1, 3].

```

**Example 3:**

```

**Input:** numbers = [-1,0], target = -1
**Output:** [1,2]
**Explanation:** The sum of -1 and 0 is -1. Therefore index1 = 1, index2 = 2. We return [1, 2].

```

 

**Constraints:**

	
- `2 <= numbers.length <= 3 * 104`

	
- `-1000 <= numbers[i] <= 1000`

	
- `numbers` is sorted in **non-decreasing order**.

	
- `-1000 <= target <= 1000`

	
- The tests are generated such that there is **exactly one solution**.

## Key Idea

Left/right pointers instead of a hash map, O(1) space

## Approach

1. Identify the core pattern for this category: **1.1 Two Pointers**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — the two pointers together traverse the array at most once.
**Space Complexity:** O(1) — only the two pointer indices are used, no extra data structures.

## Reference Solution (Python)

```python
def twoSum(numbers: list[int], target: int) -> list[int]:
    left, right = 0, len(numbers) - 1

    while left < right:
        current_sum = numbers[left] + numbers[right]
        if current_sum == target:
            return [left + 1, right + 1]
        if current_sum < target:
            left += 1
        else:
            right -= 1

    return []
```

## Reference

- LeetCode: https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/
