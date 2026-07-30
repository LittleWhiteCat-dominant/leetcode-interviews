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

1. Identify the core pattern for this category: **4.1 Basic Stack Applications**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

## Reference

- LeetCode: https://leetcode.com/problems/flatten-nested-list-iterator/
