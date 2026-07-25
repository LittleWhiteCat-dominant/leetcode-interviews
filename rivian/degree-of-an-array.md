# 697. Degree of an Array

**Difficulty:** Easy
**Topics:** Array, Hash Table
**Reported at Rivian:** Tracked in Rivian's known coding question bank (CodeJeet).

## Problem Description

Given a non-empty array of non-negative integers `nums`, the **degree** of this array is defined as the maximum frequency of any one of its elements.

Your task is to find the smallest possible length of a (contiguous) subarray of `nums`, that has the same degree as `nums`.

## Example 1

```
Input: nums = [1,2,2,3,1]
Output: 2
Explanation:
The input array has a degree of 2 because both elements 1 and 2 appear twice.
Of the subarrays that have the same degree:
[1, 2, 2, 3, 1], [1, 2, 2, 3], [2, 2, 3, 1], [1, 2, 2], [2, 2, 3], [2, 2]
The shortest length is 2. So return 2.
```

## Example 2

```
Input: nums = [1,2,2,3,1,4,2]
Output: 6
```

## Constraints

- `nums.length` will be between 1 and 50,000.
- `nums[i]` will be an integer between 0 and 49,999.

## Approach

1. First pass: build a frequency count for every value, and track the **first** and **last** index at which each value occurs.
2. The array's degree is the maximum frequency found.
3. For every value whose frequency equals the degree, the candidate subarray spans from its first occurrence to its last occurrence — its length is `last_index - first_index + 1`.
4. The answer is the minimum such length among all values that achieve the maximum degree.

**Time Complexity:** O(n) — one pass to build the maps, one pass over the distinct values.
**Space Complexity:** O(n) for the count/first/last hash maps.

## Reference Solution (Python)

```python
def find_shortest_subarray(nums: list[int]) -> int:
    first_index: dict[int, int] = {}
    count: dict[int, int] = {}

    for i, num in enumerate(nums):
        if num not in first_index:
            first_index[num] = i
        count[num] = count.get(num, 0) + 1

    degree = max(count.values())
    shortest = len(nums)

    for num, freq in count.items():
        if freq == degree:
            # Iterate to find the last index for this value.
            last_index = max(i for i, n in enumerate(nums) if n == num)
            shortest = min(shortest, last_index - first_index[num] + 1)

    return shortest
```

> Note: the reference solution above recomputes the last index with an O(n) scan per candidate for clarity; a more optimal O(n) single-pass solution tracks `last_index` incrementally in the first loop as well.

## Follow-up Questions Interviewers May Ask

- Can you compute the answer in a single pass instead of two/three passes?
- How would you handle a streaming array where you must answer the query after each new element arrives?
