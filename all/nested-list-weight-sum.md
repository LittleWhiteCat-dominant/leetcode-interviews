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

1. Identify the core pattern for this category: **4.1 Basic Stack Applications**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
