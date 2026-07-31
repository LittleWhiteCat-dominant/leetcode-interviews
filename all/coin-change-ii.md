# 518. Coin Change II

**Difficulty:** Medium
**Topics:** Array, Dynamic Programming
**Common companies:** Amazon, Google
**Category (README):** 12.2 2D DP

## Problem Description

You are given an integer array `coins` representing coins of different denominations and an integer `amount` representing a total amount of money.

Return *the number of combinations that make up that amount*. If that amount of money cannot be made up by any combination of the coins, return `0`.

You may assume that you have an infinite number of each kind of coin.

The **final** answer is **guaranteed** to fit into a signed **32-bit** integer.

 

**Example 1:**

```

**Input:** amount = 5, coins = [1,2,5]
**Output:** 4
**Explanation:** there are four ways to make up the amount:
5=5
5=2+2+1
5=2+1+1+1
5=1+1+1+1+1

```

**Example 2:**

```

**Input:** amount = 3, coins = [2]
**Output:** 0
**Explanation:** the amount of 3 cannot be made up just with coins of 2.

```

**Example 3:**

```

**Input:** amount = 10, coins = [10]
**Output:** 1

```

 

**Constraints:**

	
- `1 <= coins.length <= 300`

	
- `1 <= coins[i] <= 5000`

	
- All the values of `coins` are **unique**.

	
- `0 <= amount <= 5000`

## Key Idea

Unbounded knapsack counting the number of combinations

## Approach

This is solved with **unbounded-knapsack DP that counts combinations rather than minimizing coins**:

1. Define `dp[i]` as the number of ways to make up amount `i` using the coins considered so far; initialize `dp[0] = 1` (one way to make `0`: use nothing) and all other entries to `0`.
2. Process coins one denomination at a time in the outer loop — this is the key to counting *combinations* (order-independent) instead of *permutations*.
3. For each coin, iterate `i` from `coin` up to `amount` in increasing order, updating `dp[i] += dp[i - coin]`.
4. Because the coin loop is outermost, each way of using a given coin is only counted once regardless of order, avoiding permutation duplicates.
5. After processing all coins, `dp[amount]` holds the total number of distinct combinations.

**Time Complexity:** O(amount * len(coins)) — for each coin, we update every amount from that coin's value up to the target.
**Space Complexity:** O(amount) — for the 1D `dp` array.

## Reference Solution (Python)

```python
def change(amount: int, coins: list[int]) -> int:
    dp = [0] * (amount + 1)
    dp[0] = 1

    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] += dp[i - coin]

    return dp[amount]
```

## Reference

- LeetCode: https://leetcode.com/problems/coin-change-ii/
