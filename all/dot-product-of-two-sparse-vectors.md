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

This is solved with **a hash map storing only nonzero index-value pairs, skipping zero entries entirely**:

1. In the constructor, build `self.nonzero = {i: v for i, v in enumerate(nums) if v != 0}`, so sparse vectors with mostly zeros only store the few entries that matter.
2. For `dotProduct`, first swap so the smaller `nonzero` map is iterated over, minimizing the number of lookups performed.
3. For each `(i, v)` in the smaller map, check if index `i` exists in the other vector's `nonzero` map, and if so multiply and accumulate into `result`.
4. Indices that are zero in either vector contribute nothing to the dot product, so skipping them entirely avoids wasted work.
5. Return the accumulated `result`.

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
