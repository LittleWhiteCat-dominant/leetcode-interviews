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

1. Identify the core pattern for this category: **7.3 Trie (Prefix Tree)**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

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
