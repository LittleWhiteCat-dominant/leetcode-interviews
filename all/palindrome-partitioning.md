# 131. Palindrome Partitioning

**Difficulty:** Medium
**Topics:** String, Dynamic Programming, Backtracking
**Common companies:** Amazon, Google
**Category (README):** 11. Backtracking

## Problem Description

Given a string `s`, partition `s` such that every substring of the partition is a **palindrome**. Return *all possible palindrome partitioning of *`s`.

 

**Example 1:**

```
**Input:** s = "aab"
**Output:** [["a","a","b"],["aa","b"]]

```

**Example 2:**

```
**Input:** s = "a"
**Output:** [["a"]]

```

 

**Constraints:**

	
- `1 <= s.length <= 16`

	
- `s` contains only lowercase English letters.

## Key Idea

Backtracking + palindrome check for pruning

## Approach

This is solved with **backtracking that only extends the current partition with palindromic prefixes**:

1. Recurse on a `start` index representing the beginning of the next unpartitioned substring.
2. At each call, try every possible `end` from `start + 1` to `n`, and check whether `s[start:end]` is a palindrome using a simple two-pointer helper.
3. If `s[start:end]` is a palindrome, append it to the current path and recurse from `end`; otherwise skip that split point (pruning invalid partitions early).
4. When `start` reaches `n`, the path is a complete valid partition, so record a copy of it in the results.
5. Backtrack by popping the last piece before trying the next `end`, so the path can be reused across branches.

**Time Complexity:** O(n \* 2^n) — in the worst case there are O(2^n) partitions, each costing up to O(n) to validate/build.
**Space Complexity:** O(n) — recursion depth for the backtracking path, excluding the output.

## Reference Solution (Python)

```python
from typing import List

def partition(s: str) -> List[List[str]]:
    n = len(s)
    result = []
    path = []

    def is_palindrome(i: int, j: int) -> bool:
        while i < j:
            if s[i] != s[j]:
                return False
            i += 1
            j -= 1
        return True

    def backtrack(start: int) -> None:
        if start == n:
            result.append(path[:])
            return
        for end in range(start + 1, n + 1):
            if is_palindrome(start, end - 1):
                path.append(s[start:end])
                backtrack(end)
                path.pop()

    backtrack(0)
    return result
```

## Reference

- LeetCode: https://leetcode.com/problems/palindrome-partitioning/
