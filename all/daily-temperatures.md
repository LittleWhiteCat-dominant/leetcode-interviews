# 739. Daily Temperatures

**Difficulty:** Medium
**Topics:** Array, Stack, Monotonic Stack
**Common companies:** Amazon, Google
**Category (README):** 4.2 Monotonic Stack

## Problem Description

Given an array of integers `temperatures` represents the daily temperatures, return *an array* `answer` *such that* `answer[i]` *is the number of days you have to wait after the* `ith` *day to get a warmer temperature*. If there is no future day for which this is possible, keep `answer[i] == 0` instead.

 

**Example 1:**

```
**Input:** temperatures = [73,74,75,71,69,72,76,73]
**Output:** [1,1,4,2,1,1,0,0]

```

**Example 2:**

```
**Input:** temperatures = [30,40,50,60]
**Output:** [1,1,1,0]

```

**Example 3:**

```
**Input:** temperatures = [30,60,90]
**Output:** [1,1,0]

```

 

**Constraints:**

	
- `1 <= temperatures.length <= 105`

	
- `30 <= temperatures[i] <= 100`

## Key Idea

Monotonically decreasing stack to find the next greater element

## Approach

This is solved with **a monotonically decreasing stack of pending indices**:

1. Keep a stack of indices whose "warmer day" hasn't been found yet; the temperatures at these indices are strictly decreasing from bottom to top.
2. For each new index `i`, while the stack is non-empty and the temperature at the top of the stack is colder than `temperatures[i]`, pop that index and set `answer[popped] = i - popped`, since `i` is its first warmer day.
3. Push the current index `i` onto the stack, since its warmer day is still unknown.
4. Any indices left on the stack at the end never found a warmer day, so their `answer` entries correctly stay at the initialized 0.

**Time Complexity:** O(n) — each index is pushed and popped from the stack at most once.
**Space Complexity:** O(n) — the monotonic stack can hold up to n indices in the worst case.

## Reference Solution (Python)

```python
def dailyTemperatures(temperatures: list[int]) -> list[int]:
    answer = [0] * len(temperatures)
    stack: list[int] = []  # indices with strictly decreasing temperatures

    for i, temp in enumerate(temperatures):
        while stack and temperatures[stack[-1]] < temp:
            prev = stack.pop()
            answer[prev] = i - prev
        stack.append(i)

    return answer
```

## Reference

- LeetCode: https://leetcode.com/problems/daily-temperatures/
