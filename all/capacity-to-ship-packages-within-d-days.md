# 1011. Capacity To Ship Packages Within D Days

**Difficulty:** Medium
**Topics:** Array, Binary Search
**Common companies:** Amazon
**Category (README):** 1.4 Binary Search

## Problem Description

A conveyor belt has packages that must be shipped from one port to another within `days` days.

The `ith` package on the conveyor belt has a weight of `weights[i]`. Each day, we load the ship with packages on the conveyor belt (in the order given by `weights`). We may not load more weight than the maximum weight capacity of the ship.

Return the least weight capacity of the ship that will result in all the packages on the conveyor belt being shipped within `days` days.

 

**Example 1:**

```

**Input:** weights = [1,2,3,4,5,6,7,8,9,10], days = 5
**Output:** 15
**Explanation:** A ship capacity of 15 is the minimum to ship all the packages in 5 days like this:
1st day: 1, 2, 3, 4, 5
2nd day: 6, 7
3rd day: 8
4th day: 9
5th day: 10

Note that the cargo must be shipped in the order given, so using a ship of capacity 14 and splitting the packages into parts like (2, 3, 4, 5), (1, 6, 7), (8), (9), (10) is not allowed.

```

**Example 2:**

```

**Input:** weights = [3,2,2,4,1,4], days = 3
**Output:** 6
**Explanation:** A ship capacity of 6 is the minimum to ship all the packages in 3 days like this:
1st day: 3, 2
2nd day: 2, 4
3rd day: 1, 4

```

**Example 3:**

```

**Input:** weights = [1,2,3,1,1], days = 4
**Output:** 3
**Explanation:**
1st day: 1
2nd day: 2
3rd day: 3
4th day: 1, 1

```

 

**Constraints:**

	
- `1 <= days <= weights.length <= 5 * 104`

	
- `1 <= weights[i] <= 500`

## Key Idea

Binary search on the answer

## Approach

This is solved with **binary search over the answer (the ship capacity), guided by a greedy feasibility check**:

1. Notice that "days needed" is monotonic in capacity: a larger ship capacity can only ship everything in the same number of days or fewer, so binary search applies.
2. Set the search bounds to `left = max(weights)` (must fit the heaviest package) and `right = sum(weights)` (one day for everything).
3. Write a `days_needed(capacity)` helper that greedily loads packages onto the current day until adding the next one would exceed `capacity`, then starts a new day.
4. Binary search on capacity: if `days_needed(mid) <= days`, `mid` is feasible, so search the lower half (`right = mid`); otherwise search the upper half (`left = mid + 1`).
5. The loop converges to the smallest feasible capacity, returned as `left`.

**Time Complexity:** O(n log(sum(weights))) — binary search over the capacity range, with an O(n) feasibility check at each step.
**Space Complexity:** O(1) extra space.

## Reference Solution (Python)

```python
def shipWithinDays(weights: list[int], days: int) -> int:
    def days_needed(capacity: int) -> int:
        required_days = 1
        current_load = 0
        for weight in weights:
            if current_load + weight > capacity:
                required_days += 1
                current_load = 0
            current_load += weight
        return required_days

    left, right = max(weights), sum(weights)

    while left < right:
        mid = (left + right) // 2
        if days_needed(mid) <= days:
            right = mid
        else:
            left = mid + 1

    return left
```

## Reference

- LeetCode: https://leetcode.com/problems/capacity-to-ship-packages-within-d-days/
