# 309. Best Time to Buy and Sell Stock with Cooldown

**Difficulty:** Medium
**Topics:** Array, Dynamic Programming
**Common companies:** Amazon, Google
**Category (README):** 12.2 2D DP

## Problem Description

You are given an array `prices` where `prices[i]` is the price of a given stock on the `ith` day.

Find the maximum profit you can achieve. You may complete as many transactions as you like (i.e., buy one and sell one share of the stock multiple times) with the following restrictions:

	
- After you sell your stock, you cannot buy stock on the next day (i.e., cooldown one day).

**Note:** You may not engage in multiple transactions simultaneously (i.e., you must sell the stock before you buy again).

 

**Example 1:**

```

**Input:** prices = [1,2,3,0,2]
**Output:** 3
**Explanation:** transactions = [buy, sell, cooldown, buy, sell]

```

**Example 2:**

```

**Input:** prices = [1]
**Output:** 0

```

 

**Constraints:**

	
- `1 <= prices.length <= 5000`

	
- `0 <= prices[i] <= 1000`

## Key Idea

State-machine DP: holding/not-holding/cooldown

## Approach

This is solved with **state-machine DP over three states: holding a share, just sold (must cool down), and resting/free to buy**:

1. Track three running values: `hold` (max profit while currently holding a share), `sold` (max profit on the day right after selling, triggering cooldown), and `rest` (max profit while not holding and free to buy).
2. For each price, compute the new `sold` as `hold + price` — sell whatever share we were holding.
3. Update `hold` as `max(hold, rest - price)` — either keep holding, or buy today using profit accumulated while resting (never from the cooldown-restricted `sold` state).
4. Update `rest` as `max(rest, previous sold)` — resting today is either a continuation of resting, or the day after a cooldown from a sale.
5. After the pass, the answer is `max(sold, rest)`, since ending while still holding a share is never optimal.

**Time Complexity:** O(n) — a single pass through the prices array, updating three running states.
**Space Complexity:** O(1) — only the `hold`, `sold`, and `rest` states are kept.

## Reference Solution (Python)

```python
def maxProfit(prices: list[int]) -> int:
    if not prices:
        return 0

    hold = float("-inf")
    sold = 0
    rest = 0

    for price in prices:
        prev_sold = sold
        sold = hold + price
        hold = max(hold, rest - price)
        rest = max(rest, prev_sold)

    return max(sold, rest)
```

## Reference

- LeetCode: https://leetcode.com/problems/best-time-to-buy-and-sell-stock-with-cooldown/
