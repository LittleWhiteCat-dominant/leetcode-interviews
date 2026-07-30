# 1235. Maximum Profit in Job Scheduling

**Difficulty:** Hard
**Topics:** Array, Binary Search, Dynamic Programming, Sorting
**Common companies:** Company list
**Category (README):** Company-Specific High-Frequency Lists

## Problem Description

We have `n` jobs, where every job is scheduled to be done from `startTime[i]` to `endTime[i]`, obtaining a profit of `profit[i]`.

You're given the `startTime`, `endTime` and `profit` arrays, return the maximum profit you can take such that there are no two jobs in the subset with overlapping time range.

If you choose a job that ends at time `X` you will be able to start another job that starts at time `X`.

 

**Example 1:**

****

```

**Input:** startTime = [1,2,3,3], endTime = [3,4,5,6], profit = [50,10,40,70]
**Output:** 120
**Explanation:** The subset chosen is the first and fourth job. 
Time range [1-3]+[3-6] , we get profit of 120 = 50 + 70.

```

**Example 2:**

** **

```

**Input:** startTime = [1,2,3,4,6], endTime = [3,5,10,6,9], profit = [20,20,100,70,60]
**Output:** 150
**Explanation:** The subset chosen is the first, fourth and fifth job. 
Profit obtained 150 = 20 + 70 + 60.

```

**Example 3:**

****

```

**Input:** startTime = [1,1,1], endTime = [2,3,4], profit = [5,6,4]
**Output:** 6

```

 

**Constraints:**

	
- `1 <= startTime.length == endTime.length == profit.length <= 5 * 104`

	
- `1 <= startTime[i] < endTime[i] <= 109`

	
- `1 <= profit[i] <= 104`

## Key Idea

See company-specific high-frequency lists.

## Approach

1. Identify the core pattern for this category: **Company-Specific High-Frequency Lists**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n log n) — for sorting jobs by end time and performing a binary search per job during the DP.
**Space Complexity:** O(n) — for the sorted jobs array and the DP array.

## Reference Solution (Python)

```python
from bisect import bisect_right


def jobScheduling(startTime: list[int], endTime: list[int], profit: list[int]) -> int:
    jobs = sorted(zip(endTime, startTime, profit))
    n = len(jobs)
    ends = [job[0] for job in jobs]
    dp = [0] * (n + 1)

    for i in range(1, n + 1):
        end, start, prof = jobs[i - 1]
        j = bisect_right(ends, start, 0, i - 1)
        dp[i] = max(dp[i - 1], dp[j] + prof)

    return dp[n]
```

## Reference

- LeetCode: https://leetcode.com/problems/maximum-profit-in-job-scheduling/
