# 253. Meeting Rooms II

**Difficulty:** Medium
**Topics:** Array, Two Pointers, Greedy, Sorting, Heap (Priority Queue)
**Reported at Asana:** Tracked in Asana's known coding question bank (InterviewSolver) — naturally aligned with Asana's own scheduling/collaboration product domain.

## Problem Description

Given an array of meeting time intervals `intervals` where `intervals[i] = [start_i, end_i]`, return *the minimum number of conference rooms required*.

## Example 1

```
Input: intervals = [[0,30],[5,10],[15,20]]
Output: 2
```

## Example 2

```
Input: intervals = [[7,10],[2,4]]
Output: 1
```

## Constraints

- `1 <= intervals.length <= 10^4`
- `0 <= start_i < end_i <= 10^6`

## Approach

**Approach A — Min-Heap of end times**
1. Sort the meetings by start time.
2. Use a min-heap to track the end times of meetings currently occupying a room.
3. For each meeting, if the earliest-ending meeting in the heap (the heap's top) ends at or before the current meeting's start time, that room is now free — pop it and reuse the room (pop then push).
4. Otherwise, a new room is needed — just push the new end time.
5. The maximum heap size ever reached (or simply the final heap size, since it only ever grows when a new room is needed) is the answer.

**Approach B — Two sorted arrays (chronological sweep)**
1. Separate all start times and all end times into two sorted arrays.
2. Use two pointers scanning through both arrays. Whenever a meeting starts before the earliest currently-active meeting ends, increment the room count; otherwise, a room frees up (advance the end pointer) and the room count doesn't need to increase.
3. Track the running maximum room count.

**Time Complexity:** O(n log n) for both approaches (dominated by sorting).
**Space Complexity:** O(n) for the heap or the sorted start/end arrays.

## Reference Solution (Python, Min-Heap)

```python
import heapq


def min_meeting_rooms(intervals: list[list[int]]) -> int:
    if not intervals:
        return 0

    intervals.sort(key=lambda interval: interval[0])
    end_times_heap: list[int] = []  # min-heap of end times for rooms in use

    for start, end in intervals:
        if end_times_heap and end_times_heap[0] <= start:
            heapq.heapreplace(end_times_heap, end)
        else:
            heapq.heappush(end_times_heap, end)

    return len(end_times_heap)
```

## Follow-up Questions Interviewers May Ask

- How would you also report which specific room each meeting is assigned to?
- How would you handle meetings that can be split or rescheduled to minimize the room count further?
- How would you support inserting new meetings dynamically and updating the room count incrementally?
