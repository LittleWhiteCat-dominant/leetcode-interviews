# 339. Nested List Weight Sum

**Difficulty:** Medium (LeetCode Premium — statement not publicly available)
**Topics:** Depth-First Search, Breadth-First Search
**Common companies:** **Meta favorite**
**Category (README):** 4.1 Basic Stack Applications

## Problem Description

This is a Premium problem. View it on LeetCode: https://leetcode.com/problems/nested-list-weight-sum/

## Key Idea

DFS/stack accumulating depth-weighted sums

## Approach

This is solved with **recursive DFS that tracks nesting depth**:

1. Write a helper `dfs(items, depth)` that processes a list of `NestedInteger` elements at a given nesting `depth`, starting at `depth = 1` for the top level.
2. For each element, if it's a plain integer, add `value * depth` to the running total, since deeper integers are weighted more heavily.
3. If it's a nested list instead, recurse into it with `depth + 1` and add the returned sum.
4. Sum the contributions of all elements at the current level and return the total up the recursion, so the top-level call yields the full depth-weighted sum.

**Time Complexity:** O(n) — every integer and every nested list is visited exactly once, where `n` is the total number of elements across all nesting levels.
**Space Complexity:** O(d) — recursion depth is bounded by the maximum nesting depth `d`.

## Reference Solution (Python)

```python
class NestedInteger:
    def isInteger(self) -> bool: ...
    def getInteger(self) -> int: ...
    def getList(self) -> list["NestedInteger"]: ...


class Solution:
    def depthSum(self, nestedList: list[NestedInteger]) -> int:
        def dfs(items: list[NestedInteger], depth: int) -> int:
            total = 0
            for item in items:
                if item.isInteger():
                    total += item.getInteger() * depth
                else:
                    total += dfs(item.getList(), depth + 1)
            return total

        return dfs(nestedList, 1)
```

## Reference

- LeetCode: https://leetcode.com/problems/nested-list-weight-sum/
