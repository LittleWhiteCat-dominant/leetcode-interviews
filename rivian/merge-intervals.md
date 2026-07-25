# 56. Merge Intervals

**Difficulty:** Medium
**Topics:** Array, Sorting
**Reported at Rivian:** Confirmed — tracked in Rivian's known coding question bank.

## Problem Description

Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return *an array of the non-overlapping intervals that cover all the intervals in the input*.

## Example 1

```
Input: intervals = [[1,3],[2,6],[8,10],[15,18]]
Output: [[1,6],[8,10],[15,18]]
Explanation: Since intervals [1,3] and [2,6] overlap, merge them into [1,6].
```

## Example 2

```
Input: intervals = [[1,4],[4,5]]
Output: [[1,5]]
Explanation: Intervals [1,4] and [4,5] are considered overlapping.
```

## Constraints

- `1 <= intervals.length <= 10^4`
- `intervals[i].length == 2`
- `0 <= start_i <= end_i <= 10^4`

## Approach

1. **Sort** the intervals by their start value. After sorting, any intervals that need merging will be adjacent to each other.
2. Iterate through the sorted intervals, maintaining a `merged` result list.
   - If the current interval's start is `<=` the end of the last merged interval, they overlap — extend the last merged interval's end to `max(last.end, current.end)`.
   - Otherwise, append the current interval as a new entry.
3. Return the `merged` list.

**Time Complexity:** O(n log n) dominated by the sort.
**Space Complexity:** O(n) for the output (O(log n) or O(n) extra for the sort, depending on the implementation).

## Reference Solution (Python)

```python
def merge(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []

    intervals.sort(key=lambda interval: interval[0])
    merged: list[list[int]] = [intervals[0]]

    for start, end in intervals[1:]:
        last_start, last_end = merged[-1]
        if start <= last_end:
            merged[-1][1] = max(last_end, end)
        else:
            merged.append([start, end])

    return merged
```

## Follow-up Questions Interviewers May Ask

- How would you handle streaming intervals that arrive one at a time (insert interval into an already-merged list, see LC 57)?
- How would you extend this to support removing an interval?
- Can you solve this without sorting if the intervals are guaranteed to already be sorted?
