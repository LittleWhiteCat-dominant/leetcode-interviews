# 1046. Last Stone Weight

**Difficulty:** Easy
**Topics:** Array, Heap (Priority Queue)
**Common companies:** Amazon, Apple
**Category (README):** 8. Heap / Priority Queue

## Problem Description

You are given an array of integers `stones` where `stones[i]` is the weight of the `ith` stone.

We are playing a game with the stones. On each turn, we choose the **heaviest two stones** and smash them together. Suppose the heaviest two stones have weights `x` and `y` with `x <= y`. The result of this smash is:

	
- If `x == y`, both stones are destroyed, and

	
- If `x != y`, the stone of weight `x` is destroyed, and the stone of weight `y` has new weight `y - x`.

At the end of the game, there is **at most one** stone left.

Return *the weight of the last remaining stone*. If there are no stones left, return `0`.

 

**Example 1:**

```

**Input:** stones = [2,7,4,1,8,1]
**Output:** 1
**Explanation:** 
We combine 7 and 8 to get 1 so the array converts to [2,4,1,1,1] then,
we combine 2 and 4 to get 2 so the array converts to [2,1,1,1] then,
we combine 2 and 1 to get 1 so the array converts to [1,1,1] then,
we combine 1 and 1 to get 0 so the array converts to [1] then that's the value of the last stone.

```

**Example 2:**

```

**Input:** stones = [1]
**Output:** 1

```

 

**Constraints:**

	
- `1 <= stones.length <= 30`

	
- `1 <= stones[i] <= 1000`

## Key Idea

Max-heap, repeatedly pop the two largest and push back the difference

## Approach

This is solved with **a max-heap simulation using negated values** (since Python's `heapq` is a min-heap):

1. Negate every stone weight and heapify the list so the largest stone is always at the top.
2. While more than one stone remains, pop the two largest (negate back to get `y >= x`).
3. If the two weights differ, push the negated difference `y - x` back onto the heap as the new stone.
4. If they are equal, both stones are destroyed and nothing is pushed back.
5. Repeat until at most one stone is left; return its weight negated, or `0` if the heap is empty.

**Time Complexity:** O(n log n) — each of the up to n smashes performs two heap pops and at most one push, each O(log n).
**Space Complexity:** O(n) — for the heap storing the negated stone weights.

## Reference Solution (Python)

```python
import heapq


def lastStoneWeight(stones: list[int]) -> int:
    heap = [-s for s in stones]
    heapq.heapify(heap)

    while len(heap) > 1:
        y = -heapq.heappop(heap)
        x = -heapq.heappop(heap)
        if y != x:
            heapq.heappush(heap, -(y - x))

    return -heap[0] if heap else 0
```

## Reference

- LeetCode: https://leetcode.com/problems/last-stone-weight/
