# 239. Sliding Window Maximum

**Difficulty:** Hard
**Topics:** Array, Sliding Window, Monotonic Queue, Heap (Priority Queue)
**Reported at Asana:** Tracked in Asana's known coding question bank (InterviewSolver).

## Problem Description

You are given an array of integers `nums`, there is a sliding window of size `k` which is moving from the very left of the array to the very right. You can only see the `k` numbers in the window. Each time the sliding window moves right by one position.

Return *the max sliding window*.

## Example 1

```
Input: nums = [1,3,-1,-3,5,3,6,7], k = 3
Output: [3,3,5,5,6,7]
Explanation:
Window position                Max
---------------               -----
[1  3  -1] -3  5  3  6  7       3
 1 [3  -1  -3] 5  3  6  7       3
 1  3 [-1  -3  5] 3  6  7       5
 1  3  -1 [-3  5  3] 6  7       5
 1  3  -1  -3 [5  3  6] 7       6
 1  3  -1  -3  5 [3  6  7]      7
```

## Example 2

```
Input: nums = [1], k = 1
Output: [1]
```

## Constraints

- `1 <= nums.length <= 10^5`
- `-10^4 <= nums[i] <= 10^4`
- `1 <= k <= nums.length`

## Approach

Use a **monotonic decreasing deque** that stores indices (not values):

1. For each new index `i`, pop indices from the **back** of the deque while `nums[deque_back] <= nums[i]` — those elements can never be the maximum again since `nums[i]` is both later and at least as large.
2. Push `i` onto the back of the deque.
3. Pop the index at the **front** of the deque if it has fallen outside the current window (`front_index <= i - k`).
4. Once `i >= k - 1`, the front of the deque holds the index of the maximum for the current window — append `nums[front]` to the result.

Because each index is pushed and popped from the deque at most once, the total work across the whole array is linear.

**Time Complexity:** O(n) — amortized constant work per element.
**Space Complexity:** O(k) for the deque.

## Reference Solution (Python)

```python
from collections import deque


def max_sliding_window(nums: list[int], k: int) -> list[int]:
    dq: deque[int] = deque()  # stores indices, values are monotonically decreasing
    result: list[int] = []

    for i, num in enumerate(nums):
        while dq and nums[dq[-1]] <= num:
            dq.pop()
        dq.append(i)

        if dq[0] <= i - k:
            dq.popleft()

        if i >= k - 1:
            result.append(nums[dq[0]])

    return result
```

## Follow-up Questions Interviewers May Ask

- Can you solve this with a heap instead of a deque? What's the complexity difference (O(n log n) vs O(n))?
- How would you support a sliding window **minimum** as well?
- How would you handle a streaming input where you don't know the total length in advance?
