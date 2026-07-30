# 1570. Dot Product of Two Sparse Vectors

**Difficulty:** Medium (LeetCode Premium — statement not publicly available)
**Topics:** Array, Hash Table, Two Pointers, Design
**Common companies:** **Meta favorite**
**Category (README):** 6. Hash Table

## Problem Description

This is a Premium problem. View it on LeetCode: https://leetcode.com/problems/dot-product-of-two-sparse-vectors/

## Key Idea

Hash map storing nonzero values, or two-pointer traversal

## Approach

1. Identify the core pattern for this category: **6. Hash Table**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** Constructor is O(n). `dotProduct` is O(min(L1, L2)) — iterate over the vector with fewer nonzero entries and do O(1) hash lookups into the other.
**Space Complexity:** O(L) — only the nonzero entries are stored per vector.

## Reference Solution (Python)

```python
class SparseVector:
    def __init__(self, nums: list[int]):
        self.nonzero: dict[int, int] = {i: v for i, v in enumerate(nums) if v != 0}

    def dotProduct(self, vec: "SparseVector") -> int:
        if len(self.nonzero) > len(vec.nonzero):
            return vec.dotProduct(self)

        result = 0
        for i, v in self.nonzero.items():
            if i in vec.nonzero:
                result += v * vec.nonzero[i]
        return result
```

## Reference

- LeetCode: https://leetcode.com/problems/dot-product-of-two-sparse-vectors/
