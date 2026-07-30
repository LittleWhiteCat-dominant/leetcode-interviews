# 933. Number of Recent Calls

**Difficulty:** Easy
**Topics:** Design, Queue, Data Stream
**Common companies:** Google
**Category (README):** 5. Queue / Monotonic Queue

## Problem Description

You have a `RecentCounter` class which counts the number of recent requests within a certain time frame.

Implement the `RecentCounter` class:

	
- `RecentCounter()` Initializes the counter with zero recent requests.

	
- `int ping(int t)` Adds a new request at time `t`, where `t` represents some time in milliseconds, and returns the number of requests that has happened in the past `3000` milliseconds (including the new request). Specifically, return the number of requests that have happened in the inclusive range `[t - 3000, t]`.

It is **guaranteed** that every call to `ping` uses a strictly larger value of `t` than the previous call.

 

**Example 1:**

```

**Input**
["RecentCounter", "ping", "ping", "ping", "ping"]
[[], [1], [100], [3001], [3002]]
**Output**
[null, 1, 2, 3, 3]

**Explanation**
RecentCounter recentCounter = new RecentCounter();
recentCounter.ping(1);     // requests = [1], range is [-2999,1], return 1
recentCounter.ping(100);   // requests = [1, 100], range is [-2900,100], return 2
recentCounter.ping(3001);  // requests = [1, 100, 3001], range is [1,3001], return 3
recentCounter.ping(3002);  // requests = [1, 100, 3001, 3002], range is [2,3002], return 3

```

 

**Constraints:**

	
- `1 <= t <= 109`

	
- Each test case will call `ping` with **strictly increasing** values of `t`.

	
- At most `104` calls will be made to `ping`.

## Key Idea

Monotonic queue / prefix sum optimization

## Approach

1. Identify the core pattern for this category: **5. Queue / Monotonic Queue**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(1) amortized per `ping` call — each request is pushed once and popped at most once across all calls.
**Space Complexity:** O(w) — where `w` is the number of requests within the 3000ms window currently stored in the queue.

## Reference Solution (Python)

```python
from collections import deque


class RecentCounter:
    def __init__(self) -> None:
        self.requests: deque[int] = deque()

    def ping(self, t: int) -> int:
        self.requests.append(t)
        while self.requests[0] < t - 3000:
            self.requests.popleft()
        return len(self.requests)
```

## Reference

- LeetCode: https://leetcode.com/problems/number-of-recent-calls/
