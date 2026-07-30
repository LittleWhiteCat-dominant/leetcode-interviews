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

1. Identify the core pattern for this category: **1.5 Intervals**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
