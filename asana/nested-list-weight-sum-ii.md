# 364. Nested List Weight Sum II

**Difficulty:** Medium
**Topics:** Depth-First Search, Breadth-First Search, Design
**Reported at Asana:** Tracked in Asana's known coding question bank (InterviewSolver).

## Problem Description

You are given a nested list of integers `nestedList`. Each element is either an integer or a list whose elements may also be integers or other lists.

The **depth** of an integer is the number of lists that it is inside of. For example, the nested list `[1,[2,2],[[3],2],1]` has each integer's value set to its **depth**.

Let `maxDepth` be the **maximum depth** of any integer.

The **weight** of an integer is `maxDepth - (the depth of the integer) + 1`.

Return the sum of each integer in `nestedList` multiplied by its weight.

## Example 1

```
Input: nestedList = [[1,1],2,[1,1]]
Output: 8
Explanation: Four 1's with a weight of 1, one 2 with a weight of 2.
1*1 + 1*1 + 2*2 + 1*1 + 1*1 = 8
```

## Example 2

```
Input: nestedList = [1,[4,[6]]]
Output: 17
Explanation: One 1 at depth 3, one 4 at depth 2, and one 6 at depth 1.
1*3 + 4*2 + 6*1 = 17
```

## Constraints

- `1 <= nestedList.length <= 50`
- The values of the integers in the nested list is in the range `[-100, 100]`.
- The maximum **depth** of any integer is less than or equal to `50`.

## Approach

The tricky part is that the weight formula (`maxDepth - depth + 1`) depends on `maxDepth`, which you don't know until you've scanned the whole structure — so you cannot compute the weighted sum in a single naive top-down pass without knowing `maxDepth` first.

**Two-pass approach:**
1. First pass (DFS/BFS): traverse the nested list to find `maxDepth`.
2. Second pass (DFS/BFS): traverse again, this time computing `sum += value * (maxDepth - depth + 1)`.

**Clever single-pass approach (BFS with running sums):**
1. Process the structure level by level (BFS). Maintain `level_sum` (running sum of all integers seen at the current or shallower unweighted level) and `total`.
2. At each level, add every integer at that level into `level_sum`, then add the **entire accumulated** `level_sum` into `total`.
3. Because shallower levels get added into `total` repeatedly at every subsequent level, this naturally computes the reversed-depth weighting without knowing `maxDepth` ahead of time.

**Time Complexity:** O(n), where n is the total number of integers and nested lists.
**Space Complexity:** O(d) for the recursion/queue, where d is the maximum depth.

## Reference Solution (Python, single-pass BFS trick)

```python
from collections import deque
from typing import Union

NestedElement = Union[int, list]


def depth_sum_inverse(nested_list: list[NestedElement]) -> int:
    queue = deque(nested_list)
    level_sum = 0
    total = 0

    while queue:
        for _ in range(len(queue)):
            item = queue.popleft()
            if isinstance(item, int):
                level_sum += item
            else:
                queue.extend(item)
        total += level_sum  # Shallower levels accumulate into every later level's total.

    return total
```

## Follow-up Questions Interviewers May Ask

- How does this differ from Nested List Weight Sum I (LC 339), where the weight increases with depth instead of decreasing?
- Can you solve this with a single DFS pass instead of two passes or the BFS trick?
- How would you handle extremely deep nesting that risks a stack overflow with recursive DFS?
