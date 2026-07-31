# 312. Burst Balloons

**Difficulty:** Hard
**Topics:** Array, Dynamic Programming
**Common companies:** Google, Amazon
**Category (README):** 12.2 2D DP

## Problem Description

You are given `n` balloons, indexed from `0` to `n - 1`. Each balloon is painted with a number on it represented by an array `nums`. You are asked to burst all the balloons.

If you burst the `ith` balloon, you will get `nums[i - 1] * nums[i] * nums[i + 1]` coins. If `i - 1` or `i + 1` goes out of bounds of the array, then treat it as if there is a balloon with a `1` painted on it.

Return *the maximum coins you can collect by bursting the balloons wisely*.

 

**Example 1:**

```

**Input:** nums = [3,1,5,8]
**Output:** 167
**Explanation:**
nums = [3,1,5,8] --> [3,5,8] --> [3,8] --> [8] --> []
coins =  3*1*5    +   3*5*8   +  1*3*8  + 1*8*1 = 167
```

**Example 2:**

```

**Input:** nums = [1,5]
**Output:** 10

```

 

**Constraints:**

	
- `n == nums.length`

	
- `1 <= n <= 300`

	
- `0 <= nums[i] <= 100`

## Key Idea

Interval DP; think backward about the last balloon burst

## Approach

This is solved with **interval DP that thinks about which balloon is burst *last* in each range**:

1. Pad `nums` with a virtual `1` on both ends so boundary multiplications never go out of range; call this padded array `balloons`.
2. Define `dp[left][right]` as the maximum coins obtainable from bursting all balloons strictly between indices `left` and `right` (both boundaries left intact until the very end).
3. Iterate over increasing interval `length`, and for each `left`/`right = left + length` pair, try every `k` strictly between them as the *last* balloon burst in that interval.
4. Bursting `k` last means its neighbors at that point are still `balloons[left]` and `balloons[right]`, so the coins gained equal `balloons[left] * balloons[k] * balloons[right]`, added to the two already-solved sub-intervals `dp[left][k]` and `dp[k][right]`.
5. Take the max over all choices of `k` to fill `dp[left][right]`; the final answer is `dp[0][n - 1]` for the fully padded array.

**Time Complexity:** O(n^3) — three nested loops over the interval length, left boundary, and the last balloon burst in that interval.
**Space Complexity:** O(n^2) — for the `dp` table over all sub-intervals.

## Reference Solution (Python)

```python
def maxCoins(nums: list[int]) -> int:
    balloons = [1] + nums + [1]
    n = len(balloons)
    dp = [[0] * n for _ in range(n)]

    for length in range(2, n):
        for left in range(n - length):
            right = left + length
            for k in range(left + 1, right):
                dp[left][right] = max(
                    dp[left][right],
                    dp[left][k] + dp[k][right] + balloons[left] * balloons[k] * balloons[right],
                )

    return dp[0][n - 1]
```

## Reference

- LeetCode: https://leetcode.com/problems/burst-balloons/
