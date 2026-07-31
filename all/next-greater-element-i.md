# 496. Next Greater Element I

**Difficulty:** Easy
**Topics:** Array, Hash Table, Stack, Monotonic Stack
**Common companies:** Amazon, Google
**Category (README):** 4.2 Monotonic Stack

## Problem Description

The **next greater element** of some element `x` in an array is the **first greater** element that is **to the right** of `x` in the same array.

You are given two **distinct 0-indexed** integer arrays `nums1` and `nums2`, where `nums1` is a subset of `nums2`.

For each `0 <= i < nums1.length`, find the index `j` such that `nums1[i] == nums2[j]` and determine the **next greater element** of `nums2[j]` in `nums2`. If there is no next greater element, then the answer for this query is `-1`.

Return *an array *`ans`* of length *`nums1.length`* such that *`ans[i]`* is the **next greater element** as described above.*

 

**Example 1:**

```

**Input:** nums1 = [4,1,2], nums2 = [1,3,4,2]
**Output:** [-1,3,-1]
**Explanation:** The next greater element for each value of nums1 is as follows:
- 4 is underlined in nums2 = [1,3,4,2]. There is no next greater element, so the answer is -1.
- 1 is underlined in nums2 = [1,3,4,2]. The next greater element is 3.
- 2 is underlined in nums2 = [1,3,4,2]. There is no next greater element, so the answer is -1.

```

**Example 2:**

```

**Input:** nums1 = [2,4], nums2 = [1,2,3,4]
**Output:** [3,-1]
**Explanation:** The next greater element for each value of nums1 is as follows:
- 2 is underlined in nums2 = [1,2,3,4]. The next greater element is 3.
- 4 is underlined in nums2 = [1,2,3,4]. There is no next greater element, so the answer is -1.

```

 

**Constraints:**

	
- `1 <= nums1.length <= nums2.length <= 1000`

	
- `0 <= nums1[i], nums2[i] <= 104`

	
- All integers in `nums1` and `nums2` are **unique**.

	
- All the integers of `nums1` also appear in `nums2`.

 

**Follow up:** Could you find an `O(nums1.length + nums2.length)` solution?

## Key Idea

Monotonic stack + hash map lookup

## Approach

This is solved with **a monotonic decreasing stack over `nums2`, feeding a hash map lookup for `nums1`**:

1. Iterate through `nums2` while maintaining a stack that stays in decreasing order from bottom to top.
2. For each new number, pop every stack element smaller than it, since the current number is each popped element's next greater element; record each such pair in a `next_greater` map.
3. Push the current number onto the stack after popping, so the stack always represents numbers still waiting for their next greater element.
4. Once `nums2` is fully processed, any numbers left on the stack have no next greater element.
5. Answer each query in `nums1` by looking up `next_greater.get(num, -1)`.

**Time Complexity:** O(n2 + n1) — the monotonic stack pass over `nums2` is linear, plus a linear lookup pass for `nums1`.
**Space Complexity:** O(n2) — for the stack and the next-greater hash map.

## Reference Solution (Python)

```python
def nextGreaterElement(nums1: list[int], nums2: list[int]) -> list[int]:
    next_greater = {}
    stack: list[int] = []

    for num in nums2:
        while stack and stack[-1] < num:
            next_greater[stack.pop()] = num
        stack.append(num)

    return [next_greater.get(num, -1) for num in nums1]
```

## Reference

- LeetCode: https://leetcode.com/problems/next-greater-element-i/
