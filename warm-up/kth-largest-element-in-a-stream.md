# 703. Kth Largest Element in a Stream

**Difficulty:** Easy
**Topics:** Heap (Priority Queue), Design, Sorting
**Category warm-up for:** Heap / Priority Queue

## Problem Description

Design a class to find the `k`th largest element in a stream. Note that it is the `k`th largest element in the sorted order, not the `k`th distinct element.

Implement `KthLargest` class:

- `KthLargest(int k, int[] nums)` Initializes the object with the integer `k` and the stream of integers `nums`.
- `int add(int val)` Appends the integer `val` to the stream and returns the element representing the `k`th largest element in the stream.

## Example

```
Input:
["KthLargest", "add", "add", "add", "add", "add"]
[[3, [4, 5, 8, 2]], [3], [5], [10], [9], [4]]

Output:
[null, 4, 5, 5, 8, 8]

Explanation:
KthLargest kthLargest = new KthLargest(3, [4, 5, 8, 2]);
kthLargest.add(3);  // return 4
kthLargest.add(5);  // return 5
kthLargest.add(10); // return 5
kthLargest.add(9);  // return 8
kthLargest.add(4);  // return 8
```

## Constraints

- `1 <= k <= 10^4`
- `0 <= nums.length <= 10^4`
- `-10^4 <= nums[i] <= 10^4`
- `-10^4 <= val <= 10^4`
- At most `10^4` calls will be made to `add`.
- It is guaranteed that there will be at least `k` elements in the array when you search for the `k`th element.

## Approach

1. Maintain a **min-heap of size at most `k`** containing the `k` largest elements seen so far.
2. On initialization, push all of `nums` into the heap one at a time, popping whenever the heap size exceeds `k`.
3. On `add(val)`, push `val` into the heap, then pop if the size exceeds `k`.
4. After each `add`, the top of the min-heap (the smallest of the `k` largest elements) *is* the `k`th largest element overall — return it.

This is efficient because the heap never grows beyond size `k`, regardless of how many elements are added over the life of the stream.

**Time Complexity:** O(log k) per `add` call; O(n log k) for the initial construction from `nums`.
**Space Complexity:** O(k) for the heap.

## Reference Solution (Python)

```python
import heapq


class KthLargest:
    def __init__(self, k: int, nums: list[int]):
        self.k = k
        self.heap: list[int] = []
        for num in nums:
            self.add(num)

    def add(self, val: int) -> int:
        heapq.heappush(self.heap, val)
        if len(self.heap) > self.k:
            heapq.heappop(self.heap)
        return self.heap[0]
```

## Follow-up Questions Interviewers May Ask

- How would you solve the static, non-streaming version — **Kth Largest Element in an Array** (LC 215) — using Quickselect instead?
- How would you support **removing** an element from the stream as well as adding one?
- How would you extend this to track the `k` largest elements **per category/group** within a single stream?
