# 322. Coin Change

**Difficulty:** Medium
**Topics:** Array, Dynamic Programming, Breadth-First Search
**Common companies:** All big tech
**Category (README):** 12.1 1D DP

## Problem Description

You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.

Return *the fewest number of coins that you need to make up that amount*. If that amount of money cannot be made up by any combination of the coins, return `-1`.

You may assume that you have an infinite number of each kind of coin.

 

**Example 1:**

```

**Input:** coins = [1,2,5], amount = 11
**Output:** 3
**Explanation:** 11 = 5 + 5 + 1

```

**Example 2:**

```

**Input:** coins = [2], amount = 3
**Output:** -1

```

**Example 3:**

```

**Input:** coins = [1], amount = 0
**Output:** 0

```

 

**Constraints:**

	
- `1 <= coins.length <= 12`

	
- `1 <= coins[i] <= 231 - 1`

	
- `0 <= amount <= 104`

## Key Idea

Unbounded knapsack style 1D DP

## Approach

This is solved with **unbounded-knapsack style bottom-up DP, minimizing coin count for every sub-amount**:

1. Define `dp[i]` as the fewest coins needed to make amount `i`; initialize `dp[0] = 0` and every other entry to infinity (unreachable so far).
2. Iterate `i` from `1` up to `amount`, and for each `i`, try every coin denomination that is `<= i`.
3. For each usable coin, `dp[i] = min(dp[i], dp[i - coin] + 1)` — using that coin means we need one more coin than however many were needed to make the remainder `i - coin`.
4. Because smaller amounts are always solved before larger ones, `dp[i - coin]` is guaranteed to already hold its final value.
5. After the loop, return `dp[amount]` if it's finite, otherwise `-1` since the amount is unreachable with the given coins.

**Time Complexity:** O(amount * len(coins)) — for each amount from 1 to `amount`, we try every coin.
**Space Complexity:** O(amount) — for the 1D `dp` array.

## Reference Solution (Python)

```python
def coinChange(coins: list[int], amount: int) -> int:
    dp = [0] + [float("inf")] * amount

    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)

    return dp[amount] if dp[amount] != float("inf") else -1
```

## Reference

- LeetCode: https://leetcode.com/problems/coin-change/
