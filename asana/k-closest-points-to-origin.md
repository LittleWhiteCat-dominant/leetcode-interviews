# 973. K Closest Points to Origin

**Difficulty:** Medium
**Topics:** Array, Math, Divide and Conquer, Geometry, Sorting, Heap (Priority Queue), Quickselect
**Reported at Asana:** Confirmed — reported in multiple candidate interviews within the last 6 months.

## Problem Description

Given an array of `points` where `points[i] = [x_i, y_i]` represents a point on the X-Y plane and an integer `k`, return the `k` closest points to the origin `(0, 0)`.

The distance between two points on the X-Y plane is the Euclidean distance (i.e., `sqrt((x1 - x2)^2 + (y1 - y2)^2)`).

You may return the answer in **any order**. The answer is **guaranteed** to be unique (except for the order that it is in).

## Example 1

```
Input: points = [[1,3],[-2,2]], k = 1
Output: [[-2,2]]
Explanation:
The distance between (1, 3) and the origin is sqrt(10).
The distance between (-2, 2) and the origin is sqrt(8).
Since sqrt(8) < sqrt(10), (-2, 2) is closer to the origin.
We only want the closest k = 1 points from the origin, so the answer is just [[-2,2]].
```

## Example 2

```
Input: points = [[3,3],[5,-1],[-2,4]], k = 2
Output: [[3,3],[-2,4]]
Explanation: The answer [[-2,4],[3,3]] would also be accepted.
```

## Constraints

- `1 <= k <= points.length <= 10^4`
- `-10^4 <= x_i, y_i <= 10^4`

## Approach

**Approach A — Max-Heap of size k**
1. Use squared distance (`x*x + y*y`) to avoid unnecessary `sqrt` calls, since it preserves relative ordering.
2. Maintain a max-heap of size `k`. Push each point's `(negated distance, point)` (Python's `heapq` is a min-heap, so negate to simulate a max-heap), and pop whenever the heap exceeds size `k`.
3. After processing all points, the heap holds the `k` closest points.

**Approach B — Quickselect**
1. Partition the array around a pivot distance, similar to finding the k-th smallest element.
2. Recurse only into the partition that contains the k-th position, achieving O(n) average time.

**Time Complexity:**
- Heap approach: O(n log k).
- Quickselect: O(n) average case, O(n²) worst case.

**Space Complexity:** O(k) for the heap approach, O(1) extra for quickselect (in-place, excluding recursion stack).

## Reference Solution (Python, Heap)

```python
import heapq


def k_closest(points: list[list[int]], k: int) -> list[list[int]]:
    heap: list[tuple[int, list[int]]] = []

    for x, y in points:
        dist_sq = x * x + y * y
        heapq.heappush(heap, (-dist_sq, [x, y]))
        if len(heap) > k:
            heapq.heappop(heap)

    return [point for _, point in heap]
```

## Follow-up Questions Interviewers May Ask

- How would you solve this with Quickselect instead of a heap, and what's the trade-off in worst-case complexity?
- How would you handle streaming points where `k` closest must be maintained online as new points arrive?
- What if the "origin" could be an arbitrary point instead of `(0, 0)`?
