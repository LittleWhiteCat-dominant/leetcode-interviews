# 295. Find Median from Data Stream

**Difficulty:** Hard
**Topics:** Two Pointers, Design, Sorting, Heap (Priority Queue), Data Stream
**Common companies:** All big tech
**Category (README):** 8. Heap / Priority Queue

## Problem Description

The **median** is the middle value in an ordered integer list. If the size of the list is even, there is no middle value, and the median is the mean of the two middle values.

	
- For example, for `arr = [2,3,4]`, the median is `3`.

	
- For example, for `arr = [2,3]`, the median is `(2 + 3) / 2 = 2.5`.

Implement the MedianFinder class:

	
- `MedianFinder()` initializes the `MedianFinder` object.

	
- `void addNum(int num)` adds the integer `num` from the data stream to the data structure.

	
- `double findMedian()` returns the median of all elements so far. Answers within `10-5` of the actual answer will be accepted.

 

**Example 1:**

```

**Input**
["MedianFinder", "addNum", "addNum", "findMedian", "addNum", "findMedian"]
[[], [1], [2], [], [3], []]
**Output**
[null, null, null, 1.5, null, 2.0]

**Explanation**
MedianFinder medianFinder = new MedianFinder();
medianFinder.addNum(1);    // arr = [1]
medianFinder.addNum(2);    // arr = [1, 2]
medianFinder.findMedian(); // return 1.5 (i.e., (1 + 2) / 2)
medianFinder.addNum(3);    // arr[1, 2, 3]
medianFinder.findMedian(); // return 2.0

```

 

**Constraints:**

	
- `-105 <= num <= 105`

	
- There will be at least one element in the data structure before calling `findMedian`.

	
- At most `5 * 104` calls will be made to `addNum` and `findMedian`.

 

**Follow up:**

	
- If all integer numbers from the stream are in the range `[0, 100]`, how would you optimize your solution?

	
- If `99%` of all integer numbers from the stream are in the range `[0, 100]`, how would you optimize your solution?

## Key Idea

Max-heap (left half) + min-heap (right half)

## Approach

This is solved with **two heaps that split the stream into a smaller half and a larger half**:

1. Keep a max-heap `small` (values negated) holding the lower half of numbers seen so far, and a min-heap `large` holding the upper half.
2. On `addNum`, always push the new value into `small` first, then move `small`'s largest element over to `large` to keep everything correctly partitioned.
3. If `large` ends up bigger than `small`, move its smallest element back to `small` so `small` never has fewer elements than `large`.
4. On `findMedian`, if `small` has one extra element it alone holds the median; otherwise the median is the average of the two heaps' tops.

**Time Complexity:** O(log n) per `addNum` (heap push/pop), O(1) per `findMedian`.
**Space Complexity:** O(n) — both heaps together hold all inserted numbers.

## Reference Solution (Python)

```python
import heapq


class MedianFinder:
    def __init__(self):
        self.small: list[int] = []  # max-heap (values negated), holds the smaller half
        self.large: list[int] = []  # min-heap, holds the larger half

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -num)
        heapq.heappush(self.large, -heapq.heappop(self.small))

        if len(self.large) > len(self.small):
            heapq.heappush(self.small, -heapq.heappop(self.large))

    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -self.small[0]
        return (-self.small[0] + self.large[0]) / 2.0
```

## Reference

- LeetCode: https://leetcode.com/problems/find-median-from-data-stream/
