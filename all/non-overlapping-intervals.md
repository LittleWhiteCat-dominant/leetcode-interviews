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

1. Identify the core pattern for this category: **1.5 Intervals**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
