# 990. Satisfiability of Equality Equations

**Difficulty:** Medium
**Topics:** Array, String, Union-Find, Graph Theory
**Common companies:** Google, Amazon
**Category (README):** 10. Union Find

## Problem Description

You are given an array of strings `equations` that represent relationships between variables where each string `equations[i]` is of length `4` and takes one of two different forms: `"xi==yi"` or `"xi!=yi"`.Here, `xi` and `yi` are lowercase letters (not necessarily different) that represent one-letter variable names.

Return `true`* if it is possible to assign integers to variable names so as to satisfy all the given equations, or *`false`* otherwise*.

 

**Example 1:**

```

**Input:** equations = ["a==b","b!=a"]
**Output:** false
**Explanation:** If we assign say, a = 1 and b = 1, then the first equation is satisfied, but not the second.
There is no way to assign the variables to satisfy both equations.

```

**Example 2:**

```

**Input:** equations = ["b==a","a==b"]
**Output:** true
**Explanation:** We could assign a = 1 and b = 1 to satisfy both equations.

```

 

**Constraints:**

	
- `1 <= equations.length <= 500`

	
- `equations[i].length == 4`

	
- `equations[i][0]` is a lowercase letter.

	
- `equations[i][1]` is either `'='` or `'!'`.

	
- `equations[i][2]` is `'='`.

	
- `equations[i][3]` is a lowercase letter.

## Key Idea

Union Find handling equivalence relations

## Approach

1. Identify the core pattern for this category: **10. Union Find**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) — with union by find and path compression over a fixed alphabet of 26 letters, each union/find is amortized near O(1).
**Space Complexity:** O(1) — the parent array is a fixed size of 26.

## Reference Solution (Python)

```python
def equationsPossible(equations: list[str]) -> bool:
    parent = list(range(26))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        rx, ry = find(x), find(y)
        if rx != ry:
            parent[rx] = ry

    for eq in equations:
        if eq[1] == "=":
            union(ord(eq[0]) - ord("a"), ord(eq[3]) - ord("a"))

    for eq in equations:
        if eq[1] == "!" and find(ord(eq[0]) - ord("a")) == find(ord(eq[3]) - ord("a")):
            return False

    return True
```

## Reference

- LeetCode: https://leetcode.com/problems/satisfiability-of-equality-equations/
