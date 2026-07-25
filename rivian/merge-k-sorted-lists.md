# 23. Merge k Sorted Lists

**Difficulty:** Hard
**Topics:** Linked List, Heap (Priority Queue), Divide and Conquer, Merge Sort
**Reported at Rivian:** Confirmed — tracked in Rivian's known coding question bank, typically for senior roles.

## Problem Description

You are given an array of `k` linked-lists `lists`, each linked-list is sorted in ascending order.

*Merge all the linked-lists into one sorted linked-list and return it.*

## Example 1

```
Input: lists = [[1,4,5],[1,3,4],[2,6]]
Output: [1,1,2,3,4,4,5,6]
Explanation: The linked-lists are:
[
  1->4->5,
  1->3->4,
  2->6
]
merging them into one sorted list:
1->1->2->3->4->4->5->6
```

## Example 2

```
Input: lists = []
Output: []
```

## Example 3

```
Input: lists = [[]]
Output: []
```

## Constraints

- `k == lists.length`
- `0 <= k <= 10^4`
- `0 <= lists[i].length <= 500`
- `-10^4 <= lists[i][j] <= 10^4`
- `lists[i]` is sorted in **ascending order**.
- The sum of `lists[i].length` will not exceed `10^4`.

## Approach

Two standard approaches:

**Approach A — Min-Heap**
1. Push the head node of every non-empty list into a min-heap, keyed by node value (with a tiebreaker index to avoid comparing `ListNode` objects directly).
2. Repeatedly pop the smallest node, append it to the result list, and if that node has a `next`, push `next` into the heap.
3. Continue until the heap is empty.

**Approach B — Divide and Conquer (pairwise merge)**
1. Recursively split the `k` lists in half, merge each half, then merge the two sorted halves together using the standard two-list merge (LC 21) — this mirrors merge sort.
2. This avoids maintaining a heap and is often considered a cleaner follow-up after solving with the heap approach.

**Time Complexity:**
- Heap approach: O(N log k), where N is the total number of nodes across all lists and k is the number of lists.
- Divide and conquer: O(N log k) as well, since there are O(log k) merge passes and each pass processes O(N) nodes total.

**Space Complexity:** O(k) for the heap approach (heap size), O(log k) recursion stack for divide and conquer.

## Reference Solution (Python, Min-Heap)

```python
import heapq


class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next


def merge_k_lists(lists: list["ListNode | None"]) -> "ListNode | None":
    heap: list[tuple[int, int, ListNode]] = []
    for i, node in enumerate(lists):
        if node:
            heapq.heappush(heap, (node.val, i, node))

    dummy = ListNode()
    tail = dummy

    while heap:
        val, i, node = heapq.heappop(heap)
        tail.next = node
        tail = tail.next
        if node.next:
            heapq.heappush(heap, (node.next.val, i, node.next))

    return dummy.next
```

## Follow-up Questions Interviewers May Ask

- Can you solve it without a heap, using divide and conquer instead? What's the trade-off?
- How would this scale if the lists were extremely long and stored across different machines (distributed merge)?
- How would you merge k sorted **arrays** instead of linked lists — does the approach change?
