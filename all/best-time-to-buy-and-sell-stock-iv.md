# 188. Best Time to Buy and Sell Stock IV

**Difficulty:** Hard
**Topics:** Array, Dynamic Programming
**Common companies:** All big tech
**Category (README):** 12.2 2D DP

## Problem Description

You are given an integer array `prices` where `prices[i]` is the price of a given stock on the `ith` day, and an integer `k`.

Find the maximum profit you can achieve. You may complete at most `k` transactions: i.e. you may buy at most `k` times and sell at most `k` times.

**Note:** You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

 

**Example 1:**

```

**Input:** k = 2, prices = [2,4,1]
**Output:** 2
**Explanation:** Buy on day 1 (price = 2) and sell on day 2 (price = 4), profit = 4-2 = 2.

```

**Example 2:**

```

**Input:** k = 2, prices = [3,2,6,5,0,3]
**Output:** 7
**Explanation:** Buy on day 2 (price = 2) and sell on day 3 (price = 6), profit = 6-2 = 4. Then buy on day 5 (price = 0) and sell on day 6 (price = 3), profit = 3-0 = 3.

```

 

**Constraints:**

	
- `1 <= k <= 100`

	
- `1 <= prices.length <= 1000`

	
- `0 <= prices[i] <= 1000`

## Key Idea

State-machine DP

## Approach

This is solved with **state-machine DP tracking, for each of the `k` allowed transactions, whether we are currently holding a share or holding cash**:

1. Maintain two length-`(k + 1)` arrays: `hold[j]` (max profit after buying for the `j`-th time, currently holding) and `cash[j]` (max profit after selling for the `j`-th time, currently not holding).
2. Initialize `hold[j] = -inf` for all `j` (can't be holding before any transaction) and `cash[j] = 0`.
3. For each price, update `hold[j] = max(hold[j], cash[j - 1] - price)` — either keep holding, or buy using the profit from `j - 1` completed transactions.
4. Then update `cash[j] = max(cash[j], hold[j] + price)` — either keep resting, or sell the share just considered for `hold[j]`.
5. After processing all prices, `cash[k]` holds the best achievable profit using at most `k` transactions.

**Time Complexity:** O(n * k) — for each of the n prices, we update k transaction states.
**Space Complexity:** O(k) — two length-(k + 1) arrays track the hold/cash states.

## Reference Solution (Python)

```python
def maxProfit(k: int, prices: list[int]) -> int:
    if not prices or k == 0:
        return 0

    hold = [float("-inf")] * (k + 1)
    cash = [0] * (k + 1)

    for price in prices:
        for j in range(1, k + 1):
            hold[j] = max(hold[j], cash[j - 1] - price)
            cash[j] = max(cash[j], hold[j] + price)

    return cash[k]
```

## Reference

- LeetCode: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-iv/
