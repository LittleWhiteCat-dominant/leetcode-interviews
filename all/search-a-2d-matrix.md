# 74. Search a 2D Matrix

**Difficulty:** Medium
**Topics:** Array, Binary Search, Matrix
**Common companies:** Amazon, Apple
**Category (README):** 1.4 Binary Search

## Problem Description

You are given an `m x n` integer matrix `matrix` with the following two properties:

	
- Each row is sorted in non-decreasing order.

	
- The first integer of each row is greater than the last integer of the previous row.

Given an integer `target`, return `true` *if* `target` *is in* `matrix` *or* `false` *otherwise*.

You must write a solution in `O(log(m * n))` time complexity.

 

**Example 1:**

```

**Input:** matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 3
**Output:** true

```

**Example 2:**

```

**Input:** matrix = [[1,3,5,7],[10,11,16,20],[23,30,34,60]], target = 13
**Output:** false

```

 

**Constraints:**

	
- `m == matrix.length`

	
- `n == matrix[i].length`

	
- `1 <= m, n <= 100`

	
- `-104 <= matrix[i][j], target <= 104`

## Key Idea

Flatten to 1D binary search or start from a corner with two pointers

## Approach

This is solved with **binary search over the matrix treated as a flattened sorted array**:

1. Because each row is sorted and each row starts after the previous row ends, the entire matrix is equivalent to one sorted 1D array of length `rows * cols`.
2. Run standard binary search over the virtual index range `[0, rows * cols - 1]`.
3. For a given midpoint index `mid`, map it back to 2D coordinates with `mid // cols` and `mid % cols` to read the corresponding value.
4. Compare that value to `target` and shrink the search range (`lo`/`hi`) exactly as in normal binary search.
5. Return `True` on a match, or `False` once the range is exhausted.

**Time Complexity:** O(log(m * n)) — binary search over the matrix treated as a flattened sorted array.
**Space Complexity:** O(1) — no extra data structures, just index math.

## Reference Solution (Python)

```python
def searchMatrix(matrix: list[list[int]], target: int) -> bool:
    rows, cols = len(matrix), len(matrix[0])
    lo, hi = 0, rows * cols - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        val = matrix[mid // cols][mid % cols]
        if val == target:
            return True
        if val < target:
            lo = mid + 1
        else:
            hi = mid - 1

    return False
```

## Reference

- LeetCode: https://leetcode.com/problems/search-a-2d-matrix/
