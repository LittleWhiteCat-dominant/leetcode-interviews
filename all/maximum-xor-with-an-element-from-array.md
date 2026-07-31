# 1707. Maximum XOR With an Element From Array

**Difficulty:** Hard
**Topics:** Array, Bit Manipulation, Trie
**Common companies:** Google, Amazon
**Category (README):** 15. Design Problems

## Problem Description

You are given an array `nums` consisting of non-negative integers. You are also given a `queries` array, where `queries[i] = [xi, mi]`.

The answer to the `ith` query is the maximum bitwise `XOR` value of `xi` and any element of `nums` that does not exceed `mi`. In other words, the answer is `max(nums[j] XOR xi)` for all `j` such that `nums[j] <= mi`. If all elements in `nums` are larger than `mi`, then the answer is `-1`.

Return *an integer array *`answer`* where *`answer.length == queries.length`* and *`answer[i]`* is the answer to the *`ith`* query.*

 

**Example 1:**

```

**Input:** nums = [0,1,2,3,4], queries = [[3,1],[1,3],[5,6]]
**Output:** [3,3,7]
**Explanation:**
1) 0 and 1 are the only two integers not greater than 1. 0 XOR 3 = 3 and 1 XOR 3 = 2. The larger of the two is 3.
2) 1 XOR 2 = 3.
3) 5 XOR 2 = 7.

```

**Example 2:**

```

**Input:** nums = [5,2,4,6,6,3], queries = [[12,4],[8,1],[6,3]]
**Output:** [15,-1,5]

```

 

**Constraints:**

	
- `1 <= nums.length, queries.length <= 105`

	
- `queries[i].length == 2`

	
- `0 <= nums[j], xi, mi <= 109`

## Key Idea

Hash map counting by coordinate

## Approach

This is solved with **offline processing: sort queries by their threshold `m` and incrementally build a bitwise Trie of eligible numbers**:

1. Sort `nums` ascending, and sort the query indices by their threshold `m` so queries are processed from smallest to largest threshold.
2. Maintain a bitwise Trie (same structure as Maximum XOR of Two Numbers) that is built up incrementally.
3. For each query in threshold order, insert all numbers from `nums` that are `<= m` and haven't been inserted yet, advancing a pointer through the sorted array.
4. If no numbers have been inserted yet (all exceed `m`), the answer for that query is `-1`.
5. Otherwise, query the trie with `x`, greedily choosing the opposite bit at each level to maximize the XOR result, and store it at the query's original index.

**Time Complexity:** O((n + q) log(n + q) + (n + q) * L) — for sorting nums and queries by threshold, and L = ~31 bit trie operations per element/query.
**Space Complexity:** O(n * L + q) — for the trie built from `nums` and the answer array.

## Reference Solution (Python)

```python
class TrieNode:
    __slots__ = ("children",)

    def __init__(self):
        self.children: list["TrieNode | None"] = [None, None]


def maximizeXor(nums: list[int], queries: list[list[int]]) -> list[int]:
    HIGH_BIT = 30
    root = TrieNode()

    def insert(num: int) -> None:
        node = root
        for i in range(HIGH_BIT, -1, -1):
            bit = (num >> i) & 1
            if node.children[bit] is None:
                node.children[bit] = TrieNode()
            node = node.children[bit]

    def query(x: int) -> int:
        node = root
        result = 0
        for i in range(HIGH_BIT, -1, -1):
            bit = (x >> i) & 1
            toggled = 1 - bit
            if node.children[toggled]:
                result |= (1 << i)
                node = node.children[toggled]
            else:
                node = node.children[bit]
        return result

    nums.sort()
    indexed_queries = sorted(range(len(queries)), key=lambda i: queries[i][1])

    answer = [-1] * len(queries)
    num_idx = 0

    for qi in indexed_queries:
        x, m = queries[qi]
        while num_idx < len(nums) and nums[num_idx] <= m:
            insert(nums[num_idx])
            num_idx += 1
        if num_idx > 0:
            answer[qi] = query(x)

    return answer
```

## Reference

- LeetCode: https://leetcode.com/problems/maximum-xor-with-an-element-from-array/
