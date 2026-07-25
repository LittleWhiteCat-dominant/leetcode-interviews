# 217. Contains Duplicate

**Difficulty:** Easy
**Topics:** Array, Hash Table, Sorting
**Category warm-up for:** Hash Table

## Problem Description

Given an integer array `nums`, return `true` *if any value appears **at least twice** in the array, and return* `false` *if every element is distinct*.

## Example 1

```
Input: nums = [1,2,3,1]
Output: true
```

## Example 2

```
Input: nums = [1,2,3,4]
Output: false
```

## Example 3

```
Input: nums = [1,1,1,3,3,4,3,2,4,2]
Output: true
```

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^9 <= nums[i] <= 10^9`

## Approach

1. **Optimal — hash set:** iterate through `nums`, checking whether the current value already exists in a hash set. If it does, return `True` immediately. Otherwise, add it to the set and continue. If the loop finishes without finding a duplicate, return `False`.
2. **Alternative — sorting:** sort the array, then check whether any two adjacent elements are equal. Simpler to reason about, but O(n log n) instead of O(n), and it also mutates the input order (or requires a copy).
3. **One-liner alternative:** compare `len(nums) == len(set(nums))` — if the set (which removes duplicates) is smaller than the original list, a duplicate must exist. Concise, but does an unnecessary full pass if you only needed to short-circuit early.

**Time Complexity:** O(n) with the hash set approach; O(n log n) with sorting.
**Space Complexity:** O(n) for the hash set; O(1) extra for the sorting approach (in-place sort, excluding the sort's own overhead).

## Reference Solution (Python)

```python
def contains_duplicate(nums: list[int]) -> bool:
    seen: set[int] = set()

    for num in nums:
        if num in seen:
            return True
        seen.add(num)

    return False
```

## Follow-up Questions Interviewers May Ask

- How would you solve **Contains Duplicate II** (LC 219), where duplicates only count if they're within `k` indices of each other?
- How would you find the **actual duplicate value(s)**, not just whether one exists?
- How would you solve this with O(1) extra space if the array values are guaranteed to be within `[0, n-1]` (in-place marking, see LC 287, Find the Duplicate Number)?
