# 384. Shuffle an Array

**Difficulty:** Medium
**Topics:** Array, Math, Design, Randomized
**Common companies:** Google, Amazon
**Category (README):** 15. Design Problems

## Problem Description

Given an integer array `nums`, design an algorithm to randomly shuffle the array. All permutations of the array should be **equally likely** as a result of the shuffling.

Implement the `Solution` class:

	
- `Solution(int[] nums)` Initializes the object with the integer array `nums`.

	
- `int[] reset()` Resets the array to its original configuration and returns it.

	
- `int[] shuffle()` Returns a random shuffling of the array.

 

**Example 1:**

```

**Input**
["Solution", "shuffle", "reset", "shuffle"]
[[[1, 2, 3]], [], [], []]
**Output**
[null, [3, 1, 2], [1, 2, 3], [1, 3, 2]]

**Explanation**
Solution solution = new Solution([1, 2, 3]);
solution.shuffle();    // Shuffle the array [1,2,3] and return its result.
                       // Any permutation of [1,2,3] must be equally likely to be returned.
                       // Example: return [3, 1, 2]
solution.reset();      // Resets the array back to its original configuration [1,2,3]. Return [1, 2, 3]
solution.shuffle();    // Returns the random shuffling of array [1,2,3]. Example: return [1, 3, 2]

```

 

**Constraints:**

	
- `1 <= nums.length <= 50`

	
- `-106 <= nums[i] <= 106`

	
- All the elements of `nums` are **unique**.

	
- At most `104` calls **in total** will be made to `reset` and `shuffle`.

## Key Idea

Array + Fisher–Yates shuffle

## Approach

1. Identify the core pattern for this category: **15. Design Problems**.
2. Use the key idea above as the primary strategy.
3. Confirm edge cases and state time/space complexity before coding.
4. Implement and verify against the examples above / on LeetCode.

**Time Complexity:** O(n) per call to `shuffle` or `reset` — each element is touched once.
**Space Complexity:** O(n) — storing the original array plus the working copy.

## Reference Solution (Python)

```python
import random

class Solution:
    def __init__(self, nums: list[int]):
        self.original = nums[:]
        self.array = nums[:]

    def reset(self) -> list[int]:
        self.array = self.original[:]
        return self.array

    def shuffle(self) -> list[int]:
        for i in range(len(self.array) - 1, 0, -1):
            j = random.randint(0, i)
            self.array[i], self.array[j] = self.array[j], self.array[i]
        return self.array
```

## Reference

- LeetCode: https://leetcode.com/problems/shuffle-an-array/
