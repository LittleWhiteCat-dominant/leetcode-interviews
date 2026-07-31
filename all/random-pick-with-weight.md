# 528. Random Pick with Weight

**Difficulty:** Medium
**Topics:** Array, Math, Binary Search, Prefix Sum, Randomized
**Common companies:** **Meta favorite**
**Category (README):** 1.3 Prefix Sum

## Problem Description

You are given a **0-indexed** array of positive integers `w` where `w[i]` describes the **weight** of the `ith` index.

You need to implement the function `pickIndex()`, which **randomly** picks an index in the range `[0, w.length - 1]` (**inclusive**) and returns it. The **probability** of picking an index `i` is `w[i] / sum(w)`.

	
- For example, if `w = [1, 3]`, the probability of picking index `0` is `1 / (1 + 3) = 0.25` (i.e., `25%`), and the probability of picking index `1` is `3 / (1 + 3) = 0.75` (i.e., `75%`).

 

**Example 1:**

```

**Input**
["Solution","pickIndex"]
[[[1]],[]]
**Output**
[null,0]

**Explanation**
Solution solution = new Solution([1]);
solution.pickIndex(); // return 0. The only option is to return 0 since there is only one element in w.

```

**Example 2:**

```

**Input**
["Solution","pickIndex","pickIndex","pickIndex","pickIndex","pickIndex"]
[[[1,3]],[],[],[],[],[]]
**Output**
[null,1,1,1,1,0]

**Explanation**
Solution solution = new Solution([1, 3]);
solution.pickIndex(); // return 1. It is returning the second element (index = 1) that has a probability of 3/4.
solution.pickIndex(); // return 1
solution.pickIndex(); // return 1
solution.pickIndex(); // return 1
solution.pickIndex(); // return 0. It is returning the first element (index = 0) that has a probability of 1/4.

Since this is a randomization problem, multiple answers are allowed.
All of the following outputs can be considered correct:
[null,1,1,1,1,0]
[null,1,1,1,1,1]
[null,1,1,1,0,0]
[null,1,1,1,0,1]
[null,1,0,1,0,0]
......
and so on.

```

 

**Constraints:**

	
- `1 <= w.length <= 104`

	
- `1 <= w[i] <= 105`

	
- `pickIndex` will be called at most `104` times.

## Key Idea

Prefix sum + binary search to locate the interval

## Approach

This is solved with **prefix sums plus binary search over the cumulative weight ranges**:

1. In the constructor, build a prefix-sum array `prefix_sums` where `prefix_sums[i]` is the cumulative weight of `w[0..i]`; this partitions the range `[1, total]` into contiguous segments, one per index, each of length `w[i]`.
2. To pick an index proportional to its weight, generate a uniformly random integer `target` in `[1, total]`.
3. `target` falls inside exactly one index's segment; find that segment's index with `bisect_left` on `prefix_sums`, which locates the first prefix sum `>= target` in O(log n).
4. Because each index's segment length equals its weight, larger weights occupy proportionally larger ranges of `target`, giving the correct `w[i] / sum(w)` selection probability.

**Time Complexity:** O(n) for construction, O(log n) per `pickIndex` call via binary search.
**Space Complexity:** O(n) — for the prefix sum array.

## Reference Solution (Python)

```python
import bisect
import random
from typing import List


class Solution:
    def __init__(self, w: List[int]):
        self.prefix_sums = []
        total = 0
        for weight in w:
            total += weight
            self.prefix_sums.append(total)
        self.total = total

    def pickIndex(self) -> int:
        target = random.randint(1, self.total)
        return bisect.bisect_left(self.prefix_sums, target)
```

## Reference

- LeetCode: https://leetcode.com/problems/random-pick-with-weight/
