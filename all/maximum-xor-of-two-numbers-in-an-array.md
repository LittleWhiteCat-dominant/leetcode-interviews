# 421. Maximum XOR of Two Numbers in an Array

**Difficulty:** Medium
**Topics:** Array, Hash Table, Bit Manipulation, Trie
**Common companies:** Google
**Category (README):** 7.3 Trie (Prefix Tree)

## Problem Description

Given an integer array `nums`, return *the maximum result of *`nums[i] XOR nums[j]`, where `0 <= i <= j < n`.

 

**Example 1:**

```

**Input:** nums = [3,10,5,25,2,8]
**Output:** 28
**Explanation:** The maximum result is 5 XOR 25 = 28.

```

**Example 2:**

```

**Input:** nums = [14,70,53,83,49,91,36,80,92,51,66,70]
**Output:** 127

```

 

**Constraints:**

	
- `1 <= nums.length <= 2 * 105`

	
- `0 <= nums[i] <= 231 - 1`

## Key Idea

Build a bitwise Trie, greedily walk the opposite bit

## Approach

This is solved with **a bitwise Trie built incrementally, greedily choosing the opposite bit at each level to maximize XOR**:

1. Determine `highest_bit`, the position of the most significant bit across all numbers, so every number is processed with a fixed bit width.
2. Build a binary trie where each node has two children (for bit `0` and bit `1`); `insert(num)` walks from the highest bit to the lowest, creating child nodes as needed.
3. For each number, first `insert` it into the trie, then immediately `query` it: at each bit level, try to go to the child representing the opposite bit (`1 - bit`), since XOR-ing opposite bits maximizes that bit's contribution.
4. If the opposite-bit child doesn't exist yet, fall back to the same-bit child (no better option exists).
5. Track the maximum XOR value seen across all `query` calls as numbers are inserted one at a time.

**Time Complexity:** O(n * L) — where L is the bit width (~32); each of the n numbers is inserted into and queried against the trie in O(L).
**Space Complexity:** O(n * L) — for the trie nodes created while inserting all numbers.

## Reference Solution (Python)

```python
class TrieNode:
    __slots__ = ("children",)

    def __init__(self):
        self.children: list["TrieNode | None"] = [None, None]


def findMaximumXOR(nums: list[int]) -> int:
    highest_bit = max(nums).bit_length() - 1 if nums else 0
    root = TrieNode()

    def insert(num: int) -> None:
        node = root
        for i in range(highest_bit, -1, -1):
            bit = (num >> i) & 1
            if node.children[bit] is None:
                node.children[bit] = TrieNode()
            node = node.children[bit]

    def query(num: int) -> int:
        node = root
        result = 0
        for i in range(highest_bit, -1, -1):
            bit = (num >> i) & 1
            toggled = 1 - bit
            if node.children[toggled]:
                result |= (1 << i)
                node = node.children[toggled]
            else:
                node = node.children[bit]
        return result

    max_xor = 0
    for num in nums:
        insert(num)
        max_xor = max(max_xor, query(num))

    return max_xor
```

## Reference

- LeetCode: https://leetcode.com/problems/maximum-xor-of-two-numbers-in-an-array/
