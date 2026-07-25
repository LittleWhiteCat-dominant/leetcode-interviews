# 215. Kth Largest Element in an Array

**Difficulty:** Medium
**Topics:** Array, Sorting, Heap (Priority Queue), Quickselect, Divide and Conquer
**Reported at Rivian:** Confirmed — reported as a coding challenge question for the Software Engineer II (RIV-4) role.

## Problem Description

Given an integer array `nums` and an integer `k`, return *the* `k`*th largest element in the array*.

Note that it is the `k`th largest element in the **sorted order**, not the `k`th distinct element.

Can you solve it without sorting?

## Example 1

```
Input: nums = [3,2,1,5,6,4], k = 2
Output: 5
```

## Example 2

```
Input: nums = [3,2,3,1,2,4,5,5,6], k = 4
Output: 4
```

## Constraints

- `1 <= k <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`

## Approach

**Approach A — Min-Heap of size k**
1. Push elements onto a min-heap; whenever the heap size exceeds `k`, pop the smallest.
2. After processing all elements, the heap's top (minimum) is the k-th largest element.

**Approach B — Quickselect (average O(n))**
1. Use the partitioning idea from quicksort. Pick a pivot, partition the array so elements greater than the pivot are on one side and smaller on the other.
2. Determine which partition contains the k-th largest element based on the pivot's final index, and recurse only into that partition (discard the other side entirely).
3. This avoids fully sorting the array and achieves O(n) average time complexity.

**Time Complexity:**
- Heap approach: O(n log k).
- Quickselect: O(n) average case, O(n²) worst case (mitigated with random pivot selection).

**Space Complexity:** O(k) for the heap approach, O(1) extra (in-place) for quickselect (excluding recursion stack).

## Reference Solution (Python, Quickselect)

```python
import random


def find_kth_largest(nums: list[int], k: int) -> int:
    target_index = len(nums) - k  # Index of the k-th largest in sorted order.

    def partition(left: int, right: int) -> int:
        pivot_index = random.randint(left, right)
        pivot_value = nums[pivot_index]
        nums[pivot_index], nums[right] = nums[right], nums[pivot_index]

        store_index = left
        for i in range(left, right):
            if nums[i] < pivot_value:
                nums[store_index], nums[i] = nums[i], nums[store_index]
                store_index += 1

        nums[store_index], nums[right] = nums[right], nums[store_index]
        return store_index

    left, right = 0, len(nums) - 1
    while True:
        pivot_final_index = partition(left, right)
        if pivot_final_index == target_index:
            return nums[pivot_final_index]
        elif pivot_final_index < target_index:
            left = pivot_final_index + 1
        else:
            right = pivot_final_index - 1
```

## Follow-up Questions Interviewers May Ask

- How would you handle this for a continuous data stream instead of a static array (see LC 703, Kth Largest Element in a Stream)?
- What's the worst-case time complexity of Quickselect, and how does random pivot selection mitigate it?
- How would you find the k-th largest element across multiple machines (distributed top-k)?
