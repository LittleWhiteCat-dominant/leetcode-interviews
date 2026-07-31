# 435. Non-overlapping Intervals

**Difficulty:** Medium
**Topics:** Array, Dynamic Programming, Greedy, Sorting
**Common companies:** Amazon, Google
**Category (README):** 1.5 Intervals

## Problem Description

Given an array of intervals `intervals` where `intervals[i] = [starti, endi]`, return *the minimum number of intervals you need to remove to make the rest of the intervals non-overlapping*.

**Note** that intervals which only touch at a point are **non-overlapping**. For example, `[1, 2]` and `[2, 3]` are non-overlapping.

 

**Example 1:**

```

**Input:** intervals = [[1,2],[2,3],[3,4],[1,3]]
**Output:** 1
**Explanation:** [1,3] can be removed and the rest of the intervals are non-overlapping.

```

**Example 2:**

```

**Input:** intervals = [[1,2],[1,2],[1,2]]
**Output:** 2
**Explanation:** You need to remove two [1,2] to make the rest of the intervals non-overlapping.

```

**Example 3:**

```

**Input:** intervals = [[1,2],[2,3]]
**Output:** 0
**Explanation:** You don't need to remove any of the intervals since they're already non-overlapping.

```

 

**Constraints:**

	
- `1 <= intervals.length <= 105`

	
- `intervals[i].length == 2`

	
- `-5 * 104 <= starti < endi <= 5 * 104`

## Key Idea

Sort by right endpoint, greedy selection

## Approach

This is solved with **greedy interval scheduling, sorting by end time**:

1. Sort all intervals by their end point, so the interval that finishes earliest is always considered first.
2. Track `prev_end`, the end time of the last interval kept (initialized to negative infinity).
3. Walk through the sorted intervals: if the current interval's start is at or after `prev_end`, it doesn't overlap with what's kept, so keep it and update `prev_end` to its end.
4. Otherwise, the current interval overlaps with the previously kept one; since intervals are sorted by end time, the previously kept interval always ends no later, so it's optimal to discard the current interval and increment a `removed` counter.
5. Return `removed`, the minimum number of intervals that must be removed to eliminate all overlaps.

**Time Complexity:** O(n log n) — dominated by sorting the intervals by end time; the greedy scan afterward is O(n).
**Space Complexity:** O(1) extra — aside from the space used by the sort.

## Reference Solution (Python)

```python
def eraseOverlapIntervals(intervals: list[list[int]]) -> int:
    intervals.sort(key=lambda interval: interval[1])
    removed = 0
    prev_end = float('-inf')

    for start, end in intervals:
        if start >= prev_end:
            prev_end = end
        else:
            removed += 1

    return removed
```

## Reference

- LeetCode: https://leetcode.com/problems/non-overlapping-intervals/
