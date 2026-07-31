# 252. Meeting Rooms

**Difficulty:** Easy (LeetCode Premium — statement not publicly available)
**Topics:** Array, Sorting
**Common companies:** All big tech
**Category (README):** 1.5 Intervals

## Problem Description

This is a Premium problem. View it on LeetCode: https://leetcode.com/problems/meeting-rooms/

## Key Idea

Sort + sweep line / min-heap

## Approach

This is solved with **sorting intervals by start time and checking each pair of consecutive meetings for overlap**:

1. Sort `intervals` by start time, so any overlap must occur between adjacent meetings in this order.
2. Iterate through the sorted intervals starting from the second one.
3. If the current meeting's start time is earlier than the previous meeting's end time, the two overlap, so return `False` immediately.
4. If no overlaps are found after checking all consecutive pairs, return `True`.

**Time Complexity:** O(n log n) — dominated by sorting the intervals by start time.
**Space Complexity:** O(1) extra — excluding the space used by the sort itself.

## Reference Solution (Python)

```python
def canAttendMeetings(intervals: list[list[int]]) -> bool:
    intervals.sort(key=lambda interval: interval[0])

    for i in range(1, len(intervals)):
        if intervals[i][0] < intervals[i - 1][1]:
            return False

    return True
```

## Reference

- LeetCode: https://leetcode.com/problems/meeting-rooms/
