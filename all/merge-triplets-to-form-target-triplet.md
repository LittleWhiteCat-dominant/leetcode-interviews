# 1899. Merge Triplets to Form Target Triplet

**Difficulty:** Medium
**Topics:** Array, Greedy
**Common companies:** Google, Amazon
**Category (README):** 13. Greedy

## Problem Description

A **triplet** is an array of three integers. You are given a 2D integer array `triplets`, where `triplets[i] = [ai, bi, ci]` describes the `ith` **triplet**. You are also given an integer array `target = [x, y, z]` that describes the **triplet** you want to obtain.

To obtain `target`, you may apply the following operation on `triplets` **any number** of times (possibly **zero**):

	
- Choose two indices (**0-indexed**) `i` and `j` (`i != j`) and **update** `triplets[j]` to become `[max(ai, aj), max(bi, bj), max(ci, cj)]`.

	
		
- For example, if `triplets[i] = [2, 5, 3]` and `triplets[j] = [1, 7, 5]`, `triplets[j]` will be updated to `[max(2, 1), max(5, 7), max(3, 5)] = [2, 7, 5]`.

	
	

Return `true` *if it is possible to obtain the *`target`* **triplet** *`[x, y, z]`* as an** element** of *`triplets`*, or *`false`* otherwise*.

 

**Example 1:**

```

**Input:** triplets = [[2,5,3],[1,8,4],[1,7,5]], target = [2,7,5]
**Output:** true
**Explanation:** Perform the following operations:
- Choose the first and last triplets [[2,5,3],[1,8,4],[1,7,5]]. Update the last triplet to be [max(2,1), max(5,7), max(3,5)] = [2,7,5]. triplets = [[2,5,3],[1,8,4],[2,7,5]]
The target triplet [2,7,5] is now an element of triplets.

```

**Example 2:**

```

**Input:** triplets = [[3,4,5],[4,5,6]], target = [3,2,5]
**Output:** false
**Explanation:** It is impossible to have [3,2,5] as an element because there is no 2 in any of the triplets.

```

**Example 3:**

```

**Input:** triplets = [[2,5,3],[2,3,4],[1,2,5],[5,2,3]], target = [5,5,5]
**Output:** true
**Explanation: **Perform the following operations:
- Choose the first and third triplets [[2,5,3],[2,3,4],[1,2,5],[5,2,3]]. Update the third triplet to be [max(2,1), max(5,2), max(3,5)] = [2,5,5]. triplets = [[2,5,3],[2,3,4],[2,5,5],[5,2,3]].
- Choose the third and fourth triplets [[2,5,3],[2,3,4],[2,5,5],[5,2,3]]. Update the fourth triplet to be [max(2,5), max(5,2), max(5,3)] = [5,5,5]. triplets = [[2,5,3],[2,3,4],[2,5,5],[5,5,5]].
The target triplet [5,5,5] is now an element of triplets.

```

 

**Constraints:**

	
- `1 <= triplets.length <= 105`

	
- `triplets[i].length == target.length == 3`

	
- `1 <= ai, bi, ci, x, y, z <= 1000`

## Key Idea

Greedily filter triplets that satisfy the condition

## Approach

This is solved with **greedy filtering of "compatible" triplets**:

1. Note that the `max` operation can only ever raise a coordinate, never lower it, so any triplet with a coordinate exceeding the matching `target` coordinate can never help and must be discarded.
2. Scan through `triplets`, keeping only those where `a <= x`, `b <= y`, and `c <= z`.
3. Among the surviving triplets, track for each of the three positions whether some triplet already matches `target` exactly at that position (a `good` flag per coordinate).
4. If all three flags become true, some combination of `max` operations can assemble `target`, so return `True`; otherwise return `False`.

**Time Complexity:** O(n) — a single pass over the triplets array.
**Space Complexity:** O(1) — only a fixed-size `good` flag array is used.

## Reference Solution (Python)

```python
def mergeTriplets(triplets: list[list[int]], target: list[int]) -> bool:
    x, y, z = target
    good = [False, False, False]

    for a, b, c in triplets:
        if a <= x and b <= y and c <= z:
            good[0] |= a == x
            good[1] |= b == y
            good[2] |= c == z

    return all(good)
```

## Reference

- LeetCode: https://leetcode.com/problems/merge-triplets-to-form-target-triplet/
