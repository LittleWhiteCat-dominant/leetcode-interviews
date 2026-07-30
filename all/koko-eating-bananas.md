# 875. Koko Eating Bananas

**Difficulty:** Medium
**Topics:** Array, Binary Search
**Common companies:** Google, Amazon
**Category (README):** 1.4 Binary Search

## Problem Description

Koko loves to eat bananas. There are `n` piles of bananas, the `ith` pile has `piles[i]` bananas. The guards have gone and will come back in `h` hours.

Koko can decide her bananas-per-hour eating speed of `k`. Each hour, she chooses some pile of bananas and eats `k` bananas from that pile. If the pile has less than `k` bananas, she eats all of them instead and will not eat any more bananas during this hour.

Koko likes to eat slowly but still wants to finish eating all the bananas before the guards return.

Return *the minimum integer* `k` *such that she can eat all the bananas within* `h` *hours*.

 

**Example 1:**

```

**Input:** piles = [3,6,7,11], h = 8
**Output:** 4

```

**Example 2:**

```

**Input:** piles = [30,11,23,4,20], h = 5
**Output:** 30

```

**Example 3:**

```

**Input:** piles = [30,11,23,4,20], h = 6
**Output:** 23

```

 

**Constraints:**

	
- `1 <= piles.length <= 104`

	
- `piles.length <= h <= 109`

	
- `1 <= piles[i] <= 109`

## Key Idea

Binary search on the answer + a feasibility check function

## Approach

1. Identify the core pattern for this category: **1.4 Binary Search**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n log m) — where `n` is the number of piles and `m` is the max pile size; binary search over the speed range, with an O(n) feasibility check each iteration.
**Space Complexity:** O(1) — only a few scalar variables are used.

## Reference Solution (Python)

```python
import math


def minEatingSpeed(piles: list[int], h: int) -> int:
    def hours_needed(speed: int) -> int:
        return sum(math.ceil(pile / speed) for pile in piles)

    lo, hi = 1, max(piles)
    while lo < hi:
        mid = (lo + hi) // 2
        if hours_needed(mid) <= h:
            hi = mid
        else:
            lo = mid + 1

    return lo
```

## Reference

- LeetCode: https://leetcode.com/problems/koko-eating-bananas/
