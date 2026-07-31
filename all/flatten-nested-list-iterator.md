# 341. Flatten Nested List Iterator

**Difficulty:** Medium
**Topics:** Stack, Tree, Depth-First Search, Design, Queue, Iterator
**Common companies:** **Meta favorite**
**Category (README):** 4.1 Basic Stack Applications

## Problem Description

You are given a nested list of integers `nestedList`. Each element is either an integer or a list whose elements may also be integers or other lists. Implement an iterator to flatten it.

Implement the `NestedIterator` class:

	
- `NestedIterator(List<NestedInteger> nestedList)` Initializes the iterator with the nested list `nestedList`.

	
- `int next()` Returns the next integer in the nested list.

	
- `boolean hasNext()` Returns `true` if there are still some integers in the nested list and `false` otherwise.

Your code will be tested with the following pseudocode:

```

initialize iterator with nestedList
res = []
while iterator.hasNext()
    append iterator.next() to the end of res
return res

```

If `res` matches the expected flattened list, then your code will be judged as correct.

 

**Example 1:**

```

**Input:** nestedList = [[1,1],2,[1,1]]
**Output:** [1,1,2,1,1]
**Explanation:** By calling next repeatedly until hasNext returns false, the order of elements returned by next should be: [1,1,2,1,1].

```

**Example 2:**

```

**Input:** nestedList = [1,[4,[6]]]
**Output:** [1,4,6]
**Explanation:** By calling next repeatedly until hasNext returns false, the order of elements returned by next should be: [1,4,6].

```

 

**Constraints:**

	
- `1 <= nestedList.length <= 500`

	
- The values of the integers in the nested list is in the range `[-106, 106]`.

## Key Idea

Stack + lazy expansion

## Approach

This is solved with **a stack holding the nested list in reverse order, expanded lazily**:

1. Initialize a stack with the top-level `nestedList` reversed, so the first element to process ends up on top.
2. Define a helper that "flattens the top": while the top of the stack is a nested list (not a plain integer), pop it and push its children back in reversed order.
3. Call this helper before every `hasNext()`/`next()` so the top of the stack is always guaranteed to be an integer if one remains.
4. `hasNext()` then simply checks whether the stack is non-empty, and `next()` pops and returns the integer on top.

**Time Complexity:** O(n) total across all `next()`/`hasNext()` calls — each integer and list is pushed/popped from the stack exactly once, where `n` is the total number of integers and lists.
**Space Complexity:** O(n) — the stack holds nested list iterators in the worst case (e.g. deeply nested lists).

## Reference Solution (Python)

```python
# This is the interface that allows for creating nested lists.
# You should not implement it, or speculate about its implementation.
class NestedInteger:
    def isInteger(self) -> bool:
        ...

    def getInteger(self) -> int:
        ...

    def getList(self) -> list["NestedInteger"]:
        ...


class NestedIterator:
    def __init__(self, nestedList: list[NestedInteger]):
        self.stack = list(reversed(nestedList))

    def _flatten_top(self) -> None:
        while self.stack and not self.stack[-1].isInteger():
            top = self.stack.pop()
            self.stack.extend(reversed(top.getList()))

    def next(self) -> int:
        self._flatten_top()
        return self.stack.pop().getInteger()

    def hasNext(self) -> bool:
        self._flatten_top()
        return len(self.stack) > 0
```

## Reference

- LeetCode: https://leetcode.com/problems/flatten-nested-list-iterator/
