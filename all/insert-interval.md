# 57. Insert Interval

**Difficulty:** Medium
**Topics:** Array
**Common companies:** All big tech
**Category (README):** 1.5 Intervals

## Problem Description

You are given an array of non-overlapping intervals `intervals` where `intervals[i] = [starti, endi]` represent the start and the end of the `ith` interval and `intervals` is sorted in ascending order by `starti`. You are also given an interval `newInterval = [start, end]` that represents the start and end of another interval.

Two intervals are considered overlapping if they share **at least** one point.

Insert `newInterval` into `intervals` such that `intervals` is still sorted in ascending order by `starti` and `intervals` still does not have any overlapping intervals (merge overlapping intervals if necessary).

Return `intervals`* after the insertion*.

**Note** that you don't need to modify `intervals` in-place. You can make a new array and return it.

 

**Example 1:**

```

**Input:** intervals = [[1,3],[6,9]], newInterval = [2,5]
**Output:** [[1,5],[6,9]]

```

**Example 2:**

```

**Input:** intervals = [[1,2],[3,5],[6,7],[8,10],[12,16]], newInterval = [4,8]
**Output:** [[1,2],[3,10],[12,16]]
**Explanation:** Because the new interval [4,8] overlaps with [3,5],[6,7],[8,10].

```

 

**Constraints:**

	
- `0 <= intervals.length <= 104`

	
- `intervals[i].length == 2`

	
- `0 <= starti <= endi <= 105`

	
- `intervals` is sorted by `starti` in **ascending** order.

	
- `newInterval.length == 2`

	
- `0 <= start <= end <= 105`

## Key Idea

Find the insertion point and merge overlapping intervals

## Approach

This is solved with **a single linear pass split into three phases: before, overlapping, and after**:

1. Append every interval that ends strictly before `newInterval` starts unchanged (they can't overlap).
2. While the current interval starts at or before `newInterval`'s end, merge it into `newInterval` by expanding its bounds: `start = min(start, intervals[i][0])`, `end = max(end, intervals[i][1])`.
3. Once no more intervals overlap, append the fully merged `[start, end]` to the result.
4. Append all remaining intervals unchanged (they start after the merged interval ends).

**Time Complexity:** O(n) — a single linear pass through the intervals.
**Space Complexity:** O(n) — for the result list (excluding the output, O(1) extra space).

## Reference Solution (Python)

```python
def insert(intervals: list[list[int]], newInterval: list[int]) -> list[list[int]]:
    result: list[list[int]] = []
    i, n = 0, len(intervals)
    start, end = newInterval

    while i < n and intervals[i][1] < start:
        result.append(intervals[i])
        i += 1

    while i < n and intervals[i][0] <= end:
        start = min(start, intervals[i][0])
        end = max(end, intervals[i][1])
        i += 1
    result.append([start, end])

    while i < n:
        result.append(intervals[i])
        i += 1

    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/insert-interval/
