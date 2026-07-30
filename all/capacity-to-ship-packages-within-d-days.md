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

1. Identify the core pattern for this category: **1.4 Binary Search**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
