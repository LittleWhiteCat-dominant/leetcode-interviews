# 398. Random Pick Index

**Difficulty:** Medium
**Topics:** Hash Table, Math, Reservoir Sampling, Design
**Reported at Asana:** Tracked in Asana's known coding question bank (InterviewSolver).

## Problem Description

Given an integer array `nums` with possible **duplicates**, randomly output the index of a given `target` number. You can assume that the given target number must exist in the array.

Implement the `Solution` class:

- `Solution(int[] nums)` Initializes the object with the array `nums`.
- `int pick(int target)` Picks a random index `i` from `nums` where `nums[i] == target`. If there are multiple valid `i`'s, then each index should have an equal probability of returning.

## Example

```
Input:
["Solution", "pick", "pick", "pick"]
[[[1, 2, 3, 3, 3]], [3], [1], [3]]

Output:
[null, 4, 0, 2]

Explanation:
Solution solution = new Solution([1, 2, 3, 3, 3]);
solution.pick(3); // It should return either index 2, 3, or 4 randomly. Each index should have equal probability of returning.
solution.pick(1); // It should return 0. Since in the array only nums[0] is equal to 1.
solution.pick(3); // It should return either index 2, 3, or 4 randomly. Each index should have equal probability of returning.
```

## Constraints

- `1 <= nums.length <= 2 * 10^4`
- `-2^31 <= nums[i] <= 2^31 - 1`
- `target` is an integer from `nums`.
- At most `10^4` calls will be made to `pick`.

## Approach

**Approach A — Precompute index lists (simple, more memory)**
1. In the constructor, build a hash map from each value to the list of indices where it occurs.
2. On `pick(target)`, look up the list for `target` and return a uniformly random element from it.

**Approach B — Reservoir Sampling (O(1) extra space per value, O(n) time per pick)**
1. On `pick(target)`, scan through `nums` once. Every time you encounter a value equal to `target` (say this is the `k`-th occurrence seen so far), replace the current answer with this index with probability `1/k`.
2. This guarantees a uniform distribution over all matching indices without needing to precompute or store an index list — useful as a follow-up for extremely large or streaming arrays where you can't (or don't want to) store all matching indices upfront.

**Time Complexity:**
- Approach A: O(n) for construction, O(1) per `pick` (after the initial index-list lookup, list length only affects the random draw).
- Approach B: O(1) for construction, O(n) per `pick`.

**Space Complexity:** O(n) for Approach A's index map; O(1) extra for Approach B (beyond the input array itself).

## Reference Solution (Python, Precomputed Index Lists)

```python
import random
from collections import defaultdict


class Solution:
    def __init__(self, nums: list[int]):
        self.index_map: dict[int, list[int]] = defaultdict(list)
        for i, num in enumerate(nums):
            self.index_map[num].append(i)

    def pick(self, target: int) -> int:
        return random.choice(self.index_map[target])
```

## Follow-up Questions Interviewers May Ask

- How would you solve this with reservoir sampling if `nums` is a huge stream that doesn't fit in memory?
- How would you prove that your reservoir-sampling approach produces a truly uniform distribution?
- How would you support the array being mutated (elements added/removed) between calls to `pick`?
