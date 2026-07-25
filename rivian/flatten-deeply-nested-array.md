# 2625. Flatten Deeply Nested Array

**Difficulty:** Medium
**Topics:** Array, Recursion
**Reported at Rivian:** Tracked in Rivian's known coding question bank (CodeJeet).

## Problem Description

Given a multi-dimensional array `arr` and a depth `n`, return a *flattened* version of that array.

A multi-dimensional array is a recursive data structure that contains integers or other multi-dimensional arrays.

The depth of `arr` is the maximum number of times you can recursively enter an array element before reaching an integer.

You should flatten the array such that any array elements found at a depth less than `n` are recursively concatenated into a single flat array. Elements at depth greater than `n` should remain (or be wrapped) as nested arrays.

The depth of the elements of `arr` is the number of times you have to extract an array element to reach that element.

## Example 1

```
Input: arr = [1, [2, [3, [4, [5, 6, 7], 8], 9], 10], 11, 12], n = 1
Output: [1, 2, [3, [4, [5, 6, 7], 8], 9], 10, 11, 12]
Explanation:
The elements that are flattened are underlined by depth:
[1, [2,[3,[4,[5,6,7],8],9],10], 11, 12] -> depth 1 elements flattened
```

## Example 2

```
Input: arr = [1, [2, [3, [4, [5, 6, 7], 8], 9], 10], 11, 12], n = 2
Output: [1, 2, 3, [4, [5, 6, 7], 8], 9, 10, 11, 12]
```

## Example 3

```
Input: arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]], n = 0
Output: [[1, 2, 3], [4, 5, 6], [7, 8, 9], [10, 11, 12]]
Explanation: n = 0 means no flattening should occur; the array is returned unchanged.
```

## Constraints

- `0 <= arr.length <= 1000`
- `0 <= arr[i].length <= 1000`
- `0 <= n <= 1000`
- All the values of the input are integers or arrays.
- The depth of `arr` (the number of nested arrays it contains) does not exceed `1000`.
- The total number of elements (leaf integers) in `arr` does not exceed `10^4`.

## Approach

1. Process the array level by level, or recursively, tracking how much "flatten budget" (`n`) is left.
2. For each element:
   - If it's an integer, keep it as-is.
   - If it's an array and `n > 0`, splice its contents directly into the result (recursing with `n - 1`).
   - If it's an array and `n == 0`, keep it nested (do not flatten further).
3. This is naturally implemented with a recursive helper function that decrements the remaining depth budget as it descends.

**Time Complexity:** O(N), where N is the total number of elements across all nesting levels (every element is visited once).
**Space Complexity:** O(D) for the recursion stack, where D is the maximum nesting depth, plus O(N) for the output array.

## Reference Solution (Python)

```python
from typing import Union

NestedArray = Union[int, list]


def flatten(arr: list[NestedArray], n: int) -> list[NestedArray]:
    result: list[NestedArray] = []

    def helper(items: list[NestedArray], depth_remaining: int) -> None:
        for item in items:
            if isinstance(item, list) and depth_remaining > 0:
                helper(item, depth_remaining - 1)
            else:
                result.append(item)

    helper(arr, n)
    return result
```

## Follow-up Questions Interviewers May Ask

- How would you implement this iteratively (using an explicit stack) instead of recursively, to avoid stack-overflow risk on very deep arrays?
- How would you flatten completely (unbounded depth) instead of by a fixed `n`?
- How would this generalize to a JSON-like nested structure with mixed dicts and arrays?
